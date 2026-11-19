# Make ML predictions human-interpretable with a Cortex Agent: code

Every file in the [Make ML predictions human-interpretable with a Cortex Agent](/developer-guide/cortex-ai-cookbook/explain-model-predictions) recipe. To run the recipe, download [explain-model-predictions.zip](/static/samples/cortex-ai-cookbook/explain-model-predictions.zip), unzip it, and run the scripts from the `explain-model-predictions/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/explain-model-predictions); the zip includes it as `README.md`.

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- =============================================================================
-- 01_setup.sql
-- Explain model predictions: roles, warehouse, database, and schema.
--
-- The first block runs as ACCOUNTADMIN and only creates or grants to this
-- recipe's own COOKBOOK_ objects:
--   COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_ADMIN  owns and builds everything
--   COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_USER   can only talk to the agent
-- Both are granted to the user running this script so the README's Verify
-- step can test the user role. Everything else runs as the admin role.
--
-- Idempotent.
-- =============================================================================

SET explain_db        = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS';
SET explain_wh        = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_WH';
SET explain_role      = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_ADMIN';
SET explain_user_role = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_USER';
SET explain_user      = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($explain_role)
  COMMENT = 'Cookbook explain-model-predictions: owns the data, model, tools, and agent.';
CREATE ROLE IF NOT EXISTS IDENTIFIER($explain_user_role)
  COMMENT = 'Cookbook explain-model-predictions: may use the agent and nothing else.';
-- Granting the roles to SYSADMIN lets ACCOUNTADMIN, which inherits SYSADMIN,
-- drop what they own in 99_teardown.sql without relying on secondary roles.
GRANT ROLE IDENTIFIER($explain_role) TO ROLE SYSADMIN;
GRANT ROLE IDENTIFIER($explain_user_role) TO ROLE SYSADMIN;
GRANT ROLE IDENTIFIER($explain_role) TO USER IDENTIFIER($explain_user);
GRANT ROLE IDENTIFIER($explain_user_role) TO USER IDENTIFIER($explain_user);

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($explain_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cookbook explain-model-predictions';
GRANT USAGE ON WAREHOUSE IDENTIFIER($explain_wh) TO ROLE IDENTIFIER($explain_role);
GRANT USAGE ON WAREHOUSE IDENTIFIER($explain_wh) TO ROLE IDENTIFIER($explain_user_role);

CREATE DATABASE IF NOT EXISTS IDENTIFIER($explain_db)
  COMMENT = 'Cookbook explain-model-predictions';
GRANT OWNERSHIP ON DATABASE IDENTIFIER($explain_db) TO ROLE IDENTIFIER($explain_role) COPY CURRENT GRANTS;

-- Cortex Agents and AI functions. Owning the database covers CREATE TABLE,
-- MODEL, PROCEDURE, and AGENT on its schemas.
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($explain_role);
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($explain_user_role);

-- ---------------------------------------------------------------------------
-- From here on, run as the recipe role.
-- ---------------------------------------------------------------------------
USE ROLE IDENTIFIER($explain_role);
USE WAREHOUSE IDENTIFIER($explain_wh);
USE DATABASE IDENTIFIER($explain_db);
CREATE SCHEMA IF NOT EXISTS CARE_MGMT
  COMMENT = 'Synthetic members, the high-cost claimant model, its tools, and the agent';

SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE();
```

### `sql/02_data.sql`

Copy code

```
-- =============================================================================
-- 02_data.sql
-- 20,000 synthetic health plan members with a HIGH_COST_CLAIMANT label, plus
-- the feature dictionary the tools use to describe and validate features.
--
-- Every value is derived from HASH(member sequence, salt), not RANDOM(), so the
-- data, the model, and the Verify numbers in the README are reproducible.
--
-- The label comes from a known logistic model. Prior-year cost, chronic
-- conditions, ER visits, inpatient admits, open care gaps, and age have direct
-- terms. RX_CLASSES and SPECIALIST_VISITS_12M have none; they rise with chronic
-- conditions, so the model may still lean on them. PORTAL_LOGINS_12M is pure
-- noise: a correct explanation gives it almost no weight.
--
-- Idempotent.
-- =============================================================================

SET explain_db   = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS';
SET explain_wh   = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_WH';
SET explain_role = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_ADMIN';

USE ROLE IDENTIFIER($explain_role);
USE WAREHOUSE IDENTIFIER($explain_wh);
USE DATABASE IDENTIFIER($explain_db);
USE SCHEMA CARE_MGMT;

-- Features are DOUBLE so the model signature, SQL inference, and the what-if
-- tool all use one type.
CREATE OR REPLACE TABLE MEMBER_FEATURES (
  MEMBER_ID              VARCHAR,
  AGE                    DOUBLE,
  PRIOR_YEAR_COST        DOUBLE,
  CHRONIC_CONDITIONS     DOUBLE,
  ER_VISITS_12M          DOUBLE,
  INPATIENT_ADMITS_12M   DOUBLE,
  RX_CLASSES             DOUBLE,
  SPECIALIST_VISITS_12M  DOUBLE,
  OPEN_CARE_GAPS         DOUBLE,
  PORTAL_LOGINS_12M      DOUBLE,
  HIGH_COST_CLAIMANT     NUMBER(1),
  HOLDOUT                BOOLEAN
) COMMENT = 'Synthetic members. HOLDOUT rows are never used for training.';

INSERT INTO MEMBER_FEATURES
WITH u AS (
  SELECT SEQ4() AS n,
    (ABS(HASH(SEQ4(), 1))  % 1000000007) / 1000000007.0::DOUBLE AS u1,
    (ABS(HASH(SEQ4(), 2))  % 1000000007) / 1000000007.0::DOUBLE AS u2,
    (ABS(HASH(SEQ4(), 3))  % 1000000007) / 1000000007.0::DOUBLE AS u3,
    (ABS(HASH(SEQ4(), 4))  % 1000000007) / 1000000007.0::DOUBLE AS u4,
    (ABS(HASH(SEQ4(), 5))  % 1000000007) / 1000000007.0::DOUBLE AS u5,
    (ABS(HASH(SEQ4(), 6))  % 1000000007) / 1000000007.0::DOUBLE AS u6,
    (ABS(HASH(SEQ4(), 7))  % 1000000007) / 1000000007.0::DOUBLE AS u7,
    (ABS(HASH(SEQ4(), 8))  % 1000000007) / 1000000007.0::DOUBLE AS u8,
    (ABS(HASH(SEQ4(), 9))  % 1000000007) / 1000000007.0::DOUBLE AS u9,
    (ABS(HASH(SEQ4(), 10)) % 1000000007) / 1000000007.0::DOUBLE AS u10,
    (ABS(HASH(SEQ4(), 11)) % 1000000007) / 1000000007.0::DOUBLE AS u11,
    (ABS(HASH(SEQ4(), 12)) % 5) = 0 AS holdout
  FROM TABLE(GENERATOR(ROWCOUNT => 20000))
), a AS (
  SELECT *, FLOOR(18 + 67 * u1)::DOUBLE AS age FROM u
), b AS (
  SELECT *, LEAST(6, FLOOR(u2 * (1 + (age - 18) / 67 * 5.5)))::DOUBLE AS chronic FROM a
), c AS (
  SELECT *,
    LEAST(12, FLOOR(-LN(1 - u4) * (0.25 + 0.35 * chronic)))::DOUBLE AS er,
    LEAST(5,  FLOOR(-LN(1 - u5) * (0.08 + 0.18 * chronic)))::DOUBLE AS ip,
    LEAST(15, chronic + FLOOR(u3 * 4))::DOUBLE AS rx,
    FLOOR(u6 * (2 + 2 * chronic))::DOUBLE AS spec,
    FLOOR(u9 * 4)::DOUBLE AS gaps,
    FLOOR(u10 * 25)::DOUBLE AS logins,
    SQRT(-2 * LN(u7 + 1e-12)) * COS(2 * PI() * u8) AS z
  FROM b
), d AS (
  SELECT *, ROUND(LEAST(400000, EXP(7.4 + 0.35 * chronic + 0.45 * ip + 0.12 * er + 0.65 * z)), 2) AS cost
  FROM c
), e AS (
  SELECT *,
    -3.9 + 0.55 * LN(cost / 3000) + 0.38 * chronic + 0.28 * er + 0.85 * ip
         + 0.25 * gaps + 0.015 * (age - 50) AS logit
  FROM d
)
SELECT 'M' || LPAD(n + 1, 6, '0'), age, cost, chronic, er, ip, rx, spec, gaps, logins,
       IFF(u11 < 1 / (1 + EXP(-logit)), 1, 0), holdout
FROM e;

-- One row per model feature: the agent's only source for what a feature means.
--   LABEL, UNIT          how to name the feature and its value
--   DEFINITION           what the feature measures and how it is counted
--   HOW_TO_EXPLAIN       how to talk about it with a care manager, including
--                        what it is a signal of and what not to say
--   POPULATION_MEDIAN    a typical member, for comparison
--   MIN_VALUE, MAX_VALUE allowlist and range check for what-if questions
-- The definitions here describe this synthetic data set. Replace them with your
-- plan's own definitions (claim types, look-back windows, condition lists) when
-- you point the recipe at real features: the agent will repeat them verbatim.
CREATE OR REPLACE TABLE FEATURE_DICTIONARY (
  FEATURE_NAME       VARCHAR,
  LABEL              VARCHAR,
  UNIT               VARCHAR,
  DEFINITION         VARCHAR,
  HOW_TO_EXPLAIN     VARCHAR,
  MIN_VALUE          DOUBLE,
  MAX_VALUE          DOUBLE,
  POPULATION_MEDIAN  DOUBLE
) COMMENT = 'Labels, definitions, explanation guidance, and valid ranges for the model features.';

INSERT INTO FEATURE_DICTIONARY (FEATURE_NAME, LABEL, UNIT, DEFINITION, HOW_TO_EXPLAIN, MIN_VALUE, MAX_VALUE)
VALUES
  ('AGE', 'Age', 'years',
   'The member''s age in whole years on the scoring date.',
   'Older members tend to have more conditions and more care, so age raises scores across the population. Mention it as background, not as something about the member that needs action.',
   18, 100),
  ('PRIOR_YEAR_COST', 'Prior-year allowed cost', 'USD',
   'Total allowed amount for all medical and pharmacy claims in the last 12 months: what the plan and the member together paid after network discounts.',
   'Past spending is usually the strongest single signal of future spending, because high-cost care often continues. It shows how much care the member used, not why. Quote it in whole dollars.',
   0, 1000000),
  ('CHRONIC_CONDITIONS', 'Number of chronic conditions', 'conditions',
   'Count of distinct long-term conditions with a diagnosis on claims in the last 24 months, from a fixed list: diabetes, heart failure, COPD, asthma, chronic kidney disease, coronary artery disease, and depression.',
   'More chronic conditions usually means more ongoing treatment and more chances for complications. Describe the count; do not guess which conditions the member has, because the model only sees the count.',
   0, 15),
  ('ER_VISITS_12M', 'Emergency room visits, last 12 months', 'visits',
   'Emergency department visits in the last 12 months that did not lead to an inpatient admission.',
   'Repeated ER use often signals health needs that are not being met in other settings, such as primary care. Describe it as a pattern of care use, not as a judgment about the member.',
   0, 30),
  ('INPATIENT_ADMITS_12M', 'Inpatient admissions, last 12 months', 'admissions',
   'Acute inpatient hospital admissions in the last 12 months. Observation stays and ER visits are not counted.',
   'Hospital stays are among the most expensive kinds of care, and a recent admission is a strong signal of further high-cost care. Zero admissions usually pulls a score down.',
   0, 10),
  ('RX_CLASSES', 'Distinct prescription drug classes', 'classes',
   'Number of distinct therapeutic drug classes filled at a pharmacy in the last 12 months.',
   'A rough measure of how many conditions are being treated with medication. It overlaps with the chronic condition count, so the model may give it only a small weight on its own.',
   0, 30),
  ('SPECIALIST_VISITS_12M', 'Specialist visits, last 12 months', 'visits',
   'Office visits with a specialist physician, not a primary care provider, in the last 12 months.',
   'Frequent specialist care usually goes with complex or chronic conditions. It overlaps with the chronic condition count, so its weight on its own is usually small.',
   0, 60),
  ('OPEN_CARE_GAPS', 'Open preventive care gaps', 'gaps',
   'Recommended preventive or chronic-care services the member is due for but has no claim for, such as an annual diabetic eye exam, a cancer screening, or a medication review.',
   'Say the member is due for that many recommended services. Do not say that closing the gaps would lower the member''s cost or score in real life; the model does not show that.',
   0, 10),
  ('PORTAL_LOGINS_12M', 'Member portal logins, last 12 months', 'logins',
   'Number of logins to the member website or mobile app in the last 12 months.',
   'Portal use has no known link to cost in this data. If it appears among the drivers, call it a minor statistical effect of the model, not a reason the member was flagged.',
   0, 365);

UPDATE FEATURE_DICTIONARY d
SET POPULATION_MEDIAN = m.MEDIAN_VALUE
FROM (
  SELECT FEATURE_NAME, MEDIAN_VALUE
  FROM (
    SELECT MEDIAN(AGE) AS AGE, MEDIAN(PRIOR_YEAR_COST) AS PRIOR_YEAR_COST,
           MEDIAN(CHRONIC_CONDITIONS) AS CHRONIC_CONDITIONS, MEDIAN(ER_VISITS_12M) AS ER_VISITS_12M,
           MEDIAN(INPATIENT_ADMITS_12M) AS INPATIENT_ADMITS_12M, MEDIAN(RX_CLASSES) AS RX_CLASSES,
           MEDIAN(SPECIALIST_VISITS_12M) AS SPECIALIST_VISITS_12M, MEDIAN(OPEN_CARE_GAPS) AS OPEN_CARE_GAPS,
           MEDIAN(PORTAL_LOGINS_12M) AS PORTAL_LOGINS_12M
    FROM MEMBER_FEATURES
  ) UNPIVOT (MEDIAN_VALUE FOR FEATURE_NAME IN (
    AGE, PRIOR_YEAR_COST, CHRONIC_CONDITIONS, ER_VISITS_12M, INPATIENT_ADMITS_12M,
    RX_CLASSES, SPECIALIST_VISITS_12M, OPEN_CARE_GAPS, PORTAL_LOGINS_12M))
) m
WHERE d.FEATURE_NAME = m.FEATURE_NAME;

SELECT COUNT(*) AS MEMBERS,
       ROUND(AVG(HIGH_COST_CLAIMANT), 3) AS HIGH_COST_RATE,
       COUNT_IF(HOLDOUT) AS HOLDOUT_MEMBERS
FROM MEMBER_FEATURES;

SELECT FEATURE_NAME, LABEL, UNIT, POPULATION_MEDIAN, LENGTH(DEFINITION) AS DEFINITION_CHARS
FROM FEATURE_DICTIONARY ORDER BY FEATURE_NAME;
```

### `sql/03_train_and_register.sql`

Copy code

```
-- =============================================================================
-- 03_train_and_register.sql
-- Trains an XGBoost high-cost claimant classifier and logs it to the Model
-- Registry as COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.HIGH_COST_CLAIMANT,
-- version V1, with explainability enabled.
--
-- The training runs inside a caller's-rights Python procedure on the recipe
-- warehouse, so the recipe needs no local Python environment. Three log_model
-- arguments decide whether the version gets an EXPLAIN method:
--   sample_input_data   a Snowpark DataFrame of training rows. It defines the
--                       signature, is the background data the Shapley values
--                       are measured against, and records lineage.
--   enable_explainability  set explicitly; do not rely on the default.
--   target_platforms    must include WAREHOUSE; EXPLAIN runs only in a warehouse.
-- A version cannot gain explainability after it is logged, so the procedure
-- drops and relogs the model on every run.
--
-- Idempotent. The CALL takes a few minutes on an XSMALL warehouse.
-- =============================================================================

SET explain_db   = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS';
SET explain_wh   = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_WH';
SET explain_role = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_ADMIN';

USE ROLE IDENTIFIER($explain_role);
USE WAREHOUSE IDENTIFIER($explain_wh);
USE DATABASE IDENTIFIER($explain_db);
USE SCHEMA CARE_MGMT;

CREATE OR REPLACE PROCEDURE TRAIN_AND_REGISTER()
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python', 'snowflake-ml-python', 'xgboost', 'scikit-learn', 'pandas')
HANDLER = 'main'
COMMENT = 'Trains the high-cost claimant model and logs version V1 with explainability.'
EXECUTE AS CALLER
AS
$$
import xgboost as xgb
from sklearn.metrics import roc_auc_score
from snowflake.ml.model import task
from snowflake.ml.registry import Registry
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

DATABASE = "COOKBOOK_EXPLAIN_MODEL_PREDICTIONS"
SCHEMA = "CARE_MGMT"
MODEL_NAME = "HIGH_COST_CLAIMANT"
VERSION_NAME = "V1"
LABEL = "HIGH_COST_CLAIMANT"
FEATURES = [
    "AGE", "PRIOR_YEAR_COST", "CHRONIC_CONDITIONS", "ER_VISITS_12M",
    "INPATIENT_ADMITS_12M", "RX_CLASSES", "SPECIALIST_VISITS_12M",
    "OPEN_CARE_GAPS", "PORTAL_LOGINS_12M",
]

def main(session: Session) -> dict:
    members = session.table(f"{DATABASE}.{SCHEMA}.MEMBER_FEATURES")
    train_df = members.filter(~col("HOLDOUT"))
    train = train_df.select(FEATURES + [LABEL]).to_pandas()
    test = members.filter(col("HOLDOUT")).select(FEATURES + [LABEL]).to_pandas()

    # Shallow, regularized trees. A deeper model fits the pure-noise
    # PORTAL_LOGINS_12M and then "explains" scores with it.
    model = xgb.XGBClassifier(
        n_estimators=250, max_depth=3, learning_rate=0.05,
        min_child_weight=20, reg_lambda=5.0,
        subsample=0.8, colsample_bytree=0.8, random_state=7,
        eval_metric="logloss",
    )
    model.fit(train[FEATURES], train[LABEL])
    holdout_auc = float(roc_auc_score(test[LABEL], model.predict_proba(test[FEATURES])[:, 1]))

    reg = Registry(session=session, database_name=DATABASE, schema_name=SCHEMA)
    if MODEL_NAME in [m.name for m in reg.models()]:
        reg.delete_model(MODEL_NAME)

    # 500 training rows, chosen deterministically, as signature + background data.
    background = train_df.sort(col("MEMBER_ID")).select(FEATURES).limit(500)

    mv = reg.log_model(
        model,
        model_name=MODEL_NAME,
        version_name=VERSION_NAME,
        sample_input_data=background,
        target_platforms=["WAREHOUSE"],
        task=task.Task.TABULAR_BINARY_CLASSIFICATION,
        options={"enable_explainability": True},
        metrics={"holdout_auc": holdout_auc, "train_rows": len(train), "holdout_rows": len(test)},
        comment="Synthetic high-cost claimant classifier (cookbook explain-model-predictions)",
    )

    return {
        "model": f"{DATABASE}.{SCHEMA}.{MODEL_NAME}",
        "version": mv.version_name,
        "functions": sorted(f["name"] for f in mv.show_functions()),
        "holdout_auc": round(holdout_auc, 4),
        "train_rows": len(train),
        "holdout_rows": len(test),
    }
$$;

CALL TRAIN_AND_REGISTER();

SHOW MODELS LIKE 'HIGH_COST_CLAIMANT' IN SCHEMA CARE_MGMT;
SHOW FUNCTIONS IN MODEL HIGH_COST_CLAIMANT VERSION V1;
```

### `sql/04_calibrate.sql`

Copy code

```
-- =============================================================================
-- 04_calibrate.sql
-- Scores the holdout members with SQL inference and writes the two tables the
-- agent uses to talk about confidence:
--   SCORE_CALIBRATION  per score band: holdout members, mean score, and the
--                      share that actually were high-cost claimants
--   MODEL_CARD         one row: holdout AUC, the flag threshold, precision and
--                      recall at that threshold, and the Shapley base value
--
-- A score of 0.26 is not a 26% chance unless the model is calibrated. The band
-- table lets the agent say what scores like this one meant on members the model
-- never saw in training.
--
-- FLAG_THRESHOLD is a business choice, not a model property: the score at
-- which a care manager would review the member. Change it in the SET block.
--
-- Idempotent.
-- =============================================================================

SET explain_db     = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS';
SET explain_wh     = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_WH';
SET explain_role   = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_ADMIN';
SET flag_threshold = 0.35;

USE ROLE IDENTIFIER($explain_role);
USE WAREHOUSE IDENTIFIER($explain_wh);
USE DATABASE IDENTIFIER($explain_db);
USE SCHEMA CARE_MGMT;

-- Holdout scores and the sum of their Shapley values. For this XGBoost
-- classifier, EXPLAIN returns log-odds contributions, so
-- LN(p / (1 - p)) - SUM(explanations) is the same base value for every row.
CREATE OR REPLACE TEMPORARY TABLE HOLDOUT_SCORES AS
SELECT f.MEMBER_ID,
       f.HIGH_COST_CLAIMANT AS ACTUAL,
       MODEL(COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.HIGH_COST_CLAIMANT, V1)!PREDICT_PROBA(
         f.AGE, f.PRIOR_YEAR_COST, f.CHRONIC_CONDITIONS, f.ER_VISITS_12M, f.INPATIENT_ADMITS_12M,
         f.RX_CLASSES, f.SPECIALIST_VISITS_12M, f.OPEN_CARE_GAPS, f.PORTAL_LOGINS_12M
       ):output_feature_1::DOUBLE AS SCORE,
       e.AGE_EXPLANATION + e.PRIOR_YEAR_COST_EXPLANATION + e.CHRONIC_CONDITIONS_EXPLANATION
       + e.ER_VISITS_12M_EXPLANATION + e.INPATIENT_ADMITS_12M_EXPLANATION + e.RX_CLASSES_EXPLANATION
       + e.SPECIALIST_VISITS_12M_EXPLANATION + e.OPEN_CARE_GAPS_EXPLANATION
       + e.PORTAL_LOGINS_12M_EXPLANATION AS SHAP_SUM
FROM MEMBER_FEATURES f,
     TABLE(MODEL(COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.HIGH_COST_CLAIMANT, V1)!EXPLAIN(
       f.AGE, f.PRIOR_YEAR_COST, f.CHRONIC_CONDITIONS, f.ER_VISITS_12M, f.INPATIENT_ADMITS_12M,
       f.RX_CLASSES, f.SPECIALIST_VISITS_12M, f.OPEN_CARE_GAPS, f.PORTAL_LOGINS_12M)) e
WHERE f.HOLDOUT;

CREATE OR REPLACE TABLE SCORE_CALIBRATION (
  BAND_ORDER     NUMBER,
  BAND           VARCHAR,
  MIN_SCORE      DOUBLE,
  MAX_SCORE      DOUBLE,
  HOLDOUT_N      NUMBER,
  MEAN_SCORE     DOUBLE,
  OBSERVED_RATE  DOUBLE
) COMMENT = 'Observed high-cost rate by score band, measured on holdout members.';

INSERT INTO SCORE_CALIBRATION
WITH bands (BAND_ORDER, BAND, MIN_SCORE, MAX_SCORE) AS (
  SELECT * FROM VALUES
    (1, 'very low',  0.00, 0.05),
    (2, 'low',       0.05, 0.10),
    (3, 'moderate',  0.10, 0.20),
    (4, 'elevated',  0.20, 0.35),
    (5, 'high',      0.35, 0.50),
    (6, 'very high', 0.50, 1.01)
)
SELECT b.BAND_ORDER, b.BAND, b.MIN_SCORE, LEAST(b.MAX_SCORE, 1.0),
       COUNT(s.MEMBER_ID), ROUND(AVG(s.SCORE), 4), ROUND(AVG(s.ACTUAL), 4)
FROM bands b
LEFT JOIN HOLDOUT_SCORES s ON s.SCORE >= b.MIN_SCORE AND s.SCORE < b.MAX_SCORE
GROUP BY 1, 2, 3, 4;

SHOW VERSIONS IN MODEL HIGH_COST_CLAIMANT;
SET holdout_auc = (
  SELECT PARSE_JSON("metadata"):metrics:holdout_auc::DOUBLE
  FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) WHERE "name" = 'V1'
);

CREATE OR REPLACE TABLE MODEL_CARD (
  MODEL_NAME              VARCHAR,
  MODEL_VERSION           VARCHAR,
  HOLDOUT_AUC             DOUBLE,
  HOLDOUT_N               NUMBER,
  POPULATION_RATE         DOUBLE,
  FLAG_THRESHOLD          DOUBLE,
  PRECISION_AT_THRESHOLD  DOUBLE,
  RECALL_AT_THRESHOLD     DOUBLE,
  SHAP_BASE_LOGODDS       DOUBLE,
  SHAP_OUTPUT_SPACE       VARCHAR
) COMMENT = 'Facts about model version V1 that the tools return with every answer.';

INSERT INTO MODEL_CARD
SELECT 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.HIGH_COST_CLAIMANT', 'V1',
       ROUND($holdout_auc, 4),
       COUNT(*),
       ROUND(AVG(ACTUAL), 4),
       $flag_threshold,
       ROUND(DIV0(COUNT_IF(SCORE >= $flag_threshold AND ACTUAL = 1), COUNT_IF(SCORE >= $flag_threshold)), 4),
       ROUND(DIV0(COUNT_IF(SCORE >= $flag_threshold AND ACTUAL = 1), COUNT_IF(ACTUAL = 1)), 4),
       ROUND(AVG(LN(SCORE / (1 - SCORE)) - SHAP_SUM), 6),
       'log-odds'
FROM HOLDOUT_SCORES;

-- The base value should be constant: a spread above about 1e-4 means the
-- explanations are not in log-odds space and the tools would misreport them.
SELECT ROUND(STDDEV(LN(SCORE / (1 - SCORE)) - SHAP_SUM), 8) AS BASE_VALUE_SPREAD FROM HOLDOUT_SCORES;

SELECT * FROM SCORE_CALIBRATION ORDER BY BAND_ORDER;
SELECT * FROM MODEL_CARD;
```

### `sql/05_tools.sql`

Copy code

```
-- =============================================================================
-- 05_tools.sql
-- The three procedures the agent calls. All run with caller's rights, take only
-- scalar arguments, and return a compact VARIANT of a few kilobytes: top
-- drivers, not every row the model touched.
--
--   SCORE_AND_EXPLAIN_MEMBER(MEMBER_ID)
--     Score from PREDICT_PROBA, the holdout calibration band the score falls
--     in, model facts, and the five features with the largest Shapley values
--     from EXPLAIN. Each driver carries the member's value, the population
--     median, and the feature's DEFINITION and HOW_TO_EXPLAIN text, so the
--     agent explains it in the plan's words rather than its own.
--
--   DESCRIBE_FEATURES()
--     The whole feature dictionary, for questions about what a feature means
--     that are not about a particular member.
--
--   WHAT_IF_MEMBER(MEMBER_ID, FEATURE_NAME, NEW_VALUE)
--     Re-scores the member with one feature changed and reports the score and
--     band before and after. FEATURE_NAME must be a row in FEATURE_DICTIONARY
--     and NEW_VALUE must be inside that row's range. The changed column is
--     chosen with IFF per column, so no user or model text reaches dynamic SQL.
--
-- Shapley values here are log-odds contributions relative to the base value
-- in MODEL_CARD. The tools report direction, size, and share of the total; they
-- never convert one feature's contribution into "percentage points".
--
-- Idempotent.
-- =============================================================================

SET explain_db   = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS';
SET explain_wh   = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_WH';
SET explain_role = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_ADMIN';

USE ROLE IDENTIFIER($explain_role);
USE WAREHOUSE IDENTIFIER($explain_wh);
USE DATABASE IDENTIFIER($explain_db);
USE SCHEMA CARE_MGMT;

CREATE OR REPLACE PROCEDURE SCORE_AND_EXPLAIN_MEMBER(MEMBER_ID VARCHAR)
RETURNS VARIANT
LANGUAGE SQL
COMMENT = 'Scores one member with HIGH_COST_CLAIMANT V1 and returns its calibration band and top Shapley drivers.'
EXECUTE AS CALLER
AS
$$
DECLARE
  member VARCHAR DEFAULT UPPER(TRIM(:MEMBER_ID));
  found INTEGER;
  result VARIANT;
BEGIN
  found := (SELECT COUNT(*) FROM COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.MEMBER_FEATURES
            WHERE MEMBER_ID = :member);
  IF (found = 0) THEN
    RETURN OBJECT_CONSTRUCT('error', 'No member with MEMBER_ID ' || COALESCE(:member, 'NULL') ||
                            '. IDs look like M000123.');
  END IF;

  result := (
    WITH s AS (
      SELECT f.MEMBER_ID,
             MODEL(COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.HIGH_COST_CLAIMANT, V1)!PREDICT_PROBA(
               f.AGE, f.PRIOR_YEAR_COST, f.CHRONIC_CONDITIONS, f.ER_VISITS_12M, f.INPATIENT_ADMITS_12M,
               f.RX_CLASSES, f.SPECIALIST_VISITS_12M, f.OPEN_CARE_GAPS, f.PORTAL_LOGINS_12M
             ):output_feature_1::DOUBLE AS SCORE,
             OBJECT_CONSTRUCT(
               'AGE', f.AGE, 'PRIOR_YEAR_COST', f.PRIOR_YEAR_COST, 'CHRONIC_CONDITIONS', f.CHRONIC_CONDITIONS,
               'ER_VISITS_12M', f.ER_VISITS_12M, 'INPATIENT_ADMITS_12M', f.INPATIENT_ADMITS_12M,
               'RX_CLASSES', f.RX_CLASSES, 'SPECIALIST_VISITS_12M', f.SPECIALIST_VISITS_12M,
               'OPEN_CARE_GAPS', f.OPEN_CARE_GAPS, 'PORTAL_LOGINS_12M', f.PORTAL_LOGINS_12M) AS FEATURE_VALUES,
             OBJECT_CONSTRUCT(
               'AGE', e.AGE_EXPLANATION, 'PRIOR_YEAR_COST', e.PRIOR_YEAR_COST_EXPLANATION,
               'CHRONIC_CONDITIONS', e.CHRONIC_CONDITIONS_EXPLANATION, 'ER_VISITS_12M', e.ER_VISITS_12M_EXPLANATION,
               'INPATIENT_ADMITS_12M', e.INPATIENT_ADMITS_12M_EXPLANATION, 'RX_CLASSES', e.RX_CLASSES_EXPLANATION,
               'SPECIALIST_VISITS_12M', e.SPECIALIST_VISITS_12M_EXPLANATION, 'OPEN_CARE_GAPS', e.OPEN_CARE_GAPS_EXPLANATION,
               'PORTAL_LOGINS_12M', e.PORTAL_LOGINS_12M_EXPLANATION) AS CONTRIBUTIONS
      FROM COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.MEMBER_FEATURES f,
           TABLE(MODEL(COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.HIGH_COST_CLAIMANT, V1)!EXPLAIN(
             f.AGE, f.PRIOR_YEAR_COST, f.CHRONIC_CONDITIONS, f.ER_VISITS_12M, f.INPATIENT_ADMITS_12M,
             f.RX_CLASSES, f.SPECIALIST_VISITS_12M, f.OPEN_CARE_GAPS, f.PORTAL_LOGINS_12M)) e
      WHERE f.MEMBER_ID = :member
    ),
    ranked AS (
      SELECT s.MEMBER_ID, s.SCORE, c.KEY AS FEATURE_NAME, c.VALUE::DOUBLE AS CONTRIBUTION,
             GET(s.FEATURE_VALUES, c.KEY)::DOUBLE AS MEMBER_VALUE,
             d.LABEL, d.UNIT, d.POPULATION_MEDIAN, d.DEFINITION, d.HOW_TO_EXPLAIN,
             ABS(c.VALUE::DOUBLE) / SUM(ABS(c.VALUE::DOUBLE)) OVER () AS SHARE,
             ROW_NUMBER() OVER (ORDER BY ABS(c.VALUE::DOUBLE) DESC) AS RANK
      FROM s, LATERAL FLATTEN(INPUT => s.CONTRIBUTIONS) c
      JOIN COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.FEATURE_DICTIONARY d ON d.FEATURE_NAME = c.KEY
    ),
    agg AS (
      SELECT ANY_VALUE(MEMBER_ID) AS MEMBER_ID, ANY_VALUE(SCORE) AS SCORE,
             ARRAY_AGG(IFF(RANK <= 5, OBJECT_CONSTRUCT(
               'rank', RANK, 'feature', FEATURE_NAME, 'label', LABEL, 'unit', UNIT,
               'definition', DEFINITION, 'how_to_explain', HOW_TO_EXPLAIN,
               'member_value', MEMBER_VALUE, 'population_median', POPULATION_MEDIAN,
               'effect_on_score', IFF(CONTRIBUTION >= 0, 'raises', 'lowers'),
               'shapley_logodds', ROUND(CONTRIBUTION, 3),
               'share_of_total_attribution', ROUND(SHARE, 3)), NULL)) WITHIN GROUP (ORDER BY RANK) AS DRIVERS,
             ROUND(SUM(IFF(RANK > 5, SHARE, 0)), 3) AS OTHER_SHARE
      FROM ranked
    )
    SELECT OBJECT_CONSTRUCT(
      'member_id', a.MEMBER_ID,
      'score', ROUND(a.SCORE, 3),
      'flagged_high_cost', a.SCORE >= m.FLAG_THRESHOLD,
      'flag_threshold', m.FLAG_THRESHOLD,
      'calibration', OBJECT_CONSTRUCT(
        'band', b.BAND, 'band_range', b.MIN_SCORE || ' to ' || b.MAX_SCORE,
        'holdout_members_in_band', b.HOLDOUT_N,
        'observed_high_cost_rate_in_band', b.OBSERVED_RATE,
        'mean_score_in_band', b.MEAN_SCORE),
      'model', OBJECT_CONSTRUCT(
        'name', m.MODEL_NAME, 'version', m.MODEL_VERSION, 'holdout_auc', m.HOLDOUT_AUC,
        'population_high_cost_rate', m.POPULATION_RATE,
        'precision_at_flag_threshold', m.PRECISION_AT_THRESHOLD,
        'recall_at_flag_threshold', m.RECALL_AT_THRESHOLD),
      'explanation', OBJECT_CONSTRUCT(
        'method', 'Shapley values from the model EXPLAIN method, in log-odds, relative to the base score',
        'base_score', ROUND(1 / (1 + EXP(-m.SHAP_BASE_LOGODDS)), 3),
        'top_drivers', a.DRIVERS,
        'share_of_attribution_from_other_features', a.OTHER_SHARE),
      'caution', 'Attributions describe how the model used each feature to produce this score. ' ||
                 'They are not causes, and changing a feature in real life will not necessarily change the outcome.')
    FROM agg a
    CROSS JOIN COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.MODEL_CARD m
    JOIN COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.SCORE_CALIBRATION b
      ON a.SCORE >= b.MIN_SCORE AND (a.SCORE < b.MAX_SCORE OR b.MAX_SCORE = 1.0)
  );
  RETURN result;
END;
$$;

CREATE OR REPLACE PROCEDURE WHAT_IF_MEMBER(MEMBER_ID VARCHAR, FEATURE_NAME VARCHAR, NEW_VALUE FLOAT)
RETURNS VARIANT
LANGUAGE SQL
COMMENT = 'Re-scores one member with one feature changed. Model sensitivity only, not an intervention effect.'
EXECUTE AS CALLER
AS
$$
DECLARE
  member VARCHAR DEFAULT UPPER(TRIM(:MEMBER_ID));
  feature VARCHAR DEFAULT UPPER(TRIM(:FEATURE_NAME));
  found INTEGER;
  lo DOUBLE;
  hi DOUBLE;
  result VARIANT;
BEGIN
  found := (SELECT COUNT(*) FROM COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.MEMBER_FEATURES
            WHERE MEMBER_ID = :member);
  IF (found = 0) THEN
    RETURN OBJECT_CONSTRUCT('error', 'No member with MEMBER_ID ' || COALESCE(:member, 'NULL') ||
                            '. IDs look like M000123.');
  END IF;

  -- FEATURE_DICTIONARY is the allowlist.
  found := (SELECT COUNT(*) FROM COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.FEATURE_DICTIONARY
            WHERE FEATURE_NAME = :feature);
  IF (found = 0) THEN
    RETURN OBJECT_CONSTRUCT('error', 'Unknown feature ' || COALESCE(:feature, 'NULL'),
      'allowed_features', (SELECT ARRAY_AGG(FEATURE_NAME) WITHIN GROUP (ORDER BY FEATURE_NAME)
                           FROM COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.FEATURE_DICTIONARY));
  END IF;
  lo := (SELECT MIN_VALUE FROM COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.FEATURE_DICTIONARY WHERE FEATURE_NAME = :feature);
  hi := (SELECT MAX_VALUE FROM COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.FEATURE_DICTIONARY WHERE FEATURE_NAME = :feature);
  IF (:NEW_VALUE IS NULL OR :NEW_VALUE < :lo OR :NEW_VALUE > :hi) THEN
    RETURN OBJECT_CONSTRUCT('error', 'NEW_VALUE for ' || :feature || ' must be between ' || :lo || ' and ' || :hi);
  END IF;

  result := (
    WITH f AS (
      SELECT * FROM COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.MEMBER_FEATURES WHERE MEMBER_ID = :member
    ),
    scenarios AS (
      SELECT 'before' AS SCENARIO, AGE, PRIOR_YEAR_COST, CHRONIC_CONDITIONS, ER_VISITS_12M, INPATIENT_ADMITS_12M,
             RX_CLASSES, SPECIALIST_VISITS_12M, OPEN_CARE_GAPS, PORTAL_LOGINS_12M
      FROM f
      UNION ALL
      SELECT 'after',
             IFF(:feature = 'AGE',                   :NEW_VALUE, AGE),
             IFF(:feature = 'PRIOR_YEAR_COST',       :NEW_VALUE, PRIOR_YEAR_COST),
             IFF(:feature = 'CHRONIC_CONDITIONS',    :NEW_VALUE, CHRONIC_CONDITIONS),
             IFF(:feature = 'ER_VISITS_12M',         :NEW_VALUE, ER_VISITS_12M),
             IFF(:feature = 'INPATIENT_ADMITS_12M',  :NEW_VALUE, INPATIENT_ADMITS_12M),
             IFF(:feature = 'RX_CLASSES',            :NEW_VALUE, RX_CLASSES),
             IFF(:feature = 'SPECIALIST_VISITS_12M', :NEW_VALUE, SPECIALIST_VISITS_12M),
             IFF(:feature = 'OPEN_CARE_GAPS',        :NEW_VALUE, OPEN_CARE_GAPS),
             IFF(:feature = 'PORTAL_LOGINS_12M',     :NEW_VALUE, PORTAL_LOGINS_12M)
      FROM f
    ),
    s AS (
      SELECT x.SCENARIO,
             MODEL(COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.HIGH_COST_CLAIMANT, V1)!PREDICT_PROBA(
               x.AGE, x.PRIOR_YEAR_COST, x.CHRONIC_CONDITIONS, x.ER_VISITS_12M, x.INPATIENT_ADMITS_12M,
               x.RX_CLASSES, x.SPECIALIST_VISITS_12M, x.OPEN_CARE_GAPS, x.PORTAL_LOGINS_12M
             ):output_feature_1::DOUBLE AS SCORE,
             OBJECT_CONSTRUCT(
               'AGE', x.AGE, 'PRIOR_YEAR_COST', x.PRIOR_YEAR_COST, 'CHRONIC_CONDITIONS', x.CHRONIC_CONDITIONS,
               'ER_VISITS_12M', x.ER_VISITS_12M, 'INPATIENT_ADMITS_12M', x.INPATIENT_ADMITS_12M,
               'RX_CLASSES', x.RX_CLASSES, 'SPECIALIST_VISITS_12M', x.SPECIALIST_VISITS_12M,
               'OPEN_CARE_GAPS', x.OPEN_CARE_GAPS, 'PORTAL_LOGINS_12M', x.PORTAL_LOGINS_12M) AS FEATURE_VALUES,
             OBJECT_CONSTRUCT(
               'AGE', e.AGE_EXPLANATION, 'PRIOR_YEAR_COST', e.PRIOR_YEAR_COST_EXPLANATION,
               'CHRONIC_CONDITIONS', e.CHRONIC_CONDITIONS_EXPLANATION, 'ER_VISITS_12M', e.ER_VISITS_12M_EXPLANATION,
               'INPATIENT_ADMITS_12M', e.INPATIENT_ADMITS_12M_EXPLANATION, 'RX_CLASSES', e.RX_CLASSES_EXPLANATION,
               'SPECIALIST_VISITS_12M', e.SPECIALIST_VISITS_12M_EXPLANATION, 'OPEN_CARE_GAPS', e.OPEN_CARE_GAPS_EXPLANATION,
               'PORTAL_LOGINS_12M', e.PORTAL_LOGINS_12M_EXPLANATION) AS CONTRIBUTIONS
      FROM scenarios x,
           TABLE(MODEL(COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.HIGH_COST_CLAIMANT, V1)!EXPLAIN(
             x.AGE, x.PRIOR_YEAR_COST, x.CHRONIC_CONDITIONS, x.ER_VISITS_12M, x.INPATIENT_ADMITS_12M,
             x.RX_CLASSES, x.SPECIALIST_VISITS_12M, x.OPEN_CARE_GAPS, x.PORTAL_LOGINS_12M)) e
    ),
    ranked AS (
      SELECT s.SCENARIO, s.SCORE, c.KEY AS FEATURE_NAME, c.VALUE::DOUBLE AS CONTRIBUTION,
             GET(s.FEATURE_VALUES, c.KEY)::DOUBLE AS VALUE,
             d.LABEL, d.DEFINITION, d.HOW_TO_EXPLAIN, d.POPULATION_MEDIAN,
             ROW_NUMBER() OVER (PARTITION BY s.SCENARIO ORDER BY ABS(c.VALUE::DOUBLE) DESC) AS RANK
      FROM s, LATERAL FLATTEN(INPUT => s.CONTRIBUTIONS) c
      JOIN COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.FEATURE_DICTIONARY d ON d.FEATURE_NAME = c.KEY
    ),
    per_scenario AS (
      SELECT r.SCENARIO, ANY_VALUE(r.SCORE) AS SCORE,
             MAX(IFF(r.FEATURE_NAME = :feature, r.VALUE, NULL)) AS FEATURE_VALUE,
             MAX(IFF(r.FEATURE_NAME = :feature, r.CONTRIBUTION, NULL)) AS FEATURE_CONTRIBUTION,
             MAX(IFF(r.FEATURE_NAME = :feature, r.RANK, NULL)) AS FEATURE_RANK,
             ANY_VALUE(IFF(r.FEATURE_NAME = :feature, r.LABEL, NULL)) AS FEATURE_LABEL,
             ANY_VALUE(IFF(r.FEATURE_NAME = :feature, r.DEFINITION, NULL)) AS FEATURE_DEFINITION,
             ANY_VALUE(IFF(r.FEATURE_NAME = :feature, r.HOW_TO_EXPLAIN, NULL)) AS FEATURE_HOW_TO_EXPLAIN,
             ANY_VALUE(IFF(r.FEATURE_NAME = :feature, r.POPULATION_MEDIAN, NULL)) AS FEATURE_MEDIAN,
             ARRAY_AGG(IFF(r.RANK <= 3, r.LABEL, NULL)) WITHIN GROUP (ORDER BY r.RANK) AS TOP_3_DRIVERS
      FROM ranked r
      GROUP BY r.SCENARIO
    ),
    banded AS (
      SELECT p.*, b.BAND, b.OBSERVED_RATE
      FROM per_scenario p
      JOIN COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.SCORE_CALIBRATION b
        ON p.SCORE >= b.MIN_SCORE AND (p.SCORE < b.MAX_SCORE OR b.MAX_SCORE = 1.0)
    ),
    -- One object per scenario, keyed 'before' and 'after'. MAX() cannot pivot
    -- the TOP_3_DRIVERS array, OBJECT_AGG can.
    pivoted AS (
      SELECT OBJECT_AGG(SCENARIO, OBJECT_CONSTRUCT(
               'score', ROUND(SCORE, 3),
               'band', BAND,
               'observed_high_cost_rate_in_band', OBSERVED_RATE,
               'feature_value', FEATURE_VALUE,
               'feature_shapley_logodds', ROUND(FEATURE_CONTRIBUTION, 3),
               'feature_rank_among_drivers', FEATURE_RANK,
               'top_3_drivers', TOP_3_DRIVERS)) AS S,
             ANY_VALUE(FEATURE_LABEL) AS FEATURE_LABEL,
             ANY_VALUE(FEATURE_DEFINITION) AS FEATURE_DEFINITION,
             ANY_VALUE(FEATURE_HOW_TO_EXPLAIN) AS FEATURE_HOW_TO_EXPLAIN,
             ANY_VALUE(FEATURE_MEDIAN) AS FEATURE_MEDIAN,
             MAX(IFF(SCENARIO = 'after', SCORE, NULL)) - MAX(IFF(SCENARIO = 'before', SCORE, NULL)) AS SCORE_CHANGE
      FROM banded
    )
    SELECT OBJECT_CONSTRUCT(
      'member_id', :member,
      'changed_feature', :feature,
      'label', FEATURE_LABEL,
      'definition', FEATURE_DEFINITION,
      'how_to_explain', FEATURE_HOW_TO_EXPLAIN,
      'population_median', FEATURE_MEDIAN,
      'from_value', S:before:feature_value,
      'to_value', S:after:feature_value,
      'before', S:before,
      'after', S:after,
      'score_change', ROUND(SCORE_CHANGE, 3),
      'caution', 'This is model sensitivity: how the score responds when one input is changed and all others are ' ||
                 'held fixed. It is not an estimate of what would happen to this member after an intervention.')
    FROM pivoted
  );
  RETURN result;
END;
$$;

CREATE OR REPLACE PROCEDURE DESCRIBE_FEATURES()
RETURNS VARIANT
LANGUAGE SQL
COMMENT = 'Returns the label, definition, explanation guidance, median, and valid range of every model feature.'
EXECUTE AS CALLER
AS
$$
DECLARE
  result VARIANT;
BEGIN
  result := (
    SELECT OBJECT_CONSTRUCT(
      'model', 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.HIGH_COST_CLAIMANT V1',
      'features', ARRAY_AGG(OBJECT_CONSTRUCT(
        'feature', FEATURE_NAME, 'label', LABEL, 'unit', UNIT,
        'definition', DEFINITION, 'how_to_explain', HOW_TO_EXPLAIN,
        'population_median', POPULATION_MEDIAN,
        'valid_range', MIN_VALUE || ' to ' || MAX_VALUE)) WITHIN GROUP (ORDER BY FEATURE_NAME))
    FROM COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.FEATURE_DICTIONARY
  );
  RETURN result;
END;
$$;

CALL SCORE_AND_EXPLAIN_MEMBER('M000003');
CALL WHAT_IF_MEMBER('M000003', 'ER_VISITS_12M', 0);
CALL WHAT_IF_MEMBER('M000003', 'BLOOD_TYPE', 1);
CALL DESCRIBE_FEATURES();
```

### `sql/06_agent.sql`

Copy code

```
-- =============================================================================
-- 06_agent.sql
-- The agent, and the grants that let COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_USER
-- use it and nothing more.
--
-- The agent has exactly three tools, all procedures from 05. There is no Cortex
-- Analyst tool and no access to raw tables: every number in an answer comes
-- from the registered model, its EXPLAIN method, or the holdout calibration,
-- and every definition of a feature comes from FEATURE_DICTIONARY.
--
-- The instructions do the interpretive work: lead with the score and what it
-- meant on holdout members, name the drivers in plain language against the
-- population median, and never turn an attribution into a cause.
--
-- The tool procedures run with caller's rights, so the user role needs USAGE on
-- the model (inference only; READ would also expose its metadata), USAGE on the
-- three procedures, and SELECT on the four tables they read. 02 to 04 recreate those tables and the model, which
-- drops grants on them, so rerun this file after rerunning any of 02 to 04.
--
-- CREATE OR REPLACE AGENT ... COPY GRANTS keeps USAGE on the agent across reruns.
-- COPY GRANTS goes after COMMENT, right before FROM SPECIFICATION.
--
-- Idempotent.
-- =============================================================================

SET explain_db        = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS';
SET explain_wh        = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_WH';
SET explain_role      = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_ADMIN';
SET explain_user_role = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_USER';

USE ROLE IDENTIFIER($explain_role);
USE WAREHOUSE IDENTIFIER($explain_wh);
USE DATABASE IDENTIFIER($explain_db);
USE SCHEMA CARE_MGMT;

CREATE OR REPLACE AGENT COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.RISK_EXPLAINER
  COMMENT = 'Explains high-cost claimant scores from a Model Registry model using its Shapley values.'
  COPY GRANTS
  FROM SPECIFICATION
$$
models:
  orchestration: auto

orchestration:
  budget:
    seconds: 90
    tokens: 24000

instructions:
  orchestration: |
    You explain scores from a high-cost claimant model to care managers. Every
    number you give must come from a tool result in this conversation.

    For any question about a specific member, call score_and_explain_member with
    the member ID. Member IDs look like M000123. If the user did not give one,
    ask for it. Call it again for each member mentioned.

    For "what if", "what would happen if", or "how much does X matter" questions
    about a member, call what_if_member with the member ID, the feature name, and
    the new value. Feature names are AGE, PRIOR_YEAR_COST, CHRONIC_CONDITIONS,
    ER_VISITS_12M, INPATIENT_ADMITS_12M, RX_CLASSES, SPECIALIST_VISITS_12M,
    OPEN_CARE_GAPS, and PORTAL_LOGINS_12M. Map the user's words to one of them.

    For questions about what a feature means, how it is counted, or which
    features the model uses, with no member involved, call describe_features.

    If a tool returns an error, tell the user what it says.

    Never create charts. Do not use the data_to_chart tool. Answer in text.

  response: |
    Write for a care manager, not a data scientist. Be brief: a short paragraph
    and a short bullet list.

    Structure an explanation of a score like this:
    1. The score, and whether it is at or above the flag threshold.
    2. What the score means, from the calibration block: "Among holdout members
       with scores in this band, X% turned out to be high-cost claimants." Say
       how many holdout members the band holds. Do not call the score itself a
       probability or a certainty.
    3. The top three drivers, in plain language, each with the member's value and
       the population median (for example "5 ER visits, against a median of 0").
       Say whether each one raised or lowered the score, and add one short clause
       on what the feature is a signal of, taken from its how_to_explain text.
    4. If the user asks how confident the model is, also give the holdout AUC and
       the precision at the flag threshold ("of members flagged at this threshold,
       X% were high-cost"). Explain that AUC measures ranking across all members,
       not certainty about this one.

    Explaining features:
    - Name each feature by its label, never by its column name.
    - Define a feature only with its definition from a tool result, in your own
      words if that reads better, but without adding facts it does not contain.
      If a user asks about something the definition does not cover (for example
      which conditions this member has, or how a term is defined elsewhere), say
      the model data does not include that.
    - Follow each feature's how_to_explain guidance. It overrides your general
      knowledge about what a feature usually means. It is written for you, not
      the user: pass on what it says the feature signals, but do not repeat its
      instructions ("say...", "do not say...") to the user.

    Language rules:
    - Drivers "contributed to" or "pushed up" the score. Never say a feature
      caused high cost, and never say changing it would lower the member's cost.
    - Do not convert a Shapley value into percentage points of probability. Use
      share_of_total_attribution if you need to compare drivers.
    - For what_if_member results, call it "model sensitivity" and state that it
      shows how the score responds to an input, not what would happen after an
      intervention.
    - Format money as USD with no cents. Round scores to two decimals.
    - Do not make clinical, coverage, or eligibility decisions. If asked, say the
      score is one input for a care manager's review.

tools:
  - tool_spec:
      type: generic
      name: score_and_explain_member
      description: >
        Scores one member with the HIGH_COST_CLAIMANT model (version V1). Returns
        the score, whether it is above the flag threshold, the calibration band
        with the observed high-cost rate among holdout members in that band, model
        facts (holdout AUC, precision and recall at the threshold), and the five
        features with the largest Shapley values, each with the member's value,
        the population median, direction, and share of total attribution.
      input_schema:
        type: object
        properties:
          member_id:
            type: string
            description: The member ID, for example M000123.
        required: [member_id]
  - tool_spec:
      type: generic
      name: what_if_member
      description: >
        Re-scores one member with a single feature set to a new value, all other
        features unchanged. Returns the score, band, and observed band rate before
        and after, and how the changed feature's attribution moved. This measures
        model sensitivity, not the effect of an intervention.
      input_schema:
        type: object
        properties:
          member_id:
            type: string
            description: The member ID, for example M000123.
          feature_name:
            type: string
            description: >
              One of AGE, PRIOR_YEAR_COST, CHRONIC_CONDITIONS, ER_VISITS_12M,
              INPATIENT_ADMITS_12M, RX_CLASSES, SPECIALIST_VISITS_12M,
              OPEN_CARE_GAPS, PORTAL_LOGINS_12M.
          new_value:
            type: number
            description: The value to use for that feature.
        required: [member_id, feature_name, new_value]
  - tool_spec:
      type: generic
      name: describe_features
      description: >
        Returns every feature the model uses, with its plain-language label,
        unit, definition (what it measures and how it is counted), guidance on
        how to explain it, the population median, and the valid range. Use it
        for "what does this feature mean" questions that are not about one
        member.
      input_schema:
        type: object
        properties: {}

tool_resources:
  score_and_explain_member:
    type: procedure
    identifier: COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.SCORE_AND_EXPLAIN_MEMBER
    name: "SCORE_AND_EXPLAIN_MEMBER(VARCHAR)"
    execution_environment:
      type: warehouse
      warehouse: COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_WH
  what_if_member:
    type: procedure
    identifier: COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.WHAT_IF_MEMBER
    name: "WHAT_IF_MEMBER(VARCHAR, VARCHAR, FLOAT)"
    execution_environment:
      type: warehouse
      warehouse: COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_WH
  describe_features:
    type: procedure
    identifier: COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.DESCRIBE_FEATURES
    name: "DESCRIBE_FEATURES()"
    execution_environment:
      type: warehouse
      warehouse: COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_WH
$$;

-- ---------------------------------------------------------------------------
-- Least-privilege grants for the role people use to talk to the agent.
-- ---------------------------------------------------------------------------
GRANT USAGE ON DATABASE IDENTIFIER($explain_db) TO ROLE IDENTIFIER($explain_user_role);
GRANT USAGE ON SCHEMA COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT TO ROLE IDENTIFIER($explain_user_role);
GRANT USAGE ON AGENT COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.RISK_EXPLAINER TO ROLE IDENTIFIER($explain_user_role);
GRANT USAGE ON PROCEDURE COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.SCORE_AND_EXPLAIN_MEMBER(VARCHAR)
  TO ROLE IDENTIFIER($explain_user_role);
GRANT USAGE ON PROCEDURE COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.WHAT_IF_MEMBER(VARCHAR, VARCHAR, FLOAT)
  TO ROLE IDENTIFIER($explain_user_role);
GRANT USAGE ON PROCEDURE COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.DESCRIBE_FEATURES()
  TO ROLE IDENTIFIER($explain_user_role);
GRANT USAGE ON MODEL COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.HIGH_COST_CLAIMANT
  TO ROLE IDENTIFIER($explain_user_role);
GRANT SELECT ON TABLE COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.MEMBER_FEATURES TO ROLE IDENTIFIER($explain_user_role);
GRANT SELECT ON TABLE COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.FEATURE_DICTIONARY TO ROLE IDENTIFIER($explain_user_role);
GRANT SELECT ON TABLE COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.SCORE_CALIBRATION TO ROLE IDENTIFIER($explain_user_role);
GRANT SELECT ON TABLE COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.MODEL_CARD TO ROLE IDENTIFIER($explain_user_role);

SHOW GRANTS TO ROLE IDENTIFIER($explain_user_role);
```

### `sql/07_ask_agent.sql`

Copy code

```
-- =============================================================================
-- 07_ask_agent.sql
-- Ask the agent the kinds of question this recipe is built for, as the
-- least-privileged user role, then call the tools directly so you can compare
-- the agent's prose with the JSON it was given. Question 5 asks for something
-- the feature dictionary does not contain; the agent should say so.
--
-- The user running this needs COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_USER, which
-- 01 grants to whoever ran it.
-- =============================================================================

SET explain_wh        = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_WH';
SET explain_user_role = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_USER';

USE ROLE IDENTIFIER($explain_user_role);
USE SECONDARY ROLES NONE;
USE WAREHOUSE IDENTIFIER($explain_wh);

-- DATA_AGENT_RUN takes constant arguments, so each question is a literal.
-- For each answer: which tools ran, with what input, and the final text.
WITH runs AS (
  SELECT 1 AS q, 'explain' AS test, TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.RISK_EXPLAINER',
    $${"messages": [{"role": "user", "content": [
      {"type": "text", "text": "Why was member M000003 flagged as a likely high-cost claimant?"}
    ]}]}$$)) AS j
  UNION ALL
  SELECT 2, 'confidence', TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.RISK_EXPLAINER',
    $${"messages": [{"role": "user", "content": [
      {"type": "text", "text": "How confident is the model about member M000003, and how much should I trust that score?"}
    ]}]}$$))
  UNION ALL
  SELECT 3, 'what-if', TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.RISK_EXPLAINER',
    $${"messages": [{"role": "user", "content": [
      {"type": "text", "text": "For member M000003, what would the score be if they had no ER visits in the last 12 months?"}
    ]}]}$$))
  UNION ALL
  SELECT 4, 'definition', TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.RISK_EXPLAINER',
    $${"messages": [{"role": "user", "content": [
      {"type": "text", "text": "What counts as an open care gap in this model, and how is prior-year cost measured?"}
    ]}]}$$))
  UNION ALL
  SELECT 5, 'not in the data', TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.RISK_EXPLAINER',
    $${"messages": [{"role": "user", "content": [
      {"type": "text", "text": "Which chronic conditions does member M000003 have?"}
    ]}]}$$))
)
SELECT r.q, r.test,
       ARRAY_AGG(DISTINCT IFF(c.value:type::STRING = 'tool_use', c.value:tool_use:name::STRING, NULL)) AS tools_called,
       ARRAY_AGG(IFF(c.value:type::STRING = 'tool_use', c.value:tool_use:input, NULL)) AS tool_inputs,
       -- The final answer is the last text block in content[].
       MAX_BY(c.value:text::STRING, IFF(c.value:type::STRING = 'text', c.index, NULL)) AS answer,
       ANY_VALUE(r.j:message::STRING) AS error_message
FROM runs r, LATERAL FLATTEN(input => r.j:content, OUTER => TRUE) c
GROUP BY r.q, r.test
ORDER BY r.q;

-- The raw tool results the agent turned into those answers.
CALL COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.SCORE_AND_EXPLAIN_MEMBER('M000003');
CALL COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.WHAT_IF_MEMBER('M000003', 'ER_VISITS_12M', 0);
CALL COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.DESCRIBE_FEATURES();
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- 99_teardown.sql
-- Removes everything this recipe created.
--
-- Dropping the database removes the model and its versions, the agent, the
-- procedures, and the tables. Then the warehouse and both roles are dropped,
-- which also removes their SNOWFLAKE.CORTEX_USER grants. There are no account
-- parameters to restore.
-- =============================================================================

SET explain_db        = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS';
SET explain_wh        = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_WH';
SET explain_role      = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_ADMIN';
SET explain_user_role = 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_USER';

USE ROLE ACCOUNTADMIN;
DROP DATABASE IF EXISTS IDENTIFIER($explain_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($explain_wh);
DROP ROLE IF EXISTS IDENTIFIER($explain_user_role);
DROP ROLE IF EXISTS IDENTIFIER($explain_role);

SHOW DATABASES LIKE 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS%';
SHOW WAREHOUSES LIKE 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS%';
SHOW ROLES LIKE 'COOKBOOK_EXPLAIN_MODEL_PREDICTIONS%';
```
