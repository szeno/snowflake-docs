# Understand budget costs

Using budgets incurs the following costs:

- **Compute costs** — Snowflake runs serverless background tasks (\_MEASUREMENT\_TASK and \_BACKFILL\_TASK)
  that collect credit usage data for the account budget and custom budgets in your account. The compute resources used for these tasks are
  billed to your account.
- **Storage costs** — Snowflake stores metadata for Budgets in your account. Storage for this metadata is billed to your account.

## Exploring compute costs

You can view costs for serverless tasks using Snowsight or the Account Usage
[SERVERLESS\_TASK\_HISTORY view](/sql-reference/account-usage/serverless_task_history).

Note

The \_MEASUREMENT\_TASK task runs when you add or remove object tags, which incurs cost for the serverless compute needed to run the task.

Example: Compute cost of all budgets
:   The following example sums the credit usage for the measure task for the previous 28 days, which helps you understand the total compute
    cost of using budgets:

    Copy code

    ```
    SELECT SUM(credits_used)
       FROM snowflake.account_usage.serverless_task_history
       WHERE task_name = '_MEASUREMENT_TASK'
         AND start_time >= DATEADD('day', -28, current_timestamp());
    ```

Example: Compute cost of individual budgets
:   The following example lists the budgets in the account along with the compute costs associated with each budget within the specified time
    period.

    Copy code

    ```
    WITH costs AS (
      SELECT instance_id, SUM(credits_used) AS sum_credits
        FROM snowflake.account_usage.serverless_task_history
        WHERE start_time >= DATE_TRUNC('month',  CURRENT_TIMESTAMP())
          AND instance_id IS NOT NULL
       GROUP BY 1)
    SELECT ci.name, ci.schema_name, ci.database_name, costs.sum_credits
    FROM snowflake.account_usage.class_instances ci
      JOIN costs
        ON costs.instance_id = ci.id
    WHERE class_name = 'BUDGET' AND class_database_name = 'SNOWFLAKE' AND deleted IS NULL;
    ```

## Exploring storage costs

The data and metadata needed for budgets is stored in the following internal tables:

- \_CONFIGURATION\_TABLE
- \_MEASUREMENT\_TABLE
- \_NOTIFICATION\_TABLE
- \_BUDGET\_HOT\_USAGE\_DATA
- \_BUDGET\_COLD\_USAGE\_DATA
- \_BUDGET\_CUSTOM\_ACTIONS

To determine costs associated with these tables, you can query the TABLES view in the Account Usage or Organization Usage schema to return
the amount of storage being used for the tables.

The following examples returns the sum of the storage being used for the internal tables associated with budgets in the current account:

Copy code

```
SELECT SUM(bytes)
   FROM snowflake.account_usage.tables
   WHERE table_name IN (
      '_CONFIGURATION_TABLE',
      '_MEASUREMENT_TABLE',
      '_NOTIFICATION_TABLE',
      '_BUDGET_HOT_USAGE_DATA',
      '_BUDGET_COLD_USAGE_DATA');
```
