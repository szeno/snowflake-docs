# Parallel hyperparameter tuning as a multi-node ML Job

Run an XGBoost hyperparameter search across a multi-node compute pool with snowflake.ml.modeling.tune, log the trials as an experiment, and register the best model.

|  |  |
| --- | --- |
| Stage | Build, Evaluate |
| Topics | Snowflake ML |
| Status | GA |
| Time to complete | 30min |
| Edition | Any edition with Snowpark Container Services |
| Regions | Any region with Snowpark Container Services compute pools; ML Jobs are not available in the People’s Republic of China |
| Privileges | ACCOUNTADMIN for sql/01\_setup.sql and sql/99\_teardown.sql (role, warehouse, compute pool, database); sql/02 and the notebook run as COOKBOOK\_HYPERPARAMETER\_TUNING\_ADMIN |
| Related skills | `machine-learning` (bundled with Cortex Code) |
| Last verified | 2026-11-16 |
| Authors | Trace Smith |
| Code | [View all files](/developer-guide/cortex-ai-cookbook/hyperparameter-tuning/code) or download [hyperparameter-tuning.zip](/static/samples/cortex-ai-cookbook/hyperparameter-tuning.zip), which includes this page as `README.md`. Teardown: [sql/99\_teardown.sql](/developer-guide/cortex-ai-cookbook/hyperparameter-tuning/code#label-cookbook-hyperparameter-tuning-sql-99-teardown-sql) |

Expand

Show lessSee more

This recipe is a reference implementation: review the code and adapt it to your environment before production use.

Run a whole XGBoost hyperparameter search on Snowflake compute instead of a laptop or a single notebook kernel. One script, submitted as a Snowflake ML Job, spreads two dozen training trials across every CPU on two compute pool nodes with `snowflake.ml.modeling.tune`. The job registers the best model in the Model Registry with its hyperparameters and metrics, and the notebook records every trial as a run in Snowflake Experiment Tracking so the search can be reviewed and compared later.

## When to use this

- A single model trains in seconds to minutes on one node, and you want to try many configurations without waiting for them one after another.
- You want the search to be reproducible and asynchronous: submitted from any Python environment, running close to the data, and reattachable later by job ID.
- You want the tuning history (every configuration and its metrics) kept in Snowflake next to the model it produced.

When not to use it:

- One model is too large to train on a single node. Train it with a distributed trainer first; see [Distributed training as a multi-node ML Job](/developer-guide/cortex-ai-cookbook/distributed-training). The two combine: call `XGBEstimator` inside `train_func` and set `uses_snowflake_trainer=True`.
- You need retraining on a schedule with a promotion gate. See [Scheduled retraining with a task graph and a quality gate](/developer-guide/cortex-ai-cookbook/ml-pipeline-orchestration), and swap its training step for this job when the search outgrows a warehouse.
- The search space is tiny. A loop in a notebook is simpler than a job.

## How it works

[![Diagram: How it works](/static/images/cortex-ai-cookbook/hyperparameter-tuning/diagram-db3003d7.svg)](/static/images/cortex-ai-cookbook/hyperparameter-tuning/diagram-db3003d7.svg)

- **The Tuner does the scheduling.** You write one `train_func` and declare a search space. `Tuner.run()` samples configurations, runs `train_func` once per trial on whichever worker has free CPUs, and collects what each trial reports through `get_tuner_context().report()`.
- **Parallelism is two numbers.** `target_instances` sets how many nodes join the job’s Ray cluster. `max_concurrent_trials` sets how many trials run at once on each node. The training code does not change when you scale either one.
- **The search runs as an ML Job.** `submit_file` uploads the script to a stage and starts a job service on the compute pool. The script’s `__return__` value comes back through `job.result()`, and the job can be reattached with `jobs.get_job(job_id)` after the notebook closes.
- **The job closes the loop itself.** It logs the best model to the Model Registry from inside the container, so there is no artifact to download. The notebook then logs every trial to an experiment for review in Snowsight.

## Prerequisites

| Requirement | Notes |
| --- | --- |
| Snowpark Container Services in your region | ML Jobs run on a compute pool. ML Jobs are not available in the People’s Republic of China. |
| `ACCOUNTADMIN` | For `sql/01_setup.sql` (creates a role, warehouse, compute pool, and database) and `sql/99_teardown.sql`. `sql/02` and the notebook run as `COOKBOOK_HYPERPARAMETER_TUNING_ADMIN`. |
| Compute pool quota for 3 `CPU_X64_M` nodes | `sql/01` creates the pool with `MAX_NODES = 3`; the job uses 2. The pool bills per active node and suspends after 10 idle minutes. |
| Python 3.11+ locally | `pip install -r notebooks/requirements.txt`, plus Jupyter or VS Code. `snowflake-ml-python` 1.26.0 or later is required for ML Jobs. |
| A Snowflake connection for your own user | The notebook uses the active Snowpark session, or `Session.builder.getOrCreate()` with `SNOWFLAKE_DEFAULT_CONNECTION_NAME`. |

Expand

Show lessSee more

## Quickstart

Object names are fixed. Besides the warehouse size, you may change the pool’s `INSTANCE_FAMILY` and `MAX_NODES` in `sql/01`, and the search settings (`TARGET_INSTANCES`, `NUM_TRIALS`, `MAX_CONCURRENT_TRIALS`, `THREADS_PER_TRIAL`) in the notebook’s configuration cell. Keep `TARGET_INSTANCES` at or below `MAX_NODES`.

1. `sql/01_setup.sql` as `ACCOUNTADMIN`: the role, warehouse, compute pool, database, `ML` schema, and `ML.JOBS_STAGE`.
2. `sql/02_data.sql`: builds `ML.LOAN_APPLICATIONS` (1M rows) and prints its row count and default rate.
3. `notebooks/01_hyperparameter_tuning.ipynb`: run every cell. The job takes several minutes, longer on the first run while the pool starts its nodes.
4. `sql/99_teardown.sql` as `ACCOUNTADMIN`.

## Walkthrough

### Setup (`sql/01`)

Copy code

```
CREATE COMPUTE POOL IF NOT EXISTS IDENTIFIER($cookbook_pool)
  MIN_NODES = 1 MAX_NODES = 3 INSTANCE_FAMILY = CPU_X64_M
  AUTO_RESUME = TRUE AUTO_SUSPEND_SECS = 600 INITIALLY_SUSPENDED = TRUE;
GRANT USAGE, MONITOR ON COMPUTE POOL IDENTIFIER($cookbook_pool) TO ROLE IDENTIFIER($cookbook_role);
GRANT OWNERSHIP ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($cookbook_role) COPY CURRENT GRANTS;
```

An ML Job needs `USAGE` on the compute pool, `CREATE SERVICE` on the schema it runs in, and access to a stage for its payload. Owning the database gives the recipe role `CREATE SERVICE`, `CREATE STAGE`, `CREATE MODEL`, and `CREATE EXPERIMENT` on the `ML` schema, so the role needs nothing at account level beyond the pool and warehouse grants. `MONITOR` on the pool lets the role see the pool’s state.

### The trial function (`notebooks/src/tune_xgb.py`)

Copy code

```
SEARCH_SPACE = {
    "n_estimators": tune.randint(50, 300),
    "max_depth": tune.randint(3, 10),
    "learning_rate": tune.loguniform(0.01, 0.3),
    ...
}

def train_func():
    ctx = tune.get_tuner_context()
    params = ctx.get_hyper_params()
    datasets = ctx.get_dataset_map()
    model = xgb.XGBClassifier(..., n_jobs=threads_per_trial).fit(...)
    ctx.report(metrics={"roc_auc": ..., "log_loss": ..., "train_seconds": ...}, model=model)

tuner = tune.Tuner(train_func, SEARCH_SPACE, tune.TunerConfig(
    metric="roc_auc", mode="max", search_alg=RandomSearch(random_state=42),
    num_trials=24, max_concurrent_trials=3, uses_snowflake_trainer=False))
results = tuner.run(dataset_map={"train": ..., "valid": ...})
```

The train and validation splits are `DataConnector`s over a deterministic hash split of `LOAN_ID`, so the notebook can rebuild the same hold-out set. Trials train open-source XGBoost, so `uses_snowflake_trainer=False` tells the Tuner to pack several single-process trials onto each node. The script accepts `--table` only as an unquoted `DATABASE.SCHEMA.TABLE`, because the name is placed into the split query.

### Submitting the job (notebook step 3)

Copy code

```
job = jobs.submit_file(
    "src/tune_xgb.py", COMPUTE_POOL, stage_name=STAGE,
    args=["--table", SOURCE_TABLE, "--model-name", MODEL_NAME, ...],
    target_instances=TARGET_INSTANCES, session=session)
job.wait()
result = job.result()
```

Search settings travel as command-line arguments, so the budget changes without editing the script. On `CPU_X64_M` the notebook’s defaults run 3 trials of 2 threads each per node, 6 at a time across 2 nodes. Raise `TARGET_INSTANCES` (up to the pool’s `MAX_NODES`) to finish the same search sooner.

### Reviewing and using the result (notebook steps 5 to 7)

`job.result()` returns every trial’s configuration and validation metrics. The notebook plots search progress and each hyperparameter against validation ROC AUC, logs each trial with `ExperimentTracking.start_run`, `log_params`, and `log_metrics`, and scores ten rows with the registered model in the warehouse with `ModelVersion.run(..., function_name="predict_proba")`.

## Verify

- `sql/02` returns `n_rows = 1000000` and a `default_rate` between 0.15 and 0.20.
- Notebook step 1 prints `COOKBOOK_HYPERPARAMETER_TUNING_ADMIN`, `COOKBOOK_HYPERPARAMETER_TUNING_WH`, and `ML`.
- Step 4 prints `Final status: DONE`, and the key log lines include `Ray cluster: 2 node(s)` and `Tuning finished: 24 trials`.
- Step 5 shows 24 trials. The best validation ROC AUC is well above 0.5, and the spread between best and median is small.
- Step 6 prints `Logged 24 runs to experiment COOKBOOK_HYPERPARAMETER_TUNING.ML.LOAN_DEFAULT_HPO`.
- Step 7 prints the registered metrics and ten rows with a `DEFAULT_PROBABILITY` between 0 and 1.
- In SQL, as the recipe role:

  Copy code

  ```
  SHOW VERSIONS IN MODEL COOKBOOK_HYPERPARAMETER_TUNING.ML.LOAN_DEFAULT_XGB_TUNED;
  SHOW EXPERIMENTS IN SCHEMA COOKBOOK_HYPERPARAMETER_TUNING.ML;
  ```

  The first returns one version per notebook run, and the second lists `LOAN_DEFAULT_HPO`.

## Gotchas

| Symptom | Cause | Fix |
| --- | --- | --- |
| The job stays `PENDING` for several minutes on the first run | The compute pool starts suspended and is provisioning nodes | Wait; check `DESCRIBE COMPUTE POOL COOKBOOK_HYPERPARAMETER_TUNING_POOL` for `ACTIVE` or `IDLE` |
| The job logs “Compute pool busy (2/3 nodes in use, 2 nodes required)” and waits | The pool is still adding nodes, or another job on the same pool holds them | Informational; the job starts once enough nodes are free. Check `SHOW SERVICES IN COMPUTE POOL COOKBOOK_HYPERPARAMETER_TUNING_POOL` |
| The job fails waiting for instances | `target_instances` is above the pool’s `MAX_NODES`, or the account’s node quota is exhausted | Keep `TARGET_INSTANCES` at or below `MAX_NODES`, or lower it |
| `submit_file` fails with insufficient privileges on the compute pool or schema | The session is not using the recipe role | Run notebook step 1, which calls `session.use_role(ROLE)` |
| `ImportError` for `snowflake.ml.jobs` or `snowflake.ml.experiment` | Old `snowflake-ml-python` | `pip install -r notebooks/requirements.txt` (ML Jobs need 1.26.0 or later) |
| Trials run one at a time | `max_concurrent_trials` times `threads_per_trial` exceeds a node’s schedulable CPUs | Lower either value; a `CPU_X64_M` node fits 3 trials of 2 threads |
| `parser.error: --table must be an unquoted DATABASE.SCHEMA.TABLE name` | A quoted or two-part name was passed | Pass the fully qualified, unquoted name |
| Integer hyperparameters arrive as floats | Search spaces sample numbers; the trial casts them | Keep the `int(...)` casts in `train_func` |

Expand

Show lessSee more

## Teardown

Run `sql/99_teardown.sql` as `ACCOUNTADMIN`. It stops everything running on the compute pool and drops the pool, then drops the database, which removes the table, the payload stage, the job services, the model and its versions, and the experiment with its runs. Last, it drops the warehouse and the role. Every name comes from the script’s `SET` block, which matches setup, and the script ends with `SHOW` statements that should all return no rows.

## Run it with a coding agent

```
Run the recipe in hyperparameter-tuning/ against my current Snowflake
connection. Enable the bundled machine-learning skill and use it for any follow-up modeling
questions; this recipe does not repeat what that skill covers.

1. Run SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_WAREHOUSE(); and show
   me the result. Stop if it fails.
2. Tell me that sql/01 creates a role, a MEDIUM warehouse, a compute pool of up to 3 CPU_X64_M
   nodes, and a database, all named COOKBOOK_HYPERPARAMETER_TUNING*. Wait for my yes, then run
   sql/01_setup.sql and sql/02_data.sql in order with snow sql -f, and report the row count and
   default rate.
3. pip install -r notebooks/requirements.txt, then run notebooks/01_hyperparameter_tuning.ipynb
   from the notebooks folder, cell by cell. Report the job's final status, the number of trials,
   the best ROC AUC and its hyperparameters, and the number of experiment runs logged.
4. Run the SQL queries under Verify in the README as COOKBOOK_HYPERPARAMETER_TUNING_ADMIN and
   report the results.
5. When I say so, run sql/99_teardown.sql and show that every SHOW at the end returns no rows.
Never drop or alter objects that do not start with COOKBOOK_.
```

## Related skills

- `machine-learning` (bundled): training, registering, deploying, and monitoring models on Snowflake, including ML Jobs. This recipe covers one end-to-end tuning pattern; that skill covers the rest of the ML workflow and ad-hoc modeling questions.

## References

- [Parallel Hyperparameter Optimization (HPO) on Container Runtime](/developer-guide/snowflake-ml/container-hpo)
- [Snowflake ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview)
- [Snowflake Multi-Node ML Jobs](/developer-guide/snowflake-ml/ml-jobs/distributed-ml-jobs)
- [Access control requirements for ML Jobs](/developer-guide/snowflake-ml/ml-jobs/access-control-requirements)
- [Run an experiment to compare and select models](/developer-guide/snowflake-ml/experiments)
- [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview)
- [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool)
