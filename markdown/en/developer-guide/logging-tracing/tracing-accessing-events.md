# Viewing trace data

You can view trace data either through Snowsight or by querying the event table in which trace data is stored.

Note

Before you can begin using trace data, you must [enable telemetry data collection](/developer-guide/logging-tracing/logging-tracing-enabling).

## View trace entries in Snowsight

You can use Snowsight to view trace data captured in the event table.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Monitoring** » **Traces & logs**.
3. In the **Traces & Logs** page, you can view trace entries with the following columns:

   | Column | Description |
   | --- | --- |
   | Date | Date on which the entry was recorded. |
   | Duration | Length of time from the trace’s start to its end. |
   | Trace Name | The name of the executable generating the event. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-event-source) `snow.executable.name` value. |
   | Status | `Error` if the trace reported errors; otherwise, `Success`. |
   | Spans | Number of spans in the trace. |

   Expand

   Show lessSee more
4. In the **Traces & Logs** page, you can perform the following actions:

   - To filter the displayed rows, use the drop-down menus at the top of the page. You can filter by the following characteristics:

     - Date range during which the entry was recorded
     - Status of the trace, such as `Success` or `Error`
     - Database on which the trace was run
   - To sort rows, select the name of the column by which you want to sort.
5. To view more detailed information about an entry in its **Trace Details** page, select the entry’s row.
6. In the **Traces Details** page, you can view a list of spans.

   A span object contains trace events. For more information, see [How Snowflake represents trace events](/developer-guide/logging-tracing/tracing-how-events-work).

   - To filter the displayed rows use the drop-down menu at the top of the page. You can filter by **Span Type**: UDF, procedure, or
     Streamlit.
   - To view a legend describing data shown in the rows, select the **Legend** dropdown, and then select the legend you want to see.
   - To view more detailed information about an entry, select the entry’s row.

     On this panel, you can view more information stored in the event table. The following tables describe values in the panel:

     **Details tab**

     | Detail | Description |
     | --- | --- |
     | Trace ID | A unique identifier for calls made from a query. Retrieved from the [TRACE column](/developer-guide/logging-tracing/event-table-columns#label-event-table-trace-column) `trace_id` value. For more information, see [Trace value](/developer-guide/logging-tracing/event-table-columns#label-event-table-trace-value). |
     | Span ID | A unique identifier tied to the threading model. Retrieved from the [TRACE column](/developer-guide/logging-tracing/event-table-columns#label-event-table-trace-column) `span_id` value. For more information, see [Trace value](/developer-guide/logging-tracing/event-table-columns#label-event-table-trace-value). |
     | Scope | Namespace of code emitting the event. Retrieved from the [SCOPE column](/developer-guide/logging-tracing/event-table-columns#label-event-table-scope-column). |
     | Duration | The span’s duration from start to finish. For more information, see [For `SPAN` RECORD\_TYPE](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-column-span). |
     | Name | The span’s name. Retrieved from the [RECORD column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-column-span) `name` value. |
     | Parent Span ID | Unique ID of the span containing the selected span. |
     | Status Code | The span’s status code. Retrieved from the [RECORD column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-column-span) `status` value. |
     | Other attributes | Attributes and values added by user code. |
     | Query ID | ID of the query that initiated the trace. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-execution-environment) `snow.query.id` value. |
     | Name | The name of the executable generating the event. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-event-source) `snow.executable.name` value. |
     | Type | The type of executable that generated the event. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-event-source) `snow.executable.type` value. |
     | User | The name of the user executing the function or procedure. For a Streamlit app, the name of the user who was viewing the app for a given event. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-execution-environment) `db.user` value. |
     | Owner | The name of the role with OWNERSHIP privilege for the executable. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-event-source) `snow.owner.name` value. |
     | Role | The name of the primary role in the session. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-execution-environment) `snow.session.role.primary.name` value. |
     | Warehouse | The name of the warehouse running the query generating the event. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-execution-environment) `snow.warehouse.name` value. |
     | Database | The name of the database containing the executable. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-event-source) `snow.database.name` value. |
     | Schema | The name of the schema containing the executable. Retrieved from the [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-event-source) `snow.schema.name` value. |

     Expand

     Show lessSee more

     **Span Events tab**

     Displays data recorded for trace events. For more information, see [Event data recorded](/developer-guide/logging-tracing/tracing-how-events-work#label-trace-events-event-data).

     **Related Metrics tab**

     Displays charts illustrating CPU and memory metrics for resource consumption by Snowpark Python stored procedures and UDFs. Metrics
     associated with the UDF are for a specific query. If you select a UDF span from the list, the metrics are related to one or more
     UDF spans for the same query. If you select a procedure from the list, you will see procedure metrics for a single span.

     **Logs tab**

     Displays the value logged by the event. Retrieved from the [VALUE column](/developer-guide/logging-tracing/event-table-columns#label-event-table-value-column).

## Query the event table for trace entries

An event table has a set of predefined columns that capture information about the logged messages, including:

- The timestamp when a span began.
- The timestamp when the event was created.
- The type of data recorded, such as whether the data is for a span or span event.
- The name of the span or event.
- Attributes, if any, associated with the span or event.

For reference information about event table columns, see [Event table columns](/developer-guide/logging-tracing/event-table-columns).

### Trace data query example

The following sections illustrate with example data how you can query the event table for trace data.

#### Collected data

Output in the following example shows content from a selected subset of columns from an event table after trace data has been captured
for three separate handlers written in Python.

For reference information on event table columns that collect trace data, see [Data for trace events](/developer-guide/logging-tracing/event-table-columns#label-event-table-schema-data-trace-events).

```
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| TIMESTAMP          | START_TIMESTAMP    | RESOURCE_ATTRIBUTES   | RECORD_TYPE | RECORD                                                                                                  | RECORD_ATTRIBUTES                                                           |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-20 0:45:49 | 2023-04-20 0:45:49 | **See excerpt below** | SPAN        | { "kind": "SPAN_KIND_INTERNAL", "name": "digits_of_number", "status": { "code": "STATUS_CODE_UNSET" } } |                                                                             |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-20 0:45:49 |                    |                       | SPAN_EVENT  | { "name": "test_udtf_init" }                                                                            |                                                                             |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-20 0:45:49 |                    |                       | SPAN_EVENT  | { "name": "test_udtf_process" }                                                                         | { "input": "42" }                                                           |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-20 0:45:49 |                    |                       | SPAN_EVENT  | { "name": "test_udtf_end_partition" }                                                                   |                                                                             |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-20 0:46:00 | 2023-04-20 0:46:00 |                       | SPAN        | { "kind": "SPAN_KIND_INTERNAL", "name": "times_two", "status": { "code": "STATUS_CODE_UNSET" } }        | { "example.func.times_two": "begin", "example.func.times_two.response": 8 } |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-20 0:46:00 |                    |                       | SPAN_EVENT  | { "name": "event_without_attributes" }                                                                  |                                                                             |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-20 0:46:00 |                    |                       | SPAN_EVENT  | { "name": "event_with_attributes" }                                                                     | { "example.key1": "value1", "example.key2": "value2" }                      |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-20 0:46:08 | 2023-04-20 0:46:08 |                       | SPAN        | { "kind": "SPAN_KIND_INTERNAL", "name": "do_tracing", "status": { "code": "STATUS_CODE_UNSET" } }       | { "example.proc.do_tracing": "begin" }                                      |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-20 0:46:08 |                    |                       | SPAN_EVENT  | { "name": "event_with_attributes" }                                                                     | { "example.key1": "value1", "example.key2": "value2" }                      |
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

**RESOURCE\_ATTRIBUTES Excerpts**

The following JSON excerpts contain two of the attributes included in the RESOURCE\_ATTRIBUTES column for each of the three handlers whose
data is included in the preceding output. The SELECT statement following these excerpts selects values from these attributes.

The RESOURCE\_ATTRIBUTES column contains data about the event’s source. For reference information, see
[RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-column).

Copy code

```
{
  ...
  "snow.executable.name": "DIGITS_OF_NUMBER(INPUT NUMBER):TABLE: (RESULT NUMBER)",
  "snow.executable.type": "FUNCTION",
  ...
}

{
  ...
  "snow.executable.name": "TIMES_TWO(X NUMBER):NUMBER(38,0)",
  "snow.executable.type": "FUNCTION",
  ...
}

{
  ...
  "snow.executable.name": "DO_TRACING():VARIANT",
  "snow.executable.type": "PROCEDURE",
  ...
}
```

#### Query with SELECT statement

When querying for data, you can select attribute values within a column by using
[bracket notation](/user-guide/querying-semistructured#label-bracket-notation-when-querying-semistructured-data), as in the following form:

Copy code

```
COLUMN_NAME['attribute_name']
```

Code in the example below queries the preceding table with the intention of isolating data related to the `DIGITS_OF_NUMBER`
function.

Copy code

```
SET EVENT_TABLE_NAME='my_db.public.my_events';

SELECT
  TIMESTAMP as time,
  RESOURCE_ATTRIBUTES['snow.executable.name'] as handler_name,
  RESOURCE_ATTRIBUTES['snow.executable.type'] as handler_type,
  RECORD['name'] as event_name,
  RECORD_ATTRIBUTES as attributes
FROM
  IDENTIFIER($event_table_name)
WHERE
  RECORD_TYPE = 'SPAN_EVENT'
  AND HANDLER_NAME LIKE 'DIGITS_OF_NUMBER%';
```

#### Query results

Output in the following example illustrates the query’s result.

```
-------------------------------------------------------------------------------------------------------------------------------------------
| TIME               | HANDLER_NAME                                          | HANDLER_TYPE | EVENT_NAME              | ATTRIBUTES        |
-------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-20 0:45:49 | DIGITS_OF_NUMBER(INPUT NUMBER):TABLE: (RESULT NUMBER) | FUNCTION     | test_udtf_init          |                   |
-------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-20 0:45:49 | DIGITS_OF_NUMBER(INPUT NUMBER):TABLE: (RESULT NUMBER) | FUNCTION     | test_udtf_process       | { "input": "42" } |
-------------------------------------------------------------------------------------------------------------------------------------------
| 2023-04-20 0:45:49 | DIGITS_OF_NUMBER(INPUT NUMBER):TABLE: (RESULT NUMBER) | FUNCTION     | test_udtf_end_partition |                   |
-------------------------------------------------------------------------------------------------------------------------------------------
```
