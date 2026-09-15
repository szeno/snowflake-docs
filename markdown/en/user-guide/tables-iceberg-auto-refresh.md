# Automatically refresh Apache Iceberg™ tables

Configure automated metadata refreshes for new or existing externally managed
[Apache Iceberg™ tables](/user-guide/tables-iceberg). With automated refreshes, Snowflake polls your external Iceberg catalog in
a continuous and serverless fashion to synchronize the metadata with the most recent remote changes.

Automated refresh for Iceberg tables works differently from automated refresh for directory tables or external tables because it
doesn’t rely on cloud provider notifications. Instead, you configure the feature according to the following steps:

1. [Set a refresh interval on a catalog integration](#label-tables-iceberg-auto-refresh-configure-cat-int).
   Snowflake supports automated refresh for the following external Iceberg catalog options:

   - REST catalog that complies with the Apache Iceberg REST OpenAPI specification
   - Snowflake Open Catalog
   - Object storage (Delta Lake only)
   - AWS Glue
2. [Create one or more Iceberg tables that use the catalog integration](#label-tables-iceberg-auto-refresh-create-table).
3. [Control automated refresh for each table with the AUTO\_REFRESH parameter](#label-tables-iceberg-auto-refresh-update).

This approach lets you centrally manage refresh settings through the catalog integration while you control individual tables as needed.

Warning

If another engine upgrades an externally managed Iceberg table in a standard Snowflake database from v2 to v3, Snowflake’s
manual and automated refresh for the table will fail. To recover:

1. Using the external engine, perform a DML operation that creates a new snapshot. Updating table properties to change the format
   version (for example, `SET TBLPROPERTIES('format-version'='3')`) doesn’t create a new snapshot on its own. Only after a new
   snapshot is created does the updated format version appear in the Iceberg metadata.
2. After the new snapshot exists, replace the table in Snowflake by running
   [CREATE OR REPLACE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table). Snowflake reads the updated Iceberg metadata
   and recognizes the table as v3.

For more information, see [Iceberg v3 considerations and limitations](/user-guide/tables-iceberg-v3-specification-support#iceberg-v3-considerations-limitations).

## Set the refresh interval on a catalog integration

When you run the [CREATE CATALOG INTEGRATION](/sql-reference/sql/create-catalog-integration) command,
you can specify a value for the `REFRESH_INTERVAL_SECONDS` parameter. Otherwise, the default refresh interval
is 30 seconds. Snowflake only polls the external catalog if there are Iceberg tables defined with the catalog integration.

The following example creates a catalog integration for AWS Glue, specifying a refresh interval of 60 seconds:

Copy code

```
CREATE CATALOG INTEGRATION auto_refresh_catalog_integration
  CATALOG_SOURCE = GLUE
  CATALOG_NAMESPACE = 'my_catalog_namespace'
  TABLE_FORMAT = ICEBERG
  GLUE_AWS_ROLE_ARN = 'arn:aws:iam::123456789123:role/my-catalog-role'
  GLUE_CATALOG_ID = '123456789123'
  ENABLED = TRUE
  REFRESH_INTERVAL_SECONDS = 60;
```

To update the refresh interval for a catalog integration, use the [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) command.

For example:

Copy code

```
ALTER CATALOG INTEGRATION auto_refresh_catalog_integration SET REFRESH_INTERVAL_SECONDS = 120;
```

## Create an Iceberg table with automated refresh

Create an Iceberg table by using the [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) command. To specify that the
table should use automated metadata refreshes, set `AUTO_REFRESH = TRUE`.

The following example creates an Iceberg table that uses AWS Glue as the catalog, specifying
the catalog integration created previously (`auto_refresh_catalog_integration`)
and the [CATALOG\_TABLE\_NAME](/sql-reference/sql/create-iceberg-table-aws-glue#label-create-iceberg-table-aws-glue-table-name-param) from AWS Glue.

Copy code

```
CREATE OR REPLACE ICEBERG TABLE auto_refresh_iceberg_table
  CATALOG_TABLE_NAME = 'myGlueTable'
  CATALOG = 'auto_refresh_catalog_integration'
  AUTO_REFRESH = TRUE;
```

## Enable or turn off automated refresh

Note

- If the table uses a catalog integration created before Snowflake version 8.22, you must use the
  [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) command to
  set the `REFRESH_INTERVAL_SECONDS` parameter before you enable automated refresh on the table.
- Frequently toggling automated refresh on and off for an Iceberg table can slow metadata refreshes for the table.

Use the [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) command to enable or turn off automated refresh for an existing Iceberg table.

For example:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table SET AUTO_REFRESH = FALSE;
```

## Monitoring automated refresh status

### SHOW ICEBERG TABLES

To get the automated refresh status for multiple tables, use the [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) command.

Copy code

```
SHOW ICEBERG TABLES;
```

The command output includes a column named `auto_refresh_status`, which displays the same information as
the [SYSTEM$AUTO\_REFRESH\_STATUS](/sql-reference/functions/system_auto_refresh_status) function for each table that you have access privileges on.

### SYSTEM$AUTO\_REFRESH\_STATUS

To retrieve the automated refresh status for a specific table, call the [SYSTEM$AUTO\_REFRESH\_STATUS](/sql-reference/functions/system_auto_refresh_status) function.

Copy code

```
SELECT SYSTEM$AUTO_REFRESH_STATUS('my_iceberg_table');
```

The function returns details about the pipe that Snowflake uses to automate refreshes for the table, such as the execution state
and size of the snapshot queue.
An execution state of `RUNNING` indicates that automated refresh is running as expected.
For more information, see [SYSTEM$AUTO\_REFRESH\_STATUS](/sql-reference/functions/system_auto_refresh_status).

### ICEBERG\_TABLE\_SNAPSHOT\_REFRESH\_HISTORY

To retrieve metadata and snapshot information about the most recent refresh history for a specific table,
use the [ICEBERG\_TABLE\_SNAPSHOT\_REFRESH\_HISTORY](/sql-reference/functions/iceberg_table_snapshot_refresh_history) function.

Copy code

```
SELECT *
FROM TABLE(INFORMATION_SCHEMA.ICEBERG_TABLE_SNAPSHOT_REFRESH_HISTORY(
  TABLE_NAME => 'my_iceberg_table'
));
```

### Monitor automated refresh events

You can configure Snowflake to record an event that provides information about the status of automated refresh for an Iceberg table.
Snowflake records the event in the [event table for your account](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-set-for-account).

Important

To monitor Iceberg auto refresh events, you need an active account-level event table and you need to set [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) to DEBUG at either
the table, database, or schema level. Snowflake records events to your active event table set at the account level, not the database level.

Monitoring automated refresh events can help you gain insight into the following areas:

- **Automated refresh progress**: Track how snapshots move through the automated refresh process.
- **Aggregated statistics**: Review summarized statistics for automated refresh operations.

You can also configure alerts for the following critical conditions:

- Refresh errors
- High refresh latencies

Note

Logging events for automated refresh incurs costs. For more information, see [Costs of telemetry data collection](/developer-guide/logging-tracing/logging-tracing-billing).

Snowflake records an event when automated refresh starts, completes, or results in error.

#### Set the severity level to capture events

To capture automated refresh events, you must set the [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) parameter at the Iceberg table level or account level.
`LOG_EVENT_LEVEL` determines which log events to capture based on the following values:

- **ERROR**: Events that signal a change requiring human intervention to resolve.
- **WARN**: Events that signal an issue that can be resolved without human intervention.
- **DEBUG**: High-volume events.

Note

There is no default severity level. To capture events, you must set the severity level at either the
account level or Iceberg table level.

For example, to capture DEBUG-level automated refresh events for a specific Iceberg table, use the following command:

Copy code

```
ALTER ICEBERG TABLE <my_table_name> SET LOG_EVENT_LEVEL = DEBUG;
```

For more information, see [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

#### Query your event table for automated refresh events

Before you can query for automated refresh events, you must set up an event table and [set the severity level for event capture](#label-tables-iceberg-set-severity-level-events).

The following example shows how to retrieve Iceberg automated refresh events that are generated during snapshot processing:

Copy code

```
SELECT record_type,
       record:"name" event_name,
       record:"severity_text" log_level,
       resource_attributes:"snow.database.name" database_name,
       resource_attributes:"snow.schema.name" schema_name,
       resource_attributes:"snow.table.name" table_name,
       resource_attributes:"snow.catalog.integration.name" catalog_integration_name,
       record_attributes:"snow.snapshot.id" snapshot_id,
       parse_json(value):metadata_file_location metadata_file_location,
       parse_json(value):snapshot_state snapshot_state
  FROM my_active_event_table
  WHERE record_type='EVENT' AND event_name='iceberg_auto_refresh_snapshot_lifecycle';
```

Output:

```
+-------------+-----------------------------------------+-----------+---------------+-------------+------------+--------------------------+---------------+------------------------+----------------+
| RECORD_TYPE | EVENT_NAME                              | LOG_LEVEL | DATABASE_NAME | SCHEMA_NAME | TABLE_NAME | CATALOG_INTEGRATION_NAME | SNAPSHOT_ID   | METADATA_FILE_LOCATION | SNAPSHOT_STATE |
+-------------+-----------------------------------------+-----------+---------------+-------------+------------+--------------------------+---------------+------------------------+----------------+
| EVENT       | iceberg_auto_refresh_snapshot_lifecycle | DEBUG     | TESTDB        | TESTSH      | TESTTABLE  | glue_integration         | 4281775564368 | metadata.json          | started        |
| EVENT       | iceberg_auto_refresh_snapshot_lifecycle | DEBUG     | TESTDB        | TESTSH      | TESTTABLE  | glue_integration         | 4281775564368 | metadata.json          | completed      |
+-------------+-----------------------------------------+-----------+---------------+-------------+------------+--------------------------+---------------+------------------------+----------------+
```

#### Query your event table for stale automated refresh events

You can query your event table for tables whose last successful refresh is older than a threshold you define.

1. The following example defines a threshold of 20 minutes:

   Copy code

   ```
   SET STALENESS_THRESHOLD_MINUTES = 20;
   ```
2. Query for tables whose last successful refresh is older than the threshold you defined:

   Copy code

   ```
   WITH last_successful_refresh AS (
     -- Find the most recent 'completed' event for each table
     SELECT
    resource_attributes:"snow.table.name"::STRING AS table_name,
    MAX(timestamp) AS last_success_timestamp
     FROM
    <my_active_event_table>
     WHERE
    record:"name" = 'iceberg_auto_refresh_snapshot_lifecycle'
    AND parse_json(value):snapshot_state::STRING = 'completed'
     GROUP BY
    table_name
   )

   -- Select tables whose the last successful refresh was longer ago than our threshold
   SELECT
     table_name,
     last_success_timestamp
   FROM
     last_successful_refresh
   WHERE
     last_success_timestamp < DATEADD(minute, -$STALENESS_THRESHOLD_MINUTES, CURRENT_TIMESTAMP())
   ORDER BY
     last_success_timestamp ASC;
   ```

> - Where `my_active_event_table` is your active event table.
>
> Output:
>
> ```
> +------------+-------------------------+
> | TABLE_NAME | LAST_SUCCESS_TIMESTAMP  |
> +------------+-------------------------+
> | my_table   | 2025-10-10 07:24:30.854 |
> +------------+-------------------------+
> ```

## Error recovery

When an error occurs during the automated refresh process,
Snowflake updates the execution state to one of the following values:

- `STALLED` means that Snowflake is attempting to recover from the error. If recovery succeeds, the automated refresh process
  continues running as expected and the execution state transitions back to the healthy `RUNNING` state.
- `STOPPED` means the automated refresh process encountered an unrecoverable error, and automated refreshes for the table have been
  stopped.

  An unrecoverable error might occur, for example, when Snowflake can’t establish a direct lineage between the target snapshot and the current snapshot.

  To recover from a `STOPPED` state, take the following actions:

  1. [Turn off automated refresh](#label-tables-iceberg-auto-refresh-update) on the table.
  2. Perform a manual metadata refresh. For instructions, see [Refresh the table metadata](/user-guide/tables-iceberg-manage#label-tables-iceberg-refresh-metadata).
  3. Re-enable automated refresh using an [ALTER ICEBERG TABLE … SET AUTO\_REFRESH](/sql-reference/sql/alter-iceberg-table) statement.
  4. Verify that automated refresh is in the `RUNNING` state by calling the [SYSTEM$AUTO\_REFRESH\_STATUS](/sql-reference/functions/system_auto_refresh_status) function.
     You can also call the function multiple times to confirm that the number of queued snapshots (`pendingSnapshotCount`) gradually decreases.

## Billing

Snowflake uses Snowpipe to automate refreshes for Iceberg tables, so charges for automated refresh appear
in the same line item on your bill as Snowpipe charges.
Using [events to monitor automated refresh](#label-tables-iceberg-auto-refresh-events)
also incurs cost. For more information, see [Costs of telemetry data collection](/developer-guide/logging-tracing/logging-tracing-billing).

There are no Snowpipe file charges for this feature.

You can estimate charges incurred by examining the Account Usage [PIPE\_USAGE\_HISTORY view](/sql-reference/account-usage/pipe_usage_history), which displays
the Iceberg table name in the `pipe_name` column.

For Delta-based Iceberg tables, automated refresh pipes display a NULL pipe name.

For more information about Iceberg table charges, see [Iceberg table billing](/user-guide/tables-iceberg#label-tables-iceberg-billing).

## Considerations and limitations

Consider the following when you work with Iceberg tables that use automated refresh:

- For catalog integrations created before Snowflake version 8.22 (or 9.2 for Delta-based tables), you must manually set the `REFRESH_INTERVAL_SECONDS` parameter
  before you enable automated refresh on tables that depend on that catalog integration.
  For instructions, see [ALTER CATALOG INTEGRATION … SET AUTO\_REFRESH](/sql-reference/sql/alter-catalog-integration).
- For [catalog integrations for object storage](/user-guide/tables-iceberg-configure-catalog-integration-object-storage), automated refresh is only supported
  for integrations with `TABLE_FORMAT = DELTA`.
- For tables with frequent updates, using a shorter polling interval (`REFRESH_INTERVAL_SECONDS`) can cause performance degradation.
- Automated refresh synchronizes schema changes alongside [DML](/sql-reference/sql-dml) operations such as INSERT, UPDATE,
  or DELETE. To apply schema changes made through DDL operations alone, perform a [manual refresh](/user-guide/tables-iceberg-manage#label-tables-iceberg-refresh-metadata).
