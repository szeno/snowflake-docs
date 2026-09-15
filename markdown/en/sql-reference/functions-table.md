# Table functions

A table function returns a set of rows for each input row. The returned set can contain zero, one, or more rows. Each row can
contain one or more columns.

Table functions are sometimes called “tabular functions”.

## What are table functions?

Table functions are typically used when a function returns multiple rows for each individual input.

Each time that a table function is called, it can return a different number of rows. For example, a function
`record_high_temperatures_for_date()`, which returns a list of record high temperatures for a specified date, might
return 0 rows on April 10, 1 row on June 10, and 40 rows on August 20.

### Simple examples of table functions

The following are appropriate as table functions:

- A function that accepts an account number and a date, and returns all charges billed to that account on that date.
  (More than one charge might have been billed on a particular date.)
- A function that accepts a user ID and returns the database roles assigned to that user.
  (A user might have multiple roles, including “sysadmin” and “useradmin”.)

### Functions in which each output row depends upon multiple input rows

Table functions can be grouped into two categories based on the number of input rows that affect each output row:

- 1-to-N
- M-to-N

The functions described earlier are 1-to-N table functions: each output row depends upon only one input row. For example, a
function `record_high_temperatures_for_date()` might produce multiple output rows (one for each city that hit a record on
that date). Each output row for a specific input date depends only on that date; each output row is independent of the rows for
every other date.

Snowflake also supports M-to-N table functions: each output row can depend upon multiple input rows. For example, if a function
generates a moving average of stock prices, that function uses stock prices from multiple input rows (multiple dates) to generate
each output row.

More generally, in an M-to-N function, a group of M input rows produces a group of N output rows. M can be one or more rows.
N can be zero, one, or more rows.

For example, in a 10-day moving average, M is 10. N is 1 because each group of 10 input rows produces one average price.

### Built-in table functions vs user-defined table functions

Snowflake provides hundreds of built-in functions, many of which are table functions. Built-in table functions are listed in
[System-Defined Table Functions](#label-list-of-system-defined-table-functions).

Users can also write their own functions, called user-defined functions or “UDFs”. Some UDFs are scalar; some are tabular.
User-defined table functions are called “UDTFs”. For information about UDFs (including UDTFs), see
[User-defined functions overview](/developer-guide/udf/udf-overview).

Built-in table functions and user-defined table functions generally follow the same rules; for example, they are called the same way
from SQL statements.

## Using a table function

### Using a table function in the FROM clause

A table contains a set of rows. Similarly, a table function returns a set of rows. Both tables and table functions are used in
contexts that expect a set of rows. Specifically, table functions are used in the [FROM](/sql-reference/constructs/from) clause of a
SQL statement.

To help the SQL compiler recognize a table function as a source of rows, Snowflake requires that the table function call be
wrapped by the `TABLE()` keyword.

For example, the following statement calls a table function named `record_high_temperatures_for_date()`, which takes a DATE
value as an argument:

> Copy code
>
> ```
> SELECT city_name, temperature
>     FROM TABLE(record_high_temperatures_for_date('2021-06-27'::DATE))
>     ORDER BY city_name;
> ```

For more information about the syntax of `TABLE()`, see [Table literals](/sql-reference/literals-table).

Table functions, like functions in general, can accept zero, one, or multiple input arguments in each invocation. Each argument
must be a scalar expression.

For more details about the syntax of table function calls, see [Syntax](#label-table-function-syntax) (in this topic).

### Using a table as input to a table function

The argument to a table function can be a literal or an expression, such as a column of a table.
For example, the SELECT statement below passes values from a table as arguments to a table function:

Copy code

```
CREATE OR REPLACE table dates_of_interest (event_date DATE);
INSERT INTO dates_of_interest (event_date) VALUES
    ('2021-06-21'::DATE),
    ('2022-06-21'::DATE);

CREATE OR REPLACE FUNCTION record_high_temperatures_for_date(d DATE)
    RETURNS TABLE (event_date DATE, city VARCHAR, temperature NUMBER)
    as
    $$
    SELECT d, 'New York', 65.0
    UNION ALL
    SELECT d, 'Los Angeles', 69.0
    $$;
```

Copy code

```
SELECT
        doi.event_date as "Date", 
        record_temperatures.city,
        record_temperatures.temperature
    FROM dates_of_interest AS doi,
         TABLE(record_high_temperatures_for_date(doi.event_date)) AS record_temperatures
      ORDER BY doi.event_date, city;
+------------+-------------+-------------+
| Date       | CITY        | TEMPERATURE |
|------------+-------------+-------------|
| 2021-06-21 | Los Angeles |          69 |
| 2021-06-21 | New York    |          65 |
| 2022-06-21 | Los Angeles |          69 |
| 2022-06-21 | New York    |          65 |
+------------+-------------+-------------+
```

The arguments to a table function can come from other table-like sources, including views and other table functions.

## List of system-defined table functions

Snowflake provides the following system-defined (i.e. built-in) table functions:

| Sub-category | Function | Notes |
| --- | --- | --- |
| Data Loading | [INFER\_SCHEMA](/sql-reference/functions/infer_schema) | For more information, see [Load data into Snowflake](/guides-overview-loading-data). |
|  | [VALIDATE](/sql-reference/functions/validate) |  |
| Data Generation | [GENERATOR](/sql-reference/functions/generator) |  |
| Data Conversion | [SPLIT\_TO\_TABLE](/sql-reference/functions/split_to_table) |  |
|  | [STRTOK\_SPLIT\_TO\_TABLE](/sql-reference/functions/strtok_split_to_table) |  |
| Differential Privacy | [CUMULATIVE\_PRIVACY\_LOSSES](/sql-reference/functions/cumulative_privacy_losses) |  |
| Object Modeling | [GET\_OBJECT\_REFERENCES](/sql-reference/functions/get_object_references) |  |
| Parameterized Queries | [TO\_QUERY](/sql-reference/functions/to_query) |  |
| Semi-structured Queries | [FLATTEN](/sql-reference/functions/flatten) | For more information, see [Querying Semi-structured Data](/user-guide/querying-semistructured). |
| Query Results | [RESULT\_SCAN](/sql-reference/functions/result_scan) | Can be used to perform SQL operations on the output from another SQL operation (e.g. SHOW). |
| Query Profile | [GET\_QUERY\_OPERATOR\_STATS](/sql-reference/functions/get_query_operator_stats) |  |
| Historical & Usage Information |  | Includes:   - [Snowflake Information Schema](/sql-reference/info-schema) - [Account Usage](/sql-reference/account-usage) - [LOCAL schema](/sql-reference/local) |
| User Login | [LOGIN\_HISTORY , LOGIN\_HISTORY\_BY\_USER](/sql-reference/functions/login_history) |  |
| Queries | [QUERY\_HISTORY , QUERY\_HISTORY\_BY\_\*](/sql-reference/functions/query_history) |  |
|  | [QUERY\_ACCELERATION\_HISTORY](/sql-reference/functions/query_acceleration_history) | TO BE DEPRECATED - Refer to [QUERY\_ACCELERATION\_HISTORY view](/sql-reference/account-usage/query_acceleration_history). For more information, see [Using the Query Acceleration Service (QAS)](/user-guide/query-acceleration-service). |
| Warehouse & Storage Usage | [DATABASE\_STORAGE\_USAGE\_HISTORY](/sql-reference/functions/database_storage_usage_history) | TO BE DEPRECATED - Refer to [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/database_storage_usage_history). |
|  | [WAREHOUSE\_LOAD\_HISTORY](/sql-reference/functions/warehouse_load_history) |  |
|  | [WAREHOUSE\_METERING\_HISTORY](/sql-reference/functions/warehouse_metering_history) | TO BE DEPRECATED - Refer to [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history). |
|  | [STAGE\_STORAGE\_USAGE\_HISTORY](/sql-reference/functions/stage_storage_usage_history) | TO BE DEPRECATED - Refer to [STAGE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/stage_storage_usage_history). |
|  | [ESTIMATE\_HYBRID\_TABLE\_STORAGE\_USAGE](/sql-reference/functions/estimate_hybrid_table_storage_usage) | Returns a near-real-time estimate of the total storage used by a hybrid table. |
| Storage Lifecycle Policies | [STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/functions/storage_lifecycle_policy_history) | Information Schema table function. For more information, see [Storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies). |
| Column-level & Row-level Security | [POLICY\_REFERENCES](/sql-reference/functions/policy_references) |  |
| Object Tagging | [TAG\_REFERENCES](/sql-reference/functions/tag_references) | Information Schema table function. |
|  | [TAG\_REFERENCES\_ALL\_COLUMNS](/sql-reference/functions/tag_references_all_columns) | Information Schema table function. |
|  | [TAG\_REFERENCES\_WITH\_LINEAGE](/sql-reference/functions/tag_references_with_lineage) | Account Usage table function. |
| Account Replication | [REPLICATION\_GROUP\_DANGLING\_REFERENCES](/sql-reference/functions/replication_group_dangling_references) | For more information, see [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro) |
|  | [REPLICATION\_GROUP\_REFRESH\_HISTORY, REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL](/sql-reference/functions/replication_group_refresh_history) |  |
|  | [REPLICATION\_GROUP\_REFRESH\_PROGRESS, REPLICATION\_GROUP\_REFRESH\_PROGRESS\_BY\_JOB, REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL](/sql-reference/functions/replication_group_refresh_progress) |  |
|  | [REPLICATION\_GROUP\_USAGE\_HISTORY](/sql-reference/functions/replication_group_usage_history) | TO BE DEPRECATED - Refer to [REPLICATION\_GROUP\_USAGE\_HISTORY view](/sql-reference/account-usage/replication_group_usage_history). |
| Alerts | [ALERT\_HISTORY](/sql-reference/functions/alert_history) | For more information, see [Setting up alerts based on data in Snowflake](/user-guide/alerts). |
|  | [SERVERLESS\_ALERT\_HISTORY](/sql-reference/functions/serverless_alert_history) | TO BE DEPRECATED - Refer to [SERVERLESS\_ALERT\_HISTORY view](/sql-reference/account-usage/serverless_alert_history). |
| Bind variables | [BIND\_VALUES](/sql-reference/functions/bind_values) | For more information, see [Retrieve bind variable values](/sql-reference/bind-variables#label-bind-variables-retrieving-values). |
| Database Replication | [DATABASE\_REFRESH\_HISTORY](/sql-reference/functions/database_refresh_history) | For more information, see [Replicating databases across multiple accounts](/user-guide/db-replication-config). |
|  | [DATABASE\_REFRESH\_PROGRESS , DATABASE\_REFRESH\_PROGRESS\_BY\_JOB](/sql-reference/functions/database_refresh_progress) |  |
|  | [DATABASE\_REPLICATION\_USAGE\_HISTORY](/sql-reference/functions/database_replication_usage_history) | TO BE DEPRECATED - Refer to [DATABASE\_REPLICATION\_USAGE\_HISTORY view](/sql-reference/account-usage/database_replication_usage_history). |
| Data Loading & Transfer | [COPY\_HISTORY](/sql-reference/functions/copy_history) |  |
|  | [DATA\_TRANSFER\_HISTORY](/sql-reference/functions/data_transfer_history) | TO BE DEPRECATED - Refer to [DATA\_TRANSFER\_HISTORY view](/sql-reference/account-usage/data_transfer_history). |
|  | [PIPE\_USAGE\_HISTORY](/sql-reference/functions/pipe_usage_history) | TO BE DEPRECATED - Refer to [PIPE\_USAGE\_HISTORY view](/sql-reference/account-usage/pipe_usage_history). |
|  | [STAGE\_DIRECTORY\_FILE\_REGISTRATION\_HISTORY](/sql-reference/functions/stage_directory_file_registration_history) |  |
|  | [VALIDATE\_PIPE\_LOAD](/sql-reference/functions/validate_pipe_load) |  |
| Data Clustering (within Tables) | [AUTOMATIC\_CLUSTERING\_HISTORY](/sql-reference/functions/automatic_clustering_history) | TO BE DEPRECATED - Refer to [AUTOMATIC\_CLUSTERING\_HISTORY view](/sql-reference/account-usage/automatic_clustering_history). For more information, see [Automatic Clustering](/user-guide/tables-auto-reclustering). |
| dbt Projects on Snowflake | [DBT\_PROJECT\_EXECUTION\_HISTORY](/sql-reference/functions/dbt_project_execution_history) | For more information, see [dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake). |
| Dynamic Tables | [DYNAMIC\_TABLES](/sql-reference/functions/dynamic_tables) | For more information, see [Create a dynamic table](/user-guide/dynamic-tables/create). |
|  | [DYNAMIC\_TABLE\_GRAPH\_HISTORY](/sql-reference/functions/dynamic_table_graph_history) |  |
|  | [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) |  |
| External Functions | [EXTERNAL\_FUNCTIONS\_HISTORY](/sql-reference/functions/external_functions_history) | For more information, see [Writing external functions](/sql-reference/external-functions). |
| External Tables | [AUTO\_REFRESH\_REGISTRATION\_HISTORY](/sql-reference/functions/auto_refresh_registration_history) | TO BE DEPRECATED - Refer to [CATALOG\_LINKED\_DATABASE\_USAGE\_HISTORY view](/sql-reference/account-usage/catalog_linked_database_usage_history). For more information, see [Introduction to external tables](/user-guide/tables-external-intro). |
|  | [EXTERNAL\_TABLE\_FILES](/sql-reference/functions/external_table_files) |  |
|  | [EXTERNAL\_TABLE\_FILE\_REGISTRATION\_HISTORY](/sql-reference/functions/external_table_registration_history) |  |
| Iceberg Tables | [ICEBERG\_TABLE\_FILES](/sql-reference/functions/iceberg_table_files) | Information Schema table function. |
|  | [ICEBERG\_TABLE\_SNAPSHOT\_REFRESH\_HISTORY](/sql-reference/functions/iceberg_table_snapshot_refresh_history) | Information Schema table function. |
| Listings | [AVAILABLE\_LISTINGS](/sql-reference/functions/available_listings) |  |
|  | [AVAILABLE\_LISTING\_REFRESH\_HISTORY](/sql-reference/functions/available_listing_refresh_history) |  |
|  | [LISTING\_REFRESH\_HISTORY](/sql-reference/functions/listing_refresh_history) |  |
| Materialized Views Maintenance | [MATERIALIZED\_VIEW\_REFRESH\_HISTORY](/sql-reference/functions/materialized_view_refresh_history) | TO BE DEPRECATED - Refer to [MATERIALIZED\_VIEW\_REFRESH\_HISTORY view](/sql-reference/account-usage/materialized_view_refresh_history). For more information, see [Working with Materialized Views](/user-guide/views-materialized). |
| Machine learning | [ONLINE\_FEATURE\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/online-feature-table-refresh-history) | For more information, see [Feature store commands](/sql-reference/commands-feature-store). |
| Notifications | [NOTIFICATION\_HISTORY](/sql-reference/functions/notification_history) | For more information, see [Using SYSTEM$SEND\_EMAIL to send email notifications](/user-guide/notifications/email-stored-procedures). |
| SCIM Maintenance | [REST\_EVENT\_HISTORY](/sql-reference/functions/rest_event_history) | For more information, see [Auditing SCIM API requests](/user-guide/scim-api-references#label-scim-auditing-rest-api-requests) |
| Search Optimization Maintenance | [SEARCH\_OPTIMIZATION\_HISTORY](/sql-reference/functions/search_optimization_history) | TO BE DEPRECATED - Refer to [SEARCH\_OPTIMIZATION\_HISTORY view](/sql-reference/account-usage/search_optimization_history). For more information, see [Search optimization service](/user-guide/search-optimization-service). |
| Streams | [SYSTEM$STREAM\_BACKLOG](/sql-reference/functions/system_stream_backlog) | For more information, see [Introduction to streams](/user-guide/streams-intro). |
| Tasks | [COMPLETE\_TASK\_GRAPHS](/sql-reference/functions/complete_task_graphs) | For more information, see [Introduction to tasks](/user-guide/tasks-intro). |
|  | [CURRENT\_TASK\_GRAPHS](/sql-reference/functions/current_task_graphs) |  |
|  | [SERVERLESS\_TASK\_HISTORY](/sql-reference/functions/serverless_task_history) | TO BE DEPRECATED - Refer to [SERVERLESS\_TASK\_HISTORY view](/sql-reference/account-usage/serverless_task_history). |
|  | [TASK\_DEPENDENTS](/sql-reference/functions/task_dependents) |  |
|  | [TASK\_HISTORY](/sql-reference/functions/task_history) |  |
| Network rules | [NETWORK\_RULE\_REFERENCES](/sql-reference/functions/network_rule_references) | Information Schema table function. For details, see [Network rules](/user-guide/network-rules). |
| Data Quality | [DATA\_METRIC\_FUNCTION\_EXPECTATIONS](/sql-reference/functions/data_metric_function_expectations) |  |
|  | [DATA\_METRIC\_FUNCTION\_REFERENCES](/sql-reference/functions/data_metric_function_references) |  |
|  | [DATA\_QUALITY\_MONITORING\_EXPECTATION\_STATUS](/sql-reference/functions/data_quality_monitoring_expectation_status) |  |
|  | [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/functions/data_quality_monitoring_results) |  |
|  | [SYSTEM$DATA\_METRIC\_SCAN](/sql-reference/functions/system_data_metric_scan) |  |
|  | [SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS](/sql-reference/functions/system_evaluate_data_quality_expectations) |  |
|  | [SYSTEM$EVALUATE\_DATA\_QUALITY\_EXPECTATIONS\_PERSIST\_RESULT](/sql-reference/functions/system_evaluate_data_quality_expectations_persist_result) |  |
| Data Lineage | [GET\_LINEAGE (SNOWFLAKE.CORE)](/sql-reference/functions/get_lineage-snowflake-core) | For more information, see [Data Lineage](/user-guide/ui-snowsight-lineage). |
| Cortex Search | [CORTEX\_SEARCH\_DATA\_SCAN](/sql-reference/functions/cortex_search_data_scan) | For more information, see [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview). |
|  | [CORTEX\_SEARCH\_REFRESH\_HISTORY](/sql-reference/functions/cortex_search_refresh_history) |  |
| Contacts | [GET\_CONTACTS](/sql-reference/functions/get_contacts) |  |
| Snowpark Container Services | [GET\_JOB\_HISTORY](/sql-reference/functions/get_job_history) | For more information, see [Snowpark Container Services: Monitoring Services](/developer-guide/snowpark-container-services/monitoring-services). |
|  | [<service\_name>!SPCS\_GET\_EVENTS](/sql-reference/functions/spcs_get_events) |  |
|  | [<service\_name>!SPCS\_GET\_LOGS](/sql-reference/functions/spcs_get_logs) |  |
|  | [<service\_name>!SPCS\_GET\_METRICS](/sql-reference/functions/spcs_get_metrics) |  |
| Snowflake Native Apps | [APPLICATION\_CALLBACK\_HISTORY](/sql-reference/functions/application_callback_history) | For more information, see [Callbacks](/developer-guide/native-apps/callbacks). |
|  | [APPLICATION\_SPECIFICATION\_STATUS\_HISTORY](/sql-reference/functions/application_specification_status_history) | For more information, see [Use app specifications to request controlled access](/developer-guide/native-apps/requesting-app-specs). |
|  | [APPLICATION\_CONFIGURATION\_VALUE\_HISTORY](/sql-reference/functions/application_configuration_value_history) | For more information, see [Application configuration](/developer-guide/native-apps/app-configuration). |
| Cortex Agents | [GET\_AI\_RECORD\_TRACE (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_record_trace-snowflake-local) | For more information, see [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations) and [AI Observability data](/sql-reference/local/ai_observability_events). Supports Cortex Agent and External Agent; `agent_type` is `CORTEX AGENT` or `EXTERNAL AGENT`. |
|  | [GET\_AI\_OBSERVABILITY\_LOGS (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_observability_logs-snowflake-local) | For more information, see [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations) and [AI Observability data](/sql-reference/local/ai_observability_events). Supports Cortex Agent and External Agent; `agent_type` is `CORTEX AGENT` or `EXTERNAL AGENT`. |
|  | [GET\_AI\_OBSERVABILITY\_EVENTS (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_observability_events-snowflake-local) | For more information, see [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor), [Monitor Cortex Search requests](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor), and [AI Observability data](/sql-reference/local/ai_observability_events). `agent_type` is `CORTEX AGENT`, `EXTERNAL AGENT`, or `CORTEX SEARCH SERVICE`. |
|  | [GET\_AI\_EVALUATION\_DATA (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_evaluation_data-snowflake-local) | For more information, see [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations) and [AI Observability data](/sql-reference/local/ai_observability_events). Supports Cortex Agent and External Agent; `agent_type` is `CORTEX AGENT` or `EXTERNAL AGENT`. |
|  | [SYSTEM$CREATE\_EVALUATION\_DATASET](/sql-reference/functions/system_create_evaluation_dataset) | For more information, see [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations). |

Expand

Show lessSee more

## Syntax

Copy code

```
SELECT ...
  FROM [ <input_table> [ [AS] <alias_1> ] ,
         [ LATERAL ]
       ]
       TABLE( <table_function>( [ <arg_1> [, ... ] ] ) ) [ [ AS ] <alias_2> ];
```

For function-specific syntax, see the documentation for the individual system-defined table functions.

## Usage notes

- Table functions can also be applied to a set of rows using the LATERAL construct.
- To enable using table expressions, Snowflake supports ANSI/ISO standard syntax for table expressions in the [FROM](/sql-reference/constructs/from) clause of queries and subqueries. This syntax is used to
  indicate that an expression returns a collection of rows instead of a single row.
- This ANSI/ISO syntax is valid only in the [FROM](/sql-reference/constructs/from) clause of the [SELECT](/sql-reference/sql/select) list. You cannot omit these keywords and parentheses from a
  collection subquery specification in any other context.
