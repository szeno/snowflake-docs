# Evaluate and promote Cortex Agent versions: code

Every file in the [Evaluate and promote Cortex Agent versions](/developer-guide/cortex-ai-cookbook/agent-evaluations) recipe. To run the recipe, download [agent-evaluations.zip](/static/samples/cortex-ai-cookbook/agent-evaluations.zip), unzip it, and run the scripts from the `agent-evaluations/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/agent-evaluations); the zip includes it as `README.md`.

## `config/`

### `config/eval_baseline.yaml`

Copy code

```
# Evaluation config for the baseline run (VERSION$1).
#
# This file contains a dataset block, so START creates CMO_EVAL_DATASET from
# EVAL_QUESTIONS. A dataset with the same name must not already exist, which is
# why 04 drops it first. Later runs (eval_candidate.yaml) omit the dataset block
# and reference the existing dataset instead.
#
# Names are hardcoded to the recipe defaults. If you change the database or
# schema in the SQL SET blocks, change them here too.

dataset:
  dataset_type: "CORTEX AGENT"
  table_name: "COOKBOOK_AGENT_EVALUATIONS.MARKETING.EVAL_QUESTIONS"
  dataset_name: "CMO_EVAL_DATASET"
  column_mapping:
    query_text: "INPUT_QUERY"
    ground_truth: "GROUND_TRUTH"

evaluation:
  agent_params:
    agent_name: "COOKBOOK_AGENT_EVALUATIONS.MARKETING.CMO_ASSISTANT"
    agent_type: "CORTEX AGENT"
    # Pin a committed version so the configuration under test cannot change
    # between runs. VERSION$1 is the baseline created by 02_agent.sql.
    agent_version: "VERSION$1"
  run_params:
    label: "baseline"
    description: "Baseline instructions, no routing or scope rules"
  source_metadata:
    type: "dataset"
    dataset_name: "CMO_EVAL_DATASET"

metrics:
  # System metrics pinned to v3 so scores stay comparable across runs.
  - name: "answer_correctness"
    version: "v3"
  - name: "logical_consistency"
    version: "v3"
  # Custom metric. The model key names the judge explicitly; the default judge
  # for custom metrics is a legacy model that new accounts cannot use.
  - name: "tool_routing"
    model: "claude-sonnet-4-6"
    score_ranges:
      min_score: [1, 3]
      median_score: [4, 6]
      max_score: [7, 10]
    prompt: |
      You are grading whether a marketing assistant used the right tools.

      User question: {{input}}
      Tools the agent called: {{tool_info}}
      Expected behavior: {{ground_truth}}
      Agent answer: {{output}}

      Routing rules the agent should follow:
      - Numbers about spend, revenue, ROAS, CPA, or conversions come from campaign_analytics.
      - Strategy, methodology, benchmarks, and guidelines come from strategy_search.
      - A question that compares actual results to a benchmark or plan needs both tools.
      - A question outside marketing performance needs no tool and a polite refusal.

      Score from 1 to 10:
      1-3: wrong tool, a required tool missing, or a tool called for an out-of-scope question.
      4-6: the main tool was right but a second required tool was missing, or calls were redundant.
      7-10: exactly the tools the question needs.

      Reply with the integer score and a one-sentence reason.
```

### `config/eval_candidate.yaml`

Copy code

```
# Evaluation config for the candidate run (the version 06 commits).
#
# No dataset block: the dataset was created by the baseline run, and repeating
# the block would fail because CMO_EVAL_DATASET already exists. The metrics
# block is identical to eval_baseline.yaml so the two runs are comparable.
#
# agent_version is the CANDIDATE alias, which 06 points at the version it just
# committed (VERSION$2 on a fresh run). An alias resolves to one version when
# the run starts; the run records that version.

evaluation:
  agent_params:
    agent_name: "COOKBOOK_AGENT_EVALUATIONS.MARKETING.CMO_ASSISTANT"
    agent_type: "CORTEX AGENT"
    agent_version: "CANDIDATE"
  run_params:
    label: "candidate"
    description: "Routing rules, a comparison rule, and a scope rule"
  source_metadata:
    type: "dataset"
    dataset_name: "CMO_EVAL_DATASET"

metrics:
  - name: "answer_correctness"
    version: "v3"
  - name: "logical_consistency"
    version: "v3"
  - name: "tool_routing"
    model: "claude-sonnet-4-6"
    score_ranges:
      min_score: [1, 3]
      median_score: [4, 6]
      max_score: [7, 10]
    prompt: |
      You are grading whether a marketing assistant used the right tools.

      User question: {{input}}
      Tools the agent called: {{tool_info}}
      Expected behavior: {{ground_truth}}
      Agent answer: {{output}}

      Routing rules the agent should follow:
      - Numbers about spend, revenue, ROAS, CPA, or conversions come from campaign_analytics.
      - Strategy, methodology, benchmarks, and guidelines come from strategy_search.
      - A question that compares actual results to a benchmark or plan needs both tools.
      - A question outside marketing performance needs no tool and a polite refusal.

      Score from 1 to 10:
      1-3: wrong tool, a required tool missing, or a tool called for an out-of-scope question.
      4-6: the main tool was right but a second required tool was missing, or calls were redundant.
      7-10: exactly the tools the question needs.

      Reply with the integer score and a one-sentence reason.
```

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- =============================================================================
-- 01_setup.sql
-- Agent evaluations: role, warehouse, database, sample data, semantic view, and
-- Cortex Search service for a small marketing-analytics agent.
--
-- The first block runs as ACCOUNTADMIN and only creates or grants to this
-- recipe's own COOKBOOK_ objects. It grants EXECUTE TASK ON ACCOUNT to the
-- recipe role because evaluation runs are managed by tasks; the grant goes away
-- when 99_teardown.sql drops the role.
--
-- Idempotent.
-- =============================================================================

SET agenteval_db   = 'COOKBOOK_AGENT_EVALUATIONS';
SET agenteval_wh   = 'COOKBOOK_AGENT_EVALUATIONS_WH';
SET agenteval_role = 'COOKBOOK_AGENT_EVALUATIONS_ADMIN';
SET agenteval_user = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($agenteval_role)
  COMMENT = 'Cookbook agent-evaluations: owns the recipe objects and runs evaluations.';
-- Granting the role to SYSADMIN lets ACCOUNTADMIN, which inherits SYSADMIN,
-- drop what the role owns in 99_teardown.sql without relying on secondary roles.
GRANT ROLE IDENTIFIER($agenteval_role) TO ROLE SYSADMIN;
GRANT ROLE IDENTIFIER($agenteval_role) TO USER IDENTIFIER($agenteval_user);

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($agenteval_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cookbook agent-evaluations';
GRANT USAGE ON WAREHOUSE IDENTIFIER($agenteval_wh) TO ROLE IDENTIFIER($agenteval_role);

CREATE DATABASE IF NOT EXISTS IDENTIFIER($agenteval_db)
  COMMENT = 'Cookbook agent-evaluations';
GRANT OWNERSHIP ON DATABASE IDENTIFIER($agenteval_db) TO ROLE IDENTIFIER($agenteval_role) COPY CURRENT GRANTS;

-- Privileges the evaluation role needs (see "Access control requirements" in
-- the Cortex Agent evaluations docs). Owning the database covers USAGE and the
-- CREATE TABLE / DATASET / FILE FORMAT / STAGE / TASK privileges on the schema.
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($agenteval_role);
GRANT EXECUTE TASK ON ACCOUNT TO ROLE IDENTIFIER($agenteval_role);
-- Judges also need USE AI FUNCTIONS, which PUBLIC has by default. If your
-- account revoked it from PUBLIC, grant it to the recipe role as well.

-- ---------------------------------------------------------------------------
-- From here on, run as the recipe role.
-- ---------------------------------------------------------------------------
USE ROLE IDENTIFIER($agenteval_role);
USE WAREHOUSE IDENTIFIER($agenteval_wh);
USE DATABASE IDENTIFIER($agenteval_db);
CREATE SCHEMA IF NOT EXISTS MARKETING;
USE SCHEMA MARKETING;

-- Structured data for the Cortex Analyst tool: 4 channels x 12 months of 2024.
CREATE OR REPLACE TABLE CAMPAIGN_SPEND (
  CHANNEL        VARCHAR,
  MONTH          DATE,
  CAMPAIGN_NAME  VARCHAR,
  SPEND          NUMBER(12,2),
  IMPRESSIONS    NUMBER,
  CLICKS         NUMBER,
  CONVERSIONS    NUMBER,
  REVENUE        NUMBER(12,2)
);

INSERT INTO CAMPAIGN_SPEND VALUES
('Paid Search','2024-01-01','Q1 Brand Awareness',45000.00,520000,15600,780,156000.00),
('Paid Search','2024-02-01','Q1 Brand Awareness',48000.00,545000,16350,818,163500.00),
('Paid Search','2024-03-01','Q1 Brand Awareness',52000.00,580000,17400,870,174000.00),
('Paid Search','2024-04-01','Q2 Product Launch',62000.00,650000,19500,975,214500.00),
('Paid Search','2024-05-01','Q2 Product Launch',58000.00,610000,18300,915,201300.00),
('Paid Search','2024-06-01','Q2 Product Launch',55000.00,590000,17700,885,185850.00),
('Paid Search','2024-07-01','H2 Performance Max',50000.00,560000,16800,840,176400.00),
('Paid Search','2024-08-01','H2 Performance Max',53000.00,575000,17250,863,181125.00),
('Paid Search','2024-09-01','H2 Performance Max',56000.00,600000,18000,900,189000.00),
('Paid Search','2024-10-01','Q4 Holiday Push',72000.00,780000,23400,1170,280800.00),
('Paid Search','2024-11-01','Q4 Holiday Push',85000.00,920000,27600,1380,345000.00),
('Paid Search','2024-12-01','Q4 Holiday Push',90000.00,980000,29400,1470,367500.00),
('Social Media','2024-01-01','Q1 Brand Awareness',32000.00,890000,8900,356,62300.00),
('Social Media','2024-02-01','Q1 Brand Awareness',34000.00,920000,9200,368,64400.00),
('Social Media','2024-03-01','Q1 Brand Awareness',36000.00,960000,9600,384,67200.00),
('Social Media','2024-04-01','Q2 Influencer Program',42000.00,1100000,11000,440,88000.00),
('Social Media','2024-05-01','Q2 Influencer Program',44000.00,1150000,11500,460,92000.00),
('Social Media','2024-06-01','Q2 Influencer Program',40000.00,1050000,10500,420,84000.00),
('Social Media','2024-07-01','H2 Community Growth',38000.00,1000000,10000,400,76000.00),
('Social Media','2024-08-01','H2 Community Growth',39000.00,1020000,10200,408,77520.00),
('Social Media','2024-09-01','H2 Community Growth',41000.00,1080000,10800,432,82080.00),
('Social Media','2024-10-01','Q4 Holiday Push',55000.00,1400000,14000,560,112000.00),
('Social Media','2024-11-01','Q4 Holiday Push',62000.00,1580000,15800,632,126400.00),
('Social Media','2024-12-01','Q4 Holiday Push',58000.00,1500000,15000,600,120000.00),
('Email','2024-01-01','Q1 Brand Awareness',8000.00,180000,14400,1008,90720.00),
('Email','2024-02-01','Q1 Brand Awareness',8500.00,190000,15200,1064,95760.00),
('Email','2024-03-01','Q1 Brand Awareness',9000.00,200000,16000,1120,100800.00),
('Email','2024-04-01','Q2 Nurture Sequences',10000.00,220000,17600,1232,123200.00),
('Email','2024-05-01','Q2 Nurture Sequences',10500.00,230000,18400,1288,128800.00),
('Email','2024-06-01','Q2 Nurture Sequences',11000.00,240000,19200,1344,134400.00),
('Email','2024-07-01','H2 Retention Series',9500.00,210000,16800,1176,105840.00),
('Email','2024-08-01','H2 Retention Series',9800.00,215000,17200,1204,108360.00),
('Email','2024-09-01','H2 Retention Series',10200.00,225000,18000,1260,113400.00),
('Email','2024-10-01','Q4 Holiday Push',14000.00,310000,24800,1736,173600.00),
('Email','2024-11-01','Q4 Holiday Push',16000.00,350000,28000,1960,196000.00),
('Email','2024-12-01','Q4 Holiday Push',15000.00,330000,26400,1848,184800.00),
('Display','2024-01-01','Q1 Brand Awareness',22000.00,1200000,6000,180,27000.00),
('Display','2024-02-01','Q1 Brand Awareness',23000.00,1250000,6250,188,28125.00),
('Display','2024-03-01','Q1 Brand Awareness',24000.00,1300000,6500,195,29250.00),
('Display','2024-04-01','Q2 Retargeting',28000.00,1500000,7500,225,38250.00),
('Display','2024-05-01','Q2 Retargeting',30000.00,1600000,8000,240,40800.00),
('Display','2024-06-01','Q2 Retargeting',27000.00,1450000,7250,218,37005.00),
('Display','2024-07-01','H2 Programmatic',25000.00,1350000,6750,203,32437.50),
('Display','2024-08-01','H2 Programmatic',26000.00,1400000,7000,210,33600.00),
('Display','2024-09-01','H2 Programmatic',27000.00,1450000,7250,218,34875.00),
('Display','2024-10-01','Q4 Holiday Push',35000.00,1850000,9250,278,47175.00),
('Display','2024-11-01','Q4 Holiday Push',40000.00,2100000,10500,315,53550.00),
('Display','2024-12-01','Q4 Holiday Push',38000.00,2000000,10000,300,51000.00);

-- Unstructured strategy documents for the Cortex Search tool.
CREATE OR REPLACE TABLE STRATEGY_DOCS (
  DOC_ID    VARCHAR,
  TITLE     VARCHAR,
  CONTENT   VARCHAR,
  DOC_TYPE  VARCHAR
);

INSERT INTO STRATEGY_DOCS VALUES
('DOC-001', 'Channel Strategy 2024',
 'The 2024 channel strategy allocates budget across four channels. Paid Search receives 40 percent of total budget, Social Media 25 percent, Display 15 percent, and Email 10 percent. The remaining 10 percent is a flex budget for tests.',
 'strategy'),
('DOC-002', 'Attribution Methodology',
 'We use a data-driven multi-touch attribution model with a 30-day lookback window. First touch receives a weight of 0.2, last touch 0.3, and middle touches share the remaining 0.5 in proportion to recency. Attribution data refreshes daily with a 48-hour lag.',
 'methodology'),
('DOC-003', 'Performance Benchmarks 2024',
 'Internal 2024 benchmarks by channel. Paid Search: target ROAS 3.0x. Social Media: target ROAS 1.8x. Email: target ROAS 10.0x. Display: target ROAS 1.2x. Channels that beat their benchmark by 20 percent or more are flagged for more investment.',
 'benchmark'),
('DOC-004', 'Reporting Guidelines',
 'Report currency in USD rounded to 2 decimal places. Express ROAS and ROI as multipliers, for example 3.2x. Always state the time period.',
 'guidelines');

-- Semantic view for the Cortex Analyst tool. CREATE OR ALTER keeps grants.
CREATE OR ALTER SEMANTIC VIEW CAMPAIGN_ANALYTICS
  TABLES (
    spend AS COOKBOOK_AGENT_EVALUATIONS.MARKETING.CAMPAIGN_SPEND
      COMMENT = 'Monthly marketing spend and results by channel and campaign for 2024'
  )
  DIMENSIONS (
    spend.channel AS CHANNEL
      COMMENT = 'Marketing channel: Paid Search, Social Media, Email, or Display',
    spend.month AS MONTH
      COMMENT = 'First day of the reporting month',
    spend.campaign_name AS CAMPAIGN_NAME
      COMMENT = 'Campaign name, for example Q4 Holiday Push'
  )
  METRICS (
    spend.total_spend AS SUM(SPEND)
      COMMENT = 'Total marketing spend in USD',
    spend.total_revenue AS SUM(REVENUE)
      COMMENT = 'Total attributed revenue in USD',
    spend.total_clicks AS SUM(CLICKS)
      COMMENT = 'Total ad clicks',
    spend.total_conversions AS SUM(CONVERSIONS)
      COMMENT = 'Total conversions',
    spend.roas AS SUM(REVENUE) / NULLIF(SUM(SPEND), 0)
      COMMENT = 'Return on ad spend: revenue divided by spend, as a multiplier',
    spend.cpa AS SUM(SPEND) / NULLIF(SUM(CONVERSIONS), 0)
      COMMENT = 'Cost per acquisition in USD: spend divided by conversions'
  )
  COMMENT = 'Campaign performance analytics for the CMO assistant'
  AI_SQL_GENERATION 'Round currency to 2 decimal places. Express ROAS as a multiplier such as 3.2x.';

-- Replaced together with its base table so reruns index the fresh rows.
-- Nothing is granted on the service, so replacing it loses no grants.
CREATE OR REPLACE CORTEX SEARCH SERVICE STRATEGY_SEARCH
  ON CONTENT
  ATTRIBUTES DOC_TYPE
  WAREHOUSE = COOKBOOK_AGENT_EVALUATIONS_WH
  TARGET_LAG = '1 day'
  AS (SELECT DOC_ID, TITLE, CONTENT, DOC_TYPE FROM STRATEGY_DOCS);

SHOW CORTEX SEARCH SERVICES IN SCHEMA MARKETING;
```

### `sql/02_agent.sql`

Copy code

```
-- =============================================================================
-- 02_agent.sql
-- The agent under evaluation: a CMO assistant with a Cortex Analyst tool over
-- CAMPAIGN_ANALYTICS and a Cortex Search tool over STRATEGY_SEARCH.
--
-- The baseline instructions are deliberately thin (no routing rules, no scope
-- rule) so that 06 has something to improve.
--
-- CREATE AGENT produces a committed VERSION$1 and a LIVE copy. VERSION$1 is
-- the baseline that 04 evaluates. DEFAULT is pinned to VERSION$1 so that
-- committing the candidate in 06 does not change what unversioned callers get.
--
-- The orchestration model is named explicitly instead of auto. The evaluation
-- docs recommend this so a model change is never mistaken for agent variance.
--
-- Idempotent: CREATE AGENT IF NOT EXISTS never replaces the agent, so reruns
-- keep its versions and evaluation history.
-- =============================================================================

SET agenteval_role  = 'COOKBOOK_AGENT_EVALUATIONS_ADMIN';
SET agenteval_wh    = 'COOKBOOK_AGENT_EVALUATIONS_WH';
SET agenteval_agent = 'COOKBOOK_AGENT_EVALUATIONS.MARKETING.CMO_ASSISTANT';

USE ROLE IDENTIFIER($agenteval_role);
USE WAREHOUSE IDENTIFIER($agenteval_wh);
USE SCHEMA COOKBOOK_AGENT_EVALUATIONS.MARKETING;

CREATE AGENT IF NOT EXISTS CMO_ASSISTANT
  COMMENT = 'Cookbook: CMO assistant used to demonstrate evaluations'
  FROM SPECIFICATION
$$
models:
  orchestration: claude-sonnet-4-6
instructions:
  response: |
    You help marketing leaders understand campaign performance.
    Be concise.
tools:
  - tool_spec:
      type: cortex_analyst_text_to_sql
      name: campaign_analytics
      description: >
        Campaign performance data for 2024: spend, revenue, clicks, conversions,
        ROAS, and CPA by channel, campaign, and month.
  - tool_spec:
      type: cortex_search
      name: strategy_search
      description: >
        Marketing strategy documents: channel strategy, attribution methodology,
        performance benchmarks, and reporting guidelines.
tool_resources:
  campaign_analytics:
    semantic_view: COOKBOOK_AGENT_EVALUATIONS.MARKETING.CAMPAIGN_ANALYTICS
    execution_environment:
      type: warehouse
      warehouse: COOKBOOK_AGENT_EVALUATIONS_WH
  strategy_search:
    search_service: COOKBOOK_AGENT_EVALUATIONS.MARKETING.STRATEGY_SEARCH
    max_results: 3
$$;

ALTER AGENT IDENTIFIER($agenteval_agent) SET DEFAULT_VERSION = 'VERSION$1';

SHOW VERSIONS IN AGENT IDENTIFIER($agenteval_agent);

-- Smoke test: the baseline answers a data question.
SELECT TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'COOKBOOK_AGENT_EVALUATIONS.MARKETING.CMO_ASSISTANT!VERSION$1',
  $${"messages":[{"role":"user","content":[{"type":"text","text":"What was total marketing spend in Q4 2024?"}]}]}$$
)):content AS response_content;
```

### `sql/03_eval_dataset.sql`

Copy code

```
-- =============================================================================
-- 03_eval_dataset.sql
-- Evaluation inputs, the stage that holds the evaluation config, and the
-- upload of both config files.
--
-- Run from the recipe folder (the directory that contains config/) with a
-- client that supports PUT, for example:
--   snow sql -f sql/03_eval_dataset.sql
--
-- Dataset format: one VARCHAR column with the question and one VARIANT column
-- with the ground truth. answer_correctness reads ground_truth_output. Custom
-- metrics see the whole VARIANT through {{ground_truth}}, so expected_tools is
-- there for the tool_routing judge.
--
-- Idempotent.
-- =============================================================================

SET agenteval_role = 'COOKBOOK_AGENT_EVALUATIONS_ADMIN';
SET agenteval_wh   = 'COOKBOOK_AGENT_EVALUATIONS_WH';

USE ROLE IDENTIFIER($agenteval_role);
USE WAREHOUSE IDENTIFIER($agenteval_wh);
USE SCHEMA COOKBOOK_AGENT_EVALUATIONS.MARKETING;

CREATE OR REPLACE TABLE EVAL_QUESTIONS (
  INPUT_QUERY  VARCHAR,
  GROUND_TRUTH VARIANT
);

-- Ground truth values come from CAMPAIGN_SPEND and STRATEGY_DOCS in 01.
-- Questions are scoped to absolute dates so answers do not drift.
INSERT INTO EVAL_QUESTIONS
SELECT column1, PARSE_JSON(column2) FROM VALUES
(
  'What was total marketing spend across all channels in Q4 2024?',
  '{"ground_truth_output": "Total spend across all four channels for October to December 2024 was $580,000.00. The answer must be scoped to Q4 2024. Values within 1 percent are acceptable.",
    "expected_tools": ["campaign_analytics"], "intent": "metric"}'
),
(
  'Which channel had the highest ROAS in Q4 2024?',
  '{"ground_truth_output": "Email had the highest ROAS in Q4 2024, about 12.3x ($554,400 revenue on $45,000 spend). Paid Search was second at about 4.0x. The answer must name Email.",
    "expected_tools": ["campaign_analytics"], "intent": "comparison"}'
),
(
  'What attribution methodology do we use?',
  '{"ground_truth_output": "A data-driven multi-touch attribution model with a 30-day lookback window. First touch weight 0.2, last touch 0.3, middle touches share 0.5 by recency. Data refreshes daily with a 48-hour lag. The answer must not invent details that are not in the strategy documents.",
    "expected_tools": ["strategy_search"], "intent": "document"}'
),
(
  'Did Email beat its ROAS benchmark for full-year 2024?',
  '{"ground_truth_output": "Yes. Email ROAS for 2024 was about 11.8x ($1,555,680 revenue on $131,500 spend) against a benchmark of 10.0x, about 18 percent above target. That is below the 20 percent threshold that flags a channel for more investment. The answer needs the actual ROAS and the benchmark.",
    "expected_tools": ["campaign_analytics", "strategy_search"], "intent": "actual_vs_benchmark"}'
),
(
  'What will the weather be in Chicago tomorrow?',
  '{"ground_truth_output": "The assistant should say that weather is outside what it can help with and offer marketing performance or strategy help instead. It must not give a forecast.",
    "expected_tools": [], "intent": "out_of_scope"}'
);

SELECT INPUT_QUERY, GROUND_TRUTH:intent::STRING AS INTENT FROM EVAL_QUESTIONS;

-- EXECUTE_AI_EVALUATION reads its config from a stage whose file format is CSV
-- with FIELD_DELIMITER = NONE. IF NOT EXISTS keeps the stage's reference to
-- the format intact on reruns.
CREATE FILE FORMAT IF NOT EXISTS EVAL_YAML_FORMAT
  TYPE = 'CSV'
  FIELD_DELIMITER = NONE
  RECORD_DELIMITER = '\n'
  SKIP_HEADER = 0
  FIELD_OPTIONALLY_ENCLOSED_BY = NONE
  ESCAPE_UNENCLOSED_FIELD = NONE;

CREATE STAGE IF NOT EXISTS EVAL_CONFIG
  FILE_FORMAT = EVAL_YAML_FORMAT
  COMMENT = 'Agent evaluation config files';

-- Upload the configs uncompressed. Paths are relative to the recipe folder.
PUT file://config/eval_baseline.yaml  @EVAL_CONFIG AUTO_COMPRESS = FALSE OVERWRITE = TRUE;
PUT file://config/eval_candidate.yaml @EVAL_CONFIG AUTO_COMPRESS = FALSE OVERWRITE = TRUE;

LIST @EVAL_CONFIG;
```

### `sql/04_run_baseline.sql`

Copy code

```
-- =============================================================================
-- 04_run_baseline.sql
-- Start the baseline evaluation run and poll its status.
--
-- EXECUTE_AI_EVALUATION always takes three arguments:
--   1. 'START' | 'STATUS' | 'CANCEL' | 'DELETE'
--   2. OBJECT_CONSTRUCT('run_name', '<name>')
--   3. '@<stage>/<config>.yaml'  (a stage path, not a signed URL)
--
-- With SQL, the evaluation runs in the session's current database and schema,
-- so USE SCHEMA before calling it.
--
-- Rerunnable: the block deletes an earlier run with the same name and drops the
-- dataset, because eval_baseline.yaml creates the dataset on START.
-- =============================================================================

SET agenteval_role = 'COOKBOOK_AGENT_EVALUATIONS_ADMIN';
SET agenteval_wh   = 'COOKBOOK_AGENT_EVALUATIONS_WH';

USE ROLE IDENTIFIER($agenteval_role);
USE WAREHOUSE IDENTIFIER($agenteval_wh);
USE SCHEMA COOKBOOK_AGENT_EVALUATIONS.MARKETING;

-- Clean slate for a rerun. DELETE fails if the run does not exist, so ignore
-- that error.
EXECUTE IMMEDIATE $$
BEGIN
  CALL EXECUTE_AI_EVALUATION('DELETE', OBJECT_CONSTRUCT('run_name', 'baseline'),
                             '@EVAL_CONFIG/eval_baseline.yaml');
  RETURN 'Deleted earlier baseline run';
EXCEPTION
  WHEN OTHER THEN RETURN 'No earlier baseline run deleted: ' || SQLERRM;
END;
$$;
DROP DATASET IF EXISTS CMO_EVAL_DATASET;

CALL EXECUTE_AI_EVALUATION(
  'START',
  OBJECT_CONSTRUCT('run_name', 'baseline'),
  '@EVAL_CONFIG/eval_baseline.yaml'
);

-- The first status is usually CREATED. A five-question run finishes in a few
-- minutes. Each snow sql -f call is a new session, so poll with 05, which
-- shows this STATUS and stops until the run is COMPLETED:
--   snow sql -f sql/05_results.sql
CALL EXECUTE_AI_EVALUATION(
  'STATUS',
  OBJECT_CONSTRUCT('run_name', 'baseline'),
  '@EVAL_CONFIG/eval_baseline.yaml'
);
```

### `sql/05_results.sql`

Copy code

```
-- =============================================================================
-- 05_results.sql
-- Read evaluation results with GET_AI_EVALUATION_DATA.
--
-- GET_AI_EVALUATION_DATA(database, schema, agent, 'CORTEX AGENT', run_name)
-- returns one row per input and metric. EVAL_AGG_SCORE is the score.
--   * System metrics (answer_correctness, logical_consistency) score 0 to 1.
--   * A custom metric scores on the scale its prompt defines (1 to 10 for
--     tool_routing here), so do not average it together with system metrics.
-- METRIC_CALLS[0]:explanation holds the judge's reasoning.
--
-- The file first shows STATUS for the run and stops with an error until the
-- run is COMPLETED, so it doubles as the polling command. It reads the
-- baseline run by default; the Snowflake CLI passes the run name in:
--   snow sql -f sql/05_results.sql                        # baseline
--   snow sql -f sql/05_results.sql -D run_name=candidate  # candidate
-- In a client without Snowflake CLI templating (for example a Snowsight
-- worksheet), replace the agenteval_run value with 'baseline' or 'candidate'.
-- =============================================================================

SET agenteval_role = 'COOKBOOK_AGENT_EVALUATIONS_ADMIN';
SET agenteval_wh   = 'COOKBOOK_AGENT_EVALUATIONS_WH';
SET agenteval_run  = '<% run_name | default("baseline") %>';

USE ROLE IDENTIFIER($agenteval_role);
USE WAREHOUSE IDENTIFIER($agenteval_wh);
USE SCHEMA COOKBOOK_AGENT_EVALUATIONS.MARKETING;

-- Allowlist: only the two runs this recipe creates map to a config file.
SET agenteval_config = (SELECT CASE $agenteval_run
                          WHEN 'baseline'  THEN '@EVAL_CONFIG/eval_baseline.yaml'
                          WHEN 'candidate' THEN '@EVAL_CONFIG/eval_candidate.yaml'
                        END);

EXECUTE IMMEDIATE $$
DECLARE
  bad_run EXCEPTION (-20001, 'run_name must be baseline or candidate');
BEGIN
  IF ($agenteval_config IS NULL) THEN
    RAISE bad_run;
  END IF;
  RETURN 'Reading run ' || $agenteval_run;
END;
$$;

-- Status of the run. STATUS moves through states such as
-- INVOCATION_IN_PROGRESS to COMPLETED; a five-question run takes a few minutes.
CALL EXECUTE_AI_EVALUATION('STATUS', OBJECT_CONSTRUCT('run_name', $agenteval_run),
                           $agenteval_config);
SET agenteval_status = (SELECT "STATUS" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())));

-- Stop here unless the run is COMPLETED, so the score queries below never read
-- a partial run.
EXECUTE IMMEDIATE $$
DECLARE
  in_progress EXCEPTION (-20002, 'The run is still in progress. Run this file again in a minute.');
  partial     EXCEPTION (-20003, 'The run is PARTIALLY_COMPLETED. It can still move to COMPLETED, so run this file again in a minute or two; if it stays PARTIALLY_COMPLETED, see STATUS_DETAILS above.');
  cancelled   EXCEPTION (-20004, 'The run was cancelled. Run 04 (or 06) again to start a new one.');
BEGIN
  IF ($agenteval_status = 'COMPLETED') THEN
    RETURN $agenteval_run || ' is COMPLETED';
  END IF;
  IF ($agenteval_status = 'PARTIALLY_COMPLETED') THEN
    RAISE partial;
  END IF;
  IF ($agenteval_status = 'CANCELLED') THEN
    RAISE cancelled;
  END IF;
  RAISE in_progress;
END;
$$;

-- Average per metric.
SELECT METRIC_NAME, METRIC_TYPE, COUNT(*) AS N,
       ROUND(AVG(EVAL_AGG_SCORE), 3) AS AVG_SCORE,
       MIN(EVAL_AGG_SCORE) AS MIN_SCORE
FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
  'COOKBOOK_AGENT_EVALUATIONS', 'MARKETING', 'CMO_ASSISTANT', 'CORTEX AGENT', $agenteval_run))
GROUP BY METRIC_NAME, METRIC_TYPE
ORDER BY METRIC_NAME;

-- Lowest scores first, with the judge's explanation.
SELECT INPUT, METRIC_NAME, EVAL_AGG_SCORE,
       METRIC_CALLS[0]:explanation::STRING AS EXPLANATION
FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
  'COOKBOOK_AGENT_EVALUATIONS', 'MARKETING', 'CMO_ASSISTANT', 'CORTEX AGENT', $agenteval_run))
ORDER BY METRIC_TYPE, EVAL_AGG_SCORE
LIMIT 10;

-- Scores by intent, joined back to the dataset table on the question text.
SELECT q.GROUND_TRUTH:intent::STRING AS INTENT,
       ROUND(AVG(IFF(r.METRIC_NAME = 'answer_correctness', r.EVAL_AGG_SCORE, NULL)), 3) AS ANSWER_CORRECTNESS,
       ROUND(AVG(IFF(r.METRIC_NAME = 'logical_consistency', r.EVAL_AGG_SCORE, NULL)), 3) AS LOGICAL_CONSISTENCY,
       ROUND(AVG(IFF(r.METRIC_NAME = 'tool_routing', r.EVAL_AGG_SCORE, NULL)), 1) AS TOOL_ROUTING_1_TO_10
FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
  'COOKBOOK_AGENT_EVALUATIONS', 'MARKETING', 'CMO_ASSISTANT', 'CORTEX AGENT', $agenteval_run)) r
JOIN EVAL_QUESTIONS q ON q.INPUT_QUERY = r.INPUT
GROUP BY INTENT
ORDER BY INTENT;

-- Errors and warnings for the run, if any metric is missing.
SELECT TIMESTAMP, RECORD:"severity_text"::STRING AS SEVERITY, VALUE::STRING AS MESSAGE
FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_LOGS(
  'COOKBOOK_AGENT_EVALUATIONS', 'MARKETING', 'CMO_ASSISTANT', 'CORTEX AGENT'))
WHERE RECORD:"severity_text" IN ('ERROR', 'WARN')
  AND RECORD_ATTRIBUTES:"snow.ai.observability.run.name" = $agenteval_run
ORDER BY TIMESTAMP DESC
LIMIT 20;
```

### `sql/06_candidate.sql`

Copy code

```
-- =============================================================================
-- 06_candidate.sql
-- Improve the agent based on the baseline results, commit the change as a new
-- named version, point the CANDIDATE alias at it, and evaluate it with the
-- same dataset and metrics.
--
-- One change at a time: this version only adds orchestration rules (routing,
-- a comparison rule, and a scope rule). The model and tools are unchanged, so
-- a score difference comes from the instructions.
--
-- MODIFY LIVE VERSION SET SPECIFICATION replaces the whole spec, so the tools
-- and tool_resources are repeated in full.
--
-- Rerunnable: each run commits one more version and re-points CANDIDATE.
-- =============================================================================

SET agenteval_role  = 'COOKBOOK_AGENT_EVALUATIONS_ADMIN';
SET agenteval_wh    = 'COOKBOOK_AGENT_EVALUATIONS_WH';
SET agenteval_agent = 'COOKBOOK_AGENT_EVALUATIONS.MARKETING.CMO_ASSISTANT';

USE ROLE IDENTIFIER($agenteval_role);
USE WAREHOUSE IDENTIFIER($agenteval_wh);
USE SCHEMA COOKBOOK_AGENT_EVALUATIONS.MARKETING;

-- COMMIT consumes LIVE; add one back if a previous run committed it.
EXECUTE IMMEDIATE $$
BEGIN
  SHOW VERSIONS IN AGENT IDENTIFIER($agenteval_agent);
  LET qid VARCHAR := SQLID;
  LET live_count INTEGER := (SELECT COUNT(*) FROM TABLE(RESULT_SCAN(:qid))
                             WHERE "spec_file_path" ILIKE '%/versions/live/');
  IF (live_count = 0) THEN
    ALTER AGENT IDENTIFIER($agenteval_agent) ADD LIVE VERSION FROM LAST;
    RETURN 'Added a LIVE version from LAST';
  END IF;
  RETURN 'LIVE version already exists';
END;
$$;

ALTER AGENT IDENTIFIER($agenteval_agent) MODIFY LIVE VERSION SET SPECIFICATION =
$$
models:
  orchestration: claude-sonnet-4-6
instructions:
  response: |
    You help marketing leaders understand campaign performance.
    Be concise. State the time period of every number. Express ROAS as a
    multiplier such as 3.2x and round currency to 2 decimal places.
  orchestration: |
    Tool routing rules:
    1. Questions about spend, revenue, clicks, conversions, ROAS, or CPA: use campaign_analytics.
    2. Questions about strategy, attribution, benchmarks, or reporting guidelines: use strategy_search.
    3. Questions that compare actual results with a benchmark or plan: use campaign_analytics
       for the actual number and strategy_search for the target, then compare them.
    4. Questions outside marketing performance and strategy (weather, news, other companies):
       do not call a tool. Say it is outside what you can help with and offer a marketing
       question you can answer instead.
tools:
  - tool_spec:
      type: cortex_analyst_text_to_sql
      name: campaign_analytics
      description: >
        Campaign performance data for 2024: spend, revenue, clicks, conversions,
        ROAS, and CPA by channel, campaign, and month.
  - tool_spec:
      type: cortex_search
      name: strategy_search
      description: >
        Marketing strategy documents: channel strategy, attribution methodology,
        performance benchmarks, and reporting guidelines.
tool_resources:
  campaign_analytics:
    semantic_view: COOKBOOK_AGENT_EVALUATIONS.MARKETING.CAMPAIGN_ANALYTICS
    execution_environment:
      type: warehouse
      warehouse: COOKBOOK_AGENT_EVALUATIONS_WH
  strategy_search:
    search_service: COOKBOOK_AGENT_EVALUATIONS.MARKETING.STRATEGY_SEARCH
    max_results: 3
$$;

ALTER AGENT IDENTIFIER($agenteval_agent) COMMIT
  COMMENT = 'Candidate: routing, comparison, and scope rules';

-- Point CANDIDATE at the version just committed. MODIFY VERSION needs a system
-- name, so resolve LAST through DESCRIBE AGENT and validate it first.
EXECUTE IMMEDIATE $$
BEGIN
  DESCRIBE AGENT IDENTIFIER($agenteval_agent);
  LET qid VARCHAR := SQLID;
  LET last_version VARCHAR := (SELECT TRY_PARSE_JSON("aliases"):LAST::STRING FROM TABLE(RESULT_SCAN(:qid)));
  IF (NOT REGEXP_LIKE(last_version, '^VERSION\\$[0-9]+$')) THEN
    RETURN 'Unexpected version name: ' || COALESCE(last_version, 'NULL');
  END IF;
  EXECUTE IMMEDIATE 'ALTER AGENT IDENTIFIER($agenteval_agent) MODIFY VERSION '
                    || last_version || ' SET ALIAS = candidate';
  RETURN 'CANDIDATE now points at ' || last_version;
END;
$$;

-- Evaluate the candidate. eval_candidate.yaml has no dataset block and targets
-- the CANDIDATE alias.
EXECUTE IMMEDIATE $$
BEGIN
  CALL EXECUTE_AI_EVALUATION('DELETE', OBJECT_CONSTRUCT('run_name', 'candidate'),
                             '@EVAL_CONFIG/eval_candidate.yaml');
  RETURN 'Deleted earlier candidate run';
EXCEPTION
  WHEN OTHER THEN RETURN 'No earlier candidate run';
END;
$$;

CALL EXECUTE_AI_EVALUATION(
  'START',
  OBJECT_CONSTRUCT('run_name', 'candidate'),
  '@EVAL_CONFIG/eval_candidate.yaml'
);

-- Poll and read the candidate run with 05, which shows this STATUS and stops
-- until the run is COMPLETED:
--   snow sql -f sql/05_results.sql -D run_name=candidate
CALL EXECUTE_AI_EVALUATION(
  'STATUS',
  OBJECT_CONSTRUCT('run_name', 'candidate'),
  '@EVAL_CONFIG/eval_candidate.yaml'
);
```

### `sql/07_compare_and_promote.sql`

Copy code

```
-- =============================================================================
-- 07_compare_and_promote.sql
-- Compare the baseline and candidate runs, and promote the candidate to the
-- PRODUCTION alias only if it passes a gate.
--
-- Gate used here (tune it to your own baselines):
--   * candidate answer_correctness >= baseline answer_correctness, and
--   * candidate answer_correctness >= 0.80, and
--   * candidate logical_consistency >= 0.80.
-- Scores move between runs of the same version because each run re-invokes the
-- agent. Before gating CI on a threshold, run the same dataset several times
-- and gate on the range you observe.
-- =============================================================================

SET agenteval_role  = 'COOKBOOK_AGENT_EVALUATIONS_ADMIN';
SET agenteval_wh    = 'COOKBOOK_AGENT_EVALUATIONS_WH';
SET agenteval_agent = 'COOKBOOK_AGENT_EVALUATIONS.MARKETING.CMO_ASSISTANT';

USE ROLE IDENTIFIER($agenteval_role);
USE WAREHOUSE IDENTIFIER($agenteval_wh);
USE SCHEMA COOKBOOK_AGENT_EVALUATIONS.MARKETING;

-- Side by side, per metric.
WITH scores AS (
  SELECT 'baseline' AS RUN_NAME, METRIC_NAME, EVAL_AGG_SCORE
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
    'COOKBOOK_AGENT_EVALUATIONS', 'MARKETING', 'CMO_ASSISTANT', 'CORTEX AGENT', 'baseline'))
  UNION ALL
  SELECT 'candidate', METRIC_NAME, EVAL_AGG_SCORE
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
    'COOKBOOK_AGENT_EVALUATIONS', 'MARKETING', 'CMO_ASSISTANT', 'CORTEX AGENT', 'candidate'))
)
SELECT METRIC_NAME,
       ROUND(AVG(IFF(RUN_NAME = 'baseline', EVAL_AGG_SCORE, NULL)), 3)  AS BASELINE,
       ROUND(AVG(IFF(RUN_NAME = 'candidate', EVAL_AGG_SCORE, NULL)), 3) AS CANDIDATE,
       ROUND(CANDIDATE - BASELINE, 3) AS DELTA
FROM scores
GROUP BY METRIC_NAME
ORDER BY METRIC_NAME;

-- Per question: where did the score move?
SELECT b.INPUT, b.METRIC_NAME,
       b.EVAL_AGG_SCORE AS BASELINE, c.EVAL_AGG_SCORE AS CANDIDATE,
       c.METRIC_CALLS[0]:explanation::STRING AS CANDIDATE_EXPLANATION
FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
  'COOKBOOK_AGENT_EVALUATIONS', 'MARKETING', 'CMO_ASSISTANT', 'CORTEX AGENT', 'baseline')) b
JOIN TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
  'COOKBOOK_AGENT_EVALUATIONS', 'MARKETING', 'CMO_ASSISTANT', 'CORTEX AGENT', 'candidate')) c
  ON b.INPUT = c.INPUT AND b.METRIC_NAME = c.METRIC_NAME
WHERE b.EVAL_AGG_SCORE <> c.EVAL_AGG_SCORE
ORDER BY b.METRIC_NAME, b.INPUT;

-- Gate, then promote by moving the PRODUCTION alias and the DEFAULT pin to the
-- CANDIDATE version. A version holds one alias, so CANDIDATE is replaced by
-- PRODUCTION on that version.
EXECUTE IMMEDIATE $$
BEGIN
  LET base_ac FLOAT := (SELECT AVG(EVAL_AGG_SCORE) FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
    'COOKBOOK_AGENT_EVALUATIONS', 'MARKETING', 'CMO_ASSISTANT', 'CORTEX AGENT', 'baseline'))
    WHERE METRIC_NAME = 'answer_correctness');
  LET cand_ac FLOAT := (SELECT AVG(EVAL_AGG_SCORE) FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
    'COOKBOOK_AGENT_EVALUATIONS', 'MARKETING', 'CMO_ASSISTANT', 'CORTEX AGENT', 'candidate'))
    WHERE METRIC_NAME = 'answer_correctness');
  LET cand_lc FLOAT := (SELECT AVG(EVAL_AGG_SCORE) FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
    'COOKBOOK_AGENT_EVALUATIONS', 'MARKETING', 'CMO_ASSISTANT', 'CORTEX AGENT', 'candidate'))
    WHERE METRIC_NAME = 'logical_consistency');

  IF (cand_ac IS NULL OR base_ac IS NULL OR cand_lc IS NULL) THEN
    RETURN 'Not promoted: a run has no scores yet. Check STATUS for both runs.';
  END IF;
  IF (NOT (cand_ac >= base_ac AND cand_ac >= 0.80 AND cand_lc >= 0.80)) THEN
    RETURN 'Not promoted: candidate answer_correctness ' || ROUND(cand_ac, 3)
        || ' vs baseline ' || ROUND(base_ac, 3) || ', logical_consistency ' || ROUND(cand_lc, 3);
  END IF;

  DESCRIBE AGENT IDENTIFIER($agenteval_agent);
  LET qid VARCHAR := SQLID;
  LET candidate_version VARCHAR := (SELECT TRY_PARSE_JSON("aliases"):CANDIDATE::STRING FROM TABLE(RESULT_SCAN(:qid)));
  IF (NOT REGEXP_LIKE(candidate_version, '^VERSION\\$[0-9]+$')) THEN
    RETURN 'Not promoted: CANDIDATE alias resolves to ' || COALESCE(candidate_version, 'nothing');
  END IF;
  EXECUTE IMMEDIATE 'ALTER AGENT IDENTIFIER($agenteval_agent) MODIFY VERSION '
                    || candidate_version || ' SET ALIAS = production';
  EXECUTE IMMEDIATE 'ALTER AGENT IDENTIFIER($agenteval_agent) SET DEFAULT_VERSION = '''
                    || candidate_version || '''';
  RETURN 'Promoted ' || candidate_version || ': answer_correctness ' || ROUND(base_ac, 3)
      || ' -> ' || ROUND(cand_ac, 3);
END;
$$;

DESCRIBE AGENT IDENTIFIER($agenteval_agent);
SELECT "default_version_name", "aliases" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));

-- Applications call the alias, never a version number. The out-of-scope
-- question from the dataset shows the promoted behavior.
SELECT TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'COOKBOOK_AGENT_EVALUATIONS.MARKETING.CMO_ASSISTANT!PRODUCTION',
  $${"messages":[{"role":"user","content":[{"type":"text","text":"What will the weather be in Chicago tomorrow?"}]}]}$$
)):content AS production_response;
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- 99_teardown.sql
-- Removes everything this recipe created.
--
-- Evaluation runs are deleted first, while the agent and config still exist.
-- Dropping the database then removes the agent, its versions, the dataset,
-- the stage, and the tables. Dropping the role removes its EXECUTE TASK ON
-- ACCOUNT grant. There are no account parameters to restore.
-- =============================================================================

SET agenteval_db   = 'COOKBOOK_AGENT_EVALUATIONS';
SET agenteval_wh   = 'COOKBOOK_AGENT_EVALUATIONS_WH';
SET agenteval_role = 'COOKBOOK_AGENT_EVALUATIONS_ADMIN';

-- A Snowflake Scripting block needs an active warehouse, and the user running
-- teardown may have no default warehouse. IF NOT EXISTS only recreates the
-- recipe warehouse if an earlier, partial teardown dropped it; it is dropped
-- again below, so a rerun of this file always finishes.
USE ROLE ACCOUNTADMIN;
CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($agenteval_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;
USE WAREHOUSE IDENTIFIER($agenteval_wh);

-- Delete the runs as the recipe role. Ignore errors if a run or the role is
-- already gone.
EXECUTE IMMEDIATE $$
BEGIN
  USE ROLE IDENTIFIER($agenteval_role);
  USE WAREHOUSE IDENTIFIER($agenteval_wh);
  USE SCHEMA COOKBOOK_AGENT_EVALUATIONS.MARKETING;
  BEGIN
    CALL EXECUTE_AI_EVALUATION('DELETE', OBJECT_CONSTRUCT('run_name', 'baseline'),
                               '@EVAL_CONFIG/eval_baseline.yaml');
  EXCEPTION WHEN OTHER THEN NULL;
  END;
  BEGIN
    CALL EXECUTE_AI_EVALUATION('DELETE', OBJECT_CONSTRUCT('run_name', 'candidate'),
                               '@EVAL_CONFIG/eval_candidate.yaml');
  EXCEPTION WHEN OTHER THEN NULL;
  END;
  RETURN 'Evaluation runs deleted';
EXCEPTION
  WHEN OTHER THEN RETURN 'Skipped run deletion: ' || SQLERRM;
END;
$$;

USE ROLE ACCOUNTADMIN;
DROP DATABASE IF EXISTS IDENTIFIER($agenteval_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($agenteval_wh);
DROP ROLE IF EXISTS IDENTIFIER($agenteval_role);

SHOW DATABASES LIKE 'COOKBOOK_AGENT_EVALUATIONS%';
SHOW WAREHOUSES LIKE 'COOKBOOK_AGENT_EVALUATIONS%';
SHOW ROLES LIKE 'COOKBOOK_AGENT_EVALUATIONS%';
```
