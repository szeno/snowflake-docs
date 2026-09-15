# ALTER DBT PROJECT

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

Modifies the properties of an existing [dbt project object](/user-guide/data-engineering/dbt-projects-on-snowflake).

See also:
:   [CREATE DBT PROJECT](/sql-reference/sql/create-dbt-project), [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project), [DESCRIBE DBT PROJECT](/sql-reference/sql/desc-dbt-project), [DROP DBT PROJECT](/sql-reference/sql/drop-dbt-project), [SHOW DBT PROJECTS](/sql-reference/sql/show-dbt-projects)

## Syntax

Copy code

```
ALTER DBT PROJECT [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER DBT PROJECT <name> DEPLOY FROM '<source_location>'

ALTER DBT PROJECT [ IF EXISTS ] <name> SET
  [ DBT_VERSION = '<version_number>' ]
  [ DEFAULT_TARGET = '<default_target>' ]
  [ DEFAULT_ENVIRONMENT = '<environment_name>' ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [, ... ] ) ]
  [ AUTO_COMPILE = { TRUE | FALSE } ]
  [ DEFAULT_WRITEBACK = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]

ALTER DBT PROJECT [ IF EXISTS ] <name> UNSET
  [ DBT_VERSION ]
  [ DEFAULT_TARGET ]
  [ DEFAULT_ENVIRONMENT ]
  [ EXTERNAL_ACCESS_INTEGRATIONS ]
  [ AUTO_COMPILE ]
  [ DEFAULT_WRITEBACK ]
  [ COMMENT ]
```

## Parameters

`name`
:   Specifies the identifier for the dbt project object to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Changes the name of the dbt project object to `new_name`. The new identifier must be unique for the schema.

    For more information about identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object is renamed, other objects that reference it must be updated with the new name.

`DEPLOY FROM 'source_location'`
:   Deploys source files to the mutable `live` version of the dbt project object. The deployment
    replaces the contents of the live version in a single operation, including existing target artifacts.

    The source location must point to a directory that contains a single `dbt_project.yml` file at its
    root. The source files can be in any of the following locations:

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

`SET ...`
:   Sets one or more specified properties or parameters for the dbt project object:

    `DBT_VERSION = 'version_number'`
    :   Specifies a version for the dbt project object.

        If no value is specified, the system defaults to the version set by the [DEFAULT\_DBT\_VERSION](/sql-reference/parameters#label-default-dbt-version) account parameter. For more information, see [Set the account-level default version](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions#label-dbt-projects-set-account-level-default).

    `AUTO_COMPILE = { TRUE | FALSE }`
    :   Specifies whether Snowflake compiles the dbt project after each deployment:

        - `TRUE`: Runs `dbt compile` during deployment. If an external access integration is configured,
          Snowflake first runs `dbt deps`, then `dbt compile`. Stores the compile artifacts in the live
          version.
        - `FALSE`: Skips both commands. You can run either command later with
          [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project).

    `DEFAULT_WRITEBACK = { TRUE | FALSE }`
    :   Specifies whether subsequent executions write generated target and log files back to the live
        version by default. You can override this value for an individual execution with the `WRITEBACK`
        parameter of [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project).

        Regardless of this setting, Snowflake separately stores per-query result artifacts and an archive
        for each execution.

    `DEFAULT_TARGET = default_target`
    :   Specifies the profile used for compilation and subsequent executions (for example, `prod`) of the dbt project object. This parameter can be overridden by using the [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project)
        command with `ARGS = '--target <other_target>'`.

    `DEFAULT_ENVIRONMENT = 'environment_name'`
    :   Sets or changes the default environment used for compilation and subsequent executions of the dbt
        project object. The value identifies an environment defined in the project’s `env.yml` file. If
        this attribute isn’t set, Snowflake uses `default_environment:` from `env.yml`. You can override
        this per run with the `ENVIRONMENT` argument on the [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project)
        command. Use the reserved name `NO_ENV` to run without any environment by default.

        For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

    `EXTERNAL_ACCESS_INTEGRATIONS = ( integration_name [ , ... ] )`
    :   Specifies the external access integrations used to grant permissions to pull remote dependencies from dbt package hub or GitHub. When declared on an object, `dbt deps` will run automatically during deployment.
        For more information, see [Understand dependencies for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dependencies).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the dbt project object.

`UNSET ...`
:   Unsets one or more specified properties or parameters for the dbt project object to NULL or no value:

    - `DBT_VERSION`
    - `DEFAULT_TARGET`
    - `DEFAULT_ENVIRONMENT`
    - `EXTERNAL_ACCESS_INTEGRATIONS`
    - `AUTO_COMPILE`
    - `DEFAULT_WRITEBACK`
    - `COMMENT`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | dbt project | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Usage notes

- `ALTER DBT PROJECT` operates on a deployed dbt project object in a named database/schema. It doesn’t operate on a workspace. If you receive a `SQL compilation error: DBT PROJECT 'USER$...' does not exist or not authorized` error, there are two common causes: you’re targeting a workspace path instead of a deployed project object, or the active role doesn’t have the OWNERSHIP privilege on the object. Use SHOW DBT PROJECTS to confirm the correct fully qualified name (for example, `mydb.my_schema.my_project`) and verify that your role has the required privileges before retrying the `ALTER` command.
- Use `DEPLOY FROM '<source_location>'` to update a dbt project object. Deployment replaces the live
  project contents in a single operation.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

### Set a dbt version

The following example sets a new dbt version to a dbt project object:

Copy code

```
ALTER DBT PROJECT finance_analytics SET dbt_version = '1.11.11';
```

### Deploy an update to the live version

The following example updates a Git repository object in Snowflake to fetch the latest code from the Git repository and then updates the
live contents of the dbt project object:

Copy code

```
-- Update the Git repository object to fetch the latest code

ALTER GIT REPOSITORY sales_db.integrations_schema.sales_dbt_git_stage FETCH;

-- Deploy the updated Git repository object to the live version

ALTER DBT PROJECT sales_db.dbt_projects_schema.sales_model
  DEPLOY FROM '@sales_db.integrations_schema.sales_dbt_git_stage/branches/main/sales_dbt_project';
```

### Set a default target and new external access integration

The following example updates an existing dbt project object with the following changes:

- Sets a default target that Snowflake uses when executing EXECUTE DBT PROJECT without specifying a `--target` argument. For example, if
  `DEFAULT_TARGET = 'prod'`, then a command such as `EXECUTE DBT PROJECT sales_db.dbt_projects_schema.sales_model ARGS = 'run';` would
  automatically execute using `--target prod` unless overridden by `ARGS = '--target <other_target>'`.
- Assigns an external access integration for the dbt project object to use.

  You can provide a single integration or a list: `EXTERNAL_ACCESS_INTEGRATIONS = ('integration1', 'integration2')`.

Copy code

```
ALTER DBT PROJECT sales_db.dbt_projects_schema.sales_model SET
  DEFAULT_TARGET = 'prod',
  EXTERNAL_ACCESS_INTEGRATIONS = ('my_external_access_integration');
```

### Revert to the system default version

The following example reverts the dbt project object to the system default version, which is currently 1.9.4. Account administrators can change the default for all future dbt project objects in the account using the [DEFAULT\_DBT\_VERSION](/sql-reference/parameters#label-default-dbt-version) account parameter.

For more information, see [Set the account-level default version](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions#label-dbt-projects-set-account-level-default).

Copy code

```
ALTER DBT PROJECT finance_analytics UNSET DBT_VERSION;
```

```
Statement executed successfully.
```
