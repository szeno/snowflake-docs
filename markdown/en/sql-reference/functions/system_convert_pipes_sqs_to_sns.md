Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$CONVERT\_PIPES\_SQS\_TO\_SNS

Converts all the auto-ingest pipes in the current account that load data from an S3 bucket through Amazon Simple Queue Service (SQS) notifications so that they use
an Amazon Simple Notification Service (SNS) topic instead. One call converts every such pipe for the bucket; you can’t convert pipes individually. The function also subscribes the bucket’s Snowflake SQS queue to the topic.

For more information, see [Migrate to Amazon Simple Notification Service (SNS)](/user-guide/account-replication-stages-pipes-load-history#label-account-replication-stages-pipes-load-history-migrate-to-sns) and
[Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3).

If you’re configuring multi-location resilience, converting pipes to SNS is one step in moving pipes that use only Amazon SQS notifications (SQS-only pipes) onto a Multi-Queue
Notification Integration (MQNI). If you need to recreate pipes for multi-location resilience, finish recreating them before you convert them, because recreating a converted pipe from its original definition, which specifies neither `AWS_SNS_TOPIC` nor `INTEGRATION`, makes the pipe an SQS-only pipe again. Follow the procedure in [Move existing SQS-only pipes to Amazon SNS](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-sqs-to-sns). Then use `SYSTEM$CONVERT_PIPES_TO_MULTI_QUEUE` to create an MQNI from the SNS
topic that you passed to this function and an SNS topic in your secondary region, as described in
[Create the MQNI from your pipes’ queues](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-mqni-scenario-b-create).

See also:
:   [SYSTEM$GET\_AWS\_SNS\_IAM\_POLICY](/sql-reference/functions/system_get_aws_sns_iam_policy) , [SYSTEM$INGEST\_REBIND\_PIPE](/sql-reference/functions/system_ingest_rebind_pipe)

## Syntax

Copy code

```
SYSTEM$CONVERT_PIPES_SQS_TO_SNS( '<bucket_name>' , '<sns_topic_arn>' )
```

## Arguments

`bucket_name`
:   Name of the S3 bucket, without the `s3://` prefix.

`sns_topic_arn`
:   Amazon Resource Name (ARN) of the Amazon SNS topic.

## Returns

When the conversion succeeds, the function returns the following message:

```
SQS pipes associated with the bucket <bucket_name> have been successfully altered to bind with the provided SNS topic <sns_topic_arn>.
```

If `sns_topic_arn` isn’t a valid SNS topic ARN, the function raises the error `invalid value [<sns_topic_arn>] for parameter 'SNS topic Arn'` before it converts any pipes. If the conversion fails, the function raises an error with the text `Alteration to new SNS topic failed: <message>.` Values of
`<message>` include the following:

| Error | Cause | Solution |
| --- | --- | --- |
| `The bucket's region and the provided SNS's region mismatch. Please provide an SNS topic in the same region as the bucket's one.` | The S3 bucket and SNS topic aren’t in the same AWS region. | Use an SNS topic that’s in the same AWS region as the S3 bucket. |
| `Unrecognized bucket name. Either the bucket does not exist, or there is no SQS pipe associated with the bucket.` | The S3 bucket doesn’t exist, no SQS-only pipe loads from the bucket, or the bucket’s pipes were already converted. | Use the correct S3 bucket name, and verify that SQS-only pipes load data from the bucket. If you already converted the bucket’s pipes, run `DESCRIBE PIPE` to confirm that `notification_channel` shows the topic ARN. |
| `SQS to SNS pipe conversion is not supported for the bucket whose region has been modified.` | Pipes in the account load from buckets with this name in more than one AWS region, for example because the bucket was deleted and recreated in another region. | Contact [Snowflake Support](/user-guide/contacting-support). |
| `Failed to update the existing SQS queue's policy: <queue_arn>` | Snowflake couldn’t update the access policy of its SQS queue for the bucket. | Retry the call. If the error persists, contact [Snowflake Support](/user-guide/contacting-support). |
| `The existing SQS queue fails to bind with the provided SNS topic: <message>` | Snowflake couldn’t subscribe its SQS queue to the topic, usually because the topic’s access policy doesn’t allow the subscription. | Update the topic’s access policy as described in the usage notes, and then retry the call. |

Expand

Show lessSee more

## Access control requirements

Run this function with `ACCOUNTADMIN` as the primary role of your session. In an organization account, use `GLOBALORGADMIN` instead.
Using a role that inherits `ACCOUNTADMIN`, or activating `ACCOUNTADMIN` only as a secondary role, isn’t enough.

## Usage notes

- Before you call this function, update the access policy for your topic with the following permissions:

  - Allow the Snowflake AWS Identity and Access Management (IAM) user of the current account to subscribe that account’s SQS queue to your topic. If you replicate the
    pipes to a target account, also allow the Snowflake IAM user of each target account to subscribe that account’s SQS queue. Snowflake subscribes each of those queues to the topic at the
    target account’s next refresh. To get the policy statement for an account, run
    [SYSTEM$GET\_AWS\_SNS\_IAM\_POLICY](/sql-reference/functions/system_get_aws_sns_iam_policy) in that account.
  - Allow Amazon S3 to publish event notifications from your bucket to the SNS topic.

  For instructions, see [Step 1: Subscribe the Snowflake SQS Queue to the SNS Topic](/user-guide/data-load-snowpipe-auto-s3#label-create-sns-topic-subscription) in [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3).
- The function converts every SQS-only pipe in the current account that loads from the bucket, including directory table
  auto-refresh pipes. It sets the SNS topic on each converted pipe and on the stage of each directory table auto-refresh pipe.
  You can’t run `DESCRIBE PIPE` on a directory table auto-refresh pipe, so to confirm its conversion, run
  [DESCRIBE STAGE](/sql-reference/sql/desc-stage) and check that the `AWS_SNS_TOPIC` property in the `DIRECTORY` group shows the
  topic ARN.
- Call this function *before* you update your S3 bucket to send notifications to the SNS topic. Don’t update the bucket until
  `DESCRIBE PIPE` shows the topic ARN in `notification_channel` for every pipe, as described in the next note, and `DESCRIBE STAGE`
  shows it for every directory table that refreshes from the bucket, as described in the previous note.
- If a pipe was created before Snowflake began storing the metadata that this function requires, the pipe stays on Amazon SQS and the
  function returns no error. To find such pipes, run `DESCRIBE PIPE` after the call for each pipe that loads from the bucket, and
  check whether `notification_channel` still shows an Amazon SQS queue ARN instead of the topic ARN. Recreate each of those pipes by
  following [Recreating pipes](/user-guide/data-load-snowpipe-manage#label-snowpipe-management-recreate-pipes), and then call the function again. Recreating a pipe generates the
  metadata that the conversion requires, but it also drops the pipe’s load history, so make sure that the recreated pipe doesn’t
  load files that the original pipe already loaded.
- To prevent data loss, Snowpipe continues to consume messages from the SQS queue after the conversion.
- The S3 bucket and SNS topic must be in the same AWS region.

## Examples

Convert the pipes that load from the bucket `my-s3-bucket` to receive notifications from an SNS topic:

Copy code

```
SELECT SYSTEM$CONVERT_PIPES_SQS_TO_SNS(
   'my-s3-bucket', 'arn:aws:sns:us-east-2:111122223333:sns_topic');
```
