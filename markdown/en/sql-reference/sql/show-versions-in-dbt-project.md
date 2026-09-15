# SHOW VERSIONS IN DBT PROJECT

Displays the `live` version of a
[dbt project object](/user-guide/data-engineering/dbt-projects-on-snowflake).

Note

An object that hasn’t been migrated to the mutable `live` version still lists numbered versions. For
details about the live-version model and how to migrate an existing object, see
[dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version (Pending)](/release-notes/bcr-bundles/2026_06/bcr-2362) and
[SYSTEM$MIGRATE\_DBT\_PROJECT](/sql-reference/functions/system_migrate_dbt_project).

See also:
:   [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project), [DESCRIBE DBT PROJECT](/sql-reference/sql/desc-dbt-project), [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project), [SHOW DBT PROJECTS](/sql-reference/sql/show-dbt-projects), [DROP DBT PROJECT](/sql-reference/sql/drop-dbt-project)

## Syntax

Copy code

```
SHOW VERSIONS IN DBT PROJECT <name>
  [ LIMIT <number> ]
```

## Parameters

`name`
:   String that specifies the identifier (that is, the name) for the dbt project object within Snowflake; must be unique for the schema in which
    the dbt project is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| USAGE | The dbt project object |
| MONITOR | The dbt project object |
| OWNERSHIP | The dbt project object |

Expand

Show lessSee more

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

## Output

The command output provides table properties and metadata about a dbt project object in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the dbt project object was created. |
| `name` | Deprecated column. Returns `NULL` because the live version doesn’t have a numbered version name. |
| `alias` | Deprecated column. Returns `NULL` because the live version doesn’t have a version alias. |
| `location_uri` | Full URL of the dbt project version. |
| `is_default` | Deprecated column. Returns `FALSE` for the live version. |
| `is_live` | Returns `TRUE`, indicating that this row represents the live version. |
| `is_first` | Deprecated column. Returns `FALSE` because dbt project objects don’t have ordered numbered versions. |
| `is_last` | Deprecated column. Returns `FALSE` because dbt project objects don’t have ordered numbered versions. |
| `comment` | Comment set on the dbt Project. |
| `source_location_uri` | The source location URI where this dbt project version is created from. |
| `git_commit_hash` | The git commit hash, if the dbt project version was created from a git source. |

Expand

Show lessSee more

## Examples

Show the live version of `my_dbt_project`:

Copy code

```
SHOW VERSIONS IN DBT PROJECT my_dbt_project;
```

```
+----------------------------------+------+-------+----------------------------------------------------------------+------------+---------+----------+---------+---------+---------------------+-----------------+
| created_on                       | name | alias | location_uri                                                   | is_default | is_live | is_first | is_last | comment | source_location_uri | git_commit_hash |
+----------------------------------+------+-------+----------------------------------------------------------------+------------+---------+----------+---------+---------+---------------------+-----------------+
| 2026-08-26 10:46:26.349 -0700    | null | null  | snow://dbt/mydb.my_schema.my_dbt_project/versions/live/        | FALSE      | TRUE    | FALSE    | FALSE   | null    | null                | null            |
+----------------------------------+------+-------+----------------------------------------------------------------+------------+---------+----------+---------+---------+---------------------+-----------------+
```
