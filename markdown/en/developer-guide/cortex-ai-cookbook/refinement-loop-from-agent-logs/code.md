# Refine a semantic view from agent logs: triage, SME review, and verified queries: code

Every file in the [Refine a semantic view from agent logs: triage, SME review, and verified queries](/developer-guide/cortex-ai-cookbook/refinement-loop-from-agent-logs) recipe. To run the recipe, download [refinement-loop-from-agent-logs.zip](/static/samples/cortex-ai-cookbook/refinement-loop-from-agent-logs.zip), unzip it, and run the scripts from the `refinement-loop-from-agent-logs/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/refinement-loop-from-agent-logs); the zip includes it as `README.md`.

## `sql/`

### `sql/01_example_setup.sql`

Copy code

```
-- =============================================================================
-- Refinement loop from agent logs: example setup
-- A support-tickets table with coded values (P1/P2/P3, PENDING_CUSTOMER), a
-- deliberately thin semantic view, an agent over it, and a change log. The thin
-- view is what a first draft often looks like: correct, but with nothing that
-- maps the words people use ("urgent", "escalated", "waiting on the customer")
-- to the codes.
-- Rerunning this script resets the example: table, view, and change log.
-- =============================================================================

SET DB        = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS';
SET WH        = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_WH';
SET ROLE_NAME = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_ROLE';
SET CUR_USER  = '"' || CURRENT_USER() || '"';

-- Account-level setup: role, warehouse, database. The recipe runs as ROLE_NAME.
USE ROLE ACCOUNTADMIN;
CREATE ROLE IF NOT EXISTS IDENTIFIER($ROLE_NAME) COMMENT = 'Cortex AI Cookbook: refinement-loop-from-agent-logs';
GRANT ROLE IDENTIFIER($ROLE_NAME) TO USER IDENTIFIER($CUR_USER);
GRANT ROLE IDENTIFIER($ROLE_NAME) TO ROLE SYSADMIN;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($ROLE_NAME);
CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($WH)
  WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cortex AI Cookbook: refinement-loop-from-agent-logs';
GRANT USAGE, OPERATE ON WAREHOUSE IDENTIFIER($WH) TO ROLE IDENTIFIER($ROLE_NAME);
CREATE DATABASE IF NOT EXISTS IDENTIFIER($DB) COMMENT = 'Cortex AI Cookbook: refinement-loop-from-agent-logs';
GRANT OWNERSHIP ON DATABASE IDENTIFIER($DB) TO ROLE IDENTIFIER($ROLE_NAME) COPY CURRENT GRANTS;

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
CREATE SCHEMA IF NOT EXISTS SUPPORT;
USE SCHEMA SUPPORT;

-- 120 fictional tickets across three products. Every product has OPEN P1 and
-- P2 tickets, so "escalated" questions have a non-zero answer.
CREATE OR REPLACE TABLE TICKETS (
    TICKET_ID        NUMBER,
    OPENED_ON        DATE,
    PRIORITY         VARCHAR,
    STATUS           VARCHAR,
    PRODUCT          VARCHAR,
    HOURS_TO_RESOLVE NUMBER(6,1)     -- NULL unless STATUS = 'RESOLVED'
);
INSERT INTO TICKETS
WITH g AS (SELECT SEQ4() AS i FROM TABLE(GENERATOR(ROWCOUNT => 120))),
t AS (
  SELECT i,
         ARRAY_CONSTRUCT('P1', 'P2', 'P2', 'P3', 'P3', 'P3')[MOD(i, 6)]::VARCHAR                        AS priority,
         ARRAY_CONSTRUCT('Billing', 'Mobile App', 'Integrations')[MOD(FLOOR(i / 6), 3)]::VARCHAR        AS product,
         ARRAY_CONSTRUCT('OPEN', 'RESOLVED', 'RESOLVED', 'PENDING_CUSTOMER')[MOD(i + FLOOR(i / 18), 4)]::VARCHAR AS status
  FROM g
)
SELECT 1000 + i,
       DATEADD(day, MOD(i * 7, 62), '2026-07-01'::DATE),
       priority,
       status,
       product,
       IFF(status = 'RESOLVED', 2 + MOD(i * 13, 70) / 2, NULL)
FROM t;

-- The thin first draft: every column present, nothing that explains the codes.
CREATE OR ALTER SEMANTIC VIEW TICKETS_SV
  TABLES (tickets AS TICKETS PRIMARY KEY (TICKET_ID) COMMENT = 'Support tickets.')
  FACTS (tickets.hours_to_resolve AS HOURS_TO_RESOLVE COMMENT = 'Hours to resolve.')
  DIMENSIONS (
    tickets.opened_on AS OPENED_ON COMMENT = 'Date opened.',
    tickets.priority AS PRIORITY COMMENT = 'Priority.',
    tickets.status AS STATUS COMMENT = 'Status.',
    tickets.product AS PRODUCT COMMENT = 'Product.'
  )
  METRICS (
    tickets.ticket_count AS COUNT(ticket_id) COMMENT = 'Number of tickets.',
    tickets.avg_hours_to_resolve AS AVG(hours_to_resolve) COMMENT = 'Average hours to resolve.'
  )
  COMMENT = 'Support tickets.';

-- The agent. Created once; the loop changes the semantic view, not the agent.
-- The spec names the database and warehouse literally; edit both if you change them.
CREATE AGENT IF NOT EXISTS SUPPORT_AGENT
  COMMENT = 'Cortex AI Cookbook: refinement-loop-from-agent-logs'
  FROM SPECIFICATION $$
  {
    "models": {"orchestration": "auto"},
    "instructions": {"orchestration": "Use tickets for every question about support tickets."},
    "tools": [{"tool_spec": {"type": "cortex_analyst_text_to_sql", "name": "tickets",
                             "description": "Support tickets by priority, status, product, and date."}}],
    "tool_resources": {"tickets": {
      "semantic_view": "COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.TICKETS_SV",
      "execution_environment": {"type": "warehouse", "warehouse": "COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_WH", "query_timeout": 60}}}
  }
  $$;

-- One row per shipped change to the semantic view, grouped by VIEW_VERSION (one
-- deploy). Triage uses it to label each turn with the version that answered it,
-- and it is the record you send back to the subject matter expert ("your answer
-- shipped as ..."). CHANGED_AT is UTC, like the observability events.
CREATE OR REPLACE TABLE CHANGE_LOG (
    VIEW_VERSION    VARCHAR,
    CHANGE_ID       VARCHAR,
    CHANGED_AT      TIMESTAMP_NTZ,
    CHANGE          VARCHAR,
    SOURCE_QUESTION VARCHAR,
    CONFIRMED_BY    VARCHAR
);
INSERT INTO CHANGE_LOG VALUES
  ('v0', 'setup', SYSDATE(), 'First-draft semantic view deployed', NULL, NULL);
```

### `sql/02_grant_unredacted.sql`

Copy code

```
-- =============================================================================
-- Refinement loop from agent logs: let the curating role read conversation text
-- Without READ UNREDACTED AI OBSERVABILITY EVENTS TABLE, the observability table
-- functions return metadata (span names, tools, latency, tokens) but the
-- question and answer text is redacted, and there is nothing to triage.
--
-- This is an ACCOUNT-LEVEL privilege. A role that holds it can read the full
-- text of every conversation with every agent it can MONITOR. Grant it only to
-- the small role that curates the semantic layer, after privacy review.
-- 99_teardown.sql drops the role, which removes the grant.
-- =============================================================================

SET ROLE_NAME = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_ROLE';

USE ROLE ACCOUNTADMIN;
GRANT READ UNREDACTED AI OBSERVABILITY EVENTS TABLE ON ACCOUNT TO ROLE IDENTIFIER($ROLE_NAME);
```

### `sql/03_generate_traffic.sql`

Copy code

```
-- =============================================================================
-- Refinement loop from agent logs: a week of traffic, in miniature
-- In production this traffic comes from real users in Snowflake CoWork, an MCP
-- client, or the Agent REST API. Here, five questions sent with DATA_AGENT_RUN.
-- Run each statement on its own: one request is one turn, and one turn is one
-- trace. Traces reach the observability table functions within about a minute.
-- 06_retest.sql sends the same five questions after the view is refined.
-- =============================================================================

SET DB        = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS';
SET WH        = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_WH';
SET ROLE_NAME = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_ROLE';

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA SUPPORT;

SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.SUPPORT_AGENT',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "How many urgent tickets are still open?"}]}]}$$);

SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.SUPPORT_AGENT',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "How many escalated tickets do we have for the Mobile App?"}]}]}$$);

SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.SUPPORT_AGENT',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "How many tickets are waiting on the customer?"}]}]}$$);

SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.SUPPORT_AGENT',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "What is the average time to resolve Billing tickets?"}]}]}$$);

SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.SUPPORT_AGENT',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "Which support engineer closed the most tickets?"}]}]}$$);
```

### `sql/04_triage.sql`

Copy code

```
-- =============================================================================
-- Refinement loop from agent logs: triage
-- One row per turn from the agent's traces: the question, the answer, the SQL
-- the agent ran, whether a verified query was used, the semantic view version
-- in effect (from the change log), and a first-pass bucket. Buckets are heuristics
-- to sort review work, not a verdict: a person reads every row that is not a
-- clean answer, plus a sample of the clean ones, because a confident wrong
-- answer looks exactly like a right one.
--
-- Access: OWNERSHIP or MONITOR on the agent, SNOWFLAKE.CORTEX_USER, and (for
-- the text) READ UNREDACTED AI OBSERVABILITY EVENTS TABLE from 02.
--
-- Span and attribute names below (AgentV2RequestResponseInfo,
-- SystemExecuteSQLTool_system_execute_sql, ...) are what the event table holds
-- today; the documentation defines the table functions and the event layout,
-- not these names. If a column comes back empty, list the span names first:
--   SELECT DISTINCT RECORD:name FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_EVENTS(...));
-- =============================================================================

SET DB            = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS';
SET WH            = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_WH';
SET ROLE_NAME     = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_ROLE';
SET AGENT_SCHEMA  = 'SUPPORT';
SET AGENT_NAME    = 'SUPPORT_AGENT';
SET CHANGE_LOG    = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.CHANGE_LOG';
SET LOOKBACK_DAYS = 7;     -- the review cadence: one week of traffic per cycle
SET SPOT_CHECK    = 5;     -- clean answers per bucket that also go to review

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA SUPPORT;

-- Rebuilds TRIAGE in the caller's current schema. Caller's rights: it reads only
-- the traces the calling role may MONITOR. Every name arrives as a parameter:
-- the agent goes to the table function as bind variables, and the change log is
-- read through IDENTIFIER(:CHANGE_LOG_TABLE). Nothing is concatenated into SQL.
--
-- CHANGE_LOG_TABLE is the fully qualified change log of the agent's semantic
-- view (it needs VIEW_VERSION and CHANGED_AT columns), or NULL for an agent that
-- has none. With NULL, VIEW_VERSION is empty and the window is LOOKBACK_DAYS
-- alone.
--
-- The earlier four-argument version is dropped first, so a rerun leaves one
-- procedure rather than two overloads.
DROP PROCEDURE IF EXISTS REFRESH_TRIAGE(VARCHAR, VARCHAR, VARCHAR, NUMBER);
CREATE OR REPLACE PROCEDURE REFRESH_TRIAGE(
    AGENT_DB VARCHAR, AGENT_SCHEMA VARCHAR, AGENT_NAME VARCHAR, LOOKBACK_DAYS NUMBER,
    CHANGE_LOG_TABLE VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SQL
  EXECUTE AS CALLER
AS
$$
DECLARE
  since TIMESTAMP_NTZ;
  turns NUMBER;
  with_text NUMBER;
BEGIN
  -- The versions of this agent's semantic view, from the change log passed in.
  CREATE OR REPLACE TEMPORARY TABLE TRIAGE_VERSIONS (VIEW_VERSION VARCHAR, CHANGED_AT TIMESTAMP_NTZ);
  IF (CHANGE_LOG_TABLE IS NOT NULL) THEN
    INSERT INTO TRIAGE_VERSIONS
      SELECT VIEW_VERSION, CHANGED_AT FROM IDENTIFIER(:CHANGE_LOG_TABLE);
  END IF;

  -- Event timestamps are UTC (TIMESTAMP_NTZ), so compare against SYSDATE().
  -- Never read further back than the first change log entry: events outlive a
  -- dropped agent, and a recreated agent with the same name sees them again.
  since := (SELECT GREATEST(DATEADD(day, -:LOOKBACK_DAYS, SYSDATE()),
                            COALESCE(MIN(CHANGED_AT), '1970-01-01'::TIMESTAMP_NTZ))
            FROM TRIAGE_VERSIONS);

  CREATE OR REPLACE TABLE TRIAGE AS
  WITH ev AS (
    SELECT TRACE:trace_id::VARCHAR AS TRACE_ID, TIMESTAMP AS TS,
           RECORD:name::VARCHAR AS SPAN, RECORD_ATTRIBUTES AS A
    FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_EVENTS(:AGENT_DB, :AGENT_SCHEMA, :AGENT_NAME, 'CORTEX AGENT'))
    WHERE TIMESTAMP >= :since
      AND TRACE:trace_id IS NOT NULL
  ), turns AS (
    SELECT TRACE_ID,
           MIN(TS) AS STARTED_AT,
           MAX(IFF(SPAN = 'AgentV2RequestResponseInfo', A:"ai.observability.record_root.input"::VARCHAR, NULL))  AS QUESTION,
           MAX(IFF(SPAN = 'AgentV2RequestResponseInfo', A:"ai.observability.record_root.output"::VARCHAR, NULL)) AS ANSWER,
           COUNT_IF(SPAN = 'AgentV2RequestResponseInfo') AS IS_TURN,
           COUNT_IF(SPAN = 'SystemExecuteSQLTool_system_execute_sql') AS SQL_RUNS,
           LISTAGG(IFF(SPAN = 'SystemExecuteSQLTool_system_execute_sql',
                       A:"snow.ai.observability.agent.tool.sql_execution.query"::VARCHAR, NULL), '\n---\n')
             WITHIN GROUP (ORDER BY TS) AS AGENT_SQL,
           BOOLOR_AGG(COALESCE(A:"snow.ai.observability.agent.tool.sql_execution.verified_query_used"::BOOLEAN, FALSE))
             AS USED_VERIFIED_QUERY
    FROM ev
    GROUP BY TRACE_ID
  )
  SELECT t.TRACE_ID, t.STARTED_AT, v.VIEW_VERSION,
         t.QUESTION, t.ANSWER, t.SQL_RUNS, t.USED_VERIFIED_QUERY, t.AGENT_SQL,
         CASE
           -- Said the data is not there. Either a real scope gap or a missing definition.
           WHEN REGEXP_LIKE(t.ANSWER, '.*(can.?t answer|cannot answer|unable to|not available|isn.?t available'
                                      || '|doesn.?t (contain|track|include|have)|does not (contain|track|include|have)'
                                      || '|no (field|column) ).*', 'is')
             THEN 'NO_DATA'
           -- Answered without running any SQL.
           WHEN t.SQL_RUNS = 0 THEN 'NO_TOOL'
           -- Had to guess what a word means.
           WHEN REGEXP_LIKE(t.ANSWER, '.*(interpreted|assum|if by |could mean|took .* to mean|let me know if).*', 'is')
             THEN 'GUESSED'
           -- Queried more than once, usually to discover the coded values.
           WHEN t.SQL_RUNS > 1 THEN 'EXPLORED'
           WHEN t.USED_VERIFIED_QUERY THEN 'VERIFIED'
           ELSE 'ANSWERED'
         END AS BUCKET
  FROM turns t
  LEFT JOIN TRIAGE_VERSIONS v ON v.CHANGED_AT <= t.STARTED_AT
  WHERE t.IS_TURN > 0
  QUALIFY ROW_NUMBER() OVER (PARTITION BY t.TRACE_ID ORDER BY v.CHANGED_AT DESC NULLS LAST) = 1;

  turns := (SELECT COUNT(*) FROM TRIAGE);
  with_text := (SELECT COUNT(QUESTION) FROM TRIAGE);
  RETURN turns || ' turns since ' || since || ' UTC, ' || with_text || ' with question text'
         || IFF(turns > 0 AND with_text = 0, ' (text is redacted: run 02_grant_unredacted.sql)', '');
END;
$$;

CALL REFRESH_TRIAGE($DB, $AGENT_SCHEMA, $AGENT_NAME, $LOOKBACK_DAYS, $CHANGE_LOG);

-- The bucket counts for this cycle.
SELECT VIEW_VERSION, BUCKET, COUNT(*) AS TURNS
FROM TRIAGE
GROUP BY ALL
ORDER BY VIEW_VERSION, BUCKET;

-- The engineer's review queue: every turn that is not a clean answer, plus a
-- random sample of the clean ones.
SELECT BUCKET, STARTED_AT, QUESTION, ANSWER, SQL_RUNS, USED_VERIFIED_QUERY, AGENT_SQL
FROM TRIAGE
QUALIFY BUCKET NOT IN ('ANSWERED', 'VERIFIED')
     OR ROW_NUMBER() OVER (PARTITION BY BUCKET ORDER BY RANDOM()) <= $SPOT_CHECK
ORDER BY BUCKET, STARTED_AT;

-- What goes to the subject matter expert: the question and the answer, never the SQL.
SELECT QUESTION, ANSWER, 'Is this right? If not, what is the correct answer or definition?' AS ASK
FROM TRIAGE
QUALIFY BUCKET NOT IN ('ANSWERED', 'VERIFIED')
     OR ROW_NUMBER() OVER (PARTITION BY BUCKET ORDER BY RANDOM()) <= $SPOT_CHECK
ORDER BY STARTED_AT;
```

### `sql/05_apply_refinements.sql`

Copy code

```
-- =============================================================================
-- Refinement loop from agent logs: turn confirmed answers into the view
-- The subject matter expert's replies to the questions from 04 (fictional):
--   "urgent"                  = P1
--   "escalated"               = P1 or P2 that is still OPEN
--   "waiting on the customer" = STATUS = PENDING_CUSTOMER
--   resolution time exists only for RESOLVED tickets; say how many were averaged
--   assignee / engineer data is not in this dataset; say so, do not substitute
-- Each reply becomes a description, a dimension, a metric, a custom
-- instruction, or a verified query. CREATE OR ALTER keeps grants on the view;
-- anything omitted from the statement is removed, so always send the full view.
-- =============================================================================

SET DB        = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS';
SET WH        = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_WH';
SET ROLE_NAME = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_ROLE';
SET SV_FQ     = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.TICKETS_SV';

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA SUPPORT;

CREATE OR ALTER SEMANTIC VIEW TICKETS_SV
  TABLES (
    tickets AS TICKETS PRIMARY KEY (TICKET_ID)
      COMMENT = 'One row per customer support ticket opened July to August 2026, any status.'
  )
  FACTS (
    tickets.hours_to_resolve AS HOURS_TO_RESOLVE
      COMMENT = 'Hours from open to resolution. Set only when STATUS = RESOLVED; NULL for OPEN and PENDING_CUSTOMER tickets.'
  )
  DIMENSIONS (
    tickets.opened_on AS OPENED_ON COMMENT = 'Date the ticket was opened.',
    tickets.priority AS PRIORITY
      COMMENT = 'Priority code. P1 = urgent (highest), P2 = high, P3 = normal.'
      SAMPLE_VALUES ('P1', 'P2', 'P3')
      IS_ENUM,
    tickets.status AS STATUS
      COMMENT = 'Ticket state. OPEN = being worked; PENDING_CUSTOMER = waiting on the customer to reply; RESOLVED = closed.'
      SAMPLE_VALUES ('OPEN', 'PENDING_CUSTOMER', 'RESOLVED')
      IS_ENUM,
    tickets.is_escalated AS (PRIORITY IN ('P1', 'P2') AND STATUS = 'OPEN')
      COMMENT = 'TRUE for escalated tickets: priority P1 or P2 and still OPEN. This is the support team''s definition of escalated.',
    tickets.product AS PRODUCT
      COMMENT = 'Product the ticket is about.'
      SAMPLE_VALUES ('Billing', 'Mobile App', 'Integrations')
      IS_ENUM
  )
  METRICS (
    tickets.ticket_count AS COUNT(ticket_id) COMMENT = 'Number of tickets.',
    tickets.avg_hours_to_resolve AS AVG(hours_to_resolve)
      COMMENT = 'Average hours to resolve, over RESOLVED tickets only (others have no resolution time).',
    tickets.resolved_ticket_count AS COUNT(hours_to_resolve)
      COMMENT = 'Number of RESOLVED tickets, the population behind AVG_HOURS_TO_RESOLVE.'
  )
  COMMENT = 'Customer support tickets: volume, priority, status, and resolution time.'
  AI_SQL_GENERATION
    'When reporting AVG_HOURS_TO_RESOLVE, also return RESOLVED_TICKET_COUNT so the answer states how many tickets were averaged.'
  AI_QUESTION_CATEGORIZATION
    'This view has no assignee, engineer, or agent data. For questions about who handled or closed tickets, say that the data is not available instead of substituting another measure.'
  AI_VERIFIED_QUERIES (
    vq_urgent_open AS (
      QUESTION 'How many urgent tickets are still open?'
      VERIFIED_AT 1790640000
      ONBOARDING_QUESTION TRUE
      VERIFIED_BY '(STEWARD = support_operations)'
      SQL 'SELECT COUNT(ticket_id) AS urgent_open_tickets FROM tickets WHERE priority = ''P1'' AND status = ''OPEN'''
    ),
    vq_escalated_by_product AS (
      QUESTION 'How many escalated tickets are there by product?'
      VERIFIED_AT 1790640000
      ONBOARDING_QUESTION TRUE
      VERIFIED_BY '(STEWARD = support_operations)'
      SQL 'SELECT product, COUNT(ticket_id) AS escalated_tickets FROM tickets WHERE is_escalated GROUP BY product ORDER BY escalated_tickets DESC'
    )
  );

-- Record what shipped as version v1 and whose answer each change came from. This
-- is the list you send back to the subject matter experts. MERGE keeps a rerun
-- from adding duplicates.
MERGE INTO CHANGE_LOG c
USING (
  SELECT 'v1' AS VIEW_VERSION, column1 AS CHANGE_ID, column2 AS CHANGE,
         column3 AS SOURCE_QUESTION, column4 AS CONFIRMED_BY
  FROM VALUES
    ('urgent',        'PRIORITY described (P1 = urgent), IS_ENUM; verified query vq_urgent_open',
                      'How many urgent tickets are still open?', 'support_operations'),
    ('escalated',     'IS_ESCALATED dimension; verified query vq_escalated_by_product',
                      'How many escalated tickets do we have for the Mobile App?', 'support_operations'),
    ('pending',       'STATUS values described, IS_ENUM',
                      'How many tickets are waiting on the customer?', 'support_operations'),
    ('resolution',    'RESOLVED_TICKET_COUNT metric; AI_SQL_GENERATION: report the population',
                      'What is the average time to resolve Billing tickets?', 'support_operations'),
    ('scope',         'AI_QUESTION_CATEGORIZATION: no assignee data, say so',
                      'Which support engineer closed the most tickets?', 'support_operations')
) s
ON c.VIEW_VERSION = s.VIEW_VERSION AND c.CHANGE_ID = s.CHANGE_ID
WHEN NOT MATCHED THEN INSERT (VIEW_VERSION, CHANGE_ID, CHANGED_AT, CHANGE, SOURCE_QUESTION, CONFIRMED_BY)
  VALUES (s.VIEW_VERSION, s.CHANGE_ID, SYSDATE(), s.CHANGE, s.SOURCE_QUESTION, s.CONFIRMED_BY);

-- The close-out note for the subject matter experts.
SELECT VIEW_VERSION, CONFIRMED_BY, SOURCE_QUESTION, CHANGE
FROM CHANGE_LOG
WHERE VIEW_VERSION = 'v1'
ORDER BY CHANGE_ID;

-- The same view as YAML, for teams that review semantic views as YAML in pull
-- requests. Export it, commit it, and validate it in CI with the four-argument
-- procedure: verify_only = TRUE validates and creates nothing; create_or_alter
-- = TRUE uses CREATE OR ALTER semantics when you deploy with verify_only = FALSE.
SELECT SYSTEM$READ_YAML_FROM_SEMANTIC_VIEW($SV_FQ) AS TICKETS_SV_YAML;

-- CI-style check: validate the exported YAML without creating anything.
EXECUTE IMMEDIATE $$
DECLARE
  yaml VARCHAR;
  result VARCHAR;
BEGIN
  yaml := (SELECT SYSTEM$READ_YAML_FROM_SEMANTIC_VIEW('COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.TICKETS_SV'));
  CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML('COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT', :yaml, TRUE, TRUE)
    INTO :result;
  RETURN result;
END;
$$;
```

### `sql/06_retest.sql`

Copy code

```
-- =============================================================================
-- Refinement loop from agent logs: next cycle
-- The same five questions against the refined view, then the same triage. Each
-- turn is labeled with the view version that answered it (from CHANGE_LOG), so
-- one table shows the question before and after. In production this is simply
-- next week's traffic: new questions, the same triage, a new review queue.
-- Wait about a minute after the last DATA_AGENT_RUN before calling the triage.
-- =============================================================================

SET DB            = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS';
SET WH            = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_WH';
SET ROLE_NAME     = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_ROLE';
SET AGENT_SCHEMA  = 'SUPPORT';
SET AGENT_NAME    = 'SUPPORT_AGENT';
SET CHANGE_LOG    = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.CHANGE_LOG';
SET LOOKBACK_DAYS = 7;

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA SUPPORT;

SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.SUPPORT_AGENT',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "How many urgent tickets are still open?"}]}]}$$);

SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.SUPPORT_AGENT',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "How many escalated tickets do we have for the Mobile App?"}]}]}$$);

SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.SUPPORT_AGENT',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "How many tickets are waiting on the customer?"}]}]}$$);

SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.SUPPORT_AGENT',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "What is the average time to resolve Billing tickets?"}]}]}$$);

SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS.SUPPORT.SUPPORT_AGENT',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "Which support engineer closed the most tickets?"}]}]}$$);

CALL REFRESH_TRIAGE($DB, $AGENT_SCHEMA, $AGENT_NAME, $LOOKBACK_DAYS, $CHANGE_LOG);

-- Before and after, side by side. BEFORE is the first-draft view (v0); AFTER is
-- any later version in CHANGE_LOG.
WITH labeled AS (
  SELECT QUESTION, BUCKET, SQL_RUNS, USED_VERIFIED_QUERY, ANSWER,
         IFF(VIEW_VERSION = 'v0', 'BEFORE', 'AFTER') AS PHASE
  FROM TRIAGE
  QUALIFY ROW_NUMBER() OVER (PARTITION BY QUESTION, PHASE ORDER BY STARTED_AT DESC) = 1
)
SELECT b.QUESTION,
       b.BUCKET AS BUCKET_BEFORE, a.BUCKET AS BUCKET_AFTER,
       b.SQL_RUNS AS SQL_RUNS_BEFORE, a.SQL_RUNS AS SQL_RUNS_AFTER,
       a.USED_VERIFIED_QUERY AS VERIFIED_QUERY_AFTER,
       LEFT(b.ANSWER, 300) AS ANSWER_BEFORE, LEFT(a.ANSWER, 300) AS ANSWER_AFTER
FROM labeled b
LEFT JOIN labeled a ON a.QUESTION = b.QUESTION AND a.PHASE = 'AFTER'
WHERE b.PHASE = 'BEFORE'
ORDER BY b.QUESTION;

-- The ground truth for the five questions, computed from the table.
SELECT COUNT_IF(PRIORITY = 'P1' AND STATUS = 'OPEN')                                  AS URGENT_OPEN,
       COUNT_IF(PRIORITY IN ('P1', 'P2') AND STATUS = 'OPEN' AND PRODUCT = 'Mobile App') AS ESCALATED_MOBILE_APP,
       COUNT_IF(STATUS = 'PENDING_CUSTOMER')                                          AS WAITING_ON_CUSTOMER,
       ROUND(AVG(IFF(PRODUCT = 'Billing', HOURS_TO_RESOLVE, NULL)), 2)                AS AVG_HOURS_BILLING,
       COUNT_IF(PRODUCT = 'Billing' AND STATUS = 'RESOLVED')                          AS RESOLVED_BILLING
FROM TICKETS;
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- Refinement loop from agent logs: teardown
-- Drops the role first (which also removes the READ UNREDACTED grant from 02),
-- then the database (agent, semantic view, tables, procedure) and the warehouse.
-- The agent's events stay in SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS: ingested
-- rows can't be modified, and only a role with SNOWFLAKE.AI_OBSERVABILITY_ADMIN
-- can delete them for retention management.
-- =============================================================================

SET DB        = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS';
SET WH        = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_WH';
SET ROLE_NAME = 'COOKBOOK_REFINEMENT_LOOP_FROM_AGENT_LOGS_ROLE';

USE ROLE ACCOUNTADMIN;

DROP ROLE IF EXISTS IDENTIFIER($ROLE_NAME);
DROP DATABASE IF EXISTS IDENTIFIER($DB);
DROP WAREHOUSE IF EXISTS IDENTIFIER($WH);

SHOW DATABASES LIKE 'COOKBOOK_REFINEMENT_LOOP%';
SHOW WAREHOUSES LIKE 'COOKBOOK_REFINEMENT_LOOP%';
SHOW ROLES LIKE 'COOKBOOK_REFINEMENT_LOOP%';
```
