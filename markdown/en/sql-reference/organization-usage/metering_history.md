Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# METERING\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The METERING\_HISTORY view in the ORGANIZATION\_USAGE schema can be used to return the hourly credit usage for each account in the organization.

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
| SERVICE\_TYPE | VARCHAR | Type of service that is consuming credits. The following list includes many, **but not all**, of the possible service types:   - `AI_SERVICES`: See [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql) and [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst). - `ARCHIVE_STORAGE_RETRIEVAL_FILE_PROCESSING`: See [Billing for storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies-billing). - `ARCHIVE_STORAGE_WRITE`: See [Billing for storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies-billing). - `AUTO_CLUSTERING`: See [Automatic Clustering](/user-guide/tables-auto-reclustering). - `BACKUP`: See [Backups for disaster recovery and immutable storage](/user-guide/backups). - `COPY_FILES`: See [COPY FILES](/sql-reference/sql/copy-files). - `DATA_QUALITY_MONITORING`: See [Introduction to data quality checks](/user-guide/data-quality-intro). - `FAILSAFE_RECOVERY`: See [Understanding and viewing Fail-safe](/user-guide/data-failsafe). - `HYBRID_TABLE_REQUESTS`: See [Hybrid tables](/user-guide/tables-hybrid). - `MATERIALIZED_VIEW`: See [Working with Materialized Views](/user-guide/views-materialized). - `OPENFLOW_COMPUTE_BYOC`: See [Openflow BYOC cost and scaling considerations](/user-guide/data-integration/openflow/cost-byoc). - `OPENFLOW_COMPUTE_SNOWFLAKE`: See [Openflow Snowflake Deployment cost and scaling considerations](/user-guide/data-integration/openflow/cost-spcs). - `PIPE`: See [Snowpipe](/user-guide/data-load-snowpipe-intro). - `POSTGRES_COMPUTE`: See [Snowflake Postgres](/user-guide/snowflake-postgres/about). - `POSTGRES_COMPUTE_HA`: See [Snowflake Postgres](/user-guide/snowflake-postgres/about). - `QUERY_ACCELERATION`: See [Using the Query Acceleration Service (QAS)](/user-guide/query-acceleration-service). - `REPLICATION`: See [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro). - `SEARCH_OPTIMIZATION`: See [Search optimization service](/user-guide/search-optimization-service). - `SENSITIVE_DATA_CLASSIFICATION`: See [Introduction to sensitive data classification](/user-guide/classify-intro). - `SERVERLESS_ALERTS`: See [Setting up alerts based on data in Snowflake](/user-guide/alerts). - `SERVERLESS_TASK`: See [Introduction to tasks](/user-guide/tasks-intro). - `SNOWPARK_CONTAINER_SERVICES`: See [Snowpark Container Services](/developer-guide/snowpark-container-services/overview). - `SNOWPIPE_STREAMING`: See [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview). - `STORAGE_LIFECYCLE_POLICY_EXECUTION`: Compute cost to apply a policy on a target table and expire or archive rows (policy execution). See [Storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies). - `TELEMETRY_DATA_INGEST`: See [Event table overview](/developer-guide/logging-tracing/event-table-setting-up). - `TRUST_CENTER`: See [Trust Center](/user-guide/trust-center/overview). - `WAREHOUSE_METERING`: See [Overview of warehouses](/user-guide/warehouses-overview). - `WAREHOUSE_METERING_READER`: See [Manage reader accounts](/user-guide/data-sharing-reader-create). |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the usage took place. |
| ENTITY\_ID | NUMBER | A system-generated identifier for the entity associated with the service.  In most cases, this is the internal ID of the monitored entity; for example, a pipe, task, or replication group.  When the SERVICE\_TYPE is COPY\_FILES, this column shows the ID of the database, schema, or stage from which files are copied.  If the SERVICE\_TYPE is an Openflow type, the value is NULL.  If the SERVICE\_TYPE is Snowpipe Streaming, this shows the ID of the relevant pipe; which is the default pipe ID for the default pipe. |
| ENTITY\_TYPE | VARCHAR | Type of Snowflake resource that consumed credits, such as WAREHOUSE, TASK, or TABLE. Note that TABLE is used for all table-like objects. |
| NAME | VARCHAR | The name of the service or object associated with the cost entry, which varies significantly based on the SERVICE\_TYPE.  Standard (General): This column shows the name of the service type itself; for example, REPLICATION, TASK.  SNOWPIPE\_STREAMING: This service type generates two distinct cost entries, and the NAME column varies for each:   - Cost entry 1 (table name): The value is the name of the Snowflake target table. For the high-performance default pipe, the name is derived from the target table name and appended with -STREAMING; for example, MY\_TABLE-STREAMING. - Cost entry 2 (client string): The value is a colon-separated string in the format: SNOWPIPE\_STREAMING:CLIENT\_NAME:SNOWFLAKE\_PROVIDED\_ID. This is used for tracking client-side costs.   COPY\_FILES: The value is the name of the database from which the files are copied.  Openflow Types: The value is NULL. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier of the database associated with the resource of type `ENTITY_TYPE`. Contains a NULL value when the resource isn’t associated with a specific database; for example, a warehouse or compute pool. |
| DATABASE\_NAME | VARCHAR | Name of the database associated with the resource of type `ENTITY_TYPE`. Contains a NULL value when the resource isn’t associated with a specific database. |
| SCHEMA\_ID | NUMBER | Internal or system-generated identifier of the schema associated with the resource of type `ENTITY_TYPE`. Contains a NULL value when the resource isn’t associated with a specific schema. |
| SCHEMA\_NAME | VARCHAR | Name of the schema associated with the resource of type `ENTITY_TYPE`. Contains a NULL value when the resource isn’t associated with a specific schema. |
| CREDITS\_USED\_COMPUTE | NUMBER | Number of credits used by warehouses, serverless compute, and [Openflow](/user-guide/data-integration/openflow/about) resources in the hour. |
| CREDITS\_USED\_CLOUD\_ SERVICES | NUMBER | Number of credits used for cloud services in the hour. Always `0` when the SERVICE\_TYPE is one of the Openflow types. |
| CREDITS\_USED | NUMBER | Total number of credits used for the account in the hour. This is a sum of CREDITS\_USED\_COMPUTE and CREDITS\_USED\_CLOUD\_SERVICES. This value does not take into account the adjustment for cloud services, and may therefore be greater than your actual credit consumption. |
| BYTES | NUMBER | When the service type is `auto_clustering`, indicates the number of bytes reclustered during the START\_TIME and END\_TIME window. When the service type is `pipe`, indicates the number of bytes inserted during the START\_TIME and END\_TIME window. When the service type is `SNOWPIPE_STREAMING`, indicates the number of bytes migrated during the START\_TIME and END\_TIME window. When the service type is `COPY_FILES`, columns are aggregated at the database level. |
| ROWS | NUMBER | When the service type is `auto_clustering`, indicates number of rows reclustered during the START\_TIME and END\_TIME window. When the service type is `SNOWPIPE_STREAMING`, indicates the number of rows migrated during the START\_TIME and END\_TIME window. |
| FILES | NUMBER | When the service type is `pipe`, indicates number of files loaded during the START\_TIME and END\_TIME window. When the service type is `SNOWPIPE_STREAMING`, this is NULL. When the service type is `COPY_FILES`, columns are aggregated at the database level. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
