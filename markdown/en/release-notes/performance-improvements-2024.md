# 2024 Performance Improvements

Important

Performance improvements often target specific query patterns or workloads. These improvements might or might not have a material impact
on a specific workload.

The following performance improvements were introduced in 2024:

| Released | Description | Impact |
| --- | --- | --- |
| December 2024 | Improved sharing of common or similar parts of a query. | Reduces query execution time for queries with multiple WITH clauses. |
| December 2024 | Improved scaling of document pre-processing and inference in Document AI. | Decreases processing time of documents. |
| November 2024 | Top-K pruning for queries that contain aggregate functions. | Expands [top-K pruning](/user-guide/querying-top-k-pruning-optimization) to include queries that contain [aggregate functions](/sql-reference/functions-aggregation). |
| October 2024 | Improved performance for queries that have equivalent (or similar) subqueries or sub-expressions. | Reduces query execution time by eliminating duplicate parts of a query plan. |
| October 2024 | Improved handling of skew. | Reduces query execution time by automatically detecting and resolving skew in the build side of joins. |
| October 2024 | Search Optimization Update: Support for [join queries](/user-guide/search-optimization/join-queries). (General Availability) | Improves the performance of join queries that have a small number of distinct values on the build side of the join. |
| October 2024 | Improved metadata replication. | Reduces the time spent in the SECONDARY\_UPLOADING\_INVENTORY, PRIMARY\_UPLOADING\_METADATA, and SECONDARY\_DOWNLOADING\_METADATA phases of a replication refresh by optimizing serverless compute allocation. This improvement targets refreshes with larger metadata sizes. |
| September 2024 | Improved cloning operations through parallelization. | Reduces the time it takes to clone objects, especially for databases and schemas with extensive metadata. |
| September 2024 | Improved replication refreshes through parallelization. | Reduces the overall refresh time when replicating large volumes of data. |
| August 2024 | Improved performance for LIMIT queries. | Reduces compilation and execution time for queries that use a [LIMIT](/sql-reference/constructs/limit) clause to return `n` rows from a table. This optimization shrinks the partitions that are scanned to cover only the first `n` rows. |
| July 2024 | Improved table column synchronization for replication. | Reduces the time spent in the SECONDARY\_DOWNLOADING\_METADATA phase of a refresh operation. |
| July 2024 | Improved warehouse utilization for queries that scan only a small amount of micro-partitions when compared to the compute resources that are available to the virtual warehouse. | Faster execution for queries with expensive operations when scanning data from a small number of micro-partitions, which is common in BI and dashboard use cases. |
| July 2024 | Improved query processing that:   - Pushes down LIMIT clauses into aggregation nodes that do not contain any aggregations besides the ANY\_VALUE function. - Eliminates redundant grouping keys when PRIMARY KEY or UNIQUE constraints are enforced by validation, or when the RELY constraint   property is used. | Faster execution for some queries with LIMIT clauses and GROUP BY statements. |
| June 2024 | Improved single instruction, multiple data (SIMD) processing. | - Reduces query execution time and improves scan performance for queries that access columns that contain NULL values. - Provides better scan performance by decoding numbers more efficiently when reading data from remote storage. |
| May 2024 | Improved efficiency of [Automatic Clustering](/user-guide/tables-auto-reclustering). | Reduces the cost of Automatic Clustering because it works more efficiently. |
| May 2024 | Improved object replication. | Reduces the time spent in the SECONDARY\_UPLOADING\_INVENTORY and SECONDARY\_DOWNLOADING\_METADATA phases of a refresh operation by optimizing the synchronization of some objects and the authorization mechanism for replication operations. |
| May 2024 | Reduced the latency for loading most Parquet files by up to 50% when the file format option, [USE\_VECTORIZED\_SCANNER](/sql-reference/sql/copy-into-table#label-use-vectorized-scanner), is set to `TRUE`. | The vectorized scanner is well suited for the columnar format of a [Parquet](https://parquet.apache.org/docs/file-format/) file and reduces the ingestion latency by downloading only relevant sections of the Parquet file into memory, such as the subset of selected columns. |
| May 2024 | Improved evaluation of aggregations so they are made at more intermediate join trees. | Reduces query execution time for complex queries with aggregations by reducing the amount of data that needs to be processed at the earliest point possible. |
| May 2024 | Improved query execution times for queries that spend a significant amount of time communicating across virtual warehouse nodes. | Increases throughput between compute resources in a warehouse. Each warehouse is a cluster of compute resources. |
| May 2024 | Improved top-k pruning for LIMIT and ORDER BY queries. | Reduces execution time for top-k queries due to fewer scanned files and file header reads. Expands existing top-k improvements to include STRING/BINARY support in ORDER BY columns. Further increases pruning efficiency by sorting the scan set in order of largest/smallest files with respect to the value domain. |
| May 2024 | Improved join order decisions by calculating selectivity estimates with more granularity. | Reduces compilation time and query execution time by calculating selectivity estimates at the micro-partition level. |
| May 2024 | Faster loading time for Python. | Improves performance for Streamlit in Snowflake apps (including Streamlit apps within a Snowflake Native App), Python worksheets, Python UDFs, and stored procedures in Python. |
| April 2024 | Reduced lock/mutex contention. | Reduces query execution times by improving scan performance in a variety of scenarios such as highly concurrent queries running on a warehouse. |
| April 2024 | Improved broadcast join decisions. | Reduces query execution time and improves memory management by optimizing broadcast joins in scenarios like right-deep join trees. |
| April 2024 | Faster query results in Snowsight. | Reduces the time it takes for query results to appear when run in Snowsight. Improvements are most noticeable for queries that return result sets larger than 10,000 rows. |
| March 2024 | Improved metadata replication. | Reduces the time spent in the PRIMARY\_UPLOADING\_METADATA, SECONDARY\_DOWNLOADING\_METADATA, and SECONDARY\_UPLOADING\_INVENTORY phases for metadata. |
| March 2024 | Improved query performance as a result of more accurately calculating selectivity estimates in order to optimize the order of joins. | Reduces execution time when there are mismatches between partition metadata and actual cardinality from join filters. |
| March 2024 | Improved performance for loading JSON files. | Results in lower ingestion latency of up to 25% for many JSON loading scenarios. |
| February 2024 | Improved object replication. | Reduces the time spent in the PRIMARY\_UPLOADING\_METADATA, SECONDARY\_DOWNLOADING\_METADATA, and SECONDARY\_UPLOADING\_INVENTORY phases of a refresh operation by optimizing portions of the snapshot operation and the way some objects are added to the replication inventory. |
| February 2024 | Support for the `upper` and `lower` collation specifications added to some functions. | Ability to set the `upper` and `lower` collation specifications for some functions. The `upper` and `lower` collation specifications perform better than the `ci` specification for some use cases. The `upper` and `lower` collation specifications are now supported for the following functions: [CHARINDEX](/sql-reference/functions/charindex), [CONTAINS](/sql-reference/functions/contains), [ENDSWITH](/sql-reference/functions/endswith), [POSITION](/sql-reference/functions/position), [SPLIT](/sql-reference/functions/split), [SPLIT\_PART](/sql-reference/functions/split_part), and [STARTSWITH](/sql-reference/functions/startswith). For more information, see [Differences between `ci` and `upper` / `lower`](/sql-reference/collation#label-collation-upper-lower-difference). |
| January 2024 | Improved execution time for LIMIT 0 queries. | Reduces execution time for queries that use a count of `0` with [LIMIT](/sql-reference/constructs/limit), which is often used by applications to return column headings and data types for query results. |
| January 2024 | General Availability of [larger warehouses](/user-guide/warehouses-overview) (5X-LARGE and 6X-LARGE) in Microsoft Azure regions, excluding Azure Government regions. | Ability to use larger compute resources for memory-intensive queries compared to smaller warehouses. |

Expand

Show lessSee more
