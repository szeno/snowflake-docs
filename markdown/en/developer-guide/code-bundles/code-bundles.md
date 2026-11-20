# Snowflake Code Bundles

Note

Notebook Project Objects have been renamed to **Code Bundles**. The `NOTEBOOK PROJECT` grammar is still supported, and existing objects,
tasks, and schedules keep working. For background on the rename, see the
[behavior change announcement](/release-notes/bcr-bundles/un-bundled/bcr-2393). To schedule notebooks as Code Bundles from Snowsight,
see [Run and schedule Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule).

Code Bundles let you package and execute non-SQL jobs, like Python, directly on Snowflake compute. Instead of building containers, wrapping logic in stored procedures, or porting your scripts into notebooks, you can upload your project code and run it with a single command. Snowflake automatically injects a Snowpark session at runtime, giving your code direct access to your data without managing connection credentials. You can orchestrate Code Bundles natively with Snowflake Tasks, or externally with the Snowflake CLI, the Snowflake Python API, or the Snowflake REST API.

Code Bundles support three bundle types, which you set with `type` in your `code_bundle.yml` file:

- **`custom`**: Run Python, Java, or Scala code. Python runs on a warehouse or a compute pool; Java and Scala run on a warehouse. This is the type described on this page.
- **`spark`**: Run Spark jobs (Scala, Java, or Python) on Snowflake warehouse compute. See [Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle) for details.
- **`ml`**: Run a workload as a Snowflake ML Job on compute pool compute, in the [Snowflake Container Runtime](/developer-guide/snowflake-ml/container-runtime-ml). See [Run ML Jobs with Code Bundles](/developer-guide/code-bundles/ml-code-bundles) for details.

For the fields each type accepts, see the [`code_bundle.yml` reference](/developer-guide/code-bundles/code-bundle-yml-reference).

Code Bundles support two compute targets:

- **Warehouse**: Run Python, Java, or Scala code on Snowflake warehouse compute. Best for data processing jobs, ETL scripts, and workloads where the majority of the processing occurs in the warehouse as pushed-down SQL or UDFs.
- **Compute pool (Snowpark Container Services)**: Run on Snowpark Container Services. Best for workloads where more processing occurs in the Python process, jobs requiring GPU, or custom container runtimes.

## Availability

Code Bundles are generally available, including:

- The `custom`, `spark`, and `ml` bundle types, on warehouses and compute pools.
- Python, Java, and Scala `custom` Code Bundles on warehouses.
- Anonymous runs (`EXECUTE CODE BUNDLE FROM ...`), Python method entrypoints, and return values.
- Inline specifications (`WITH SPECIFICATION`).
- The Code Bundles page in Snowsight, and the REST API, Python API, and Snowflake CLI clients.

## What you can run, and where

The following table shows the supported combinations of bundle type, compute, language, and entrypoint, and how each one returns a value:

| Bundle type and compute | Languages | Entrypoints | Anonymous run source (`FROM`) | `RETURN_VALUE` |
| --- | --- | --- | --- | --- |
| `custom` on a warehouse | Python | `file.py` or `file.py:method` | Stage directory | The method’s return value for `file.py:method`; otherwise NULL |
| `custom` on a warehouse | Java, Scala | Fully qualified main class | Main JAR file on a stage | NULL |
| `custom` on a compute pool | Python | `file.py`, `file.py:method`, or `notebook.ipynb` | Workspace | The value passed to `notebook.exit()`, or the method’s return value; otherwise NULL |
| `spark` on a warehouse | Python, Java, Scala | `file.py`, or fully qualified main class | Stage directory (Python) or JAR file (Java, Scala) | NULL |
| `ml` on a compute pool | Python | `file.py` | N/A | NULL; the ML Job writes its result to `result_stage` |

Expand

Show lessSee more

For details, see [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle),
[Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle), and
[Run ML Jobs with Code Bundles](/developer-guide/code-bundles/ml-code-bundles).

## Key concepts

| Concept | Description |
| --- | --- |
| **Code Bundle** | A named object containing your project source files, created from a stage, workspace, or local directory. |
| **Specification** | A YAML configuration (`code_bundle.yml`) defining compute type, runtime version, dependencies, secrets, environment variables, and other settings. |
| **Entrypoint** | The file within the bundle that Snowflake executes (for example, `main.py`). |
| **Source** | Where the bundle files come from: a stage path (`@my_stage/path`), workspace path (`snow://workspace/...`), or local directory. |
| **Version** | An immutable snapshot of bundle files. New versions are added with `ALTER CODE BUNDLE ... ADD VERSION`. Runs use the default version, which is the last version added. |
| **Anonymous run** | A run of source files from a stage or workspace with `EXECUTE CODE BUNDLE FROM ...`, without creating a Code Bundle. The inline specification is the whole configuration. |
| **Return value** | The value a run returns in the `RETURN_VALUE` column: the value passed to `notebook.exit()`, or the return value of a Python method entrypoint (`file.py:method`). |
| **Execution name** | An optional name for a run, set with `EXECUTION_NAME`, that you can filter on in the run history. |

Expand

Show lessSee more

## Access control

Code Bundles use Snowflake’s standard role-based access control model. There are two privileges
relevant to Code Bundles:

- **CREATE CODE BUNDLE** on a schema: Allows a role to create new Code Bundles in that schema.
- **OWNERSHIP or USAGE** on a Code Bundle: Allows a role to execute the Code Bundle.

A role can also hold MONITOR on a Code Bundle, which allows it to view the bundle’s run history without being able to run it.

If a role already has the CREATE NOTEBOOK PROJECT privilege on a schema, it can create Code Bundles in that schema; you don’t need to grant
CREATE CODE BUNDLE as well.

### Grant permission to create Code Bundles

An administrator must grant the CREATE CODE BUNDLE privilege on a schema to the roles that need to create bundles in that schema:

Copy code

```
GRANT CREATE CODE BUNDLE ON SCHEMA my_db.my_schema TO ROLE developer_role;
```

### Grant permission to execute Code Bundles

Once a Code Bundle exists, any role with OWNERSHIP or USAGE on it can execute it:

Copy code

```
GRANT USAGE ON CODE BUNDLE my_db.my_schema.my_bundle TO ROLE data_engineer_role;
```

Running a Code Bundle also requires privileges on the compute it runs on and on the objects its specification references, such as secrets
and external access integrations. For the full list, see
[EXECUTE CODE BUNDLE access control requirements](/sql-reference/sql/execute-code-bundle#access-control-requirements). For all Code Bundle
privileges, see [Code Bundle privileges](/user-guide/security-access-control-privileges#label-access-control-privileges-code-bundle).

## Quickstart (Snowsight)

This minimal example creates and executes a Code Bundle using SQL.

1. **Create a new private workspace.**

   Go to **Projects** » **Workspaces** » **+** » **Private Workspace** and create a new private workspace named `my_private_workspace`.

   [![Snowsight Workspaces menu showing the option to create a new private workspace.](/static/images/code-bundles/create-private-workspace.png)](/static/images/code-bundles/create-private-workspace.png)
2. **Write a Python script (`main.py`).**

   Select **Add new** » **Python file**.

   [![Snowsight Add new menu showing the option to add a Python file.](/static/images/code-bundles/add-python-file.png)](/static/images/code-bundles/add-python-file.png)

   Name it `main.py` and paste in the following contents.

   Copy code

   ```
   from snowflake.snowpark.context import get_active_session

   session = get_active_session()
   df = session.sql("SELECT CURRENT_TIMESTAMP() AS ts, CURRENT_USER() AS user")
   df.show()
   ```
3. **Add a bundle definition file.**

   Create a file named `code_bundle.yml` and paste in the following contents.

   Copy code

   ```
   bundle:
     type: custom
     compute_type: warehouse
     language: python

     compute_options:
       runtime_version: '3.11'
   ```

   You can also configure your Code Bundle to run on compute pools, as shown in [Compute pool (Snowpark Container Services) compute](#compute-pool-spcs-compute).
4. **Create the Code Bundle.**

   Open a SQL file, paste the contents below, and replace the `<placeholder>` strings with the database and schema to create the Code Bundle in.

   Copy code

   ```
   USE DATABASE <your_database>;
   USE SCHEMA <your_schema>;
   USE WAREHOUSE <your_warehouse>;

   CREATE OR REPLACE CODE BUNDLE my_first_bundle
   FROM 'snow://workspace/"USER$"."PUBLIC"."my_private_workspace"/versions/live';
   ```
5. **Execute the bundle.**

   Copy code

   ```
   EXECUTE CODE BUNDLE my_first_bundle
   ENTRYPOINT = 'main.py';
   ```

### Next steps

Now that you have created and executed your first Code Bundle, here are some common scenarios you might encounter:

- [Scheduling with a task](#scheduling-with-tasks)
- [Passing input arguments](#passing-arguments)
- [Monitor Code Bundle runs](#monitor-runs)
- [Return a value from a run](#return-values)

## Quickstart (Snowflake CLI)

This guide walks you through setting up your environment, creating your first Code Bundle, and executing it using the Snowflake CLI.

**Prerequisites**

- Python 3.10 through 3.12, to run the Snowflake CLI locally. This is separate from the runtime version your Code Bundle uses on Snowflake compute, which you set in `code_bundle.yml`.
- Snowflake CLI version 3.29.0 or later, which adds the `snow bundle` commands.
- A [Snowflake CLI connection](/developer-guide/snowflake-cli/connecting/configure-connections) with a default warehouse, database, and schema.

1. **Install the Snowflake CLI using `uv` or `pip`.**

   Copy code

   ```
   # Using uv
   uv tool install snowflake-cli
   # Using pip
   pip install snowflake-cli
   ```

   Verify that the version is 3.29.0 or later:

   Copy code

   ```
   snow --version
   ```
2. **Prepare your project.**

   Create a directory named `my_project` that contains two files:

   - `main.py`: The Python job that runs on Snowflake.

     Copy code

     ```
     from snowflake.snowpark.context import get_active_session

     session = get_active_session()
     session.sql("SELECT CURRENT_TIMESTAMP() AS ts, CURRENT_USER() AS user").show()
     ```
   - `code_bundle.yml`: The bundle configuration, which runs the project on the warehouse of your session.

     Copy code

     ```
     bundle:
       type: custom
       compute_type: warehouse
       language: python

       compute_options:
         runtime_version: '3.11'
     ```

   Create a Code Bundle from your local directory. Use the `--exclude` flag with a glob pattern to ignore unnecessary files like virtual environments or bytecode. To exclude a directory and its contents, match the contents with a pattern like `venv/**`.

   Copy code

   ```
   snow bundle create MY_BUNDLE \
     --source ./my_project \
     --exclude "venv/**"
   ```
3. **Execute the Code Bundle.**

   Run your Code Bundle by specifying the entrypoint file. This command executes your Python script on Snowflake compute:

   Copy code

   ```
   snow bundle execute MY_BUNDLE --entrypoint main.py
   ```

### Next steps

Now that you have created and executed your first Code Bundle, here are some common scenarios you might encounter:

- [Scheduling with a task](#scheduling-with-tasks)
- [Passing input arguments](#passing-arguments)
- [Monitor Code Bundle runs](#monitor-runs)
- [Return a value from a run](#return-values)

## Configuration overview (`code_bundle.yml`)

The `code_bundle.yml` file defines how your Code Bundle runs. Place it in the root of your project directory. The following examples show how to run your Code Bundle on virtual warehouses and compute pools. For a full reference of the configuration options, see [`code_bundle.yml` reference](/developer-guide/code-bundles/code-bundle-yml-reference).

### Warehouse compute

To run your Code Bundle on a Snowflake warehouse, set the `compute_type` to `warehouse`. When `EXECUTE CODE BUNDLE` runs, the Code Bundle runs on the virtual warehouse set in the current session (for example, set by `USE WAREHOUSE ...`).

Copy code

```
bundle:
  type: custom
  compute_type: warehouse
  language: python

  compute_options:
    runtime_version: '3.11'

  properties:
    requirements_file: requirements.txt
```

To run Java or Scala code on a warehouse, set `language` to `java` or `scala`, and set `runtime_version` to the JDK version (`'11'` or
`'17'`) or the Scala version (`'2.12'`). For details, see [Run Java or Scala code on a warehouse](#java-scala-warehouse).

Copy code

```
bundle:
  type: custom
  compute_type: warehouse
  language: java

  compute_options:
    runtime_version: '17'
```

### Compute pool (Snowpark Container Services) compute

To run your Code Bundle on a compute pool, set the `compute_type` to `compute_pool`. The Code Bundle runs on the compute pool specified in `compute_options.compute_pool`. For a full list of Container Runtime options, see [Snowflake Container Runtime releases](/developer-guide/snowflake-ml/container-runtime/releases).

Copy code

```
bundle:
  type: custom
  compute_type: compute_pool
  language: python

  compute_options:
    compute_pool: system_compute_pool_cpu
    query_warehouse: MY_WAREHOUSE
    runtime_version: 'V2.9-CPU-PY3.12'

  properties:
    requirements_file: requirements.txt
```

### ML compute (Container Runtime)

To run the bundle as a Snowflake ML Job, set `type: ml` and `compute_type: compute_pool`. ML bundles run on Snowflake Container Runtime, mount their files and a result stage into the container, and can run on multiple nodes. See [Run ML Jobs with Code Bundles](/developer-guide/code-bundles/ml-code-bundles).

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
```

### Other configurations

The `code_bundle.yml` file also lets you configure many additional settings like external access integrations, artifact repositories, Snowflake secrets, and more. See the [`code_bundle.yml` reference](/developer-guide/code-bundles/code-bundle-yml-reference) for more information.

## Examples

### Passing arguments

Pass arguments to your code with the `ARGUMENTS` clause in SQL or after the `--` option in the CLI. Your application code can get these input arguments using standard library methods like `sys.argv` or `argparse`.

**SQL:**

Copy code

```
EXECUTE CODE BUNDLE my_bundle
    ENTRYPOINT = 'jobs/main.py'
    ARGUMENTS = ('--source-table', 'DB.SCHEMA.RAW_SALES', '--output-table', 'DB.SCHEMA.SALES_AGG', '--days-back', '7');
```

**CLI:**

Copy code

```
snow bundle execute MY_BUNDLE \
--entrypoint jobs/main.py \
-- --source-table DB.SCHEMA.RAW_SALES \
--output-table DB.SCHEMA.SALES_AGG \
--days-back 7
```

Python example that gets the input arguments:

Copy code

```
import argparse
from snowflake.snowpark.context import get_active_session

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-table", required=True)
    parser.add_argument("--output-table", required=True)
    parser.add_argument("--days-back", type=int, default=30)
    args = parser.parse_args()

    ...

if __name__ == "__main__":
    main()
```

### Return a value from a run

A run can return a value to the statement that started it, in the `RETURN_VALUE` column of the
[EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle#label-execute-code-bundle-output) output:

- **From a Python function:** use a method entrypoint in the form `file.py:method`. Snowflake imports the file and calls the function, and
  the function’s return value becomes `RETURN_VALUE`. Code under `if __name__ == "__main__":` doesn’t run.
- **From a notebook on a compute pool:** call `notebook.exit(value)`.

On a compute pool, returning a value requires [Container Runtime 3.0](/developer-guide/container-runtime/version-3) or later, for example `runtime_version: 'V3-CPU-PY3.12'`.
Container Runtime 2.x versions don’t support return values.

A Python `str` is returned as is; any other value is returned as JSON text, as produced by `json.dumps()` with its default settings. Other runs, including a Python script entrypoint such as
`main.py`, return NULL. A failed run raises an error and returns no row, so decide whether a run succeeded from whether the statement
succeeds, not from `RETURN_VALUE`.

For example, `jobs.py` defines a function that returns a summary of the work it did:

Copy code

```
# jobs.py
from snowflake.snowpark.context import get_active_session

def load_sales():
    session = get_active_session()
    rows = session.sql("INSERT INTO sales_agg SELECT * FROM raw_sales").collect()
    return {"rows_loaded": rows[0][0]}
```

Call the function as the entrypoint:

Copy code

```
EXECUTE CODE BUNDLE my_bundle
  ENTRYPOINT = 'jobs.py:load_sales';
```

```
+-----------------------+
| RETURN_VALUE          |
|-----------------------|
| {"rows_loaded": 1200} |
+-----------------------+
```

In a Snowflake Scripting block, such as a task body, capture the value with `INTO` and use it in later statements:

Copy code

```
DECLARE
  run_output VARCHAR;
BEGIN
  EXECUTE CODE BUNDLE my_bundle
    ENTRYPOINT = 'jobs.py:load_sales'
    INTO :run_output;
  RETURN PARSE_JSON(:run_output):rows_loaded;
END;
```

Note

Before the [RETURN\_VALUE behavior change](/release-notes/bcr-bundles/un-bundled/bcr-code-bundles-return-value), runs returned a `status`
or `result` column with a success message instead of `RETURN_VALUE`.

### Attaching secrets and external access

To call external APIs, create a secret, network rule, and external access integration, then attach them to your bundle.

1. **Create the Snowflake objects:**

   Copy code

   ```
   CREATE OR REPLACE SECRET MY_DB.PUBLIC.MY_API_KEY
       TYPE = GENERIC_STRING
       SECRET_STRING = 'sk-abc123...';

   CREATE OR REPLACE NETWORK RULE MY_NETWORK_RULE
       TYPE = HOST_PORT
       MODE = EGRESS
       VALUE_LIST = ('api.example.com');

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION MY_DB.PUBLIC.MY_EAI
       ALLOWED_NETWORK_RULES = (MY_NETWORK_RULE)
       ALLOWED_AUTHENTICATION_SECRETS = (MY_API_KEY)
       ENABLED = TRUE;
   ```
2. **Attach the objects to the Code Bundle.**

   To attach the secret and external access integration objects to the Code Bundle, add the object names to the `code_bundle.yml` file under the `secrets` and `external_access_integrations` properties respectively.

   Copy code

   ```
   # code_bundle.yml

   bundle:
     ...

     secrets:
       - MY_DB.PUBLIC.MY_API_KEY

     external_access_integrations:
       - MY_DB.PUBLIC.MY_EAI
   ```
3. **Read the secret in Python.**

   In your Python script or notebook file, you can get the secret value as shown below.

   Copy code

   ```
   from snowflake.snowpark import secrets as sf_secrets
   import urllib.request

   api_key = sf_secrets.get_generic_secret_string("MY_DB.PUBLIC.MY_API_KEY")
   req = urllib.request.Request(
       "https://api.example.com/data",
       headers={"Authorization": f"Bearer {api_key}"}
   )
   with urllib.request.urlopen(req) as response:
       data = response.read()
   ```

   The string you pass to `get_generic_secret_string()` (`"MY_DB.PUBLIC.MY_API_KEY"`) must match the name of a secret listed under `secrets` in `code_bundle.yml`.

### Define environment variables

You can define environment variables in `code_bundle.yml`. From your application code, you can access them with standard libraries like `os.environ` (for Python).

**`code_bundle.yml`:**

Copy code

```
bundle:
  ...

  env_vars:
    - API_URL: https://api.example.com/
    - ENV: production
```

**Python:**

Copy code

```
# main.py
import os

api_url = os.environ["API_URL"]
env = os.environ["ENV"]
```

### Mounting stages

You can mount Snowflake stages as local file system paths. On compute pools, mounted stages are readable and writable. On warehouses, mounted stages are read-only.

**`code_bundle.yml`:**

Copy code

```
bundle:
  ...
  stage_mounts:
    myData:
      stage_url: '@DB.SCHEMA.DATA_STAGE'
      mount_path: '/mnt/data/'
```

**Python:**

Copy code

```
import os

for filename in os.listdir("/mnt/data/"):
    with open(f"/mnt/data/{filename}") as f:
        print(f.read())
```

### Async execution

Run a bundle asynchronously to avoid blocking. Use `status` to poll and `cancel` to abort.

**CLI:**

Copy code

```
snow bundle execute MY_BUNDLE --entrypoint main.py --async
# Output: Request submitted. Query ID: 01c51743-c819-4261-0000-5349586311aa

snow bundle status 01c51743-c819-4261-0000-5349586311aa
# Output: Query 01c51743-...: RUNNING

snow bundle cancel 01c51743-c819-4261-0000-5349586311aa
# Output: query [01c51743-...] terminated.
```

An asynchronous run returns NULL in `RETURN_VALUE`. To check the outcome of an asynchronous run, use `snow bundle status`, or query
[CODE\_BUNDLE\_HISTORY](/sql-reference/functions/code_bundle_history) by the query ID.

### Change the specification for one run

To change the configuration of a single run without changing the Code Bundle, add `WITH SPECIFICATION`. The inline specification is merged
over the stored `code_bundle.yml`: name only the fields you want to change, and every other field keeps its stored value. Lists, including
`env_vars` and `secrets`, are replaced as a whole, and `null` removes a field for the run. This can be helpful to test changes to the Code Bundle before applying the change formally to the Code Bundle specification, like confirming that a newer version of Python works correctly with the Code Bundle.

For example, run the bundle with a different Python version:

Copy code

```
EXECUTE CODE BUNDLE my_bundle
  ENTRYPOINT = 'main.py'
  WITH SPECIFICATION
$$
bundle:
  compute_options:
    runtime_version: '3.12'
$$;
```

For the full merge rules and an example of the resulting specification, see
[How WITH SPECIFICATION is merged](/sql-reference/sql/execute-code-bundle#label-execute-code-bundle-spec-merge).

### Run code without creating a Code Bundle

To run source files once, for example during development or from a CI/CD job, use `EXECUTE CODE BUNDLE FROM` with the source location and
an inline specification. Snowflake doesn’t create a Code Bundle. Because there’s no stored specification, the inline specification is the
whole configuration, and a `code_bundle.yml` file in the source location is ignored.

Give the run an `EXECUTION_NAME` so you can find it later in the run history:

Copy code

```
EXECUTE CODE BUNDLE FROM '@my_db.my_schema.my_stage/jobs'
  ENTRYPOINT = 'main.py'
  EXECUTION_NAME = 'adhoc_backfill'
  WITH SPECIFICATION
$$
bundle:
  type: custom
  compute_type: warehouse
  language: python
  compute_options:
    runtime_version: '3.11'
$$;
```

The source depends on where the code runs:

- **Python on a warehouse:** a stage directory that contains the entrypoint file.
- **Java or Scala on a warehouse:** the main JAR file on a stage. See [Run Java or Scala code on a warehouse](#java-scala-warehouse).
- **Python on a compute pool:** a workspace path, such as `'snow://workspace/USER$.PUBLIC."my_workspace"/versions/live'`. Stages aren’t
  supported. For a shared workspace, use a committed version; `versions/live` isn’t supported. If the workspace changes while Snowflake
  reads it, the run fails with error 099139; run the statement again.
- **Spark:** see [Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle#submit-with-sql).

### Run Java or Scala code on a warehouse

A `custom` Code Bundle can run a Java or Scala application on a warehouse:

- Set `language` to `java` or `scala`.
- Set `compute_options.runtime_version` to the JDK version (`'11'` or `'17'`) for Java, or to the Scala version (`'2.12'`) for Scala.
  There’s no `language_version` field for `custom` bundles.
- Set `ENTRYPOINT` to the fully qualified name of a class that defines `public static void main(String[] args)` (Java) or
  `def main(args: Array[String]): Unit` (Scala). `ARGUMENTS` are passed to `main`. Calling another method isn’t supported.
- List dependency JARs under `properties.java_dependencies.jars`. It’s the only key allowed under `properties`. Each entry must be a stage
  path to a `.jar` file, and the file names must be unique and differ from the main JAR’s name. Dependencies aren’t resolved from external
  repositories, so `requirements_file` and `artifact_repositories` aren’t supported.
- `env_vars` are available through `System.getenv()`.
- `stage_mounts` are read-only, and each `mount_path` must be under `/tmp`.

Get the Snowpark session in your code with `Session.builder().getOrCreate()`.

Which JAR files are on the classpath depends on how you run the code:

- **Named Code Bundle, or a workspace source:** every `.jar` file in the Code Bundle, plus the JAR files in `java_dependencies.jars`.
- **Anonymous run from a stage:** only the main JAR named in `FROM` and the JAR files in `java_dependencies.jars`. Other JAR files next to
  the main JAR, or in mounted stages, aren’t on the classpath.

Avoid including the same class in more than one JAR file; this can cause unexpected behavior.

A Java or Scala execution returns NULL in `RETURN_VALUE`. If `main` throws an exception, the statement fails with that error.

For example, run a Java application from a JAR file without creating a Code Bundle:

Copy code

```
EXECUTE CODE BUNDLE FROM '@my_db.my_schema.my_stage/app/app.jar'
  ENTRYPOINT = 'com.example.MyApp'
  ARGUMENTS = ('--label', 'value with space', '42')
  WITH SPECIFICATION
$$
bundle:
  type: custom
  compute_type: warehouse
  language: java
  compute_options:
    runtime_version: '17'
  properties:
    java_dependencies:
      jars:
        - '@my_db.my_schema.libs/utils-1.0.jar'
$$;
```

### Scheduling with tasks

Wrap `EXECUTE CODE BUNDLE` in a Snowflake task to run on a schedule.

Copy code

```
CREATE OR REPLACE TASK my_daily_job
    WAREHOUSE = SNOWFLAKE_LEARNING_WH
    SCHEDULE = 'USING CRON 0 9 * * * America/Los_Angeles'
    AS
EXECUTE CODE BUNDLE my_bundle
ENTRYPOINT = 'main.py';

ALTER TASK my_daily_job RESUME;
```

### Local development

If you choose to do your development in an external environment, like VS Code or Cortex Code on your laptop, you can create a Snowpark session to connect to your Snowflake account and iterate on your scripts locally for development. To allow the same code to run on the Snowflake server without code changes, the session configuration is overridden when you run it as a Code Bundle on Snowflake.

Let’s look at an example.

The example script below connects to Snowflake using a connection defined in the [`connections.toml`](/developer-guide/snowflake-cli/connecting/configure-connections) file.

Copy code

```
# main.py
from snowflake.snowpark import Session

connection_name = "my_connection" # Connection name in connections.toml
session = Session.builder.configs({'connection_name': connection_name}).getOrCreate()

results = session.sql("SELECT * FROM my_table LIMIT 10").collect()
```

You can run this from your laptop using `python main.py` (or, if using `uv`, `uv run main.py`). The Snowpark client connects to the given Snowflake account, and you can develop from your laptop.

When you’re ready to deploy to Snowflake, you can use the Snowflake CLI:

Copy code

```
# Create code bundle from current working directory
snow bundle create my_bundle --source .

snow bundle execute my_bundle --entrypoint main.py
```

Now when this Code Bundle executes on Snowflake, `getOrCreate()` returns the Snowpark session that Snowflake injects at runtime. The runtime overrides the local session configuration, so the same code runs on Snowflake without changes.

## Monitor Code Bundle runs

You can see the status, duration, errors, and results of runs in the following places:

- **Snowsight:** In the navigation menu, select **Transformation** » **Code Bundles**. The page lists the Code Bundles in the
  account and the runs across the account, including runs on warehouses and compute pools, Spark and ML runs, and anonymous runs. Select a
  Code Bundle to see its details, files, run history, and schedules.
- **SQL:** Query the [CODE\_BUNDLE\_HISTORY](/sql-reference/functions/code_bundle_history) table function. Filter by Code Bundle name, query ID,
  execution name, status, time range, or type:

  Copy code

  ```
  SELECT CODE_BUNDLE_NAME, ENTRYPOINT, STATUS, ERROR_MESSAGE, START_TIME, END_TIME, QUERY_ID
    FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(
      BUNDLE_NAME => 'my_db.my_schema.my_bundle',
      RESULT_LIMIT => 100));
  ```

  The function returns up to 1000 rows per call (`RESULT_LIMIT`, default 100). To get the next page, pass the `PAGE_TOKEN` value from the
  last row as the `PAGE_TOKEN` argument.
- **Snowflake CLI:** Run [`snow bundle history`](#snow-bundle-history) or, for a single asynchronous run, [`snow bundle status`](#snow-bundle-status).

Each run is identified by the query ID of the `EXECUTE CODE BUNDLE` statement. Logs, metrics, and traces are written to the event table. For
details, see [Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).

## Troubleshooting

| Symptom | Cause and resolution |
| --- | --- |
| A query or tool that reads the `status` or `result` column fails with an invalid identifier error, or reports a successful run as failed. | Runs return a `RETURN_VALUE` column instead. Decide whether a run succeeded from whether the statement succeeds. See [the behavior change](/release-notes/bcr-bundles/un-bundled/bcr-code-bundles-return-value). |
| `RETURN_VALUE` is NULL for a run that should return a value. | Use a method entrypoint (`file.py:method`) or call `notebook.exit(value)`. A script entrypoint such as `main.py` doesn’t return a value. Asynchronous runs also return NULL. |
| A run fails with `ReturnValueError`. | The returned value can’t be encoded as JSON, or, on a compute pool, it’s larger than 16 MiB. Return a `str`, or a smaller value that `json.dumps()` can encode. |
| An anonymous run (`EXECUTE CODE BUNDLE FROM`) ignores settings in `code_bundle.yml`. | Anonymous runs don’t read `code_bundle.yml`. Pass the whole specification in `WITH SPECIFICATION`. |
| An inline specification drops environment variables or secrets that are in `code_bundle.yml`. | Lists are replaced, not merged. Restate the full list in `WITH SPECIFICATION`. |
| An anonymous run on a compute pool fails with error 099139. | The workspace changed while Snowflake read it. Run the statement again. |
| A Java or Scala run can’t find the main class. | For an anonymous run, `FROM` must name the JAR file that contains the main class, and other JAR files must be listed in `properties.java_dependencies.jars`. |
| `EXECUTE CODE BUNDLE` fails in an owner’s rights stored procedure or a notebook cell. | The command runs with caller’s rights. See [Supported invocation contexts](/sql-reference/sql/execute-code-bundle#label-execute-code-bundle-invocation-contexts). |

Expand

Show lessSee more

## Frequently asked questions

**Are Code Bundles the same as Notebook Project Objects (NPOs)?**
Yes. Notebook Project Objects were renamed to Code Bundles. Existing objects are Code Bundles, and the `CREATE NOTEBOOK PROJECT`,
`EXECUTE NOTEBOOK PROJECT`, and `SHOW NOTEBOOK PROJECTS` commands keep working. Use the `CODE BUNDLE` commands for new work. See the
[behavior change announcement](/release-notes/bcr-bundles/un-bundled/bcr-2393).

**Do I have to migrate existing notebook schedules?**
No. Tasks that run `EXECUTE NOTEBOOK PROJECT` will continue to run. Code that reads the command’s output must handle the `RETURN_VALUE` column; see
the [behavior change](/release-notes/bcr-bundles/un-bundled/bcr-code-bundles-return-value).

**Should I create a Code Bundle, or run code anonymously?**
Create a Code Bundle for code that you run repeatedly or on a schedule, so each run uses a versioned snapshot and you can grant USAGE on it.
Use an anonymous run (`EXECUTE CODE BUNDLE FROM`) for one-off runs, development, and CI/CD jobs that deploy code to a stage and run it.

**Should I run on a warehouse or a compute pool?**
Use a warehouse for jobs that mostly push work down to SQL, and for Java and Scala code. Use a compute pool for notebooks, jobs that need a
GPU or a large Python process, and Container Runtime images.

## `code_bundle.yml` reference

The `code_bundle.yml` file defines how your Code Bundle runs, including the bundle type, compute type, runtime version, dependencies, secrets, environment variables, and stage mounts. For the full field-by-field reference, see [`code_bundle.yml` reference](/developer-guide/code-bundles/code-bundle-yml-reference).

## SQL reference

Code Bundles are created, run, and managed with the following SQL commands and table function:

| Command or function | Description |
| --- | --- |
| [CREATE CODE BUNDLE](/sql-reference/sql/create-code-bundle) | Creates a Code Bundle from a stage or workspace. |
| [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle) | Runs a Code Bundle, or source files from a stage or workspace, at an entrypoint. |
| [ALTER CODE BUNDLE](/sql-reference/sql/alter-code-bundle) | Adds a version to a Code Bundle, or sets or unsets its comment. |
| [DESCRIBE CODE BUNDLE](/sql-reference/sql/desc-code-bundle) | Describes the properties and versions of a Code Bundle. |
| [SHOW CODE BUNDLES](/sql-reference/sql/show-code-bundles) | Lists Code Bundles. |
| [DROP CODE BUNDLE](/sql-reference/sql/drop-code-bundle) | Removes a Code Bundle. |
| [CODE\_BUNDLE\_HISTORY](/sql-reference/functions/code_bundle_history) | Returns the run history of Code Bundles, including anonymous runs. |

Expand

Show lessSee more

## CLI reference

The `snow bundle` commands are available in Snowflake CLI version 3.29.0 and later:

Copy code

```
uv tool install snowflake-cli
```

`WITH SPECIFICATION` isn’t available through the CLI. To run with an inline specification, use
[EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle), for example with `snow sql`.

### snow bundle create

Creates a Code Bundle from a local directory, stage, or workspace.

```
Usage: snow bundle create [OPTIONS] IDENTIFIER
```

| Option | Description |
| --- | --- |
| `--source`, `-s` (required) | Source location. Supports stage (`@stage/path`), workspace (`snow://workspace/...`), or local path (`./my_project/`). |
| `--comment` | Comment for the object. |
| `--overwrite` | Replace if it already exists (`CREATE OR REPLACE`). |
| `--skip-if-exists` | Skip creation if it already exists (`IF NOT EXISTS`). |
| `--exclude` | Glob pattern to exclude from local source (repeatable). Ignored for stage and workspace sources. |

Expand

Show lessSee more

**Examples:**

Copy code

```
snow bundle create MY_BUNDLE --source ./my_project --exclude "venv"
snow bundle create MY_BUNDLE --source @MY_STAGE/project --overwrite
snow bundle create MY_BUNDLE --source 'snow://workspace/"USER$"."PUBLIC"."DEFAULT$"/versions/live'
```

### snow bundle execute

Executes a Code Bundle. Arguments after `--` are passed to the script.

```
Usage: snow bundle execute [OPTIONS] IDENTIFIER [-- ARGS...]
```

| Option | Description |
| --- | --- |
| `--entrypoint` (required) | File path within the bundle to execute. |
| `--execution-name` | Name recorded with the run, the same as `EXECUTION_NAME` in SQL. Filter on it with `snow bundle history --execution-name`. |
| `--async` | Run asynchronously and return the query ID immediately. |

Expand

Show lessSee more

**Examples:**

Copy code

```
snow bundle execute MY_BUNDLE --entrypoint main.py
snow bundle execute MY_BUNDLE --entrypoint jobs/main.py -- --source-table RAW_SALES --output-table SALES_AGG
snow bundle execute MY_BUNDLE --entrypoint main.py --async
snow bundle execute MY_BUNDLE --entrypoint main.py --execution-name nightly_run
```

### snow bundle list

Lists Code Bundles.

```
Usage: snow bundle list [OPTIONS]
```

| Option | Description |
| --- | --- |
| `--like` | Filter bundles by pattern (for example, `"MY_%"`). |
| `--in-account` | List all bundles across the account. |
| `--in <scope> <name>` | Scope to a database or schema, for example `--in database MY_DB` or `--in schema MY_DB.MY_SCHEMA`. |

Expand

Show lessSee more

**Examples:**

Copy code

```
snow bundle list
snow bundle list --like "SALES%"
snow bundle list --in-account
```

### snow bundle alter

Alters a Code Bundle by adding a new version.

```
Usage: snow bundle alter [OPTIONS] IDENTIFIER
```

| Option | Description |
| --- | --- |
| `--add-version` | Source path for the new version. |

Expand

Show lessSee more

**Example:**

Copy code

```
snow bundle alter MY_BUNDLE --add-version @MY_STAGE/updated_project
```

### snow bundle delete

Drops a Code Bundle.

```
Usage: snow bundle delete [OPTIONS] IDENTIFIER
```

| Option | Description |
| --- | --- |
| `--if-exists` | Don’t error if the bundle doesn’t exist. |

Expand

Show lessSee more

**Examples:**

Copy code

```
snow bundle delete MY_BUNDLE
snow bundle delete MY_BUNDLE --if-exists
```

### snow bundle status

Returns the execution status of an async Code Bundle execution.

```
Usage: snow bundle status QUERY_ID
```

**Example:**

Copy code

```
snow bundle status 01c51743-c819-4261-0000-5349586311aa
```

### snow bundle history

Returns the run history of Code Bundles from [CODE\_BUNDLE\_HISTORY](/sql-reference/functions/code_bundle_history). All options are
optional filters.

```
Usage: snow bundle history [OPTIONS]
```

| Option | Description |
| --- | --- |
| `--bundle-name` | Return runs of the Code Bundle with this name. |
| `--bundle-database`, `--bundle-schema` | Return runs of Code Bundles in this database or schema. |
| `--entrypoint` | Return runs with this entrypoint. |
| `--start-time-range-start`, `--start-time-range-end` | Return runs that started in this time range. |
| `--bundle-types`, `--compute-types`, `--language-types` | Return runs of these bundle types (`custom`, `spark`, `ml`), compute types (`warehouse`, `compute_pool`), or languages (`python`, `java`, `scala`). |
| `--status` | Return runs with this status: `pending`, `running`, `done` (or `succeeded`), `failed`, `cancelled` (or `canceled`), or `deleted`. |
| `--execution-name` | Return runs with this execution name. |
| `--result-limit` | Maximum number of runs to return. Default: 100. |

Expand

Show lessSee more

**Example:**

Copy code

```
snow bundle history --bundle-name MY_BUNDLE
snow bundle history --bundle-name MY_BUNDLE --status failed --result-limit 5
snow bundle history --execution-name nightly_run
```

### snow bundle cancel

Cancels an async Code Bundle execution.

```
Usage: snow bundle cancel QUERY_ID
```

**Example:**

Copy code

```
snow bundle cancel 01c51743-c819-4261-0000-5349586311aa
```
