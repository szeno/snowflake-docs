# Reducing queues

This topic discusses how a warehouse owner or administrator can reduce queuing in order to improve the performance of queries running
on a warehouse.

If too many queries are sent to a warehouse at the same time, the warehouse’s compute resources become exhausted and subsequent queries
are queued until resources become available. The time between submitting a query and getting its results is longer when the query must
wait in a queue before starting.

Note

You must have [access to the shared SNOWFLAKE database](/sql-reference/account-usage#label-enabling-usage-for-other-roles) to execute the diagnostic queries provided in this topic. By default, only the ACCOUNTADMIN role has the privileges needed to execute the queries.

## Finding queues

Snowsight:
:   To determine if a particular warehouse is experiencing queues:

    1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
    2. In the navigation menu, select **Compute** » **Warehouses**.
    3. Select the warehouse.
    4. In the **Warehouse Activity** chart, use the color associated with **Queued load** to identify queues.
    5. Look for patterns in the height of the bars to determine if the queues are associated with usage spikes.

SQL:
:   **Query: Warehouses with queueing**

    This query lists the warehouses that had a queue in the last month, sorted by date.

    Copy code

    ```
    SELECT TO_DATE(start_time) AS date
      ,warehouse_name
      ,SUM(avg_running) AS sum_running
      ,SUM(avg_queued_load) AS sum_queued
    FROM snowflake.account_usage.warehouse_load_history
    WHERE TO_DATE(start_time) >= DATEADD(month,-1,CURRENT_TIMESTAMP())
    GROUP BY 1,2
    HAVING SUM(avg_queued_load) > 0;
    ```

    You can also write queries against the [QUERY\_HISTORY view](/sql-reference/account-usage/query_history) to calculate the time
    that queries spend in the queue.

## Options for reducing queues

You have several options to stop warehouse queuing:

> - For a regular warehouse (i.e. not a multi-cluster warehouse), consider creating additional warehouses, and then distribute the queries
>   among them. If specific queries are causing usage spikes, focus on moving those queries.
> - Consider converting a warehouse to a [multi-cluster warehouse](/user-guide/warehouses-multicluster) so the warehouse can elastically
>   provision additional compute resources when demand spikes. Multi-cluster warehouses require the
>   [Enterprise Edition](/user-guide/intro-editions) of Snowflake.
> - If you are already using a multi-cluster warehouse, increase the maximum number of clusters.

## Cost considerations

For a description of how running a multi-cluster warehouse affects credit consumption, refer to [Multi-cluster size and credit usage](/user-guide/warehouses-multicluster#label-size-and-credit-usage).

If you are running a multi-cluster warehouse in Auto-scale mode, you can use a [scaling policy](/user-guide/warehouses-multicluster#label-mcw-scaling-policies) to help
control the costs. The Economy scaling policy favors conserving credits over cluster elasticity by keeping running clusters fully-loaded
rather than starting additional clusters. This might result in queries being queued and taking longer to complete.

## How to configure warehouses to reduce queues

Regular Warehouses:
:   To create new warehouses to which queries can be distributed, sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), and in the navigation menu, select **Compute** » **Warehouses**.
    You can also use the [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse) command.

Multi-Cluster Warehouses:
:   To convert an existing warehouse to a multi-cluster warehouse or to increase the maximum number of clusters for an existing warehouse:

    1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
    2. In the navigation menu, select **Compute** » **Warehouses**.
    3. Find the warehouse, and select **…** » **Edit**.
    4. If you are converting to a multi-cluster warehouse, turn on the **Multi-cluster Warehouse** option. If you do not see this option,
       upgrade to Enterprise Edition or higher.
    5. Use the **Max Clusters** drop-down to adjust the maximum number of clusters.
