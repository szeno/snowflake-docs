# Trying query acceleration

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides an overview of how a warehouse owner or administrator can use the query acceleration service to improve the performance
of queries running on a warehouse. For complete details about query acceleration, refer to [Using the Query Acceleration Service (QAS)](/user-guide/query-acceleration-service).

The query acceleration service offloads portions of query processing to
[serverless compute resources](/user-guide/cost-understanding-compute#label-serverless-credit-usage), which speeds up the processing of a query while reducing its demand
on the warehouse’s compute resources.

When a warehouse has outlier queries (i.e. queries that use more resources than a typical query), the query acceleration service might
also improve the performance of the warehouse’s other queries because the extra computing demands of the outlier queries are offloaded
to serverless compute resources.

Examples of workloads that might benefit from the query acceleration service include ad hoc analytics, workloads with unpredictable data
volume per query, and queries with large scans and selective filters.

Note

You must have [access to the shared SNOWFLAKE database](/sql-reference/account-usage#label-enabling-usage-for-other-roles) to execute the diagnostic queries provided in this topic. By default, only the ACCOUNTADMIN role has the privileges needed to execute the queries.

## Finding candidates for query acceleration

You can use a function or queries to determine whether enabling the query acceleration service might improve the performance of a query
or set of queries.

**Function: Determine if a specific query might benefit**

The [SYSTEM$ESTIMATE\_QUERY\_ACCELERATION](/sql-reference/functions/system_estimate_query_acceleration) function allows you to check whether a specific query is a good
candidate for query acceleration service.

The function accepts a query id as its sole argument. Wrapping the function in the PARSE\_JSON function makes it easier to interpret the
results. For example:

Copy code

```
SELECT PARSE_JSON(system$estimate_query_acceleration('8cd54bf0-1651-5b1c-ac9c-6a9582ebd20f'));
```

If a query is a candidate for query acceleration service and has not yet been accelerated, the `status` of the response is `eligible`.
A status of `ineligible` indicates the query will not benefit if you enable query acceleration service for a warehouse.

For additional information about evaluating the query acceleration service for a particular query, including estimated execution times for
different scale factors, refer to the [reference documentation](/sql-reference/functions/system_estimate_query_acceleration).

**Query: Best query candidates across warehouses**

This query identifies the queries in the past week that might benefit most from the query acceleration service by calculating the amount of query execution
time that is eligible for acceleration.

Copy code

```
SELECT query_id, eligible_query_acceleration_time
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
  WHERE start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
  ORDER BY eligible_query_acceleration_time DESC;
```

**Query: Best warehouse candidates by execution time**

This query identifies the warehouses that might benefit the most from the query acceleration service in the past week. For each warehouse, it calculates
the total query execution time eligible for acceleration.

Copy code

```
SELECT warehouse_name, SUM(eligible_query_acceleration_time) AS total_eligible_time
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
  WHERE start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
  GROUP BY warehouse_name
  ORDER BY total_eligible_time DESC;
```

**Query: Best warehouse candidates by number of queries**

This query identifies the warehouses with the most queries, in the past week, eligible for the query acceleration service.

Copy code

```
SELECT warehouse_name, COUNT(query_id) AS num_eligible_queries
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
  WHERE start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
  GROUP BY warehouse_name
  ORDER BY num_eligible_queries DESC;
```

## Cost considerations

The serverless compute resources leased by a warehouse for query acceleration consume credits independent of the credits consumed by the
warehouse, and are billed separately.

Query acceleration service is enabled for an entire warehouse, but unlike upsizing a warehouse, it is only used for queries that benefit
from increased compute power. This can be cost effective for warehouses that run a mixed workload because queries that do not require
additional compute resources do not incur the additional cost of using a larger warehouse.

You can use the warehouse’s [scale factor](/user-guide/query-acceleration-service#label-query-acceleration-scale-factor) to help control the cost of the query acceleration
service. This scale factor, which is a multiplier of the warehouse’s credit consumption, sets a limit on how much serverless compute can
be used by a warehouse. For example, if a warehouse has a scale factor of 5, the credit consumption rate of serverless compute resources
cannot exceed the consumption rate of the warehouse by more than 5 times.

You can use the [SYSTEM$ESTIMATE\_QUERY\_ACCELERATION](/sql-reference/functions/system_estimate_query_acceleration) function to gauge how the scale factor affects the
performance of a query.

To maximize performance without considering cost, set the scale factor to 0.

## How to enable Query Acceleration Service

To enable the query acceleration service with a maximized performance boost, use the [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) command as
follows:

Copy code

```
ALTER WAREHOUSE my_wh SET
  ENABLE_QUERY_ACCELERATION = true
  QUERY_ACCELERATION_MAX_SCALE_FACTOR = 0;
```
