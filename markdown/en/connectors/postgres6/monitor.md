# Monitoring the Snowflake Connector for PostgreSQL

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for PostgreSQL.
Note that we’re now focused on a next-generation solution that will offer a significantly improved experience.
Hence, moving this connector to the general availability status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/about) and
includes better performance, customizability, and enhanced deployment options.

The following sections describe how to monitor the connector by querying views and examining log files:

- [Viewing general information about the connector](#label-postgres-connector-monitoring-general-info-6)
- [Viewing data sources](#label-postgres-connector-monitoring-data-sources-6)
- [Viewing the replication state of data sources](#label-postgres-connector-monitoring-data-sources-state-6)
- [Viewing the replication state of source tables](#label-postgres-connector-monitoring-replication-state-6)
- [Viewing table schema version history](#label-postgres-connector-monitoring-schema-version-history-6)
- [Viewing connector metrics](#label-postgres-connector-monitoring-connector-stats-6)
- [Viewing aggregated connector metrics](#label-postgres-connector-monitoring-connector-aggregated-stats-6)
- [Viewing experimental views](#label-postgres-connector-examining-experimental-views)
- [Viewing the connector audit log view](#label-postgres-connector-audit-log-6)
- [Viewing the agent audit log view](#label-postgres-connector-agent-audit-log-6)
- [Viewing the connector logs](#label-postgres-connector-viewing-connector-logs-6)
- [Viewing the agent logs](#label-postgres-connector-viewing-agent-logs-6)

## Viewing general information about the connector

To view general information about the connector, run [DESCRIBE APPLICATION](/sql-reference/sql/desc-application) command:

> Copy code
>
> ```
> DESCRIBE APPLICATION <app_db_name>;
> ```
>
> Where:
>
> > `app_db_name`
> > :   Specifies the name of the connector database.

To view more specific information about the connector, query the `PUBLIC.CONNECTOR_CONFIGURATION` view:

> Copy code
>
> ```
> SELECT * FROM PUBLIC.CONNECTOR_CONFIGURATION;
> ```

The `PUBLIC.CONNECTOR_CONFIGURATION` view displays a row for each parameter configured for the connector.

The following table describes these parameters:

| Parameter | Description |
| --- | --- |
| alertingLogsView | If you [enabled email notifications](/connectors/postgres6/email-notifications#label-postgres-connector-enable-email-notifications-6), this specifies the name of [the view that provides access to the event table](/connectors/postgres6/email-notifications#label-postgres-connector-create-logs-view-6). |
| alertingNotificationIntegration | If you [enabled email notifications](/connectors/postgres6/email-notifications#label-postgres-connector-enable-email-notifications-6), this specifies the name of the notification integration object used for email notifications. |
| alertingRecipients | If you [enabled email notifications](/connectors/postgres6/email-notifications#label-postgres-connector-enable-email-notifications-6), this specifies the list of email addresses (separated by commas) that can receive email notifications from the connector. |
| alertingSchedule | If you [enabled email notifications](/connectors/postgres6/email-notifications#label-postgres-connector-enable-email-notifications-6), this specifies the schedule or frequency at which the connector should check for errors and send a notification. |
| operational\_warehouse | Name of the operational warehouse used by the connector. |
| warehouse | Name of the compute warehouse for merging data. |

Expand

Show lessSee more

## Viewing data sources

To view information about data sources, query the `PUBLIC.DATA_SOURCES` view:

> Copy code
>
> ```
> SELECT * FROM PUBLIC.DATA_SOURCES;
> ```

The `PUBLIC.DATA_SOURCES` view displays a row for each data source configured for the connector. The view consists of the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| NAME | VARCHAR | Name of the data source. |
| SCHEDULE | VARCHAR | Schedule for running the replication. Displays NULL if scheduled replication of that data source is disabled. |
| DESTINATION\_DB\_NAME | VARCHAR | Name of the destination database. |

Expand

Show lessSee more

## Viewing the replication state of data sources

To view the current replication state of data sources, query the `PUBLIC.DATA_SOURCE_REPLICATION_STATE` view:

> Copy code
>
> ```
> SELECT * FROM PUBLIC.DATA_SOURCE_REPLICATION_STATE;
> ```

The `PUBLIC.DATA_SOURCE_REPLICATION_STATE` view displays a row for each data source configured in the connector. The view consists of the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| NAME | VARCHAR | Name of the data source. |
| TABLES\_ADDED\_COUNT | NUMBER | Numbers of tables actively replicated in this data source. This number does not include tables for which the replication failed permanently. |
| CONNECTED\_AGENT\_ID | VARCHAR | ID of the agent application assigned to the data source. |
| SCHEDULE | VARCHAR | Schedule for running the replication. Displays NULL if scheduled replication of that data source is disabled. |
| REPLICATION\_STATUS | VARCHAR | Replication status of the data source. Possible values:   - `WAITING` - `ONGOING` |
| PREVIOUS\_SCHEDULED\_RUN\_STATUS | VARCHAR | Status of previous scheduled replication. Displays NULL if scheduled replication of that data source is disabled. Possible values:   - `DONE` - `WARNING` |
| PREVIOUS\_RUN\_FINISHED\_AT | TIMESTAMP\_NTZ | Timestamp of the end of last scheduled replication. Displays NULL if scheduled replication of that data source is disabled. |

Expand

Show lessSee more

## Viewing the replication state of source tables

To view the current replication state of each source table, query the `PUBLIC.REPLICATION_STATE` view:

> Copy code
>
> ```
> SELECT * FROM PUBLIC.REPLICATION_STATE;
> ```

The `PUBLIC.REPLICATION_STATE` view displays a row for each source table. The view consists of the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| DATA\_SOURCE\_NAME | VARCHAR | Name of the data source that contains the source table |
| SCHEMA\_NAME | VARCHAR | Name of the schema of the source table |
| TABLE\_NAME | VARCHAR | Name of the source table |
| REPLICATION\_PHASE | VARCHAR | Current replication phase. Possible values:   - `SCHEMA_INTROSPECTION` - `INITIAL_LOAD` - `INCREMENTAL_LOAD`   For descriptions of each status, see [Understanding replication phases](#label-postgres-connector-monitoring-replication-phase-descriptions-6). |
| SCHEMA\_INTROSPECTION\_STATUS | VARCHAR | Current schema introspection status. Possible values:   - `WAITING` - `IN_PROGRESS` - `DONE` - `RETRYING` - `FAILED` |
| SNAPSHOT\_REPLICATION\_STATUS | VARCHAR | Current snapshot replication status. Possible values:   - `WAITING` - `IN_PROGRESS` - `DONE` - `RETRYING` - `FAILED` |
| INCREMENTAL\_REPLICATION\_STATUS | VARCHAR | Current incremental replication status. Possible values:   - `WAITING` - `IN_PROGRESS` - `DONE` - `RETRYING` - `FAILED` |

Expand

Show lessSee more

### Understanding replication phases

Replication of each of the source tables can be in the following replication phases:

| Replication Phase | Description |
| --- | --- |
| `SCHEMA_INTROSPECTION` | Schema of the source table is being checked. Once this phase is done the destination table is created. |
| `INITIAL_LOAD` | The connector is processing the snapshot load for the source table. |
| `INCREMENTAL_LOAD` | Initial load is done, data is being replicated using change data capture process. |

Expand

Show lessSee more

Note

You can start FAILED replications from the beginning by removing table from replication and adding it again as described in [Configuring replication for the Snowflake Connector for PostgreSQL](/connectors/postgres6/configure-replication#label-postgres-connector-configure-replication-6).

## Viewing table schema version history

To view the history of table schema changes, query the `PUBLIC.SCHEMA_CHANGE_HISTORY` view using a command similar to:

> Copy code
>
> ```
> SELECT * FROM PUBLIC.SCHEMA_CHANGE_HISTORY;
> ```

The `PUBLIC.SCHEMA_CHANGE_HISTORY` view displays one or two rows for each table’s valid schema version.

The view consists of the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| DATA\_SOURCE\_NAME | VARCHAR | Source table data source name. |
| SCHEMA\_NAME | VARCHAR | Source table schema name. |
| TABLE\_NAME | VARCHAR | Source table name. |
| VERSION | INTEGER | Schema version identifier, initially 0, and incremented by 1 with each schema change. Numbering restarts at zero if the table is removed and later re-added. |
| STATE | VARCHAR | one of:  - ACCEPTED: schema change is valid, but has yet to be applied to the destination table. - APPLIED: schema change has already been applied to the destination table.  Initially, at the start of the replication, contains only a single row with the value APPLIED. After subsequent valid schema changes will include two rows - one with state=ACCEPTED and one with state=APPLIED. |
| SOURCE\_SCHEMA | VARIANT | JSON describing the schema of the source table. |
| DESTINATION\_TABLE\_SCHEMA | VARIANT | JSON describing the schema of the destination table after this schema version is applied. |
| INSERTED\_AT | TIMESTAMP\_NTZ | UTC timestamp when this record was inserted. |

Expand

Show lessSee more

## Viewing connector metrics

To view the connector replication metrics, query the `PUBLIC.CONNECTOR_STATS` view:

> Copy code
>
> ```
> SELECT * FROM PUBLIC.CONNECTOR_STATS;
> ```

The `PUBLIC.CONNECTOR_STATS` view displays a row for each periodic merge of data into destination table during incremental load replication phase.

Note

The first run for a given table in this view will be longer and larger than a typical later run. This is due to the fact that the connector gathers incremental updates to tables during the initial load phase, but processes them only after the whole table has been replicated.

The view consists of the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| RESOURCE\_INGESTION\_DEFINITION\_ID | VARCHAR | Identifier of a replicated table constructed from data source name, schema name and table name. |
| INGESTION\_CONFIGURATION\_ID | VARCHAR | Internal column for future integrations. |
| INGESTION\_PROCESS\_ID | VARCHAR | ID of the merge process. |
| INGESTION\_DEFINITION\_NAME | VARCHAR | Internal column for future integrations. |
| DATA\_SOURCE\_NAME | VARCHAR | Name of the data source to which the table belongs. |
| SCHEMA\_NAME | VARCHAR | Name of the table’s schema. |
| RESOURCE\_NAME | VARCHAR | Table name. |
| STARTED\_AT | TIMESTAMP\_NTZ | Time when the first record of the batch of records merged to the destination table was read from source database. |
| STATUS | VARCHAR | Merge process status. Possible values:   - `FINISHED` - `FAILED` |
| INGESTED\_ROWS | NUMBER | Number of rows merged in the batch |
| INGESTION\_DURATION\_S | NUMBER | Batch processing time in seconds calculated as difference between first record being observed and the batch of records being merged into the destination table. |
| NATIVE\_APP\_PROCESSING\_DURATION\_S | NUMBER | Duration in seconds of data processing on Snowflake side. |
| AGENT\_PROCESSING\_DURATION\_S | NUMBER | Duration in seconds of data processing on agent side. |
| THROUGHPUT\_RPS | NUMBER | Connector throughput in records per second (RPS). Takes into account the overall processing time. |
| NATIVE\_APP\_THROUGHPUT\_RPS | NUMBER | Throughput of the data processing on Snowflake side in records per second (RPS). |

Expand

Show lessSee more

## Viewing aggregated connector metrics

To view the connector replication metrics, query the `PUBLIC.AGGREGATED_CONNECTOR_STATS` view:

> Copy code
>
> ```
> SELECT * FROM PUBLIC.AGGREGATED_CONNECTOR_STATS;
> ```

The `PUBLIC.AGGREGATED_CONNECTOR_STATS` view shows the metrics of the connector aggregated hourly. Additional columns with data source name, schema name and table name are provided for further aggregations and analysis.

The view consists of the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| DATE | DATE | Date of the aggregate, hourly. |
| PROCESSED\_ROWS\_COUNT | NUMBER | Sum of rows ingested for the table during the aggregate time. |
| THROUGHPUT\_RPS | NUMBER | Throughput for the table for the aggregate time in records per second (RPS). |
| DATA\_SOURCE\_NAME | VARCHAR | Name of the data source to which the table belongs. |
| SCHEMA\_NAME | VARCHAR | Name of the table’s schema. |
| SOURCE\_TABLE\_NAME | VARCHAR | Table name. |

Expand

Show lessSee more

## Viewing experimental views

The connector comes with a several additional views containing low-level information about the state of the connector and support state
change history tracking. These views are found in the `PUBLIC` schema with names that begin with the prefix `EXPERIMENTAL`.

The following table summarizes the currently available experimental views:

| View Name | Description |
| --- | --- |
| **EXPERIMENTAL\_TABLE\_REPLICATION\_HISTORY** | A history of state changes for all enabled source tables in the connector. |
| **EXPERIMENTAL\_DATA\_SOURCE\_REPLICATION\_HISTORY** | A history of state changes for all configured data sources in the connector. |
| **EXPERIMENTAL\_EVENTS\_HISTORY** | A history of all events that occurred in the connector. |

Expand

Show lessSee more

Note

Experimental views are subject to change and can be modified or removed in future connector releases.

## Viewing the connector audit log view

To view the audit log of user actions in the connector, query the `PUBLIC.AUDIT_LOG` view:

> Copy code
>
> ```
> SELECT * FROM PUBLIC.AUDIT_LOG;
> ```

The `PUBLIC.AUDIT_LOG` view displays a row for each user-initiated action recorded by the connector.

The view consists of the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| ACTION\_TIME | TIMESTAMP\_NTZ | Time when the action happened. |
| ACTION\_TYPE | VARCHAR | Action type. |
| PARAMETERS | VARIANT | Additional parameters of the action. |

Expand

Show lessSee more

Actions recorded in this view are:

> - Data source added
> - Table replication enabled
> - Table replication disabled
> - Scheduled replication enabled for data source
> - Scheduled replication disabled for data source

## Viewing the agent audit log view

To view the audit log of agent actions in the connector, query the `PUBLIC.AGENT_AUDIT_LOG` view:

> Copy code
>
> ```
> SELECT * FROM PUBLIC.AGENT_AUDIT_LOG;
> ```

The `PUBLIC.AGENT_AUDIT_LOG` view displays a row for each agent-reported action registered by the connector.

The view consists of the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| ACTION\_TIME | TIMESTAMP\_NTZ | Time when the action happened. |
| ACTION\_TYPE | VARCHAR | Action type. |
| PARAMETERS | VARIANT | Additional parameters of the action. |

Expand

Show lessSee more

Actions shown in this view are:

> - Agent assigned to data source
> - Agent unassigned from data source
> - Agent registered
> - Agent unregistered
> - Snapshot load started
> - Snapshot load finished
> - Snapshot load failed
> - Snapshot load terminated
> - Schema introspection succeeded
> - Schema introspection failed
> - Incremental load started
> - Incremental load stopped
> - Incremental load failed
> - Incremental load terminated
> - Schema change reported

## Viewing the connector logs

To view the connector logs, query the event table that you created while setting up the connector [log view](/connectors/postgres6/install-snowsight#label-postgres-connector-configure-logging-6).

Copy code

```
SELECT * FROM <fully_qualified_event_table_name>
   WHERE RECORD_TYPE = 'LOG'
   AND RESOURCE_ATTRIBUTES:"snow.database.name" = '<app_db_name>';
```

Where:

`fully_qualified_event_table_name`
:   Specifies the fully qualified name of the event table.

`app_db_name`
:   Specifies the name of the connector database.

## Viewing the agent logs

> When the agent is running, it periodically sends logs to Snowflake. These logs are available in the `AGENT_LOGS` view
> and can be retrieved using the following query:
>
> > Copy code
> >
> > ```
> > SELECT * FROM PUBLIC.AGENT_LOGS;
> > ```

## Next steps

If required, and after completing these procedures, review the steps in [Troubleshooting the Snowflake Connector for PostgreSQL](/connectors/postgres6/troubleshoot).
