# Mixed-grain tables: diagnose and fix wrong agent answers with a GRAIN dimension and verified queries: code

Every file in the [Mixed-grain tables: diagnose and fix wrong agent answers with a GRAIN dimension and verified queries](/developer-guide/cortex-ai-cookbook/mixed-grain-and-verified-queries) recipe. To run the recipe, download [mixed-grain-and-verified-queries.zip](/static/samples/cortex-ai-cookbook/mixed-grain-and-verified-queries.zip), unzip it, and run the scripts from the `mixed-grain-and-verified-queries/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/mixed-grain-and-verified-queries); the zip includes it as `README.md`.

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- =============================================================================
-- Mixed-grain semantic views: setup
-- A store sales table that holds two grains as sibling rows: one row per store
-- per day, and one roll-up row per store per month. Nothing in the table says
-- which is which except PERIOD_START = PERIOD_END on daily rows. Also creates
-- the test questions the agent is scored on, with expected answers computed
-- from the data.
-- =============================================================================

SET DB        = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES';
SET WH        = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_WH';
SET ROLE_NAME = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_ROLE';
SET ANALYST_ROLE = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_ANALYST';
SET CUR_USER  = '"' || CURRENT_USER() || '"';

-- -----------------------------------------------------------------------------
-- 1. Account objects (ACCOUNTADMIN only for these statements)
-- -----------------------------------------------------------------------------
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($ROLE_NAME)
  COMMENT = 'Cortex AI Cookbook: mixed-grain-and-verified-queries';
GRANT ROLE IDENTIFIER($ROLE_NAME) TO USER IDENTIFIER($CUR_USER);
-- Keeps the recipe role in the system hierarchy so ACCOUNTADMIN can drop its objects in teardown.
GRANT ROLE IDENTIFIER($ROLE_NAME) TO ROLE SYSADMIN;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($ROLE_NAME);

-- A consumer role that only gets SELECT on the semantic view. Used to show that
-- CREATE OR ALTER keeps grants when the view is fixed in 06.
CREATE ROLE IF NOT EXISTS IDENTIFIER($ANALYST_ROLE)
  COMMENT = 'Cortex AI Cookbook: mixed-grain-and-verified-queries consumer';

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($WH)
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cortex AI Cookbook: mixed-grain-and-verified-queries';
GRANT USAGE, OPERATE ON WAREHOUSE IDENTIFIER($WH) TO ROLE IDENTIFIER($ROLE_NAME);

CREATE DATABASE IF NOT EXISTS IDENTIFIER($DB)
  COMMENT = 'Cortex AI Cookbook: mixed-grain-and-verified-queries';
GRANT OWNERSHIP ON DATABASE IDENTIFIER($DB) TO ROLE IDENTIFIER($ROLE_NAME) COPY CURRENT GRANTS;

-- -----------------------------------------------------------------------------
-- 2. Data (runs as the recipe role)
-- -----------------------------------------------------------------------------
USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
CREATE SCHEMA IF NOT EXISTS RETAIL;
USE SCHEMA RETAIL;

-- Four fictional Northwind Outfitters stores, January to March 2026.
CREATE OR REPLACE TABLE STORE_SALES_SUMMARY (
    STORE_ID      VARCHAR,
    STORE_NAME    VARCHAR,
    REGION        VARCHAR,
    PERIOD_START  DATE,
    PERIOD_END    DATE,
    NET_SALES     NUMBER(12,2),
    ORDER_COUNT   NUMBER,
    SALES_TARGET  NUMBER(12,2)      -- set on monthly rows only
);

-- Daily rows. Values are deterministic (hash-based), so every run gets the same numbers.
INSERT INTO STORE_SALES_SUMMARY
WITH stores AS (
  SELECT * FROM VALUES
    ('S01', 'Harbor Street', 'North', 1.00),
    ('S02', 'Mill Road',     'North', 0.85),
    ('S03', 'Canal Park',    'South', 1.20),
    ('S04', 'Elm Square',    'South', 0.70) AS t(STORE_ID, STORE_NAME, REGION, SCALE)
), days AS (
  SELECT DATEADD(day, SEQ4(), '2026-01-01'::DATE) AS D
  FROM TABLE(GENERATOR(ROWCOUNT => 90))
)
SELECT s.STORE_ID, s.STORE_NAME, s.REGION, d.D, d.D,
       ROUND(s.SCALE * (900 + MOD(ABS(HASH(s.STORE_ID, d.D)), 600)
             + IFF(DAYOFWEEKISO(d.D) >= 6, 400, 0)), 2) AS NET_SALES,
       ROUND(s.SCALE * (18 + MOD(ABS(HASH(d.D, s.STORE_ID)), 14))) AS ORDER_COUNT,
       NULL
FROM stores s CROSS JOIN days d;

-- Monthly roll-up rows: the exact sum of each store's daily rows, plus a target.
INSERT INTO STORE_SALES_SUMMARY
SELECT STORE_ID, STORE_NAME, REGION,
       DATE_TRUNC('month', PERIOD_START) AS PERIOD_START,
       LAST_DAY(PERIOD_START)            AS PERIOD_END,
       SUM(NET_SALES), SUM(ORDER_COUNT),
       ROUND(SUM(NET_SALES) * CASE STORE_ID
                                WHEN 'S01' THEN 0.97 WHEN 'S02' THEN 1.04
                                WHEN 'S03' THEN 0.99 ELSE 1.06 END, -2) AS SALES_TARGET
FROM STORE_SALES_SUMMARY
WHERE PERIOD_START = PERIOD_END
GROUP BY STORE_ID, STORE_NAME, REGION, DATE_TRUNC('month', PERIOD_START), LAST_DAY(PERIOD_START);

-- -----------------------------------------------------------------------------
-- 3. Test questions and their correct answers, computed from the daily rows
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE AGENT_TEST_QUESTIONS (
    QUESTION_ID     VARCHAR,
    QUESTION        VARCHAR,
    EXPECTED_VALUE  NUMBER(14,2),    -- for numeric answers
    EXPECTED_STORES ARRAY            -- for "which stores" answers
);

INSERT INTO AGENT_TEST_QUESTIONS (QUESTION_ID, QUESTION, EXPECTED_VALUE)
SELECT 'Q1', 'What were total net sales for the Harbor Street store in February 2026?', SUM(NET_SALES)
FROM STORE_SALES_SUMMARY
WHERE PERIOD_START = PERIOD_END AND STORE_NAME = 'Harbor Street'
  AND PERIOD_START BETWEEN '2026-02-01' AND '2026-02-28';

INSERT INTO AGENT_TEST_QUESTIONS (QUESTION_ID, QUESTION, EXPECTED_VALUE)
SELECT 'Q2', 'What were total net sales across all stores in Q1 2026 (January through March)?', SUM(NET_SALES)
FROM STORE_SALES_SUMMARY
WHERE PERIOD_START = PERIOD_END;

INSERT INTO AGENT_TEST_QUESTIONS (QUESTION_ID, QUESTION, EXPECTED_VALUE)
SELECT 'Q3', 'What was the average daily net sales for Canal Park in January 2026?', ROUND(AVG(NET_SALES), 2)
FROM STORE_SALES_SUMMARY
WHERE PERIOD_START = PERIOD_END AND STORE_NAME = 'Canal Park'
  AND PERIOD_START BETWEEN '2026-01-01' AND '2026-01-31';

INSERT INTO AGENT_TEST_QUESTIONS (QUESTION_ID, QUESTION, EXPECTED_STORES)
SELECT 'Q4', 'Which stores missed their March 2026 sales target?', ARRAY_AGG(STORE_NAME) WITHIN GROUP (ORDER BY STORE_NAME)
FROM STORE_SALES_SUMMARY
WHERE PERIOD_START <> PERIOD_END AND PERIOD_START = '2026-03-01' AND NET_SALES < SALES_TARGET;

SELECT QUESTION_ID, QUESTION, EXPECTED_VALUE, EXPECTED_STORES FROM AGENT_TEST_QUESTIONS ORDER BY QUESTION_ID;
```

### `sql/02_semantic_view_before.sql`

Copy code

```
-- =============================================================================
-- Mixed-grain semantic views: the "before" semantic view
-- A reasonable-looking first draft. It exposes the table as if every row were a
-- day of sales. Nothing tells Cortex Analyst that monthly roll-up rows sit next
-- to the daily rows, so sums and averages over a date range count each sale
-- twice (or skew the average).
-- =============================================================================

SET DB        = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES';
SET WH        = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_WH';
SET ROLE_NAME = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_ROLE';
SET ANALYST_ROLE = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_ANALYST';

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA RETAIL;

CREATE OR ALTER SEMANTIC VIEW STORE_SALES_SV
  TABLES (
    sales AS STORE_SALES_SUMMARY
      PRIMARY KEY (STORE_ID, PERIOD_START, PERIOD_END)
      COMMENT = 'Northwind Outfitters store sales.'
  )
  FACTS (
    sales.net_sales AS NET_SALES COMMENT = 'Net sales in USD.',
    sales.order_count AS ORDER_COUNT COMMENT = 'Number of orders.',
    sales.sales_target AS SALES_TARGET COMMENT = 'Sales target in USD.'
  )
  DIMENSIONS (
    sales.store_name AS STORE_NAME COMMENT = 'Store name.',
    sales.region AS REGION COMMENT = 'Store region: North or South.',
    sales.sale_date AS PERIOD_START COMMENT = 'Date of the sales.'
  )
  METRICS (
    sales.total_net_sales AS SUM(net_sales) COMMENT = 'Total net sales in USD.',
    sales.avg_net_sales AS AVG(net_sales) COMMENT = 'Average net sales in USD.',
    sales.total_orders AS SUM(order_count) COMMENT = 'Total orders.',
    sales.total_target AS SUM(sales_target) COMMENT = 'Total sales target in USD.'
  )
  COMMENT = 'Store sales for Northwind Outfitters.';

-- A consumer role needs SELECT on the semantic view, not on the table.
GRANT USAGE ON DATABASE IDENTIFIER($DB) TO ROLE IDENTIFIER($ANALYST_ROLE);
GRANT USAGE ON SCHEMA RETAIL TO ROLE IDENTIFIER($ANALYST_ROLE);
GRANT SELECT ON SEMANTIC VIEW STORE_SALES_SV TO ROLE IDENTIFIER($ANALYST_ROLE);
```

### `sql/03_agent_and_test_harness.sql`

Copy code

```
-- =============================================================================
-- Mixed-grain semantic views: the agent and the test harness
-- An agent with one Cortex Analyst tool over STORE_SALES_SV, and a procedure
-- that asks it every question in AGENT_TEST_QUESTIONS and scores the answers.
-- The agent itself never changes in this recipe: only the semantic view does.
-- =============================================================================

SET DB          = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES';
SET WH          = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_WH';
SET ROLE_NAME   = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_ROLE';
SET AGENT_MODEL = 'auto';   -- orchestration model; auto lets Snowflake choose

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA RETAIL;

-- 1. Agent. CREATE AGENT IF NOT EXISTS + MODIFY LIVE VERSION keeps grants on rerun.
--    The spec is built in a block so the tool warehouse comes from $WH and the
--    orchestration model from $AGENT_MODEL. Both are checked against a pattern
--    before they go into the spec.
EXECUTE IMMEDIATE $$
DECLARE
  wh VARCHAR;
  model VARCHAR;
  spec VARCHAR;
BEGIN
  SELECT UPPER($WH), LOWER($AGENT_MODEL) INTO :wh, :model;
  IF (NOT REGEXP_LIKE(wh, '^[A-Z][A-Z0-9_]*$')) THEN
    RETURN 'Not deployed: WH must be a plain identifier.';
  END IF;
  IF (NOT REGEXP_LIKE(model, '^[a-z0-9][a-z0-9._-]*$')) THEN
    RETURN 'Not deployed: AGENT_MODEL must be a model name such as auto or claude-sonnet-4-6.';
  END IF;
  spec := REPLACE(REPLACE('{
    "models": {"orchestration": "__MODEL__"},
    "instructions": {
      "response": "Answer with the number or list the user asked for, the period, and the store or region it covers.",
      "orchestration": "Use store_sales for every question about store sales, orders, and targets."
    },
    "tools": [
      {"tool_spec": {"type": "cortex_analyst_text_to_sql", "name": "store_sales",
                     "description": "Northwind Outfitters store sales, orders, and sales targets by store and date."}}
    ],
    "tool_resources": {
      "store_sales": {"semantic_view": "COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES.RETAIL.STORE_SALES_SV",
                      "execution_environment": {"type": "warehouse", "warehouse": "__WH__", "query_timeout": 60}}
    }
  }', '__WH__', wh), '__MODEL__', model);
  -- The spec is spliced into a quoted literal below; escape any apostrophe.
  spec := REPLACE(spec, '''', '''''');
  EXECUTE IMMEDIATE 'CREATE AGENT IF NOT EXISTS COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES.RETAIL.STORE_SALES_AGENT '
    || 'COMMENT = ''Cortex AI Cookbook: mixed-grain-and-verified-queries'' '
    || 'FROM SPECIFICATION ''' || spec || '''';
  EXECUTE IMMEDIATE 'ALTER AGENT COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES.RETAIL.STORE_SALES_AGENT '
    || 'MODIFY LIVE VERSION SET SPECIFICATION = ''' || spec || '''';
  RETURN 'Agent deployed with warehouse ' || wh || ' and orchestration model ' || model;
END;
$$;

-- 2. Results of every test run, one row per question per run.
CREATE TABLE IF NOT EXISTS AGENT_TEST_RESULTS (
    RUN_LABEL     VARCHAR,
    QUESTION_ID   VARCHAR,
    QUESTION      VARCHAR,
    ANSWER_TEXT   VARCHAR,
    AGENT_SQL     VARCHAR,
    EXPECTED      VARCHAR,
    PASSED        BOOLEAN,
    RESPONSE      VARIANT,
    RUN_AT        TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 3. Test harness (caller's rights). Numeric answers pass when a number in the
--    answer is within 0.5% of the expected value. "Which stores" answers are
--    judged by AI_COMPLETE with a boolean structured output.
CREATE OR REPLACE PROCEDURE RUN_AGENT_TESTS(RUN_LABEL VARCHAR, JUDGE_MODEL VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = 'Cortex AI Cookbook: asks STORE_SALES_AGENT every test question and scores the answers'
EXECUTE AS CALLER
AS
$$
DECLARE
  resp VARIANT;
  answer VARCHAR;
  agent_sql VARCHAR;
  expected VARCHAR;
  passed BOOLEAN;
  judge VARIANT;
  n_pass NUMBER DEFAULT 0;
  n_total NUMBER DEFAULT 0;
  v_qid VARCHAR;
  v_question VARCHAR;
  v_expected_value NUMBER(14,2);
  v_expected_stores ARRAY;
  v_content VARIANT;
  body VARCHAR;
BEGIN
  DELETE FROM COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES.RETAIL.AGENT_TEST_RESULTS WHERE RUN_LABEL = :run_label;
  LET rs RESULTSET := (SELECT QUESTION_ID, QUESTION, EXPECTED_VALUE, EXPECTED_STORES
                       FROM COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES.RETAIL.AGENT_TEST_QUESTIONS
                       ORDER BY QUESTION_ID);
  LET c1 CURSOR FOR rs;
  FOR q IN c1 DO
    v_qid := q.QUESTION_ID;
    v_question := q.QUESTION;
    v_expected_value := q.EXPECTED_VALUE;
    v_expected_stores := q.EXPECTED_STORES;
    passed := NULL;
    -- DATA_AGENT_RUN needs a constant request body, so build it into a variable first.
    body := TO_JSON(OBJECT_CONSTRUCT('messages', ARRAY_CONSTRUCT(OBJECT_CONSTRUCT(
              'role', 'user',
              'content', ARRAY_CONSTRUCT(OBJECT_CONSTRUCT('type', 'text', 'text', v_question))))));
    SELECT TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
             'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES.RETAIL.STORE_SALES_AGENT', :body))
      INTO :resp;
    v_content := resp:content;

    -- Final answer text, and the SQL the agent wrote (tool_use inputs only; tool
    -- results also carry the verified queries and the compiled SQL).
    SELECT LISTAGG(c.value:text::VARCHAR, ' ') WITHIN GROUP (ORDER BY c.index) INTO :answer
      FROM TABLE(FLATTEN(input => :v_content)) c WHERE c.value:type::VARCHAR = 'text';
    SELECT LISTAGG(s.value::VARCHAR, '\n---\n') INTO :agent_sql
      FROM TABLE(FLATTEN(input => :v_content, recursive => TRUE)) s
     WHERE s.path LIKE '%tool_use.input.sql' AND IS_VARCHAR(s.value);

    IF (v_expected_value IS NOT NULL) THEN
      expected := v_expected_value::VARCHAR;
      SELECT COUNT_IF(ABS(TRY_TO_NUMBER(REPLACE(n.value::VARCHAR, ',', ''), 18, 2) - :v_expected_value)
                      <= 0.005 * ABS(:v_expected_value)) > 0
        INTO :passed
        FROM TABLE(FLATTEN(input => REGEXP_SUBSTR_ALL(COALESCE(:answer, ''), '[0-9][0-9,]*[.]?[0-9]*'))) n;
    ELSE
      expected := ARRAY_TO_STRING(v_expected_stores, ', ');
      SELECT AI_COMPLETE(
               model => :judge_model,
               prompt => 'Question: ' || :v_question || '\nCorrect answer: exactly these stores: ' || :expected
                 || '\nAgent answer: ' || COALESCE(:answer, '')
                 || '\nDoes the agent answer name exactly the correct stores as the ones that missed, and no others?',
               model_parameters => {'temperature': 0},
               response_format => {'type': 'json', 'schema': {'type': 'object',
                 'properties': {'correct': {'type': 'boolean'}, 'reason': {'type': 'string'}},
                 'required': ['correct', 'reason']}})
        INTO :judge;
      passed := judge:correct::BOOLEAN;
    END IF;

    INSERT INTO COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES.RETAIL.AGENT_TEST_RESULTS
      (RUN_LABEL, QUESTION_ID, QUESTION, ANSWER_TEXT, AGENT_SQL, EXPECTED, PASSED, RESPONSE)
      SELECT :run_label, :v_qid, :v_question, :answer, :agent_sql, :expected, COALESCE(:passed, FALSE), :resp;
    n_total := n_total + 1;
    n_pass := n_pass + IFF(COALESCE(passed, FALSE), 1, 0);
  END FOR;
  RETURN run_label || ': ' || n_pass || ' of ' || n_total || ' answers correct';
END;
$$;
```

### `sql/04_test_before.sql`

Copy code

```
-- =============================================================================
-- Mixed-grain semantic views: test the agent against the "before" view
-- Takes a few minutes: one agent call per question.
-- =============================================================================

SET DB        = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES';
SET WH        = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_WH';
SET ROLE_NAME = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_ROLE';
SET MODEL     = 'claude-sonnet-4-6';     -- judge model for the "which stores" question

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA RETAIL;

CALL RUN_AGENT_TESTS('before', $MODEL);

SELECT QUESTION_ID, PASSED, EXPECTED, ANSWER_TEXT
FROM AGENT_TEST_RESULTS
WHERE RUN_LABEL = 'before'
ORDER BY QUESTION_ID;
```

### `sql/05_diagnose.sql`

Copy code

```
-- =============================================================================
-- Mixed-grain semantic views: diagnose the wrong answers
-- Three checks, from symptom to cause.
-- =============================================================================

SET DB        = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES';
SET WH        = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_WH';
SET ROLE_NAME = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_ROLE';

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA RETAIL;

-- 1. Symptom: how far off was each answer? A ratio near 2.0 on a SUM is the
--    signature of two grains being added together.
SELECT r.QUESTION_ID, r.EXPECTED,
       MAX(TRY_TO_NUMBER(REPLACE(n.value::VARCHAR, ',', ''), 18, 2)) AS LARGEST_NUMBER_IN_ANSWER,
       ROUND(LARGEST_NUMBER_IN_ANSWER / NULLIF(TRY_TO_NUMBER(r.EXPECTED, 18, 2), 0), 2) AS RATIO_TO_EXPECTED
FROM AGENT_TEST_RESULTS r,
     LATERAL FLATTEN(input => REGEXP_SUBSTR_ALL(r.ANSWER_TEXT, '[0-9][0-9,]*[.][0-9]+')) n
WHERE r.RUN_LABEL = 'before' AND TRY_TO_NUMBER(r.EXPECTED, 18, 2) IS NOT NULL
GROUP BY r.QUESTION_ID, r.EXPECTED
ORDER BY r.QUESTION_ID;

-- 2. The SQL the agent ran. Note the date filter with no grain filter.
SELECT QUESTION_ID, AGENT_SQL
FROM AGENT_TEST_RESULTS
WHERE RUN_LABEL = 'before'
ORDER BY QUESTION_ID;

-- 3. Cause: the table holds two grains that the semantic view never mentions.
SELECT IFF(PERIOD_START = PERIOD_END, 'DAILY', 'MONTHLY') AS IMPLICIT_GRAIN,
       COUNT(*) AS ROWS_, SUM(NET_SALES) AS NET_SALES, COUNT(SALES_TARGET) AS ROWS_WITH_TARGET
FROM STORE_SALES_SUMMARY
GROUP BY 1
ORDER BY 1;
-- Both grains sum to the same total, so any SUM over a date range that includes
-- both counts every sale twice, and SALES_TARGET exists only on MONTHLY rows.
```

### `sql/06_fix_semantic_view.sql`

Copy code

```
-- =============================================================================
-- Mixed-grain semantic views: the fix
-- Same view name, applied with CREATE OR ALTER so grants on the view are kept.
-- Three changes:
--   1. A GRAIN dimension that names the two row types, marked IS_ENUM.
--   2. Grain rules in AI_SQL_GENERATION: filter to exactly one GRAIN.
--   3. Verified queries for the question shapes that broke. They use different
--      stores and months from the test questions on purpose, so the re-test
--      measures whether the rules generalize, not whether a stored query matched.
-- Syntax for these clauses is covered by the coco-skills semantic-view-patterns
-- ai_metadata snippet; this file only shows how to apply them to a grain problem.
-- =============================================================================

SET DB        = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES';
SET WH        = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_WH';
SET ROLE_NAME = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_ROLE';

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA RETAIL;

CREATE OR ALTER SEMANTIC VIEW STORE_SALES_SV
  TABLES (
    sales AS STORE_SALES_SUMMARY
      PRIMARY KEY (STORE_ID, PERIOD_START, PERIOD_END)
      COMMENT = 'Northwind Outfitters store sales. Holds two grains as sibling rows: one row per store per day (DAILY) and one roll-up row per store per month (MONTHLY). Always filter to one GRAIN; summing both counts every sale twice.'
  )
  FACTS (
    sales.net_sales AS NET_SALES
      COMMENT = 'Net sales in USD for the row''s period: one day on DAILY rows, one month on MONTHLY rows.',
    sales.order_count AS ORDER_COUNT
      COMMENT = 'Orders in the row''s period.',
    sales.sales_target AS SALES_TARGET
      COMMENT = 'Monthly sales target in USD. Present on MONTHLY rows only; NULL on DAILY rows.'
  )
  DIMENSIONS (
    sales.store_name AS STORE_NAME
      COMMENT = 'Store name.'
      SAMPLE_VALUES ('Harbor Street', 'Mill Road', 'Canal Park', 'Elm Square')
      IS_ENUM,
    sales.region AS REGION
      COMMENT = 'Store region.'
      SAMPLE_VALUES ('North', 'South')
      IS_ENUM,
    sales.grain AS IFF(PERIOD_START = PERIOD_END, 'DAILY', 'MONTHLY')
      WITH SYNONYMS = ('granularity', 'row level')
      COMMENT = 'Row type. DAILY = one store, one day. MONTHLY = one store, one calendar month, equal to the sum of that month''s DAILY rows, and the only rows with SALES_TARGET. Every query must filter to exactly one GRAIN.'
      SAMPLE_VALUES ('DAILY', 'MONTHLY')
      IS_ENUM,
    sales.period_start AS PERIOD_START
      COMMENT = 'First day of the row''s period: the sales date on DAILY rows, the first of the month on MONTHLY rows.',
    sales.period_end AS PERIOD_END
      COMMENT = 'Last day of the row''s period: equal to PERIOD_START on DAILY rows, the last day of the month on MONTHLY rows.'
  )
  METRICS (
    sales.total_net_sales AS SUM(net_sales)
      COMMENT = 'Total net sales in USD. Valid only within one GRAIN.',
    sales.avg_net_sales AS AVG(net_sales)
      COMMENT = 'Average net sales per row in USD. With GRAIN = DAILY this is average daily sales.',
    sales.total_orders AS SUM(order_count)
      COMMENT = 'Total orders. Valid only within one GRAIN.',
    sales.total_target AS SUM(sales_target)
      COMMENT = 'Total sales target in USD. Use with GRAIN = MONTHLY.'
  )
  COMMENT = 'Store sales for Northwind Outfitters. Mixed-grain table: always filter to one GRAIN.'
  AI_SQL_GENERATION
    'STORE_SALES_SUMMARY stores two grains as sibling rows. GRAIN = DAILY rows cover one day (PERIOD_START = PERIOD_END). GRAIN = MONTHLY rows cover a calendar month and already equal the sum of that month''s DAILY rows. Every query must filter to exactly one grain; never aggregate across both. Choose the grain as follows. Totals for whole calendar months, quarters, or years: use MONTHLY rows and filter on PERIOD_START. Anything about targets or attainment: use MONTHLY rows, because SALES_TARGET exists only there. Daily figures, averages per day, individual dates, or ranges that do not cover whole months: use DAILY rows. Compare net sales with target on the same MONTHLY row rather than summing either across grains.'
  AI_VERIFIED_QUERIES (
    vq_store_month_total AS (
      QUESTION 'What were total net sales for Mill Road in January 2026?'
      VERIFIED_AT 1790000000
      ONBOARDING_QUESTION TRUE
      VERIFIED_BY '(STEWARD = retail_analytics)'
      SQL 'SELECT store_name, period_start AS month, net_sales
             FROM sales
            WHERE grain = ''MONTHLY''
              AND store_name = ''Mill Road''
              AND period_start = ''2026-01-01'''
    ),
    vq_region_quarter_total AS (
      QUESTION 'What were total net sales for the South region in Q1 2026?'
      VERIFIED_AT 1790000000
      ONBOARDING_QUESTION TRUE
      VERIFIED_BY '(STEWARD = retail_analytics)'
      SQL 'SELECT region, SUM(net_sales) AS total_net_sales
             FROM sales
            WHERE grain = ''MONTHLY''
              AND region = ''South''
              AND period_start BETWEEN ''2026-01-01'' AND ''2026-03-01''
            GROUP BY region'
    ),
    vq_stores_vs_target AS (
      QUESTION 'How did each store do against its February 2026 sales target?'
      VERIFIED_AT 1790000000
      ONBOARDING_QUESTION FALSE
      VERIFIED_BY '(STEWARD = retail_analytics)'
      SQL 'SELECT store_name, net_sales, sales_target, net_sales - sales_target AS variance,
                  IFF(net_sales < sales_target, ''missed'', ''met'') AS status
             FROM sales
            WHERE grain = ''MONTHLY''
              AND period_start = ''2026-02-01''
            ORDER BY variance'
    )
  );

-- CREATE OR ALTER kept the SELECT grant from 02:
SHOW GRANTS ON SEMANTIC VIEW STORE_SALES_SV;
```

### `sql/07_test_after.sql`

Copy code

```
-- =============================================================================
-- Mixed-grain semantic views: re-test the unchanged agent against the fixed view
-- =============================================================================

SET DB        = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES';
SET WH        = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_WH';
SET ROLE_NAME = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_ROLE';
SET MODEL     = 'claude-sonnet-4-6';     -- judge model for the "which stores" question

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA RETAIL;

CALL RUN_AGENT_TESTS('after', $MODEL);

-- Before and after, side by side.
SELECT b.QUESTION_ID, b.EXPECTED,
       IFF(b.PASSED, 'PASS', 'FAIL') AS BEFORE_RESULT, b.ANSWER_TEXT AS BEFORE_ANSWER,
       IFF(a.PASSED, 'PASS', 'FAIL') AS AFTER_RESULT,  a.ANSWER_TEXT AS AFTER_ANSWER,
       a.AGENT_SQL AS AFTER_SQL
FROM AGENT_TEST_RESULTS b
JOIN AGENT_TEST_RESULTS a ON a.QUESTION_ID = b.QUESTION_ID AND a.RUN_LABEL = 'after'
WHERE b.RUN_LABEL = 'before'
ORDER BY b.QUESTION_ID;

SELECT RUN_LABEL, COUNT_IF(PASSED) AS CORRECT, COUNT(*) AS QUESTIONS
FROM AGENT_TEST_RESULTS
GROUP BY RUN_LABEL
ORDER BY RUN_LABEL DESC;
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- Mixed-grain semantic views: teardown
-- The agent, semantic view, tables, and procedure go with the database.
-- =============================================================================

SET DB           = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES';
SET WH           = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_WH';
SET ROLE_NAME    = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_ROLE';
SET ANALYST_ROLE = 'COOKBOOK_MIXED_GRAIN_AND_VERIFIED_QUERIES_ANALYST';

USE ROLE ACCOUNTADMIN;

DROP DATABASE IF EXISTS IDENTIFIER($DB);
DROP WAREHOUSE IF EXISTS IDENTIFIER($WH);
DROP ROLE IF EXISTS IDENTIFIER($ANALYST_ROLE);
DROP ROLE IF EXISTS IDENTIFIER($ROLE_NAME);

SHOW DATABASES LIKE 'COOKBOOK_MIXED_GRAIN%';
SHOW WAREHOUSES LIKE 'COOKBOOK_MIXED_GRAIN%';
SHOW ROLES LIKE 'COOKBOOK_MIXED_GRAIN%';
```
