# Snowflake-managed MCP or the Cortex Agents REST API: code

Every file in the [Snowflake-managed MCP or the Cortex Agents REST API](/developer-guide/cortex-ai-cookbook/mcp-or-agent-rest-api) recipe. To run the recipe, download [mcp-or-agent-rest-api.zip](/static/samples/cortex-ai-cookbook/mcp-or-agent-rest-api.zip), unzip it, and run the scripts from the `mcp-or-agent-rest-api/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/mcp-or-agent-rest-api); the zip includes it as `README.md`.

## `client/`

### `client/mcp_stream_check.py`

Copy code

```
#!/usr/bin/env python3
"""
Stream diagnostic for a Snowflake-managed MCP server.

Sends one tools/call the way a spec-compliant client does and times every frame
of the Server-Sent Events stream as it arrives. It reports:

  transport          Content-Type, plus the no-buffering headers the server sets
  keep-alives        count of `: keep-alive` comment frames and their interval
  longest gap        the longest silence on the wire, from the request onward,
                     against your proxy's idle timeout
  progress           notifications/progress events received for the progressToken it
                     sends (--no-progress-token sends none, for comparison)
  result             result events, and whether the stream ended with `data: [DONE]`
  request id         x-snowflake-request-id, which joins CORTEX_AGENT_USAGE_HISTORY

Use it to find out why a client times out. If the longest gap is under the idle
timeout of every proxy between the client and Snowflake, keep-alives are doing
their job and a timeout comes from the client's own per-request limit instead.
If progress events arrive, a client that resets its timeout on progress (the MCP
specification allows it) can wait longer than that limit.

Standard library only.

    export SNOWFLAKE_ACCOUNT_URL=https://<account_identifier>.snowflakecomputing.com
    export SNOWFLAKE_TOKEN=<OAuth access token or programmatic access token>
    python client/mcp_stream_check.py
    python client/mcp_stream_check.py --idle-timeout 30 --compare-json
    python client/mcp_stream_check.py --tool revenue_agent --text "Total revenue by region?"

Use hyphens, not underscores, in the account hostname.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

DATABASE = os.environ.get("MCP_DATABASE", "COOKBOOK_MCP_OR_AGENT_REST_API")
SCHEMA = os.environ.get("MCP_SCHEMA", "APP")
SERVER = os.environ.get("MCP_SERVER", "REVENUE_MCP")

SSE_ACCEPT = "application/json, text/event-stream"
PROGRESS_TOKEN = "stream-check-1"

def _url(account_url):
    return f"{account_url.rstrip('/')}/api/v2/databases/{DATABASE}/schemas/{SCHEMA}/mcp-servers/{SERVER}"

def _request(account_url, token, payload, accept):
    return urllib.request.Request(
        _url(account_url),
        data=json.dumps(payload).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": accept,
        },
    )

def _open(request, timeout):
    try:
        return urllib.request.urlopen(request, timeout=timeout)
    except urllib.error.HTTPError as err:
        detail = err.read().decode(errors="replace")[:500]
        sys.exit(f"HTTP {err.code}: {detail}")

def list_tools(account_url, token, timeout):
    """tools/list answers with one JSON body whatever the Accept header says."""
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    with _open(_request(account_url, token, payload, SSE_ACCEPT), timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        raw = response.read().decode()
    if "text/event-stream" in content_type:
        raw = next((ln[5:].strip() for ln in raw.splitlines() if ln.startswith("data:")), "{}")
    tools = (json.loads(raw).get("result") or {}).get("tools") or []
    return tools, content_type

def _text_argument(tool):
    """Name of the argument that carries the question: `text` for agent tools,
    `message` for Cortex Analyst, `query` for Cortex Search."""
    schema = tool.get("inputSchema") or {}
    for name in schema.get("required") or []:
        if name in ("text", "message", "query"):
            return name
    for name in ("text", "message", "query"):
        if name in (schema.get("properties") or {}):
            return name
    return "text"

def stream_call(account_url, token, tool, arguments, accept, timeout, progress_token=True):
    """One tools/call. Reads the body line by line and timestamps every frame."""
    params = {"name": tool, "arguments": arguments}
    if progress_token:
        params["_meta"] = {"progressToken": PROGRESS_TOKEN}
    payload = {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": params}
    report = {
        "accept": accept,
        "progress_token": progress_token,
        "keepalives": [],
        "progress": [],
        "results": 0,
        "done": False,
        "other": [],
        "error": None,
        "result_bytes": 0,
    }
    started = time.monotonic()
    frame_times = []
    with _open(_request(account_url, token, payload, accept), timeout) as response:
        report["headers_s"] = time.monotonic() - started
        report["status"] = response.status
        for name in ("Content-Type", "Cache-Control", "X-Accel-Buffering", "x-snowflake-request-id"):
            report[name] = response.headers.get(name, "")
        streaming = "text/event-stream" in report["Content-Type"]
        if not streaming:
            body = response.read()
            report["first_byte_s"] = time.monotonic() - started
            frame_times.append(report["first_byte_s"])
            report["result_bytes"] = len(body)
            report["results"] = 1
            rpc = json.loads(body or b"{}")
            report["error"] = rpc.get("error")
        else:
            while True:
                line = response.readline()
                if not line:
                    break  # stream closed
                at = time.monotonic() - started
                text = line.decode(errors="replace").rstrip("\r\n")
                if not text:
                    continue  # event separator
                report.setdefault("first_byte_s", at)
                frame_times.append(at)
                if text.startswith(":"):
                    report["keepalives"].append(at)
                elif text.startswith("data:"):
                    _classify(text[5:].strip(), at, report)
                elif not text.startswith(("event:", "id:", "retry:")):
                    report["other"].append(text[:80])
    report["total_s"] = time.monotonic() - started
    report["streaming"] = streaming
    # Measure from the request, not from the headers: a proxy's idle clock starts
    # when the request is sent, and the server sends headers with the first frame.
    edges = [0.0, *frame_times, report["total_s"]]
    report["longest_gap_s"] = max(b - a for a, b in zip(edges, edges[1:]))
    return report

def _classify(data, at, report):
    if data == "[DONE]":
        report["done"] = True
        return
    try:
        message = json.loads(data)
    except json.JSONDecodeError:
        report["other"].append(data[:80])
        return
    if message.get("method") == "notifications/progress":
        report["progress"].append((at, (message.get("params") or {}).get("progress")))
    elif "result" in message or "error" in message:
        report["results"] += 1
        report["result_bytes"] += len(data)
        report["error"] = report["error"] or message.get("error")
    else:
        report["other"].append(data[:80])

def _interval(times):
    if len(times) < 2:
        return "n/a"
    gaps = [b - a for a, b in zip(times, times[1:])]
    return f"every {sum(gaps) / len(gaps):.1f}s (min {min(gaps):.1f}s, max {max(gaps):.1f}s)"

def print_report(report, idle_timeout):
    print(f"\n  Accept             {report['accept']}")
    print(f"  progressToken      {'sent' if report['progress_token'] else 'not sent'}")
    print(f"  HTTP status        {report['status']}")
    print(f"  Content-Type       {report['Content-Type'] or '(none)'}")
    print(f"  Cache-Control      {report['Cache-Control'] or '(none)'}")
    print(f"  X-Accel-Buffering  {report['X-Accel-Buffering'] or '(none)'}")
    print(f"  request id         {report['x-snowflake-request-id'] or '(none)'}")
    print(f"  headers after      {report['headers_s']:6.1f}s")
    print(f"  first byte after   {report.get('first_byte_s', report['total_s']):6.1f}s")
    if report["streaming"]:
        print(f"  keep-alives        {len(report['keepalives'])}, {_interval(report['keepalives'])}")
        print(f"  progress events    {len(report['progress'])}, {_interval([t for t, _ in report['progress']])}")
        print(f"  result events      {report['results']} ({report['result_bytes'] / 1024:.0f} KB)")
        print(f"  ended with [DONE]  {'yes' if report['done'] else 'no, the stream closed'}")
        if report["other"]:
            print(f"  other frames       {len(report['other'])}, first: {report['other'][0]}")
    else:
        print(f"  body               one JSON document ({report['result_bytes'] / 1024:.0f} KB)")
    print(f"  total              {report['total_s']:6.1f}s")
    flag = "  OVER the idle timeout" if report["longest_gap_s"] >= idle_timeout else ""
    print(f"  longest silence    {report['longest_gap_s']:6.1f}s  (idle timeout {idle_timeout:.0f}s){flag}")
    if report["error"]:
        print(f"  JSON-RPC error     {report['error']}")

def verdict(report, idle_timeout, client_deadline):
    """Plain-language reading of one streamed call."""
    lines = []
    if not report["streaming"]:
        lines.append(
            "The server sent one JSON body. Managed MCP streams tools/call by default, so the "
            "Accept header that reached Snowflake did not list text/event-stream. Check the "
            "client and any proxy that rewrites headers."
        )
    elif report["longest_gap_s"] < idle_timeout:
        lines.append(
            f"Keep-alives kept every silence under {idle_timeout:.0f}s, so a proxy with that idle "
            "timeout will not drop this call."
        )
    else:
        lines.append(
            f"A {report['longest_gap_s']:.0f}s silence exceeds the {idle_timeout:.0f}s idle timeout. "
            "Look for a proxy that buffers the response (it would hide keep-alives)."
        )
    if report["total_s"] >= client_deadline:
        lines.append(
            f"The call took {report['total_s']:.0f}s, past the {client_deadline:.0f}s client limit. "
            "Streaming does not deliver the answer earlier. Reset the timeout on progress if your "
            "client supports it, make the agent faster, or split the work into submit and fetch "
            "calls (see the long-running agents over MCP recipe)."
        )
    if report["streaming"] and report["progress_token"]:
        if report["progress"]:
            lines.append(
                f"{len(report['progress'])} progress notifications arrived. A client that resets its "
                "per-request timeout on progress keeps waiting while the tool runs; one that does not "
                "still times out at its own limit."
            )
        else:
            lines.append(
                "No progress notifications arrived for the progressToken. Rely on keep-alives "
                "for idle timeouts and on your client's per-request limit for everything else."
            )
    if report["streaming"] and not report["done"]:
        lines.append("The stream ended on close, without data: [DONE]. End reading on close, not on the sentinel.")
    if report["results"] != 1:
        lines.append(f"Expected one result event, got {report['results']}.")
    return lines

def main():
    parser = argparse.ArgumentParser(description="Time the SSE stream of one managed MCP tools/call.")
    parser.add_argument("--tool", help="tool name; defaults to the first tool the server lists")
    parser.add_argument("--text", default="What was total revenue by region in August 2026?")
    parser.add_argument(
        "--idle-timeout",
        type=float,
        default=float(os.environ.get("MCP_IDLE_TIMEOUT_S", "60")),
        help="shortest idle timeout of any proxy or load balancer on the path (seconds)",
    )
    parser.add_argument(
        "--client-deadline",
        type=float,
        default=float(os.environ.get("MCP_CLIENT_CEILING_S", "120")),
        help="your MCP client's absolute per-call limit (seconds)",
    )
    parser.add_argument(
        "--no-progress-token",
        action="store_true",
        help="omit _meta.progressToken, as a client that does not track progress would",
    )
    parser.add_argument(
        "--compare-json",
        action="store_true",
        help="repeat the call with Accept: application/json to show what a non-streaming client sees",
    )
    parser.add_argument("--timeout", type=float, default=600, help="socket read timeout (seconds)")
    args = parser.parse_args()

    account_url = os.environ.get("SNOWFLAKE_ACCOUNT_URL")
    token = os.environ.get("SNOWFLAKE_TOKEN")
    if not account_url or not token:
        sys.exit("Set SNOWFLAKE_ACCOUNT_URL and SNOWFLAKE_TOKEN.")

    tools, list_type = list_tools(account_url, token, args.timeout)
    if not tools:
        sys.exit("tools/list returned no tools: check USAGE on the server for the session's role.")
    tool = next((t for t in tools if t.get("name") == args.tool), None) if args.tool else tools[0]
    if tool is None:
        sys.exit(f"no tool named {args.tool}; the server lists {[t.get('name') for t in tools]}")
    print(f"\nserver   {DATABASE}.{SCHEMA}.{SERVER}")
    print(f"tools    {[t.get('name') for t in tools]}  (tools/list Content-Type: {list_type})")
    print(f"calling  {tool['name']}")

    arguments = {_text_argument(tool): args.text}
    progress_token = not args.no_progress_token
    report = stream_call(account_url, token, tool["name"], arguments, SSE_ACCEPT, args.timeout, progress_token)
    print_report(report, args.idle_timeout)
    if args.compare_json:
        print("\nsame call, Accept: application/json only")
        json_report = stream_call(
            account_url, token, tool["name"], arguments, "application/json", args.timeout, progress_token
        )
        print_report(json_report, args.idle_timeout)

    print("\nverdict")
    for line in verdict(report, args.idle_timeout, args.client_deadline):
        print(f"  - {line}")
    healthy = (
        report["streaming"]
        and report["results"] == 1
        and report["longest_gap_s"] < args.idle_timeout
        and report["total_s"] < args.client_deadline
    )
    sys.exit(0 if healthy else 1)

if __name__ == "__main__":
    main()
```

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- =============================================================================
-- 01_setup.sql
-- A small governed data product for an external MCP client to reach:
-- roles, warehouse, database, synthetic data, a fail-closed row access policy,
-- a semantic view, and one Cortex Agent with a Cortex Analyst tool.
--
--   *_ADMIN   owns the recipe objects.
--   *_ACCESS  is the MCP access role: the role an MCP user's session runs as.
--             It is entitled to the EMEA region only, which is how Verify shows
--             that row access policies apply through the agent and MCP path.
--
-- ACCOUNTADMIN is used only to create and grant the roles, warehouse, and
-- database. Idempotent: safe to rerun.
-- =============================================================================

SET cookbook_db          = 'COOKBOOK_MCP_OR_AGENT_REST_API';
SET cookbook_schema      = 'COOKBOOK_MCP_OR_AGENT_REST_API.APP';
SET cookbook_wh          = 'COOKBOOK_MCP_OR_AGENT_REST_API_WH';
SET cookbook_admin_role  = 'COOKBOOK_MCP_OR_AGENT_REST_API_ADMIN';
SET cookbook_access_role = 'COOKBOOK_MCP_OR_AGENT_REST_API_ACCESS';
SET me                   = '"' || CURRENT_USER() || '"';

-- ── Account-scoped setup (ACCOUNTADMIN) ─────────────────────────────────────
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($cookbook_admin_role);
CREATE ROLE IF NOT EXISTS IDENTIFIER($cookbook_access_role);
GRANT ROLE IDENTIFIER($cookbook_admin_role)  TO USER IDENTIFIER($me);
GRANT ROLE IDENTIFIER($cookbook_access_role) TO USER IDENTIFIER($me);

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;
CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db);

GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($cookbook_admin_role);
GRANT USAGE, CREATE SCHEMA ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($cookbook_admin_role);
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($cookbook_admin_role);

-- ── Recipe objects (admin role) ─────────────────────────────────────────────
USE ROLE IDENTIFIER($cookbook_admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($cookbook_schema);
USE SCHEMA IDENTIFIER($cookbook_schema);

-- Which role may see which region. Onboarding a population is a row, not DDL.
CREATE OR REPLACE TABLE REGION_ENTITLEMENTS (ROLE_NAME STRING, REGION STRING);
INSERT INTO REGION_ENTITLEMENTS VALUES
  ('COOKBOOK_MCP_OR_AGENT_REST_API_ACCESS', 'EMEA');

-- Synthetic monthly revenue for a fictional company, Northwind.
CREATE OR REPLACE TABLE ORDERS (
  ORDER_MONTH  DATE          COMMENT 'First day of the order month',
  REGION       STRING        COMMENT 'Sales region: AMER, EMEA, or APJ',
  PRODUCT_LINE STRING        COMMENT 'Product line: Hardware, Software, or Services',
  REVENUE_USD  NUMBER(14,2)  COMMENT 'Recognized revenue in US dollars'
);
INSERT INTO ORDERS VALUES
  ('2026-07-01', 'AMER', 'Hardware', 1200000), ('2026-07-01', 'AMER', 'Software', 2100000), ('2026-07-01', 'AMER', 'Services', 600000),
  ('2026-07-01', 'EMEA', 'Hardware',  800000), ('2026-07-01', 'EMEA', 'Software', 1300000), ('2026-07-01', 'EMEA', 'Services', 400000),
  ('2026-07-01', 'APJ',  'Hardware',  500000), ('2026-07-01', 'APJ',  'Software',  700000), ('2026-07-01', 'APJ',  'Services', 200000),
  ('2026-08-01', 'AMER', 'Hardware', 1300000), ('2026-08-01', 'AMER', 'Software', 2200000), ('2026-08-01', 'AMER', 'Services', 650000),
  ('2026-08-01', 'EMEA', 'Hardware',  850000), ('2026-08-01', 'EMEA', 'Software', 1400000), ('2026-08-01', 'EMEA', 'Services', 450000),
  ('2026-08-01', 'APJ',  'Hardware',  550000), ('2026-08-01', 'APJ',  'Software',  750000), ('2026-08-01', 'APJ',  'Services', 250000);

-- Recreating ORDERS above detached the policy, so it can be replaced here.
-- Fail closed: a role with no matching row sees nothing. The admin role sees all
-- rows so it can build and test the semantic view.
CREATE OR REPLACE ROW ACCESS POLICY REGION_RAP AS (REGION_VALUE STRING) RETURNS BOOLEAN ->
  IS_ROLE_IN_SESSION('COOKBOOK_MCP_OR_AGENT_REST_API_ADMIN')
  OR EXISTS (
    SELECT 1 FROM REGION_ENTITLEMENTS e
    WHERE e.ROLE_NAME = CURRENT_ROLE() AND e.REGION = REGION_VALUE
  );

ALTER TABLE ORDERS ADD ROW ACCESS POLICY REGION_RAP ON (REGION);

-- CREATE OR ALTER keeps grants on the semantic view across reruns.
CREATE OR ALTER SEMANTIC VIEW ORDERS_SV
  TABLES (
    orders AS ORDERS PRIMARY KEY (ORDER_MONTH, REGION, PRODUCT_LINE)
      COMMENT = 'Monthly recognized revenue by region and product line'
  )
  FACTS (
    orders.revenue AS REVENUE_USD COMMENT = 'Recognized revenue in US dollars'
  )
  DIMENSIONS (
    orders.order_month  AS ORDER_MONTH  COMMENT = 'First day of the order month',
    orders.region       AS REGION       COMMENT = 'Sales region: AMER, EMEA, or APJ',
    orders.product_line AS PRODUCT_LINE COMMENT = 'Product line: Hardware, Software, or Services'
  )
  METRICS (
    orders.total_revenue AS SUM(orders.revenue) COMMENT = 'Total recognized revenue in US dollars'
  )
  COMMENT = 'Northwind revenue, synthetic data for the managed MCP best-practices recipe';

-- One agent, one Cortex Analyst tool. Add Cortex Search as a second phase.
-- The spec is YAML inside $$ ... $$ and cannot read SQL variables: if you change
-- the names above, change them here too. COMMENT must come before COPY GRANTS.
CREATE OR REPLACE AGENT REVENUE_AGENT
  COMMENT = 'Governed revenue questions over ORDERS_SV'
  COPY GRANTS
  FROM SPECIFICATION $$
models:
  orchestration: auto
instructions:
  orchestration: "Use RevenueAnalyst for every question about revenue, regions, product lines, or months."
  response: "Lead with the number. Format dollars in millions. State the month and region."
tools:
  - tool_spec:
      type: "cortex_analyst_text_to_sql"
      name: "RevenueAnalyst"
      description: "Answers questions about Northwind recognized revenue by month, region, and product line."
tool_resources:
  RevenueAnalyst:
    semantic_view: "COOKBOOK_MCP_OR_AGENT_REST_API.APP.ORDERS_SV"
    execution_environment:
      type: "warehouse"
      warehouse: "COOKBOOK_MCP_OR_AGENT_REST_API_WH"
      query_timeout: 120
$$;

SELECT 'setup complete' AS status;
```

### `sql/02_mcp_server.sql`

Copy code

```
-- =============================================================================
-- 02_mcp_server.sql
-- The MCP server, exposing the agent as one CORTEX_AGENT_RUN tool, and the
-- least-privilege grants for the MCP access role.
--
-- There is no ALTER for an MCP server's specification, so changes go through
-- CREATE OR REPLACE, which drops every grant on the server. The server grant is
-- therefore made in this same script, after the CREATE. Always rerun the whole file.
--
-- USAGE on the server lets the role discover tools (tools/list). Invoking the
-- agent tool also needs USAGE on the agent and privileges on everything the
-- agent's tools read.
-- =============================================================================

SET cookbook_db          = 'COOKBOOK_MCP_OR_AGENT_REST_API';
SET cookbook_schema      = 'COOKBOOK_MCP_OR_AGENT_REST_API.APP';
SET cookbook_wh          = 'COOKBOOK_MCP_OR_AGENT_REST_API_WH';
SET cookbook_admin_role  = 'COOKBOOK_MCP_OR_AGENT_REST_API_ADMIN';
SET cookbook_access_role = 'COOKBOOK_MCP_OR_AGENT_REST_API_ACCESS';

USE ROLE IDENTIFIER($cookbook_admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($cookbook_schema);

-- The client picks a tool from its name and description, so write them to be
-- domain-specific and mutually exclusive with any other tool on the server.
CREATE OR REPLACE MCP SERVER REVENUE_MCP
  FROM SPECIFICATION $$
tools:
  - title: "Northwind revenue agent"
    name: "revenue_agent"
    type: "CORTEX_AGENT_RUN"
    identifier: "COOKBOOK_MCP_OR_AGENT_REST_API.APP.REVENUE_AGENT"
    description: "Governed questions about Northwind recognized revenue by month, region, and product line."
$$;

-- ── Grants for the MCP access role ──────────────────────────────────────────
-- Account-scoped grants (warehouse, database role) need the owner of those
-- objects; run this block as ACCOUNTADMIN or a role that owns them.
USE ROLE ACCOUNTADMIN;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE IDENTIFIER($cookbook_access_role);
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($cookbook_access_role);
GRANT USAGE ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($cookbook_access_role);

USE ROLE IDENTIFIER($cookbook_admin_role);
GRANT USAGE ON SCHEMA IDENTIFIER($cookbook_schema) TO ROLE IDENTIFIER($cookbook_access_role);
-- Reapplied on every run because CREATE OR REPLACE MCP SERVER dropped it.
GRANT USAGE ON MCP SERVER REVENUE_MCP TO ROLE IDENTIFIER($cookbook_access_role);
GRANT USAGE ON AGENT REVENUE_AGENT TO ROLE IDENTIFIER($cookbook_access_role);
-- A semantic view needs SELECT only. The agent's Analyst tool can also query the
-- base table under the caller's role, so grant SELECT on it too. The row access
-- policy still filters every row the caller reads.
GRANT SELECT ON SEMANTIC VIEW ORDERS_SV TO ROLE IDENTIFIER($cookbook_access_role);
GRANT SELECT ON TABLE ORDERS TO ROLE IDENTIFIER($cookbook_access_role);

SHOW GRANTS ON MCP SERVER COOKBOOK_MCP_OR_AGENT_REST_API.APP.REVENUE_MCP;
```

### `sql/03_oauth_integration.sql`

Copy code

```
-- =============================================================================
-- 03_oauth_integration.sql   (ACCOUNT-LEVEL: review before running)
--
-- Snowflake OAuth is the default for managed MCP servers. This creates one
-- confidential OAuth client that every user of the MCP client shares; each user
-- still signs in individually and gets their own token.
--
-- Before running:
--   1. Replace OAUTH_REDIRECT_URI with the exact callback URI your MCP client
--      shows during connector setup. A mismatch fails the consent step.
--   2. Decide which of your users will connect. Their session runs as their
--      DEFAULT_ROLE, so it must be the access role, with a DEFAULT_WAREHOUSE
--      (step 3 below). This script changes no user; step 3 is a template you
--      apply to your own users, and teardown does not undo it.
--
-- To authenticate against your own identity provider instead, create an
-- External OAuth integration and bind it with OAUTH_AUTHORIZATION_SERVER at the
-- account, database, or schema level. See the MCP server docs.
-- =============================================================================

SET cookbook_oauth_integration = 'COOKBOOK_MCP_OR_AGENT_REST_API_OAUTH';

USE ROLE ACCOUNTADMIN;

-- Recommended MCP settings: no secondary roles, and only the MCP access role
-- may be the session role.
CREATE SECURITY INTEGRATION IF NOT EXISTS COOKBOOK_MCP_OR_AGENT_REST_API_OAUTH
  TYPE = OAUTH
  OAUTH_CLIENT = CUSTOM
  ENABLED = TRUE
  OAUTH_CLIENT_TYPE = 'CONFIDENTIAL'
  OAUTH_REDIRECT_URI = 'https://mcp-client.example.com/oauth/callback'
  OAUTH_USE_SECONDARY_ROLES = NONE
  ALLOWED_ROLES_LIST = ('COOKBOOK_MCP_OR_AGENT_REST_API_ACCESS');

-- Client ID and secret to paste into the MCP client. The integration name must
-- be uppercase here.
SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS($cookbook_oauth_integration);

-- 3. Template, not run by this script. For each of your users who will connect
--    (replace <user>), first record the current values, because teardown drops
--    the role and warehouse set below and restores nothing:
--   DESCRIBE USER <user>;   -- note DEFAULT_ROLE and DEFAULT_WAREHOUSE
--   GRANT ROLE COOKBOOK_MCP_OR_AGENT_REST_API_ACCESS TO USER <user>;
--   ALTER USER <user> SET
--     DEFAULT_ROLE      = 'COOKBOOK_MCP_OR_AGENT_REST_API_ACCESS'
--     DEFAULT_WAREHOUSE = 'COOKBOOK_MCP_OR_AGENT_REST_API_WH';
-- Before teardown, put back the values you recorded:
--   ALTER USER <user> SET DEFAULT_ROLE = '<previous role>' DEFAULT_WAREHOUSE = '<previous warehouse>';
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- 99_teardown.sql
-- Removes everything this recipe created. Safe to run twice.
--
-- The security integration is account-level. No script in this recipe changes an
-- existing user's DEFAULT_ROLE or DEFAULT_WAREHOUSE, so this script restores
-- none. If you applied the template in 03_oauth_integration.sql to your own
-- users, restore the values you recorded before running this, because the role
-- and warehouse those settings point at are dropped below.
-- =============================================================================

SET cookbook_db          = 'COOKBOOK_MCP_OR_AGENT_REST_API';
SET cookbook_wh          = 'COOKBOOK_MCP_OR_AGENT_REST_API_WH';
SET cookbook_admin_role  = 'COOKBOOK_MCP_OR_AGENT_REST_API_ADMIN';
SET cookbook_access_role = 'COOKBOOK_MCP_OR_AGENT_REST_API_ACCESS';

USE ROLE ACCOUNTADMIN;

-- For each of your users you changed with the 03 template (you run this, not teardown):
--   ALTER USER <user> SET DEFAULT_ROLE = '<previous role>' DEFAULT_WAREHOUSE = '<previous warehouse>';

DROP SECURITY INTEGRATION IF EXISTS COOKBOOK_MCP_OR_AGENT_REST_API_OAUTH;

-- The database drop removes the MCP server, agent, semantic view, tables, and policy.
DROP DATABASE  IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);
DROP ROLE      IF EXISTS IDENTIFIER($cookbook_access_role);
DROP ROLE      IF EXISTS IDENTIFIER($cookbook_admin_role);

SHOW DATABASES LIKE 'COOKBOOK_MCP_OR_AGENT_REST_API%';
```
