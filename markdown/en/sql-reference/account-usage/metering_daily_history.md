Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# METERING\_DAILY\_HISTORY view

The METERING\_DAILY\_HISTORY view in the ACCOUNT\_USAGE schema can be used to return the daily credit usage and a cloud services rebate for an account within the last 365 days (1 year).

Note

As of March 1, 2026, Snowflake no longer bills customers for hybrid table requests,
and metering was disabled soon after this pricing change took effect. Any new data
in the view as of March 1, 2026, will not be billed to customers, and you can still
query the historical data in the view.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| SERVICE\_TYPE | VARCHAR | Type of service that is consuming credits. The following list includes many, **but not all**, of the possible service types:   - `AI_SERVICES`: See [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql) and [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst). - `ARCHIVE_STORAGE_RETRIEVAL_FILE_PROCESSING`: See [Billing for storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies-billing). - `ARCHIVE_STORAGE_WRITE`: See [Billing for storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies-billing). - `AUTO_CLUSTERING`: See [Automatic Clustering](/user-guide/tables-auto-reclustering). - `BACKUP`: See [Backups for disaster recovery and immutable storage](/user-guide/backups). - `COPY_FILES`: See [COPY FILES](/sql-reference/sql/copy-files). - `CORTEX_CODE_CLI`: See [CoCo CLI](/user-guide/cortex-code/cortex-code-cli). - `CORTEX_CODE_SNOWSIGHT`: See [CoCo in Snowsight](/user-guide/cortex-code/cortex-code-snowsight). - `DATA_QUALITY_MONITORING`: See [Introduction to data quality checks](/user-guide/data-quality-intro). - `FAILSAFE_RECOVERY`: See [Understanding and viewing Fail-safe](/user-guide/data-failsafe). - `HYBRID_TABLE_REQUESTS`: See [Hybrid tables](/user-guide/tables-hybrid). - `MATERIALIZED_VIEW`: See [Working with Materialized Views](/user-guide/views-materialized). - `OPENFLOW_COMPUTE_BYOC`: See [Openflow BYOC cost and scaling considerations](/user-guide/data-integration/openflow/cost-byoc). - `OPENFLOW_COMPUTE_SNOWFLAKE`: See [Openflow Snowflake Deployment cost and scaling considerations](/user-guide/data-integration/openflow/cost-spcs). - `PIPE`: See [Snowpipe](/user-guide/data-load-snowpipe-intro). - `POSTGRES_COMPUTE`: See [Snowflake Postgres](/user-guide/snowflake-postgres/about). - `POSTGRES_COMPUTE_HA`: See [Snowflake Postgres](/user-guide/snowflake-postgres/about). - `QUERY_ACCELERATION`: See [Using the Query Acceleration Service (QAS)](/user-guide/query-acceleration-service). - `REPLICATION`: See [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro). - `SEARCH_OPTIMIZATION`: See [Search optimization service](/user-guide/search-optimization-service). - `SENSITIVE_DATA_CLASSIFICATION`: See [Introduction to sensitive data classification](/user-guide/classify-intro). - `SERVERLESS_ALERTS`: See [Setting up alerts based on data in Snowflake](/user-guide/alerts). - `SERVERLESS_TASK`: See [Introduction to tasks](/user-guide/tasks-intro). - `SNOWPARK_CONTAINER_SERVICES`: See [Snowpark Container Services](/developer-guide/snowpark-container-services/overview). - `SNOWPIPE_STREAMING`: See [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview). - `STORAGE_LIFECYCLE_POLICY_EXECUTION`: Compute cost to apply a policy on a target table and expire or archive rows (policy execution). See [Storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies). - `TELEMETRY_DATA_INGEST`: See [Event table overview](/developer-guide/logging-tracing/event-table-setting-up). - `TRUST_CENTER`: See [Trust Center](/user-guide/trust-center/overview). - `WAREHOUSE_METERING`: See [Overview of warehouses](/user-guide/warehouses-overview). - `WAREHOUSE_METERING_READER`: See [Manage reader accounts](/user-guide/data-sharing-reader-create). |
| USAGE\_DATE | DATE | Date when the usage took place. |
| CREDITS\_USED\_COMPUTE | NUMBER | Number of credits billed for warehouses, serverless compute, and [Openflow](/user-guide/data-integration/openflow/about) resources in the day. |
| CREDITS\_USED\_CLOUD\_SERVICES | NUMBER | Number of credits billed for cloud services in the day. Always *0* when the SERVICE\_TYPE is one of the Openflow types. |
| CREDITS\_USED | NUMBER | Sum of CREDITS\_USED\_COMPUTE and CREDITS\_USED\_CLOUD\_SERVICES. |
| CREDITS\_ADJUSTMENT\_CLOUD\_SERVICES | NUMBER | Number of credits [adjusted for cloud services](/user-guide/cost-understanding-compute#label-understanding-billing-for-cloud-services-usage). This is a negative value (e.g. `-9`). |
| CREDITS\_BILLED | NUMBER | Total number of credits billed for the account in the day. This is a sum of CREDITS\_USED\_COMPUTE, CREDITS\_USED\_CLOUD\_SERVICES, and CREDITS\_ADJUSTMENT\_CLOUD\_SERVICES. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- If you want to reconcile the data in this view with a corresponding view in the [ORGANIZATION USAGE schema](/sql-reference/organization-usage), you must first set the timezone of the session to UTC. Before querying the Account Usage view, execute:

  > Copy code
  >
  > ```
  > ALTER SESSION SET TIMEZONE = UTC;
  > ```

## Example

[Usage for cloud services](/user-guide/cost-understanding-compute#label-understanding-billing-for-cloud-services-usage) is billed only if the daily consumption of cloud
services exceeds 10% of the daily usage of virtual warehouses. This query returns how much of cloud services consumption was actually
billed for a particular day, ordered by the highest billed amount.

Copy code

```
SELECT
    usage_date,
    credits_used_cloud_services,
    credits_adjustment_cloud_services,
    credits_used_cloud_services + credits_adjustment_cloud_services AS billed_cloud_services
FROM snowflake.account_usage.metering_daily_history
WHERE usage_date >= DATEADD(month,-1,CURRENT_TIMESTAMP())
    AND credits_used_cloud_services > 0
ORDER BY 4 DESC;
```
