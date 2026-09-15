# Optimizing query performance

You can optimize Snowflake query performance in the following ways:

- Search optimization service
- Query acceleration
- Creating one or more materialized views (clustered or unclustered)
- Clustering a table

Each of these optimization methods has different advantages, as shown in the following table:

| Feature | Supported query types | Notes |
| --- | --- | --- |
| [Search optimization service](/user-guide/search-optimization-service) | - [Equality searches](/user-guide/search-optimization/point-lookup-queries#label-search-optimization-service-queries-equality-in). - [Substring and regular expression searches](/user-guide/search-optimization/substring-queries#label-search-optimization-service-queries-wildcard-regexp). - [Character data (text) and IP address searches](/user-guide/search-optimization/text-queries). - Searches of [elements in VARIANT](/user-guide/search-optimization/semi-structured-queries#label-search-optimization-service-queries-variant). - Searches of [elements in structured types](/user-guide/search-optimization/structured-queries#label-search-optimization-service-queries-structured). - Searches of [GEOGRAPHY columns using geospatial functions](/user-guide/search-optimization/geospatial-queries#label-search-optimization-service-queries-geo).   The search optimization service can improve the performance of these types of searches for the [supported data types](/user-guide/search-optimization/queries-that-benefit#label-search-optimization-service-supported-data-types). |  |
| [Query acceleration service](/user-guide/query-acceleration-service) | Queries with filters or aggregation. If the query includes LIMIT, the query must also include ORDER BY. The filters must be highly selective, and the ORDER BY clause must have a low cardinality.  Query acceleration works well with ad-hoc analytics, queries with unpredictable data volume, and queries with large scans and selective filters. | Query acceleration and search optimization are complementary. Both can accelerate the same query. See [Compatibility with query acceleration](/user-guide/performance-query-options#label-sos-with-query-acceleration). |
| [Materialized views](/user-guide/views-materialized) | - Equality searches. - Range searches. - Sort operations. | You can also use materialized views to define different clustering keys on the same source table, or a subset of that table, or to store flattened JSON or VARIANT data so it only needs to be flattened once.  Materialized views improve performance only for the subset of rows and columns included in the materialized view. |
| [Clustering the table](/user-guide/tables-clustering-keys) | - Equality searches. - Range searches. | A table can be clustered only on a single key, which can contain one or more columns or expressions. |

Expand

Show lessSee more

The following table shows which of these optimizations have storage or compute costs:

| Optimization | Storage cost | Compute cost |
| --- | --- | --- |
| Search optimization service | ✔ | ✔ |
| Query acceleration service |  | ✔ |
| Materialized view | ✔ | ✔ |
| Clustering the table | ✔ [[1]](#footnote-1) | ✔ |

Expand

Show lessSee more

[1]
The process of reclustering can increase the size of [fail-safe](/user-guide/data-failsafe) storage
because of the rewriting of existing partitions into new partitions. Reclustering doesn’t introduce any new rows.
For more information, see [Credit and Storage Impact of Reclustering](/user-guide/tables-clustering-keys#label-clustering-keys-reclustering-credit-storage).

## Compatibility with query acceleration

Search optimization and [query acceleration](/user-guide/query-acceleration-service) can work together to
optimize query performance. First, search optimization can prune the [micro-partitions](/user-guide/tables-clustering-micropartitions#label-what-are-micropartitions) that aren’t needed for a query. Then, for [eligible queries](/user-guide/query-acceleration-service#label-identifying-queries-warehouses-for-qas), query acceleration can offload portions of the rest of the work to
shared compute resources that the service provides.

The performance of queries that are accelerated by both services varies depending on the workload and available resources.
