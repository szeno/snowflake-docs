# Optimizing warehouses for performance

In the Snowflake architecture, virtual warehouses provide the computing power that is required to execute queries. Fine-tuning the compute
resources provided by a warehouse can improve the performance of a query or set of queries.

A warehouse owner or administrator can try the following warehouse-related strategies as they attempt to improve the performance of one or
more queries. As they adjust a warehouse based on one of these strategies, they can test the change by re-running the query and
[checking its execution time](/user-guide/performance-query-exploring#label-perf-query-snowsight).

Warehouse-related strategies are just one way to boost the performance of queries. For performance strategies involving how data
is stored, refer to [Optimizing storage for performance](/user-guide/performance-query-storage).

| Strategy | Description |
| --- | --- |
| [Reduce queues](/user-guide/performance-query-warehouse-queue) | Minimizing queuing can improve performance because the time between submitting a query and getting its results is longer when the query must wait in a queue before starting. |
| [Resolve memory spillage](/user-guide/performance-query-warehouse-memory) | Adjusting the available memory of a warehouse can improve performance because a query runs substantially slower when a warehouse runs out of memory, which results in bytes “spilling” onto storage. |
| [Increase warehouse size](/user-guide/performance-query-warehouse-size) | The larger a warehouse, the more compute resources are available to execute a query or set of queries. |
| [Try query acceleration](/user-guide/performance-query-warehouse-qas) | The query acceleration service offloads portions of query processing to serverless compute resources, which speeds up the processing of a query while reducing its demand on the warehouse’s compute resources. |
| [Optimize the warehouse cache](/user-guide/performance-query-warehouse-cache) | Query performance improves if a query can read from the warehouse’s cache instead of from tables. |
| [Limit concurrently running queries](/user-guide/performance-query-warehouse-max-concurrency) | Limiting the number of queries that are running concurrently in a warehouse can improve performance because there are fewer queries putting demands on the warehouse’s resources. |

Expand

Show lessSee more

Tip

Optimizing a warehouse for query performance is more straightforward when the warehouse runs similar workloads. For example, if a
warehouse runs significantly different queries, the cost of a performance enhancement might be wasted on a query that does not benefit
from the optimization.

For general guidelines about distributing workloads to your organization’s warehouses, see the Analyzing Your Workloads section of
the [Managing Snowflake’s Compute Resources](https://www.snowflake.com/blog/managing-snowflakes-compute-resources/) (Snowflake blog).
