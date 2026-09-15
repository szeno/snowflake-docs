# SHOW INDEXES

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

Lists all the indexes in your account for which you have access privileges.

See also:
:   [CREATE HYBRID TABLE](/sql-reference/sql/create-hybrid-table) , [CREATE INDEX](/sql-reference/sql/create-index) , [DROP INDEX](/sql-reference/sql/drop-index) , [DROP TABLE](/sql-reference/sql/drop-table) , [DESCRIBE TABLE](/sql-reference/sql/desc-table) , [SHOW HYBRID TABLES](/sql-reference/sql/show-hybrid-tables)

## Syntax

Copy code

```
SHOW [ TERSE ] INDEXES
  [ LIKE '<pattern>' ]
  [ IN { ACCOUNT | DATABASE [ <database_name> ] | SCHEMA [ <schema_name> ] | TABLE | TABLE <table_name> } ]
  [ STARTS WITH '<name_string>' ]
  [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`TERSE`
:   Returns only a subset of the output columns:

    - `created_on`
    - `name`
    - `kind`
    - `database_name`
    - `schema_name`

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN { ACCOUNT | DATABASE [ database_name ] | SCHEMA [ schema_name ] | TABLE | TABLE table_name }`
:   Filters the output by the specified database, schema, table, or account.

    If you specify the keyword `ACCOUNT`, then the command retrieves records for all schemas in all databases
    of the current account.

    If you specify the keyword `DATABASE`, then:

    - If you specify a `db_name`, then the command retrieves records for all schemas of the specified database.
    - If you don’t specify a `db_name`, then:
      - If there is a current database, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and schemas in the account.

    If you specify the keyword `SCHEMA`, then:

    - If you specify a qualified schema name (for example, `my_database.my_schema`), then the command
      retrieves records for the specified database and schema.
    - If you specify an unqualified `schema_name`, then:

      - If there is a current database, then the command retrieves records for the specified schema in the current database.
      - If there is no current database, then the command displays the error
        `SQL compilation error: Object does not exist, or operation cannot be performed`.
    - If you don’t specify a `schema_name`, then:

      - If there is a current database, then:

        - If there is a current schema, then the command retrieves records for the current schema in the current database.
        - If there is no current schema, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and all schemas in the account.

    If you specify the keyword `TABLE` without a `table_name`, then:

    - If there is a current database, then:

      - If there is a current schema, then the command retrieves records for the current schema in the current database.
      - If there is no current schema, then the command retrieves records for all schemas in the current database.
    - If there is no current database, then the command retrieves records for all databases and all schemas in the account.

    If you specify a `table_name` (with or without the keyword `TABLE`), then:

    - If you specify a fully-qualified `table_name` (e.g. `my_database_name.my_schema_name.my_table_name`),
      then the command retrieves all records for the specified table.
    - If you specify a schema-qualified `table_name` (e.g. `my_schema_name.my_table_name`), then:

      - If a current database exists, then the command retrieves all records for the specified table.
      - If no current database exists, then the command displays an error similar to
        `Cannot perform SHOW object_type. This session does not have a current database...`.
    - If you specify an unqualified `table_name`, then:

      - If a current database and current schema exist, then the command retrieves records for the specified table in the current
        schema of the current database.
      - If no current database exists or no current schema exists, then the command displays an error similar to:
        `SQL compilation error: object does not exist or not authorized.`.

    Default: Depends on whether the session currently has a database in use:

    - Database: `DATABASE` is the default (i.e. the command returns the objects you have privileges to view in the database).
    - No database: `ACCOUNT` is the default (i.e. the command returns the objects you have privileges to view in your account).

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

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the index was created. |
| `name` | Name of the index. |
| `is_unique` | Whether the index is a unique index. |
| `columns` | List of indexed columns. |
| `included_columns` | List of covered columns. |
| `table` | Name of the table. |
| `database_name` | Database in which the index is stored. |
| `schema_name` | Schema in which the index is stored. |
| `owner` | Role that owns the index. |
| `owner_role_type` | Role type of the owner. |
| `status` | Build status of the index. For the possible values, see [CREATE INDEX](/sql-reference/sql/create-index). |
| `status_info` | More detail about the build status, such as the reason a build failed validation. |

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

## Examples

These SHOW INDEX examples use the current database and schema.

Return a terse list of indexes that contain the string `DEVICE` in their names:

Copy code

```
SHOW TERSE INDEXES LIKE '%DEVICE%';
```

```
+-------------------------------+---------------------------------------+-----------------+---------------+-------------+
| created_on                    | name                                  | kind            | database_name | schema_name |
|-------------------------------+---------------------------------------+-----------------+---------------+-------------|
| 2024-08-29 12:24:49.197 -0700 | SYS_INDEX_SENSOR_DATA_DEVICE1_PRIMARY | KEY_VALUE_INDEX | HT_SENSORS    | HT_SCHEMA   |
| 2024-08-29 12:24:49.197 -0700 | DEVICE_IDX                            | KEY_VALUE_INDEX | HT_SENSORS    | HT_SCHEMA   |
| 2024-08-29 14:03:36.537 -0700 | SYS_INDEX_SENSOR_DATA_DEVICE2_PRIMARY | KEY_VALUE_INDEX | HT_SENSORS    | HT_SCHEMA   |
| 2024-08-29 14:03:36.537 -0700 | DEVICE_IDX                            | KEY_VALUE_INDEX | HT_SENSORS    | HT_SCHEMA   |
+-------------------------------+---------------------------------------+-----------------+---------------+-------------+
```

Only return indexes that have covered columns (`included_columns`). Use the [pipe operator](/sql-reference/operators-flow)
(`->>`) to select specific rows and columns from the full output of the SHOW INDEXES command.

Copy code

```
SHOW INDEXES
  ->> SELECT "name",
             "is_unique",
             "table",
             "columns",
             "included_columns",
             "database_name",
             "schema_name"
        FROM $1
        WHERE "included_columns" != '[]';
```

The following output shows the SELECT query result only. One index qualifies for the WHERE clause condition:

```
+------------+-----------+---------------------+-------------+------------------+---------------+-------------+
| name       | is_unique | table               | columns     | included_columns | database_name | schema_name |
|------------+-----------+---------------------+-------------+------------------+---------------+-------------|
| DEVICE_IDX | N         | SENSOR_DATA_DEVICE2 | [DEVICE_ID] | [TEMPERATURE]    | HT_SENSORS    | HT_SCHEMA   |
+------------+-----------+---------------------+-------------+------------------+---------------+-------------+
```
