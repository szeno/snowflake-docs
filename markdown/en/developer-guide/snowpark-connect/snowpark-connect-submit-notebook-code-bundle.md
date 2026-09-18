# Submit Spark notebooks (Code Bundles)

You can run an existing Spark notebook (`.ipynb`) on Snowflake as a batch job, without rewriting it into a `.py`
script. This guide describes how to launch a notebook programmatically
through the Code Bundle API, with SQL (`EXECUTE CODE BUNDLE`) or the REST API, so that you can run it from a worksheet,
from a [Snowflake task](/developer-guide/code-bundles/code-bundles#scheduling-with-tasks), or from an external
orchestrator. Each run returns a job ID that you use to track, monitor, and cancel it.

Everything that is not specific to Spark works the same as for any notebook run as a Code Bundle: compute setup, package
management, secrets, scheduling, parameters, and observability. This page links to those general guides and concentrates
on the parts that are specific to Spark notebooks and to the programmatic API. For the general model, see
[Run and schedule Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule).

Note

Running notebooks as Code Bundles on a compute pool (Snowpark Container Services) is generally available. The inline
`WITH SPECIFICATION` override used in the SQL and REST paths below is in Public Preview.

## Prerequisites

Before you submit a notebook, make sure you have:

- The Spark notebook in a [Snowflake Workspace](/developer-guide/snowpark-connect/snowpark-connect-snowflake-workspaces),
  or deployed to a stage for CI/CD (see [Promote from Git (CI/CD)](#from-stage)).
- A compute pool to run the notebook on, and a warehouse for the SQL the notebook issues against Snowflake. For how to
  choose and size compute, see [Compute setup for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-compute-setup).

The role that submits the job needs:

- `USAGE` on the compute pool that runs the notebook.
- `USAGE` on the warehouse set as `query_warehouse`.
- `CREATE CODE BUNDLE` on the schema where the bundle is created, and `USAGE` or `OWNERSHIP` on the bundle to execute it.

## Bring your notebook

The notebook must be a [Snowpark Connect application](/developer-guide/snowpark-connect/snowpark-connect-overview): it
initializes a Snowpark Connect session and then uses the Spark API against Snowflake compute. For how to write one, see
[Run Spark workloads on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-overview) and
[Spark application examples](/developer-guide/snowpark-connect/snowpark-connect-samples). Initialize the session near the
top of the notebook:

Copy code

```
import snowflake.snowpark_connect

spark = snowflake.snowpark_connect.init_spark_session()
```

When you develop a notebook interactively, it runs against whatever database and schema your session has selected with
`USE DATABASE` and `USE SCHEMA`. A Code Bundle run is non-interactive and does not inherit that interactive context, so
an unqualified table or view name may not resolve the way it did during development. Reference Snowflake objects by
their fully-qualified names (`database.schema.object`) so the notebook runs consistently regardless of session context.

## Run with SQL

Use SQL to run a notebook from a worksheet, wrap it in a task, or drive it from an external orchestrator. First create a
named Code Bundle from the notebook source, which can be a workspace version or a stage location:

Copy code

```
CREATE OR REPLACE CODE BUNDLE my_db.my_schema.scos_nb_bundle
  FROM 'snow://workspace/USER$.my_schema."my_workspace"/versions/last';
```

Then run the bundle, passing the notebook entrypoint and the specification that selects the compute pool. The statement
runs synchronously and returns when the notebook finishes; its query ID is the job ID.

Copy code

```
EXECUTE CODE BUNDLE my_db.my_schema.scos_nb_bundle
  ENTRYPOINT = 'scos_nb.ipynb'
  WITH SPECIFICATION $$
bundle:
  type: custom
  compute_type: compute_pool
  language: python
  compute_options:
    compute_pool: my_compute_pool
    query_warehouse: my_warehouse
    runtime_version: "V2.9-CPU-PY3.12"
$$;
```

Check the run by its query ID in [`CODE_BUNDLE_HISTORY`](/developer-guide/code-bundles/code-bundles), and read whatever
the notebook wrote:

Copy code

```
SELECT query_id, status, execution_name
  FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(BUNDLE_NAME => NULL))
  WHERE query_id = '<job_id>';
```

For the full `EXECUTE CODE BUNDLE` syntax, see [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle) and
[CREATE CODE BUNDLE](/sql-reference/sql/create-code-bundle).

## Run with the REST API

You can run a notebook entirely over REST: create the named Code Bundle, then execute it by name.

Create the bundle from the notebook source (a workspace version or a stage) with the create endpoint. Set `createMode`
to `orReplace` to replace an existing bundle of the same name:

```
POST /api/v2/databases/{database}/schemas/{schema}/code-bundles?createMode=orReplace
```

Copy code

```
{
  "name": "scos_nb_bundle",
  "from_location": "@my_db.my_schema.my_stage/notebooks"
}
```

Then execute the bundle by name, passing the `entrypoint`, an optional `execution_name`, and the inline `specification`
(the same `bundle` object you use in the SQL `WITH SPECIFICATION` clause, passed as a JSON object):

```
POST /api/v2/databases/{database}/schemas/{schema}/code-bundles/{name}:execute?asyncExec=true
```

Copy code

```
{
  "entrypoint": "scos_nb.ipynb",
  "execution_name": "scos_nb_run",
  "specification": {
    "bundle": {
      "type": "custom",
      "compute_type": "compute_pool",
      "language": "python",
      "compute_options": {
        "compute_pool": "my_compute_pool",
        "query_warehouse": "my_warehouse",
        "runtime_version": "V2.9-CPU-PY3.12"
      }
    }
  }
}
```

With `asyncExec=true`, the call returns `202` with a `job_id` (the run’s query ID). Poll the run’s status with the
execution endpoint:

```
GET /api/v2/code-bundle-executions/{job_id}
```

For authentication and the request headers that set the run’s context, see the REST section of
[Submit Spark jobs on Snowflake (via Code Bundles)](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle#submit-with-rest).

## Parameterize a run

Pass values into a run with `ARGUMENTS` so one notebook can drive different environments, dates, or tables without
editing code. Each argument is a string; Snowflake places them in the notebook’s `sys.argv` list, where `sys.argv[0]` is
the notebook name and `sys.argv[1]` is your first argument.

Copy code

```
EXECUTE CODE BUNDLE my_db.my_schema.scos_nb_bundle
  ENTRYPOINT = 'scos_nb.ipynb'
  ARGUMENTS = ('prod')
  WITH SPECIFICATION $$
bundle:
  type: custom
  compute_type: compute_pool
  language: python
  compute_options:
    compute_pool: my_compute_pool
    query_warehouse: my_warehouse
    runtime_version: "V2.9-CPU-PY3.12"
$$;
```

Read the value in the notebook:

Copy code

```
import sys

env = sys.argv[1]  # 'prod'  (sys.argv[0] is the notebook name)
print("running for env:", env)
```

For more ways to read and process parameters, see
[Running notebooks with parameters](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-parameters).

## Manage packages and the Snowpark Connect version

A notebook runs on a Container Runtime image, which you select with `compute_options.runtime_version` in the
[notebook specification](#specification). That image ships a base set of packages, including a pinned `snowpark-connect`
client. Importing `snowflake.snowpark_connect` in your notebook uses that pinned version. To check it:

Copy code

```
import importlib.metadata
print(importlib.metadata.version("snowpark-connect"))
```

A compute pool has no outbound internet access by default, so there are two supported ways to add or upgrade packages
(including a newer `snowpark-connect`): a declarative requirements file served by a Snowflake artifact repository
(recommended), or an in-notebook `pip install` backed by an external access integration. For the general treatment of
packages and runtimes, see
[Managing packages and runtime](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-packages-runtime)
and [Using artifact repositories](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-artifact-repositories).

### Requirements file with an artifact repository (recommended)

Package a `requirements.txt` in the bundle alongside the notebook and install from the Snowflake-managed repository
`snowflake.snowpark.pypi_shared_repository`, which proxies PyPI from inside Snowflake. No external access integration is
required, and the packages are resolved before the notebook runs.

`requirements.txt`, packaged in the bundle:

```
snowpark-connect==1.42.0
```

Reference the repository and the requirements file in the specification:

Copy code

```
EXECUTE CODE BUNDLE my_db.my_schema.scos_nb_bundle
  ENTRYPOINT = 'scos_nb.ipynb'
  WITH SPECIFICATION $$
bundle:
  type: custom
  compute_type: compute_pool
  language: python
  artifact_repositories:
    - snowflake.snowpark.pypi_shared_repository
  compute_options:
    compute_pool: my_compute_pool
    query_warehouse: my_warehouse
    runtime_version: "V2.9-CPU-PY3.12"
  properties:
    requirements_file: "requirements.txt"
$$;
```

The requested packages are installed for the run, and importing `snowflake.snowpark_connect` uses the upgraded release.
Omit the version to install the latest release the repository carries. Keep these constraints in mind:

- `requirements_file` must be a **bundle-relative path** to a file packaged in the notebook bundle (for example,
  `requirements.txt`). A `@stage/...` URL is not supported for `compute_pool` bundles.
- Declare `artifact_repositories` explicitly. It does not default to the shared repository; a requirements file with no
  repository declared fails because the pool has no reachable package source.

### In-notebook pip install with an external access integration

For ad hoc installs, `pip install` in the notebook after attaching an
[external access integration](/developer-guide/external-network-access/creating-using-external-network-access) that
allows `pypi.org` and `files.pythonhosted.org`. Add it at the **top level** of the specification (under `bundle`, not
under `compute_options`):

Copy code

```
EXECUTE CODE BUNDLE my_db.my_schema.scos_nb_bundle
  ENTRYPOINT = 'scos_nb.ipynb'
  WITH SPECIFICATION $$
bundle:
  type: custom
  compute_type: compute_pool
  language: python
  external_access_integrations:
    - pypi_access_integration
  compute_options:
    compute_pool: my_compute_pool
    query_warehouse: my_warehouse
    runtime_version: "V2.9-CPU-PY3.12"
$$;
```

Then install and verify in the notebook, before you initialize the session:

Copy code

```
!pip install --upgrade snowpark-connect

import importlib.metadata
print(importlib.metadata.version("snowpark-connect"))
```

## Schedule the notebook

To run the notebook on a cadence, wrap the `EXECUTE CODE BUNDLE` statement in a
[Snowflake task](/developer-guide/code-bundles/code-bundles#scheduling-with-tasks). Tasks let you chain notebooks into
dependency graphs and run them natively in Snowflake, without operating a separate scheduler.

Copy code

```
CREATE OR REPLACE TASK my_db.my_schema.scos_nb_task
  WAREHOUSE = my_warehouse
  SCHEDULE = 'USING CRON 0 9 * * * America/Los_Angeles'
AS
  EXECUTE CODE BUNDLE my_db.my_schema.scos_nb_bundle
    ENTRYPOINT = 'scos_nb.ipynb';

ALTER TASK my_db.my_schema.scos_nb_task RESUME;
```

If you prefer to schedule from Snowsight without writing SQL, open the notebook in your workspace and use its scheduled
runs. For the full UI walkthrough, including deploying edits and managing the schedule, see
[Run and schedule Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule).

## Monitor a run

Every run is tracked by its query ID (the job ID). Look up status and errors in `CODE_BUNDLE_HISTORY`:

Copy code

```
SELECT query_id, status, error_message, start_time, end_time
  FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(BUNDLE_NAME => NULL))
  WHERE query_id = '<job_id>';
```

`STATUS` is `DONE` on success or `FAILED` on error, and `ERROR_MESSAGE` carries the failure detail, including the
traceback for a failed run.

You can also monitor runs over the Code Bundle REST API. `GET /api/v2/code-bundle-executions` lists executions
(filterable by bundle name, entrypoint, or query ID), and `GET /api/v2/code-bundle-executions/{executionId}` returns the
status of a single run. For the endpoint details, see [Submit Spark jobs on Snowflake (via Code Bundles)](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle#submit-with-rest).

The notebook’s log output (`print` statements, logger output, and stack traces) is ingested into the event table
configured for the run’s session database, falling back to your account’s event table if that database has none. Logs
can take a few minutes to appear. For querying logs and traces, see
[Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).

## Promote from Git (CI/CD)

For production, keep the notebook under version control and let a CI/CD pipeline promote it. Develop in a
[Git-backed workspace](/user-guide/ui-snowsight/workspaces-git) or your own IDE, then have your pipeline deploy the
`.ipynb` to a stage and create (or version) the Code Bundle from that stage. The `FROM` source is the only thing that
changes; the `EXECUTE CODE BUNDLE` step and specification are identical to the workspace path.

Copy code

```
PUT file://scos_nb.ipynb @my_db.my_schema.my_stage/notebooks/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

CREATE OR REPLACE CODE BUNDLE my_db.my_schema.scos_nb_bundle
  FROM '@my_db.my_schema.my_stage/notebooks';
```

On later changes, add a new version instead of recreating the bundle:

Copy code

```
ALTER CODE BUNDLE my_db.my_schema.scos_nb_bundle
  ADD VERSION FROM '@my_db.my_schema.my_stage/notebooks';
```

For the end-to-end CI/CD walkthrough, see
[Scheduling workflows by scenario](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-workflow-scenarios).

## Notebook specification

A notebook runs as a `type: custom` Code Bundle (not `type: spark`) on a compute pool. Running a notebook on a warehouse
is not supported; warehouse bundles take `.py` entrypoints only. Set the following fields in the specification:

| Field | Value |
| --- | --- |
| `type` | `custom` |
| `compute_type` | `compute_pool` |
| `language` | `python` |
| `compute_options.compute_pool` | The compute pool that runs the notebook. |
| `compute_options.query_warehouse` | The warehouse used for SQL the notebook issues against Snowflake. |
| `compute_options.runtime_version` | The Container Runtime image version (for example, `"V2.9-CPU-PY3.12"`). |

Expand

Show lessSee more

Note

For a notebook, `compute_options.runtime_version` selects the **Container Runtime image**, not the Snowpark Connect
client version. This is different from a warehouse Spark job, where `runtime_version` selects the
[`snowpark-connect`](/release-notes/clients-drivers/snowpark-connect-2026) client version. To control the Snowpark
Connect version in a notebook, see [Manage packages and the Snowpark Connect version](#control-scos-version).
