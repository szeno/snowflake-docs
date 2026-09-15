Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# QUERY\_ATTRIBUTION\_HISTORY view

This Account Usage view can be used to determine the compute cost of a given query run on warehouses in your account
in the last 365 days (1 year).

For more information, see [Viewing cost by tag in SQL](/user-guide/cost-attributing#label-cost-attribute-tag-sql).

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| QUERY\_ID | VARCHAR | Internal/system-generated identifier for the SQL statement. |
| PARENT\_QUERY\_ID | VARCHAR | Query ID of the parent query or NULL if the query does not have a parent. |
| ROOT\_QUERY\_ID | VARCHAR | Query ID of the topmost query in the chain or NULL if the query does not have a parent. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse that the query was executed on. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse that the query executed on. |
| QUERY\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-hash) computed based on the canonicalized SQL text. |
| QUERY\_PARAMETERIZED\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-parameterized-hash) computed based on the parameterized query. |
| QUERY\_TAG | VARCHAR | Query tag set for this statement through the [QUERY\_TAG](/sql-reference/parameters#label-query-tag) session parameter. |
| USER\_NAME | VARCHAR | User who issued the query. |
| START\_TIME | TIMESTAMP\_LTZ | Time when query execution started (in the local time zone). |
| END\_TIME | TIMESTAMP\_LTZ | Time when query execution ended (in the local time zone). |
| CREDITS\_ATTRIBUTED\_COMPUTE | FLOAT | Number of credits attributed to this query. Includes only the credit usage for the query execution and doesn’t include any warehouse idle time. |
| CREDITS\_USED\_QUERY\_ACCELERATION | FLOAT | Number of credits consumed by the [Query Acceleration Service](/user-guide/query-acceleration-service) to accelerate the query. NULL if the query is not accelerated.     The total cost for an accelerated query is the sum of this column and the CREDITS\_ATTRIBUTED\_COMPUTE column. |

Expand

Show lessSee more

## Usage notes

- Latency for this view can be up to eight hours.
- This view displays results for any role granted the USAGE\_VIEWER or GOVERNANCE\_VIEWER
  [database role](/sql-reference/snowflake-db-roles).

- The value in the `credits_attributed_compute` column contains the warehouse credit usage for executing the query,
  inclusive of any resizing and/or autoscaling of multi-cluster warehouse(s). This cost is attributed based on
  the weighted average of the resource consumption.

  The value doesn’t include any credit usage for warehouse idle time. Idle time is a period
  of time in which no queries are running in the warehouse and can be measured at the warehouse level.

  The value doesn’t include any other credit usage that is incurred as a result of query execution.
  For example, the following are not included in the query cost:

  - Data transfer costs
  - Storage costs
  - Cloud services costs
  - Costs for serverless features
  - Costs for tokens processed by AI services
- For queries that are executed concurrently, the cost of the warehouse is attributed to individual queries based on the
  weighted average of their resource consumption during a given time interval.
- Short-running queries (<= ~100ms) are currently too short for per query cost attribution and are not included in the view.
- Data for all columns is available starting from mid-August, 2024. Some data prior to this date might be available in the view, but
  might be incomplete.
- This view doesn’t include records for jobs executed by [Adaptive Warehouses](/user-guide/warehouses-adaptive).
  For per-query credit usage on Adaptive Warehouses, use
  [QUERY\_METERING\_HISTORY view](/sql-reference/account-usage/query_metering_history).

## Examples

### Query costs for related queries

To determine the costs of a specific query and similar queries using the query parameterized hash, replace `<query_id>`
and execute the following statements:

Copy code

```
SET query_id = '<query_id>';

WITH query_hash_of_query AS (
  SELECT query_parameterized_hash
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ATTRIBUTION_HISTORY
  WHERE query_id = $query_id
  LIMIT 1
)
SELECT
  query_parameterized_hash,
  COUNT (*) AS query_count,
  SUM(credits_attributed_compute) AS recurrent_query_attributed_credits
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ATTRIBUTION_HISTORY
WHERE start_time >= DATE_TRUNC('MONTH', CURRENT_DATE)
  AND start_time < CURRENT_DATE
  AND query_parameterized_hash = (SELECT query_parameterized_hash FROM query_hash_of_query)
GROUP BY ALL;
```

### Query costs for the current user

To determine the costs of queries executed by the current user for the current month, execute the following statement:

Copy code

```
SELECT user_name, SUM(credits_attributed_compute) AS credits
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ATTRIBUTION_HISTORY
  WHERE user_name = CURRENT_USER()
    AND start_time >= DATE_TRUNC('MONTH', CURRENT_DATE)
    AND start_time < CURRENT_DATE
  GROUP BY user_name;
```

For an example of attributing warehouse costs to users, see [Resources shared by users from different departments](/user-guide/cost-attributing#label-cost-attribute-tag-sql-resources-shared).

### Query costs for stored procedures

For stored procedures that issue multiple hierarchical queries, you can compute the attributed query costs for the
procedure by using the root query ID for the procedure.

1. To find the root query ID for a stored procedure, use the [ACCESS\_HISTORY view](/sql-reference/account-usage/access_history). For example,
   to find the root query ID for a stored procedure, set the `query_id` and execute the following statements:

   Copy code

   ```
   SET query_id = '<query_id>';

   SELECT query_id,
       parent_query_id,
       root_query_id,
       direct_objects_accessed
     FROM SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY
     WHERE query_id = $query_id;
   ```

   For more information, see [Ancestor queries with stored procedures](/user-guide/access-history#label-access-history-ancestor-queries).
2. To sum the query cost for the entire procedure, replace `root_query_id` and execute the following statements:

   Copy code

   ```
   SET query_id = '<root_query_id>';

   SELECT SUM(credits_attributed_compute) AS total_attributed_credits
     FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ATTRIBUTION_HISTORY
     WHERE (root_query_id = $query_id OR query_id = $query_id);
   ```

### Additional examples

For more examples, see [Resources shared by users from different departments](/user-guide/cost-attributing#label-cost-attribute-tag-sql-resources-shared).
