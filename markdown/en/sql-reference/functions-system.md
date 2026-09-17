# System functions

Snowflake provides the following types of system functions:

- Control functions that allow you to execute actions in the system (for example, aborting a query).
- Information functions that return information about the system (for example, calculating the clustering depth of a table).
- Information functions that return information about queries (for example, information about EXPLAIN plans).

Many of these system functions have the prefix `SYSTEM$` (for example, `SYSTEM$TYPEOF`). For the system functions that use
this prefix, you must specify the prefix when calling the function. For example:

Copy code

```
SELECT SYSTEM$TYPEOF('a');
```

| Function Name | Notes |
| --- | --- |
| **Control** |  |
| [EXECUTE\_AI\_EVALUATION](/sql-reference/functions/execute_ai_evaluation) |  |
| [SYSTEM$ABORT\_SESSION](/sql-reference/functions/system_abort_session) |  |
| [SYSTEM$ABORT\_TRANSACTION](/sql-reference/functions/system_abort_transaction) |  |
| [SYSTEM$ACTIVATE\_CMK\_INFO](/sql-reference/functions/system_activate_cmk_info) |  |
| [SYSTEM$ACTIVATE\_CMK\_INFO\_POSTGRES](/sql-reference/functions/system_activate_cmk_info_postgres) |  |
| [SYSTEM$ADD\_EVENT (for Snowflake Scripting)](/sql-reference/functions/system_add_event) |  |
| [SYSTEM$ADD\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_add_privatelink_endpoint_hostname) |  |
| [SYSTEM$ADD\_REFERENCE](/sql-reference/functions/system_add_reference) |  |
| [SYSTEM$AUTHORIZE\_PRIVATELINK](/sql-reference/functions/system_authorize_privatelink) |  |
| [SYSTEM$AUTHORIZE\_STAGE\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_authorize_stage_privatelink_access) |  |
| [SYSTEM$AUTHORIZE\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_authorize_snowflake_managed_storage_volume_privatelink_access) |  |
| [SYSTEM$BEGIN\_DEBUG\_APPLICATION](/sql-reference/functions/system_begin_debug_application) |  |
| [SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS](/sql-reference/functions/system_block_internal_stages_public_access) |  |
| [SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS\_WITH\_EXCEPTION](/sql-reference/functions/system_block_internal_stages_public_access_with_exception) |  |
| [SYSTEM$BLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS](/sql-reference/functions/system_block_snowflake_managed_storage_volume_public_access) |  |
| [SYSTEM$BLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS\_WITH\_EXCEPTION](/sql-reference/functions/system_block_snowflake_managed_storage_volume_public_access_with_exception) |  |
| [SYSTEM$CANCEL\_ALL\_QUERIES](/sql-reference/functions/system_cancel_all_queries) |  |
| [SYSTEM$CANCEL\_QUERY](/sql-reference/functions/system_cancel_query) |  |
| [SYSTEM$CLEANUP\_DATABASE\_ROLE\_GRANTS](/sql-reference/functions/system_cleanup_database_role_grants) |  |
| [SYSTEM$COMMIT\_MOVE\_ORGANIZATION\_ACCOUNT](/sql-reference/functions/system_commit_move_organization_account) |  |
| [SYSTEM$CONVERT\_PIPES\_SQS\_TO\_SNS](/sql-reference/functions/system_convert_pipes_sqs_to_sns) |  |
| [SYSTEM$CREATE\_BILLING\_EVENT](/sql-reference/functions/system_create_billing_event) |  |
| [SYSTEM$CREATE\_BILLING\_EVENTS](/sql-reference/functions/system_create_billing_events) |  |
| [SYSTEM$CREATE\_EVALUATION\_DATASET](/sql-reference/functions/system_create_evaluation_dataset) |  |
| [SYSTEM$DEACTIVATE\_CMK\_INFO](/sql-reference/functions/system_deactivate_cmk_info) |  |
| [SYSTEM$DEMIGRATE\_DBT\_PROJECT](/sql-reference/functions/system_demigrate_dbt_project) |  |
| [SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) |  |
| [SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT\_TSS](/sql-reference/functions/system_deprovision_privatelink_endpoint_tss) |  |
| [SYSTEM$DEREGISTER\_CMK\_INFO](/sql-reference/functions/system_deregister_cmk_info) |  |
| [SYSTEM$DEREGISTER\_CMK\_INFO\_POSTGRES](/sql-reference/functions/system_deregister_cmk_info_postgres) |  |
| [SYSTEM$DISABLE\_BEHAVIOR\_CHANGE\_BUNDLE](/sql-reference/functions/system_disable_behavior_change_bundle) |  |
| [SYSTEM$DISABLE\_DATABASE\_REPLICATION](/sql-reference/functions/system_disable_database_replication) |  |
| [SYSTEM$DISABLE\_FEATURE\_GROUPS](/sql-reference/functions/system_disable_feature_groups) |  |
| [SYSTEM$DISABLE\_FEATURE\_GROUPS\_PREVIEW](/sql-reference/functions/system_disable_feature_groups_preview) |  |
| [SYSTEM$DISABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_disable_global_data_sharing_for_account) |  |
| [SYSTEM$DISABLE\_PREVIEW\_ACCESS](/sql-reference/functions/system_disable_preview_access) |  |
| [SYSTEM$DISABLE\_PRIVATELINK\_ACCESS\_ONLY](/sql-reference/functions/system_disable_privatelink_access_only) |  |
| [SYSTEM$ENABLE\_BEHAVIOR\_CHANGE\_BUNDLE](/sql-reference/functions/system_enable_behavior_change_bundle) |  |
| [SYSTEM$ENABLE\_FEATURE\_GROUPS](/sql-reference/functions/system_enable_feature_groups) |  |
| [SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_enable_global_data_sharing_for_account) |  |
| [SYSTEM$ENABLE\_PREVIEW\_ACCESS](/sql-reference/functions/system_enable_preview_access) |  |
| [SYSTEM$END\_DEBUG\_APPLICATION](/sql-reference/functions/system_end_debug_application) |  |
| [SYSTEM$ENFORCE\_PRIVATELINK\_ACCESS\_ONLY](/sql-reference/functions/system_enforce_privatelink_access_only) |  |
| [SYSTEM$FINISH\_OAUTH\_FLOW](/sql-reference/functions/system_finish_oauth_flow) |  |
| [SYSTEM$GLOBAL\_ACCOUNT\_SET\_PARAMETER](/sql-reference/functions/system_global_account_set_parameter) |  |
| [SYSTEM$INITIATE\_MOVE\_ORGANIZATION\_ACCOUNT](/sql-reference/functions/system_initiate_move_organization_account) |  |
| [SYSTEM$ISSUE\_PER\_ACCOUNT\_APP\_SERVICE\_CERTIFICATE](/sql-reference/functions/system_issue_per_account_app_service_certificate) |  |
| [SYSTEM$ISSUE\_PER\_ACCOUNT\_CERTIFICATES](/sql-reference/functions/system_issue_per_account_certificates) |  |
| [SYSTEM$ISSUE\_WORKLOAD\_IDENTITY\_FEDERATION\_TOKEN](/sql-reference/functions/system_issue_workload_identity_federation_token) |  |
| [SYSTEM$LINK\_ACCOUNT\_OBJECTS\_BY\_NAME](/sql-reference/functions/system_link_account_objects_by_name) |  |
| [SYSTEM$LINK\_ORGANIZATION\_USER](/sql-reference/functions/system_link_organization_user) |  |
| [SYSTEM$LINK\_ORGANIZATION\_USER\_GROUP](/sql-reference/functions/system_link_organization_user_group) |  |
| [SYSTEM$MIGRATE\_DBT\_PROJECT](/sql-reference/functions/system_migrate_dbt_project) |  |
| [SYSTEM$MIGRATE\_SAML\_IDP\_REGISTRATION](/sql-reference/functions/system_migrate_saml_idp_registration) |  |
| [SYSTEM$OPT\_IN\_INTERNAL\_STAGE\_NETWORK\_LOGS](/sql-reference/functions/system_opt_in_internal_stage_network_logs) |  |
| [SYSTEM$OPT\_OUT\_INTERNAL\_STAGE\_NETWORK\_LOGS](/sql-reference/functions/system_opt_out_internal_stage_network_logs) |  |
| [SYSTEM$OPT\_OUT\_MALICIOUS\_IP\_PROTECTION\_BY\_CATEGORY](/sql-reference/functions/system_opt_out_malicious_ip_protection_by_category) |  |
| [SYSTEM$PIPE\_FORCE\_RESUME](/sql-reference/functions/system_pipe_force_resume) |  |
| [SYSTEM$PIPE\_REBINDING\_WITH\_NOTIFICATION\_CHANNEL](/sql-reference/functions/system_pipe_rebinding_with_notification_channel) |  |
| [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) |  |
| [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT\_TSS](/sql-reference/functions/system_provision_privatelink_endpoint_tss) |  |
| [SYSTEM$REGISTER\_CMK\_INFO](/sql-reference/functions/system_register_cmk_info) |  |
| [SYSTEM$REGISTER\_CMK\_INFO\_POSTGRES](/sql-reference/functions/system_register_cmk_info_postgres) |  |
| [SYSTEM$REGISTER\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_register_privatelink_endpoint) |  |
| [SYSTEM$REMOVE\_ALL\_REFERENCES](/sql-reference/functions/system_remove_all_references) |  |
| [SYSTEM$REMOVE\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_remove_privatelink_endpoint_hostname) |  |
| [SYSTEM$REMOVE\_REFERENCE](/sql-reference/functions/system_remove_reference) |  |
| [SYSTEM$RESTORE\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_restore_privatelink_endpoint) |  |
| [SYSTEM$RESTORE\_PRIVATELINK\_ENDPOINT\_TSS](/sql-reference/functions/system_restore_privatelink_endpoint_tss) |  |
| [SYSTEM$REVOKE\_PRIVATELINK](/sql-reference/functions/system_revoke_privatelink) |  |
| [SYSTEM$REVOKE\_STAGE\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_revoke_stage_privatelink_access) |  |
| [SYSTEM$REVOKE\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_revoke_snowflake_managed_storage_volume_privatelink_access) |  |
| [SYSTEM$SCHEDULE\_ASYNC\_REPLICATION\_GROUP\_REFRESH](/sql-reference/functions/system_schedule_async_replication_group_refresh) |  |
| [SYSTEM$SEND\_NOTIFICATIONS\_TO\_CATALOG](/sql-reference/functions/system_send_notifications_to_catalog) |  |
| [SYSTEM$SET\_APPLICATION\_RESTRICTED\_FEATURE\_ACCESS](/sql-reference/functions/system_set_application_restricted_feature_access) |  |
| [SYSTEM$SET\_CATALOG\_INTEGRATION](/sql-reference/functions/system_set_catalog_integration) |  |
| [SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_set_default_columns_override_for_show_command) |  |
| [SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_set_default_columns_override_for_system_object) |  |
| [SYSTEM$SET\_EVENT\_SHARING\_ACCOUNT\_FOR\_REGION](/sql-reference/functions/system_set_event_sharing_account_for_region) |  |
| [SYSTEM$SET\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_set_privatelink_endpoint_hostname) |  |
| [SYSTEM$SET\_REFERENCE](/sql-reference/functions/system_set_reference) |  |
| [SYSTEM$SET\_ROW\_TIMESTAMP\_ON\_ALL\_SUPPORTED\_TABLES](/sql-reference/functions/system_set_row_timestamp_on_all_supported_tables) |  |
| [SYSTEM$SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS\_STATUS](/sql-reference/functions/system_snowflake_managed_storage_volume_public_access_status) |  |
| [SYSTEM$SNOWPIPE\_STREAMING\_UPDATE\_CHANNEL\_OFFSET\_TOKEN](/sql-reference/functions/system_snowpipe_streaming_update_channel_offset_token) |  |
| [SYSTEM$START\_OAUTH\_FLOW](/sql-reference/functions/system_start_oauth_flow) |  |
| [SYSTEM$START\_USER\_EMAIL\_VERIFICATION](/sql-reference/functions/system_start_user_email_verification) |  |
| [SYSTEM$TASK\_DEPENDENTS\_ENABLE](/sql-reference/functions/system_task_dependents_enable) |  |
| [SYSTEM$TRIGGER\_LISTING\_REFRESH](/sql-reference/functions/system_trigger_listing_refresh) |  |
| [SYSTEM$UNBLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS](/sql-reference/functions/system_unblock_internal_stages_public_access) |  |
| [SYSTEM$UNBLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS](/sql-reference/functions/system_unblock_snowflake_managed_storage_volume_public_access) |  |
| [SYSTEM$UNLINK\_ORGANIZATION\_USER](/sql-reference/functions/system_unlink_organization_user) |  |
| [SYSTEM$UNLINK\_ORGANIZATION\_USER\_GROUP](/sql-reference/functions/system_unlink_organization_user_group) |  |
| [SYSTEM$UNREGISTER\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_unregister_privatelink_endpoint) |  |
| [SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_unset_default_columns_override_for_show_command) |  |
| [SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_unset_default_columns_override_for_system_object) |  |
| [SYSTEM$UNSET\_EVENT\_SHARING\_ACCOUNT\_FOR\_REGION](/sql-reference/functions/system_unset_event_sharing_account_for_region) |  |
| [SYSTEM$UNVERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_unverify_dns_domain) |  |
| [SYSTEM$USER\_TASK\_CANCEL\_ONGOING\_EXECUTIONS](/sql-reference/functions/system_user_task_cancel_ongoing_executions) |  |
| [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain) |  |
| [SYSTEM$WAIT](/sql-reference/functions/system_wait) |  |
| **Information** |  |
| [EXTRACT\_SEMANTIC\_CATEGORIES](/sql-reference/functions/extract_semantic_categories) |  |
| [GET\_ANACONDA\_PACKAGES\_REPODATA](/sql-reference/functions/get_anaconda_packages_repodata) |  |
| [SHOW\_PYTHON\_PACKAGES\_DEPENDENCIES](/sql-reference/functions/show_python_packages_dependencies) |  |
| [SYSTEM$ALLOWLIST](/sql-reference/functions/system_allowlist) |  |
| [SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink) |  |
| [SYSTEM$APP\_COMPATIBILITY\_CHECK](/sql-reference/functions/system_app_compatibility_check) |  |
| [SYSTEM$APPLICATION\_GET\_LOG\_LEVEL](/sql-reference/functions/system_application_get_log_level) |  |
| [SYSTEM$APPLICATION\_GET\_METRIC\_LEVEL](/sql-reference/functions/system_application_get_metric_level) |  |
| [SYSTEM$APPLICATION\_GET\_TRACE\_LEVEL](/sql-reference/functions/system_application_get_trace_level) |  |
| [SYSTEM$AUTO\_REFRESH\_STATUS](/sql-reference/functions/system_auto_refresh_status) |  |
| [SYSTEM$BEHAVIOR\_CHANGE\_BUNDLE\_STATUS](/sql-reference/functions/system_behavior_change_bundle_status) |  |
| [SYSTEM$CATALOG\_LINK\_STATUS](/sql-reference/functions/system_catalog_link_status) |  |
| [SYSTEM$CKE\_HASH\_FUNCTION](/sql-reference/functions/system_cke_hash_function) |  |
| [SYSTEM$CLIENT\_VERSION\_INFO](/sql-reference/functions/system_client_version_info) |  |
| [SYSTEM$CLIENT\_VULNERABILITY\_INFO](/sql-reference/functions/system_client_vulnerability_info) |  |
| [SYSTEM$CLUSTERING\_DEPTH](/sql-reference/functions/system_clustering_depth) |  |
| [SYSTEM$CLUSTERING\_INFORMATION](/sql-reference/functions/system_clustering_information) |  |
| [SYSTEM$CLUSTERING\_RATIO](/sql-reference/functions/system_clustering_ratio) | Deprecated; use the other clustering functions instead. |
| [SYSTEM$CURRENT\_USER\_TASK\_NAME](/sql-reference/functions/system_current_user_task_name) |  |
| [SYSTEM$DATA\_METRIC\_SCAN](/sql-reference/functions/system_data_metric_scan) |  |
| [SYSTEM$DATABASE\_REFRESH\_HISTORY](/sql-reference/functions/system_database_refresh_history) | Deprecated; use [DATABASE\_REFRESH\_HISTORY](/sql-reference/functions/database_refresh_history) instead. |
| [SYSTEM$DATABASE\_REFRESH\_PROGRESS, SYSTEM$DATABASE\_REFRESH\_PROGRESS\_BY\_JOB](/sql-reference/functions/system_database_refresh_progress) | Deprecated; use [DATABASE\_REFRESH\_PROGRESS , DATABASE\_REFRESH\_PROGRESS\_BY\_JOB](/sql-reference/functions/database_refresh_progress) instead. |
| [SYSTEM$DBT\_GET\_LAST\_FAILED\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_failed_run_target) |  |
| [SYSTEM$DBT\_GET\_LAST\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_run_target) |  |
| [SYSTEM$DBT\_GET\_LAST\_SUCCESSFUL\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_successful_run_target) |  |
| [SYSTEM$DECODE\_PAT](/sql-reference/functions/system_decode_pat) |  |
| [SYSTEM$DESC\_ICEBERG\_ACCESS\_IDENTITY](/sql-reference/functions/system_desc_iceberg_access_identity) |  |
| [SYSTEM$ENCODE\_CKE\_PRIMARY\_KEY](/sql-reference/functions/system_encode_cke_primary_key) |  |
| [SYSTEM$ESTIMATE\_AUTOMATIC\_CLUSTERING\_COSTS](/sql-reference/functions/system_estimate_automatic_clustering_costs) |  |
| [SYSTEM$ESTIMATE\_SEARCH\_OPTIMIZATION\_COSTS](/sql-reference/functions/system_estimate_search_optimization_costs) |  |
| [SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS](/sql-reference/functions/system_evaluate_data_quality_expectations) |  |
| [SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS\_PERSIST\_RESULT](/sql-reference/functions/system_evaluate_data_quality_expectations_persist_result) |  |
| [SYSTEM$EXECUTE\_CATALOG\_OPERATION](/sql-reference/functions/system_execute_catalog_operation) |  |
| [EXPLAIN\_PRIVILEGES](/sql-reference/functions/explain_privileges) |  |
| [SYSTEM$EXPORT\_TDS\_FROM\_SEMANTIC\_VIEW](/sql-reference/functions/system_export_tds_from_semantic_view) |  |
| [SYSTEM$EXTERNAL\_TABLE\_PIPE\_STATUS](/sql-reference/functions/system_external_table_pipe_status) |  |
| [SYSTEM$FETCH\_EXTERNAL\_SECRET\_FROM\_INTEGRATION](/sql-reference/functions/system_fetch_external_secret_from_integration) |  |
| [SYSTEM$GENERATE\_SAML\_CSR](/sql-reference/functions/system_generate_saml_csr) |  |
| [SYSTEM$GENERATE\_SCIM\_ACCESS\_TOKEN](/sql-reference/functions/system_generate_scim_access_token) |  |
| [SYSTEM$GET\_ALERT\_TEMPLATE](/sql-reference/functions/system_get_alert_template) |  |
| [SYSTEM$GET\_ALL\_DEFAULT\_COLUMNS\_OVERRIDES](/sql-reference/functions/system_get_all_default_columns_overrides) |  |
| [SYSTEM$GET\_ALL\_REFERENCES](/sql-reference/functions/system_get_all_references) |  |
| [SYSTEM$GET\_AWS\_SNS\_IAM\_POLICY](/sql-reference/functions/system_get_aws_sns_iam_policy) |  |
| [SYSTEM$GET\_CATALOG\_LINKED\_DATABASE\_CONFIG](/sql-reference/functions/system_get_catalog_linked_database_config) |  |
| [SYSTEM$GET\_CLASSIFICATION\_RESULT](/sql-reference/functions/system_get_classification_result) |  |
| [SYSTEM$GET\_CMK\_AKV\_CONSENT\_URL](/sql-reference/functions/system_get_cmk_akv_consent_url) |  |
| [SYSTEM$GET\_CMK\_CONFIG](/sql-reference/functions/system_get_cmk_config) |  |
| [SYSTEM$GET\_CMK\_CONFIG\_POSTGRES](/sql-reference/functions/system_get_cmk_config_postgres) |  |
| [SYSTEM$GET\_CMK\_INFO](/sql-reference/functions/system_get_cmk_info) |  |
| [SYSTEM$GET\_CMK\_INFO\_POSTGRES](/sql-reference/functions/system_get_cmk_info_postgres) |  |
| [SYSTEM$GET\_CMK\_KMS\_KEY\_POLICY](/sql-reference/functions/system_get_cmk_kms_key_policy) |  |
| [SYSTEM$GET\_COMPUTE\_POOL\_PENDING\_MAINTENANCE](/sql-reference/functions/system_get_compute_pool_pending_maintenance) |  |
| [SYSTEM$GET\_DBT\_LOG](/sql-reference/functions/system_get_dbt_log) |  |
| [SYSTEM$GET\_DEBUG\_STATUS](/sql-reference/functions/system_get_debug_status) |  |
| [SYSTEM$GET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_get_default_columns_override_for_show_command) |  |
| [SYSTEM$GET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_get_default_columns_override_for_system_object) |  |
| [SYSTEM$GET\_DIRECTORY\_TABLE\_STATUS](/sql-reference/functions/system_get_directory_table_status) |  |
| [SYSTEM$GET\_GCP\_KMS\_CMK\_GRANT\_ACCESS\_CMD](/sql-reference/functions/system_get_gcp_kms_cmk_grant_access_cmd) |  |
| [SYSTEM$GET\_HASH\_FOR\_APPLICATION](/sql-reference/functions/system_get_hash_for_application) |  |
| [SYSTEM$GET\_ICEBERG\_TABLE\_INFORMATION](/sql-reference/functions/system_get_iceberg_table_information) |  |
| [SYSTEM$GET\_INSTANCE\_FAMILY\_PLACEMENT\_GROUPS](/sql-reference/functions/system_get_instance_family_placement_groups) |  |
| [SYSTEM$GET\_LOGIN\_FAILURE\_DETAILS](/sql-reference/functions/system_get_login_failure_details) |  |
| [SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](/sql-reference/functions/system_get_predecessor_return_value) |  |
| [SYSTEM$GET\_PREVIEW\_ACCESS\_STATUS](/sql-reference/functions/system_get_preview_access_status) |  |
| [SYSTEM$GET\_PRIVATELINK](/sql-reference/functions/system_get_privatelink) |  |
| [SYSTEM$GET\_PRIVATELINK\_AUTHORIZED\_ENDPOINTS](/sql-reference/functions/system_get_privatelink_authorized_endpoints) |  |
| [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) |  |
| [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) |  |
| [SYSTEM$GET\_PRIVATELINK\_ENDPOINT\_REGISTRATIONS](/sql-reference/functions/system_get_privatelink_endpoint_registrations) |  |
| [SYSTEM$GET\_PURCHASE\_ATTRIBUTES](/sql-reference/functions/system_get_purchase_attributes) |  |
| [SYSTEM$GET\_REFERENCED\_OBJECT\_ID\_HASH](/sql-reference/functions/system_get_referenced_object_id_hash) |  |
| [SYSTEM$GET\_SECURITY\_INTEGRATIONS\_FOR\_API\_PROVIDER](/sql-reference/functions/system_get_security_integrations_for_api_provider) |  |
| [SYSTEM$GET\_SERVICE\_CALLER\_TOKEN\_EXPIRY](/sql-reference/functions/system_get_service_caller_token_expiry) | Returns the expiration timestamp of a caller’s rights login token. |
| [SYSTEM$GET\_SERVICE\_DNS\_DOMAIN](/sql-reference/functions/system_get_service_dns_domain) |  |
| [SYSTEM$GET\_SERVICE\_LOGS](/sql-reference/functions/system_get_service_logs) |  |
| [SYSTEM$GET\_SERVICE\_STATUS — Deprecated](/sql-reference/functions/system_get_service_status) | Deprecated; use the [SHOW SERVICE CONTAINERS IN SERVICE](/sql-reference/sql/show-service-containers-in-service) command instead. |
| [SYSTEM$GET\_SNOWFLAKE\_EGRESS\_IP\_RANGES](/sql-reference/functions/system_get_snowflake_egress_ip_ranges) |  |
| [SYSTEM$GET\_SNOWFLAKE\_PLATFORM\_INFO](/sql-reference/functions/system_get_snowflake_platform_info) |  |
| [SYSTEM$GET\_STAGE\_PRIVATELINK\_AUTHORIZED\_ENDPOINTS](/sql-reference/functions/system_get_stage_privatelink_authorized_endpoints) |  |
| [SYSTEM$GET\_TABLE\_ARCHIVE\_METADATA](/sql-reference/functions/system_get_table_archive_metadata) |  |
| [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag) | Returns an error if a [multi-value tag](/user-guide/object-tagging/multi-value-tags) has more than one value assigned. Use [SYSTEM$TAG\_VALUE\_CONTAINS](/sql-reference/functions/system_tag_value_contains) instead. |
| [SYSTEM$GET\_TAG\_ALLOWED\_VALUES](/sql-reference/functions/system_get_tag_allowed_values) |  |
| [SYSTEM$GET\_TAG\_ON\_CURRENT\_COLUMN](/sql-reference/functions/system_get_tag_on_current_column) |  |
| [SYSTEM$GET\_TAG\_ON\_CURRENT\_TABLE](/sql-reference/functions/system_get_tag_on_current_table) |  |
| [SYSTEM$GET\_TASK\_GRAPH\_CONFIG](/sql-reference/functions/system_get_task_graph_config) |  |
| [SYSTEM$HOLD\_PRIVILEGE\_ON\_ACCOUNT](/sql-reference/functions/system_hold_privilege_on_account) |  |
| [SYSTEM$INTERNAL\_STAGES\_PUBLIC\_ACCESS\_STATUS](/sql-reference/functions/system_internal_stages_public_access_status) |  |
| [SYSTEM$IS\_APPLICATION\_ALL\_MANDATORY\_TELEMETRY\_EVENT\_DEFINITIONS\_ENABLED](/sql-reference/functions/system_is_application_all_mandatory_telemetry_event_definitions_enabled) |  |
| [SYSTEM$IS\_APPLICATION\_AUTHORIZED\_FOR\_TELEMETRY\_EVENT\_SHARING](/sql-reference/functions/system_is_application_authorized_for_telemetry_event_sharing) |  |
| [SYSTEM$IS\_APPLICATION\_INSTALLED\_FROM\_SAME\_ACCOUNT](/sql-reference/functions/system_is_application_installed_from_same_account) |  |
| [SYSTEM$IS\_APPLICATION\_SHARING\_EVENTS\_WITH\_PROVIDER](/sql-reference/functions/system_is_application_sharing_events_with_provider) |  |
| [SYSTEM$IS\_GLOBAL\_DATA\_SHARING\_ENABLED\_FOR\_ACCOUNT](/sql-reference/functions/system_is_global_data_sharing_enabled_for_account) |  |
| [SYSTEM$IS\_LISTING\_PURCHASED](/sql-reference/functions/system_is_listing_purchased) |  |
| [SYSTEM$IS\_LISTING\_TRIAL](/sql-reference/functions/system_is_listing_trial) |  |
| [SYSTEM$LAST\_CHANGE\_COMMIT\_TIME](/sql-reference/functions/system_last_change_commit_time) |  |
| [SYSTEM$LIST\_ALERT\_TEMPLATES](/sql-reference/functions/system_list_alert_templates) |  |
| [SYSTEM$LIST\_APPLICATION\_RESTRICTED\_FEATURES](/sql-reference/functions/system_list_application_restricted_features) |  |
| [SYSTEM$LIST\_EXTERNAL\_SECRETS](/sql-reference/functions/system_list_external_secrets) |  |
| [SYSTEM$LIST\_ICEBERG\_TABLES\_FROM\_CATALOG](/sql-reference/functions/system_list_iceberg_tables_from_catalog) |  |
| [SYSTEM$LIST\_NAMESPACES\_FROM\_CATALOG](/sql-reference/functions/system_list_namespaces_from_catalog) |  |
| [SYSTEM$LOCATE\_DBT\_ARCHIVE](/sql-reference/functions/system_locate_dbt_archive) |  |
| [SYSTEM$LOCATE\_DBT\_ARTIFACTS](/sql-reference/functions/system_locate_dbt_artifacts) |  |
| [SYSTEM$LOG, SYSTEM$LOG\_<level> (for Snowflake Scripting)](/sql-reference/functions/system_log) |  |
| [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) |  |
| [SYSTEM$QUERY\_REFERENCE](/sql-reference/functions/system_query_reference) |  |
| [SYSTEM$READ\_YAML\_FROM\_SEMANTIC\_VIEW](/sql-reference/functions/system_read_yaml_from_semantic_view) |  |
| [SYSTEM$READ\_OSI\_YAML\_FROM\_SEMANTIC\_VIEW](/sql-reference/functions/system_read_osi_yaml_from_semantic_view) |  |
| [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) |  |
| [SYSTEM$REGISTRY\_LIST\_IMAGES](/sql-reference/functions/system_registry_list_images) | Deprecated; use the [SHOW IMAGES IN IMAGE REPOSITORY](/sql-reference/sql/show-images-in-image-repository) command instead. |
| [SYSTEM$REPORT\_HEALTH\_STATUS](/sql-reference/functions/system_report_health_status) |  |
| [SYSTEM$SET\_RETURN\_VALUE](/sql-reference/functions/system_set_return_value) |  |
| [SYSTEM$SET\_SPAN\_ATTRIBUTES (for Snowflake Scripting)](/sql-reference/functions/system_set_span_attributes) |  |
| [SYSTEM$SHOW\_ACTIVE\_BEHAVIOR\_CHANGE\_BUNDLES](/sql-reference/functions/system_show_active_behavior_change_bundles) |  |
| [SYSTEM$SHOW\_BUDGETS\_FOR\_RESOURCE](/sql-reference/functions/system_show_budgets_for_resource) |  |
| [SYSTEM$SHOW\_BUDGETS\_IN\_ACCOUNT](/sql-reference/functions/system_show_budgets_in_account) |  |
| [SYSTEM$SHOW\_EVENT\_SHARING\_ACCOUNTS](/sql-reference/functions/system_show_event_sharing_accounts) |  |
| [SYSTEM$SHOW\_MOVE\_ORGANIZATION\_ACCOUNT\_STATUS](/sql-reference/functions/system_show_move_organization_account_status) |  |
| [SYSTEM$SHOW\_OAUTH\_CLIENT\_SECRETS](/sql-reference/functions/system_show_oauth_client_secrets) |  |
| [SYSTEM$SHOW\_SENSITIVE\_DATA\_MONITORED\_ENTITIES](/sql-reference/functions/system_show_sensitive_data_monitored_entities) |  |
| [SYSTEM$STREAM\_BACKLOG](/sql-reference/functions/system_stream_backlog) | This function is a [table function](/sql-reference/functions-table). |
| [SYSTEM$STREAM\_GET\_TABLE\_TIMESTAMP](/sql-reference/functions/system_stream_get_table_timestamp) |  |
| [SYSTEM$STREAM\_HAS\_DATA](/sql-reference/functions/system_stream_has_data) |  |
| [SYSTEM$SUPPORTED\_DBT\_VERSIONS](/sql-reference/functions/system_supported_dbt_versions) |  |
| [SYSTEM$TAG\_VALUE\_CONTAINS](/sql-reference/functions/system_tag_value_contains) |  |
| [SYSTEM$TASK\_RUNTIME\_INFO](/sql-reference/functions/system_task_runtime_info) |  |
| [SYSTEM$TYPEOF](/sql-reference/functions/system_typeof) |  |
| [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](/sql-reference/functions/system_validate_storage_integration) |  |
| [SYSTEM$VERIFY\_CATALOG\_INTEGRATION](/sql-reference/functions/system_verify_catalog_integration) |  |
| [SYSTEM$VERIFY\_CMK\_INFO](/sql-reference/functions/system_verify_cmk_info) |  |
| [SYSTEM$VERIFY\_CMK\_INFO\_POSTGRES](/sql-reference/functions/system_verify_cmk_info_postgres) |  |
| [SYSTEM$VERIFY\_EXTERNAL\_OAUTH\_TOKEN](/sql-reference/functions/system_verify_ext_oauth_token) |  |
| [SYSTEM$VERIFY\_EXTERNAL\_SECRET\_INTEGRATION](/sql-reference/functions/system_verify_external_secret_integration) |  |
| [SYSTEM$VERIFY\_EXTERNAL\_VOLUME](/sql-reference/functions/system_verify_external_volume) |  |
| [SYSTEM$WHITELIST](/sql-reference/functions/system_whitelist) | Deprecated; use [SYSTEM$ALLOWLIST](/sql-reference/functions/system_allowlist) instead. |
| [SYSTEM$WAIT\_FOR\_SERVICES](/sql-reference/functions/system_wait_for_services) |  |
| [SYSTEM$WHITELIST\_PRIVATELINK](/sql-reference/functions/system_whitelist_privatelink) | Deprecated; use [SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink) instead. |
| **Query Information** |  |
| [EXPLAIN\_GRANTABLE\_PRIVILEGES](/sql-reference/functions/explain_grantable_privileges) |  |
| [EXPLAIN\_JSON](/sql-reference/functions/explain_json) |  |
| [GET\_QUERY\_OPERATOR\_STATS](/sql-reference/functions/get_query_operator_stats) |  |
| [GET\_PYTHON\_PROFILER\_OUTPUT (SNOWFLAKE.CORE)](/sql-reference/functions/get_python_profiler_output) |  |
| [SYSTEM$ESTIMATE\_QUERY\_ACCELERATION](/sql-reference/functions/system_estimate_query_acceleration) |  |
| [SYSTEM$EXPLAIN\_PLAN\_JSON](/sql-reference/functions/system_explain_plan_json) |  |
| [SYSTEM$EXPLAIN\_JSON\_TO\_TEXT](/sql-reference/functions/system_explain_json_to_text) |  |
| [SYSTEM$GET\_RESULTSET\_STATUS](/sql-reference/functions/system_get_resultset_status) |  |

Expand

Show lessSee more
