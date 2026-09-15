Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# COPY\_HISTORY view

This Account Usage view can be used to query Snowflake data loading history for the last 365 days (1 year). The view displays load activity
for both [COPY INTO <table>](/sql-reference/sql/copy-into-table) statements and continuous data loading using
[Snowpipe](/user-guide/data-load-snowpipe-intro). The view avoids the 10,000 row limitation of
the [LOAD\_HISTORY view](/sql-reference/info-schema/load_history).

You can also view data loading details in Snowsight. See [Monitor data loading activity by using Copy History](/user-guide/data-load-monitor).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| FILE\_NAME | VARCHAR | Name of the source file and relative path to the file. |
| STAGE\_LOCATION | VARCHAR | Name of the stage where the source file is located. |
| LAST\_LOAD\_TIME | TIMESTAMP\_LTZ | Date and time of when the file finished loading. |
| ROW\_COUNT | NUMBER | Number of rows loaded from the source file. |
| ROW\_PARSED | NUMBER | Number of rows parsed from the source file; `NULL` if STATUS is `Load in progress`. |
| FILE\_SIZE | NUMBER | Observed size of the source file in the internal or external stage before it loads. If the file is compressed, this shows the compressed size. If the file is uncompressed, this shows the uncompressed size. |
| FIRST\_ERROR\_MESSAGE | VARCHAR | First error of the source file. |
| FIRST\_ERROR\_LINE\_NUMBER | NUMBER | Line number of the first error. |
| FIRST\_ERROR\_CHARACTER\_POS | NUMBER | Position of the first error character. |
| FIRST\_ERROR\_COLUMN\_NAME | VARCHAR | Column name of the first error. |
| ERROR\_COUNT | NUMBER | Number of error rows in the source file. |
| ERROR\_LIMIT | NUMBER | If the number of errors reaches this limit, then abort. |
| STATUS | VARCHAR | Status: `Loaded`, `Load failed`, `Partially loaded`, or `Load skipped`. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the target table. |
| TABLE\_NAME | VARCHAR | Name of the target table.TABLE\_NAME |
| TABLE\_SCHEMA\_ID | NUMBER | Internal, Snowflake-generated identifier of the schema for the table. |
| TABLE\_SCHEMA\_NAME | VARCHAR | Name of the schema in which the target table resides. |
| TABLE\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the table. |
| TABLE\_CATALOG\_NAME | VARCHAR | Name of the database in which the target table resides. |
| PIPE\_CATALOG\_NAME | VARCHAR | Name of the database in which the pipe resides. |
| PIPE\_SCHEMA\_NAME | VARCHAR | Name of the schema in which the pipe resides. |
| PIPE\_NAME | VARCHAR | Name of the pipe defining the load parameters; `NULL` for COPY statement loads. |
| PIPE\_RECEIVED\_TIME | TIMESTAMP\_LTZ | Date and time when the INSERT request for the file loaded through the pipe was received; `NULL` for COPY statement loads. |
| FIRST\_COMMIT\_TIME | TIMESTAMP\_LTZ | Date and time when the first chunk of the file is committed. Snowpipe may load a file in multiple chunks that are separately committed. |
| BYTES\_BILLED | NUMBER | Represents the number of bytes Snowpipe uses for billing purposes, providing visibility into Snowpipe’s cost implications directly within these history views. |

Expand

Show lessSee more

## Usage notes

- In most cases, latency for the view may be up to 120 minutes (2 hours). The latency for a given table’s copy history may be up to 2 days
  if both of the following conditions are true:
  - Fewer than 32 DML statements have been added to the given table since it was last updated in COPY\_HISTORY.
  - Fewer than 100 rows have been added to the given table since it was last updated in COPY\_HISTORY.

- The view only includes COPY INTO commands that executed to completion, with or without errors.
- Dropping or recreating a table object removes the load history metadata for bulk data load deduplication (COPY INTO *<table>* statements) into the table.
- Renaming a table object updates the corresponding TABLE\_NAME entries in the copy history.
- Dropping or recreating a pipe object doesn’t remove the load history metadata for the pipe.
- The view only displays objects for which the current role for the session has been granted access privileges.
- After the replication of copy history, the COPY\_HISTORY Account Usage view shows the history only after the latest truncate operation on the target table. This is different from the view without replication, which shows a complete copy history.

## Examples

Retrieve records for the 10 most recent COPY INTO commands executed:

Copy code

```
select file_name, error_count, status, last_load_time from snowflake.account_usage.copy_history
  order by last_load_time desc
  limit 10;
```
