# Account Usage

In the SNOWFLAKE database, the ACCOUNT\_USAGE and READER\_ACCOUNT\_USAGE schemas enable querying object metadata, as well as historical
usage data, for your account and all reader accounts (if any) associated with the account.

## Overview of Account Usage schemas

ACCOUNT\_USAGE:
:   Views that display object metadata and usage metrics for your account.

    In general, these views mirror the corresponding views and table functions in the Snowflake [Snowflake Information Schema](/sql-reference/info-schema), but
    with the following differences:

    - Records for dropped objects are included in each view.
    - Longer retention time for historical usage data.
    - Data latency.

    For more details, see [Differences Between Account Usage and Information Schema](#differences-between-account-usage-and-information-schema) (in this topic). For more details about each
    view, see [ACCOUNT\_USAGE Views](#account-usage-views) (in this topic).

READER\_ACCOUNT\_USAGE:
:   Views that display object metadata and usage metrics for all the reader accounts that have been created for
    your account (as a [Secure Data Sharing](/guides-overview-sharing) provider).

    These views are a small subset of the ACCOUNT\_USAGE views that apply to reader accounts. Also, each view in this schema contains an
    additional `READER_ACCOUNT_NAME` column for filtering results by reader account.

    For more details about each view, see [READER\_ACCOUNT\_USAGE Views](#reader-account-usage-views) (in this topic).

    Note that these views are empty if no reader accounts have been created for your account.

## Differences between Account Usage and Information Schema

The Account Usage views and the corresponding views (or table functions) in the [Snowflake Information Schema](/sql-reference/info-schema) utilize identical
structures and naming conventions, but with some key differences, as described in this section:

| Difference | Account Usage | Information Schema |
| --- | --- | --- |
| Includes dropped objects | Yes | No |
| Latency of data | From 45 minutes to 3 hours (varies by view) | None |
| Retention of historical data | 1 year | From 7 days to 6 months (varies by view/table function) |

Expand

Show lessSee more

For more details, see the following sections.

### Dropped object records

Account usage views include records for all objects that have been dropped. Many of the views for object types contain an
additional `DELETED` column that displays the timestamp when the object was dropped.

In addition, because objects can be dropped and recreated with the same name, to differentiate between object records that have the
same name, the account usage views include ID columns, where appropriate, that display the internal IDs generated and assigned to
each record by the system.

If a column for an object name (for example, the `TABLE_NAME` column) is NULL, that object has been dropped. In this case, the
columns for the names and IDs of the parent objects (for example, the `DATABASE_NAME` and `SCHEMA_NAME` columns) are also
NULL.

Note that in some views, the column for the object name might still contain the name of the object, even if the object has been
dropped.

### Data latency

Due to the process of extracting the data from Snowflake’s internal metadata store, the account usage views have some natural latency:

- For most of the views, the latency is 2 hours (120 minutes).
- For the remaining views, the latency varies between 45 minutes and 3 hours.

For details, see the list of views for each schema (in this topic). Also, note that these are all maximum time lengths; the actual
latency for a given view when the view is queried may be less.

In contrast, views/table functions in the [Snowflake Information Schema](/sql-reference/info-schema) do not have any latency.

### Historical data retention

Certain account usage views provide historical usage metrics. The retention period for these views is 1 year (365 days).

In contrast, the corresponding views and table functions in the [Snowflake Information Schema](/sql-reference/info-schema) have much shorter retention periods,
ranging from 7 days to 6 months, depending on the view.

## ACCOUNT\_USAGE views

The ACCOUNT\_USAGE schema contains the following views:

| View | Type | Latency [1] | Edition [3] | Notes |
| --- | --- | --- | --- | --- |
| [ACCESS\_HISTORY](/sql-reference/account-usage/access_history) | Historical | 3 hours | Enterprise Edition (or higher) | Data retained for 1 year. |
| [AGGREGATE\_ACCESS\_HISTORY](/sql-reference/account-usage/aggregate_access_history) | Historical | 3 hours | Enterprise Edition (or higher) | Data retained for 1 year. |
| [AGGREGATE\_QUERY\_HISTORY](/sql-reference/account-usage/aggregate_query_history) | Historical | 3 hours |  |  |
| [AGGREGATION\_POLICIES](/sql-reference/account-usage/aggregation_policies) | Object | 2 hours |  |  |
| [ALERT\_HISTORY](/sql-reference/account-usage/alert_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [ANOMALIES\_DAILY](/sql-reference/account-usage/anomalies_daily) | Historical | 3 hours |  | Data retained for 1 year. |
| [APPLICATION\_CALLBACK\_HISTORY](/sql-reference/account-usage/application_callback_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [APPLICATION\_CONFIGURATIONS](/sql-reference/account-usage/application_configurations) | Object | 3 hours |  | Data retained for 1 year. |
| [APPLICATION\_CONFIGURATION\_VALUE\_HISTORY](/sql-reference/account-usage/application_configuration_value_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [APPLICATION\_DAILY\_USAGE\_HISTORY](/sql-reference/account-usage/application_daily_usage_history) | Historical | 24 hours |  | Data retained for 1 year. |
| [APPLICATION\_REMOTE\_OPERATION\_HISTORY](/sql-reference/account-usage/application_remote_operation_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [APPLICATION\_SPECIFICATION\_STATUS\_HISTORY](/sql-reference/account-usage/application_specification_status_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [APPLICATION\_SPECIFICATIONS](/sql-reference/account-usage/application_specifications) | Historical | 1 hour |  | Data for deleted app specifications is retained for 1 year. |
| [ARCHIVE\_STORAGE\_DATA\_RETRIEVAL\_USAGE\_HISTORY](/sql-reference/account-usage/archive_storage_data_retrieval_usage_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [AUTOMATIC\_CLUSTERING\_HISTORY](/sql-reference/account-usage/automatic_clustering_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [BACKUP\_OPERATION\_HISTORY](/sql-reference/account-usage/backup_operation_history) | Historical | 6 hours |  | Data retained for 1 year. |
| [BACKUP\_POLICIES](/sql-reference/account-usage/backup_policies) | Object | 6 hours |  |  |
| [BACKUP\_SETS](/sql-reference/account-usage/backup_sets) | Object | 6 hours |  |  |
| [BACKUP\_STORAGE\_USAGE](/sql-reference/account-usage/backup_storage_usage) | Historical | 6 hours |  | Data retained for 1 year. |
| [BACKUPS](/sql-reference/account-usage/backups) | Object | 6 hours |  |  |
| [BLOCK\_STORAGE\_HISTORY](/sql-reference/account-usage/block_storage_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [BLOCK\_STORAGE\_SNAPSHOTS](/sql-reference/account-usage/block_storage_snapshots) | Object | 3 hours |  |  |
| [CATALOG\_LINKED\_DATABASE\_USAGE\_HISTORY](/sql-reference/account-usage/catalog_linked_database_usage_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [CLASS\_INSTANCES](/sql-reference/account-usage/class_instances) | Object | 3 hours |  | Data retained for 1 year. |
| [CLASSES](/sql-reference/account-usage/classes) | Object | 3 hours |  | Data retained for 1 year. |
| [COLUMN\_QUERY\_PRUNING\_HISTORY](/sql-reference/account-usage/column_query_pruning_history) | Historical | 4 hours |  | Data retained for 1 year. |
| [COLUMNS](/sql-reference/account-usage/columns) | Object | 90 minutes |  |  |
| [COMPLETE\_TASK\_GRAPHS](/sql-reference/account-usage/complete_task_graphs) | Historical | 45 minutes |  | Data retained for 1 year. |
| [COMPUTE\_POOLS](/sql-reference/account-usage/compute_pools) | Historical | 3 hours |  | Data retained for 1 year. |
| [CONTACT\_REFERENCES](/sql-reference/account-usage/contact_references) | Object | 3 hours |  |  |
| [CONTACTS](/sql-reference/account-usage/contacts) | Object | 3 hours |  |  |
| [COPY\_FILES\_HISTORY](/sql-reference/account-usage/copy_files_history) | Historical |  |  | Data retained for 1 year. |
| [COPY\_HISTORY](/sql-reference/account-usage/copy_history) | Historical | 2 hours [2] |  | Data retained for 1 year. |
| [CORTEX\_AGENT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_agent_usage_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_ai_functions_usage_history) | Historical |  |  | Data retained for 1 year. |
| [CORTEX\_AI\_GUARDRAILS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_ai_guardrails_usage_history) | Historical |  |  | Data retained for 1 year. |
| [CORTEX\_AISQL\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_aisql_usage_history) | Historical |  |  | Data retained for 1 year. |
| [CORTEX\_CODE\_CLI\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_code_cli_usage_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [CORTEX\_CODE\_SNOWSIGHT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_code_snowsight_usage_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [CORTEX\_ANALYST\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_analyst_usage_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [CORTEX\_DOCUMENT\_PROCESSING\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_document_processing_usage_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [CORTEX\_FINE\_TUNING\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_fine_tuning_usage_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [CORTEX\_FUNCTIONS\_QUERY\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_functions_query_usage_history) | Historical |  |  | Data retained for 1 year. |
| [CORTEX\_FUNCTIONS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_functions_usage_history) | Historical |  |  | Data retained for 1 year. |
| [CORTEX\_PROVISIONED\_THROUGHPUT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_provisioned_throughput_usage_history) | Historical |  |  | Data retained for 1 year. |
| [CORTEX\_REST\_API\_RATE\_LIMIT\_POLICIES](/sql-reference/account-usage/cortex_rest_api_rate_limit_policies) | Object | 6 hours |  |  |
| [CORTEX\_REST\_API\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_rest_api_usage_history) | Historical |  |  | Data retained for 1 year. |
| [CORTEX\_SEARCH\_BATCH\_QUERY\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_search_batch_query_usage_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [CORTEX\_SEARCH\_DAILY\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_search_daily_usage_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [CORTEX\_SEARCH\_SERVING\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_search_serving_usage_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [CREDENTIALS](/sql-reference/account-usage/credentials) | Object | 2 hours |  |  |
| [DATA\_CLASSIFICATION\_HISTORY](/sql-reference/account-usage/data_classification_history) | Historical | 3 hours | Enterprise Edition (or higher) | Data retained for 1 year. |
| [DATA\_CLASSIFICATION\_LATEST](/sql-reference/account-usage/data_classification_latest) | Object | 3 hours | Enterprise Edition (or higher) | Data retained for as long as the table exists. |
| [DATA\_METRIC\_FUNCTION\_EXPECTATIONS](/sql-reference/account-usage/data_metric_function_expectations) | Object | 30 minutes | Enterprise Edition (or higher) |  |
| [DATA\_METRIC\_FUNCTION\_REFERENCES](/sql-reference/account-usage/data_metric_function_references) | Object | 3 hours | Enterprise Edition (or higher) |  |
| [DATA\_MOVEMENT\_POLICIES](/sql-reference/account-usage/data_movement_policies) | Object | 2 hours |  |  |
| [DATA\_MOVEMENT\_POLICY\_RULES](/sql-reference/account-usage/data_movement_policy_rules) | Object | 2 hours |  |  |
| [DATA\_MOVEMENT\_RULE\_REFERENCES](/sql-reference/account-usage/data_movement_rule_references) | Historical | 3 hours |  |  |
| [DATA\_MOVEMENT\_VIOLATIONS](/sql-reference/account-usage/data_movement_violations) | Historical | 3 hours |  | Data is retained for one year. |
| [DATA\_QUALITY\_MONITORING\_USAGE\_HISTORY](/sql-reference/account-usage/data_quality_monitoring_usage_history) | Historical | 3 hours | Enterprise Edition (or higher) | Data retained for 1 year. |
| [DATABASES](/sql-reference/account-usage/databases) | Object | 3 hours |  |  |
| [DATABASE\_REPLICATION\_USAGE\_HISTORY](/sql-reference/account-usage/database_replication_usage_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [DATABASE\_STORAGE\_USAGE\_HISTORY](/sql-reference/account-usage/database_storage_usage_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [DATA\_TRANSFER\_HISTORY](/sql-reference/account-usage/data_transfer_history) | Historical | 2 hours |  | Data retained for 1 year. |
| [DBT\_PROJECT\_EXECUTION\_HISTORY](/sql-reference/account-usage/dbt_project_execution_history) | Historical | 2 hours |  | Data retained for 1 year. |
| [DOCUMENT\_AI\_USAGE\_HISTORY](/sql-reference/account-usage/document_ai_usage_history) | Historical |  |  | Data retained for 1 year. |
| [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/account-usage/dynamic_table_refresh_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [ELEMENT\_TYPES](/sql-reference/account-usage/element_types) | Object | 90 minutes |  |  |
| [EVENT\_ROUTING\_TABLES](/sql-reference/account-usage/event_routing_tables) | Object | 2 hours |  |  |
| [EVENT\_USAGE\_HISTORY](/sql-reference/account-usage/event_usage_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [EXTERNAL\_ACCESS\_HISTORY](/sql-reference/account-usage/external_access_history) | Historical | 2 hours |  | Data retained for 1 year. |
| [FIELDS](/sql-reference/account-usage/fields) | Object | 90 minutes |  |  |
| [FILE\_FORMATS](/sql-reference/account-usage/file_formats) | Object | 2 hours |  |  |
| [FUNCTIONS](/sql-reference/account-usage/functions) | Object | 2 hours |  |  |
| [GRANTS\_TO\_ROLES](/sql-reference/account-usage/grants_to_roles) | Object | 2 hours |  |  |
| [GRANTS\_TO\_SHARES](/sql-reference/account-usage/grants_to_shares) | Object | 3 hours |  |  |
| [GRANTS\_TO\_USERS](/sql-reference/account-usage/grants_to_users) | Object | 2 hours |  |  |
| [HYBRID\_TABLES](/sql-reference/account-usage/hybrid_tables) | Object | 3 hours |  |  |
| [HYBRID\_TABLE\_USAGE\_HISTORY](/sql-reference/account-usage/hybrid_table_usage_history) | Historical | 3 hours |  | Data retained for 1 year. (As of March 1, 2026, hybrid table requests are no longer billed, and metering was disabled soon after this pricing change took effect.) |
| [ICEBERG\_STORAGE\_OPTIMIZATION\_HISTORY](/sql-reference/account-usage/iceberg_storage_optimization_history) | Historical | 2 hours |  | Data retained for 1 year. |
| [INDEX\_COLUMNS](/sql-reference/account-usage/index_columns) | Object | 3 hours |  |  |
| [INDEXES](/sql-reference/account-usage/indexes) | Object | 3 hours |  |  |
| [INGRESS\_NETWORK\_ACCESS\_HISTORY](/sql-reference/account-usage/ingress_network_access_history) | Historical | 4 hours |  | Data retained for 1 year. |
| [INTERNAL\_DATA\_TRANSFER\_HISTORY](/sql-reference/account-usage/internal_data_transfer_history) | Historical | 3 hours |  |  |
| [INTERNAL\_STAGE\_NETWORK\_ACCESS\_HISTORY](/sql-reference/account-usage/internal_stage_network_access_history) | Historical | 6 hours |  | Data retained for 1 year. |
| [JOIN\_POLICIES](/sql-reference/account-usage/join_policies) | Object | 2 hours |  |  |
| [LISTINGS](/sql-reference/account-usage/listings) | Object | 3 hours |  |  |
| [LOAD\_HISTORY](/sql-reference/account-usage/load_history) | Historical | 90 minutes [2] |  | Data retained for 1 year. |
| [LOCK\_WAIT\_HISTORY](/sql-reference/account-usage/lock_wait_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [LOGIN\_HISTORY](/sql-reference/account-usage/login_history) | Historical | 2 hours |  | Data retained for 1 year. |
| [MASKING\_POLICIES](/sql-reference/account-usage/masking_policies) | Object | 2 hours |  |  |
| [MATERIALIZED\_VIEW\_REFRESH\_HISTORY](/sql-reference/account-usage/materialized_view_refresh_history) | Historical | 3 hours | Enterprise Edition (or higher) | Data retained for 1 year. |
| [METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [METERING\_HISTORY](/sql-reference/account-usage/metering_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [MODEL\_SERVING\_USAGE\_HISTORY](/sql-reference/account-usage/model_serving_usage_history) | Historical |  |  | Data retained for 1 year. |
| [NETWORK\_POLICIES](/sql-reference/account-usage/network_policies) | Object | 2 hours |  |  |
| [NETWORK\_RULE\_REFERENCES](/sql-reference/account-usage/network_rule_references) | Object | 2 hours |  |  |
| [NETWORK\_RULES](/sql-reference/account-usage/network_rules) | Object | 2 hours |  |  |
| [NOTEBOOKS\_CONTAINER\_RUNTIME\_HISTORY](/sql-reference/account-usage/notebooks_container_runtime_history) | Historical | 3 hours |  |  |
| [OBJECT\_ACCESS\_REQUEST\_HISTORY](/sql-reference/account-usage/object_access_request_history) | Historical | 3 hours |  |  |
| [OBJECT\_DEPENDENCIES](/sql-reference/account-usage/object_dependencies) | Historical | 3 hours |  |  |
| [ONLINE\_FEATURE\_TABLE\_REFRESH\_HISTORY](/sql-reference/account-usage/online_feature_table_refresh_history) | Historical | 3 hours |  |  |
| [OPENFLOW\_USAGE\_HISTORY](/sql-reference/account-usage/openflow_usage_history) | Historical | 3 hours |  |  |
| [OUTBOUND\_PRIVATELINK\_ENDPOINTS](/sql-reference/account-usage/outbound_privatelink_endpoints) | Object | 2 hours | Business Critical (or higher) | Data for deleted endpoints is retained for 1 year. |
| [PASSWORD\_POLICIES](/sql-reference/account-usage/password_policies) | Object | 2 hours |  |  |
| [PIPES](/sql-reference/account-usage/pipes) | Object | 2 hours |  |  |
| [PIPE\_USAGE\_HISTORY](/sql-reference/account-usage/pipe_usage_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [POLICY\_REFERENCES](/sql-reference/account-usage/policy_references) | Object | 2 hours |  |  |
| [POSTGRES\_COMPUTE\_USAGE\_HISTORY](/sql-reference/account-usage/postgres_compute_usage_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [POSTGRES\_STORAGE\_USAGE\_HISTORY](/sql-reference/account-usage/postgres_storage_usage_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [PRIVACY\_BUDGETS](/sql-reference/account-usage/privacy_budgets) | Object | 24 hours | Enterprise Edition (or higher) |  |
| [PRIVACY\_POLICIES](/sql-reference/account-usage/privacy_policies) | Object | 2 hours | Enterprise Edition (or higher) |  |
| [PROCEDURES](/sql-reference/account-usage/procedures) | Object | 2 hours |  |  |
| [PROJECTION\_POLICIES](/sql-reference/account-usage/projection_policies) | Object | 2 hours |  |  |
| [QUERY\_ACCELERATION\_ELIGIBLE](/sql-reference/account-usage/query_acceleration_eligible) | Historical | 3 hours |  | Data retained for 1 year. |
| [QUERY\_ACCELERATION\_HISTORY](/sql-reference/account-usage/query_acceleration_history) | Historical | 3 hours | Enterprise Edition (or higher) | Data retained for 1 year. |
| [QUERY\_ATTRIBUTION\_HISTORY](/sql-reference/account-usage/query_attribution_history) | Historical | 8 hours |  | Data retained for 1 year. |
| [QUERY\_HISTORY](/sql-reference/account-usage/query_history) | Historical | 45 minutes |  | Data retained for 1 year. |
| [QUERY\_INSIGHTS](/sql-reference/account-usage/query_insights) | Historical |  |  | Data retained for 1 year. |
| [QUERY\_METERING\_HISTORY](/sql-reference/account-usage/query_metering_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [REFERENTIAL\_CONSTRAINTS](/sql-reference/account-usage/referential_constraints) | Object | 2 hours |  |  |
| [REPLICATION\_GROUP\_REFRESH\_HISTORY](/sql-reference/account-usage/replication_group_refresh_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [REPLICATION\_GROUP\_USAGE\_HISTORY](/sql-reference/account-usage/replication_group_usage_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [REPLICATION\_GROUPS](/sql-reference/account-usage/replication_groups) | Object | 2 hours |  |  |
| [REPLICATION\_USAGE\_HISTORY](/sql-reference/account-usage/replication_usage_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [RESOURCE\_MONITORS](/sql-reference/account-usage/resource_monitors) | Object | 2 hours |  |  |
| [ROLES](/sql-reference/account-usage/roles) | Object | 2 hours |  |  |
| [ROW\_ACCESS\_POLICIES](/sql-reference/account-usage/row_access_policies) | Object | 2 hours |  |  |
| [SCHEMATA](/sql-reference/account-usage/schemata) | Object | 2 hours |  |  |
| [SEARCH\_OPTIMIZATION\_BENEFITS](/sql-reference/account-usage/search_optimization_benefits) | Historical | 6 hours | Enterprise Edition (or higher) | Data retained for 1 year. |
| [SEARCH\_OPTIMIZATION\_HISTORY](/sql-reference/account-usage/search_optimization_history) | Historical | 3 hours | Enterprise Edition (or higher) | Data retained for 1 year. |
| [SECRETS](/sql-reference/account-usage/secrets) | Object | 2 hours |  |  |
| [SEMANTIC\_DIMENSIONS](/sql-reference/account-usage/semantic_dimensions) | Object | 2 hours |  |  |
| [SEMANTIC\_FACTS](/sql-reference/account-usage/semantic_facts) | Object | 2 hours |  |  |
| [SEMANTIC\_METRICS](/sql-reference/account-usage/semantic_metrics) | Object | 2 hours |  |  |
| [SEMANTIC\_RELATIONSHIPS](/sql-reference/account-usage/semantic_relationships) | Object | 2 hours |  |  |
| [SEMANTIC\_TABLES](/sql-reference/account-usage/semantic_tables) | Object | 2 hours |  |  |
| [SEMANTIC\_VIEWS](/sql-reference/account-usage/semantic_views) | Object | 2 hours |  |  |
| [SEQUENCES](/sql-reference/account-usage/sequences) | Object | 2 hours |  |  |
| [SERVERLESS\_ALERT\_HISTORY](/sql-reference/account-usage/serverless_alert_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [SERVERLESS\_TASK\_HISTORY](/sql-reference/account-usage/serverless_task_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [SERVICES](/sql-reference/account-usage/services) | Object | 3 hours |  |  |
| [SESSION\_POLICIES](/sql-reference/account-usage/session_policies) | Object | 2 hours |  |  |
| [SESSIONS](/sql-reference/account-usage/sessions) | Historical | 3 hours |  | Data retained for 1 year. |
| [SHARES](/sql-reference/account-usage/shares) | Object | 3 hours |  |  |
| [SNAPSHOT\_OPERATION\_HISTORY](/sql-reference/account-usage/snapshot_operation_history) | Historical | 6 hours |  | Data retained for 1 year. This view is deprecated. Use the [BACKUP\_OPERATION\_HISTORY](/sql-reference/account-usage/backup_operation_history) view instead. |
| [SNAPSHOT\_POLICIES](/sql-reference/account-usage/snapshot_policies) | Object | 6 hours |  | This view is deprecated. Use the [BACKUP\_POLICIES](/sql-reference/account-usage/backup_policies) view instead. |
| [SNAPSHOT\_SETS](/sql-reference/account-usage/snapshot_sets) | Object | 6 hours |  | This view is deprecated. Use the [BACKUP\_SETS](/sql-reference/account-usage/backup_sets) view instead. |
| [SNAPSHOT\_STORAGE\_USAGE](/sql-reference/account-usage/snapshot_storage_usage) | Historical | 6 hours |  | Data retained for 1 year. This view is deprecated. Use the [BACKUP\_STORAGE\_USAGE](/sql-reference/account-usage/backup_storage_usage) view instead. |
| [SNAPSHOTS](/sql-reference/account-usage/snapshots) | Object | 6 hours |  | This view is deprecated. Use the [BACKUPS](/sql-reference/account-usage/backups) view instead. |
| [SNOWFLAKE\_APP\_RUNTIME\_COMPUTE\_HISTORY](/sql-reference/account-usage/snowflake_app_runtime_compute_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [SNOWFLAKE\_COCO\_USAGE\_HISTORY](/sql-reference/account-usage/snowflake_coco_usage_history) | Historical | 1 hour |  | Data retained for 1 year. |
| [SNOWFLAKE\_COWORK\_USAGE\_HISTORY](/sql-reference/account-usage/snowflake_cowork_usage_history_view) | Historical | 1 hour |  | Data retained for 1 year. |
| [SNOWPARK\_CONTAINER\_SERVICES\_HISTORY](/sql-reference/account-usage/snowpark_container_services_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY](/sql-reference/account-usage/snowpipe_streaming_channel_history) | Historical |  |  |  |
| [SNOWPIPE\_STREAMING\_CLIENT\_HISTORY](/sql-reference/account-usage/snowpipe_streaming_client_history) | Historical | 2 hours |  | Data retained for 1 year. |
| [SNOWPIPE\_STREAMING\_FILE\_MIGRATION\_HISTORY](/sql-reference/account-usage/snowpipe_streaming_file_migration_history) | Historical | 12 hours |  | Data retained for 1 year. |
| [STAGES](/sql-reference/account-usage/stages) | Object | 2 hours |  |  |
| [STAGE\_STORAGE\_USAGE\_HISTORY](/sql-reference/account-usage/stage_storage_usage_history) | Historical | 2 hours |  | Data retained for 1 year. |
| [STORAGE\_LIFECYCLE\_POLICIES](/sql-reference/account-usage/storage_lifecycle_policies) | Object | 2 hours |  |  |
| [STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/account-usage/storage_lifecycle_policy_history) | Historical | 2 hours |  | Data retained for 1 year. |
| [STORAGE\_REQUEST\_HISTORY](/sql-reference/account-usage/storage_request_history) | Historical | 6 hours |  | Data retained for 1 year. |
| [STORAGE\_USAGE](/sql-reference/account-usage/storage_usage) | Historical | 2 hours |  | Combined usage across all database tables and internal stages. Data retained for 1 year. |
| [TABLES](/sql-reference/account-usage/tables) | Object | 90 minutes |  |  |
| [TABLE\_CONSTRAINTS](/sql-reference/account-usage/table_constraints) | Object | 2 hours |  |  |
| [TABLE\_DML\_HISTORY](/sql-reference/account-usage/table_dml_history) | Historical | 6 hours |  | Data retained for 1 year. |
| [TABLE\_PRUNING\_HISTORY](/sql-reference/account-usage/table_pruning_history) | Historical | 6 hours |  | Data retained for 1 year. |
| [TABLE\_QUERY\_PRUNING\_HISTORY](/sql-reference/account-usage/table_query_pruning_history) | Historical | 4 hours |  | Data retained for 1 year. |
| [TABLE\_STORAGE\_METRICS](/sql-reference/account-usage/table_storage_metrics) | Object | 90 minutes |  |  |
| [TAG\_REFERENCES](/sql-reference/account-usage/tag_references) | Object | 2 hours |  |  |
| [TAGS](/sql-reference/account-usage/tags) | Object | 2 hours |  |  |
| [TASK\_HISTORY](/sql-reference/account-usage/task_history) | Historical | 45 minutes |  |  |
| [TASK\_VERSIONS](/sql-reference/account-usage/task_versions) | Object | 3 hours |  |  |
| [TRI\_SECRET\_SECURE\_HISTORY](/sql-reference/account-usage/tri-secret-secure-history) | Historical | 2 hours |  |  |
| [TRUST\_CENTER\_FINDINGS](/sql-reference/account-usage/trust_center_findings) | Historical | 1 hour |  |  |
| [TYPES](/sql-reference/account-usage/types) | Object | 2 hours |  |  |
| [USERS](/sql-reference/account-usage/users) | Object | 2 hours |  |  |
| [VIEWS](/sql-reference/account-usage/views) | Object | 90 minutes |  |  |
| [WAREHOUSE\_EVENTS\_HISTORY](/sql-reference/account-usage/warehouse_events_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [WAREHOUSE\_LOAD\_HISTORY](/sql-reference/account-usage/warehouse_load_history) | Historical | 3 hours |  | Data retained for 1 year. |
| [WAREHOUSE\_METERING\_HISTORY](/sql-reference/account-usage/warehouse_metering_history) | Historical | 3 hours |  | Data retained for 1 year. |

Expand

Show lessSee more

[1] All latency times are approximate; in some instances, the actual latency may be lower.

[2] The latency of the views for a given table may be up to 2 days if both of the following conditions are true: 1. Fewer than 32 DML statements have been added to the given table since it was last updated in LOAD\_HISTORY or COPY\_HISTORY. 2. Fewer than 100 rows have been added to the given table since it was last updated in LOAD\_HISTORY or COPY\_HISTORY.

[3] Unless otherwise noted, the Account Usage view is available to all accounts.

### Account Usage table functions

Currently, Snowflake supports one ACCOUNT\_USAGE table function:

| Table Function | Data Retention | Notes |
| --- | --- | --- |
| [TAG\_REFERENCES\_WITH\_LINEAGE](/sql-reference/functions/tag_references_with_lineage) | N/A | Results are only returned for the role that has access to the specified object. |

Expand

Show lessSee more

Note

Similar to the Account Usage views, please account for latency when calling this table function. The expected latency for this table
function is similar to the latency for the [TAG\_REFERENCES](#label-account-usage-views) view.

## READER\_ACCOUNT\_USAGE views

The READER\_ACCOUNT\_USAGE schema contains the following views:

| View | Type | Latency [1] | Notes |
| --- | --- | --- | --- |
| [LOGIN\_HISTORY](/sql-reference/account-usage/login_history) | Historical | 2 hours | Data retained for 1 year. |
| [QUERY\_HISTORY](/sql-reference/account-usage/query_history) | Historical | 45 minutes | Data retained for 1 year. |
| [RESOURCE\_MONITORS](/sql-reference/account-usage/resource_monitors) | Object | 2 hours |  |
| [STORAGE\_USAGE](/sql-reference/account-usage/storage_usage) | Historical | 24 hours | Combined usage across all database tables and internal stages. Data retained for 1 year. |
| [WAREHOUSE\_METERING\_HISTORY](/sql-reference/account-usage/warehouse_metering_history) | Historical | 24 hours | Data retained for 1 year. |

Expand

Show lessSee more

[1] All latency times are approximate; in some instances, the actual latency may be lower.

## Enabling other roles to use schemas in the SNOWFLAKE database

By default, the SNOWFLAKE database is visible to all users; however, access to schemas in this database can be granted by a user with the
ACCOUNTADMIN role using either of the following approaches:

- Grant IMPORTED PRIVILEGES on the SNOWFLAKE database.
- Grant a [SNOWFLAKE database role](#label-account-usage-snowflake-db-roles) to an account role.

Important

To avoid unintentionally granting access to organization-level data, consider using [SNOWFLAKE database roles](#label-account-usage-snowflake-db-roles) to grant access to views in the ACCOUNT\_USAGE schema.

For more information, refer to [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role).

For example, to grant IMPORTED PRIVILEGES on the SNOWFLAKE database to two additional roles:

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE SYSADMIN;
> GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE customrole1;
> ```

A user who is granted the `customrole1` role can query a view as follows:

> Copy code
>
> ```
> USE ROLE customrole1;
>
> SELECT database_name, database_owner FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASES;
> ```

For additional examples, see [Querying the Account Usage views](#label-account-usage-query-views).

### ACCOUNT\_USAGE schema SNOWFLAKE database roles

In addition, you can grant finer control to accounts using SNOWFLAKE database roles.
For more information on database roles, see [database roles](/user-guide/security-access-control-considerations#label-access-control-considerations-database-roles).

[ACCOUNT\_USAGE](/sql-reference/account-usage) schemas have four defined SNOWFLAKE database roles, each granted the SELECT privilege on specific views.

| Role | Purpose and Description |
| --- | --- |
| OBJECT\_VIEWER | The OBJECT\_VIEWER role provides visibility into object metadata. |
| USAGE\_VIEWER | The USAGE\_VIEWER role provides visibility into historical usage information. |
| GOVERNANCE\_VIEWER | The GOVERNANCE\_VIEWER role provides visibility into data-governance-related information. |
| SECURITY\_VIEWER | The SECURITY\_VIEWER role provides visibility into security-based information. |

Expand

Show lessSee more

# Database role required to access ACCOUNT\_USAGE views

The OBJECT\_VIEWER, USAGE\_VIEWER, GOVERNANCE\_VIEWER, and SECURITY\_VIEWER roles have the SELECT privilege to query Account Usage
views in the shared SNOWFLAKE database. Use the following table to determine which database role has access to a view.

| View | Database Role |
| --- | --- |
| [ACCESS\_HISTORY view](/sql-reference/account-usage/access_history) | GOVERNANCE\_VIEWER |
| [AGGREGATE\_ACCESS\_HISTORY view](/sql-reference/account-usage/aggregate_access_history) | GOVERNANCE\_VIEWER |
| [AGGREGATE\_QUERY\_HISTORY view](/sql-reference/account-usage/aggregate_query_history) | GOVERNANCE\_VIEWER |
| [AGGREGATION\_POLICIES view](/sql-reference/account-usage/aggregation_policies) | GOVERNANCE\_VIEWER |
| [ANOMALIES\_DAILY view](/sql-reference/account-usage/anomalies_daily) | USAGE\_VIEWER |
| [APPLICATION\_CALLBACK\_HISTORY view](/sql-reference/account-usage/application_callback_history) | SECURITY\_VIEWER |
| [APPLICATION\_CONFIGURATIONS view](/sql-reference/account-usage/application_configurations) | SECURITY\_VIEWER |
| [APPLICATION\_CONFIGURATION\_VALUE\_HISTORY view](/sql-reference/account-usage/application_configuration_value_history) | SECURITY\_VIEWER |
| [APPLICATION\_DAILY\_USAGE\_HISTORY view](/sql-reference/account-usage/application_daily_usage_history) | USAGE\_VIEWER |
| [APPLICATION\_SPECIFICATION\_STATUS\_HISTORY view](/sql-reference/account-usage/application_specification_status_history) | SECURITY\_VIEWER |
| [APPLICATION\_SPECIFICATIONS view](/sql-reference/account-usage/application_specifications) | SECURITY\_VIEWER |
| [ARCHIVE\_STORAGE\_DATA\_RETRIEVAL\_USAGE\_HISTORY view](/sql-reference/account-usage/archive_storage_data_retrieval_usage_history) | USAGE\_VIEWER |
| [AUTOMATIC\_CLUSTERING\_HISTORY view](/sql-reference/account-usage/automatic_clustering_history) | USAGE\_VIEWER |
| [BLOCK\_STORAGE\_HISTORY view](/sql-reference/account-usage/block_storage_history) | USAGE\_VIEWER |
| [BLOCK\_STORAGE\_SNAPSHOTS view](/sql-reference/account-usage/block_storage_snapshots) | OBJECT\_VIEWER |
| [CATALOG\_LINKED\_DATABASE\_USAGE\_HISTORY view](/sql-reference/account-usage/catalog_linked_database_usage_history) | USAGE\_VIEWER |
| [CLASS\_INSTANCES view](/sql-reference/account-usage/class_instances) | USAGE\_VIEWER |
| [CLASSES view](/sql-reference/account-usage/classes) | USAGE\_VIEWER |
| [COLUMN\_QUERY\_PRUNING\_HISTORY view](/sql-reference/account-usage/column_query_pruning_history) | USAGE\_VIEWER |
| [COLUMNS view](/sql-reference/account-usage/columns) | OBJECT\_VIEWER |
| [COMPLETE\_TASK\_GRAPHS view](/sql-reference/account-usage/complete_task_graphs) | OBJECT\_VIEWER |
| [CONTACT\_REFERENCES view](/sql-reference/account-usage/contact_references) | GOVERNANCE\_VIEWER |
| [CONTACTS view](/sql-reference/account-usage/contacts) | GOVERNANCE\_VIEWER |
| [COPY\_FILES\_HISTORY view](/sql-reference/account-usage/copy_files_history) | USAGE\_VIEWER |
| [COPY\_HISTORY view](/sql-reference/account-usage/copy_history) | USAGE\_VIEWER |
| [CORTEX\_AGENT\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_agent_usage_history) | USAGE\_VIEWER |
| [CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_ai_functions_usage_history) | USAGE\_VIEWER |
| [CORTEX\_AI\_GUARDRAILS\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_ai_guardrails_usage_history) | USAGE\_VIEWER |
| [CORTEX\_AISQL\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_aisql_usage_history) | USAGE\_VIEWER |
| [CORTEX\_ANALYST\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_analyst_usage_history) | USAGE\_VIEWER |
| [CORTEX\_DOCUMENT\_PROCESSING\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_document_processing_usage_history) | USAGE\_VIEWER |
| [CORTEX\_FINE\_TUNING\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_fine_tuning_usage_history) | USAGE\_VIEWER |
| [CORTEX\_FUNCTIONS\_QUERY\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_functions_query_usage_history) | USAGE\_VIEWER |
| [CORTEX\_FUNCTIONS\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_functions_usage_history) | USAGE\_VIEWER |
| [CORTEX\_PROVISIONED\_THROUGHPUT\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_provisioned_throughput_usage_history) | USAGE\_VIEWER |
| [CORTEX\_REST\_API\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_rest_api_usage_history) | USAGE\_VIEWER |
| [CORTEX\_SEARCH\_BATCH\_QUERY\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_search_batch_query_usage_history) | USAGE\_VIEWER |
| [CORTEX\_SEARCH\_DAILY\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_search_daily_usage_history) | USAGE\_VIEWER |
| [CORTEX\_SEARCH\_SERVING\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_search_serving_usage_history) | USAGE\_VIEWER |
| [CREDENTIALS view](/sql-reference/account-usage/credentials) | SECURITY\_VIEWER |
| [DATA\_CLASSIFICATION\_HISTORY view](/sql-reference/account-usage/data_classification_history) | GOVERNANCE\_VIEWER |
| [DATA\_CLASSIFICATION\_LATEST view](/sql-reference/account-usage/data_classification_latest) | GOVERNANCE\_VIEWER |
| [DATA\_METRIC\_FUNCTION\_EXPECTATIONS view](/sql-reference/account-usage/data_metric_function_expectations) | USAGE\_VIEWER or GOVERNANCE\_VIEWER |
| [DATA\_METRIC\_FUNCTION\_REFERENCES view](/sql-reference/account-usage/data_metric_function_references) | USAGE\_VIEWER or GOVERNANCE\_VIEWER |
| [DATA\_QUALITY\_MONITORING\_USAGE\_HISTORY view](/sql-reference/account-usage/data_quality_monitoring_usage_history) | USAGE\_VIEWER |
| [DATA\_TRANSFER\_HISTORY view](/sql-reference/account-usage/data_transfer_history) | USAGE\_VIEWER |
| [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/database_storage_usage_history) | USAGE\_VIEWER |
| [DATABASES view](/sql-reference/account-usage/databases) | OBJECT\_VIEWER |
| [DOCUMENT\_AI\_USAGE\_HISTORY view](/sql-reference/account-usage/document_ai_usage_history) | USAGE\_VIEWER |
| [DYNAMIC\_TABLE\_REFRESH\_HISTORY view](/sql-reference/account-usage/dynamic_table_refresh_history) | USAGE\_VIEWER |
| [ELEMENT\_TYPES view](/sql-reference/account-usage/element_types) | OBJECT\_VIEWER |
| [EVENT\_USAGE\_HISTORY view](/sql-reference/account-usage/event_usage_history) | USAGE\_VIEWER |
| [EXTERNAL\_ACCESS\_HISTORY view](/sql-reference/account-usage/external_access_history) | USAGE\_VIEWER |
| [FIELDS view](/sql-reference/account-usage/fields) | OBJECT\_VIEWER |
| [FILE\_FORMATS view](/sql-reference/account-usage/file_formats) | OBJECT\_VIEWER |
| [FUNCTIONS view](/sql-reference/account-usage/functions) | OBJECT\_VIEWER |
| [GRANTS\_TO\_ROLES view](/sql-reference/account-usage/grants_to_roles) | SECURITY\_VIEWER |
| [GRANTS\_TO\_SHARES view](/sql-reference/account-usage/grants_to_shares) | SECURITY\_VIEWER |
| [GRANTS\_TO\_USERS view](/sql-reference/account-usage/grants_to_users) | SECURITY\_VIEWER |
| [HYBRID\_TABLE\_USAGE\_HISTORY view](/sql-reference/account-usage/hybrid_table_usage_history) | USAGE\_VIEWER |
| [HYBRID\_TABLES view](/sql-reference/account-usage/hybrid_tables) | OBJECT\_VIEWER |
| [ICEBERG\_STORAGE\_OPTIMIZATION\_HISTORY view](/sql-reference/account-usage/iceberg_storage_optimization_history) | USAGE\_VIEWER |
| [INDEX\_COLUMNS view](/sql-reference/account-usage/index_columns) | OBJECT\_VIEWER |
| [INDEXES view](/sql-reference/account-usage/indexes) | OBJECT\_VIEWER |
| [INGRESS\_NETWORK\_ACCESS\_HISTORY view](/sql-reference/account-usage/ingress_network_access_history) | SECURITY\_VIEWER |
| [INTERNAL\_DATA\_TRANSFER\_HISTORY view](/sql-reference/account-usage/internal_data_transfer_history) | USAGE\_VIEWER |
| [INTERNAL\_STAGE\_NETWORK\_ACCESS\_HISTORY view](/sql-reference/account-usage/internal_stage_network_access_history) | SECURITY\_VIEWER |
| [JOIN\_POLICIES view](/sql-reference/account-usage/join_policies) | GOVERNANCE\_VIEWER |
| [LISTINGS view](/sql-reference/account-usage/listings) | SECURITY\_VIEWER |
| [LOAD\_HISTORY view](/sql-reference/account-usage/load_history) | USAGE\_VIEWER |
| [LOGIN\_HISTORY view](/sql-reference/account-usage/login_history) | SECURITY\_VIEWER |
| [MASKING\_POLICIES view](/sql-reference/account-usage/masking_policies) | GOVERNANCE\_VIEWER |
| [MATERIALIZED\_VIEW\_REFRESH\_HISTORY view](/sql-reference/account-usage/materialized_view_refresh_history) | USAGE\_VIEWER |
| [METERING\_DAILY\_HISTORY view](/sql-reference/account-usage/metering_daily_history) | USAGE\_VIEWER |
| [METERING\_HISTORY view](/sql-reference/account-usage/metering_history) | USAGE\_VIEWER |
| [MODEL\_SERVING\_USAGE\_HISTORY view](/sql-reference/account-usage/model_serving_usage_history) | USAGE\_VIEWER |
| [NETWORK\_POLICIES view](/sql-reference/account-usage/network_policies) | SECURITY\_VIEWER |
| [NETWORK\_RULE\_REFERENCES view](/sql-reference/account-usage/network_rule_references) | SECURITY\_VIEWER |
| [NETWORK\_RULES view](/sql-reference/account-usage/network_rules) | SECURITY\_VIEWER |
| [NOTEBOOKS\_CONTAINER\_RUNTIME\_HISTORY view](/sql-reference/account-usage/notebooks_container_runtime_history) | USAGE\_VIEWER |
| [OBJECT\_ACCESS\_REQUEST\_HISTORY view](/sql-reference/account-usage/object_access_request_history) | OBJECT\_VIEWER |
| [OBJECT\_DEPENDENCIES view](/sql-reference/account-usage/object_dependencies) | OBJECT\_VIEWER |
| [ONLINE\_FEATURE\_TABLE\_REFRESH\_HISTORY view](/sql-reference/account-usage/online_feature_table_refresh_history) | USAGE\_VIEWER |
| [OPENFLOW\_USAGE\_HISTORY view](/sql-reference/account-usage/openflow_usage_history) | USAGE\_VIEWER |
| [OUTBOUND\_PRIVATELINK\_ENDPOINTS view](/sql-reference/account-usage/outbound_privatelink_endpoints) | SECURITY\_VIEWER |
| [PASSWORD\_POLICIES view](/sql-reference/account-usage/password_policies) | SECURITY\_VIEWER |
| [PIPE\_USAGE\_HISTORY view](/sql-reference/account-usage/pipe_usage_history) | USAGE\_VIEWER |
| [PIPES view](/sql-reference/account-usage/pipes) | OBJECT\_VIEWER |
| [POLICY\_REFERENCES view](/sql-reference/account-usage/policy_references) | GOVERNANCE\_VIEWER, SECURITY\_VIEWER |
| [POSTGRES\_COMPUTE\_USAGE\_HISTORY view](/sql-reference/account-usage/postgres_compute_usage_history) | USAGE\_VIEWER |
| [POSTGRES\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/postgres_storage_usage_history) | USAGE\_VIEWER |
| [PRIVACY\_BUDGETS view](/sql-reference/account-usage/privacy_budgets) | GOVERNANCE\_VIEWER |
| [PRIVACY\_POLICIES view](/sql-reference/account-usage/privacy_policies) | GOVERNANCE\_VIEWER |
| [PROCEDURES view](/sql-reference/account-usage/procedures) | OBJECT\_VIEWER |
| [PROJECTION\_POLICIES view](/sql-reference/account-usage/projection_policies) | GOVERNANCE\_VIEWER |
| [QUERY\_ACCELERATION\_ELIGIBLE view](/sql-reference/account-usage/query_acceleration_eligible) | GOVERNANCE\_VIEWER |
| [QUERY\_ATTRIBUTION\_HISTORY view](/sql-reference/account-usage/query_attribution_history) | USAGE\_VIEWER, GOVERNANCE\_VIEWER |
| [QUERY\_HISTORY view](/sql-reference/account-usage/query_history) | GOVERNANCE\_VIEWER |
| [QUERY\_INSIGHTS view](/sql-reference/account-usage/query_insights) | GOVERNANCE\_VIEWER |
| [QUERY\_METERING\_HISTORY view](/sql-reference/account-usage/query_metering_history) | USAGE\_VIEWER, GOVERNANCE\_VIEWER |
| [REFERENTIAL\_CONSTRAINTS view](/sql-reference/account-usage/referential_constraints) | OBJECT\_VIEWER |
| [REPLICATION\_GROUP\_REFRESH\_HISTORY view](/sql-reference/account-usage/replication_group_refresh_history) | USAGE\_VIEWER |
| [REPLICATION\_GROUP\_USAGE\_HISTORY view](/sql-reference/account-usage/replication_group_usage_history) | USAGE\_VIEWER |
| [REPLICATION\_GROUPS view](/sql-reference/account-usage/replication_groups) | OBJECT\_VIEWER |
| [REPLICATION\_USAGE\_HISTORY view](/sql-reference/account-usage/replication_usage_history) | USAGE\_VIEWER |
| [RESOURCE\_MONITORS view](/sql-reference/account-usage/resource_monitors) | OBJECT\_VIEWER |
| [ROLES view](/sql-reference/account-usage/roles) | SECURITY\_VIEWER |
| [ROW\_ACCESS\_POLICIES view](/sql-reference/account-usage/row_access_policies) | GOVERNANCE\_VIEWER |
| [SCHEMATA view](/sql-reference/account-usage/schemata) | OBJECT\_VIEWER |
| [SEARCH\_OPTIMIZATION\_BENEFITS view](/sql-reference/account-usage/search_optimization_benefits) | USAGE\_VIEWER |
| [SEARCH\_OPTIMIZATION\_HISTORY view](/sql-reference/account-usage/search_optimization_history) | USAGE\_VIEWER |
| [SECRETS view](/sql-reference/account-usage/secrets) | SECURITY\_VIEWER |
| [SEMANTIC\_DIMENSIONS view](/sql-reference/account-usage/semantic_dimensions) | OBJECT\_VIEWER |
| [SEMANTIC\_FACTS view](/sql-reference/account-usage/semantic_facts) | OBJECT\_VIEWER |
| [SEMANTIC\_METRICS view](/sql-reference/account-usage/semantic_metrics) | OBJECT\_VIEWER |
| [SEMANTIC\_RELATIONSHIPS view](/sql-reference/account-usage/semantic_relationships) | OBJECT\_VIEWER |
| [SEMANTIC\_TABLES view](/sql-reference/account-usage/semantic_tables) | OBJECT\_VIEWER |
| [SEMANTIC\_VIEWS view](/sql-reference/account-usage/semantic_views) | OBJECT\_VIEWER |
| [SEQUENCES view](/sql-reference/account-usage/sequences) | OBJECT\_VIEWER |
| [SERVERLESS\_ALERT\_HISTORY view](/sql-reference/account-usage/serverless_alert_history) | USAGE\_VIEWER |
| [SERVERLESS\_TASK\_HISTORY view](/sql-reference/account-usage/serverless_task_history) | USAGE\_VIEWER |
| [SERVICES view](/sql-reference/account-usage/services) | OBJECT\_VIEWER |
| [SESSION\_POLICIES view](/sql-reference/account-usage/session_policies) | SECURITY\_VIEWER |
| [SESSIONS view](/sql-reference/account-usage/sessions) | SECURITY\_VIEWER |
| [SHARES view](/sql-reference/account-usage/shares) | SECURITY\_VIEWER |
| [SNAPSHOT\_OPERATION\_HISTORY view --- Deprecated](/sql-reference/account-usage/snapshot_operation_history) | OBJECT\_VIEWER |
| [SNAPSHOT\_POLICIES view --- Deprecated](/sql-reference/account-usage/snapshot_policies) | OBJECT\_VIEWER |
| [SNAPSHOT\_SETS view --- Deprecated](/sql-reference/account-usage/snapshot_sets) | OBJECT\_VIEWER |
| [SNAPSHOT\_STORAGE\_USAGE view --- Deprecated](/sql-reference/account-usage/snapshot_storage_usage) | OBJECT\_VIEWER |
| [SNAPSHOTS view — Deprecated](/sql-reference/account-usage/snapshots) | OBJECT\_VIEWER |
| [SNOWFLAKE\_COCO\_USAGE\_HISTORY view](/sql-reference/account-usage/snowflake_coco_usage_history) | USAGE\_VIEWER |
| [SNOWFLAKE\_COWORK\_USAGE\_HISTORY view](/sql-reference/account-usage/snowflake_cowork_usage_history) | USAGE\_VIEWER |
| [SNOWPARK\_CONTAINER\_SERVICES\_HISTORY view](/sql-reference/account-usage/snowpark_container_services_history) | USAGE\_VIEWER |
| [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY view](/sql-reference/account-usage/snowpipe_streaming_channel_history) | USAGE\_VIEWER |
| [STAGE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/stage_storage_usage_history) | USAGE\_VIEWER |
| [STAGES view](/sql-reference/account-usage/stages) | OBJECT\_VIEWER |
| [STORAGE\_LIFECYCLE\_POLICIES view](/sql-reference/account-usage/storage_lifecycle_policies) | GOVERNANCE\_VIEWER |
| [STORAGE\_LIFECYCLE\_POLICY\_HISTORY view](/sql-reference/account-usage/storage_lifecycle_policy_history) | GOVERNANCE\_VIEWER |
| [STORAGE\_REQUEST\_HISTORY view](/sql-reference/account-usage/storage_request_history) | USAGE\_VIEWER |
| [STORAGE\_USAGE view](/sql-reference/account-usage/storage_usage) | USAGE\_VIEWER |
| [TABLE\_CONSTRAINTS view](/sql-reference/account-usage/table_constraints) | OBJECT\_VIEWER |
| [TABLE\_DML\_HISTORY view](/sql-reference/account-usage/table_dml_history) | USAGE\_VIEWER |
| [TABLE\_PRUNING\_HISTORY view](/sql-reference/account-usage/table_pruning_history) | USAGE\_VIEWER |
| [TABLE\_QUERY\_PRUNING\_HISTORY view](/sql-reference/account-usage/table_query_pruning_history) | USAGE\_VIEWER |
| [TABLE\_STORAGE\_METRICS view](/sql-reference/account-usage/table_storage_metrics) | USAGE\_VIEWER |
| [TABLES view](/sql-reference/account-usage/tables) | OBJECT\_VIEWER |
| [TAG\_REFERENCES view](/sql-reference/account-usage/tag_references) | GOVERNANCE\_VIEWER |
| [TAGS view](/sql-reference/account-usage/tags) | OBJECT\_VIEWER or GOVERNANCE\_VIEWER |
| [TASK\_HISTORY view](/sql-reference/account-usage/task_history) | USAGE\_VIEWER |
| [TASKS view](/sql-reference/account-usage/tasks) | OBJECT\_VIEWER |
| [TRUST\_CENTER\_FINDINGS view](/sql-reference/account-usage/trust_center_findings) | SECURITY\_VIEWER |
| [USERS view](/sql-reference/account-usage/users) | SECURITY\_VIEWER |
| [VIEWS view](/sql-reference/account-usage/views) | OBJECT\_VIEWER |
| [WAREHOUSE\_EVENTS\_HISTORY view](/sql-reference/account-usage/warehouse_events_history) | USAGE\_VIEWER |
| [WAREHOUSE\_LOAD\_HISTORY view](/sql-reference/account-usage/warehouse_load_history) | USAGE\_VIEWER |
| [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history) | USAGE\_VIEWER |

Expand

Show lessSee more

### READER\_ACCOUNT\_USAGE schema SNOWFLAKE database roles

The READER\_USAGE\_VIEWER SNOWFLAKE database role is granted SELECT privilege on all READER\_ACCOUNT\_USAGE views.
As reader accounts are created by clients, the READER\_USAGE\_VIEWER role is expected to be granted to those roles used to monitor reader account use.

| View |
| --- |
| [LOGIN\_HISTORY view](/sql-reference/account-usage/login_history) |
| [QUERY\_HISTORY view](/sql-reference/account-usage/query_history) |
| [RESOURCE\_MONITORS view](/sql-reference/account-usage/resource_monitors) |
| [STORAGE\_USAGE view](/sql-reference/account-usage/storage_usage) |
| [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history) |

Expand

Show lessSee more

## Querying the Account Usage views

This section includes considerations when querying the Account Usage views along with query examples.

### Selecting columns

The Snowflake-specific views are subject to change. Avoid selecting all columns from these views. Instead, select the columns that you want.
For example, if you want the `name` column, use `SELECT name`, rather than `SELECT *`.

### Reconciling cost views

There are several Account Usage views that contain data related to the cost of compute resources, storage, and data transfers. If you are trying to reconcile these views against a corresponding view in the [ORGANIZATION\_USAGE schema](/sql-reference/organization-usage), you must first set the timezone of the session to UTC.

For example, if you are trying to reconcile ACCOUNT\_USAGE.WAREHOUSE\_METERING\_HISTORY to the account’s data in ORGANIZATION\_USAGE.WAREHOUSE\_METERING\_HISTORY, you must run the following command before querying the Account Usage view:

Copy code

```
ALTER SESSION SET TIMEZONE = UTC;
```

### Examples

The following examples show some typical/useful queries using the views in the [ACCOUNT\_USAGE](#label-account-usage-views)
schema.

Note

- These examples assume the SNOWFLAKE database and the ACCOUNT\_USAGE schema are in use for the current session. The examples also
  assume the ACCOUNTADMIN role (or a role granted IMPORTED PRIVILEGES on the database) is in use. If they are not in use, execute
  the following commands before running the queries in the examples:

  Copy code

  ```
  USE ROLE ACCOUNTADMIN;

  USE SCHEMA snowflake.account_usage;
  ```

#### Examples: User login metrics

Average number of seconds between failed login attempts by user (month-to-date):

> Copy code
>
> ```
> select user_name,
>        count(*) as failed_logins,
>        avg(seconds_between_login_attempts) as average_seconds_between_login_attempts
> from (
>       select user_name,
>              timediff(seconds, event_timestamp, lead(event_timestamp)
>                  over(partition by user_name order by event_timestamp)) as seconds_between_login_attempts
>       from login_history
>       where event_timestamp > date_trunc(month, current_date)
>       and is_success = 'NO'
>      )
> group by 1
> order by 3;
> ```

Failed logins by user (month-to-date):

> Copy code
>
> ```
> select user_name,
>        sum(iff(is_success = 'NO', 1, 0)) as failed_logins,
>        count(*) as logins,
>        sum(iff(is_success = 'NO', 1, 0)) / nullif(count(*), 0) as login_failure_rate
> from login_history
> where event_timestamp > date_trunc(month, current_date)
> group by 1
> order by 4 desc;
> ```

Failed logins by user and connecting client (month-to-date):

> Copy code
>
> ```
> select reported_client_type,
>        user_name,
>        sum(iff(is_success = 'NO', 1, 0)) as failed_logins,
>        count(*) as logins,
>        sum(iff(is_success = 'NO', 1, 0)) / nullif(count(*), 0) as login_failure_rate
> from login_history
> where event_timestamp > date_trunc(month, current_date)
> group by 1,2
> order by 5 desc;
> ```

#### Examples: Warehouse performance

This query calculates virtual warehouse performance metrics such as throughput and latency for 15-minute time intervals over the course of
one day.

In the code sample below, you can replace `CURRENT_WAREHOUSE()` with the name of a warehouse to calculate metrics for that warehouse. In
addition, change the `time_from` and `time_to` dates in the WITH clause to specify the time period.

> Copy code
>
> ```
> WITH
> params AS (
> SELECT
>     CURRENT_WAREHOUSE() AS warehouse_name,
>     '2021-11-01' AS time_from,
>     '2021-11-02' AS time_to
> ),
>
> jobs AS (
> SELECT
>     query_id,
>     time_slice(start_time::timestamp_ntz, 15, 'minute','start') as interval_start,
>     qh.warehouse_name,
>     database_name,
>     query_type,
>     total_elapsed_time,
>     compilation_time AS compilation_and_scheduling_time,
>     (queued_provisioning_time + queued_repair_time + queued_overload_time) AS queued_time,
>     transaction_blocked_time,
>     execution_time
> FROM snowflake.account_usage.query_history qh, params
> WHERE
>     qh.warehouse_name = params.warehouse_name
> AND start_time >= params.time_from
> AND start_time <= params.time_to
> AND execution_status = 'SUCCESS'
> AND query_type IN ('SELECT','UPDATE','INSERT','MERGE','DELETE')
> ),
>
> interval_stats AS (
> SELECT
>     query_type,
>     interval_start,
>     COUNT(DISTINCT query_id) AS numjobs,
>     MEDIAN(total_elapsed_time)/1000 AS p50_total_duration,
>     (percentile_cont(0.95) within group (order by total_elapsed_time))/1000 AS p95_total_duration,
>     SUM(total_elapsed_time)/1000 AS sum_total_duration,
>     SUM(compilation_and_scheduling_time)/1000 AS sum_compilation_and_scheduling_time,
>     SUM(queued_time)/1000 AS sum_queued_time,
>     SUM(transaction_blocked_time)/1000 AS sum_transaction_blocked_time,
>     SUM(execution_time)/1000 AS sum_execution_time,
>     ROUND(sum_compilation_and_scheduling_time/sum_total_duration,2) AS compilation_and_scheduling_ratio,
>     ROUND(sum_queued_time/sum_total_duration,2) AS queued_ratio,
>     ROUND(sum_transaction_blocked_time/sum_total_duration,2) AS blocked_ratio,
>     ROUND(sum_execution_time/sum_total_duration,2) AS execution_ratio,
>     ROUND(sum_total_duration/numjobs,2) AS total_duration_perjob,
>     ROUND(sum_compilation_and_scheduling_time/numjobs,2) AS compilation_and_scheduling_perjob,
>     ROUND(sum_queued_time/numjobs,2) AS queued_perjob,
>     ROUND(sum_transaction_blocked_time/numjobs,2) AS blocked_perjob,
>     ROUND(sum_execution_time/numjobs,2) AS execution_perjob
> FROM jobs
> GROUP BY 1,2
> ORDER BY 1,2
> )
> SELECT * FROM interval_stats;
> ```
>
> Note
>
> Analyze different statement types separately (e.g., SELECT statements independent of INSERT or DELETE or other statements).

- The NUMJOBS value represents the throughput for that time interval.
- The P50\_TOTAL\_DURATION (median) and P95\_TOTAL\_DURATION (peak) values represent latency.
- The SUM\_TOTAL\_DURATION is the sum of the SUM\_<job\_stage>\_TIME values for the different job stages (COMPILATION\_AND\_SCHEDULING, QUEUED,
  BLOCKED, EXECUTION).
- Analyze the <job\_stage>\_RATIO values when the load (NUMJOBS) increases. Look for ratio changes or deviations from the average.
- If the QUEUED\_RATIO is high, there might not be sufficient capacity in the warehouse. Add more clusters or increase the warehouse size.

#### Examples: Warehouse credit usage

Credits used by each warehouse in your account (month-to-date):

> Copy code
>
> ```
> select warehouse_name,
>        sum(credits_used) as total_credits_used
> from warehouse_metering_history
> where start_time >= date_trunc(month, current_date)
> group by 1
> order by 2 desc;
> ```

Credits used over time by each warehouse in your account (month-to-date):

> Copy code
>
> ```
> select start_time::date as usage_date,
>        warehouse_name,
>        sum(credits_used) as total_credits_used
> from warehouse_metering_history
> where start_time >= date_trunc(month, current_date)
> group by 1,2
> order by 2,1;
> ```

#### Examples: Data storage usage

Billable terabytes stored in your account over time:

> Copy code
>
> ```
> select date_trunc(month, usage_date) as usage_month
>   , avg(storage_bytes + stage_bytes + failsafe_bytes) / power(1024, 4) as billable_tb
> from storage_usage
> group by 1
> order by 1;
> ```

#### Examples: User query totals and execution times

Total jobs executed in your account (month-to-date):

> Copy code
>
> ```
> select count(*) as number_of_jobs
> from query_history
> where start_time >= date_trunc(month, current_date);
> ```

Total jobs executed by each warehouse in your account (month-to-date):

> Copy code
>
> ```
> select warehouse_name,
>        count(*) as number_of_jobs
> from query_history
> where start_time >= date_trunc(month, current_date)
> group by 1
> order by 2 desc;
> ```

Average query execution time by user (month-to-date):

> Copy code
>
> ```
> select user_name,
>        avg(execution_time) as average_execution_time
> from query_history
> where start_time >= date_trunc(month, current_date)
> group by 1
> order by 2 desc;
> ```

Average query execution time by query type and warehouse size (month-to-date):

> Copy code
>
> ```
> select query_type,
>        warehouse_size,
>        avg(execution_time) as average_execution_time
> from query_history
> where start_time >= date_trunc(month, current_date)
> group by 1,2
> order by 3 desc;
> ```

#### Examples: Obtain a query count for every login event

Join columns from LOGIN\_HISTORY, QUERY\_HISTORY, and SESSIONS to obtain a query count for each user login event.

> Note
>
> The SESSIONS view records information starting on July 20-21, 2020, therefore the query result will only contain overlapping
> information for each of the three views starting from this date.
>
> Copy code
>
> ```
> select l.user_name,
>        l.event_timestamp as login_time,
>        l.client_ip,
>        l.reported_client_type,
>        l.first_authentication_factor,
>        l.second_authentication_factor,
>        count(q.query_id)
> from snowflake.account_usage.login_history l
> join snowflake.account_usage.sessions s on l.event_id = s.login_event_id
> join snowflake.account_usage.query_history q on q.session_id = s.session_id
> group by 1,2,3,4,5,6
> order by l.user_name
> ;
> ```
