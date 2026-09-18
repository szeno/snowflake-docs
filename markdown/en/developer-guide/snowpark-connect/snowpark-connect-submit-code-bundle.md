# Submit Spark jobs on Snowflake (via Code Bundles)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Run your Spark applications as batch jobs on Snowflake. You submit a job, Snowflake runs it on Snowflake compute, and
you get back an ID that you use to track, monitor, and cancel the run.

Note

Submitting Spark jobs as Code Bundles is the recommended way to run batch Spark workloads on Snowflake. Jobs run
directly on warehouse compute, so there’s no need to provision or manage a Snowpark Container Services compute pool. You
submit with a synchronous SQL statement ([`EXECUTE CODE BUNDLE`](#submit-with-sql)) that integrates natively with
[Snowflake tasks](/developer-guide/code-bundles/code-bundles#scheduling-with-tasks), or with the
[REST API](#submit-with-rest), which external orchestrators such as Apache Airflow and CI/CD systems can call to submit
and poll jobs.

## Overview

A Spark job runs your packaged Spark application (a `.jar` or `.py` on a stage) as a single batch run on warehouse
compute and returns a job ID you use to [monitor and manage the run](#monitor-and-manage).

This guide focuses on submitting a complete job in a single call: you pass the application, entrypoint, arguments, and
[specification](#specification-reference) (language, runtime version, and dependencies) inline with the request, so
nothing has to be created in advance. You can make that call two ways:

- [Submit a job with the REST API](#submit-with-rest): synchronous, or asynchronous with `asyncExec=true`. Recommended
  for orchestrating from CI/CD systems and data pipelines such as Apache Airflow.
- [Submit a job with SQL](#submit-with-sql): a synchronous `EXECUTE CODE BUNDLE` statement that integrates natively with
  [Snowflake tasks](/developer-guide/code-bundles/code-bundles#scheduling-with-tasks) for scheduled Spark pipelines.

You can also [persist a job definition](#persist-a-job-definition) as a named Code Bundle once and then rerun it by
name from either the REST API or SQL.

## Supported languages and runtimes

| Language | `language` | Entrypoint |
| --- | --- | --- |
| Scala (JVM) | `scala` (or `java`) | Fully-qualified main class (for example, `com.example.MySparkApp`) |
| Python | `python` | Python file name (for example, `main.py`) |

Expand

Show lessSee more

For accepted runtime version and language runtime values, see
[Job specification reference](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle-specification).

## Prerequisites

Before you submit a Spark job, make sure you have:

- A warehouse to run the job on.
- A stage containing your packaged application (a fat JAR or `.py` file) and any dependencies. To develop and package an
  application, see [Run Spark workloads on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-overview) and
  [Spark application examples](/developer-guide/snowpark-connect/snowpark-connect-samples).

The role that submits the job (the session role for SQL, or the role in the `X-Snowflake-Role` header for REST) needs
the following privileges:

- `USAGE` on the warehouse that runs the job.
- Read access to the stage that holds your application and dependencies.
- `USAGE` or `OWNERSHIP` on any [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access)
  and artifact repositories referenced in the specification.
- `READ` or `OWNERSHIP` on any [secrets](/sql-reference/sql/create-secret) referenced in the specification. (`USAGE` on a
  secret is not sufficient.)

To reuse a [persisted job definition](#persist-a-job-definition), also grant `CREATE CODE BUNDLE` on the schema and
`USAGE` or `OWNERSHIP` on the stored Code Bundle:

Copy code

```
GRANT CREATE CODE BUNDLE ON SCHEMA my_db.my_schema TO ROLE developer_role;
GRANT USAGE ON CODE BUNDLE my_db.my_schema.my_spark_job TO ROLE data_engineer_role;
```

## Quickstart

This is the shortest path to running a packaged Spark application and checking its result. It uses SQL
(`EXECUTE CODE BUNDLE`); to submit from an external orchestrator instead, see
[Submit a job with the REST API](#submit-with-rest).

1. Package your application as a fat JAR (Scala/Java) or a `.py` file, and upload it to a stage. For a Scala or Java
   application, note the fully-qualified main class.

   Copy code

   ```
   -- Scala/Java
   PUT file://target/scala-2.12/my-app_2.12-1.0.0.jar @my_db.my_schema.my_stage/spark_jobs/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

   -- Python
   PUT file://job.py @my_db.my_schema.my_stage/python_jobs/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
   ```
2. Set your session warehouse and submit the job. The statement runs synchronously and returns when the job finishes;
   its query ID is the job ID.

   Copy code

   ```
   USE WAREHOUSE my_warehouse;

   EXECUTE CODE BUNDLE FROM '@my_db.my_schema.my_stage/spark_jobs/my-app_2.12-1.0.0.jar'
     ENTRYPOINT = 'com.example.MySparkApp'
     WITH SPECIFICATION $$
   bundle:
     type: spark
     compute_type: warehouse
     language: scala
     compute_options:
       language_version: "2.12"
   $$;
   ```
3. Check the run’s status and logs, by its job ID, in `CODE_BUNDLE_HISTORY` or the event table. See
   [Monitor and manage jobs](#monitor-and-manage).

For all specification fields, see the [Spark job specification reference](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle-specification).

## Submit a job with the REST API

Submit a Spark job by posting the job definition to the Code Bundle executions endpoint. This is the recommended option
for orchestrating Spark job pipelines from external orchestrators such as Apache Airflow and other clients such as
CI/CD and custom UIs.

### Endpoint

```
POST /api/v2/code-bundle-executions
```

By default the call is synchronous and returns when the run finishes. To submit asynchronously, set the `asyncExec`
query parameter to `true`; the call returns immediately with a job ID that you poll for status.

```
POST /api/v2/code-bundle-executions?asyncExec=true
```

### Request headers

Authenticate with any authentication method supported by the Snowflake REST API. Set the `Authorization` header, and
for token-based methods the `X-Snowflake-Authorization-Token-Type` header:

| Authentication method | `Authorization` | `X-Snowflake-Authorization-Token-Type` |
| --- | --- | --- |
| [Key-pair JWT](/user-guide/key-pair-auth) | `Bearer <jwt>` | `KEYPAIR_JWT` |
| [Programmatic access token](/user-guide/programmatic-access-tokens) | `Bearer <token>` | `PROGRAMMATIC_ACCESS_TOKEN` |
| [OAuth](/user-guide/oauth-intro) | `Bearer <token>` | `OAUTH` |

Expand

Show lessSee more

Each request runs in a new session, so set the run’s context with the `X-Snowflake-Warehouse`, `X-Snowflake-Database`,
`X-Snowflake-Schema`, and `X-Snowflake-Role` headers. If you omit a header, the value falls back to the authenticating
user’s default (`DEFAULT_WAREHOUSE` for the warehouse, `DEFAULT_NAMESPACE` for the database and schema). A Spark job
needs a warehouse, database, and schema to start, so make sure each is supplied either by a header or by a user default.

The following example authenticates with a key-pair JWT and supplies the session context in headers:

Copy code

```
curl -X POST \
  "https://<account_identifier>.snowflakecomputing.com/api/v2/code-bundle-executions?asyncExec=true&requestId=5f3f8b16-1d2c-4b9a-9c2a-7c0d2a3b4c5d" \
  -H "Authorization: Bearer ${SNOWFLAKE_TOKEN}" \
  -H "X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "User-Agent: myApplicationName/1.0" \
  -H "X-Snowflake-Role: MY_ROLE" \
  -H "X-Snowflake-Warehouse: MY_SUBMIT_WAREHOUSE" \
  -H "X-Snowflake-Database: MY_DB" \
  -H "X-Snowflake-Schema: MY_SCHEMA" \
  -d @request-body.json
```

### Idempotent submission

`requestId` is an optional query parameter (a client-generated UUID) that makes submission idempotent. If a submit call
times out or you retry with the same `requestId`, Snowflake doesn’t start a duplicate run, which prevents orchestrator
retries (Airflow, CI/CD) from starting the same batch twice. Idempotency is keyed only on `requestId`: the request body
isn’t compared, so a retry that reuses a `requestId` with a different body is still treated as a duplicate and starts no
new run.

Note

A retry with an already-used `requestId` returns `200 OK` with a body of `{"status": null}` and no `job_id` or
`Location` header. It doesn’t re-return the original run’s job ID, so capture the `job_id` from the first successful
submission if you need it later.

### Request body

The body contains the stage location of your application (`from_location`), the `entrypoint`, an optional `arguments`
array, an optional `execution_name`, and the job `specification`: a JSON `bundle` object with the same structure and
fields as the YAML you use in the SQL `WITH SPECIFICATION` clause. In the REST API, pass the specification as a JSON
object, not a string. See [Job specification reference](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle-specification) for the fields.

The optional `execution_name` assigns a name to the run, the same as the SQL `EXECUTION_NAME` parameter: Snowflake
stores it in `CODE_BUNDLE_HISTORY` and renders it into the server-side `EXECUTE CODE BUNDLE` statement. If you omit it,
the run’s `EXECUTION_NAME` is empty.

**Scala/Java:**

Copy code

```
{
  "from_location": "@my_db.my_schema.my_stage/spark_jobs/job.jar",
  "entrypoint": "com.example.MySparkApp",
  "arguments": ["--input", "@my_db.my_schema.my_stage/input.csv", "--partitions", "10"],
  "execution_name": "my_spark_application",
  "specification": {
    "bundle": {
      "type": "spark",
      "compute_type": "warehouse",
      "language": "scala",
      "compute_options": { "language_version": "2.12" },
      "properties": {
        "java_dependencies": {
          "jars": ["@my_db.my_schema.my_stage/source/jars/library1.jar"]
        }
      }
    }
  }
}
```

**Python:**

Copy code

```
{
  "from_location": "@my_db.my_schema.my_stage/python_jobs/job.py",
  "entrypoint": "job.py",
  "arguments": ["--input", "@my_db.my_schema.my_stage/input.csv", "--partitions", "10"],
  "execution_name": "my_spark_application",
  "specification": {
    "bundle": {
      "type": "spark",
      "compute_type": "warehouse",
      "language": "python",
      "compute_options": {},
      "properties": {
        "python_dependencies": {
          "requirements_files": ["@my_db.my_schema.my_stage/python_jobs/requirements.txt"]
        }
      }
    }
  }
}
```

### Response

An asynchronous submission (`asyncExec=true`) returns `202 Accepted` with a job ID in the body. Use the job ID to
[monitor and manage the run](#monitor-and-manage).

```
HTTP/1.1 202 Accepted
Content-Type: application/json
Location: /api/v2/results/01b1f2e0-0000-df4f-0000-00100006589e0
```

Copy code

```
{
  "code": "392604",
  "message": "Request execution in progress. Use provided Location header or result handler id to perform query monitoring and management.",
  "result_handler": "01b1f2e0-0000-df4f-0000-00100006589e0",
  "job_id": "01b1f2e0-0000-df4f-0000-00100006589e"
}
```

Use `job_id` as the run identifier for status and cancel calls. The `Location` header points to a results path keyed by
`result_handler`, which is the `job_id` with a trailing `0` appended, so it is not the same value as `job_id`.

Note

When you submit asynchronously, the API doesn’t validate the specification at submission time. An invalid
specification (for example, an unsupported field) still returns `202 Accepted`, and the run then ends with status
`FAILED`, which you see when you [check its status](#check-status). The synchronous SQL command, by
contrast, rejects an invalid specification when you submit it.

## Submit a job with SQL

Submit a Spark job with the `EXECUTE CODE BUNDLE` command. The command takes the entrypoint, arguments, and an optional
execution name as SQL parameters; the rest of the job definition is passed inline as YAML in the `WITH SPECIFICATION`
clause. The job inherits the role that runs the statement and runs on the warehouse set in the session. The statement
is synchronous: it returns when the run finishes.

### Set the session context

Set the warehouse, database, and schema before submitting. Your job runs on the session warehouse.

Copy code

```
USE WAREHOUSE my_warehouse;
USE DATABASE my_db;
USE SCHEMA my_schema;
```

### Submit a job

Define and submit the job in a single statement, with the application, entrypoint, and specification all passed inline.

**Scala/Java:**

Copy code

```
EXECUTE CODE BUNDLE FROM '@my_db.my_schema.my_stage/spark_jobs/job.jar'
  ENTRYPOINT = 'com.example.MySparkApp'
  ARGUMENTS = ('--input', '@my_db.my_schema.my_stage/input.csv', '--partitions', '10')
  EXECUTION_NAME = 'my_spark_application'
  WITH SPECIFICATION $$
bundle:
  type: spark
  compute_type: warehouse
  language: scala
  compute_options:
    language_version: "2.12"
  properties:
    java_dependencies:
      jars:
        - '@my_db.my_schema.my_stage/source/jars/library1.jar'
        - '@my_db.my_schema.my_stage/source/jars/library2.jar'
$$;
```

**Python:**

Copy code

```
EXECUTE CODE BUNDLE FROM '@my_db.my_schema.my_stage/python_jobs/job.py'
  ENTRYPOINT = 'job.py'
  ARGUMENTS = ('--input', '@my_db.my_schema.my_stage/input.csv', '--partitions', '10')
  EXECUTION_NAME = 'my_spark_application'
  WITH SPECIFICATION $$
bundle:
  type: spark
  compute_type: warehouse
  language: python
  compute_options: {}
  properties:
    python_dependencies:
      requirements_files:
        - '@my_db.my_schema.my_stage/python_jobs/requirements.txt'
$$;
```

### Command parameters

| Parameter | Description |
| --- | --- |
| `FROM` | Stage path to the main application file: a `.jar` (Scala/Java) or `.py` (Python). |
| `ENTRYPOINT` | For Scala/Java, the fully-qualified main class. For Python, the main `.py` file name. |
| `ARGUMENTS` | Optional. A parenthesized, comma-separated list of argument strings passed to your application’s `main` method. |
| `EXECUTION_NAME` | Optional. A name for the run, recorded with the run so you can identify it later. |
| `WITH SPECIFICATION` | The inline YAML specification. See [Job specification reference](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle-specification). |

Expand

Show lessSee more

The statement runs synchronously and returns when the run finishes. Each run is identified by its query ID. This is the
same value the REST API returns as `job_id` and that you pass as the `executionId` to the status and cancel endpoints,
so you can use it to [monitor and manage the run](#monitor-and-manage).

### Persist a job definition

If you would like to reuse a stored job definition, you can register it once and then submit it by name (for example,
`EXECUTE CODE BUNDLE my_spark_job ENTRYPOINT = 'com.example.MySparkApp'`). The submission parameters are the same as for
inline submission. For details, see
[Snowflake Code Bundles](/developer-guide/code-bundles/code-bundles#execute-code-bundle).

For a Scala or Java job, running a persisted bundle by name does not automatically add the JARs inside the bundle to the
classpath. Declare the JAR that contains your main class (and any dependency JARs) under
`properties.java_dependencies.jars` in the specification; otherwise the run fails to find the class. Python entrypoints
run by name with no extra configuration.

### Schedule with a task

Because you submit the job with a SQL statement, you can wrap it in a
[Snowflake task](/developer-guide/code-bundles/code-bundles#scheduling-with-tasks) to run it on a schedule. Tasks let you
build and orchestrate Spark data pipelines natively in Snowflake: you can chain jobs into dependency graphs and run them
on a schedule, similar to how teams orchestrate Spark workloads with Airflow, but without operating a separate
scheduler.

## Examples

These examples show common Spark-specific fields in the job specification. Each snippet is the `bundle` object you pass
inline: as YAML in the SQL `WITH SPECIFICATION` clause, or as the `bundle` object in the REST request body. For the full
field list, see [Spark job specification reference](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle-specification).

### Pin the Snowpark Connect client version

By default (when you omit `runtime_version`), a job runs with the **latest** available Snowpark Connect for Spark
client version ([`snowpark-connect`](/release-notes/clients-drivers/snowpark-connect-2026)). Because the latest version
changes over time, pin a specific version when you need reproducible runs. Set `compute_options.runtime_version`;
Snowflake installs `snowpark-connect==<version>` at job startup. The version you choose also determines the
`snowflake-snowpark-python` version and the range of Python interpreter versions you can request with `language_version`.

Copy code

```
bundle:
  type: spark
  compute_type: warehouse
  language: python
  compute_options:
    runtime_version: "1.42.0"
```

To always run on the latest client version, omit `runtime_version` (the `compute_options` block is still required):

Copy code

```
bundle:
  type: spark
  compute_type: warehouse
  language: python
  compute_options: {}
```

### Add dependencies

For Scala or Java, list dependency JARs on a stage; they’re added to the classpath automatically:

Copy code

```
bundle:
  type: spark
  compute_type: warehouse
  language: scala
  compute_options:
    language_version: "2.12"
  properties:
    java_dependencies:
      jars:
        - '@my_db.my_schema.my_stage/jars/library1.jar'
        - '@my_db.my_schema.my_stage/jars/library2.jar'
```

For Python, install packages from PyPI or a requirements file:

Copy code

```
bundle:
  type: spark
  compute_type: warehouse
  language: python
  compute_options: {}
  properties:
    python_dependencies:
      packages:
        - numpy==1.26.4
      requirements_files:
        - '@my_db.my_schema.my_stage/python_jobs/requirements.txt'
```

### Use a customer-managed artifact repository

By default, Python packages are resolved from `snowflake.snowpark.pypi_shared_repository`. To resolve them from your own
package index instead (for example, a self-hosted Sonatype Nexus), first create a `PYPI`
[artifact repository](/sql-reference/sql/create-artifact-repository) that points at your index. This ties together a
secret for credentials, an API integration for network access, and the repository’s index URL:

Copy code

```
CREATE OR REPLACE SECRET my_repo_secret
  TYPE = PASSWORD
  USERNAME = 'your_username'
  PASSWORD = 'your_password_or_token';

CREATE OR REPLACE API INTEGRATION my_repo_integration
  API_PROVIDER = ARTIFACT_REPOSITORY_API
  API_ALLOWED_PREFIXES = ('https://nexus.example.com')
  ALLOWED_AUTHENTICATION_SECRETS = (my_repo_secret)
  ENABLED = TRUE;

CREATE OR REPLACE ARTIFACT REPOSITORY my_db.my_schema.my_nexus_repo
  TYPE = PYPI
  API_INTEGRATION = my_repo_integration
  INDEX_URL = 'https://nexus.example.com/repository/pypi-proxy/simple/'
  AUTHENTICATION_SECRET = my_repo_secret;
```

Then reference the repository by its fully-qualified name in the specification:

Copy code

```
bundle:
  type: spark
  compute_type: warehouse
  language: python
  compute_options: {}
  artifact_repositories:
    - my_db.my_schema.my_nexus_repo
  properties:
    python_dependencies:
      packages:
        - my-internal-package==1.2.3
```

Note

When you set a custom artifact repository, Snowflake resolves **all** of the job’s Python dependencies through it,
including `snowpark-connect` and `snowflake-snowpark-python` themselves. The repository must proxy PyPI (not only host
your private packages), or the runtime dependencies won’t resolve.

### Attach secrets and external access integrations

Attach Snowflake secrets and external access integrations your job needs (for example, to reach an external API). The
submitting role needs `USAGE` or `OWNERSHIP` on the external access integration and `READ` or `OWNERSHIP` on the
secret:

Copy code

```
bundle:
  type: spark
  compute_type: warehouse
  language: python
  compute_options: {}
  secrets:
    - my_db.my_schema.my_secret
  external_access_integrations:
    - my_db.my_schema.my_eai
```

Note

A `secrets` entry must be paired with an `external_access_integrations` entry whose integration lists the secret in its
`ALLOWED_AUTHENTICATION_SECRETS`; `secrets` on its own is rejected. In your application, read an attached secret with the
Snowflake Python API, for example, `_snowflake.get_generic_secret_string('my_secret')`, using the secret’s bare name.

### Set Spark configuration

Pass Spark configuration properties with `spark_conf`:

Copy code

```
bundle:
  type: spark
  compute_type: warehouse
  language: scala
  compute_options:
    language_version: "2.12"
  properties:
    spark_conf:
      spark.sql.shuffle.partitions: "200"
      spark.sql.session.timeZone: "UTC"
```

## Job specification reference

The job specification defines how your Spark job runs. In SQL it’s the YAML in the `WITH SPECIFICATION` clause; in the
REST API it’s the `bundle` object in the request body. For the full list of fields, see
[Spark job specification reference](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle-specification).

## Monitor and manage jobs

Every Spark job has one identifier, and it’s the same value everywhere you refer to the run. The query ID returned by
`EXECUTE CODE BUNDLE`, the `job_id` returned by a REST submission, and the `executionId` you pass to the status and
cancel endpoints (returned as `query_id` in the status response) are all the same ID (for example,
`01c51743-c819-4261-0000-5349586311aa`). Use it to check status, cancel the run, and find logs. You can monitor and
manage a run with SQL or the REST API, regardless of how you submitted it.

### Check status

Check a run’s status by its job ID, using SQL or the REST API.

**Using SQL:**

Look up the run in the `CODE_BUNDLE_HISTORY` table function. Filter on `QUERY_ID` (the job ID returned at submission):

Copy code

```
SELECT
  CODE_BUNDLE_NAME, DATABASE_NAME, SCHEMA_NAME, ENTRYPOINT, STATUS,
  RUNTIME_STATUS_DETAILS, SQL_ERROR_CODE, ERROR_MESSAGE, BUNDLE_TYPE,
  COMPUTE_TYPE, LANGUAGE_TYPE, RUNTIME_NAME, START_TIME, END_TIME,
  QUERY_ID, EXECUTION_NAME
FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(BUNDLE_NAME => NULL))
WHERE QUERY_ID = '<job_id>';
```

The query returns a single row for the run. For example:

Copy code

```
{
  "CODE_BUNDLE_NAME": null,
  "DATABASE_NAME": null,
  "SCHEMA_NAME": null,
  "ENTRYPOINT": "com.example.MySparkApp",
  "STATUS": "DONE",
  "RUNTIME_STATUS_DETAILS": "",
  "SQL_ERROR_CODE": "",
  "ERROR_MESSAGE": "",
  "BUNDLE_TYPE": "SPARK",
  "COMPUTE_TYPE": "WAREHOUSE",
  "LANGUAGE_TYPE": "SCALA",
  "RUNTIME_NAME": "MY_WAREHOUSE",
  "START_TIME": "2026-07-14 10:50:00+00:00",
  "END_TIME": "2026-07-14 10:50:39+00:00",
  "QUERY_ID": "01c51743-c819-4261-0000-5349586311aa",
  "EXECUTION_NAME": "my_spark_application"
}
```

For a job submitted inline from a stage, `CODE_BUNDLE_NAME`, `DATABASE_NAME`, and `SCHEMA_NAME` are `null` because
there’s no stored job definition. `STATUS` shows the run’s state, such as `DONE` or `FAILED`; when a run fails,
`ERROR_MESSAGE` carries the failure details.

If you assigned an `execution_name` when submitting (with SQL or REST), you can look the run up by that name instead of
the job ID: pass `EXECUTION_NAME => '<execution_name>'` to `CODE_BUNDLE_HISTORY`, or filter on the `EXECUTION_NAME`
column.

**Using the REST API:**

Get the status of a run by ID. The `{executionId}` is the job ID returned at submission. Pass the database and schema as
headers:

```
GET /api/v2/code-bundle-executions/{executionId}
X-Snowflake-Database: MY_DB
X-Snowflake-Schema: MY_SCHEMA
```

The response is an array with a single execution record. `status` comes from the account query history. A run is still
in progress while `status` is `RUNNING`, `QUEUED`, `RESUMING_WAREHOUSE`, or `BLOCKED`, and it has finished when `status`
is `DONE`, `FAILED`, or `CANCELLED`:

Copy code

```
[
  {
    "query_id": "01b1f2e0-0000-df4f-0000-00100006589e",
    "status": "DONE",
    "start_time": "2026-07-14T10:50:00Z",
    "end_time": "2026-07-14T10:50:39Z",
    "database_name": "MY_DB",
    "schema_name": "MY_SCHEMA",
    "runtime_name": "MY_WAREHOUSE"
  }
]
```

Note

When you poll for status, use a poll interval of about 10 to 25 seconds. Polling more frequently (for example, every 5
seconds) can return HTTP `429` (`LimitExceeded`). If you get a `429`, back off and retry.

### View logs in the event table

Application logs, metrics, and traces are written to the event table configured for the run’s **session database** (the one you set with `USE DATABASE` in SQL, or the `X-Snowflake-Database` header for REST submissions). This can be a different event table from the one configured at the account level. Each record is tagged with the job’s query ID in `RESOURCE_ATTRIBUTES['snow.query.id']`. Resolve the event table
for your session database, then query it by the job ID (replace `<job_id>` with the ID returned at submission):

Copy code

```
SHOW PARAMETERS LIKE 'EVENT_TABLE' IN DATABASE <session_db>;

SELECT TIMESTAMP, RECORD_TYPE, VALUE
FROM my_event_table
WHERE RESOURCE_ATTRIBUTES['snow.query.id'] = '<job_id>'
  AND RECORD_TYPE = 'LOG'
ORDER BY TIMESTAMP;
```

Drop the `RECORD_TYPE` filter to also see the `METRIC` and `SPAN` records emitted for the run.

Note

Logs route to the event table of the run’s session database. If that database has no event table of its own, the
records fall back to your account’s event table (`SHOW PARAMETERS LIKE 'EVENT_TABLE' IN ACCOUNT`). The account event
table otherwise receives only the `EXECUTE CODE BUNDLE` query span, not the application’s logs.

### View a failed job’s stack trace

To find why a job failed, query the same event table and filter to `ERROR` and `FATAL` severity. The results include the
full stack trace, with source line numbers:

Copy code

```
SELECT
  TIMESTAMP,
  RECORD['severity_text']::string AS severity,
  SCOPE['name']::string AS scope,
  VALUE::string AS body
FROM my_event_table
WHERE RESOURCE_ATTRIBUTES['snow.query.id'] = '<job_id>'
  AND RECORD_TYPE = 'LOG'
  AND RECORD['severity_text']::string IN ('ERROR', 'FATAL')
ORDER BY TIMESTAMP;
```

Snowflake also records structured exception attributes on these records, which you can select individually:
`RECORD_ATTRIBUTES['exception.type']`, `RECORD_ATTRIBUTES['exception.message']`, and
`RECORD_ATTRIBUTES['exception.stacktrace']`.

### Spark Monitoring UI

You can browse your Spark runs in the Spark Monitoring UI in Snowsight. Sign in to Snowsight, then open the Spark run
history at `https://app.snowflake.com/<organization>/<account>/#/compute/history/spark` (replace `<organization>` and
`<account>` with your own). The page lists Spark runs over a selectable time range, such as the last 7 days. Each run
appears as a single entry identified by the same job ID returned at submission, so you can set the time range and locate
a run by its ID.

### Cancel a job

Cancel a running job by its job ID, using SQL or the REST API.

**Using SQL:**

Cancel the run’s query by ID with [`SYSTEM$CANCEL_QUERY`](/sql-reference/functions/system_cancel_query):

Copy code

```
SELECT SYSTEM$CANCEL_QUERY('<job_id>');
```

**Using the REST API:**

```
POST /api/v2/code-bundle-executions/{executionId}:cancel
```

## SQL reference

Spark jobs are submitted and managed with the `CODE BUNDLE` SQL commands. This section covers the commands as they apply
to Spark jobs. For the complete command reference, including `custom` (non-Spark) bundles, see
[Snowflake Code Bundles](/developer-guide/code-bundles/code-bundles#sql-reference).

### EXECUTE CODE BUNDLE

Submits a Spark job and waits for it to finish. Submit inline from a stage, or run a
[persisted job definition](#persist-a-job-definition) by name. The statement’s query ID is the job ID you use to
[monitor and manage](#monitor-and-manage) the run.

Copy code

```
EXECUTE CODE BUNDLE { <name> | FROM '<stage_path>' }
    ENTRYPOINT = '<entrypoint>'
    [ ARGUMENTS = ( '<arg>' [ , '<arg>' ... ] ) ]
    [ EXECUTION_NAME = '<name>' ]
    [ WITH SPECIFICATION $$ <yaml_spec> $$ ];
```

**Parameters:**

| Parameter | Description |
| --- | --- |
| `<name>` | Runs a persisted Spark job definition by name. Mutually exclusive with `FROM`. |
| `FROM '<stage_path>'` | Stage path to the main application file: a `.jar` (Scala/Java) or `.py` (Python). |
| `ENTRYPOINT` | For Scala/Java, the fully-qualified main class; for Python, the `.py` file name. |
| `ARGUMENTS` | Optional list of argument strings passed to your application’s `main` method. |
| `EXECUTION_NAME` | Optional name recorded with the run so you can identify it later. |
| `WITH SPECIFICATION` | Inline YAML Spark specification. See [Spark job specification reference](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle-specification). |

Expand

Show lessSee more

**Example:**

Copy code

```
EXECUTE CODE BUNDLE FROM '@my_db.my_schema.my_stage/spark_jobs/my-app_2.12-1.0.0.jar'
  ENTRYPOINT = 'com.example.MySparkApp'
  WITH SPECIFICATION $$
bundle:
  type: spark
  compute_type: warehouse
  language: scala
  compute_options:
    language_version: "2.12"
$$;
```

For more examples, see [Submit a job with SQL](#submit-with-sql).

#### Access control requirements

The submitting role needs the privileges described in [Access control](#access-control): `USAGE` on the warehouse, read
access to the stage, `READ` or `OWNERSHIP` on any referenced secrets, and `USAGE` or `OWNERSHIP` on any referenced
external access integrations and artifact repositories.

### CREATE CODE BUNDLE

Persists a Spark job definition so you can run it by name with `EXECUTE CODE BUNDLE`. See
[Persist a job definition](#persist-a-job-definition).

Copy code

```
CREATE [ OR REPLACE ] CODE BUNDLE [ IF NOT EXISTS ] <name>
    FROM '<stage_path>'
    [ COMMENT = '<string>' ];
```

`FROM` must reference a stage **directory** (the bundle is created from the files under that path), not an individual
file. This differs from `EXECUTE CODE BUNDLE FROM '<stage_path>'`, which accepts a single `.jar` or `.py` file.

### ALTER CODE BUNDLE

Adds a new version to a persisted Spark job definition.

Copy code

```
ALTER CODE BUNDLE <name> ADD VERSION FROM '<stage_path>';
```

### DESCRIBE CODE BUNDLE

Returns metadata about a persisted Code Bundle.

Copy code

```
DESCRIBE CODE BUNDLE <name>;
```

### SHOW CODE BUNDLES

Lists the Code Bundles in the current schema.

Copy code

```
SHOW CODE BUNDLES;
```

### DROP CODE BUNDLE

Removes a persisted Code Bundle.

Copy code

```
DROP CODE BUNDLE [ IF EXISTS ] <name>;
```

You must have `OWNERSHIP` of the Code Bundle to drop it. A role without ownership (even `ACCOUNTADMIN`) can’t drop a
bundle owned by another role; drop it as the owning role, or transfer ownership first.

### CODE\_BUNDLE\_HISTORY (table function)

Returns run history. Look up a single Spark run by its job ID with `QUERY_ID`, or filter to Spark runs with
`BUNDLE_TYPES => 'spark'`. See [Check status](#check-status) for the columns returned.

Copy code

```
SELECT * FROM TABLE(INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(
    QUERY_ID       => '<job_id>',
    BUNDLE_TYPES   => 'spark',
    LANGUAGE_TYPES => 'scala, java, python',
    STATUS         => '<status>',
    RESULT_LIMIT   => 100
));
```

For the full parameter list, see [`CODE_BUNDLE_HISTORY`](/developer-guide/code-bundles/code-bundles#code_bundle_history).

### SYSTEM$CANCEL\_QUERY

Cancels a running Spark job by its job ID. See [Cancel a job](#cancel).

Copy code

```
SELECT SYSTEM$CANCEL_QUERY('<job_id>');
```
