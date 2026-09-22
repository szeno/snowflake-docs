# Best practices for hybrid tables

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

This topic describes best practices and important considerations when using hybrid tables.
To achieve optimal performance with hybrid tables, follow these best practices in
your deployment. This guide outlines specific configuration, design, and operational practices that maximize
performance for production workloads.

- General best practices:

  - [Query performance in Snowsight versus driver-based access](#label-best-practices-general-snowsight)
  - [Client drivers for hybrid tables](#label-best-practices-general-drivers)
  - [Client configuration and access methods](#label-best-practices-general-clientconfig)
  - [Index design and usage](#label-best-practices-general-indexdesign)
- Best practices for optimizing performance:

  - [Bulk loading data](#label-best-practices-optimization-bulkloading)
  - [Warehouse optimization](#label-best-practices-optimization-warehouse)
  - [Troubleshooting performance issues](#label-best-practices-optimization-troubleshooting)
  - [Stored procedures and hybrid tables](#label-best-practices-optimization-stored-procedures)
  - [Serverless tasks and hybrid tables](#label-best-practices-optimization-tasks)
  - [Foreign keys for join queries](#label-best-practices-foreign-keys)
- Best practices for operating and monitoring hybrid tables:

  - [Caching and warm-up](#label-best-practices-monitoring-cache)
  - [Performance monitoring](#label-best-practices-monitoring-performance)
  - [Monitoring quotas and throttling](#label-best-practices-monitoring-quotas)

## Query performance in Snowsight versus driver-based access

Attention

Performance statistics reported in Snowsight are not indicative of query performance for driver-based workloads.

[Snowsight](/user-guide/ui-snowsight) provides rich access to query plans, data statistics, query history,
and other detailed information that is useful for interactive query prototyping, debugging, investigation, monitoring, and
other activities. Providing that rich interactive experience adds overhead to the Snowflake query engine. As such,
latency for short-running queries executed through Snowsight is not indicative of performance that can be achieved with
programmatic drivers. Queries executed via code-based or driver-based solutions execute with lower latency and variability than
queries executed via Snowsight.

Note

Run a [simple performance test](/user-guide/tables-hybrid-test) to validate performance for
your scenario.

## Client drivers for hybrid tables

In order to access hybrid tables, you will need to use one of the following driver versions:

> | Driver | Minimum Version |
> | --- | --- |
> | Go | 1.6.25 |
> | JDBC | 3.13.31 |
> | .NET | 2.1.2 |
> | Node.js | 1.9.0 |
> | ODBC | 3.0.2 |
> | PHP | 2.0.0 |
> | Python Connector | 3.1.0 |
> | Snowflake CLI | 3.10.0 |
> | SnowSQL | 1.2.28 |
>
> Expand
>
> Show lessSee more
>
> Note
>
> You may not be able to access hybrid tables using an earlier driver version.

For optimal performance with hybrid tables, be sure to use the latest version of your selected driver.

You can also access hybrid tables by using the [Snowflake SQL API](/developer-guide/sql-api/index);
however, this API is not recommended for use cases that require optimal latency.

## Client configuration and access methods

Connection management directly affects performance and scalability. When connecting to databases that contain hybrid tables, consider the
following best practices for achieving good performance.

- Use connection pooling with long-lived connections to eliminate the overhead of repeatedly establishing new connections. Most client
  frameworks that connect to Snowflake provide a connection-pooling mechanism to efficiently manage access.
- Network proximity significantly affects end-to-end latency; therefore, colocate your client software in the same cloud region as the
  Snowflake account.
- Use prepared statements with bound parameters so the query planner will reuse previously created query plans.
- Use the supported programmatic client drivers, not Snowsight, to achieve optimal latency.
  See [Client drivers for hybrid tables](#label-best-practices-general-drivers).

## Index design and usage

Creating and using indexes is a key component to achieving optimal performance for hybrid tables. Consider the
following recommendations:

- Create secondary indexes for frequently used predicates.
- Design composite indexes to match complete query patterns.
- Avoid using multiple indexes with columns in the same ordinal position.
- Understand the cardinality of your data before creating indexes. Indexes built with a single, low-cardinality column have
  limited benefit. See [Estimating the Number of Distinct Values](/user-guide/querying-approximate-cardinality).
- Indexes add write overhead and storage requirements. Be careful to balance read versus write performance for
  applications that require low-latency write operations.

Properly designed indexes significantly improve query performance by providing efficient
data access paths. If possible, choose primary keys for optimal selectivity while minimizing complexity.
In some cases, adding columns with calculated or surrogate key values provides better performance
than complex composite indexes. Secondary indexes dramatically improve performance for frequently accessed columns.

For well-defined queries, using the INCLUDE keyword to add columns to an index when you create the table might further decrease
latency. See [INCLUDE columns](/user-guide/tables-hybrid-index#label-indexes-with-include-columns).

Attention

Be mindful of the indexes you create on a hybrid table; non-selective index scans result in
sub-optimal performance, throttling, and higher cost.

### Queries that qualify for index use

Hybrid table indexes may be accessed when queries use one of the following conditions:

- `<column_reference> {=, >, >=, <, <=} <constant_value>`
- `<column_reference> IN <constant_in_list>`
- `<column_reference> BETWEEN <constant_value> AND <constant_value>`
- `STARTSWITH(<column_reference>, <constant_value>)`
- `<column_reference> LIKE '<constant_prefix>%'`

Note that `ILIKE` patterns don’t qualify for index use and require a full table scan.

Expressions can be chained together using [Logical operators](/sql-reference/operators-logical).

For example:

Copy code

```
CREATE OR REPLACE HYBRID TABLE icecream_orders (
  id NUMBER PRIMARY KEY AUTOINCREMENT START 1 INCREMENT 1 ORDER,
  store_id NUMBER NOT NULL,
  flavor VARCHAR(20) NOT NULL,
  order_ts TIMESTAMP_NTZ,
  num_scoops NUMERIC,
  INDEX idx_icecream_order_store (store_id, order_ts),
  INDEX idx_icecream_timestamp (order_ts)
  );

-- Generate sample data for testing

INSERT INTO icecream_orders (store_id, flavor, order_ts, num_scoops)
  SELECT
    UNIFORM(1, 10, RANDOM()),
    ARRAY_CONSTRUCT('CHOCOLATE', 'VANILLA', 'STRAWBERRY', 'LEMON')[UNIFORM(0, 3, RANDOM())],
    DATEADD(SECOND, UNIFORM(0, 86400, RANDOM()), DATEADD(DAY, UNIFORM(-90, 0, RANDOM()), CURRENT_DATE())),
    UNIFORM(1, 3, RANDOM())
  FROM TABLE(GENERATOR(ROWCOUNT => 10000))
  ;

-- Use idx_icecream_order_store (first column)

  SELECT *
    FROM icecream_orders
    WHERE store_id = 5;

-- Use idx_icecream_order_store (both columns)

  SELECT *
    FROM icecream_orders
    WHERE store_id IN (1,2,3) AND order_ts > DATEADD(DAY, -7, CURRENT_DATE());

-- Use idx_icecream_timestamp

  SELECT *
    FROM icecream_orders
    WHERE order_ts BETWEEN DATEADD(DAY, -2, CURRENT_DATE()) AND DATEADD(DAY, -2, CURRENT_DATE());
```

## Foreign keys for join queries

In general, queries that require joins benefit from the definition of FOREIGN KEY constraints. Although foreign keys aren’t required
for running hybrid table queries, they do assist the optimizer in building the most effective query plan. Foreign keys provide two important functions:

- They establish referential integrity between tables.
- They provide the query planner with metadata for optimization.

A FOREIGN KEY constraint informs the query optimizer that a particular record in a child table points to exactly one record in a parent table. This
behavior is one way in which query predicates are “pushed down” during a join, thereby optimizing storage I/O. The query is executed as a
“one-to-many” join. Joining hybrid tables without foreign keys means that they are executed as “many-to-many” joins, such that additional query predicates
might be necessary to optimize the query.

For more information, see the following topics:

- [REFERENTIAL\_CONSTRAINTS view](/sql-reference/info-schema/referential_constraints)
- [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint)
- [Constraints](/sql-reference/constraints)

## Bulk loading data

You can use several optimizations and best practices for loading data into hybrid tables:

- Use [CREATE TABLE … AS SELECT (also referred to as CTAS)](/sql-reference/sql/create-table#label-ctas-syntax) for creating and immediately loading empty tables.
- Verify use of optimized bulk loading in query profiles.
- Prefer initial data loading as a single bulk transaction.

Hybrid tables provide an optimized bulk loading path that delivers up to 10x faster loading performance than standard
loading methods. When a hybrid table is empty, CTAS, `COPY`, and all variants of `INSERT`, including `INSERT ALL`,
use optimized bulk loading. When a hybrid table already contains data, optimized bulk loading is automatically used
for `COPY` and for all variants of `INSERT`, including `INSERT ALL`, depending on the size and number of rows
being loaded.

You can verify that the optimization is being used by checking the statistics section of the query profile,
where rows will be reported as `Number of rows bulk loaded` rather than `Number of rows inserted`.

Note

CTAS operations do not support FOREIGN KEY constraints. If your table requires foreign keys, either use
COPY or INSERT INTO SELECT instead, or use CTAS to create and load the table without the foreign key and
then add the foreign key with [ALTER TABLE](/sql-reference/sql/alter-table). See
[Add and drop constraints on an existing hybrid table](/sql-reference/sql/create-hybrid-table#label-hybrid-table-online-constraints).

## Warehouse optimization

A warehouse of size X-Small is sufficient for many operational workloads.
In order to achieve higher concurrency and throughput on short-running
operational queries, increase the compute node count by using a
[multi-cluster warehouse](/user-guide/warehouses-multicluster) rather than
increasing compute resources with a larger warehouse.

If your workload has variable throughput patterns, you can enable autoscaling to
reduce consumption when demand is lower. Set the scaling policy to `Standard`
rather than `Economy` for the best performance and efficiency on workloads
that require high throughput or low latency. For more information, see
[Setting the scaling policy for a multi-cluster warehouse](/user-guide/warehouses-multicluster#label-mcw-scaling-policies).

In some cases, isolating workloads in separate
warehouses might be beneficial to enable independent scaling. If you
have a mixed hybrid workload with operational and analytical components, it is
beneficial to separate the operational and analytical components into different
warehouses. If you cannot separate them and must execute them together on the
same warehouse, choose the warehouse size based on the analytical query
latency requirements and choose the multi-cluster node count based on what is
required to support your workload’s throughput.

## Caching and warm-up

The first hybrid table query issued to a newly started warehouse triggers activities such as query planning,
index selection, I/O to load data, caching decisions, and, of course, query execution. The query engine continues
to optimize memory and storage for the query. This time is called the “warm-up” period. Query latency
drops until the engine converges on a steady-state latency.

- Use dedicated warehouses for hybrid table workloads to avoid cache interference.
- Understand that reaching steady-state latency takes from several seconds to 2-3 minutes as the cache warms up.
- Configure auto-suspend and auto-scaling to balance efficiency and cache warmth.

Hybrid tables utilize multiple caching approaches to optimize performance. The plan cache reduces compilation
overhead by storing frequently used query plans. The column store data cache maintains frequently accessed data in
memory, and the metadata cache provides rapid access to table and index information. Hybrid tables do not
use a result cache.

These caches require some time to optimize for your workload patterns. Using dedicated warehouses
for hybrid table workloads prevents cache interference from other workloads. Initial queries
after a cold start experience higher latency until caches are populated.
If your workload has variable throughput patterns, you can enable autoscaling and auto-suspend to
reduce consumption or suspend your warehouse when demand is lower. When your warehouse restarts or
auto-scales to add a new cluster, caches will need to rehydrate. Set the scaling policy to
`Standard` rather than `Economy` for the best performance. See [Multi-cluster warehouses](/user-guide/warehouses-multicluster).

## Stored procedures and hybrid tables

Stored procedures are supported for hybrid tables; however, executing
transactions with [AUTOCOMMIT](/sql-reference/parameters#label-autocommit) enabled or multi-statement transactions
offers better performance and efficiency than calling a stored procedure.

## Serverless tasks and hybrid tables

While serverless tasks are supported, be aware that you may
not experience optimal performance or efficiency for workloads that use hybrid
tables.

## Performance monitoring

The recommended view to use for hybrid table performance monitoring is
the [AGGREGATE\_QUERY\_HISTORY view](/sql-reference/account-usage/aggregate_query_history). This view
contains query execution details aggregated over a short period of time.

For example, to retrieve the average default interval performance over the last 24 hours
for a warehouse serving hybrid table requests:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.AGGREGATE_QUERY_HISTORY
  WHERE warehouse_name = 'HYBRID_TABLES_WAREHOUSE'
  AND query_type = 'SELECT'
  AND interval_start_time >= DATEADD(hour, -24, CURRENT_TIMESTAMP());
```

See the [AGGREGATE\_QUERY\_HISTORY view](/sql-reference/account-usage/aggregate_query_history) for more examples.

## Monitoring quotas and throttling

Hybrid tables implement quota controls at the database level for both hybrid storage and hybrid table requests throughput.
These quotas ensure consistent performance across all users. The default quotas are sufficient for
most initial implementations, but may need adjustment as workloads grow.

- Monitor the hybrid table requests quota by using the [AGGREGATE\_QUERY\_HISTORY view](/sql-reference/account-usage/aggregate_query_history).
- Monitor the hybrid storage quota by using the [STORAGE\_USAGE view](/sql-reference/account-usage/storage_usage).
- High throttling percentages in query profiles indicate you’re approaching throughput limits. When you consistently utilize more
  than 70% of either quota, proactively request an increase through Snowflake Support.

The performance of hybrid tables is subject to throttling even in a case where virtual warehouse compute usage is not high.
To monitor your usage and determine whether a hybrid table is being throttled, see the example in the
[AGGREGATE\_QUERY\_HISTORY view](/sql-reference/account-usage/aggregate_query_history). You can also retrieve the number of throttled hybrid table requests from
the `HYBRID_TABLE_REQUESTS_THROTTLED_COUNT` column.

For more information, see [Quotas and throttling](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-ht-quotas-throttling).

## Troubleshooting performance issues

If you’re not achieving expected performance after implementing these best practices,
Snowflake Support can help analyze and optimize your implementation. When creating a support case,
include the following information to enable rapid resolution:

- Query IDs (UUIDs) for representative queries showing suboptimal performance
- Workload characteristics:

  - Typical query patterns
  - Expected versus actual latency
  - Concurrency requirements
  - Data storage volumes
  - Query response row size
  - Column [cardinality estimates](/user-guide/querying-approximate-cardinality)
- Any recent changes to table schemas, indexes, or workload patterns
- Throttling metrics from query profiles
- Performance differences between cold and warm warehouses

Include both fast and slow examples of similar queries if possible to help identify optimization
opportunities. This comparison helps support teams quickly identify potential configuration or design improvements.
