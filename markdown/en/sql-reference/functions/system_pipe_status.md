Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$PIPE\_STATUS

Retrieves a JSON representation of the current status of a pipe.

For more information, see [Snowpipe](/user-guide/data-load-snowpipe-intro).

## Syntax

Copy code

```
SYSTEM$PIPE_STATUS( '<pipe_name>' )
```

## Arguments

`pipe_name`
:   Pipe for which you want to retrieve the current status.

## Usage notes

- Returns results only for the pipe owner (the role with the OWNERSHIP privilege on the pipe) or a role with the MONITOR privilege on
  the pipe.
- `pipe_name` is a string so it must be enclosed in single quotes:

  - Note that the entire name must be enclosed in single quotes, including the database and schema (if the name is fully qualified): `'<db>.<schema>.<pipe_name>'`.
  - If the pipe name is case-sensitive or includes any special characters or spaces, double quotes are required to process the case/characters. The double quotes must be enclosed within the single quotes, i.e. `'"<pipe_name>"'`.
- The `oldestPendingFilePath` and `oldestFileTimestamp` fields are not available in the JSON output if `pendingFileCount` is `0`, as these fields only appear when there are files queued for ingestion.

## Output

The function returns a JSON object containing the following name/value pairs (if applicable to the current pipe status):

> `{"executionState":"<value>","oldestPendingFilePath":"<value>","oldestFileTimestamp":<value>,"pendingFileCount":<value>,"lastPipeErrorTimestamp":"<value>","lastPipeFaultTimestamp":"<value>","lastIngestedTimestamp":"<value>","lastIngestedFilePath":"<value>","notificationChannelName":"<value>","numOutstandingMessagesOnChannel":<value>,"lastReceivedMessageTimestamp":"<value>","lastForwardedMessageTimestamp":"<value>","error":<value>,"fault":<value>,"lastPulledFromChannelTimestamp":"<value>","lastForwardedFilePath":"<value>","loadHistoryRemainingEntriesToSync":"<value>", "oldestPendingHistoryRefreshJobCreationTime":"<value>", "pendingHistoryRefreshJobsCount":"<value>"}`

Where:

> `executionState`
> :   Current execution state of the pipe. The value could be any one of the following:
>
>     - `FAILING_OVER` (the pipe is in the process of failing over from primary to secondary account)
>     - `PAUSED`
>     - `READ_ONLY` (the pipe or the target table is in a secondary read-only database.) A pipe in a secondary database is
>       read only until you promote the secondary database to primary. For more information, see [Pipes in secondary databases](/user-guide/account-replication-stages-pipes-load-history#label-pipes-in-secondary-databases).
>     - `RUNNING` (everything is normal; Snowflake may or may not be actively processing files for this pipe)
>     - `STOPPED_BY_SNOWFLAKE_ADMIN` (the pipe is stopped by [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support). The pipe will not accept new files for ingestion. )
>     - `STOPPED_CLONED` (the pipe is contained by a database or schema clone)
>     - `STOPPED_FEATURE_DISABLED`
>     - `STOPPED_STAGE_ALTERED` (the pipe is stopped because the underlying stage location has been altered.)
>     - `STOPPED_STAGE_DROPPED`
>     - `STOPPED_FILE_FORMAT_DROPPED`
>     - `STOPPED_NOTIFICATION_INTEGRATION_DROPPED`
>     - `STOPPED_MISSING_PIPE`
>     - `STOPPED_MISSING_TABLE` (the target table defined in the pipe definition is dropped)
>     - `STALLED_COMPILATION_ERROR`
>     - `STALLED_INITIALIZATION_ERROR`
>     - `STALLED_EXECUTION_ERROR`
>     - `STALLED_INTERNAL_ERROR`
>     - `STALLED_STAGE_PERMISSION_ERROR` (an external stage permission error is detected.)
>
> `oldestPendingFilePath`
> :   Path to the oldest data file currently queued for processing. The timestamp when the file was added to the queue is returned in the existing oldestFileTimestamp property.
>
> `oldestFileTimestamp`
> :   Earliest timestamp among data files currently queued (if applicable), where the timestamp is set when the file is added to the queue.
>
> `pendingFileCount`
> :   Number of files queued for loading by the pipe.
>
>     This count can increase even if a pipe is paused. Depending on the `AUTO_INGEST` setting for the pipe, the number of queued
>     files can increase as follows:
>
>     `AUTO_INGEST = TRUE`
>     :   Files added to the cloud storage bucket or container trigger new file event notifications for the pipe.
>
>         Note that if a paused pipe becomes [stale](/user-guide/data-load-snowpipe-manage#label-snowpipe-resume-stale-pipe), the `pendingFileCount` count ignores
>         any event notifications older than the limited retention period.
>
>     `AUTO_INGEST = FALSE`
>     :   Calls to the `insertFiles` REST endpoint trigger files to be queued for loading by the pipe.
>
> `lastPipeErrorTimestamp`
> :   Timestamp when compiling the COPY INTO <table> statement in the pipe definition for execution last produced an error.
>
> `lastPipeFaultTimestamp`
> :   Timestamp when an internal Snowflake process error was last detected.
>
> `lastIngestedTimestamp`
> :   Timestamp when the most recent file was loaded successfully by Snowpipe into the destination table.
>
> `lastIngestedFilePath`
> :   Path of the file loaded at the timestamp specified in lastIngestedTimestamp.
>
> `notificationChannelName`
> :   Amazon SQS queue or Microsoft Azure storage queue associated with the pipe.
>
> `numOutstandingMessagesOnChannel`
> :   Number of messages in the queue that have been queued but not received yet.
>
> `lastReceivedMessageTimestamp`
> :   Timestamp of the last message received from the queue. Note that this message might not apply to the specific pipe (e.g., if the path/prefix associated with the message does not match the path/prefix in the pipe definition). In addition, only messages triggered by created data objects are consumed by auto-ingest pipes.
>
> `lastForwardedMessageTimestamp`
> :   Timestamp of the last “create object” event message with a matching path/prefix that was forwarded to the pipe.
>
> `channelErrorMessage`
> :   Error message produced when attempting to read messages from the associated Google Cloud Pub/Sub queue or Microsoft Azure Event
>     Grid storage queue.
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
> :   Timestamp when Snowpipe last pulled “create object” event notifications for the pipe from the Amazon Simple Queue Service (SQS) queue, Google Pub/Sub queue, or Microsoft Azure storage queue.
>
>     This value applies to auto-ingest Snowpipe loads only.
>
> `lastForwardedFilePath`
> :   Path of the data file identified in the last “create object” event message that was forwarded to the pipe.
>
> `loadHistoryRemainingEntriesToSync`
> :   Number of remaining load history entries to be replicated. When a pipe fails over, load history entries might continue to be replicated for the pipe, ensuring that changes from the last refresh operation are up to date. You can use this field to monitor the progress of load history replication for a pipe.
>
> `oldestPendingHistoryRefreshJobCreationTime`
> :   Timestamp of the oldest pending refresh job creation time, displayed only when a pending job exists.
>
> `pendingHistoryRefreshJobsCount`
> :   Total number of pending history refresh jobs for non-table-owned pipes. Displays `0` if no jobs are pending.

## Examples

Retrieve the status for a pipe with a case-insensitive name:

> Copy code
>
> ```
> SELECT SYSTEM$PIPE_STATUS('mydb.myschema.mypipe');
>
> +---------------------------------------------------+
> | SYSTEM$PIPE_STATUS('MYDB.MYSCHEMA.MYPIPE')        |
> |---------------------------------------------------|
> | {"executionState":"RUNNING","pendingFileCount":0} |
> +---------------------------------------------------+
> ```

Retrieve the status for a pipe with a case-sensitive name:

> Copy code
>
> ```
> SELECT SYSTEM$PIPE_STATUS('mydb.myschema."myPipe"');
>
> +---------------------------------------------------+
> | SYSTEM$PIPE_STATUS('MYDB.MYSCHEMA."MYPIPE"')      |
> |---------------------------------------------------|
> | {"executionState":"RUNNING","pendingFileCount":0} |
> +---------------------------------------------------+
> ```
