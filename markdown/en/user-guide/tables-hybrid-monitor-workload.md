# Monitor hybrid table workloads

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

Unistore workloads that leverage hybrid tables will be different from many
analytical workloads that you are running in Snowflake. For example, your
workloads might contain fewer unique queries that take less time to run and
execute at a higher frequency. You have several options to monitor your
workloads.

> - [Monitor transactions](#label-hybrid-tables-monitor-transactions)
> - [Monitor workloads](#label-hybrid-tables-monitor-workloads)
> - [Monitor overall workload health](#label-hybrid-tables-monitor-workload-health)
> - [Identify and investigate repeated queries](#label-hybrid-tables-monitor-identify-queries)

## Monitor transactions

Hybrid tables support Snowflake transaction monitoring features, including [SHOW TRANSACTIONS](/sql-reference/sql/show-transactions),
[DESCRIBE TRANSACTION](/sql-reference/sql/desc-transaction), [SHOW LOCKS](/sql-reference/sql/show-locks), and
[LOCK WAIT HISTORY](/sql-reference/account-usage/lock_wait_history).

The behavior of these commands and views for hybrid tables is consistent with the behavior for standard
Snowflake tables, except for the following changes:

- A new `ROW` lock type is introduced in the [SHOW LOCKS](/sql-reference/sql/show-locks) command to
  represent row locks against hybrid tables. The locks are summarized to show one transaction holding
  (one or multiple) row locks and another transaction waiting for these locks.
- [LOCK WAIT HISTORY](/sql-reference/account-usage/lock_wait_history) does not show schema-related information.
- LOCK\_WAIT\_HISTORY does not summarize BLOCKER\_QUERIES. If a query is blocked by multiple blockers,
  then they will appear as multiple records in the view rather than as multiple entries in the
  BLOCKER\_QUERIES JSON array for the single waiter record.
- For the result of SHOW LOCKS, and the LOCK\_WAIT\_HISTORY view:
  - As the row locks are summarized, the lock-holding transaction is assumed to acquire the lock when it starts.
  - Due to the potential high volume of Unistore transactions, only locks that have blocked other transaction(s)
    for an extended period (approximately 5 seconds) are shown.
  - The lock-waiting transaction might still appear to be waiting for the locks even if it has acquired them
    (for no more than 1 minute). The accuracy of lock reporting will improve in future releases.
  - If a statement that blocked a waiting query has completed and was a short-running query against hybrid
    tables, the following information for the blocker query is not shown in the BLOCKER\_QUERY field
    of the waiting query record:
    - Query UUID of the blocker query
    - Session ID of the blocker query
    - User name of the blocker query
    - Database ID of the blocker query
    - Database name of the blocker query

## Monitor workloads

To monitor your operational workloads effectively, use the
[AGGREGATE\_QUERY\_HISTORY view](/sql-reference/account-usage/aggregate_query_history). This view enables
you to monitor the health of your workload, diagnose issues, and identify avenues
for optimization. The AGGREGATE\_QUERY\_HISTORY view aggregates query execution statistics
for a repeated parameterized query over a time interval so that it is easier
and more efficient to identify patterns in your workloads and queries over time. Note
that all Snowflake workloads and queries will be combined in the output of this view.

The AGGREGATE\_QUERY\_HISTORY view helps you answer the following questions about your workloads:

> - How many operations per second are being executed in my virtual warehouse?
> - Which queries are consuming the most total time or resources in my workload?
> - Has the performance of a specific query changed substantially over time?

To help improve performance and efficiency in your workload, individual
executions of low latency operations (under one second) will not be
stored in [QUERY\_HISTORY view](/sql-reference/account-usage/query_history) nor will they
generate a unique query profile. Instead, aggregate statistics for repeated
executions of that query will be returned in the AGGREGATE\_QUERY\_HISTORY view.
You will also be able to view a sampled query profile for the query over a selected
time interval. For more information about this behavior, see [Usage notes](/sql-reference/account-usage/query_history#label-query-history-usage-notes-acct-usage).

Tip

You can use the [Grouped Query History view](/user-guide/ui-snowsight-activity#label-snowsight-grouped-query-history)
in Snowsight to visualize performance and statistics for typical hybrid table workloads.
This view does not capture all hybrid table activity, but it provides a good alternative to
monitoring performance for a large volume of individual queries that are somewhat repetitive and
run extremely fast.

## Monitor overall workload health

Use the AGGREGATE\_QUERY\_HISTORY view to monitor your overall workload
throughput and concurrency, and to investigate unexpected spikes or drops in
your workloads. For example:

Copy code

```
SELECT
    interval_start_time
    , SUM(calls) as execution_count
    , SUM(calls) / 60 as queries_per_second
    , COUNT(DISTINCT session_id) as unique_sessions
    , COUNT(user_name) as unique_users
FROM snowflake.account_usage.aggregate_query_history
WHERE warehouse_name = '<MY_WAREHOUSE>'
  AND interval_start_time > $START_DATE
  AND interval_start_time < $END_DATE
GROUP BY ALL;
```

You can also use aggregate query history to monitor for potential problems
with errors, queueing, lock blocking, or throttling. For example:

Copy code

```
WITH time_issues AS
(
    SELECT
        interval_start_time
        , SUM(transaction_blocked_time:"SUM") as transaction_blocked_time
        , SUM(queued_provisioning_time:"SUM") as queued_provisioning_time
        , SUM(queued_repair_time:"SUM") as queued_repair_time
        , SUM(queued_overload_time:"SUM") as queued_overload_time
        , SUM(hybrid_table_requests_throttled_count) as hybrid_table_requests_throttled_count
    FROM snowflake.account_usage.aggregate_query_history
    WHERE WAREHOUSE_NAME = '<MY_WAREHOUSE>'
      AND interval_start_time > $START_DATE
      AND interval_start_time < $END_DATE
    GROUP BY ALL
),
errors AS
(
    SELECT
        interval_start_time
        , SUM(value:"count") as error_count
    FROM
    (
        SELECT
            a.interval_start_time
            ,e.*
        FROM
            snowflake.account_usage.aggregate_query_history a,
            TABLE(flatten(input => errors)) e
        WHERE interval_start_time > $START_DATE
          AND interval_start_time < $END_DATE
  )
  GROUP BY ALL
)
    SELECT
        ts.interval_start_time
        , error_count
        , transaction_blocked_time
        , queued_provisioning_time
        , queued_repair_time
        , queued_overload_time
        , hybrid_table_requests_throttled_count
    FROM time_issues ts
    FULL JOIN errors e ON e.interval_start_time = ts.interval_start_time
;
```

Ordinarily, such metrics should remain low. If you see an unexpected spike, it is recommended that you
investigate the cause.

## Identify and investigate repeated queries

You may opt to optimize or investigate the performance of common and often
executed queries to improve the efficiency of your workload. Use the
AGGREGATE\_QUERY\_HISTORY view to identify top queries for a workload by
execution count. For example:

Copy code

```
SELECT
    query_parameterized_hash
    , any_value(query_text)
    , SUM(calls) as execution_count
FROM snowflake.account_usage.aggregate_query_history
WHERE TRUE
          AND warehouse_name = '<MY_WAREHOUSE>'
          AND interval_start_time > '2024-02-01'
          AND interval_start_time < '2024-02-08'
GROUP BY
          query_parameterized_hash
ORDER BY execution_count DESC
;
```

You can choose to view metrics for the slowest queries. For example:

Copy code

```
SELECT
    query_parameterized_hash
    , any_value(query_text)
    , SUM(total_elapsed_time:"sum"::NUMBER) / SUM (calls) as avg_latency
FROM snowflake.account_usage.aggregate_query_history
WHERE TRUE
          AND warehouse_name = '<MY_WAREHOUSE>'
          AND interval_start_time > '2024-02-01'
          AND interval_start_time < '2024-02-08'
GROUP BY
          query_parameterized_hash
ORDER BY avg_latency DESC
;
```

You can analyze the performance of a particular query over time to gain insight
into trends in latency. For example:

Copy code

```
SELECT
    interval_start_time
    , total_elapsed_time:"avg"::number avg_elapsed_time
    , total_elapsed_time:"min"::number min_elapsed_time
    , total_elapsed_time:"p90"::number p90_elapsed_time
    , total_elapsed_time:"p99"::number p99_elapsed_time
    , total_elapsed_time:"max"::number max_elapsed_time
FROM snowflake.account_usage.aggregate_query_history
WHERE TRUE
          AND query_parameterized_hash = '<123456>'
          AND interval_start_time > '2024-02-01'
          AND interval_start_time < '2024-02-08'
ORDER BY interval_start_time DESC
;
```

This query calculates total query time. You can also modify the query to return
more granular metrics on the different phases of a query (compilation, execution,
queuing, and lock waiting). Aggregate statistics will be returned for each phase.
