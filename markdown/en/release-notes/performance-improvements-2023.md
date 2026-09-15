# 2023 Performance Improvements

Important

Performance improvements often target specific query patterns or workloads. These improvements might or might not have a material impact
on a specific workload.

The following performance improvements were introduced in 2023:

| Released | Description | Impact |
| --- | --- | --- |
| December 2024 | Improved column replication. | Reduces the time spent in the SECONDARY\_DOWNLOADING\_METADATA phase of a refresh operation for table columns. Improvements scale linearly with the number of columns replicated. |
| November 2023 | Improved execution times for some SHOW commands. | Reduces the execution time for the [SHOW TABLES](/sql-reference/sql/show-tables), [SHOW SCHEMAS](/sql-reference/sql/show-schemas), and [SHOW DATABASES](/sql-reference/sql/show-databases) commands. Improvements are most significant for queries that return large result sets. |
| November 2023 | Search Optimization: Support for [substring search in semi-structured data](/user-guide/search-optimization/semi-structured-queries#label-search-optimization-service-variant-substring). (General Availability) | Improves the performance of point lookup queries that use substring and regular expression functions against semi-structured data, including ARRAY, OBJECT, and VARIANT types. Previously, only equality searches on such columns could be optimized. |
| October 2023 | Reduced maintenance costs for materialized views. | Reduces materialized view maintenance credits by improving the utilization of service resources. |
| October 2023 | Improved compile times for SQL expressions. | Reduces the compilation time of queries that contain many SQL expressions. |
| September 2023 | Improved compile times. | Reduces compilation times by skipping optimizations that will not result in performance improvements. |
| August 2023 | Ability to use a query hash to identify patterns and trends in query execution. | Helps to [monitor and analyze recurring queries](/user-guide/query-hash) by including a query hash of each query in ACCOUNT\_USAGE views and INFORMATION\_SCHEMA table functions. Can be used to determine the effects of performance improvements like choosing a new cluster key. |
| August 2023 | Improved execution times for non-clustered tables. | Reduces execution time for SELECT and DML operations against non-clustered tables with micro-partitions that are smaller than average. |
| August 2023 | Ability to call the [GET\_QUERY\_OPERATOR\_STATS](/sql-reference/functions/get_query_operator_stats) function to obtain query profile statistics. (General Availability) | Helps to programmatically debug queries and gain insights into query performance. |
| August 2023 | Improved execution times for joins on wide build-side rows. | Reduces execution time and improves memory management for queries matching wide rows on the build side of a join (for example, rows that include columns with long strings). |
| July 2023 | Improved compile times for materialized views. | Reduces compilation times for materialized views based on tables that have 100s or 1000s of micro-partitions. |
| July 2023 | Ability to use [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview). (General Availability) | Enables low-latency streaming data pipelines to support writing data rows directly into Snowflake. |
| July 2023 | Improved selectivity and cardinality estimation. | Uses improved plan selection to reduce execution time for queries with low selectivity. |
| July 2023 | Search Optimization Update: Support for [substring search in VARIANT types](/user-guide/search-optimization/semi-structured-queries#label-search-optimization-service-variant-substring). (Preview) | Improves the performance of point lookup queries that use substring and regular expression functions against semi-structured data, including ARRAY, OBJECT, and VARIANT types. |
| July 2023 | Improved compile times for simple queries and DML statements. | Reduces compilation times and improves memory management for simple DML statements and single-table queries with simple equality or range predicates. |
| June 2023 | Improved execution times for SELECT statements with LIMIT and ORDER BY clauses. | Reduces execution time of some queries with long-running SELECT statements containing both LIMIT and ORDER BY clauses. |
| June 2023 | Improved execution times against [secure views](/user-guide/views-secure). | Uses predicate pushdown to reduce execution time for queries against secure views. |
| May 2023 | Improved compile times for queries with numerous extraction expressions. | Reduces compilation times for queries with many extraction expressions (such as those used for processing JSON). |
| May 2023 | Improved compile times for queries with numerous subqueries. | Reduces compilation time for queries with 100+ subqueries. |
| April 2023 | Search Optimization Update: Ability to enable Search Optimization for [specific columns](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-adding). (General Availability) | Point lookup queries that act upon a column can be improved without incurring the expense of enabling Search Optimization for the entire table. |
| April 2023 | Search Optimization Update: Support for [substring operations](/user-guide/search-optimization/substring-queries#label-search-optimization-service-queries-wildcard-regexp). (General Availability) | Improves the performance of point lookup queries that use substring operations such as LIKE and ENDSWITH. |
| April 2023 | Search Optimization Update: Support for [VARIANT data](/user-guide/search-optimization/semi-structured-queries#label-search-optimization-service-queries-variant). (General Availability) | Improves the performance of point lookup queries that act upon VARIANT data (such as JSON). |
| April 2023 | Search Optimization Update: Support for [geospatial functions with GEOGRAPHY objects](/user-guide/search-optimization/geospatial-queries#label-search-optimization-service-queries-geo). (General Availability) | Improves the performance of point lookup queries that use a geospatial function in a predicate. |
| April 2023 | Ability to use the [query acceleration service](/user-guide/query-acceleration-service) to speed up queries against tables that have [Search Optimization](/user-guide/search-optimization-service) enabled. (General Availability) | Additional compute power provided by the query acceleration service can be combined with performance boost provided by search optimization. |
| March 2023 | Ability to use [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview). (Preview) | Enables low-latency streaming data pipelines to support writing data rows directly into Snowflake. |
| February 2023 | Ability to use the [query acceleration service](/user-guide/query-acceleration-service). (General Availability) | Improves overall warehouse performance by reducing the impact of outlier queries. |
| February 2023 | Ability to call the [GET\_QUERY\_OPERATOR\_STATS](/sql-reference/functions/get_query_operator_stats) function to obtain programmatic Query Profile statistics. (Preview) | Helps debug queries and gain insights into query performance. |
| February 2023 | Ability to use [memory-optimized warehouses](/user-guide/warehouses-snowpark-optimized). | Memory-intensive queries can be run on Snowpark-optimized warehouses that provide 16x more memory per node and 10x the local cache compared with standard warehouses. |

Expand

Show lessSee more
