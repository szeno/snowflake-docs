# Viewing log messages

You can view the log messages either through Snowsight or by querying the event table in which log entries are stored.

Note

Before you can begin using log messages, you must [enable telemetry data collection](/developer-guide/logging-tracing/logging-tracing-enabling).

## Required privileges

To view log entries in Snowsight or query the event table directly, your active role must have one
of the following:

- The ACCOUNTADMIN role.
- The `SNOWFLAKE.EVENTS_VIEWER` application role, which grants SELECT access to the
  [EVENTS\_VIEW](/sql-reference/telemetry/events_view) of the default event table.
- The `SNOWFLAKE.EVENTS_ADMIN` application role, which grants broader access including SELECT,
  TRUNCATE, and DELETE on the default event table.
- The SELECT privilege on a [custom event table](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-custom), if your account
  uses a custom event table instead of the default.

For information on granting these roles, see
[Roles for access to the default event table and EVENTS\_VIEW](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default-roles).

## View log entries in Snowsight

You can use Snowsight to view log data captured in the event table.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Monitoring** » **Traces & logs**.
3. In the **Traces & Logs** page, you can do the following actions:
   - To filter the displayed rows, use the drop-down menus at the top of the page. You can filter by the following characteristics:

     - Date range during which the entry was recorded
     - Name of the Snowflake user executing the code that emitted the entry
     - Log entry severity
     - Programming language of the code that emitted the log entry
   - To filter entries by a specific time period in the displayed data, select the graph bar representing the time period.
   - To sort rows, select the name of the column by which you want to sort.
   - To view more detailed information about an entry in its **Details** panel, select the entry’s row.

     On this panel, you can view more information stored in the event table. The following table describes values in the panel:

     | Detail | Description |
     | --- | --- |
     | Record Type | Type of event the selected row represents. Retrieved from the [RECORD\_TYPE column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-type-column) value. |
     | Database | Name of the database containing the code that emitted the entry. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-column) `snow.database.name` value. |
     | Schema | Name of the schema containing the code that emitted the entry. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-column) `snow.schema.name` value. |
     | Severity | Severity of the log entry. Retrieved from the [RECORD column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-column) `severity_text` value. |
     | Query ID | ID of the query within which the log entry was emitted. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-column) `snow.query.id` value. |
     | Object | Name of the emitted log entry’s source, such as the function or procedure. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-column) `snow.executable.name` value. |
     | Warehouse | Name of the warehouse running the query that generated the event. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-column) `snow.warehouse.name` value. |
     | Owner | Name of the primary role in the session. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-column) `snow.session.role.primary.name` value. |
     | Log Text | Log message text. Retrieved from the [VALUE column](/developer-guide/logging-tracing/event-table-columns#label-event-table-value-column) value. |

     Expand

     Show lessSee more

## Query the event table for log entries

To access the logged messages, execute the SELECT command on the event table.

An event table has a set of predefined columns that capture information about the logged messages, including the following:

- The timestamp when the message was ingested
- The scope of the log event, such as the name of the class where the log event was created
- The log event source, including the database, schema, user, warehouse
- The severity level of the log
- The log message

For reference information about the event table’s structure, see [Event table columns](/developer-guide/logging-tracing/event-table-columns).

The following sections illustrate with example data how you can query the event table for log message data.

### Collected data

Output in the following example shows content from a selected subset of columns from an event table after log messages have been captured
for two separate handlers: one written in Scala and the other in Python.

For reference information about event table columns that collect log message data, see [Data captured by event type](/developer-guide/logging-tracing/event-table-columns#label-event-table-schema-data-logs).

```
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| TIMESTAMP           | SCOPE                             | RESOURCE_ATTRIBUTES   | RECORD_TYPE | RECORD                       | VALUE                                                      |
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-19 22:00:49 | { "name": "python_logger" }       | **See excerpt below** | LOG         | { "severity_text": "INFO" }  | Logging from Python module.                                |
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-19 22:00:49 | { "name": "python_logger" }       | **See excerpt below** | LOG         | { "severity_text": "INFO" }  | Logging from Python function start.                        |
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-19 22:00:49 | { "name": "python_logger" }       | **See excerpt below** | LOG         | { "severity_text": "ERROR" } | Logging an error from Python handler.                      |
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-19 22:12:55 | { "name": "ScalaLoggingHandler" } | **See excerpt below** | LOG         | { "severity_text": "INFO" }  | Logging from within the Scala constructor.                 |
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-19 22:12:56 | { "name": "ScalaLoggingHandler" } | **See excerpt below** | LOG         | { "severity_text": "INFO" }  | Logging from Scala method start.                           |
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-19 22:12:56 | { "name": "ScalaLoggingHandler" } | **See excerpt below** | LOG         | { "severity_text": "ERROR" } | Logging an error from Scala handler: Something went wrong. |
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

#### RESOURCE\_ATTRIBUTES excerpts

The following JSON includes excerpts from values you’d find in the preceding output’s RESOURCE\_ATTRIBUTES column. Each
`snow.executable.name` name-value pair is from a different row in the preceding output.

The SELECT query code following this excerpt selects from the RESOURCE\_ATTRIBUTES column’s value.

The RESOURCE\_ATTRIBUTES column contains data about the event’s source. For reference information, see
[RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-column).

Copy code

```
{
  ...
  "snow.executable.name": "ADD_TWO_NUMBERS(A FLOAT, B FLOAT):FLOAT"
  ...
}

{
  ...
  "snow.executable.name": "ADD_TWO_NUMBERS(A FLOAT, B FLOAT):FLOAT"
  ...
}

{
  ...
  "snow.executable.name": "ADD_TWO_NUMBERS(A FLOAT, B FLOAT):FLOAT"
  ...
}

{
  ...
  "snow.executable.name": "DO_LOGGING():VARCHAR(16777216)"
  ...
}

{
  ...
  "snow.executable.name": "DO_LOGGING():VARCHAR(16777216)"
  ...
}

{
  ...
  "snow.executable.name": "DO_LOGGING():VARCHAR(16777216)"
  ...
}
```

### Query with SELECT statement

When querying for message data, to select attribute values within a column, use
[bracket notation](/user-guide/querying-semistructured#label-bracket-notation-when-querying-semistructured-data), as in the following form:

Copy code

```
COLUMN_NAME['attribute_name']
```

Code in the following example queries the preceding table with the intention of isolating data related to the Python handler’s log messages.
The query selects the `severity_text` attribute for the log entry severity. It selects the `VALUE` column’s content for the log
message.

The procedure containing the handler is called `do_logging`. Note that for the query to work, you must specify the procedure name
in all capital letters.

Copy code

```
SET event_table_name='my_db.public.my_event_table';

SELECT
  TIMESTAMP as time,
  RESOURCE_ATTRIBUTES['snow.executable.name'] as executable,
  RECORD['severity_text'] as severity,
  VALUE as message
FROM
  IDENTIFIER($event_table_name)
WHERE
  SCOPE['name'] = 'python_logger'
  AND RESOURCE_ATTRIBUTES['snow.executable.name'] LIKE '%DO_LOGGING%'
  AND RECORD_TYPE = 'LOG';
```

### Query results

Output in the following example illustrates the query’s result:

```
----------------------------------------------------------------------------------------------------------------
| TIME                | EXECUTABLE                       | SEVERITY   | MESSAGE                                |
----------------------------------------------------------------------------------------------------------------
| 2023-04-19 22:00:49 | "DO_LOGGING():VARCHAR(16777216)" | "INFO"     | "Logging from Python module."          |
----------------------------------------------------------------------------------------------------------------
| 2023-04-19 22:00:49 | "DO_LOGGING():VARCHAR(16777216)" | "INFO"     | "Logging from Python function start."  |
----------------------------------------------------------------------------------------------------------------
| 2023-04-19 22:00:49 | "DO_LOGGING():VARCHAR(16777216)" | "ERROR"    | "Logging an error from Python handler" |
----------------------------------------------------------------------------------------------------------------
```
