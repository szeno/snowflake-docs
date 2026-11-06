# Multi-tenant agents with session attributes and fail-closed policies: code

Every file in the [Multi-tenant agents with session attributes and fail-closed policies](/developer-guide/cortex-ai-cookbook/multi-tenant-agents) recipe. To run the recipe, download [multi-tenant-agents.zip](/static/samples/cortex-ai-cookbook/multi-tenant-agents.zip), unzip it, and run the scripts from the `multi-tenant-agents/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/multi-tenant-agents); the zip includes it as `README.md`.

## `client/`

### `client/requirements.txt`

```
cryptography==45.0.7
PyJWT==2.15.1
requests==2.34.2
snowflake-connector-python==3.17.4
```

### `client/tenant_client.py`

Copy code

```
"""App-server client for the multi-tenant agent.

Your application authenticates the end user with its own identity provider,
then calls the agent as ONE Snowflake service user, naming the end user in an
immutable session attribute. Snowflake's policies derive the tenant from that
end user's entitlement row. The client never sends a tenant ID.

Two paths:
  rest  POST /api/v2/databases/{db}/schemas/{schema}/agents/{agent}:run with
        a `variables` block (recommended for applications)
  sql   CALL SET_SYS_CONTEXT(...) then SNOWFLAKE.CORTEX.DATA_AGENT_RUN(...) on a
        fresh connection

Environment:
  SNOWFLAKE_ACCOUNT           account identifier, for example myorg-myaccount
  SNOWFLAKE_ACCOUNT_URL       https://<account_identifier>.snowflakecomputing.com
  SNOWFLAKE_USER              COOKBOOK_MULTI_TENANT_AGENTS_APP_SVC
  SNOWFLAKE_PRIVATE_KEY_FILE  path to the service user's unencrypted PKCS#8 key

Usage:
  python tenant_client.py --end-user u-acme-admin "What is total revenue by region?"
  python tenant_client.py --path sql --end-user u-northwind-ops "What is total revenue?"
"""

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time

import jwt
import requests
from cryptography.hazmat.primitives import serialization

AGENT_DB = os.environ.get("AGENT_DATABASE", "COOKBOOK_MULTI_TENANT_AGENTS")
AGENT_SCHEMA = os.environ.get("AGENT_SCHEMA", "APP")
AGENT_NAME = os.environ.get("AGENT_NAME", "ORDERS_AGENT")
ATTRIBUTE = "end_user_id"  # must match the key the policies read; keys are case-sensitive

# End-user IDs come from your IdP. Reject anything that is not a plain ID so a
# malformed value never reaches Snowflake.
END_USER_ID_PATTERN = re.compile(r"^[A-Za-z0-9._@-]{1,128}$")

def _private_key():
    with open(os.environ["SNOWFLAKE_PRIVATE_KEY_FILE"], "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def _keypair_jwt():
    """Key-pair JWT for the Snowflake REST API."""
    key = _private_key()
    pub = key.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    fingerprint = "SHA256:" + base64.b64encode(hashlib.sha256(pub).digest()).decode()
    account = os.environ["SNOWFLAKE_ACCOUNT"].upper().split(".")[0]
    user = os.environ["SNOWFLAKE_USER"].upper()
    now = int(time.time())
    claims = {"iss": f"{account}.{user}.{fingerprint}", "sub": f"{account}.{user}", "iat": now, "exp": now + 3000}
    return jwt.encode(claims, key, algorithm="RS256")

def _text(response):
    return "\n".join(b.get("text", "") for b in response.get("content", []) if b.get("type") == "text").strip()

def ask_rest(end_user_id, question):
    url = (
        f"{os.environ['SNOWFLAKE_ACCOUNT_URL'].rstrip('/')}/api/v2/databases/{AGENT_DB}"
        f"/schemas/{AGENT_SCHEMA}/agents/{AGENT_NAME}:run"
    )
    body = {
        "messages": [{"role": "user", "content": [{"type": "text", "text": question}]}],
        "variables": {
            ATTRIBUTE: {"value": end_user_id, "type": "string", "is_immutable_session_attribute": True},
        },
        "stream": False,
    }
    headers = {
        "Authorization": f"Bearer {_keypair_jwt()}",
        "X-Snowflake-Authorization-Token-Type": "KEYPAIR_JWT",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    r = requests.post(url, headers=headers, json=body, timeout=300)
    r.raise_for_status()
    return r.json()

def ask_sql(end_user_id, question):
    import snowflake.connector

    # One connection per request. Session attributes are immutable, so a pooled
    # connection that already served another end user cannot be reused: the
    # second SET_SYS_CONTEXT fails instead of switching users.
    conn = snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        private_key_file=os.environ["SNOWFLAKE_PRIVATE_KEY_FILE"],
        paramstyle="qmark",
    )
    try:
        cur = conn.cursor()
        cur.execute("CALL SET_SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', ?, ?)", (ATTRIBUTE, end_user_id))
        body = json.dumps({"messages": [{"role": "user", "content": [{"type": "text", "text": question}]}]})
        cur.execute("SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(?, ?)", (f"{AGENT_DB}.{AGENT_SCHEMA}.{AGENT_NAME}", body))
        return json.loads(cur.fetchone()[0])
    finally:
        conn.close()

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--end-user",
        required=True,
        help="Authenticated end-user ID from your IdP session (never from the request body)",
    )
    p.add_argument("--path", choices=["rest", "sql"], default="rest")
    p.add_argument("question")
    args = p.parse_args()

    if not END_USER_ID_PATTERN.match(args.end_user):
        sys.exit("invalid end-user ID")
    resp = ask_rest(args.end_user, args.question) if args.path == "rest" else ask_sql(args.end_user, args.question)
    if resp.get("code"):
        sys.exit(f"agent error {resp['code']}: {resp.get('message')}")
    print(_text(resp))

if __name__ == "__main__":
    main()
```

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- =============================================================================
-- 01_setup.sql  (run as ACCOUNTADMIN)
-- Multi-tenant agents: account-scoped setup.
--
-- Creates the database, warehouse, an admin role that owns the recipe objects,
-- an app role, and the app server's service user. The service user is the
-- only Snowflake identity your end users ever act through: the app server
-- authenticates them itself and tells Snowflake who they are with an
-- immutable session attribute.
--
-- The service user is TYPE = SERVICE with no credential. The admin role gets
-- MODIFY PROGRAMMATIC AUTHENTICATION METHODS on it, and nothing else on the
-- user, so you can attach a key pair as the admin role (README, Quickstart
-- step 6) without ACCOUNTADMIN.
-- Idempotent.
-- =============================================================================

SET cookbook_db = 'COOKBOOK_MULTI_TENANT_AGENTS';
SET cookbook_wh = 'COOKBOOK_MULTI_TENANT_AGENTS_WH';
SET admin_role  = 'COOKBOOK_MULTI_TENANT_AGENTS_ADMIN';
SET app_role    = 'COOKBOOK_MULTI_TENANT_AGENTS_APP';
SET app_user    = 'COOKBOOK_MULTI_TENANT_AGENTS_APP_SVC';
SET my_user     = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($admin_role)
  COMMENT = 'Cookbook multi-tenant-agents: owns the recipe objects.';
GRANT ROLE IDENTIFIER($admin_role) TO USER IDENTIFIER($my_user);
-- In the SYSADMIN hierarchy, so ACCOUNTADMIN can always manage and drop what it owns.
GRANT ROLE IDENTIFIER($admin_role) TO ROLE SYSADMIN;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($admin_role);

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cookbook multi-tenant-agents warehouse.';
GRANT OWNERSHIP ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($admin_role) COPY CURRENT GRANTS;

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db)
  COMMENT = 'Cookbook multi-tenant-agents.';
GRANT OWNERSHIP ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($admin_role) COPY CURRENT GRANTS;

-- App role: what the app server's service user runs as.
CREATE ROLE IF NOT EXISTS IDENTIFIER($app_role)
  COMMENT = 'Cookbook multi-tenant-agents: the app server role. Can run the agent; sees rows only for the end user named in the session.';
GRANT ROLE IDENTIFIER($app_role) TO ROLE IDENTIFIER($admin_role);
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE IDENTIFIER($app_role);

CREATE USER IF NOT EXISTS IDENTIFIER($app_user) TYPE = SERVICE
  COMMENT = 'Cookbook multi-tenant-agents: app server identity.';
ALTER USER IDENTIFIER($app_user) SET
  DEFAULT_ROLE = $app_role DEFAULT_WAREHOUSE = $cookbook_wh DEFAULT_SECONDARY_ROLES = ();
GRANT ROLE IDENTIFIER($app_role) TO USER IDENTIFIER($app_user);
-- Lets the admin role set the service user's public key. It cannot change the
-- user's roles or other properties.
GRANT MODIFY PROGRAMMATIC AUTHENTICATION METHODS ON USER IDENTIFIER($app_user)
  TO ROLE IDENTIFIER($admin_role);

SHOW USERS LIKE 'COOKBOOK_MULTI_TENANT_AGENTS%';
```

### `sql/02_data.sql`

Copy code

```
-- =============================================================================
-- 02_data.sql  (run as COOKBOOK_MULTI_TENANT_AGENTS_ADMIN)
-- Shared orders table for three tenants, plus the entitlements table that
-- binds end users to tenants.
--
-- Two schemas:
--   APP       what the agent can reach (orders, semantic view, agent)
--   SECURITY  entitlements; the app role has no privileges here. Policies read
--             it with their owner's rights.
--
-- All data is synthetic. Idempotent.
-- =============================================================================

SET cookbook_db = 'COOKBOOK_MULTI_TENANT_AGENTS';
SET cookbook_wh = 'COOKBOOK_MULTI_TENANT_AGENTS_WH';
SET admin_role  = 'COOKBOOK_MULTI_TENANT_AGENTS_ADMIN';

USE ROLE IDENTIFIER($admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);

CREATE SCHEMA IF NOT EXISTS APP      COMMENT = 'Objects the agent can reach.';
CREATE SCHEMA IF NOT EXISTS SECURITY COMMENT = 'Entitlements. No grants to the app role.';

-- ---------------------------------------------------------------------------
-- Orders: one table shared by every tenant, 10 orders per tenant.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS APP.ORDERS (
  TENANT_ID      VARCHAR       NOT NULL,
  ORDER_ID       VARCHAR       NOT NULL,
  ORDER_DATE     DATE          NOT NULL,
  REGION         VARCHAR       NOT NULL,
  PRODUCT        VARCHAR       NOT NULL,
  AMOUNT_USD     NUMBER(12, 2) NOT NULL,
  CUSTOMER_EMAIL VARCHAR       NOT NULL
)
COMMENT = 'Orders for all tenants (synthetic). Row access is filtered per end user.';

INSERT OVERWRITE INTO APP.ORDERS
WITH tenants AS (
  SELECT * FROM VALUES ('acme_health', 'acmehealth', 1000), ('northwind', 'northwind', 2000), ('contoso_bank', 'contosobank', 3000)
    AS t(tenant_id, domain, base)
),
n AS (SELECT SEQ4() + 1 AS i FROM TABLE(GENERATOR(ROWCOUNT => 10)))
SELECT
  t.tenant_id,
  UPPER(LEFT(t.tenant_id, 3)) || '-' || LPAD(n.i::VARCHAR, 3, '0'),
  DATEADD(day, n.i * 7, '2026-01-05'::DATE),
  CASE MOD(n.i, 3) WHEN 0 THEN 'North' WHEN 1 THEN 'South' ELSE 'West' END,
  CASE MOD(n.i, 2) WHEN 0 THEN 'Platform' ELSE 'Support plan' END,
  t.base + n.i * 100,
  'buyer' || n.i || '@' || t.domain || '.example.com'
FROM tenants t CROSS JOIN n;

-- ---------------------------------------------------------------------------
-- Entitlements: which end user belongs to which tenant, at which access level,
-- and which Snowflake service user is allowed to assert that end user.
-- Onboarding and offboarding an end user is an INSERT or DELETE here.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS SECURITY.TENANT_ENTITLEMENTS (
  END_USER_ID  VARCHAR NOT NULL,  -- the app's user ID, from its identity provider
  APP_USER     VARCHAR NOT NULL,  -- Snowflake user allowed to assert END_USER_ID
  TENANT_ID    VARCHAR NOT NULL,
  ACCESS_LEVEL VARCHAR NOT NULL   -- 'full' sees customer emails; 'summary' does not
)
COMMENT = 'End user -> tenant entitlements, bound to the app service user.';

INSERT OVERWRITE INTO SECURITY.TENANT_ENTITLEMENTS VALUES
  ('u-acme-admin',     'COOKBOOK_MULTI_TENANT_AGENTS_APP_SVC', 'acme_health',  'full'),
  ('u-acme-analyst',   'COOKBOOK_MULTI_TENANT_AGENTS_APP_SVC', 'acme_health',  'summary'),
  ('u-northwind-ops',  'COOKBOOK_MULTI_TENANT_AGENTS_APP_SVC', 'northwind',    'summary'),
  ('u-contoso-admin',  'COOKBOOK_MULTI_TENANT_AGENTS_APP_SVC', 'contoso_bank', 'full');

-- Expect 30 on the first run. Once 03 has attached the row access policy, the
-- admin sees 0 here as well: the policy fails closed for any session without
-- an entitled end user.
SELECT COUNT(*) AS orders_visible FROM APP.ORDERS;
```

### `sql/03_policies.sql`

Copy code

```
-- =============================================================================
-- 03_policies.sql  (run as COOKBOOK_MULTI_TENANT_AGENTS_ADMIN)
-- Tenant isolation: one fail-closed row access policy and one masking policy.
--
-- The tenant is never read from the client. The app server sets exactly one
-- immutable session attribute, end_user_id. The policy derives the tenant by
-- looking that end user up in SECURITY.TENANT_ENTITLEMENTS, and only accepts
-- the row if the entitlement also names the Snowflake user running the
-- session (CURRENT_USER()). So:
--   * no attribute                      -> no rows
--   * unknown end user                  -> no rows
--   * end user asserted by another user -> no rows
--   * a forged tenant_id attribute      -> ignored; the policy never reads one
--
-- Policies are created once and updated with SET BODY, so re-runs never need
-- to detach them. The table has exactly one row access policy.
-- =============================================================================

SET cookbook_db = 'COOKBOOK_MULTI_TENANT_AGENTS';
SET cookbook_wh = 'COOKBOOK_MULTI_TENANT_AGENTS_WH';
SET admin_role  = 'COOKBOOK_MULTI_TENANT_AGENTS_ADMIN';

USE ROLE IDENTIFIER($admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA APP;

-- ── Row access: tenant from the entitlement, never from the client ──────────
CREATE ROW ACCESS POLICY IF NOT EXISTS TENANT_ISOLATION_POLICY
  AS (tenant_col VARCHAR) RETURNS BOOLEAN -> FALSE
  COMMENT = 'Fail closed: a row is visible only to an entitled end user asserted by the bound app user.';

ALTER ROW ACCESS POLICY TENANT_ISOLATION_POLICY SET BODY ->
  EXISTS (
    SELECT 1
    FROM COOKBOOK_MULTI_TENANT_AGENTS.SECURITY.TENANT_ENTITLEMENTS e
    WHERE e.END_USER_ID = SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'end_user_id')
      AND e.APP_USER    = CURRENT_USER()
      AND e.TENANT_ID   = tenant_col
  );

-- Attach only if missing. Dropping and re-adding on a rerun would leave ORDERS
-- unprotected between the two statements. Any other row access policy on ORDERS
-- is an error, not "already attached".
EXECUTE IMMEDIATE $$
DECLARE
  unexpected_policy EXCEPTION (-20001, 'ORDERS has a row access policy other than TENANT_ISOLATION_POLICY; detach it and rerun.');
  ours INTEGER;
  other INTEGER;
BEGIN
  SELECT COUNT(IFF(POLICY_NAME = 'TENANT_ISOLATION_POLICY', 1, NULL)),
         COUNT(IFF(POLICY_NAME <> 'TENANT_ISOLATION_POLICY', 1, NULL))
    INTO :ours, :other
    FROM TABLE(INFORMATION_SCHEMA.POLICY_REFERENCES(
      REF_ENTITY_NAME => 'COOKBOOK_MULTI_TENANT_AGENTS.APP.ORDERS', REF_ENTITY_DOMAIN => 'TABLE'))
   WHERE POLICY_KIND = 'ROW_ACCESS_POLICY';
  IF (other > 0) THEN
    RAISE unexpected_policy;
  END IF;
  IF (ours = 0) THEN
    ALTER TABLE COOKBOOK_MULTI_TENANT_AGENTS.APP.ORDERS
      ADD ROW ACCESS POLICY TENANT_ISOLATION_POLICY ON (TENANT_ID);
    RETURN 'Row access policy attached';
  END IF;
  RETURN 'Row access policy already attached';
END;
$$;

-- ── Masking: customer emails only for 'full' end users ──────────────────────
CREATE MASKING POLICY IF NOT EXISTS CUSTOMER_EMAIL_MASK
  AS (val VARCHAR) RETURNS VARCHAR -> '***MASKED***'
  COMMENT = 'Fail closed: emails are masked unless the end user has ACCESS_LEVEL = full.';

ALTER MASKING POLICY CUSTOMER_EMAIL_MASK SET BODY ->
  CASE
    WHEN EXISTS (
      SELECT 1
      FROM COOKBOOK_MULTI_TENANT_AGENTS.SECURITY.TENANT_ENTITLEMENTS e
      WHERE e.END_USER_ID  = SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'end_user_id')
        AND e.APP_USER     = CURRENT_USER()
        AND e.ACCESS_LEVEL = 'full'
    ) THEN val
    ELSE '***MASKED***'
  END;

ALTER TABLE ORDERS MODIFY COLUMN CUSTOMER_EMAIL SET MASKING POLICY CUSTOMER_EMAIL_MASK FORCE;

-- Verify: this session has no end_user_id attribute, so it sees nothing.
SELECT COUNT(*) AS rows_visible_without_attribute FROM ORDERS;

-- Coverage check: every table the agent can read should have a policy.
SELECT POLICY_NAME, POLICY_KIND, REF_COLUMN_NAME
FROM TABLE(INFORMATION_SCHEMA.POLICY_REFERENCES(
  REF_ENTITY_NAME => 'COOKBOOK_MULTI_TENANT_AGENTS.APP.ORDERS', REF_ENTITY_DOMAIN => 'TABLE'));
```

### `sql/04_agent.sql`

Copy code

```
-- =============================================================================
-- 04_agent.sql  (run as COOKBOOK_MULTI_TENANT_AGENTS_ADMIN)
-- One semantic view and one agent, shared by every tenant.
--
-- Nothing in the agent knows about tenants. Isolation is entirely in the
-- policies (03), which apply to whatever SQL the agent generates.
--
-- CREATE OR ALTER keeps grants on the semantic view; CREATE OR REPLACE ...
-- COPY GRANTS keeps grants on the agent. Object names are fixed and appear as
-- literals in the DDL below. The model is the one value you may change: it
-- lives in the agent specification under models: orchestration.
-- =============================================================================

SET cookbook_db = 'COOKBOOK_MULTI_TENANT_AGENTS';
SET cookbook_wh = 'COOKBOOK_MULTI_TENANT_AGENTS_WH';
SET admin_role  = 'COOKBOOK_MULTI_TENANT_AGENTS_ADMIN';

USE ROLE IDENTIFIER($admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA APP;

CREATE OR ALTER SEMANTIC VIEW ORDERS_SEMANTIC_VIEW
  TABLES (
    orders AS COOKBOOK_MULTI_TENANT_AGENTS.APP.ORDERS
      PRIMARY KEY (ORDER_ID)
      COMMENT = 'One row per order. Only the current customer''s orders are visible.'
  )
  FACTS (
    orders.amount AS AMOUNT_USD COMMENT = 'Order amount in USD.'
  )
  DIMENSIONS (
    orders.order_id AS ORDER_ID COMMENT = 'Order identifier.',
    orders.order_date AS ORDER_DATE COMMENT = 'Date the order was placed, in 2026.',
    orders.region AS REGION COMMENT = 'Sales region: North, South, or West.',
    orders.product AS PRODUCT COMMENT = 'Product: Platform or Support plan.',
    orders.customer_email AS CUSTOMER_EMAIL COMMENT = 'Buyer email. May be masked for some users.'
  )
  METRICS (
    orders.total_revenue AS SUM(orders.amount)
      WITH SYNONYMS = ('revenue', 'sales', 'total sales')
      COMMENT = 'Total order amount in USD.',
    orders.order_count AS COUNT(orders.order_id)
      COMMENT = 'Number of orders.'
  )
  COMMENT = 'Orders for the current customer account.';

CREATE OR REPLACE AGENT ORDERS_AGENT
  COMMENT = 'Multi-tenant orders agent. Tenant isolation is enforced by row access and masking policies.'
  PROFILE = '{"display_name": "Orders Assistant"}'
  COPY GRANTS
  FROM SPECIFICATION
$$
models:
  orchestration: claude-sonnet-4-6   # the model: change it here
orchestration:
  budget:
    seconds: 120
    tokens: 40000
instructions:
  orchestration: >-
    Use orders_analyst for every question about orders, revenue, regions,
    products, or buyers.
  response: >-
    Answer concisely and lead with the number. If the data returns no rows,
    say that no orders are available for this account; do not guess.
  sample_questions:
    - question: "What is total revenue by region?"
tools:
  - tool_spec:
      type: cortex_analyst_text_to_sql
      name: orders_analyst
      description: Orders, revenue, regions, products, and buyer emails for the current customer account.
tool_resources:
  orders_analyst:
    semantic_view: COOKBOOK_MULTI_TENANT_AGENTS.APP.ORDERS_SEMANTIC_VIEW
    execution_environment:
      type: warehouse
      warehouse: COOKBOOK_MULTI_TENANT_AGENTS_WH
      query_timeout: 60
$$;

SHOW AGENTS IN SCHEMA APP;
```

### `sql/05_grants.sql`

Copy code

```
-- =============================================================================
-- 05_grants.sql  (run as COOKBOOK_MULTI_TENANT_AGENTS_ADMIN; re-run after 04)
-- The app role can run the agent and read the orders table through the
-- policies. It has no privileges on the SECURITY schema, so the agent cannot
-- read or change entitlements.
-- =============================================================================

SET cookbook_db = 'COOKBOOK_MULTI_TENANT_AGENTS';
SET cookbook_wh = 'COOKBOOK_MULTI_TENANT_AGENTS_WH';
SET admin_role  = 'COOKBOOK_MULTI_TENANT_AGENTS_ADMIN';
SET app_role    = 'COOKBOOK_MULTI_TENANT_AGENTS_APP';

USE ROLE IDENTIFIER($admin_role);
USE DATABASE IDENTIFIER($cookbook_db);

GRANT USAGE  ON DATABASE IDENTIFIER($cookbook_db)          TO ROLE IDENTIFIER($app_role);
GRANT USAGE  ON SCHEMA APP                                  TO ROLE IDENTIFIER($app_role);
GRANT USAGE  ON WAREHOUSE IDENTIFIER($cookbook_wh)          TO ROLE IDENTIFIER($app_role);
GRANT USAGE  ON AGENT APP.ORDERS_AGENT                      TO ROLE IDENTIFIER($app_role);
GRANT SELECT ON SEMANTIC VIEW APP.ORDERS_SEMANTIC_VIEW      TO ROLE IDENTIFIER($app_role);
-- Cortex Analyst runs its generated SQL against the base table as the caller.
GRANT SELECT ON TABLE APP.ORDERS                            TO ROLE IDENTIFIER($app_role);

SHOW GRANTS TO ROLE IDENTIFIER($app_role);
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- 99_teardown.sql  (run as ACCOUNTADMIN)
-- Removes everything the recipe created. Dropping the database removes the
-- agent, semantic view, policies, and tables.
-- =============================================================================

SET cookbook_db = 'COOKBOOK_MULTI_TENANT_AGENTS';
SET cookbook_wh = 'COOKBOOK_MULTI_TENANT_AGENTS_WH';
SET admin_role  = 'COOKBOOK_MULTI_TENANT_AGENTS_ADMIN';
SET app_role    = 'COOKBOOK_MULTI_TENANT_AGENTS_APP';
SET app_user    = 'COOKBOOK_MULTI_TENANT_AGENTS_APP_SVC';

USE ROLE ACCOUNTADMIN;

DROP DATABASE  IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);
DROP USER      IF EXISTS IDENTIFIER($app_user);
DROP ROLE      IF EXISTS IDENTIFIER($app_role);
DROP ROLE      IF EXISTS IDENTIFIER($admin_role);

SHOW DATABASES  LIKE 'COOKBOOK_MULTI_TENANT_AGENTS%';
SHOW WAREHOUSES LIKE 'COOKBOOK_MULTI_TENANT_AGENTS%';
SHOW ROLES      LIKE 'COOKBOOK_MULTI_TENANT_AGENTS%';
SHOW USERS      LIKE 'COOKBOOK_MULTI_TENANT_AGENTS%';
```
