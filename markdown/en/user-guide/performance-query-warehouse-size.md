# Increasing warehouse size

This topic discusses how a warehouse owner or administrator can adjust the size of a warehouse to improve the performance of queries
running on it.

The larger a warehouse, the more compute resources are available to execute a query or set of queries. This makes increasing the size of a
warehouse a straightforward strategy for improving query performance; simply upsize the warehouse, re-run the query, and if the increased
performance does not justify the increased cost of running the query, return the warehouse to its original size.

Using a larger warehouse has the biggest impact on larger, more complex queries, and may not improve the performance of small, basic
queries.

Note

You must have [access to the shared SNOWFLAKE database](/sql-reference/account-usage#label-enabling-usage-for-other-roles) to execute the diagnostic queries provided in this topic. By default, only the ACCOUNTADMIN role has the privileges needed to execute the queries.

## Determining the load of the warehouse

Examining the load of a warehouse can help determine whether increasing its size can help improve performance. If a warehouse is heavily
loaded, concurrent queries might be competing for its compute resources, in which case increasing the size of a warehouse might not
provide as big of a performance boost as expected. But if you can determine that the load is low, there is a good chance that increasing
the size of the warehouse will improve the performance of a complex query.

**Query: Warehouse Load**

This query provides insight into the total load of a warehouse for executed and queued queries. These load values represent the ratio of the total execution time (in seconds) of all queries in a specific state in an interval by the total time (in seconds) for that interval.

For example, if 276 seconds was the total time for 4 queries in a 5 minute (300 second) interval, then the query load value is 276 / 300 = 0.92.

Copy code

```
 SELECT TO_DATE(start_time) AS date,
  warehouse_name,
  SUM(avg_running) AS sum_running,
  SUM(avg_queued_load) AS sum_queued
FROM snowflake.account_usage.warehouse_load_history
WHERE TO_DATE(start_time) >= DATEADD(month,-1,CURRENT_TIMESTAMP())
GROUP BY 1,2
HAVING SUM(avg_queued_load) >0;
```

## Cost considerations

A larger warehouse consumes more credits for a given length of time:

| Warehouse size | Credits / hour (Gen1 warehouses) | Credits / second (Gen1 warehouses) | Notes |
| --- | --- | --- | --- |
| X-Small | 1 | 0.0003 | Default size for warehouses created in Snowsight and using [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse). |
| Small | 2 | 0.0006 |  |
| Medium | 4 | 0.0011 |  |
| Large | 8 | 0.0022 |  |
| X-Large | 16 | 0.0044 | Default size for warehouses created using Snowsight. |
| 2X-Large | 32 | 0.0089 |  |
| 3X-Large | 64 | 0.0178 |  |
| 4X-Large | 128 | 0.0356 |  |
| 5X-Large | 256 | 0.0711 | Generally available in Amazon Web Services (AWS) and Microsoft Azure regions, and in preview in US Government regions. |
| 6X-Large | 512 | 0.1422 | Generally available in Amazon Web Services (AWS) and Microsoft Azure regions, and in preview in US Government regions. |

Expand

Show lessSee more

The numbers in the preceding table refer to the first generation (Gen1) of Snowflake standard warehouses.
For usage information about the newer Gen2 warehouses, see [Snowflake generation 2 standard warehouses](/user-guide/warehouses-gen2).
For information about credit consumption for generation 2 standard warehouses,
see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
Gen2 warehouses aren’t yet available for all cloud service providers or for all regions, and currently are not the default
when you create a standard warehouse.

Tip

For information about cost implications of changing the RESOURCE\_CONSTRAINT property, see
[considerations for changing RESOURCE\_CONSTRAINT while a warehouse is running or suspended](/user-guide/warehouses-gen2#label-gen-2-standard-warehouses-altering).

Another way that you can scale the capacity of Snowflake warehouses without changing the warehouse size is by using
multi-cluster warehouses. For more information about that feature, see [Multi-cluster warehouses](/user-guide/warehouses-multicluster).

If a query takes less time to execute on a larger warehouse, the increased cost of running a large warehouse might be offset by the reduced
execution time. For example, if a query runs twice as fast on the next largest warehouse, the total cost of running the query remains the
same.

Tip

Best practice is to limit who can adjust the size of a warehouse. Allowing users to increase the size of a warehouse to meet the needs
of an individual query can result in unexpected costs if they forget to return the warehouse to its original size once the query has
been executed.

## How to increase the warehouse size

To increase the size of a warehouse, do one of the following:

Snowsight:
:   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
    2. In the navigation menu, select **Compute** » **Warehouses**.
    3. Find the warehouse, and select **…** » **Edit**.
    4. Use the **Size** drop-down to select the new warehouse size.
    5. Select **Save Warehouse**.

SQL:
:   Use the [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) command to change the warehouse size. For example:

    Copy code

    ```
    ALTER WAREHOUSE my_wh SET WAREHOUSE_SIZE = large;
    ```
