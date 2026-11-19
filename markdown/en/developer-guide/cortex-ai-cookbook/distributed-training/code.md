# Distributed training as a multi-node ML Job: code

Every file in the [Distributed training as a multi-node ML Job](/developer-guide/cortex-ai-cookbook/distributed-training) recipe. To run the recipe, download [distributed-training.zip](/static/samples/cortex-ai-cookbook/distributed-training.zip), unzip it, and run the scripts from the `distributed-training/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/distributed-training); the zip includes it as `README.md`.

## `notebooks/`

### `notebooks/01_distributed_training.ipynb`

Jupyter notebook, shown as Python with Markdown cells as comments.

Copy code

```
# %% [markdown]
# # Distributed XGBoost training with Snowflake ML Jobs
#
# Train a gradient-boosted classifier across **multiple nodes** of a Snowpark Container Services
# compute pool using Snowflake's distributed `XGBEstimator`. You launch the run from this notebook
# as a **Snowflake ML Job**. Snowflake provisions a multi-node Ray cluster on the compute pool,
# shards the training data across the nodes, and trains one XGBoost model collectively. The finished
# model is logged to the **Model Registry** and used for batch inference from a warehouse.
#
# Before you run it:
#
# 1. Run `sql/01_setup.sql` and `sql/02_data.sql` as described in the recipe README. They create the
#    role, warehouse, compute pool, database, stage, and the `LOAN_APPLICATIONS` table.
# 2. Run the notebook locally (Jupyter or VS Code) after `pip install -r requirements.txt`, with a
#    Snowflake connection for your own user (for example
#    `SNOWFLAKE_DEFAULT_CONNECTION_NAME=<your connection>`). It can also run as a Snowflake Notebook
#    in a Workspace, where it reuses the active session.
#
# The notebook switches to the recipe role, so it needs nothing beyond what `sql/01` granted.

# %%
from datetime import datetime

import matplotlib.pyplot as plt
from IPython.display import Code
from sklearn.metrics import roc_auc_score
from snowflake.ml import jobs
from snowflake.ml.registry import Registry
from snowflake.snowpark import Session
from src.helpers import (
    key_log_lines,
    metrics_frame,
    plot_feature_importance,
    plot_lift_by_decile,
)

# %% [markdown]
# ## Configuration
#
# Object names match `sql/01_setup.sql` and are fixed. `TARGET_INSTANCES` sets the number of
# compute pool nodes the job spans (one head node plus `TARGET_INSTANCES - 1` workers); keep it at
# or below the pool's `MAX_NODES` (3). The hyperparameters are safe to change.

# %%
DATABASE = "COOKBOOK_DISTRIBUTED_TRAINING"
SCHEMA = "ML"
ROLE = "COOKBOOK_DISTRIBUTED_TRAINING_ADMIN"
WAREHOUSE = "COOKBOOK_DISTRIBUTED_TRAINING_WH"
COMPUTE_POOL = "COOKBOOK_DISTRIBUTED_TRAINING_POOL"
STAGE = "JOBS_STAGE"

SOURCE_TABLE = f"{DATABASE}.{SCHEMA}.LOAN_APPLICATIONS"
LABEL_COL = "IS_DEFAULT"
ID_COL = "LOAN_ID"
TEST_PCT = 20  # deterministic hash split: about 20% of rows held out

MODEL_NAME = "LOAN_DEFAULT_XGB_DISTRIBUTED"
VERSION_NAME = f"V_{datetime.now():%Y%m%d_%H%M%S}"

TARGET_INSTANCES = 2
HYPERPARAMS = {"n-estimators": 150, "max-depth": 6, "learning-rate": 0.1}

# %% [markdown]
# ## Step 1: Connect to Snowflake
#
# Inside a Snowflake Notebook the active session is reused. Locally, `Session.builder.getOrCreate()`
# reads your connection from `~/.snowflake/connections.toml` (set `SNOWFLAKE_DEFAULT_CONNECTION_NAME`
# to choose one). No credentials live in the notebook. The session then switches to the recipe role,
# warehouse, and schema.

# %%
try:
    from snowflake.snowpark.context import get_active_session

    session = get_active_session()
except Exception:
    session = Session.builder.getOrCreate()

session.use_role(ROLE)
session.use_warehouse(WAREHOUSE)
session.use_schema(f"{DATABASE}.{SCHEMA}")
print(session.sql("SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_SCHEMA()").collect()[0])

# %% [markdown]
# ## Step 2: Explore the Training Data
#
# `LOAN_APPLICATIONS` holds 1M synthetic loan applications with 18 numeric features and a binary
# `IS_DEFAULT` label. Rows are split by a hash of `LOAN_ID`, so the training job and this notebook
# always agree on which rows are in the hold-out set.

# %%
session.sql(f"""
    SELECT
        IFF(MOD(ABS(HASH({ID_COL})), 100) < {TEST_PCT}, 'TEST', 'TRAIN') AS SPLIT,
        COUNT(*) AS N_ROWS,
        ROUND(AVG({LABEL_COL}), 4) AS DEFAULT_RATE
    FROM {SOURCE_TABLE}
    GROUP BY 1
    ORDER BY 1 DESC
""").to_pandas()

# %% [markdown]
# ## Step 3: How Distributed Training Works
#
# ```
#  This notebook                         Recipe compute pool (Container Runtime)  
# +--------------+   submit_file()     +-------------------------------------------+
# | job config   | ------------------> |  Head node (rank 0)      Worker node(s)   |
# | + script     |                     |  +----------------+    +----------------+ |
# +--------------+                     |  | Ray head       |<-->| Ray worker     | |
#        ^                             |  | XGB worker 0   |    | XGB worker 1   | |
#        |  job.result()               |  +-------+--------+    +--------+-------+ |
#        +---------------------------- |          |  DataConnector shards |         |
#                                      +----------+-----------------------+---------+
#                                                 v                       v
#                                           Snowflake table: LOAN_APPLICATIONS
# ```
#
# 1. `submit_file()` uploads the script to `JOBS_STAGE` and starts `TARGET_INSTANCES` containers
#    on the compute pool. Together they form one Ray cluster.
# 2. Inside the job, `DataConnector.from_dataframe()` reads the table in parallel.
# 3. `XGBEstimator.fit()` starts one XGBoost worker per node. Each worker trains on its data shard,
#    and the workers sync histogram statistics every boosting round (XGBoost's Rabit/collective
#    protocol). The result is a single model trained on all of the data.
# 4. The head node evaluates the booster, logs it to the Model Registry, and returns a summary dict
#    through `__return__`.
#
# **When to use it:** data that doesn't fit in one node's memory, or boosting runs that are too slow on a single node. For small data,
# plain open-source `xgboost` on one node is simpler and often faster, because coordinating the
# nodes adds overhead.
#
# The full training script is shown below.

# %%
Code("src/train_xgb_distributed.py", language="python")

# %% [markdown]
# ## Step 4: Submit the ML Job
#
# Key `submit_file` arguments:
#
# | Argument | Purpose |
# |----------|---------|
# | `compute_pool` | SPCS pool that runs the job |
# | `stage_name` | Where the payload (script and runtime files) is uploaded |
# | `args` | Command-line arguments passed to the script |
# | `target_instances` | Number of nodes in the job's Ray cluster |
#
# The call returns immediately with an `MLJob` handle. The job runs asynchronously on Snowflake,
# so you can close this notebook and reattach later with `jobs.get_job(job_id)`.

# %%
script_args = [
    "--table",
    SOURCE_TABLE,
    "--model-name",
    MODEL_NAME,
    "--version-name",
    VERSION_NAME,
    "--test-pct",
    str(TEST_PCT),
]
for k, v in HYPERPARAMS.items():
    script_args += [f"--{k}", str(v)]

job = jobs.submit_file(
    "src/train_xgb_distributed.py",
    COMPUTE_POOL,
    stage_name=STAGE,
    args=script_args,
    target_instances=TARGET_INSTANCES,
    session=session,
)
print(f"Submitted job: {job.id}")
print(f"Status: {job.status}")

# %% [markdown]
# ## Step 5: Monitor the Job
#
# `job.wait()` blocks until the job finishes. While it runs, you can check it with `job.status` and
# `job.get_logs()`, from this notebook or after reattaching with `jobs.get_job(job_id)`. The first run takes a few extra
# minutes while the compute pool starts its nodes.

# %%
final_status = job.wait()
print(f"Final status: {final_status}")
print(key_log_lines(job.get_logs()))

# %% [markdown]
# ## Step 6: Review the Results
#
# `job.result()` returns the dictionary that the script assigned to `__return__`. It includes the
# cluster size, training time, hold-out metrics, and per-feature gain.

# %%
result = job.result()
print(
    f"Nodes: {result['n_nodes']}  |  CPUs: {result['n_cpus']}  |  "
    f"Train rows: {result['n_train_rows']:,}  |  Test rows: {result['n_test_rows']:,}  |  "
    f"Training time: {result['train_seconds']}s"
)
metrics_frame(result["metrics"])

# %%
plot_feature_importance(result["feature_importance"])
plt.show()

# %% [markdown]
# The top features (`NUM_DELINQUENCIES`, `CREDIT_SCORE`, `LOAN_TO_INCOME`, `INTEREST_RATE`) are the
# main drivers built into the synthetic data generator (`sql/02_data.sql`), so the model has learned the real signal.
# Accuracy is only modestly above the majority-class baseline (one minus the default rate, about 82%). For an imbalanced risk problem
# like this one, **ROC AUC** and ranking quality are the better measures (see Step 8).

# %% [markdown]
# > **A note on scale:** this 1M-row dataset is deliberately small so the recipe runs quickly, and
# > it fits easily on one node. Here, single-node open-source XGBoost trains in seconds (see the
# > trial times in the [Hyperparameter tuning](../../hyperparameter-tuning/README.md) recipe), while the
# > distributed run spends most of its time on cross-node coordination. The workflow on this page
# > stays the same when the table grows to hundreds of millions of rows. At that point a single
# > node runs out of memory, and adding nodes is what makes training possible.

# %% [markdown]
# ## Step 7: Inspect the Model in the Registry
#
# The job logged the booster with its metrics, so every training run is versioned and auditable.

# %%
registry = Registry(session=session, database_name=DATABASE, schema_name=SCHEMA)
model = registry.get_model(MODEL_NAME)
mv = model.version(VERSION_NAME)
print(f"{model.name} versions: {[v.version_name for v in model.versions()]}")
print("Logged metrics:", {k: round(v, 4) for k, v in mv.show_metrics().items()})
mv.show_functions()[0]["name"]

# %% [markdown]
# ## Step 8: Batch Inference from a Warehouse
#
# `mv.run()` scores a Snowpark DataFrame inside the warehouse, so no data leaves Snowflake. Here we
# score the hold-out split and check two things: that predicted risk ranks borrowers correctly
# (lift) and that the predicted probabilities match observed default rates (calibration).

# %%
test_df = session.sql(f"SELECT * FROM {SOURCE_TABLE} WHERE MOD(ABS(HASH({ID_COL})), 100) < {TEST_PCT}")
scored = mv.run(test_df, function_name="predict")
scored_pdf = scored.select(ID_COL, LABEL_COL, '"output_feature_0"').to_pandas()
scored_pdf = scored_pdf.rename(columns={"output_feature_0": "DEFAULT_PROBABILITY"})

print(f"Scored {len(scored_pdf):,} rows in the warehouse")
print(f"Warehouse-scored ROC AUC: {roc_auc_score(scored_pdf[LABEL_COL], scored_pdf['DEFAULT_PROBABILITY']):.4f}")

# %%
fig, lift = plot_lift_by_decile(scored_pdf, "DEFAULT_PROBABILITY", LABEL_COL)
plt.show()
lift

# %% [markdown]
# In a typical run the highest-risk decile defaults far more often than the lowest (roughly 60% vs 1%), and the predicted
# and observed bars line up closely. The model is well calibrated and ready for thresholding
# (for example, routing the top deciles to manual review).
#
# You can also call the model directly from SQL:
#
# ```sql
# WITH mv AS MODEL COOKBOOK_DISTRIBUTED_TRAINING.ML.LOAN_DEFAULT_XGB_DISTRIBUTED VERSION <VERSION_NAME>
# SELECT LOAN_ID, mv!PREDICT(*):output_feature_0::FLOAT AS DEFAULT_PROBABILITY
# FROM COOKBOOK_DISTRIBUTED_TRAINING.ML.LOAN_APPLICATIONS
# LIMIT 10;
# ```

# %% [markdown]
# ## Key Takeaways
#
# - **ML Jobs separate where you write code from where it runs.** You develop anywhere, and the
#   work runs on a managed, multi-node Container Runtime close to your data.
# - **`XGBEstimator` is a drop-in for multi-node XGBoost.** You pass a `DataConnector`, the input
#   columns, and the label, and it handles sharding and worker coordination.
# - **`target_instances` is the scaling knob.** It sets the node count without changing your code.
# - **Register from inside the job.** The model is versioned with its metrics, and you don't need
#   to download artifacts.
# - **Use distributed training when the data or the training time justifies it.** On small data,
#   single-node training avoids the coordination overhead.
#
# ## Next Steps
#
# - [Hyperparameter tuning](../../hyperparameter-tuning/README.md): find better XGBoost parameters with parallel HPO
# - Raise the `GENERATOR` row count in `sql/02_data.sql` and raise `TARGET_INSTANCES` to see how training time scales
# - Set `XGBScalingConfig(use_gpu=True)` on a GPU compute pool for GPU-accelerated boosting

# %% [markdown]
# ## Cleanup
#
# The job service and the model live in the recipe database. Run `sql/99_teardown.sql` as described
# in the README to remove them together with the compute pool, warehouse, and role.
```

### `notebooks/requirements.txt`

```
# Notebook (notebooks/01_distributed_training.ipynb), run locally. The ML Job itself runs on
# the Snowflake Container Runtime, which already includes Ray and XGBoost.
snowflake-ml-python==2.5.0
snowflake-snowpark-python==1.55.1
pandas==2.3.3
scikit-learn==1.9.1
matplotlib==3.11.2
ipython==9.17.1
```

### `notebooks/src/__init__.py`

Copy code

### `notebooks/src/helpers.py`

Copy code

```
"""Notebook helpers for the distributed training recipe."""

import re

import matplotlib.pyplot as plt
import pandas as pd

LOG_PATTERN = re.compile(
    r"Ray cluster|Distributed training finished|Test metrics|Registered|"
    r"\[\d+\]\s+(train|valid|validation)"
)

def key_log_lines(logs: str, max_lines: int = 40) -> str:
    """Keep only the informative lines from an ML Job log."""
    lines = [line for line in logs.splitlines() if LOG_PATTERN.search(line)]
    return "\n".join(lines[-max_lines:])

def metrics_frame(metrics: dict) -> pd.DataFrame:
    """Format a metrics dict as a one-column table."""
    return pd.DataFrame.from_dict(metrics, orient="index", columns=["value"]).round(4)

def plot_feature_importance(importance: dict, top_n: int = 15, title: str = "Feature importance (gain)"):
    """Horizontal bar chart of the top-N features by XGBoost gain."""
    s = pd.Series(importance).sort_values().tail(top_n)
    fig, ax = plt.subplots(figsize=(8, 0.35 * len(s) + 1))
    s.plot.barh(ax=ax, color="#29B5E8")
    ax.set_title(title)
    ax.set_xlabel("Average gain")
    fig.tight_layout()
    return fig

def plot_lift_by_decile(df: pd.DataFrame, score_col: str, label_col: str):
    """Observed default rate per predicted-score decile (decile 10 = highest risk)."""
    d = df[[score_col, label_col]].copy()
    d["decile"] = pd.qcut(d[score_col].rank(method="first"), 10, labels=range(1, 11))
    summary = d.groupby("decile", observed=True).agg(
        predicted=(score_col, "mean"),
        observed=(label_col, "mean"),
        n=(label_col, "size"),
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    x = range(1, 11)
    ax.bar(
        [i - 0.2 for i in x],
        summary["observed"],
        width=0.4,
        label="Observed default rate",
        color="#11567F",
    )
    ax.bar(
        [i + 0.2 for i in x],
        summary["predicted"],
        width=0.4,
        label="Mean predicted probability",
        color="#29B5E8",
    )
    ax.set_xticks(list(x))
    ax.set_xlabel("Predicted risk decile")
    ax.set_ylabel("Rate")
    ax.set_title("Calibration and lift by decile")
    ax.legend()
    fig.tight_layout()
    return fig, summary.round(4)
```

### `notebooks/src/train_xgb_distributed.py`

Copy code

```
"""Distributed XGBoost training entrypoint for a Snowflake ML Job.

This script runs on the Snowflake Container Runtime across every node assigned to
the job (``target_instances``). It:

1. Reads train/test splits from a Snowflake table with ``DataConnector``.
2. Trains a binary classifier with Snowflake's distributed ``XGBEstimator``,
   which shards data and boosting work across all Ray workers in the cluster.
3. Evaluates the booster on the hold-out split.
4. Logs the model (with metrics) to the Snowflake Model Registry.

The dictionary assigned to ``__return__`` is returned to the caller by
``MLJob.result()``.
"""

import argparse
import re
import time

import numpy as np
import ray
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from snowflake.ml.data.data_connector import DataConnector
from snowflake.ml.modeling.distributors.xgboost import XGBEstimator, XGBScalingConfig
from snowflake.ml.registry import Registry
from snowflake.snowpark import Session

LABEL_COL = "IS_DEFAULT"
ID_COL = "LOAN_ID"
# --table is interpolated into SQL, so accept only an unquoted DB.SCHEMA.TABLE.
TABLE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*(\.[A-Za-z_][A-Za-z0-9_$]*){2}$")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Distributed XGBoost training")
    parser.add_argument("--table", required=True, help="Fully qualified source table")
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--version-name", required=True)
    parser.add_argument("--test-pct", type=int, default=20)
    parser.add_argument("--n-estimators", type=int, default=150)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--learning-rate", type=float, default=0.1)
    args = parser.parse_args()
    if not TABLE_NAME.match(args.table):
        parser.error("--table must be an unquoted DATABASE.SCHEMA.TABLE name")
    return args

def split_query(table: str, test: bool, test_pct: int) -> str:
    """Deterministic hash split so the notebook can rebuild the same test set."""
    op = "<" if test else ">="
    return f"SELECT * FROM {table} WHERE MOD(ABS(HASH({ID_COL})), 100) {op} {test_pct}"

def main() -> dict:
    args = parse_args()
    session = Session.builder.getOrCreate()

    resources = ray.cluster_resources()
    n_nodes = len([n for n in ray.nodes() if n["Alive"]])
    print(f"Ray cluster: {n_nodes} node(s), {int(resources.get('CPU', 0))} CPUs")

    train_df = session.sql(split_query(args.table, test=False, test_pct=args.test_pct))
    test_df = session.sql(split_query(args.table, test=True, test_pct=args.test_pct))
    feature_cols = [c for c in train_df.columns if c not in (LABEL_COL, ID_COL)]

    params = {
        "objective": "binary:logistic",
        "eval_metric": ["logloss", "auc"],
        "tree_method": "hist",
        "max_depth": args.max_depth,
        "eta": args.learning_rate,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
    }
    estimator = XGBEstimator(
        n_estimators=args.n_estimators,
        params=params,
        # Defaults to one worker per node using all of its CPUs.
        scaling_config=XGBScalingConfig(use_gpu=False),
    )

    start = time.time()
    booster = estimator.fit(
        DataConnector.from_dataframe(train_df),
        input_cols=feature_cols,
        label_col=LABEL_COL,
        eval_set=DataConnector.from_dataframe(test_df),
        verbose_eval=50,
    )
    train_seconds = round(time.time() - start, 1)
    print(f"Distributed training finished in {train_seconds}s")

    # Evaluate on the head node with the open-source booster.
    test_pdf = DataConnector.from_dataframe(test_df).to_pandas()
    y_true = test_pdf[LABEL_COL].to_numpy()
    y_prob = booster.predict(xgb.DMatrix(test_pdf[feature_cols]))
    y_pred = (y_prob >= 0.5).astype(int)
    metrics = {
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "log_loss": float(log_loss(y_true, y_prob)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred)),
        "recall": float(recall_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred)),
    }
    print("Test metrics:", {k: round(v, 4) for k, v in metrics.items()})

    # Log the booster to the Model Registry next to the source table, so it can be
    # served from SQL or Python.
    database, schema, _ = args.table.split(".")
    registry = Registry(session=session, database_name=database, schema_name=schema)
    mv = registry.log_model(
        booster,
        model_name=args.model_name,
        version_name=args.version_name,
        sample_input_data=test_pdf[feature_cols].head(100),
        metrics={**metrics, "train_seconds": train_seconds, "n_nodes": n_nodes},
        comment="Loan default classifier trained with distributed XGBEstimator",
        target_platforms=["WAREHOUSE"],
    )
    print(f"Registered {mv.model_name} version {mv.version_name}")

    importance = booster.get_score(importance_type="gain")
    return {
        "metrics": metrics,
        "train_seconds": train_seconds,
        "n_nodes": n_nodes,
        "n_cpus": int(resources.get("CPU", 0)),
        "n_train_rows": int(train_df.count()),
        "n_test_rows": len(test_pdf),
        "feature_importance": {k: float(v) for k, v in importance.items()},
        "positive_rate_test": float(np.mean(y_true)),
        "model_name": mv.model_name,
        "version_name": mv.version_name,
    }

if __name__ == "__main__":
    __return__ = main()
```

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- =============================================================================
-- 01_setup.sql
-- Distributed training: role, warehouse, compute pool, database, schema, stage.
--
-- The first block runs as ACCOUNTADMIN and only creates or grants to this
-- recipe's own COOKBOOK_ objects:
--   COOKBOOK_DISTRIBUTED_TRAINING_ADMIN  owns the database and runs the job
--   COOKBOOK_DISTRIBUTED_TRAINING_POOL   multi-node CPU pool for the ML Job
-- The role is granted to the user running this script. Everything after the
-- first block runs as that role.
--
-- Idempotent.
-- =============================================================================

SET cookbook_db   = 'COOKBOOK_DISTRIBUTED_TRAINING';
SET cookbook_wh   = 'COOKBOOK_DISTRIBUTED_TRAINING_WH';
SET cookbook_pool = 'COOKBOOK_DISTRIBUTED_TRAINING_POOL';
SET cookbook_role = 'COOKBOOK_DISTRIBUTED_TRAINING_ADMIN';
SET me            = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($cookbook_role)
  COMMENT = 'Cookbook distributed-training: owns the data, job payloads, and model.';
-- Granting the role to SYSADMIN lets ACCOUNTADMIN, which inherits SYSADMIN,
-- drop what it owns in 99_teardown.sql without relying on secondary roles.
GRANT ROLE IDENTIFIER($cookbook_role) TO ROLE SYSADMIN;
GRANT ROLE IDENTIFIER($cookbook_role) TO USER IDENTIFIER($me);

-- The warehouse runs the data generation, the job's SQL, and warehouse inference.
CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = MEDIUM AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cookbook distributed-training';
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($cookbook_role);

-- The ML Job runs on this pool. MAX_NODES must be at least the job's
-- target_instances (the notebook uses 2). Each CPU_X64_M node has 8 vCPU and
-- 32 GB. The pool bills per active node and suspends after 10 idle minutes.
CREATE COMPUTE POOL IF NOT EXISTS IDENTIFIER($cookbook_pool)
  MIN_NODES = 1
  MAX_NODES = 3
  INSTANCE_FAMILY = CPU_X64_M
  AUTO_RESUME = TRUE
  AUTO_SUSPEND_SECS = 600
  INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cookbook distributed-training: distributed XGBoost ML Job';
GRANT USAGE, MONITOR ON COMPUTE POOL IDENTIFIER($cookbook_pool) TO ROLE IDENTIFIER($cookbook_role);

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db)
  COMMENT = 'Cookbook distributed-training';
-- Owning the database covers CREATE TABLE, STAGE, SERVICE (the ML Job), and
-- MODEL on its schemas.
GRANT OWNERSHIP ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($cookbook_role) COPY CURRENT GRANTS;

-- ---------------------------------------------------------------------------
-- From here on, run as the recipe role.
-- ---------------------------------------------------------------------------
USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
CREATE SCHEMA IF NOT EXISTS ML
  COMMENT = 'Loan data, ML Job payloads, and the distributed model';
CREATE STAGE IF NOT EXISTS ML.JOBS_STAGE
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  COMMENT = 'ML Job payloads uploaded by submit_file';

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

SET cookbook_db   = 'COOKBOOK_DISTRIBUTED_TRAINING';
SET cookbook_wh   = 'COOKBOOK_DISTRIBUTED_TRAINING_WH';
SET cookbook_role = 'COOKBOOK_DISTRIBUTED_TRAINING_ADMIN';

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
-- Stopping the compute pool ends any ML Job still running on it. Dropping the
-- database removes the table, the job payload stage, the job services, and the
-- registered model and its versions. Then the warehouse and the role are
-- dropped, which also removes the role's grants.
-- There are no account parameters to restore.
--
-- Run as ACCOUNTADMIN. Safe to rerun.
-- =============================================================================

SET cookbook_db   = 'COOKBOOK_DISTRIBUTED_TRAINING';
SET cookbook_wh   = 'COOKBOOK_DISTRIBUTED_TRAINING_WH';
SET cookbook_pool = 'COOKBOOK_DISTRIBUTED_TRAINING_POOL';
SET cookbook_role = 'COOKBOOK_DISTRIBUTED_TRAINING_ADMIN';

USE ROLE ACCOUNTADMIN;
ALTER COMPUTE POOL IF EXISTS IDENTIFIER($cookbook_pool) STOP ALL;
DROP COMPUTE POOL IF EXISTS IDENTIFIER($cookbook_pool);
DROP DATABASE IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);
DROP ROLE IF EXISTS IDENTIFIER($cookbook_role);

-- Each of these should return no rows.
SHOW COMPUTE POOLS LIKE 'COOKBOOK_DISTRIBUTED_TRAINING%';
SHOW DATABASES LIKE 'COOKBOOK_DISTRIBUTED_TRAINING%';
SHOW WAREHOUSES LIKE 'COOKBOOK_DISTRIBUTED_TRAINING%';
SHOW ROLES LIKE 'COOKBOOK_DISTRIBUTED_TRAINING%';
```
