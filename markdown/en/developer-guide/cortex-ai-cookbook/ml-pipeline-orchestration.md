# Scheduled retraining with a task graph and a quality gate

Retrain, evaluate, and promote a model on a schedule: Python procedures as a Snowflake task graph that share config, pass return values, and gate the default version on AUC.

|  |  |
| --- | --- |
| Stage | Operate, Build |
| Topics | Snowflake ML |
| Status | GA |
| Time to complete | 30min |
| Edition | Any edition |
| Regions | Any region with Python stored procedures and the Snowflake Anaconda channel |
| Privileges | ACCOUNTADMIN for sql/01\_setup.sql (role, warehouse, database, and EXECUTE TASK ON ACCOUNT to the recipe role) and sql/99\_teardown.sql; sql/02 and the notebook run as COOKBOOK\_ML\_PIPELINE\_ORCHESTRATION\_ADMIN |
| Related skills | `snowflake-tasks` (bundled with Cortex Code), `machine-learning` (bundled with Cortex Code) |
| Last verified | 2026-11-16 |
| Authors | Trace Smith |
| Code | [View all files](/developer-guide/cortex-ai-cookbook/ml-pipeline-orchestration/code) or download [ml-pipeline-orchestration.zip](/static/samples/cortex-ai-cookbook/ml-pipeline-orchestration.zip), which includes this page as `README.md`. Teardown: [sql/99\_teardown.sql](/developer-guide/cortex-ai-cookbook/ml-pipeline-orchestration/code#label-cookbook-ml-pipeline-orchestration-sql-99-teardown-sql) |

Expand

Show lessSee more

This recipe is a reference implementation: review the code and adapt it to your environment before production use.

Retrain a model on a schedule without an external orchestrator. Three Python stored procedures (feature engineering, training, and evaluation) run as a Snowflake task graph. They read their inputs and the quality bar from the task graph config, and pass the new model version from one step to the next with task return values. Every run registers a new version in the Model Registry and appends its metrics to a history table, and only a version whose hold-out ROC AUC clears the threshold becomes the default that consumers score with.

## When to use this

- A model needs regular retraining on fresh data, and the training fits in a warehouse-run Python procedure.
- Consumers should always score with the last model that passed evaluation, even when a retrain comes out worse.
- You want to change inputs or the promotion threshold without redeploying code.

When not to use it:

- Training outgrows a warehouse. Keep this graph and replace `TRAIN_MODEL` with a task that submits an ML Job; see [Distributed training as a multi-node ML Job](/developer-guide/cortex-ai-cookbook/distributed-training) and [Parallel hyperparameter tuning as a multi-node ML Job](/developer-guide/cortex-ai-cookbook/hyperparameter-tuning).
- The pipeline is mostly SQL transformations with no model step. Dynamic tables or plain tasks are simpler; see the bundled `snowflake-tasks` skill.
- Retraining should start when data lands rather than on a clock. The same graph works with `schedule=None` and a stream condition on the root task.

## How it works

[![Diagram: How it works](/static/images/cortex-ai-cookbook/ml-pipeline-orchestration/diagram-4c5926c1.svg)](/static/images/cortex-ai-cookbook/ml-pipeline-orchestration/diagram-4c5926c1.svg)

- **Procedures are the unit of work.** Each step is a permanent Python stored procedure that you can test on its own with `CALL`. The task graph only wires them together.
- **Config makes the graph reusable.** Table names, the model name, and `auc_threshold` live in the root task’s `CONFIG`. Every procedure reads them at run time with `TaskContext.get_task_graph_config_property`, so a change is an `ALTER TASK ... SET CONFIG`.
- **Return values connect the steps.** `TRAIN_MODEL` calls `set_return_value` with the version it registered, and `EVALUATE_MODEL` reads it with `get_predecessor_return_value("TRAIN_MODEL")`. The values are also recorded in `TASK_HISTORY`.
- **The gate protects consumers.** Every run is registered with its metrics, but `model.default` moves only when the new version passes. Downstream scoring that uses the default version never sees a rejected retrain.

## Prerequisites

| Requirement | Notes |
| --- | --- |
| `ACCOUNTADMIN` | For `sql/01_setup.sql` and `sql/99_teardown.sql`. `sql/01` grants `EXECUTE TASK ON ACCOUNT` to the recipe role, which a task owner needs; dropping the role in teardown removes it. `sql/02` and the notebook run as `COOKBOOK_ML_PIPELINE_ORCHESTRATION_ADMIN`. |
| Snowflake Anaconda packages | The procedures import `snowflake-ml-python`, `snowflake` (the Python API, for `TaskContext`), `xgboost`, and `scikit-learn` from the Snowflake Anaconda channel. An organization administrator must have acknowledged the Anaconda terms. |
| Python 3.11+ locally | `pip install -r notebooks/requirements.txt`, plus Jupyter or VS Code. Procedures registered from a notebook use its Python version, and the handlers need 3.11 or later. |
| A Snowflake connection for your own user | The notebook uses the active Snowpark session, or `Session.builder.getOrCreate()` with `SNOWFLAKE_DEFAULT_CONNECTION_NAME`. |

Expand

Show lessSee more

## Quickstart

Object names are fixed. Besides the warehouse size, you may change `SCHEDULE` and the values in `PIPELINE_CONFIG` other than the table and model names in the notebook’s configuration cell.

1. `sql/01_setup.sql` as `ACCOUNTADMIN`: the role, warehouse, `EXECUTE TASK` grant, database, `ML` schema, and `ML.PIPELINE_STAGE`.
2. `sql/02_data.sql`: builds `ML.LOAN_APPLICATIONS` (1M rows) and prints its row count and default rate.
3. `notebooks/01_ml_pipeline_orchestration.ipynb`: run every cell. Step 4 deploys the graph resumed on a weekly schedule, steps 5 and 7 each trigger a run of two to three minutes, and step 8 suspends the graph.
4. `sql/99_teardown.sql` as `ACCOUNTADMIN`.

## Walkthrough

### Setup (`sql/01`)

Copy code

```
GRANT EXECUTE TASK ON ACCOUNT TO ROLE IDENTIFIER($cookbook_role);
GRANT OWNERSHIP ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($cookbook_role) COPY CURRENT GRANTS;
```

The recipe role owns the database, so it can create the procedures, tasks, tables, and model in `ML`. It also owns the tasks, so they run as that role on the recipe warehouse.

### The pipeline steps (`notebooks/src/pipeline_steps.py`)

Copy code

```
def train_model(session):
    ctx = TaskContext(session)
    feature_table = ctx.get_task_graph_config_property("feature_table")
    ...
    mv = Registry(session=session).log_model(model, model_name=model_name, version_name=version_name, ...)
    ctx.set_return_value(version_name)

def evaluate_model(session):
    ctx = TaskContext(session)
    version_name = ctx.get_predecessor_return_value("TRAIN_MODEL")
    ...
    if auc >= auc_threshold:
        model.default = version_name
```

`FEATURE_ENGINEERING` adds an amortized monthly payment, payment-to-income, a delinquency flag, and a score-by-headroom feature, and assigns a deterministic `TRAIN`/`TEST` split by hashing `LOAN_ID`. `EVALUATE_MODEL` scores the `TEST` split with `mv.run(..., function_name="predict_proba")` in the warehouse, records the metrics on the version and in `ML_PIPELINE_METRICS`, and promotes the version only if it passes.

### Procedures and the graph (notebook steps 3 and 4)

Copy code

```
session.sproc.register_from_file(
    "src/pipeline_steps.py", step, name=f"ML_PIPELINE_{step.upper()}",
    packages=PACKAGES, is_permanent=True, stage_location="@PIPELINE_STAGE/ml_pipeline",
    replace=True, execute_as="caller")

with DAG("ML_PIPELINE_DAG", schedule=timedelta(days=7), warehouse=WAREHOUSE,
         config=PIPELINE_CONFIG, stage_location="@PIPELINE_STAGE/ml_pipeline") as dag:
    features = DAGTask("FEATURE_ENGINEERING", definition="CALL ML_PIPELINE_FEATURE_ENGINEERING()")
    train = DAGTask("TRAIN_MODEL", definition="CALL ML_PIPELINE_TRAIN_MODEL()")
    evaluate = DAGTask("EVALUATE_MODEL", definition="CALL ML_PIPELINE_EVALUATE_MODEL()")
    features >> train >> evaluate
DAGOperation(schema_ref).deploy(dag, mode=CreateMode.or_replace)
```

The procedures run with caller’s rights, the cookbook default. Inside a task the caller is the task owner, so each step can do only what the recipe role can do. Child tasks are named `ML_PIPELINE_DAG$<TASK_NAME>`. `deploy` creates or replaces every task and resumes the graph, so the weekly schedule is live as soon as the cell runs.

### Change behavior with config only (notebook step 7)

Copy code

```
ALTER TASK ML_PIPELINE_DAG SUSPEND;
ALTER TASK ML_PIPELINE_DAG SET CONFIG = $${"auc_threshold": "0.99", ...}$$;
ALTER TASK ML_PIPELINE_DAG RESUME;
EXECUTE TASK ML_PIPELINE_DAG;
```

The root task must be suspended to alter it, and `SET CONFIG` replaces the whole config, so the notebook sends every key. With an unreachable threshold the next run still registers a version, but the default does not move. The notebook then restores the original config.

## Verify

- `sql/02` returns `n_rows = 1000000` and a `default_rate` between 0.15 and 0.20.
- Notebook step 1 prints `COOKBOOK_ML_PIPELINE_ORCHESTRATION_ADMIN`, `COOKBOOK_ML_PIPELINE_ORCHESTRATION_WH`, and `ML`.
- Step 4 prints the deployed tasks `ML_PIPELINE_DAG$FEATURE_ENGINEERING`, `ML_PIPELINE_DAG$TRAIN_MODEL`, and `ML_PIPELINE_DAG$EVALUATE_MODEL`.
- Step 5 shows all three child tasks `SUCCEEDED`. `TRAIN_MODEL`’s `RETURN_VALUE` is a version name such as `V_20261116_120000`, and `EVALUATE_MODEL`’s is JSON with that version, `"promoted": true`, and a `roc_auc` above 0.75.
- Step 6 shows a row in `ML_PIPELINE_METRICS` with `PROMOTED = TRUE`, and the default version is the one from step 5.
- Step 7 prints `"promoted": false`, and the default version is still the one from step 5.
- Step 8 shows the root task `suspended`.
- In SQL, as the recipe role:

  Copy code

  ```
  SELECT VERSION_NAME, ROC_AUC, AUC_THRESHOLD, PROMOTED
  FROM COOKBOOK_ML_PIPELINE_ORCHESTRATION.ML.ML_PIPELINE_METRICS
  ORDER BY EVALUATED_AT;
  SHOW VERSIONS IN MODEL COOKBOOK_ML_PIPELINE_ORCHESTRATION.ML.LOAN_DEFAULT_PIPELINE;
  ```

  The first returns two rows, promoted and then not promoted. The second returns two versions, with `is_default_version` true on the first.

## Gotchas

| Symptom | Cause | Fix |
| --- | --- | --- |
| Tasks fail with “Cannot execute task, EXECUTE TASK privilege must be granted to owner role” | The recipe role lacks `EXECUTE TASK` | Rerun `sql/01` as `ACCOUNTADMIN` |
| `register_from_file` fails resolving packages | The Anaconda terms have not been acknowledged, or a package is not on the channel | Have an organization administrator acknowledge the terms; check package names against the channel |
| `ALTER TASK ... SET CONFIG` fails | The root task is still started | Suspend the root task first, as notebook step 7 does |
| A config change drops a setting | `SET CONFIG` replaces the whole config | Send every key, not just the one you change |
| `EVALUATE_MODEL` fails reading the version | It ran without its predecessor, for example from a manual `CALL` | Run the whole graph with `EXECUTE TASK ML_PIPELINE_DAG`; test a step alone only where it does not read a return value |
| The model’s default did not change after a run | The new version failed the gate | Expected; check `ML_PIPELINE_METRICS` for `ROC_AUC` against `AUC_THRESHOLD` |
| Runs keep happening every week | The graph was deployed resumed and never suspended | Run notebook step 8, or `ALTER TASK COOKBOOK_ML_PIPELINE_ORCHESTRATION.ML.ML_PIPELINE_DAG SUSPEND` |

Expand

Show lessSee more

## Teardown

Run `sql/99_teardown.sql` as `ACCOUNTADMIN`. It drops the database, which removes the task graph (so no further runs are scheduled), the procedures, stage, tables, and the model and its versions. Last, it drops the warehouse and the role, which removes the role’s `EXECUTE TASK` grant. Every name comes from the script’s `SET` block, which matches setup, and the script ends with `SHOW` statements that should all return no rows.

## Run it with a coding agent

```
Run the recipe in ml-pipeline-orchestration/ against my current Snowflake
connection. Enable the bundled snowflake-tasks and machine-learning skills and use them for any
follow-up task graph or modeling questions; this recipe does not repeat what those skills cover.

1. Run SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_WAREHOUSE(); and show
   me the result. Stop if it fails.
2. Tell me that sql/01 creates a role, a MEDIUM warehouse, and a database named
   COOKBOOK_ML_PIPELINE_ORCHESTRATION*, and grants EXECUTE TASK ON ACCOUNT to that role (an
   account-level privilege). Wait for my yes, then run sql/01_setup.sql and sql/02_data.sql in
   order with snow sql -f, and report the row count and default rate.
3. pip install -r notebooks/requirements.txt, then run notebooks/01_ml_pipeline_orchestration.ipynb
   from the notebooks folder, cell by cell. Report each task's state and return value from steps 5
   and 7, and the default version after each. Make sure step 8 leaves the root task suspended.
4. Run the SQL queries under Verify in the README as COOKBOOK_ML_PIPELINE_ORCHESTRATION_ADMIN and
   report the results.
5. When I say so, run sql/99_teardown.sql and show that every SHOW at the end returns no rows.
Never drop or alter objects that do not start with COOKBOOK_.
```

## Related skills

- `snowflake-tasks` (bundled): creating, scheduling, monitoring, and troubleshooting tasks and task graphs, including config and return values. This recipe covers one ML retraining graph; that skill covers task graphs in general.
- `machine-learning` (bundled): training, registering, deploying, and monitoring models on Snowflake. Use it to extend the training or evaluation steps.

## References

- [Create a sequence of tasks with a task graph](/user-guide/tasks-graphs)
- [Managing Snowflake tasks and task graphs with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-tasks)
- [SYSTEM$SET\_RETURN\_VALUE](/sql-reference/functions/system_set_return_value)
- [SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](/sql-reference/functions/system_get_predecessor_return_value)
- [ALTER TASK](/sql-reference/sql/alter-task)
- [Creating stored procedures with Snowpark Python](/developer-guide/snowpark/python/creating-sprocs)
- [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview)
- [Using third-party packages from Anaconda](/developer-guide/udf/python/udf-python-packages)
