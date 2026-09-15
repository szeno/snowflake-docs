# EXECUTE DBT PROJECT

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

Executes the specified [dbt project object](/user-guide/data-engineering/dbt-projects-on-snowflake) or the dbt project in a Snowflake workspace using the dbt command and command-line options specified.

See also:
:   [CREATE DBT PROJECT](/sql-reference/sql/create-dbt-project), [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project), [DESCRIBE DBT PROJECT](/sql-reference/sql/desc-dbt-project), [DROP DBT PROJECT](/sql-reference/sql/drop-dbt-project), [SHOW DBT PROJECTS](/sql-reference/sql/show-dbt-projects)

## Syntax

Executes the dbt project object with the specified name.

Copy code

```
EXECUTE DBT PROJECT [ IF EXISTS ] <name>
  [ ARGS = '[ <dbt_command> ] [ --<dbt_cli_option> <option_value_1> [ ... ] ] [ ... ]' ]
  [ DBT_VERSION = 'version_number' ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
  [ ENVIRONMENT = '<environment_name>' ]
  [ ENV_VARS = ( '<key>' = '<value>' [ , ... ] ) ]
  [ IMPORTS = ( { '<source_location>' | <system_function> } [ AS '<alias>' ] [ , ... ] ) ]
  [ WRITEBACK = { TRUE | FALSE } ]
```

## Variant syntax

Executes the dbt project that is saved in a workspace with the specified workspace name. The user who owns the workspace must be the user who runs this command variant.

Copy code

```
EXECUTE DBT PROJECT [ IF EXISTS ] [ FROM WORKSPACE <name> ]
  [ ARGS = '[ <dbt_command> ] [ --<dbt_cli_option> <option_value_1> [ ... ] [ ... ] ]' ]
  [ DBT_VERSION = 'version_number' ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
  [ ENVIRONMENT = '<environment_name>' ]
  [ ENV_VARS = ( '<key>' = '<value>' [ , ... ] ) ]
  [ PROJECT_ROOT = '<subdirectory_path>' ]
```

## Required parameters

`name`
:   When executing a dbt project object, specifies the name of the dbt project object to execute.

    When executing a dbt project by using the FROM WORKSPACE option, specifies the name of the workspace for dbt Projects on Snowflake. The workspace name is always specified in reference to the `public` schema in the user’s personal database, which is indicated by `user$`.

    We recommend enclosing the workspace name in double quotes because workspace names are case-sensitive and can contain special characters.

    The following example shows a workspace name reference:

    `user$.public."My dbt Project Workspace"`

## Optional parameters

`ARGS = '[ dbt_command ] [ --dbt_cli_option option_value_1 [ ... ] [ ... ] ]'`
:   Specifies the [dbt command](https://docs.getdbt.com/reference/dbt-commands) and supported [command-line options](https://docs.getdbt.com/reference/global-configs/about-global-configs#available-flags) to use when the dbt project object executes. This is a literal string that must conform to the syntax and requirements of dbt CLI commands.

    If no value is specified, the dbt project object executes with the [dbt command](https://docs.getdbt.com/reference/dbt-commands) and [command-line options](https://docs.getdbt.com/reference/global-configs/about-global-configs#available-flags) specified in the [dbt project object definition](/sql-reference/sql/create-dbt-project). If you specify dbt CLI options without specifying a dbt command, the dbt `run` command executes by default.

    Default: No value

`DBT_VERSION = 'version_number'`
:   Specifies a version for the dbt project object.

    Default: When you execute a dbt project object, the system uses the default version you specified when creating the dbt project object. If none was specified, the system uses `1.9.4` by default.

    For more information, see [Supported dbt versions for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions).

`PROJECT_ROOT = 'subdirectory_path'`
:   Specifies the subdirectory path to the `dbt_project.yml` file within the dbt project object or workspace. This parameter is only supported when executing a dbt project by using the FROM WORKSPACE option.

    If no value is specified, the dbt project object executes with the `dbt_project.yml` file in the root directory of the dbt project object.

    If no `dbt_project.yml` file exists in the root directory or in the PROJECT\_ROOT subdirectory, an error occurs.

    Default: No value

`EXTERNAL_ACCESS_INTEGRATIONS = ( integration_name [ , ... ] )`
:   Specifies the external access integration that grants dbt outbound network access to external endpoints. Most commonly, this lets dbt pull remote packages from the dbt package hub or a Git provider such as GitHub when `dbt deps` runs during execution.

    If a command needs external access during execution (for example, `dbt deps`), specify `EXTERNAL_ACCESS_INTEGRATIONS` on the EXECUTE DBT PROJECT command. This also applies when your project resolves a Snowflake secret from an `env.yml` file to authenticate private Git packages. For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

    For more information, see [Understand dependencies for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dependencies).

`ENVIRONMENT = 'environment_name'`
:   Selects the named environment defined in the project’s `env.yml` file for this execution. The environment determines which set of environment variables and secrets is injected before dbt runs.

    This argument takes the highest precedence for environment selection, overriding the `DEFAULT_ENVIRONMENT` set on the dbt project object and the `default_environment` in `env.yml`. To run without any environment, use the reserved name `NO_ENV`.

    Default: The dbt project object’s `DEFAULT_ENVIRONMENT`, or the `default_environment:` in `env.yml` if `DEFAULT_ENVIRONMENT` isn’t set.

    For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

`ENV_VARS = ( 'key' = 'value' [ , ... ] )`
:   Overrides individual environment variables for a single execution. These overrides merge into the selected environment and take final precedence over values in `env.yml`.

    Keys must be prefixed with `DBT_` and uppercase. Values can be SQL that resolves to a single `VARCHAR` value, string literals, session variables (`$var`), or bind placeholders (`?`). Snowflake secrets can’t be referenced directly in `ENV_VARS`; manage secrets through the `env.yml` file instead.

    Default: No value

    For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

`IMPORTS = ( { 'source_location' | system_function } [ AS 'alias' ] [ , ... ] )`
:   When executing a deployed dbt project object, makes files from one or more source locations
    available under the project’s `./imports` directory. You can import from a stage, a deployed dbt
    project object, a workspace, or one of these system functions:

    - [SYSTEM$DBT\_GET\_LAST\_SUCCESSFUL\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_successful_run_target)
    - [SYSTEM$DBT\_GET\_LAST\_FAILED\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_failed_run_target)
    - [SYSTEM$DBT\_GET\_LAST\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_run_target)
    - [SYSTEM$LOCATE\_DBT\_ARTIFACTS](/sql-reference/functions/system_locate_dbt_artifacts)
    - [SYSTEM$LOCATE\_DBT\_ARCHIVE](/sql-reference/functions/system_locate_dbt_archive)

    Other system functions aren’t supported in `IMPORTS`.

    Use `AS '<alias>'` to name the subdirectory for an import. For example, `AS 'state'` mounts the
    imported files at `./imports/state`. The `--state` option in `ARGS` must point to the mounted
    directory. `IMPORTS` alone doesn’t tell dbt to use the files as state. For a complete example, see
    [Run changed models by importing state from a production project](#label-execute-dbt-project-state-import-example).

    Without an alias, Snowflake derives a lowercase directory name in the form
    `{lowercased object name}_{lowercased last folder name}`. For example, `@my_dbt_project/target/`
    mounts at `./imports/my_dbt_project_target`, while a `target` directory from a dbt project object named
    `DBT_PROD` mounts at `./imports/dbt_prod_target`. Use an alias when you want a shorter, more
    predictable path.

    An `IMPORTS` list can include at most one ZIP file. To import it, use the
    [`SYSTEM$LOCATE_DBT_ARCHIVE`](/sql-reference/functions/system_locate_dbt_archive) system function,
    which returns the archive from a dbt project object’s results stage. ZIP files from other source
    locations aren’t supported. Snowflake extracts the archive automatically.

    For dbt artifacts from the most recent successful execution of a dbt project object, use
    [SYSTEM$DBT\_GET\_LAST\_SUCCESSFUL\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_successful_run_target). To import dbt artifacts from
    a specific query, use [SYSTEM$LOCATE\_DBT\_ARTIFACTS](/sql-reference/functions/system_locate_dbt_artifacts). This function mounts
    the query’s results directory, so the dbt artifacts are under `./imports/<alias>/target`.

    Default: No value

`WRITEBACK = { TRUE | FALSE }`
:   When executing a deployed dbt project object, overrides its `DEFAULT_WRITEBACK` property for this
    execution:

    - `TRUE`: Writes generated target and log files back to the mutable live version.
    - `FALSE`: Doesn’t write generated target and log files back to the live version.

    For concurrent executions that don’t need to update the live version, Snowflake recommends `WRITEBACK = FALSE`. If writeback is required, use
    distinct, non-overlapping target and log directories for each execution. Snowflake stores the per-query result artifacts and archive
    regardless of this setting.

    Default: The dbt project object’s `DEFAULT_WRITEBACK` value.

## Output

| Column | Description |
| --- | --- |
| `0|1 Success` | `TRUE` if the dbt project object executed successfully; otherwise, `FALSE`. If the dbt project object fails to execute, an exception message is returned. |
| `EXCEPTION` | Any exception message returned by the dbt project execution. If the dbt project object executes successfully, the string `None` is returned. |
| `STDOUT` | The standard output returned by the dbt project execution. |
| `OUTPUT_ARCHIVE_URL` | The URL of the output archive that contains output files of the dbt project execution. This includes log files and artifacts that dbt writes to the `/target` directory. For more information, see [About dbt artifacts](https://docs.getdbt.com/reference/artifacts/dbt-artifacts) in dbt documentation. Selecting this link directly results in an error; however, you can use this URL to retrieve dbt project files and output. For more information, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs). |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| USAGE | dbt project |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

Note

The dbt command specified in EXECUTE DBT PROJECT runs with the privileges of the `role` specified in the `outputs` block of the project’s [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` file. Operations are further restricted to only those privileges granted to the Snowflake user calling EXECUTE DBT PROJECT. Both the user and the role specified must have the required privileges to use the `warehouse`, perform operations on the `database` and `schema` specified in the profile file, and perform operations on any other Snowflake objects that the dbt model specifies. Snowflake uses `dbt_projects_profiles.yml` when both files are present.

## Examples

- [Default run command with target and models specified](#label-execute-dbt-project-default-run-example)
- [Explicit test command with target and models specified](#label-execute-dbt-project-test-example)
- [Explicit run command with downstream models specified](#label-execute-dbt-project-explicit-run-example)
- [Run changed models by importing state from a production project](#label-execute-dbt-project-state-import-example)
- [Run changed models by importing state from a specific query](#label-execute-dbt-project-query-state-import-example)
- [Run a dbt project object concurrently](#label-execute-dbt-project-concurrent-no-writeback-example)
- [Execute and test dbt project objects using production tasks](#label-execute-dbt-project-tasks-example)

### Default run command with target and models specified

Execute a dbt `run` targeting the `dev` profile in the `dbt_project.yml` file in the root directory of the dbt project object and selecting three models from the project DAG. No `run` command is explicitly specified and is executed by default.

Copy code

```
EXECUTE DBT PROJECT my_database.my_schema.my_dbt_project
  ARGS = '--select simple_customers combined_bookings prepped_data --target dev';
```

### Explicit test command with target and models specified

Execute a dbt `test` command targeting the `prod` profile in the `dbt_project.yml` file in the root directory of the dbt project object and selecting three models from the project DAG.

Copy code

```
EXECUTE DBT PROJECT my_database.my_schema.my_dbt_project
  ARGS = '--select simple_customers combined_bookings prepped_data --target prod';
```

### Explicit run command with downstream models specified

Execute a dbt `run` command targeting the `dev` profile in the `dbt_project.yml` file and selecting all models downstream of the `simple_customers` model using the dbt `+` notation.

Copy code

```
EXECUTE DBT PROJECT my_database.my_schema.my_dbt_project
  ARGS = 'run --select simple_customers+ --target dev';
```

### Run changed models by importing state from a production project

Import dbt artifacts from the most recent successful execution of a production dbt project
object. The alias `state` mounts the returned artifacts at `./imports/state`. The dbt arguments
compare the current project with those artifacts, select changed nodes and their downstream
dependencies, and defer references for unbuilt nodes:

Copy code

```
EXECUTE DBT PROJECT ci_database.dbt_projects.pr_test_project
  ARGS = 'run --state ./imports/state --defer --select state:modified+'
  IMPORTS = (
    SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET(
      'prod_database.dbt_projects.production_project'
    ) AS 'state'
  );
```

The role that executes this statement must have the `MONITOR` privilege on
`prod_database.dbt_projects.production_project`. That object must have a successful execution from
the previous 7 days. For details, see
[SYSTEM$DBT\_GET\_LAST\_SUCCESSFUL\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_successful_run_target).

### Run changed models by importing state from a specific query

Use `SYSTEM$LOCATE_DBT_ARTIFACTS` to import the results directory from a specific dbt project
execution. The `state` alias mounts the directory at `./imports/state`, and the dbt artifacts are
in its `target` subdirectory:

Copy code

```
EXECUTE DBT PROJECT ci_database.dbt_projects.pr_test_project
  ARGS = 'run --state ./imports/state/target --defer --select state:modified+'
  IMPORTS = (
    SYSTEM$LOCATE_DBT_ARTIFACTS(
      '01c6a772-001e-db19-0000-5349650b6cfe'
    ) AS 'state'
  );
```

For requirements and query ID lookup examples, see
[SYSTEM$LOCATE\_DBT\_ARTIFACTS](/sql-reference/functions/system_locate_dbt_artifacts).

### Import a ZIP archive from a results stage

`SYSTEM$LOCATE_DBT_ARCHIVE` is the supported way to import a ZIP file. It returns an archive from a
dbt project object’s results stage. An `IMPORTS` list can include at most one ZIP file. ZIP files
from other source locations aren’t supported. Snowflake extracts the archive automatically:

Copy code

```
EXECUTE DBT PROJECT ci_database.dbt_projects.pr_test_project
  ARGS = 'run --state ./imports/archive --defer --select state:modified+'
  IMPORTS = (
    SYSTEM$LOCATE_DBT_ARCHIVE(
      '01c6a772-001e-db19-0000-5349650b6cfe'
    ) AS 'archive'
  );
```

To let Snowflake generate the mount directory name, omit `AS '<alias>'`. For example, if the query
ID identifies an execution of a dbt project object named `PROD_PROJECT`, Snowflake extracts the
archive under `./imports/prod_project_dbt_artifacts/`:

Copy code

```
EXECUTE DBT PROJECT ci_database.dbt_projects.pr_test_project
  ARGS = 'run --state ./imports/prod_project_dbt_artifacts/target --defer --select state:modified+'
  IMPORTS = (
    SYSTEM$LOCATE_DBT_ARCHIVE('<query_id>')
  );
```

For requirements, see [SYSTEM$LOCATE\_DBT\_ARCHIVE](/sql-reference/functions/system_locate_dbt_archive).

### Run a dbt project object concurrently

For concurrent executions of the same dbt project object, Snowflake recommends
`WRITEBACK = FALSE` when the executions don’t need to persist target and log artifacts to the live
version. This prevents the executions from writing artifacts to overlapping target and log
directories. Snowflake continues to store per-query result artifacts.

Use `WRITEBACK = FALSE` for each concurrent execution:

Copy code

```
EXECUTE DBT PROJECT my_database.my_schema.my_dbt_project
  ARGS = 'run --target prod'
  WRITEBACK = FALSE;
```

For an alternative that writes to distinct target and log directories, see
[Run a dbt project object concurrently](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod#label-dbt-project-concurrent-executions).

### Execute and test dbt project objects using production tasks

Create a task for a production dbt target that executes a dbt `run` command on a six-hour interval. Then create a task that executes the dbt `test` command after each dbt `run` task completes. The EXECUTE DBT PROJECT command for each task targets the `prod` profile in the `dbt_project.yml` file in the root directory of the dbt project object.

Copy code

```
CREATE OR ALTER TASK my_database.my_schema.run_dbt_project
  WAREHOUSE = my_warehouse
  SCHEDULE = '6 hours'
AS
  EXECUTE DBT PROJECT my_database.my_schema.my_dbt_project args='run --target prod';

CREATE OR ALTER TASK change_this.public.test_dbt_project
        WAREHOUSE = my_warehouse
        AFTER run_dbt_project
AS
  EXECUTE DBT PROJECT my_database.my_schema.my_dbt_project args='test --target prod';
```

### Override the project’s pinned version at execution time for testing or temporary needs

`my_dbt_project` is pinned to 1.9.4. This execution overrides the dbt project object’s default 1.9.4 version:

Copy code

```
EXECUTE DBT PROJECT finance_analytics
  DBT_VERSION = '1.11.11'
```

### Select an environment and override variables at execution time

Run against the `prod` environment defined in `env.yml`, overriding a single variable for this execution:

Copy code

```
EXECUTE DBT PROJECT my_database.my_schema.my_dbt_project
  ARGS = 'run --target prod'
  ENVIRONMENT = 'prod'
  ENV_VARS = ( 'DBT_DATABASE' = 'tasty_bytes_staging_db' );
```

For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).
