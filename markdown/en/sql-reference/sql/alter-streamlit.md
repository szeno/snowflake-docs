# ALTER STREAMLIT

Modifies the properties of an existing Streamlit object.

See also:
:   [CREATE STREAMLIT](/sql-reference/sql/create-streamlit), [SHOW STREAMLITS](/sql-reference/sql/show-streamlits), [DESCRIBE STREAMLIT](/sql-reference/sql/desc-streamlit), [DROP STREAMLIT](/sql-reference/sql/drop-streamlit)

## Syntax

Copy code

```
ALTER STREAMLIT [ IF EXISTS ] <name> SET
  [ MAIN_FILE = '<filename>']
  [ QUERY_WAREHOUSE = <warehouse_name> ]
  [ RUNTIME_NAME = '<runtime_name>' ]
  [ COMPUTE_POOL = <compute_pool_name> ]
  [ COMMENT = '<string_literal>']
  [ TITLE = '<app_title>' ]
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [ , ... ] ) ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
  [ SECRETS = ( '<snowflake_secret_name>' = <snowflake_secret> [ , ... ] ) ]

ALTER STREAMLIT [ IF EXISTS ] <name> UNSET { SECRETS                      |
                                             EXTERNAL_ACCESS_INTEGRATIONS |
                                             QUERY_WAREHOUSE              |
                                             TITLE                        |
                                             COMMENT
                                           }
                                           [ , ... ]

ALTER STREAMLIT [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER STREAMLIT <name> COMMIT

ALTER STREAMLIT <name> PUSH [ TO <git_branch_uri> ]
  [
    {
      GIT_CREDENTIALS = <snowflake_secret>
      | USERNAME = <git_username> PASSWORD = <git_password>
    }
    NAME = <git_author_name>
    EMAIL = <git_author_email>
  ]
  [ COMMENT = <git_push_comment> ]

ALTER STREAMLIT <name> ABORT

ALTER STREAMLIT <name> PULL

ALTER STREAMLIT <name> ADD LIVE VERSION FROM LAST
```

**For Streamlit objects created with ROOT\_LOCATION, only the following syntax is supported:**

Important

- ROOT\_LOCATION is a legacy parameter and may be deprecated in a future release.
- For container runtimes, ROOT\_LOCATION is not supported.
- For Streamlit apps created using ROOT\_LOCATION, multi-file editing and Git integration are not supported.

Copy code

```
ALTER STREAMLIT [ IF EXISTS ] <name> SET
  [ ROOT_LOCATION = '<stage_path_and_root_directory>' ]
  [ MAIN_FILE = '<path_to_main_file>']
  [ QUERY_WAREHOUSE = <warehouse_name> ]
  [ COMMENT = '<string_literal>']
  [ TITLE = '<app_title>' ]
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [ , ... ] ) ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]

ALTER STREAMLIT [ IF EXISTS ] <name> RENAME TO <new_name>
```

## Parameters

`name`
:   Identifier for the Streamlit object. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`SET ...`
:   Specifies the property to set for the Streamlit object:

    `MAIN_FILE = 'filename'`
    :   Specifies the Streamlit entrypoint file. The requirements depend on the runtime type:

    - **Warehouse runtimes**: The file must be in the root of the source directory specified in FROM.
      Only a filename is allowed, not a path.
    - **Container runtimes**: The file can be in the root or a subdirectory. You can specify a relative
      path from the root of the source directory, like `'subdir/my_app.py'`.

      If your app was created with ROOT\_LOCATION instead of FROM, then MAIN\_FILE can be a path relative to ROOT\_LOCATION
      even though ROOT\_LOCATION only supports warehouse runtimes.

    `QUERY_WAREHOUSE = warehouse_name`
    :   Specifies the warehouse used by the Streamlit app. The behavior depends on the runtime type:

        - **Warehouse runtimes**: Specifies the warehouse to run the app code and execute SQL queries.
          This is the code warehouse. It’s recommended to manually switch to a different warehouse within your app code for queries.
        - **Container runtimes**: Specifies the warehouse to execute SQL queries issued by the app.
          The app code runs on the compute pool specified by COMPUTE\_POOL.

    `RUNTIME_NAME = 'runtime_name'`
    :   Specifies the runtime environment for the Streamlit app. Use this to change the runtime from
        warehouse to container or from container to warehouse.

        - **Warehouse runtime**: Run the app in a virtual warehouse. Each viewer gets a personal instance
          of the app. Use `SYSTEM$WAREHOUSE_RUNTIME`. The Python version is selected separately
          using the `environment.yml` file.
        - **Container runtimes**: Run the app in a Snowpark Container Services compute pool. All viewers
          share a single, long-running instance of the app. Container runtime names include the Python
          version. The following container runtimes are valid:
          - `SYSTEM$ST_CONTAINER_RUNTIME_PY3_11`

        Important

        When changing from a warehouse runtime to a container runtime, you must also
        set the COMPUTE\_POOL parameter as appropriate. Container runtimes require a compute pool.

    `COMPUTE_POOL = compute_pool_name`
    :   Specifies the compute pool where the Streamlit app runs. This parameter is required when using
        a container runtime and is ignored for warehouse runtimes.

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the Streamlit object.

    `TITLE = 'app_title'`
    :   Adds a title for the Streamlit app to display in Snowsight.

    `IMPORTS = ( 'stage_path_and_directory_or_file_name_to_read' [ , ... ] )`
    :   The location (stage), path, and name of the directory or file(s) to import. This only applies to warehouse runtimes and
        is ignored for container runtimes.

    `EXTERNAL_ACCESS_INTEGRATIONS = ( integration_name [ , ... ] )`
    :   The names of [external access integrations](/sql-reference/sql/create-external-access-integration) needed in order for the
        Streamlit app code to access external networks.

        For container runtimes, external access integrations are required to install packages from external package indexes
        like PyPI. For all runtime types, external access integrations enable the app to make outbound network requests.

    `SECRETS = ( 'snowflake_secret_name' = snowflake_secret [ , ... ] )`
    :   Maps Snowflake secrets to secret names that can be referenced in the Streamlit app code. The secret name (left side)
        is how you reference the secret in your code, and the secret object (right side) is the identifier of the Snowflake secret.

        For example: `SECRETS = ('api_key' = my_database.my_schema.my_secret)`

        In warehouse runtimes, secrets are accessed through the `_snowflake` module. In container runtimes,
        secrets are accessible through `st.secrets` and are also mapped to environment variables.
        Secrets must be associated with an external access integration in EXTERNAL\_ACCESS\_INTEGRATIONS.
        For more information, see [Manage secrets and configure your Streamlit app](/developer-guide/streamlit/app-development/secrets-and-configuration).

    `ROOT_LOCATION = 'stage_path_and_root_directory'`
    :   Specifies the root stage name and prefix containing the Streamlit Python files, media files, and `environment.yml`
        file. This parameter must point to a single directory inside a named internal stage.

`UNSET ...`
:   Specifies one or more properties to unset for the Streamlit object, which resets them to their defaults:

    - `SECRETS`
    - `EXTERNAL_ACCESS_INTEGRATIONS`
    - `QUERY_WAREHOUSE`
    - `TITLE`
    - `COMMENT`

`RENAME TO new_name`
:   Specifies the new identifier for the Streamlit object. The identifier must be unique for the schema where the object was created.

    For more details about identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

`COMMIT`
:   Commits the pending edits in the LIVE version to a new LAST version. Immediately after the commit,
    the LIVE version is identical to the LAST version.

    [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

`PUSH`
:   Pushes the latest committed changes to the Git repo, using the branch stored in the base version if `TO git_branch_uri` is not specified.

    If the base version is not based on a Git branch, this throws an error.

    [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

    `TO git_branch_uri`
    :   Pushes committed changes to the specified branch.

    `GIT_CREDENTIALS = snowflake_secret`
    :   Specifies the Snowflake secret containing the credentials to use for authenticating with the repository.

    `USERNAME = git_username`
    :   Specifies a Git username.

    `PASSWORD = git_password`
    :   Specifies a Git password.

    `NAME = git_author_name`
    :   Specifies the name of the git author to use.

    `EMAIL = git_author_email`
    :   Specifies a valid e-mail address to use as the git author’s name.

    `COMMENT = git_push_comment`
    :   Specifies a comment to include in the git push.

`ABORT`
:   Removes the current live version of the app, including all edits made in
    Snowsight that have not been committed.

    [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

`PULL`
:   Pulls latest changes. You must abort the current live version before pulling.

    [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

`ADD LIVE VERSION FROM LAST`
:   Creates a new live version of the app based on the last committed version.

    When the owner of a Streamlit app opens the app in Snowsight and a
    live version doesn’t exist, this command is executed automatically. If a
    different user visits the app and a live version doesn’t exist, an error is
    returned.

## Access control requirements

If your role does not own the objects in the following table, then your role
must have the listed
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) on those objects:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Streamlit object that you alter |  |
| USAGE | Warehouse used by the Streamlit app | This privilege is only required if you set a new value for QUERY\_WAREHOUSE. |
| USAGE | Compute pool used by the Streamlit app | This privilege is only required if you set a new value for COMPUTE\_POOL. |
| USAGE | External access integrations used by the Streamlit app | This privilege is only required if you set a new value for EXTERNAL\_ACCESS\_INTEGRATIONS. |
| USAGE | Secrets used by the Streamlit app | This privilege is only required if you set a new value for SECRETS. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- If you remove the live version of the app, a user can’t visit the app until
  you do one of the following actions:

  - Execute ALTER STREAMLIT … ADD LIVE VERSION FROM LAST on the Streamlit
    object.
  - Visit the app in Snowsight with the role that owns the app.
- If you run the ALTER STREAMLIT command while viewing a Streamlit app in Snowsight,
  the app reflects the changes differently depending on the runtime type:

  - **Warehouse runtime**: The app doesn’t reflect the changes until you select **Run**.
  - **Container runtime**: The app reflects the changes immediately when you next interact with the app.

  If you want your changes reflected in the app, you must reload or reboot the app.
- When migrating from warehouse runtime to container runtime:

  - You must set both RUNTIME\_NAME and COMPUTE\_POOL.
  - Your app must use Python 3.11 and Streamlit 1.50 or later.
  - Ensure your app code is thread-safe and optimized for concurrent viewers.
  - Replace `get_active_session()` with `st.connection("snowflake")`.
  - Replace `_snowflake` module with native Python equivalents.

  For a complete migration checklist, see [Migrating between runtime environments](/developer-guide/streamlit/migrations-and-upgrades/runtime-migration).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

### Change the query warehouse

To change the warehouse used by a Streamlit app, run the ALTER STREAMLIT command as shown in the following example:

Copy code

```
ALTER STREAMLIT my_app
  SET QUERY_WAREHOUSE = new_warehouse;
```

### Migrate from a warehouse runtime to a container runtime

To migrate a Streamlit app from warehouse runtime to container runtime, run the ALTER STREAMLIT command as shown in the following example:

Copy code

```
ALTER STREAMLIT my_app SET
  RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
  COMPUTE_POOL = my_compute_pool
  EXTERNAL_ACCESS_INTEGRATIONS = (pypi_access_integration);
```

Container runtimes require an external access integration to install packages from external package indexes like PyPI. Otherwise, they
can only use the default, pre-installed packages. For more information, see [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management).

### Add secrets to an existing warehouse-runtime app

To add secrets to an existing warehouse-runtime Streamlit app, run the ALTER STREAMLIT command as shown in the following example:

Copy code

```
ALTER STREAMLIT my_app SET
  EXTERNAL_ACCESS_INTEGRATIONS = (my_access_integration)
  SECRETS = ('api_key' = my_database.my_schema.my_api_secret);
```

Secrets must be associated with an external access integration. In warehouse runtimes, secrets are accessed
through the `_snowflake` module. In container runtimes, secrets are accessible through `st.secrets`
and as environment variables. For more information, see
[Manage secrets and configure your Streamlit app](/developer-guide/streamlit/app-development/secrets-and-configuration).

### Remove secrets from an app

To remove all secrets from a Streamlit app, run the ALTER STREAMLIT command as shown in the following example:

Copy code

```
ALTER STREAMLIT my_app
  UNSET SECRETS;
```

This removes all secret associations from the app. The underlying secret objects remain in your Snowflake account.
To also remove the external access integrations, unset both properties:

Copy code

```
ALTER STREAMLIT my_app
  UNSET SECRETS, EXTERNAL_ACCESS_INTEGRATIONS;
```

For more information, see [Manage secrets and configure your Streamlit app](/developer-guide/streamlit/app-development/secrets-and-configuration).

### Rename a Streamlit app

To rename a Streamlit app, run the ALTER STREAMLIT command as shown in the following example:

Copy code

```
ALTER STREAMLIT old_app_name
  RENAME TO new_app_name;
```
