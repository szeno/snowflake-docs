Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$PARQUET\_DIRECT\_AUTO\_REFRESH\_STATUS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns the current auto-refresh status for a [Parquet Direct](/user-guide/tables-iceberg-parquet-direct) Iceberg table.
Use this function to check whether event-driven auto-refresh is running as expected and to diagnose issues.

Note

This function is specific to Parquet Direct tables (tables that use a catalog integration with `TABLE_FORMAT = NONE` or
`TABLE_FORMAT = HIVE`). For other externally managed Iceberg tables, such as Delta Direct or REST catalog tables, use
[SYSTEM$AUTO\_REFRESH\_STATUS](/sql-reference/functions/system_auto_refresh_status) instead.

## Syntax

Copy code

```
SYSTEM$PARQUET_DIRECT_AUTO_REFRESH_STATUS('<table_name>')
```

## Arguments

`'table_name'`
:   The name of the Parquet Direct table for which you want to retrieve the current auto-refresh status.

    If you use the fully qualified name, enclose the entire name in single quotes, including the database and schema.
    If the table name is case-sensitive or includes any special characters or spaces, you must use double quotes.
    Enclose the double quotes within the single quotes; for example, `'"Table_Name"'`.

## Returns

The function returns a JSON object that contains the following name/value pairs:

Copy code

```
{
  "executionState": "<value>",
  "invalidExecutionStateReason": "<value>",
  "pendingFileCount": "<value>",
  "oldestFileTimestamp": "<value>",
  "notificationChannelName": "<value>",
  "numOutstandingMessagesOnChannel": "<value>",
  "lastReceivedMessageTimestamp": "<value>",
  "lastForwardedMessageTimestamp": "<value>",
  "lastForwardedFilePath": "<value>",
  "channelErrorMessage": "<value>",
  "lastErrorRecordTimestamp": "<value>"
}
```

Where:

`executionState`
:   Current execution state of auto-refresh for the table.

    Values:

    - `RUNNING`: Auto-refresh is running as expected. This status doesn’t indicate whether Snowflake is actively processing
      event notifications at this moment.
    - `STALLED`: Auto-refresh encountered an error and is attempting to recover.
    - `STOPPED`: Auto-refresh encountered an unrecoverable error and has stopped. You must take action to resume
      auto-refresh. For more information, see [Refresh fails](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-troubleshoot-refresh-fails).

`invalidExecutionStateReason`
:   Error message associated with a `STALLED` or `STOPPED` execution state.

`pendingFileCount`
:   Number of Apache Parquet™ files queued for processing.

`oldestFileTimestamp`
:   Timestamp of the oldest file in the pending queue. Snowflake sets this timestamp when the file is added to the queue.

`notificationChannelName`
:   Name of the notification channel (for example, the Amazon SQS queue, Azure Storage queue, or Google Cloud Pub/Sub
    subscription) that delivers event notifications for the table.

`numOutstandingMessagesOnChannel`
:   Approximate number of pending messages in the notification channel.

`lastReceivedMessageTimestamp`
:   Timestamp of the most recent notification message received from the channel.

`lastForwardedMessageTimestamp`
:   Timestamp of the most recent notification message that Snowflake forwarded for processing for this table.

`lastForwardedFilePath`
:   Path of the file in the most recent notification message that Snowflake forwarded for processing for this table.

`channelErrorMessage`
:   Error message from the notification channel, if any.

`lastErrorRecordTimestamp`
:   Timestamp of the most recent error message from the notification channel.

Snowflake always returns `executionState` and `pendingFileCount`. The other fields appear only when they apply; for example,
the notification channel fields appear only when the table has a notification channel.

## Usage notes

- Calling this function requires a role that has the OWNERSHIP privilege on the Parquet Direct table.
- This function only works with Parquet Direct tables. Calling it on any other table returns an error.
- The function returns status only when `AUTO_REFRESH = TRUE` is set on the table. If auto-refresh isn’t enabled, the
  function returns a message that indicates auto-refresh isn’t enabled for the table.

## Examples

Retrieve the auto-refresh status for the Parquet Direct table `my_parquet_table` in the schema `db1.schema1`:

Copy code

```
SELECT SYSTEM$PARQUET_DIRECT_AUTO_REFRESH_STATUS('db1.schema1.my_parquet_table');
```

Extract individual fields from the result:

Copy code

```
SELECT status:executionState::STRING AS execution_state,
       status:pendingFileCount::NUMBER AS pending_files,
       status:lastReceivedMessageTimestamp::TIMESTAMP_LTZ AS last_notification,
       status:channelErrorMessage::STRING AS channel_error
  FROM (
    SELECT PARSE_JSON(SYSTEM$PARQUET_DIRECT_AUTO_REFRESH_STATUS('db1.schema1.my_parquet_table')) AS status
  );
```
