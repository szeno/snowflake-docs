# DESCRIBE DBT PROJECT

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

Describes the properties of a [dbt project object](/user-guide/data-engineering/dbt-projects-on-snowflake).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE DBT PROJECT](/sql-reference/sql/create-dbt-project), [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project), [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project), [DROP DBT PROJECT](/sql-reference/sql/drop-dbt-project), [SHOW DBT PROJECTS](/sql-reference/sql/show-dbt-projects)

## Syntax

Copy code

```
{ DESC | DESCRIBE } DBT PROJECT <name>
```

## Parameters

`name`
:   Specifies the identifier for the dbt project object to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `name` | The identifier (name) of the dbt project object. |
| `owner` | The role that was used to create the dbt project object. |
| `comment` | The comment associated with the dbt project object. |
| `dbt_version` | The version for the dbt project object. If no value is specified, the system uses version 1.9.4 by default. For more information on supported versions, see [Supported dbt versions for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions). |
| `dbt_snowflake_version` | The Snowflake version the dbt project object is on. |
| `default_target` | The default execution target (for example, `prod` or `dev`) used by dbt commands executed through Snowflake. |
| `external_access_integrations` | The name of the external access integrations the dbt project object is permitted to use to pull remote dependencies from dbt package hub or GitHub. |
| `default_writeback` | Whether executions write generated target and log files back to the live version by default. |
| `auto_compile` | Whether Snowflake compiles the project after deployment. |
| `last_deployed_from` | An OBJECT that describes the source of the most recent deployment. Depending on the source, it can contain `git_url` or `stage_url`, `git_commit`, `git_branch`, `user`, and `timestamp` fields. Returns `NULL` when no deployment metadata was recorded. |

Expand

Show lessSee more

The version-related columns have the following values:

| Column | Description |
| --- | --- |
| `default_version` | Returns `LIVE`, the single mutable version of the dbt project object. |
| `default_version_name` | Deprecated column. Returns `NULL` because dbt project objects don’t have numbered versions. |
| `default_version_alias` | Deprecated column. Returns `NULL` because dbt project objects don’t have version aliases. |
| `default_version_location_uri` | The location URI of the live version, which uses the path `.../versions/live/`. |
| `default_version_source_location_uri` | The location URI of the live version’s source files in its Git object. If the dbt project object is not connected to a Git object, this is null. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| MONITOR | dbt project |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

The following example describes the dbt project object named `my_dbt_project`:

Copy code

```
DESCRIBE DBT PROJECT my_dbt_project;
```

The following output shows the live-version and deployment columns:

```
| name           | default_version | default_version_location_uri                             | default_writeback | auto_compile | last_deployed_from                                                                                                                   |
|----------------|-----------------|----------------------------------------------------------|-------------------|--------------|--------------------------------------------------------------------------------------------------------------------------------------|
| my_dbt_project | LIVE            | snow://dbt/MY_DB.MY_SCHEMA.my_dbt_project/versions/live/ | true              | true         | {"git_url":"https://github.com/example/my_dbt_project","git_commit":"abc123","git_branch":"main","user":"DBT_CI","timestamp":"..."}     |
```
