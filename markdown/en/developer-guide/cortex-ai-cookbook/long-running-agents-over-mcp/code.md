# Long-running Cortex Agent runs over managed MCP: code

Every file in the [Long-running Cortex Agent runs over managed MCP](/developer-guide/cortex-ai-cookbook/long-running-agents-over-mcp) recipe. To run the recipe, download [long-running-agents-over-mcp.zip](/static/samples/cortex-ai-cookbook/long-running-agents-over-mcp.zip), unzip it, and run the scripts from the `long-running-agents-over-mcp/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/long-running-agents-over-mcp); the zip includes it as `README.md`.

## `client/`

### `client/submit_fetch_client.py`

Copy code

```
#!/usr/bin/env python3
"""
Submit-and-fetch client for the long-running agents recipe.

Calls the Snowflake-managed MCP server BOOKINGS_ASYNC_MCP directly over HTTP:

    submit_bookings_question(QUESTION) -> {"run_id": ..., "thread_id": ...}   returns in seconds
    fetch_bookings_answer(RUN_ID)      -> {"status": ..., "answer": ...}      waits up to ~60 s

It prints the duration of every tools/call so you can confirm that no single
call approaches your MCP client's ceiling, however long the agent run takes.

Standard library only.

    export SNOWFLAKE_ACCOUNT_URL=https://<account_identifier>.snowflakecomputing.com
    export SNOWFLAKE_TOKEN=<OAuth access token or programmatic access token>
    python client/submit_fetch_client.py "What were total new bookings in FY26-Q4?"
    python client/submit_fetch_client.py --slow "What were total new bookings in FY26-Q4?"

Use hyphens, not underscores, in the account hostname.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

DATABASE = os.environ.get("MCP_DATABASE", "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP")
SCHEMA = os.environ.get("MCP_SCHEMA", "APP")
SERVER = os.environ.get("MCP_SERVER", "BOOKINGS_ASYNC_MCP")

# The ceiling you are designing under. Set it to your MCP client's limit.
CLIENT_CEILING_S = float(os.environ.get("MCP_CLIENT_CEILING_S", "120"))
# Stop polling after this long. Background runs can last up to six hours.
POLL_TIMEOUT_S = float(os.environ.get("MCP_POLL_TIMEOUT_S", "1800"))
# Per-request socket timeout. Must exceed the fetch tool's server-side wait.
HTTP_TIMEOUT_S = 150

class McpError(RuntimeError):
    pass

def _url(account_url):
    return f"{account_url.rstrip('/')}/api/v2/databases/{DATABASE}/schemas/{SCHEMA}/mcp-servers/{SERVER}"

def call_tool(account_url, token, tool, arguments, rpc_id):
    """One MCP tools/call. Returns (tool_payload, elapsed_seconds, content_type)."""
    body = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "method": "tools/call",
            "params": {"name": tool, "arguments": arguments},
        }
    ).encode()
    request = urllib.request.Request(
        _url(account_url),
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            # Required: the server answers tools/call as a Server-Sent Events stream.
            "Accept": "application/json, text/event-stream",
        },
    )

    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_S) as response:
            content_type = response.headers.get("Content-Type", "")
            raw = response.read().decode()
    except urllib.error.HTTPError as err:
        detail = err.read().decode(errors="replace")[:500]
        if err.code == 401:
            # The server returns 401 when the request carries no valid token. The
            # response's WWW-Authenticate header points OAuth clients at the
            # protected resource metadata so they can sign in again.
            raise McpError(
                f"HTTP 401: not authenticated. The token is missing, expired, or invalid; obtain a new one. {detail}"
            ) from err
        raise McpError(f"HTTP {err.code}: {detail}") from err
    elapsed = time.monotonic() - started

    rpc = _parse_rpc(raw, content_type)
    if rpc is None:
        raise McpError(f"could not parse response: {raw[:500]}")
    if rpc.get("error"):
        raise McpError(f"JSON-RPC error: {rpc['error']}")
    return _tool_payload(rpc), elapsed, content_type

def _parse_rpc(raw, content_type):
    """Accept a JSON body or an SSE stream.

    A tools/call stream carries the JSON-RPC result in `data:` events. The docs say
    it closes with `data: [DONE]`; in testing it closed without one after a single
    result event. Take the last JSON event and stop at [DONE] if it ever appears.
    """
    if "text/event-stream" not in content_type:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    last = None
    for line in raw.splitlines():
        if not line.startswith("data:"):
            continue  # comment and blank lines
        data = line[5:].strip()
        if data == "[DONE]":
            break
        try:
            last = json.loads(data)
        except json.JSONDecodeError:
            continue
    return last

def _tool_payload(rpc):
    """Procedure tools return a JSON string in result.content[].text."""
    for block in (rpc.get("result") or {}).get("content") or []:
        if isinstance(block, dict) and block.get("type") == "text":
            try:
                return json.loads(block["text"])
            except (json.JSONDecodeError, TypeError):
                return {"raw": block.get("text")}
    return rpc.get("result")

def run(account_url, token, question, slow=False):
    submit_tool = "submit_bookings_question_slow" if slow else "submit_bookings_question"
    durations = []
    wall_start = time.monotonic()

    payload, elapsed, ctype = call_tool(account_url, token, submit_tool, {"QUESTION": question}, 1)
    durations.append(elapsed)
    print(f"  submit             {elapsed:6.1f}s  transport={'SSE' if 'event-stream' in ctype else 'JSON'}")
    if (payload or {}).get("status") == "FAILED":
        raise McpError(f"submit failed: {payload.get('error')}")
    run_id = (payload or {}).get("run_id")
    if not run_id:
        raise McpError(f"no run_id in submit response: {payload}")
    print(f"  run_id             {run_id}")
    print(f"  thread_id          {payload.get('thread_id')}")

    rpc_id = 1
    while time.monotonic() - wall_start < POLL_TIMEOUT_S:
        rpc_id += 1
        # No client-side sleep: the fetch tool already waits server-side.
        payload, elapsed, _ = call_tool(account_url, token, "fetch_bookings_answer", {"RUN_ID": run_id}, rpc_id)
        durations.append(elapsed)
        status = (payload or {}).get("status")
        print(f"  fetch {rpc_id - 1:>2}           {elapsed:6.1f}s  status={status}")
        if status == "SUCCEEDED":
            return payload, durations, time.monotonic() - wall_start
        if status in ("FAILED", "NOT_FOUND"):
            raise McpError(f"run {status}: {payload.get('error')}")
    raise McpError(f"run {run_id} did not finish within {POLL_TIMEOUT_S:.0f}s")

def main():
    parser = argparse.ArgumentParser(description="Submit a question and fetch the answer over managed MCP.")
    parser.add_argument("question", nargs="?", default="What were total new bookings in FY26-Q4?")
    parser.add_argument("--slow", action="store_true", help="use the test agent that runs for over two minutes")
    args = parser.parse_args()

    account_url = os.environ.get("SNOWFLAKE_ACCOUNT_URL")
    token = os.environ.get("SNOWFLAKE_TOKEN")
    if not account_url or not token:
        sys.exit("Set SNOWFLAKE_ACCOUNT_URL and SNOWFLAKE_TOKEN.")

    print(f"\nquestion: {args.question}\n")
    try:
        result, durations, wall = run(account_url, token, args.question, slow=args.slow)
    except McpError as err:
        sys.exit(f"\nFAILED: {err}")

    longest = max(durations)
    print(f"\n  MCP calls          {len(durations)}")
    print(f"  longest call       {longest:.1f}s  (ceiling {CLIENT_CEILING_S:.0f}s)")
    print(f"  total wall time    {wall:.1f}s")
    print(f"  thread_id          {result.get('thread_id')}")
    print(f"  assistant_msg_id   {result.get('assistant_message_id')}")
    print(f"\n--- answer ---\n{result.get('answer')}\n")
    sys.exit(1 if longest > CLIENT_CEILING_S else 0)

if __name__ == "__main__":
    main()
```

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- =============================================================================
-- 01_setup.sql
-- Roles, warehouse, database, synthetic bookings data, and a semantic view.
--
-- Two roles:
--   *_ADMIN  owns every object in the recipe schema (agent, procedures, server).
--   *_USER   is the role an MCP client connects as. Least privilege: it gets
--            USAGE on the server, the tool procedures, and the agent, plus
--            SELECT on the semantic view and its base table. Nothing else.
--
-- ACCOUNTADMIN is used only to create the roles, warehouse, and database and to
-- grant them. Everything after that runs as the admin role.
-- Idempotent: safe to rerun.
-- =============================================================================

SET cookbook_db         = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP';
SET cookbook_schema     = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP';
SET cookbook_wh         = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_WH';
SET cookbook_admin_role = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_ADMIN';
SET cookbook_user_role  = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_USER';
SET me                  = '"' || CURRENT_USER() || '"';

-- ── Account-scoped setup (ACCOUNTADMIN) ─────────────────────────────────────
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($cookbook_admin_role);
CREATE ROLE IF NOT EXISTS IDENTIFIER($cookbook_user_role);
GRANT ROLE IDENTIFIER($cookbook_admin_role) TO USER IDENTIFIER($me);
GRANT ROLE IDENTIFIER($cookbook_user_role)  TO USER IDENTIFIER($me);

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;
CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db);

GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($cookbook_admin_role);
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($cookbook_user_role);
GRANT USAGE, CREATE SCHEMA ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($cookbook_admin_role);
GRANT USAGE ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($cookbook_user_role);

-- CORTEX_AGENT_USER is enough to run agents and read threads.
-- CORTEX_USER (a superset) is granted to the admin so it can also build them.
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER       TO ROLE IDENTIFIER($cookbook_admin_role);
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE IDENTIFIER($cookbook_user_role);

-- ── Recipe objects (admin role) ─────────────────────────────────────────────
USE ROLE IDENTIFIER($cookbook_admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($cookbook_schema);
USE SCHEMA IDENTIFIER($cookbook_schema);

-- Synthetic quarterly bookings for a fictional company, Northwind.
CREATE OR REPLACE TABLE BOOKINGS (
  FISCAL_QUARTER   STRING  COMMENT 'Fiscal quarter, for example FY26-Q2',
  REGION           STRING  COMMENT 'Sales region: AMER, EMEA, or APJ',
  NEW_BOOKINGS_USD NUMBER(14,2) COMMENT 'New bookings in US dollars',
  TARGET_USD       NUMBER(14,2) COMMENT 'Bookings target in US dollars'
);

INSERT INTO BOOKINGS VALUES
  ('FY26-Q1', 'AMER', 41200000, 40000000), ('FY26-Q1', 'EMEA', 22800000, 24000000), ('FY26-Q1', 'APJ', 9700000, 9000000),
  ('FY26-Q2', 'AMER', 44900000, 42000000), ('FY26-Q2', 'EMEA', 25100000, 25000000), ('FY26-Q2', 'APJ', 10400000, 10000000),
  ('FY26-Q3', 'AMER', 43300000, 45000000), ('FY26-Q3', 'EMEA', 26700000, 26000000), ('FY26-Q3', 'APJ', 11900000, 11000000),
  ('FY26-Q4', 'AMER', 52600000, 48000000), ('FY26-Q4', 'EMEA', 29800000, 28000000), ('FY26-Q4', 'APJ', 13100000, 12500000);

-- CREATE OR ALTER keeps grants on the semantic view across reruns.
CREATE OR ALTER SEMANTIC VIEW BOOKINGS_SV
  TABLES (
    bookings AS BOOKINGS PRIMARY KEY (FISCAL_QUARTER, REGION)
      COMMENT = 'Quarterly new bookings and targets by region'
  )
  FACTS (
    bookings.new_bookings AS NEW_BOOKINGS_USD COMMENT = 'New bookings in US dollars',
    bookings.target       AS TARGET_USD       COMMENT = 'Bookings target in US dollars'
  )
  DIMENSIONS (
    bookings.fiscal_quarter AS FISCAL_QUARTER COMMENT = 'Fiscal quarter, formatted FY26-Q1',
    bookings.region         AS REGION         COMMENT = 'Sales region: AMER, EMEA, or APJ'
  )
  METRICS (
    bookings.total_new_bookings AS SUM(bookings.new_bookings) COMMENT = 'Total new bookings in US dollars',
    bookings.total_target       AS SUM(bookings.target)       COMMENT = 'Total bookings target in US dollars'
  )
  COMMENT = 'Northwind bookings, synthetic data for the long-running agents recipe';

-- The semantic view itself needs SELECT only (not REFERENCES). The agent's
-- Analyst tool can also generate SQL against the base table, so the caller role
-- needs SELECT on the table too; without it those queries fail under caller's rights.
GRANT USAGE ON SCHEMA IDENTIFIER($cookbook_schema) TO ROLE IDENTIFIER($cookbook_user_role);
GRANT SELECT ON SEMANTIC VIEW BOOKINGS_SV TO ROLE IDENTIFIER($cookbook_user_role);
GRANT SELECT ON TABLE BOOKINGS TO ROLE IDENTIFIER($cookbook_user_role);

SELECT 'setup complete' AS status;
```

### `sql/02_agent.sql`

Copy code

```
-- =============================================================================
-- 02_agent.sql
-- The Cortex Agent that answers bookings questions over the semantic view.
--
-- CREATE OR REPLACE AGENT ... COPY GRANTS keeps the USAGE grant on reruns.
-- Plain CREATE OR REPLACE AGENT would drop it.
--
-- The agent specification is YAML inside $$ ... $$, so it cannot read SQL
-- variables. Object names are fixed, so the semantic view and warehouse names
-- below match the SET blocks. The orchestration model is `auto`; change it in
-- the spec if you need to pin one.
-- =============================================================================

SET cookbook_schema     = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP';
SET cookbook_wh         = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_WH';
SET cookbook_admin_role = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_ADMIN';
SET cookbook_user_role  = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_USER';

USE ROLE IDENTIFIER($cookbook_admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($cookbook_schema);

-- COMMENT has to come before COPY GRANTS; the other order fails to parse. This
-- differs from the published CREATE AGENT syntax, which lists COPY GRANTS first.
CREATE OR REPLACE AGENT BOOKINGS_AGENT
  COMMENT = 'Answers Northwind bookings questions from BOOKINGS_SV'
  COPY GRANTS
  FROM SPECIFICATION $$
models:
  orchestration: auto
orchestration:
  budget:
    seconds: 300
    tokens: 100000
instructions:
  orchestration: "Use BookingsAnalyst for every question about bookings, targets, fiscal quarters, or regions."
  response: "Lead with the number. Format dollars in millions. Always state the fiscal quarter and region."
  sample_questions:
    - question: "What were total new bookings in FY26-Q4?"
    - question: "Which region beat its target by the most in FY26-Q2?"
tools:
  - tool_spec:
      type: "cortex_analyst_text_to_sql"
      name: "BookingsAnalyst"
      description: "Answers questions about Northwind new bookings and bookings targets by fiscal quarter and region."
tool_resources:
  BookingsAnalyst:
    semantic_view: "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP.BOOKINGS_SV"
    execution_environment:
      type: "warehouse"
      warehouse: "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_WH"
      query_timeout: 120
$$;

GRANT USAGE ON AGENT BOOKINGS_AGENT TO ROLE IDENTIFIER($cookbook_user_role);

SHOW AGENTS IN SCHEMA COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP;
```

### `sql/03_run_procs.sql`

Copy code

```
-- =============================================================================
-- 03_run_procs.sql
-- Submit and fetch procedures for background agent runs. All EXECUTE AS CALLER:
-- the agent run and the thread read both happen under the identity and role of
-- whoever called the MCP tool, so row access and masking policies on the data
-- the agent reads still apply per user.
--
--   START_AGENT_RUN(question, agent, thread_id, parent_message_id)
--       Internal. Starts a background run with DATA_AGENT_RUN and returns at once.
--   FETCH_AGENT_RUN(run_id)
--       Long-polls THREAD_MESSAGES for up to BLOCK_SECONDS, then returns
--       SUCCEEDED (with the answer), FAILED, RUNNING, or NOT_FOUND.
--   SUBMIT_BOOKINGS_QUESTION(question)
--       Thin wrapper exposed as the MCP submit tool. Names the agent so the
--       client never chooses which agent runs.
--
-- The procedures are Python so the agent name and request body are passed to
-- DATA_AGENT_RUN as bind parameters; nothing is concatenated into SQL.
-- =============================================================================

SET cookbook_schema     = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP';
SET cookbook_wh         = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_WH';
SET cookbook_admin_role = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_ADMIN';
SET cookbook_user_role  = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_USER';

USE ROLE IDENTIFIER($cookbook_admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($cookbook_schema);

-- ── Start a background run ─────────────────────────────────────────────────
CREATE OR REPLACE PROCEDURE START_AGENT_RUN(
    QUESTION STRING,
    AGENT_NAME STRING,
    THREAD_ID NUMBER,
    PARENT_MESSAGE_ID NUMBER
)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.11'
  PACKAGES = ('snowflake-snowpark-python')
  HANDLER = 'run'
  EXECUTE AS CALLER
AS
$$
import json

def run(session, question, agent_name, thread_id, parent_message_id):
    if not question or not question.strip():
        return json.dumps({"status": "FAILED", "error": "QUESTION is empty."})

    body = {
        "background": True,
        "messages": [{"role": "user", "content": [{"type": "text", "text": question}]}],
    }
    # Continue an existing thread when the caller passes one. parent_message_id
    # must be the assistant message the new question follows.
    create_thread = thread_id is None
    if not create_thread:
        body["thread_id"] = int(thread_id)
        body["parent_message_id"] = int(parent_message_id or 0)

    raw = session.sql(
        "SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(?, ?, ?) AS RESP",
        params=[agent_name, json.dumps(body), create_thread],
    ).collect()[0]["RESP"]

    try:
        resp = json.loads(raw)
    except (TypeError, ValueError):
        return json.dumps({"status": "FAILED", "error": str(raw)[:2000]})

    meta = resp.get("metadata") or {}
    run_id = meta.get("run_id")
    user_message_id = meta.get("user_message_id")
    if not run_id or user_message_id is None:
        # DATA_AGENT_RUN reports errors (for example 399513, no access to the
        # agent) in the payload rather than raising.
        return json.dumps({"status": "FAILED", "error": resp.get("message") or str(raw)[:2000],
                           "code": resp.get("code")})

    # The background response carries run_id and user_message_id. Use a
    # thread_id from the response when present; otherwise take it from the
    # run_id, which has the form <thread_id>-<user_message_id>.
    resolved_thread = meta.get("thread_id") or body.get("thread_id")
    if resolved_thread is None:
        prefix, _, suffix = str(run_id).rpartition("-")
        if suffix == str(user_message_id) and prefix.isdigit():
            resolved_thread = int(prefix)
    if resolved_thread is None:
        return json.dumps({"status": "FAILED", "run_id": run_id,
                           "error": "Could not determine thread_id for this run."})

    return json.dumps({
        "status": "RUNNING",
        "run_id": f"{int(resolved_thread)}-{int(user_message_id)}",
        "agent_run_id": run_id,
        "thread_id": int(resolved_thread),
        "user_message_id": int(user_message_id),
        "next_step": "The answer is not ready yet. Call the fetch tool now with this exact run_id.",
    })
$$;

-- ── Fetch, with a bounded server-side wait ──────────────────────────────────
CREATE OR REPLACE PROCEDURE FETCH_AGENT_RUN(RUN_ID STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.11'
  PACKAGES = ('snowflake-snowpark-python')
  HANDLER = 'run'
  EXECUTE AS CALLER
AS
$$
import json, time

# Keep BLOCK_SECONDS well under the MCP client's per-call ceiling, and keep the
# MCP tool's query_timeout above it. Each pass issues a query, so a call lasts
# somewhat longer than BLOCK_SECONDS.
BLOCK_SECONDS = 60
TICK_SECONDS = 5
FAILED_STATES = {"error", "failed", "cancelled", "canceled"}

def _reply(session, thread_id, user_message_id):
    """The assistant message whose parent is this run's user message, or None.

    Match on parent_id. Do not rely on message_id ordering.
    """
    raw = session.sql("SELECT SNOWFLAKE.CORTEX.THREAD_MESSAGES(?) AS M", params=[thread_id]).collect()[0]["M"]
    for msg in (json.loads(raw) or {}).get("messages", []):
        if msg.get("role") == "assistant" and int(msg.get("parent_id") or -1) == user_message_id:
            return msg
    return None

def _payload(msg):
    payload = msg.get("message_payload")
    return json.loads(payload) if isinstance(payload, str) else (payload or {})

def run(session, run_id):
    try:
        thread_part, msg_part = str(run_id).strip().rsplit("-", 1)
        thread_id, user_message_id = int(thread_part), int(msg_part)
    except (AttributeError, ValueError):
        return json.dumps({"run_id": run_id, "status": "NOT_FOUND",
                           "error": "run_id must look like <thread_id>-<user_message_id>."})

    waited = 0
    while True:
        try:
            msg = _reply(session, thread_id, user_message_id)
        except Exception as exc:  # unknown thread, or no access to it
            return json.dumps({"run_id": run_id, "status": "NOT_FOUND", "error": str(exc)[:500]})

        if msg is not None:
            payload = _payload(msg)
            status = str(payload.get("status") or "").lower()
            base = {"run_id": run_id, "thread_id": thread_id,
                    "assistant_message_id": msg.get("message_id"), "waited_seconds": waited}
            if status in FAILED_STATES:
                err = payload.get("error") or msg.get("error") or {}
                return json.dumps({**base, "status": "FAILED",
                                   "error": err.get("message") if isinstance(err, dict) else str(err)})
            text = "\n\n".join(c.get("text", "").strip() for c in payload.get("content", [])
                               if c.get("type") == "text" and c.get("text", "").strip())
            # A written assistant message with status "completed" is the answer.
            # Any other non-failed status means the run is still going.
            if status == "completed" or (not status and text):
                return json.dumps({**base, "status": "SUCCEEDED", "answer": text})

        if waited >= BLOCK_SECONDS:
            return json.dumps({
                "run_id": run_id, "thread_id": thread_id, "status": "RUNNING", "waited_seconds": waited,
                "next_step": "Still running. Call the fetch tool again now with the same run_id. "
                             "Do not stop while status is RUNNING; long questions can take several minutes.",
            })
        time.sleep(TICK_SECONDS)
        waited += TICK_SECONDS
$$;

-- ── One wrapper per agent, so the MCP submit tool takes only a question ─────
CREATE OR REPLACE PROCEDURE SUBMIT_BOOKINGS_QUESTION(QUESTION STRING)
  RETURNS STRING
  LANGUAGE SQL
  EXECUTE AS CALLER
AS
$$
DECLARE
  res STRING;
BEGIN
  -- NULL thread and parent: start a new thread. Typed NULLs match the NUMBER parameters.
  CALL COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP.START_AGENT_RUN(
    :QUESTION, 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP.BOOKINGS_AGENT', NULL::NUMBER, NULL::NUMBER) INTO :res;
  RETURN :res;
END;
$$;

-- Caller's rights: the MCP user role needs USAGE on the wrapper AND on the
-- procedures it calls.
GRANT USAGE ON PROCEDURE START_AGENT_RUN(STRING, STRING, NUMBER, NUMBER) TO ROLE IDENTIFIER($cookbook_user_role);
GRANT USAGE ON PROCEDURE FETCH_AGENT_RUN(STRING)                         TO ROLE IDENTIFIER($cookbook_user_role);
GRANT USAGE ON PROCEDURE SUBMIT_BOOKINGS_QUESTION(STRING)                TO ROLE IDENTIFIER($cookbook_user_role);

SHOW USER PROCEDURES IN SCHEMA COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP;
```

### `sql/04_slow_test_agent.sql`

Copy code

```
-- =============================================================================
-- 04_slow_test_agent.sql   (TEST ONLY: skip in production)
--
-- A copy of the bookings agent that must call a slow checkpoint tool twice
-- before it answers, so a run reliably lasts well over two minutes. Use it to
-- prove that submit/fetch keeps every call short no matter how long the run is.
--
-- SLOW_CHECKPOINT caps each wait at 90 seconds so a single tool call stays
-- inside the tool's query_timeout.
-- =============================================================================

SET cookbook_schema     = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP';
SET cookbook_wh         = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_WH';
SET cookbook_admin_role = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_ADMIN';
SET cookbook_user_role  = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_USER';

USE ROLE IDENTIFIER($cookbook_admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($cookbook_schema);

CREATE OR REPLACE PROCEDURE SLOW_CHECKPOINT(SECONDS FLOAT)
  RETURNS STRING
  LANGUAGE SQL
  EXECUTE AS CALLER
AS
$$
DECLARE
  s FLOAT;
BEGIN
  s := LEAST(GREATEST(COALESCE(:SECONDS, 0), 0), 90);
  CALL SYSTEM$WAIT(:s, 'SECONDS');
  RETURN 'Checkpoint complete after ' || :s || ' seconds. Continue with the analysis.';
END;
$$;

CREATE OR REPLACE AGENT BOOKINGS_AGENT_SLOW_TEST
  COMMENT = 'Test only: bookings agent with a deliberately slow checkpoint tool'
  COPY GRANTS
  FROM SPECIFICATION $$
models:
  orchestration: auto
orchestration:
  budget:
    seconds: 600
    tokens: 100000
instructions:
  orchestration: |
    Before answering anything, call DataRefreshCheckpoint with seconds=70, wait for
    the result, then call it a second time with seconds=70. Call it twice in sequence,
    never in parallel. Only after both calls return, use BookingsAnalyst to answer.
  response: "Lead with the number. Format dollars in millions. Always state the fiscal quarter and region."
tools:
  - tool_spec:
      type: "cortex_analyst_text_to_sql"
      name: "BookingsAnalyst"
      description: "Answers questions about Northwind new bookings and bookings targets by fiscal quarter and region."
  - tool_spec:
      type: "generic"
      name: "DataRefreshCheckpoint"
      description: "Mandatory data freshness checkpoint. Call it twice, in sequence, with seconds=70 before any analysis."
      input_schema:
        type: "object"
        properties:
          seconds:
            type: "number"
            description: "How long the checkpoint takes. Always pass 70."
        required: ["seconds"]
tool_resources:
  BookingsAnalyst:
    semantic_view: "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP.BOOKINGS_SV"
    execution_environment:
      type: "warehouse"
      warehouse: "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_WH"
      query_timeout: 120
  DataRefreshCheckpoint:
    type: "procedure"
    identifier: "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP.SLOW_CHECKPOINT"
    execution_environment:
      type: "warehouse"
      warehouse: "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_WH"
      query_timeout: 120
$$;

CREATE OR REPLACE PROCEDURE SUBMIT_BOOKINGS_QUESTION_SLOW(QUESTION STRING)
  RETURNS STRING
  LANGUAGE SQL
  EXECUTE AS CALLER
AS
$$
DECLARE
  res STRING;
BEGIN
  CALL COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP.START_AGENT_RUN(
    :QUESTION, 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP.BOOKINGS_AGENT_SLOW_TEST', NULL::NUMBER, NULL::NUMBER) INTO :res;
  RETURN :res;
END;
$$;

-- The agent runs as the caller, so the caller also needs the checkpoint tool.
GRANT USAGE ON AGENT BOOKINGS_AGENT_SLOW_TEST                TO ROLE IDENTIFIER($cookbook_user_role);
GRANT USAGE ON PROCEDURE SLOW_CHECKPOINT(FLOAT)               TO ROLE IDENTIFIER($cookbook_user_role);
GRANT USAGE ON PROCEDURE SUBMIT_BOOKINGS_QUESTION_SLOW(STRING) TO ROLE IDENTIFIER($cookbook_user_role);
```

### `sql/05_mcp_server.sql`

Copy code

```
-- =============================================================================
-- 05_mcp_server.sql
-- The Snowflake-managed MCP server that exposes submit and fetch as tools.
--
-- There is no ALTER to change an MCP server's specification, so this script
-- uses CREATE OR REPLACE. Replacing the server drops every grant on it, so the
-- USAGE grant is reapplied at the end of the script. Always rerun the whole file.
--
-- The tool descriptions are the only instructions the client's model sees about
-- how the two tools relate. Keep all four points when you adapt them:
--   1. what the submit tool is for, in business terms
--   2. submit returns immediately with a run_id, not the answer
--   3. the client must keep calling fetch while status is RUNNING
--   4. fetch waits up to 60 seconds and is safe to call repeatedly
--
-- query_timeout on the fetch tool must exceed BLOCK_SECONDS in FETCH_AGENT_RUN.
--
-- submit_bookings_question_slow calls the procedure from 04_slow_test_agent.sql.
-- If you skipped 04 (production), delete that tool from the spec below.
-- =============================================================================

SET cookbook_schema     = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP';
SET cookbook_wh         = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_WH';
SET cookbook_admin_role = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_ADMIN';
SET cookbook_user_role  = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_USER';

USE ROLE IDENTIFIER($cookbook_admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($cookbook_schema);

CREATE OR REPLACE MCP SERVER BOOKINGS_ASYNC_MCP
  FROM SPECIFICATION $$
tools:
  - title: "Submit bookings question"
    name: "submit_bookings_question"
    identifier: "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP.SUBMIT_BOOKINGS_QUESTION"
    type: "GENERIC"
    description: >
      Start a question about Northwind new bookings and bookings targets by fiscal
      quarter and region. Returns IMMEDIATELY with a run_id; it does NOT return the
      answer. After calling this tool you MUST call fetch_bookings_answer with the
      returned run_id, and keep calling it until status is SUCCEEDED or FAILED.
    config:
      type: "procedure"
      warehouse: "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_WH"
      query_timeout: 60
      input_schema:
        type: "object"
        properties:
          QUESTION:
            description: "The user's bookings question, verbatim."
            type: "string"
        required: ["QUESTION"]
  - title: "Submit bookings question (slow test agent)"
    name: "submit_bookings_question_slow"
    identifier: "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP.SUBMIT_BOOKINGS_QUESTION_SLOW"
    type: "GENERIC"
    description: >
      Test only. Same contract as submit_bookings_question, but routes to an agent
      that deliberately takes more than two minutes. Returns a run_id immediately;
      then call fetch_bookings_answer until status is SUCCEEDED or FAILED.
    config:
      type: "procedure"
      warehouse: "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_WH"
      query_timeout: 60
      input_schema:
        type: "object"
        properties:
          QUESTION:
            description: "The user's bookings question, verbatim."
            type: "string"
        required: ["QUESTION"]
  - title: "Fetch bookings answer"
    name: "fetch_bookings_answer"
    identifier: "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP.FETCH_AGENT_RUN"
    type: "GENERIC"
    description: >
      Retrieve the answer to a submitted bookings question. This tool WAITS up to
      60 seconds for the run to finish before it responds, so it is safe to call
      repeatedly. Returns status RUNNING, SUCCEEDED, FAILED, or NOT_FOUND. If status
      is RUNNING, call this tool again IMMEDIATELY with the SAME run_id; do not give
      up, because long questions can take several minutes. On SUCCEEDED the answer
      field holds the result, and thread_id identifies the conversation.
    config:
      type: "procedure"
      warehouse: "COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_WH"
      query_timeout: 110
      input_schema:
        type: "object"
        properties:
          RUN_ID:
            description: "The run_id returned by a submit tool."
            type: "string"
        required: ["RUN_ID"]
$$;

-- CREATE OR REPLACE dropped any previous grant on the server. Reapply it.
-- USAGE on the server lets the role list tools; invoking them also needs the
-- procedure, agent, and data grants made in the earlier scripts.
GRANT USAGE ON MCP SERVER BOOKINGS_ASYNC_MCP TO ROLE IDENTIFIER($cookbook_user_role);

SHOW MCP SERVERS IN SCHEMA COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP.APP;
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- 99_teardown.sql
-- Removes everything this recipe created. Safe to run twice.
--
-- DROP DATABASE removes the schema, table, semantic view, agents, procedures,
-- and MCP server. Threads created by agent runs are Cortex objects this recipe
-- never owns; there is nothing else to unwind (no tasks, streams, or tables of
-- run state). No account-level settings were changed.
-- =============================================================================

SET cookbook_db         = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP';
SET cookbook_wh         = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_WH';
SET cookbook_admin_role = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_ADMIN';
SET cookbook_user_role  = 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_USER';

USE ROLE ACCOUNTADMIN;

DROP DATABASE  IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);
DROP ROLE      IF EXISTS IDENTIFIER($cookbook_user_role);
DROP ROLE      IF EXISTS IDENTIFIER($cookbook_admin_role);

-- If you created a programmatic access token for the sample client, remove it:
--   ALTER USER <your_user> REMOVE PROGRAMMATIC ACCESS TOKEN COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP_PAT;

SHOW DATABASES LIKE 'COOKBOOK_LONG_RUNNING_AGENTS_OVER_MCP%';
```
