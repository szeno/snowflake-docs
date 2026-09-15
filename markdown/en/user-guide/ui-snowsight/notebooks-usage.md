# Notebook usage and cost monitoring

A notebook consumes compute resources through its configured [virtual warehouses](/user-guide/warehouses-overview)
or [compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pools-default-compute-pools-for-notebooks). To manage costs and ensure efficient operations,
it’s important to monitor usage across individual notebooks, users, and the underlying compute infrastructure. This visibility helps ensure
efficient operations and supports cost accountability throughout your environment.

Snowflake provides access to detailed usage data through [ACCOUNT\_USAGE](/sql-reference/account-usage) views and system tables. This
data can help answer questions such as:

- What is the hourly credit consumption per notebook?
- How frequently were notebooks run in the past week?
- Which users ran notebooks in the past month?
- Which compute pools or warehouses did notebooks use over the past week?
- What is the total credit cost of notebooks using a specific compute resource?

For a broader overview of compute-related cost management, see [Exploring compute cost](/user-guide/cost-exploring-compute).

## Example query

You can query Snowflake’s [ACCOUNT\_USAGE](/sql-reference/account-usage) views to gain insight into the credit consumption for a notebook.
These views break down cost by notebook, user, or compute pool level at a daily or hourly basis.

### Usage

In the following example, each row represents a single notebook execution and includes details such as the execution timestamp, the user who ran the notebook, and the runtime
environment (Warehouse or Container Runtime).

Copy code

```
-- Warehouse Runtime
SELECT query_text, t1.user_name, credits_attributed_compute as total_warehouse_credits
FROM snowflake.account_usage.query_history t1
INNER JOIN snowflake.account_usage.query_attribution_history t2
ON t1.query_id = t2.query_id

-- Add your notebook name
AND t1.query_text ILIKE 'execute notebook% <example_nb_name>'
;

-- Container Runtime
SELECT
  start_time, notebook_name, user_name, SUM(credits) AS total_container_runtime_credits
FROM snowflake.account_usage.notebooks_container_runtime_history
WHERE notebook_name = '<example_nb_name>'
GROUP BY ALL;
```

## Cost monitoring on Container Runtime

The following queries help you monitor the credit consumption of notebooks in your account. Use these queries to analyze notebook usage patterns,
estimate costs, and understand how individual notebooks contribute to compute pool expenses.

Query: Hourly credit consumption by notebook
:   This query retrieves runtime history for a specific notebook, including credit usage and execution timestamps. Use this data to understand how
    often and how long a notebook runs, and to identify patterns or spikes in credit consumption by hour.

    Copy code

    ```
    SELECT * FROM snowflake.account_usage.notebooks_container_runtime_history
    WHERE notebook_name = '<example_nb_name>';
    ```

Query: Cost to run a specific notebook
:   This query shows the total credits consumed by a specific notebook. Use this to estimate a notebook’s cost and identify high-cost notebooks.

    Copy code

    ```
    SELECT
      notebook_name,
      SUM(credits) AS total_credits
    FROM snowflake.account_usage.notebooks_container_runtime_history
    WHERE notebook_name = '<example_nb_name>'
    GROUP BY notebook_name;
    ```

Query: Total compute pool cost per notebook
:   This query shows the total credits consumed by each notebook running on a specific compute pool. Use this to break down compute usage by
    notebook, which can help identify which notebooks contribute most to the compute pool’s overall cost.

    Copy code

    ```
    SELECT
      notebook_name,
      SUM(credits) AS total_credits
    FROM snowflake.account_usage.notebooks_container_runtime_history
    WHERE compute_pool_name = '<example_cp_name>'
    GROUP BY notebook_name;
    ```

Query: Identify users who ran a specific notebook
:   This query returns a list of users who have executed a specific notebook. Use this to understand usage patterns, or identify collaborators
    and consumers of shared notebooks.

    Copy code

    ```
    SELECT
      DISTINCT user_name
    FROM snowflake.account_usage.notebooks_container_runtime_history
    WHERE notebook_name = '<example_nb_name>';
    ```

### Additional notes

Costs for querying are associated with the underlying warehouse. For information on how warehouses work, see [Virtual warehouse credit usage](/user-guide/cost-understanding-compute#label-virtual-warehouse-credit-usage).
