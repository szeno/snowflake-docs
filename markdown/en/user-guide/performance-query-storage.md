# Optimizing storage for performance

This topic discusses storage optimizations that can improve query performance, such as storing similar data together, creating optimized
data structures, and defining specialized data sets. Snowflake provides three of these storage strategies: automatic clustering, search
optimization, and materialized views.

In general, these storage strategies do not substantially improve the performance of queries that already execute in a second or faster.

The strategies discussed in this topic are just one way to boost the performance of queries. For strategies related to the computing
resources used to execute a query, refer to [Optimizing warehouses for performance](/user-guide/performance-query-warehouse).

## Introduction to storage strategies

### Automatic Clustering

Snowflake stores a table’s data in [micro-partitions](/user-guide/tables-clustering-micropartitions#label-what-are-micropartitions). Among these micro-partitions, Snowflake
organizes (i.e. clusters) data based on dimensions of the data. If a query filters, joins, or aggregates along those dimensions, fewer
micro-partitions must be scanned to return results, which speeds up the query considerably.

You can set a [cluster key](/user-guide/tables-clustering-keys#label-clustering-keys) to change the default organization of the micro-partitions so data is clustered
around specific dimensions (i.e. columns). Choosing a cluster key improves the performance of queries that filter, join, or aggregate by
the columns defined in the cluster key.

Snowflake enables Automatic Clustering to maintain the clustering of the table as soon as you define a cluster key. Once enabled, Automatic
Clustering updates micro-partitions as new data is added to the table. [Learn More](/user-guide/tables-auto-reclustering)

### Search Optimization Service

The Search Optimization Service improves the performance of point lookup queries (i.e. “needle in a haystack searches”) that return a
small number of rows from a table using highly selective filters. The Search Optimization Service is ideal when it is critical to have
low-latency point lookup queries (e.g. investigative log searches, threat or anomaly detection, and critical dashboards with selective
filters).

The Search Optimization Service reduces the latency of point lookup queries by building a persistent data structure that is optimized for
a particular type of search.

You can enable the Search Optimization Service for an entire table or for specific columns. As long as they are selective enough,
[equality searches](/user-guide/search-optimization/point-lookup-queries#label-search-optimization-service-queries-equality-in),
[substring searches](/user-guide/search-optimization/substring-queries#label-search-optimization-service-queries-wildcard-regexp), and
[geo searches](/user-guide/search-optimization/geospatial-queries#label-search-optimization-service-queries-geo) against those columns can be sped up significantly.

The Search Optimization Service supports both structured and semi-structured data (see [supported data types](/user-guide/search-optimization/queries-that-benefit#label-search-optimization-service-when-should-you-use-search-paths)).

The Search Optimization Service requires Snowflake Enterprise Edition or higher. [Learn More](/user-guide/search-optimization-service)

### Materialized views

A materialized view is a pre-computed data set derived from a SELECT statement that is stored for later use. Because the data is
pre-computed, querying a materialized view is faster than executing a query against the base table on which the view is defined. For
example, if you specify `SELECT SUM(column1)` when creating the materialized view, then a query that returns `SUM(column1)` from the
view executes faster because `column1` has already been aggregated.

Materialized views are designed to improve query performance for workloads composed of common, repeated query patterns that return a small
number of rows and/or columns relative to the base table.

A materialized view cannot be based on more than one table.

Materialized views require Snowflake Enterprise Edition or higher. [Learn More](/user-guide/views-materialized)

## Choosing an optimization strategy

Different types of queries benefit from different storage strategies. You can use the following sections to discover which strategy best
fits a workload.

Automatic Clustering is the broadest option that can benefit a range of queries that access the same columns of a table. An administrator
often picks the most important queries based on frequency and latency requirements, and then chooses a cluster key that maximizes the
performance of those queries. Automatic Clustering makes sense when many queries filter, join, or aggregate the same few columns.

The Search Optimization Service and materialized views have a narrower scope. When specific queries access a well-defined subset of a
table’s data, the administrator can use the characteristics of the query to decide whether using the Search Optimization Service or a
materialized view might improve performance. For example, administrators could identify important point lookup queries and implement the
Search Optimization Service for a table or column. Likewise, the administrator could optimize specific query patterns by creating a
materialized view.

You can implement more than one of these strategies for a table, and an individual query with multiple filters could potentially benefit
from both Automatic Clustering and the Search Optimization Service. However, enabling the Search Optimization Service or creating a
materialized view on a clustered table can be more expensive. To learn why this increases compute costs, refer
to [Ongoing Costs](#label-perf-query-storage-ongoing-cost) (in this topic).

If more than one strategy could potentially improve the performance of a particular query, you might want to start with Automatic
Clustering or the Search Optimization Service because other queries with similar access patterns could also be improved.

### Differentiating considerations

The following is not an exhaustive comparison of the storage strategies, but rather provides the most important considerations when
differentiating between them.

Automatic Clustering:
:   - Biggest performance boost comes from a WHERE clause that filters on a column of the cluster key, but it can also improve the performance
      of other clauses and functions that act upon that same column (e.g. joins and aggregations).
    - Ideal for range queries or queries with an inequality filter. Also improves an equality filter, but the Search Optimization Service is
      usually faster for point lookup queries.
    - Available in Standard Edition of Snowflake.
    - There can be only one cluster key. [1] If different queries against a table act upon different columns, consider using the Search
      Optimization Service or a materialized view instead.

Search Optimization Service:
:   - Improves point lookup queries that return *a small number of rows*. If the query returns more than a few records, consider Automatic
      Clustering instead.
    - Includes support for point lookup queries that:
      - Match substrings or regular expressions using predicates such as LIKE and RLIKE.
      - Search for specific fields in VARIANT, ARRAY, or OBJECT columns.
      - Use geospatial functions with GEOGRAPHY values.

Materialized view:
:   - Improves intensive and frequent calculations such as aggregation and analyzing semi-structured data (not just filtering).
    - Usually focused on a specific query/subquery calculation.
    - Improves queries against [external tables](/user-guide/tables-external-intro).

[1] If there is an important reason to define multiple cluster keys, you could create multiple materialized views, each with its own
cluster key.

### Prototypical queries

The following examples are intended to highlight which type of query typically runs faster with a particular storage strategy.

Prototypical Query for Clustering
:   Automatic Clustering provides a performance boost for *range queries* with large table scans. For example, the following query will
    execute faster if the `shipdate` column is the table’s cluster key because the `WHERE` clause scans a lot of data.

    Copy code

    ```
    SELECT
      SUM(quantity) AS sum_qty,
      SUM(extendedprice) AS sum_base_price,
      AVG(quantity) AS avg_qty,
      AVG(extendedprice) AS avg_price,
      COUNT(*) AS count_order
    FROM lineitem
    WHERE shipdate >= DATEADD(day, -90, to_date('2023-01-01'));
    ```

    For an additional example of a query that might run faster if the table was clustered, refer to [Benefits of Defining Clustering Keys (for Very Large Tables)](/user-guide/tables-clustering-keys#label-clustering-benefits).

Prototypical Query for Search Optimization
:   The Search Optimization Service can provide a performance boost for *point lookup queries* that scan a large table to return a small
    subset of records. For example, the following query will execute faster with the Search Optimization Service if the `sender_ip` column
    has a large number of distinct values.

    Copy code

    ```
    SELECT error_message, receiver_ip
    FROM logs
    WHERE sender_ip IN ('198.2.2.1', '198.2.2.2');
    ```

    To review other queries that might run faster with the Search Optimization Service, refer to the following examples:

    - [Equality operators](/user-guide/search-optimization-service#label-search-optimization-service-examples)
    - [Geospatial functions](/user-guide/search-optimization/geospatial-queries#label-search-optimization-service-geo-examples)
    - [Substring and Regular Expressions](/user-guide/search-optimization/substring-queries#label-search-optimization-service-queries-wildcard-regexp)
    - [Fields in VARIANT Columns](/user-guide/search-optimization/semi-structured-queries#label-search-optimization-service-queries-variant)

Prototypical Query for Materialized View
:   A materialized view can provide a performance boost for queries that access a small subset of data using expensive operations like
    aggregation. As an example, suppose that an administrator aggregated the `totalprice` column when creating a materialized view
    `mv_view1`. The following query against the materialized view will execute faster than it would against the base table.

    Copy code

    ```
    SELECT
      orderdate,
      SUM(totalprice)
    FROM mv_view1
    GROUP BY 1;
    ```

    For more use cases where materialized views can speed up queries, refer to [Examples of Use Cases For Materialized Views](/user-guide/views-materialized#label-materialized-views-use-cases).

## Implementation and cost considerations

This section discusses cost considerations of using a storage strategy to improve query performance, along with implementation
considerations as you balance cost and performance.

### Initial investment

Implementing a storage strategy can require a bigger time commitment and upfront financial investment than other types of performance
optimizations (e.g. re-writing SQL statements or [optimizing the warehouse](/user-guide/performance-query-warehouse) running the query), but the
performance improvements can be significant.

Snowflake uses [serverless compute resources](/user-guide/cost-understanding-compute#label-serverless-credit-usage) to implement each storage strategy, which consumes
credits before you can test how well the optimization improves performance. In addition, it can take Snowflake a significant amount of
time to fully implement Automatic Clustering and the Search Optimization Service (e.g. a week for a very large table).

The Search Optimization Service and materialized views also require the Enterprise Edition or higher, which increases the price of a credit.

### Ongoing cost

Storage strategies incur both compute and storage costs.

Compute Costs
:   Snowflake uses serverless compute resources to maintain storage optimizations as new data is added to a table. The more changes to a
    table, the higher the maintenance costs. If a table is constantly updated, the cost of maintaining a storage optimization might be
    prohibitive.

    The cost of maintaining materialized views or the Search Optimization Service can be significant when Automatic Clustering is enabled
    for the underlying table. With Automatic Clustering, Snowflake is constantly reclustering its micro-partitions around the dimensions of
    the cluster key. Every time the base table is reclustered, Snowflake must use serverless compute resources to update the storage used by
    materialized views and the Search Optimization Service. As a result, Automatic Clustering activities on the base table can trigger
    maintenance costs for materialized views and the Search Optimization Service beyond the cost of the DML commands on the base table.

Storage Costs
:   Automatic Clustering
    :   Unlike the Search Optimization Service and materialized views, Automatic Clustering reorganizes existing data rather than creating
        additional storage. However, reclustering can incur additional storage costs if it increases the size of
        [Fail-safe](/user-guide/data-failsafe) storage. For details, refer to [Credit and Storage Impact of Reclustering](/user-guide/tables-clustering-keys#label-clustering-keys-reclustering-credit-storage).

    Search Optimization / Materialized Views
    :   Materialized views and the Search Optimization Service incur the cost of additional storage, which is billed at the standard rate.

### Estimating costs

Automatic Clustering
:   You can run the [SYSTEM$ESTIMATE\_AUTOMATIC\_CLUSTERING\_COSTS](/sql-reference/functions/system_estimate_automatic_clustering_costs) function to help estimate the cost of enabling Automatic Clustering for a table and maintaining the table in a well-clustered state. This estimate is based on the change history of the table. Actual costs can vary significantly, especially if DML patterns change after enabling Automatic Clustering.

Search Optimization Service
:   You can run the [SYSTEM$ESTIMATE\_SEARCH\_OPTIMIZATION\_COSTS](/sql-reference/functions/system_estimate_search_optimization_costs) function to help estimate the cost of adding the
    Search Optimization Service to a column or entire table. The estimated costs are proportional to the number of columns that will be
    enabled and how much the table has recently changed.

### Implementation strategy

Because the compute costs and storage costs of a storage strategy can be significant, you might want to start small and carefully track the
initial and ongoing costs before committing to a more extensive implementation. For example, you might choose a cluster key for just one or
two tables, and then assess the cost before choosing a key for other tables.

When tracking the ongoing cost associated with a storage strategy, remember that virtual warehouses consume credits only during the time
they are running a query, so a faster query costs less to run. Snowflake recommends carefully reporting on the cost of running a query
before the storage optimization and comparing it to the cost of running the same query after the storage optimization so it can be factored
into the cost assessment.
