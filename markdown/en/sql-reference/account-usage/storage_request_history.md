Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# STORAGE\_REQUEST\_HISTORY view

This Account Usage view displays historical data for storage request usage within the last 365 days (1 year).
The view tracks HTTP requests made by external query engines through
[Snowflake Horizon Catalog](/user-guide/snowflake-horizon) to access
[Iceberg tables that use Snowflake storage](/user-guide/tables-iceberg-internal-storage).

See also:
:   [Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the data aggregation window. |
| END\_TIME | TIMESTAMP\_LTZ | End of the data aggregation window. |
| OPERATION\_TYPE | VARCHAR | The type of operation: `Class 1` (PUT, COPY, POST, PATCH, and LIST operations) or `Class 2` (GET and SELECT operations). |
| COUNT | NUMBER | Total number of API calls during the aggregation window. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 6 hours.
- This view tracks requests that are billed under the `STORAGE_REQUEST-1` (Class 1) and
  `STORAGE_REQUEST-2` (Class 2) SKUs on the billing report.
- This view only tracks requests for Iceberg tables that use Snowflake storage. For Iceberg tables
  that use customer-owned external storage (buckets), this view doesn’t apply.
- Snowflake doesn’t bill your account when you use the Snowflake query engine to directly access
  Iceberg tables. Only requests made through Horizon Catalog by external query engines are tracked
  in this view.
- For billing rates, see Table 3(g) of the
  [Snowflake service consumption table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Examples

Retrieve the storage request counts for the past 7 days:

Copy code

```
SELECT
  START_TIME,
  END_TIME,
  OPERATION_TYPE,
  COUNT
FROM SNOWFLAKE.ACCOUNT_USAGE.STORAGE_REQUEST_HISTORY
WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
ORDER BY START_TIME DESC;
```

Calculate total requests by operation type for the past month:

Copy code

```
SELECT
  OPERATION_TYPE,
  SUM(COUNT) AS TOTAL_REQUESTS
FROM SNOWFLAKE.ACCOUNT_USAGE.STORAGE_REQUEST_HISTORY
WHERE START_TIME >= DATEADD(month, -1, CURRENT_TIMESTAMP())
GROUP BY OPERATION_TYPE;
```
