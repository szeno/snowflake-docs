Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$EXTERNAL\_TABLE\_PIPE\_STATUS

Retrieves a JSON representation of the current refresh status for the internal (hidden) pipe object associated with an external table.

Automatically refreshing the metadata for an external table relies internally on Snowpipe, which receives event notifications when changes occur in the monitored cloud storage. For more information, see [Introduction to external tables](/user-guide/tables-external-intro).

## Syntax

Copy code

```
SYSTEM$EXTERNAL_TABLE_PIPE_STATUS( '<external_table_name>' )
```

## Arguments

`external_table_name`
:   External table for which you want to retrieve the current automatic refresh status.

## Usage notes

- This function only returns results for the external table owner (i.e. the role that has the OWNERSHIP privilege on the external table).
- `external_table_name` is a string so it must be enclosed in single quotes:
  - Note that the entire name must be enclosed in single quotes, including the database and schema (if the name is fully-qualified), i.e. `'<db>.<schema>.<external_table_name>'`.
  - If the external table name is case-sensitive or includes any special characters or spaces, double quotes are required to process the case/characters. The double quotes must be enclosed within the single quotes, i.e. `'"<external_table_name>"'`.

## Output

The function returns a JSON object containing the following name/value pairs (if applicable to the current pipe status):

> `{"executionState":"<value>","oldestPendingFilePath":"<value>","oldestFileTimestamp":<value>,"pendingFileCount":<value>,"lastPipeFaultTimestamp":"<value>","notificationChannelName":"<value>","numOutstandingMessagesOnChannel":<value>,"lastReceivedMessageTimestamp":"<value>","lastForwardedMessageTimestamp":"<value>","error":<value>,"fault":<value>,"lastPulledFromChannelTimestamp":"<value>","lastForwardedFilePath":"<value>"}`

Where:

> `executionState`
> :   Current execution state of the pipe. The value could be any one of the following:
>
>     - `RUNNING` (i.e. everything is normal; Snowflake may or may not be actively processing event messages for this pipe)
>     - `STOPPED_CLONED` (i.e. the pipe is contained by a database or schema clone)
>     - `STOPPED_FEATURE_DISABLED`
>     - `STOPPED_STAGE_DROPPED`
>     - `STOPPED_FILE_FORMAT_DROPPED`
>     - `STOPPED_NOTIFICATION_INTEGRATION_DROPPED`
>     - `STOPPED_MISSING_PIPE`
>     - `STOPPED_MISSING_TABLE` (the target table defined in the pipe definition was dropped)
>     - `STALLED_COMPILATION_ERROR`
>     - `STALLED_INITIALIZATION_ERROR`
>     - `STALLED_EXECUTION_ERROR`
>     - `STALLED_INTERNAL_ERROR`
>     - `PAUSED`
>     - `PAUSED_BY_SNOWFLAKE_ADMIN`
>     - `PAUSED_BY_ACCOUNT_ADMIN`
>
> `oldestPendingFilePath`
> :   Path to the oldest data file currently queued for a metadata refresh operation. The timestamp when the file was added to the queue is returned in the `oldestFileTimestamp` property.
>
> `oldestFileTimestamp`
> :   Earliest timestamp among data files currently queued for a metadata refresh operation (if applicable), where the timestamp is set when the file is added to the queue.
>
> `pendingFileCount`
> :   Number of files currently being processed by the pipe. This value decreases as the external table metadata is refreshed. When this value is `0`, no metadata refreshes are queued for this pipe.
>
> `lastPipeFaultTimestamp`
> :   Timestamp when an internal Snowflake process error was last detected.
>
> `notificationChannelName`
> :   Amazon SQS queue or Microsoft Azure storage queue associated with the pipe.
>
> `numOutstandingMessagesOnChannel`
> :   Number of messages in the queue that have been queued but not received yet.
>
> `lastReceivedMessageTimestamp`
> :   Timestamp of the last message received from the queue.
>
> `lastForwardedMessageTimestamp`
> :   Timestamp of the last applicable event message with a matching path/prefix that was forwarded to the pipe.
>
> `channelErrorMessage`
> :   Error message produced when attempting to read messages from the associated cloud messaging service queue.
>
> `lastErrorRecordTimestamp`
> :   Timestamp of last channel error message (i.e. error message reported in the `channelErrorMessage` value).
>
> `error`
> :   Error message produced when the pipe was last compiled for execution (if applicable); often caused by problems accessing the necessary objects (i.e. table, stage, file format) due to permission problems or dropped objects.
>
> `fault`
> :   Most recent internal Snowflake process error (if applicable). Used primarily by Snowflake for debugging purposes.
>
> `lastPulledFromChannelTimestamp`
> :   Timestamp when Snowpipe last pulled event notifications for the pipe from the cloud messaging service queue.
>
> `lastForwardedFilePath`
> :   Path of the data file identified in the last applicable event message that was forwarded to the pipe.

## Examples

Retrieve the automatic refresh status for an external table with a case-insensitive name:

> Copy code
>
> ```
> SELECT SYSTEM$EXTERNAL_TABLE_PIPE_STATUS('mydb.myschema.exttable');
>
> +---------------------------------------------------------------+
> | SYSTEM$EXTERNAL_TABLE_PIPE_STATUS('MYDB.MYSCHEMA.EXTTABLE')   |
> |---------------------------------------------------------------|
> | {"executionState":"RUNNING","pendingFileCount":0}             |
> +---------------------------------------------------------------+
> ```

Retrieve the status for a pipe with a case-sensitive name:

> Copy code
>
> ```
> SELECT SYSTEM$EXTERNAL_TABLE_PIPE_STATUS('mydb.myschema."extTable"');
>
> +---------------------------------------------------------------+
> | SYSTEM$EXTERNAL_TABLE_PIPE_STATUS('MYDB.MYSCHEMA."extTable"') |
> |---------------------------------------------------------------|
> | {"executionState":"RUNNING","pendingFileCount":0}             |
> +---------------------------------------------------------------+
> ```
