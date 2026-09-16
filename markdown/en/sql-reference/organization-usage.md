# Organization Usage

Snowflake provides historical usage data for all accounts in your organization via the ORGANIZATION\_USAGE schema in a shared database named
SNOWFLAKE.

## ORGANIZATION\_USAGE views

The ORGANIZATION\_USAGE schema contains the following views:

| View | Type | Latency [1] | Notes |
| --- | --- | --- | --- |
| [ACCESS\_HISTORY](/sql-reference/organization-usage/access_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [ACCOUNTS](/sql-reference/organization-usage/accounts) | Object | 24 hours |  |
| [AGGREGATE\_QUERY\_HISTORY](/sql-reference/organization-usage/aggregate_query_history) | Historical | 5 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [AGGREGATION\_POLICIES](/sql-reference/organization-usage/aggregation_policies) | Object | 4 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [ALERT\_HISTORY](/sql-reference/organization-usage/alert_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [ANOMALIES\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/anomalies_in_currency_daily) | Historical | 24 hours |  |
| [AUTOMATIC\_CLUSTERING\_HISTORY](/sql-reference/organization-usage/automatic_clustering_history) | Historical | 24 hours | Data retained for 1 year. |
| [BACKUP\_OPERATION\_HISTORY](/sql-reference/organization-usage/backup_operation_history) | Historical | 6 hours | Data retained for 1 year. |
| [BACKUP\_POLICIES](/sql-reference/organization-usage/backup_policies) | Object | 6 hours |  |
| [BACKUP\_SETS](/sql-reference/organization-usage/backup_sets) | Object | 6 hours |  |
| [BACKUPS](/sql-reference/organization-usage/backups) | Object | 6 hours |  |
| [BLOCK\_STORAGE\_HISTORY](/sql-reference/organization-usage/block_storage_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CATALOG\_LINKED\_DATABASE\_USAGE\_HISTORY](/sql-reference/organization-usage/catalog_linked_database_usage_history) | Historical | 5 hours | Data retained for 1 year. [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CLASSES](/sql-reference/organization-usage/classes) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CLASS\_INSTANCES](/sql-reference/organization-usage/class_instances) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [COLUMNS](/sql-reference/organization-usage/columns) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [COLUMN\_QUERY\_PRUNING\_HISTORY](/sql-reference/organization-usage/column_query_pruning_history) | Historical | 6 hours | Data retained for 1 year. [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [COMPLETE\_TASK\_GRAPHS](/sql-reference/organization-usage/complete_task_graphs) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [COMPUTE\_POOLS](/sql-reference/organization-usage/compute_pools) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CONTACTS](/sql-reference/organization-usage/contacts) | Object | 4 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CONTACT\_REFERENCES](/sql-reference/organization-usage/contact_references) | Object | 4 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CONTRACT\_ITEMS](/sql-reference/organization-usage/contract_items) [2] | Historical | 24 hours |  |
| [AI\_GATEWAY\_USAGE\_HISTORY](/sql-reference/organization-usage/ai_gateway_usage_history) | Historical |  | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CORTEX\_AGENT\_USAGE\_HISTORY](/sql-reference/organization-usage/cortex_agent_usage_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY](/sql-reference/organization-usage/cortex_ai_functions_usage_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CORTEX\_CODE\_CLI\_USAGE\_HISTORY](/sql-reference/organization-usage/cortex_code_cli_usage_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CORTEX\_CODE\_DESKTOP\_USAGE\_HISTORY](/sql-reference/organization-usage/cortex_code_desktop_usage_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CORTEX\_CODE\_SNOWSIGHT\_USAGE\_HISTORY](/sql-reference/organization-usage/cortex_code_snowsight_usage_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CORTEX\_SEARCH\_SERVING\_USAGE\_HISTORY](/sql-reference/organization-usage/cortex_search_serving_usage_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [COPY\_HISTORY](/sql-reference/organization-usage/copy_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [CREDENTIALS](/sql-reference/organization-usage/credentials) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [DATA\_CLASSIFICATION\_HISTORY](/sql-reference/organization-usage/data_classification_history) | Historical | 5 hours | Data retained for 1 year. [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [DATA\_CLASSIFICATION\_LATEST](/sql-reference/organization-usage/data_classification_latest) | Object | 5 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [DATA\_TRANSFER\_DAILY\_HISTORY](/sql-reference/organization-usage/data_transfer_daily_history) | Historical | 2 hours | Data retained for 1 year. |
| [DATA\_TRANSFER\_HISTORY](/sql-reference/organization-usage/data_transfer_history) | Historical | 24 hours | Data retained for 1 year. |
| [DATABASE\_STORAGE\_USAGE\_HISTORY](/sql-reference/organization-usage/database_storage_usage_history) | Historical | 24 hours | Data retained for 1 year. |
| [DATABASES](/sql-reference/organization-usage/databases) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/organization-usage/dynamic_table_refresh_history) | Historical | 5 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [FEATURE\_POLICIES](/sql-reference/organization-usage/feature_policies) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [FILE\_FORMATS](/sql-reference/organization-usage/file_formats) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [FUNCTIONS](/sql-reference/organization-usage/functions) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [GRANTS\_TO\_ROLES](/sql-reference/organization-usage/grants_to_roles) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [GRANTS\_TO\_SHARES](/sql-reference/organization-usage/grants_to_shares) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [GRANTS\_TO\_USERS](/sql-reference/organization-usage/grants_to_users) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [HYBRID\_TABLES](/sql-reference/organization-usage/hybrid_tables) | Object | 5 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [INDEX\_COLUMNS](/sql-reference/organization-usage/index_columns) | Object | 5 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [INDEXES](/sql-reference/organization-usage/indexes) | Object | 5 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [JOIN\_POLICIES](/sql-reference/organization-usage/join_policies) | Object | 4 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [LISTING\_AUTO\_FULFILLMENT\_USAGE\_HISTORY](/sql-reference/organization-usage/listing_auto_fulfillment_usage_history) | Historical | 72 hours | Data retained for 1 year. |
| [LISTINGS](/sql-reference/organization-usage/listings) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [LOAD\_HISTORY](/sql-reference/organization-usage/load_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [LOCK\_WAIT\_HISTORY](/sql-reference/organization-usage/lock_wait_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [LOGIN\_HISTORY](/sql-reference/organization-usage/login_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [MARKETPLACE\_DISBURSEMENT\_REPORT](/collaboration/views/marketplace-disbursement-report-org) | Historical | 24 hours | Data retained for 1 year. |
| [MARKETPLACE\_PAID\_USAGE\_DAILY](/collaboration/views/marketplace-paid-usage-daily-org) | Historical | 24 hours | Data retained for 1 year. |
| [MASKING\_POLICIES](/sql-reference/organization-usage/masking_policies) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [MATERIALIZED\_VIEW\_REFRESH\_HISTORY](/sql-reference/organization-usage/materialized_view_refresh_history) | Historical | 24 hours | Data retained for 1 year. |
| [METERING\_DAILY\_HISTORY](/sql-reference/organization-usage/metering_daily_history) | Historical | 2 hours | Data retained for 1 year. |
| [METERING\_HISTORY](/sql-reference/organization-usage/metering_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [MODEL\_SERVING\_USAGE\_HISTORY](/sql-reference/organization-usage/model_serving_usage_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [MONETIZED\_USAGE\_DAILY](/collaboration/views/monetized-usage-daily-org) | Historical | 24 hours | Data retained for 1 year. |
| [NETWORK\_POLICIES](/sql-reference/organization-usage/network_policies) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [NETWORK\_RULE\_REFERENCES](/sql-reference/organization-usage/network_rule_references) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [NETWORK\_RULES](/sql-reference/organization-usage/network_rules) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [NOTEBOOKS\_CONTAINER\_RUNTIME\_HISTORY](/sql-reference/organization-usage/notebooks_container_runtime_history) | Historical | 5 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [OBJECT\_ACCESS\_REQUEST\_HISTORY](/sql-reference/organization-usage/object_access_request_history) | Historical | 5 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [OBJECT\_DEPENDENCIES](/sql-reference/organization-usage/object_dependencies) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [ORGANIZATION\_USAGE\_STORAGE\_HISTORY](/sql-reference/organization-usage/organization_usage_storage_history) | Historical | 24 hours | Data retained for 1 year. |
| [OUTBOUND\_PRIVATELINK\_ENDPOINTS](/sql-reference/organization-usage/outbound_privatelink_endpoints) | Object | 2 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). Business Critical (or higher). Data for deleted endpoints is retained for 1 year. |
| [PASSWORD\_POLICIES](/sql-reference/organization-usage/password_policies) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [PIPE\_USAGE\_HISTORY](/sql-reference/organization-usage/pipe_usage_history) | Historical | 24 hours | Data retained for 1 year. |
| [PIPES](/sql-reference/organization-usage/pipes) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [POLICY\_REFERENCES](/sql-reference/organization-usage/policy_references) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [POSTGRES\_COMPUTE\_USAGE\_HISTORY](/sql-reference/organization-usage/postgres_compute_usage_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). Data retained for 1 year. |
| [PRIVACY\_POLICIES](/sql-reference/organization-usage/privacy_policies) | Object | 4 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [PROCEDURES](/sql-reference/organization-usage/procedures) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [PROJECTION\_POLICIES](/sql-reference/organization-usage/projection_policies) | Object | 4 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [QUERY\_ACCELERATION\_ELIGIBLE](/sql-reference/organization-usage/query_acceleration_eligible) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [QUERY\_ACCELERATION\_HISTORY](/sql-reference/organization-usage/query_acceleration_history) | Historical | 24 hours | Data retained for 1 year. |
| [QUERY\_ATTRIBUTION\_HISTORY](/sql-reference/organization-usage/query_attribution_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [QUERY\_HISTORY](/sql-reference/organization-usage/query_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [QUERY\_INSIGHTS](/sql-reference/organization-usage/query_insights) | Historical | 3.5 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [QUERY\_METERING\_HISTORY](/sql-reference/organization-usage/query_metering_history) | Historical | 24 hours | Coming soon. [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [RATE\_SHEET\_DAILY](/sql-reference/organization-usage/rate_sheet_daily) [2] | Historical | 24 hours |  |
| [REFERENTIAL\_CONSTRAINTS](/sql-reference/organization-usage/referential_constraints) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [REMAINING\_BALANCE\_DAILY](/sql-reference/organization-usage/remaining_balance_daily) [2] | Historical | 72 hours |  |
| [REPLICATION\_GROUPS](/sql-reference/organization-usage/replication_groups) | Object | 4 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [REPLICATION\_GROUP\_REFRESH\_HISTORY](/sql-reference/organization-usage/replication_group_refresh_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [REPLICATION\_GROUP\_USAGE\_HISTORY](/sql-reference/organization-usage/replication_group_usage_history) | Historical | 24 hours | Data retained for 1 year. |
| [REPLICATION\_USAGE\_HISTORY](/sql-reference/organization-usage/replication_usage_history) | Historical | 24 hours | Data retained for 1 year. |
| [RESOURCE\_MONITORS](/sql-reference/organization-usage/resource_monitors) |  | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [ROLES](/sql-reference/organization-usage/roles) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [ROW\_ACCESS\_POLICIES](/sql-reference/organization-usage/row_access_policies) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SCHEMATA](/sql-reference/organization-usage/schemata) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SEARCH\_OPTIMIZATION\_BENEFITS](/sql-reference/organization-usage/search_optimization_benefits) | Historical | 8 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SEARCH\_OPTIMIZATION\_HISTORY](/sql-reference/organization-usage/search_optimization_history) | Historical | 24 hours | Data retained for 1 year. |
| [SECRETS](/sql-reference/organization-usage/secrets) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SEMANTIC\_DIMENSIONS](/sql-reference/organization-usage/semantic_dimensions) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SEMANTIC\_FACTS](/sql-reference/organization-usage/semantic_facts) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SEMANTIC\_METRICS](/sql-reference/organization-usage/semantic_metrics) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SEMANTIC\_RELATIONSHIPS](/sql-reference/organization-usage/semantic_relationships) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SEMANTIC\_TABLES](/sql-reference/organization-usage/semantic_tables) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SEMANTIC\_VARIABLES](/sql-reference/organization-usage/semantic_variables) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SEMANTIC\_VIEWS](/sql-reference/organization-usage/semantic_views) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SEMANTIC\_VIEW\_IMPORTS](/sql-reference/organization-usage/semantic_view_imports) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SEQUENCES](/sql-reference/organization-usage/sequences) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SERVICES](/sql-reference/organization-usage/services) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SESSION\_POLICIES](/sql-reference/organization-usage/session_policies) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SESSIONS](/sql-reference/organization-usage/sessions) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SHARES](/sql-reference/organization-usage/shares) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SNAPSHOT\_OPERATION\_HISTORY](/sql-reference/organization-usage/snapshot_operation_history) | Historical | 6 hours | Data retained for 1 year. This view is deprecated. Use the [BACKUP\_OPERATION\_HISTORY](/sql-reference/organization-usage/backup_operation_history) view instead. |
| [SNAPSHOT\_POLICIES](/sql-reference/organization-usage/snapshot_policies) | Object | 6 hours | This view is deprecated. Use the [BACKUP\_POLICIES](/sql-reference/organization-usage/backup_policies) view instead. |
| [SNAPSHOT\_SETS](/sql-reference/organization-usage/snapshot_sets) | Object | 6 hours | This view is deprecated. Use the [BACKUP\_SETS](/sql-reference/organization-usage/backup_sets) view instead. |
| [SNAPSHOTS](/sql-reference/organization-usage/snapshots) | Object | 6 hours | This view is deprecated. Use the [BACKUPS](/sql-reference/organization-usage/backups) view instead. |
| [SNOWFLAKE\_COCO\_USAGE\_HISTORY](/sql-reference/organization-usage/snowflake_coco_usage_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SNOWFLAKE\_COWORK\_USAGE\_HISTORY](/sql-reference/organization-usage/snowflake_cowork_usage_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SNOWPARK\_CONTAINER\_SERVICES\_HISTORY](/sql-reference/organization-usage/snowpark_container_services_history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY](/sql-reference/organization-usage/snowpipe_streaming_channel_history) | Historical | 5 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SNOWPIPE\_STREAMING\_CLIENT\_HISTORY](/sql-reference/organization-usage/snowpipe_streaming_client_history) | Historical | 4 hours | Data retained for 1 year. [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [SNOWPIPE\_STREAMING\_FILE\_MIGRATION\_HISTORY](/sql-reference/organization-usage/snowpipe_streaming_file_migration_history) | Historical | 14 hours | Data retained for 1 year. [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [STAGES](/sql-reference/organization-usage/stages) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [STAGE\_STORAGE\_USAGE\_HISTORY](/sql-reference/organization-usage/stage_storage_usage_history) | Historical | 24 hours | Data retained for 1 year. |
| [STORAGE\_DAILY\_HISTORY](/sql-reference/organization-usage/storage_daily_history) | Historical | 2 hours | Data retained for 1 year. |
| [STORAGE\_LIFECYCLE\_POLICIES](/sql-reference/organization-usage/storage_lifecycle_policies) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/organization-usage/storage_lifecycle_policy_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). Data retained for 1 year. |
| [STORAGE\_USAGE](/sql-reference/organization-usage/storage_usage) | Historical | 4 hours | Data retained for 1 year. [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TABLE\_CONSTRAINTS](/sql-reference/organization-usage/table_constraints) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TABLE\_DML\_HISTORY](/sql-reference/organization-usage/table_dml_history) | Historical | 8 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TABLE\_PRUNING\_HISTORY](/sql-reference/organization-usage/table_pruning_history) | Historical | 8 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TABLE\_QUERY\_PRUNING\_HISTORY](/sql-reference/organization-usage/table_query_pruning_history) | Historical | 6 hours | Data retained for 1 year. [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TABLE\_STORAGE\_METRICS](/sql-reference/organization-usage/table_storage_metrics) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TABLES](/sql-reference/organization-usage/tables) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TAG\_REFERENCES](/sql-reference/organization-usage/tag_references) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TAGS](/sql-reference/organization-usage/tags) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TASKS](/sql-reference/organization-usage/tasks) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TASK\_HISTORY](/sql-reference/organization-usage/task_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TASK\_VERSIONS](/sql-reference/organization-usage/task_versions) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TRI\_SECRET\_SECURE\_HISTORY](/sql-reference/organization-usage/tri-secret-secure-history) | Historical | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TRUST\_CENTER\_FINDINGS](/sql-reference/organization-usage/trust_center_findings) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [TYPES](/sql-reference/organization-usage/types) | Object | 24 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) [2] | Historical | 72 hours |  |
| [USERS](/sql-reference/organization-usage/users) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [VIEWS](/sql-reference/organization-usage/views) | Object | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [WAREHOUSE\_EVENTS\_HISTORY](/sql-reference/organization-usage/warehouse_events_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [WAREHOUSE\_LOAD\_HISTORY](/sql-reference/organization-usage/warehouse_load_history) | Historical | 3 hours | [Premium view](/user-guide/organization-accounts-premium-views) (only available in organization account). |
| [WAREHOUSE\_METERING\_HISTORY](/sql-reference/organization-usage/warehouse_metering_history) | Historical | 24 hours | Data retained for 1 year. |

Expand

Show lessSee more

[1] All latency times are approximate; in some instances, the actual latency may be lower.

[2] The organization billing views do not display the actual, final amount because some adjustments are made at the end of the month. Customers who signed a contract through a Snowflake reseller cannot access data in these views.

## Accessing the ORGANIZATION\_USAGE schema

The ORGANIZATION\_USAGE schema is available in the [organization account](/user-guide/organization-accounts) and a regular account that has the ORGADMIN role enabled. How you access the views in the schema differs depending on which type of account you are using. For details about accessing views, see the following:

- [Access schema in the organization account](#label-org-usage-access-org-account)
- [Access schema in an ORGADMIN-enabled account](#label-org-usage-access-orgadmin-account)

Note

The views in the ORGANIZATION\_USAGE schema are currently not available in
[US SnowGov Regions](/user-guide/intro-regions#label-intro-regions-snowgov-regions) on AWS GovCloud and Microsoft Azure Government.

### Access schema in the organization account

By default, only users granted the GLOBALORGADMIN role can access ORGANIZATION\_USAGE views in the [organization account](/user-guide/organization-accounts).

To grant access to other users, the organization administrator can grant the appropriate *application role* to an account role or user.

Users who have been granted the SNOWFLAKE.ORG\_USAGE\_ADMIN application role can access all views in the ORGANIZATION\_USAGE schema of the
organization account. The following example lets user `joe` access all views in the schema:

Copy code

```
USE ROLE GLOBALORGADMIN;

GRANT APPLICATION ROLE SNOWFLAKE.ORG_USAGE_ADMIN TO ROLE custom_role;

GRANT ROLE custom_role TO USER joe;
```

The organization administrator can also grant access on a more granular level. For example, the ORGANIZATION\_OBJECT\_VIEWER application role
grants access to the DATABASES view but does not grant access to the TASK\_HISTORY view.

Use the following list to determine which application role grants access to a specific view. These application roles are in the SNOWFLAKE
application. Use the fully qualified name of the application role when granting it to another role (for example,
SNOWFLAKE.ORGANIZATION\_USAGE\_VIEWER).

| View | Required application role |
| --- | --- |
| [ACCESS\_HISTORY view](/sql-reference/organization-usage/access_history) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [ACCOUNTS view](/sql-reference/organization-usage/accounts) | ORGANIZATION\_ACCOUNTS\_VIEWER |
| [AGGREGATE\_QUERY\_HISTORY view](/sql-reference/organization-usage/aggregate_query_history) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [AGGREGATION\_POLICIES view](/sql-reference/organization-usage/aggregation_policies) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [ALERT\_HISTORY view](/sql-reference/organization-usage/alert_history) | ORGANIZATION\_USAGE\_VIEWER |
| [AUTOMATIC\_CLUSTERING\_HISTORY view](/sql-reference/organization-usage/automatic_clustering_history) | ORGANIZATION\_USAGE\_VIEWER |
| [CATALOG\_LINKED\_DATABASE\_USAGE\_HISTORY view](/sql-reference/organization-usage/catalog_linked_database_usage_history) | ORGANIZATION\_USAGE\_VIEWER |
| [CLASSES view](/sql-reference/organization-usage/classes) | ORGANIZATION\_USAGE\_VIEWER |
| [CLASS\_INSTANCES view](/sql-reference/organization-usage/class_instances) | ORGANIZATION\_USAGE\_VIEWER |
| [COLUMNS view](/sql-reference/organization-usage/columns) | ORGANIZATION\_OBJECT\_VIEWER |
| [COLUMN\_QUERY\_PRUNING\_HISTORY view](/sql-reference/organization-usage/column_query_pruning_history) | ORGANIZATION\_USAGE\_VIEWER |
| [COMPLETE\_TASK\_GRAPHS view](/sql-reference/organization-usage/complete_task_graphs) | ORGANIZATION\_OBJECT\_VIEWER |
| [CONTACTS view](/sql-reference/organization-usage/contacts) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [CONTACT\_REFERENCES view](/sql-reference/organization-usage/contact_references) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [CONTRACT\_ITEMS view](/sql-reference/organization-usage/contract_items) | ORGANIZATION\_BILLING\_VIEWER |
| [COPY\_HISTORY view](/sql-reference/organization-usage/copy_history) | ORGANIZATION\_USAGE\_VIEWER |
| [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/organization-usage/database_storage_usage_history) | ORGANIZATION\_USAGE\_VIEWER |
| [DATABASES view](/sql-reference/organization-usage/databases) | ORGANIZATION\_OBJECT\_VIEWER |
| [DATA\_CLASSIFICATION\_HISTORY view](/sql-reference/organization-usage/data_classification_history) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [DATA\_CLASSIFICATION\_LATEST view](/sql-reference/organization-usage/data_classification_latest) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [DATA\_TRANSFER\_DAILY\_HISTORY view](/sql-reference/organization-usage/data_transfer_daily_history) | ORGANIZATION\_USAGE\_VIEWER |
| [DATA\_TRANSFER\_HISTORY view](/sql-reference/organization-usage/data_transfer_history) | ORGANIZATION\_USAGE\_VIEWER |
| [DYNAMIC\_TABLE\_REFRESH\_HISTORY view](/sql-reference/organization-usage/dynamic_table_refresh_history) | ORGANIZATION\_USAGE\_VIEWER |
| [FILE\_FORMATS view](/sql-reference/organization-usage/file_formats) | ORGANIZATION\_OBJECT\_VIEWER |
| [FUNCTIONS view](/sql-reference/organization-usage/functions) | ORGANIZATION\_OBJECT\_VIEWER |
| [GRANTS\_TO\_ROLES view](/sql-reference/organization-usage/grants_to_roles) | ORGANIZATION\_SECURITY\_VIEWER |
| [GRANTS\_TO\_SHARES view](/sql-reference/organization-usage/grants_to_shares) | ORGANIZATION\_SECURITY\_VIEWER |
| [GRANTS\_TO\_USERS view](/sql-reference/organization-usage/grants_to_users) | ORGANIZATION\_SECURITY\_VIEWER |
| [HYBRID\_TABLES view](/sql-reference/organization-usage/hybrid_tables) | ORGANIZATION\_OBJECT\_VIEWER |
| [INDEX\_COLUMNS view](/sql-reference/organization-usage/index_columns) | ORGANIZATION\_OBJECT\_VIEWER |
| [INDEXES view](/sql-reference/organization-usage/indexes) | ORGANIZATION\_OBJECT\_VIEWER |
| [JOIN\_POLICIES view](/sql-reference/organization-usage/join_policies) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [LISTING\_AUTO\_FULFILLMENT\_USAGE\_HISTORY view](/sql-reference/organization-usage/listing_auto_fulfillment_usage_history) | ORGANIZATION\_BILLING\_VIEWER |
| [LISTINGS view](/sql-reference/organization-usage/listings) | ORGANIZATION\_SECURITY\_VIEWER |
| [LOAD\_HISTORY view](/sql-reference/organization-usage/load_history) | ORGANIZATION\_USAGE\_VIEWER |
| [LOCK\_WAIT\_HISTORY view](/sql-reference/organization-usage/lock_wait_history) | ORGANIZATION\_USAGE\_VIEWER |
| [LOGIN\_HISTORY view](/sql-reference/organization-usage/login_history) | ORGANIZATION\_SECURITY\_VIEWER |
| [MARKETPLACE\_DISBURSEMENT\_REPORT View](/collaboration/views/marketplace-disbursement-report-org) | ORGANIZATION\_BILLING\_VIEWER |
| [MARKETPLACE\_PAID\_USAGE\_DAILY View](/collaboration/views/marketplace-paid-usage-daily-org) | ORGANIZATION\_USAGE\_VIEWER |
| MARKETPLACE\_PURCHASE\_EVENTS view | ORGANIZATION\_BILLING\_VIEWER |
| [MASKING\_POLICIES view](/sql-reference/organization-usage/masking_policies) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [MATERIALIZED\_VIEW\_REFRESH\_HISTORY view](/sql-reference/organization-usage/materialized_view_refresh_history) | ORGANIZATION\_USAGE\_VIEWER |
| [METERING\_DAILY\_HISTORY view](/sql-reference/organization-usage/metering_daily_history) | ORGANIZATION\_USAGE\_VIEWER |
| [METERING\_HISTORY view](/sql-reference/organization-usage/metering_history) | ORGANIZATION\_USAGE\_VIEWER |
| [MONETIZED\_USAGE\_DAILY](/collaboration/views/monetized-usage-daily-org) | ORGANIZATION\_USAGE\_VIEWER |
| [NOTEBOOKS\_CONTAINER\_RUNTIME\_HISTORY view](/sql-reference/organization-usage/notebooks_container_runtime_history) | ORGANIZATION\_USAGE\_VIEWER |
| [OBJECT\_ACCESS\_REQUEST\_HISTORY view](/sql-reference/organization-usage/object_access_request_history) | ORGANIZATION\_USAGE\_VIEWER |
| [OBJECT\_DEPENDENCIES view](/sql-reference/organization-usage/object_dependencies) | ORGANIZATION\_OBJECT\_VIEWER |
| [PASSWORD\_POLICIES view](/sql-reference/organization-usage/password_policies) | ORGANIZATION\_SECURITY\_VIEWER |
| [PIPE\_USAGE\_HISTORY view](/sql-reference/organization-usage/pipe_usage_history) | ORGANIZATION\_USAGE\_VIEWER |
| [PIPES view](/sql-reference/organization-usage/pipes) | ORGANIZATION\_OBJECT\_VIEWER |
| [POLICY\_REFERENCES view](/sql-reference/organization-usage/policy_references) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [PRIVACY\_POLICIES view](/sql-reference/organization-usage/privacy_policies) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [PROCEDURES view](/sql-reference/organization-usage/procedures) | ORGANIZATION\_OBJECT\_VIEWER |
| [PROJECTION\_POLICIES view](/sql-reference/organization-usage/projection_policies) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [QUERY\_ACCELERATION\_ELIGIBLE view](/sql-reference/organization-usage/query_acceleration_eligible) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [QUERY\_ACCELERATION\_HISTORY view](/sql-reference/organization-usage/query_acceleration_history) | - ORGANIZATION\_GOVERNANCE\_VIEWER - ORGANIZATION\_USAGE\_VIEWER |
| [QUERY\_ATTRIBUTION\_HISTORY view](/sql-reference/organization-usage/query_attribution_history) | - ORGANIZATION\_GOVERNANCE\_VIEWER - ORGANIZATION\_USAGE\_VIEWER |
| [QUERY\_HISTORY view](/sql-reference/organization-usage/query_history) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [QUERY\_INSIGHTS view](/sql-reference/organization-usage/query_insights) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [QUERY\_METERING\_HISTORY view (coming soon)](/sql-reference/organization-usage/query_metering_history) | - ORGANIZATION\_GOVERNANCE\_VIEWER - ORGANIZATION\_USAGE\_VIEWER |
| [RATE\_SHEET\_DAILY view](/sql-reference/organization-usage/rate_sheet_daily) | ORGANIZATION\_BILLING\_VIEWER |
| [REFERENTIAL\_CONSTRAINTS view](/sql-reference/organization-usage/referential_constraints) | ORGANIZATION\_OBJECT\_VIEWER |
| [REMAINING\_BALANCE\_DAILY view](/sql-reference/organization-usage/remaining_balance_daily) | ORGANIZATION\_BILLING\_VIEWER |
| [REPLICATION\_GROUPS view](/sql-reference/organization-usage/replication_groups) | ORGANIZATION\_OBJECT\_VIEWER |
| [REPLICATION\_GROUP\_REFRESH\_HISTORY view](/sql-reference/organization-usage/replication_group_refresh_history) | ORGANIZATION\_USAGE\_VIEWER |
| [REPLICATION\_GROUP\_USAGE\_HISTORY view](/sql-reference/organization-usage/replication_group_usage_history) | ORGANIZATION\_USAGE\_VIEWER |
| [REPLICATION\_USAGE\_HISTORY view](/sql-reference/organization-usage/replication_usage_history) | ORGANIZATION\_USAGE\_VIEWER |
| [RESOURCE\_MONITORS view](/sql-reference/organization-usage/resource_monitors) | ORGANIZATION\_OBJECT\_VIEWER |
| [ROLES view](/sql-reference/organization-usage/roles) | ORGANIZATION\_SECURITY\_VIEWER |
| [ROW\_ACCESS\_POLICIES view](/sql-reference/organization-usage/row_access_policies) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [SCHEMATA view](/sql-reference/organization-usage/schemata) | ORGANIZATION\_OBJECT\_VIEWER |
| [SEARCH\_OPTIMIZATION\_BENEFITS view](/sql-reference/organization-usage/search_optimization_benefits) | ORGANIZATION\_USAGE\_VIEWER |
| [SEARCH\_OPTIMIZATION\_HISTORY view](/sql-reference/organization-usage/search_optimization_history) | ORGANIZATION\_USAGE\_VIEWER |
| [SECRETS view](/sql-reference/organization-usage/secrets) | ORGANIZATION\_SECURITY\_VIEWER |
| [SEQUENCES view](/sql-reference/organization-usage/sequences) | ORGANIZATION\_OBJECT\_VIEWER |
| [SESSION\_POLICIES view](/sql-reference/organization-usage/session_policies) | ORGANIZATION\_SECURITY\_VIEWER |
| [SESSIONS view](/sql-reference/organization-usage/sessions) | ORGANIZATION\_SECURITY\_VIEWER |
| [SHARES view](/sql-reference/organization-usage/shares) | ORGANIZATION\_SECURITY\_VIEWER |
| [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY view](/sql-reference/organization-usage/snowpipe_streaming_channel_history) | ORGANIZATION\_USAGE\_VIEWER |
| [SNOWPIPE\_STREAMING\_CLIENT\_HISTORY view](/sql-reference/organization-usage/snowpipe_streaming_client_history) | ORGANIZATION\_USAGE\_VIEWER |
| [SNOWPIPE\_STREAMING\_FILE\_MIGRATION\_HISTORY view](/sql-reference/organization-usage/snowpipe_streaming_file_migration_history) | ORGANIZATION\_USAGE\_VIEWER |
| [STAGE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/organization-usage/stage_storage_usage_history) | ORGANIZATION\_USAGE\_VIEWER |
| [STAGES view](/sql-reference/organization-usage/stages) | ORGANIZATION\_OBJECT\_VIEWER |
| [STORAGE\_LIFECYCLE\_POLICIES view](/sql-reference/organization-usage/storage_lifecycle_policies) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [STORAGE\_LIFECYCLE\_POLICY\_HISTORY view](/sql-reference/organization-usage/storage_lifecycle_policy_history) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [STORAGE\_DAILY\_HISTORY view](/sql-reference/organization-usage/storage_daily_history) | ORGANIZATION\_USAGE\_VIEWER |
| [STORAGE\_USAGE view](/sql-reference/organization-usage/storage_usage) | ORGANIZATION\_USAGE\_VIEWER |
| [TABLE\_CONSTRAINTS view](/sql-reference/organization-usage/table_constraints) | ORGANIZATION\_OBJECT\_VIEWER |
| [TABLE\_DML\_HISTORY view](/sql-reference/organization-usage/table_dml_history) | ORGANIZATION\_USAGE\_VIEWER |
| [TABLE\_PRUNING\_HISTORY view](/sql-reference/organization-usage/table_pruning_history) | ORGANIZATION\_USAGE\_VIEWER |
| [TABLE\_QUERY\_PRUNING\_HISTORY view](/sql-reference/organization-usage/table_query_pruning_history) | ORGANIZATION\_USAGE\_VIEWER |
| [TABLE\_STORAGE\_METRICS view](/sql-reference/organization-usage/table_storage_metrics) | ORGANIZATION\_USAGE\_VIEWER |
| [TABLES view](/sql-reference/organization-usage/tables) | ORGANIZATION\_OBJECT\_VIEWER |
| [TAG\_REFERENCES view](/sql-reference/organization-usage/tag_references) | ORGANIZATION\_GOVERNANCE\_VIEWER |
| [TAGS view](/sql-reference/organization-usage/tags) | ORGANIZATION\_OBJECT\_VIEWER |
| [TASKS view](/sql-reference/organization-usage/tasks) | ORGANIZATION\_OBJECT\_VIEWER |
| [TASK\_HISTORY view](/sql-reference/organization-usage/task_history) | ORGANIZATION\_USAGE\_VIEWER |
| [TASK\_VERSIONS view](/sql-reference/organization-usage/task_versions) | ORGANIZATION\_OBJECT\_VIEWER |
| [TRI\_SECRET\_SECURE\_HISTORY view](/sql-reference/organization-usage/tri-secret-secure-history) | ORGANIZATION\_SECURITY\_VIEWER |
| [TRUST\_CENTER\_FINDINGS view](/sql-reference/organization-usage/trust_center_findings) | ORGANIZATION\_SECURITY\_VIEWER |
| [USAGE\_IN\_CURRENCY\_DAILY view](/sql-reference/organization-usage/usage_in_currency_daily) | ORGANIZATION\_BILLING\_VIEWER |
| [USERS view](/sql-reference/organization-usage/users) | ORGANIZATION\_SECURITY\_VIEWER |
| [VIEWS view](/sql-reference/organization-usage/views) | ORGANIZATION\_OBJECT\_VIEWER |
| [WAREHOUSE\_EVENTS\_HISTORY view](/sql-reference/organization-usage/warehouse_events_history) | ORGANIZATION\_USAGE\_VIEWER |
| [WAREHOUSE\_LOAD\_HISTORY view](/sql-reference/organization-usage/warehouse_load_history) | ORGANIZATION\_USAGE\_VIEWER |
| [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/organization-usage/warehouse_metering_history) | ORGANIZATION\_USAGE\_VIEWER |

Expand

Show lessSee more

### Access schema in an ORGADMIN-enabled account

An ORGADMIN-enabled account is a regular account that has the ORGADMIN role enabled. Within an ORGADMIN-enabled account, anyone who has
access to the shared SNOWFLAKE database has access to the ORGANIZATION\_USAGE schema. By default, only the ACCOUNTADMIN role has privileges
to this database, which means the ORGADMIN role does not have the necessary privileges. To grant these privileges to the ORGADMIN role, see [Enabling other roles to use schemas in the SNOWFLAKE database](/sql-reference/account-usage#label-enabling-usage-for-other-roles).

To grant access to non-administrators, the organization administrator can grant the appropriate *database role* to an account role or user.

Use the following list to determine which database role grants access to specific views.

The ORGANIZATION\_USAGE\_VIEWER, ORGANIZATION\_BILLING\_VIEWER, and ORGANIZATION\_ACCOUNTS\_VIEWER SNOWFLAKE database roles are granted the SELECT privilege on Organization Usage views in the shared SNOWFLAKE database.

| View | ORGANIZATION\_BILLING\_VIEWER Role | ORGANIZATION\_USAGE\_VIEWER Role | ORGANIZATION\_ACCOUNTS\_VIEWER Role |
| --- | --- | --- | --- |
| [ACCOUNTS view](/sql-reference/organization-usage/accounts) |  |  | ✔ |
| [ANOMALIES\_IN\_CURRENCY\_DAILY view](/sql-reference/organization-usage/anomalies_in_currency_daily) | ✔ |  |  |
| [CONTRACT\_ITEMS view](/sql-reference/organization-usage/contract_items) | ✔ |  |  |
| [LISTING\_AUTO\_FULFILLMENT\_USAGE\_HISTORY view](/sql-reference/organization-usage/listing_auto_fulfillment_usage_history) | ✔ |  |  |
| [RATE\_SHEET\_DAILY view](/sql-reference/organization-usage/rate_sheet_daily) | ✔ |  |  |
| [REMAINING\_BALANCE\_DAILY view](/sql-reference/organization-usage/remaining_balance_daily) | ✔ |  |  |
| [USAGE\_IN\_CURRENCY\_DAILY view](/sql-reference/organization-usage/usage_in_currency_daily) | ✔ |  |  |
| [MARKETPLACE\_DISBURSEMENT\_REPORT View](/collaboration/views/marketplace-disbursement-report-org) | ✔ |  |  |
| [DATA\_TRANSFER\_DAILY\_HISTORY view](/sql-reference/organization-usage/data_transfer_daily_history) |  | ✔ |  |
| [DATA\_TRANSFER\_HISTORY view](/sql-reference/organization-usage/data_transfer_history) |  | ✔ |  |
| [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/organization-usage/database_storage_usage_history) |  | ✔ |  |
| [AUTOMATIC\_CLUSTERING\_HISTORY view](/sql-reference/organization-usage/automatic_clustering_history) |  | ✔ |  |
| [MARKETPLACE\_PAID\_USAGE\_DAILY View](/collaboration/views/marketplace-paid-usage-daily-org) |  | ✔ |  |
| [MATERIALIZED\_VIEW\_REFRESH\_HISTORY view](/sql-reference/account-usage/materialized_view_refresh_history) |  | ✔ |  |
| [METERING\_DAILY\_HISTORY view](/sql-reference/organization-usage/metering_daily_history) |  | ✔ |  |
| [MONETIZED\_USAGE\_DAILY View](/collaboration/views/monetized-usage-daily-org) |  | ✔ |  |
| [PIPE\_USAGE\_HISTORY view](/sql-reference/organization-usage/pipe_usage_history) |  | ✔ |  |
| [QUERY\_ACCELERATION\_HISTORY view](/sql-reference/organization-usage/query_acceleration_history) |  | ✔ |  |
| [REPLICATION\_GROUP\_USAGE\_HISTORY view](/sql-reference/organization-usage/replication_group_usage_history) |  | ✔ |  |
| [REPLICATION\_USAGE\_HISTORY view](/sql-reference/organization-usage/replication_usage_history) |  | ✔ |  |
| [SEARCH\_OPTIMIZATION\_HISTORY view](/sql-reference/organization-usage/search_optimization_history) |  | ✔ |  |
| [STAGE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/organization-usage/stage_storage_usage_history) |  | ✔ |  |
| [STORAGE\_DAILY\_HISTORY view](/sql-reference/organization-usage/storage_daily_history) |  | ✔ |  |
| [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/organization-usage/warehouse_metering_history) |  | ✔ |  |

Expand

Show lessSee more

For more information, refer to [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role).

## General usage notes

The Snowflake-specific views are subject to change. Avoid selecting all columns from these views. Instead, select the columns that you want.
For example, if you want the `name` column, use `SELECT name`, rather than `SELECT *`.

Treat every **historical** ORGANIZATION\_USAGE query as a warehouse job across all accounts: open the reference topic for that **named view**
(for example [QUERY\_HISTORY](/sql-reference/organization-usage/query_history) or [COPY\_HISTORY](/sql-reference/organization-usage/copy_history)),
**constrain its primary time column**, **list the columns you need**, and add **`account_name IN (…)`** when that column exists on the view and you are
not reporting on the full organization. Latency in [ORGANIZATION\_USAGE views](#label-organization-usage-views) is freshness **per view**, not query cost.

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

### Performance

ORGANIZATION\_USAGE views can contain large volumes of data across every account in your organization. **For each view you query**, follow
the same two rules on **historical** and other large views:

1. **Always bound the time range** on that view’s primary time column (see the table below, then that view’s reference topic for the exact name and type).
2. **Select explicit columns** instead of `SELECT *`.

Note

This page recommends query patterns and time filters for ORGANIZATION\_USAGE. Like [Warehouse considerations](/user-guide/warehouses-considerations), it’s general guidance only: not a service commitment, requirement, or guaranteed outcome. See each view’s reference topic for authoritative column definitions and semantics.

Note

For filters, use documented columns from each view’s reference topic, especially the **primary time filter column** in the following table. Internal ingestion, telemetry, or storage identifiers are not a supported customer SQL surface and can change in any release. Ignore them if they appear in older previews.

### Historical views and time filters

Most large ORGANIZATION\_USAGE views expose a primary timestamp or date column. **Put a bounded range on that column in every query for that view**
(for example `WHERE start_time >= … AND start_time < …` on [QUERY\_HISTORY](/sql-reference/organization-usage/query_history), using
`start_time` because that is the primary time filter column for QUERY\_HISTORY in the table below). Open-ended time ranges force
Snowflake to consider the full history across your organization before it can return rows.

The following table lists common historical views (and similar large scans) where bounded time predicates matter most. The table is
illustrative, not exhaustive; apply the same bounded-time approach to other historical ORGANIZATION\_USAGE views, using each view’s reference
topic to choose the column. For each row below, start with the **primary time filter column** in a bounded predicate (for example
`WHERE col >= … AND col < …`). View revisions
(for example `v30`, `v21`) change over time; use each view’s reference topic for authoritative column names and types.

| View | Primary time filter column |
| --- | --- |
| [QUERY\_HISTORY](/sql-reference/organization-usage/query_history) | `start_time` |
| [QUERY\_ACCELERATION\_ELIGIBLE](/sql-reference/organization-usage/query_acceleration_eligible) | `start_time` |
| [BACKUP\_OPERATION\_HISTORY](/sql-reference/organization-usage/backup_operation_history) | `start_time` |
| [SNAPSHOT\_OPERATION\_HISTORY](/sql-reference/organization-usage/snapshot_operation_history) | `start_time` |
| [ACCESS\_HISTORY](/sql-reference/organization-usage/access_history) | `query_start_time` |
| [LOGIN\_HISTORY](/sql-reference/organization-usage/login_history) | `event_timestamp` |
| [SESSIONS](/sql-reference/organization-usage/sessions) | `created_on` |
| [COPY\_HISTORY](/sql-reference/organization-usage/copy_history) | `last_load_time` |
| [LOAD\_HISTORY](/sql-reference/organization-usage/load_history) | `last_load_time` |
| [LOCK\_WAIT\_HISTORY](/sql-reference/organization-usage/lock_wait_history) | `requested_at` |
| [METERING\_HISTORY](/sql-reference/organization-usage/metering_history) | `start_time` (bounded range). When you must split usage by Snowflake service, include `service_type` in the same predicate. |
| [QUERY\_ATTRIBUTION\_HISTORY](/sql-reference/organization-usage/query_attribution_history) | `start_time` |
| [QUERY\_INSIGHTS](/sql-reference/organization-usage/query_insights) | `start_time` |
| [AGGREGATE\_QUERY\_HISTORY](/sql-reference/organization-usage/aggregate_query_history) | `interval_start_time` |
| [WAREHOUSE\_EVENTS\_HISTORY](/sql-reference/organization-usage/warehouse_events_history) | `timestamp` |
| [COMPLETE\_TASK\_GRAPHS](/sql-reference/organization-usage/complete_task_graphs) | `query_start_time` |
| [TASK\_HISTORY](/sql-reference/organization-usage/task_history) | `scheduled_time` |
| [ALERT\_HISTORY](/sql-reference/organization-usage/alert_history) | `scheduled_time` |
| [OUTBOUND\_PRIVATELINK\_ENDPOINTS](/sql-reference/organization-usage/outbound_privatelink_endpoints) | `created_on` |
| [CATALOG\_LINKED\_DATABASE\_USAGE\_HISTORY](/sql-reference/organization-usage/catalog_linked_database_usage_history) | `start_time` |
| [COLUMN\_QUERY\_PRUNING\_HISTORY](/sql-reference/organization-usage/column_query_pruning_history) | `interval_start_time` |
| [DATA\_CLASSIFICATION\_HISTORY](/sql-reference/organization-usage/data_classification_history) | `classified_on` |
| [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/organization-usage/dynamic_table_refresh_history) | `refresh_start_time` |
| [NOTEBOOKS\_CONTAINER\_RUNTIME\_HISTORY](/sql-reference/organization-usage/notebooks_container_runtime_history) | `start_time` |
| [OBJECT\_ACCESS\_REQUEST\_HISTORY](/sql-reference/organization-usage/object_access_request_history) | `timestamp` |
| [SEARCH\_OPTIMIZATION\_BENEFITS](/sql-reference/organization-usage/search_optimization_benefits) | `start_time` |
| [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY](/sql-reference/organization-usage/snowpipe_streaming_channel_history) | `created_on` |
| [SNOWPIPE\_STREAMING\_CLIENT\_HISTORY](/sql-reference/organization-usage/snowpipe_streaming_client_history) | `event_timestamp` |
| [SNOWPIPE\_STREAMING\_FILE\_MIGRATION\_HISTORY](/sql-reference/organization-usage/snowpipe_streaming_file_migration_history) | `start_time` |
| [STORAGE\_USAGE](/sql-reference/organization-usage/storage_usage) | `usage_date` |
| [TABLE\_DML\_HISTORY](/sql-reference/organization-usage/table_dml_history) | `start_time` |
| [TABLE\_PRUNING\_HISTORY](/sql-reference/organization-usage/table_pruning_history) | `start_time` |
| [TABLE\_QUERY\_PRUNING\_HISTORY](/sql-reference/organization-usage/table_query_pruning_history) | `interval_start_time` |

Expand

Show lessSee more

Before joining several ORGANIZATION\_USAGE views, apply bounded time predicates on **each view you reference** (for example bound
`QUERY_HISTORY.start_time` and `COPY_HISTORY.last_load_time` separately when both appear in the join). For dashboards that
rerun the same logic, materialize results in a table you own and refresh it on a schedule instead of rescanning wide history.

### Good query patterns

Each example names the **ORGANIZATION\_USAGE** view it applies to. Every example follows the two rules above: **bounded time** on that view’s
primary time column (from the table) and **explicit columns** in the `SELECT` list. When that view includes `account_name`,
add `AND account_name IN (…)` so the scan is limited to the accounts you care about.

**[QUERY\_HISTORY](/sql-reference/organization-usage/query_history)**: Bound `start_time`.

> Copy code
>
> ```
> SELECT query_id, start_time, user_name, warehouse_name
>   FROM SNOWFLAKE.ORGANIZATION_USAGE.QUERY_HISTORY
>   WHERE start_time > '2025-01-01 00:00:00'::timestamp_ltz;
> ```

**[COPY\_HISTORY](/sql-reference/organization-usage/copy_history)**: Bound `last_load_time`.

> Copy code
>
> ```
> SELECT account_name, file_name, error_count, status, last_load_time
>   FROM SNOWFLAKE.ORGANIZATION_USAGE.COPY_HISTORY
>   WHERE last_load_time >= '2025-01-01 00:00:00'::timestamp_ltz
>     AND last_load_time < '2025-02-01 00:00:00'::timestamp_ltz;
> ```

**[DATABASES](/sql-reference/organization-usage/databases)**: Object inventory (no time predicate in this pattern; still list columns).

> Copy code
>
> ```
> SELECT database_name, account_name
>   FROM SNOWFLAKE.ORGANIZATION_USAGE.DATABASES;
> ```

**[USERS](/sql-reference/organization-usage/users)**: Filter `account_name` when you do not need every account.

> Copy code
>
> ```
> SELECT account_name, name, login_name
>   FROM SNOWFLAKE.ORGANIZATION_USAGE.USERS
>   WHERE account_name IN ('ACC1', 'ACC2', 'ACC3');
> ```

The **DATABASES** and **USERS** examples use **object-style** views with smaller result sets; keep **explicit column lists** so downstream schemas
stay stable when Snowflake adds columns.

### Query patterns to avoid (history views)

The following anti-patterns are shown for **specific views**; the same issues apply to any large history view when you omit a bounded time
predicate on that view’s primary time column (see the table above).

**[QUERY\_HISTORY](/sql-reference/organization-usage/query_history)**: Unbounded aggregate.

> Copy code
>
> ```
> SELECT COUNT(*) FROM SNOWFLAKE.ORGANIZATION_USAGE.QUERY_HISTORY;
> ```

**[LOAD\_HISTORY](/sql-reference/organization-usage/load_history)**: `LIMIT` without a time predicate on `last_load_time`.

> Copy code
>
> ```
> SELECT * FROM SNOWFLAKE.ORGANIZATION_USAGE.LOAD_HISTORY LIMIT 1;
> ```

**[QUERY\_ATTRIBUTION\_HISTORY](/sql-reference/organization-usage/query_attribution_history)**: `SELECT *` with no time predicate on `start_time`.

> Copy code
>
> ```
> SELECT * FROM SNOWFLAKE.ORGANIZATION_USAGE.QUERY_ATTRIBUTION_HISTORY;
> ```

### Why unbounded patterns are expensive

ORGANIZATION\_USAGE views surface organization-wide history. When a query does not include selective time predicates (and `account_name`
filters when you only need certain accounts), Snowflake may need to consider a very large amount of history before it returns rows or completes
an aggregate. On wide views such as [QUERY\_HISTORY](/sql-reference/organization-usage/query_history), that work can scale to very large row
counts, which increases run time and warehouse cost.

The **Latency** values in [ORGANIZATION\_USAGE views](/sql-reference/organization-usage#label-organization-usage-views) describe how current the data is **for each listed view**; they do not
remove the need to constrain time ranges (and `account_name` when applicable) on those same views for large scans.
