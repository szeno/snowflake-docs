Schema:
:   [DATA\_SHARING\_USAGE](/sql-reference/data-sharing-usage)

# PROVIDER\_APPLICATION\_DAILY\_USAGE\_HISTORY view

Use this view to analyze the daily credit and storage usage for each consumer account of your Snowflake Native App listings. The view returns a record for each
consumer account that had credit or storage activity for a given date.

## Columns

The following table provides definitions for the columns in this view:

**PROVIDER\_APPLICATION\_DAILY\_USAGE\_HISTORY**

| Field | Type | Description |
| --- | --- | --- |
| CONSUMER\_SNOWFLAKE\_REGION | VARCHAR | Snowflake Region where the consumer account is located. |
| CONSUMER\_ORGANIZATION\_NAME | VARCHAR | Organization name of the consumer account. |
| CONSUMER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the consumer account. |
| CONSUMER\_ACCOUNT\_NAME | VARCHAR | Account name of the consumer account. |
| APPLICATION\_NAME\_HASH | VARCHAR | A hash that uniquely identifies the application installation on the consumer account. This value matches the result of the [SYSTEM$GET\_HASH\_FOR\_APPLICATION](/sql-reference/functions/system_get_hash_for_application) function, which consumers can call to look up the hash for their installed application. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global name of the listing associated with the application. |
| USAGE\_DATE | DATE | The date the usage occurred. |
| CREDITS\_USED | NUMBER | Daily total credits consumed by the Snowflake Native App in the consumer account. |
| CREDITS\_USED\_BREAKDOWN | ARRAY | An array of objects identifying the Snowflake service and credits consumed. See [CREDITS\_USED\_BREAKDOWN array](/sql-reference/data-sharing-usage/provider-application-daily-usage-history#label-credits-used-breakdown-array) for formatting. |
| STORAGE\_BYTES | NUMBER | Daily average storage bytes used by the Snowflake Native App in the consumer account. |
| STORAGE\_BYTES\_BREAKDOWN | ARRAY | An array of objects identifying the type and number of storage bytes used. See [STORAGE\_BYTES\_BREAKDOWN array](/sql-reference/data-sharing-usage/provider-application-daily-usage-history#label-storage-bytes-breakdown-array) for formatting. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 2 days.
- The data is retained for 365 days (1 year).
- The view only returns data for listings owned by the current account.

### CREDITS\_USED\_BREAKDOWN array

The CREDITS\_USED\_BREAKDOWN array provides details about the services that consumed daily credits.

Example:

Copy code

```
[
  {
    "Credits": 0.005840921,
    "ServiceType": "AUTO_CLUSTERING"
  },
  {
    "Credits": 0.115940725,
    "ServiceType": "SERVERLESS_TASK"
  }
]
```

The following table provides descriptions for the key-value pairs in the objects in the array.

| Field | Data type | Description |
| --- | --- | --- |
| `Credits` | DECIMAL | Number of credits consumed by the service type specified by `ServiceType` on the usage date. |
| `ServiceType` | VARCHAR | The service type, which can be one of the following values:   - `AUTO_CLUSTERING`: See [Automatic Clustering](/user-guide/tables-auto-reclustering). - `DATA_QUALITY_MONITORING`: See [Introduction to data quality checks](/user-guide/data-quality-intro). - `MATERIALIZED_VIEW`: See [Working with Materialized Views](/user-guide/views-materialized). - `PIPE`: See [Snowpipe](/user-guide/data-load-snowpipe-intro). - `SEARCH_OPTIMIZATION`: See [Search optimization service](/user-guide/search-optimization-service). - `SERVERLESS_TASK`: See [Introduction to tasks](/user-guide/tasks-intro). - `SNOWPARK_CONTAINER_SERVICES`: See [Snowpark Container Services](/developer-guide/snowpark-container-services/overview). - `WAREHOUSE_METERING`: See [Overview of warehouses](/user-guide/warehouses-overview). |

Expand

Show lessSee more

The following are used in the determination of credit consumption:

- The credits used by objects in the Snowflake Native App. For example, auto-clustering on tables in the Snowflake Native App.
- The credits used by the warehouses owned by the Snowflake Native App.
- The credits used by the compute pools dedicated to the Snowflake Native App.

### STORAGE\_BYTES\_BREAKDOWN array

The STORAGE\_BYTES\_BREAKDOWN array provides details about the storage types that consumed storage.

Example:

Copy code

```
[
  {
    "Bytes": 34043221,
    "ServiceType": "DATABASE"
  },
  {
    "Bytes": 109779541,
    "ServiceType": "FAILSAFE"
  }
]
```

The following table provides descriptions for the key-value pairs in the objects in the array.

| Field | Data type | Description |
| --- | --- | --- |
| `Bytes` | INTEGER | Number of storage bytes used. |
| `ServiceType` | VARCHAR | The storage type, which can be one of the following values:   - `DATABASE`: Database storage. - `FAILSAFE`: [Fail-safe storage](/user-guide/data-failsafe). - `HYBRID_TABLE`: Storage for [hybrid tables](/user-guide/tables-hybrid). |

Expand

Show lessSee more

Only data stored in the Snowflake Native App is used to determine storage byte consumption.
External databases created by the Snowflake Native App are not included in the determination of this value.

## Examples

Shows top applications by credit usage for the last month:

Copy code

```
SELECT
  application_name_hash,
  consumer_account_name,
  consumer_organization_name,
  SUM(credits_used) AS total_credits
FROM snowflake.data_sharing_usage.provider_application_daily_usage_history
WHERE usage_date >= DATEADD(month, -1, CURRENT_DATE())
GROUP BY 1, 2, 3
ORDER BY total_credits DESC;
```

Shows credit and storage consumption per application with the number of distinct consumer accounts for the last month:

Copy code

```
SELECT
  application_name_hash,
  SUM(credits_used)                        AS total_credits,
  SUM(storage_bytes)                       AS total_storage_bytes,
  COUNT(DISTINCT consumer_account_locator) AS unique_consumers
FROM snowflake.data_sharing_usage.provider_application_daily_usage_history
WHERE usage_date >= DATEADD(month, -1, CURRENT_DATE())
GROUP BY 1
ORDER BY total_credits DESC;
```
