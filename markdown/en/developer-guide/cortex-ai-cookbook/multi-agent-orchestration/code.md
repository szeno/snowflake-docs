# Multi-agent orchestration with a CoWork profile: code

Every file in the [Multi-agent orchestration with a CoWork profile](/developer-guide/cortex-ai-cookbook/multi-agent-orchestration) recipe. To run the recipe, download [multi-agent-orchestration.zip](/static/samples/cortex-ai-cookbook/multi-agent-orchestration.zip), unzip it, and run the scripts from the `multi-agent-orchestration/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/multi-agent-orchestration); the zip includes it as `README.md`.

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- =============================================================================
-- 01_setup.sql  (run as ACCOUNTADMIN)
-- Multi-agent orchestration: account-scoped setup.
--
-- Creates the recipe database, warehouse, an admin role that owns the recipe
-- objects, three persona roles, and three persona service users. The front-door
-- profile lives in the recipe's own schema, so no grants outside it are needed.
-- These are the only statements in the recipe that need ACCOUNTADMIN.
-- Everything after this file runs as COOKBOOK_MULTI_AGENT_ADMIN.
--
-- The persona users are TYPE = SERVICE with no password and no key, so nobody
-- can sign in as them until you attach a key pair or a PAT (see README, Verify).
-- They exist because Cortex Agents authorize a run against the calling user's
-- DEFAULT role, so the persona boundary is only testable as a user whose
-- default role is the persona role.
--
-- Idempotent.
-- =============================================================================

SET cookbook_db    = 'COOKBOOK_MULTI_AGENT';
SET cookbook_wh    = 'COOKBOOK_MULTI_AGENT_WH';
SET admin_role     = 'COOKBOOK_MULTI_AGENT_ADMIN';
SET sales_global   = 'COOKBOOK_MULTI_AGENT_SALES_GLOBAL';
SET sales_emea     = 'COOKBOOK_MULTI_AGENT_SALES_EMEA';
SET support_role   = 'COOKBOOK_MULTI_AGENT_SUPPORT';
SET sales_global_u = 'COOKBOOK_MULTI_AGENT_SALES_GLOBAL_USER';
SET sales_emea_u   = 'COOKBOOK_MULTI_AGENT_SALES_EMEA_USER';
SET support_u      = 'COOKBOOK_MULTI_AGENT_SUPPORT_USER';
SET my_user        = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

-- ---------------------------------------------------------------------------
-- Admin role: owns every recipe object. Granted to you so you can run 02-07.
-- ---------------------------------------------------------------------------
CREATE ROLE IF NOT EXISTS IDENTIFIER($admin_role)
  COMMENT = 'Cookbook multi-agent-orchestration: owns the recipe objects.';
GRANT ROLE IDENTIFIER($admin_role) TO USER IDENTIFIER($my_user);
-- In the SYSADMIN hierarchy, so ACCOUNTADMIN can always manage and drop what it owns.
GRANT ROLE IDENTIFIER($admin_role) TO ROLE SYSADMIN;

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cookbook multi-agent-orchestration warehouse.';
GRANT OWNERSHIP ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($admin_role) COPY CURRENT GRANTS;

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db)
  COMMENT = 'Cookbook multi-agent-orchestration.';
GRANT OWNERSHIP ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($admin_role) COPY CURRENT GRANTS;

GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($admin_role);
-- Agent evaluations (07) run on serverless tasks.
GRANT EXECUTE TASK ON ACCOUNT TO ROLE IDENTIFIER($admin_role);

-- ---------------------------------------------------------------------------
-- Persona roles. Granted to the admin role so it can manage their grants.
-- ---------------------------------------------------------------------------
CREATE ROLE IF NOT EXISTS IDENTIFIER($sales_global)
  COMMENT = 'Persona: global sales exec. Reaches the sales specialist, all theaters.';
CREATE ROLE IF NOT EXISTS IDENTIFIER($sales_emea)
  COMMENT = 'Persona: EMEA seller. Reaches the sales specialist, EMEA rows only.';
CREATE ROLE IF NOT EXISTS IDENTIFIER($support_role)
  COMMENT = 'Persona: support rep. Reaches the support specialist only.';

GRANT ROLE IDENTIFIER($sales_global) TO ROLE IDENTIFIER($admin_role);
GRANT ROLE IDENTIFIER($sales_emea)   TO ROLE IDENTIFIER($admin_role);
GRANT ROLE IDENTIFIER($support_role) TO ROLE IDENTIFIER($admin_role);

GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE IDENTIFIER($sales_global);
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE IDENTIFIER($sales_emea);
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE IDENTIFIER($support_role);

-- ---------------------------------------------------------------------------
-- Persona users. DEFAULT_ROLE and DEFAULT_WAREHOUSE are load-bearing: agent
-- runs authorize against the default role, and fail without a default
-- warehouse the default role can use. DEFAULT_SECONDARY_ROLES = () keeps the
-- session to exactly one role, so the row access policy sees one role.
-- ---------------------------------------------------------------------------
CREATE USER IF NOT EXISTS IDENTIFIER($sales_global_u) TYPE = SERVICE
  COMMENT = 'Cookbook persona: global sales exec.';
CREATE USER IF NOT EXISTS IDENTIFIER($sales_emea_u) TYPE = SERVICE
  COMMENT = 'Cookbook persona: EMEA seller.';
CREATE USER IF NOT EXISTS IDENTIFIER($support_u) TYPE = SERVICE
  COMMENT = 'Cookbook persona: support rep.';

-- Re-assert on every run: CREATE USER IF NOT EXISTS does not update an existing user.
ALTER USER IDENTIFIER($sales_global_u) SET DEFAULT_ROLE = $sales_global DEFAULT_WAREHOUSE = $cookbook_wh DEFAULT_SECONDARY_ROLES = ();
ALTER USER IDENTIFIER($sales_emea_u)   SET DEFAULT_ROLE = $sales_emea   DEFAULT_WAREHOUSE = $cookbook_wh DEFAULT_SECONDARY_ROLES = ();
ALTER USER IDENTIFIER($support_u)      SET DEFAULT_ROLE = $support_role DEFAULT_WAREHOUSE = $cookbook_wh DEFAULT_SECONDARY_ROLES = ();

GRANT ROLE IDENTIFIER($sales_global) TO USER IDENTIFIER($sales_global_u);
GRANT ROLE IDENTIFIER($sales_emea)   TO USER IDENTIFIER($sales_emea_u);
GRANT ROLE IDENTIFIER($support_role) TO USER IDENTIFIER($support_u);

SHOW USERS LIKE 'COOKBOOK_MULTI_AGENT%';
```

### `sql/02_data.sql`

Copy code

```
-- =============================================================================
-- 02_data.sql  (run as COOKBOOK_MULTI_AGENT_ADMIN)
-- Schema, sample data for the two specialist domains.
--
-- SALES_BOOKINGS is stored at a single grain (one row per territory per fiscal
-- quarter), so SUM and AVG are always correct and no row is a pre-aggregated
-- roll-up. If your real table mixes grains, see the mixed-grain recipe linked
-- in the README before you point an agent at it.
--
-- All data is synthetic. Idempotent: CREATE TABLE IF NOT EXISTS plus INSERT
-- OVERWRITE keeps grants and the row access policy attachment on re-runs.
-- =============================================================================

SET cookbook_db     = 'COOKBOOK_MULTI_AGENT';
SET cookbook_schema = 'COOKBOOK_MULTI_AGENT.APP';
SET cookbook_wh     = 'COOKBOOK_MULTI_AGENT_WH';
SET admin_role      = 'COOKBOOK_MULTI_AGENT_ADMIN';

USE ROLE IDENTIFIER($admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);

CREATE SCHEMA IF NOT EXISTS IDENTIFIER($cookbook_schema)
  COMMENT = 'Cookbook multi-agent-orchestration objects.';
USE SCHEMA IDENTIFIER($cookbook_schema);

-- ---------------------------------------------------------------------------
-- Sales domain: one row per territory per fiscal quarter. Values in USD millions.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS SALES_BOOKINGS (
  FISCAL_QUARTER     VARCHAR(10)   NOT NULL,
  THEATER            VARCHAR(20)   NOT NULL,
  TERRITORY          VARCHAR(40)   NOT NULL,
  NEW_BOOKINGS_USD_M NUMBER(10, 2) NOT NULL,
  TARGET_USD_M       NUMBER(10, 2) NOT NULL,
  PIPELINE_USD_M     NUMBER(10, 2) NOT NULL
)
COMMENT = 'Northwind Software sales bookings (synthetic). One row per territory per fiscal quarter.';

INSERT OVERWRITE INTO SALES_BOOKINGS
WITH quarters AS (
  SELECT * FROM VALUES ('FY25-Q1', 1.00), ('FY25-Q2', 1.05), ('FY25-Q3', 1.10), ('FY25-Q4', 1.20)
    AS q(fiscal_quarter, growth)
),
territories AS (
  SELECT * FROM VALUES
    ('Americas', 'West',          20.0, 0.97),
    ('Americas', 'East',          16.0, 1.04),
    ('Americas', 'Central',        9.0, 0.91),
    ('Americas', 'LATAM',          5.0, 1.08),
    ('EMEA',     'UK and Ireland', 12.0, 1.02),
    ('EMEA',     'DACH',          10.0, 0.94),
    ('EMEA',     'France',         6.0, 1.06),
    ('EMEA',     'Nordics',        4.0, 0.99),
    ('APAC',     'ANZ',            7.0, 1.03),
    ('APAC',     'Japan',          6.0, 0.95),
    ('APAC',     'Southeast Asia', 5.0, 1.10)
    AS t(theater, territory, base_target, attainment)
)
SELECT
  q.fiscal_quarter,
  t.theater,
  t.territory,
  ROUND(t.base_target * q.growth * t.attainment, 2) AS new_bookings_usd_m,
  ROUND(t.base_target * q.growth, 2)                AS target_usd_m,
  ROUND(t.base_target * q.growth * 3.0, 2)          AS pipeline_usd_m
FROM quarters q CROSS JOIN territories t;

-- ---------------------------------------------------------------------------
-- Support domain: product knowledge base articles.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS SUPPORT_KB (
  ARTICLE_ID VARCHAR(10) NOT NULL,
  TITLE      VARCHAR     NOT NULL,
  CATEGORY   VARCHAR(40) NOT NULL,
  CONTENT    VARCHAR     NOT NULL
)
COMMENT = 'Northwind Software support knowledge base (synthetic).';

INSERT OVERWRITE INTO SUPPORT_KB VALUES
  ('KB-001', 'Set up single sign-on with SAML 2.0', 'Authentication',
   'Go to Settings > Security > SSO, choose your identity provider, and paste its metadata URL. Map the SAML NameID to the user email attribute. Test with one admin account before you enable "Require SSO for all members", to avoid locking everyone out.'),
  ('KB-002', 'Generate and use API tokens', 'API',
   'Create a token under Settings > Developer > API Tokens. Tokens are scoped (read, write, admin) and expire after 90 days. Send the token in the Authorization header as "Bearer <token>". Revoking a token invalidates it immediately.'),
  ('KB-003', 'Troubleshoot 401 and 403 API errors', 'API',
   'A 401 means authentication failed: check the Authorization header format, and confirm the token has not expired or been revoked. A 403 means the token is valid but lacks the scope for that endpoint: create a token with the right scope. Rate-limited requests return 429, not 401.'),
  ('KB-004', 'Understand your invoice and seat count', 'Billing',
   'Invoices are generated monthly from the active seats on the billing date. A seat is any member with a non-Viewer role. Moving a member to Viewer reduces billed seats from the next cycle.'),
  ('KB-005', 'Schedule a recurring data export', 'Data management',
   'Use Settings > Data > Scheduled Exports to deliver CSV or JSON files daily or weekly to a cloud storage bucket. Exports respect the requesting member role: Viewers export only the data they can see.'),
  ('KB-006', 'Reset a password', 'Authentication',
   'Use "Forgot password" on the sign-in page to receive a reset link, valid for 60 minutes. If SSO is enforced, password reset is disabled and you recover access through your identity provider.'),
  ('KB-007', 'Why a dashboard loads slowly', 'Performance',
   'Slow dashboards are usually caused by very wide date ranges or unfiltered high-cardinality views. Narrow the date range, add filters, and keep a single view under 50,000 rows. Use scheduled reports for large extracts.'),
  ('KB-008', 'Review audit logs', 'Administration',
   'Admins see sign-ins, permission changes, exports, and token activity under Settings > Security > Audit Log. Logs are retained for 90 days, or one year on the Enterprise plan.');

SELECT THEATER, COUNT(*) AS ROWS_LOADED, SUM(NEW_BOOKINGS_USD_M) AS BOOKINGS_USD_M
FROM SALES_BOOKINGS GROUP BY THEATER ORDER BY THEATER;
```

### `sql/03_semantic_views.sql`

Copy code

```
-- =============================================================================
-- 03_semantic_views.sql  (run as COOKBOOK_MULTI_AGENT_ADMIN)
-- One semantic view per specialist. Each specialist agent gets a Cortex Analyst
-- tool over exactly one of these, which keeps each domain's context small.
--
-- CREATE OR ALTER keeps grants on re-runs.
-- Names inside the DDL are literals. Object names are fixed; do not rename them.
-- =============================================================================

SET cookbook_schema = 'COOKBOOK_MULTI_AGENT.APP';
SET cookbook_wh     = 'COOKBOOK_MULTI_AGENT_WH';
SET admin_role      = 'COOKBOOK_MULTI_AGENT_ADMIN';

USE ROLE IDENTIFIER($admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($cookbook_schema);

CREATE OR ALTER SEMANTIC VIEW SALES_SEMANTIC_VIEW
  TABLES (
    bookings AS COOKBOOK_MULTI_AGENT.APP.SALES_BOOKINGS
      PRIMARY KEY (FISCAL_QUARTER, TERRITORY)
      COMMENT = 'One row per sales territory per fiscal quarter. Values are in USD millions.'
  )
  FACTS (
    bookings.new_bookings AS NEW_BOOKINGS_USD_M
      COMMENT = 'New bookings for the territory and quarter, USD millions.',
    bookings.target AS TARGET_USD_M
      COMMENT = 'Bookings target for the territory and quarter, USD millions.',
    bookings.pipeline AS PIPELINE_USD_M
      COMMENT = 'Open pipeline for the territory and quarter, USD millions.'
  )
  DIMENSIONS (
    bookings.fiscal_quarter AS FISCAL_QUARTER
      WITH SYNONYMS = ('quarter', 'fiscal period')
      COMMENT = 'Fiscal quarter, FY25-Q1 through FY25-Q4.',
    bookings.theater AS THEATER
      WITH SYNONYMS = ('region', 'geo')
      COMMENT = 'Sales theater: Americas, EMEA, or APAC.',
    bookings.territory AS TERRITORY
      COMMENT = 'Sales territory within a theater.'
  )
  METRICS (
    bookings.total_new_bookings AS SUM(bookings.new_bookings)
      WITH SYNONYMS = ('bookings', 'new bookings')
      COMMENT = 'Total new bookings, USD millions.',
    bookings.total_target AS SUM(bookings.target)
      COMMENT = 'Total bookings target, USD millions.',
    bookings.total_pipeline AS SUM(bookings.pipeline)
      COMMENT = 'Total open pipeline, USD millions.',
    bookings.attainment_pct AS ROUND(100 * SUM(bookings.new_bookings) / NULLIF(SUM(bookings.target), 0), 1)
      WITH SYNONYMS = ('attainment', 'percent of target')
      COMMENT = 'New bookings as a percentage of target.'
  )
  COMMENT = 'Northwind Software sales bookings, pipeline, and targets by quarter, theater, and territory.';

CREATE OR ALTER SEMANTIC VIEW SUPPORT_SEMANTIC_VIEW
  TABLES (
    kb AS COOKBOOK_MULTI_AGENT.APP.SUPPORT_KB
      PRIMARY KEY (ARTICLE_ID)
      COMMENT = 'One row per support knowledge base article.'
  )
  DIMENSIONS (
    kb.article_id AS ARTICLE_ID
      COMMENT = 'Article identifier, for example KB-003.',
    kb.title AS TITLE
      COMMENT = 'Article title.',
    kb.category AS CATEGORY
      COMMENT = 'Article category: Authentication, API, Billing, Data management, Performance, Administration.',
    kb.content AS CONTENT
      WITH SYNONYMS = ('instructions', 'steps', 'article body')
      COMMENT = 'Full article text with the step-by-step answer.'
  )
  METRICS (
    kb.article_count AS COUNT(kb.article_id)
      COMMENT = 'Number of articles.'
  )
  COMMENT = 'Northwind Software support knowledge base. Answer how-to questions from CONTENT.';

SHOW SEMANTIC VIEWS IN SCHEMA IDENTIFIER($cookbook_schema);
```

### `sql/04_row_access_policy.sql`

Copy code

```
-- =============================================================================
-- 04_row_access_policy.sql  (run as COOKBOOK_MULTI_AGENT_ADMIN)
-- One fail-closed row access policy on SALES_BOOKINGS.
--
-- Two questions, two mechanisms:
--   * Which specialist can a persona reach?   -> USAGE grants on the agents (06)
--   * Which rows does the sales specialist return for that persona? -> this file
--
-- The policy looks the caller's role up in SALES_ENTITLEMENTS. A role with no
-- row sees no rows (fail closed). 'ALL' grants every theater. The table has
-- exactly one row access policy: re-runs update the body in place and never
-- attach a second policy.
--
-- Why CURRENT_ROLE(): an agent run executes tool queries under one primary
-- role (the user's default role, or the X-Snowflake-Role override on REST).
-- Keying on the primary role means the answer depends on that single role and
-- not on whatever secondary roles the user happens to hold.
-- =============================================================================

SET cookbook_schema = 'COOKBOOK_MULTI_AGENT.APP';
SET cookbook_wh     = 'COOKBOOK_MULTI_AGENT_WH';
SET admin_role      = 'COOKBOOK_MULTI_AGENT_ADMIN';

USE ROLE IDENTIFIER($admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($cookbook_schema);

-- Entitlements: role -> theater. Maintained by the data owner, not by the app.
CREATE TABLE IF NOT EXISTS SALES_ENTITLEMENTS (
  ROLE_NAME VARCHAR NOT NULL,
  THEATER   VARCHAR NOT NULL   -- a THEATER value, or 'ALL'
)
COMMENT = 'Row access entitlements for SALES_BOOKINGS. No row for a role = no data.';

INSERT OVERWRITE INTO SALES_ENTITLEMENTS VALUES
  ('COOKBOOK_MULTI_AGENT_ADMIN',        'ALL'),
  ('COOKBOOK_MULTI_AGENT_SALES_GLOBAL', 'ALL'),
  ('COOKBOOK_MULTI_AGENT_SALES_EMEA',   'EMEA');

-- Create once, then keep the body current. ALTER ... SET BODY works while the
-- policy is attached, so no detach/re-attach cycle is needed on re-runs.
CREATE ROW ACCESS POLICY IF NOT EXISTS SALES_THEATER_POLICY
  AS (theater_col VARCHAR) RETURNS BOOLEAN -> FALSE
  COMMENT = 'Fail closed: rows are visible only for theaters entitled to CURRENT_ROLE().';

ALTER ROW ACCESS POLICY SALES_THEATER_POLICY SET BODY ->
  EXISTS (
    SELECT 1
    FROM COOKBOOK_MULTI_AGENT.APP.SALES_ENTITLEMENTS e
    WHERE e.ROLE_NAME = CURRENT_ROLE()
      AND (e.THEATER = 'ALL' OR e.THEATER = theater_col)
  );

-- Exactly one policy on the table: drop whatever is attached, then attach ours.
ALTER TABLE SALES_BOOKINGS DROP ALL ROW ACCESS POLICIES;
ALTER TABLE SALES_BOOKINGS ADD ROW ACCESS POLICY SALES_THEATER_POLICY ON (THEATER);

-- Verify with POLICY_CONTEXT, which evaluates the policy as if another role
-- were current. Expect 44 (admin), 16 EMEA rows (EMEA seller), 0 (support,
-- which has no entitlement row).
SELECT 'admin' AS context, COUNT(*) AS rows_visible FROM SALES_BOOKINGS;
EXECUTE USING POLICY_CONTEXT(CURRENT_ROLE => 'COOKBOOK_MULTI_AGENT_SALES_EMEA')
  AS SELECT 'sales_emea' AS context, THEATER, COUNT(*) AS rows_visible FROM SALES_BOOKINGS GROUP BY THEATER;
EXECUTE USING POLICY_CONTEXT(CURRENT_ROLE => 'COOKBOOK_MULTI_AGENT_SUPPORT')
  AS SELECT 'support (unmapped)' AS context, COUNT(*) AS rows_visible FROM SALES_BOOKINGS;
```

### `sql/05_agents.sql`

Copy code

```
-- =============================================================================
-- 05_agents.sql  (run as COOKBOOK_MULTI_AGENT_ADMIN)
-- Two specialists and one CoWork profile that routes to them.
--
--   SALES_AGENT                  Cortex Analyst over SALES_SEMANTIC_VIEW
--   SUPPORT_AGENT                Cortex Analyst over SUPPORT_SEMANTIC_VIEW
--   COOKBOOK_MULTI_AGENT_PROFILE agent_router tool -> the two specialists
--
-- The profile is an agent in the recipe schema, next to the specialists; a
-- profile can live in any schema. Its specification is identical for every
-- persona. What each persona can reach is decided by the grants in 06: with
-- tool_not_accessible: accept, a run skips any specialist the caller lacks
-- USAGE on and returns warning 399569. The routing instructions
-- choose a specialist; they are not an access control.
--
-- CREATE OR REPLACE ... COPY GRANTS keeps existing grants on re-runs. Put COPY
-- GRANTS directly before FROM SPECIFICATION; placed before COMMENT or PROFILE
-- it is a syntax error. This differs from the published CREATE AGENT syntax,
-- which lists COPY GRANTS first (see README, Gotchas).
-- The orchestration model is pinned (not auto) so evaluation runs compare the
-- same configuration; change it here if claude-sonnet-4-6 is not available to
-- you. Names inside the $$ bodies are literals. Object names are fixed; do not
-- rename them.
-- =============================================================================

SET cookbook_schema = 'COOKBOOK_MULTI_AGENT.APP';
SET cookbook_wh     = 'COOKBOOK_MULTI_AGENT_WH';
SET admin_role      = 'COOKBOOK_MULTI_AGENT_ADMIN';

USE ROLE IDENTIFIER($admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($cookbook_schema);

-- ── Specialist 1: sales ─────────────────────────────────────────────────────
CREATE OR REPLACE AGENT SALES_AGENT
  COMMENT = 'Sales specialist: bookings, pipeline, and targets via Cortex Analyst.'
  PROFILE = '{"display_name": "Sales Specialist"}'
  COPY GRANTS
  FROM SPECIFICATION
$$
models:
  orchestration: claude-sonnet-4-6
orchestration:
  budget:
    seconds: 180
    tokens: 60000
instructions:
  orchestration: >-
    Use sales_analyst for every question about new bookings, targets, attainment,
    or pipeline by fiscal quarter, theater, or territory. Always state the fiscal
    quarter and theater you answered for.
  response: >-
    Lead with the number. Values are in USD millions; format as $X.XM.
    Keep markdown tables intact.
  sample_questions:
    - question: "What were total new bookings in FY25-Q4 by theater?"
tools:
  - tool_spec:
      type: cortex_analyst_text_to_sql
      name: sales_analyst
      description: >-
        Sales bookings, targets, attainment, and pipeline by fiscal quarter
        (FY25-Q1 to FY25-Q4), theater (Americas, EMEA, APAC), and territory.
tool_resources:
  sales_analyst:
    semantic_view: COOKBOOK_MULTI_AGENT.APP.SALES_SEMANTIC_VIEW
    execution_environment:
      type: warehouse
      warehouse: COOKBOOK_MULTI_AGENT_WH
      query_timeout: 120
$$;

-- ── Specialist 2: support ───────────────────────────────────────────────────
CREATE OR REPLACE AGENT SUPPORT_AGENT
  COMMENT = 'Support specialist: answers product how-to questions from the knowledge base.'
  PROFILE = '{"display_name": "Support Specialist"}'
  COPY GRANTS
  FROM SPECIFICATION
$$
models:
  orchestration: claude-sonnet-4-6
orchestration:
  budget:
    seconds: 120
    tokens: 40000
instructions:
  orchestration: >-
    Use support_kb for every question. Retrieve the CONTENT of the relevant
    article and answer from it.
  response: >-
    Answer step by step and cite the article ID you used, for example KB-003.
  sample_questions:
    - question: "How do I set up single sign-on?"
tools:
  - tool_spec:
      type: cortex_analyst_text_to_sql
      name: support_kb
      description: >-
        Support knowledge base articles: SSO, passwords, API tokens and 401/403
        errors, billing and seats, scheduled exports, dashboard performance,
        audit logs. Returns article IDs, titles, categories, and content.
tool_resources:
  support_kb:
    semantic_view: COOKBOOK_MULTI_AGENT.APP.SUPPORT_SEMANTIC_VIEW
    execution_environment:
      type: warehouse
      warehouse: COOKBOOK_MULTI_AGENT_WH
      query_timeout: 120
$$;

-- ── Profile ─────────────────────────────────────────────────────────────────
-- Every subagents entry needs name, display_name, description, and source; one
-- incomplete entry silently drops the whole list. The tool_resources key must
-- match the router tool's name.
CREATE OR REPLACE AGENT COOKBOOK_MULTI_AGENT_PROFILE
  COMMENT = 'Cookbook multi-agent-orchestration: routes to the sales and support specialists.'
  PROFILE = '{"display_name": "Northwind Assistant"}'
  COPY GRANTS
  FROM SPECIFICATION
$$
models:
  orchestration: claude-sonnet-4-6
orchestration:
  tool_not_accessible: accept
  budget:
    seconds: 600
    tokens: 100000
instructions:
  orchestration: |
    Route every question to a subagent. Do not answer from your own knowledge.
    If a question spans sales and support, route to both and answer each part
    under its own heading.
    When a follow-up refers to earlier turns ("break that down by territory"),
    rewrite it as a self-contained question before routing, because subagents
    do not see the conversation history.
    If no subagent you can use covers a question or part of one, reply for that
    part: "This type of question is not available at your access level. Contact
    your administrator for access."
  response: |
    Return each subagent's answer faithfully, including markdown tables, without
    adding numbers of your own. No preamble.
  sample_questions:
    - question: "What were total new bookings in FY25-Q4 by theater?"
    - question: "How do I set up single sign-on?"
tools:
  - tool_spec:
      type: agent_router
      name: router
tool_resources:
  router:
    subagents:
      - name: COOKBOOK_MULTI_AGENT.APP.SALES_AGENT
        display_name: Sales
        description: >-
          New bookings, targets, attainment, and pipeline by fiscal quarter,
          theater, and territory. Not for product support.
        source:
          type: DATA_AGENT
          fqn: COOKBOOK_MULTI_AGENT.APP.SALES_AGENT
          sample_questions: []
      - name: COOKBOOK_MULTI_AGENT.APP.SUPPORT_AGENT
        display_name: Support
        description: >-
          Product how-to and troubleshooting: SSO, passwords, API tokens, 401/403
          errors, billing and seats, exports, dashboard performance, audit logs.
          Not for sales numbers.
        source:
          type: DATA_AGENT
          fqn: COOKBOOK_MULTI_AGENT.APP.SUPPORT_AGENT
          sample_questions: []
$$;

SHOW AGENTS IN SCHEMA IDENTIFIER($cookbook_schema);
```

### `sql/06_grants.sql`

Copy code

```
-- =============================================================================
-- 06_grants.sql  (run as COOKBOOK_MULTI_AGENT_ADMIN; run last, and after any
-- re-run of 05)
-- The persona boundary. No prompt, no application code, and no model decision
-- participates in it.
--
--   Layer 1  USAGE on the profile, plus its database and schema:
--            every persona can open the front door.
--   Layer 2  USAGE on a specialist agent: the profile routes only to
--            specialists the caller can use. No USAGE -> the specialist is skipped
--            with warning 399569 and the profile refuses that part.
--   Layer 3  SELECT on the specialist's semantic view AND its base table: the
--            specialist's Cortex Analyst tool runs its generated SQL against
--            the base table as the caller, so this holds even if layer 2 were
--            wrong. Without SELECT on the table the tool returns a compilation
--            error even though the semantic view grant is present.
--   Layer 4  The row access policy (04) filters rows inside the sales domain.
--
-- REVOKE statements make re-runs converge on exactly this set of grants.
-- For a full audit of who can reach which agent and tool, use the
-- check-agent-access skill (see README, Related skills).
-- =============================================================================

SET cookbook_db     = 'COOKBOOK_MULTI_AGENT';
SET cookbook_schema = 'COOKBOOK_MULTI_AGENT.APP';
SET cookbook_wh     = 'COOKBOOK_MULTI_AGENT_WH';
SET admin_role      = 'COOKBOOK_MULTI_AGENT_ADMIN';
SET sales_global    = 'COOKBOOK_MULTI_AGENT_SALES_GLOBAL';
SET sales_emea      = 'COOKBOOK_MULTI_AGENT_SALES_EMEA';
SET support_role    = 'COOKBOOK_MULTI_AGENT_SUPPORT';
SET profile         = 'COOKBOOK_MULTI_AGENT.APP.COOKBOOK_MULTI_AGENT_PROFILE';

USE ROLE IDENTIFIER($admin_role);
USE SCHEMA IDENTIFIER($cookbook_schema);

-- ── Shared plumbing and layer 1 (all three personas) ────────────────────────
GRANT USAGE ON DATABASE  IDENTIFIER($cookbook_db)     TO ROLE IDENTIFIER($sales_global);
GRANT USAGE ON DATABASE  IDENTIFIER($cookbook_db)     TO ROLE IDENTIFIER($sales_emea);
GRANT USAGE ON DATABASE  IDENTIFIER($cookbook_db)     TO ROLE IDENTIFIER($support_role);
GRANT USAGE ON SCHEMA    IDENTIFIER($cookbook_schema) TO ROLE IDENTIFIER($sales_global);
GRANT USAGE ON SCHEMA    IDENTIFIER($cookbook_schema) TO ROLE IDENTIFIER($sales_emea);
GRANT USAGE ON SCHEMA    IDENTIFIER($cookbook_schema) TO ROLE IDENTIFIER($support_role);
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh)     TO ROLE IDENTIFIER($sales_global);
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh)     TO ROLE IDENTIFIER($sales_emea);
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh)     TO ROLE IDENTIFIER($support_role);

GRANT USAGE ON AGENT IDENTIFIER($profile) TO ROLE IDENTIFIER($sales_global);
GRANT USAGE ON AGENT IDENTIFIER($profile) TO ROLE IDENTIFIER($sales_emea);
GRANT USAGE ON AGENT IDENTIFIER($profile) TO ROLE IDENTIFIER($support_role);

-- ── Layers 2 and 3: sales personas reach sales only ─────────────────────────
GRANT USAGE  ON AGENT SALES_AGENT                   TO ROLE IDENTIFIER($sales_global);
GRANT USAGE  ON AGENT SALES_AGENT                   TO ROLE IDENTIFIER($sales_emea);
GRANT SELECT ON SEMANTIC VIEW SALES_SEMANTIC_VIEW   TO ROLE IDENTIFIER($sales_global);
GRANT SELECT ON SEMANTIC VIEW SALES_SEMANTIC_VIEW   TO ROLE IDENTIFIER($sales_emea);
GRANT SELECT ON TABLE SALES_BOOKINGS                TO ROLE IDENTIFIER($sales_global);
GRANT SELECT ON TABLE SALES_BOOKINGS                TO ROLE IDENTIFIER($sales_emea);
REVOKE USAGE  ON AGENT SUPPORT_AGENT                 FROM ROLE IDENTIFIER($sales_global);
REVOKE USAGE  ON AGENT SUPPORT_AGENT                 FROM ROLE IDENTIFIER($sales_emea);
REVOKE SELECT ON SEMANTIC VIEW SUPPORT_SEMANTIC_VIEW FROM ROLE IDENTIFIER($sales_global);
REVOKE SELECT ON SEMANTIC VIEW SUPPORT_SEMANTIC_VIEW FROM ROLE IDENTIFIER($sales_emea);
REVOKE SELECT ON TABLE SUPPORT_KB                    FROM ROLE IDENTIFIER($sales_global);
REVOKE SELECT ON TABLE SUPPORT_KB                    FROM ROLE IDENTIFIER($sales_emea);

-- ── Layers 2 and 3: support persona reaches support only ────────────────────
GRANT USAGE  ON AGENT SUPPORT_AGENT                 TO ROLE IDENTIFIER($support_role);
GRANT SELECT ON SEMANTIC VIEW SUPPORT_SEMANTIC_VIEW TO ROLE IDENTIFIER($support_role);
GRANT SELECT ON TABLE SUPPORT_KB                    TO ROLE IDENTIFIER($support_role);
REVOKE USAGE  ON AGENT SALES_AGENT                   FROM ROLE IDENTIFIER($support_role);
REVOKE SELECT ON SEMANTIC VIEW SALES_SEMANTIC_VIEW   FROM ROLE IDENTIFIER($support_role);
REVOKE SELECT ON TABLE SALES_BOOKINGS                FROM ROLE IDENTIFIER($support_role);

SHOW GRANTS TO ROLE IDENTIFIER($sales_emea);
SHOW GRANTS TO ROLE IDENTIFIER($support_role);
```

### `sql/07_routing_eval.sql`

Copy code

```
-- =============================================================================
-- 07_routing_eval.sql  (run as COOKBOOK_MULTI_AGENT_ADMIN)
-- Measure whether the profile reaches the right specialist and returns the
-- right answer, with Cortex Agent evaluations.
--
-- Metrics are pinned to judge version v3 so scores stay comparable across
-- runs. To see which specialist answered a single question, read subagent_name
-- in the response (see README, Verify).
--
-- The evaluation invokes the agent as the role running it (the admin role,
-- entitled to all theaters). Evaluations cannot pass session attributes and do
-- not impersonate personas, so the persona boundary is tested separately (see
-- README, Verify).
--
-- Idempotent: the dataset is created once; the run is deleted and restarted.
-- Names inside $$ bodies are literals. Object names are fixed; do not rename
-- them.
-- =============================================================================

SET cookbook_schema = 'COOKBOOK_MULTI_AGENT.APP';
SET cookbook_wh     = 'COOKBOOK_MULTI_AGENT_WH';
SET admin_role      = 'COOKBOOK_MULTI_AGENT_ADMIN';

USE ROLE IDENTIFIER($admin_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($cookbook_schema);

-- ── Ground truth ────────────────────────────────────────────────────────────
-- Values match the seed data in 02 (USD millions).
CREATE TABLE IF NOT EXISTS ROUTING_EVAL_INPUT (
  INPUT_QUERY  VARCHAR,
  GROUND_TRUTH VARIANT
);

INSERT OVERWRITE INTO ROUTING_EVAL_INPUT
SELECT q, PARSE_JSON(gt) FROM VALUES
  ('What were total new bookings in FY25-Q4 by theater?',
   '{"ground_truth_output": "FY25-Q4 new bookings: Americas about $59.6M, EMEA about $38.4M, APAC about $22.1M, total $120.0M. Values within 0.1M are acceptable."}'),
  ('What was EMEA attainment against target in FY25-Q3?',
   '{"ground_truth_output": "EMEA FY25-Q3 new bookings were about $35.2M against a $35.2M target, attainment about 99.9%."}'),
  ('How do I set up single sign-on?',
   '{"ground_truth_output": "Go to Settings > Security > SSO, choose the identity provider, paste its metadata URL, map the SAML NameID to the email attribute, and test with one admin before requiring SSO for all members. Cites KB-001."}'),
  ('Why is the API returning 403 for a valid token?',
   '{"ground_truth_output": "A 403 means the token is valid but lacks the scope for the endpoint; create a token with the right scope. Cites KB-003."}'),
  ('What was total pipeline in FY25-Q4, and how do I schedule a recurring export?',
   '{"ground_truth_output": "Total FY25-Q4 pipeline was $360.0M. Recurring exports are set up under Settings > Data > Scheduled Exports, daily or weekly, as CSV or JSON. Both parts must be answered."}')
  AS t(q, gt);

-- Create the dataset once; later runs reuse it.
EXECUTE IMMEDIATE $$
BEGIN
  CALL SYSTEM$CREATE_EVALUATION_DATASET(
    'Cortex Agent',
    'COOKBOOK_MULTI_AGENT.APP.ROUTING_EVAL_INPUT',
    'COOKBOOK_MULTI_AGENT.APP.ROUTING_EVAL_DATASET',
    OBJECT_CONSTRUCT('query_text', 'INPUT_QUERY', 'expected_tools', 'GROUND_TRUTH'));
  RETURN 'dataset created';
EXCEPTION
  WHEN OTHER THEN RETURN 'dataset already exists: ' || SQLERRM;
END;
$$;

-- ── Evaluation config on a stage ────────────────────────────────────────────
CREATE FILE FORMAT IF NOT EXISTS EVAL_YAML_FORMAT
  TYPE = CSV FIELD_DELIMITER = NONE RECORD_DELIMITER = '\n' SKIP_HEADER = 0
  FIELD_OPTIONALLY_ENCLOSED_BY = NONE ESCAPE_UNENCLOSED_FIELD = NONE;
CREATE STAGE IF NOT EXISTS EVAL_CONFIG FILE_FORMAT = EVAL_YAML_FORMAT;

-- Written with COPY INTO so the script needs no local file or PUT.
COPY INTO @EVAL_CONFIG/routing_eval.yaml
FROM (SELECT $$evaluation:
  agent_params:
    agent_name: "COOKBOOK_MULTI_AGENT.APP.COOKBOOK_MULTI_AGENT_PROFILE"
    agent_type: "CORTEX AGENT"
    agent_version: "LIVE"
  run_params:
    label: "routing"
    description: "Does the profile reach the right specialist and answer correctly?"
  source_metadata:
    type: "dataset"
    dataset_name: "COOKBOOK_MULTI_AGENT.APP.ROUTING_EVAL_DATASET"
metrics:
  - name: "answer_correctness"
    version: "v3"
  - name: "logical_consistency"
    version: "v3"
$$)
FILE_FORMAT = (TYPE = CSV COMPRESSION = NONE RECORD_DELIMITER = NONE FIELD_DELIMITER = NONE
               FIELD_OPTIONALLY_ENCLOSED_BY = NONE ESCAPE_UNENCLOSED_FIELD = NONE)
OVERWRITE = TRUE SINGLE = TRUE HEADER = FALSE;

-- ── Start the run (replacing a previous run of the same name) ───────────────
EXECUTE IMMEDIATE $$
BEGIN
  CALL EXECUTE_AI_EVALUATION('DELETE', OBJECT_CONSTRUCT('run_name', 'routing-baseline'),
                             '@COOKBOOK_MULTI_AGENT.APP.EVAL_CONFIG/routing_eval.yaml');
EXCEPTION
  WHEN OTHER THEN NULL;  -- no previous run
END;
$$;

CALL EXECUTE_AI_EVALUATION('START', OBJECT_CONSTRUCT('run_name', 'routing-baseline'),
                           '@COOKBOOK_MULTI_AGENT.APP.EVAL_CONFIG/routing_eval.yaml');

-- Poll until the status reports completion (a few minutes for five inputs):
--   CALL EXECUTE_AI_EVALUATION('STATUS', OBJECT_CONSTRUCT('run_name', 'routing-baseline'),
--                              '@COOKBOOK_MULTI_AGENT.APP.EVAL_CONFIG/routing_eval.yaml');
-- Then read scores:
--   SELECT METRIC_NAME, ROUND(AVG(EVAL_AGG_SCORE), 2) AS avg_score, COUNT(*) AS n
--   FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
--     'COOKBOOK_MULTI_AGENT', 'APP', 'COOKBOOK_MULTI_AGENT_PROFILE', 'CORTEX AGENT', 'routing-baseline'))
--   GROUP BY METRIC_NAME;
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- 99_teardown.sql  (run as ACCOUNTADMIN)
-- Removes everything the recipe created. Dropping the database removes the
-- profile, specialists, semantic views, policy, tables, stage, evaluation
-- dataset, and evaluation runs stored in it.
--
-- If you attached the profile to the Snowflake CoWork object (optional step in
-- the README), detach it first:
--   ALTER SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT
--     DROP AGENT COOKBOOK_MULTI_AGENT.APP.COOKBOOK_MULTI_AGENT_PROFILE;
-- =============================================================================

SET cookbook_db    = 'COOKBOOK_MULTI_AGENT';
SET cookbook_wh    = 'COOKBOOK_MULTI_AGENT_WH';
SET admin_role     = 'COOKBOOK_MULTI_AGENT_ADMIN';
SET sales_global   = 'COOKBOOK_MULTI_AGENT_SALES_GLOBAL';
SET sales_emea     = 'COOKBOOK_MULTI_AGENT_SALES_EMEA';
SET support_role   = 'COOKBOOK_MULTI_AGENT_SUPPORT';
SET sales_global_u = 'COOKBOOK_MULTI_AGENT_SALES_GLOBAL_USER';
SET sales_emea_u   = 'COOKBOOK_MULTI_AGENT_SALES_EMEA_USER';
SET support_u      = 'COOKBOOK_MULTI_AGENT_SUPPORT_USER';

USE ROLE ACCOUNTADMIN;

DROP DATABASE  IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);

DROP USER IF EXISTS IDENTIFIER($sales_global_u);
DROP USER IF EXISTS IDENTIFIER($sales_emea_u);
DROP USER IF EXISTS IDENTIFIER($support_u);

DROP ROLE IF EXISTS IDENTIFIER($sales_global);
DROP ROLE IF EXISTS IDENTIFIER($sales_emea);
DROP ROLE IF EXISTS IDENTIFIER($support_role);
DROP ROLE IF EXISTS IDENTIFIER($admin_role);

SHOW DATABASES  LIKE 'COOKBOOK_MULTI_AGENT%';
SHOW WAREHOUSES LIKE 'COOKBOOK_MULTI_AGENT%';
SHOW ROLES      LIKE 'COOKBOOK_MULTI_AGENT%';
SHOW USERS      LIKE 'COOKBOOK_MULTI_AGENT%';
```
