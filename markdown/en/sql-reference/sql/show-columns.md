# SHOW COLUMNS

Lists the columns in the tables or views and the dimensions, facts, and metrics in the
[semantic views](/user-guide/views-semantic/overview) for which you have access privileges. This command can be used to list
the columns, dimensions, facts, and metrics for the following objects:

- The specified table or view.
- All tables and views in the specified schema or in the schema that is currently in use.
- All tables and views in the specified database or in the database that is currently in use.
- All tables and views in your account.

See also:
:   [DESCRIBE TABLE](/sql-reference/sql/desc-table)

    [COLUMNS view](/sql-reference/info-schema/columns) (Information Schema)

## Syntax

Copy code

```
SHOW COLUMNS [ LIKE '<pattern>' ]
             [ IN { ACCOUNT | DATABASE [ <database_name> ] | SCHEMA [ <schema_name> ] | TABLE | [ TABLE ] <table_name> | VIEW | [ VIEW ] <view_name> } | APPLICATION <application_name> | APPLICATION PACKAGE <application_package_name> ]
```

## Parameters

`LIKE '<pattern>'`
:   Filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL wildcard
    characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

`IN { ACCOUNT | DATABASE [ <database_name> ] | SCHEMA [ <schema_name> ] | TABLE | [ TABLE ] <table_name> | VIEW | [ VIEW ] <view_name> | APPLICATION <application_name> | APPLICATION PACKAGE <application_package_name> }`
:   Specifies the scope of the command, which determines whether the command lists records only for the current/specified database,
    schema, table, or view, or across your entire account:

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

    If you specify the `VIEW` keyword or a view name, the rules for views parallel the rules for tables.

    If you specify the `APPLICATION` or `APPLICATION PACKAGE` keywords, records for the specified Snowflake Native App Framework application or
    application package are returned.

    Default: Depends on whether the session currently has a database in use:

    > - Database: `DATABASE` is the default (i.e. the command returns the objects you have privileges to view in the database).
    > - No database: `ACCOUNT` is the default (i.e. the command returns the objects you have privileges to view in your account).

## Usage notes

- You can use the `VIEW` keyword and specify a view name for standard views, materialized views, and semantic views.

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

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

Note

The column names in the output table for the SHOW COLUMNS command are lowercase (that is,
`table_name`, `schema_name`, `column_name`, and so on). However, the values in
the `column_name` column reflect the column name that is stored. For example, if a column name
is added without being enclosed in double quotes using the `ALTER TABLE ... ADD COLUMN MYCOLUMN`
statement, the column name is stored in uppercase and appears as `MYCOLUMN` in the `column_name`
column.

## Output

The command output provides column properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `table_name` | Name of the table or view that the column, dimension, fact, or metric belongs to. |
| `schema_name` | Schema for the table. |
| `column_name` | Name of the column, dimension, fact, or metric. |
| `data_type` | JSON object containing the data type and applicable properties of the column, dimension, fact, or metric.  The `type` key-value pair specifies the data type of the column, dimension, fact, or metric.  For [string](/sql-reference/data-types-text) and [numeric](/sql-reference/data-types-numeric) data types, `type` specifies one of the following values:   - `TEXT` for all string types. - `FIXED` for all fixed-point numeric types. - `REAL` for all floating-point numeric types.   The other key-value pairs describe the properties that are applicable to the particular data type. For example:   - If `type` is `TEXT` or `BINARY`, the additional key-value pairs can include `length`, `byteLength`,   `nullable`, and `fixed`. - If `type` is `FIXED`, `TIME`, `TIMESTAMP_NTZ`, `TIMESTAMP_LTZ`, or `TIMESTAMP_TZ`, the additional key-value   pairs can include `precision`, `scale`, and `nullable`. - If `type` is `REAL`, `DATE`, or `BOOLEAN`, the additional key-value pairs can include `nullable`. |
| `null?` | Whether the column can contain NULL values. |
| `default` | Default value, if any, defined for the column. |
| `kind` | One of the following values:   - `COLUMN` for columns in tables, views, and materialized views. - `VIRTUAL_COLUMN` for virtual columns defined by an expression. - `DIMENSION` for dimensions in [semantic views](/user-guide/views-semantic/overview). - `FACT` for facts in semantic views. - `METRIC` for metrics in semantic views. |
| `expression` | The SQL expression that defines a virtual column. Empty for non-virtual columns. |
| `comment` | Comment, if any, for the column, dimension, fact, or metric. |
| `database_name` | Database for the table. |
| `autoincrement` | Auto-increment start and increment values, if any, for the column. If the column has the NOORDER property, the value includes `NOORDER` (for example, `IDENTITY START 1 INCREMENT 1 NOORDER`). Otherwise, the value includes `ORDER`. |
| `schema_evolution_record` | Records information about the latest triggered Schema Evolution for a given table column. This column contains the following subfields:   - EvolutionType: The type of the triggered schema evolution (ADD\_COLUMN or DROP\_NOT\_NULL). - EvolutionMode: The triggering ingestion mechanism (COPY, SNOWPIPE, or SNOWPIPE\_STREAMING). - FileName: The file name that triggered the evolution (NULL for SNOWPIPE\_STREAMING). - TriggeringTime: The approximate time when the column was evolved. - QueryId or PipeId: A unique identifier of the triggering query or pipe (QUERY ID for COPY, PIPE ID for SNOWPIPE, or NULL for SNOWPIPE\_STREAMING). - Pipe name: Fully qualified pipe name that triggered schema evolution (SNOWPIPE\_STREAMING only). - Channel name: Channel that triggered schema evolution (SNOWPIPE\_STREAMING only). - offsetTokenUpperBound: An offset at or before which schema evolution was triggered (SNOWPIPE\_STREAMING only). |

Expand

Show lessSee more

## Examples

The following example creates a table and then runs the SHOW COLUMNS command to list the
columns in the table:

Copy code

```
CREATE OR REPLACE TABLE test_show_columns (
  n1 NUMBER DEFAULT 5,
  n2_int INTEGER DEFAULT n1+5,
  n3_bigint BIGINT AUTOINCREMENT,
  n4_dec DECIMAL IDENTITY (1,10),
  f1 FLOAT,
  f2_double DOUBLE,
  f3_real REAL,
  s1 STRING,
  s2_var VARCHAR,
  s3_char CHAR,
  s4_text TEXT,
  "s5_case_sensitive" VARCHAR,
  b1 BINARY,
  b2_var VARBINARY,
  bool1 BOOLEAN,
  d1 DATE,
  t1 TIME,
  ts1 TIMESTAMP,
  ts2_ltz TIMESTAMP_LTZ,
  ts3_ntz TIMESTAMP_NTZ,
  ts4_tz TIMESTAMP_TZ);

SHOW COLUMNS IN TABLE test_show_columns;
```

```
+-------------------+----------------+-------------------+---------------------------------------------------------------------------------------+-------+--------------------------+--------+------------+---------+---------------+---------------------------------------+-------------------------+
| table_name        | schema_name    | column_name       | data_type                                                                             | null? | default                  | kind   | expression | comment | database_name | autoincrement                         | schema_evolution_record |
|-------------------+----------------+-------------------+---------------------------------------------------------------------------------------+-------+--------------------------+--------+------------+---------+---------------+---------------------------------------+-------------------------|
| TEST_SHOW_COLUMNS | MY_SCHEMA      | N1                | {"type":"FIXED","precision":38,"scale":0,"nullable":true}                             | true  | 5                        | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | N2_INT            | {"type":"FIXED","precision":38,"scale":0,"nullable":true}                             | true  | TEST_SHOW_COLUMNS.N1 + 5 | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | N3_BIGINT         | {"type":"FIXED","precision":38,"scale":0,"nullable":true}                             | true  |                          | COLUMN |            |         | MY_DB         | IDENTITY START 1 INCREMENT 1 NOORDER  | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | N4_DEC            | {"type":"FIXED","precision":38,"scale":0,"nullable":true}                             | true  |                          | COLUMN |            |         | MY_DB         | IDENTITY START 1 INCREMENT 10 NOORDER | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | F1                | {"type":"REAL","nullable":true}                                                       | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | F2_DOUBLE         | {"type":"REAL","nullable":true}                                                       | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | F3_REAL           | {"type":"REAL","nullable":true}                                                       | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | S1                | {"type":"TEXT","length":16777216,"byteLength":16777216,"nullable":true,"fixed":false} | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | S2_VAR            | {"type":"TEXT","length":16777216,"byteLength":16777216,"nullable":true,"fixed":false} | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | S3_CHAR           | {"type":"TEXT","length":1,"byteLength":4,"nullable":true,"fixed":false}               | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | S4_TEXT           | {"type":"TEXT","length":16777216,"byteLength":16777216,"nullable":true,"fixed":false} | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | s5_case_sensitive | {"type":"TEXT","length":16777216,"byteLength":16777216,"nullable":true,"fixed":false} | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | B1                | {"type":"BINARY","length":8388608,"byteLength":8388608,"nullable":true,"fixed":true}  | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | B2_VAR            | {"type":"BINARY","length":8388608,"byteLength":8388608,"nullable":true,"fixed":false} | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | BOOL1             | {"type":"BOOLEAN","nullable":true}                                                    | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | D1                | {"type":"DATE","nullable":true}                                                       | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | T1                | {"type":"TIME","precision":0,"scale":9,"nullable":true}                               | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | TS1               | {"type":"TIMESTAMP_NTZ","precision":0,"scale":9,"nullable":true}                      | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | TS2_LTZ           | {"type":"TIMESTAMP_LTZ","precision":0,"scale":9,"nullable":true}                      | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | TS3_NTZ           | {"type":"TIMESTAMP_NTZ","precision":0,"scale":9,"nullable":true}                      | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
| TEST_SHOW_COLUMNS | MY_SCHEMA      | TS4_TZ            | {"type":"TIMESTAMP_TZ","precision":0,"scale":9,"nullable":true}                       | true  |                          | COLUMN |            |         | MY_DB         |                                       | NULL                    |
+-------------------+----------------+-------------------+---------------------------------------------------------------------------------------+-------+--------------------------+--------+------------+---------+---------------+---------------------------------------+-------------------------+
```
