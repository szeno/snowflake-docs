# Snowflake Code Bundles

Availability

Notebook Project Objects have been renamed to **Code Bundles**. Scheduling notebooks on **compute pools (Snowpark Container Services)**, the capability previously delivered as Notebook Projects, is **generally available**. Running on **warehouses**, submitting **Spark jobs**, **inline specification** overrides, and the **REST API, Python API, and Snowflake CLI clients** are in **Public Preview**. For background on the rename, see the [behavior change announcement](/release-notes/bcr-bundles/un-bundled/bcr-2393). To schedule notebooks as Code Bundles, see [Run and schedule Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule).

Code Bundles let you package and execute non-SQL jobs, like Python, directly on Snowflake compute. Instead of building containers, wrapping logic in stored procedures, or porting your scripts into notebooks, you can upload your project code and run it with a single command. Snowflake automatically injects a Snowpark session at runtime, giving your code direct access to your data without managing connection credentials. You can orchestrate Code Bundles natively with Snowflake Tasks, or externally with the Snowflake CLI, the Snowflake Python API, or the Snowflake REST API.

You can also use Code Bundles to run Spark jobs (Scala, Java, or Python) on Snowflake warehouse compute. See [Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle) for details.

Code Bundles support two compute targets:

- **Warehouse**: Run Python scripts on Snowflake warehouse compute. Best for data processing jobs, ETL scripts, and workloads where the majority of the processing occurs in the warehouse as pushed-down SQL or UDFs.
- **Compute pool (Snowpark Container Services)**: Run on Snowpark Container Services. Best for workloads where more processing occurs in the Python process, jobs requiring GPU, or custom container runtimes.

## Key concepts

| Concept | Description |
| --- | --- |
| **Code Bundle** | A named object containing your project source files, created from a stage, workspace, or local directory. |
| **Specification** | A YAML configuration (`code_bundle.yml`) defining compute type, runtime version, dependencies, secrets, environment variables, and other settings. |
| **Entrypoint** | The file within the bundle that Snowflake executes (for example, `main.py`). |
| **Source** | Where the bundle files come from: a stage path (`@my_stage/path`), workspace path (`snow://workspace/...`), or local directory. |
| **Version** | An immutable snapshot of bundle files. New versions are added with `ALTER CODE BUNDLE ... ADD VERSION`. |

Expand

Show lessSee more

## Access control

Code Bundles use Snowflake’s standard role-based access control model. There are two privileges
relevant to Code Bundles:

- **CREATE CODE BUNDLE** on a schema: Allows a role to create new Code Bundles in that schema.
- **OWNERSHIP or USAGE** on a Code Bundle: Allows a role to execute the Code Bundle.

### Grant permission to create Code Bundles

An administrator must grant the CREATE CODE BUNDLE privilege to the roles that need to create bundles.
You can grant this at the schema level or omit `ON SCHEMA` to grant it at the account level:

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
- [Monitor Code Bundle execution status](#snow-bundle-history)

## Quickstart (Snowflake CLI)

This guide walks you through setting up your environment, creating your first Code Bundle, and executing it using the Snowflake CLI.

**Prerequisites**

- Ensure you have Python installed (3.10 through 3.12) to run the Snowflake CLI locally. This is separate from the runtime version your Code Bundle uses on Snowflake compute, which you set in `code_bundle.yml`.
- You need to install the development version of the Snowflake CLI to access Code Bundle features.

1. **Install the development version of the CLI using `uv` or `pip`.**

   Copy code

   ```
   # Using uv
   uv tool install git+https://github.com/snowflakedb/snowflake-cli@code
   # Using pip
   pip install git+https://github.com/snowflakedb/snowflake-cli@code
   ```

   Verify the installation by checking the version. Confirm that the output version ends with `.dev0`. The major, minor, and patch versions might be different.

   Copy code

   ```
   snow --version
   # Expected: Snowflake CLI version: 3.20.0.dev0
   ```
2. **Prepare your project.**

   Clone the sample repository to your local machine:

   Copy code

   ```
   git clone https://github.com/sfc-gh-jfreeberg/code-bundle-samples
   cd code-bundle-samples/python-on-wh
   ```

   This sample project contains two key files:

   - `main.py`: The Python job that runs on Snowflake.
   - `code_bundle.yml`: The bundle configuration, which is set up to run the Python project on warehouses.

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
- [Monitor Code Bundle execution status](#snow-bundle-history)

## Configuration overview (`code_bundle.yml`)

The `code_bundle.yml` file defines how your Code Bundle runs. Place it in the root of your project directory. The following examples show how to run your Code Bundle on virtual warehouses and compute pools. For a full reference of the configuration options, see [`code_bundle.yml` reference](/developer-guide/code-bundles/code-bundle-yml-reference).

### Warehouse compute

Note

Running Code Bundles on warehouse compute is in Public Preview. Running on compute pools (Snowpark Container Services) is generally available.

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
    query_warehouse: MY_DB.MY_SCHEMA.MY_WAREHOUSE
    runtime_version: 'V2.9-CPU-PY3.12'

  properties:
    requirements-file: requirements.txt
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

### Inline specification override

Note

Inline specification override is in Public Preview.

Override the stored `code_bundle.yml` at execution time using `WITH SPECIFICATION`. This is useful for testing different configurations without modifying the bundle.

Copy code

```
EXECUTE CODE BUNDLE my_bundle 
ENTRYPOINT = 'main.py'
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

## `code_bundle.yml` reference

The `code_bundle.yml` file defines how your Code Bundle runs, including the bundle type, compute type, runtime version, dependencies, secrets, environment variables, and stage mounts. For the full field-by-field reference, see [`code_bundle.yml` reference](/developer-guide/code-bundles/code-bundle-yml-reference).

## SQL reference

### CREATE CODE BUNDLE

Creates a new Code Bundle from source files.

Copy code

```
CREATE [ OR REPLACE ] CODE BUNDLE [ IF NOT EXISTS ] <name>
    FROM <source>
    [ COMMENT = '<string>' ];
```

**Parameters:**

| Parameter | Description |
| --- | --- |
| `<name>` | Identifier for the code bundle. |
| `FROM <source>` | Source location: a stage path (`@stage/path`) or a workspace path (`snow://workspace/...`). |
| `COMMENT` | Optional description. |

Expand

Show lessSee more

**Examples:**

Copy code

```
CREATE CODE BUNDLE my_bundle
  FROM @my_stage/project_files;

CREATE CODE BUNDLE my_bundle
  FROM snow://workspace/"USER$"."PUBLIC"."DEFAULT$"/versions/live;

CREATE OR REPLACE CODE BUNDLE my_bundle
  FROM @my_stage/project_files;
```

#### Access control requirements

To execute CREATE CODE BUNDLE, a role must have sufficient privileges to create objects in the target database and schema. Required privileges include:

- USAGE or OWNERSHIP on the database.
- USAGE or OWNERSHIP on the schema.
- CREATE CODE BUNDLE on the schema that allows creating objects within that schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on [securable objects](/user-guide/security-access-control-overview), see [Overview of Access Control](/user-guide/security-access-control-overview).

### EXECUTE CODE BUNDLE

Runs a Code Bundle at the specified entrypoint.

Copy code

```
EXECUTE CODE BUNDLE <name>
    ENTRYPOINT = '<path>'
    [ ARGUMENTS = ( '<arg>' [ , '<arg>' ... ] ) ]
    [ WITH SPECIFICATION $$ <yaml_spec> $$ ];
```

**Parameters:**

| Parameter | Description |
| --- | --- |
| `ENTRYPOINT` | File path within the bundle to execute. |
| `ARGUMENTS` | List of command-line argument strings passed to the script. |
| `WITH SPECIFICATION` | Inline YAML specification that overrides the stored `code_bundle.yml`. |

Expand

Show lessSee more

**Examples:**

Copy code

```
EXECUTE CODE BUNDLE my_bundle
  ENTRYPOINT = 'main.py';

EXECUTE CODE BUNDLE my_bundle
  ENTRYPOINT = 'jobs/main.py'
  ARGUMENTS = ('--source-table', 'RAW_SALES', '--output-table', 'SALES_AGG');

EXECUTE CODE BUNDLE my_bundle ENTRYPOINT = 'main.py'
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

#### Access control requirements

To execute EXECUTE CODE BUNDLE, a role must have either OWNERSHIP or USAGE privileges on the Code Bundle object.

If the Code Bundle is configured to run on Compute Pools (`compute_type: compute_pool`) then the executing role must have USAGE and MONITOR on the query warehouse, and USAGE or OWNERSHIP on the compute pool and the database and schema containing the Code Bundle.

In addition, the executing role must have READ or OWNERSHIP on any secrets referenced in the configuration file, and USAGE or OWNERSHIP on the external access integrations, artifact repositories, and other objects it references. USAGE on a secret is not sufficient.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on [securable objects](/user-guide/security-access-control-overview), see [Overview of Access Control](/user-guide/security-access-control-overview).

### ALTER CODE BUNDLE

Adds a new version to an existing Code Bundle.

Copy code

```
ALTER CODE BUNDLE <name> ADD VERSION FROM <source>;
```

**Example:**

Copy code

```
ALTER CODE BUNDLE my_bundle ADD VERSION FROM snow://workspace/"USER$"."PUBLIC"."DEFAULT$"/versions/live;
```

### DESCRIBE CODE BUNDLE

Returns metadata about a Code Bundle.

Copy code

```
DESCRIBE CODE BUNDLE <name>;
```

### SHOW CODE BUNDLES

Lists all Code Bundles in the current schema.

Copy code

```
SHOW CODE BUNDLES;
```

### DROP CODE BUNDLE

Removes a Code Bundle.

Copy code

```
DROP CODE BUNDLE [ IF EXISTS ] <name>;
```

### CODE\_BUNDLE\_HISTORY (table function)

Returns the execution history for a Code Bundle. All parameters are optional and act as filters.

Qualify the function with the `SNOWFLAKE` database, as shown in the following examples. If you call it unqualified and your session has no current database set, the query fails.

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(
    BUNDLE_NAME              => '<name>',
    DATABASE                 => '<database_name>',
    SCHEMA                   => '<schema_name>',
    ENTRYPOINT               => '<file_path>',
    START_TIME_RANGE_START   => '<timestamp>',
    START_TIME_RANGE_END     => '<timestamp>',
    BUNDLE_TYPES             => '<type>[, <type>, ...]',
    COMPUTE_TYPES            => '<type>[, <type>, ...]',
    LANGUAGE_TYPES           => '<type>[, <type>, ...]',
    STATUS                   => '<status>',
    EXECUTION_NAME           => '<name>',
    RESULT_LIMIT             => <integer>
));
```

**Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `BUNDLE_NAME` | STRING | Name of the Code Bundle to filter by. You can supply a fully qualified name (`DATABASE.SCHEMA.BUNDLE`) or a bare identifier combined with the `DATABASE` and `SCHEMA` parameters. |
| `DATABASE` | STRING | Database to use when resolving a bare `BUNDLE_NAME`. Ignored when `BUNDLE_NAME` is fully qualified. |
| `SCHEMA` | STRING | Schema to use when resolving a bare `BUNDLE_NAME`. Ignored when `BUNDLE_NAME` is fully qualified. |
| `ENTRYPOINT` | STRING | Exact match on the path of the entrypoint file that was executed (for example, `main.py`). |
| `START_TIME_RANGE_START` | TIMESTAMP\_LTZ | Start of the time window (inclusive). Returns only executions whose start time is on or after this timestamp. |
| `START_TIME_RANGE_END` | TIMESTAMP\_LTZ | End of the time window (inclusive). Returns only executions whose start time is on or before this timestamp. |
| `BUNDLE_TYPES` | STRING | Comma-separated list of bundle types to include. Case-insensitive. Allowed values: `custom` and `spark`. |
| `COMPUTE_TYPES` | STRING | Comma-separated list of compute types to include. Case-insensitive. Allowed values: `warehouse` and `compute_pool`. |
| `LANGUAGE_TYPES` | STRING | Comma-separated list of language runtimes to include. Case-insensitive. Allowed values: `python`, `java`, `scala`. |
| `STATUS` | STRING | Single status value to filter by. Allowed values: `pending`, `running`, `done` (succeeded), `failed`, `cancelled` (or `canceled`), `deleted`. |
| `EXECUTION_NAME` | STRING | Exact match on the `EXECUTION_NAME` property that was set in EXECUTE CODE BUNDLE. |
| `RESULT_LIMIT` | INTEGER | Maximum number of rows to return. Defaults to `100`. |

Expand

Show lessSee more

**Example:**

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(
    BUNDLE_NAME            => 'my_bundle',
    DATABASE               => 'my_db',
    SCHEMA                 => 'my_schema',
    ENTRYPOINT             => 'main.py',
    START_TIME_RANGE_START => '2026-07-01'::TIMESTAMP_LTZ,
    START_TIME_RANGE_END   => CURRENT_TIMESTAMP(),
    BUNDLE_TYPES           => 'custom',
    COMPUTE_TYPES          => 'warehouse',
    LANGUAGE_TYPES         => 'python',
    STATUS                 => 'failed',
    EXECUTION_NAME         => 'my-execution',
    RESULT_LIMIT           => 100
));
```

## CLI reference

Install the CLI with Code Bundle support:

Copy code

```
uv tool install git+https://github.com/snowflakedb/snowflake-cli@code
```

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
| `--async` | Run asynchronously and return the query ID immediately. |

Expand

Show lessSee more

**Examples:**

Copy code

```
snow bundle execute MY_BUNDLE --entrypoint main.py
snow bundle execute MY_BUNDLE --entrypoint jobs/main.py -- --source-table RAW_SALES --output-table SALES_AGG
snow bundle execute MY_BUNDLE --entrypoint main.py --async
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
| `--in-database` | Scope to a specific database. |

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

Returns the execution history of a Code Bundle.

```
Usage: snow bundle history [OPTIONS] IDENTIFIER
```

| Option | Description |
| --- | --- |
| `--result-limit` | Maximum number of history records to return. |

Expand

Show lessSee more

**Example:**

Copy code

```
snow bundle history MY_BUNDLE
snow bundle history MY_BUNDLE --result-limit 5
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
