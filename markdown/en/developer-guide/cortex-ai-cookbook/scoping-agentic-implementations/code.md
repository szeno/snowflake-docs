# Scoping agentic implementations: from ‘talk to your data’ to a testable agent spec: code

Every file in the [Scoping agentic implementations: from ‘talk to your data’ to a testable agent spec](/developer-guide/cortex-ai-cookbook/scoping-agentic-implementations) recipe. To run the recipe, download [scoping-agentic-implementations.zip](/static/samples/cortex-ai-cookbook/scoping-agentic-implementations.zip), unzip it, and run the scripts from the `scoping-agentic-implementations/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/scoping-agentic-implementations); the zip includes it as `README.md`.

## `config/`

### `config/eval_config.yaml`

Copy code

```
# Evaluation config for the Phase 1 agent. Upload it to the EVAL_CONFIGS stage
# as eval_config.yaml (the name the README commands use), after you replace the
# agent name and version.
#
# There is no `dataset:` block: 03_eval_dataset.sql already registered
# SCOPING_EVAL_DATASET, and a `dataset:` block would try to recreate it on
# every run.
evaluation:
  agent_params:
    agent_name: "MY_AGENT_DB.MY_AGENT_SCHEMA.MY_AGENT"
    agent_type: "CORTEX AGENT"
    agent_version: "VERSION$1" # pin a committed version so runs are comparable
  run_params:
    label: "phase-1-baseline"
    description: "Baseline against the scoping workshop dataset"
  source_metadata:
    type: "dataset"
    dataset_name: "COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS.LAB.SCOPING_EVAL_DATASET"

# Pin metric versions: scores from different versions are not comparable, and
# unpinned metrics roll forward when a judge model is deprecated.
metrics:
  - name: "answer_correctness"
    version: "v3"
  - name: "logical_consistency"
    version: "v3"
  # tool_selection_accuracy is in Public Preview. To use it, add
  # ground_truth_invocations to GROUND_TRUTH, then uncomment:
  # - name: "tool_selection_accuracy"
  #   version: "v3"
```

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- 01_setup.sql
-- Lab objects for the scoping workshop: a role, warehouse, and database, a
-- small synthetic sales table to anchor questions in real columns, an
-- entitlements table for the multi-tenancy exercise, and a stage for
-- evaluation configs with the file format evaluations require.
-- Run as ACCOUNTADMIN (or a role with CREATE ROLE, CREATE WAREHOUSE, CREATE DATABASE).

SET cookbook_db   = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS';
SET cookbook_wh   = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS_WH';
SET cookbook_role = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS_ROLE';
SET lab_schema    = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS.LAB';
SET me            = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($cookbook_role)
  COMMENT = 'Cookbook scoping-agentic-implementations lab role';
-- Rolls up to ACCOUNTADMIN, not SYSADMIN: ACCOUNTADMIN can drop the lab objects in
-- 99_teardown.sql, and 04_observability.sql gives this role unredacted reads of an
-- agent's conversations, which SYSADMIN holders would otherwise inherit.
GRANT ROLE IDENTIFIER($cookbook_role) TO ROLE ACCOUNTADMIN;
GRANT ROLE IDENTIFIER($cookbook_role) TO USER IDENTIFIER($me);

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($cookbook_role);

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($lab_schema);
GRANT OWNERSHIP ON SCHEMA IDENTIFIER($lab_schema) TO ROLE IDENTIFIER($cookbook_role) COPY CURRENT GRANTS;
GRANT OWNERSHIP ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($cookbook_role) COPY CURRENT GRANTS;

-- AI_COMPLETE and AI_CLASSIFY need CORTEX_USER. USAGE_VIEWER exposes the
-- ACCOUNT_USAGE views used in 04_observability.sql.
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($cookbook_role);
GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER TO ROLE IDENTIFIER($cookbook_role);
-- The baseline evaluation (Walkthrough, Activity 4) is managed by tasks, so the
-- role that starts it needs EXECUTE TASK on the account. The grant goes away
-- when 99_teardown.sql drops the role.
GRANT EXECUTE TASK ON ACCOUNT TO ROLE IDENTIFIER($cookbook_role);

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($lab_schema);

-- Evaluation configs are read as single-column text: CSV with no field delimiter.
CREATE FILE FORMAT IF NOT EXISTS YAML_FILE_FORMAT
  TYPE = 'CSV'
  FIELD_DELIMITER = NONE
  RECORD_DELIMITER = '\n'
  SKIP_HEADER = 0
  FIELD_OPTIONALLY_ENCLOSED_BY = NONE
  ESCAPE_UNENCLOSED_FIELD = NONE;

-- Qualify the format name so the stage resolves it from any session schema.
CREATE STAGE IF NOT EXISTS EVAL_CONFIGS
  FILE_FORMAT = COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS.LAB.YAML_FILE_FORMAT
  COMMENT = 'Evaluation configuration files (eval_config.yaml)';

-- Synthetic deals. Questions in the taxonomy should be answerable from columns
-- that actually exist; this table keeps the exercise honest.
CREATE OR REPLACE TABLE SAMPLE_DEALS (
    deal_id           VARCHAR,
    region            VARCHAR,
    product_line      VARCHAR,
    revenue           NUMBER(12, 2),
    close_date        DATE,
    stage             VARCHAR,
    customer_name     VARCHAR,
    sales_cycle_days  NUMBER,
    owner_tenant_id   VARCHAR
);

INSERT INTO SAMPLE_DEALS VALUES
  ('D001', 'West',      'Enterprise', 4200000.00, '2024-06-15', 'Closed Won',  'Northwind Traders',    45,   'tenant_west'),
  ('D002', 'East',      'Mid-Market',  850000.00, '2024-06-20', 'Closed Won',  'Contoso Bank',         30,   'tenant_east'),
  ('D003', 'West',      'Enterprise', 3100000.00, '2024-07-10', 'Closed Won',  'Acme Health',          60,   'tenant_west'),
  ('D004', 'Northeast', 'SMB',         120000.00, '2024-07-22', 'Closed Lost', 'Fabrikam',             25,   'tenant_east'),
  ('D005', 'South',     'Mid-Market',  950000.00, '2024-08-05', 'Closed Won',  'Tailspin Toys',        35,   'tenant_south'),
  ('D006', 'West',      'Enterprise', 5500000.00, '2024-08-18', 'Stage 3',     'Wide World Importers', NULL, 'tenant_west'),
  ('D007', 'East',      'SMB',         200000.00, '2024-09-01', 'Closed Won',  'Litware',              20,   'tenant_east'),
  ('D008', 'Northeast', 'Enterprise', 2800000.00, '2024-09-15', 'Closed Lost', 'Adventure Works',      90,   'tenant_east'),
  ('D009', 'South',     'Mid-Market', 1100000.00, '2024-10-01', 'Closed Won',  'Proseware',            40,   'tenant_south'),
  ('D010', 'West',      'Enterprise', 6200000.00, '2024-10-20', 'Stage 4',     'Woodgrove Bank',       NULL, 'tenant_west');

-- Entitlements: maps an application user to the rows they may see, without a
-- Snowflake user, role, or grant per person. Used in the multi-tenancy exercise.
CREATE OR REPLACE TABLE ENTITLEMENTS (
    tenant_id       VARCHAR,
    user_id         VARCHAR,
    allowed_region  VARCHAR,
    access_level    VARCHAR
);

INSERT INTO ENTITLEMENTS VALUES
  ('tenant_west',  'user_001', 'West',      'full'),
  ('tenant_west',  'user_002', 'West',      'read_only'),
  ('tenant_east',  'user_003', 'East',      'full'),
  ('tenant_east',  'user_003', 'Northeast', 'full'),
  ('tenant_east',  'user_004', 'East',      'read_only'),
  ('tenant_south', 'user_005', 'South',     'full');

SELECT COUNT(*) AS deals FROM SAMPLE_DEALS;
```

### `sql/02_question_taxonomy.sql`

Copy code

```
-- 02_question_taxonomy.sql
-- Activity 2 and 3 of the workshop: record the seed question taxonomy, then
-- expand it with AI_COMPLETE (new questions per category, plus rephrasings of
-- the questions that users ask most). One AI_COMPLETE call per category or seed
-- row, with a JSON schema so the output is always parseable.
-- Replace the seed rows with your own; keep every date absolute.
-- Run as the lab role after 01_setup.sql.

SET cookbook_wh   = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS_WH';
SET cookbook_role = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS_ROLE';
SET lab_schema    = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS.LAB';
SET model         = 'claude-sonnet-4-6';
SET persona       = 'a regional sales manager who reads dashboards but does not write SQL';

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($lab_schema);

-- Seed taxonomy: what the Phase 1 persona would actually type on a Monday morning.
-- category: lookup | aggregation | reasoning | policy | out_of_scope
-- expected_tool: the Snowflake primitive that should answer it (or none)
CREATE OR REPLACE TABLE SEED_QUESTIONS (
    question       VARCHAR,
    category       VARCHAR,
    expected_tool  VARCHAR,
    risk           VARCHAR,
    phase          NUMBER
);

INSERT INTO SEED_QUESTIONS VALUES
  ('What was closed-won revenue for the West region between April 1 and June 30, 2024?',      'lookup',       'cortex_analyst', 'medium', 1),
  ('How many deals closed won in September 2024?',                                           'lookup',       'cortex_analyst', 'medium', 1),
  ('Which customer had the largest closed-won deal in 2024?',                                'lookup',       'cortex_analyst', 'low',    1),
  ('Compare closed-won revenue by product line for July 1 to September 30, 2024.',           'aggregation',  'cortex_analyst', 'high',   1),
  ('Which region had the highest win rate between June 1 and October 31, 2024?',             'aggregation',  'cortex_analyst', 'high',   1),
  ('What was the average sales cycle in days for Enterprise deals closed in 2024?',          'aggregation',  'cortex_analyst', 'medium', 1),
  ('Why did the Northeast region lose both of its deals between July and September 2024?',   'reasoning',    'cortex_analyst', 'high',   2),
  ('What is our discount approval process for Enterprise deals?',                            'policy',       'cortex_search',  'high',   2),
  ('What are the territory assignment criteria?',                                            'policy',       'cortex_search',  'high',   2),
  ('Write a cold outreach email for Woodgrove Bank.',                                        'out_of_scope', 'none',           'medium', 1),
  ('What is our competitor''s pricing for Enterprise plans?',                                'out_of_scope', 'none',           'high',   1);

SELECT category, COUNT(*) AS seed_questions FROM SEED_QUESTIONS GROUP BY category ORDER BY category;

-- New questions per category. The prompt carries the category's existing
-- examples so the model stays inside the taxonomy instead of inventing new scope.
CREATE OR REPLACE TABLE SYNTHETIC_QUESTIONS AS
WITH by_category AS (
    SELECT category,
           ANY_VALUE(expected_tool) AS expected_tool,
           MIN(phase)               AS phase,
           LISTAGG('- ' || question, '\n') WITHIN GROUP (ORDER BY question) AS examples
      FROM SEED_QUESTIONS
     GROUP BY category
),
generated AS (
    SELECT category, expected_tool, phase,
           AI_COMPLETE(
             model => $model,
             prompt => 'You are helping build an evaluation dataset for an AI agent used by ' || $persona || '. '
                    || 'The agent answers questions about sales deals (region, product line, revenue, close date, stage, customer, sales cycle). '
                    || 'Category: ' || category || '.\nExisting examples:\n' || examples || '\n'
                    || 'Write 3 new questions in this category that differ from the examples in metric, dimension, or time period. '
                    || 'Use absolute dates in 2024 (for example "between July 1 and September 30, 2024"), never relative dates such as "last month". '
                    || 'Rate each question''s risk: low (informational), medium (operational decision), high (financial or strategic decision).',
             model_parameters => {'temperature': 0},
             response_format => {
               'type': 'json',
               'schema': {
                 'type': 'object',
                 'properties': {
                   'questions': {
                     'type': 'array',
                     'items': {
                       'type': 'object',
                       'properties': {
                         'question': {'type': 'string'},
                         'risk': {'type': 'string', 'enum': ['low', 'medium', 'high']}
                       },
                       'required': ['question', 'risk']
                     }
                   }
                 },
                 'required': ['questions']
               }
             }
           ) AS resp
      FROM by_category
)
SELECT q.value:question::VARCHAR AS question,
       g.category,
       g.expected_tool,
       q.value:risk::VARCHAR     AS risk,
       g.phase,
       'synthetic_new'           AS source,
       NULL::VARCHAR             AS original_question
  FROM generated g,
       LATERAL FLATTEN(input => g.resp:questions) q;

-- Rephrasings of the Phase 1 lookup and aggregation questions: same intent,
-- different wording. These catch agents that only work for one phrasing.
INSERT INTO SYNTHETIC_QUESTIONS
WITH generated AS (
    SELECT s.question, s.category, s.expected_tool, s.risk, s.phase,
           AI_COMPLETE(
             model => $model,
             prompt => 'Rephrase this question 2 different ways. Ask for exactly the same information, keep the same dates, '
                    || 'and vary the wording and formality the way a busy manager would type it.\nOriginal: ' || s.question,
             model_parameters => {'temperature': 0},
             response_format => {
               'type': 'json',
               'schema': {
                 'type': 'object',
                 'properties': {'variations': {'type': 'array', 'items': {'type': 'string'}}},
                 'required': ['variations']
               }
             }
           ) AS resp
      FROM SEED_QUESTIONS s
     WHERE s.phase = 1 AND s.category IN ('lookup', 'aggregation')
)
SELECT v.value::VARCHAR, g.category, g.expected_tool, g.risk, g.phase, 'variation', g.question
  FROM generated g,
       LATERAL FLATTEN(input => g.resp:variations) v;

-- The full question set: seeds plus synthetic, one table to review with the team.
CREATE OR REPLACE VIEW ALL_QUESTIONS AS
SELECT question, category, expected_tool, risk, phase, 'manual' AS source, NULL::VARCHAR AS original_question
  FROM SEED_QUESTIONS
UNION ALL
SELECT question, category, expected_tool, risk, phase, source, original_question
  FROM SYNTHETIC_QUESTIONS;

SELECT source, category, COUNT(*) AS questions
  FROM ALL_QUESTIONS
 GROUP BY source, category
 ORDER BY source, category;
```

### `sql/03_eval_dataset.sql`

Copy code

```
-- 03_eval_dataset.sql
-- Activity 4: turn the Phase 1 questions into a Cortex Agent evaluation dataset.
--   INPUT_QUERY  VARCHAR  the question
--   GROUND_TRUTH VARIANT  {"ground_truth_output": "..."} plus your own review keys
-- Where the answer is known, compute it from the data and state the literal value.
-- Everywhere else, draft a rubric with AI_COMPLETE and mark it needs_review so a
-- person signs off before the dataset gates anything.
-- Run as the lab role after 02_question_taxonomy.sql.

SET cookbook_wh   = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS_WH';
SET cookbook_role = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS_ROLE';
SET lab_schema    = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS.LAB';
SET model         = 'claude-sonnet-4-6';

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($lab_schema);

CREATE OR REPLACE TABLE EVAL_QUESTIONS (
    INPUT_QUERY  VARCHAR,
    GROUND_TRUTH VARIANT
);

-- 1. Literal ground truth for questions with one correct answer, computed from
--    SAMPLE_DEALS so the expected value cannot drift from the data.
--    OBJECT_CONSTRUCT returns OBJECT; TO_VARIANT guarantees the column type.
--    These are the sample seeds' answers. Rows are kept only if the question is
--    still in your Phase 1 taxonomy; replace them with queries for your own
--    literal questions, which otherwise get a drafted rubric in step 2.
INSERT INTO EVAL_QUESTIONS
SELECT $1, $2 FROM (
SELECT 'What was closed-won revenue for the West region between April 1 and June 30, 2024?',
       TO_VARIANT(OBJECT_CONSTRUCT(
         'ground_truth_output',
           'Closed-won revenue for the West region between April 1 and June 30, 2024 is $'
           || TRIM(TO_VARCHAR(SUM(revenue), '999,999,999.00')) || '. The answer must use that date range and count only Closed Won deals.',
         'category', 'lookup', 'needs_review', FALSE))
  FROM SAMPLE_DEALS
 WHERE region = 'West' AND stage = 'Closed Won' AND close_date BETWEEN '2024-04-01' AND '2024-06-30'
UNION ALL
SELECT 'How many deals closed won in September 2024?',
       TO_VARIANT(OBJECT_CONSTRUCT(
         'ground_truth_output',
           TO_VARCHAR(COUNT(*)) || ' deal(s) closed won between September 1 and September 30, 2024. Closed Lost deals in that month must not be counted.',
         'category', 'lookup', 'needs_review', FALSE))
  FROM SAMPLE_DEALS
 WHERE stage = 'Closed Won' AND close_date BETWEEN '2024-09-01' AND '2024-09-30'
UNION ALL
SELECT 'Which customer had the largest closed-won deal in 2024?',
       TO_VARIANT(OBJECT_CONSTRUCT(
         'ground_truth_output',
           MAX_BY(customer_name, revenue) || ' had the largest closed-won deal in 2024, at $'
           || TRIM(TO_VARCHAR(MAX(revenue), '999,999,999.00')) || '. Open-stage deals must not be considered.',
         'category', 'lookup', 'needs_review', FALSE))
  FROM SAMPLE_DEALS
 WHERE stage = 'Closed Won' AND YEAR(close_date) = 2024
)
WHERE $1 IN (SELECT question FROM ALL_QUESTIONS WHERE phase = 1);

-- 2. Drafted rubrics for the remaining Phase 1 questions: what a correct answer
--    must and must not contain. One AI_COMPLETE call per question.
INSERT INTO EVAL_QUESTIONS
WITH phase1 AS (
    SELECT question, category, expected_tool, source
      FROM ALL_QUESTIONS
     WHERE phase = 1
       AND question NOT IN (SELECT INPUT_QUERY FROM EVAL_QUESTIONS)
),
drafted AS (
    SELECT question, category, expected_tool, source,
           AI_COMPLETE(
             model => $model,
             prompt => 'Write the ground truth rubric used to grade an AI sales agent''s answer to the question below. '
                    || 'In 2 or 3 sentences, state what a correct answer must contain and what it must not contain. '
                    || 'Be specific enough that two reviewers would agree, but do not invent numbers. '
                    || CASE WHEN category = 'out_of_scope'
                            THEN 'This question is out of scope: a correct answer declines, says what the agent can help with, and does not attempt the task. '
                            ELSE '' END
                    || '\nCategory: ' || category || '\nQuestion: ' || question,
             model_parameters => {'temperature': 0},
             response_format => {
               'type': 'json',
               'schema': {
                 'type': 'object',
                 'properties': {'ground_truth_output': {'type': 'string'}},
                 'required': ['ground_truth_output']
               }
             }
           ) AS resp
      FROM phase1
)
SELECT question,
       TO_VARIANT(OBJECT_CONSTRUCT(
         'ground_truth_output', resp:ground_truth_output::VARCHAR,
         'category', category,
         'expected_tool', expected_tool,
         'source', source,
         'needs_review', TRUE))
  FROM drafted
 WHERE resp:ground_truth_output IS NOT NULL;

SELECT GROUND_TRUTH:category::VARCHAR     AS category,
       GROUND_TRUTH:needs_review::BOOLEAN AS needs_review,
       COUNT(*)                           AS questions
  FROM EVAL_QUESTIONS
 GROUP BY ALL
 ORDER BY category, needs_review;

-- 3. Register the dataset. Recreate it so this script stays idempotent; the
--    dataset is a snapshot, so rerun this step after you edit EVAL_QUESTIONS.
DROP DATASET IF EXISTS SCOPING_EVAL_DATASET;

CALL SYSTEM$CREATE_EVALUATION_DATASET(
  'Cortex Agent',
  'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS.LAB.EVAL_QUESTIONS',
  'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS.LAB.SCOPING_EVAL_DATASET',
  OBJECT_CONSTRUCT('query_text', 'INPUT_QUERY', 'expected_tools', 'GROUND_TRUTH')
);

SHOW DATASETS IN SCHEMA IDENTIFIER($lab_schema);
```

### `sql/04_observability.sql`

Copy code

```
-- 04_observability.sql
-- Post-deploy: compare what users actually ask with the taxonomy you scoped.
-- Point the agent_* variables at your deployed Phase 1 agent. An account
-- administrator grants the lab role two things first:
--   GRANT MONITOR ON AGENT <db>.<schema>.<agent> TO ROLE COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS_ROLE;
--   GRANT READ UNREDACTED AI OBSERVABILITY EVENTS TABLE ON ACCOUNT
--     TO ROLE COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS_ROLE;
-- plus USAGE on the agent's database and schema. MONITOR lets the role read the
-- agent's monitoring events. The account privilege lets it see the text of
-- users' questions in them; without it the question field is redacted and
-- step 2b stops the script. It exposes every conversation the role can monitor,
-- so grant it only to people allowed to read them. Dropping the role in
-- 99_teardown.sql removes both grants.
-- Run as the lab role.

SET cookbook_wh   = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS_WH';
SET cookbook_role = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS_ROLE';
SET lab_schema    = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS.LAB';
SET agent_db      = 'MY_AGENT_DB';      -- database of your Phase 1 agent
SET agent_schema  = 'MY_AGENT_SCHEMA';  -- schema of your Phase 1 agent
SET agent_name    = 'MY_AGENT';         -- agent name
SET lookback_days = 30;

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($lab_schema);

-- 1. Volume and cost by user and surface, from the documented usage view.
--    Rows can take up to about an hour to appear.
SELECT USER_NAME,
       METADATA:interaction_interface::VARCHAR AS surface,
       COUNT(*)                                AS requests,
       SUM(TOKEN_CREDITS)                      AS token_credits,
       SUM(TOKENS)                             AS tokens
  FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AGENT_USAGE_HISTORY
 WHERE AGENT_DATABASE_NAME = $agent_db
   AND AGENT_SCHEMA_NAME   = $agent_schema
   AND AGENT_NAME          = $agent_name
   AND START_TIME >= DATEADD('day', -$lookback_days, CURRENT_TIMESTAMP())
 GROUP BY ALL
 ORDER BY token_credits DESC;

-- 2. The questions users asked. Each turn has one record_root span; its input
--    is the user's message. Evaluation runs write the same spans with a run
--    name, so filter those out to keep only real usage. Snowflake notes that
--    event attribute names can change; re-check them if this returns nothing.
CREATE OR REPLACE TABLE OBSERVED_QUESTIONS AS
SELECT TIMESTAMP                                                               AS asked_at,
       RECORD_ATTRIBUTES:"ai.observability.record_root.input"::VARCHAR         AS question,
       RECORD_ATTRIBUTES:"snow.ai.observability.object.version.name"::VARCHAR  AS agent_version
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_EVENTS(
         $agent_db, $agent_schema, $agent_name, 'CORTEX AGENT'))
 WHERE RECORD_ATTRIBUTES:"ai.observability.span_type"::VARCHAR = 'record_root'
   AND RECORD_ATTRIBUTES:"snow.ai.observability.run.name" IS NULL
   AND TIMESTAMP >= DATEADD('day', -$lookback_days, CURRENT_TIMESTAMP());

-- 2b. Stop if the questions are redacted. Without READ UNREDACTED AI
--     OBSERVABILITY EVENTS TABLE the spans come back with the question field
--     removed, so every question is NULL and step 3 would report 0% real usage
--     for every category without an error.
EXECUTE IMMEDIATE $$
DECLARE
  redacted EXCEPTION (-20001, 'Real-usage turns were found, but their question text is redacted. Grant READ UNREDACTED AI OBSERVABILITY EVENTS TABLE ON ACCOUNT to the lab role (see the header) and run this file again.');
  turns    INTEGER;
  readable INTEGER;
BEGIN
  SELECT COUNT(*), COUNT(question) INTO :turns, :readable FROM OBSERVED_QUESTIONS;
  IF (turns > 0 AND readable = 0) THEN
    RAISE redacted;
  END IF;
  RETURN turns || ' real-usage turns, ' || readable || ' with readable question text';
END;
$$;

-- 3. Classify observed questions into the taxonomy categories and compare the
--    distribution with the scoped one. Categories come from SEED_QUESTIONS so
--    the two stay in sync.
CREATE OR REPLACE TABLE OBSERVED_CLASSIFIED AS
SELECT o.question,
       o.agent_version,
       AI_CLASSIFY(o.question, c.categories):labels[0]::VARCHAR AS category
  FROM OBSERVED_QUESTIONS o,
       (SELECT ARRAY_AGG(DISTINCT category) AS categories FROM SEED_QUESTIONS) c
 WHERE o.question IS NOT NULL;

WITH observed AS (
    SELECT category, COUNT(*) AS n FROM OBSERVED_CLASSIFIED GROUP BY category
),
scoped AS (
    SELECT category, COUNT(*) AS n FROM ALL_QUESTIONS WHERE phase = 1 GROUP BY category
)
SELECT COALESCE(o.category, s.category)                                   AS category,
       ROUND(100 * COALESCE(s.n, 0) / NULLIF(SUM(s.n) OVER (), 0), 1)     AS pct_of_eval_set,
       ROUND(100 * COALESCE(o.n, 0) / NULLIF(SUM(o.n) OVER (), 0), 1)     AS pct_of_real_usage
  FROM observed o
  FULL OUTER JOIN scoped s ON o.category = s.category
 ORDER BY pct_of_real_usage DESC NULLS LAST;
```

### `sql/99_teardown.sql`

Copy code

```
-- 99_teardown.sql
-- Removes everything this lab created: the database (tables, views, stage,
-- file format, and evaluation dataset), the warehouse, and the role.
-- No account parameters were changed. Run as ACCOUNTADMIN.
-- If you granted the lab role MONITOR on your own agent or READ UNREDACTED AI
-- OBSERVABILITY EVENTS TABLE on the account, dropping the role removes those grants too.

SET cookbook_db   = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS';
SET cookbook_wh   = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS_WH';
SET cookbook_role = 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS_ROLE';

USE ROLE ACCOUNTADMIN;

DROP DATABASE IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);
DROP ROLE IF EXISTS IDENTIFIER($cookbook_role);

SHOW DATABASES LIKE 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS%';
SHOW WAREHOUSES LIKE 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS%';
SHOW ROLES LIKE 'COOKBOOK_SCOPING_AGENTIC_IMPLEMENTATIONS%';
```
