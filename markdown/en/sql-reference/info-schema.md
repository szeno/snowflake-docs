# Snowflake Information Schema

The Snowflake Information Schema (aka “Data Dictionary”) consists of a set of system-defined views and table functions that provide
extensive metadata information about the objects created in your account. The Snowflake Information Schema is based on the SQL-92 ANSI
Information Schema, but with the addition of views and functions that are specific to Snowflake.

The Information Schema is implemented as a schema named INFORMATION\_SCHEMA that Snowflake automatically creates in every database in
an account.

Note

ANSI uses the term “catalog” to refer to databases. To maintain compatibility with the standard, the Snowflake Information Schema
topics use “catalog” in place of “database” where applicable. For all intents and purposes, the terms are conceptually equivalent
and interchangeable.

## What is INFORMATION\_SCHEMA?

Each database created in your account automatically includes a built-in, read-only schema named INFORMATION\_SCHEMA. The schema contains
the following objects:

- Views for all the objects contained in the database, as well as views for account-level objects (i.e. non-database objects such as
  roles, warehouses, and databases)
- Table functions for historical and usage data across your account.

## List of Information Schema views

The views in INFORMATION\_SCHEMA display metadata about objects defined in the database, as well as metadata for non-database,
account-level objects that are common across all databases. Each instance of INFORMATION\_SCHEMA includes:

> - ANSI-standard views for the database and account-level objects that are relevant to Snowflake.
> - Snowflake-specific views for the non-standard objects that Snowflake supports (stages, file formats, etc.).

Information Schema views that are Snowflake-specific (that is, that are **not** ANSI-standard) are marked with ✔ in
the “Snowflake-specific” column in the following table.

| View | Type | Snowflake-specific | Notes |
| --- | --- | --- | --- |
| [APPLICABLE\_ROLES](/sql-reference/info-schema/applicable_roles) | Account |  |  |
| [APPLICATION\_CONFIGURATIONS](/sql-reference/info-schema/application_configurations) | Database | ✔ |  |
| [APPLICATION\_SPECIFICATIONS](/sql-reference/info-schema/application_specifications) | Database | ✔ |  |
| [CHECK\_CONSTRAINTS](/sql-reference/info-schema/check_constraints) | Database |  |  |
| [CLASS\_INSTANCE\_FUNCTIONS](/sql-reference/info-schema/class_instance_functions) | Database | ✔ |  |
| [CLASS\_INSTANCE\_PROCEDURES](/sql-reference/info-schema/class_instance_procedures) | Database | ✔ |  |
| [CLASS\_INSTANCES](/sql-reference/info-schema/class_instances) | Database | ✔ |  |
| [CLASSES](/sql-reference/info-schema/classes) | Database | ✔ |  |
| [COLUMNS](/sql-reference/info-schema/columns) | Database |  |  |
| [CORTEX\_SEARCH\_SERVICE](/sql-reference/info-schema/cortex_search) | Database | ✔ |  |
| [CORTEX\_SEARCH\_SERVICE\_SCORING\_PROFILES](/sql-reference/info-schema/cortex_search_service_scoring_profiles) | Database | ✔ |  |
| [CURRENT\_PACKAGES\_POLICY](/sql-reference/info-schema/current_packages_policy) | Database | ✔ |  |
| [DATABASES](/sql-reference/info-schema/databases) | Account | ✔ |  |
| [ELEMENT\_TYPES](/sql-reference/info-schema/element_types) | Database |  |  |
| [ENABLED\_ROLES](/sql-reference/info-schema/enabled_roles) | Account |  |  |
| [EVENT\_TABLES](/sql-reference/info-schema/event_tables) | Database | ✔ |  |
| [EXTERNAL\_TABLES](/sql-reference/info-schema/external_tables) | Database | ✔ |  |
| [FIELDS](/sql-reference/info-schema/fields) | Database |  |  |
| [FILE FORMATS](/sql-reference/info-schema/file_formats) | Database | ✔ |  |
| [FUNCTIONS](/sql-reference/info-schema/functions) | Database |  |  |
| [HYBRID\_TABLES](/sql-reference/info-schema/hybrid_tables) | Database | ✔ |  |
| [INDEXES](/sql-reference/info-schema/indexes) | Database | ✔ |  |
| [INDEX\_COLUMNS](/sql-reference/info-schema/index_columns) | Database | ✔ |  |
| [INFORMATION\_SCHEMA\_CATALOG\_NAME](/sql-reference/info-schema/information_schema_catalog_name) | Account |  |  |
| [LISTINGS](/sql-reference/info-schema/listings) | Account | ✔ |  |
| [LOAD\_HISTORY](/sql-reference/info-schema/load_history) | Account | ✔ | Data retained for 14 days. |
| [MODEL\_VERSIONS](/sql-reference/info-schema/model_versions) | Database | ✔ |  |
| [OBJECT\_PRIVILEGES](/sql-reference/info-schema/object_privileges) | Account |  |  |
| [PACKAGES](/sql-reference/info-schema/packages) | Database | ✔ |  |
| [PIPES](/sql-reference/info-schema/pipes) | Database | ✔ |  |
| [PROCEDURES](/sql-reference/info-schema/procedures) | Database | ✔ |  |
| [REFERENTIAL\_CONSTRAINTS](/sql-reference/info-schema/referential_constraints) | Database |  |  |
| [REPLICATION\_DATABASES](/sql-reference/info-schema/replication_databases) | Account | ✔ |  |
| [REPLICATION\_GROUPS](/sql-reference/info-schema/replication_groups) | Account | ✔ |  |
| [SCHEMATA](/sql-reference/info-schema/schemata) | Database |  |  |
| [SEMANTIC\_DIMENSIONS](/sql-reference/info-schema/semantic_dimensions) | Database | ✔ |  |
| [SEMANTIC\_FACTS](/sql-reference/info-schema/semantic_facts) | Database | ✔ |  |
| [SEMANTIC\_METRICS](/sql-reference/info-schema/semantic_metrics) | Database | ✔ |  |
| [SEMANTIC\_RELATIONSHIPS](/sql-reference/info-schema/semantic_relationships) | Database | ✔ |  |
| [SEMANTIC\_TABLES](/sql-reference/info-schema/semantic_tables) | Database | ✔ |  |
| [SEMANTIC\_VIEW](/sql-reference/info-schema/semantic_views) | Database | ✔ |  |
| [SEQUENCES](/sql-reference/info-schema/sequences) | Database |  |  |
| [SERVICES](/sql-reference/info-schema/services) | Database | ✔ |  |
| [SHARES](/sql-reference/info-schema/shares) | Account | ✔ |  |
| [STAGES](/sql-reference/info-schema/stages) | Database | ✔ |  |
| [TABLE\_CONSTRAINTS](/sql-reference/info-schema/table_constraints) | Database |  |  |
| [TABLE\_PRIVILEGES](/sql-reference/info-schema/table_privileges) | Database |  |  |
| [TABLE\_STORAGE\_METRICS](/sql-reference/info-schema/table_storage_metrics) | Database | ✔ |  |
| [TABLES](/sql-reference/info-schema/tables) | Database |  | Displays tables and views. |
| [TYPES](/sql-reference/info-schema/types) | Database | ✔ |  |
| [USAGE\_PRIVILEGES](/sql-reference/info-schema/usage_privileges) | Database |  | Displays privileges on sequences only; to view privileges on other types of objects, use OBJECT\_PRIVILEGES. |
| [VIEWS](/sql-reference/info-schema/views) | Database |  |  |

Expand

Show lessSee more

## List of Information Schema table functions

The table functions in INFORMATION\_SCHEMA can be used to return account-level usage and historical information for storage, warehouses,
user logins, and queries:

| Table Function | Data Retention | Notes |
| --- | --- | --- |
| [ALERT\_HISTORY](/sql-reference/functions/alert_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [APPLICATION\_CALLBACK\_HISTORY](/sql-reference/functions/application_callback_history) | 365 days | Results depend on the privileges assigned to the user’s current role. |
| [APPLICATION\_CONFIGURATION\_VALUE\_HISTORY](/sql-reference/functions/application_configuration_value_history) | 365 days | Results depend on the privileges assigned to the user’s current role. |
| [APPLICATION\_SPECIFICATION\_STATUS\_HISTORY](/sql-reference/functions/application_specification_status_history) | 365 days | Results depend on the privileges assigned to the user’s current role. |
| [AUTOMATIC\_CLUSTERING\_HISTORY](/sql-reference/functions/automatic_clustering_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [AUTO\_REFRESH\_REGISTRATION\_HISTORY](/sql-reference/functions/auto_refresh_registration_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [AVAILABLE\_LISTINGS](/sql-reference/functions/available_listings) | N/A | Results are returned for all listings that consumers can discover and access. |
| [AVAILABLE\_LISTING\_REFRESH\_HISTORY](/sql-reference/functions/available_listing_refresh_history) | 14 days | Results are only returned for consumers of listings who have any privilege on the available listing or mounted database. |
| [COMPLETE\_TASK\_GRAPHS](/sql-reference/functions/complete_task_graphs) | 60 minutes | Results returned only for the ACCOUNTADMIN role, the task owner (i.e. the role with the OWNERSHIP privilege on the task), or a role with the global MONITOR EXECUTION privilege. |
| [COPY\_HISTORY](/sql-reference/functions/copy_history) | 14 days | Results depend on the privileges assigned to the user’s current role. |
| [CORTEX\_SEARCH\_REFRESH\_HISTORY](/sql-reference/functions/cortex_search_refresh_history) | 7 days | Results depend on the privileges assigned to the user’s current role. |
| [CURRENT\_TASK\_GRAPHS](/sql-reference/functions/current_task_graphs) | N/A | Results returned only for the ACCOUNTADMIN role, the task owner (i.e. the role with the OWNERSHIP privilege on the task), or a role with the global MONITOR EXECUTION privilege. |
| [DATA\_METRIC\_FUNCTION\_REFERENCES](/sql-reference/functions/data_metric_function_references) | N/A | Results depend on the privileges or database role assigned to the user’s current role. |
| [DATA\_TRANSFER\_HISTORY](/sql-reference/functions/data_transfer_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [DATABASE\_REFRESH\_HISTORY](/sql-reference/functions/database_refresh_history) | 14 days | Results depend on the privileges assigned to the user’s current role. |
| [DATABASE\_REFRESH\_PROGRESS , DATABASE\_REFRESH\_PROGRESS\_BY\_JOB](/sql-reference/functions/database_refresh_progress) | 14 days | Results depend on the privileges assigned to the user’s current role. |
| [DATABASE\_REPLICATION\_USAGE\_HISTORY](/sql-reference/functions/database_replication_usage_history) | 14 days | Results returned only for the ACCOUNTADMIN role. |
| [DATABASE\_STORAGE\_USAGE\_HISTORY](/sql-reference/functions/database_storage_usage_history) | 6 months | Results depend on MONITOR USAGE privilege. [1] |
| [DBT\_PROJECT\_EXECUTION\_HISTORY](/sql-reference/functions/dbt_project_execution_history) | 7 days | Results depend on MONITOR, OWNERSHIP, or USAGE privilege. |
| [DCM\_DEPLOYMENT\_HISTORY](/sql-reference/info-schema/dcm_deployment_history) | 7 days | Results depend on the privileges assigned to the user’s current role. |
| [DYNAMIC\_TABLES](/sql-reference/functions/dynamic_tables) | 7 days | Results depend on the privileges assigned to the user’s current role. For more information, see [Dynamic table access control](/user-guide/dynamic-tables/privileges). [1] |
| [DYNAMIC\_TABLE\_GRAPH\_HISTORY](/sql-reference/functions/dynamic_table_graph_history) | 7 days | Results depend on the privileges assigned to the user’s current role. For more information, see [Dynamic table access control](/user-guide/dynamic-tables/privileges). [1] |
| [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) | 7 days | Results depend on the privileges assigned to the user’s current role. For more information, see [Dynamic table access control](/user-guide/dynamic-tables/privileges). [1] |
| [EXTERNAL\_FUNCTIONS\_HISTORY](/sql-reference/functions/external_functions_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [EXTERNAL\_TABLE\_FILES](/sql-reference/functions/external_table_files) | N/A | Results depend on the privileges assigned to the user’s current role. |
| [EXTERNAL\_TABLE\_FILE\_REGISTRATION\_HISTORY](/sql-reference/functions/external_table_registration_history) | 30 days | Results depend on the privileges assigned to the user’s current role. |
| [ICEBERG\_TABLE\_FILES](/sql-reference/functions/iceberg_table_files) | Varies | Results depend on the value of the [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days) parameter set for the table. For more information, see [Metadata and retention for Apache Iceberg™ tables](/user-guide/tables-iceberg-metadata). |
| [ICEBERG\_TABLE\_SNAPSHOT\_REFRESH\_HISTORY](/sql-reference/functions/iceberg_table_snapshot_refresh_history) | Varies | Results depend on the value of the [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days) parameter set for the table. For more information, see [Metadata and retention for Apache Iceberg™ tables](/user-guide/tables-iceberg-metadata). |
| [LISTING\_REFRESH\_HISTORY](/sql-reference/functions/listing_refresh_history) | 14 days | Results are only returned for a role with any privilege on Listing Auto-Fulfillment. |
| [LOGIN\_HISTORY , LOGIN\_HISTORY\_BY\_USER](/sql-reference/functions/login_history) | 7 days | Results depend on the privileges assigned to the user’s current role. |
| [MATERIALIZED\_VIEW\_REFRESH\_HISTORY](/sql-reference/functions/materialized_view_refresh_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [NOTIFICATION\_HISTORY](/sql-reference/functions/notification_history) | 14 days | Results returned only for the ACCOUNTADMIN role, the integration owner (i.e. the role with the OWNERSHIP privilege on the integration) or a role with the USAGE privilege on the integration. |
| [ONLINE\_FEATURE\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/online-feature-table-refresh-history) | 7 days | Results depend on the privileges assigned to the user’s current role. |
| [PIPE\_USAGE\_HISTORY](/sql-reference/functions/pipe_usage_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [POLICY\_REFERENCES](/sql-reference/functions/policy_references) | N/A | Results returned only for the ACCOUNTADMIN role. |
| [QUERY\_ACCELERATION\_HISTORY](/sql-reference/functions/query_acceleration_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [QUERY\_HISTORY , QUERY\_HISTORY\_BY\_\*](/sql-reference/functions/query_history) | 7 days | Results depend on the privileges assigned to the user’s current role. |
| [REPLICATION\_GROUP\_DANGLING\_REFERENCES](/sql-reference/functions/replication_group_dangling_references) | N/A |  |
| [REPLICATION\_GROUP\_REFRESH\_HISTORY, REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL](/sql-reference/functions/replication_group_refresh_history) | 14 days | Results are only returned for a role with any privilege on the replication or failover group. |
| [REPLICATION\_GROUP\_REFRESH\_PROGRESS, REPLICATION\_GROUP\_REFRESH\_PROGRESS\_BY\_JOB, REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL](/sql-reference/functions/replication_group_refresh_progress) | 14 days | Results are only returned for a role with any privilege on the replication or failover group. |
| [REPLICATION\_GROUP\_USAGE\_HISTORY](/sql-reference/functions/replication_group_usage_history) | 14 days | Results depend on the MONITOR USAGE privilege. [1] |
| [REPLICATION\_USAGE\_HISTORY](/sql-reference/functions/replication_usage_history) | 14 days | Results returned only for the ACCOUNTADMIN role. |
| [REST\_EVENT\_HISTORY](/sql-reference/functions/rest_event_history) | 7 days | Results returned only for the ACCOUNTADMIN role. |
| [SEARCH\_OPTIMIZATION\_HISTORY](/sql-reference/functions/search_optimization_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [SERVERLESS\_ALERT\_HISTORY](/sql-reference/functions/serverless_alert_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [SERVERLESS\_TASK\_HISTORY](/sql-reference/functions/serverless_task_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [STAGE\_DIRECTORY\_FILE\_REGISTRATION\_HISTORY](/sql-reference/functions/stage_directory_file_registration_history) | 14 days | Results depend on the privileges assigned to the user’s current role. |
| [STAGE\_STORAGE\_USAGE\_HISTORY](/sql-reference/functions/stage_storage_usage_history) | 6 months | Results depend on MONITOR USAGE privilege. [1] |
| [STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/functions/storage_lifecycle_policy_history) | 14 days | Results depend on the privileges assigned to the user’s current role. |
| [TAG\_REFERENCES](/sql-reference/functions/tag_references) | N/A | Results are only returned for the role that has access to the specified object. |
| [TAG\_REFERENCES\_ALL\_COLUMNS](/sql-reference/functions/tag_references_all_columns) | N/A | Results are only returned for the role that has access to the specified object. |
| [TASK\_DEPENDENTS](/sql-reference/functions/task_dependents) | N/A | Results returned only for the ACCOUNTADMIN role or task owner (role with OWNERSHIP privilege on task). |
| [TASK\_HISTORY](/sql-reference/functions/task_history) | 7 days | Results returned only for the ACCOUNTADMIN role, the task owner (i.e. the role with the OWNERSHIP privilege on the task), or a role with the global MONITOR EXECUTION privilege. |
| [VALIDATE\_PIPE\_LOAD](/sql-reference/functions/validate_pipe_load) | 14 days | Results depend on the privileges assigned to the user’s current role. |
| [WAREHOUSE\_LOAD\_HISTORY](/sql-reference/functions/warehouse_load_history) | 14 days | Results depend on MONITOR USAGE privilege. [1] |
| [WAREHOUSE\_METERING\_HISTORY](/sql-reference/functions/warehouse_metering_history) | 6 months | Results depend on MONITOR USAGE privilege. [1] |

Expand

Show lessSee more

[1] Returns results if role has been assigned the MONITOR USAGE global privilege; otherwise, returns results only for the ACCOUNTADMIN role.

## General usage notes

- Each INFORMATION\_SCHEMA schema is read-only (i.e. the schema, and all the views and table functions in the schema, cannot be modified
  or dropped).
- Queries on INFORMATION\_SCHEMA views do not guarantee consistency with respect to concurrent DDL. For example, if a set of tables are
  created while a long-running INFORMATION\_SCHEMA query is being executed, the result of the query may include some, none, or all of
  the tables created.
- The output of a view or table function depend on the privileges granted to the user’s current role. When querying an INFORMATION\_SCHEMA
  view or table function, only objects for which the current role has been granted access privileges are returned.
- To prevent performance issues, the following error is returned if the filters specified in an INFORMATION\_SCHEMA query are not
  sufficiently selective:
  `Information schema query returned too much data. Please repeat query with more selective predicates.`
- The Snowflake-specific views are subject to change. Avoid selecting all columns from these views. Instead, select the columns that you want.
  For example, if you want the `name` column, use `SELECT name`, rather than `SELECT *`.

Tip

The Information Schema views are optimized for queries that retrieve a small subset of objects from the dictionary. Whenever possible,
maximize the performance of your queries by filtering on schema and object names.

For more usage information and details, see the
[Snowflake Information Schema blog post](https://www.snowflake.com/blog/using-snowflake-information-schema/).

## Considerations for replacing SHOW commands with Information Schema views

The INFORMATION\_SCHEMA views provide a SQL interface to the same information provided by the [SHOW <objects>](/sql-reference/sql/show) commands.
You can use the views to replace these commands; however, there are some key differences to consider before switching:

| Considerations | SHOW Commands | Information Schema Views |
| --- | --- | --- |
| Warehouses | Not required to execute. | Warehouse must be running and currently in use to query the views. |
| Pattern matching/filtering | Case-insensitive (when filtering using LIKE). | Standard (case-sensitive) SQL semantics. Snowflake automatically converts unquoted, case-insensitive identifiers to uppercase internally, so unquoted object names must be queried in uppercase in the Information Schema views. |
| Query results | Most SHOW commands limit results to the current schema by default. | Views display all objects in the current/specified database. To query against a particular schema, you must use a filter predicate (e.g. `... WHERE table_schema = CURRENT_SCHEMA()...`). Note that Information Schema queries lacking sufficiently selective filters return an error and do not execute (see [General Usage Notes](#general-usage-notes) in this topic). |

Expand

Show lessSee more

## Qualifying the names of Information Schema views and table functions in queries

When querying an INFORMATION\_SCHEMA view or table function, you must use the qualified name of the view/table function or the
INFORMATION\_SCHEMA schema must be in use for the session.

For example:

- To query using the fully-qualified names of the view and table function, in the form of `database.information_schema.name`:

  Copy code

  ```
  SELECT table_name, comment FROM testdb.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'PUBLIC' ... ;

  SELECT event_timestamp, user_name FROM TABLE(testdb.INFORMATION_SCHEMA.LOGIN_HISTORY( ... ));
  ```
- To query using the qualified names of the view and table function, in the form of `information_schema.name`:

  Copy code

  ```
  USE DATABASE testdb;

  SELECT table_name, comment FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'PUBLIC' ... ;

  SELECT event_timestamp, user_name FROM TABLE(INFORMATION_SCHEMA.LOGIN_HISTORY( ... ));
  ```
- To query with the INFORMATION\_SCHEMA schema in use for the session:

  Copy code

  ```
  USE SCHEMA testdb.INFORMATION_SCHEMA;

  SELECT table_name, comment FROM TABLES WHERE TABLE_SCHEMA = 'PUBLIC' ... ;

  SELECT event_timestamp, user_name FROM TABLE(LOGIN_HISTORY( ... ));
  ```

  Note

  If you are using a database that was created from a share and you have selected INFORMATION\_SCHEMA as the current schema for the
  session, the SELECT statement might fail with the following error:

  `INFORMATION_SCHEMA does not exist or is not authorized`

  If this occurs, select a different schema for the current schema for the session.

For more detailed examples, see the reference documentation for each view/table function.
