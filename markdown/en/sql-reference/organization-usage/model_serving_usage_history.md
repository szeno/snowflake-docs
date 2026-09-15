Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

# MODEL\_SERVING\_USAGE\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

This Organization Usage view can be used to query the estimated credit usage history for model serving (inference) workloads run through
the [Model Registry](/developer-guide/snowflake-ml/model-registry/overview) across all the accounts in your organization. The
view consolidates usage from both ways that a model can be served:

- **Warehouse**: The model function is called in a SQL query and runs as part of an ordinary warehouse operation.
- **Snowpark Container Services (SPCS)**: The model runs as an inference service or job deployed with `SYSTEM$DEPLOY_MODEL`. Estimated
  credit usage is based on the uptime of the SPCS service or job, regardless of whether it’s invoked through Python, REST, or a
  deployed service function.

Each row represents either an hour window of Snowpark Container Services usage for a model, or a single warehouse query that invoked
one or more model functions. For SPCS, the view emits one row per hour window during which the service or job ran. If a service or
job starts or ends partway through an hour, the row for that hour shows the estimated credits based only on the portion of the hour
the service or job was up.

Note

Because this view provides estimated credits, the values might not exactly match the credits billed on your usage statement.

See also:
:   [MODEL\_SERVING\_USAGE\_HISTORY view](/sql-reference/account-usage/model_serving_usage_history) (Account Usage)

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| INVOCATION\_TYPE | VARCHAR | How the model was served: SPCS or WAREHOUSE. |
| START\_TIME | TIMESTAMP\_LTZ | For SPCS rows, the start of the hour in which the usage took place. For warehouse rows, the time the query was submitted. |
| END\_TIME | TIMESTAMP\_LTZ | For SPCS rows, the end of the hour in which the usage took place. For warehouse rows, the time the query completed. |
| DATABASE\_ID | NUMBER | ID of the database containing the model. |
| DATABASE\_NAME | VARCHAR | Name of the database containing the model. |
| SCHEMA\_ID | NUMBER | ID of the schema containing the model. |
| SCHEMA\_NAME | VARCHAR | Name of the schema containing the model. |
| MODEL\_ID | NUMBER | ID of the model. |
| MODEL\_NAME | VARCHAR | Name of the model. |
| MODEL\_VERSION\_ID | NUMBER | ID of the model version. |
| MODEL\_VERSION\_NAME | VARCHAR | Name of the model version. |
| USER\_NAME | VARCHAR | Name of the user who ran the query that called the model function. NULL for SPCS rows. |
| CREDITS | NUMBER(38, 9) | Number of estimated credits attributed to the model serving usage. For SPCS rows, this is the sum of estimated credits attributed to the service for the hour. For warehouse rows, this is the query’s total estimated credits divided equally across the distinct model, model version, and function combinations that the query called. |
| COMPUTE\_POOL\_ID | NUMBER | ID of the compute pool running the service. NULL for warehouse rows. |
| COMPUTE\_POOL\_NAME | VARCHAR | Name of the compute pool running the service. NULL for warehouse rows. |
| SERVICE\_ID | NUMBER | ID of the Snowpark Container Services service or job running the model. NULL for warehouse rows. |
| SERVICE\_NAME | VARCHAR | Name of the Snowpark Container Services service or job running the model. NULL for warehouse rows. |
| WORKLOAD\_TYPE | VARCHAR | For SPCS rows, SERVICE (a long-lived service, such as an online inference service or a model build) or JOB (a one-shot job, such as a batch inference job). For warehouse rows, always WAREHOUSE\_INFERENCE. |
| FUNCTION\_NAME | VARCHAR | Name of the model function invoked (for example, PREDICT). NULL for SPCS rows. |
| QUERY\_ID | VARCHAR | ID of the query that called the model function. NULL for SPCS rows. |
| WAREHOUSE\_ID | NUMBER | ID of the warehouse that ran the query. NULL for SPCS rows. |
| QUERY\_TAG | VARCHAR | Query tag, if any, associated with the query that called the model function. NULL for SPCS rows. |

Expand

Show lessSee more

## Usage notes

- Usage that occurred before August 25, 2026 might be included, but historical data prior to this date isn’t guaranteed to be complete.
- Latency for the view might be up to 24 hours.
- For SPCS rows, a row is emitted only for hours in which the service was up and had a nonzero amount of estimated credits
  attributed to it. If the service wasn’t running during an hour, no row is emitted for that hour.
- For SPCS rows, the estimated credits shown are an attribution of compute pool usage to a model, not a precise, standalone
  charge. The actual charge comes from the compute pool itself; see
  [SNOWPARK\_CONTAINER\_SERVICES\_HISTORY](/sql-reference/organization-usage/snowpark_container_services_history). So if a compute
  pool runs only ML models, the sum of the estimated credits attributed to those models won’t equal the compute pool’s total
  cost, because compute pools also accrue idle time.
- For warehouse rows, a row appears only after the query completes successfully and its estimated credits have settled in
  [QUERY\_ATTRIBUTION\_HISTORY](/sql-reference/organization-usage/query_attribution_history) for classic warehouses or
  [QUERY\_METERING\_HISTORY](/sql-reference/organization-usage/query_metering_history) for adaptive warehouses.
- For warehouse rows, repeated calls to the same model, model version, and function within a single query are deduplicated into
  a single row. A query that calls multiple distinct model, model version, and function combinations produces one row per
  combination, with the query’s estimated credits split equally across them.
- This view doesn’t include model import jobs, for example, jobs created by `SYSTEM$IMPORT_MODEL` or the import step that
  `SYSTEM$DEPLOY_MODEL` runs before deploying an inference service.

## Examples

Retrieve model serving usage history across all accounts in the organization:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ORGANIZATION_USAGE.MODEL_SERVING_USAGE_HISTORY;
```

```
+-------------------+-----------------+--------------+-----------------+-------------------------------+-------------------------------+-------------+---------------+-----------+-------------+----------+------------------+------------------+--------------------+-----------+-------------+-----------------+-------------------+------------+---------------------+---------------------+---------------+--------------------------------------+--------------+-----------+
| ORGANIZATION_NAME | ACCOUNT_LOCATOR | ACCOUNT_NAME | INVOCATION_TYPE | START_TIME                    | END_TIME                      | DATABASE_ID | DATABASE_NAME | SCHEMA_ID | SCHEMA_NAME | MODEL_ID | MODEL_NAME       | MODEL_VERSION_ID | MODEL_VERSION_NAME | USER_NAME | CREDITS     | COMPUTE_POOL_ID | COMPUTE_POOL_NAME | SERVICE_ID | SERVICE_NAME        | WORKLOAD_TYPE       | FUNCTION_NAME | QUERY_ID                             | WAREHOUSE_ID | QUERY_TAG |
+-------------------+-----------------+--------------+-----------------+-------------------------------+-------------------------------+-------------+---------------+-----------+-------------+----------+------------------+------------------+--------------------+-----------+-------------+-----------------+-------------------+------------+---------------------+---------------------+---------------+--------------------------------------+--------------+-----------+
| MY_ORG            | AB12345         | MY_ACCOUNT   | SPCS            | 2026-08-20 14:00:00.000 +0000 | 2026-08-20 15:00:00.000 +0000 | 154         | ML_MODELS     | 2201      | PUBLIC      | 5001     | FRAUD_DETECTION  | 8001             | V1                 | NULL      | 0.041666667 | 301             | ML_INFERENCE_POOL | 4021       | FRAUD_DETECTION_SVC | SERVICE             | NULL          | NULL                                 | NULL         | NULL      |
+-------------------+-----------------+--------------+-----------------+-------------------------------+-------------------------------+-------------+---------------+-----------+-------------+----------+------------------+------------------+--------------------+-----------+-------------+-----------------+-------------------+------------+---------------------+---------------------+---------------+--------------------------------------+--------------+-----------+
| MY_ORG            | AB12345         | MY_ACCOUNT   | WAREHOUSE       | 2026-08-20 15:32:10.123 +0000 | 2026-08-20 15:32:12.456 +0000 | 154         | ML_MODELS     | 2201      | PUBLIC      | 5002     | CHURN_PREDICTION | 8002             | V2                 | JSMITH    | 0.000123000 | NULL            | NULL              | NULL       | NULL                | WAREHOUSE_INFERENCE | PREDICT       | 01b2c3d4-0001-1234-0000-0001abcd0002 | 21           | NULL      |
+-------------------+-----------------+--------------+-----------------+-------------------------------+-------------------------------+-------------+---------------+-----------+-------------+----------+------------------+------------------+--------------------+-----------+-------------+-----------------+-------------------+------------+---------------------+---------------------+---------------+--------------------------------------+--------------+-----------+
```
