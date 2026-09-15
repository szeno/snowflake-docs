# Stored procedures

Snowflake provides stored procedures to facilitate using certain Snowflake features. To find the stored procedures that are associated with a particular Snowflake Class, see [SQL class reference](/sql-reference-classes).

Use [CALL](/sql-reference/sql/call) to call a stored procedure. For example:

Copy code

```
CALL SYSTEM$CLASSIFY('hr.tables.empl_info', null);
```

Snowflake supports the following stored procedures, grouped by feature:

| Feature | Stored procedure |
| --- | --- |
| [Cortex Powered Object Descriptions](/user-guide/sql-cortex-descriptions) | - [AI\_GENERATE\_TABLE\_DESC](/sql-reference/stored-procedures/ai_generate_table_desc) |
| [Data classification](/user-guide/classify-intro) | - [ASSOCIATE\_SEMANTIC\_CATEGORY\_TAGS](/sql-reference/stored-procedures/associate_semantic_category_tags) - [SYSTEM$CLASSIFY](/sql-reference/stored-procedures/system_classify) - [SYSTEM$CLASSIFY\_SCHEMA](/sql-reference/stored-procedures/system_classify_schema) - [SYSTEM$CANCEL\_CLASSIFY\_SCHEMA](/sql-reference/stored-procedures/system_cancel_classify_schema) |
| [Data sharing and collaboration](/guides-overview-sharing) | - [SYSTEM$REQUEST\_LISTING\_AND\_WAIT](/sql-reference/stored-procedures/system_request_listing_and_wait) |
| [Default event table](/developer-guide/logging-tracing/event-table-setting-up) | - [ADD\_ROW\_ACCESS\_POLICY\_ON\_EVENTS\_VIEW](/sql-reference/stored-procedures/snowflake_telemetry_add_row_access_policy_on_events_view) - [DROP\_ROW\_ACCESS\_POLICY\_ON\_EVENTS\_VIEW](/sql-reference/stored-procedures/snowflake_telemetry_drop_row_access_policy_on_events_view) |
| [Differential privacy](/user-guide/diff-privacy/differential-privacy-overview) | - [RESET\_PRIVACY\_BUDGET](/sql-reference/stored-procedures/reset_privacy_budget) |
| [Network security](/user-guide/network-policy-advisor) | - [EVALUATE\_CANDIDATE\_NETWORK\_POLICY](/sql-reference/stored-procedures/evaluate_candidate_network_policy) - [RECOMMEND\_NETWORK\_POLICY](/sql-reference/stored-procedures/recommend_network_policy) |
| [Notifications](/user-guide/notifications/about-notifications) | - [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) - [SYSTEM$SEND\_EMAIL](/sql-reference/stored-procedures/system_send_email) |
| [Semantic views](/user-guide/views-semantic/overview) | - [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_yaml) |
| [Synthetic data](/user-guide/synthetic-data) | - [GENERATE\_SYNTHETIC\_DATA](/sql-reference/stored-procedures/generate_synthetic_data) |
| [Trust Center](/user-guide/trust-center/overview) | - [REGISTER\_EXTENSION](/sql-reference/stored-procedures/register_extension) - [DEREGISTER\_EXTENSION](/sql-reference/stored-procedures/deregister_extension) - [GET\_AUTO\_ENABLEMENT\_STATUS](/sql-reference/stored-procedures/get_auto_enablement_status) - [UPDATE\_AUTO\_ENABLEMENT\_STATUS](/sql-reference/stored-procedures/update_auto_enablement_status) |

Expand

Show lessSee more
