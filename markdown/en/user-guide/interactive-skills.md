# Cortex Code skills for Snowflake interactive analytics

[Cortex Code](/user-guide/cortex-code/cortex-code) includes two skills that help you work with [interactive analytics](/user-guide/interactive). You describe what you want in plain language, and Cortex Code connects to your account, inspects your objects, and proposes the SQL to run. Cortex Code asks for your approval before it changes anything.

| Skill | Use it to | Where it’s available |
| --- | --- | --- |
| `snowflake-interactive` | Start using interactive warehouses, evaluate whether a query is a good fit, manage warehouses, choose clustering keys, query, and troubleshoot. | Cortex Code CLI, Cortex Code Desktop, and Snowsight |
| `interactive-benchmark` | Load test a query on an interactive warehouse and check whether it meets a latency goal under concurrency. | Cortex Code CLI and Cortex Code Desktop |

Expand

Show lessSee more

To use either skill, start Cortex Code and describe your goal. Cortex Code loads the matching skill automatically based on your request. You can also name the skill in your prompt.

## The snowflake-interactive skill

The `snowflake-interactive` skill covers the full lifecycle of interactive analytics. If you’re new to interactive warehouses, start here: the skill can take you from your first interactive warehouse to running queries on it. It routes your request to the part of the skill that matches your intent:

| Task | What the skill does |
| --- | --- |
| Getting started | Walks you through setting up interactive analytics for the first time. Also checks whether a specific query is a good fit by running it on a standard warehouse first and measuring a baseline. |
| Warehouse management | Creates interactive warehouses, adds and removes tables, resumes and suspends, and sets a fallback warehouse. |
| Clustering | Recommends clustering keys based on your filter patterns and join columns. |
| Querying | Runs and compares queries, including joins, and measures latency. |
| Updates and deletes | Explains how to run DML against data that an interactive warehouse serves, because interactive warehouses reject DML. |
| Troubleshooting | Diagnoses timeouts, fallback warehouse issues, cache warming, and errors on interactive warehouses. |

Expand

Show lessSee more

### Example: set up interactive analytics for a dashboard

If you have a dashboard that needs to respond quickly to many users, you can ask the skill to guide you through setting up interactive analytics from scratch. Describe the table, the filters, the latency goal, and the expected concurrency:

```
I want to make my sales dashboard faster. The dashboard queries
SALES_DB.PUBLIC.ORDERS, filters on order date and region, and needs to
respond in under a second for about 100 concurrent users. Help me set up
interactive analytics.
```

In this example, the skill helps the AI agent inspect the table and its current clustering, and then build a plan. The plan typically covers creating an interactive warehouse, attaching the table, and configuring a fallback warehouse. Review the plan, then approve each change.

### Example: check whether a query is a good fit

Not every query benefits from an interactive warehouse. Before you change anything, you can ask the skill to check whether a specific query is a good candidate:

```
Is the following query a good fit for an interactive warehouse? The database
is DM_TESTTPCH_BENCH_DB and the schema is TPCH_SF100.

SELECT N_NAME, COUNT(*) AS ORDERS
FROM ORDERS AS O
INNER JOIN CUSTOMER AS C ON O_CUSTKEY = C_CUSTKEY
INNER JOIN NATION AS N ON C_NATIONKEY = N_NATIONKEY
WHERE O_ORDERDATE BETWEEN '1996-01-01' AND '1996-12-31'
GROUP BY ROLLUP (N_NAME)
ORDER BY N_NAME NULLS LAST;
```

In this example, the skill helps the AI agent measure the query instead of judging it by its shape. The agent runs the query on a standard warehouse, collects metrics such as elapsed time and bytes scanned, checks the table’s clustering, and then bases its recommendation on those measurements.

### Example: choose a clustering key

Correct clustering is pivotal for getting the best performance out of Interactive Analytics. You can use the provided skill to make sure clustering is used and is actually helping the performances:

```
Suggest a clustering key for SALES_DB.PUBLIC.ORDERS. Most queries filter on
ORDER_DATE and CUSTOMER_REGION, and some sort by ORDER_DATE descending with
a LIMIT.
```

In this example, the skill helps the AI agent read the table’s current clustering together with your filter and sort patterns, and then recommend clustering columns. Because the prompt mentions a descending sort with a LIMIT, the agent considers a key that matches the sort column so that “most recent rows” queries prune well.

### Example: manage a warehouse

When you already know what you need, you can ask the skill to create and configure the interactive warehouse for you, without writing the SQL yourself:

```
Create an XSMALL interactive warehouse called dash_wh, attach the ORDERS and
CUSTOMERS tables, and use ANALYTICS_WH as the fallback warehouse.
```

In this example, the skill helps the AI agent write the CREATE INTERACTIVE WAREHOUSE, ALTER WAREHOUSE ADD TABLES, and fallback warehouse statements with the right syntax.

### Example: troubleshoot

If queries on an interactive warehouse time out or the fallback warehouse isn’t used as you expect, you can ask the skill to investigate:

```
Queries on my interactive warehouse dash_wh are timing out after 5 seconds
and the fallback warehouse doesn't seem to be used. Help me find out why.
```

In this example, the skill helps the AI agent check the warehouse configuration, the fallback warehouse setting, the privileges on both warehouses, and the query history. It also helps the agent consider whether missing clustering on the table or a query shape that is too wide (for example, one that scans too much data) is the cause. The agent then explains the likely cause and the fix.

### Example: run updates

Interactive warehouses reject DML statements such as UPDATE and DELETE. If you hit that error, you can ask the skill how to apply the change:

```
I need to update rows in a table that dash_wh serves. UPDATE fails with
"Cannot run statement type on an interactive warehouse". What should I do?
```

In this example, the skill helps the AI agent recognize that interactive warehouses reject DML, and it will give agent information on what option you have to to handle DML in such cases.

## The interactive-benchmark skill

The `interactive-benchmark` skill measures whether a query can meet a latency target under concurrent load on an interactive warehouse. It deploys a benchmark API and a [Locust](https://locust.io) load generator to a Snowpark Container Services (SPCS), runs the load test, and produces an HTML report.

The skill uses the `snowflake-interactive` skill to validate that the query suits interactive warehouses and to configure the warehouse before it runs the test.

Note

The skill runs the benchmark autonomously. Before it starts, the agent asks for the scope of the benchmark: the maximum warehouse size, the maximum cluster count, and the maximum number of escalation iterations. After the scope is confirmed, the agent runs the benchmark until it ends and never goes beyond those limits.

A benchmark can take a significant amount of time. Each load test runs for 3 minutes, and the agent can repeat the test with different configuration options, such as a larger warehouse size or more clusters, until the latency goal is met or the limits are reached. Start the benchmark, let the agent run it, and do other work in the meantime. The agent reports when the results are ready.

### Prerequisites

- Cortex Code CLI or Cortex Code Desktop. The skill isn’t available in Snowsight.
- The `snow` CLI, Python 3, and `envsubst` installed on your machine.
- A Snowflake connection configured in `~/.snowflake/connections.toml`.
- A role that can create the benchmark database, schema, stage, warehouses, compute pools, and services, and that can create public service endpoints. `SYSADMIN` is one option if it has the required privileges. The role also needs access to the source data.
- Access to Snowpark Container Services.

### What the skill does

1. Collects the benchmark inputs, such as the database, schema, latency goal, and number of concurrent users, and asks you to confirm them.
2. Validates that the query is a good fit for an interactive warehouse. If the query isn’t a good fit, the skill stops and explains why.
3. Validates the interactive warehouse setup, configures concurrency and a fallback warehouse, and warms the cache.
4. Deploys the benchmark API and Locust services to SPCS.
5. Runs a baseline test and then the load test.
6. Collects server-side metrics and checks the results against your latency goal. If the goal isn’t met, the skill scales the warehouse up or out, within the limits you set, and runs the test again.
7. Generates an HTML report and offers to tear down the benchmark resources or keep them.

### Benchmark inputs

The skill asks for these values in a single prompt, with defaults where possible:

| Input | Default |
| --- | --- |
| Database and schema | Required |
| Interactive warehouse and standard warehouse | The skill creates dedicated warehouses |
| Connection name | Required |
| P95 latency goal | 1 second |
| Concurrent users | 50 |
| Maximum warehouse size (scale-up limit) | Medium |
| Maximum cluster count (scale-out limit) | Calculated from the number of users |
| Benchmark name | A generated name that starts with `IWB_` |
| Maximum escalation iterations | 5 |

Expand

Show lessSee more

The skill interprets any latency figure that you give as a P95 latency unless you say otherwise.

### Example: benchmark a dashboard query

To find out whether a dashboard query meets its latency target when many users run it at the same time, you can ask the skill to benchmark it. Provide the query, the P95 target, and the number of concurrent users:

```
Benchmark this query on an interactive warehouse. It needs to return in under
a second at P95 with 100 concurrent users. Use database DM_TESTTPCH_BENCH_DB,
schema TPCH_SF100, and my connection named my_connection.

SELECT N_NAME, COUNT(*) AS ORDERS
FROM ORDERS AS O
INNER JOIN CUSTOMER AS C ON O_CUSTKEY = C_CUSTKEY
INNER JOIN NATION AS N ON C_NATIONKEY = N_NATIONKEY
WHERE O_ORDERDATE BETWEEN '1996-01-01' AND '1996-12-31'
GROUP BY ROLLUP (N_NAME)
ORDER BY N_NAME NULLS LAST;
```

In this example, the skill helps the AI agent validate the query, deploy the benchmark services to SPCS, and run a load test with 100 simulated users. The agent then compares the measured P95 latency against your one-second goal and, if needed, scales the warehouse within your limits and retests.

### Example: size a warehouse for a target load

If you want to know how much warehouse capacity a target load needs, you can ask the skill to find out and set the limits that it can’t exceed:

```
Can my query handle 200 concurrent users with a P95 latency under 500 ms?
Don't scale beyond a Large warehouse and limit scale-out to 8 clusters.
```

In this example, the skill helps the AI agent treat the limits that you give as the ceiling for scale-up and scale-out. The agent escalates the warehouse size or cluster count only up to those limits, and the report shows whether the 500 ms goal was met at 200 users.

### Results and cleanup

The skill writes the HTML report, which includes the results of each iteration, to `~/.snowflake/interactive-benchmark/reports/<benchmark_name>/` and opens it in your browser. If your role can write benchmark reports, the skill also records the results in the `SNOWFLAKE.INTERACTIVE_ANALYTICS` schema so that you can view them in Snowsight.

At the end of the run, the skill lists the resources that it created and asks whether to remove them or keep them. The SPCS compute pools and warehouses consume credits while they run, so remove the resources when you finish testing.

## Related topics

- [Snowflake interactive analytics](/user-guide/interactive)
- [Performance for Snowflake interactive analytics](/user-guide/interactive-performance)
- [Cortex Code](/user-guide/cortex-code/cortex-code)
