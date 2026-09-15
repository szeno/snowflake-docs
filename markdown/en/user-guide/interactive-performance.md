# Performance for Snowflake interactive analytics

## Performance considerations

- [Query best practices for interactive warehouses](#query-best-practices-for-interactive-warehouses)
- [Data layout best practices](#data-layout-best-practices)
- [Choosing a size for an interactive warehouse](#choosing-a-size-for-an-interactive-warehouse)
- [Performance optimization for interactive analytics](#performance-optimization-for-interactive-analytics)
- [Using search optimization for point lookups](#using-search-optimization-for-point-lookups)

The following sections explain how to solve performance issues that you might encounter due to
the special characteristics of interactive warehouses and the workloads they’re best suited for.

### Query best practices for interactive warehouses

Interactive warehouses are optimized for queries with **selective workloads**. This means queries
with good selectivity see substantially more improvements on performance than other query types.

#### Scenario 1: Narrow projection versus full-table projection

This query is likely to see **more benefit**:

Copy code

```
SELECT col1, col4, AVG(col_x)
  FROM my_table
  GROUP BY col1, col4;
```

This query is highly selective because it only requires a few columns. Snowflake can optimize
loading only columns required for this one query.

This query is likely to see **limited benefit**:

Copy code

```
SELECT * FROM my_table;
```

This query processes all columns. Although the query is simple, Snowflake must process a large amount of data, which might exceed the size of the cache. Even if the content of the table can fit in the cache, causing other queries to load new data into the cache at runtime, leading to lower concurrency.

#### Scenario 2: Targeted filters versus broad time-range filters

This query is likely to see **more benefit**:

Copy code

```
SELECT col1, col2
  FROM my_table
  WHERE
    col_x IN (1,4,7,8)
    AND event_time >=
      DATEADD(hour, -1, CURRENT_TIMESTAMP());
```

The conditions in the WHERE clause make this query highly selective. The IN clause limits the
results to a relatively few items, and the time comparison further limits the data to a
certain time period.

This query is likely to see **limited benefit**:

Copy code

```
SELECT col1, col2
  FROM my_table
  WHERE
    event_time >=
      DATEADD(day, -365, CURRENT_TIMESTAMP());
```

Asking for data for an entire year makes this query less selective. If your dataset is big,
this query might process all rows in the table.

Other complexities such as large joins (for example, by joining two fact tables), or compute-intensive expressions such
as regular expressions, might result in lower concurrency due to higher use of compute resources.
See [Choosing a size for an interactive warehouse](#label-interactive-warehouse-size-considerations) for information about optimizing for
those situations.

### Data layout best practices

#### Clustering

Tables queried through interactive warehouses benefit from a **well-clustered table**, a table
that’s sorted based on the same column or columns that you are filtering on. For example, if
your query often filters on a TIMESTAMP column such as `sale_date`, then it makes sense to use
that column as the clustering key.

For interactive tables, you specify the [clustering key](/user-guide/tables-clustering-keys) during creation:

Copy code

```
CREATE INTERACTIVE TABLE product_sales (<column definitions>) CLUSTER BY (sale_date);
```

For standard tables, specify the clustering key during table creation or, if the table already exists,
use the [ALTER TABLE … CLUSTER BY](/sql-reference/sql/alter-table) command to set or change
the clustering key.

That way, SELECT queries that filter on `sale_date` can quickly skip all irrelevant data
and return results. For example, the following query filters on a date range by testing the
`sale_date` column:

Copy code

```
SELECT ... WHERE sale_date > '2025-10-24' AND ...
```

For more details about choosing the best clustering keys, see
[Clustering Keys & Clustered Tables](/user-guide/tables-clustering-keys).

Interactive tables support up to 1 KB total across all clustering key columns. The per-column 5-byte limit for standard tables
doesn’t apply.

#### Target file size with Iceberg tables

For Iceberg tables queried through interactive warehouses, set the `TARGET_FILE_SIZE` table property to `AUTO`. This lets
Snowflake choose the optimal file size for interactive workloads, which improves cache utilization and query performance.
For more information about this property, see [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table-snowflake).

Snowflake [Cortex Code](/user-guide/cortex-code/cortex-code) supports automatic clustering key selection for interactive tables. To use it, start Cortex Code and prompt it to suggest a clustering key using the `interactive-clustering-key-recommendation` skill.

### Choosing a size for an interactive warehouse

You should start by sizing your warehouse based on the approximate size of the *working set* in your tables. Interactive warehouses pre-warm the data cache based on tables you’ve attached to the warehouse via ALTER WAREHOUSE ADD TABLES(table\_1, table\_2, …).

For example, if your table is 120TB (compressed), and it represents 1 year worth of data. If you mostly query the last 7 days, then you should size your warehouse as MEDIUM to be able to hold the last 7 days of data. (120TB / 365 days \* 7 days = 2.19TB) Interactive warehouses have a range of sizes from XSMALL to 4XLARGE, see [the warehouse sizing table](#label-interactive-working-set-to-warehouse-size-table) for more information.

![Diagram showing how a warehouse cache holds only the working set of a table, not the full dataset.](/static/images/interactive-cache-size.png)

Once you’ve completed all your queries and layout optimizations, consider **scaling your warehouse** to meet demand. Choose a minimum number of clusters sufficient to support the expected number of concurrent users. See [Multi-cluster warehouses](/user-guide/warehouses-multicluster).

This is because the interactive warehouse utilizes *local storage caching*. While the data for your entire data set (table) is always accessible, accessing non-cached data does incur higher read latency on the first read.

Choose a warehouse size to fit the needs of your workloads. Experiment with your data and workload to determine the optimal size for your interactive warehouse.

Tip

For good performance, pick a cache size that’s sufficient to hold your *working set*. The warehouse doesn’t need fit your entire table into the cache.

| Working Set or Data Cache Size (Approximate Maximum) | Warehouse Size |
| --- | --- |
| 350 GB | XSMALL |
| 600 GB | SMALL |
| 1.2 TB | MEDIUM |
| 2.5 TB | LARGE |
| 5.5 TB | XLARGE |
| 11 TB | 2XLARGE |
| 22 TB | 3XLARGE |
| 44 TB | 4XLARGE |

Expand

Show lessSee more

### Performance optimization for interactive analytics

Interactive analytics is optimized for short-running queries and enforces a default statement timeout of 5s. You might encounter patterns where queries run slower than expected. The following sections describe common problems, how to recognize them, and what to try.

For all of these patterns, your primary diagnostic tool is the [Snowsight Query Profile](/user-guide/ui-snowsight-activity#label-snowsight-query-profile), especially the remote read percentage and the time breakdown between compilation, queuing, and execution. For programmatic access to query operator statistics, see [GET\_QUERY\_OPERATOR\_STATS](/sql-reference/functions/get_query_operator_stats).

#### Problem 1: A single query is taking too long

**Likely causes:**

- The query needs more compute resources than the warehouse provides. Examples include predicates with regular expressions or `CASE` expressions, and high-memory operations like `COUNT(DISTINCT ...)`.
- The warehouse is too small to hold a useful working set in the local data cache, so the query reads heavily from remote storage. You can see this in Query Profile as a high remote read percentage.
- The query scans more data than necessary because the `ORDER BY`, `LIMIT`, or `WHERE` clauses aren’t aligned with the table’s clustering keys, so micropartition pruning isn’t effective.

**What to try:**

- Increase the warehouse size. Start with the recommended size for your working set (see the sizing table above) and keep increasing until single-query latency is acceptable.
- Select only the columns you need, and add selective predicates in the `WHERE` clause so the query can effectively prune micropartitions.
- For `ORDER BY` + `LIMIT` queries (for example, “most recent N rows”), make sure the clustering key matches the column used in `ORDER BY`. A table clustered by its timestamp column prunes efficiently for “most recent” queries; one that isn’t clustered by the sort column might read the full table. For help choosing clustering keys, see [Cortex Code clustering key recommendation](/user-guide/interactive-performance#label-interactive-clustering-key-recommendation).

#### Problem 2: Queries are suddenly taking longer (high tail latency, high P95 latency)

In Query Profile, the slow queries show an elevated remote read percentage compared to earlier fast queries in the same session.

**Likely causes:**

- The warehouse was suspended between bursts and resumed for this burst. Cache warming hasn’t finished when the first queries arrive.
- The new burst touches different micropartitions of the table than the prior workload, so the first queries read from remote storage until the new micropartitions are cached.
- The total size of all tables attached to the warehouse far exceeds the data cache capacity, so different query patterns keep evicting each other’s cached data. In this case you see chronic high remote reads across all queries, not just the first few in a burst.
- The first one or two queries immediately after a resume can show uneven per-worker latency as different nodes finish warming at slightly different times. This is typically self-resolving after a few queries.

**What to try:**

- If chronic high remote reads persist across all queries (not only the first few in a burst), your attached table footprint probably exceeds the data cache capacity of the warehouse. Detach unused tables with `ALTER WAREHOUSE ... DROP TABLES`, or use a larger warehouse size.
- For benchmarks, wait for cache warming to finish before measuring latency. Cache warm-up speed depends on warehouse size and table size: bigger tables take longer, bigger warehouses warm faster.

#### Problem 3: The first query of a new shape is slow, later similar queries are fast

In Query Profile, the slow first query spends most of its time in compilation, and later queries of the same shape compile quickly.

**Likely cause:**

- Query metadata caches on the compilation cache are cold for this query pattern.

**What to try:**

- Use [bind variables](/sql-reference/bind-variables) instead of embedding literal values directly in SQL text. Queries that differ only in their literal values (for example, different filter parameters from a dashboard) share the same query shape, so they all benefit from a single warm compilation cache entry.
- Remember that steady production query volume keeps these caches warm. Latency measured at very low throughput does not reflect what you’ll see at realistic load.

#### Problem 4: Queries are queuing or you’re not achieving the expected concurrency

In Query Profile, queued queries spend a significant portion of their time queuing before execution starts.

**Likely causes:**

- The peak of concurrent queries exceeds the warehouse’s concurrency capacity.

**What to try:**

- Scale out by setting `MIN_CLUSTER_COUNT` and `MAX_CLUSTER_COUNT` to run a multi-cluster interactive warehouse. If `MAX_CLUSTER_COUNT` is greater than `MIN_CLUSTER_COUNT`, Snowflake adds clusters automatically as load increases.
- If your workload has a predictable ramp-up (for example, at the start of a business day), use [task based multi-cluster sizing](/user-guide/interactive#label-interactive-task-based-multi-cluster-sizing) to scale out the warehouse.

### Using search optimization for point lookups

We recommend adding [search optimization](/user-guide/search-optimization/enabling) when you
perform point lookup queries on your tables. Point lookups are queries that filter on a
single column to retrieve one or a few rows of data. A good example is `WHERE some_id = some_UUID`.

### Benchmarking best practices

When assessing the performance of interactive warehouses in a test environment, follow these
best practices to avoid inconsistent or misleading results:

- Turn off the query result cache to make the benchmark results consistent between multiple
  benchmark runs. You can turn off the query result cache at the account, user, and session level by
  setting the [USE\_CACHED\_RESULT](/sql-reference/parameters#label-use-cached-result) session parameter. That way, the
  queries only use the table data cache from the interactive warehouse. When you turn result caching
  on in your production environment, you can expect equal or better performance than in your
  benchmark testing.
- Because an interactive warehouse takes some time to warm the table data cache, wait for a while
  after you create or resume an interactive warehouse before testing query performance. This
  simulates the typical production configuration, where the warehouse remains active for long
  periods. Snowflake applies optimizations to the cache warming process. Therefore, it’s more
  efficient to let Snowflake complete this process than to warm the cache yourself by running sample
  queries.
- When comparing performance of interactive tables against standard Snowflake tables, don’t
  interleave the queries between standard and interactive tables. Instead, run the full benchmark on
  standard tables, then run the same tests on interactive tables.
- When doing comparative benchmarks with other database systems, make sure that the clustering
  columns in your tables match the WHERE clause predicates in your queries. For more
  information about choosing the best clustering columns, see
  [Clustering Keys & Clustered Tables](/user-guide/tables-clustering-keys). In particular, don’t cluster on columns with
  high cardinality, such as unique IDs or timestamps.
- If your queries are short and simple, you can achieve higher concurrency by setting the
  [MAX\_CONCURRENCY\_LEVEL](/sql-reference/parameters#label-max-concurrency-level) parameter to a higher value for
  your interactive warehouse.

## AI-assisted optimization with Cortex Code

[Cortex Code](/user-guide/cortex-code/cortex-code) includes a built-in `snowflake-interactive` skill
that can analyze your queries and recommend how to configure interactive analytics for your workload.
The skill helps you with clustering key selection, warehouse sizing, table attachment, and overall
performance tuning.

To use the skill, start Cortex Code (CLI or Desktop) and describe your workload. For example:

```
I have the following query:

SELECT
  N_NAME,
  COUNT(*) AS ORDERS
FROM ORDERS AS O
INNER JOIN CUSTOMER AS C ON O_CUSTKEY = C_CUSTKEY
INNER JOIN NATION   AS N ON C_NATIONKEY = N_NATIONKEY
WHERE O_ORDERDATE BETWEEN '1996-01-01' AND '1996-12-31'
GROUP BY ROLLUP (N_NAME)
ORDER BY N_NAME NULLS LAST;

I want to understand how it can benefit from interactive analytics. The query
is used in a dashboard along with other queries. The query must answer in less
than a second. The database with the tables used by the query is
DM_TESTTPCH_BENCH_DB and the schema is TPCH_SF100. The filter on order date
will be different, and users might also filter data for a specific nation,
region, or market. How can I make sure that I can obtain the performance I need?
Use the current connection to connect to Snowflake.
```

The skill connects to your Snowflake account, inspects the tables and their current clustering,
evaluates the query profile, and provides recommendations including:

- Whether an interactive warehouse or interactive table is the best fit for your workload.
- Clustering key suggestions based on your filter patterns and join columns.
- Warehouse sizing guidance based on your data volume.
- Materialized view candidates for frequently run aggregation patterns.
