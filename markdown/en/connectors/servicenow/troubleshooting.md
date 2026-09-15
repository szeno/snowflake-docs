# Troubleshooting the connector

Feature — Generally Available

The Snowflake Connector for ServiceNow® is generally available on supported cloud platforms.

This topic provides guidelines for troubleshooting issues with the Snowflake Connector for ServiceNow®.

Note

The following sections describe stored procedures that are defined in the PUBLIC schema of
[the connector application](/connectors/servicenow/installing-sql#label-connector-servicenow-connector-name-v2). Before
calling these stored procedures, select that application as the database to use for the session.

For example, if that application is named `my_connector_servicenow` and you would call the `TEST_CONNECTION`
connector procedure by running the following commands:

Copy code

```
USE APPLICATION my_connector_servicenow;
CALL TEST_CONNECTION();
```

## Resolving problems during connector installation

Most common issues during the installation of the connector are related to the ACLs set on the metadata tables such as
`sys_db_object`, `sys_dictionary` and `sys_glide_object`. Additionally, the connector requires access to the
`sys_table_rotation` table to determine the correct ingestion strategy and optionally to the journal table (usually
`sys_audit_delete`) to propagate data deletion.

### Authentication step errors

Issues can occur when [connecting to ServiceNow](/connectors/servicenow/installing-snowsight#label-connector-servicenow-authentication) in the installation wizard or
running manually the [SET\_CONNECTION\_CONFIGURATION](/connectors/servicenow/installing-sql#label-connector-servicenow-install-configure-connection-v2) procedure.
If encountered errors during this step, please make sure that the user used to install the connector has access to the `sys_db_object` table.

The error status codes that might be related to ACL issues in the returned JSON object from the `SET_CONNECTION_CONFIGURATION` procedure are as follows:

- `REQUEST_FAILED`

You can perform below query similar to the connector’s to verify the access. Until the request doesn’t return the expected result,
it won’t be possible to install the connector. For example, if you are using curl to send the HTTP request:

Copy code

```
# checking access to the sys_db_object table
curl -u '<username>:<password>' "https://<servicenow_instance>.service-now.com/api/now/table/sys_db_object?sysparm_limit=1"
```

Where:
:   `servicenow_instance`
    :   Specifies the name of your ServiceNow® instance.

    `username` and `password`
    :   Specify the credentials for your ServiceNow® instance.

Example responses:

- At least some of the fields are returned - the user has the necessary permissions to access the table.
- The response is empty - the user has the permission to access the table, but not to the processed record. It might cause
  issues at a later point.
- The response contains an error - the user does not have the necessary permissions to access the table.

### Validate source step errors

Issues might occur when [validating source](/connectors/servicenow/installing-snowsight#label-connector-servicenow-validate-source) in the installation wizard or
running manually the [FINALIZE\_CONNECTOR\_CONFIGURATION](/connectors/servicenow/installing-sql#label-connector-servicenow-install-finalize-configuration-v2) procedure.
If encountered errors during this step, please make sure that the user used to install the connector has the necessary permissions to access the metadata tables.

The error status codes that might be related to ACL issues in the returned JSON object from the `FINALIZE_CONNECTOR_CONFIGURATION` procedure are as follows:

- `METADATA_TABLE_ACCESS_VALIDATION_ERROR`
- `JOURNAL_TABLE_ACCESS_VALIDATION_ERROR`

You can perform below queries similar to the connector’s to verify the access. Until the requests don’t return the expected results,
it won’t be possible to install the connector. For example, if you are using curl to send the HTTP request:

Copy code

```
# checking access to the sys_db_object table
# expected fields in the result object: sys_id, super_class, name
curl -u '<username>:<password>' "https://<servicenow_instance>.service-now.com/api/now/table/sys_db_object?sysparm_fields=sys_id,super_class,name&sysparm_limit=1&sysparm_query=name=sys_db_object"

# checking access to the sys_dictionary table
# expected fields in the result object: sys_id, name, element, internal_type
curl -u '<username>:<password>' "https://<servicenow_instance>.service-now.com/api/now/table/sys_dictionary?sysparm_fields=sys_id,name,element,internal_type&sysparm_limit=1&sysparm_query=name=sys_dictionary"

# checking access to the sys_glide_object table
# expected fields in the result object: sys_id, name, scalar_type
curl -u '<username>:<password>' "https://<servicenow_instance>.service-now.com/api/now/table/sys_glide_object?sysparm_fields=sys_id,name,scalar_type&sysparm_limit=1&sysparm_query=name=datetime"

# checking access to the sys_table_rotation table
# expected fields in the result object: sys_id, name
curl -u '<username>:<password>' "https://<servicenow_instance>.service-now.com/api/now/table/sys_table_rotation?sysparm_fields=sys_id,name&sysparm_limit=1&sysparm_query=name=syslog"

# (optional) - check only if deletions auditing is going to be used
# checking access to the journal table
# if known, "&sysparm_query=tablename=<table_name>" or "&sysparm_query=documentkey=<sys_id>" can be appended to the request
# expected fields in the result object: sys_id, sys_created_on, documentkey, tablename
curl -u '<username>:<password>' "https://<servicenow_instance>.service-now.com/api/now/table/<journal_table>?sysparm_fields=sys_id,sys_created_on,documentkey,tablename&sysparm_limit=1"
```

Where:
:   `servicenow_instance`
    :   Specifies the name of your ServiceNow® instance.

    `username` and `password`
    :   Specify the credentials for your ServiceNow® instance.

    `journal_table`
    :   Specifies the name of your ServiceNow® table used for deletions audit. Usually this has value of `sys_audit_delete`.

Example responses:

- All of the expected fields are present in the response - the user has the necessary permissions.
- Some of the expected fields are missing - the user does not have the necessary permissions to all of the columns.
- The response is empty - the user does not have the necessary permissions to all of the rows.
- The response contains an error - the user does not have the necessary permissions to the table.

## Verifying the connection to the ServiceNow® instance

To verify that the Snowflake Connector for ServiceNow® can access the ServiceNow® instance, call the
`TEST_CONNECTION` stored procedure:

Copy code

```
CALL TEST_CONNECTION();
```

If the connector is set up correctly, the stored procedure returns the following response:

Copy code

```
{
  "responseCode": "OK",
  "message": "Test request to ServiceNow succeeded."
}
```

## Verifying access to the specific table in the ServiceNow® instance

To verify that the Snowflake Connector for ServiceNow® can acces data from the specific table in the ServiceNow® instance, call the
`TEST_TABLE_ACCESS` stored procedure:

Copy code

```
CALL TEST_TABLE_ACCESS('<table_name>');
```

Where:

`table_name`
:   Specifies the name of a table in the ServiceNow® instance.

If the connector is set up correctly and data is available to the user used by the connector, the stored procedure returns the following response:

Copy code

```
{
  "responseCode": "OK",
  "message": "Test request to ServiceNow® succeeded."
}
```

Note

If table is empty or all the rows are hidden from the connector because of ACLs, the message will say:
`Test request to ServiceNow® succeeded but it didn't return any record.`
In this situation, make sure that the table is really empty. If any rows are visible from the UI, it means that the connector is not able to ingest them.

## Comparing table row counts in ServiceNow® and Snowflake

To compare the current row count for a table in both ServiceNow® and Snowflake, call the `CHECK_ROW_COUNT` procedure:

Copy code

```
CALL CHECK_ROW_COUNT('<table_name>');
```

or

Copy code

```
CALL CHECK_ROW_COUNT('<table_name>', <max_sys_created_on>);
```

Where:

`table_name`
:   Specifies the name of a table in the ServiceNow® instance.

`max_sys_created_on`
:   Specifies additional optional filter on maximal value of `sys_created_on` column. Only rows matching this filter
    will be counted. Default value of this parameter is `NULL` which means the filter won’t be applied. This parameter
    helps to compare only counts of records already ingested to Snowflake, without taking into account records recently
    created in ServiceNow® but not yet ingested into Snowflake.

The following example shows how to call `CHECK_ROW_COUNT` stored procedure with `max_sys_created_on` parameter:

Copy code

```
CALL CHECK_ROW_COUNT('sys_db_object', '2021-09-10 12:34:56');
```

If the procedure times out, the procedure was unable to use the `stats` API
to determine the row count of the table in ServiceNow®. This may mean that the number of
rows in this table is too large to be counted by this API.

Note

The number of rows returned may vary. A ServiceNow® table may contain more rows that the equivalent Snowflake
table. This may be caused by the access control list rules (ACLs) set for a given table in ServiceNow®.

The connector uses different endpoints for retrieving information about the number of rows in a ServiceNow®
table. The connector uses `stats` for information about a table, including the number of rows. It uses
`table` to ingest data into Snowflake.

## Checking the status of the ingestion of a row

To check the status of the ingestion of a row in all possible places in ServiceNow® and Snowflake, call the `CHECK_RECORD_HISTORY` procedure:

Copy code

```
CALL CHECK_RECORD_HISTORY('<table_name>', '<sys_id>');
```

Where:

`table_name`
:   Specifies the name of a table in the ServiceNow® instance.

`sys_id`
:   Specifies the `sys_id` of the row to check.

The procedure returns a JSON object containing the following properties:

| Property | Description |
| --- | --- |
| `table_name` | Name of the table. |
| `sys_id` | Unique identifier for the row in ServiceNow®. |
| `status` | Status of the ingestion of the row. |
| `is_present_in_servicenow` | `true` if the row is present in the table in ServiceNow®; `false` otherwise. |
| `is_present_in_servicenow_audit_table` | `true` if the row is tracked in the audit table in ServiceNow®; `false` otherwise. |
| `is_present_in_snowflake_destination_table` | `true` if the row has already been ingested and is available in the `dest_db` database in Snowflake; `false` otherwise. |
| `event_log_records` | Array of JSON objects that represent [entries in the event log](/connectors/servicenow/accessing-data#label-servicenow-connector-accessing-data-event-logs-v2) for the row with this `sys_id`.  Each object contains the following properties, which correspond to the columns in the event log table that specify the timestamps and event types of the data change:   - `sys_updated_on` - `event_date` - `event_type` |

Expand

Show lessSee more

## Determining if a table is audited for deletion

The Snowflake Connector for ServiceNow® relies on auditing to propagate the deletion of records to Snowflake.

To verify that a given table in ServiceNow® is configured to audit the deletion of records, call the `CHECK_IF_AUDIT_ENABLED` stored procedure:

Copy code

```
CALL CHECK_IF_AUDIT_ENABLED('<table_name>');
```

Where:

`table_name`
:   Specifies the name of a table in the ServiceNow® instance.

The procedure returns a JSON object containing the following properties:

| Property | Description |
| --- | --- |
| `response_code` | `OK` value if the procedure succeeded or a code of the error in case of a failure. |
| `audit` | Value of the `audit` attribute for the checked table. If set to true then audit is enabled on the table. |
| `no_audit_delete` | Value of the `no_audit_delete` attribute for the checked table. If it’s set, then it overrides value from the `audit` field for delete events. |
| `summary` | Human-readable explanation at to whether audit is enabled on the table based on values of `audit` and `no_audit_delete` fields. Audit is enabled on the table when either:   - `audit` field is set to true and `no_audit_delete` isn’t set to true. - `no_audit_delete` is set to false. |

Expand

Show lessSee more

### Obtaining troubleshooting data

To obtain troubleshooting data, call the `GET_TROUBLESHOOTING_DATA` stored procedure:

Copy code

```
CALL GET_TROUBLESHOOTING_DATA(<from_timestamp>, <to_timestamp>);
```

Where:

`from_timestamp`
:   Specifies the start of dates range (in UTC timezone) for which data should be fetched.

`to_timestamp`
:   Specifies the end of dates range (in UTC timezone) for which data should be fetched.

This stored procedure returns the following data in tabular format:

- Configuration information
- Errors experienced by connector
- Ingestion history

The following example shows how to call this stored procedure:

Copy code

```
CALL GET_TROUBLESHOOTING_DATA('2024-02-05 10:00:00', '2024-02-10 22:30:00');
```

You can save the returned data in CSV format to send to [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Recovering an inaccessible object

The connector requires multiple database objects that are external to the connector application. If these objects are unavailable, the connector will fail or stop working correctly. Situations where objects can become unavailable
include:

- Dropping an object.
- Recreating an object without keeping or restoring the required grants.
- Revoking the grants necessary for the connector to use these objects.

In most cases you can restore these objects manually by recreating them and granting the necessary privileges. The
following sections describe how to restore different objects.

### Restoring the connector warehouse

If the connector loses access to its warehouse, configure a new one by calling the
[UPDATE\_WAREHOUSE](/connectors/servicenow/managing#label-servicenow-connector-update-warehouse-v2) stored procedure.

### Restoring the database and schema for the ServiceNow® data

If the [database or schema for the ServiceNow® data](/connectors/servicenow/installing-sql#label-servicenow-connector-prereqs-dest-schema-v2) is
dropped, the only way to recover is by running the
[UNDROP <object>](/sql-reference/sql/undrop) command. If this command is unavailable, you
must reinstall the connector and ingest the ServiceNow® data again.

If a [view containing the ServiceNow® data](/connectors/servicenow/accessing-data#label-servicenow-connector-accessing-data-flattened-v2) is dropped,
it should be recreated automatically the next time the background task responsible for creating them runs.

If one of the tables containing the ServiceNow® data (either the [event logs](/connectors/servicenow/accessing-data#label-servicenow-connector-accessing-data-event-logs-v2)
or [raw data](/connectors/servicenow/accessing-data#label-servicenow-connector-accessing-data-raw-v2) tables) is dropped and you cannot use the
[UNDROP TABLE](/sql-reference/sql/undrop-table) command to recover it, do the following to start the ingestion of the ServiceNow® table again:

- Ensure both event logs and raw data tables for this ServiceNow® table are dropped.
- [Disable the ServiceNow® table](/connectors/servicenow/ingestion#label-servicenow-connector-configure-enable-sync-v2).
- Use the [DELETE\_TABLE procedure](/connectors/servicenow/managing#label-servicenow-connector-deleting-tables-v2).
- [Enable the ServiceNow® table](/connectors/servicenow/ingestion#label-servicenow-connector-configure-enable-sync-v2).

### Restoring the notification integration for the connector

If the connector loses access to the notification integration object, do the procedures for
[configuring alerts](/connectors/servicenow/monitoring#label-monitoring-the-servicenow-connector-email-alerts-enabling-v2) again, recreating the
notification integration object if necessary.

If email notifications are configured via Snowsight then you can just disable and re-enable them to restore
the necessary external objects.

## Error when ingesting data from table. Request to ServiceNow® failed after 2 attempts.

The error occurs because of table ingestion failure. You can check for it in the `CONNECTOR_ERRORS` view. The error message
can include the following sentences:

- Error when ingesting data from table
- Minimal page size of 1 was reached
- Request to ServiceNow® failed after 2 attempts
- Request to ServiceNow® timed out

The error means that the connector tried to perform requests to ServiceNow® API. ServiceNow® API couldn’t correctly
respond to any of these requests. This usually indicates performance problem with the API. There are several possible
solutions to this issue:

- Increase API timeout on the ServiceNow® side:

  1. Log in to the ServiceNow® instance.
  2. Navigate to **Transaction Quota Rules** panel.
  3. Find and open the **REST Table API request timeout** rule.
  4. Increase the value of **Maximum Duration (seconds)**. The maximum duration the connector can handle is 120 seconds. Higher duration values aren’t supported and will result in timeouts on the connector side.
- Ensure that there are no unnecessary ACLs on the table. The ACLs heavily impact performance of the API. Ideally, the connector user shouldn’t have any ACLs set on the table. If there is a need to omit some rows from the ingested table, consider using [row filtering](/connectors/servicenow/ingestion#label-servicenow-connector-row-filtering).
- In the ServiceNow® table, create a composite index on either sys\_updated\_on and sys\_id columns or sys\_created\_on and sys\_id columns, if the sys\_updated\_on column isn’t present.
- Investigate ServiceNow® logs to find out why the API was slow to respond. A good starting point is the Transaction Log in ServiceNow®. To see connector requests:

  1. Log in to the ServiceNow® instance.
  2. Navigate to **System Logs > Transactions (all user)** panel.
  3. Filter the table by **Created by** column set to connector user, and **URL** column containing ingested table name.
  4. Check **Response time** column for unusually high response time, more than REST Table API request timeout set in the previous step.
  5. Investigate further suspicious transactions for potential bottlenecks.

## Determining the reason for missing columns in flattened views

The connector creates flattened views in the destination schema based on the ServiceNow® metadata.
There are several reasons why a column can be missing on the Snowflake side.

### Checking if column metadata is present in Snowflake

To check if column metadata is present in the `sys_dictionary` table on Snowflake, execute the following query:

Copy code

```
SELECT * FROM <dest_db>.<dest_schema>.sys_dictionary__view WHERE name = '<table_name>' AND element = '<column_name>';
```

If the table you’re investigating has parent tables (inherited from another table in ServiceNow®)
and the column you are looking for was added to the parent table, you should use the parent table name instead.

To list all the tables from which the table you’re interested in inherits, please use the following query:

Copy code

```
SELECT
    sys_id,
    name,
    PARSE_JSON(super_class):value::string AS super_class_sys_id
FROM <dest_db>.<dest_schema>.sys_db_object__view
START WITH name = '<table_name>'
CONNECT BY sys_id = PRIOR super_class_sys_id;
```

If rows are returned, metadata for the column was correctly ingested into Snowflake but the view has not yet been refreshed.
Check the status and if:

- the view was refreshed recently but the column is still not present, please contact support.
- the view was not refreshed yet, wait for the next ingestion schedule.

If an empty result is returned, it means that the connector didn’t ingest metadata for this column yet.
You need to validate on the ServiceNow® side if the record is visible to the connector and has correct timestamp.

### View refresh status

To validate when the views for a given table were last refreshed and if the operation was successful, execute the following query:

Copy code

```
SELECT flattened_views_status, flattened_views_last_updated FROM tables_state WHERE table_name = '<table_name>';
```

If the last refresh failed, you may want to query event table and look for errors reported by the connector.

### View ServiceNow® column metadata availability

It’s possible, that the reason for missing columns in the flattened view is that column metadata cannot be ingested by the connector.
This may be caused by ACLs preventing the row in the `sys_dictionary` table from being returned by the Table API.
Another possible reason is a past timestamp value in the `sys_updated_on` column.
It can also be the case that the column/table definition was imported from a different ServiceNow® instance.
To determine if the connector can access column metadata execute GET request to the following endpoint:

Copy code

```
https://<servicenow_instance>.service-now.com/api/now/table/sys_dictionary?sysparm_query=name=<table_name>^element=<column_name>
```

If an empty result is returned the connector cannot access the column. The column may be protected by an ACL or not present.

If a column definition was returned, examine the value of the `sys_updated_on` field.
Confirm the date matches the expected time when the column was added to the table.
If it was imported from another instance it may show the point in time when the column was created.
The CDC (incremental updates) mechanism in the connector may not notice that the record dated in the past was added. In this case, trigger a reload of `sys_dictionary` table.
After reload is completed wait for the next scheduled ingestion to recreate the view with correct list of columns.

## Table with continuous schedule disabled by the connector

The connector automatically disables tables with continuous schedule when it detects that ingestion on such a table failed
for 10 consecutive times, and the cause of all failed ingestion runs is related to the ServiceNow® instance. This mechanism
prevents overloading of the ServiceNow® instance when too many tables with continuous schedule are enabled and allows the
ServiceNow® instance to recover after the table is disabled. The connector does not enable the table again automatically,
it must be enabled manually by the user.

Information that a table is automatically disabled is visible in the `CONNECTOR_ERRORS` view when filtering by
`TABLE_INGESTION_DISABLED` code. When the error occurs, investigate why ingestion runs on the table failed.
You can find detailed information about errors in the `CONNECTOR_ERRORS` view after filtering by `INGESTION_FAILED`
code.

After the cause of error is investigated and resolved, the table can be [enabled](/connectors/servicenow/ingestion#label-servicenow-connector-configure-enable-sync-v2)
again by calling the `ENABLE_TABLE` or `ENABLE_TABLES` procedure.

## Connector is unavailable

The connector can enter an `ERROR` state, which could happen for a variety of reasons.
For instance internal connector error, which cannot be recovered.
In such situations the `Connector unavailable` error message will be displayed when examining connector state.

Currently, there is no automatic recovery mechanism for this state. However you can still execute several connector functions,
including the [EXPORT\_CONNECTOR\_STATE](/connectors/servicenow/managing#label-servicenow-connector-exporting-connector-state-v2) procedure.

To examine if the connector is in an `ERROR` state, execute the query:

Copy code

```
CALL GET_CONNECTOR_STATUS();
```

In addition please contact the [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to help us better understand the problem or determine how it can be possibly avoided. You should also execute
[manual connector reinstallation](/connectors/servicenow/managing#label-reinstalling-the-servicenow-connector-v2) in order to restore the connector to a working state.
Note that previously ingested data isn’t lost and the connector can continue the ingestion from where it previously stopped.
