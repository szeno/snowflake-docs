# LangChain agents on Cortex AI Gateway with MCP tools and traces: code

Every file in the [LangChain agents on Cortex AI Gateway with MCP tools and traces](/developer-guide/cortex-ai-cookbook/langchain-mcp-agent-tracing) recipe. To run the recipe, download [langchain-mcp-agent-tracing.zip](/static/samples/cortex-ai-cookbook/langchain-mcp-agent-tracing.zip), unzip it, and run the scripts from the `langchain-mcp-agent-tracing/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/langchain-mcp-agent-tracing); the zip includes it as `README.md`.

## `app/`

### `app/requirements.txt`

```
# Trace analyzer (app/streamlit_app.py), run locally.
streamlit==1.50.0
snowflake-snowpark-python==1.40.0
snowflake-connector-python==3.18.1
pandas==2.3.3
pyarrow==21.0.0
```

### `app/streamlit_app.py`

Copy code

```
"""Trace analyzer for the recipe's external agents.

Reads AGENT_TRACE_TABLE('SNOWFLAKE') and the recipe's cost view as the ANALYST
role (MONITOR on the gateway and no USAGE of its own). Every query is scoped to
the recipe's service user and conversation-id prefix and takes user input only
as bind parameters. Values that come from traces (model names, prompts,
responses) are untrusted: they are rendered in dataframes, st.code, or through
esc().

Run locally:
    SNOWFLAKE_DEFAULT_CONNECTION_NAME=<your connection> streamlit run streamlit_app.py
"""

from __future__ import annotations

import html
import re

import pandas as pd
import streamlit as st
from snowflake.snowpark import Session

ANALYST_ROLE = "COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_ANALYST"
WAREHOUSE = "COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_WH"
SVC_USER = "COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_SVC"
CONV_PREFIX = "cookbook-lcmcp-"
COST_VIEW = "COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING.OBS.AGENT_GATEWAY_COST"
LOOKBACK_HOURS = {"Last hour": 1, "Last 24 hours": 24, "Last 7 days": 168}

st.set_page_config(page_title="Gateway agent traces", layout="wide")

_MD_SPECIAL = re.compile(r"([\\`*_{}\[\]()#+\-.!|>~])")

def esc(value) -> str:
    """HTML-escape, then backslash-escape Markdown, for text shown via st.markdown."""
    return _MD_SPECIAL.sub(r"\\\1", html.escape(str(value), quote=False))

@st.cache_resource
def get_session() -> Session:
    try:
        from snowflake.snowpark.context import get_active_session

        session = get_active_session()
    except Exception:
        session = Session.builder.getOrCreate()
    session.use_role(ANALYST_ROLE)
    session.sql("USE SECONDARY ROLES NONE").collect()
    session.use_warehouse(WAREHOUSE)
    return session

SPANS_SQL = """
SELECT REGEXP_SUBSTR(record_attributes:"gen_ai.conversation.id"::STRING,
                     '^cookbook-lcmcp-(.+)-[0-9a-f]{10}$', 1, 1, 'e')   AS agent,
       record_attributes:"gen_ai.conversation.id"::STRING               AS conversation_id,
       trace:"trace_id"::STRING                                         AS trace_id,
       trace:"span_id"::STRING                                          AS span_id,
       record_attributes:"gen_ai.request.model"::STRING                 AS model,
       record_attributes:"gen_ai.provider.name"::STRING                 AS provider,
       record:"status":"code"::STRING                                   AS status,
       TRY_TO_NUMBER(record_attributes:"http.status_code"::STRING)       AS http_status,
       record_attributes:"gen_ai.usage.input_tokens"::INT                AS input_tokens,
       record_attributes:"gen_ai.usage.output_tokens"::INT               AS output_tokens,
       DATEDIFF('millisecond', start_timestamp, timestamp)              AS duration_ms,
       start_timestamp
FROM TABLE(AGENT_TRACE_TABLE('SNOWFLAKE'))
WHERE timestamp >= DATEADD('hour', -1 * ?, CURRENT_TIMESTAMP())
  AND resource_attributes:"user"::STRING = ?
  AND STARTSWITH(record_attributes:"gen_ai.conversation.id"::STRING, ?)
ORDER BY start_timestamp
"""

PAYLOAD_SQL = """
SELECT trace:"span_id"::STRING                           AS span_id,
       start_timestamp,
       record_attributes:"gen_ai.input.messages"::STRING  AS input_messages,
       record_attributes:"gen_ai.output.messages"::STRING AS output_messages
FROM TABLE(AGENT_TRACE_TABLE('SNOWFLAKE'))
WHERE timestamp >= DATEADD('hour', -1 * ?, CURRENT_TIMESTAMP())
  AND resource_attributes:"user"::STRING = ?
  AND trace:"trace_id"::STRING = ?
ORDER BY start_timestamp
"""

# CONTAINS on the lower-cased payload: no LIKE wildcards to escape, and the search
# term is a bind parameter, never part of the SQL text.
SEARCH_SQL = """
SELECT start_timestamp,
       record_attributes:"gen_ai.conversation.id"::STRING AS conversation_id,
       trace:"trace_id"::STRING                           AS trace_id,
       record_attributes:"gen_ai.request.model"::STRING   AS model,
       LEFT(record_attributes:"gen_ai.output.messages"::STRING, 400) AS output_preview
FROM TABLE(AGENT_TRACE_TABLE('SNOWFLAKE'))
WHERE timestamp >= DATEADD('hour', -1 * ?, CURRENT_TIMESTAMP())
  AND resource_attributes:"user"::STRING = ?
  AND STARTSWITH(record_attributes:"gen_ai.conversation.id"::STRING, ?)
  AND CONTAINS(LOWER(record_attributes:"gen_ai.input.messages"::STRING
                     || ' ' || record_attributes:"gen_ai.output.messages"::STRING), LOWER(?))
ORDER BY start_timestamp DESC
LIMIT 200
"""

COST_SQL = f"""
SELECT model,
       COUNT(DISTINCT request_id) AS requests,
       SUM(input_tokens)          AS input_tokens,
       SUM(output_tokens)         AS output_tokens,
       ROUND(SUM(credits), 6)     AS credits
FROM {COST_VIEW}
WHERE start_time >= DATEADD('hour', -1 * ?, CURRENT_TIMESTAMP())
GROUP BY 1
ORDER BY credits DESC
"""

@st.cache_data(ttl=120, show_spinner="Reading traces")
def load_spans(hours: int) -> pd.DataFrame:
    df = get_session().sql(SPANS_SQL, params=[hours, SVC_USER, CONV_PREFIX]).to_pandas()
    df.columns = [c.lower() for c in df.columns]
    return df

def query(sql: str, params: list) -> pd.DataFrame:
    df = get_session().sql(sql, params=params).to_pandas()
    df.columns = [c.lower() for c in df.columns]
    return df

def advisor(df: pd.DataFrame) -> list[tuple[str, str]]:
    """Rule-based findings. Titles and details are escaped before rendering."""
    findings = []
    turns = df.groupby("trace_id").agg(calls=("span_id", "count"), agent=("agent", "first"))
    long_turns = turns[turns["calls"] >= 5]
    if not long_turns.empty:
        findings.append(
            (
                f"{len(long_turns)} turn(s) needed 5 or more model calls",
                "Each extra call is another round trip and more input tokens, because the "
                "whole history is resent. Check whether tool descriptions steer the model "
                "to the right tool the first time.",
            )
        )
    for model, grp in df.groupby("model"):
        errors = int((grp["http_status"] >= 400).sum())
        if errors:
            codes = sorted(grp.loc[grp["http_status"] >= 400, "http_status"].dropna().astype(int).unique())
            findings.append(
                (
                    f"{model}: {errors} failed call(s), HTTP {codes}",
                    "401 usually means the model is outside the gateway allowlist. 400 or 503 "
                    "for a Claude model means it was sent to /v1/chat/completions instead of "
                    "/v1/messages. 400 on a gpt-5 model is often max_tokens instead of "
                    "max_completion_tokens.",
                )
            )
    heavy = df.groupby(["agent", "model"])["input_tokens"].mean()
    for (agent, model), avg_in in heavy.items():
        if avg_in and avg_in > 4000:
            findings.append(
                (
                    f"{agent} on {model} averages {avg_in:,.0f} input tokens per call",
                    "Input grows with every turn because tool results stay in the history. "
                    "Trim tool output (fewer columns, a row limit) or summarize older turns.",
                )
            )
    return findings

st.title("Gateway agent traces")
st.caption(
    "Scope: service user "
    + esc(SVC_USER)
    + ", conversations starting "
    + esc(CONV_PREFIX)
    + ". Traces are best effort and are not a billing source; use the Cost tab for credits."
)

window = st.sidebar.selectbox("Window", list(LOOKBACK_HOURS), index=1)
hours = LOOKBACK_HOURS[window]  # allowlisted integer, still passed as a bind parameter
if st.sidebar.button("Refresh"):
    st.cache_data.clear()

try:
    spans = load_spans(hours)
except Exception as exc:  # noqa: BLE001
    st.error("Could not read AGENT_TRACE_TABLE. The ANALYST role needs MONITOR on the gateway.")
    st.code(str(exc)[:1000])
    st.stop()

if spans.empty:
    st.info("No spans for this recipe's agents in the window. Run client/agent.py, then Refresh.")
    st.stop()

agents = sorted(spans["agent"].dropna().unique())
chosen = st.sidebar.multiselect("Agents", agents, default=agents)
spans = spans[spans["agent"].isin(chosen)]

overview, conversations, search, cost, findings_tab = st.tabs(
    ["Overview", "Conversations", "Search", "Cost", "Advisor"]
)

with overview:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Model calls", len(spans))
    c2.metric("Turns", spans["trace_id"].nunique())
    c3.metric("Conversations", spans["conversation_id"].nunique())
    c4.metric("Failed calls", int((spans["http_status"] >= 400).sum()))
    by_agent = (
        spans.groupby(["agent", "model"])
        .agg(
            calls=("span_id", "count"),
            input_tokens=("input_tokens", "sum"),
            output_tokens=("output_tokens", "sum"),
            p50_ms=("duration_ms", "median"),
        )
        .reset_index()
    )
    st.dataframe(by_agent, hide_index=True, width="stretch")

with conversations:
    conv = st.selectbox("Conversation", sorted(spans["conversation_id"].unique(), reverse=True))
    turns = (
        spans[spans["conversation_id"] == conv]
        .groupby("trace_id")
        .agg(
            started=("start_timestamp", "min"),
            calls=("span_id", "count"),
            input_tokens=("input_tokens", "sum"),
            output_tokens=("output_tokens", "sum"),
        )
        .sort_values("started")
        .reset_index()
    )
    st.dataframe(turns, hide_index=True, width="stretch")
    trace_id = st.selectbox("Turn (trace_id)", turns["trace_id"].tolist())
    payload = query(PAYLOAD_SQL, [hours, SVC_USER, trace_id])
    if payload["input_messages"].isna().all():
        st.info("No payloads: capture_payload.request_response is off in the gateway specification.")
    for _, row in payload.iterrows():
        with st.expander(f"span {esc(row['span_id'])}"):
            st.code(str(row["input_messages"])[:6000], language="json")
            st.code(str(row["output_messages"])[:3000], language="json")

with search:
    term = st.text_input("Find text in captured prompts and responses", max_chars=200)
    if term.strip():
        st.dataframe(query(SEARCH_SQL, [hours, SVC_USER, CONV_PREFIX, term.strip()]), hide_index=True, width="stretch")

with cost:
    st.caption(
        "From ACCOUNT_USAGE.AI_GATEWAY_USAGE_HISTORY, which lags and is per user, "
        "not per agent. Give each agent its own service user for per-agent cost."
    )
    st.dataframe(query(COST_SQL, [hours]), hide_index=True, width="stretch")

with findings_tab:
    items = advisor(spans)
    if not items:
        st.success("No findings for this window.")
    for title, detail in items:
        with st.container(border=True):
            st.markdown("**" + esc(title) + "**")
            st.write(detail)
```

## `client/`

### `client/agent.py`

Copy code

```
"""External LangChain agents that reason through Cortex AI Gateway and act through a
Snowflake-managed MCP server.

The agents run wherever this script runs. Two things cross into Snowflake, both
authenticated with the agent service user's programmatic access token (PAT):

  * model inference, through the gateway endpoint from SHOW AI GATEWAYS
  * tool calls, through the MCP server (Cortex Analyst, Cortex Search, read-only SQL)

Every model call carries two headers that shape the gateway's traces:

  traceparent                              one trace_id per user turn (W3C Trace Context)
  x-snowflake-ai-gateway-conversation-id   one id per conversation

The conversation id starts with "cookbook-lcmcp-<agent>-", which is how the
analyzer app scopes itself to this recipe's traffic.

Usage:
    export AGENT_PAT='<token_secret from sql/03>'
    export AI_GATEWAY_BASE_URL='<base_url from SHOW AI GATEWAYS>'
    python agent.py
"""

from __future__ import annotations

import asyncio
import os
import sys
import uuid
from urllib.parse import urlsplit, urlunsplit

DATABASE = "COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING"
SCHEMA = "DATA"
MCP_SERVER = "MARKETING_MCP"
CONVERSATION_PREFIX = "cookbook-lcmcp"

CLAUDE_MODEL = os.getenv("AGENT_CLAUDE_MODEL", "claude-sonnet-4-6")  # /v1/messages
OPENAI_MODEL = os.getenv("AGENT_OPENAI_MODEL", "openai-gpt-5-mini")  # /v1/chat/completions

SYSTEM_PROMPT = (
    "You answer questions about Northwind marketing using Snowflake tools.\n"
    "- For numbers (spend, revenue, conversions, ROAS, CPA): call query_campaigns to "
    "get SQL, then call execute_sql with exactly that SQL to get the rows.\n"
    "- For strategy, methodology, plans, or benchmarks: call search_strategy_docs.\n"
    "- Use both when a question compares results to a plan or benchmark.\n"
    "Cite the numbers you used. Express ROAS as a multiplier such as 3.2x. Be brief."
)

# Each conversation is a list of turns; later turns rely on earlier context.
AGENTS = [
    {
        "slug": "campaign-analyst",
        "family": "anthropic",
        "model": CLAUDE_MODEL,
        "conversations": [
            ["What was ROAS by channel in Q4 2025?", "Which of those channels beat its benchmark?"],
            ["What is our attribution methodology?"],
        ],
    },
    {
        "slug": "strategy-advisor",
        "family": "openai",
        "model": OPENAI_MODEL,
        "conversations": [
            ["Did the Q4 Holiday Push meet the CPA target in the Q4 planning brief?"],
        ],
    },
]

def gateway_base_url() -> str:
    """The gateway endpoint, with the host normalised for TLS.

    Take the value from SHOW AI GATEWAYS (base_url, or privatelink_base_url on
    private connectivity). /api/v2/cortex is Cortex Inference, not the gateway:
    requests there skip the allowlist and write no gateway spans, so it is refused.
    """
    raw = os.getenv("AI_GATEWAY_BASE_URL", "").strip().rstrip("/")
    if not raw:
        sys.exit("Set AI_GATEWAY_BASE_URL to base_url from SHOW AI GATEWAYS.")
    parts = urlsplit(raw)
    if parts.scheme != "https" or "/api/v2/aigateways/" not in parts.path + "/":
        sys.exit(f"Refusing {raw!r}: only https://<host>/api/v2/aigateways/<name> is governed and traced.")
    # Snowflake TLS certificates use hyphens; account hosts from SHOW may contain underscores.
    return urlunsplit((parts.scheme, parts.netloc.replace("_", "-"), parts.path, "", ""))

def mcp_url(base_url: str) -> str:
    host = urlsplit(base_url).netloc
    return f"https://{host}/api/v2/databases/{DATABASE}/schemas/{SCHEMA}/mcp-servers/{MCP_SERVER}"

def new_traceparent() -> tuple[str, str]:
    trace_id = uuid.uuid4().hex
    return f"00-{trace_id}-{uuid.uuid4().hex[:16]}-01", trace_id

def build_llm(family: str, model: str, pat: str, base_url: str, headers: dict):
    if family == "anthropic":
        from langchain_anthropic import ChatAnthropic

        # Claude is served on /v1/messages only. The Anthropic client appends
        # /v1/messages itself and sends x-api-key; the gateway wants a Bearer
        # token, so the real credential travels in default_headers.
        return ChatAnthropic(
            model=model,
            anthropic_api_url=base_url,
            anthropic_api_key="not-used",
            default_headers={"Authorization": f"Bearer {pat}", **headers},
            max_tokens=1024,
            temperature=0,
            timeout=180,
        )
    from langchain_openai import ChatOpenAI

    # gpt-5 models reject max_tokens and require max_completion_tokens.
    return ChatOpenAI(
        model=model,
        base_url=f"{base_url}/v1",
        api_key=pat,
        default_headers=headers,
        max_completion_tokens=2048,
        timeout=180,
    )

async def run() -> int:
    pat = os.getenv("AGENT_PAT")
    if not pat:
        sys.exit("Set AGENT_PAT to the token from sql/03_service_user_pat.sql.")
    base_url = gateway_base_url()

    from langchain.agents import create_agent
    from langchain_mcp_adapters.client import MultiServerMCPClient

    mcp = MultiServerMCPClient(
        {
            "snowflake": {
                "transport": "streamable_http",
                "url": mcp_url(base_url),
                "headers": {"Authorization": f"Bearer {pat}"},
            }
        }
    )
    tools = await mcp.get_tools()
    print(f"gateway : {base_url}")
    print(f"mcp     : {mcp_url(base_url)}")
    print(f"tools   : {', '.join(t.name for t in tools)}\n")

    failures = 0
    for agent_def in AGENTS:
        for turns in agent_def["conversations"]:
            conversation_id = f"{CONVERSATION_PREFIX}-{agent_def['slug']}-{uuid.uuid4().hex[:10]}"
            history: list = []
            print(f"[{agent_def['slug']}] model={agent_def['model']} conversation={conversation_id}")
            for question in turns:
                traceparent, trace_id = new_traceparent()
                headers = {"traceparent": traceparent, "x-snowflake-ai-gateway-conversation-id": conversation_id}
                llm = build_llm(agent_def["family"], agent_def["model"], pat, base_url, headers)
                agent = create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)
                history.append({"role": "user", "content": question})
                seen = len(history)
                print(f"  Q  {question}\n     trace_id={trace_id}")
                try:
                    result = await agent.ainvoke({"messages": history})
                except Exception as exc:  # noqa: BLE001 - report and move on to the next conversation
                    failures += 1
                    print(f"     ERROR {type(exc).__name__}: {str(exc)[:300]}\n")
                    break
                history = result["messages"]
                used = [c["name"] for m in history[seen:] for c in (getattr(m, "tool_calls", None) or [])]
                answer = history[-1].content
                if isinstance(answer, list):  # Anthropic content blocks
                    answer = " ".join(b.get("text", "") for b in answer if isinstance(b, dict))
                print(f"     tools: {', '.join(used) or 'none'}")
                print(f"  A  {answer.strip()[:600]}\n")
    print("Traces land in AGENT_TRACE_TABLE('SNOWFLAKE') within about a minute; see sql/04.")
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(asyncio.run(run()))
```

### `client/requirements.txt`

```
# External agent (client/agent.py). Runs outside Snowflake; needs no Snowflake SDK.
# Pinned as a set: langchain-mcp-adapters 0.1.x fails to import against mcp 2.x.
langchain==1.0.0
langchain-core==1.6.5
langgraph==1.0.0
langchain-anthropic==1.0.0
langchain-openai==1.0.0
langchain-mcp-adapters==0.3.2
mcp==1.30.0
anthropic==0.69.0
openai==2.3.0
httpx==0.28.1
```

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- LangChain + MCP agent tracing: roles, service user, network policy, warehouse,
-- database.
-- Run as ACCOUNTADMIN (creates a user, a network policy, and grants on the
-- account's AI gateway). Idempotent.

SET cookbook_db   = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING';
SET cookbook_wh   = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_WH';
SET agent_role    = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_AGENT';     -- the external agent's identity
SET analyst_role  = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_ANALYST';   -- reads traces and cost
SET svc_user      = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_SVC';
SET svc_network_rule   = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING.OBS.COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_SVC_CLIENTS';
SET svc_network_policy = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_SVC_POLICY';
SET gateway       = 'SNOWFLAKE';
SET me            = '"' || CURRENT_USER() || '"';

-- Where the agent runs. A service user can only use a programmatic access token
-- while it is subject to a network policy, so the service user gets its own
-- policy allowing this range and nothing else. The default is this session's
-- egress address. If the agent runs on another host, set it to that host's
-- address instead, for example
--   SET client_cidr = '203.0.113.10/32';
SET client_cidr   = CURRENT_IP_ADDRESS() || '/32';

USE ROLE ACCOUNTADMIN;

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db);
USE DATABASE IDENTIFIER($cookbook_db);
CREATE SCHEMA IF NOT EXISTS DATA;   -- tables, semantic view, search service, MCP server
CREATE SCHEMA IF NOT EXISTS OBS;    -- cost view for the analyzer

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;

CREATE ROLE IF NOT EXISTS IDENTIFIER($agent_role);
CREATE ROLE IF NOT EXISTS IDENTIFIER($analyst_role);

-- AGENT: model inference through the gateway, plus what the MCP tools need.
-- Object grants for the tools are in sql/02, after the objects exist.
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($agent_role);
GRANT USAGE ON AI GATEWAY IDENTIFIER($gateway) TO ROLE IDENTIFIER($agent_role);
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($agent_role);
GRANT USAGE ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($agent_role);
GRANT USAGE ON SCHEMA DATA TO ROLE IDENTIFIER($agent_role);

-- ANALYST: AGENT_TRACE_TABLE needs MONITOR on the gateway. This role gets
-- MONITOR and no USAGE of its own. It can still send inference while PUBLIC
-- holds USAGE on the gateway (the default, which this recipe leaves in place).
-- Revoke USAGE from PUBLIC to make the split real; see the README.
GRANT MONITOR ON AI GATEWAY IDENTIFIER($gateway) TO ROLE IDENTIFIER($analyst_role);
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($analyst_role);
GRANT USAGE ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($analyst_role);
GRANT USAGE ON SCHEMA OBS TO ROLE IDENTIFIER($analyst_role);
GRANT ROLE IDENTIFIER($analyst_role) TO USER IDENTIFIER($me);

-- The agent's identity. The MCP server opens a session with the user's default
-- role and needs a default warehouse, so both are set.
CREATE USER IF NOT EXISTS IDENTIFIER($svc_user)
  TYPE = SERVICE
  DEFAULT_ROLE = $agent_role
  DEFAULT_WAREHOUSE = $cookbook_wh
  COMMENT = 'Cookbook: external LangChain agent identity';
ALTER USER IDENTIFIER($svc_user) SET DEFAULT_ROLE = $agent_role DEFAULT_WAREHOUSE = $cookbook_wh;
GRANT ROLE IDENTIFIER($agent_role) TO USER IDENTIFIER($svc_user);

-- Network policy for the service user only. Stop here unless client_cidr is a
-- single IPv4 address or range from /16 to /32: an IPv6 address, a malformed
-- value, or a broad range such as 0.0.0.0/0 is refused. The account-level
-- network policy, if any, is not touched; a user-level policy takes precedence
-- for this user only.
EXECUTE IMMEDIATE $$
DECLARE
  bad_cidr EXCEPTION (-20002, 'client_cidr must be one IPv4 address or range from /16 to /32, for example 203.0.113.10/32');
  cidr VARCHAR DEFAULT $client_cidr;
BEGIN
  IF (cidr IS NULL OR NOT REGEXP_LIKE(cidr,
      '^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])[.]){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])/(1[6-9]|2[0-9]|3[0-2])$')) THEN
    RAISE bad_cidr;
  END IF;
  RETURN 'service user network policy will allow ' || cidr;
END;
$$;

CREATE NETWORK RULE IF NOT EXISTS IDENTIFIER($svc_network_rule)
  TYPE = IPV4 MODE = INGRESS VALUE_LIST = ($client_cidr)
  COMMENT = 'Cookbook: addresses the LangChain agent service user may connect from';
ALTER NETWORK RULE IDENTIFIER($svc_network_rule) SET VALUE_LIST = ($client_cidr);   -- a rerun picks up a new address
CREATE NETWORK POLICY IF NOT EXISTS IDENTIFIER($svc_network_policy)
  ALLOWED_NETWORK_RULE_LIST = ($svc_network_rule)
  COMMENT = 'Cookbook: LangChain agent service user only';
ALTER USER IDENTIFIER($svc_user) SET NETWORK_POLICY = $svc_network_policy;

-- Per-user cost for the agent, from the billing view. Traces are best effort and
-- are not a billing source. Owned by ACCOUNTADMIN so the analyst role does not
-- need ACCOUNT_USAGE access; it only sees this service user's rows.
CREATE OR REPLACE VIEW OBS.AGENT_GATEWAY_COST
  COMMENT = 'Cookbook: gateway credits for the agent service user, per request and model'
AS
SELECT h.start_time,
       h.request_id,
       u.name                                          AS user_name,
       c.key::STRING                                   AS model,
       c.value::FLOAT                                  AS credits,
       h.operation_details[c.key]:"input_tokens"::INT  AS input_tokens,
       h.operation_details[c.key]:"output_tokens"::INT AS output_tokens
FROM SNOWFLAKE.ACCOUNT_USAGE.AI_GATEWAY_USAGE_HISTORY h
JOIN SNOWFLAKE.ACCOUNT_USAGE.USERS u ON u.user_id = h.user_id,
LATERAL FLATTEN(input => h.credits_granular) c
WHERE u.name = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_SVC';
GRANT SELECT ON VIEW OBS.AGENT_GATEWAY_COST TO ROLE IDENTIFIER($analyst_role);

SHOW AI GATEWAYS;
SELECT "name" AS gateway, "base_url", "privatelink_base_url"
FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

### `sql/02_data_and_mcp_server.sql`

Copy code

```
-- Synthetic marketing data, a semantic view, a Cortex Search service, and a
-- Snowflake-managed MCP server exposing them as tools. Run as ACCOUNTADMIN.
-- Idempotent. Company and campaign names are fictional (Northwind).

SET cookbook_db = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING';
SET cookbook_wh = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_WH';
SET agent_role  = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_AGENT';

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA DATA;

-- Monthly spend and outcomes for four channels in 2025, generated deterministically.
CREATE OR REPLACE TABLE CAMPAIGN_SPEND (
  channel       VARCHAR,
  month         DATE,
  campaign_name VARCHAR,
  spend         NUMBER(12,2),
  impressions   NUMBER,
  clicks        NUMBER,
  conversions   NUMBER,
  revenue       NUMBER(12,2)
) COMMENT = 'Cookbook: synthetic Northwind marketing spend';

INSERT INTO CAMPAIGN_SPEND
WITH channels (channel, base_spend, cpm, ctr, cvr, aov) AS (
  SELECT * FROM VALUES
    ('Paid Search',  50000, 90.0, 0.030, 0.050, 200.0),
    ('Social Media', 38000, 38.0, 0.010, 0.040, 200.0),
    ('Email',         9500, 44.0, 0.080, 0.070, 100.0),
    ('Display',      27000, 18.5, 0.005, 0.030, 150.0)
),
months AS (
  SELECT DATEADD('month', SEQ4(), '2025-01-01'::DATE) AS month,
         SEQ4() + 1 AS m
  FROM TABLE(GENERATOR(ROWCOUNT => 12))
)
SELECT c.channel,
       mo.month,
       CASE WHEN mo.m <= 3 THEN 'Q1 Brand Awareness'
            WHEN mo.m <= 6 THEN 'Q2 Product Launch'
            WHEN mo.m <= 9 THEN 'H2 Always On'
            ELSE 'Q4 Holiday Push' END                                  AS campaign_name,
       ROUND(c.base_spend * IFF(mo.m >= 10, 1.45, 1 + mo.m * 0.01), 2)  AS spend,
       ROUND(spend / c.cpm * 1000)                                      AS impressions,
       ROUND(impressions * c.ctr)                                       AS clicks,
       ROUND(clicks * c.cvr)                                            AS conversions,
       ROUND(conversions * c.aov, 2)                                    AS revenue
FROM channels c CROSS JOIN months mo;

CREATE OR REPLACE TABLE STRATEGY_DOCS (
  doc_id   VARCHAR,
  title    VARCHAR,
  content  VARCHAR,
  doc_type VARCHAR
) COMMENT = 'Cookbook: synthetic Northwind strategy documents';

INSERT INTO STRATEGY_DOCS VALUES
('DOC-001', 'Channel strategy 2025',
 'Northwind splits its 2025 budget across four channels. Paid Search receives 40 percent for direct response. Social Media receives 25 percent for awareness. Display receives 15 percent for retargeting. Email receives 10 percent and is the most cost-efficient channel. The remaining 10 percent is a flex budget for tests.',
 'strategy'),
('DOC-002', 'Attribution methodology',
 'Revenue is attributed with a multi-touch model and a 30-day lookback. First touch gets 20 percent of the credit, last touch 30 percent, and middle touches share 50 percent by recency. Attributed revenue refreshes daily with a 48-hour lag.',
 'methodology'),
('DOC-003', 'Q4 planning brief',
 'Q4 2025 is the peak period. The Holiday Push campaign runs on all channels from October 1. Targets for Q4: return on ad spend of at least 3.0x across the portfolio and cost per acquisition below 45 dollars.',
 'brief'),
('DOC-004', 'Performance benchmarks',
 'Benchmarks by channel. Paid Search: ROAS 3.0x, conversion rate 5 percent. Social Media: ROAS 1.8x. Email: ROAS 10x, conversion rate 7 percent. Display: ROAS 1.2x. Channels beating benchmark by 20 percent are flagged for more budget.',
 'methodology');

-- Semantic view for Cortex Analyst. CREATE OR ALTER keeps existing grants.
CREATE OR ALTER SEMANTIC VIEW CAMPAIGN_ANALYTICS
  TABLES (
    spend AS COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING.DATA.CAMPAIGN_SPEND
  )
  DIMENSIONS (
    spend.channel       AS channel       COMMENT = 'Marketing channel: Paid Search, Social Media, Email, or Display',
    spend.month         AS month         COMMENT = 'First day of the calendar month',
    spend.campaign_name AS campaign_name COMMENT = 'Campaign name'
  )
  METRICS (
    spend.total_spend       AS SUM(spend)       COMMENT = 'Total spend in USD',
    spend.total_revenue     AS SUM(revenue)     COMMENT = 'Total attributed revenue in USD',
    spend.total_conversions AS SUM(conversions) COMMENT = 'Total conversions',
    spend.roas              AS SUM(revenue) / NULLIF(SUM(spend), 0)     COMMENT = 'Return on ad spend: revenue divided by spend',
    spend.cpa               AS SUM(spend) / NULLIF(SUM(conversions), 0) COMMENT = 'Cost per acquisition in USD'
  )
  COMMENT = 'Cookbook: Northwind campaign performance';

-- Cortex Search over the strategy documents.
CREATE OR REPLACE CORTEX SEARCH SERVICE STRATEGY_SEARCH
  ON content
  ATTRIBUTES doc_type
  WAREHOUSE = COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_WH
  TARGET_LAG = '1 day'
AS SELECT doc_id, title, content, doc_type FROM STRATEGY_DOCS;

-- MCP server. The tool identifiers and warehouse are literals inside the spec,
-- which is why the recipe's object names are fixed.
-- execute_sql is read-only and runs as the caller, whose role can SELECT only the
-- two tables below.
CREATE OR REPLACE MCP SERVER MARKETING_MCP FROM SPECIFICATION $$
tools:
  - name: query_campaigns
    title: Campaign analytics
    type: CORTEX_ANALYST_MESSAGE
    identifier: COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING.DATA.CAMPAIGN_ANALYTICS
    description: >-
      Turns a question about Northwind campaign spend, revenue, conversions, ROAS
      or CPA into SQL. Returns the SQL; run it with execute_sql to get rows.
  - name: search_strategy_docs
    title: Strategy documents
    type: CORTEX_SEARCH_SERVICE_QUERY
    identifier: COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING.DATA.STRATEGY_SEARCH
    description: Searches Northwind strategy, attribution, planning and benchmark documents.
  - name: execute_sql
    title: Run read-only SQL
    type: SYSTEM_EXECUTE_SQL
    description: Runs a read-only SQL query, such as one returned by query_campaigns, and returns rows.
    config:
      read_only: true
      query_timeout: 60
      warehouse: COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_WH
$$;

-- CREATE OR REPLACE drops every grant on the replaced objects: grant again, every run.
GRANT USAGE  ON MCP SERVER MARKETING_MCP             TO ROLE IDENTIFIER($agent_role);
GRANT USAGE  ON CORTEX SEARCH SERVICE STRATEGY_SEARCH TO ROLE IDENTIFIER($agent_role);
GRANT SELECT ON SEMANTIC VIEW CAMPAIGN_ANALYTICS     TO ROLE IDENTIFIER($agent_role);
GRANT SELECT ON TABLE CAMPAIGN_SPEND                 TO ROLE IDENTIFIER($agent_role);
GRANT SELECT ON TABLE STRATEGY_DOCS                  TO ROLE IDENTIFIER($agent_role);

SHOW GRANTS TO ROLE IDENTIFIER($agent_role);
SELECT channel, ROUND(SUM(revenue) / SUM(spend), 2) AS roas_2025 FROM CAMPAIGN_SPEND GROUP BY 1 ORDER BY 1;
```

### `sql/03_service_user_pat.sql`

Copy code

```
-- Issue a programmatic access token (PAT) for the agent's service user.
-- Run this yourself, not through a coding agent, as ACCOUNTADMIN from a normal
-- (password, SSO, or key-pair) session: a session that itself signed in with a
-- PAT cannot issue a token restricted to a different role. Rerunning revokes the
-- previous token and issues a new one.
--
-- sql/01 put the service user under its own network policy. Without one, a
-- TYPE = SERVICE user can neither generate nor use a PAT, and the token works
-- only from the addresses that policy allows.
--
-- Copy token_secret from the ADD result into the agent's environment:
--   export AGENT_PAT='<token_secret>'
-- ROLE_RESTRICTION pins the token to the agent role, so it can reach only the
-- gateway and the MCP tools' objects.

SET svc_user   = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_SVC';
SET agent_role = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_AGENT';

USE ROLE ACCOUNTADMIN;

ALTER USER IDENTIFIER($svc_user) REMOVE PROGRAMMATIC ACCESS TOKEN IF EXISTS COOKBOOK_AGENT_PAT;

ALTER USER IDENTIFIER($svc_user) ADD PROGRAMMATIC ACCESS TOKEN COOKBOOK_AGENT_PAT
  ROLE_RESTRICTION = $agent_role
  DAYS_TO_EXPIRY = 7
  COMMENT = 'Cookbook: external LangChain agent token';
```

### `sql/04_trace_queries.sql`

Copy code

```
-- Read the agent's traces and cost. Run as the ANALYST role (MONITOR on the
-- gateway and no USAGE of its own). Every trace query (1 to 3) is scoped to this
-- recipe's service user and its conversation-id prefix, so other traffic on the
-- account's gateway stays out. The cost query (4) is scoped to the service user
-- only, because billing rows carry no conversation id.
--
-- Traces are best effort: a span can arrive late or not at all, and token totals
-- from traces can come in under metered usage. Bill from OBS.AGENT_GATEWAY_COST
-- (AI_GATEWAY_USAGE_HISTORY), never from AGENT_TRACE_TABLE.

SET cookbook_wh  = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_WH';
SET analyst_role = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_ANALYST';
SET svc_user     = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_SVC';
SET conv_prefix  = 'cookbook-lcmcp-';
SET lookback_h   = 24;

USE ROLE IDENTIFIER($analyst_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);

-- 1. Turns: one row per trace_id (one user question, one or more model calls).
--    The agent name is the conversation id's middle segment.
WITH spans AS (
  SELECT trace:"trace_id"::STRING                                    AS trace_id,
         record_attributes:"gen_ai.conversation.id"::STRING          AS conversation_id,
         record_attributes:"gen_ai.request.model"::STRING            AS model,
         TRY_TO_NUMBER(record_attributes:"http.status_code"::STRING)  AS http_status,
         record_attributes:"gen_ai.usage.input_tokens"::INT           AS input_tokens,
         record_attributes:"gen_ai.usage.output_tokens"::INT          AS output_tokens,
         start_timestamp, timestamp
  FROM TABLE(AGENT_TRACE_TABLE('SNOWFLAKE'))
  WHERE timestamp >= DATEADD('hour', -$lookback_h, CURRENT_TIMESTAMP())
    AND resource_attributes:"user"::STRING = $svc_user
    AND STARTSWITH(record_attributes:"gen_ai.conversation.id"::STRING, $conv_prefix)
)
SELECT REGEXP_SUBSTR(conversation_id, '^cookbook-lcmcp-(.+)-[0-9a-f]{10}$', 1, 1, 'e') AS agent,
       conversation_id,
       trace_id,
       MIN(start_timestamp)                                          AS started_at,
       COUNT(*)                                                      AS model_calls,
       ANY_VALUE(model)                                              AS model,
       SUM(input_tokens)                                             AS input_tokens,
       SUM(output_tokens)                                            AS output_tokens,
       DATEDIFF('millisecond', MIN(start_timestamp), MAX(timestamp)) AS duration_ms,
       IFF(COUNT_IF(http_status >= 400) = 0, 'SUCCESS', 'FAILURE')   AS status
FROM spans
GROUP BY conversation_id, trace_id
ORDER BY started_at DESC;

-- 2. One turn, span by span. Set trace_id from the query above.
SET trace_id = '<paste a trace_id>';
SELECT trace:"span_id"::STRING                                             AS span_id,
       record:"name"::STRING                                               AS span_name,
       DATEDIFF('millisecond', MIN(start_timestamp) OVER (), start_timestamp) AS offset_ms,
       DATEDIFF('millisecond', start_timestamp, timestamp)                 AS duration_ms,
       record_attributes:"gen_ai.usage.input_tokens"::INT                   AS input_tokens,
       record_attributes:"gen_ai.usage.output_tokens"::INT                  AS output_tokens,
       TRY_TO_NUMBER(record_attributes:"http.status_code"::STRING)          AS http_status
FROM TABLE(AGENT_TRACE_TABLE('SNOWFLAKE'))
WHERE timestamp >= DATEADD('hour', -$lookback_h, CURRENT_TIMESTAMP())
  AND resource_attributes:"user"::STRING = $svc_user
  AND STARTSWITH(record_attributes:"gen_ai.conversation.id"::STRING, $conv_prefix)
  AND trace:"trace_id"::STRING = $trace_id
ORDER BY start_timestamp;

-- 3. What the traces do not contain: MCP tool execution. The gateway records model
--    calls only (operation chat). Tool calls appear inside the next model call's
--    input messages, and only when payload capture is on in the gateway spec.
SELECT record_attributes:"gen_ai.operation.name"::STRING AS operation, COUNT(*) AS spans
FROM TABLE(AGENT_TRACE_TABLE('SNOWFLAKE'))
WHERE timestamp >= DATEADD('hour', -$lookback_h, CURRENT_TIMESTAMP())
  AND resource_attributes:"user"::STRING = $svc_user
  AND STARTSWITH(record_attributes:"gen_ai.conversation.id"::STRING, $conv_prefix)
GROUP BY 1;

-- 4. Cost, from the billing view. Attribution is per user: this is the service
--    user's spend across every agent it ran. Give each agent its own service user
--    if you need cost per agent. ACCOUNT_USAGE lags, so recent calls may be missing.
SELECT model,
       COUNT(DISTINCT request_id) AS requests,
       SUM(input_tokens)          AS input_tokens,
       SUM(output_tokens)         AS output_tokens,
       ROUND(SUM(credits), 6)     AS credits
FROM COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING.OBS.AGENT_GATEWAY_COST
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY 1
ORDER BY credits DESC;
```

### `sql/99_teardown.sql`

Copy code

```
-- Teardown: drop everything this recipe created. Run as ACCOUNTADMIN. Safe to rerun.
-- This recipe does not change the gateway specification.
--
-- Every name below comes from this SET block, which matches sql/01. Object names
-- in this recipe are fixed; do not edit them here.

SET cookbook_db        = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING';
SET cookbook_wh        = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_WH';
SET agent_role         = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_AGENT';
SET analyst_role       = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_ANALYST';
SET svc_user           = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_SVC';
SET svc_network_policy = 'COOKBOOK_LANGCHAIN_MCP_AGENT_TRACING_SVC_POLICY';

USE ROLE ACCOUNTADMIN;

-- Dropping the user revokes its token. The network policy must be detached
-- before it can be dropped, and dropped before the database that holds its
-- network rule.
ALTER USER IF EXISTS IDENTIFIER($svc_user) UNSET NETWORK_POLICY;
DROP USER IF EXISTS IDENTIFIER($svc_user);
DROP NETWORK POLICY IF EXISTS IDENTIFIER($svc_network_policy);

-- Dropping the database drops the MCP server, search service, semantic view,
-- tables, cost view, and the network rule.
DROP DATABASE IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);
-- Dropping the roles also removes their USAGE and MONITOR grants on the gateway.
DROP ROLE IF EXISTS IDENTIFIER($agent_role);
DROP ROLE IF EXISTS IDENTIFIER($analyst_role);

SHOW GRANTS ON AI GATEWAY SNOWFLAKE;
```
