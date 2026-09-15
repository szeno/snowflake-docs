# Set up data ingestion for your ServiceNow® data

Feature — Generally Available

The Snowflake Connector for ServiceNow® is generally available on supported cloud platforms.

This topic describes how to set up data ingestion for the Snowflake Connector for ServiceNow®.

Note

The Snowflake Connector for ServiceNow® ingests data from ServiceNow® tables into Snowflake. Data ingestion
depends on `v2` of the ServiceNow® [table API](https://developer.servicenow.com/dev.do#!/reference/api/latest/rest/c_TableAPI).

## Strategies for ingesting ServiceNow® tables

Note

- The connector can only ingest tables with `sys_id` columns present.
- [ServiceNow views](https://docs.servicenow.com/bundle/washingtondc-application-development/page/use/reporting/concept/c_DatabaseViews.html) are not supported. Instead of ingesting these views, you should synchronize all tables
  for the underlying view and join the synchronized tables in Snowflake.

The connector uses different ingestion strategies, depending on the table schema. The connector uses three
ingestion modes:

- The initial load of data occurs for each table when the table is enabled for synchronization.

  In this mode, the table is ingested by iterating through the records identified by the IDs in the `sys_id` column. When all records are ingested,
  the initial load phase is complete. For certain tables, you can also set the
  [data range start time](#label-servicenow-connector-configure-tables-range-start-time) value which can restrict which records are ingested.
- Incremental updates occur only for tables with `sys_updated_on` or `sys_created_on` columns.

  Incremental updates begin after the initial load is done and occur on a regular schedule that you can configure.
  In this mode, the connector ingests only the records that were added, updated, or deleted since the last
  synchronization. Information about deletions comes from the journal table provided during connector configuration.
- For tables that don’t have `sys_updated_on` or `sys_created_on` columns, the connector uses the
  truncate and load mode.

  In this mode, the table is always ingested using the initial load approach, and newly ingested data replaces
  the old data. The connector replaces the data by running the `INSERT OVERWRITE` command.

Note

- In the “incremental updates” mode, the connector uses the `sys_updated_on` column, if that column is
  present. If the column is not present, the connector uses the `sys_created_on` column instead.
- For [rotated tables](https://docs.servicenow.com/bundle/washingtondc-platform-administration/page/administer/platform-performance/concept/c_TableRotation.html), the connector always uses the `sys_created_on` column. If the table is rotated using
  a different column than `sys_created_on`, the ingestion of that table might cause performance issues.
- If the `sys_updated_on` or `sys_created_on` fields are not updated when the record is modified
  in ServiceNow, those modifications won’t be propagated to Snowflake, which results in data
  inconsistency. Snowflake recommends that you avoid [disabling the update of system fields](https://developer.servicenow.com/dev.do#!/reference/api/washingtondc/server_legacy/c_GlideRecordAPI%23r_GlideRecord-autoSysFields_Boolean).
- If a record deletion is [not audited](https://developer.servicenow.com/dev.do#!/reference/api/washingtondc/server_legacy/c_GlideRecordAPI#r_GlideRecord-setWorkFlow_Boolean), information about deleted records won’t be propagated to
  Snowflake, resulting in a data inconsistency.

Note

Because of restrictions on the Snowflake and ServiceNow® REST APIs, the connector cannot ingest data
into a table if a single row exceeds 128 MB of data. In that case, the connector tries to ingest data
with the frequency defined in the table schedule. If a row exceeds the limit, the connector
generates an error message and continues ingesting other tables. To overcome this limitation,
you can configure [column filtering](#label-servicenow-connector-column-filtering)
to exclude large columns from ingestion.

### Archived records

The connector does not actively reflect the [records archived in ServiceNow](https://docs.servicenow.com/bundle/washingtondc-platform-administration/page/administer/database-rotation/concept/c_ArchiveData.html) on the Snowflake side for the ingested tables.
Assuming that you archive inactive records older than a certain date, the following apply:

- Any record archived before the connector ingested it (for example, before the initial load of the table) will not be present in the table on the Snowflake side at all.
- Any record archived after it was already ingested by the connector remains on the Snowflake side with no indication of archive action occurring.
- Any archived record restored for a table that is already operating in incremental updates mode will not be ingested on the Snowflake side unless that record is also modified afterwards (with its `sys_updated_on` value being updated to current time).
- An archived record restored during the initial load of the table may be ingested on the Snowflake side depending on its ID in the `sys_id` column.

If you want to bring the table with an active archive rule up to date, you can [reload the entire table](#label-servicenow-connector-reload-table)
but any record archived or restored after the reload is finished will follow the same principles listed above.

ServiceNow archive tables `ar_[table_name]` can be enabled for synchronization. However, the first incremental update
that follows the initial load of such table are searched for records created/updated past the date
the initial load of the archive table has started. Because neither `sys_updated_on` nor `sys_created_on`
are modified when the record is archived, records archived after the initial load of the archive
table up to a certain point in time are missing in it on the Snowflake side. For example, if you archive records older
than a year, then any record archived for a year after the initial load of the archive table is not ingested
to the archive table on the Snowflake side. The archived records that were restored or deleted by a [destroy rule](https://docs.servicenow.com/bundle/washingtondc-platform-administration/page/administer/database-rotation/task/t_CreateADestructionRule.html)
following initial load of an archive table is never removed from it on the Snowflake side.

## Parallel ingestion of ServiceNow® tables

The connector ingests a few tables in parallel, but the ingestion of each individual table is a synchronous
process. This means that ingesting large tables might block the connector from updating other tables. This issue
is more likely to occur during the initial load phase than in other phases.
By default the connector uses 10 worker threads, which is considered an optimal value to not overload the ServiceNow® instance.
If you are sure that your instance can support additional concurrency, you can increase this value to a maximum of 30 by calling
[CONFIGURE\_CONCURRENCY procedure](/connectors/servicenow/managing#label-servicenow-connector-scaling-the-connector-v2).

## Set up data ingestion using Snowsight

To set up data ingestion using Snowsight, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the Snowflake Connector for ServiceNow® app, then select the tile for the connector.
4. In the page for the **Snowflake Connector for ServiceNow®**, select **Data Sync** tab.

   This displays a list of all the ServiceNow® tables.

   Note

   The connector can only ingest tables with `sys_id` columns present.
5. Select the tables you want to ingest:

   1. Search for the table you want to ingest.
   2. Select the checkbox in the **Status** column from the left to the table you want to select.
   3. Under **Sync Schedule**, select how frequently you want to synchronize the table between Snowflake and ServiceNow®.
   4. Repeat these steps for each table you want to ingest into Snowflake.
6. Select the heading of the **Status** column to see the tables you have currently selected.
7. Select **Start sync** to begin ingesting data into your Snowflake account.

The connector status changes to **Syncing data**. When at least one of the tables is ingested successfully, the
connector status changes to **Last Sync: just now**.

Refer to [Monitoring the Snowflake Connector for ServiceNow®](/connectors/servicenow/monitoring) for information on how to view the contents of the tables in Snowflake.

### Modify data ingestion using Snowsight

To modify the ServiceNow® tables to be ingested or the synchronization schedule for the tables, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the Snowflake Connector for ServiceNow® app, then select the tile for the connector.
4. In the page for the **Snowflake Connector for ServiceNow®**, select **Data Sync**.
5. Select **Edit tables** button to enter into the editing mode.
6. Modify the tables you want to ingest:

   1. Search for the table you want to ingest.
   2. Select the checkbox in the **Status** column from the left to the table you want to select or deselect.
   3. Under **Sync Schedule**, select how frequently you want to synchronize the table between Snowflake
      and ServiceNow®.
7. Select **Update data sync**.

## Set up data ingestion using SQL statements

To set up data ingestion using SQL statements, do the following:

- [The schedule for synchronizing the tables](#label-servicenow-connector-configure-schedule).
- [The list of tables that should be synchronized](#label-servicenow-connector-configure-enable-sync-v2).

Note

To configure these settings, you use stored procedures that are defined in the PUBLIC schema of
[the database that serves as an instance of the connector](/connectors/servicenow/installing-sql#label-connector-servicenow-connector-name-v2).

Before calling these stored procedures, select that database as the database to use for the session.

For example, if that database is named `my_connector_servicenow`, run the following command:

Copy code

```
USE DATABASE my_connector_servicenow;
```

### Enable or disable the table synchronization

This section describes how to enable or disable the synchronization of a table in ServiceNow®.
Synchronization enablement can be done with both default and custom configuration.

#### Enable multiple tables using the default configuration

To enable the synchronization of data for at least one table in ServiceNow®, call the `ENABLE_TABLES` stored procedure with the following arguments:

Copy code

```
CALL ENABLE_TABLES(<tables_to_enable>);
```

Where:

`tables_to_enable`
:   Specifies an array of ServiceNow® table names.

    Use the table name, not the label displayed in the ServiceNow® UI. You can find the table name in the
    [data dictionary tables in ServiceNow](https://docs.servicenow.com/bundle/washingtondc-application-development/page/administer/managing-data/concept/c_DataDictionaryTables.html). In the ServiceNow® UI, go to
    **System Definition** » **Tables**. The **Name** column displays the name of the table.

For example, to enable the synchronization of the tables named `table1`, `table2`, and `table3`, run
the following command:

Copy code

```
CALL ENABLE_TABLES(['table1', 'table2', 'table3']);
```

#### Disable multiple tables

To disable table data synchronization for a specific table in ServiceNow®, call the `DISABLE_TABLES`
stored procedure with the following arguments:

Copy code

```
CALL DISABLE_TABLES(<tables_to_disable>);
```

Where:

`tables_to_disable`
:   Specifies an array of ServiceNow® table names.

    Use the table name, not the label displayed in the ServiceNow® UI. You can find the table name in the
    [data dictionary tables in ServiceNow](https://docs.servicenow.com/bundle/washingtondc-application-development/page/administer/managing-data/concept/c_DataDictionaryTables.html). In the ServiceNow® UI, go to
    **System Definition** » **Tables**. The **Name** column displays the name of the table.

For example, to disable the synchronization of the tables named `table1` and `table2`, run the following command:

Copy code

```
CALL DISABLE_TABLES(['table1', 'table2']);
```

Disabling the table stops synchronization gracefully, as soon as it’s possible.
When the table synchronization is re-enabled, ingestion resumes from where it was paused.

Note

Disabling all tables from synchronization does not mean that the Snowflake Connector for ServiceNow® stops incurring cost.
Background tasks, such as those related to notifications, can continue to execute.

The `ENABLE_TABLES` and `DISABLE_TABLES` procedures add the specified table names to the `CONFIGURED_TABLES` view.

Note

The connector does not support [roll backs or delete recoveries](https://docs.servicenow.com/bundle/washingtondc-application-development/page/administer/table-administration/concept/rollback-delete-recovery.html) in ServiceNow®.

Using the roll back and delete recovery features may result in data inconsistency. Records that are recovered in
ServiceNow® may still be marked as deleted in Snowflake. To resolve it you can [reload](#label-servicenow-connector-reload-table)
the table.

#### Enable a single table by using custom configuration

- To enable the synchronization of data with custom configuration for a specific table in ServiceNow®, call the `ENABLE_TABLE` stored procedure with the following arguments:

  Copy code

  ```
  CALL ENABLE_TABLE('<table_to_enable>', <table_config>);
  ```

  Where:

  **`table_to_enable`**

  Specifies a ServiceNow® table name.

  **`table_config`**

  Optional: Specifies an object with table ingestion configuration. If not specified, table ingestion uses the default configuration.

  Currently supported configurations are:

  - [column filtering](#label-servicenow-connector-column-filtering): Provide `include_columns` or `exclude_columns` properties with a list of column names.
  - [row filtering](#label-servicenow-connector-row-filtering): Provide `filter` property with a filter expression.
  - [synchronization schedule](#label-servicenow-connector-configure-schedule): Provide the `schedule` property with custom ingestion schedule.
  - [deletions synchronization enablement](#label-servicenow-connector-sync-deletions): Provide the `sync_deletions` boolean property.
  - [display values fetching](#label-servicenow-connector-display-values): Provide the `fetch_display_values` boolean property.

  Note

  All of the custom configurations can be combined in a single object and used simultaneously for a single table ingestion.

  **Example**:

  The table `sys_audit` has the following configuration:

  - The table should be synchronized every Saturday at 10:00 AM UTC.
  - Only the columns `newvalue` and `reason` should be ingested.
  - Only the rows that have the `newvalue` column starting with the string `privacy` should be ingested.
  - If a journal table is configured, deletions shouldn’t be synchronized.
  - Display values should be fetched for all fields.

  To enable ingestion of the table, run the following command:

  Copy code

  ```
  CALL ENABLE_TABLE('sys_audit', {
    'schedule': { 'type': 'custom', 'value': { 'hour': 10, 'day_of_week': '6' } },
    'include_columns': ['newvalue', 'reason'],
    'row_filter': 'newvalue STARTSWITH "privacy"',
    'sync_deletions': false,
    'fetch_display_values': true
  });
  ```

### Enable a single table by using column filtering

If you don’t need all columns from a ServiceNow® table in Snowflake, the connector can ignore them. For example, skip columns if a single row exceeds the maximum row size of 128 MB.

To enable table ingestion with specified columns, run the following command:

Copy code

```
CALL ENABLE_TABLE('<table_to_enable>', <table_config>);
```

Where:

`table_to_enable`
:   Specifies a ServiceNow® table name.

`table_config`
:   Object including `include_columns` or `exclude_columns` properties with a list of column names.
    If `sys_id`, `sys_created_on`, and `sys_updated_on` exist, they are always included.
    You don’t have to add them to `included_columns` array and cannot exclude them using `excluded_columns` as the connector uses them in the ingestion process.

Note

Since columns in ServiceNow® are written in lowercase and the API that the connector uses is case-sensitive, the values provided for specified columns must also be in lowercase.

Note

You shouldn’t provide both `include_columns` and `exclude_columns`. If you want to list `include_columns`, you should skip the `exclude_columns` property, and vice versa.
If both arrays are not empty and there aren’t any conflicting columns, `include_columns` takes precedence over `exclude_columns`.

If both `include_columns` and `exclude_columns` are empty arrays, all the available columns will be ingested.

For example with a ServiceNow® table named `u_table` with columns `sys_id`, `sys_updated_on`, `col_1` and `col_2` and executing:

Copy code

```
CALL ENABLE_TABLE('u_table', { 'include_columns': ['sys_id', 'sys_updated_on'] });
```

will ingest only `sys_id` and `sys_updated_on` columns for the given table, but calling:

Copy code

```
CALL ENABLE_TABLE('u_table', { 'exclude_columns': ['col_1'] });
```

will ingest `sys_id`, `sys_updated_on` and also `col_2`.

The connector validates the provided columns and rejects the enablement request if any of the columns are not available in ServiceNow®.
ServiceNow® API supports only include mode. As a result the connector transforms provided column arrays into included columns list and sends them with each request to ServiceNow®.
The URL with included columns could possibly be too long to be handled by ServiceNow®. The connector validates this limitation when the `ENABLE_TABLE` is invoked.

Columns configuration for each table can be found in the `INCLUDED_COLUMNS` column of the `CONFIGURED_TABLES` view.
To modify the list of ingested columns, you need to disable the specific table first.
If column filtering is configured for a table, you can enable the table only using the `ENABLE_TABLE` procedure. You cannot use the `ENABLE_TABLES`, which accepts a list of tables as an argument.

Flattened views only include the columns specified when the table was enabled. They are updated every time the list of included columns changes.
If column filtering is not configured, views contain all the available columns.

Note

Configuration change does not affect the previously ingested data. Column filtering applies only to the newly ingested records.
To apply the filter to the previously ingested data, the table needs to be [reloaded](#label-servicenow-connector-reload-table).

### Enable a single table by using row filtering

You can exclude data ingestion for select rows from a ServiceNow® table by specifying a filter condition.
For example, to exclude the rows which include sensitive data that you don’t want in Snowflake,
or exclude the rows which include unnecessary data in order to reduce cost.

To enable table ingestion with specified row filter run the following command:

Copy code

```
CALL ENABLE_TABLE('<table_to_enable>', <table_config>);
```

Where:

`table_to_enable`
:   Specifies a ServiceNow® table name.

`table_config`
:   Object including `row_filter` property with a filter expression, which is a valid string.

    Currently supported filter operators are:

    | Operator | Description | Example |
    | --- | --- | --- |
    | `AND` | Logical operator to join conditions, where both must be fulfilled. | `active = "true" AND impact = "2"` |
    | `OR` | Logical operator to join conditions, where at least one of them must be fulfilled. Important Takes precedence over `AND` operator. See the [examples](#label-servicenow-connector-row-filtering-examples) below. | `tablename = "incident" OR tablename = "problem"` |
    | `=` | Returns `true` if the values are equal. | `priority = "1"` |
    | `!=` | Returns `true` if the values are not equal. | `state != "7"` |
    | `LIKE` | Returns `true` if the value contains the specified character sequence. [1] | `newvalue LIKE "privacy"` |
    | `NOT LIKE` | Returns `true` if the value doesn’t contain a specified character sequence. [1] | `description NOT LIKE "test"` |
    | `STARTSWITH` | Returns `true` if the value starts with the specified character sequence. [1] | `description STARTSWITH "important"` |
    | `ENDSWITH` | Returns `true` if value ends with specified character sequence. [1] | `description ENDSWITH "important"` |
    | `IN` | Returns `true` if the value is equal to any of the list of values. [2] | `tablename IN ("incident", "task", "cmdb_ci")` |
    | `NOT IN` | Returns `true` if the value is not equal to any of the list values. [2] | `status NOT IN ("in progress", "on hold", "cancelled")` |

    Expand

    Show lessSee more

[1] - fields must be of `string` data type.

[2] - choice fields must contain strings.

> Filter expression rules and limitations:
>
> > - Any two filter expressions must be joined with the `AND` or the `OR` operator.
> > - Operators must be separated by space and be in uppercase.
> > - Value expressions must be enclosed in double quotes.
> > - Expressions are case-sensitive.
> > - The expression cannot operate on `sys_id`, `sys_updated_on`, or `sys_created_on` columns.
> > - A value can be an empty string (`""`) to match rows where the field is empty, for example, `u_name = ""`.
> >   Empty values are not allowed inside `IN` or `NOT IN` lists.

Note

Configuration changes do not affect the previously ingested data. Row filtering applies only to the newly ingested records.
To apply the filter to the already ingested data, the table must be [reloaded](#label-servicenow-connector-reload-table).

#### Examples

- To enable ingestion of table `sys_audit`, but synchronize only the rows that are related to the privacy incidents in the `INCIDENT` table, execute:

Copy code

```
CALL ENABLE_TABLE('sys_audit', {
  'row_filter': 'tablename = "incident" AND fieldname = "cause" AND newvalue LIKE "privacy"'
});
```

- To enable ingestion of table `incident`, but synchronize only the rows under such conditions that:

  - `active` field is equal to `true`,
  - `sys_created_by` field starts with `support` or ends with `admin`,
  - `category` field is one of `Network`, `Cloud Management`,

  execute:

Copy code

```
CALL ENABLE_TABLE('incident', {
  'row_filter': 'active = "true" AND sys_created_by STARTSWITH "support" OR sys_created_by ENDSWITH "admin" AND category IN ("Network", "Cloud Management")'
});
```

- To enable ingestion of table `incident`, but ingest only the rows in the specified incident state and only the given columns, execute:

Copy code

```
CALL ENABLE_TABLE('incident', {
  'row_filter': 'incident_state IN ("1", "2", "3")', -- "New", "In Progress", "On Hold"
  'include_columns': ['incident_state', 'description']
});
```

### Specify the synchronization schedule

The Snowflake Connector for ServiceNow® synchronizes data from all ServiceNow® tables to Snowflake on a specified
schedule. By default, all of the tables are synchronized once every hour (1h).

To change the default synchronization schedule for all tables, call the `CONFIGURE_DATA_INGESTION_SCHEDULE` stored procedure
with the following arguments:

Copy code

```
CALL CONFIGURE_DATA_INGESTION_SCHEDULE(<schedule>);
```

Where:

> `schedule`
> :   Specifies the frequency of the synchronization. You can specify one of the following JSON values:
>
>     - `{ 'type': 'continuous' }`, which is near real-time ingestion schedule. A table with this synchronization schedule
>       uses dedicated worker to ingest data and doesn’t count towards the maximum number of tables that can be synchronized in
>       parallel. For more information, see [Scaling the connector](/connectors/servicenow/managing#label-servicenow-connector-scaling-the-connector-v2). You can configure up to
>       20 tables with continuous schedule.
>
>       Warning
>
>       Tables with continuous schedule cause increased load on a ServiceNow® instance. Additionally, it causes the connector
>       warehouse to be constantly utilised, which ramps up warehouse credit consumption. Snowflake recommends using continuous
>       schedules carefully and only for tables that require near real-time data in Snowflake. To prevent overloading of a
>       ServiceNow® instance, the connector implements a detection mechanism that is able to automatically disable
>       failing tables with continuous schedule. See [Table with continuous schedule disabled by the connector](/connectors/servicenow/troubleshooting#label-servicenow-connector-continuous-table-disabled-v2) for more
>       information.
>     - `{ 'type': 'interval', 'value': '<interval_value>' }`, where `interval_value` is one of the following
>       string values:
>
>       - `'30m'`
>       - `'1h'`
>       - `'3h'`
>       - `'6h'`
>       - `'12h'`
>       - `'1d'`
>     - `{ 'type': 'custom', 'value': { 'hour': <hour>, 'day_of_week': '<day_of_week>' } }`, where `hour` specifies the
>       hour in UTC timezone at which the ingestion should start, and `day_of_week` specifies day of the week when the ingestion
>       should be performed. It is possible to use special expressions as a day of week:
>
>       - `'*'` to run the ingestion everyday.
>       - `'1-3'` to run the ingestion from Monday to Wednesday.
>       - `'0,5,6'` to run the ingestion on Friday, Saturday and Sunday.
>
>       Possible values that can be used in the expression for `day_of_week` configuration are:
>
>       - `'0'` - Sunday
>       - `'1'` - Monday
>       - `'2'` - Tuesday
>       - `'3'` - Wednesday
>       - `'4'` - Thursday
>       - `'5'` - Friday
>       - `'6'` - Saturday
>
>       Other non-digit values like `'5L'` indicating the last Friday of a month or `'FRI-SUN'` indicating
>       the range from Friday to Sunday are not supported.

It’s possible to configure ingestion schedule for a specific table during its enablement.
To enable a single table and set its ingestion schedule, call the `ENABLE_TABLE` stored procedure with the following arguments:

Copy code

```
CALL ENABLE_TABLE('<table_name>', <table_config>);
```

Where:

> `table_name`
> :   Specifies a ServiceNow® table name to enable.
>
> `table_config`
> :   Object including `schedule` property, which specifies the configuration of the table synchronization.
>     Check `schedule` of `CONFIGURE_DATA_INGESTION_SCHEDULE` stored procedure for details.

For example to enable ingestion of table `table_1` and synchronize data every 3h call the following stored procedure:

Copy code

```
CALL ENABLE_TABLE('table_1', { 'schedule': { 'type': 'interval', 'value': '3h' } });
```

The connector also allows you to specify a different schedule for each table that is enabled for
synchronization. To change the synchronization schedule for a selected set of tables, call the
`CONFIGURE_TABLES_SCHEDULE` stored procedure with the following arguments:

Copy code

```
CALL CONFIGURE_TABLES_SCHEDULE(<table_names>, <schedule>);
```

Where:

> `table_names`
> :   Specifies an array of table names for which you want to configure the synchronization schedule.
>
> `schedule`
> :   Specifies the frequency of the synchronization. Check `schedule` of `CONFIGURE_DATA_INGESTION_SCHEDULE` stored procedure for details.

For example to ingest tables `table_1` and `table_2` each Saturday and Sunday at 11:00 PM UTC call the following stored
procedure:

Copy code

```
CALL CONFIGURE_TABLES_SCHEDULE(['table_1', 'table_2'], { 'type': 'custom', 'value': { 'hour': 23, 'day_of_week': '0,6' } });
```

By default the connector tries to start the ingestion in 3 hour time window from scheduled start time. If it
is not possible to start the ingestion within that time frame, for example, when the connector is ingesting other
tables, the current scheduled run is not executed. The connector attempts to run the ingestion at the next
scheduled time frame. It is possible to change the duration of the time frame by calling `CONFIGURE_CUSTOM_SCHEDULE_START_INGESTION_WINDOW`
stored procedure:

Copy code

```
CALL CONFIGURE_CUSTOM_SCHEDULE_START_INGESTION_WINDOW(<window_length>);
```

where `window_length` is the window length in ISO 8601 duration format. The duration must be rounded up to
the next whole hour, and must last for at least 1 hour. For example, value `'PT12H'` specifies a window that lasts for
12 hours, and `'P2D'` specifies a window that lasts for 2 days.

If you only enable tables with custom schedules, this configuration only affects time it takes to create and
refresh flattened views for the configured tables. The flattened views are created in the first ingestion cycle after
the following conditions are met:

- Ingestion of metadata tables is finished
- Ingestion of the configured table has started.

If email alerts are enabled, Snowflake recommends changing the alert frequency to **Once per day** when using
custom scheduling.

### Specify whether deletions should be synchronized

You can specify if the connector should synchronize deletions from ServiceNow® to Snowflake. By default, the connector
synchronizes deletions if a journal table is configured. However, you might want to disable deletions synchronization
of a specific table and not change the global configuration.

To enable table ingestion with specified deletions synchronization setting, run the following command:

Copy code

```
CALL ENABLE_TABLE('<table_to_enable>', <table_config>);
```

Where:

`table_to_enable`
:   Specifies a ServiceNow® table name.

`table_config`
:   Object including `sync_deletions` boolean property. If the value is set to `true`, the connector synchronizes deletions for the table;
    if the value is set to `false`, the connector does not synchronize deletions for the table.

For example, to enable ingestion of the table `incident` but not synchronize the deletions, run the following command:

Copy code

```
CALL ENABLE_TABLE('incident', { 'sync_deletions': false });
```

Note

If you want to use the default configuration, don’t provide the `sync_deletions` property in the configuration object.
If the journal table is not configured, the connector does not synchronize deletions regardless of the provided configuration.

### Specify whether display values should be fetched

The connector can fetch display values for any supported types of fields in ServiceNow®.
Display values are readable values that correspond to the actual values stored in the database, for example, a field with a value of `1` might have a display value of `High`.
To learn more about display values, see [the ServiceNow® documentation](https://www.servicenow.com/docs/bundle/xanadu-platform-administration/page/administer/field-administration/concept/c_DisplayValues.html).

The resolved value is displayed in a flattened view in a separate column with the suffix `__DISPLAY_VALUE`.
The connector creates text and boolean columns with the Snowflake types, however for other types, for example,
different possible formats of number or date values, the display values are stored as variants.

Warning

Metadata tables are not supported for display values fetching.

Note

Configuration changes do not affect the previously ingested data. Display values fetching applies only to the newly ingested records.
To fetch display values for the already ingested data, the table must be [reloaded](#label-servicenow-connector-reload-table).

#### Display values fetching per table

To enable fetching display values for a specific table, call the `ENABLE_TABLE` stored procedure with the following arguments:

Copy code

```
CALL ENABLE_TABLE('<table_to_enable>', <table_config>);
```

Where:

`table_to_enable`
:   Specifies a ServiceNow® table name.

`table_config`
:   Object including `fetch_display_values` boolean property. If the value is set to `true`, the connector fetches display values for the table;
    if the value is set to `false` (default), the connector does not fetch display values for the table.

For example, to enable ingestion of the table `incident` and fetch display values for it, run the following command:

Copy code

```
CALL ENABLE_TABLE('incident', { 'fetch_display_values': true });
```

Note

Per table configuration is not affected by the global configuration.

#### Configure default display values fetching setting for all tables

To enable fetching display values for all tables, call the `CONFIGURE_DISPLAY_VALUE_FETCHING` stored procedure with the following arguments:

Copy code

```
CALL CONFIGURE_DISPLAY_VALUE_FETCHING(<fetch_display_values>);
```

Where:

`fetch_display_values`
:   Specifies a boolean value. If the value is set to `true`, the connector fetches display values for all tables;
    if the value is set to `false` (default), the connector does not fetch display values for any table by default.

For example, to enable fetching display values for all tables, run the following command:

Copy code

```
CALL CONFIGURE_DISPLAY_VALUE_FETCHING(true);
```

### Specify the data range start time

By default, the Snowflake Connector for ServiceNow® synchronizes all the records in the corresponding ServiceNow® tables. For the tables with: `sys_updated_on` or `sys_created_on`
columns (from now on here called *time columns*) present, it is possible to restrict the range of synchronized
data by setting a *data range start time* - i.e. lower bound for the corresponding *time column* value of the records.

With such a configuration, records with the corresponding *time column* value older than the *data range start timestamp* are **not** ingested.
The corresponding *time column* used by this procedure is determined in [the same way](#label-servicenow-connector-incremental-updates-column-choice-v2) as for the incremental updates .

To change the *data range start time* value, call the `CONFIGURE_TABLES_RANGE_START` stored procedure with the following arguments:

> Copy code
>
> ```
> CALL CONFIGURE_TABLES_RANGE_START(<table_names>, <range_start>);
> ```

Where:

> `table_names`
> :   Specifies an array of table names for which you want to configure the *data range start time*.
>
> `range_start`
> :   Timestamp specifying the *data range start time* in TIMESTAMP\_TZ format or NULL to unset the current value.

Note

You cannot set the data range start time for the tables with neither `sys_updated_on` nor `sys_created_on` column present.

- If the ingestion of the table has not been started yet, the *data range start time* value is taken into account with the first ingestion.
- If the ingestion of the table has already been started (e.g. a reload is in progress), the *data range start time* value is ignored
  and (another) [reload of the table(s)](#label-servicenow-connector-reload-table)
  is required to filter out the records with too old corresponding *time column* value.

It is therefore recommended to set the *data range start time* before starting the first ingestion of a table (hence also before enabling it).

For example, if tables `table1` and `table2` have the required *time column(s)*, in order to set the *data range start time* to 2022-11-23 07:00:00 UTC for theses two tables,
run the following command:

> Copy code
>
> ```
> CALL CONFIGURE_TABLES_RANGE_START(['table1', 'table2'], TO_TIMESTAMP_TZ('2022-11-23 07:00:00 +00:00'));
> ```

Then:

- for table `table1`, for example, if its ingestion has not started yet, all records with a corresponding *time column* value before 2022-11-23 07:00:00 are **not** ingested.
- for table `table2`, for example, if its ingestion has already started, the *data range time start* value is ignored in all data synchronizations until reloading this table.
  During the reload, all records with a corresponding *time column* value before 2022-11-23 07:00:00 are not ingested.

It is also possible to unset the *data range start time*. For example, in order to unset it for table `table1`, run the following command:

> Copy code
>
> ```
> CALL CONFIGURE_TABLES_RANGE_START(['table1'], NULL);
> ```

Again, if an ingestion of table `table1` has already been started, reloading this table is required to ingest all the records back from ServiceNow®.

Note

Loading data with the *data range start time* may take longer than loading all historical data because of lower performance of incremental updates.

## Reload data in a table

The connector allows you to reload data in a table. It’s useful when you want to apply the changes in the configuration to the
already ingested data or when you want to make sure that the data is up to date with the source.

There are two types of reloads, full for complete data replacement and filtered for affecting only part of the data by
specifying conditions for the reload.

> Note
>
> Every reload takes the current reloaded table configuration into account. For example, this can restrict which records are ingested.
>
> To see the configuration of the main table, check the `CONFIGURED_TABLES` view.
>
> To see the result configuration of the reloaded table, check the `RELOADED_TABLES` view.

### Full reload

To reload data in particular table, call the `RELOAD_TABLE` stored procedure:

Copy code

```
CALL RELOAD_TABLE('<table_name>');
```

Where:

`table_name`
:   Specifies the name of the table to reload.

When you call the `RELOAD_TABLE` stored procedure, the connector performs the following:

1. The connector suspends the original table for ingestion temporarily.

   Note

   While the table is being reloaded, you cannot re-enable the table for ingestion.
2. The connector creates a separate temporary table for ingestion.
3. The connector ingests the data into this new temporary table. This table is visible in
   the [CONNECTOR\_STATS](/connectors/servicenow/monitoring#label-monitoring-the-servicenow-connector-v2) view as a table named with a
   `__tmp` suffix).
4. After the data is ingested, the connector replaces the data in the original table with the data in the
   temporary table.
5. The connector deletes the temporary table.
6. The connector re-enables the original table for ingestion.

During this process, you can continue to query the existing data in the original table. However,
changes to the data in the ServiceNow® table won’t be reflected in the Snowflake table
until the ingestion process completes.

### Filtered reload

To reload only part of data in particular table, call the `RELOAD_TABLE` stored procedure with a configuration object parameter:

Copy code

```
CALL RELOAD_TABLE('<table_name>', <config>);
```

Where:

`table_name`
:   Specifies the name of the table to reload.

`config`
:   Specifies the configuration of the reload. The configuration object can include the following properties:

    - `sys_ids`: An array of ServiceNow® record identifiers (`sys_id`) to be reloaded.
    - `data_reload_range_start_time` and `data_reload_range_end_time`: Timestamp values specifying the data range in TIMESTAMP\_TZ format.
      Depending on the given table ingestion type, only records with `sys_updated_on` or `sys_created_on` within the specified time frame are reloaded.
    - `conditions`: A string expression that specifies the conditions on the fields in a ServiceNow® table.
      Only the records that meet the conditions are reloaded.

      The syntax of the expression is the same as for the [row filtering](#label-servicenow-connector-row-filtering).
      If row filtering is configured on the regular table, it is applied to the conditions as well.

In contrast to the full reload, the filtered reload does not replace the data in the original table, but only changes the selected records.

Tip

Right after enabling a large table for ingestion for the first time, you can quickly ingest a small subset of records
that you are interested in without waiting for the initial load to complete using filtered reload.

Note

`data_reload_range_start_time` and `data_reload_range_end_time` time ranges and `conditions` filter
can be used simultaneously. The records that meet both conditions are reloaded.

`sys_ids` is exclusive with other configuration properties.

For example, to reload only the records with the `sys_id` values of `1`, `2`, and `3` in the table `incident`, run the following command:

Copy code

```
CALL RELOAD_TABLE('incident', { 'sys_ids': ['1', '2', '3'] });
```

To reload only the records with the `sys_updated_on` values between 2022-11-23 07:00:00 and 2022-11-23 08:00:00 UTC,
and are still active in the table `incident`, run the following command:

Copy code

```
CALL RELOAD_TABLE('incident', {
  'data_reload_range_start_time': TO_TIMESTAMP_TZ('2022-11-23 07:00:00 +00:00'),
  'data_reload_range_end_time': TO_TIMESTAMP_TZ('2022-11-23 08:00:00 +00:00'),
  'conditions': 'active = "true"'
});
```

### Cancel table reload

To cancel the process of reloading the data in a table, use the `CANCEL_RELOAD_TABLE` stored procedure as
shown in the following example:

Copy code

```
CALL CANCEL_RELOAD_TABLE('<table_name>');
```

Where:

`table_name`
:   Specifies the name of the table whose reload you want to cancel.

When you cancel the reload, the connector drops all temporary objects created during the reload. The table is
then available for ingestion as part of the normal synchronization schedule.

## Configure the use of read replicas

To configure the connector to use read replicas in your ServiceNow® environment, you can set up a custom query category.
This configuration allows the connector to direct API requests to read replicas instead of the primary instance, which
can help distribute load and improve performance.

To configure a custom query category for read replica usage, call the `CONFIGURE_QUERY_CATEGORY` stored procedure with
the following argument:

Copy code

```
CALL CONFIGURE_QUERY_CATEGORY('<query_category>');
```

Where:

`query_category`
:   Specifies the query category identifier that will be added to ServiceNow® API requests.

When configured, the connector will add the `sysparm_query_category=<query_category>` parameter to all ServiceNow® API requests, allowing ServiceNow® to route these requests to the appropriate read replicas based on your instance configuration.

Default query category value set during connector installation is `list`.

For example, to configure the connector to use a query category named `connector_replica`, run the following command:

Copy code

```
CALL CONFIGURE_QUERY_CATEGORY('connector_replica');
```

## Configure the event log scan during incremental ingestion

During [incremental updates](#label-servicenow-connector-incremental-updates-column-choice-v2), the connector
classifies each fetched row as an `INSERT` or an `UPDATE`. To do this, it probes the internal `__EVENT_LOG`
table with an `EXISTS` subquery for every batch of rows. The connector records this classification as the
`event_type` of each change in the `__EVENT_LOG` table, so that you can distinguish inserts from updates when you
audit a table’s change history using the [event logs](/connectors/servicenow/accessing-data#label-servicenow-connector-accessing-data-event-logs-v2). This classification is not used when the connector merges changes into the
destination table, because the merge only distinguishes the `DELETE` and `FILTERED` events. On accounts with
large `__EVENT_LOG` tables, the probe forces a full scan of the unclustered `__EVENT_LOG` table for every batch,
which can read tens of terabytes of data per day.

If you do not need the exact event type for each row (for example, if you do not use the event log for auditing),
you can disable this probe by calling:

Copy code

```
CALL CONFIGURE_SCAN_EVENT_LOG_IN_INCREMENTAL(false);
```

## Configure the size of a single page fetch for a table

The connector fetches data from a table by dividing it into smaller chunks called pages.
Each API request to ServiceNow® fetches one page.

To account for this, the connector limits the number of rows fetched within a single API request. This limit is the page size.

The connector uses the following process to determine the page size:

1. Initially, the default page size is set to 10,000 rows.
2. If the fetch request fails during ingestion because the response size is exceeded, the page size is
   gradually decreased by 1000, 100, 10 and 1 until the request succeeds or the final page size
   is set to 1.
3. The successful page size is saved in the connector state and this value is used by subsequent requests.

The current page size for a table is available in the `TABLES_STATE` view. To see the page size, run
the following command:

Copy code

```
SELECT PAGE_SIZE FROM TABLES_STATE WHERE TABLE_NAME = '<table_name>';
```

Where:

`table_name`
:   Specifies the name of the ServiceNow® table being ingested.

The process the connector uses for determining the page size may lead to inefficiencies. This process only
reduces the page size. It does not increase the page size. This can happen in situations where a table has a
single large row that causes the page size to be set to a lower value.

To avoid this situation, you can manually set the page size by calling the `RESET_PAGE_SIZE` stored
procedure as shown in the following examples:

Copy code

```
CALL RESET_PAGE_SIZE('<table_name>');
```

or

Copy code

```
CALL RESET_PAGE_SIZE('<table_name>', <page_size>);
```

Where:

`table_name`
:   Specifies the name of the ServiceNow® table being ingested.

`page_size`
:   (Optional) Specifies the number of rows to fetch in a single page. If not provided, the default value provided in the connector configuration is used. The default and recommended value is 10000. The minimum value is 1 and the maximum value is 25000.

Note

The page size can be also set for a configured journal table, usually `sys_audit_delete`. If failures occur
during the deletions ingestion from an underperforming journal table, you can lower the page size to avoid further failures.

Note that the journal table does not need to be explicitly enabled for ingestion to make the connector synchronize deleted rows.

## Ingestion run

Ingestion runs for a given table are triggered according to the configured schedule.
A run downloads all the relevant rows divided into pages mentioned in the previous paragraph from the source table in a loop.

**Initial load and updates**

As soon as a page of data is fetched, it is inserted into the corresponding event log table.
At this stage the newly fetched changes are not yet available in the sync table or through flattened views.
When it is done the next request with updated criteria is issued as long as any data is returned.
When the ingestion run is complete, and there is no more data to fetch in the source table, an asynchronous merge task is triggered,
that takes all the changes from the event log inserted since the last merge and applies them to the sync table.
When it is complete, the data becomes available in sync table and flattened views.

**Truncate and load**

In truncate and load mode a temporary table is created for each ingestion run.
Each fetched page of rows is first inserted into this temporary table (this table exists in the internal connector schema and is not available to connector users).
At this stage the newly fetched changes are not yet available in the sync table or through flattened views, they still show data fetched in the previous run.
When the ingestion run is completed, and there is no more data available in the source table, data from the temporary table replaces existing data in the sync table.
All the fetched rows are also added to the event log.
At the end the temporary table is dropped.

**Monitoring progress**

To check the status of a current or past ingestion run, you can query the `CONNECTOR_STATS` view. It’s visible in the `STATUS` column.
It’s set to `DONE` only if data was successfully fetched and all the changes were applied to the sync table.
When the ingestion is running or the merge to the sync table/replace of rows in the sync table has not been completed yet, the status is `RUNNING`.

## Next steps

After configuring ingestion, perform the steps described in [Access the ServiceNow® data in Snowflake](/connectors/servicenow/accessing-data) to view and otherwise access ServiceNow® data.
