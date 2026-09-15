# Queries too large to fit in memory

This topic discusses how a warehouse owner or administrator can resolve memory spillage in order to improve the performance of a query.

Performance degrades drastically when a warehouse runs out of memory while executing a query because memory bytes must “spill” onto local
disk storage. If the query requires even more memory, it spills onto remote cloud-provider storage, which results in even worse performance.

Note

You must have [access to the shared SNOWFLAKE database](/sql-reference/account-usage#label-enabling-usage-for-other-roles) to execute the diagnostic queries provided in this topic. By default, only the ACCOUNTADMIN role has the privileges needed to execute the queries.

## Finding queries that spill to storage

This query identifies the top 10 worst offending queries in terms of bytes spilled to local and remote storage.

Copy code

```
SELECT query_id, SUBSTR(query_text, 1, 50) partial_query_text, user_name, warehouse_name,
  bytes_spilled_to_local_storage, bytes_spilled_to_remote_storage
FROM  snowflake.account_usage.query_history
WHERE (bytes_spilled_to_local_storage > 0
  OR  bytes_spilled_to_remote_storage > 0 )
  AND start_time::date > dateadd('days', -45, current_date)
ORDER BY bytes_spilled_to_remote_storage, bytes_spilled_to_local_storage DESC
LIMIT 10;
```

## Recommendations

Data spilling to storage can have a negative impact on query performance (especially if the query has to spill to remote storage). To alleviate this, Snowflake recommends:

- Using a larger warehouse (effectively increasing the available memory/local storage space for the operation)
- Processing data in smaller batches.

You can use the [Query Profile](/user-guide/ui-snowsight-activity#label-snowsight-query-profile) to identify which operation nodes are causing data to spill to storage.
For considerations for selecting the appropriate warehouse sizing, please refer to [Warehouse considerations](/user-guide/warehouses-considerations).

For more information about the performance implications of spilling, see the community article
[Performance impact from local and remote disk spilling](https://community.snowflake.com/s/article/Performance-impact-from-local-and-remote-disk-spilling).

Tip

When the query acceleration service (QAS) is enabled, Snowflake writes a small amount of data to remote storage
for each eligible query, even if QAS isn’t used for that query. Therefore, don’t be concerned by a nonzero
value for `bytes_spilled_to_remote_storage` in the QUERY\_HISTORY view when QAS is enabled.
