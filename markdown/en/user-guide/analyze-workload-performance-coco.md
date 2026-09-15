# Analyze Workload Performance with CoCo

The **`workload-performance-analysis`** bundled skill in [Cortex Code](/user-guide/cortex-code/cortex-code) analyzes
Snowflake SQL query execution using [ACCOUNT\_USAGE](/sql-reference/account-usage) views. You ask questions in natural
language; the skill queries historical performance data, summarizes what it finds, and can suggest next steps.

The skill is built into Cortex Code. You don’t install or configure it separately.

## Overview

Use this skill when you need to understand **how queries ran** and **what to tune next**: spilling, partition pruning,
cache efficiency, clustering, and eligibility for [Search Optimization Service](/user-guide/search-optimization-service)
(SOS) or [Query Acceleration Service](/user-guide/performance-query-warehouse-qas) (QAS).

The skill is a single entry point for performance analysis. Depending on what you ask, it focuses on a specific query,
warehouse, table, query pattern, stored procedure run, a set of queries, or a broad account health scan.

## When the skill applies

Cortex Code selects **workload-performance-analysis** when your request matches performance analysis topics such as:

- Spilling, memory pressure, or spill to local or remote storage
- Partition pruning, scan volume, or tables that prune poorly
- Cache hit rates or warehouse cache efficiency
- Clustering keys, `CLUSTER BY`, or predicate columns for clustering or SOS
- Search optimization or SOS candidates
- Query Acceleration Service (QAS) or acceleration eligibility
- Slow SQL diagnosis, bottlenecks, root cause, or concurrency issues
- Per-warehouse spill, prune, or cache metrics

## What this skill is not for

Use other Cortex Code skills for the following topics:

| Topic | Use instead |
| --- | --- |
| Cost, credits, or spend analysis | [`cost-intelligence`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cost-intelligence) |
| Access audit or data governance | [`data-governance`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-data-governance) |
| Writing, editing, or debugging your SQL | General Cortex Code assistance outside this skill |

Expand

Show lessSee more

## What the skill can do

The skill analyzes SQL query performance using [ACCOUNT\_USAGE](/sql-reference/account-usage) views. It can help you:

- **Disk spilling:** Find queries with excessive local or remote spilling and suggest fixes.
- **Partition pruning:** Review pruning ratios and scan efficiency on large tables.
- **Cache hit rates:** Evaluate local disk cache and warehouse cache efficiency.
- **Clustering keys:** Recommend clustering keys when pruning is poor.
- **Search Optimization Service (SOS):** Identify workloads that may benefit from SOS.
- **Query Acceleration Service (QAS):** Find queries that may be eligible for QAS.
- **Predicate analysis:** Relate filter columns to clustering or SOS opportunities.
- **Stored procedure runs:** Analyze a parent `CALL` and its child queries as one run.
- **Query sets and patterns:** Compare multiple queries, recurring patterns, or filtered workloads.

Results are summarized with top findings first, not raw dumps of every row.

## Questions the skill can help answer

- Which queries are spilling to disk, and should I upsize the warehouse or change the query?
- Is warehouse **ANALYTICS\_WH** showing spill, prune, or cache problems across recent runs?
- Are scans on **DB.SCHEMA.ORDERS** pruning enough partitions?
- Which recurring query patterns are slowest or most expensive to execute?
- What happened inside this stored procedure run, including child queries?
- Are there SOS or QAS candidates in my recent workload?
- Give me a quick account-level performance health check (spilling, pruning, cache, QAS).

Be specific when you can: a query ID, warehouse name, fully qualified table name, time range, or symptom (for example
“remote spilling on ANALYTICS\_WH last 7 days”) helps the skill scope the analysis.

## How deep the analysis goes

You control depth with how you phrase the request. The following table summarizes typical outcomes:

| You ask for | What you get |
| --- | --- |
| Summary, overview, quick look, health check | High-level findings; you can ask to go deeper afterward |
| What’s wrong, root cause, bottlenecks, why is X slow | Summary plus issue detection |
| Recommend, how to fix, optimize, action items | Summary, detection, and concrete recommendations |

Expand

Show lessSee more

If you don’t specify depth, the skill starts with a summary and offers deeper analysis or recommendations.

## Where you can use the skill

The skill is available in four places. In Snowsight, select **Analyze with CoCo** to pass page context to the skill.
In [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli), [Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop),
or the [Cortex Code panel in Snowsight](/user-guide/cortex-code/cortex-code-snowsight), describe what to analyze or
invoke `/workload-performance-analysis`.

### Query Details

From a single query’s detail view in Snowsight, select **Analyze with CoCo**. Cortex Code receives that
query’s context and analyzes that execution (including stored procedure runs when the query is a `CALL`). For more
information, see [Review details and profile of a specific query](/user-guide/ui-snowsight-activity#label-snowsight-specific-query-details).

![Query Details page with Analyze with CoCo selected and Cortex Code summarizing query profile metrics such as partitions scanned and cache hit rate](/static/images/user-guide/analyze-workload-performance-coco/query-details-analyze-with-coco.png)

### Query History

From **Query History**, select **Analyze with CoCo** when you have one or more queries in view. The skill uses the
list context from the page to summarize or compare those queries. For more information, see
[Query history in Snowsight](/user-guide/ui-snowsight-activity).

![Query History page with Analyze with CoCo selected and Cortex Code summarizing query status and key findings for the visible queries](/static/images/user-guide/analyze-workload-performance-coco/query-history-analyze-with-coco.png)

### Performance Explorer

From the Performance Explorer dashboard, select **Analyze with CoCo** to interpret workload trends, hotspots, or
changes over time in the context of the charts and filters you already applied. For more information, see
[Analyzing query workloads with Performance Explorer](/user-guide/performance-explorer).

![Performance Explorer dashboard with Analyze with CoCo selected and Cortex Code presenting a health metrics summary and key takeaways](/static/images/user-guide/analyze-workload-performance-coco/performance-explorer-analyze-with-coco.png)

### Cortex Code (CLI, Desktop, Snowsight panel)

Open Cortex Code directly and describe what to analyze, or type `/workload-performance-analysis` to invoke the skill.
This path also applies when you open the Cortex Code panel in Snowsight without using a page-specific **Analyze**
action. For more information, see
[Cortex Code CLI bundled skills](/user-guide/cortex-code/bundled-skills#label-bundled-skill-workload-performance-analysis).

![Cortex Code panel showing the workload-performance-analysis skill description and analysis type options](/static/images/user-guide/analyze-workload-performance-coco/coco-workload-performance-analysis-skill.png)

Snowsight entry points pass page context so you don’t need to copy query IDs or re-enter filters. In CLI, Desktop, or
the general Snowsight panel, include the scope in your prompt (warehouse name, query ID, table name, time range, and so on).

## Example ways to use the skill

These outcomes match common workloads the skill is designed for:

- Identify queries with excessive disk spilling and get concrete fix recommendations.
- Analyze partition pruning ratios and suggest better clustering keys for large tables.
- Find queries eligible for Search Optimization Service or Query Acceleration Service.

Example prompts:

```
Summarize spill and cache metrics for warehouse ANALYTICS_WH over the last 7 days.

Why is query 01b24bb0-0007-9627-0000-0001234abcde slow? Root cause and recommendations.

Which tables have the worst partition pruning? Recommend clustering keys for the top offenders.

Are any of my recurring query patterns good QAS candidates?

Health check: spilling, pruning, cache, and QAS eligibility account-wide for the last week.
```

In [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli), you can also run `/workload-performance-analysis`
and then describe your question.

## Prerequisites and access

You need:

- Access to [Cortex Code](/user-guide/cortex-code/cortex-code) in your account. See
  [Cortex Code in Snowsight](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-snowsight-access-control)
  and [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli).
- Privileges to read the ACCOUNT\_USAGE views the skill queries. Many analyses require the
  `SNOWFLAKE.USAGE_VIEWER` database role (or related usage or governance roles for specific views). An administrator
  can grant access, for example:

  Copy code

  ```
  GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER TO ROLE <your_role>;
  ```

What you can see matches the query and account activity your roles can access in Snowsight and
[ACCOUNT\_USAGE](/sql-reference/account-usage).

## Limitations

Keep these constraints in mind:

- **Historical data only:** The skill analyzes past runs in [ACCOUNT\_USAGE](/sql-reference/account-usage); it does not
  predict future performance.
- **Latency:** ACCOUNT\_USAGE data can lag behind real time (for example, up to about 45 minutes for query history
  and longer for some pruning views).
- **Hybrid tables:** Visibility in these views can be limited for hybrid tables.
- **Benefit estimates:** The skill can flag SOS or clustering candidates but can’t guarantee exact savings from
  enabling them.

When recommending warehouse sizing or queuing tradeoffs, the skill may ask whether your workload prioritizes **speed**
(minimize wait time and runtime) or **cost** (accept some queuing or spilling to save credits). That framing helps
tailor guidance; for credit and spend analysis, use the
[`cost-intelligence`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cost-intelligence) skill instead.

## Related performance resources

- [Using query insights to improve performance](/user-guide/query-insights): Rule-based insights on individual queries
  in Snowsight.
- [Analyzing query workloads with Performance Explorer](/user-guide/performance-explorer): Interactive workload
  dashboards in Snowsight.
- [Optimizing query performance](/user-guide/performance-query-options): Manual tuning strategies and reference material.
- [Cortex Code CLI bundled skills](/user-guide/cortex-code/bundled-skills#label-bundled-skill-workload-performance-analysis):
  Bundled skill reference entry.
