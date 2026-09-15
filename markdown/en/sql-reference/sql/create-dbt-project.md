# CREATE DBT PROJECT

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

Creates a new [dbt project object](/user-guide/data-engineering/dbt-projects-on-snowflake) or replaces
an existing dbt project object. This command deploys the project files to `versions/live`.

Warning

`CREATE OR REPLACE DBT PROJECT` recreates the object and may remove its run history. To update the
files of an existing dbt project object, use
[`ALTER DBT PROJECT ... DEPLOY`](/sql-reference/sql/alter-dbt-project) instead.

See also:
:   [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project), [DESCRIBE DBT PROJECT](/sql-reference/sql/desc-dbt-project), [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project), [SHOW DBT PROJECTS](/sql-reference/sql/show-dbt-projects), [DROP DBT PROJECT](/sql-reference/sql/drop-dbt-project)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] DBT PROJECT [ IF NOT EXISTS ] <name>
  FROM '<source_location>'
  [ DBT_VERSION = <version_number> ]
  [ DEFAULT_TARGET = <default_target> ]
  [ DEFAULT_ENVIRONMENT = '<environment_name>' ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
  [ AUTO_COMPILE = { TRUE | FALSE } ]
  [ DEFAULT_WRITEBACK = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
```

## Parameters

`name`
:   String that specifies the name of the dbt project object. Must be unique within the schema in which the dbt project object is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`FROM 'source_location'`
:   Required. A string that specifies the location of the dbt project source files.

    The source location must point to a directory that contains a single `dbt_project.yml` file at its root. Although
    workspaces support working with repositories that contain multiple dbt projects, you must select a specific project
    directory when deploying a dbt project object.

    The dbt project object source files can be in any one of the following locations:

    > - **An internal named stage**, for example:
    >
    >   `'@my_db.my_schema.my_internal_named_stage/path/to/dbt_projects_or_projects_parent'`
    >
    >   Internal user stages and table stages aren’t supported.
    > - **A dbt workspace**, for example:
    >
    >   `'snow://workspace/user$.public."my_workspace_name"/versions/live'`
    >
    >   Workspace URIs use `versions/live`, which refers to the active working state of the workspace. We recommend enclosing the workspace name in double quotes because workspace names are case-sensitive and can contain special characters.
    > - **An existing dbt project stage**, for example:
    >
    >   `'snow://dbt/my_db.my_schema.my_existing_dbt_project_object/versions/live'`
    >
    >   The version specifier is required and is `live`.
    > - **A Git repository stage**, for example:
    >
    >   `'@my_db.my_schema.my_git_repository_stage/branches/my_branch/path/to/dbt_project_or_projects_parent'`
    >
    >   For more information about creating and managing a Git repository object and stage, see [Using a Git repository in Snowflake](/developer-guide/git/git-overview) and [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository).

`COMMENT = 'string_literal'`
:   Specifies a comment for the dbt project object.

    Default: No value

`DBT_VERSION = version_number`
:   Specifies a version for the dbt project object.

    If no value is specified, the system defaults to the version set by the [DEFAULT\_DBT\_VERSION](/sql-reference/parameters#label-default-dbt-version) account parameter. For more information, see [Set the account-level default version](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions#label-dbt-projects-set-account-level-default).

`AUTO_COMPILE = { TRUE | FALSE }`
:   Specifies whether Snowflake compiles the dbt project after deploying the source files:

    - `TRUE`: Runs `dbt compile` during deployment. If an external access integration is configured,
      Snowflake first runs `dbt deps`, then `dbt compile`. Stores the compile artifacts in the live
      version.
    - `FALSE`: Skips both commands. You can run either command later with
      [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project).

    Default: `TRUE`

`DEFAULT_WRITEBACK = { TRUE | FALSE }`
:   Specifies whether subsequent executions write generated target and log files back to the live
    version by default. You can override this value for an individual execution with the `WRITEBACK`
    parameter of [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project).

    Regardless of this setting, Snowflake separately stores per-query result artifacts and an archive
    for each execution.

    Default: `TRUE`

`DEFAULT_TARGET = default_target`
:   Specifies the profile used for compilation and subsequent executions (for example, `prod`) of the dbt project object. You can override this parameter by using the [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project)
    command with `ARGS = '--target <other_target>'`.

    Default: No value

`DEFAULT_ENVIRONMENT = 'environment_name'`
:   Specifies the default environment used for compilation and subsequent executions of the dbt project
    object. The value identifies an environment defined in the project’s `env.yml` file. If this
    attribute isn’t set, Snowflake uses `default_environment:` from `env.yml`. You can override this per
    run with the `ENVIRONMENT` argument on the [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project) command. Use
    the reserved name `NO_ENV` to run without any environment by default.

    Default: No value

    For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

`EXTERNAL_ACCESS_INTEGRATIONS = ( integration_name [ , ... ] )`
:   Specifies the external access integration used to grant permissions to pull remote dependencies from dbt package hub or GitHub. When declared on an object, `dbt deps` runs automatically during deployment.

    This setting is used when you deploy (create) the dbt project object. If a command needs external access during execution, you can also specify `EXTERNAL_ACCESS_INTEGRATIONS` on the [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project) command.

    For more information, see [Understand dependencies for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dependencies).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| CREATE DBT PROJECT | Schema |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Note

`CREATE DBT PROJECT` creates a dbt project object in a named database and schema (for example, `mydb.my_schema.my_project`). You can use a workspace as the source in the `FROM` clause, but the object name must always be a fully qualified path in a regular named database and schema. If you try use a workspace path (such as `USER$.PUBLIC.my_workspace`) as the object name, the command will fail.

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

- [Create a dbt project object from a Git repository stage in Snowflake](#label-create-dbt-project-from-git-example)
- [Create a dbt project object from a subdirectory within a Git repository stage in Snowflake](#label-create-dbt-project-from-git-subdirectory-example)
- [Create a dbt project object from the live version of an existing dbt project object](#label-create-dbt-project-from-live-version-example)
- [Create a dbt project object from a workspace that contains multiple dbt projects](#label-create-dbt-project-from-workspace-example)

### Create a dbt project object from a Git repository stage in Snowflake

Create a dbt project object named `sales_dbt_model` from dbt project files in a Git repository stage. This example references the `main`
branch of a Git repository stage named `sales_dbt_git_stage` in Snowflake, where the project’s `dbt_project.yml` file is saved in the
repository root. The command also sets the default target used when executing dbt commands and specifies the external access integrations required
by the project.

Copy code

```
CREATE DBT PROJECT sales_db.dbt_projects_schema.sales_model
  FROM '@sales_db.integrations_schema.sales_dbt_git_stage/branches/main'
  DEFAULT_TARGET = 'prod'
  EXTERNAL_ACCESS_INTEGRATIONS = 'my_external_access_integration'
  COMMENT = 'Generates sales data models.';
```

### Create a dbt project object from a subdirectory within a Git repository stage in Snowflake

Create a dbt project object named `sw_region_sales_model` from a subdirectory inside a Git repository stage that contains multiple dbt projects.
The example references the `main` branch of a Git repository stage named `sales_dbt_git_stage` in Snowflake, where the project’s
`dbt_project.yml` file is saved in the `sw_region_dbt_project` subdirectory of the `sales_dbt_projects_parent` directory.

This example also sets the following properties:

- dbt version
- Default execution target (for example, `prod` or `dev`) used by dbt commands executed through Snowflake.
- External access integrations the dbt project object is permitted to use to pull remote dependencies from dbt package hub or Github.

Copy code

```
CREATE DBT PROJECT sales_db.dbt_projects_schema.sw_region_sales_model
  FROM '@sales_db.integrations_schema.sales_dbt_git_stage/branches/main/sales_dbt_projects_parent/sw_region_dbt_project'
  DBT_VERSION = '1.11.11'
  DEFAULT_TARGET = 'prod'
  EXTERNAL_ACCESS_INTEGRATIONS = 'my_external_access_integration'
  COMMENT = 'Generates data models for SW sales region.';
```

### Create a dbt project object from the live version of an existing dbt project object

Create a new dbt project object named `sales_model_nw_region` from the live version of the existing
`sales_model` dbt project object.

This example also sets a default execution target using DEFAULT\_TARGET, and specifies allowed external access integrations using EXTERNAL\_ACCESS\_INTEGRATIONS.

Copy code

```
CREATE DBT PROJECT sales_db.dbt_projects_schema.sales_model_nw_region
  FROM 'snow://dbt/sales_db.dbt_projects_schema.sales_model/versions/live'
  DEFAULT_TARGET = 'prod'
  EXTERNAL_ACCESS_INTEGRATIONS = (my_ext_integration_1, my_ext_integration_2)
  COMMENT = 'Generates data models for the NW sales region.';
```

### Create a dbt project object from a workspace that contains multiple dbt projects

Create a new dbt project object named `sales_model_from_workspace` from the live version of a workspace containing multiple dbt project directories. “My dbt
Project Workspace” inside the user’s personal database. This is useful when the workspace has several subprojects and you want to create a dbt project object
from a specific subdirectory. Workspaces are case-sensitive and can include special characters, so we recommend enclosing the workspace name in double quotes.

Copy code

```
CREATE DBT PROJECT sales_db.dbt_projects_schema.sales_model_from_workspace
  FROM 'snow://workspace/user$.public."My dbt Project Workspace"/versions/live/project2'

EXECUTE DBT PROJECT sales_db.dbt_projects_schema.sales_model_from_workspace
  ARGS = 'run --target prod';
```
