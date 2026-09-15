# SNOWFLAKE database roles

When an account is provisioned, the SNOWFLAKE database is automatically imported.
The database is an example of Snowflake using [Secure Data Sharing](/user-guide/data-sharing-gs) to provide object metadata and other usage metrics for your organization and accounts.

Access to schema objects in the SNOWFLAKE database is controlled by different [database roles](/user-guide/security-access-control-considerations#label-access-control-considerations-database-roles).
The following sections describe each SNOWFLAKE database role, its associated privileges, and the associated schema objects the role is granted access to.

## ACCOUNT\_USAGE schema

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

## READER\_ACCOUNT\_USAGE schema

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

## ORGANIZATION\_USAGE schema

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

## CORE schema

The CORE\_VIEWER SNOWFLAKE database role is granted to the PUBLIC role in all Snowflake accounts containing a shared SNOWFLAKE database.
The USAGE privilege is granted to all Snowflake-defined functions and bundles in the CORE schema.

### Budget class

The BUDGET\_CREATOR Snowflake database role is granted the USAGE privilege on the SNOWFLAKE.CORE schema and the BUDGET class
in the schema. This grant allows users with the BUDGET\_CREATOR role to create instances of the BUDGET class.

For more information, see [Create a custom role to create budgets](/user-guide/budgets/custom-budget#label-custom-budgets-owner-role).

### Tag objects

The CORE\_VIEWER database role is granted the APPLY privilege on the
[classification system tags](/user-guide/classify-intro#label-classify-classification-tags) SNOWFLAKE.CORE.PRIVACY\_CATEGORY and
SNOWFLAKE.CORE.SEMANTIC\_CATEGORY. These grants allow users with a role that is granted the CORE\_VIEWER database role to assign these system
tags to columns.

## ALERT schema

The ALERT\_VIEWER SNOWFLAKE database role is granted the USAGE privilege on the functions defined in this schema.

## ML schema

The ML\_USER SNOWFLAKE database role is granted to the PUBLIC role in all Snowflake accounts that contain a shared
SNOWFLAKE database and allows customers to access and use [ML functions](/guides-overview-ml-functions).
Users must also have the USAGE privilege on the ML schema to call these functions.

## MONITORING schema

The MONITORING\_VIEWER database role has the SELECT privilege on all views in the MONITORING schema.

The MONITORING\_VIEWER database role is granted to the PUBLIC role in all Snowflake accounts containing a shared SNOWFLAKE
database.

## SNOWFLAKE.CLASSIFICATION\_ADMIN database role

The SNOWFLAKE.CLASSIFICATION\_ADMIN database role allows a data engineer or steward to create an instance of the [CLASSIFICATION\_PROFILE](/sql-reference/classes/classification_profile) class.
A classification profile is used to implement [sensitive data classification](/user-guide/classify-auto).

## SNOWFLAKE.CORTEX\_AGENT\_USER database role

You can use the SNOWFLAKE.CORTEX\_AGENT\_USER database role to grant your users access to Snowflake Cortex Agents API without granting access to other Cortex
features. Using the Cortex Agents API requires *either* the SNOWFLAKE.CORTEX\_USER database role *or* the
SNOWFLAKE.CORTEX\_AGENT\_USER database role.

By default, the SNOWFLAKE.CORTEX\_USER database role is granted to the PUBLIC role. For fine-grained access control, revoke access from the PUBLIC role and grant access to the SNOWFLAKE.CORTEX\_AGENT\_USER database role.
For more information, see [Limiting access to specific roles](/user-guide/snowflake-cortex/cortex-agents-setup#label-snowflake-agents-access).

## SNOWFLAKE.AI\_FUNCTIONS\_USER database role

The SNOWFLAKE.AI\_FUNCTIONS\_USER database role is used to grant customers access to Snowflake Cortex scalar AI
functions (all Cortex AI functions except the aggregate functions AI\_AGG and AI\_SUMMARIZE\_AGG) without granting
access to Cortex services such as Cortex Agent, Cortex Analyst, Cortex Fine-tuning, or Cortex Search. Calling
scalar AI functions requires *either* the SNOWFLAKE.CORTEX\_USER database role *or* the
SNOWFLAKE.AI\_FUNCTIONS\_USER database role.

By default, this role is not granted to any roles. If you want users to have access to scalar AI functions,
grant this database role to appropriate roles. For details, see [Cortex LLM Functions required privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges).

## SNOWFLAKE.CORTEX\_EMBED\_USER database role

The SNOWFLAKE.CORTEX\_EMBED\_USER database role is used to grant customers access to Snowflake Cortex embedding functions AI\_EMBED,
AI\_MULTI\_EMBED, SNOWFLAKE.CORTEX.EMBED\_768, and SNOWFLAKE.CORTEX\_EMBED\_TEXT\_1024 without granting access to other Cortex
features. Calling these embedding functions requires *either* the SNOWFLAKE.CORTEX\_USER database role *or* the
SNOWFLAKE.CORTEX\_EMBED\_USER database role. This role is not granted to any roles by default.

By default, this role is not granted to any roles. If you want users to have access to the embedding functions,
grant this database role to appropriate roles. For details, see [Cortex LLM Functions required privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges)

## SNOWFLAKE.CORTEX\_REST\_API\_USER database role

The SNOWFLAKE.CORTEX\_REST\_API\_USER database role is used to grant customers access to the Snowflake
Cortex REST API without granting access to other Cortex features such as Cortex AI functions, Cortex Agent,
Cortex Analyst, Cortex Fine-tuning, or Cortex Search. Using the Cortex REST API requires *either* the
SNOWFLAKE.CORTEX\_USER database role *or* the SNOWFLAKE.CORTEX\_REST\_API\_USER database role.

By default, this role is not granted to any roles. If you want users to have access to the Cortex REST API
without granting broader Cortex privileges, grant this database role to appropriate roles.
For details, see [Limiting access using the Cortex REST API user role](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-rest-api-user-role).

## SNOWFLAKE.CORTEX\_USER database role

This SNOWFLAKE.CORTEX\_USER database role is used to grant customers access to Snowflake Cortex features.
By default, this role is granted to the PUBLIC role. The PUBLIC role is automatically granted
to all users and roles, so this allows all users in your account to use Snowflake Cortex LLM functions.

If you don’t want all users to have this privilege, you can revoke access from the PUBLIC role and grant access to specific roles.
For details, see [Cortex LLM Functions required privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges).

## SNOWFLAKE.COPILOT\_USER database role

The SNOWFLAKE.COPILOT\_USER database role allows customers to access Cortex Code features in Snowsight. Initially, this database role
is granted to the PUBLIC role. The PUBLIC role is automatically granted to all users and roles, so this allows all users in your account
to use Cortex Code. If you want to limit access to Cortex Code features in Snowsight, you can revoke access from the PUBLIC role and grant access to
specific roles. For details, see [Access control requirements](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-snowsight-access-control).

## Using SNOWFLAKE database roles

Administrators can use the [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role) to assign a SNOWFLAKE database role to another role,
which can then be granted to a user. This would allow the user to access a specific subset of views in the SNOWFLAKE database.

In the following example a role is created which can be used to view SNOWFLAKE database object metadata, and does the following:

1. Creates a custom role.
2. Grants the OBJECT\_VIEWER role to the custom role.
3. Grants the custom role to a user.

To create and grant the custom role, do the following:

1. Create the `CAN_VIEWMD` role, using [CREATE ROLE](/sql-reference/sql/create-role) that will be used to grant access to object metadata.

   Only users with the USERADMIN system role or higher, or another role with the CREATE ROLE privilege on the
   account, can create roles.

   Copy code

   ```
   CREATE ROLE CAN_VIEWMD COMMENT = 'This role can view metadata per SNOWFLAKE database role definitions';
   ```
2. Grant the OBJECT\_VIEWER role to the CAN\_VIEWMD role.

   Only users with the OWNERSHIP role can grant SNOWFLAKE database roles. For additional information, refer to [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role).

   Copy code

   ```
   GRANT DATABASE ROLE OBJECT_VIEWER TO ROLE CAN_VIEWMD;
   ```
3. Assign `CAN_VIEWMD` role to user `smith`.

   Only users with the SECURITYADMIN role can grant roles to users. For additional options, refer to [GRANT ROLE](/sql-reference/sql/grant-role).

   Copy code

   ```
   GRANT ROLE CAN_VIEWMD TO USER smith;
   ```
