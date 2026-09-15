# CREATE STREAMLIT

Creates a new Streamlit object in Snowflake or replaces an existing Streamlit
object in the same schema.

See also:
:   [SHOW STREAMLITS](/sql-reference/sql/show-streamlits), [DESCRIBE STREAMLIT](/sql-reference/sql/desc-streamlit), [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit),
    [DROP STREAMLIT](/sql-reference/sql/drop-streamlit), [UNDROP STREAMLIT](/sql-reference/sql/undrop-streamlit)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] STREAMLIT [ IF NOT EXISTS ] <name>
  [ FROM <source_location> ]
  [ MAIN_FILE = '<filename>' ]
  [ QUERY_WAREHOUSE = <warehouse_name> ]
  [ RUNTIME_NAME = '<runtime_name>' ]
  [ COMPUTE_POOL = <compute_pool_name> ]
  [ COMMENT = '<string_literal>' ]
  [ TITLE = '<app_title>' ]
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [ , ... ] ) ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
  [ SECRETS = ( '<snowflake_secret_name>' = <snowflake_secret> [ , ... ] ) ]
```

**The following syntax is legacy:**

Important

- ROOT\_LOCATION is a legacy parameter and may be deprecated in a future release.
- For container runtimes, ROOT\_LOCATION is not supported.
- For Streamlit apps created using ROOT\_LOCATION, multi-file editing and Git integration are not supported.

Copy code

```
CREATE [ OR REPLACE ] STREAMLIT [ IF NOT EXISTS ] <name>
  ROOT_LOCATION = '<stage_path_and_root_directory>'
  MAIN_FILE = '<path_to_main_file_in_root_directory>'
  [ QUERY_WAREHOUSE = <warehouse_name> ]
  [ COMMENT = '<string_literal>' ]
  [ TITLE = '<app_title>' ]
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [ , ... ] ) ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
```

## Required parameters

`name`
:   Specifies the identifier (i.e. name) for the Streamlit object. This identifier
    must be unique for the schema where the object is created.

    In addition, the identifier must start with an alphabetic character and can’t
    contain spaces or special characters unless the entire identifier string is
    enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in
    double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`FROM source_location`
:   Copies the app source files from the specified location. The location must be
    within an internal named stage. The path can be relative or fully qualified.
    For example, if the stage is named
    `@streamlit_db.streamlit_schema.streamlit_stage`, valid source locations can
    include:

    - A fully qualified path to the root of the stage:
      `FROM '@streamlit_db.streamlit_schema.streamlit_stage'`
    - A relative path to the root of the stage:
      `FROM '@streamlit_stage'`
    - A fully qualified or relative path to a subdirectory within the stage:
      `FROM '@streamlit_db.streamlit_schema.streamlit_stage/subdir'`

    Files are copied only one time when the CREATE command is executed; future
    changes to the source location don’t automatically update the Streamlit app.

    If this parameter isn’t specified, Snowflake copies the source files for a
    default app with a `streamlit_app.py` entrypoint file.

`MAIN_FILE = 'filename'`
:   Specifies the Streamlit entrypoint file. The requirements depend on the runtime type:

    - **Warehouse runtimes**: The file must be in the root of the source directory specified in FROM.
      Only a filename is allowed, not a path.
    - **Container runtimes**: The file can be in the root or a subdirectory. You can specify a relative
      path from the root of the source directory, like `'subdir/my_app.py'`.

    If you are using ROOT\_LOCATION instead of FROM, then MAIN\_FILE can be a path relative to ROOT\_LOCATION
    even though ROOT\_LOCATION only supports warehouse runtimes.

    DEFAULT: `'streamlit_app.py'`

`QUERY_WAREHOUSE = warehouse_name`
:   Specifies the warehouse used by the Streamlit app. The behavior depends on the runtime type:

    - **Warehouse runtimes**: Specifies the warehouse to run the app code and execute SQL queries.
      This is the code warehouse. It’s recommended to manually switch to a different warehouse within your app code for queries.
    - **Container runtimes**: Specifies the warehouse to execute SQL queries issued by the app.
      The app code runs on the compute pool specified by COMPUTE\_POOL.

    DEFAULT: No value

    Note

    Although you can create a Streamlit object without this parameter, the app
    won’t run until you specify a query warehouse.

`RUNTIME_NAME = 'runtime_name'`
:   Specifies the runtime environment for the Streamlit app. The runtime determines where and how
    the app executes.

    - **Warehouse runtime**: Run the app in a virtual warehouse. Each viewer gets a personal instance
      of the app. Use `SYSTEM$WAREHOUSE_RUNTIME`. The Python version is selected separately
      using the `environment.yml` file.
    - **Container runtimes**: Run the app in a Snowpark Container Services compute pool. All viewers
      share a single, long-running instance of the app. Container runtime names include the Python
      version. The following container runtimes are valid:
      - `SYSTEM$ST_CONTAINER_RUNTIME_PY3_11`

    The runtime defaults to the warehouse runtime.

    DEFAULT: `SYSTEM$WAREHOUSE_RUNTIME`

`COMPUTE_POOL = compute_pool_name`
:   Specifies the compute pool where the Streamlit app runs. This parameter is used only with
    container runtimes and is ignored for warehouse runtimes.

    If you omit this parameter when using a container runtime, Snowflake uses the compute pool specified by the
    [DEFAULT\_STREAMLIT\_COMPUTE\_POOL](/sql-reference/parameters#label-default-streamlit-compute-pool) parameter. If the DEFAULT\_STREAMLIT\_COMPUTE\_POOL parameter is
    updated after the Streamlit app is created, it won’t affect the compute pool used by the app.

    DEFAULT: The compute pool specified by the DEFAULT\_STREAMLIT\_COMPUTE\_POOL account parameter.

`COMMENT = 'string_literal'`
:   Specifies a comment for the Streamlit object.

    DEFAULT: No value

`TITLE = 'app_title'`
:   Specifies a title for the Streamlit object to display in Snowsight.

    DEFAULT: The name of the Streamlit object passed to CREATE STREAMLIT.

`IMPORTS = ( 'stage_path_and_directory_or_file_name_to_read' [ , ... ] )`
:   The location (stage), path, and name of the directory or file(s) to import. This only applies to warehouse runtimes and
    is ignored for container runtimes.

    DEFAULT: No value

`EXTERNAL_ACCESS_INTEGRATIONS = ( integration_name [ , ... ] )`
:   The names of [external access integrations](/sql-reference/sql/create-external-access-integration) needed in order for the
    Streamlit app code to access external networks.

    For container runtimes, external access integrations are required to install packages from external package indexes
    like PyPI. For all runtime types, external access integrations enable the app to make outbound network requests.

    DEFAULT: No value

`SECRETS = ( 'snowflake_secret_name' = snowflake_secret [ , ... ] )`
:   Maps Snowflake secrets to secret names that can be referenced in the Streamlit app code. The secret name (left side)
    is how you reference the secret in your code, and the secret object (right side) is the identifier of the Snowflake secret.

    For example: `SECRETS = ('api_key' = my_database.my_schema.my_secret)`

    In warehouse runtimes, secrets are accessed through the `_snowflake` module. In container runtimes,
    secrets are accessible through `st.secrets` and are also mapped to environment variables.
    Secrets must be associated with an external access integration in EXTERNAL\_ACCESS\_INTEGRATIONS.
    For more information, see [Manage secrets and configure your Streamlit app](/developer-guide/streamlit/app-development/secrets-and-configuration).

    DEFAULT: No value

`ROOT_LOCATION = 'stage_path_and_root_directory'`
:   Specifies the path to the named stage containing the Streamlit Python files, media files, and the
    `environment.yml` file, for example:

    Copy code

    ```
    ROOT_LOCATION = '@streamlit_db.streamlit_schema.streamlit_stage'
    ```

    In this example, the Streamlit files are located on a named stage named `streamlit_stage` within a database named
    `streamlit_db` and schema named `streamlit_schema`.

    Note

    - This parameter must point to a single directory inside a named internal stage.
    - External stages are not supported for Streamlit in Snowflake.
    - If you’re creating or replacing a Streamlit application object within the Snowflake Native App Framework, use `FROM 'relative_path_from_stage_root_directory'` and not `ROOT_LOCATION = 'stage_path_and_root_directory'`.

## Access control requirements

If your role does not own the objects in the following table, then your role
must have the listed
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) on those objects:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE STREAMLIT | Schema where you create the Streamlit object |  |
| READ | Stage from which you copy the Streamlit app source files |  |
| USAGE | Warehouse used by the Streamlit app |  |
| USAGE | Compute pool used by the Streamlit app | This privilege is only required if your app uses a container runtime. |
| USAGE | External access integrations used by the Streamlit app | This privilege is only required if your app uses external access integrations. For container runtimes, this privilege is required to install packages from external package indexes like PyPI. |
| USAGE | Secrets used by the Streamlit app | This privilege is only required if your app uses secrets and only applies to warehouse runtimes. |
| CREATE STAGE | Schema where you create the Streamlit object | This privilege is only required to create Streamlit objects with the ROOT\_LOCATION parameter. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You must initialize the app after creating it.

  Important

  After you use CREATE STREAMLIT, the Streamlit app isn’t live until you do one of the
  following actions:

  - Execute ALTER STREAMLIT … ADD LIVE VERSION FROM LAST on the new
    Streamlit object.
  - Visit the app in Snowsight with the role that owns the app.
- When you clone a schema or database containing a Streamlit object, the Streamlit object is not cloned.
- To specify the packages used by the Streamlit application, include a dependency file in the source files.
  The format of the dependency file depends on the runtime type:

  - **Warehouse runtime**: Use an `environment.yml` file.
  - **Container runtime**: Use a `pyproject.toml` or `requirements.txt` file.

  For more information, see [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

### Create a Streamlit app with default source files

To create a container-runtime Streamlit app from built-in default files, run the CREATE STREAMLIT
command as shown in the following example:

Copy code

```
CREATE STREAMLIT hello_streamlit
  RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
  COMPUTE_POOL = my_compute_pool
  QUERY_WAREHOUSE = my_warehouse;
```

By default, apps use the latest warehouse runtime if RUNTIME\_NAME isn’t specified. To create a warehouse-runtime
Streamlit app from built-in default files, run the CREATE STREAMLIT command as shown in the following example:

Copy code

```
CREATE STREAMLIT hello_streamlit
  QUERY_WAREHOUSE = my_warehouse;
```

### Create a Streamlit app from a custom source files

To create a container-runtime Streamlit app from custom source files, run the CREATE STREAMLIT
command as shown in the following example:

Copy code

```
CREATE STREAMLIT hello_streamlit
  FROM @streamlit_db.streamlit_schema.streamlit_stage
  MAIN_FILE = 'streamlit_main.py'
  QUERY_WAREHOUSE = my_warehouse
  RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
  COMPUTE_POOL = my_compute_pool;
```

To create a warehouse-runtime Streamlit app from custom source files, run the CREATE STREAMLIT
command as shown in the following example:

Copy code

```
CREATE STREAMLIT hello_streamlit
  FROM @streamlit_db.streamlit_schema.streamlit_stage
  MAIN_FILE = 'streamlit_main.py'
  QUERY_WAREHOUSE = my_warehouse;
```

### Create a warehouse-runtime Streamlit app with secrets

To create a warehouse-runtime Streamlit app with secrets, run the CREATE STREAMLIT command as shown in the following example:

Copy code

```
CREATE STREAMLIT hello_streamlit
  FROM @streamlit_db.streamlit_schema.streamlit_stage
  MAIN_FILE = 'streamlit_main.py'
  QUERY_WAREHOUSE = my_warehouse
  SECRETS = ('api_key' = streamlit_db.streamlit_schema.my_api_secret);
```

For container-runtime apps, secrets are accessible through `st.secrets` and as environment variables.
For more information, see [Manage secrets and configure your Streamlit app](/developer-guide/streamlit/app-development/secrets-and-configuration).

### Create a Streamlit app from a Git repository

To create a Streamlit app from a Git repository, run the CREATE STREAMLIT command as shown in the following example:

Copy code

```
CREATE STREAMLIT hello_streamlit
  FROM @streamlit_db.streamlit_schema.streamlit_repo/branches/streamlit_branch/
  MAIN_FILE = 'streamlit_main.py'
  QUERY_WAREHOUSE = my_warehouse;
```
