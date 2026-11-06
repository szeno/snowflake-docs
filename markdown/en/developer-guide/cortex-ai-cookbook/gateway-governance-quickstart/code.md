# Cortex AI Gateway governance quickstart: code

Every file in the [Cortex AI Gateway governance quickstart](/developer-guide/cortex-ai-cookbook/gateway-governance-quickstart) recipe. To run the recipe, download [gateway-governance-quickstart.zip](/static/samples/cortex-ai-cookbook/gateway-governance-quickstart.zip), unzip it, and run the scripts from the `gateway-governance-quickstart/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/gateway-governance-quickstart); the zip includes it as `README.md`.

## `notebooks/`

### `notebooks/01_gateway_governance.ipynb`

Jupyter notebook, shown as Python with Markdown cells as comments.

Copy code

```
# %% [markdown]
# # Cortex AI Gateway governance quickstart
#
# Cortex AI Gateway is in preview and available on AWS commercial regions only.
#
# This notebook plays two parts:
#
# - **The application.** It calls the gateway with the service user's programmatic access token (PAT), in both API formats.
# - **The platform team.** It reads what the gateway recorded (traces, credits, quota state) with the `MONITOR` role. That role has no gateway `USAGE` of its own, but it can still send inference while `PUBLIC` holds `USAGE` on the gateway (the default). The recipe README shows how to revoke it.
#
# Before you run it:
#
# 1. Run `sql/01` to `sql/04` as described in the recipe README. `sql/01` puts the service user under a network policy that allows only `client_cidr`, so run this notebook from that address.
# 2. Export the token that `sql/03` printed: `export COOKBOOK_GATEWAY_PAT='<token_secret>'`.
# 3. Run the notebook locally (Jupyter or VS Code) with a Snowflake connection for your own user, for example `SNOWFLAKE_DEFAULT_CONNECTION_NAME=<your connection>`.
#
# Nothing here changes the gateway. The allowlist step in section 6 relies on `sql/05`, and `sql/06` undoes it.

# %%
import os
import time
import uuid

import requests
from snowflake.snowpark import Session

try:
    from snowflake.snowpark.context import get_active_session

    session = get_active_session()
except Exception:
    session = Session.builder.getOrCreate()

MONITOR_ROLE = "COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_MONITOR"
QUOTA_ADMIN_ROLE = "COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_QUOTA_ADMIN"
WAREHOUSE = "COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_WH"
SVC_USER = "COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_SVC"
QUOTA = "COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART.GOV.GATEWAY_APP_QUOTA"
USAGE_VIEW = "COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART.GOV.GATEWAY_USAGE_BY_USER"

OPENAI_MODEL = os.environ.get("GATEWAY_OPENAI_MODEL", "openai-gpt-5")  # /v1/chat/completions
CLAUDE_MODEL = os.environ.get("GATEWAY_CLAUDE_MODEL", "claude-sonnet-4-6")  # /v1/messages

PAT = os.environ["COOKBOOK_GATEWAY_PAT"]  # the service user's token from sql/03

# Read with exactly the MONITOR role's privileges: no secondary roles.
session.use_role(MONITOR_ROLE)
session.sql("USE SECONDARY ROLES NONE").collect()
session.use_warehouse(WAREHOUSE)
print(session.sql("SELECT CURRENT_USER(), CURRENT_ROLE()").collect()[0])

# %% [markdown]
# ## 0. Resolve the endpoint
#
# Read the base URL from `SHOW AI GATEWAYS`. Accounts on private connectivity get a different host, and `/api/v2/cortex` is a different service that skips the gateway's allowlist, traces, and gateway metering.
#
# TLS certificates use hyphens, so an underscore in the account host is replaced in the host part only.

# %%
gw = session.sql("SHOW AI GATEWAYS").collect()[0]
GATEWAY = gw["name"]
scheme, rest = gw["base_url"].split("://", 1)
host, path = rest.split("/", 1)
HOST = host.replace("_", "-")
BASE_URL = f"{scheme}://{HOST}/{path}"
assert "/api/v2/aigateways/" in BASE_URL, BASE_URL

# One conversation for this notebook run; one trace per turn.
CONVERSATION_ID = f"cookbook-governance-{uuid.uuid4().hex[:12]}"

def gateway_headers():
    """Bearer PAT, plus the two headers that shape the traces.

    traceparent (W3C) groups the model calls of one turn under one trace_id.
    x-snowflake-ai-gateway-conversation-id groups turns into a conversation.
    """
    return {
        "Authorization": f"Bearer {PAT}",
        "Content-Type": "application/json",
        "traceparent": f"00-{uuid.uuid4().hex}-{uuid.uuid4().hex[:16]}-01",
        "x-snowflake-ai-gateway-conversation-id": CONVERSATION_ID,
    }

def chat(model, text, **extra):
    body = {"model": model, "messages": [{"role": "user", "content": text}], **extra}
    return requests.post(f"{BASE_URL}/v1/chat/completions", headers=gateway_headers(), json=body, timeout=180)

def messages(model, text, max_tokens=256):
    body = {"model": model, "max_tokens": max_tokens, "messages": [{"role": "user", "content": text}]}
    return requests.post(f"{BASE_URL}/v1/messages", headers=gateway_headers(), json=body, timeout=180)

print("gateway        :", GATEWAY)
print("base url       :", BASE_URL)
print("conversation id:", CONVERSATION_ID)

# %% [markdown]
# ## 1. OpenAI Chat Completions format
#
# `/v1/chat/completions` serves every model family except Claude. gpt-5 models reject `max_tokens` and require `max_completion_tokens`.

# %%
r = chat(OPENAI_MODEL, "In one sentence, what is a data warehouse?", max_completion_tokens=512)
print("HTTP", r.status_code)
if r.ok:
    print(r.json()["choices"][0]["message"]["content"])

r_bad = chat(OPENAI_MODEL, "hi", max_tokens=64)
print("\nwith max_tokens -> HTTP", r_bad.status_code, r_bad.text[:160])

# %% [markdown]
# ## 2. Anthropic Messages format
#
# Claude is served on `/v1/messages` only. The same model on `/v1/chat/completions` fails.

# %%
r = messages(CLAUDE_MODEL, "In one sentence, what is a data warehouse?")
print("HTTP", r.status_code)
if r.ok:
    print(r.json()["content"][0]["text"])

r_wrong = chat(CLAUDE_MODEL, "hi", max_tokens=64)
print("\nClaude on /v1/chat/completions -> HTTP", r_wrong.status_code)

# %% [markdown]
# ## 3. Official SDKs
#
# Only the base URL and the credential change. The Anthropic SDK sends `x-api-key` by default, so give it an HTTP client that sends the Bearer token, and leave `/v1` off its base URL because the SDK appends `/v1/messages` itself.

# %%
from openai import OpenAI

oai = OpenAI(
    api_key=PAT, base_url=f"{BASE_URL}/v1", default_headers={"x-snowflake-ai-gateway-conversation-id": CONVERSATION_ID}
)
resp = oai.chat.completions.create(
    model=OPENAI_MODEL,
    max_completion_tokens=512,
    messages=[{"role": "user", "content": "Name one benefit of a central LLM gateway."}],
)
print("openai sdk   :", resp.choices[0].message.content)

import anthropic
import httpx

ant = anthropic.Anthropic(
    api_key="not-used",
    base_url=BASE_URL,
    http_client=httpx.Client(headers={"Authorization": f"Bearer {PAT}"}),
    default_headers={"Authorization": f"Bearer {PAT}", "x-snowflake-ai-gateway-conversation-id": CONVERSATION_ID},
)
msg = ant.messages.create(
    model=CLAUDE_MODEL,
    max_tokens=256,
    messages=[{"role": "user", "content": "Name one benefit of a central LLM gateway."}],
)
print("anthropic sdk:", msg.content[0].text)

# %% [markdown]
# ## 4. Traces
#
# With `logging.enabled` in the specification, every request is a span in `AGENT_TRACE_TABLE('SNOWFLAKE')`, an event table in your account. Reading it needs `MONITOR` on the gateway, which is all this session has.
#
# The query is scoped to this notebook's service user and conversation id, passed as bind parameters. Delivery is best effort: spans usually land within a minute, and a span can be late or missing. Do not bill from this table.

# %%
TRACE_SQL = """
SELECT trace:"trace_id"::STRING                                   AS trace_id,
       record:"name"::STRING                                      AS span_name,
       record_attributes:"gen_ai.provider.name"::STRING           AS provider,
       TRY_TO_NUMBER(record_attributes:"http.status_code"::STRING) AS http_status,
       record_attributes:"gen_ai.usage.input_tokens"::INT          AS input_tokens,
       record_attributes:"gen_ai.usage.output_tokens"::INT         AS output_tokens,
       DATEDIFF('millisecond', start_timestamp, timestamp)        AS duration_ms,
       start_timestamp
FROM TABLE(AGENT_TRACE_TABLE('SNOWFLAKE'))
WHERE timestamp >= DATEADD('hour', -2, CURRENT_TIMESTAMP())
  AND resource_attributes:"user"::STRING = ?
  AND record_attributes:"gen_ai.conversation.id"::STRING = ?
ORDER BY start_timestamp
"""

def conversation_spans():
    return session.sql(TRACE_SQL, params=[SVC_USER, CONVERSATION_ID]).to_pandas()

def wait_for_spans(minimum, timeout_s=180):
    deadline = time.time() + timeout_s
    df = conversation_spans()
    while len(df) < minimum and time.time() < deadline:
        time.sleep(15)
        df = conversation_spans()
    return df

# Sections 1 to 3 made 6 gateway calls with this conversation id.
spans = wait_for_spans(6)
print(f"{len(spans)} spans for {CONVERSATION_ID}")
spans

# %% [markdown]
# ## 5. The path that bypasses the gateway
#
# `/api/v2/cortex` is Cortex Inference. It accepts the same request and the same token, but the gateway never sees it: no gateway span, no allowlist, and it meters to `CORTEX_REST_API_USAGE_HISTORY` instead of `AI_GATEWAY_USAGE_HISTORY`.

# %%
before = len(conversation_spans())
direct = requests.post(
    f"https://{HOST}/api/v2/cortex/v1/chat/completions",
    headers=gateway_headers(),
    json={"model": OPENAI_MODEL, "max_completion_tokens": 256, "messages": [{"role": "user", "content": "hi"}]},
    timeout=180,
)
print("direct /api/v2/cortex -> HTTP", direct.status_code)
time.sleep(90)
after = len(conversation_spans())
print(f"gateway spans for this conversation: before={before} after={after}")

# %% [markdown]
# ## 6. Model allowlist (run `sql/05` first)
#
# `sql/05` replaces the specification with one that exposes `claude-*` only. Run it, wait about a minute, then run this cell. Then run `sql/06` to restore the original specification.

# %%
spec = session.sql("SHOW AI GATEWAYS").collect()[0]["specification"]
print(spec, "\n")

r_openai = chat(OPENAI_MODEL, "hi", max_completion_tokens=256)
r_claude = messages(CLAUDE_MODEL, "hi", max_tokens=32)
r_direct = requests.post(
    f"https://{HOST}/api/v2/cortex/v1/chat/completions",
    headers=gateway_headers(),
    json={"model": OPENAI_MODEL, "max_completion_tokens": 256, "messages": [{"role": "user", "content": "hi"}]},
    timeout=180,
)
print(f"gateway, {OPENAI_MODEL:<18} -> HTTP {r_openai.status_code}")
print(f"gateway, {CLAUDE_MODEL:<18} -> HTTP {r_claude.status_code}")
print(f"direct,  {OPENAI_MODEL:<18} -> HTTP {r_direct.status_code}  (not governed by the allowlist)")

# %% [markdown]
# ## 7. Credits
#
# Credits come from `ACCOUNT_USAGE.AI_GATEWAY_USAGE_HISTORY`, which is the billing source of truth and is not real time. The recipe's view resolves `USER_ID` to a name and takes credits per model from `CREDITS_GRANULAR`. The only attribution dimension is the user, which is why each application gets its own service user.

# %%
session.sql(f"""
SELECT user_name, model,
       COUNT(DISTINCT request_id) AS requests,
       SUM(input_tokens)          AS input_tokens,
       SUM(output_tokens)         AS output_tokens,
       ROUND(SUM(credits), 6)     AS credits
FROM {USAGE_VIEW}
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY credits DESC
""").to_pandas()

# %% [markdown]
# ## 8. Quota state
#
# The quota from `sql/04` blocks the service user once it spends its daily limit on the gateway. Enforcement lands within minutes of the spend, so some overshoot is expected. This cell switches to the quota admin role to read the quota's configuration, scope, and current blocks.

# %%
session.use_role(QUOTA_ADMIN_ROLE)
for method in ("GET_CONFIG", "GET_QUOTA_SCOPE", "GET_ACTIVE_BLOCKS_V2"):
    rows = session.sql(f"CALL {QUOTA}!{method}()").collect()
    print(f"--- {method}")
    for row in rows:
        print({k: v for k, v in row.as_dict().items() if v is not None})
session.use_role(MONITOR_ROLE)

# %% [markdown]
# ## Next
#
# - If you ran `sql/05`, run `sql/06_restore_gateway_spec.sql` now and confirm `matches_snapshot = TRUE`.
# - When you are done, run `sql/99_teardown.sql`. It restores the specification, removes the quota, and drops every recipe object.
```

### `notebooks/requirements.txt`

```
# Notebook (notebooks/01_gateway_governance.ipynb), run locally.
requests==2.32.5
openai==2.3.0
anthropic==0.69.0
httpx==0.28.1
snowflake-snowpark-python==1.40.0
snowflake-connector-python==3.18.1
pandas==2.3.3
pyarrow==21.0.0
```

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- Gateway governance quickstart: roles, service user, network policy, tag,
-- warehouse, database.
-- Run as ACCOUNTADMIN (creates a user, a network policy, and grants on the
-- account's AI gateway). Idempotent.

SET cookbook_db        = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART';
SET cookbook_wh        = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_WH';
SET app_role           = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_APP';          -- sends inference
SET monitor_role       = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_MONITOR';      -- reads traces and usage
SET quota_admin_role   = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_QUOTA_ADMIN';  -- owns the quota
SET svc_user           = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_SVC';          -- the application identity
SET gateway            = 'SNOWFLAKE';                                           -- each account has one gateway
SET cost_center_tag    = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART.GOV.COST_CENTER';
SET cost_center_value  = 'cookbook_gateway_app';
SET svc_network_rule   = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART.GOV.COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_SVC_CLIENTS';
SET svc_network_policy = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_SVC_POLICY';
SET me                 = '"' || CURRENT_USER() || '"';

-- Where the application calls the gateway from. A service user can only use a
-- programmatic access token while it is subject to a network policy, so the
-- service user gets its own policy allowing this range and nothing else.
-- The default is this session's egress address. If the client runs on another
-- host, set it to that host's address instead, for example
--   SET client_cidr = '203.0.113.10/32';
SET client_cidr        = CURRENT_IP_ADDRESS() || '/32';

USE ROLE ACCOUNTADMIN;

-- Database, schema, warehouse --------------------------------------------------
CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db);
USE DATABASE IDENTIFIER($cookbook_db);
CREATE SCHEMA IF NOT EXISTS GOV;

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;

-- Roles ------------------------------------------------------------------------
CREATE ROLE IF NOT EXISTS IDENTIFIER($app_role);
CREATE ROLE IF NOT EXISTS IDENTIFIER($monitor_role);
CREATE ROLE IF NOT EXISTS IDENTIFIER($quota_admin_role);

-- APP: inference only. USAGE on the gateway picks the path; CORTEX_USER is the
-- model entitlement. No warehouse and no database: gateway inference needs neither.
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($app_role);
GRANT USAGE ON AI GATEWAY IDENTIFIER($gateway) TO ROLE IDENTIFIER($app_role);

-- MONITOR: read traces (AGENT_TRACE_TABLE needs MONITOR on the gateway) and the
-- gateway usage view below. This role gets MONITOR and no USAGE of its own. It
-- can still send inference while PUBLIC holds USAGE on the gateway (the
-- default, which this recipe leaves in place). Revoke USAGE from PUBLIC to make
-- the split real; see the README.
GRANT MONITOR ON AI GATEWAY IDENTIFIER($gateway) TO ROLE IDENTIFIER($monitor_role);
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($monitor_role);
GRANT USAGE ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($monitor_role);
GRANT USAGE ON SCHEMA GOV TO ROLE IDENTIFIER($monitor_role);

-- AI_GATEWAY_USAGE_HISTORY carries USER_ID only. Resolving it to a name needs
-- ACCOUNT_USAGE.USERS, which would otherwise mean granting SECURITY_VIEWER (login
-- history and more). This view, owned by ACCOUNTADMIN, exposes just the gateway
-- rows with the user name, one row per request per model, credits from
-- CREDITS_GRANULAR so multi-model requests are not double counted.
CREATE OR REPLACE VIEW GOV.GATEWAY_USAGE_BY_USER
  COMMENT = 'Cookbook: gateway credits per request and model, with user name'
AS
SELECT h.start_time,
       h.request_id,
       h.gateway_name,
       h.user_id,
       u.name                                         AS user_name,
       c.key::STRING                                  AS model,
       c.value::FLOAT                                 AS credits,
       h.operation_details[c.key]:"input_tokens"::INT  AS input_tokens,
       h.operation_details[c.key]:"output_tokens"::INT AS output_tokens
FROM SNOWFLAKE.ACCOUNT_USAGE.AI_GATEWAY_USAGE_HISTORY h
LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.USERS u ON u.user_id = h.user_id,
LATERAL FLATTEN(input => h.credits_granular) c;
GRANT SELECT ON VIEW GOV.GATEWAY_USAGE_BY_USER TO ROLE IDENTIFIER($monitor_role);

-- QUOTA_ADMIN: create and configure the per-user quota in GOV.
GRANT DATABASE ROLE SNOWFLAKE.QUOTA_CREATOR TO ROLE IDENTIFIER($quota_admin_role);
GRANT USAGE ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($quota_admin_role);
GRANT USAGE ON SCHEMA GOV TO ROLE IDENTIFIER($quota_admin_role);
GRANT CREATE SNOWFLAKE.CORE.QUOTA ON SCHEMA GOV TO ROLE IDENTIFIER($quota_admin_role);
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($quota_admin_role);
-- The quota admin role owns the quota. Granting it to SYSADMIN (the usual role
-- hierarchy) lets ACCOUNTADMIN manage and drop the quota in teardown.
GRANT ROLE IDENTIFIER($quota_admin_role) TO ROLE SYSADMIN;

-- You run the notebook and the quota script with these roles.
GRANT ROLE IDENTIFIER($monitor_role)     TO USER IDENTIFIER($me);
GRANT ROLE IDENTIFIER($quota_admin_role) TO USER IDENTIFIER($me);

-- Service user: the identity an application uses to call the gateway. Cost and
-- traces are attributed to it, so give each application its own user.
CREATE USER IF NOT EXISTS IDENTIFIER($svc_user)
  TYPE = SERVICE
  DEFAULT_ROLE = $app_role
  COMMENT = 'Cookbook: gateway governance quickstart application identity';
GRANT ROLE IDENTIFIER($app_role) TO USER IDENTIFIER($svc_user);

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
  COMMENT = 'Cookbook: addresses the gateway quickstart service user may connect from';
ALTER NETWORK RULE IDENTIFIER($svc_network_rule) SET VALUE_LIST = ($client_cidr);   -- a rerun picks up a new address
CREATE NETWORK POLICY IF NOT EXISTS IDENTIFIER($svc_network_policy)
  ALLOWED_NETWORK_RULE_LIST = ($svc_network_rule)
  COMMENT = 'Cookbook: gateway quickstart service user only';
ALTER USER IDENTIFIER($svc_user) SET NETWORK_POLICY = $svc_network_policy;

-- Cost-center tag: scopes the quota (and the optional budget) to this user only.
CREATE TAG IF NOT EXISTS GOV.COST_CENTER
  ALLOWED_VALUES 'cookbook_gateway_app'
  COMMENT = 'Cookbook: scopes gateway quota and budget to tagged users';
GRANT APPLYBUDGET ON TAG GOV.COST_CENTER TO ROLE IDENTIFIER($quota_admin_role);
ALTER USER IDENTIFIER($svc_user) SET TAG IDENTIFIER($cost_center_tag) = $cost_center_value;

-- Endpoint to use. Read it from here, never from /api/v2/cortex.
SHOW AI GATEWAYS;
SELECT "name" AS gateway, "base_url", "privatelink_base_url"
FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

### `sql/02_snapshot_gateway_spec.sql`

Copy code

```
-- Snapshot the gateway specification and install a restore procedure.
-- Run as ACCOUNTADMIN (the gateway owner). Idempotent.
--
-- ALTER AI GATEWAY ... FROM SPECIFICATION replaces the whole specification.
-- Anything you leave out falls back to its default. So before this recipe
-- changes the spec (sql/05), it records the current one here, and
-- sql/06_restore_gateway_spec.sql and sql/99_teardown.sql put it back.
--
-- Only the FIRST snapshot is kept. Rerunning this script never overwrites it,
-- so a rerun after a half-finished run cannot record the restricted spec as
-- the "original".

SET cookbook_db = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART';
SET cookbook_wh = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_WH';
SET gateway     = 'SNOWFLAKE';

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA GOV;

CREATE TABLE IF NOT EXISTS GATEWAY_SPEC_SNAPSHOT (
  gateway_name   VARCHAR,
  specification  VARCHAR,
  spec_sha2      VARCHAR,
  captured_at    TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
  captured_by    VARCHAR DEFAULT CURRENT_USER()
);

DESCRIBE AI GATEWAY IDENTIFIER($gateway);

INSERT INTO GATEWAY_SPEC_SNAPSHOT (gateway_name, specification, spec_sha2)
SELECT d."name", d."specification", SHA2(d."specification")
FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) d
WHERE NOT EXISTS (SELECT 1 FROM GATEWAY_SPEC_SNAPSHOT s WHERE s.gateway_name = d."name");

SELECT gateway_name, spec_sha2, captured_at, specification FROM GATEWAY_SPEC_SNAPSHOT;

-- Restore procedure. Caller's rights: it can only do what the caller's role can
-- already do (ALTER AI GATEWAY needs the gateway owner). The gateway name is
-- checked against SHOW AI GATEWAYS and the spec text comes from the snapshot
-- table, never from user input. A spec containing a double dollar sign is
-- refused because it would terminate the dollar-quoted literal. CHR(36) is '$',
-- spelled out so it does not end this procedure's own $$ body.
-- Caller's-rights procedures resolve unqualified names in the caller's session,
-- so the snapshot table is fully qualified. Object names in this recipe are
-- fixed; sql/05, sql/06 and sql/99 name the same table and procedure.
CREATE OR REPLACE PROCEDURE RESTORE_GATEWAY_SPEC()
  RETURNS VARCHAR
  LANGUAGE SQL
  EXECUTE AS CALLER
AS
$$
DECLARE
  gw        VARCHAR;
  spec      VARCHAR;
  want_sha  VARCHAR;
  have_sha  VARCHAR;
  known     INTEGER;
  show_id   VARCHAR;
  stmt      VARCHAR;
  dd        VARCHAR DEFAULT CHR(36) || CHR(36);
BEGIN
  SELECT gateway_name, specification, spec_sha2
    INTO :gw, :spec, :want_sha
    FROM COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART.GOV.GATEWAY_SPEC_SNAPSHOT
    ORDER BY captured_at
    LIMIT 1;

  SHOW AI GATEWAYS;
  show_id := SQLID;   -- inside Snowflake Scripting, use SQLID rather than LAST_QUERY_ID()
  SELECT COUNT(*) INTO :known FROM TABLE(RESULT_SCAN(:show_id)) WHERE "name" = :gw;
  IF (known <> 1) THEN
    RETURN 'REFUSED: snapshot gateway ' || gw || ' not found in SHOW AI GATEWAYS';
  END IF;
  IF (CONTAINS(spec, dd)) THEN
    RETURN 'REFUSED: snapshot spec contains a double dollar sign; restore it manually';
  END IF;

  stmt := 'ALTER AI GATEWAY "' || gw || '" FROM SPECIFICATION ' || dd || spec || dd;
  EXECUTE IMMEDIATE :stmt;

  SHOW AI GATEWAYS;
  show_id := SQLID;
  SELECT SHA2("specification") INTO :have_sha
    FROM TABLE(RESULT_SCAN(:show_id)) WHERE "name" = :gw;

  IF (have_sha = want_sha) THEN
    RETURN 'RESTORED: ' || gw || ' spec matches snapshot (sha2 ' || LEFT(want_sha, 12) || ')';
  END IF;
  RETURN 'MISMATCH: ' || gw || ' now sha2 ' || LEFT(have_sha, 12) || ', snapshot ' || LEFT(want_sha, 12);
END;
$$;
```

### `sql/03_service_user_pat.sql`

Copy code

```
-- Issue a programmatic access token (PAT) for the application's service user.
-- Run this yourself, not through a coding agent, as ACCOUNTADMIN from a normal
-- (password, SSO, or key-pair) session: a session that itself signed in with a
-- PAT cannot issue a token restricted to a different role. Rerunning revokes the
-- previous token and issues a new one.
--
-- sql/01 put the service user under its own network policy. Without one, a
-- TYPE = SERVICE user can neither generate nor use a PAT, and the token works
-- only from the addresses that policy allows.
--
-- The token secret is shown ONCE in the result of the ADD statement. Copy it into
-- an environment variable on the machine that runs the client, for example
--   export COOKBOOK_GATEWAY_PAT='<token_secret>'
-- and never commit it. ROLE_RESTRICTION pins every session the token opens to the
-- inference-only role, so a leaked token cannot read data or change the gateway.

SET svc_user = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_SVC';
SET app_role = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_APP';

USE ROLE ACCOUNTADMIN;

ALTER USER IDENTIFIER($svc_user) REMOVE PROGRAMMATIC ACCESS TOKEN IF EXISTS COOKBOOK_GATEWAY_APP_PAT;

ALTER USER IDENTIFIER($svc_user) ADD PROGRAMMATIC ACCESS TOKEN COOKBOOK_GATEWAY_APP_PAT
  ROLE_RESTRICTION = $app_role
  DAYS_TO_EXPIRY = 7
  COMMENT = 'Cookbook: gateway governance quickstart client token';
```

### `sql/04_per_user_quota.sql`

Copy code

```
-- Per-user quota on AI Gateway spend, with built-in blocking.
-- Run as the QUOTA_ADMIN role created in sql/01 (no ACCOUNTADMIN needed).
-- Idempotent: every method call below sets state rather than appending to it.
--
-- A new quota monitors ALL users in the account until you narrow it. This script
-- narrows it to users tagged COST_CENTER = 'cookbook_gateway_app' (only the
-- recipe's service user) BEFORE it sets a limit, and no enforcement happens
-- until a limit exists. Keep that order if you adapt it.

SET cookbook_db      = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART';
SET cookbook_wh      = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_WH';
SET quota_admin_role = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_QUOTA_ADMIN';
SET cost_center_tag  = $cookbook_db || '.GOV.COST_CENTER';   -- created in sql/01
SET cost_center_value = 'cookbook_gateway_app';
SET daily_credits    = 5;     -- per user, per UTC day

USE ROLE IDENTIFIER($quota_admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA GOV;

CREATE SNOWFLAKE.CORE.QUOTA IF NOT EXISTS GATEWAY_APP_QUOTA();

-- 1. Scope: users carrying the tag value. SET_USER_TAGS replaces any prior tags.
--    The calling role needs APPLYBUDGET on the tag (granted in sql/01).
CALL GATEWAY_APP_QUOTA!SET_USER_TAGS(
  [[(SELECT SYSTEM$REFERENCE('TAG', $cost_center_tag, 'SESSION', 'APPLYBUDGET')),
    $cost_center_value]],
  'UNION');

-- 2. Domain: the AI Gateway. Each account has one gateway, so the domain covers it.
CALL GATEWAY_APP_QUOTA!ADD_SHARED_RESOURCE('AI GATEWAY');

-- 3. Limit, then enforcement. Arguments: (block, notify_blocked_user_by_email).
--    The service user has no mailbox, so email notification is off.
CALL GATEWAY_APP_QUOTA!SET_PER_USER_LIMIT($daily_credits, 'DAILY');
CALL GATEWAY_APP_QUOTA!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, FALSE);

-- Verify. Limit and scope changes take roughly 5 to 10 minutes to propagate, and
-- GET_USERS resolves tags through TAG_REFERENCES, which can lag up to about 2 hours.
CALL GATEWAY_APP_QUOTA!GET_QUOTA_SCOPE();
CALL GATEWAY_APP_QUOTA!GET_CONFIG();
CALL GATEWAY_APP_QUOTA!GET_USERS();
```

### `sql/05_allowlist_restrict.sql`

Copy code

```
-- Model allowlist, enforced at the gateway. Run as ACCOUNTADMIN.
--
-- WARNING: this replaces the account's whole gateway specification. Every
-- client in the account is limited to Claude models until you run
-- sql/06_restore_gateway_spec.sql. Run sql/02 first so the original is saved.
--
-- ALTER AI GATEWAY ... FROM SPECIFICATION does not patch fields: anything you
-- omit falls back to its default. This spec therefore states logging explicitly,
-- so traces keep flowing while the restriction is in place.

SET gateway        = 'SNOWFLAKE';
SET cookbook_db    = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART';
SET cookbook_wh    = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_WH';
SET snapshot_table = $cookbook_db || '.GOV.GATEWAY_SPEC_SNAPSHOT';   -- created in sql/02

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE IDENTIFIER($cookbook_wh);

-- Stop here (division by zero) if there is no snapshot to restore from.
SELECT COUNT(*) AS snapshots, 1 / COUNT(*) AS precheck
FROM IDENTIFIER($snapshot_table);

ALTER AI GATEWAY IDENTIFIER($gateway) FROM SPECIFICATION $$
schema_version: 1
models:
  - name: 'claude-*'
logging:
  enabled: true
  capture_payload:
    request_response: false
$$;

DESCRIBE AI GATEWAY IDENTIFIER($gateway);
```

### `sql/06_restore_gateway_spec.sql`

Copy code

```
-- Restore the gateway specification captured by sql/02. Run as ACCOUNTADMIN.
-- Safe to run at any time; teardown runs the same procedure.

SET cookbook_db    = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART';
SET cookbook_wh    = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_WH';
SET restore_proc   = $cookbook_db || '.GOV.RESTORE_GATEWAY_SPEC';    -- created in sql/02
SET snapshot_table = $cookbook_db || '.GOV.GATEWAY_SPEC_SNAPSHOT';   -- created in sql/02

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE IDENTIFIER($cookbook_wh);

CALL IDENTIFIER($restore_proc)();

-- Independent check: the live spec hash equals the snapshot hash.
SHOW AI GATEWAYS;
SELECT g."name"                                   AS gateway,
       SHA2(g."specification") = s.spec_sha2      AS matches_snapshot,
       g."specification"                          AS live_specification
FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) g
JOIN IDENTIFIER($snapshot_table) s
  ON s.gateway_name = g."name";
```

### `sql/07_shared_resource_budget_optional.sql`

Copy code

```
-- OPTIONAL: shared resource budget for gateway spend by cost center.
-- Run as ACCOUNTADMIN. Idempotent.
--
-- A budget tracks the gateway spend of tagged users against a monthly limit and
-- notifies (or runs your stored procedure) at thresholds. It does not block, and
-- it is evaluated periodically: an action can run hours after the threshold is
-- crossed. Use the quota in sql/04 when usage must actually stop.

SET cookbook_db = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART';
SET cookbook_wh = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_WH';
SET cost_center_tag   = $cookbook_db || '.GOV.COST_CENTER';   -- created in sql/01
SET cost_center_value = 'cookbook_gateway_app';
SET monthly_credits = 50;

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA GOV;

CREATE SNOWFLAKE.CORE.BUDGET IF NOT EXISTS GATEWAY_APP_BUDGET();

-- Shared resources are attributed by user tag; a budget with no tags tracks nothing.
CALL GATEWAY_APP_BUDGET!SET_USER_TAGS(
  [[(SELECT SYSTEM$REFERENCE('TAG', $cost_center_tag, 'SESSION', 'APPLYBUDGET')),
    $cost_center_value]],
  'UNION');

CALL GATEWAY_APP_BUDGET!ADD_SHARED_RESOURCE('AI GATEWAY');
CALL GATEWAY_APP_BUDGET!SET_SPENDING_LIMIT($monthly_credits);

CALL GATEWAY_APP_BUDGET!GET_BUDGET_SCOPE();
```

### `sql/99_teardown.sql`

Copy code

```
-- Teardown: restore the gateway spec, remove the quota and budget, drop every object.
-- Run as ACCOUNTADMIN. Safe to rerun.
--
-- Every name below comes from this SET block, which matches sql/01 and sql/02.
-- Object names in this recipe are fixed; do not edit them here.

SET cookbook_db        = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART';
SET cookbook_wh        = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_WH';
SET app_role           = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_APP';
SET monitor_role       = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_MONITOR';
SET quota_admin_role   = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_QUOTA_ADMIN';
SET svc_user           = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_SVC';
SET svc_network_policy = 'COOKBOOK_GATEWAY_GOVERNANCE_QUICKSTART_SVC_POLICY';
SET gateway            = 'SNOWFLAKE';
SET gov_schema         = $cookbook_db || '.GOV';
SET restore_proc       = $cookbook_db || '.GOV.RESTORE_GATEWAY_SPEC';
SET snapshot_table     = $cookbook_db || '.GOV.GATEWAY_SPEC_SNAPSHOT';

USE ROLE ACCOUNTADMIN;
-- The checks below read SHOW output, which needs a warehouse. Dropped in step 5.
CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;
USE WAREHOUSE IDENTIFIER($cookbook_wh);

-- 1. Restore the gateway spec from the snapshot, then disable and drop the quota
--    and budget. If the restore does not confirm a hash match, this block raises
--    and the script stops with the database and snapshot intact, so you can fix
--    it and rerun. If the recipe database does not exist, or sql/02 never ran (no
--    snapshot, so sql/05 could not have changed the spec), there is nothing to
--    restore; the block says so and still drops the quota and budget.
EXECUTE IMMEDIATE $$
DECLARE
  restore_failed EXCEPTION (-20001, 'Gateway spec restore did not match the snapshot; teardown stopped and the snapshot kept. Run sql/06 to see why.');
  db           VARCHAR DEFAULT $cookbook_db;
  gov_schema   VARCHAR DEFAULT $gov_schema;
  restore_proc VARCHAR DEFAULT $restore_proc;
  procs_view   VARCHAR DEFAULT $cookbook_db || '.INFORMATION_SCHEMA.PROCEDURES';
  quota_admin_role VARCHAR DEFAULT $quota_admin_role;
  tables_view  VARCHAR DEFAULT $cookbook_db || '.INFORMATION_SCHEMA.TABLES';
  schemata_view VARCHAR DEFAULT $cookbook_db || '.INFORMATION_SCHEMA.SCHEMATA';
  msg          VARCHAR DEFAULT 'SKIPPED: recipe database not found, so there is no snapshot to restore';
  n            INTEGER;
  show_id      VARCHAR;
BEGIN
  SHOW DATABASES;
  show_id := SQLID;
  SELECT COUNT(*) INTO :n FROM TABLE(RESULT_SCAN(:show_id)) WHERE "name" = :db;
  IF (n = 1) THEN
    SELECT COUNT(*) INTO :n FROM IDENTIFIER(:procs_view)
      WHERE procedure_schema = 'GOV' AND procedure_name = 'RESTORE_GATEWAY_SPEC';
    IF (n > 0) THEN
      LET rs RESULTSET := (CALL IDENTIFIER(:restore_proc)());
      LET c CURSOR FOR rs;
      OPEN c;
      FETCH c INTO msg;
      CLOSE c;
      IF (msg IS NULL OR NOT STARTSWITH(msg, 'RESTORED')) THEN
        RAISE restore_failed;
      END IF;
    ELSE
      -- No restore procedure. A snapshot without it means sql/02 half ran: stop.
      SELECT COUNT(*) INTO :n FROM IDENTIFIER(:tables_view)
        WHERE table_schema = 'GOV' AND table_name = 'GATEWAY_SPEC_SNAPSHOT';
      IF (n > 0) THEN
        RAISE restore_failed;
      END IF;
      msg := 'SKIPPED: sql/02 never ran, so the gateway spec was never snapshotted or changed';
    END IF;
    SELECT COUNT(*) INTO :n FROM IDENTIFIER(:schemata_view) WHERE schema_name = 'GOV';
    IF (n > 0) THEN
      -- The quota admin role owns the quota. sql/01 grants it to SYSADMIN so that
      -- ACCOUNTADMIN inherits ownership; grant it again in case setup predates that.
      SHOW ROLES;
      show_id := SQLID;
      SELECT COUNT(*) INTO :n FROM TABLE(RESULT_SCAN(:show_id)) WHERE "name" = :quota_admin_role;
      IF (n = 1) THEN
        GRANT ROLE IDENTIFIER(:quota_admin_role) TO ROLE SYSADMIN;
      END IF;
      USE SCHEMA IDENTIFIER(:gov_schema);
      SHOW SNOWFLAKE.CORE.QUOTA;
      show_id := SQLID;
      SELECT COUNT(*) INTO :n FROM TABLE(RESULT_SCAN(:show_id))
        WHERE "name" = 'GATEWAY_APP_QUOTA' AND "database_name" = :db AND "schema_name" = 'GOV';
      IF (n > 0) THEN
        -- Release any block this quota placed, then drop it. Errors here stop
        -- teardown rather than being ignored.
        CALL GATEWAY_APP_QUOTA!SET_BLOCK_ENFORCEMENT_ENABLED(FALSE, FALSE);
        DROP SNOWFLAKE.CORE.QUOTA GATEWAY_APP_QUOTA;
      END IF;
      DROP SNOWFLAKE.CORE.BUDGET IF EXISTS GATEWAY_APP_BUDGET;
    END IF;
  END IF;
  RETURN msg;
END;
$$;

-- 2. The service user and its network policy. Dropping the user revokes its
--    token. The policy must be detached before it can be dropped, and dropped
--    before the database that holds its network rule.
ALTER USER IF EXISTS IDENTIFIER($svc_user) UNSET NETWORK_POLICY;
DROP USER IF EXISTS IDENTIFIER($svc_user);
DROP NETWORK POLICY IF EXISTS IDENTIFIER($svc_network_policy);

-- 3. The database, which holds the snapshot, the network rule, the tag and the
--    usage view. A second guard: it is dropped only if there is no snapshot, or
--    the live spec matches the snapshot. Otherwise this raises and the snapshot
--    stays, even if a client carried on past an error in step 1.
EXECUTE IMMEDIATE $$
DECLARE
  not_restored EXCEPTION (-20003, 'The live gateway spec does not match the snapshot; the recipe database and snapshot were kept. Run sql/06, then rerun teardown.');
  db             VARCHAR DEFAULT $cookbook_db;
  gw             VARCHAR DEFAULT $gateway;
  snapshot_table VARCHAR DEFAULT $snapshot_table;
  tables_view    VARCHAR DEFAULT $cookbook_db || '.INFORMATION_SCHEMA.TABLES';
  want_sha       VARCHAR;
  have_sha       VARCHAR;
  n              INTEGER;
  show_id        VARCHAR;
BEGIN
  SHOW DATABASES;
  show_id := SQLID;
  SELECT COUNT(*) INTO :n FROM TABLE(RESULT_SCAN(:show_id)) WHERE "name" = :db;
  IF (n = 0) THEN
    RETURN 'SKIPPED: recipe database not found';
  END IF;
  SELECT COUNT(*) INTO :n FROM IDENTIFIER(:tables_view)
    WHERE table_schema = 'GOV' AND table_name = 'GATEWAY_SPEC_SNAPSHOT';
  IF (n > 0) THEN
    SELECT spec_sha2 INTO :want_sha FROM IDENTIFIER(:snapshot_table) ORDER BY captured_at LIMIT 1;
    SHOW AI GATEWAYS;
    show_id := SQLID;
    SELECT SHA2("specification") INTO :have_sha FROM TABLE(RESULT_SCAN(:show_id)) WHERE "name" = :gw;
    IF (want_sha IS NOT NULL AND have_sha IS DISTINCT FROM want_sha) THEN
      RAISE not_restored;
    END IF;
  END IF;
  DROP DATABASE IDENTIFIER(:db);
  RETURN 'DROPPED: ' || db;
END;
$$;

-- 4. Roles. Dropping them removes their grants on the gateway.
DROP ROLE IF EXISTS IDENTIFIER($app_role);
DROP ROLE IF EXISTS IDENTIFIER($monitor_role);
DROP ROLE IF EXISTS IDENTIFIER($quota_admin_role);

-- 5. Confirm: no COOKBOOK_ grants remain on the gateway, and the spec is the one
--    you started with.
SHOW GRANTS ON AI GATEWAY SNOWFLAKE;
DESCRIBE AI GATEWAY SNOWFLAKE;

USE ROLE ACCOUNTADMIN;
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);
```
