Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# QUERY\_METERING\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available to Adaptive Compute, which requires Enterprise Edition or higher. To inquire about
upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The query metering history view (`QUERY_METERING_HISTORY`) returns per-query credit usage for
queries run on [Adaptive Warehouses](/user-guide/warehouses-adaptive) within the last 365 days
(1 year). This view is available in the ACCOUNT\_USAGE schema. Coming soon: a corresponding
[ORGANIZATION\_USAGE](/sql-reference/organization-usage/query_metering_history) view for
organization-wide reporting (latency may be up to 24 hours).

Use this view to monitor price and performance at the query level. For aggregated warehouse
credit usage, see [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history).

## Columns

Several columns can be NULL until the query completes. For details, see
[usage notes](/sql-reference/account-usage/query_metering_history#label-query-metering-history-data-freshness).

| Column name | Data type | Description |
| --- | --- | --- |
| QUERY\_ID | VARCHAR | Internal/system-generated identifier for the SQL statement. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse that the query was executed on. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse that the query executed on. |
| QUERY\_METERING\_HOUR | TIMESTAMP\_LTZ | Start of the metering hour window this row represents. |
| QUERY\_START\_TIME | TIMESTAMP\_LTZ | Time when query execution started (in the local time zone). |
| QUERY\_END\_TIME | TIMESTAMP\_LTZ | Time when query execution ended (in the local time zone). NULL until the query completes; see [usage notes](/sql-reference/account-usage/query_metering_history#label-query-metering-history-data-freshness). |
| PARENT\_QUERY\_ID | VARCHAR | Query ID of the parent query. NULL until the query completes, or NULL if the query does not have a parent. |
| ROOT\_QUERY\_ID | VARCHAR | Query ID of the topmost query in the chain. NULL until the query completes, or NULL if the query is a standalone query (not part of a chain). |
| USER\_ID | NUMBER | Internal/system-generated identifier for the user who issued the query. |
| USER\_NAME | VARCHAR | User who issued the query. |
| ROLE\_NAME | VARCHAR | Role that issued the query. |
| QUERY\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-hash) computed based on the canonicalized SQL text. |
| QUERY\_PARAMETERIZED\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-parameterized-hash) computed based on the parameterized query. |
| QUERY\_TAG | VARCHAR | Query tag set for this statement through the [QUERY\_TAG](/sql-reference/parameters#label-query-tag) session parameter. |
| CREDITS\_USED\_COMPUTE | NUMBER | Number of credits used for compute for this query in this metering hour. |
| CREDITS\_USED\_CLOUD\_SERVICES | NUMBER | Number of credits used for cloud services for this query in this metering hour. |
| CREDITS\_USED | NUMBER | Total number of credits used for this query in this metering hour. |

Expand

Show lessSee more

## Usage notes

- This view displays results for any role granted the USAGE\_VIEWER or GOVERNANCE\_VIEWER
  [database role](/sql-reference/snowflake-db-roles).

- Latency for the view may be up to 1 hour. Charges accrued by a job may take up to 1 hour to appear
  in the view.

- This view includes per-query credit usage for queries run on [Adaptive Warehouses](/user-guide/warehouses-adaptive).
- Each query can have multiple rows in this view: one row per metering hour while the query runs. Use
  `QUERY_METERING_HOUR` to identify the metering window for each row.
- While a query is running, each metering-hour row is refreshed in-place with updated credit usage.
  When the query finishes, the final row for that metering hour is written and no longer changes.
- Until a query completes, the following columns can be NULL on in-progress rows: `WAREHOUSE_NAME`,
  `QUERY_START_TIME`, `QUERY_END_TIME`, `PARENT_QUERY_ID`, `ROOT_QUERY_ID`, `USER_NAME`, `ROLE_NAME`,
  `QUERY_HASH`, `QUERY_PARAMETERIZED_HASH`, and `QUERY_TAG`. After the query completes,
  `PARENT_QUERY_ID` and `ROOT_QUERY_ID` remain NULL when the query has no parent or is not part of a
  chain.
- Queries with extremely low or zero credit usage might not be included in the view.
- For aggregated warehouse credit usage (all warehouse types), use
  [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history).
- For per-query compute cost attribution on standard warehouses, use
  [QUERY\_ATTRIBUTION\_HISTORY view](/sql-reference/account-usage/query_attribution_history).

### Data freshness examples

**Query runs for one hour**

A query runs for an entire hour. The view contains one row for that metering hour. While the query
is running, that row is updated in-place with current credit usage. When the query finishes at the
end of the hour, that row is final.

**Query runs for multiple hours**

A query runs across multiple hours. The view contains one row per metering hour (`QUERY_METERING_HOUR`).
Each row follows the same in-place refresh behavior while the query is still running.

## Examples

The following example filters on `warehouse_name` and `query_start_time`, which excludes in-progress
rows where those columns are still NULL.

Return total credits used per query for an Adaptive Warehouse over the past 7 days:

Copy code

```
SELECT
  query_id,
  SUM(credits_used) AS total_credits_used,
  SUM(credits_used_compute) AS total_credits_used_compute,
  SUM(credits_used_cloud_services) AS total_credits_used_cloud_services
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_METERING_HISTORY
WHERE warehouse_name = 'my_adaptive_wh'
  AND query_start_time >= DATEADD(day, -7, CURRENT_DATE())
GROUP BY query_id
ORDER BY total_credits_used DESC;
```
