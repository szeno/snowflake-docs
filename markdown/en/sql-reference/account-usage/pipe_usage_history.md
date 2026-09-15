Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# PIPE\_USAGE\_HISTORY view

This Account Usage view can be used to query the history of data loaded into tables
using [Snowpipe](/user-guide/data-load-snowpipe-intro) or the history of credits used for
[Iceberg automated refresh](/user-guide/tables-iceberg-auto-refresh) within the last 365 days (1 year).

The view displays the history of data loaded and credits billed for your entire Snowflake account.
You can use the `pipe_name` column to filter the view for a specific pipe or Iceberg table with automated refresh.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| PIPE\_ID | NUMBER | Internal/system-generated identifier for the pipe used for the data load. Displays NULL if no pipe name was specified in the query. Each row includes the totals for all pipes in use within the time range. |
| PIPE\_NAME | VARCHAR | Name of the pipe or Iceberg table with automated refresh. Displays NULL for the internal (hidden) pipe object used to refresh the metadata for an external table or Delta-based Iceberg table. |
| START\_TIME | TIMESTAMP\_LTZ | Start time of the period when data-ingestion information is aggregated. |
| END\_TIME | TIMESTAMP\_LTZ | End time of the period when data-ingestion information is aggregated. |
| CREDITS\_USED | NUMBER | Number of credits billed for Snowpipe data loads during the START\_TIME and END\_TIME window. |
| BYTES\_INSERTED | FLOAT | Number of bytes loaded during the START\_TIME and END\_TIME window. |
| FILES\_INSERTED | VARIANT | Number of files loaded during the START\_TIME and END\_TIME window. |
| BYTES\_BILLED | NUMBER | Represents the number of bytes Snowpipe uses for billing purposes, providing visibility into Snowpipe’s cost implications directly within these history views. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- If you want to reconcile the data in this view with a corresponding view in the [ORGANIZATION USAGE schema](/sql-reference/organization-usage), you must first set the timezone of the session to UTC. Before querying the Account Usage view, execute:

  > Copy code
  >
  > ```
  > ALTER SESSION SET TIMEZONE = UTC;
  > ```
- Occasionally, the data compaction and maintenance process can consume Snowflake credits. For example, the returned results might show that you consumed credits with 0 BYTES\_INSERTED and 0 FILES\_INSERTED. This means that your data is not being loaded, but the data compaction and maintenance process has consumed some credits.

- Snowflake bills for auto-refresh notifications in external tables and directory tables on internal named stages and external stages at a rate equivalent to the Snowpipe file charge. You can estimate charges incurred by your external table and directory table auto-refresh
  notifications by examining this PIPE\_USAGE\_HISTORY view or querying the [PIPE\_USAGE\_HISTORY](/sql-reference/functions/pipe_usage_history) function. Note that the auto-refresh pipes will be listed under a NULL pipe
  name. You can also view your external table auto-refresh notification history at the table-level/stage-level granularity by using the
  Information Schema table function [AUTO\_REFRESH\_REGISTRATION\_HISTORY](/sql-reference/functions/auto_refresh_registration_history).

  To avoid charges for auto-refresh notifications, perform a manual refresh for external tables and directory tables. For external tables, the
  ALTER EXTERNAL TABLE <name> REFRESH … statement can be used to manually synchronize your external table to external storage. For directory
  tables, the ALTER STAGE <name> REFRESH … statement can be used to manually synchronize the directory to external storage.
- Snowflake does not bill Snowpipe file charges for [Iceberg automated refresh](/user-guide/tables-iceberg-auto-refresh).

## Examples

This query provides the pipe usage history for a pipe named `my_auto_refresh_pipe` starting on a particular date:

Copy code

```
SELECT
    pipe_id,
    start_time,
    end_time,
    credits_used,
    bytes_inserted,
    files_inserted
  FROM SNOWFLAKE.ACCOUNT_USAGE.PIPE_USAGE_HISTORY
  WHERE pipe_name = 'my_auto_refresh_pipe'
  AND START_TIME >= '2025-04-01';
```

This query displays the credits used for automated refresh charges for an Iceberg table named `iceberg_glue_table`
starting on a particular date:

Copy code

```
SELECT
    pipe_id,
    start_time,
    end_time,
    credits_used,
  FROM SNOWFLAKE.ACCOUNT_USAGE.PIPE_USAGE_HISTORY
  WHERE pipe_name = 'iceberg_glue_table'
  AND START_TIME >= '2025-04-01';
```
