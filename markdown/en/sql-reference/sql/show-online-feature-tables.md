# SHOW ONLINE FEATURE TABLES

Lists the [online feature tables](/sql-reference/sql/create-online-feature-table) for which you have access privileges.

You can use this command to list objects in the current database and schema for the session, a specified database or schema, or
your entire account.

The output includes the metadata and properties for each object. The objects are sorted lexicographically by database, schema,
and object name (see Output in this topic for descriptions of the output columns). The order of rows in the results is important
to note if you want to filter the results.

See also:
:   [CREATE ONLINE FEATURE TABLE](/sql-reference/sql/create-online-feature-table) , [ALTER ONLINE FEATURE TABLE](/sql-reference/sql/alter-online-feature-table), [DESCRIBE ONLINE FEATURE TABLE](/sql-reference/sql/desc-online-feature-table) , [DROP ONLINE FEATURE TABLE](/sql-reference/sql/drop-online-feature-table)

## Syntax

Copy code

```
SHOW ONLINE FEATURE TABLES [ LIKE '<pattern>' ]
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

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `created_on` | Creation time of the online feature table. |
| `name` | Name of the online feature table. |
| `database_name` | The database in which the online feature table resides. |
| `schema_name` | The schema in which the online feature table resides. |
| `rows` | Number of rows in the storage. |
| `bytes` | Number of bytes that will be scanned if the entire online feature table is scanned in a query.  Note that this number may be different than the number of actual physical bytes stored for the table. |
| `owner` | Role that owns the online feature table. |
| `source` | Name of the source of the online feature table data. |
| `target_lag` | The maximum duration that the online feature table’s content should lag behind real time. |
| `warehouse` | The warehouse used for online feature table refreshes. |
| `timestamp_column` | The timestamp column specified when the online feature table was created. |
| `refresh_mode` | `INCREMENTAL` if the table refreshes the data from source incrementally, or `FULL` if it ingests the full data source on every refresh. |
| `refresh_mode_reason` | Explanation for why the refresh mode was chosen. If Snowflake chose `FULL` when `INCREMENTAL` is supported, the output provides a reason for why it thinks full refresh performs better. `NULL` if no pertinent information is available. |
| `scheduling_state` | Displays `RUNNING` for online feature tables that are actively scheduling refreshes and `SUSPENDED` for suspended online feature tables. |
| `comment` | Comment for the online feature table. |

Expand

Show lessSee more

Note

Numbers in the `rows` and `bytes` columns might not be accurate if data is changing frequently. You can run a `SELECT COUNT(*)` query on the table to get an accurate row count.

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Schema | Role that has the USAGE privilege on the schema. |

Expand

Show lessSee more

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

- Executing the command for schema-level objects only returns an object if the current role also has at least one privilege on the
  parent database and schema.

## Examples

The following example lists the online feature tables that you have the privileges to view in the PUBLIC schema of the `mydb` database:

Copy code

```
USE DATABASE mydb;

SHOW ONLINE FEATURE TABLES;
```

The following example lists all online feature tables in the current account that start with `feature_`:

Copy code

```
SHOW ONLINE FEATURE TABLES STARTS WITH 'feature_' IN ACCOUNT;
```

The following example lists online feature tables with names that match the pattern `%test%` in the `analytics` schema:

Copy code

```
SHOW ONLINE FEATURE TABLES LIKE '%test%' IN SCHEMA analytics;
```
