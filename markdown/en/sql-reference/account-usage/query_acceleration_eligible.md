Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# QUERY\_ACCELERATION\_ELIGIBLE view

This Account Usage view can be used to identify queries that are eligible for the
[query acceleration service](/user-guide/query-acceleration-service) (QAS).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| QUERY\_ID | VARCHAR | Internal/system-generated identifier for the SQL statement. |
| QUERY\_TEXT | VARCHAR | Text of the SQL statement. |
| START\_TIME | TIMESTAMP\_LTZ | Statement start time. |
| END\_TIME | TIMESTAMP\_LTZ | Statement end time. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse that the query executed on. |
| WAREHOUSE\_SIZE | VARCHAR | Size of the warehouse when this statement executed. |
| ELIGIBLE\_QUERY\_ACCELERATION\_TIME | NUMBER | Amount of query execution time (in seconds) eligible for the query acceleration service. |
| UPPER\_LIMIT\_SCALE\_FACTOR | NUMBER | Upper limit [scale factor](/sql-reference/sql/create-warehouse#label-query-acceleration-max-scale-factor) for the given query. |
| QUERY\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-hash) computed based on the canonicalized SQL text. |
| QUERY\_HASH\_VERSION | NUMBER | The [version of the logic](/user-guide/query-hash#label-query-hash-version) used to compute `QUERY_HASH`. |
| QUERY\_PARAMETERIZED\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-parameterized-hash) computed based on the parameterized query. |
| QUERY\_PARAMETERIZED\_HASH\_VERSION | NUMBER | The [version of the logic](/user-guide/query-hash#label-query-hash-version) used to compute `QUERY_PARAMETERIZED_HASH`. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (three hours).

- Query acceleration is supported for the following SQL commands:

  > - SELECT
  > - INSERT
  > - CREATE TABLE AS SELECT (CTAS)
  > - COPY INTO <table>

  For more information about query eligibility, see [Eligible queries](/user-guide/query-acceleration-service#label-qas-eligible-queries).
- This view only includes eligible queries that have *not* been accelerated. If you have enabled
  the query acceleration service and previously QAS-eligible queries are now accelerated, they
  are not included in this view.

## Examples

Identify the warehouses with the most queries eligible in a given period of time for the query acceleration service:

Copy code

```
SELECT warehouse_name, COUNT(query_id) AS num_eligible_queries
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
  WHERE start_time >= '2024-06-01 00:00'::TIMESTAMP
  AND end_time <= '2024-06-07 00:00'::TIMESTAMP
  GROUP BY warehouse_name
  ORDER BY num_eligible_queries DESC;
```

For more example queries, see [Identifying queries and warehouses with the QUERY\_ACCELERATION\_ELIGIBLE view](/user-guide/query-acceleration-service#label-query-acceleration-eligible-queries).
