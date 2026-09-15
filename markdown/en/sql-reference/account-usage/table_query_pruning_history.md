Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# TABLE\_QUERY\_PRUNING\_HISTORY view

Use this Account Usage view to gain a better understanding of data access patterns during
query execution.

You can use this view in combination with the [COLUMN\_QUERY\_PRUNING\_HISTORY view](/sql-reference/account-usage/column_query_pruning_history). For example,
you can identify access to target tables by using the TABLE\_QUERY\_PRUNING\_HISTORY view, then
identify frequently used columns on those tables by using the COLUMN\_QUERY\_PRUNING\_HISTORY view.

In particular, these views can help you make a more educated choice for
[clustering keys](/user-guide/tables-clustering-keys).

Each row in this view represents the query pruning history for a specific table within a given time interval. The data is
aggregated by time interval and includes information about the number of queries executed, partitions scanned, partitions pruned,
rows scanned, rows pruned, and rows matched.

See also [TABLE\_PRUNING\_HISTORY view](/sql-reference/account-usage/table_pruning_history) and [Query Pruning](/user-guide/tables-clustering-micropartitions#label-micropartitions-query-pruning).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| INTERVAL\_START\_TIME | TIMESTAMP\_LTZ | Start of the time range (on the hour mark) during which the queries were executed. |
| INTERVAL\_END\_TIME | TIMESTAMP\_LTZ | End of the time range (on the hour mark) during which the queries were executed. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table that was queried. |
| TABLE\_NAME | VARCHAR | Name of the table that was queried. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table that was queried. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table that was queried. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table that was queried. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table that was queried. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse that was used to run the queries. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse that ran the queries. |
| QUERY\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-hash) computed based on the canonicalized SQL text. |
| QUERY\_PARAMETERIZED\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-parameterized-hash) computed based on the parameterized query. |
| NUM\_QUERIES | NUMBER | Number of queries executed in this time range with this specific QUERY\_HASH value, using this warehouse, accessing this table. |
| AGGREGATE\_QUERY\_ELAPSED\_TIME | NUMBER | Total elapsed time (in milliseconds) for queries defined by NUM\_QUERIES. This total includes queueing and other time not associated with compilation and execution. |
| AGGREGATE\_QUERY\_COMPILATION\_TIME | NUMBER | Total compilation time (in milliseconds) for queries defined by NUM\_QUERIES. |
| AGGREGATE\_QUERY\_EXECUTION\_TIME | NUMBER | Total execution time (in milliseconds) for queries defined by NUM\_QUERIES. |
| PARTITIONS\_SCANNED | NUMBER | Number of partitions scanned on this table for queries defined by NUM\_QUERIES. |
| PARTITIONS\_PRUNED | NUMBER | Number of partitions pruned on this table for queries defined by NUM\_QUERIES. These partitions were eliminated during query processing and not scanned, improving the efficiency of the query. |
| ROWS\_SCANNED | NUMBER | Number of rows scanned on this table for queries defined by NUM\_QUERIES. |
| ROWS\_PRUNED | NUMBER | Number of rows pruned on this table for queries defined by NUM\_QUERIES. These rows were eliminated during query processing and not scanned, improving the efficiency of the query. |
| ROWS\_MATCHED | NUMBER | Number of rows that matched the WHERE clause filters while scanning this table for the queries defined by NUM\_QUERIES. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 4 hours.
- Data is retained for 1 year.
- This view does not include pruning information for [hybrid tables](/user-guide/tables-hybrid).
- For complex filtering conditions that can’t benefit from a pushdown optimization, rows might not be filtered out during the table scan operation, even if they do not match the filtering condition. Therefore, these rows are counted in the ROWS\_MATCHED value.
- Users and roles that have been granted the USAGE\_VIEWER database role can access this view. For more information, see
  [SNOWFLAKE database roles](/sql-reference/snowflake-db-roles).
- This view retains data for the 1,000 longest-running table scans per query. Only extremely complex queries
  exceed this number of scans so data is rarely omitted.

## Examples

The first query is a simple functional example that returns the pruning history for queries against a specific table
on a specific date where at least one row was pruned. Each row in the result belongs to a specific one-hour time window
for queries that were completed on the date specified in the WHERE clause (INTERVAL\_START\_TIME).

The `sensor_data_ts` table in this query contains 5356800 rows of synthetic time-series data. Exactly half of the rows in the table (2678400) were pruned for all of the queries shown here. The number of matched rows varies for these queries.

Copy code

```
SELECT interval_start_time, interval_end_time, table_id, table_name,
    num_queries, query_hash, rows_scanned, rows_pruned, rows_matched
  FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_QUERY_PRUNING_HISTORY
  WHERE interval_start_time LIKE '2025-04-24%'
    AND table_name='SENSOR_DATA_TS'
    AND rows_pruned > 0
  ORDER BY 1;
```

```
+-------------------------------+-------------------------------+----------+----------------+-------------+----------------------------------+--------------+-------------+--------------+
| INTERVAL_START_TIME           | INTERVAL_END_TIME             | TABLE_ID | TABLE_NAME     | NUM_QUERIES | QUERY_HASH                       | ROWS_SCANNED | ROWS_PRUNED | ROWS_MATCHED |
|-------------------------------+-------------------------------+----------+----------------+-------------+----------------------------------+--------------+-------------+--------------|
| 2025-04-24 14:00:00.000 -0700 | 2025-04-24 15:00:00.000 -0700 |   652324 | SENSOR_DATA_TS |           1 | 833f4ec4ebbda62c7882e1839faec799 |      2678400 |     2678400 |            5 |
| 2025-04-24 14:00:00.000 -0700 | 2025-04-24 15:00:00.000 -0700 |   652324 | SENSOR_DATA_TS |           1 | 94d16d2fa0892247d27066e45b58d3e4 |      2678400 |     2678400 |            5 |
| 2025-04-24 15:00:00.000 -0700 | 2025-04-24 16:00:00.000 -0700 |   652324 | SENSOR_DATA_TS |           1 | 24e89f5c01209d7b395f56559f893dc8 |      2678400 |     2678400 |      2678400 |
| 2025-04-24 15:00:00.000 -0700 | 2025-04-24 16:00:00.000 -0700 |   652324 | SENSOR_DATA_TS |           1 | 71c9c6570ef849e66f83af0625b793a2 |      2678400 |     2678400 |      2678400 |
| 2025-04-24 15:00:00.000 -0700 | 2025-04-24 16:00:00.000 -0700 |   652324 | SENSOR_DATA_TS |           1 | c75cb64d446c1ba222ac14ebd1923641 |      2678400 |     2678400 |      2678400 |
| 2025-04-24 15:00:00.000 -0700 | 2025-04-24 16:00:00.000 -0700 |   652324 | SENSOR_DATA_TS |           1 | 5a3784c59fc788804c903d96698dd969 |      2678400 |     2678400 |            5 |
| 2025-04-24 17:00:00.000 -0700 | 2025-04-24 18:00:00.000 -0700 |   652324 | SENSOR_DATA_TS |           1 | 069a076d4d6850e3d242fccf498c7c6d |      2678400 |     2678400 |       216642 |
| 2025-04-24 17:00:00.000 -0700 | 2025-04-24 18:00:00.000 -0700 |   652324 | SENSOR_DATA_TS |           1 | 4c9c5aacb7a61fc6858d107c5c46fb14 |      2678400 |     2678400 |       216642 |
| 2025-04-24 17:00:00.000 -0700 | 2025-04-24 18:00:00.000 -0700 |   652324 | SENSOR_DATA_TS |           1 | 3e509721380b262906c62c76107e46c9 |      2678400 |     2678400 |      2678400 |
| 2025-04-24 17:00:00.000 -0700 | 2025-04-24 18:00:00.000 -0700 |   652324 | SENSOR_DATA_TS |           1 | 9f7e607fe48faa18e332f65cde49f037 |      2678400 |     2678400 |      2678400 |
| 2025-04-24 17:00:00.000 -0700 | 2025-04-24 18:00:00.000 -0700 |   652324 | SENSOR_DATA_TS |           1 | b4488d8a84ab18b00dd6b2fead4a4cb4 |      2678400 |     2678400 |       394106 |
| 2025-04-24 17:00:00.000 -0700 | 2025-04-24 18:00:00.000 -0700 |   652324 | SENSOR_DATA_TS |           1 | 157d775a79c5bae120fb5db9f7d8d027 |      2678400 |     2678400 |       216642 |
+-------------------------------+-------------------------------+----------+----------------+-------------+----------------------------------+--------------+-------------+--------------+
```

The following example calculates a “pruning ratio” for each table to help determine the pruning efficiency for queries
run on a given warehouse at a given time. The query also returns the number of partitions scanned per query, which
helps you to understand query performance with respect to the volume of data that has to be scanned.

Given the results of this query, users might conclude that while `sensor_data_ts` is accessed much more than `sensor_data1`,
these queries typically take less time and scan far fewer micro-partitions.

Copy code

```
SELECT
    SUM(aggregate_query_execution_time) as sum_exec_time,
    SUM(num_queries) as sum_num_queries,
    SUM(partitions_pruned)/SUM(partitions_pruned+partitions_scanned) AS pruning_ratio,
    SUM(partitions_scanned)/SUM(num_queries) AS partitions_scanned_per_query,
    table_name,
    schema_name,
    database_name
  FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_QUERY_PRUNING_HISTORY
  WHERE interval_start_time > '2025-04-25 12:00:00.000 -0700'
    AND warehouse_name = 'SENSORS_WH'
  GROUP BY ALL
  ORDER BY 1 DESC;
```

```
+---------------+-----------------+---------------+------------------------------+----------------+----------------+---------------+
| SUM_EXEC_TIME | SUM_NUM_QUERIES | PRUNING_RATIO | PARTITIONS_SCANNED_PER_QUERY | TABLE_NAME     | SCHEMA_NAME    | DATABASE_NAME |
|---------------+-----------------+---------------+------------------------------+----------------+----------------+---------------|
|       1938743 |           19283 |      0.230000 |                  1800.000000 | SENSOR_DATA1   | SENSORS_SCHEMA | SENSORS_DB    |
|        123732 |           39320 |      0.950000 |                    12.000000 | SENSOR_DATA_TS | SENSORS_SCHEMA | SENSORS_DB    |
+---------------+-----------------+---------------+------------------------------+----------------+----------------+---------------+
```
