# Error tables

When error logging is turned on for a table, Snowflake automatically creates an error table that is associated with
the table. The table for which error logging is turned on is called the *base table*. To turn on error logging, see
[Turn on error logging](/user-guide/data-engineering/error-logging#label-dml-error-logging-configure). For how each source records errors
and how to correct them, see [Error logging for COPY INTO and Snowpipe](/user-guide/data-load-error-tables) and
[Error logging for DML statements](/user-guide/data-engineering/error-logging-dml).

Error tables have a fixed definition. The only statements that you can run directly on an error table are `SELECT`
and `TRUNCATE`. You can use error tables in dynamic tables, either directly or through a view, but not in materialized
views. For the privileges that you need to query an error table, see
[Access control requirements for error tables](#label-dml-error-logging-access-control-error-tables).

You can copy the data out of the error table to other tables. To remove the data in an error table, run the
`TRUNCATE` command.

To query an error table, pass the name of its base table to the `ERROR_TABLE` table function, such as
`SELECT * FROM ERROR_TABLE(my_table)`. For more information, see [Query and truncate an error table](#label-error-logging-query-truncate).

## Error table columns

Snowflake creates error tables with a standard definition that can’t be modified. An error table has the following
columns:

| Name | Type | Description |
| --- | --- | --- |
| `timestamp` | TIMESTAMP\_LTZ | The time when the statement that triggered the error started. For errors from Snowpipe, the value can be earlier than the time when the error was recorded. For more information, see [Error table fields for file loads](/user-guide/data-load-error-tables-query#label-data-load-error-tables-fields). |
| `query_id` | VARCHAR | The unique ID of the statement that triggered the error. For errors from Snowpipe, this value is `NULL`. |
| `error_code` | NUMBER | The error code. When multiple columns in one row contain errors, this column contains only the first error that’s encountered. |
| `error_metadata` | OBJECT | The error metadata.  The OBJECT values have the following structure:  ``` {   "error_code": <value>,   "error_message": "<value>",   "error_source": "<value>",   "sql_state": "<value>" } ```  The OBJECT values contain the following key-value pairs:   - `error_code`: The error code. - `error_message`: The error message. - `error_source`: The origin of the error, such as a column name. - `sql_state`: A five-character code that is modeled on the ANSI SQL standard   [SQLSTATE](https://en.wikipedia.org/wiki/SQLSTATE). Snowflake uses additional values beyond   those in the ANSI SQL standard.   When multiple columns in one row contain errors, this column contains only the first error that’s encountered. |
| `error_data` | OBJECT | The data that caused the error.  The OBJECT values have the following structure:  ``` {   "<column_name>": [     <invalid_column_values>   ],   "<column_name>": <valid_column_values>   ... } ```  The OBJECT values contain the key-value pairs that represent each column in the base table. The key is the column name. For invalid column values that caused the error, the value in the key-value pair is an array that contains the values. Valid values aren’t in arrays.  For an `UPDATE` statement or the update in a `MERGE` statement, the values are the ones that the row would have had after the update. For an `INSERT` statement or the insert in a `MERGE` statement, they’re the values of the row that the statement would have inserted. In both cases, the keys are the column names of the base table.  For an expression evaluation error, such as division by zero, the array can contain the operands of the expression, for example both inputs of a division, so its first element isn’t always the source value of the column.  If the data can’t be represented in an OBJECT value, the value is `NULL`. |

Expand

Show lessSee more

For errors from data loading, the `error_metadata` value also contains `service` and `details` fields, and in most
cases, the `error_data` value contains the source record in a `$1` field instead of column values. The following table
shows how the fields differ by source:

| Source | `error_metadata:service` | `error_metadata:details` | `error_data` | `query_id` |
| --- | --- | --- | --- | --- |
| DML statements and `CREATE TABLE ... AS SELECT` statements | None. | None. | The column values. | The query ID of the statement. |
| `COPY INTO` | `copy` | Fields such as the file, the location of the record in it, and the `ON_ERROR` value. For more information, see [Error table fields for file loads](/user-guide/data-load-error-tables-query#label-data-load-error-tables-fields). | In most cases, the source record in a `$1` field. | The query ID of the `COPY INTO` statement. |
| Snowpipe | `snowpipe` | Fields such as the pipe, the file, the location of the record in it, and the `ON_ERROR` value. | In most cases, the source record in a `$1` field. | `NULL`. |

Expand

Show lessSee more

To see only the errors from one source, filter on the `service` field. For example, to see only the errors from DML
statements and `CREATE TABLE ... AS SELECT` statements, filter on `error_metadata:service IS NULL`.

For errors from data loading, the error table stores the complete source record for each rejected row, including
values for columns that have a masking policy on the target table and fields that the load doesn’t insert into the
table. For more information, see [Access control requirements](/user-guide/data-load-error-tables#label-data-load-error-tables-access-control).

## Error table lifecycle

Snowflake doesn’t remove errors from an error table automatically. Errors stay in the error table until you truncate
it, turn off error logging, or drop or replace the base table.

When you turn off error logging for a base table, drop a base table that has an error table, or replace the base
table with `CREATE OR REPLACE TABLE`, the error table associated with the base table is dropped automatically. If you
restore a dropped base table with [UNDROP TABLE](/sql-reference/sql/undrop-table), its error table and the errors in it are
restored too. You can restore a dropped base table only during its
[Time Travel retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period).

Error tables store transient data, so they don’t have a Fail-safe period. You can’t use Time Travel to query an error
table at an earlier point in time. Errors that you remove with `TRUNCATE`, or that are dropped when you turn off error
logging, can’t be recovered.

## Query and truncate an error table

You can run `SELECT` statements and `TRUNCATE` statements on error tables by using the following
syntax:

Copy code

```
SELECT ... FROM ERROR_TABLE( <base_table_name> )

TRUNCATE [ TABLE ] [ IF EXISTS ] ERROR_TABLE( <base_table_name> )
```

Where:

`base_table_name`
:   The name of the table for which the error table was created.

For example, if the name of the base table is `my_table`, the following statement queries
the error table for this base table:

Copy code

```
SELECT * FROM ERROR_TABLE(my_table);
```

`TRUNCATE` removes every error in the error table, including errors from statements and loads that you didn’t
process, and errors that are recorded while you work with the table. You can’t delete individual errors, and you can’t
recover errors after you truncate the error table. Before you truncate, stop the statements and loads that write to the
base table, and copy any errors that you want to keep to another table. For the order of steps, see
[Correct and write rows again](/user-guide/data-engineering/error-logging-dml#label-dml-error-logging-correct-rows) for DML statements and
[Correct and reload rejected rows](/user-guide/data-load-error-tables-reload) for `COPY INTO` and Snowpipe.

The following statement truncates the error table:

Copy code

```
TRUNCATE ERROR_TABLE(my_table);
```

## Access control requirements for error tables

The following table summarizes the privileges for working with an error table:

| Task | Required privileges |
| --- | --- |
| Turn on or turn off error logging | OWNERSHIP on the base table. To create a table with error logging turned on, CREATE TABLE on the schema, or CREATE ICEBERG TABLE for a Snowflake-managed Apache Iceberg™ table. |
| Record errors in the error table | None. Any role that can write to the base table can cause errors to be recorded in its error table. |
| Query the error table | OWNERSHIP, or both SELECT and SELECT ERROR TABLE, on the base table. If a masking policy, a row access policy, or a projection policy is set directly on the base table or on its columns, also the global READ UNREDACTED ERROR TABLE privilege. As for any query, the role also needs USAGE on the database, the schema, and a warehouse. |
| Clear the error table with `TRUNCATE` | OWNERSHIP or TRUNCATE on the base table. |

Expand

Show lessSee more

Warning

The policies on the base table don’t mask or filter the data in the error table, so a role that can query the error
table sees the values that the policies protect.

Masking policies that are assigned through [tags](/user-guide/tag-based-masking-policies) don’t require the READ
UNREDACTED ERROR TABLE privilege, no matter which object the tag is set on. A role that has the SELECT and SELECT ERROR
TABLE privileges on the base table sees the masked values when it queries the base table, but it sees the original
values in the error table, both in the `error_data` column and in any error messages that include them. Grant the
SELECT ERROR TABLE privilege only to roles that are allowed to see the unmasked data.

Regardless of the current role, direct inserts into an error table aren’t allowed.

To let a role query an error table, grant it both the SELECT privilege and the SELECT ERROR TABLE privilege on the base
table. The SELECT ERROR TABLE privilege alone isn’t enough. For example, the following statements let the `myrole`
role query the error table of a base table named `mybasetable`:

Copy code

```
GRANT SELECT ON TABLE mybasetable TO ROLE myrole;
GRANT SELECT ERROR TABLE ON TABLE mybasetable TO ROLE myrole;
```

To grant the SELECT ERROR TABLE privilege, run a [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) statement or a
[GRANT <privileges> … TO USER](/sql-reference/sql/grant-privilege-user) statement. These statements use the following syntax:

Copy code

```
GRANT SELECT ERROR TABLE ON TABLE <base_table_name> TO ROLE <role_name>

GRANT SELECT ERROR TABLE ON TABLE <base_table_name> TO USER <user_name>
```

Granting `ALL` privileges on a table also grants the SELECT ERROR TABLE privilege, including when you grant the
privileges on all tables or on future tables in a schema or database. Before you turn on error logging for a table that
stores sensitive data, run [SHOW GRANTS](/sql-reference/sql/show-grants) for the table to see which roles have the SELECT ERROR
TABLE privilege, and revoke it from roles that shouldn’t see the source data:

Copy code

```
SHOW GRANTS ON TABLE mybasetable;

REVOKE SELECT ERROR TABLE ON TABLE mybasetable FROM ROLE analyst_role;
```

To find the roles that get the privilege on tables that are created later, run `SHOW FUTURE GRANTS IN SCHEMA` and
`SHOW FUTURE GRANTS IN DATABASE`.

To find every table that has error logging turned on, see
[Find and monitor tables that have error logging turned on](/user-guide/data-engineering/error-logging#label-error-logging-find-tables).

If a masking policy, a row access policy, or a projection policy is set directly on the base table or on its columns, a
query on the error table also requires the global READ UNREDACTED ERROR TABLE privilege. Without this privilege, the
query fails. The role needs this privilege even if it owns the base table. This privilege must be granted by the
`ACCOUNTADMIN` role:

Copy code

```
USE ROLE ACCOUNTADMIN;
GRANT READ UNREDACTED ERROR TABLE ON ACCOUNT TO ROLE myrole;
```

Because READ UNREDACTED ERROR TABLE is a global privilege, it applies to the error tables of every table in the account.
The role still needs the OWNERSHIP privilege, or both the SELECT and SELECT ERROR TABLE privileges, on each base table
whose error table it queries. For more information, see
[Global privileges (account privileges)](/user-guide/security-access-control-privileges#label-global-privileges).

Instead of granting the SELECT ERROR TABLE privilege, the base table owner can create a view based on the error table
and grant access to that view. The view uses the privileges of the view owner, so any role
that can query the view can see the errors, including the source data for each error. To limit what the view
exposes, select only the columns that the roles need. The `error_data` column and the error messages in the
`error_metadata` column can contain source data. For example, the following view lets a support role see which errors
occurred, without the source data or the error messages:

Copy code

```
CREATE VIEW mybasetable_error_summary AS
  SELECT timestamp,
         query_id,
         error_code,
         error_metadata:service::STRING AS service,
         error_metadata:error_source::STRING AS error_source
    FROM ERROR_TABLE(mybasetable);

GRANT SELECT ON VIEW mybasetable_error_summary TO ROLE support_role;
```

To let a role clear an error table, grant it the TRUNCATE privilege on the base table:

Copy code

```
GRANT TRUNCATE ON TABLE mybasetable TO ROLE myrole;
```

The SELECT ERROR TABLE privilege doesn’t allow a role to truncate the error table. The TRUNCATE privilege also allows
the role to run `TRUNCATE TABLE` on the base table, which deletes the rows in the base table.

## Streams on error tables

[Streams](/user-guide/streams-intro) aren’t supported directly on error tables. To track changes to an error table,
create a view on the error table, and then create a stream on the view.

The following example creates a view on an error table and a stream on the view:

1. Run the [CREATE VIEW](/sql-reference/sql/create-view) command to create a view on the error table:

   Copy code

   ```
   CREATE VIEW my_error_view AS
     SELECT timestamp,
            query_id,
            error_code,
            error_metadata,
            error_data
       FROM ERROR_TABLE(mydb.myschema.my_table);
   ```
2. Run the [CREATE STREAM](/sql-reference/sql/create-stream) command to create a stream on the view:

   Copy code

   ```
   CREATE STREAM my_error_stream ON VIEW my_error_view;
   ```

When you truncate the error table, the stream returns a `DELETE` row for each error that you removed. To process only
new errors, select the rows where `METADATA$ACTION` is `INSERT`:

Copy code

```
SELECT * FROM my_error_stream WHERE METADATA$ACTION = 'INSERT';
```

A standard stream returns the net changes since you last consumed it, so an error that’s recorded and then removed
before you consume the stream doesn’t appear in it. Consume the stream before you truncate the error table.

Querying a stream doesn’t consume it. To consume the stream, use it in a DML statement. For example, the following
statements create a table named `my_error_log`, which has the same columns as the error table, and copy the new errors
to it. After the `INSERT` statement commits, the stream returns only the errors that are recorded later:

Copy code

```
CREATE TABLE my_error_log (
  timestamp TIMESTAMP_LTZ,
  query_id VARCHAR,
  error_code NUMBER,
  error_metadata OBJECT,
  error_data OBJECT
);

INSERT INTO my_error_log
  SELECT timestamp, query_id, error_code, error_metadata, error_data
    FROM my_error_stream
    WHERE METADATA$ACTION = 'INSERT';
```

The view on the error table uses the privileges of its owner, so any role that can query the view or the stream can
see the errors. Grant access to the view, the stream, and any table that you copy the errors to only to roles that are
allowed to see the source data.

## Usage notes

- Snowflake charges for data stored in the error table at the standard storage rate. For information about how long
  errors stay in the error table, see [Error table lifecycle](#label-error-logging-error-table-lifecycle). The `bytes` value that
  [SHOW TABLES](/sql-reference/sql/show-tables) reports for the base table, and the `BYTES` column of the
  [TABLES view](/sql-reference/account-usage/tables), don’t include the storage of its error table.
- When a base table with an associated error table is cloned, the behavior is as follows:
  - The base table’s schema and content are cloned.
  - The error table’s content isn’t cloned.
  - The cloned base table has the `ERROR_LOGGING` property turned on, which implicitly creates an empty error
    table for it.
- When you replicate a database, its error tables and the errors in them are replicated with it, so the source data in
  the errors is copied to every account that the database is replicated to. If the source data must not leave the
  account, truncate the error tables before each refresh, or don’t turn on error logging for those tables. Before you
  truncate an error table, stop the statements and loads that write to the base table, as described in
  [Query and truncate an error table](#label-error-logging-query-truncate). For more information, see
  [Replicated database objects](/user-guide/account-replication-intro#label-replicated-database-objects).
