# Scheduled retraining with a task graph and a quality gate: code

Every file in the [Scheduled retraining with a task graph and a quality gate](/developer-guide/cortex-ai-cookbook/ml-pipeline-orchestration) recipe. To run the recipe, download [ml-pipeline-orchestration.zip](/static/samples/cortex-ai-cookbook/ml-pipeline-orchestration.zip), unzip it, and run the scripts from the `ml-pipeline-orchestration/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/ml-pipeline-orchestration); the zip includes it as `README.md`.

## `notebooks/`

### `notebooks/01_ml_pipeline_orchestration.ipynb`

Jupyter notebook, shown as Python with Markdown cells as comments.

Copy code

```
# %% [markdown]
# # ML pipeline orchestration with Snowflake Tasks
#
# Automate an end-to-end ML pipeline as a **Snowflake task graph (DAG)**. Three Python stored
# procedures (feature engineering, training, and evaluation) run as dependent tasks on a schedule.
# They share runtime settings through the **task graph config** and pass results to each other with
# **task return values**. A new model version is registered in the **Model Registry** on every run,
# and it is promoted to the default version only if it clears a quality gate.
#
# Before you run it:
#
# 1. Run `sql/01_setup.sql` and `sql/02_data.sql` as described in the recipe README. They create the
#    role (with `EXECUTE TASK`), warehouse, database, stage, and the `LOAN_APPLICATIONS` table.
# 2. Run the notebook locally (Jupyter or VS Code) after `pip install -r requirements.txt`, with a
#    Snowflake connection for your own user (for example
#    `SNOWFLAKE_DEFAULT_CONNECTION_NAME=<your connection>`). It can also run as a Snowflake Notebook
#    in a Workspace, where it reuses the active session.
#
# Step 4 deploys the task graph **resumed**, on a weekly schedule. Step 8 suspends it, and
# `sql/99_teardown.sql` removes it.

# %%
import json
import logging
import time
from datetime import timedelta

from IPython.display import Code
from snowflake.core import CreateMode, Root
from snowflake.core.task.dagv1 import DAG, DAGOperation, DAGTask
from snowflake.ml.registry import Registry
from snowflake.snowpark import Session

# Hide Snowpark's local-vs-server package version notices during procedure registration.
logging.getLogger("snowflake.snowpark").setLevel(logging.ERROR)

# %% [markdown]
# ## Configuration
#
# Object names match `sql/01_setup.sql` and are fixed. `PIPELINE_CONFIG` becomes the task graph
# config. Every task reads it at run time, so you can change the inputs or the quality bar without
# redeploying any code. `SCHEDULE` and `auc_threshold` are safe to change.

# %%
DATABASE = "COOKBOOK_ML_PIPELINE_ORCHESTRATION"
SCHEMA = "ML"
ROLE = "COOKBOOK_ML_PIPELINE_ORCHESTRATION_ADMIN"
WAREHOUSE = "COOKBOOK_ML_PIPELINE_ORCHESTRATION_WH"
STAGE = "PIPELINE_STAGE"

DAG_NAME = "ML_PIPELINE_DAG"
SCHEDULE = timedelta(days=7)  # retrain weekly; a Cron("0 6 * * 1", "UTC") also works
PROC_PREFIX = "ML_PIPELINE"
STEPS = ["feature_engineering", "train_model", "evaluate_model"]

PIPELINE_CONFIG = {
    "source_table": f"{DATABASE}.{SCHEMA}.LOAN_APPLICATIONS",
    "feature_table": f"{DATABASE}.{SCHEMA}.LOAN_FEATURES",
    "test_pct": "20",
    "model_name": "LOAN_DEFAULT_PIPELINE",
    "metrics_table": f"{DATABASE}.{SCHEMA}.ML_PIPELINE_METRICS",
    "auc_threshold": "0.75",  # quality gate for promoting a new version
}

# %% [markdown]
# ## Step 1: Connect to Snowflake
#
# Inside a Snowflake Notebook the active session is reused. Locally, `Session.builder.getOrCreate()`
# reads your connection from `~/.snowflake/connections.toml` (set `SNOWFLAKE_DEFAULT_CONNECTION_NAME`
# to choose one). No credentials live in the notebook. The session then switches to the recipe role,
# warehouse, and schema, so the procedures and tasks are owned by the recipe role and the tasks run
# as it.

# %%
try:
    from snowflake.snowpark.context import get_active_session

    session = get_active_session()
except Exception:
    session = Session.builder.getOrCreate()

session.use_role(ROLE)
session.use_warehouse(WAREHOUSE)
session.use_schema(f"{DATABASE}.{SCHEMA}")
schema_ref = Root(session).databases[DATABASE].schemas[SCHEMA]
print(session.sql("SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_SCHEMA()").collect()[0])

# %% [markdown]
# ## Step 2: How the Pipeline Works
#
# ```
#                  task graph config  (source_table, model_name, auc_threshold, ...)
#                          |  read by every task at run time
#                          v
#  ML_PIPELINE_DAG   +---------------------+     +---------------+     +------------------+
#  (root, weekly) -> | FEATURE_ENGINEERING | --> |  TRAIN_MODEL  | --> |  EVALUATE_MODEL  |
#                    +---------------------+     +---------------+     +------------------+
#                      LOAN_APPLICATIONS           XGBoost on TRAIN      score TEST split
#                      -> LOAN_FEATURES            -> Model Registry     metrics -> registry
#                         (+ TRAIN/TEST split)     returns version  ---> + ML_PIPELINE_METRICS
#                                                                        AUC >= threshold?
#                                                                          -> set as default
# ```
#
# Each task calls one stored procedure. The handlers live in
# [`src/pipeline_steps.py`](src/pipeline_steps.py):
#
# - **`feature_engineering`** derives payment and credit features and assigns a deterministic
#   TRAIN/TEST split by hashing `LOAN_ID`.
# - **`train_model`** fits XGBoost on the TRAIN split and logs a new timestamped version to the
#   registry. Its return value is the version name.
# - **`evaluate_model`** reads that version name from its predecessor, scores the TEST split in the
#   warehouse with `mv.run()`, records metrics, and promotes the version only if ROC AUC clears
#   `auc_threshold`.

# %%
Code("src/pipeline_steps.py", language="python")

# %% [markdown]
# ## Step 3: Register the Pipeline Steps as Stored Procedures
#
# `register_from_file` uploads `pipeline_steps.py` to the stage and creates one permanent procedure
# per handler. Two settings matter for tasks:
#
# - **`execute_as="caller"`**: the procedures run with caller's rights, and the caller is the task
#   owner (the recipe role). `TaskContext` then reads the graph config and sets return values in the
#   task's own session, and each procedure can do only what the recipe role can do.
# - **`packages`** must include `snowflake` (for `snowflake.core.task.context.TaskContext`) plus
#   everything the handlers import.

# %%
PACKAGES = [
    "snowflake-snowpark-python",
    "snowflake-ml-python",
    "snowflake",
    "xgboost",
    "scikit-learn",
]

for step in STEPS:
    session.sproc.register_from_file(
        "src/pipeline_steps.py",
        step,
        name=f"{PROC_PREFIX}_{step.upper()}",
        input_types=[],
        return_type=None,
        packages=PACKAGES,
        is_permanent=True,
        stage_location=f"@{STAGE}/ml_pipeline",
        replace=True,
        execute_as="caller",
    )
    print(f"Registered {PROC_PREFIX}_{step.upper()}")

# %% [markdown]
# ## Step 4: Define and Deploy the Task Graph
#
# The `DAG` context manager defines the root task: its schedule, warehouse, and config. Each
# `DAGTask` becomes a child task named `<DAG_NAME>$<TASK_NAME>`, and `>>` sets the dependencies.
# `DAGOperation.deploy` creates or replaces every task and resumes the graph, so the schedule is
# live as soon as this cell runs.

# %%
with DAG(
    DAG_NAME,
    schedule=SCHEDULE,
    warehouse=WAREHOUSE,
    config=PIPELINE_CONFIG,
    stage_location=f"@{STAGE}/ml_pipeline",
    comment="Cookbook ml-pipeline-orchestration: weekly loan-default retraining",
) as dag:
    features = DAGTask("FEATURE_ENGINEERING", definition=f"CALL {PROC_PREFIX}_FEATURE_ENGINEERING()")
    train = DAGTask("TRAIN_MODEL", definition=f"CALL {PROC_PREFIX}_TRAIN_MODEL()")
    evaluate = DAGTask("EVALUATE_MODEL", definition=f"CALL {PROC_PREFIX}_EVALUATE_MODEL()")
    features >> train >> evaluate

dag_op = DAGOperation(schema_ref)
dag_op.deploy(dag, mode=CreateMode.or_replace)
print("Deployed tasks:", [f"{DAG_NAME}${t.name}" for t in dag.tasks])

# %% [markdown]
# ## Step 5: Trigger a Run and Wait for It
#
# You don't have to wait for the schedule. `dag_op.run(dag)` runs the graph once right away (it is
# the same as `EXECUTE TASK ML_PIPELINE_DAG`). The cell below polls `TASK_HISTORY` until every
# task in the run has finished. A full run takes two to three minutes on a MEDIUM warehouse.

# %%
HISTORY_SQL = f"""
    SELECT name, state, return_value, error_message,
           DATEDIFF('second', query_start_time, completed_time) AS seconds,
           graph_run_group_id
    FROM TABLE({DATABASE}.INFORMATION_SCHEMA.TASK_HISTORY(
        SCHEDULED_TIME_RANGE_START => DATEADD('hour', -1, CURRENT_TIMESTAMP())))
    WHERE graph_run_group_id = ? AND name LIKE '{DAG_NAME}%'
    ORDER BY scheduled_time
"""

def latest_run_group_id():
    rows = session.sql(
        f"SELECT graph_run_group_id FROM TABLE({DATABASE}.INFORMATION_SCHEMA.TASK_HISTORY("
        f"TASK_NAME => '{DAG_NAME}', SCHEDULED_TIME_RANGE_START => "
        f"DATEADD('hour', -1, CURRENT_TIMESTAMP()))) "
        f"WHERE state <> 'SCHEDULED' ORDER BY scheduled_time DESC LIMIT 1"
    ).collect()
    return rows[0][0] if rows else None

# %%
previous_run = latest_run_group_id()
dag_op.run(dag)

# Wait for the new run to appear, then for all three child tasks to finish.
run_id = previous_run
while run_id == previous_run:
    time.sleep(5)
    run_id = latest_run_group_id()

while True:
    runs = session.sql(HISTORY_SQL, params=[run_id]).to_pandas()
    children = runs[runs["NAME"] != DAG_NAME]
    done = children["STATE"].isin(["SUCCEEDED", "FAILED", "CANCELLED", "SKIPPED"])
    if len(children) == len(STEPS) and done.all() or (runs["STATE"] == "FAILED").any():
        break
    time.sleep(15)

runs[["NAME", "STATE", "SECONDS", "RETURN_VALUE", "ERROR_MESSAGE"]]

# %% [markdown]
# Each task's `RETURN_VALUE` is what it passed to `set_return_value`. `TRAIN_MODEL` returned the
# new version name, and `EVALUATE_MODEL` picked it up with
# `get_predecessor_return_value("TRAIN_MODEL")`. You can also follow runs in Snowsight under
# **Transformation » Tasks**, or open the task graph view from the root task.

# %% [markdown]
# ## Step 6: Inspect the Results
#
# Every run appends one row to the metrics table, so you get a history of model quality across
# retrains. The registry stores the same metrics on each version, and it marks the promoted version
# as the default.

# %%
session.table(PIPELINE_CONFIG["metrics_table"]).sort("EVALUATED_AT", ascending=False).limit(5).to_pandas().round(4)

# %%
registry = Registry(session=session, database_name=DATABASE, schema_name=SCHEMA)
model = registry.get_model(PIPELINE_CONFIG["model_name"])
print("Default version:", model.default.version_name)
model.show_versions()[["name", "created_on", "is_default_version", "comment"]]

# %% [markdown]
# Downstream consumers can always score with the **default** version. When the gate rejects a
# retrain, they keep using the last good model, and nothing else needs to change.

# %%
sample = session.table(PIPELINE_CONFIG["feature_table"]).filter("SPLIT = 'TEST'").limit(5)
model.default.run(sample, function_name="predict_proba").select(
    "LOAN_ID", "IS_DEFAULT", '"output_feature_1"'
).with_column_renamed('"output_feature_1"', "DEFAULT_PROBABILITY").to_pandas().round(4)

# %% [markdown]
# ## Step 7: Change Behavior with Config Only
#
# Because the tasks read their settings from the graph config, you can change the pipeline with a
# single `ALTER TASK`, with no code changes and no redeploy. Here the quality gate is raised to an
# unreachable AUC. The next run still registers a new version, but it does **not** promote it.
#
# The root task must be suspended to alter it.

# %%
strict_config = {**PIPELINE_CONFIG, "auc_threshold": "0.99"}
session.sql(f"ALTER TASK {DAG_NAME} SUSPEND").collect()
session.sql(f"ALTER TASK {DAG_NAME} SET CONFIG = $${json.dumps(strict_config)}$$").collect()
session.sql(f"ALTER TASK {DAG_NAME} RESUME").collect()

previous_run = run_id
session.sql(f"EXECUTE TASK {DAG_NAME}").collect()
while run_id == previous_run:
    time.sleep(5)
    run_id = latest_run_group_id()
while True:
    runs = session.sql(HISTORY_SQL, params=[run_id]).to_pandas()
    evaluated = runs[runs["NAME"] == f"{DAG_NAME}$EVALUATE_MODEL"]
    if not evaluated.empty and evaluated["STATE"].iloc[0] != "EXECUTING" or (runs["STATE"] == "FAILED").any():
        break
    time.sleep(15)

print(json.loads(evaluated["RETURN_VALUE"].iloc[0]))
print(
    "Default version is still:",
    registry.get_model(PIPELINE_CONFIG["model_name"]).default.version_name,
)

# %%
# Restore the original quality gate.
session.sql(f"ALTER TASK {DAG_NAME} SUSPEND").collect()
session.sql(f"ALTER TASK {DAG_NAME} SET CONFIG = $${json.dumps(PIPELINE_CONFIG)}$$").collect()
session.sql(f"ALTER TASK {DAG_NAME} RESUME").collect()
print(f"Restored auc_threshold={PIPELINE_CONFIG['auc_threshold']}")

# %% [markdown]
# ## Step 8: Manage the Schedule
#
# The graph is now resumed on its weekly schedule. Suspend the root task to pause all future runs.
# Child tasks only run when the root triggers them, so you only need to suspend the root.

# %%
session.sql(f"ALTER TASK {DAG_NAME} SUSPEND").collect()
session.sql(f"SHOW TASKS LIKE '{DAG_NAME}%' IN SCHEMA {DATABASE}.{SCHEMA}").select(
    '"name"', '"state"', '"schedule"', '"predecessors"'
).to_pandas()

# %% [markdown]
# ## Key Takeaways
#
# - **One DAG, plain Python.** `DAG` / `DAGTask` / `>>` define the graph in code, and
#   `DAGOperation.deploy` creates every task in a single call.
# - **Stored procedures are the unit of work.** Each step is a versioned, permanent procedure, so
#   you can test it on its own with `CALL` and reuse it across graphs.
# - **Config makes the graph reusable.** Inputs, model names, and thresholds come from the task
#   graph config, so changing them is an `ALTER TASK ... SET CONFIG`, not a redeploy.
# - **Return values connect the steps.** Small results (a version name, a metrics summary) pass
#   between tasks, and they are recorded in `TASK_HISTORY` for monitoring.
# - **Gate promotion on quality.** Every run is registered, but only versions that clear the bar
#   become the default that consumers use.
# - **Caller's rights keep the procedures scoped.** They run as the task owner and can do only what
#   that role can do.
#
# ## Next Steps
#
# - Swap `TRAIN_MODEL` for an ML Job (see [Distributed training](../../distributed-training/README.md) or
#   [Hyperparameter tuning](../../hyperparameter-tuning/README.md)) when training outgrows a warehouse.
# - Add a finalizer task (`DAG(..., finalizer=...)`) that sends a notification with the run outcome.
# - Replace the full feature rebuild with a Dynamic Table, or trigger the DAG from a stream when new
#   data lands (`DAG(..., schedule=None)` with a `WHEN SYSTEM$STREAM_HAS_DATA(...)` condition).

# %% [markdown]
# ## Cleanup
#
# The task graph, procedures, tables, and model all live in the recipe database. Run
# `sql/99_teardown.sql` as described in the README: it drops the
# database, warehouse, and role.
```

### `notebooks/requirements.txt`

```
# Notebook (notebooks/01_ml_pipeline_orchestration.ipynb), run locally. The procedures run in
# the warehouse with Snowflake Anaconda packages, declared in the notebook's PACKAGES list.
snowflake-ml-python==2.5.0
snowflake-snowpark-python==1.55.1
snowflake==1.14.0
pandas==2.3.3
ipython==9.17.1
```

### `notebooks/src/__init__.py`

Copy code

### `notebooks/src/pipeline_steps.py`

Copy code

```
"""Stored procedure handlers for the ML pipeline task graph.

Each function is registered as a permanent Python stored procedure and called by
one task in the DAG:

    FEATURE_ENGINEERING  ->  TRAIN_MODEL  ->  EVALUATE_MODEL

Runtime parameters (table names, model name, quality threshold) come from the task
graph config, so the same DAG can be pointed at different inputs without
redeploying. Each step passes a small result to the next step through task return
values. The return values are also recorded in TASK_HISTORY for monitoring.
"""

import json
from datetime import UTC, datetime

from snowflake.core.task.context import TaskContext
from snowflake.snowpark import Session
from snowflake.snowpark import functions as F

LABEL_COL = "IS_DEFAULT"
ID_COL = "LOAN_ID"

def _config(ctx: TaskContext, key: str) -> str:
    return ctx.get_task_graph_config_property(key)

def feature_engineering(session: Session) -> str:
    """Build a model-ready feature table with a deterministic train/test split."""
    ctx = TaskContext(session)
    source = _config(ctx, "source_table")
    target = _config(ctx, "feature_table")
    test_pct = int(_config(ctx, "test_pct"))

    df = session.table(source)
    monthly_rate = F.col("INTEREST_RATE") / F.lit(1200)
    # Amortized monthly payment for the loan.
    payment = (
        F.col("LOAN_AMOUNT") * monthly_rate / (F.lit(1) - F.pow(F.lit(1) + monthly_rate, -F.col("LOAN_TERM_MONTHS")))
    )
    features = df.select(
        F.col(ID_COL),
        *[c for c in df.columns if c not in (ID_COL, LABEL_COL)],
        payment.alias("MONTHLY_PAYMENT"),
        (payment / (F.col("ANNUAL_INCOME") / F.lit(12))).alias("PAYMENT_TO_INCOME"),
        (F.col("NUM_DELINQUENCIES") > 0).cast("INT").alias("HAS_DELINQUENCY"),
        (F.col("CREDIT_SCORE") * (F.lit(1) - F.col("CREDIT_UTILIZATION"))).alias("SCORE_X_HEADROOM"),
        F.iff(F.abs(F.hash(F.col(ID_COL))) % 100 < test_pct, F.lit("TEST"), F.lit("TRAIN")).alias("SPLIT"),
        F.col(LABEL_COL),
    )
    features.write.save_as_table(target, mode="overwrite")

    n_rows = session.table(target).count()
    ctx.set_return_value(json.dumps({"feature_table": target, "rows": n_rows}))
    return f"Wrote {n_rows} rows to {target}"

def train_model(session: Session) -> str:
    """Train an XGBoost classifier on the TRAIN split and log it to the registry."""
    import xgboost as xgb
    from snowflake.ml.registry import Registry

    ctx = TaskContext(session)
    feature_table = _config(ctx, "feature_table")
    model_name = _config(ctx, "model_name")

    train_pdf = session.table(feature_table).filter(F.col("SPLIT") == "TRAIN").to_pandas()
    feature_cols = [c for c in train_pdf.columns if c not in (ID_COL, LABEL_COL, "SPLIT")]

    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.08,
        subsample=0.8,
        colsample_bytree=0.8,
        tree_method="hist",
        n_jobs=-1,
    )
    model.fit(train_pdf[feature_cols], train_pdf[LABEL_COL])

    version_name = f"V_{datetime.now(UTC):%Y%m%d_%H%M%S}"
    mv = Registry(session=session).log_model(
        model,
        model_name=model_name,
        version_name=version_name,
        sample_input_data=train_pdf[feature_cols].head(100),
        comment=f"Trained by task graph run {ctx.get_current_task_graph_run_group_id()}",
        target_platforms=["WAREHOUSE"],
    )
    ctx.set_return_value(version_name)
    return f"Registered {mv.model_name} {mv.version_name} on {len(train_pdf)} rows"

def evaluate_model(session: Session) -> str:
    """Score the TEST split, record metrics, and promote the model if it passes."""
    from sklearn.metrics import accuracy_score, log_loss, roc_auc_score
    from snowflake.ml.registry import Registry

    ctx = TaskContext(session)
    feature_table = _config(ctx, "feature_table")
    model_name = _config(ctx, "model_name")
    metrics_table = _config(ctx, "metrics_table")
    auc_threshold = float(_config(ctx, "auc_threshold"))
    version_name = ctx.get_predecessor_return_value("TRAIN_MODEL")

    model = Registry(session=session).get_model(model_name)
    mv = model.version(version_name)
    test_df = session.table(feature_table).filter(F.col("SPLIT") == "TEST")
    scored = mv.run(test_df, function_name="predict_proba").select(
        LABEL_COL, F.col('"output_feature_1"').alias("SCORE")
    )
    pdf = scored.to_pandas()

    auc = float(roc_auc_score(pdf[LABEL_COL], pdf["SCORE"]))
    metrics = {
        "roc_auc": auc,
        "log_loss": float(log_loss(pdf[LABEL_COL], pdf["SCORE"])),
        "accuracy": float(accuracy_score(pdf[LABEL_COL], pdf["SCORE"] >= 0.5)),
    }
    passed = auc >= auc_threshold
    for k, v in metrics.items():
        mv.set_metric(k, v)
    if passed:
        model.default = version_name

    session.create_dataframe(
        [
            [
                ctx.get_current_task_graph_run_group_id(),
                model_name,
                version_name,
                len(pdf),
                metrics["roc_auc"],
                metrics["log_loss"],
                metrics["accuracy"],
                auc_threshold,
                passed,
            ]
        ],
        schema=[
            "RUN_GROUP_ID",
            "MODEL_NAME",
            "VERSION_NAME",
            "N_TEST_ROWS",
            "ROC_AUC",
            "LOG_LOSS",
            "ACCURACY",
            "AUC_THRESHOLD",
            "PROMOTED",
        ],
    ).with_column("EVALUATED_AT", F.current_timestamp()).write.save_as_table(metrics_table, mode="append")

    result = {
        "version": version_name,
        "promoted": passed,
        **{k: round(v, 4) for k, v in metrics.items()},
    }
    ctx.set_return_value(json.dumps(result))
    return json.dumps(result)
```

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- =============================================================================
-- 01_setup.sql
-- ML pipeline orchestration: role, warehouse, database, schema, stage.
--
-- The first block runs as ACCOUNTADMIN and only creates or grants to this
-- recipe's own COOKBOOK_ objects:
--   COOKBOOK_ML_PIPELINE_ORCHESTRATION_ADMIN  owns the database, the
--     procedures, and the task graph, and is the role the tasks run as
-- The role is granted to the user running this script. Everything after the
-- first block runs as that role.
--
-- Account-level grant: EXECUTE TASK ON ACCOUNT to the recipe role, which a
-- task owner needs before its tasks can run. Dropping the role in
-- 99_teardown.sql removes it.
--
-- Idempotent.
-- =============================================================================

SET cookbook_db   = 'COOKBOOK_ML_PIPELINE_ORCHESTRATION';
SET cookbook_wh   = 'COOKBOOK_ML_PIPELINE_ORCHESTRATION_WH';
SET cookbook_role = 'COOKBOOK_ML_PIPELINE_ORCHESTRATION_ADMIN';
SET me            = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($cookbook_role)
  COMMENT = 'Cookbook ml-pipeline-orchestration: owns the data, procedures, task graph, and model.';
-- Granting the role to SYSADMIN lets ACCOUNTADMIN, which inherits SYSADMIN,
-- drop what it owns in 99_teardown.sql without relying on secondary roles.
GRANT ROLE IDENTIFIER($cookbook_role) TO ROLE SYSADMIN;
GRANT ROLE IDENTIFIER($cookbook_role) TO USER IDENTIFIER($me);

-- The tasks run their procedures on this warehouse: feature engineering,
-- XGBoost training in a Python procedure, and warehouse inference.
CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = MEDIUM AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cookbook ml-pipeline-orchestration';
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($cookbook_role);

-- The task owner needs EXECUTE TASK to run (and EXECUTE) its tasks.
GRANT EXECUTE TASK ON ACCOUNT TO ROLE IDENTIFIER($cookbook_role);

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db)
  COMMENT = 'Cookbook ml-pipeline-orchestration';
-- Owning the database covers CREATE TABLE, STAGE, PROCEDURE, TASK, and MODEL
-- on its schemas.
GRANT OWNERSHIP ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($cookbook_role) COPY CURRENT GRANTS;

-- ---------------------------------------------------------------------------
-- From here on, run as the recipe role.
-- ---------------------------------------------------------------------------
USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
CREATE SCHEMA IF NOT EXISTS ML
  COMMENT = 'Loan data, features, pipeline procedures and tasks, the model, and run metrics';
CREATE STAGE IF NOT EXISTS ML.PIPELINE_STAGE
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  COMMENT = 'Procedure handler code and task graph artifacts';

SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE();
```

### `sql/02_data.sql`

Copy code

```
-- =============================================================================
-- 02_data.sql
-- Synthetic loan-default data: 1M rows, 18 numeric features, label IS_DEFAULT.
--
-- Generated entirely in Snowflake with GENERATOR, so nothing leaves the account.
-- Categorical fields are integer-encoded so XGBoost can use them directly. The
-- label is drawn from a logistic function of the features plus noise, which
-- gives a learnable signal and a default rate of roughly 15 to 20 percent.
--
-- Runs as the recipe role. Idempotent (CREATE OR REPLACE).
-- =============================================================================

SET cookbook_db   = 'COOKBOOK_ML_PIPELINE_ORCHESTRATION';
SET cookbook_wh   = 'COOKBOOK_ML_PIPELINE_ORCHESTRATION_WH';
SET cookbook_role = 'COOKBOOK_ML_PIPELINE_ORCHESTRATION_ADMIN';

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA ML;

CREATE OR REPLACE TABLE LOAN_APPLICATIONS
  COMMENT = 'Synthetic loan applications with a binary IS_DEFAULT label'
AS
WITH base AS (
  SELECT
    SEQ8()                                                              AS LOAN_ID,
    UNIFORM(21, 75, RANDOM(1))::INT                                     AS AGE,
    ROUND(EXP(NORMAL(11, 0.5, RANDOM(2))), 0)                           AS ANNUAL_INCOME,
    ROUND(UNIFORM(1000, 50000, RANDOM(3))::FLOAT, 0)                    AS LOAN_AMOUNT,
    CASE UNIFORM(0, 2, RANDOM(4)) WHEN 0 THEN 12 WHEN 1 THEN 36 ELSE 60 END AS LOAN_TERM_MONTHS,
    ROUND(UNIFORM(3::FLOAT, 25::FLOAT, RANDOM(5)), 2)                   AS INTEREST_RATE,
    LEAST(850, GREATEST(300, ROUND(NORMAL(680, 70, RANDOM(6)), 0)))::INT AS CREDIT_SCORE,
    ROUND(UNIFORM(0::FLOAT, 0.6::FLOAT, RANDOM(7)), 3)                  AS DEBT_TO_INCOME,
    UNIFORM(0, 40, RANDOM(8))::INT                                      AS EMPLOYMENT_YEARS,
    UNIFORM(1, 30, RANDOM(9))::INT                                      AS NUM_CREDIT_LINES,
    IFF(UNIFORM(0, 100, RANDOM(10)) < 80, 0, UNIFORM(1, 6, RANDOM(11)))::INT AS NUM_DELINQUENCIES,
    UNIFORM(0, 8, RANDOM(12))::INT                                      AS NUM_INQUIRIES_6M,
    ROUND(UNIFORM(0::FLOAT, 1::FLOAT, RANDOM(13)), 3)                   AS CREDIT_UTILIZATION,
    UNIFORM(0, 2, RANDOM(14))::INT                                      AS HOME_OWNERSHIP,
    UNIFORM(0, 5, RANDOM(15))::INT                                      AS LOAN_PURPOSE,
    IFF(UNIFORM(0, 100, RANDOM(16)) < 15, 1, 0)                         AS HAS_COSIGNER,
    UNIFORM(0, 120, RANDOM(17))::INT                                    AS MONTHS_SINCE_LAST_DELINQ,
    ROUND(EXP(NORMAL(8.5, 1.2, RANDOM(18))), 0)                         AS SAVINGS_BALANCE,
    UNIFORM(0::FLOAT, 1::FLOAT, RANDOM(19))                             AS _U
  FROM TABLE(GENERATOR(ROWCOUNT => 1000000))
),
scored AS (
  SELECT
    *,
    ROUND(LOAN_AMOUNT / ANNUAL_INCOME, 4) AS LOAN_TO_INCOME,
    -2.9
    + (-0.012) * (CREDIT_SCORE - 680)
    + 3.0 * (DEBT_TO_INCOME - 0.3)
    + 1.6 * (LOAN_AMOUNT / ANNUAL_INCOME - 0.25)
    + 0.08 * (INTEREST_RATE - 14)
    + 0.35 * NUM_DELINQUENCIES
    + 0.12 * NUM_INQUIRIES_6M
    + 1.2 * POWER(CREDIT_UTILIZATION - 0.3, 2) * SIGN(CREDIT_UTILIZATION - 0.3)
    + (-0.03) * LEAST(EMPLOYMENT_YEARS, 15)
    + (-0.5) * HAS_COSIGNER
    + IFF(HOME_OWNERSHIP = 2, -0.3, 0)
    + IFF(LOAN_PURPOSE = 4, 0.4, 0)
    + IFF(AGE < 25, 0.3, 0)
    + IFF(LOAN_TERM_MONTHS = 60, 0.25, 0)
    + (-0.15) * LN(1 + SAVINGS_BALANCE / 10000)
    + NORMAL(0, 0.5, RANDOM(20)) AS _LOGIT
  FROM base
)
SELECT
  LOAN_ID, AGE, ANNUAL_INCOME, LOAN_AMOUNT, LOAN_TERM_MONTHS, INTEREST_RATE,
  CREDIT_SCORE, DEBT_TO_INCOME, EMPLOYMENT_YEARS, NUM_CREDIT_LINES,
  NUM_DELINQUENCIES, NUM_INQUIRIES_6M, CREDIT_UTILIZATION, HOME_OWNERSHIP,
  LOAN_PURPOSE, HAS_COSIGNER, MONTHS_SINCE_LAST_DELINQ, SAVINGS_BALANCE,
  LOAN_TO_INCOME,
  IFF(_U < 1 / (1 + EXP(-_LOGIT)), 1, 0) AS IS_DEFAULT
FROM scored;

-- Expect 1,000,000 rows and a default rate between 0.15 and 0.20.
SELECT COUNT(*) AS n_rows, ROUND(AVG(IS_DEFAULT), 4) AS default_rate
FROM LOAN_APPLICATIONS;
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- 99_teardown.sql
-- Removes everything this recipe created.
--
-- Dropping the database removes the task graph (so no further scheduled runs),
-- the procedures, the stage, the source, feature,
-- and metrics tables, and the registered model and its versions. Then the
-- warehouse and the role are dropped, which also removes the role's grants,
-- including EXECUTE TASK ON ACCOUNT. There are no account parameters to restore.
--
-- Run as ACCOUNTADMIN. Safe to rerun.
-- =============================================================================

SET cookbook_db   = 'COOKBOOK_ML_PIPELINE_ORCHESTRATION';
SET cookbook_wh   = 'COOKBOOK_ML_PIPELINE_ORCHESTRATION_WH';
SET cookbook_role = 'COOKBOOK_ML_PIPELINE_ORCHESTRATION_ADMIN';

USE ROLE ACCOUNTADMIN;
DROP DATABASE IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);
DROP ROLE IF EXISTS IDENTIFIER($cookbook_role);

-- Each of these should return no rows.
SHOW DATABASES LIKE 'COOKBOOK_ML_PIPELINE_ORCHESTRATION%';
SHOW WAREHOUSES LIKE 'COOKBOOK_ML_PIPELINE_ORCHESTRATION%';
SHOW ROLES LIKE 'COOKBOOK_ML_PIPELINE_ORCHESTRATION%';
```
