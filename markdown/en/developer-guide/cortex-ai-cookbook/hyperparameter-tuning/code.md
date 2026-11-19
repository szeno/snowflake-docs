# Parallel hyperparameter tuning as a multi-node ML Job: code

Every file in the [Parallel hyperparameter tuning as a multi-node ML Job](/developer-guide/cortex-ai-cookbook/hyperparameter-tuning) recipe. To run the recipe, download [hyperparameter-tuning.zip](/static/samples/cortex-ai-cookbook/hyperparameter-tuning.zip), unzip it, and run the scripts from the `hyperparameter-tuning/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/hyperparameter-tuning); the zip includes it as `README.md`.

## `notebooks/`

### `notebooks/01_hyperparameter_tuning.ipynb`

Jupyter notebook, shown as Python with Markdown cells as comments.

Copy code

```
# %% [markdown]
# # Parallel hyperparameter tuning with Snowflake ML Jobs
#
# Find better XGBoost hyperparameters by running many training trials **in parallel** across a
# multi-node compute pool. The search runs as a **Snowflake ML Job** using the Snowflake ML
# hyperparameter optimization API (`snowflake.ml.modeling.tune`). The job registers the best model
# in the **Model Registry**, and every trial is recorded in **Snowflake Experiment Tracking** so you
# can compare runs later.
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
import contextlib
import io
from datetime import datetime

import matplotlib.pyplot as plt
from IPython.display import Code
from snowflake.ml import jobs
from snowflake.ml.experiment import ExperimentTracking
from snowflake.ml.registry import Registry
from snowflake.snowpark import Session
from src.helpers import (
    key_log_lines,
    plot_param_effects,
    plot_search_progress,
    trials_frame,
)

# %% [markdown]
# ## Configuration
#
# Object names match `sql/01_setup.sql` and are fixed. The search settings control how many trials
# run in total and how many run at the same time; those are safe to change.

# %%
DATABASE = "COOKBOOK_HYPERPARAMETER_TUNING"
SCHEMA = "ML"
ROLE = "COOKBOOK_HYPERPARAMETER_TUNING_ADMIN"
WAREHOUSE = "COOKBOOK_HYPERPARAMETER_TUNING_WH"
COMPUTE_POOL = "COOKBOOK_HYPERPARAMETER_TUNING_POOL"
STAGE = "JOBS_STAGE"

SOURCE_TABLE = f"{DATABASE}.{SCHEMA}.LOAN_APPLICATIONS"
TEST_PCT = 20  # deterministic hash split: about 20% of rows held out

MODEL_NAME = "LOAN_DEFAULT_XGB_TUNED"
VERSION_NAME = f"V_{datetime.now():%Y%m%d_%H%M%S}"
EXPERIMENT_NAME = "LOAN_DEFAULT_HPO"

TARGET_INSTANCES = 2  # nodes in the job's Ray cluster (pool MAX_NODES is 3)
NUM_TRIALS = 24  # total hyperparameter configurations to evaluate
MAX_CONCURRENT_TRIALS = 3  # trials running at once on each node
THREADS_PER_TRIAL = 2  # XGBoost threads per trial

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
# ## Step 2: How Parallel HPO Works
#
# ```
#  This notebook              ML Job on the recipe compute pool (Ray, 2 nodes)  
# +-------------+  submit   +-------------------------------------------------------+
# | search cfg  | --------> |  Tuner (head node)                                    |
# | + script    |           |    | samples configs from SEARCH_SPACE (RandomSearch) |
# +-------------+           |    v                                                  |
#       ^                   |  Node 1: trial | trial | trial                        |
#       | job.result()      |  Node 2: trial | trial | trial    <- 6 at a time      |
#       +------------------ |    | each trial: fit XGBoost, report roc_auc          |
#                           |    v                                                  |
#                           |  best trial -> Model Registry                         |
#                           +-------------------------------------------------------+
# ```
#
# The building blocks of `snowflake.ml.modeling.tune`:
#
# | Component | Role in this notebook |
# |-----------|-----------------------|
# | `SEARCH_SPACE` | Distributions to sample from (`randint`, `uniform`, `loguniform`) |
# | `RandomSearch` | Search algorithm. Use `BayesOpt` for uniform-only spaces or `GridSearch` for exhaustive search. |
# | `TunerConfig` | Objective (`roc_auc`, `max`), `num_trials`, `max_concurrent_trials` per node |
# | `train_func` | Runs once per trial: gets params and data via `get_tuner_context()`, trains, then calls `report()` |
# | `Tuner.run(dataset_map=...)` | Schedules trials across the cluster and returns `TunerResults` (`results`, `best_result`, `best_model`) |
#
# **Sizing:** each `CPU_X64_M` node exposes 6 schedulable CPUs. That fits
# `MAX_CONCURRENT_TRIALS = 3` trials per node at `THREADS_PER_TRIAL = 2`, for 6 trials in parallel
# across 2 nodes. Raise `TARGET_INSTANCES` (up to the pool's `MAX_NODES` of 3) to finish the same search proportionally faster.
#
# The full job script is shown below.

# %%
Code("src/tune_xgb.py", language="python")

# %% [markdown]
# ## Step 3: Submit the HPO Job
#
# Search settings are passed to the script as command-line arguments, so you can change the
# budget without editing the script.

# %%
job = jobs.submit_file(
    "src/tune_xgb.py",
    COMPUTE_POOL,
    stage_name=STAGE,
    args=[
        "--table",
        SOURCE_TABLE,
        "--model-name",
        MODEL_NAME,
        "--version-name",
        VERSION_NAME,
        "--test-pct",
        str(TEST_PCT),
        "--num-trials",
        str(NUM_TRIALS),
        "--max-concurrent-trials",
        str(MAX_CONCURRENT_TRIALS),
        "--threads-per-trial",
        str(THREADS_PER_TRIAL),
    ],
    target_instances=TARGET_INSTANCES,
    session=session,
)
print(f"Submitted job: {job.id}")
print(f"Status: {job.status}")

# %% [markdown]
# ## Step 4: Wait for the Search to Finish
#
# The job runs asynchronously. You can close this notebook and reattach later with
# `jobs.get_job(job_id)`, and check progress with `job.status` or `job.get_logs()`.

# %%
final_status = job.wait()
print(f"Final status: {final_status}")
print(key_log_lines(job.get_logs()))

# %% [markdown]
# ## Step 5: Analyze the Trials
#
# `job.result()` returns every trial's hyperparameters and validation metrics, plus the winning
# configuration.

# %%
result = job.result()
trials = trials_frame(result["trials"])
print(f"{len(trials)} trials on {result['n_nodes']} nodes / {result['n_cpus']} CPUs in {result['tuning_seconds']}s")
trials.head(10).round(4)

# %%
plot_search_progress(trials)
plt.show()

# %%
PARAMS = [
    "n_estimators",
    "max_depth",
    "learning_rate",
    "min_child_weight",
    "subsample",
    "colsample_bytree",
    "reg_lambda",
]
plot_param_effects(trials, PARAMS)
plt.show()

# %%
spread = trials["roc_auc"].agg(["max", "median", "min"]).round(4)
print(f"Validation ROC AUC  best={spread['max']}  median={spread['median']}  worst={spread['min']}")
print("Best hyperparameters:")
{k: (round(v, 4) if isinstance(v, float) else v) for k, v in result["best_params"].items()}

# %% [markdown]
# **Reading the results:** compare these notes with your own plots; trial outcomes depend on the
# data and the sampled configurations. On this synthetic data, `learning_rate` usually has by far the clearest effect. Rates below about 0.03
# underfit within the tree budget, rates above about 0.15 start to overfit, and the best trials sit
# in the 0.04-0.12 range. The other parameters show no strong trend on their own. Many different
# configurations land within about 0.001 AUC of the best, so the main win from tuning is avoiding
# bad regions of the search space rather than finding one sharp optimum.
#
# Next steps for a production search: narrow the ranges around the best region, then rerun with
# more trials, or switch to `BayesOpt` (convert integer parameters to `tune.uniform` and cast them
# inside `train_func`).

# %% [markdown]
# ## Step 6: Log Trials to Experiment Tracking
#
# Recording each trial as a run in a Snowflake **experiment** makes the search reviewable and
# comparable over time. Open **AI & ML > Experiments** in Snowsight to sort and chart the runs.

# %%
exp = ExperimentTracking(session=session, database_name=DATABASE, schema_name=SCHEMA)
exp.set_experiment(EXPERIMENT_NAME)

# end_run() prints a Snowsight link per run; silence it to keep the output short.
with contextlib.redirect_stdout(io.StringIO()):
    for row in trials.sort_values("trial").itertuples(index=False):
        exp.start_run(f"{VERSION_NAME}_TRIAL_{row.trial:02d}")
        exp.log_params({p: getattr(row, p) for p in PARAMS})
        exp.log_metrics(
            {
                "roc_auc": row.roc_auc,
                "log_loss": row.log_loss,
                "train_seconds": row.train_seconds,
            }
        )
        exp.end_run()

print(f"Logged {len(trials)} runs to experiment {DATABASE}.{SCHEMA}.{EXPERIMENT_NAME}")

# %% [markdown]
# ## Step 7: Use the Best Model from the Registry
#
# The job registered the winning model with its hyperparameters and metrics. Below, it scores
# loan applications directly in the warehouse.

# %%
registry = Registry(session=session, database_name=DATABASE, schema_name=SCHEMA)
mv = registry.get_model(MODEL_NAME).version(VERSION_NAME)
print(
    "Registered metrics:",
    {k: v for k, v in mv.show_metrics().items() if k != "hyperparameters"},
)

sample = session.table(SOURCE_TABLE).limit(10)
preds = mv.run(sample, function_name="predict_proba")
preds.select("LOAN_ID", "IS_DEFAULT", '"output_feature_1"').with_column_renamed(
    '"output_feature_1"', "DEFAULT_PROBABILITY"
).to_pandas().round(4)

# %% [markdown]
# ## Key Takeaways
#
# - **The Tuner handles the scheduling.** You write one `train_func` and declare a search space,
#   and Snowflake spreads the trials across every CPU on every node.
# - **Scale out by adding nodes.** `target_instances` and `max_concurrent_trials` set how much
#   runs in parallel, and the training code doesn't change.
# - **The whole search runs as an ML Job.** It is reproducible and asynchronous, and you can
#   schedule it with Tasks.
# - **Close the loop.** Log the trials to Experiment Tracking and register the best model with its
#   hyperparameters.
# - **Combine the patterns.** For datasets too large for one node, call `XGBEstimator` inside
#   `train_func` and set `uses_snowflake_trainer=True`, so each trial itself trains in a distributed way.
#
# ## Next Steps
#
# - [Distributed training](../../distributed-training/README.md): train a single model across multiple nodes
# - Retrain the best configuration on the full dataset and compare it to the distributed model

# %% [markdown]
# ## Cleanup
#
# The job service, model, and experiment all live in the recipe database. Run
# `sql/99_teardown.sql` as described in the README to remove them together with the compute pool,
# warehouse, and role.
```

### `notebooks/requirements.txt`

```
# Notebook (notebooks/01_hyperparameter_tuning.ipynb), run locally. The ML Job itself runs on
# the Snowflake Container Runtime, which already includes Ray, XGBoost, and scikit-learn.
snowflake-ml-python==2.5.0
snowflake-snowpark-python==1.55.1
pandas==2.3.3
matplotlib==3.11.2
ipython==9.17.1
```

### `notebooks/src/__init__.py`

Copy code

### `notebooks/src/helpers.py`

Copy code

```
"""Notebook helpers for the hyperparameter tuning recipe."""

import re

import matplotlib.pyplot as plt
import pandas as pd

LOG_PATTERN = re.compile(r"Ray cluster|Tuning finished|Best params|Best metrics|Registered")

def key_log_lines(logs: str, max_lines: int = 20) -> str:
    """Keep only the informative lines from an ML Job log."""
    lines = [line for line in logs.splitlines() if LOG_PATTERN.search(line)]
    return "\n".join(lines[-max_lines:])

def trials_frame(trials: list[dict]) -> pd.DataFrame:
    """Turn the job's trial records into a tidy, AUC-sorted DataFrame."""
    df = pd.DataFrame(trials).rename(columns=lambda c: c.replace("config/", ""))
    for col in ("n_estimators", "max_depth", "min_child_weight"):
        df[col] = df[col].astype(int)
    df.insert(0, "trial", range(1, len(df) + 1))
    return df.sort_values("roc_auc", ascending=False).reset_index(drop=True)

def plot_search_progress(df: pd.DataFrame, metric: str = "roc_auc"):
    """Per-trial metric (in completion order) with the running best."""
    d = df.sort_values("trial")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(d["trial"], d[metric], color="#29B5E8", label="Trial")
    ax.plot(d["trial"], d[metric].cummax(), color="#11567F", label="Best so far")
    ax.set_xlabel("Trial")
    ax.set_ylabel(f"Validation {metric}")
    ax.set_title("Search progress")
    ax.legend()
    fig.tight_layout()
    return fig

def plot_param_effects(df: pd.DataFrame, params: list[str], metric: str = "roc_auc"):
    """One scatter per hyperparameter: sampled value vs. validation metric."""
    log_scale = {"learning_rate", "reg_lambda"}
    ncols = 4
    nrows = -(-len(params) // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, 3.2 * nrows), sharey=True)
    axes = axes.ravel()
    for ax, p in zip(axes, params):
        ax.scatter(df[p], df[metric], color="#29B5E8", alpha=0.8)
        ax.set_title(p)
        if p in log_scale:
            ax.set_xscale("log")
    for ax in axes[len(params) :]:
        ax.set_visible(False)
    axes[0].set_ylabel(f"Validation {metric}")
    fig.suptitle("Hyperparameter vs. validation metric")
    fig.tight_layout()
    return fig
```

### `notebooks/src/tune_xgb.py`

Copy code

```
"""Parallel hyperparameter tuning entrypoint for a Snowflake ML Job.

This script runs on the Snowflake Container Runtime. It uses the Snowflake ML
``Tuner`` to run many XGBoost training trials in parallel across every CPU on
every node assigned to the job (``target_instances``). Then it:

1. Picks the best trial by validation ROC AUC.
2. Logs the best model (with its hyperparameters and metrics) to the Model Registry.

The dictionary assigned to ``__return__`` (all trial results plus the best
configuration) is returned to the caller by ``MLJob.result()``.
"""

import argparse
import re
import time

import ray
import xgboost as xgb
from sklearn.metrics import log_loss, roc_auc_score
from snowflake.ml.data.data_connector import DataConnector
from snowflake.ml.modeling import tune
from snowflake.ml.modeling.tune.search import RandomSearch
from snowflake.ml.registry import Registry
from snowflake.snowpark import Session

LABEL_COL = "IS_DEFAULT"
ID_COL = "LOAN_ID"
# --table is interpolated into SQL, so accept only an unquoted DB.SCHEMA.TABLE.
TABLE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*(\.[A-Za-z_][A-Za-z0-9_$]*){2}$")

# Each trial samples one value per hyperparameter from these distributions.
SEARCH_SPACE = {
    "n_estimators": tune.randint(50, 300),
    "max_depth": tune.randint(3, 10),
    "learning_rate": tune.loguniform(0.01, 0.3),
    "min_child_weight": tune.randint(1, 50),
    "subsample": tune.uniform(0.6, 1.0),
    "colsample_bytree": tune.uniform(0.5, 1.0),
    "reg_lambda": tune.loguniform(0.1, 10.0),
}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parallel XGBoost HPO")
    parser.add_argument("--table", required=True, help="Fully qualified source table")
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--version-name", required=True)
    parser.add_argument("--test-pct", type=int, default=20)
    parser.add_argument("--num-trials", type=int, default=24)
    parser.add_argument("--max-concurrent-trials", type=int, default=3, help="Per node")
    parser.add_argument("--threads-per-trial", type=int, default=2)
    args = parser.parse_args()
    if not TABLE_NAME.match(args.table):
        parser.error("--table must be an unquoted DATABASE.SCHEMA.TABLE name")
    return args

def split_query(table: str, test: bool, test_pct: int) -> str:
    """Deterministic hash split, the same split the distributed-training recipe uses."""
    op = "<" if test else ">="
    return f"SELECT * FROM {table} WHERE MOD(ABS(HASH({ID_COL})), 100) {op} {test_pct}"

def make_train_func(threads_per_trial: int):
    """Build the per-trial training function that the Tuner runs on each worker."""

    def train_func():
        ctx = tune.get_tuner_context()
        params = ctx.get_hyper_params()
        datasets = ctx.get_dataset_map()

        train_pdf = datasets["train"].to_pandas()
        valid_pdf = datasets["valid"].to_pandas()
        features = [c for c in train_pdf.columns if c not in (LABEL_COL, ID_COL)]

        model = xgb.XGBClassifier(
            n_estimators=int(params["n_estimators"]),
            max_depth=int(params["max_depth"]),
            learning_rate=params["learning_rate"],
            min_child_weight=int(params["min_child_weight"]),
            subsample=params["subsample"],
            colsample_bytree=params["colsample_bytree"],
            reg_lambda=params["reg_lambda"],
            tree_method="hist",
            n_jobs=threads_per_trial,
        )
        start = time.time()
        model.fit(train_pdf[features], train_pdf[LABEL_COL])
        train_seconds = time.time() - start

        prob = model.predict_proba(valid_pdf[features])[:, 1]
        ctx.report(
            metrics={
                "roc_auc": float(roc_auc_score(valid_pdf[LABEL_COL], prob)),
                "log_loss": float(log_loss(valid_pdf[LABEL_COL], prob)),
                "train_seconds": round(train_seconds, 1),
            },
            model=model,
        )

    return train_func

def main() -> dict:
    args = parse_args()
    session = Session.builder.getOrCreate()

    n_nodes = len([n for n in ray.nodes() if n["Alive"]])
    n_cpus = int(ray.cluster_resources().get("CPU", 0))
    print(f"Ray cluster: {n_nodes} node(s), {n_cpus} CPUs")

    dataset_map = {
        "train": DataConnector.from_dataframe(session.sql(split_query(args.table, False, args.test_pct))),
        "valid": DataConnector.from_dataframe(session.sql(split_query(args.table, True, args.test_pct))),
    }

    tuner_config = tune.TunerConfig(
        metric="roc_auc",
        mode="max",
        search_alg=RandomSearch(random_state=42),
        num_trials=args.num_trials,
        max_concurrent_trials=args.max_concurrent_trials,
        # Trials train open-source XGBoost (not XGBEstimator), so the Tuner packs
        # several single-process trials onto each node.
        uses_snowflake_trainer=False,
    )
    tuner = tune.Tuner(make_train_func(args.threads_per_trial), SEARCH_SPACE, tuner_config)

    start = time.time()
    results = tuner.run(dataset_map=dataset_map)
    tuning_seconds = round(time.time() - start, 1)
    print(f"Tuning finished: {args.num_trials} trials in {tuning_seconds}s")

    trials = results.results.copy()
    print("Result columns:", list(trials.columns))
    best_row = results.best_result.iloc[0].to_dict()
    best_params = {k.split("/", 1)[1]: best_row[k] for k in best_row if k.startswith("config/")}
    best_metrics = {k: float(best_row[k]) for k in ("roc_auc", "log_loss", "train_seconds")}
    print("Best params:", best_params)
    print("Best metrics:", best_metrics)

    best_model = results.best_model
    features = list(best_model.get_booster().feature_names)
    sample = dataset_map["valid"].to_pandas()[features].head(100)

    # Register the model next to the source table.
    database, schema, _ = args.table.split(".")
    registry = Registry(session=session, database_name=database, schema_name=schema)
    mv = registry.log_model(
        best_model,
        model_name=args.model_name,
        version_name=args.version_name,
        sample_input_data=sample,
        metrics={
            **best_metrics,
            "hyperparameters": best_params,
            "num_trials": args.num_trials,
        },
        comment="Best loan default classifier from parallel HPO (snowflake.ml.modeling.tune)",
        target_platforms=["WAREHOUSE"],
    )
    print(f"Registered {mv.model_name} version {mv.version_name}")

    keep = [c for c in trials.columns if c.startswith("config/") or c in best_metrics]
    return {
        "trials": trials[keep].astype(float).to_dict(orient="records"),
        "best_params": {k: float(v) for k, v in best_params.items()},
        "best_metrics": best_metrics,
        "tuning_seconds": tuning_seconds,
        "n_nodes": n_nodes,
        "n_cpus": n_cpus,
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
-- Hyperparameter tuning: role, warehouse, compute pool, database, schema, stage.
--
-- The first block runs as ACCOUNTADMIN and only creates or grants to this
-- recipe's own COOKBOOK_ objects:
--   COOKBOOK_HYPERPARAMETER_TUNING_ADMIN  owns the database and runs the job
--   COOKBOOK_HYPERPARAMETER_TUNING_POOL   multi-node CPU pool for the ML Job
-- The role is granted to the user running this script. Everything after the
-- first block runs as that role.
--
-- Idempotent.
-- =============================================================================

SET cookbook_db   = 'COOKBOOK_HYPERPARAMETER_TUNING';
SET cookbook_wh   = 'COOKBOOK_HYPERPARAMETER_TUNING_WH';
SET cookbook_pool = 'COOKBOOK_HYPERPARAMETER_TUNING_POOL';
SET cookbook_role = 'COOKBOOK_HYPERPARAMETER_TUNING_ADMIN';
SET me            = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($cookbook_role)
  COMMENT = 'Cookbook hyperparameter-tuning: owns the data, job payloads, model, and experiment.';
-- Granting the role to SYSADMIN lets ACCOUNTADMIN, which inherits SYSADMIN,
-- drop what it owns in 99_teardown.sql without relying on secondary roles.
GRANT ROLE IDENTIFIER($cookbook_role) TO ROLE SYSADMIN;
GRANT ROLE IDENTIFIER($cookbook_role) TO USER IDENTIFIER($me);

-- The warehouse runs the data generation, the job's SQL, and warehouse inference.
CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = MEDIUM AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cookbook hyperparameter-tuning';
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
  COMMENT = 'Cookbook hyperparameter-tuning: parallel HPO ML Job';
GRANT USAGE, MONITOR ON COMPUTE POOL IDENTIFIER($cookbook_pool) TO ROLE IDENTIFIER($cookbook_role);

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db)
  COMMENT = 'Cookbook hyperparameter-tuning';
-- Owning the database covers CREATE TABLE, STAGE, SERVICE (the ML Job),
-- MODEL, and EXPERIMENT on its schemas.
GRANT OWNERSHIP ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($cookbook_role) COPY CURRENT GRANTS;

-- ---------------------------------------------------------------------------
-- From here on, run as the recipe role.
-- ---------------------------------------------------------------------------
USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
CREATE SCHEMA IF NOT EXISTS ML
  COMMENT = 'Loan data, ML Job payloads, the tuned model, and the HPO experiment';
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

SET cookbook_db   = 'COOKBOOK_HYPERPARAMETER_TUNING';
SET cookbook_wh   = 'COOKBOOK_HYPERPARAMETER_TUNING_WH';
SET cookbook_role = 'COOKBOOK_HYPERPARAMETER_TUNING_ADMIN';

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
-- database removes the table, the job payload stage, the job services, the
-- registered model and its versions, and the experiment and its runs. Then the
-- warehouse and the role are dropped, which also removes the role's grants.
-- There are no account parameters to restore.
--
-- Run as ACCOUNTADMIN. Safe to rerun.
-- =============================================================================

SET cookbook_db   = 'COOKBOOK_HYPERPARAMETER_TUNING';
SET cookbook_wh   = 'COOKBOOK_HYPERPARAMETER_TUNING_WH';
SET cookbook_pool = 'COOKBOOK_HYPERPARAMETER_TUNING_POOL';
SET cookbook_role = 'COOKBOOK_HYPERPARAMETER_TUNING_ADMIN';

USE ROLE ACCOUNTADMIN;
ALTER COMPUTE POOL IF EXISTS IDENTIFIER($cookbook_pool) STOP ALL;
DROP COMPUTE POOL IF EXISTS IDENTIFIER($cookbook_pool);
DROP DATABASE IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);
DROP ROLE IF EXISTS IDENTIFIER($cookbook_role);

-- Each of these should return no rows.
SHOW COMPUTE POOLS LIKE 'COOKBOOK_HYPERPARAMETER_TUNING%';
SHOW DATABASES LIKE 'COOKBOOK_HYPERPARAMETER_TUNING%';
SHOW WAREHOUSES LIKE 'COOKBOOK_HYPERPARAMETER_TUNING%';
SHOW ROLES LIKE 'COOKBOOK_HYPERPARAMETER_TUNING%';
```
