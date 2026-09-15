Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# TABLE\_DML\_HISTORY view

This Account Usage view can be used to determine the magnitude and effects of the DML operations performed on a table. Note that
these DML operations include ones initiated by [Snowpipe](/user-guide/data-load-snowpipe-intro) but exclude operations initiated
by background maintenance services
(for example, [Automatic Clustering](/user-guide/tables-auto-reclustering), maintenance for materialized views and
[search optimization](/user-guide/search-optimization-service)).

You can query this view with the [QUERY\_HISTORY view](/sql-reference/account-usage/query_history) and the
[LOAD\_HISTORY view](/sql-reference/account-usage/load_history) to identify the DML operations that have a significant impact. This can
help you to identify opportunities for optimization.

In addition, you can query this view with the [AUTOMATIC\_CLUSTERING\_HISTORY view](/sql-reference/account-usage/automatic_clustering_history) and the
[SEARCH\_OPTIMIZATION\_HISTORY view](/sql-reference/account-usage/search_optimization_history) to visualize the relationship between these DML operations and the
credits charged for Automatic Clustering and the search optimization service. (These services can be triggered by DML operations.)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the time range (on the hour mark) during which the DML operations were performed. |
| END\_TIME | TIMESTAMP\_LTZ | End of the time range (on the hour mark) during which the DML operations were performed. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table modified by the DML operations. |
| TABLE\_NAME | VARCHAR | Name of the table modified by the DML operations. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table modified by the DML operations. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table modified by the DML operations. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table modified by the DML operations. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table modified by the DML operations. |
| ROWS\_ADDED | NUMBER | Number of rows added by DML operations performed by users on the table during the START\_TIME and END\_TIME window. |
| ROWS\_REMOVED | NUMBER | Number of rows removed by DML operations performed by users on the table during the START\_TIME and END\_TIME window. |
| ROWS\_UPDATED | NUMBER | Number of rows updated by DML operations performed by users on the table during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 6 hours.
- This view does not include DML operations on [hybrid tables](/user-guide/tables-hybrid).

## Examples

The following example returns the top five tables that had the most rows added, removed, and updated by DML operations within the
last seven days.

Copy code

```
SELECT
    table_id,
    ANY_VALUE(table_name) AS table_name,
    SUM(rows_added) AS total_rows_added,
    SUM(rows_removed) AS total_rows_removed,
    SUM(rows_updated) AS total_rows_updated
  FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_DML_HISTORY
  WHERE start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  GROUP BY table_id
  ORDER BY total_rows_added + total_rows_removed + total_rows_updated DESC
  LIMIT 5;
```

```
+----------+----------------------+------------------+--------------------+--------------------+
| TABLE_ID | TABLE_NAME           | TOTAL_ROWS_ADDED | TOTAL_ROWS_REMOVED | TOTAL_ROWS_UPDATED |
|----------+----------------------+------------------+--------------------+--------------------|
|   338948 | SENSOR_DATA_TS       |          5356800 |             259200 |                  0 |
|   338950 | SENSOR_DATA_DEVICE2  |          2678400 |                  0 |                  0 |
|   341006 | SENSOR_DATA_30_ROWS  |               30 |                  0 |                  0 |
|   341004 | SENSOR_DATA_12_HOURS |               12 |                  0 |                  0 |
|   340005 | SENSOR_DATA_12_HOURS |               12 |                  0 |                  0 |
+----------+----------------------+------------------+--------------------+--------------------+
```
