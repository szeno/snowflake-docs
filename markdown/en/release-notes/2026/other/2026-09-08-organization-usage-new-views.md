# Sep 08, 2026: New ORGANIZATION\_USAGE premium views

The ORGANIZATION\_USAGE schema now includes 26 new [premium views](/user-guide/organization-accounts-premium-views)
that are available in the [organization account](/user-guide/organization-accounts). These views provide
visibility into governance policies, contacts, data classification, storage and pruning, Snowpipe Streaming,
replication, tasks, and other object metadata across all accounts in your organization.

The new views are:

- [AGGREGATION\_POLICIES](/sql-reference/organization-usage/aggregation_policies): Lists the aggregation policies defined in each account in your organization.
- [CATALOG\_LINKED\_DATABASE\_USAGE\_HISTORY](/sql-reference/organization-usage/catalog_linked_database_usage_history): Returns credit usage for catalog-linked databases in each account over the last 12 months.
- [COLUMN\_QUERY\_PRUNING\_HISTORY](/sql-reference/organization-usage/column_query_pruning_history): Helps you understand data access patterns during query execution, including column-level pruning details.
- [CONTACT\_REFERENCES](/sql-reference/organization-usage/contact_references): Returns one row for each association between a contact and an object.
- [CONTACTS](/sql-reference/organization-usage/contacts): Returns one row for each contact in an account.
- [DATA\_CLASSIFICATION\_HISTORY](/sql-reference/organization-usage/data_classification_history): Returns historical sensitive data classification results for each table over the last 365 days.
- [DATA\_CLASSIFICATION\_LATEST](/sql-reference/organization-usage/data_classification_latest): Returns one row for the most recent classification result for each classified table.
- [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/organization-usage/dynamic_table_refresh_history): Returns dynamic table refresh history for accounts in your organization.
- [HYBRID\_TABLES](/sql-reference/organization-usage/hybrid_tables): Returns one row for each hybrid table in an account.
- [INDEX\_COLUMNS](/sql-reference/organization-usage/index_columns): Returns one row for each column in an index in an account.
- [INDEXES](/sql-reference/organization-usage/indexes): Returns one row for each index in an account.
- [JOIN\_POLICIES](/sql-reference/organization-usage/join_policies): Returns one row for each join policy in an account.
- [NOTEBOOKS\_CONTAINER\_RUNTIME\_HISTORY](/sql-reference/organization-usage/notebooks_container_runtime_history): Returns hourly credit usage for notebooks running on Snowpark Container Services.
- [OBJECT\_ACCESS\_REQUEST\_HISTORY](/sql-reference/organization-usage/object_access_request_history): Returns audit history for object access request submission, approval, and rejection.
- [PRIVACY\_POLICIES](/sql-reference/organization-usage/privacy_policies): Returns one row for each privacy policy in an account.
- [PROJECTION\_POLICIES](/sql-reference/organization-usage/projection_policies): Returns one row for each projection policy in an account.
- [REPLICATION\_GROUPS](/sql-reference/organization-usage/replication_groups): Returns one row for each replication or failover group in an account.
- [SEARCH\_OPTIMIZATION\_BENEFITS](/sql-reference/organization-usage/search_optimization_benefits): Helps you determine the efficacy of pruning due to search optimization.
- [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY](/sql-reference/organization-usage/snowpipe_streaming_channel_history): Returns a historical record of Snowpipe Streaming channel metrics such as data volume, errors, and latency.
- [SNOWPIPE\_STREAMING\_CLIENT\_HISTORY](/sql-reference/organization-usage/snowpipe_streaming_client_history): Returns Snowpipe Streaming client load activity for the last 365 days.
- [SNOWPIPE\_STREAMING\_FILE\_MIGRATION\_HISTORY](/sql-reference/organization-usage/snowpipe_streaming_file_migration_history): Returns Snowpipe Streaming file migration history for the last 365 days.
- [STORAGE\_USAGE](/sql-reference/organization-usage/storage_usage): Returns average daily storage usage in bytes for each account for the last 365 days.
- [TABLE\_DML\_HISTORY](/sql-reference/organization-usage/table_dml_history): Helps you determine the magnitude and effects of DML operations performed on tables.
- [TABLE\_PRUNING\_HISTORY](/sql-reference/organization-usage/table_pruning_history): Helps you determine the efficiency of pruning for all tables.
- [TABLE\_QUERY\_PRUNING\_HISTORY](/sql-reference/organization-usage/table_query_pruning_history): Helps you understand data access patterns during query execution at the table level.
- [TASKS](/sql-reference/organization-usage/tasks): Returns one row for each task in an account.

For more information about accessing premium views in the organization account, see [Access schema in the organization account](/sql-reference/organization-usage#label-org-usage-access-org-account).
