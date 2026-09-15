# 2022 Performance Improvements

Important

Performance improvements often target specific query patterns or workloads. These improvements might or might not have a material impact
on a specific workload.

The following performance improvements were introduced in 2022:

| Released | Description | Impact |
| --- | --- | --- |
| November 2022 | Improved performance and resilience of Snowflake applications and content. | Improved response times and availability for Snowsight pages. |
| November 2022 | Ability to use scalar [Vectorized Python UDFs](/developer-guide/udf/python/udf-python-batch) in Snowpark. | Performance improvements for Python code that operates efficiently on batches of rows. Also requires less transformation logic when using Pandas DataFrames and arrays. |
| November 2022 | Improvements for metadata queries. | Improved query execution time for small/metadata queries. |
| October 2022 | Ability to enable [Search Optimization](/user-guide/search-optimization-service) for [specific columns](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-adding). (Preview) | Point lookup queries that act upon a column can be improved without incurring the expense of enabling Search Optimization for the entire table. |
| October 2022 | Support for [substring operations](/user-guide/search-optimization/substring-queries#label-search-optimization-service-queries-wildcard-regexp) when using Search Optimization. (Preview) | Improves the performance of point lookup queries that use substring operations such as LIKE and ENDSWITH. |
| October 2022 | Support for [VARIANT data](/user-guide/search-optimization/semi-structured-queries#label-search-optimization-service-queries-variant) when using Search Optimization. (Preview) | Improves the performance of point lookup queries that act upon VARIANT data (such as JSON). |
| October 2022 | Support for [geospatial functions with GEOGRAPHY objects](/user-guide/search-optimization/geospatial-queries#label-search-optimization-service-queries-geo) when using Search Optimization. (Preview) | Improves the performance of point lookup queries that use a geospatial function in a predicate. |
| October 2022 | Improvements for Collation and BINARY columns. | Improved pruning for collations and BINARY columns, which means fewer [micro-partitions](/user-guide/tables-clustering-micropartitions) must be scanned to return results. |
| October 2022 | Improvements for hash table joins. | Improved query performance by reducing memory I/O latency in hash table equality checks. |
| October 2022 | Improvements for DateTrunc range derivations. | Improved execution time for queries that use DateTrunc range derivation when [TIMESTAMP-TZ](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations) data is a constant. |
| August 2022 | Improvements related to Data Governance features. | More responsive Data Governance UI pages in Snowsight as well as improved query latency for [tag-based masking policies](/user-guide/tag-based-masking-policies). |
| August 2022 | Improvements for [window functions](/sql-reference/functions-window). | Improved rule-based optimization as well as improved query execution for outer join and filter pushdown in window functions. |
| August 2022 | Scheduling improvements for high-concurrency workloads. | Improved query scheduling for high concurrency and lower latency workloads. |
| July 2022 | Improved query performance using Join Elimination. | Optimized query performance through the automatic elimination of unnecessary joins, which are identified by automatically evaluating query logic. |

Expand

Show lessSee more
