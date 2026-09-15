# Working with event tables

You can perform a subset of table operations on an event table you create, which is specifically designed for capturing events. The
sections in this topic describe the operations an event table supports.

Note

You can perform only a subset of the operations listed here on the default event table, as noted in this topic.

## Operations supported on an event table

An event table is designed specifically for capturing events. You cannot perform some of the operations on an event table that you can
perform on a regular table.

With an event table, you can perform the following operations (note exceptions for the default event table):

| Operation | Default event table support | User-created event table support |
| --- | --- | --- |
| [SHOW EVENT TABLES](/sql-reference/sql/show-event-tables) | ✔ | ✔ |
| [DESCRIBE EVENT TABLE](/sql-reference/sql/desc-event-table) | ✔ | ✔ |
| [SELECT](/sql-reference/sql/select) | ✔ | ✔ |
| [DROP TABLE](/sql-reference/sql/drop-table) |  | ✔ |
| [UNDROP TABLE](/sql-reference/sql/undrop-table) |  | ✔ |
| [CREATE TABLE](/sql-reference/sql/create-table) |  | ✔ |
| [TRUNCATE TABLE](/sql-reference/sql/truncate-table) | ✔ | ✔ |
| [DELETE](/sql-reference/sql/delete) | ✔ | ✔ |
| [ALTER TABLE (event tables)](/sql-reference/sql/alter-table-event-table) | ✔ (rename is not supported) | ✔ (rename is not supported) |

Expand

Show lessSee more

## Deleting rows from an event table

If you need to delete rows from an event table, you can use the following commands:

- Use [TRUNCATE TABLE](/sql-reference/sql/truncate-table) to remove all rows from the event table.
- Use [DELETE](/sql-reference/sql/delete) to remove selected rows from the event table.

  You can use this if you need to implement more complex log retention policies (e.g. if you need to retain logs for some functions for a
  longer period of time than other functions).

## Parameters for event tables

You can use the following parameters to specify how the event table should be used by handler code.

EVENT\_TABLE
:   Specifies the name of the event table for logging messages from stored procedures and UDFs in this account. For reference information,
    see [EVENT\_TABLE](/sql-reference/parameters#label-event-table).

LOG\_LEVEL
:   Specifies the severity level of log messages produced through logging APIs that should be ingested and made available in the active event
    table. Log messages at the specified level (and at more severe levels) are ingested. For more information, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level) and
    [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

LOG\_EVENT\_LEVEL
:   Specifies the severity level of log events (rows with record type EVENT) that should be ingested and made available in the active event
    table. Log events at the specified level (and at more severe levels) are ingested. For more information, see [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) and
    [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

METRIC\_LEVEL
:   Specifies whether metrics data should be ingested and made available in the active event table. For more information, see
    [METRIC\_LEVEL](/sql-reference/parameters#label-metric-level) and [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

TRACE\_LEVEL
:   Specifies the verbosity of trace events that should be ingested and made available in the active event table. Events at the specified
    level are ingested. For more information, see [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level) and
    [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

## Access control privileges for event tables

You can use privileges in the global and event table scope to manage access to operations on an event table.

For more information, see [Event table privileges](/user-guide/security-access-control-privileges#label-event-table-privileges) and log level privileges in [Global privileges (account privileges)](/user-guide/security-access-control-privileges#label-global-privileges).

## Managing access to event table data

When it’s impractical for you to make event table data available to a range of users and roles, you can create views
for access by users with specific roles.

When you want to manage access to the data in this table, you can create views on the event table, then grant access for each view to
separate roles. Through the view, a role might have access to specified subset of the data in the event table.

For more information about creating views, see [CREATE VIEW](/sql-reference/sql/create-view).

## Using streams to track changes to event tables

You can create a stream on an event table, such as to capture changes to the table.

For more information about streams, see [Introduction to streams](/user-guide/streams-intro) and [CREATE STREAM](/sql-reference/sql/create-stream).

Code in the following example creates a stream to capture inserts on the event table `my_event_table`.

Copy code

```
CREATE STREAM append_only_comparison ON EVENT TABLE my_event_table APPEND_ONLY=TRUE;
```
