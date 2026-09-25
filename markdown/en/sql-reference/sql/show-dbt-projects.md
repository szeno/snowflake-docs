# SHOW DBT PROJECTS

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

Lists the [dbt project objects](/user-guide/data-engineering/dbt-projects-on-snowflake) for which you have access privileges.

You can use this command to list objects in the current database and schema for the session, a specified database or schema, or
your entire account.

The output includes the metadata and properties for each object. The objects are sorted lexicographically by database, schema,
and object name (see Output in this topic for descriptions of the output columns). The order of rows in the results is important
to note if you want to filter the results.

See also:
:   [CREATE DBT PROJECT](/sql-reference/sql/create-dbt-project), [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project), [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project), [DROP DBT PROJECT](/sql-reference/sql/drop-dbt-project), [SHOW DBT PROJECTS](/sql-reference/sql/show-dbt-projects)

## Syntax

Copy code

```
SHOW DBT PROJECTS [ LIKE '<pattern>' ]
           [ IN
                {
                  ACCOUNT                  |

                  DATABASE                 |
                  DATABASE <database_name> |

                  SCHEMA                   |
                  SCHEMA <schema_name>     |
                  <schema_name>
                }
           ]
           [ STARTS WITH '<name_string>' ]
           [ LIMIT <rows> ]
           [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns records for the entire account.

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or for a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

        Note

        Using SHOW commands without an `IN` clause in a database context can result in fewer than expected results.

        Objects with the same name are only displayed once if no `IN` clause is used. For example, if you have table `t1` in
        `schema1` and table `t1` in `schema2`, and they are both in scope of the database context you’ve specified (that is, the database
        you’ve selected is the parent of `schema1` and `schema2`), then SHOW TABLES only displays one of the `t1` tables.

    `SCHEMA`, `SCHEMA schema_name`
    :   Returns records for the current schema in use or a specified schema (`schema_name`).

        `SCHEMA` is optional if a database is in use or if you specify the fully qualified `schema_name` (for example, `db.schema`).

        If no database is in use, specifying `SCHEMA` has no effect on the output.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

`LIMIT rows [ FROM 'name_string' ]`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
    specified number of rows following the first row whose object name matches the specified string:

    - The string must be enclosed in single quotes and is case sensitive.
    - The string does not have to include the full object name; partial names are supported.

    Default: No value (no limit is applied to the output)

    Note

    For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
    both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
    returned.

    In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
    lexicographic value than the rows returned by `STARTS WITH 'name_string'`.

    For example:

    - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
    - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
    - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `name` | The identifier of the dbt project object. |
| `database_name` | The name of the database in which the dbt project object is defined. |
| `schema_name` | The name of the schema in which the dbt project object is defined. |
| `created_on` | Date and time when the dbt project object was created. |
| `updated_on` | Date and time when the dbt project object was last updated. |
| `owner` | The name of the role that owns the dbt project object. |
| `comment` | The comment associated with the dbt project object. |
| `dbt_version` | The version for the dbt project object. If no value is specified, the system uses version 1.9.4 by default. |
| `dbt_snowflake_version` | The Snowflake version the dbt project object is on. |
| `default_target` | The default execution target (for example, `prod` or `dev`) used by dbt commands executed through Snowflake. |
| `default_environment` | The `DEFAULT_ENVIRONMENT` attribute set on the dbt project object. Returns `NULL` if the attribute isn’t set. This column doesn’t show the `default_environment:` value from `env.yml`. Set the attribute with [CREATE DBT PROJECT](/sql-reference/sql/create-dbt-project) or [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project). For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables). |
| `default_writeback` | Whether executions write generated target and log files back to the live version by default. |
| `auto_compile` | Whether Snowflake compiles the project after deployment. |
| `external_access_integrations` | The name of the external access integrations the dbt project object is permitted to use to pull remote dependencies from dbt package hub or GitHub. |
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

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| USAGE | dbt project |
| MONITOR | dbt project |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

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

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

The following example lists the dbt project objects that you have privileges to view in the `public` schema of the `my_db` database:

Copy code

```
SHOW DBT PROJECTS IN DATABASE my_db;
```

The output includes a row for each dbt project object:

```
| name           | database_name | schema_name | created_on                    | updated_on                    | owner        | comment | dbt_version | default_version | default_version_name | default_version_alias | default_version_location_uri                                  | default_version_source_location_uri | dbt_snowflake_version | default_target | default_environment | default_writeback | auto_compile | external_access_integrations | last_deployed_from                                                                                                                |
|----------------|---------------|-------------|-------------------------------|-------------------------------|--------------|---------|-------------|-----------------|----------------------|-----------------------|---------------------------------------------------------------|-------------------------------------|-----------------------|----------------|---------------------|-------------------|--------------|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| COSMOS         | MY_DB         | PUBLIC      | 2026-04-29 17:21:25.413 -0700 | 2026-04-29 17:21:29.462 -0700 | ACCOUNTADMIN | null    | 1.9.4       | LIVE            | null                 | null                  | snow://dbt/MY_DB.PUBLIC.COSMOS/versions/live/                 | @s1                                 | 1.9.2                 | null           | null                | true              | true         | ["MY_EXT_INTEGRATION_1"]     | null                                                                                                                              |
| JAFFLE_SHOP    | MY_DB         | PUBLIC      | 2026-03-25 12:36:16.574 -0700 | 2026-03-25 12:36:17.833 -0700 | ACCOUNTADMIN | null    | 1.11.11     | LIVE            | null                 | null                  | snow://dbt/MY_DB.PUBLIC.JAFFLE_SHOP/versions/live/            | @s1                                 | 1.11.5                | prod           | prod                | true              | true         | ["MY_EXT_INTEGRATION_1"]     | {"git_url":"https://github.com/example/jaffle-shop","git_commit":"abc123","git_branch":"main","user":"DBT_CI","timestamp":"..."}     |
| MY_DBT_PROJECT | MY_DB         | PUBLIC      | 2026-05-02 13:42:36.306 -0700 | 2026-05-02 13:42:38.584 -0700 | ACCOUNTADMIN | null    | 1.10.15     | LIVE            | null                 | null                  | snow://dbt/MY_DB.PUBLIC.MY_DBT_PROJECT/versions/live/         | @s1                                 | 1.10.3                | dev            | null                | false             | false        | ["MY_EXT_INTEGRATION_2"]     | {"stage_url":"@MY_DB.PUBLIC.DBT_PROJECT_STAGE","user":"DBT_CI","timestamp":"..."}                                                   |
| MY_SHOP        | MY_DB         | PUBLIC      | 2026-04-29 17:15:27.295 -0700 | 2026-04-29 17:15:28.709 -0700 | ACCOUNTADMIN | null    | 1.9.4       | LIVE            | null                 | null                  | snow://dbt/MY_DB.PUBLIC.MY_SHOP/versions/live/                | @s1                                 | 1.9.2                 | null           | null                | true              | true         | null                         | null                                                                                                                              |
```
