# Introduction to error logging

When you turn on error logging for a table, Snowflake records the rows that can’t be written to the table in an
*error table*, along with the error and the data that caused it. For example, it records rows that have a value of the
wrong data type or that violate a [CHECK constraint](/sql-reference/constraints-overview#label-constraints-check). The
table for which error logging is turned on is called the *base table*. You can then use SQL to see why the rows
failed, correct the data, and write it again.

How error logging affects a statement or a load depends on the type of statement or load. A DML statement that
encounters a supported error writes the other rows and records the error instead of failing. For `COPY INTO` and
Snowpipe, the `ON_ERROR` copy option still controls how a load handles errors and determines which rejected rows are
recorded.

The error table records errors from sources that include the following:

| Source | What error logging records | More information |
| --- | --- | --- |
| `INSERT`, `UPDATE`, and `MERGE` statements on a table that has error logging turned on, and `CREATE TABLE ... AS SELECT` statements that set `ERROR_LOGGING = TRUE` | The supported errors that a statement encounters. The statement writes the other rows instead of failing. | [Error logging for DML statements](/user-guide/data-engineering/error-logging-dml) |
| `COPY INTO` and Snowpipe | The rows that a load rejects from CSV, JSON, and Parquet files. The `ON_ERROR` copy option determines which rejected rows are recorded. | [Error logging for COPY INTO and Snowpipe](/user-guide/data-load-error-tables) |

Expand

Show lessSee more

To record and correct errors from a source, start with the topic in the **More information** column. For the columns of
an error table, how long it keeps errors, how its storage is billed, the privileges that you need to query it, and how
replication and cloning treat it, see [Error tables](/user-guide/data-engineering/error-tables). The following sections describe how
to turn on error logging, how to prevent or limit it, and how to find the tables that have it turned on.

For error logging in Snowpipe Streaming with high-performance architecture, see
[Error logging in Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).

## Turn on error logging

You can turn on or turn off error logging when you create or alter a standard table or a Snowflake-managed
Apache Iceberg™ table. Standard tables include transient tables.

To turn on or turn off error logging for a table, use the following SQL commands to set the `ERROR_LOGGING`
property for the table:

- [CREATE TABLE](/sql-reference/sql/create-table)
- [ALTER TABLE](/sql-reference/sql/alter-table)
- [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake)
- [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) (Snowflake-managed only)

For example, the following statement turns on error logging for a table named `my_table`:

Copy code

```
ALTER TABLE my_table SET ERROR_LOGGING = TRUE;
```

To set the `ERROR_LOGGING` property for an existing table, use a role that owns the table. Use `ALTER TABLE`, not
`CREATE OR ALTER TABLE`. `CREATE OR ALTER TABLE` doesn’t change the `ERROR_LOGGING` property of a table that already
exists.

The error table stores the source data of each error. Before you turn on error logging for a table that stores
sensitive data, review which roles can query the error table, as described in
[Access control requirements for error tables](/user-guide/data-engineering/error-tables#label-dml-error-logging-access-control-error-tables).

Important

Turning on error logging affects every `INSERT`, `UPDATE`, and `MERGE` statement on the table, not only loads. A
statement that encounters a supported error no longer fails. It writes the other rows and records the error.
If an application or a pipeline relies on a failed statement to detect bad data, check the error table instead, as
described in [Detect errors in a scheduled job](/user-guide/data-engineering/error-logging-dml#label-dml-error-logging-detect-errors). Alternatively,
set the [OPT\_OUT\_ERROR\_LOGGING](/sql-reference/parameters#label-opt-out-error-logging) parameter to `TRUE` for the sessions that the application or pipeline uses.
In those sessions, `COPY INTO` statements also stop recording errors.

Turning off error logging drops the error table and every error in it. If you turn error logging on again, the table
gets a new, empty error table. For more information, see
[Error table lifecycle](/user-guide/data-engineering/error-tables#label-error-logging-error-table-lifecycle).

A DML statement, a `CREATE TABLE ... AS SELECT` statement, a `COPY INTO` statement, or a Snowpipe load records errors
in the error table only when *all* of the following conditions are met:

- The `ERROR_LOGGING` property is set to `TRUE` for the table.
- The [OPT\_OUT\_ERROR\_LOGGING](/sql-reference/parameters#label-opt-out-error-logging) parameter is `FALSE`, which is the default. Which value applies depends on the
  source of the error:
  - For DML statements, `CREATE TABLE ... AS SELECT` statements, and `COPY INTO`, the value for the session. You can
    set the parameter for the account, a user, or a session.
  - For Snowpipe, the value for the account. Values that are set for a user or a session don’t affect pipes.
- For `COPY INTO` and Snowpipe, the load uses `ON_ERROR = CONTINUE` or `ON_ERROR = SKIP_FILE`. The default for
  `COPY INTO`, `ABORT_STATEMENT`, records no errors. For more information, see
  [Which errors are recorded](/user-guide/data-load-error-tables#label-data-load-error-tables-on-error).
- For `COPY INTO` and Snowpipe, the files are CSV, JSON, or Parquet files.

If an error table doesn’t contain the errors that you expect from a load, see
[Troubleshoot missing errors](/user-guide/data-load-error-tables-query#label-data-load-error-tables-missing-errors).

## Prevent or limit error logging

When the [OPT\_OUT\_ERROR\_LOGGING](/sql-reference/parameters#label-opt-out-error-logging) parameter is `TRUE`, statements behave as if error logging were turned off: a
DML statement or a `CREATE TABLE ... AS SELECT` statement that encounters an error fails, and a `COPY INTO` statement
handles errors according to its `ON_ERROR` copy option without recording them. Unlike setting `ERROR_LOGGING = FALSE`,
the parameter doesn’t drop the error table or the errors in it. A value that’s set for a user or a session overrides the
value for the account. For example, if the parameter is `TRUE` for the account but `FALSE` for a user or a session,
statements in the affected sessions still record errors, so setting the parameter for the account doesn’t stop every
session from recording errors. Snowpipe pipes use only the value for the account, so setting the parameter to `TRUE` for
the account stops every Snowpipe pipe in the account from recording errors. To control which tables record errors,
control which roles own the tables: only a role that owns a table can turn on error logging for it.

## Find and monitor tables that have error logging turned on

To find the tables that have error logging turned on, use the following columns:

- The `error_logging` column in the output of [SHOW TABLES](/sql-reference/sql/show-tables), which is `ON` or `OFF`.
- The `ERROR_LOGGING` column of the TABLES view in [INFORMATION\_SCHEMA](/sql-reference/info-schema/tables),
  [ACCOUNT\_USAGE](/sql-reference/account-usage/tables), and
  [ORGANIZATION\_USAGE](/sql-reference/organization-usage/tables), which is `YES` or `NO`.

For example, the following query lists the tables in the account that have error logging turned on:

Copy code

```
SELECT table_catalog, table_schema, table_name, table_owner
  FROM SNOWFLAKE.ACCOUNT_USAGE.TABLES
  WHERE error_logging = 'YES'
    AND deleted IS NULL;
```

To see whether error logging is turned on for one table, you can also run the
[GET\_DDL](/sql-reference/functions/get_ddl) function and pass in the name of the base table:

Copy code

```
SELECT GET_DDL('TABLE', '[<namespace>.]<base_table_name>');
```

For example, for a base table named `my_table` in the current schema, run the following statement:

Copy code

```
SELECT GET_DDL('TABLE', 'my_table');
```

```
+------------------------------------+
| GET_DDL('TABLE', 'MY_TABLE')       |
|------------------------------------|
| create or replace TABLE MY_TABLE ( |
|     N NUMBER(4,0) NOT NULL,        |
|     T VARCHAR(5)                   |
| ) ERROR_LOGGING = true             |
| ;                                  |
+------------------------------------+
```

Metrics for error tables are recorded in the following views:

- [STORAGE\_USAGE view](/sql-reference/account-usage/storage_usage)
- [TABLE\_STORAGE\_METRICS view](/sql-reference/account-usage/table_storage_metrics)

In Cortex Code, the [`error-tables-ops`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-error-tables-ops)
bundled skill can help you find the tables that have error logging turned on, review their errors and storage, and
clean up errors.
