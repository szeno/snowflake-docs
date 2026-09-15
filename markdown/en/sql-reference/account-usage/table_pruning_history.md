Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# TABLE\_PRUNING\_HISTORY view

This Account Usage view can be used to determine the efficiency of pruning for all tables,
and to understand how a table’s default (natural) ordering of data affects pruning.

You can compare the number of partitions pruned (`PARTITIONS_PRUNED`) to the
total number of partitions scanned and pruned (`PARTITIONS_SCANNED + PARTITIONS_PRUNED`).

Each row in this view represents the pruning history for a specific table within a given time interval.
The data is aggregated by time interval and includes information about the number of scans, partitions
scanned, partitions pruned, rows scanned, and rows pruned.

You can also use this view to compare the effects on pruning before and after enabling
[Automatic Clustering](/user-guide/tables-auto-reclustering) and
[search optimization](/user-guide/search-optimization-service) for a table.

See also [TABLE\_QUERY\_PRUNING\_HISTORY view](/sql-reference/account-usage/table_query_pruning_history) and
[COLUMN\_QUERY\_PRUNING\_HISTORY view](/sql-reference/account-usage/column_query_pruning_history).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the time range (on the hour mark) during which the queries were executed and completed. |
| END\_TIME | TIMESTAMP\_LTZ | End of the time range (on the hour mark) during which the queries were executed and completed. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table that was queried. |
| TABLE\_NAME | VARCHAR | Name of the table that was queried. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table that was queried. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table that was queried. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table that was queried. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table that was queried. |
| NUM\_SCANS | NUMBER | Number of scan operations from all queries (including SELECT statements and DML statements) on the table during the START\_TIME and END\_TIME window. Note that a given query might result in multiple scan operations on the same table. |
| PARTITIONS\_SCANNED | NUMBER | Number of partitions scanned during the scan operations described in `NUM_SCANS`. |
| PARTITIONS\_PRUNED | NUMBER | Number of partitions pruned for the queries described in `NUM_SCANS`. These partitions were eliminated during query processing, improving the efficiency of the query. |
| ROWS\_SCANNED | NUMBER | Number of rows scanned during the scan operations described in `NUM_SCANS`. |
| ROWS\_PRUNED | NUMBER | Number of rows pruned for the queries described in `NUM_SCANS`. These rows were eliminated during query processing, improving the efficiency of the query. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 6 hours.
- This view does not include pruning information for [hybrid tables](/user-guide/tables-hybrid).
- This view retains data for the 1,000 longest-running table scans per query. Only extremely complex queries
  exceed this number of scans so data is rarely omitted.

## Examples

List the top five tables that had the worst pruning efficiency within the last seven days:

Copy code

```
SELECT
    table_id,
    ANY_VALUE(table_name) AS table_name,
    SUM(num_scans) AS total_num_scans,
    SUM(partitions_scanned) AS total_partitions_scanned,
    SUM(partitions_pruned) AS total_partitions_pruned,
    SUM(rows_scanned) AS total_rows_scanned,
    SUM(rows_pruned) AS total_rows_pruned
  FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_PRUNING_HISTORY
  WHERE start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  GROUP BY table_id
  ORDER BY
    total_partitions_pruned / GREATEST(total_partitions_scanned + total_partitions_pruned, 1),
    total_partitions_scanned DESC
  LIMIT 5;
```

```
+----------+----------------+-----------------+--------------------------+-------------------------+--------------------+-------------------+
| TABLE_ID | TABLE_NAME     | TOTAL_NUM_SCANS | TOTAL_PARTITIONS_SCANNED | TOTAL_PARTITIONS_PRUNED | TOTAL_ROWS_SCANNED | TOTAL_ROWS_PRUNED |
|----------+----------------+-----------------+--------------------------+-------------------------+--------------------+-------------------|
|   308226 | SENSOR_DATA_TS |              11 |                       21 |                       1 |           52500000 |           2500000 |
|   185364 | MATCH          |              16 |                       14 |                       2 |             240968 |             34424 |
|   209932 | ORDER_HEADER   |               2 |                      300 |                      56 |          421051748 |          75350790 |
|   209922 | K7_T1          |             261 |                      261 |                      52 |              30421 |              3272 |
|   338948 | SENSOR_DATA_TS |               9 |                       15 |                       3 |           38880000 |           8035200 |
+----------+----------------+-----------------+--------------------------+-------------------------+--------------------+-------------------+
```

The example above uses [GREATEST](/sql-reference/functions/greatest) to avoid dividing by zero when the sum of the number
of partitions scanned and the number of partitions pruned is zero.
