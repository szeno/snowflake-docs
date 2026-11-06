# OAuth token passthrough to a Cortex Agent: code

Every file in the [OAuth token passthrough to a Cortex Agent](/developer-guide/cortex-ai-cookbook/oauth-token-passthrough) recipe. To run the recipe, download [oauth-token-passthrough.zip](/static/samples/cortex-ai-cookbook/oauth-token-passthrough.zip), unzip it, and run the scripts from the `oauth-token-passthrough/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/oauth-token-passthrough); the zip includes it as `README.md`.

## `client/`

### `client/passthrough_client.py`

Copy code

```
"""Relay a user's own token to a Cortex Agent (token passthrough).

The relay (a bot, an orchestrator, a web backend) receives the signed-in
user's Entra ID access token and forwards it unchanged as the bearer token on
the agent's :run endpoint. Snowflake validates the token against the External
OAuth security integration, maps its `upn` claim to a Snowflake user, and runs
the agent as that user. The relay holds no Snowflake credential of its own.

Environment:
  SNOWFLAKE_ACCOUNT_URL  https://<account_identifier>.snowflakecomputing.com
  USER_ACCESS_TOKEN      the user's access token (production: taken from the
                         signed-in session; never logged or stored)

Testing the Snowflake side before Entra ID is configured:
  --test-keypair-user USER --test-keypair-file KEY.p8 --account ACCOUNT
  mints a short-lived key-pair JWT for USER and sends it with token type
  KEYPAIR_JWT, so you can prove per-user results with the same request shape.

Usage:
  python passthrough_client.py "How many tickets can I see, and which are open?"
"""

import argparse
import base64
import hashlib
import os
import sys
import time

import requests

AGENT_DB = os.environ.get("AGENT_DATABASE", "COOKBOOK_OAUTH_TOKEN_PASSTHROUGH")
AGENT_SCHEMA = os.environ.get("AGENT_SCHEMA", "APP")
AGENT_NAME = os.environ.get("AGENT_NAME", "SUPPORT_TICKETS_AGENT")

def _require(value, what):
    """Stop with a clear message instead of a KeyError when a setting is missing."""
    if not value:
        sys.exit(f"missing {what}")
    return value

def keypair_jwt(account, user, key_file):
    import jwt
    from cryptography.hazmat.primitives import serialization

    with open(key_file, "rb") as f:
        key = serialization.load_pem_private_key(f.read(), password=None)
    pub = key.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    fp = "SHA256:" + base64.b64encode(hashlib.sha256(pub).digest()).decode()
    acct, usr, now = account.upper().split(".")[0], user.upper(), int(time.time())
    return jwt.encode(
        {"iss": f"{acct}.{usr}.{fp}", "sub": f"{acct}.{usr}", "iat": now, "exp": now + 600}, key, algorithm="RS256"
    )

def run_agent(question, token, token_type="OAUTH"):
    account_url = _require(
        os.environ.get("SNOWFLAKE_ACCOUNT_URL"),
        "SNOWFLAKE_ACCOUNT_URL: export https://<account_identifier>.snowflakecomputing.com",
    )
    url = f"{account_url.rstrip('/')}/api/v2/databases/{AGENT_DB}/schemas/{AGENT_SCHEMA}/agents/{AGENT_NAME}:run"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Snowflake-Authorization-Token-Type": token_type,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    body = {"messages": [{"role": "user", "content": [{"type": "text", "text": question}]}], "stream": False}
    return requests.post(url, headers=headers, json=body, timeout=300)

def answer_text(resp_json):
    return "\n".join(b.get("text", "") for b in resp_json.get("content", []) if b.get("type") == "text").strip()

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("question")
    p.add_argument("--test-keypair-user")
    p.add_argument("--test-keypair-file")
    p.add_argument("--account", default=os.environ.get("SNOWFLAKE_ACCOUNT"))
    args = p.parse_args()

    if args.test_keypair_user:
        account = _require(args.account, "--account or SNOWFLAKE_ACCOUNT for the key-pair test")
        key_file = _require(args.test_keypair_file, "--test-keypair-file for the key-pair test")
        token, token_type = keypair_jwt(account, args.test_keypair_user, key_file), "KEYPAIR_JWT"
    else:
        token = _require(os.environ.get("USER_ACCESS_TOKEN"), "USER_ACCESS_TOKEN: the signed-in user's access token")
        token_type = "OAUTH"

    r = run_agent(args.question, token, token_type)
    if r.status_code != 200:
        # 401: token invalid, expired, wrong audience, or no user with that LOGIN_NAME.
        sys.exit(f"HTTP {r.status_code}: {r.text[:500]}")
    data = r.json()
    print(answer_text(data))
    # Log this with your own request context; usage views carry a REQUEST_ID column.
    print(f"\n[request_id={r.headers.get('X-Snowflake-Request-Id')}]")

if __name__ == "__main__":
    main()
```

### `client/requirements.txt`

```
cryptography==45.0.7
PyJWT==2.15.1
requests==2.34.2
```

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- =============================================================================
-- 01_setup.sql  (run as ACCOUNTADMIN)
-- OAuth token passthrough: database, warehouse, roles, and the Snowflake users
-- that Entra ID identities map to.
--
-- Each person who calls the agent needs a Snowflake user whose LOGIN_NAME
-- equals the claim the security integration maps (here the Entra ID `upn`).
-- The three users below stand in for people provisioned by your IdP. Replace
-- the LOGIN_NAME values with real UPNs, or provision users with SCIM instead
-- (see README).
-- Idempotent.
-- =============================================================================

SET cookbook_db   = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH';
SET cookbook_wh   = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_WH';
SET admin_role    = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ADMIN';
SET analyst_role  = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST';
SET user_a        = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST_A';
SET user_b        = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST_B';
SET user_lead     = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_LEAD';
SET upn_a         = 'analyst.a@example.com';   -- replace with the Entra ID UPN
SET upn_b         = 'analyst.b@example.com';   -- replace with the Entra ID UPN
SET upn_lead      = 'support.lead@example.com'; -- replace with the Entra ID UPN
SET my_user       = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($admin_role)
  COMMENT = 'Cookbook oauth-token-passthrough: owns the recipe objects.';
GRANT ROLE IDENTIFIER($admin_role) TO USER IDENTIFIER($my_user);
GRANT ROLE IDENTIFIER($admin_role) TO ROLE SYSADMIN;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($admin_role);

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cookbook oauth-token-passthrough warehouse.';
GRANT OWNERSHIP ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($admin_role) COPY CURRENT GRANTS;

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db)
  COMMENT = 'Cookbook oauth-token-passthrough.';
GRANT OWNERSHIP ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($admin_role) COPY CURRENT GRANTS;

-- The one role every passthrough user runs as. Identity differs per user;
-- privileges do not. The row access policy in 03 makes results differ.
CREATE ROLE IF NOT EXISTS IDENTIFIER($analyst_role)
  COMMENT = 'Cookbook oauth-token-passthrough: role granted to every mapped user.';
GRANT ROLE IDENTIFIER($analyst_role) TO ROLE IDENTIFIER($admin_role);
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE IDENTIFIER($analyst_role);

-- Users that Entra ID tokens map to. No password: they authenticate with the
-- IdP token only. DEFAULT_ROLE and DEFAULT_WAREHOUSE are required for agent runs.
CREATE USER IF NOT EXISTS IDENTIFIER($user_a)    TYPE = PERSON COMMENT = 'Cookbook passthrough user: analyst A.';
CREATE USER IF NOT EXISTS IDENTIFIER($user_b)    TYPE = PERSON COMMENT = 'Cookbook passthrough user: analyst B.';
CREATE USER IF NOT EXISTS IDENTIFIER($user_lead) TYPE = PERSON COMMENT = 'Cookbook passthrough user: support lead.';

ALTER USER IDENTIFIER($user_a)    SET LOGIN_NAME = $upn_a    DEFAULT_ROLE = $analyst_role DEFAULT_WAREHOUSE = $cookbook_wh DEFAULT_SECONDARY_ROLES = ();
ALTER USER IDENTIFIER($user_b)    SET LOGIN_NAME = $upn_b    DEFAULT_ROLE = $analyst_role DEFAULT_WAREHOUSE = $cookbook_wh DEFAULT_SECONDARY_ROLES = ();
ALTER USER IDENTIFIER($user_lead) SET LOGIN_NAME = $upn_lead DEFAULT_ROLE = $analyst_role DEFAULT_WAREHOUSE = $cookbook_wh DEFAULT_SECONDARY_ROLES = ();

GRANT ROLE IDENTIFIER($analyst_role) TO USER IDENTIFIER($user_a);
GRANT ROLE IDENTIFIER($analyst_role) TO USER IDENTIFIER($user_b);
GRANT ROLE IDENTIFIER($analyst_role) TO USER IDENTIFIER($user_lead);

-- For the key-pair test in Verify only: lets the admin role set each user's
-- public key, and nothing else on the user.
GRANT MODIFY PROGRAMMATIC AUTHENTICATION METHODS ON USER IDENTIFIER($user_a)    TO ROLE IDENTIFIER($admin_role);
GRANT MODIFY PROGRAMMATIC AUTHENTICATION METHODS ON USER IDENTIFIER($user_b)    TO ROLE IDENTIFIER($admin_role);
GRANT MODIFY PROGRAMMATIC AUTHENTICATION METHODS ON USER IDENTIFIER($user_lead) TO ROLE IDENTIFIER($admin_role);

SHOW USERS LIKE 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH%';
```

### `sql/02_security_integration.sql`

Copy code

```
-- =============================================================================
-- 02_security_integration.sql  (run as ACCOUNTADMIN; account-level change)
-- External OAuth security integration for Microsoft Entra ID.
--
-- Snowflake validates each bearer token against this integration (issuer,
-- signing keys, audience, expiry), then maps the token's `upn` claim to a
-- Snowflake user's LOGIN_NAME. The session runs as that user.
--
-- Replace the three placeholders (<entra_tenant_id> twice,
-- <snowflake_application_id_uri> once) with the values from your Entra ID app
-- registration first (see README, Prerequisites). Values are case-sensitive,
-- including the trailing slash on the issuer. Snowflake rejects the statement
-- while the keys URL still holds the placeholder, so an unedited script
-- creates nothing. The last query lists any value that still holds one.
--
-- CREATE OR REPLACE, so running this again after you correct a value applies
-- the correction. IF NOT EXISTS would keep the first values. The integration
-- has no grants to keep.
--
-- EXTERNAL_OAUTH_ANY_ROLE_MODE is left at its default (DISABLE): the role comes
-- from the scope in the token, as configured in your Entra ID app registration,
-- and the session cannot switch to another role.
-- =============================================================================

SET integration_name = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ENTRA';
SET cookbook_wh      = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_WH';

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE IDENTIFIER($cookbook_wh);

CREATE OR REPLACE SECURITY INTEGRATION IDENTIFIER($integration_name)
  TYPE = EXTERNAL_OAUTH
  ENABLED = TRUE
  EXTERNAL_OAUTH_TYPE = AZURE
  EXTERNAL_OAUTH_ISSUER = 'https://sts.windows.net/<entra_tenant_id>/'
  EXTERNAL_OAUTH_JWS_KEYS_URL = 'https://login.microsoftonline.com/<entra_tenant_id>/discovery/v2.0/keys'
  EXTERNAL_OAUTH_AUDIENCE_LIST = ('<snowflake_application_id_uri>')
  EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = 'upn'
  EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'login_name'
  COMMENT = 'Cookbook oauth-token-passthrough: Entra ID tokens mapped to Snowflake users by UPN.';

DESCRIBE SECURITY INTEGRATION IDENTIFIER($integration_name);

-- Expect no rows. A row is a placeholder you missed: fix it and run 02 again.
-- Until then no token can validate, because its issuer or audience cannot match.
SELECT "property", "property_value" AS placeholder_still_set
FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
WHERE CONTAINS("property_value", '<');
```

### `sql/03_data_and_policy.sql`

Copy code

```
-- =============================================================================
-- 03_data_and_policy.sql  (run as COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ADMIN)
-- Support tickets, and a fail-closed row access policy on CURRENT_USER().
--
-- With token passthrough, every request runs as the person's own Snowflake
-- user, so CURRENT_USER() identifies them. The policy shows each analyst only
-- the tickets assigned to them, and shows everything to users listed as leads.
-- Anyone else sees nothing. All users share one role; the answer differs only
-- because the identity differs.
--
-- All data is synthetic. Idempotent.
-- =============================================================================

SET cookbook_db = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH';
SET cookbook_wh = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_WH';
SET admin_role  = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ADMIN';

USE ROLE IDENTIFIER($admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
CREATE SCHEMA IF NOT EXISTS APP;
USE SCHEMA APP;

CREATE TABLE IF NOT EXISTS SUPPORT_TICKETS (
  TICKET_ID     NUMBER      NOT NULL,
  ASSIGNED_TO   VARCHAR     NOT NULL,  -- Snowflake user name of the assignee
  PRIORITY      VARCHAR     NOT NULL,
  STATUS        VARCHAR     NOT NULL,
  CATEGORY      VARCHAR     NOT NULL,
  CREATED_DATE  DATE        NOT NULL,
  RESOLVED_DATE DATE,
  SATISFACTION  NUMBER(2, 1)
)
COMMENT = 'Northwind support tickets (synthetic).';

INSERT OVERWRITE INTO SUPPORT_TICKETS VALUES
  (5001, 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST_A', 'High',   'Resolved',    'Billing',   '2026-01-05', '2026-01-06', 4.5),
  (5002, 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST_A', 'Medium', 'Resolved',    'Technical', '2026-01-08', '2026-01-10', 3.8),
  (5003, 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST_A', 'High',   'Open',        'Technical', '2026-02-02', NULL,         NULL),
  (5004, 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST_A', 'Low',    'Resolved',    'General',   '2026-02-10', '2026-02-12', 4.2),
  (5005, 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST_B', 'High',   'Resolved',    'Technical', '2026-01-15', '2026-01-16', 4.8),
  (5006, 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST_B', 'Medium', 'In Progress', 'Billing',   '2026-02-20', NULL,         NULL),
  (5007, 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST_B', 'Low',    'Resolved',    'General',   '2026-03-01', '2026-03-04', 3.6),
  (5008, 'UNASSIGNED',                                'High',   'Open',        'Billing',   '2026-03-05', NULL,         NULL);

-- Who sees every ticket. Maintained by the data owner.
CREATE TABLE IF NOT EXISTS TICKET_LEADS (USER_NAME VARCHAR NOT NULL)
  COMMENT = 'Users who see all tickets. Everyone else sees only tickets assigned to them.';
INSERT OVERWRITE INTO TICKET_LEADS VALUES ('COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_LEAD');

CREATE ROW ACCESS POLICY IF NOT EXISTS TICKET_OWNER_POLICY
  AS (assigned_to VARCHAR) RETURNS BOOLEAN -> FALSE
  COMMENT = 'Fail closed: own tickets for the current user, all tickets for leads, nothing otherwise.';

ALTER ROW ACCESS POLICY TICKET_OWNER_POLICY SET BODY ->
  assigned_to = CURRENT_USER()
  OR EXISTS (SELECT 1 FROM COOKBOOK_OAUTH_TOKEN_PASSTHROUGH.APP.TICKET_LEADS l
             WHERE l.USER_NAME = CURRENT_USER());

ALTER TABLE SUPPORT_TICKETS DROP ALL ROW ACCESS POLICIES;
ALTER TABLE SUPPORT_TICKETS ADD ROW ACCESS POLICY TICKET_OWNER_POLICY ON (ASSIGNED_TO);

-- The admin is neither an assignee nor a lead, so it sees nothing.
SELECT COUNT(*) AS tickets_visible_to_admin FROM SUPPORT_TICKETS;
```

### `sql/04_agent.sql`

Copy code

```
-- =============================================================================
-- 04_agent.sql  (run as COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ADMIN)
-- Semantic view, agent, and the analyst role's grants.
--
-- Object names are fixed and appear as literals in the DDL below. The model is
-- the one value you may change: it lives in the agent specification under
-- models: orchestration.
-- =============================================================================

SET cookbook_db = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH';
SET cookbook_wh = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_WH';
SET admin_role  = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ADMIN';
SET analyst_role = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST';

USE ROLE IDENTIFIER($admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA APP;

CREATE OR ALTER SEMANTIC VIEW SUPPORT_TICKETS_SEMANTIC_VIEW
  TABLES (
    tickets AS COOKBOOK_OAUTH_TOKEN_PASSTHROUGH.APP.SUPPORT_TICKETS
      PRIMARY KEY (TICKET_ID)
      COMMENT = 'Support tickets visible to the current user.'
  )
  FACTS (
    tickets.satisfaction AS SATISFACTION COMMENT = 'Customer satisfaction, 1 to 5. NULL until resolved.'
  )
  DIMENSIONS (
    tickets.ticket_id AS TICKET_ID COMMENT = 'Ticket number.',
    tickets.assigned_to AS ASSIGNED_TO COMMENT = 'Assignee.',
    tickets.priority AS PRIORITY COMMENT = 'High, Medium, or Low.',
    tickets.status AS STATUS COMMENT = 'Open, In Progress, or Resolved.',
    tickets.category AS CATEGORY COMMENT = 'Billing, Technical, or General.',
    tickets.created_date AS CREATED_DATE COMMENT = 'Date the ticket was opened, in 2026.',
    tickets.resolved_date AS RESOLVED_DATE COMMENT = 'Date resolved. NULL while open.'
  )
  METRICS (
    tickets.ticket_count AS COUNT(tickets.ticket_id) COMMENT = 'Number of tickets.',
    tickets.avg_satisfaction AS ROUND(AVG(tickets.satisfaction), 1) COMMENT = 'Average satisfaction of resolved tickets.'
  )
  COMMENT = 'Support tickets the current user is allowed to see.';

CREATE OR REPLACE AGENT SUPPORT_TICKETS_AGENT
  COMMENT = 'Support analytics agent called with the end user''s own OAuth token.'
  PROFILE = '{"display_name": "Support Analytics"}'
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
  orchestration: Use ticket_analyst for every question about tickets.
  response: >-
    Answer concisely and list ticket numbers when there are five or fewer.
    If no tickets are returned, say that no tickets are visible to this user.
  sample_questions:
    - question: "How many tickets can I see, and which are open?"
tools:
  - tool_spec:
      type: cortex_analyst_text_to_sql
      name: ticket_analyst
      description: Support ticket counts, status, priority, category, dates, and satisfaction.
tool_resources:
  ticket_analyst:
    semantic_view: COOKBOOK_OAUTH_TOKEN_PASSTHROUGH.APP.SUPPORT_TICKETS_SEMANTIC_VIEW
    execution_environment:
      type: warehouse
      warehouse: COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_WH
      query_timeout: 60
$$;

-- One role for every passthrough user. No grants to PUBLIC.
GRANT USAGE  ON DATABASE IDENTIFIER($cookbook_db)                 TO ROLE IDENTIFIER($analyst_role);
GRANT USAGE  ON SCHEMA APP                                         TO ROLE IDENTIFIER($analyst_role);
GRANT USAGE  ON WAREHOUSE IDENTIFIER($cookbook_wh)                 TO ROLE IDENTIFIER($analyst_role);
GRANT USAGE  ON AGENT SUPPORT_TICKETS_AGENT                        TO ROLE IDENTIFIER($analyst_role);
GRANT SELECT ON SEMANTIC VIEW SUPPORT_TICKETS_SEMANTIC_VIEW        TO ROLE IDENTIFIER($analyst_role);
GRANT SELECT ON TABLE SUPPORT_TICKETS                              TO ROLE IDENTIFIER($analyst_role);

SHOW GRANTS TO ROLE IDENTIFIER($analyst_role);
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- 99_teardown.sql  (run as ACCOUNTADMIN)
-- Removes everything the recipe created, including the account-level External
-- OAuth security integration.
-- =============================================================================

SET cookbook_db      = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH';
SET cookbook_wh      = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_WH';
SET admin_role       = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ADMIN';
SET analyst_role     = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST';
SET user_a           = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST_A';
SET user_b           = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ANALYST_B';
SET user_lead        = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_LEAD';
SET integration_name = 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH_ENTRA';

USE ROLE ACCOUNTADMIN;

DROP SECURITY INTEGRATION IF EXISTS IDENTIFIER($integration_name);
DROP DATABASE  IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);
DROP USER IF EXISTS IDENTIFIER($user_a);
DROP USER IF EXISTS IDENTIFIER($user_b);
DROP USER IF EXISTS IDENTIFIER($user_lead);
DROP ROLE IF EXISTS IDENTIFIER($analyst_role);
DROP ROLE IF EXISTS IDENTIFIER($admin_role);

SHOW SECURITY INTEGRATIONS LIKE 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH%';
SHOW DATABASES  LIKE 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH%';
SHOW WAREHOUSES LIKE 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH%';
SHOW ROLES      LIKE 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH%';
SHOW USERS      LIKE 'COOKBOOK_OAUTH_TOKEN_PASSTHROUGH%';
```
