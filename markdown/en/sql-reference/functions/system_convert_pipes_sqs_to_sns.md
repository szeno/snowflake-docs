Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$CONVERT\_PIPES\_SQS\_TO\_SNS

Convert pipes using Amazon SQS (Simple Queue Service) notifications to the Amazon Simple Notification Service (SNS) service for
an S3 bucket.

For more information, see [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3).

## Syntax

Copy code

```
SYSTEM$CONVERT_PIPES_SQS_TO_SNS( '<bucket_name>, '<sns_topic_arn>' )
```

## Arguments

`bucket_name`
:   Name of the S3 bucket.

`sns_topic_arn`
:   ARN of Amazon SNS topic.

## Access control requirements

Only account administrators can execute this function.

## Usage notes

- Before you call this function, update the access policy for your topic with the following permissions:

  - Allow the Snowflake IAM user to subscribe the SQS queue that is in your *target* account
    to your topic.
  - Allow Amazon S3 to publish event notifications from your bucket to the SNS topic.

  For instructions, see [Step 1: Subscribe the Snowflake SQS Queue to the SNS Topic](/user-guide/data-load-snowpipe-auto-s3#label-create-sns-topic-subscription).
- Call this function *before* you update your S3 bucket to send notifications to the SNS topic.
- To prevent any data loss, Snowpipe will continue to consume messages from the SQS queue.
- The S3 bucket and SNS topic must be in the same AWS region.

## Examples

Convert all notifications from bucket `my_s3_bucket`:

Copy code

```
SELECT SYSTEM$CONVERT_PIPES_SQS_TO_SNS(
   'my_s3_bucket', 'arn:aws:sns:us-east-2:111122223333:sns_topic');
```
