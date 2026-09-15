# LOAD\_HISTORY view

This Information Schema view enables you to retrieve the history of data loaded into tables using the [COPY INTO <table>](/sql-reference/sql/copy-into-table) command within the last 14 days. The view displays one row for each file loaded.

Note

This view does not return the history of data loaded using Snowpipe. For this historical information, query the [COPY\_HISTORY](/sql-reference/functions/copy_history) table function instead.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| SCHEMA\_NAME | VARCHAR | Schema of target table |
| FILE\_NAME | VARCHAR | Name of source file |
| TABLE\_NAME | VARCHAR | Name of target table |
| LAST\_LOAD\_TIME | TIMESTAMP\_LTZ | Timestamp of the load record |
| STATUS | VARCHAR | Status: `LOADED`, `LOAD FAILED`, or `PARTIALLY LOADED` |
| ROW\_COUNT | NUMBER | Number of rows loaded from the source file |
| ROW\_PARSED | NUMBER | Number of rows parsed from the source file |
| FIRST\_ERROR\_MESSAGE | VARCHAR | First error of the source file |
| FIRST\_ERROR\_LINE\_NUMBER | NUMBER | Line number of the first error |
| FIRST\_ERROR\_CHARACTER\_POSITION | NUMBER | Position of the first error character |
| FIRST\_ERROR\_COL\_NAME | VARCHAR | Column name of the first error |
| ERROR\_COUNT | NUMBER | Number of error rows in the source file |
| ERROR\_LIMIT | NUMBER | If the number of errors reaches this limit, then abort |

Expand

Show lessSee more

## Usage notes

- The historical data for COPY INTO commands is removed from the view when a table is dropped.
- The view only includes COPY INTO commands that executed to completion, with or without errors. No record is added if the transaction is rolled back, for example, or if the ON\_ERROR = ABORT\_STATEMENT copy option is included in the COPY INTO *<table>* statement and a detected error in a data file aborts the load operation.
- This view returns an upper limit of 10,000 rows. To avoid this limitation, use the [LOAD\_HISTORY view](/sql-reference/account-usage/load_history) (Account Usage), [COPY\_HISTORY function](/sql-reference/functions/copy_history) (Information Schema), or the [COPY\_HISTORY view](/sql-reference/account-usage/copy_history) (Account Usage).
- When including a WHERE clause that references the `LAST_LOAD_TIME` column, you can specify any day of the week. For example, April 1, 2016 was a Friday; however, specifying Sunday instead does not
  affect the query results:

  Copy code

  ```
  WHERE last_load_time > 'Sun, 01 Apr 2016 16:00:00 -0800'
  ```

- The LOAD\_HISTORY view shows load history only after the latest truncate operation on the target table. This applies to the LOAD\_HISTORY views before and after
  [replication](/user-guide/account-replication-intro).

## Examples

Retrieve the history of data loaded into the `MYDB.PUBLIC.MYTABLE` table since April 1, 2016, assuming that April 1 occurred within the previous 14 days:

> Copy code
>
> ```
> USE DATABASE mydb;
>
> SELECT table_name, last_load_time
>   FROM information_schema.load_history
>   WHERE schema_name=current_schema() AND
>   table_name='MYTABLE' AND
>   last_load_time > 'Fri, 01 Apr 2016 16:00:00 -0800';
> ```

Retrieve records for the 10 most recent COPY INTO commands executed against the `MYDB` database:

> Copy code
>
> ```
> USE DATABASE mydb;
>
> SELECT table_name, last_load_time
>   FROM information_schema.load_history
>   ORDER BY last_load_time DESC
>   LIMIT 10;
> ```
