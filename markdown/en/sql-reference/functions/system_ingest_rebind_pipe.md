Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$INGEST\_REBIND\_PIPE

Rebinds an [auto-ingest pipe](/user-guide/data-load-snowpipe-auto) to the notification channel for its stage’s current storage location or, on a Google Cloud Storage or Microsoft Azure stage, to a notification integration that you specify.

A pipe that receives Amazon S3 event notifications directly through Amazon Simple Queue Service (SQS), without an Amazon Simple Notification Service (SNS) topic or a Multi-Queue Notification Integration (MQNI), is an SQS-only pipe. Run this function once for each existing SQS-only pipe when you configure multi-location resilience. Run it in the target account, which holds the pipe’s replica. The call is a one-time setup step: it does for one pipe what `ALTER INTEGRATION ... SET ACTIVE` does for every pipe that uses an MQNI. You don’t need to call the function for SQS-only pipes that you create later: when a refresh replicates a new pipe, Snowflake binds it to the queue for its stage’s active location in that account. Call it for such a pipe only if that queue is in the wrong region, for example because the pipe’s stage doesn’t use a Multi-Location Storage Integration. In that case, fix the stage in the primary account first, and call the function after the change replicates. The failover procedure doesn’t call the function. During failback, you call it in the source account only for a pipe that isn’t bound to the queue for your primary region, such as a pipe on the stages of a Multi-Location Storage Integration whose active location you had to correct, and you confirm that the new channel is in the region of your primary storage location. For the one-time setup procedure, see [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-sqs-rebind) in [Multi-Location Resilience for Data Pipelines](/user-guide/multi-location-resilience-data-pipelines). For the failback procedure, see step 5 of [Fail back your pipelines](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-failback-steps) in the same topic.

For multi-location resilience on Amazon S3, the other notification path is Amazon SNS with an MQNI. That path redirects every pipe with one statement, so you don’t call this function for each pipe. To compare the two paths, see [Choose a notification path for Amazon S3](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-choose-aws-notification-path).

To retry a notification channel binding that failed during replication, use [SYSTEM$PIPE\_REBINDING\_WITH\_NOTIFICATION\_CHANNEL](/sql-reference/functions/system_pipe_rebinding_with_notification_channel). That function takes only the pipe name and requires the `OWNERSHIP` or `OPERATE` privilege on the pipe rather than the `ACCOUNTADMIN` role.

See also:
:   [SYSTEM$PIPE\_REBINDING\_WITH\_NOTIFICATION\_CHANNEL](/sql-reference/functions/system_pipe_rebinding_with_notification_channel) , [SYSTEM$CONVERT\_PIPES\_SQS\_TO\_SNS](/sql-reference/functions/system_convert_pipes_sqs_to_sns) , [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status)

## Syntax

Copy code

```
SYSTEM$INGEST_REBIND_PIPE( '<pipe_name>' , '<sns_topic>' , '<integration_name>' )
```

## Arguments

`pipe_name`
:   Name of the pipe to rebind. Enclose the name in single quotes. For a fully qualified name, include the database and schema inside the single quotes: `'<db>.<schema>.<pipe_name>'`.

    If you don’t qualify the name, the function looks for the pipe in the current database and schema.

    If the pipe name is case-sensitive or includes special characters or spaces, enclose the pipe name in double quotes inside the single quotes: `'"<pipe_name>"'`.

`sns_topic`
:   Amazon Resource Name (ARN) of the Amazon SNS topic to bind the pipe to. If you pass an empty string, the function keeps the pipe’s current SNS topic.

    For Amazon SQS auto-ingest, pass an empty string (`''`). Snowflake derives the new notification channel from the stage’s current bucket region.

`integration_name`
:   Name of the notification integration to bind the pipe to. To keep the pipe on its current integration, pass the value from the pipe’s `integration` column.

    Run [DESCRIBE PIPE](/sql-reference/sql/desc-pipe) and inspect the `integration` column:

    - If the column is `NULL`, pass an empty string (`''`).
    - If the column contains an integration name, pass that name exactly. On an Amazon S3 stage, if the column names an MQNI, run `ALTER INTEGRATION ... SET ACTIVE` instead, because this function doesn’t use the SNS topic of the integration that you name.

    For a pipe on a Google Cloud Storage or Microsoft Azure stage, always pass an integration name. The function doesn’t fall back to the pipe’s current integration: if you pass an empty string, the function unbinds the pipe and then fails with an error.

## Returns

A string in one of the following forms:

- `Rebind succeeded. New storage location: <url>. New channel: <channel>.` for an auto-ingest pipe.
- `Rebind succeeded. New storage location: <url>.` for a pipe that doesn’t use auto-ingest. The function updates the pipe’s storage location and doesn’t bind a channel.
- `Rebind failed. Error: <message>` for a binding failure that the function reports in its return value.

`<url>` is the full path that the pipe loads from. `<channel>` is the new notification channel, such as the ARN of an Amazon SQS queue.

Some failures return text that starts with `Rebind failed`. Others raise an error, for example when the integration that you name doesn’t exist or is on a different cloud provider from the stage. Check for both outcomes.

## Access control requirements

Only users with the `ACCOUNTADMIN` role can run this function.

The function requires the `MODIFY` privilege on the account, which can’t be granted directly to a custom role. A role that has only the `OWNERSHIP` privilege or the `OPERATE` privilege on the pipe can’t call this function.

## Usage notes

- Before you call this function, point the pipe’s stage at the storage location whose queue you want the pipe to use: your secondary location during setup in the target account, or your primary location during failback in the source account. For multi-location resilience, the stage must use a Multi-Location Storage Integration. During setup, the stage is in a secondary database, whose objects are read-only, so you can’t change the stage’s `URL`. In both setup and failback, make sure that the storage location is active in the account where you call the function. If it isn’t, run [ALTER STORAGE INTEGRATION](/sql-reference/sql/alter-storage-integration) with `SET ACTIVE`. On an Amazon S3 stage, the function derives the new queue from the stage’s current bucket region at the time of the call.
- On an Amazon S3 stage, if the stage still resolves to the previous region, the function rebinds the pipe to that region’s queue and reports success. To verify the binding of an SQS-only pipe, check that the result starts with `Rebind succeeded` and that its `New channel` ARN names a queue in the region of the storage location that you made active. Don’t rely on `notification_channel` in `DESCRIBE PIPE` for this check, because it can still show the previous channel after a failed rebind.
- If `integration_name` names an integration other than the pipe’s current one and the rebind succeeds, the function updates the pipe’s `integration` column to that integration. On a Google Cloud Storage or Microsoft Azure stage, the function also binds the pipe to that integration’s queue. If the integration doesn’t exist or is on a different cloud provider from the stage, the function raises an error. On an Amazon S3 stage, the function doesn’t use the SNS topic of the integration that you name. It binds the pipe to `sns_topic`. If you pass an empty string for `sns_topic`, the function keeps the pipe’s current SNS topic or, for an SQS-only pipe, derives the queue from the stage’s current bucket region. To change the active queue for Amazon S3 pipes that already use an MQNI, run `ALTER INTEGRATION ... SET ACTIVE` instead.
- The function checks `integration_name`, then removes the pipe from its current notification channel, and then binds the pipe to the new channel. An error about `integration_name` leaves the current binding in place, except for an empty string on a Google Cloud Storage or Microsoft Azure stage: in that case, the function unbinds the pipe before it fails. If the new binding fails after the function removes the current channel, whether the function returns `Rebind failed` or raises an error, the pipe doesn’t receive notifications until you run the function again with the correct arguments. During that time, `DESCRIBE PIPE` can still show the previous channel.
- The function accepts an optional fourth argument that’s reserved for Snowflake use. The argument only redacts ARNs from the returned text; it doesn’t preview the rebind. Don’t specify it.
- After the function returns `Rebind succeeded` for an SQS-only pipe, run `DESCRIBE PIPE` in the account where you called the function to get the ARN of the pipe’s new queue from the `notification_channel` column. Then, on the bucket in that region, make sure that an S3 event notification that targets the queue ARN covers the pipe’s path. For instructions, see [Configure event notifications](/user-guide/data-load-snowpipe-auto-s3#label-data-load-snowpipe-auto-s3-configure-sqs) in [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3). For a pipe that has an SNS topic, `notification_channel` shows the topic instead.

## Examples

Rebind an Amazon SQS auto-ingest pipe whose `integration` column is `NULL`:

Copy code

```
SELECT SYSTEM$INGEST_REBIND_PIPE('my_db.my_schema.my_sqs_pipe', '', '');
```

The result looks like the following:

```
Rebind succeeded. New storage location: s3://my-bucket-east/my_folder/my_sub_folder/my_sqs_pipe/. New channel: arn:aws:sqs:us-east-1:123456789012:sf-snowpipe-EXAMPLE.
```

Rebind a pipe that loads from a Google Cloud Storage or Microsoft Azure stage and is associated with a single-queue notification integration. Pass the integration name exactly as the pipe’s `integration` column shows it (`MY_INTEGRATION`):

Copy code

```
SELECT SYSTEM$INGEST_REBIND_PIPE('my_db.my_schema.my_ni_pipe', '', 'MY_INTEGRATION');
```
