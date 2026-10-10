# Run ML Jobs with Code Bundles

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

For the availability of other Code Bundles features, see [Snowflake Code Bundles](/developer-guide/code-bundles/code-bundles).

Set `type: ml` in your `code_bundle.yml` to run a Code Bundle as a Snowflake ML Job on a compute pool. Snowflake starts
the job on the compute pool you name in the specification, injects a Snowpark session, and mounts your bundle’s files and
the result stage into the container.

This gives you a SQL-native way to run the same kind of training and data processing payload you’d otherwise submit with
the `snowflake-ml-python` job APIs. Because it’s a SQL statement, you can run it from any client that runs SQL, without installing
`snowflake-ml-python` on the submitting machine.

## Overview

When you run `EXECUTE CODE BUNDLE` on a bundle whose specification sets `type: ml`, Snowflake does the following:

1. Starts a job service on the compute pool named in `compute_options.compute_pool`, using a
   [Snowflake Container Runtime](/developer-guide/snowflake-ml/container-runtime-ml) image. `type: ml` requires Container
   Runtime 2.9.0 or later. For the available versions, see
   [Snowflake Container Runtime release notes](/developer-guide/snowflake-ml/container-runtime/releases).
2. Mounts the bundle’s committed version read-only at `/mnt/job_stage`. Your files are under `/mnt/job_stage/app/`.
3. Mounts the stage named in `properties.result_stage` at `/mnt/job_result`. This is where the ML Job’s return value is
   stored, so the field is required.
4. Runs the file you named in `ENTRYPOINT`, as a path relative to the payload root, with the `ARGUMENTS` you passed.
5. Blocks until the job reaches a terminal state. A payload that fails returns the failure as a SQL error.

`/mnt/job_stage` is a read-only mount of one committed bundle version, and `EXECUTE CODE BUNDLE` picks that version when
you submit the statement. So your payload can’t change underneath a running job, and adding a new version with
`ALTER CODE BUNDLE ... ADD VERSION` affects only later executions. See
[ALTER CODE BUNDLE](/developer-guide/code-bundles/code-bundles#alter-code-bundle).

Note

ML Code Bundles run on **compute pools**. Set `compute_type: compute_pool` in your specification. Warehouse compute isn’t
supported for `type: ml`.

### Choosing between Code Bundles and the Python API

Both interfaces run the same kind of payload on a compute pool. They differ in where the job definition lives
and how you submit it.

| Aspect | ML Code Bundle | [`snowflake-ml-python` job API](/developer-guide/snowflake-ml/ml-jobs/overview) |
| --- | --- | --- |
| Submission | `EXECUTE CODE BUNDLE` (SQL) | `submit_file()`, `submit_directory()`, `@remote` (Python) |
| Configuration | `code_bundle.yml` stored with the code | Keyword arguments at submission time |
| Payload | Versioned Code Bundle object | Uploaded to a stage on each submission |
| Orchestration | Snowflake CLI, any SQL client | Python clients, orchestration tools such as Apache Airflow |
| Return values | Stored on the stage in `properties.result_stage` | `job.result()` in the client |

Expand

Show lessSee more

Use a Code Bundle when you want the job definition versioned in Snowflake and driven from SQL. Use the Python API when
you want to submit from Python, pass Python objects, or read a return value back into your client.

## Prerequisites

- A compute pool to run the job on. For a multi-node job, its `MAX_NODES` must be at least the number of instances you
  request.
- [Snowflake Container Runtime](/developer-guide/snowflake-ml/container-runtime-ml) 2.9.0 or later. Snowflake uses the
  latest available version unless you pin one with `compute_options.runtime_version`. Earlier versions don’t support
  `type: ml`.
- A stage for the ML Job’s return value, named in `properties.result_stage`. Snowflake mounts it at `/mnt/job_result`.
- For the [quickstart](#label-ml-code-bundles-quickstart), a table named `MY_DB.MY_SCHEMA.MY_TRAINING_DATA` with numeric
  `FEATURE_A`, `FEATURE_B`, and `TARGET` columns.
- Privileges to create the bundle and run the job service. See [Access control](#label-ml-code-bundles-access-control).

### Access control

The role that runs the bundle needs everything listed under
[EXECUTE CODE BUNDLE](/developer-guide/code-bundles/code-bundles#execute-code-bundle). For a compute pool bundle, that means:

- `OWNERSHIP` or `USAGE` on the Code Bundle.
- `USAGE` or `OWNERSHIP` on the compute pool, and on the database and schema holding the bundle.
- `USAGE` and `MONITOR` on the query warehouse.
- `READ` or `OWNERSHIP` on any secrets the specification names. `USAGE` on a secret isn’t sufficient.
- `USAGE` or `OWNERSHIP` on any external access integrations and artifact repositories the specification names.

An ML Code Bundle also runs as a job service and mounts stages, so the role needs the schema privileges to create those
objects: `CREATE SERVICE` and `CREATE STAGE`. You also need read and write access to the stage
you name in `properties.result_stage`.

For general ML Jobs access control guidance, see
[Access control requirements for ML Jobs](/developer-guide/snowflake-ml/ml-jobs/access-control-requirements).

## Run your first ML Code Bundle

This example trains a model on a Snowflake table and returns its metrics.

1. **Write your payload.** Put your training script in the bundle, for example at `src/train.py`. Assign the value you
   want to keep to the special `__return__` variable. Snowflake writes that value to the result stage for you, so the
   payload doesn’t write result files itself.

   Copy code

   ```
   # src/train.py
   import argparse

   from snowflake.snowpark.context import get_active_session
   from sklearn.linear_model import LinearRegression

   def main():
       parser = argparse.ArgumentParser()
       parser.add_argument("--source-table", required=True)
       parser.add_argument("--tag", default="run")
       args = parser.parse_args()

       # Snowflake injects the session, so there are no credentials to manage.
       session = get_active_session()
       frame = session.table(args.source_table).to_pandas()

       features = frame[["FEATURE_A", "FEATURE_B"]]
       model = LinearRegression().fit(features, frame["TARGET"])

       return {
           "tag": args.tag,
           "r2": model.score(features, frame["TARGET"]),
           "intercept": model.intercept_,
       }

   if __name__ == "__main__":
       __return__ = main()
   ```
2. **Add a `code_bundle.yml` at the root of the bundle.**

   Copy code

   ```
   bundle:
     type: ml
     compute_type: compute_pool
     language: python

     compute_options:
       compute_pool: MY_COMPUTE_POOL
       query_warehouse: MY_WAREHOUSE

     properties:
       result_stage: '@MY_DB.MY_SCHEMA.MY_RESULT_STAGE'
       enable_metrics: true
   ```
3. **Upload the files to a stage.** Keep `code_bundle.yml` at the root of the stage and `train.py` under `src/`, so the
   stage mirrors the bundle layout. Run [PUT](/sql-reference/sql/put) from a client such as the Snowflake CLI or
   SnowSQL, from the directory that contains your files.

   Copy code

   ```
   CREATE STAGE IF NOT EXISTS MY_DB.MY_SCHEMA.MY_PAYLOAD_STAGE;

   PUT file://code_bundle.yml @MY_DB.MY_SCHEMA.MY_PAYLOAD_STAGE AUTO_COMPRESS = FALSE OVERWRITE = TRUE;
   PUT file://src/train.py @MY_DB.MY_SCHEMA.MY_PAYLOAD_STAGE/src AUTO_COMPRESS = FALSE OVERWRITE = TRUE;
   ```
4. **Create the Code Bundle.** The job mounts the bundle’s committed version, so create the bundle before you run it.

   Copy code

   ```
   CREATE OR REPLACE CODE BUNDLE MY_DB.MY_SCHEMA.MY_ML_BUNDLE
     FROM '@MY_DB.MY_SCHEMA.MY_PAYLOAD_STAGE';
   ```
5. **Run it.** The `ENTRYPOINT` is a path relative to the root of the bundle, not an absolute container path such as
   `/mnt/job_stage/app/src/train.py`. One bundle can hold several entrypoints, and you choose one on each
   `EXECUTE CODE BUNDLE`. An entrypoint that isn’t in the bundle fails at SQL compilation, before any compute starts.

   Copy code

   ```
   EXECUTE CODE BUNDLE MY_DB.MY_SCHEMA.MY_ML_BUNDLE
     ENTRYPOINT = 'src/train.py'
     ARGUMENTS = ('--source-table', 'MY_DB.MY_SCHEMA.MY_TRAINING_DATA', '--tag', 'single_node');
   ```

   The statement blocks until the job finishes. When it succeeds, the job’s return value is on your result stage:

   Copy code

   ```
   LIST @MY_DB.MY_SCHEMA.MY_RESULT_STAGE;
   ```

## Specification reference for `type: ml`

These fields have meanings specific to `type: ml`. For everything else in the file, see the
[`code_bundle.yml` reference](/developer-guide/code-bundles/code-bundle-yml-reference).

| Field | Required | Description |
| --- | --- | --- |
| `type` | Yes | Must be `ml` to run the bundle as an ML Job. |
| `compute_type` | Yes | Must be `compute_pool`. |
| `language` | Yes | Must be `python`. |
| `compute_options.compute_pool` | Yes | Compute pool that runs the job service. |
| `compute_options.query_warehouse` | Recommended | Warehouse used for SQL and Snowpark queries your payload issues. |
| `compute_options.runtime_version` | No | Container Runtime version, for example `'2.9.0'`. Requires 2.9.0 or later. Defaults to the latest available version. Always quote the value. |
| `compute_options.language_version` | No | Python version to run inside the image, for example `'3.10'`. Always quote the value. |
| `compute_options.target_instances` | No | Number of instances to request for a [multi-node job](#label-ml-code-bundles-multi-node-jobs). Defaults to 1. |
| `compute_options.min_instances` | No | Instances that must be ready before the payload starts. Defaults to `target_instances`. |
| `properties.result_stage` | Yes | Stage that holds the job’s return value, mounted at `/mnt/job_result`. Qualify it with at least a schema, for example `'@MY_DB.MY_SCHEMA.MY_STAGE'`. |
| `properties.enable_metrics` | No | Set to `true` to emit platform metrics for the job service. |
| `env_vars` | No | Environment variables to set in the container. |
| `external_access_integrations` | No | External access integrations to attach, for [network egress](#label-ml-code-bundles-installing-packages). |
| `artifact_repositories` | No | Artifact repositories to install packages from. See [Installing packages](#label-ml-code-bundles-installing-packages). |
| `stage_mounts` | No | Additional stages to mount, beyond the result stage. |

Expand

Show lessSee more

Note

`compute_options.runtime_version` for `type: ml` uses the Container Runtime version format (for example `'2.9.0'`), which
differs from the image tag format used by `type: custom` bundles on compute pools (for example `'V2.9-CPU-PY3.12'`). For
available versions, see [Snowflake Container Runtime release notes](/developer-guide/snowflake-ml/container-runtime/releases).

### Fields that don’t apply

The following aren’t supported with `type: ml`:

- `compute_type: warehouse`, and any `language` other than `python`.
- `properties.requirements_file`. To install packages, include a `requirements.txt` in your payload, as described in
  [Installing packages](#label-ml-code-bundles-installing-packages).

Note

Snowflake checks these `type: ml` rules when you run the bundle, not when you create it. `CREATE CODE BUNDLE` accepts a
specification that `EXECUTE CODE BUNDLE` then rejects with `Failed to load code bundle configuration`, so validate a new
specification by running it, not by creating it.

## Filesystem layout inside the job

| Path | Access | Contents |
| --- | --- | --- |
| `/mnt/job_stage` | Read-only | The bundle’s committed version. Your files are under `/mnt/job_stage/app/`. |
| `/mnt/job_result` | Read-write | The stage from `properties.result_stage`, where Snowflake writes the job’s return value. |

Expand

Show lessSee more

Writes to `/mnt/job_stage` are rejected, so treat your payload as immutable at runtime.

You own the file layout inside your payload. Snowflake mounts the bundle the way you committed it and doesn’t restructure
your files or rewrite paths, so resolve paths in your code the same way you would anywhere else.

You don’t write to `/mnt/job_result` yourself: Snowflake serializes the value your entrypoint assigns to `__return__`
there when the job finishes. To keep other artifacts, write them to Snowflake objects through the injected [Snowpark session](#label-ml-code-bundles-session), or
mount another stage with `stage_mounts`.

## Passing arguments and environment variables

`ARGUMENTS` takes the same argument list you’d pass as `args` to `submit_file()` or `submit_directory()` in the
[ML Job Python API](/developer-guide/snowflake-ml/ml-jobs/overview): a flat list of strings that reaches your script as
`sys.argv`, so `argparse` works as it does locally. Positional and flag arguments both work, in any order.

Copy code

```
EXECUTE CODE BUNDLE MY_DB.MY_SCHEMA.MY_ML_BUNDLE
  ENTRYPOINT = 'src/train.py'
  ARGUMENTS = ('--source-table', 'MY_DB.MY_SCHEMA.MY_TRAINING_DATA', '--tag', 'nightly');
```

That’s the SQL equivalent of `args=["--source-table", "MY_DB.MY_SCHEMA.MY_TRAINING_DATA", "--tag", "nightly"]`.
Pass each flag and its value as separate list items, the same way you would in Python.

Environment variables come from `env_vars` in the specification:

Copy code

```
bundle:
  type: ml
  compute_type: compute_pool
  language: python

  compute_options:
    compute_pool: MY_COMPUTE_POOL
    query_warehouse: MY_WAREHOUSE

  properties:
    result_stage: '@MY_DB.MY_SCHEMA.MY_RESULT_STAGE'

  env_vars:
    - CB_RUN_LABEL: nightly
    - PYTHONWARNINGS: ignore
```

## Using the Snowpark session

The session works the same way it does in any ML Job. See
[Accessing Snowpark Session in ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview#label-snowflake-ml-job-snowpark-session).
Snowflake makes a Snowpark session available in the execution context, so your payload doesn’t handle credentials:

Copy code

```
from snowflake.snowpark.context import get_active_session

session = get_active_session()
session.sql("SELECT CURRENT_VERSION()").collect()
```

`Session.builder.getOrCreate()` returns the same session, so a payload you already run as an ML Job needs no change. The
injected-parameter form on that page is for function dispatch, so it doesn’t apply here: a Code Bundle entrypoint is
always a file.

Use the session to read tables, write results back to Snowflake, and log models to the
[model registry](/developer-guide/snowflake-ml/model-registry/overview) from inside the job, the same as in an ML Job.

## Multi-node jobs

Set `target_instances` to run the job on more than one instance, and `min_instances` to set how many instances have to be
ready before your payload starts. Snowflake starts a Ray cluster across the instances and runs your entrypoint on the head
instance, so you distribute work from there the same way you would in any ML Job. See
[Snowflake Multi-Node ML Jobs](/developer-guide/snowflake-ml/ml-jobs/distributed-ml-jobs).

## Installing packages

If your payload needs a package that isn’t already in the Container Runtime image, include a `requirements.txt` file in the root of your payload,
next to `code_bundle.yml`. Snowflake installs it before your entrypoint runs, which is the same behavior as
`pip_requirements` in the Python job APIs. The `properties.requirements_file` field doesn’t apply to `type: ml`. Name a
package source in your specification so the package index is reachable from inside the job.

**From an artifact repository** (no external network access needed):

Copy code

```
bundle:
  type: ml
  compute_type: compute_pool
  language: python

  compute_options:
    compute_pool: MY_COMPUTE_POOL
    query_warehouse: MY_WAREHOUSE

  properties:
    result_stage: '@MY_DB.MY_SCHEMA.MY_RESULT_STAGE'

  artifact_repositories:
    - snowflake.snowpark.pypi_shared_repository
```

`snowflake.snowpark.pypi_shared_repository` is Snowflake’s built-in PyPI repository, and it supports
[package policies](/developer-guide/udf/python/packages-policy). You can also name a
[customer-hosted artifact repository](/developer-guide/udf/python/customer-hosted-python-artifact-repositories), and you
can list more than one. The Anaconda repository (`snowflake.snowpark.anaconda_shared_repository`) can’t be used on compute
pools.

**Over external network access**, attach an
[external access integration](/developer-guide/external-network-access/creating-using-external-network-access) instead:

Copy code

```
bundle:
  external_access_integrations:
    - PYPI_EAI
```

An external access integration also governs any network calls your payload makes while it runs, not just package installs.

## Monitor a job

Code Bundles only change how you submit the job. Once it’s running, it’s an ML Job like any other, so monitor and debug it
the way you would any ML Job: see [Ray Dashboard in ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview#label-snowflake-ml-job-management).

`EXECUTE CODE BUNDLE` is synchronous, and a payload that raises an exception or exits non-zero surfaces as a SQL error. To
submit without blocking your client, run the statement asynchronously, as shown in
[Async execution](/developer-guide/code-bundles/code-bundles#async-execution). To cancel a run, cancel the query that
submitted it. For a history of bundle runs, use the
[CODE\_BUNDLE\_HISTORY](/developer-guide/code-bundles/code-bundles#code_bundle_history) table function.
