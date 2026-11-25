# Cortex Code skills for Snowflake interactive analytics

[Cortex Code](/user-guide/cortex-code/cortex-code) includes two skills that help you work with [interactive analytics](/user-guide/interactive). You describe what you want in plain language, and Cortex Code connects to your account, inspects your objects, and proposes the SQL to run. Cortex Code asks for your approval before it changes anything.

| Skill | Use it to | Where it’s available |
| --- | --- | --- |
| `snowflake-interactive` | Start using interactive warehouses, evaluate whether a query is a good fit, manage warehouses, choose clustering keys, query, and troubleshoot. | Cortex Code CLI, Cortex Code Desktop, and Snowsight |
| `interactive-benchmark` | Load test a query on an interactive warehouse. Check whether it meets a latency goal under concurrency, or find the maximum requests per second that a warehouse can sustain. | Cortex Code CLI and Cortex Code Desktop |

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

The `interactive-benchmark` skill load tests a query on an interactive warehouse. It supports two benchmark modes. It deploys a benchmark API and a [Locust](https://locust.io) load generator to a Snowpark Container Services (SPCS), runs the load test, and produces an HTML report.

### Benchmark modes

Every benchmark runs in exactly one of two modes. The skill picks the mode from your request and asks only if your request is unclear.

|  | Latency target | Maximum concurrency |
| --- | --- | --- |
| Question it answers | Can the query meet a P95 latency goal for a given number of concurrent users? | How many requests per second (RPS) can a given warehouse configuration sustain? |
| How to ask for it | Give a latency goal, for example “P95 under 1 second” or “can it serve 50 users within 2 seconds”. | Ask for maximum RPS or QPS, peak throughput, or a stress test, or ask for zero think time. |
| Think time between requests | 0.5 to 1.5 seconds by default. | Always 0. Each simulated user sends requests back to back. |
| Warehouse size and cluster count | The size and cluster count that you give are limits. The skill starts lower and scales up or out within those limits until the goal is met. | Fixed for the whole run. The skill never scales the warehouse. |
| Result | Whether the P95 latency goal was met, not met, or couldn’t be met within your limits. | The sustained requests per second, plus the P50, P95, and P99 latency observed at that load. |

Expand

Show lessSee more

Requests per second (RPS) and queries per second (QPS) mean the same thing here, because each request runs exactly one query. The skill reports the result as requests per second.

To find out how much load a larger warehouse can sustain, run a separate maximum concurrency benchmark for each size and cluster count that you want to compare.

The skill uses the `snowflake-interactive` skill to validate that the query suits interactive warehouses and to configure the warehouse before it runs the test.

Note

The skill runs the benchmark autonomously. Before it starts, the agent asks for the scope of the benchmark. For a latency target benchmark, that’s the maximum warehouse size, the maximum cluster count, and the maximum number of escalation iterations. For a maximum concurrency benchmark, that’s the fixed warehouse size and cluster count to test. After the scope is confirmed, the agent runs the benchmark until it ends and never goes beyond those limits.

A benchmark can take a significant amount of time. Each load test runs for 3 minutes. In a latency target benchmark, the agent can repeat the test with different configuration options, such as a larger warehouse size or more clusters, until the latency goal is met or the limits are reached. A maximum concurrency benchmark runs the load test once. Start the benchmark, let the agent run it, and do other work in the meantime. The agent reports when the results are ready.

### Prerequisites

- Cortex Code CLI or Cortex Code Desktop. The skill isn’t available in Snowsight.
- The `snow` CLI, Python 3, and `envsubst` installed on your machine.
- A Snowflake connection configured in `~/.snowflake/connections.toml`.
- A role that can create the benchmark database, schema, stage, warehouses, compute pools, and services, and that can create public service endpoints. `SYSADMIN` is one option if it has the required privileges. The role also needs access to the source data.
- Access to Snowpark Container Services.

### What the skill does

1. Determines the benchmark mode, collects the benchmark inputs, such as the database, schema, latency goal (latency target only), and number of concurrent users, and asks you to confirm them.
2. Validates that the query is a good fit for an interactive warehouse. If the query isn’t a good fit, the skill stops and explains why.
3. Validates the interactive warehouse setup, configures concurrency and a fallback warehouse, and warms the cache.
4. Deploys the benchmark API and Locust services to SPCS.
5. Runs a baseline test and then the load test. In a maximum concurrency benchmark, the load test uses zero think time.
6. Collects server-side metrics. In a latency target benchmark, the skill checks the results against your latency goal. If the goal isn’t met, the skill scales the warehouse up or out, within the limits you set, and runs the test again. In a maximum concurrency benchmark, the skill doesn’t scale the warehouse. It reports the sustained requests per second.
7. Generates an HTML report and offers to tear down the benchmark resources or keep them.

### Snowflake services used

The skill creates and uses the following Snowflake features and objects during a benchmark:

- [Interactive warehouses](/user-guide/interactive): run the query that you’re benchmarking.
- Standard warehouses: serve as the fallback warehouse and run the baseline measurement. The skill creates dedicated warehouses unless you specify existing ones.
- Snowpark Container Services (SPCS): runs the benchmark API and Locust load generator on two compute pools that use the `CPU_X64_M` instance family, and exposes them through public service endpoints.
- A benchmark database, schema, and stage: store the benchmark resources and files.

SPCS compute pools and warehouses consume credits while they run. For more information, see [Results and cleanup](#results-and-cleanup).

### Benchmark inputs

The skill asks for these values in a single prompt, with defaults where possible. The first input is the benchmark mode, which the skill infers from your request when it can.

| Input | Default |
| --- | --- |
| Benchmark mode | Inferred from your request: latency target or maximum concurrency |
| Database and schema | Required |
| Interactive warehouse and standard warehouse | The skill creates dedicated warehouses |
| Connection name | Required |
| P95 latency goal (latency target only) | 1 second |
| Concurrent users | 50 |
| Maximum warehouse size (scale-up limit). In a maximum concurrency benchmark, the fixed size to test. | Medium for latency target, X-Small for maximum concurrency |
| Maximum cluster count (scale-out limit). In a maximum concurrency benchmark, the fixed cluster count to test. | Calculated from the number of users for latency target, 1 for maximum concurrency |
| Benchmark name | A generated name that starts with `IWB_` |
| Maximum escalation iterations (latency target only) | 5 |

Expand

Show lessSee more

The skill interprets any latency figure that you give as a P95 latency unless you say otherwise.

The load generator and the benchmark API run on `CPU_X64_M` compute pool nodes in Snowpark Container Services. At a high number of concurrent users, or at a very high request rate, the load generator or the API can become the bottleneck instead of the warehouse. The practical limit depends on the queries that you test. Before the real load test, the skill runs a baseline test against a no-op endpoint to check that the infrastructure is healthy, and it doesn’t continue if the baseline fails. If the load generator is CPU-bound during the load test, the report flags it. In a maximum concurrency benchmark, treat the measured requests per second as a lower bound in that case, because the warehouse limit wasn’t reached.

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

### Example: size a warehouse for a latency target

If you want to know how much warehouse capacity a target load needs, you can ask the skill to find out and set the limits that it can’t exceed:

```
Can my query handle 200 concurrent users with a P95 latency under 500 ms?
Don't scale beyond a Large warehouse and limit scale-out to 8 clusters.
```

In this example, the skill helps the AI agent treat the limits that you give as the ceiling for scale-up and scale-out. The agent escalates the warehouse size or cluster count only up to those limits, and the report shows whether the 500 ms goal was met at 200 users.

### Example: find the maximum requests per second

To find out how many requests per second a specific warehouse configuration can sustain, ask for a maximum concurrency benchmark. Give the warehouse size, the cluster count, and the number of concurrent users:

```
What's the maximum QPS that a Small interactive warehouse with 2 clusters
can sustain for this query with 100 concurrent users? Use database
DM_TESTTPCH_BENCH_DB, schema TPCH_SF100, and my connection named
my_connection.

SELECT N_NAME, COUNT(*) AS ORDERS
FROM ORDERS AS O
INNER JOIN CUSTOMER AS C ON O_CUSTKEY = C_CUSTKEY
INNER JOIN NATION AS N ON C_NATIONKEY = N_NATIONKEY
WHERE O_ORDERDATE BETWEEN '1996-01-01' AND '1996-12-31'
GROUP BY ROLLUP (N_NAME)
ORDER BY N_NAME NULLS LAST;
```

In this example, the skill helps the AI agent run the load test with 100 simulated users that send requests with no think time against a fixed Small warehouse with 2 clusters. The agent doesn’t scale the warehouse. The report shows the sustained requests per second and the P50, P95, and P99 latency at that load.

### Getting started

For step-by-step instructions on installing the `interactive-benchmark` skill and running your first benchmark, see the [Getting started guide](https://github.com/Snowflake-Labs/analytics/blob/main/interactive-benchmark/GETTING-STARTED.md).

### Results and cleanup

The skill writes the HTML report, which includes the results of each iteration for a latency target benchmark or the sustained requests per second for a maximum concurrency benchmark, to `~/.snowflake/interactive-benchmark/reports/<benchmark_name>/` and opens it in your browser. To see what the report looks like, view the [sample report](https://snowflake-labs.github.io/analytics/interactive-benchmark/sample-report/benchmark-report.html). If your role can write benchmark reports, the skill also records the results in the `SNOWFLAKE.INTERACTIVE_ANALYTICS` schema so that you can view them in Snowsight.

At the end of the run, the skill lists the resources that it created and asks whether to remove them or keep them. The SPCS compute pools and warehouses consume credits while they run, so remove the resources when you finish testing.

If you plan to run more than one benchmark within the same hour, consider keeping the interactive warehouse instead of removing it after each run. The minimum billable period for an interactive warehouse is one hour, and each time that you create or resume one, a new minimum billable period starts. Removing and re-creating the warehouse between benchmarks can therefore increase your costs. For more information, see [Cost and billing considerations](/user-guide/interactive#label-interactive-cost).

## Related topics

- [Snowflake interactive analytics](/user-guide/interactive)
- [Performance for Snowflake interactive analytics](/user-guide/interactive-performance)
- [Cortex Code](/user-guide/cortex-code/cortex-code)
