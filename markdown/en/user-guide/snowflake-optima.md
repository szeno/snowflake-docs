# Snowflake Optima

Snowflake Optima extends Snowflake’s core principles of performance and simplicity by applying an
intelligent approach to workload optimization. Instead of requiring manual tuning, Snowflake Optima continuously analyzes
workload patterns and implements the most effective strategies automatically. Snowflake Optima ensures that queries run faster
and more cost-efficiently, without added configuration or maintenance. By anticipating and adapting to the evolving
nature of SQL workloads, Snowflake Optima automatically improves performance.

Note

Snowflake Optima is included in all [Snowflake editions](/user-guide/intro-editions).

The following sections describe Snowflake Optima in more detail:

- [Optima Indexing](#optima-indexing)
- [Optima Metadata](#optima-metadata)
- [Optima Planning](#optima-planning)
- [Optima Clustering](#optima-clustering)
- [Monitor Snowflake Optima use](#monitor-snowflake-optima-use)

## Optima Indexing

Note

Available on [Snowflake generation 2 standard warehouses](/user-guide/warehouses-gen2) and
[Adaptive Warehouses](/user-guide/warehouses-adaptive).

*Optima Indexing* is a Snowflake Optima feature that automatically analyzes workloads to create and maintain
indexes in the background. Optima Indexing is built on top of the
[search optimization service](/user-guide/search-optimization-service).

By continuously monitoring SQL workloads, Optima Indexing identifies opportunities to improve performance — such
as repetitive point-lookup queries on a table — and automatically generates hidden indexes to accelerate those workloads.
These indexes are built and maintained on a best-effort basis, without requiring user intervention.

There are no additional costs for Optima Indexing, and because it is fully integrated into Snowflake, no additional
configuration or effort is required to benefit from improved performance.

For specialized workloads that demand guaranteed performance — for example, threat detection in the cybersecurity industry —
you can still directly apply search optimization. This option provides consistent index freshness and ultimately consistent
performance for scenarios where near real-time results are critical.

## Optima Metadata

Note

Available on [Snowflake generation 2 standard warehouses](/user-guide/warehouses-gen2) and
[Adaptive Warehouses](/user-guide/warehouses-adaptive).

*Optima Metadata* is a Snowflake Optima feature that automatically optimizes your workloads without any user input.
Snowflake Optima analyzes your query patterns, identifies inefficient usage of columns in pruning, and creates additional
metadata to optimize these queries. Even if you don’t know all the nuances of Snowflake’s query engine, Optima still ensures
that you prune unused micro-partitions as effectively as possible.

For example, one of the scenarios that Snowflake Optima has optimized is usage of the [UPPER](/sql-reference/functions/upper) and
[LOWER](/sql-reference/functions/lower) functions in the WHERE clause. These functions are inefficient in pruning. So, if Snowflake
Optima observes frequent use of these functions in your query filter predicates, it automatically creates metadata to aid in
pruning.

In general, the best practice is to avoid scenarios that lead to inefficient pruning. However, Snowflake Optima can improve
performance when these scenarios occur. That is, you should continue to follow all existing query performance best practices and think of Optima
Metadata as a feature that works in the background to catch optimizations you might have missed.

## Optima Planning

Note

Available on [Snowflake generation 2 standard warehouses](/user-guide/warehouses-gen2) and
[Adaptive Warehouses](/user-guide/warehouses-adaptive).

*Optima Planning* is a Snowflake Optima feature that automatically improves query plans for your
workloads by learning from executions. It’s enabled by default and requires no configuration.
Optima Planning continuously observes how queries run, captures information from query execution,
and uses that information to make better planning decisions to optimize workload performance.

For example, when a query joins large tables on skewed or correlated data, the optimizer’s initial
cardinality estimates can be inaccurate, leading to a suboptimal join order. When the query runs,
Optima Planning records information from query execution, and uses that information to optimize
query plans. Workloads such as scheduled reports, ELT pipelines, and dashboard refreshes
automatically benefit from improved performance.

## Optima Clustering

*Optima Clustering* is a Snowflake Optima feature that autonomously optimizes clustered tables for query
performance. It’s the next-generation version of [Automatic Clustering](/user-guide/tables-auto-reclustering). You define a
[clustering key](/user-guide/tables-clustering-keys), and Snowflake continuously reclusters the table in the
background with no manual maintenance.

Compared with Clustering Classic (the previous Automatic Clustering behavior), Optima Clustering offers the following
advantages:

- Faster time to cluster new data, which can improve query performance on clustered tables.
- A smart clustering algorithm that prioritizes clustering the data that matters most for query performance.
- Highly predictable billing based on uncompressed data volume ingested, not compute hours. For the current per
  uncompressed GB billing rate, see the
  [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
- Expanded clustering key length: Optima Clustering can use up to 1 KB total across all clustering key columns.
  Clustering Classic uses only the first 5 bytes of each clustering key column.

Starting September 1, 2026, newly clustered tables use Optima Clustering. Tables that are already clustered remain on
Clustering Classic. You don’t need to take any action for the rollout.

To determine whether a table uses Optima Clustering or Clustering Classic, call
[SYSTEM$CLUSTERING\_INFORMATION](/sql-reference/functions/system_clustering_information).

For more information, including costs, suspend and resume behavior, and how to identify each version, see
[Automatic Clustering](/user-guide/tables-auto-reclustering).

## Monitor Snowflake Optima use

You can monitor Snowflake Optima use on the following panes in the [Query Profile tab](/user-guide/ui-snowsight-activity#label-snowsight-query-profile)
under **Query History** in Snowsight:

- [Query insights pane](#label-snowflake-optima-query-insights-pane)
- [Statistics pane](#label-snowflake-optima-statistics-pane)

You can also monitor Snowflake Optima use by querying the [QUERY\_INSIGHTS view](/sql-reference/account-usage/query_insights).
For more information about query insights, see [Using query insights to improve performance](/user-guide/query-insights).

### Query insights pane

The [Query insights](/user-guide/query-insights#label-query-insights-viewing) pane displays each type of insight detected
for a query and lists each instance of that insight type.

- To learn more about the condition that was detected, select **View** next to an entry in the
  **Query insights** pane.

If Snowflake Optima optimized the query, one or more of the following insights can appear:

| Insight | Description |
| --- | --- |
| **Snowflake Optima used** | The query benefited from [Optima Metadata](#optima-metadata) and/or [Optima Indexing](#optima-indexing)—for example, improved partition pruning or accelerated point lookups on filtered columns. |
| **Snowflake Optima planning used** | The query benefited from [Optima Planning](#optima-planning). Snowflake applied a learned execution plan that improved performance for this query. |

Expand

Show lessSee more

Select **View** next to an insight to see how Optima benefited the query. Select **Learn more** in the detail view to open this topic.

The following image shows an example of the **Query insights** pane that indicates that Snowflake Optima was used:

![Shows the Query Insights pane on the Query Profile tab.](/static/images/snowflake-optima-query-insights.png)

### Statistics pane

To view pruning statistics for Snowflake Optima, open the
[Statistics](/user-guide/search-optimization/monitoring-search-optimization) pane on the **Query Profile** tab.
Look for the row labeled **Partitions pruned by Snowflake Optima**. This row shows the number of partitions skipped during
query execution, indicating how Snowflake Optima improved performance by reducing the amount of data scanned.

The following image shows an example of the **Statistics** pane that indicates that Snowflake Optima was used:

![Shows the Statistics pane on the Query Profile tab.](/static/images/snowflake-optima-query-statistics.png)

### Review Optima impact with CoCo

The [workload-performance-analysis](/user-guide/cortex-code/bundled-skills#label-bundled-skill-workload-performance-analysis)
skill in CoCo summarizes what Snowflake Optima did for your account over a time window. The summary reports three
measures, one for each Optima capability that produces a measurable benefit:

| Optima capability | Measure | Source view |
| --- | --- | --- |
| [Optima Indexing](#optima-indexing) and [Optima Metadata](#optima-metadata) | Partitions pruned by Snowflake Optima | [TABLE\_QUERY\_PRUNING\_HISTORY view](/sql-reference/account-usage/table_query_pruning_history) |
| [Optima Clustering](#optima-clustering) | Tables maintained by Optima Clustering | [AUTOMATIC\_CLUSTERING\_HISTORY view](/sql-reference/account-usage/automatic_clustering_history) |
| [Optima Planning](#optima-planning) | Queries optimized by Optima Planning | [QUERY\_INSIGHTS view](/sql-reference/account-usage/query_insights) |

Expand

Show lessSee more

Copy a prompt into the CoCo CLI, CoCo Desktop, or the CoCo panel in Snowsight:

## Try this in CoCo first

[Open CoCo](/user-guide/cortex-code/cortex-code)

CoCo can run these workflows end to end. Copy a prompt to get started.

- Review what Snowflake Optima did for my account

  ```
  What has Snowflake Optima done for my account over the last <NUMBER_OF_DAYS> days?
  ```

  Copy prompt

The skill uses the last 7 days by default. To change the window, replace `<NUMBER_OF_DAYS>` or include a time
range in your prompt, such as “over the last 30 days.”

The summary includes the following information:

- **Partitions pruned:** The total number of partitions that Snowflake Optima pruned in the window, and the tables that
  benefited most. The summary also shows the percentage of total pruning that the top three tables account for.
- **Tables maintained:** The number of tables that Optima Clustering maintained in the window. For the top tables, the
  summary shows rows reclustered, bytes reclustered, and the number of reclustering operations.
- **Queries optimized:** The number of queries that used Optima Planning in the window.

If Snowflake Optima didn’t affect any tables or queries in the window, the summary omits that measure instead of reporting
zero. When the window has no partitions pruned, the summary checks whether your account has
[Snowflake generation 2 standard warehouses](/user-guide/warehouses-gen2) or
[Adaptive Warehouses](/user-guide/warehouses-adaptive), because Optima applies to those warehouse types.

The summary also reports which Optima features apply to the top tables, such as Optima Metadata, Optima Indexing, or
Optima Clustering. Most of these views require the `SNOWFLAKE.USAGE_VIEWER` database role. Reading the per-table feature
flags requires the `SNOWFLAKE.OBJECT_VIEWER` database role. If your role doesn’t have access to a view, the skill omits
the measures or details that depend on that view.

The summary doesn’t report Optima Clustering credits. For credit and spend analysis, use the
[`cost-intelligence`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cost-intelligence) skill.

The skill analyzes historical data from [ACCOUNT\_USAGE](/sql-reference/account-usage) views, which can lag behind real
time. For the full skill workflow and more example prompts, see
[Analyze Workload Performance with CoCo](/user-guide/analyze-workload-performance-coco).
