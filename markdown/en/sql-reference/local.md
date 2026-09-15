# LOCAL schema

Some Snowflake features use the LOCAL schema of the SNOWFLAKE database to store telemetry data for logging and results analysis. The tables, views, and functions available in the LOCAL schema depend on which features you use in an account. Visibility of available objects in the LOCAL schema is access-controlled.

For the full reference on `AI_OBSERVABILITY_EVENTS`, see [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

## LOCAL tables

All tables in the LOCAL schema use the [event table structure](/developer-guide/logging-tracing/event-table-columns).

The LOCAL schema provides the following tables:

| Table | Associated Snowflake feature | Notes |
| --- | --- | --- |
| [AI\_OBSERVABILITY\_EVENTS](/sql-reference/local/ai_observability_events) | [AI Observability](/user-guide/snowflake-cortex/ai-observability) | Raw event data for AI Observability. Query through `SNOWFLAKE.LOCAL` table functions scoped to each object; see [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events). Application roles on the table itself are for limited admin use only. |
| CORTEX\_ANALYST\_REQUESTS\_RAW | [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst) | Raw event data for Cortex Analyst. For information about querying this table, see [Querying logs with SQL](/user-guide/snowflake-cortex/cortex-analyst/admin-observability#label-cortex-analyst-querying-logs-with-sql). |
| DATA\_QUALITY\_MONITORING\_LOGS\_RAW | [Data Quality](/user-guide/data-quality-intro) | Raw event data for Data Quality log events emitted by DMFs that produce per-event detail in addition to their aggregate result. For the simplified projection, see the [DATA\_QUALITY\_MONITORING\_LOGS](/sql-reference/local/data_quality_monitoring_logs) view. |
| DATA\_QUALITY\_MONITORING\_RESULTS\_RAW | [Data Quality](/user-guide/data-quality-intro) | Raw event data for Data Quality. For information about querying this table, see [Query the DATA\_QUALITY\_MONITORING\_RESULTS\_RAW table](/user-guide/data-quality-results#label-data-quality-query-event-table). |

Expand

Show lessSee more

Note

Data stored in LOCAL tables incurs Snowflake storage charges. For information about storage costs, see [Understanding storage cost](/user-guide/cost-understanding-data-storage).

## LOCAL views

The LOCAL schema provides the following views:

| View | Associated Snowflake feature | Notes |
| --- | --- | --- |
| [CORTEX\_ANALYST\_REQUESTS\_V](/sql-reference/local/cortex_analyst_requests_v) | [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst) | For information about querying this view, see [Querying logs with SQL](/user-guide/snowflake-cortex/cortex-analyst/admin-observability#label-cortex-analyst-querying-logs-with-sql). |
| [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/data_quality_monitoring_results) | [Data Quality](/user-guide/data-quality-intro) | For information about querying this view, see [Query the DATA\_QUALITY\_MONITORING\_RESULTS view](/user-guide/data-quality-results#label-data-quality-query-dmf-view-results). |
| [DATA\_QUALITY\_MONITORING\_ANOMALY\_DETECTION\_STATUS](/sql-reference/local/data_quality_monitoring_anomaly_detection_status) | [Data quality anomaly detection](/user-guide/data-quality-anomaly) |  |
| [AUTOMATIC\_DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/automatic_data_quality_monitoring_results) | [Data quality anomaly detection](/user-guide/data-quality-anomaly) | Results of automatic data quality monitoring: one row per table, metric, and evaluation date, with the observed value, forecast, expected range, and anomaly verdict. |
| [DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS](/sql-reference/local/data_quality_monitoring_expectation_status) | [Data quality expectations](/user-guide/data-quality-expectations) |  |
| [DATA\_QUALITY\_MONITORING\_LOGS](/sql-reference/local/data_quality_monitoring_logs) | [Data Quality](/user-guide/data-quality-intro) | Simplified projection of `DATA_QUALITY_MONITORING_LOGS_RAW` with per-event log detail from DMFs that emit structured log events. |

Expand

Show lessSee more

## LOCAL functions

The LOCAL schema provides the following functions:

| Function | Associated Snowflake feature | Notes |
| --- | --- | --- |
| CORTEX\_ANALYST\_REQUESTS | [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst) | For information about how to call this function, see [Querying logs with SQL](/user-guide/snowflake-cortex/cortex-analyst/admin-observability#label-cortex-analyst-querying-logs-with-sql). |
| [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/functions/data_quality_monitoring_results) | [Data Quality](/user-guide/data-quality-intro) | For information about how to call this function, see [Call the DATA\_QUALITY\_MONITORING\_RESULTS function](/user-guide/data-quality-results#label-data-quality-query-dmf-table-function-results). |
| [GET\_AI\_EVALUATION\_DATA](/sql-reference/functions/get_ai_evaluation_data-snowflake-local) | [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations) |  |
| [GET\_AI\_OBSERVABILITY\_EVENTS](/sql-reference/functions/get_ai_observability_events-snowflake-local) | [AI Observability](/user-guide/snowflake-cortex/ai-observability), [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents-monitor), [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor) | Returns observability event rows for a Cortex Agent (`CORTEX AGENT`), External Agent (`EXTERNAL AGENT`), or Cortex Search service (`CORTEX SEARCH SERVICE`). For usage, see [GET\_AI\_OBSERVABILITY\_EVENTS (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_observability_events-snowflake-local), [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor), [Monitor Cortex Search requests](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor), and [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events). |
| [GET\_AI\_OBSERVABILITY\_LOGS](/sql-reference/functions/get_ai_observability_logs-snowflake-local) | [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations) |  |
| [GET\_AI\_RECORD\_TRACE](/sql-reference/functions/get_ai_record_trace-snowflake-local) | [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations) |  |

Expand

Show lessSee more
