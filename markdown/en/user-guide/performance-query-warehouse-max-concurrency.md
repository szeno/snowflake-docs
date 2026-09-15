# Limiting concurrently running queries

This topic discusses how a warehouse owner or administrator can reduce the number of queries that are running concurrently on a warehouse
in order to improve the performance of those queries.

Queries running concurrently in a warehouse must share the warehouse’s resources, meaning each query might be granted fewer
resources. You can use the [MAX\_CONCURRENCY\_LEVEL](/sql-reference/parameters#label-max-concurrency-level) parameter to limit the number of concurrent queries
running in a warehouse. Because fewer queries are competing for the warehouse’s resources, a query can potentially be given more resources.

Lowering the concurrency level may boost performance for individual queries, especially large, complex, or multi-statement queries, but
these adjustments should be thoroughly tested to ensure they have the desired effect.

Be aware that lowering the MAX\_CONCURRENCY\_LEVEL for a warehouse can lead to more queries being placed in a queue, which has a performance
implication for those queries. Other strategies such as using a dedicated warehouse or using the
[Query Acceleration Service](/user-guide/performance-query-warehouse-qas) can boost the performance of a large or complex query without impacting
the rest of the workload.

For more information, see [MAX\_CONCURRENCY\_LEVEL](/sql-reference/parameters#label-max-concurrency-level).

Note

> Adjusting the [STATEMENT\_QUEUED\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-queued-timeout-in-seconds) parameter can cancel queries rather than let them remain in the queue for an extended period of time.

## How to lower MAX\_CONCURRENCY\_LEVEL

The default maximum concurrency level is 8. To lower the level, use the [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) command to specify a
lower number. For example:

> Copy code
>
> ```
> ALTER WAREHOUSE my_wh SET MAX_CONCURRENCY_LEVEL = 4;
> ```
