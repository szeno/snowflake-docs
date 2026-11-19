# Distributed training as a multi-node ML Job

Train one XGBoost model across several compute pool nodes with XGBEstimator, submitted as an ML Job, then register it and score it from a warehouse.

|  |  |
| --- | --- |
| Stage | Build |
| Topics | Snowflake ML |
| Status | GA |
| Time to complete | 30min |
| Edition | Any edition with Snowpark Container Services |
| Regions | Any region with Snowpark Container Services compute pools; ML Jobs are not available in the People’s Republic of China |
| Privileges | ACCOUNTADMIN for sql/01\_setup.sql and sql/99\_teardown.sql (role, warehouse, compute pool, database); sql/02 and the notebook run as COOKBOOK\_DISTRIBUTED\_TRAINING\_ADMIN |
| Related skills | `machine-learning` (bundled with Cortex Code) |
| Last verified | 2026-11-16 |
| Authors | Trace Smith |
| Code | [View all files](/developer-guide/cortex-ai-cookbook/distributed-training/code) or download [distributed-training.zip](/static/samples/cortex-ai-cookbook/distributed-training.zip), which includes this page as `README.md`. Teardown: [sql/99\_teardown.sql](/developer-guide/cortex-ai-cookbook/distributed-training/code#label-cookbook-distributed-training-sql-99-teardown-sql) |

Expand

Show lessSee more

This recipe is a reference implementation: review the code and adapt it to your environment before production use.

Train one XGBoost model across several nodes of a compute pool instead of one machine. A training script, submitted from a notebook as a Snowflake ML Job, starts a multi-node Ray cluster on the pool. Snowflake’s distributed `XGBEstimator` shards the table across the nodes and trains a single booster collectively. The job evaluates the booster on a hold-out split and logs it to the Model Registry from inside the container, and the notebook then scores the hold-out set in a warehouse to check ranking and calibration.

## When to use this

- The training table is too large for one node’s memory, or boosting on one node takes too long.
- You want training to run on managed compute close to the data while you develop from any Python environment.
- You want each training run versioned in the Model Registry with its metrics, ready to serve from SQL.

When not to use it:

- The data fits comfortably on one node. Single-node open-source XGBoost avoids the cross-node coordination and is often faster. The 1M-row table in this recipe is deliberately small so it runs quickly; it shows the workflow, not a speedup.
- You are choosing hyperparameters. See [Parallel hyperparameter tuning as a multi-node ML Job](/developer-guide/cortex-ai-cookbook/hyperparameter-tuning), which runs many single-node trials in parallel.
- You need scheduled retraining with a promotion gate. See [Scheduled retraining with a task graph and a quality gate](/developer-guide/cortex-ai-cookbook/ml-pipeline-orchestration).

## How it works

[![Diagram: How it works](/static/images/cortex-ai-cookbook/distributed-training/diagram-cb215a24.svg)](/static/images/cortex-ai-cookbook/distributed-training/diagram-cb215a24.svg)

- **One model, many nodes.** `XGBEstimator.fit()` starts one XGBoost worker per node by default. Each worker trains on its shard, and the workers synchronize histogram statistics every boosting round, so the output is a single booster trained on all of the data.
- **`target_instances` is the scaling knob.** It sets how many pool nodes join the job’s Ray cluster. The training code does not change; the pool’s `MAX_NODES` must be at least `target_instances`.
- **`DataConnector` feeds the cluster.** `DataConnector.from_dataframe()` wraps a Snowpark DataFrame so the workers read their shards in parallel instead of pulling the table through the head node.
- **Register from inside the job.** The head node logs the booster with its hold-out metrics, so every run is a versioned, servable model and no artifact leaves Snowflake.

## Prerequisites

| Requirement | Notes |
| --- | --- |
| Snowpark Container Services in your region | ML Jobs run on a compute pool. ML Jobs are not available in the People’s Republic of China. |
| `ACCOUNTADMIN` | For `sql/01_setup.sql` (creates a role, warehouse, compute pool, and database) and `sql/99_teardown.sql`. `sql/02` and the notebook run as `COOKBOOK_DISTRIBUTED_TRAINING_ADMIN`. |
| Compute pool quota for 3 `CPU_X64_M` nodes | `sql/01` creates the pool with `MAX_NODES = 3`; the job uses 2. The pool bills per active node and suspends after 10 idle minutes. |
| Python 3.11+ locally | `pip install -r notebooks/requirements.txt`, plus Jupyter or VS Code. `snowflake-ml-python` 1.26.0 or later is required for ML Jobs. |
| A Snowflake connection for your own user | The notebook uses the active Snowpark session, or `Session.builder.getOrCreate()` with `SNOWFLAKE_DEFAULT_CONNECTION_NAME`. |

Expand

Show lessSee more

## Quickstart

Object names are fixed. Besides the warehouse size, you may change the pool’s `INSTANCE_FAMILY` and `MAX_NODES` in `sql/01`, and `TARGET_INSTANCES` and `HYPERPARAMS` in the notebook’s configuration cell. Keep `TARGET_INSTANCES` at or below `MAX_NODES`.

1. `sql/01_setup.sql` as `ACCOUNTADMIN`: the role, warehouse, compute pool, database, `ML` schema, and `ML.JOBS_STAGE`.
2. `sql/02_data.sql`: builds `ML.LOAN_APPLICATIONS` (1M rows) and prints its row count and default rate.
3. `notebooks/01_distributed_training.ipynb`: run every cell. The job takes several minutes, longer on the first run while the pool starts its nodes.
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

An ML Job needs `USAGE` on the compute pool, `CREATE SERVICE` on the schema it runs in, and access to a stage for its payload. Owning the database gives the recipe role `CREATE SERVICE`, `CREATE STAGE`, and `CREATE MODEL` on the `ML` schema.

### The training script (`notebooks/src/train_xgb_distributed.py`)

Copy code

```
estimator = XGBEstimator(
    n_estimators=args.n_estimators,
    params={"objective": "binary:logistic", "eval_metric": ["logloss", "auc"],
            "tree_method": "hist", "max_depth": args.max_depth, "eta": args.learning_rate, ...},
    scaling_config=XGBScalingConfig(use_gpu=False),
)
booster = estimator.fit(
    DataConnector.from_dataframe(train_df),
    input_cols=feature_cols, label_col="IS_DEFAULT",
    eval_set=DataConnector.from_dataframe(test_df),
)
```

Train and test are a deterministic hash split of `LOAN_ID`, so the notebook can rebuild the same hold-out set later. After training, the head node scores the hold-out split with the open-source booster, logs the booster to the registry next to the source table with `target_platforms=["WAREHOUSE"]`, and returns metrics and per-feature gain through `__return__`. The script accepts `--table` only as an unquoted `DATABASE.SCHEMA.TABLE`, because the name is placed into the split query.

### Submitting and monitoring (notebook steps 4 to 6)

Copy code

```
job = jobs.submit_file(
    "src/train_xgb_distributed.py", COMPUTE_POOL, stage_name=STAGE,
    args=["--table", SOURCE_TABLE, "--model-name", MODEL_NAME, ...],
    target_instances=TARGET_INSTANCES, session=session)
job.wait()
result = job.result()
```

`submit_file` returns immediately with an `MLJob` handle. You can close the notebook and reattach with `jobs.get_job(job_id)`, then check it with `job.status` and `job.get_logs()`.

### Batch inference from a warehouse (notebook step 8)

`ModelVersion.run(test_df, function_name="predict")` scores the hold-out split inside the warehouse. The notebook plots observed default rate against mean predicted probability for each score decile, which checks ranking and calibration together. The same model is callable from SQL:

Copy code

```
WITH mv AS MODEL COOKBOOK_DISTRIBUTED_TRAINING.ML.LOAN_DEFAULT_XGB_DISTRIBUTED VERSION <VERSION_NAME>
SELECT LOAN_ID, mv!PREDICT(*):output_feature_0::FLOAT AS DEFAULT_PROBABILITY
FROM COOKBOOK_DISTRIBUTED_TRAINING.ML.LOAN_APPLICATIONS
LIMIT 10;
```

## Verify

- `sql/02` returns `n_rows = 1000000` and a `default_rate` between 0.15 and 0.20.
- Notebook step 1 prints `COOKBOOK_DISTRIBUTED_TRAINING_ADMIN`, `COOKBOOK_DISTRIBUTED_TRAINING_WH`, and `ML`.
- Step 2 shows a `TRAIN` and a `TEST` split of roughly 800,000 and 200,000 rows with similar default rates.
- Step 5 prints `Final status: DONE`, and the key log lines include `Ray cluster: 2 node(s)` and `Distributed training finished`.
- Step 6 shows hold-out metrics with `roc_auc` well above 0.5, and the feature importance chart is led by risk drivers from `sql/02` such as `NUM_DELINQUENCIES` and `CREDIT_SCORE`.
- Step 7 lists the new version, and step 8’s warehouse-scored ROC AUC matches step 6’s `roc_auc`. The lift chart rises from decile 1 to decile 10, with predicted and observed bars close together.
- In SQL, as the recipe role, `SHOW VERSIONS IN MODEL COOKBOOK_DISTRIBUTED_TRAINING.ML.LOAN_DEFAULT_XGB_DISTRIBUTED;` returns one version per notebook run.

## Gotchas

| Symptom | Cause | Fix |
| --- | --- | --- |
| The job stays `PENDING` for several minutes on the first run | The compute pool starts suspended and is provisioning nodes | Wait; check `DESCRIBE COMPUTE POOL COOKBOOK_DISTRIBUTED_TRAINING_POOL` for `ACTIVE` or `IDLE` |
| The job logs “Compute pool busy (2/3 nodes in use, 2 nodes required)” and waits | The pool is still adding nodes, or another job on the same pool holds them | Informational; the job starts once enough nodes are free. Check `SHOW SERVICES IN COMPUTE POOL COOKBOOK_DISTRIBUTED_TRAINING_POOL` |
| The job fails waiting for instances | `target_instances` is above the pool’s `MAX_NODES`, or the account’s node quota is exhausted | Keep `TARGET_INSTANCES` at or below `MAX_NODES`, or lower it |
| Distributed training is slower than a single-node run | The table is small enough that cross-node coordination dominates | Expected at 1M rows; use single-node XGBoost until the data outgrows one node |
| `submit_file` fails with insufficient privileges on the compute pool or schema | The session is not using the recipe role | Run notebook step 1, which calls `session.use_role(ROLE)` |
| `ImportError` for `snowflake.ml.jobs` | Old `snowflake-ml-python` | `pip install -r notebooks/requirements.txt` (ML Jobs need 1.26.0 or later) |
| The job fails with memory errors as the table grows | Each node holds its shard in memory | Use a larger `INSTANCE_FAMILY` or more nodes with less data per node |
| `parser.error: --table must be an unquoted DATABASE.SCHEMA.TABLE name` | A quoted or two-part name was passed | Pass the fully qualified, unquoted name |

Expand

Show lessSee more

## Teardown

Run `sql/99_teardown.sql` as `ACCOUNTADMIN`. It stops everything running on the compute pool and drops the pool, then drops the database, which removes the table, the payload stage, the job services, and the model and its versions. Last, it drops the warehouse and the role. Every name comes from the script’s `SET` block, which matches setup, and the script ends with `SHOW` statements that should all return no rows.

## Run it with a coding agent

```
Run the recipe in distributed-training/ against my current Snowflake
connection. Enable the bundled machine-learning skill and use it for any follow-up modeling
questions; this recipe does not repeat what that skill covers.

1. Run SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_WAREHOUSE(); and show
   me the result. Stop if it fails.
2. Tell me that sql/01 creates a role, a MEDIUM warehouse, a compute pool of up to 3 CPU_X64_M
   nodes, and a database, all named COOKBOOK_DISTRIBUTED_TRAINING*. Wait for my yes, then run
   sql/01_setup.sql and sql/02_data.sql in order with snow sql -f, and report the row count and
   default rate.
3. pip install -r notebooks/requirements.txt, then run notebooks/01_distributed_training.ipynb
   from the notebooks folder, cell by cell. Report the job's final status, the node count, the
   training time, the hold-out metrics, and the warehouse-scored ROC AUC.
4. Run the SQL query under Verify in the README as COOKBOOK_DISTRIBUTED_TRAINING_ADMIN and
   report the result.
5. When I say so, run sql/99_teardown.sql and show that every SHOW at the end returns no rows.
Never drop or alter objects that do not start with COOKBOOK_.
```

## Related skills

- `machine-learning` (bundled): training, registering, deploying, and monitoring models on Snowflake, including ML Jobs. This recipe covers one end-to-end distributed training pattern; that skill covers the rest of the ML workflow and ad-hoc modeling questions.

## References

- [Distributed training](/developer-guide/snowflake-ml/distributed-training)
- [Snowflake ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview)
- [Snowflake Multi-Node ML Jobs](/developer-guide/snowflake-ml/ml-jobs/distributed-ml-jobs)
- [Access control requirements for ML Jobs](/developer-guide/snowflake-ml/ml-jobs/access-control-requirements)
- [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview)
- [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool)
