# Run an experiment to compare and select models

With Snowflake ML Experiments, you can set up *experiments*, organized evaluations of the results of model training. This allows you to quickly compare the results of hyperparameter adjustment, different target metrics, and behavior of different model types in an organized fashion in order to select the best model for your needs. Each experiment consists of a series of *runs*, which are metadata and artifacts from your training. Snowflake is unopinionated about your run artifacts – you can submit anything that’s useful for your model evaluation process.

After you complete an experiment, the results are visible through Snowsight. You can also retrieve run artifacts at any time in Python or SQL.

Note

Snowflake Experiments require `snowflake-ml-python` version 1.19.0 or later.

## Access control requirements

Creating an experiment requires the CREATE EXPERIMENT privilege on the schema where run artifacts are stored, plus USAGE or any other privilege on the parent database and schema.

## Create an experiment

First, create an experiment. This requires an existing database and schema, used to store run information.

Snowsight

1. In the navigation menu, select **AI & ML** » **Experiments**.
2. Select **New Experiment**.
3. Enter the **Name** of your experiment.
4. Select the database and schema to store your experiment’s run artifacts in.
5. Select **Create** to create the experiment, or **Cancel** to cancel.

## Start an experiment run

Each run in an experiment has its own set of metrics, parameters, and artifacts. This information is used in Snowsight to provide visualizations and data about your model training and its results.

Start a run with the `start_run(name: Optional[str])` method on your `ExperimentTracking` instance. This returns a new `Run`, which supports use in a `with` statement. Snowflake recommends that you use `with` statements, so that runs are cleanly completed and it’s easier to reason about run scope.

Copy code

```
with exp.start_run("my_run"):
  # .. Train your model and log artifacts
```

### Automatically log training information

You can autolog training information for XGBoost, LightGBM, or Keras models during model training. Autologging is performed by registering a callback which refers to your experiment and information about the model you’re training. Each time a method is called on your `Model` instance which adjusts a parameter or metric, it’s automatically logged to your experiment for the active run.

The following example shows how to configure your experiment’s callbacks for each supported model trainer and then start a basic training run to log artifacts.

LightGBMKeras

Copy code

```
# exp: ExperimentTracking

from lightgbm import LGBMClassifier

from snowflake.ml.experiment.callback.lightgbm import SnowflakeLightgbmCallback
from snowflake.ml.model.model_signature import infer_signature

sig = infer_signature(X, y)
callback = SnowflakeLightgbmCallback(
    exp, model_name="name", model_signature=sig
)
model = LGBMClassifier()
with exp.start_run("my_run"):
    model.fit(X, y, eval_set=[(X, y)], callbacks=[callback])
```

Copy code

```
# exp: ExperimentTracking

import keras

from snowflake.ml.experiment.callback.keras import SnowflakeKerasCallback
from snowflake.ml.model.model_signature import infer_signature

sig = infer_signature(X, y)
callback = SnowflakeKerasCallback(
    exp, model_name="name", model_signature=sig
)
model = keras.Sequential()
model.add(keras.layers.Dense(1))
model.compile(
    optimizer=keras.optimizers.RMSprop(learning_rate=0.1),
    loss="mean_squared_error",
    metrics=["mean_absolute_error"],
)
with exp.start_run("my_run"):
    model.fit(X, y, validation_split=0.5, callbacks=[callback])
```

### Manually log training information and artifacts

For models which don’t support automatic logging or are pre-trained, you can manually log experiment information and upload artifacts in Python. Parameters are constant inputs to the training model, while metrics are evaluated at a model *step*. You can choose to represent a training epoch as a corresponding step. The following example shows how to log parameters, log metrics, and upload artifacts.

Note

The default step value is `0`.

Copy code

```
# Logging requires an active run for the exp: ExperimentTracker instance.

# Log model parameters with the log_param(...) or log_params(...) methods
exp.log_param("learning_rate", 0.01)
exp.log_params({"optimizer": "adam", "batch_size": 64})

# Log model metrics with the log_metric(...) or log_metrics(...) methods
exp.log_metric("loss", 0.3, step=100)
exp.log_metrics({"loss": 0.4, "accuracy": 0.8}, step=200)

# Log your model to the experiment's model registry with the log_model(...) method.
exp.log_model(model, model_name="my_model", signatures={"predict": model_signature})
exp.log_model(model, model_name="my_model", sample_input_data=data)

# Log local artifacts to an experiment run with the log_artifact(...) method.
exp.log_artifact('/tmp/file.txt', artifact_path='artifacts')
```

### Log stdout and stderr output

When a run is active on a Snowflake Notebook or any other SPCS workload such as ML Jobs, you can log the stdout and stderr output as part of your run. To enable live logging, call the following method:

Copy code

```
experiment.set_live_logging_status(True)
```

When live logging is enabled, stdout and stderr output from the notebook is written to the Snowflake default [event table](/developer-guide/logging-tracing/event-table-setting-up). To view the captured output, go to the Experiments UI and select the run. The output is displayed in the **Logs** tab.

Please note that this feature does not work with legacy notebooks.

## Complete a run

Completing a run makes it immutable and records its final status in Snowsight.

If you started a run as part of a `with` statement, the run is automatically completed when exiting scope. If the scope exits normally, the run’s status is set to `FINISHED`. If the scope exits because of an exception, the run’s status is set to `FAILED`.

Otherwise, you can end a run by calling your experiment’s `end_run(run_name: Optional[str], status: Optional[str])` method with the name of the run to complete. Use the optional `status` argument to set the run’s final status to `FINISHED`, `FAILED`, or `CANCELLED`. If you don’t specify a status, the run is set to `FINISHED`.

Copy code

```
exp.end_run("my_run")

# Mark a run that you stopped early as cancelled
exp.end_run("my_other_run", status="CANCELLED")
```

### Pause and resume a run

You can pause a run to stop logging to it temporarily, and resume it later. Pausing the active run deactivates it, so a surrounding `with` statement doesn’t complete the run when it exits scope. To pause a run, call the `pause_run(run_name: Optional[str])` method. If you don’t specify a run name, the active run is paused.

To resume a paused run, call `start_run` with the name of the paused run:

Copy code

```
with exp.start_run("my_run"):
  # .. Train your model and log artifacts
  exp.pause_run()

# Later, resume the run and continue logging
with exp.start_run("my_run"):
  # .. Continue training
```

You can’t log metrics, parameters, or artifacts to a paused run. Resume the run first.

### Run statuses

Each run has one of the following statuses:

| Status | Description |
| --- | --- |
| `RUNNING` | The run is active. This is the only status that accepts new metrics, parameters, and artifacts. New runs start with this status. |
| `PAUSED` | The run is paused. Call `start_run` with the run’s name to return it to `RUNNING`. |
| `FINISHED` | The run completed successfully. |
| `FAILED` | The run failed, either because its `with` statement exited with an exception or because it was ended with `status="FAILED"`. |
| `CANCELLED` | The run was ended with `status="CANCELLED"`. |

Expand

Show lessSee more

`FINISHED`, `FAILED`, and `CANCELLED` are final statuses. A run with a final status can’t be modified or resumed.

## Compare runs within an experiment

Experiment evaluation is done through Snowsight. In the navigation menu, select **AI & ML** » **Experiments** and select your experiment to examine from the list.

The runs list displays **Run name**, **Status**, **Created** date, and a column for each metric. You can also toggle parameters as additional columns. View more details, such as artifacts, metric charts, and linked model versions from the run view and run comparison views.

Note

Viewing linked model versions is part of the [Model Lineage feature](/developer-guide/snowflake-ml/ml-lineage), which is only available for customers on Enterprise Edition and above.

You can select up to five runs in your experiment. To compare runs, select the **Compare** button. You’re presented with the comparison view, which displays run metadata, parameters, metrics, and model version information.

## Search and filter runs

You can programmatically search and filter runs using the `list_metrics` and `list_params` methods. Each method
returns a Snowpark DataFrame with one row per run: `list_metrics` includes a `run_name` column and one float column
per logged metric, while `list_params` includes a `run_name` column and one string column per logged parameter.

Because the results are Snowpark DataFrames, you can join, filter, and sort them using Snowpark expressions, or convert
them to pandas for local analysis.

pandas

Copy code

```
from snowflake.ml.experiment import ExperimentTracking

exp = ExperimentTracking(session)
exp.set_experiment("my_experiment")

run_names = ["RUN_1", "RUN_2"]

metrics_df = exp.list_metrics().to_pandas()
params_df  = exp.list_params().to_pandas()
runs_df    = metrics_df.merge(params_df, on="run_name")

results = runs_df[
  (runs_df["run_name"].isin(run_names))
  & (runs_df["loss"] > 0.3)
  & (runs_df["f1 score"] < 0.5)
  & (runs_df["model"].str.startswith("GPT"))
]

print(results)
```

You can also retrieve metrics or parameters for a single run by passing a `run_name` argument:

Copy code

```
single_run_metrics = exp.list_metrics(run_name="RUN_1")
```

## Retrieve artifacts from a run

At any time during or after a run, you can retrieve artifacts. The following example shows how to list a run’s available artifacts in the `logs` path, and download the `logs/log0.txt` artifact for the run `my_run` in the experiment `my_experiment` to the local directory `/tmp`:

SQL

Copy code

```
LIST snow://experiment/my_experiment/versions/my_run/logs;
GET snow://experiment/my_experiment/versions/my_run/logs/log0.txt file:///tmp;
```

## Delete runs and experiments

After finishing an experiment, you can remove it and all of its associated run artifacts. The following example removes the experiment `my_experiment`:

SQL

Copy code

```
DROP EXPERIMENT my_experiment;
```

You can also remove an individual run from an experiment. The following example removes the run `my_run` from the experiment `my_experiment`:

SQL

Copy code

```
ALTER EXPERIMENT my_experiment DROP RUN my_run;
```

## Limitations

Snowflake Experiments are subject to the following limitations:

- Runs are limited to 1000 unique parameters, with a combined total of 250,000 characters across all parameters.

## Cost considerations

There is no additional cost to use Snowflake Experiments. It incurs standard Snowflake consumption-based costs. These include the following:

- Cost of storing run artifacts. For general information about storage costs, see [Exploring storage cost](/user-guide/cost-exploring-data-storage).
- Cost of visualizing data. The charts in the UI are powered by virtual warehouses. For more information, see [Viewing credit usage](/user-guide/cost-exploring-compute#label-cost-exploring-viewing-credit-usage).
