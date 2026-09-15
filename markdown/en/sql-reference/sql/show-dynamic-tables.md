# SHOW DYNAMIC TABLES

Lists the [dynamic tables](/user-guide/dynamic-tables/overview) for which you have access privileges. The command can be used to list dynamic
tables for the current/specified database or schema, or across your entire account.

See also:
:   [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table), [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table), [DESCRIBE DYNAMIC TABLE](/sql-reference/sql/desc-dynamic-table), [DROP DYNAMIC TABLE](/sql-reference/sql/drop-dynamic-table),
    [SHOW OBJECTS](/sql-reference/sql/show-objects), [TABLES view](/sql-reference/info-schema/tables) (Information Schema)

Note

Frozen regions were previously named immutability constraints, and the `FROZEN WHERE` clause previously used the syntax `IMMUTABLE WHERE`. The legacy `IMMUTABLE WHERE` syntax continues to be supported, and `SHOW DYNAMIC TABLES` still uses the `immutable_where` column.

## Syntax

Copy code

```
SHOW DYNAMIC TABLES [ LIKE '<pattern>' ]
                    [ IN
                      {
                           ACCOUNT              |

                           DATABASE             |
                           DATABASE <db_name>   |

                           SCHEMA               |
                           SCHEMA <schema_name> |
                           <schema_name>
                      }
                    ]
                    [ STARTS WITH '<name_string>' ]
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

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| SELECT | The dynamic tables that you want to list. | Some metadata is hidden if you don’t have the MONITOR privilege. For more information, see [Grant MONITOR to view metadata](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges-view-metadata). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To SHOW a dynamic table, you must be using a role that has MONITOR privilege on the table.

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

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

## Output

The command output provides table properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the dynamic table was created. |
| `name` | Name of the dynamic table. |
| `database_name` | Database in which the dynamic table is stored. |
| `schema_name` | Schema in which the dynamic table is stored. |
| `cluster_by` | The clustering key(s) for the dynamic table. |
| `rows` | Number of rows in the table. |
| `bytes` | Number of bytes that will be scanned if the entire dynamic table is scanned in a query.     Note that this number may be different than the number of actual physical bytes (i.e. bytes stored on-disk) for the table. |
| `owner` | Role that owns the dynamic table. |
| `target_lag` | The maximum duration that the dynamic table’s content should lag behind real time. `NULL` if `scheduler` is set to `DISABLE`. |
| `scheduler` | Specifies whether the dynamic table is to be refreshed automatically by Snowflake. `ENABLE` if the dynamic table is scheduled automatically. `DISABLE` if the dynamic table isn’t scheduled automatically. `NULL` if the `SCHEDULER` attribute wasn’t explicitly set (the dynamic table is scheduler-managed by default). |
| `refresh_mode` | Returns `INCREMENTAL` if the dynamic table uses incremental refreshes, `FULL` if Snowflake refreshes the entire table on every refresh, `AUTO` if Snowflake selected the refresh mode automatically, `ADAPTIVE` if the dynamic table uses incremental refresh with automatic reinitialization on large upstream changes, or `CUSTOM_INCREMENTAL` if the dynamic table uses a user-defined MERGE or INSERT statement for refresh logic. |
| `refresh_mode_reason` | Explanation for why the refresh mode was chosen. If Snowflake chose `FULL` when `INCREMENTAL` is supported, the output provides a reason for why it thinks full refresh performs better. NULL if no pertinent information is available. |
| `warehouse` | Warehouse that provides the required resources to perform the incremental refreshes. |
| `comment` | Comment for the dynamic table. |
| `text` | The text of the command that created this dynamic table (e.g. `CREATE DYNAMIC TABLE ...`). |
| `automatic_clustering` | Whether auto-clustering is enabled on the dynamic table. Not currently supported for dynamic tables. |
| `scheduling_state` | Displays RUNNING for dynamic tables that are actively scheduling refreshes and SUSPENDED for suspended dynamic tables. |
| `last_suspended_on` | Timestamp of last suspension. |
| `is_clone` | TRUE if the dynamic table is a clone; else FALSE. |
| `is_replica` | TRUE if the dynamic table is a replica; else FALSE. |
| `is_iceberg` | TRUE if the dynamic table is a dynamic Apache Iceberg™ table; else FALSE. |
| `data_timestamp` | Timestamp of the data in the base object(s) that is included in the dynamic table. |
| `owner_role_type` | The type of role that owns the object, for example `ROLE`.     Database-level roles, for example `DATABASE_ROLE`, can’t be owners. The owner of a dynamic table must have the USAGE privilege on the warehouse. Since the warehouse is an account-level object, a database role, which operates at the database level, can’t be granted access to it.     If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| `immutable_where` | Displays the [frozen region](/user-guide/dynamic-tables/frozen-regions) predicate set on the dynamic table. Displays NULL if there is none. |
| `execute_as_user` | Displays the user name of a user refreshing a dynamic table using impersonated privileges (EXECUTE AS USER). NULL if executed as the system user (default). INVALID if the specified user ID is no longer valid (for example, user dropped). For more information, see [Refresh with specific user privileges (EXECUTE AS USER)](/user-guide/dynamic-tables/privileges#label-dts-execute-as-user). |

Expand

Show lessSee more

## Examples

Show all the dynamic tables with names that start with `product_` in the `mydb.myschema` schema:

> Copy code
>
> ```
> SHOW DYNAMIC TABLES LIKE 'product_%' IN SCHEMA mydb.myschema;
> ```
