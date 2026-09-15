# SHOW INTERACTIVE TABLES

Feature — Generally Available

This feature is generally available in select Amazon Web Services (AWS), Google Cloud
Platform (GCP), and Microsoft Azure regions only. For details, see
[Region availability](/user-guide/interactive-cloud-availability#label-interactive-region-availability).

Lists the [interactive tables](/user-guide/interactive) for which you have access privileges. The command can be used to list interactive
tables for the current/specified database or schema, or across your entire account.

See also:
:   [CREATE INTERACTIVE TABLE](/sql-reference/sql/create-interactive-table), [ALTER TABLE](/sql-reference/sql/alter-table), [DROP TABLE](/sql-reference/sql/drop-table),
    [SHOW TABLES](/sql-reference/sql/show-tables), [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables)

## Syntax

Copy code

```
SHOW INTERACTIVE TABLES [ LIKE '<pattern>' ]
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
| SELECT | The interactive tables that you want to list. | A role with only USAGE on the parent database and schema can run the command but sees 0 rows. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- For dynamic interactive tables (created with `TARGET_LAG` and `WAREHOUSE`), the `target_lag`, `refresh_warehouse`,
  `scheduling_state`, `last_completed_refresh_state`, and `latest_data_timestamp` columns return non-NULL values. For
  static interactive tables (created with `AS SELECT` without `TARGET_LAG`), those columns return NULL.
- Regular dynamic tables created with `CREATE DYNAMIC TABLE` don’t appear in the output. Use
  [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables) to list those.
- To suspend or resume automatic refreshes on a dynamic interactive table, use `ALTER INTERACTIVE TABLE ... SUSPEND` or
  `ALTER INTERACTIVE TABLE ... RESUME`. These operations update the `scheduling_state` column to `SUSPENDED` or `ACTIVE`
  respectively. To trigger an on-demand refresh, use `ALTER INTERACTIVE TABLE ... REFRESH`. These operations aren’t
  supported for static interactive tables.

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
| `created_on` | Date and time when the interactive table was created. |
| `name` | Name of the interactive table. |
| `database_name` | Database in which the interactive table is stored. |
| `schema_name` | Schema in which the interactive table is stored. |
| `cluster_by` | The clustering key expression for the interactive table (for example, `(id)`). |
| `rows` | Number of rows in the table. |
| `bytes` | Number of bytes that will be scanned if the entire interactive table is scanned in a query.     Note that this number may be different than the number of actual physical bytes stored on-disk for the table. |
| `owner` | Role that owns the interactive table. |
| `target_lag` | The maximum duration that a dynamic interactive table’s content should lag behind real time. NULL for static interactive tables. |
| `refresh_warehouse` | Warehouse used to perform refreshes for a dynamic interactive table. NULL for static interactive tables. |
| `comment` | Comment for the interactive table. |
| `text` | The text of the command that created the interactive table. For dynamic interactive tables, the stored DDL uses `DYNAMIC TABLE` syntax internally; use `GET_DDL('table', '<name>')` to retrieve the authoritative `CREATE OR REPLACE INTERACTIVE TABLE` statement. NULL for static interactive tables. |
| `scheduling_state` | Displays ACTIVE for dynamic interactive tables that are actively scheduling refreshes and SUSPENDED for suspended tables. NULL for static interactive tables. |
| `owner_role_type` | The type of role that owns the object, for example `ROLE`. If a Snowflake Native App owns the object, the value is `APPLICATION`. Snowflake returns NULL if the object has been deleted. |
| `initialization_warehouse` | Warehouse used for the initial population of a dynamic interactive table. Returns an empty string after initial population is complete. NULL for static interactive tables. |
| `last_completed_refresh_state` | Result of the most recently completed refresh cycle for a dynamic interactive table (for example, `SUCCEEDED`). NULL for static interactive tables. |
| `latest_data_timestamp` | Timestamp of the most recently incorporated data for a dynamic interactive table. NULL for static interactive tables. |

Expand

Show lessSee more

## Examples

Show all the interactive tables with names that start with `product_` in the `mydb.myschema` schema:

> Copy code
>
> ```
> SHOW INTERACTIVE TABLES LIKE 'product_%' IN SCHEMA mydb.myschema;
> ```

Show all interactive tables in the current schema:

> Copy code
>
> ```
> SHOW INTERACTIVE TABLES;
> ```
