# Troubleshooting Snowpipe

When a pipe doesn’t load the files that you expect, start with [the diagnostic steps](#label-snowpipe-ts-diagnose). They narrow most problems down to one of three places: the event notifications from your cloud storage service, the pipe itself, or the files. Then find your symptom in the sections that follow.

If you already know the symptom, go straight to its section:

| Symptom | Section |
| --- | --- |
| `executionState` isn’t `RUNNING` | [Pipe execution states](#label-snowpipe-ts-execution-states) |
| `executionState` is `RUNNING`, but nothing loads | [Event notifications don’t reach Snowflake](#label-snowpipe-ts-notifications-not-received) and [Event notifications arrive, but the pipe doesn’t load the files](#label-snowpipe-ts-path-mismatch) |
| Some files never loaded | [Some staged files were never loaded](#label-snowpipe-ts-missing-files) |
| Files have the `Load failed` status | [Step 3: Get details about load errors](#label-snowpipe-ts-check-files) and [Common error messages](#label-snowpipe-ts-error-messages) |
| A corrected file with the same name didn’t load | [Modified or corrected files don’t load](#label-snowpipe-ts-modified-files) |
| Rows appear more than once | [Duplicate data in the target table](#label-snowpipe-ts-duplicate-data) |
| Files load later than usual | [Step 1: Check the pipe status](#label-snowpipe-ts-check-status) |
| A load-time column is hours earlier than expected | [Load times recorded with CURRENT\_TIMESTAMP are earlier than expected](#label-load-times-inserted-snowpipe-ts) |
| Large files in Amazon S3 don’t load | [Large files in Amazon S3 don’t load](#label-snowpipe-ts-s3-multipart) |
| Files in Azure Data Lake Storage Gen2 don’t load | [Files in Azure Data Lake Storage Gen2 don’t load](#label-snowpipe-ts-adls-gen2) |
| Loads from Google Cloud Storage are slow or stop | [Loads from Google Cloud Storage are delayed or files are missed](#label-snowpipe-ts-gcs-delayed) |
| The REST API returns an error, such as `400`, `401`, `403`, `404`, or `429` | [Files don’t load with the REST API](#label-snowpipe-ts-rest-api) |
| You fixed a problem and need to load the files that were missed | [Load missed files after you fix a problem](#label-snowpipe-ts-recover) |

Expand

Show lessSee more

To find out about problems as they happen, rather than after you notice missing data, set up [error notifications](/user-guide/data-load-snowpipe-errors), or record [Snowpipe events](/user-guide/data-load-snowpipe-monitor-events) and [create an alert on them](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-alerts). To find out when a pipe stops loading files for any reason, including when event notifications stop arriving, see [Get alerted when a pipe stops loading files](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-alerts-idle).

## Diagnose a problem

To find the cause of most Snowpipe problems, complete the following steps in order.

### Step 1: Check the pipe status

Call [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status), which returns a JSON object. You need the `MONITOR` or `OWNERSHIP` privilege on the pipe, or the `MONITOR EXECUTION` privilege on the account:

Copy code

```
SELECT SYSTEM$PIPE_STATUS('mydb.myschema.orders_pipe');
```

Check the following fields:

| Field | What it tells you | If the value isn’t what you expect |
| --- | --- | --- |
| `executionState` | Whether the pipe is running. `RUNNING` is normal. | See [Pipe execution states](#label-snowpipe-ts-execution-states). |
| `lastIngestedTimestamp` | When the pipe last loaded a file. `lastIngestedFilePath` shows which file it was. | If the time is earlier than you expect, the pipe stopped loading at about that time. Check the other fields to find out why. |
| `error` | The error from the last time Snowflake compiled the pipe’s `COPY INTO` statement, such as a missing object or a missing privilege. | Use the message to find the cause in the sections that follow. |
| `lastReceivedMessageTimestamp` | For automated loading, when Snowflake last received any event notification on the pipe’s notification channel. One channel can serve several pipes, so the notification might be for another pipe. | If the field is missing, or older than your newest files, see [Event notifications don’t reach Snowflake](#label-snowpipe-ts-notifications-not-received). |
| `channelErrorMessage` | For automated loading from Google Cloud Storage or Microsoft Azure, the error that Snowflake got when it tried to read the notification channel. | Use the message to fix the configuration of the Pub/Sub subscription or the Azure storage queue, and of the notification integration. |
| `lastForwardedMessageTimestamp` | For automated loading, when Snowpipe last forwarded a notification to this pipe. Snowpipe forwards a notification to a pipe only when the notification is for a new file in the location that the pipe watches. | If notifications are received but not forwarded, see [Event notifications arrive, but the pipe doesn’t load the files](#label-snowpipe-ts-path-mismatch). |
| `pendingFileCount` | The number of files that are queued for loading. | If the count keeps growing while `executionState` is `PAUSED`, that’s expected: resume the pipe. If it keeps growing while `executionState` is `RUNNING` and `oldestFileTimestamp` doesn’t change, the oldest file isn’t loading. Contact [Snowflake Support](/user-guide/contacting-support). |

Expand

Show lessSee more

If files load later than usual but `pendingFileCount` stays low, Snowflake might be throttling the pipe. Look for [`pipe_throttled` events](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-pipe-throttled), which are recorded only if `LOG_EVENT_LEVEL` is `WARN` or more verbose.

### Step 2: Check the copy history

Next, check what happened to each file. Query the [COPY\_HISTORY](/sql-reference/functions/copy_history) table function for the pipe’s target table. You need the `MONITOR` privilege on the account, or any privilege on the target table:

Copy code

```
SELECT file_name, status, row_count, first_error_message, last_load_time
  FROM TABLE(mydb.INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'myschema.orders',
    START_TIME => DATEADD('hour', -24, CURRENT_TIMESTAMP())))
  ORDER BY last_load_time DESC;
```

The `STATUS` column shows the result for each file, such as `Loaded`, `Partially loaded`, `Load failed`, or `Load in progress`. By default (`ON_ERROR = SKIP_FILE`), Snowpipe doesn’t load a file that contains errors, and the file has the `Load failed` status. For a file that didn’t load completely, `FIRST_ERROR_MESSAGE` shows the first error in the file.

The table function covers the last 14 days. For older loads, query the [COPY\_HISTORY view](/sql-reference/account-usage/copy_history) in the Account Usage schema. To review recent loads without SQL, open the pipe’s **Copy History** tab in Snowsight. For more information, see [Review copy history and pipe metrics](/user-guide/data-load-snowpipe-snowsight#label-snowsight-pipe-copy-history).

If a file that you expect is missing from the results, check an earlier time range. If it’s still missing, one of the following happened:

- The file is still waiting in the pipe’s queue. If `pendingFileCount` isn’t `0`, check `oldestPendingFilePath` and `oldestFileTimestamp`.
- The pipe never received a notification for the file, or the file is outside the pipe path. See [Some staged files were never loaded](#label-snowpipe-ts-missing-files).
- The pipe was dropped or recreated. The table function doesn’t return loads by a pipe that was dropped or recreated, so query the [COPY\_HISTORY view](/sql-reference/account-usage/copy_history) instead.
- The target table was truncated after the file loaded. The copy history shows only the loads after the latest truncate.

If you staged a file again with the same name, and the results show only one row for that file, with a `LAST_LOAD_TIME` earlier than when you staged it again, Snowpipe ignored the new copy. If you record [Snowpipe events](/user-guide/data-load-snowpipe-monitor-events) at the `DEBUG` level, an ignored file has a `file_lifecycle` event with a `SKIPPED` state. See [Modified or corrected files don’t load](#label-snowpipe-ts-modified-files).

### Step 3: Get details about load errors

To get details about the errors in files that a pipe failed to load, query the [VALIDATE\_PIPE\_LOAD](/sql-reference/functions/validate_pipe_load) table function. The function returns details such as the line and column where each error occurred and the rejected record:

Copy code

```
SELECT *
  FROM TABLE(mydb.INFORMATION_SCHEMA.VALIDATE_PIPE_LOAD(
    PIPE_NAME => 'mydb.myschema.orders_pipe',
    START_TIME => DATEADD('hour', -24, CURRENT_TIMESTAMP())));
```

`VALIDATE_PIPE_LOAD` returns an error if the pipe’s `COPY INTO` statement transforms semi-structured data, such as JSON, Avro, ORC, Parquet, or XML. It returns results only for the role that owns the pipe, or for a role that has all of the following privileges: `MONITOR` on the pipe (or `MONITOR EXECUTION` on the account), `USAGE` on an external stage (or `READ` on an internal stage), and `SELECT` and `INSERT` on the target table.

To see every error in a file, you can also run a [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement for the same file with `VALIDATION_MODE = RETURN_ALL_ERRORS`. With this copy option, `COPY INTO` checks the file and returns its errors without loading any data. `VALIDATION_MODE` isn’t supported for Apache Iceberg™ tables, or for `COPY INTO` statements that transform data or use `MATCH_BY_COLUMN_NAME`.

If neither option works for your pipe, use the copy history. The `FIRST_ERROR_MESSAGE`, `FIRST_ERROR_LINE_NUMBER`, `FIRST_ERROR_CHARACTER_POS`, and `FIRST_ERROR_COLUMN_NAME` columns show where the first error is, and `ERROR_COUNT` shows how many rows have errors.

## Pipe execution states

When `executionState` isn’t `RUNNING`, the pipe usually isn’t loading files. `FAILING_OVER` is the exception. The following table explains each state and what to do about it:

| State | What it means | What to do |
| --- | --- | --- |
| `PAUSED` | The pipe was paused, either directly or through its schema or account. | To find where the pipe was paused, run `SHOW PARAMETERS LIKE 'PIPE_EXECUTION_PAUSED' IN PIPE mydb.myschema.orders_pipe;` and check the `level` column. A stored procedure that a [budget](/user-guide/data-load-snowpipe-billing#label-snowpipe-billing-control) calls as a custom action can also pause pipes. Then resume the pipe, as described in [Pause and resume pipes](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-pause-resume). If it was paused for more than 14 days, or its ownership changed while it was paused, resume it with `SYSTEM$PIPE_FORCE_RESUME`, as described in [Resume a stale pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-resume-stale-pipe). |
| `READ_ONLY` | The pipe or its target table is in a secondary database, which is read-only. | The pipe starts loading after you promote the secondary database to primary. For more information, see [Pipes in secondary databases](/user-guide/account-replication-stages-pipes-load-history#label-pipes-in-secondary-databases). |
| `FAILING_OVER` | After a failover, the pipe’s database is now primary, and Snowflake is still syncing the pipe’s load metadata. The pipe can load new files in this state. | No action is needed. The state changes to `RUNNING` when the sync finishes. |
| `STOPPED_CLONED` | The pipe is in a cloned database or schema. In this state, the pipe doesn’t collect event notifications, and you can’t pause it. | If you don’t want the cloned pipe to load files, no action is needed. To start loading, first check the pipe’s `COPY INTO` statement. If the statement names the target table by its fully qualified name, such as `mydb.myschema.orders`, or as `schema.table` in a cloned schema, the resumed pipe loads data into the source table instead of the cloned table, which duplicates data in the source table. In that case, recreate the pipe in the clone so that the statement names the cloned table. A recreated pipe isn’t in the `STOPPED_CLONED` state, so it starts loading as soon as you create it. If the statement doesn’t name the source table, set `PIPE_EXECUTION_PAUSED = FALSE` on the cloned pipe instead. After you resume the pipe, it loads only files from new event notifications. |
| `STOPPED_STAGE_ALTERED` | The URL of the stage that the pipe references changed. Every pipe that references the stage stops. | [Recreate the pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps), and then load the files that were missed, as described in [Load missed files after you fix a problem](#label-snowpipe-ts-recover). |
| `STOPPED_STAGE_DROPPED` or `STOPPED_NOTIFICATION_INTEGRATION_DROPPED` | The stage or the notification integration that the pipe references was dropped or replaced. | Recreate the missing object, and then [recreate the pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps). Then load the files that were missed, as described in [Load missed files after you fix a problem](#label-snowpipe-ts-recover). |
| `STOPPED_MISSING_TABLE` | The target table was dropped or renamed. | Restore the table with [UNDROP TABLE](/sql-reference/sql/undrop-table) (or [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table) for an Iceberg table), rename the table back, or create a table with the same name. The pipe resumes loading without being recreated. Files that arrived while the table was missing weren’t queued, so load them as described in [Load missed files after you fix a problem](#label-snowpipe-ts-recover). |
| `STALLED_STAGE_PERMISSION_ERROR` | Snowflake can’t access the external stage. | Check the storage integration for the stage, and the permissions that it grants in your cloud storage service. For more information, see [Access denied errors](#label-snowpipe-ts-access-denied). Then run `LIST` on the stage, and call `SYSTEM$PIPE_STATUS` again. That call rechecks access to the stage, and the state changes back to `RUNNING` when the check succeeds. You don’t need to recreate the pipe unless you changed the stage’s `URL`. In that case, [recreate the pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps). Finally, load the files that failed while access was denied, as described in [Load missed files after you fix a problem](#label-snowpipe-ts-recover). |
| `STALLED_COMPILATION_ERROR`, `STALLED_INITIALIZATION_ERROR`, or `STALLED_EXECUTION_ERROR` | The pipe hit an error while preparing or running its `COPY INTO` statement. | Read the `error` field of `SYSTEM$PIPE_STATUS`. Check that the objects that the `COPY INTO` statement references, such as the stage, the target table, and any named file format, still exist and match the statement. Also check that the role that owns the pipe still has the privileges in the **Own a pipe** column of [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control). Recreate the pipe only if you need to change the statement. The state clears after you fix the cause. |
| `STALLED_INTERNAL_ERROR`, `STOPPED_BY_SNOWFLAKE_ADMIN`, `STOPPED_FEATURE_DISABLED`, or `STOPPED_MISSING_PIPE` | Snowflake stopped the pipe, or the pipe hit an internal error. | Contact [Snowflake Support](/user-guide/contacting-support). |

Expand

Show lessSee more

## Load missed files after you fix a problem

Before you recreate a pipe to fix a problem, note when it stopped loading: the `lastIngestedTimestamp` value from [Step 1](#label-snowpipe-ts-check-status) or, if you record Snowpipe events, the timestamp of the `pipe_lifecycle` event that reported the problem. The event’s `TIMESTAMP` value is in UTC and has no time zone, so add `+00:00` when you use it, for example `2026-10-02T20:00:00+00:00`. After you recreate a pipe, `SYSTEM$PIPE_STATUS` no longer returns the old pipe’s `lastIngestedTimestamp`, and the `COPY_HISTORY` table function no longer returns its loads, so you can’t look up this time afterward.

After you fix the cause, call `SYSTEM$PIPE_STATUS` and confirm that `executionState` is `RUNNING` and that `pendingFileCount` is going down. Then load the files that didn’t load while the problem lasted:

- **Files that failed to load**, for example with an access denied error or a remote file not found error, stay in the pipe’s load metadata, so Snowpipe doesn’t try them again, even with `ALTER PIPE ... REFRESH`. To list them, query the copy history from the time that the problem started:

  Copy code

  ```
  SELECT file_name, first_error_message, last_load_time
    FROM TABLE(mydb.INFORMATION_SCHEMA.COPY_HISTORY(
      TABLE_NAME => 'myschema.orders',
      START_TIME => '2026-10-02T13:00:00-07:00'::TIMESTAMP_LTZ))
    WHERE status = 'Load failed'
    ORDER BY last_load_time;
  ```

  If you recreated the pipe, the table function no longer returns the old pipe’s loads, so query the [COPY\_HISTORY view](/sql-reference/account-usage/copy_history) instead. Its data is usually up to 2 hours behind, but it can be up to 2 days behind for a table that has had few recent loads. To load the files that you find, see [Reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files).
- **Files that the pipe never queued**, such as files whose notifications it never received or that arrived while the target table was missing, don’t appear in the copy history. To load them, see [Load historical or missed files](/user-guide/data-load-snowpipe-manage#label-snowpipe-load-historic-data). If you recreated the pipe, set `MODIFIED_AFTER` in `ALTER PIPE ... REFRESH` to the time that you noted. If you don’t, the new pipe loads files that the old pipe already loaded.

## Files don’t load with automated loading

Use the results of [Step 1](#label-snowpipe-ts-check-status) to find the section that matches your symptom.

### Some staged files were never loaded

With automated loading, a pipe loads only the files that it receives event notifications for. If the copy history doesn’t list some files at all, the pipe probably never processed event notifications for them, for one of the following reasons:

- The files were staged before you configured event notifications.
- The pipe was paused for longer than 14 days, so some of its queued files were dropped.
- The files arrived while the target table was missing. See `STOPPED_MISSING_TABLE` in [Pipe execution states](#label-snowpipe-ts-execution-states).
- The files are outside the pipe path, or don’t match the `PATTERN` copy option. See [Event notifications arrive, but the pipe doesn’t load the files](#label-snowpipe-ts-path-mismatch).
- The files were written in a way that doesn’t send the event that Snowpipe listens for. See [Large files in Amazon S3 don’t load](#label-snowpipe-ts-s3-multipart) and [Files in Azure Data Lake Storage Gen2 don’t load](#label-snowpipe-ts-adls-gen2).
- A notification failed to arrive.

To load these files, see [Load historical or missed files](/user-guide/data-load-snowpipe-manage#label-snowpipe-load-historic-data).

### Event notifications don’t reach Snowflake

If `lastReceivedMessageTimestamp` is missing or older than your newest files, Snowflake isn’t receiving event notifications from your cloud storage service. If the timestamp was updating and then stopped, confirm that the following configuration is still in place:

- **Amazon S3**: The bucket’s event notification still sends `s3:ObjectCreated` events to the queue in the `notification_channel` column of the [SHOW PIPES](/sql-reference/sql/show-pipes) output. If you use Amazon SNS or Amazon EventBridge, the topic or rule still delivers to that queue. If you use Amazon SNS, also see [Snowpipe stops loading after an Amazon SNS subscription is deleted](#label-snowpipe-ts-sns-subscription-deleted).
- **Google Cloud Storage**: `channelErrorMessage` in the `SYSTEM$PIPE_STATUS` output is empty, the Pub/Sub subscription still exists, and the Snowflake service account still has the roles that it needs. See also [Loads from Google Cloud Storage are delayed or files are missed](#label-snowpipe-ts-gcs-delayed).
- **Microsoft Azure**: `channelErrorMessage` is empty, and the Event Grid subscription still sends events to the storage queue that the notification integration references.

For the setup steps for each cloud, see [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3), [Automating Snowpipe for Google Cloud Storage](/user-guide/data-load-snowpipe-auto-gcs), or [Automating Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure). The sections that follow describe more specific causes.

After you fix the configuration, load the files that were staged while notifications weren’t arriving. For more information, see [Load historical or missed files](/user-guide/data-load-snowpipe-manage#label-snowpipe-load-historic-data).

### Event notifications arrive, but the pipe doesn’t load the files

If `lastReceivedMessageTimestamp` is recent but `lastForwardedMessageTimestamp` isn’t, the notification channel receives notifications, but none of them are for files in the location that the pipe watches. Several pipes, and several buckets in the same region, can share a channel, so the recent notifications might belong to other pipes. `lastForwardedFilePath` shows the last file that Snowpipe forwarded to the pipe. Check the following:

- **Notifications for your files**: Confirm that your storage location still sends event notifications for the path where your files land. For more information, see [Event notifications don’t reach Snowflake](#label-snowpipe-ts-notifications-not-received).
- **The pipe path**: The pipe loads files only from its pipe path, which is the path in its `FROM` clause that Snowflake appends to the stage URL. Compare that combined path with the location where your application writes files.
- **The `PATTERN` copy option**: If the pipe’s `COPY INTO` statement includes `PATTERN`, check whether the regular expression filters out the files. Snowpipe forwards notifications based only on the path, so `lastForwardedMessageTimestamp` can be recent even when `PATTERN` filters out every file.

To change the pattern or the pipe path, recreate the pipe as described in [Recreate a pipe safely](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps), and then load the files that it missed, as described in [Load missed files after you fix a problem](#label-snowpipe-ts-recover).

### Large files in Amazon S3 don’t load

When an application uploads a large file to Amazon S3 with a multipart upload, S3 sends an `s3:ObjectCreated:CompleteMultipartUpload` event. If the event notification for your bucket includes only `s3:ObjectCreated:Put`, `s3:ObjectCreated:Post`, or `s3:ObjectCreated:Copy`, Snowpipe never learns about these files, and they don’t appear in the copy history or in `SYSTEM$PIPE_STATUS`. Multipart uploads are typically used for files larger than 8 to 16 MiB, depending on the client that uploads the files. For example, the AWS CLI uses a multipart upload for files larger than 8 MiB by default.

To fix this problem, complete the following steps:

1. In the Amazon S3 console, open the bucket for your stage, and then select **Properties** » **Event notifications**.
2. Change the event types for the notification to **All object create events**, or add `s3:ObjectCreated:CompleteMultipartUpload`.
3. Upload a large file, and then confirm that it appears in the copy history.
4. Load the large files that were uploaded before you changed the event types. For more information, see [Load historical or missed files](/user-guide/data-load-snowpipe-manage#label-snowpipe-load-historic-data).

### Snowpipe stops loading after an Amazon SNS subscription is deleted

The first time that you create a pipe that references an Amazon SNS topic, Snowflake subscribes a Snowflake-owned Amazon SQS queue to the topic. If an AWS administrator deletes that subscription, every pipe that references the topic stops receiving event notifications.

Before you recreate the pipes, note when each one stopped loading, as described in [Load missed files after you fix a problem](#label-snowpipe-ts-recover), so that you can load the files that it missed afterward. Then use one of the following options:

- Wait 72 hours after the subscription was deleted, until Amazon SNS clears it, and then recreate every pipe that references the topic, with the same topic in the pipe definition. For more information, see the [Amazon SNS documentation](https://aws.amazon.com/premiumsupport/knowledge-center/sns-cross-account-subscription/).
- To avoid the 72-hour wait, create an SNS topic with a different name, and then recreate the pipes with the new topic.

For the steps to create a pipe that uses SNS, see [Step 3: Create a pipe with auto-ingest enabled](/user-guide/data-load-snowpipe-auto-s3#label-create-pipe-auto-ingest-s3).

### Files in Azure Data Lake Storage Gen2 don’t load

Some third-party clients don’t call `FlushWithClose` in the Azure Data Lake Storage Gen2 REST API. Without that call, Azure doesn’t send the event that tells Snowpipe that a file is ready. To load these files, call the Azure Data Lake Storage Gen2 REST API yourself to flush and close the files. For more information, see the [Microsoft documentation for the Flush method](https://learn.microsoft.com/en-us/dotnet/api/azure.storage.files.datalake.datalakefileclient.flush) and for the [Path Update operation](https://learn.microsoft.com/en-us/rest/api/storageservices/datalakestoragegen2/path/update).

If your clients do call `FlushWithClose`, check that the Event Grid subscription for the storage account doesn’t filter out `FlushWithClose` events. For the supported events, see [Automating Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure). After you fix the filter, load the files that arrived before the fix, as described in [Load historical or missed files](/user-guide/data-load-snowpipe-manage#label-snowpipe-load-historic-data).

### Loads from Google Cloud Storage are delayed or files are missed

If Snowpipe loads only one file and then stops reading event notifications, or if loads from Google Cloud Storage are delayed by minutes to a day or more, the Snowflake service account usually doesn’t have the `Monitoring Viewer` role. To grant the role, see [Step 2: Grant Snowflake Access to the Pub/Sub Subscription](/user-guide/data-load-snowpipe-auto-gcs#label-snowpipe-gcs-grant-pubsub-access). After you grant the role, load any files that the pipe missed, as described in [Load historical or missed files](/user-guide/data-load-snowpipe-manage#label-snowpipe-load-historic-data).

### Automated loading doesn’t work across government and commercial regions

The government regions of the cloud providers don’t allow event notifications to be sent to or from commercial regions. As a result, automated loading doesn’t work when the account is in a commercial region and the bucket is in a government region, or the reverse. For more information, see [AWS GovCloud (US)](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-s3.html) and [Azure Government](https://learn.microsoft.com/en-us/azure/azure-government/).

## Files don’t load with the REST API

If your application calls the Snowpipe REST API, check the following:

- **Authentication**: The REST API uses either key pair authentication with a JSON Web Token (JWT) or workload identity federation. The Snowflake Ingest SDKs for Java and Python generate the JWT for you. If you call the endpoints directly, you get the token yourself. A request with an invalid or expired token returns HTTP error `401`. For more information, see [Authentication and access control](/user-guide/data-load-snowpipe-rest-overview#label-snowpipe-rest-authentication). If Snowflake rejects the JWT, see [JWT token is invalid](#label-snowpipe-ts-jwt-invalid).
- **Invalid requests**: HTTP error `400` means that the request is invalid. For example, the request has no files, a file path is longer than 1,024 bytes, a required parameter is missing or invalid, or the pipe is a clone in the `STOPPED_CLONED` state. Correct the request before you send it again. For a cloned pipe, see [Pipe execution states](#label-snowpipe-ts-execution-states).
- **Pipe name and privileges**: HTTP error `404` means that Snowflake doesn’t recognize the pipe name, or that the role has no privileges on the pipe or on the database and schema that contain it. HTTP error `403` means that the role has privileges on the pipe, but not the privilege that the endpoint requires. For more information, see [Grant access privileges](/user-guide/data-load-snowpipe-rest-gs#label-snowpipe-rest-endpoints-access-control).
- **Load status**: Call the `insertReport` or `loadHistoryScan` endpoint to see what happened to the files that you submitted. For more information, see [Snowpipe REST API reference](/user-guide/data-load-snowpipe-rest-apis).
- **Rate limits**: HTTP error `429` means that a request exceeded a rate limit or, for `insertFiles`, contained more than 5,000 files. If `insertFiles` returns `429`, Snowflake didn’t queue the files. Split lists of more than 5,000 files into smaller requests, and submit the files again after a delay. Wait longer between retries if the error repeats. If `loadHistoryScan` returns `429`, call it less often and with a narrower time range, or use `insertReport` instead. For more information, see [Handle errors and retries](/user-guide/data-load-snowpipe-rest-overview#label-snowpipe-rest-errors) and [`pipe_throttled` events](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-pipe-throttled).
- **The pipe and the files**: Complete [the diagnostic steps](#label-snowpipe-ts-diagnose) to check the pipe status and the copy history.

## Modified or corrected files don’t load

Snowpipe ignores any file whose path and name match a file in the pipe’s [load metadata](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-load-metadata), which records the files that the pipe processed in the last 14 days, including files that failed to load. Snowpipe ignores a matching file even if you modify it or run `ALTER PIPE ... REFRESH`. Truncating the target table doesn’t clear the pipe’s load metadata.

To load a corrected or modified file, see [Reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files).

## Duplicate data in the target table

To find files that loaded more than once, and which pipe or `COPY INTO` statement loaded them, query the copy history. Use a role that has the `MONITOR` privilege on the pipe. Without it, the `PIPE_NAME` column is `NULL` for Snowpipe loads, and the query reports them as `COPY INTO` loads:

Copy code

```
SELECT file_name,
       COUNT(*) AS load_count,
       ARRAY_AGG(COALESCE(pipe_name, 'COPY INTO')) AS loaded_by
  FROM TABLE(mydb.INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'myschema.orders',
    START_TIME => DATEADD('day', -14, CURRENT_TIMESTAMP())))
  WHERE status IN ('Loaded', 'Partially loaded')
  GROUP BY file_name
  HAVING COUNT(*) > 1;
```

The table function covers only the last 14 days and doesn’t return loads by a pipe that was dropped or recreated. To find duplicates from a recreated pipe, or from a file that was staged again after 14 days, query the [COPY\_HISTORY view](/sql-reference/account-usage/copy_history) instead:

Copy code

```
SELECT file_name,
       COUNT(*) AS load_count,
       ARRAY_AGG(COALESCE(pipe_name, 'COPY INTO')) AS loaded_by
  FROM SNOWFLAKE.ACCOUNT_USAGE.COPY_HISTORY
  WHERE table_catalog_name = 'MYDB'
    AND table_schema_name = 'MYSCHEMA'
    AND table_name = 'ORDERS'
    AND status IN ('Loaded', 'Partially loaded')
    AND last_load_time >= DATEADD('day', -90, CURRENT_TIMESTAMP())
  GROUP BY file_name
  HAVING COUNT(*) > 1;
```

If rows appear in the target table more than once, check for the following causes:

- **Overlapping pipes**: Two pipes that load from overlapping paths, such as `<storage_location>/path1/` and `<storage_location>/path1/path2/`, both load the files in the inner path. To compare the paths in your pipe definitions, run [SHOW PIPES](/sql-reference/sql/show-pipes) or query the [PIPES view](/sql-reference/account-usage/pipes).
- **A path without a trailing slash**: A stage URL such as `s3://mybucket/orders`, or a pipe path such as `orders`, also matches `orders_archive/`, so a pipe can load files from folders that you didn’t intend. If another pipe loads that folder, both pipes load the same files. End stage URLs and pipe paths with a forward slash (`/`). For more information, see [Best practices](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-best-practices).
- **Bulk loads of the same files**: `COPY INTO` and Snowpipe keep separate load metadata, so a `COPY INTO` statement that loads files from the same location as a pipe can load them again.
- **Files staged again after 14 days**: Snowpipe loads a file with the same name again after the file’s record in the pipe’s load metadata expires.
- **A recreated pipe**: Recreating a pipe drops its load metadata, so `ALTER PIPE ... REFRESH` can load files again afterward. For the safe procedure, see [Recreate a pipe safely](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps).
- **A cloned pipe**: After you resume a pipe in a cloned database or schema, it receives event notifications for new files in the location that it watches, like the source pipe. If its `COPY INTO` statement names the target table as `db.schema.table`, or as `schema.table` in a cloned schema, it loads the data into the source table, not the clone. For more information, see [Pipe execution states](#label-snowpipe-ts-execution-states).
- **A partial load followed by a reload**: If a pipe uses `ON_ERROR = CONTINUE`, the rows that loaded from a file with errors stay in the table when you reload the file.

## Common error messages

The following sections describe common Snowpipe error messages and how to resolve them. These messages appear in the `FIRST_ERROR_MESSAGE` column of the copy history, in the `error` field of `SYSTEM$PIPE_STATUS`, or in Snowpipe events.

### Remote file was not found

You might see the following error message:

```
Remote file '<file_url>' was not found. There are several potential causes. The file might not exist. The required credentials may be missing or invalid.
```

Snowpipe received a notification for a file, but it couldn’t find the file when it tried to load it. Check the following:

- **The file still exists**: Confirm that the file is at the path in the error message. If an application or a lifecycle rule deletes or moves files before Snowpipe loads them, change the application or rule so that it waits until Snowpipe loads the files. For more information, see [Delete files after Snowpipe loads them](/user-guide/data-load-snowpipe-manage#label-snowpipe-delete-data-files).
- **The stage credentials are valid**: Confirm that the storage integration or credentials for the stage still grant access to the location.
- **No other load removed the file**: If you also load the same files with `COPY INTO` and `PURGE = TRUE`, that load can delete a file before Snowpipe loads it. Don’t purge files that a pipe also loads.

After you fix the problem, load the files that failed. For more information, see [Load missed files after you fix a problem](#label-snowpipe-ts-recover).

### Access denied errors

You might see either of the following error messages:

```
Failed to access remote file: access denied. Please check your credentials
```

```
Failure using stage area. Cause: [Access Denied (Status Code: 403; Error Code: AccessDenied)]
```

Your cloud storage service rejected Snowflake’s request to read the stage location or the file. Verify the storage integration or credentials for the stage, and check the permissions that they grant on the bucket or container and on the files to load. For the permissions that each cloud requires, see [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3), [Automating Snowpipe for Google Cloud Storage](/user-guide/data-load-snowpipe-auto-gcs), or [Automating Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure). After you fix the permissions, load the files that failed. For more information, see [Load missed files after you fix a problem](#label-snowpipe-ts-recover).

### JWT token is invalid

You might see the following error message:

```
snowflake.ingest.error.IngestResponseError: Http Error: 401, Vender Code: 390144, Message: JWT token is invalid.
```

A call to the Snowpipe REST API included a JSON Web Token that Snowflake couldn’t validate. Check the following:

- The token is signed with the private key whose public key is assigned to the user. Run `DESCRIBE USER` and confirm that `RSA_PUBLIC_KEY_FP` or `RSA_PUBLIC_KEY_2_FP` matches the fingerprint in the token.
- The account identifier and user name in the token use all uppercase characters.
- The token hasn’t expired. A token is valid for at most one hour after it’s issued.

For more information, see [Set up the Snowpipe REST API](/user-guide/data-load-snowpipe-rest-gs) and [Authenticating to the server](/developer-guide/sql-api/authenticating).

### Error: Integration `{0}` associated with the stage `{1}` cannot be found

Copy code

```
003139=SQL compilation error:\nIntegration ''{0}'' associated with the stage ''{1}'' cannot be found.
```

This error can occur when the association between the external stage and the storage
integration linked to the stage has been broken. This happens when the storage integration
object has been recreated (using
[CREATE OR REPLACE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration)).
A stage links to a storage integration using a hidden ID rather than the name of the storage
integration. Behind the scenes, the CREATE OR REPLACE syntax drops the object and recreates
it with a different hidden ID.

If you must recreate a storage integration after it has been linked to one or more stages,
you must reestablish the association between each stage and the storage integration by
executing [ALTER STAGE](/sql-reference/sql/alter-stage)
`stage_name` SET STORAGE\_INTEGRATION = `storage_integration_name`, where:

- `stage_name` is the name of the stage.
- `storage_integration_name` is the name of the storage integration.

After you set the stage’s `STORAGE_INTEGRATION` parameter, the pipes that reference the stage use the integration for their next load, so you don’t need to recreate them. To load the files that failed while the integration was missing, see [Load missed files after you fix a problem](#label-snowpipe-ts-recover).

## Load times recorded with CURRENT\_TIMESTAMP are earlier than expected

If a column captures the load time with `CURRENT_TIMESTAMP` as a default value or in the pipe’s `COPY INTO` statement, its values can be a few hours earlier than the `LAST_LOAD_TIME` values that the [COPY\_HISTORY](/sql-reference/functions/copy_history) table function or the [COPY\_HISTORY view](/sql-reference/account-usage/copy_history) returns. The difference occurs because Snowflake evaluates [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp) when it compiles the load operation in cloud services, rather than when it commits the rows to the table.

All of the following functions have this problem, so don’t use them to record load times, either in a pipe’s `COPY INTO` statement or as a column default value:

- `CURRENT_DATE`
- `CURRENT_TIME`
- `CURRENT_TIMESTAMP`
- `GETDATE`
- `LOCALTIME`
- `LOCALTIMESTAMP`
- `SYSDATE`
- `SYSTIMESTAMP`

Instead, to record when each row is loaded, enable [row timestamps](/user-guide/data-engineering/row-timestamps) on the target table (`ROW_TIMESTAMP = TRUE`) and query the `METADATA$ROW_LAST_COMMIT_TIME` metadata column, which records when each row was last committed. Keep the following in mind:

- Rows that were loaded before you enabled row timestamps have a `NULL` value.
- If a row is updated after it loads, the value reflects the update, not the load.
- Row timestamps aren’t supported for Iceberg tables.
