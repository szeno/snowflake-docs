# Automate Snowpipe for Amazon S3

This topic describes how to set up a pipe that loads files from an Amazon S3 bucket as soon as they arrive. When a file lands in the bucket, Amazon S3 sends an event notification to an Amazon Simple Queue Service (SQS) queue that Snowflake manages, and Snowpipe loads the file into your target table. For an overview of automated loading on every cloud provider, see [Automate Snowpipe with cloud event notifications](/user-guide/data-load-snowpipe-auto).

To have [CoCo](/user-guide/cortex-code/cortex-code) set up the pipeline from your S3 path instead, see [Set up continuous file ingestion with CoCo](/user-guide/data-load-snowpipe-auto-coco). After you approve a temporary access request in the AWS Management Console, Snowflake creates the IAM role and its trust policy, connects bucket notifications, and creates the storage integration, stage, and pipe, so that you don’t need to follow the steps in this topic manually. Temporary access isn’t available for AWS GovCloud or China deployments. CoCo can also generate Terraform or CloudFormation for your team to deploy.

To set up automated loading from Amazon S3, complete the following steps:

1. [Create a storage integration and an external stage](#label-data-load-snowpipe-secure-access-s3) so that Snowflake can read the bucket.
2. [Choose how Amazon S3 notifies Snowpipe](#label-data-load-snowpipe-auto-s3-choose): directly through Amazon SQS, through Amazon Simple Notification Service (SNS), or through Amazon EventBridge. Then create the pipe and connect event notifications to it by following the option for that method.
3. [Test the pipe](#label-data-load-snowpipe-auto-s3-verify).
4. [Load the files that are already in the bucket](#label-data-load-snowpipe-auto-s3-existing-files).

The examples in this topic load JSON files from the `s3://mybucket/orders/` path into the `mydb.myschema.orders` table. They use the `orders_pipe_owner` role from [Create a role to own the pipe (recommended)](#label-data-load-snowpipe-auto-s3-owner-role). If you skip that section, use a role that has the required privileges.

## Before you begin

Make sure that you have the following:

- **A target table.** Snowpipe loads files into an existing standard table or [Apache Iceberg™ table](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-iceberg).
- **Snowflake privileges.** The role that creates the pipe needs the privileges in the **Create a pipe** column of [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control). Creating a storage integration also requires the `CREATE INTEGRATION` privilege on the account, which only the `ACCOUNTADMIN` role has by default.
- **AWS permissions.** You need permission to create IAM policies and roles, and to configure event notifications on the bucket. To use Amazon SNS, you also need permission to create and edit SNS topics. To use Amazon EventBridge, you need permission to create and edit both EventBridge rules and SNS topics.

## Create a role to own the pipe (recommended)

Snowpipe loads files with the privileges of the role that owns the pipe. To follow the principle of least privilege, create a role that has only the privileges that the pipe needs, and create the pipe with that role. If you create the pipe with a different role, you can [transfer ownership](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-transfer-ownership) later, but you must pause the pipe to do so.

For example, the following statements create a role named `orders_pipe_owner` that can create a pipe that loads the `orders` table. After you create the stage in [Step 1](#label-data-load-snowpipe-secure-access-s3), you also grant the role the `USAGE` privilege on the stage.

Copy code

```
USE ROLE SECURITYADMIN;

CREATE ROLE IF NOT EXISTS orders_pipe_owner;

GRANT USAGE ON DATABASE mydb TO ROLE orders_pipe_owner;
GRANT USAGE, CREATE PIPE ON SCHEMA mydb.myschema TO ROLE orders_pipe_owner;
GRANT INSERT ON TABLE mydb.myschema.orders TO ROLE orders_pipe_owner;

-- Let users with the SYSADMIN role use and manage the new role.
GRANT ROLE orders_pipe_owner TO ROLE SYSADMIN;
```

## Step 1: Create a storage integration and an external stage

Snowpipe reads files through an external stage that points to your bucket. If you already have an external stage for the path that you want to load, make sure that its URL ends with a forward slash (`/`). If you created a role to own the pipe, grant it the `USAGE` privilege on the stage, as shown at the end of this step. Then continue with [Step 2](#label-data-load-snowpipe-auto-s3-choose).

Snowflake recommends that the stage use a storage integration, so that you don’t store AWS credentials in Snowflake. To create the IAM policy, the IAM role, and the storage integration, follow Steps 1 through 5 in [Option 1: Configure a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration). For other ways to give Snowflake access to your bucket, see [Configuring secure access to Amazon S3](/user-guide/data-load-s3-config).

Then create the stage with the [CREATE STAGE](/sql-reference/sql/create-stage) command. Creating a stage that uses a storage integration requires the `CREATE STAGE` privilege on the schema and the `USAGE` privilege on the integration. If you just created the pipe owner role, switch from the `SECURITYADMIN` role to a role that has these privileges. For example:

Copy code

```
CREATE STAGE mydb.myschema.orders_stage
  URL = 's3://mybucket/orders/'
  STORAGE_INTEGRATION = my_s3_int;
```

Important

End the stage URL with a forward slash (`/`). Without it, the stage also includes every folder and file whose name starts with the same characters. For example, `s3://mybucket/orders` also includes `s3://mybucket/orders_archive/`, so the pipe loads files that you didn’t intend.

To confirm that Snowflake can read the bucket, list the files in the stage:

Copy code

```
LIST @mydb.myschema.orders_stage;
```

If the command returns an access error, check the storage integration with [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](/sql-reference/functions/system_validate_storage_integration).

If you created a role to own the pipe, grant it the `USAGE` privilege on the stage:

Copy code

```
GRANT USAGE ON STAGE mydb.myschema.orders_stage TO ROLE orders_pipe_owner;
```

## Step 2: Choose how Amazon S3 notifies Snowpipe

Every method delivers events about new files to the Snowflake-managed SQS queue for your pipe. They differ in what sits between your bucket and that queue. Amazon S3 doesn’t let two event notifications on a bucket send the same event types for overlapping paths, so the right method depends mostly on whether other applications already receive notifications from the bucket. The following table compares the methods:

| Method | Use it when | What you configure |
| --- | --- | --- |
| [Amazon SQS](#label-data-load-snowpipe-auto-s3-option-1) | No other application receives event notifications for the path that your pipe loads, and you don’t plan to replicate the pipe to another account. This is the simplest method. | An S3 event notification that sends events to the pipe’s SQS queue. |
| [Amazon SNS](#label-configuring-amazon-sns-for-snowpipe) | Other applications already receive, or will receive, event notifications for the path that your pipe loads. Also use Amazon SNS if you plan to replicate pipes to another account or set up [multi-location resilience](/user-guide/multi-location-resilience-data-pipelines). | An SNS topic that receives the S3 event notifications, and a pipe that references the topic. Snowflake subscribes its SQS queue to the topic. |
| [Amazon EventBridge](#label-data-load-snowpipe-auto-s3-eventbridge) | You already route S3 events through EventBridge, or you need EventBridge rules to filter or route events. | An EventBridge rule that sends S3 events to an SNS topic, and then the same setup as for Amazon SNS. |

Expand

Show lessSee more

Complete one of the following options, and then continue with [Step 3](#label-data-load-snowpipe-auto-s3-verify).

If you start with Amazon SQS and later need to replicate pipes or share the bucket’s notifications, you can move every pipe for a bucket to Amazon SNS with one call to [SYSTEM$CONVERT\_PIPES\_SQS\_TO\_SNS](/sql-reference/functions/system_convert_pipes_sqs_to_sns). For more information, see [Migrate to Amazon Simple Notification Service (SNS)](/user-guide/account-replication-stages-pipes-load-history#label-account-replication-stages-pipes-load-history-migrate-to-sns).

### Option 1: Send S3 event notifications to Amazon SQS

With this method, you create the pipe first, so that Snowflake can tell you which SQS queue to send event notifications to. Then you configure an event notification on the bucket that sends events to that queue.

#### Create the pipe

Create the pipe with the [CREATE PIPE](/sql-reference/sql/create-pipe) command, and set `AUTO_INGEST = TRUE`. Before you create the pipe, check that its location doesn’t overlap the location of another pipe, as described in [Give each pipe its own location](/user-guide/data-load-snowpipe-auto#label-snowpipe-auto-pipe-paths). For example, the following statement creates a pipe named `orders_pipe` that loads JSON files from the `orders_stage` stage into the `orders` table:

Copy code

```
USE ROLE orders_pipe_owner;

CREATE PIPE mydb.myschema.orders_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO mydb.myschema.orders
    FROM @mydb.myschema.orders_stage
    FILE_FORMAT = (TYPE = 'JSON')
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

To load only part of the stage, add a path after the stage name in the `FROM` clause, such as `@mydb.myschema.orders_stage/2026/`. End the path with a forward slash (`/`).

#### Configure event notifications

1. Get the Amazon Resource Name (ARN) of the pipe’s SQS queue from the `notification_channel` column in the output of [DESCRIBE PIPE](/sql-reference/sql/desc-pipe):

   Copy code

   ```
   DESC PIPE mydb.myschema.orders_pipe;
   ```

   The ARN looks like `arn:aws:sqs:us-west-2:123456789001:sf-snowpipe-AIDA1234567890EXAMPLE-AbCdEfGhIjKlMnOpQrStUv`. Snowflake reuses one SQS queue for the pipes in your account that load from buckets in the same AWS region, so pipes that load from the same bucket usually show the same ARN. When the queue’s access policy reaches its size limit, Snowflake creates another queue in the region, so always check the ARN for each new pipe.
2. In the [Amazon S3 console](https://console.aws.amazon.com/s3/), open your bucket, and then select **Properties** » **Event notifications** » **Create event notification**.
3. Complete the fields as follows, and then select **Save changes**:

   - **Event name**: A name for the notification, such as `snowpipe-orders`.
   - **Prefix**: The path that the pipe loads, such as `orders/`. To cover every pipe on the bucket with one notification, leave the prefix empty.
   - **Suffix**: Optionally, a file extension to filter events by, such as `.json`.
   - **Event types**: **All object create events** (`s3:ObjectCreated:*`). If you select individual event types instead, include `s3:ObjectCreated:CompleteMultipartUpload`, or Snowpipe doesn’t load files that are uploaded in parts. For more information, see [Large files in Amazon S3 don’t load](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-s3-multipart).
   - **Destination**: **SQS queue**.
   - **Specify SQS queue**: **Enter SQS queue ARN**, and then paste the ARN from step 1.

   For more information, see [Enabling and configuring event notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/enable-event-notifications.html) in the Amazon S3 documentation.

If you save the notification and Amazon S3 reports that the configuration overlaps an existing one, another notification on the bucket already sends the same events for an overlapping path. If that notification already sends events to the queue ARN that `DESC PIPE` returned, you don’t need a second one. Make sure that its prefix, suffix, and event types cover the files that the pipe loads, and edit it if they don’t. Only widen the prefix, suffix, or event types, because other pipes might rely on the same notification. If that notification sends events to a different destination, Amazon S3 doesn’t allow both notifications. Drop the pipe with [DROP PIPE](/sql-reference/sql/drop-pipe), and then use [Amazon SNS](#label-configuring-amazon-sns-for-snowpipe) instead, or use [Amazon EventBridge](#label-data-load-snowpipe-auto-s3-eventbridge), which doesn’t require you to change the existing notification.

A notification with a broad prefix, or no prefix, also sends events for files that no pipe loads. Snowpipe ignores these events, but a high volume of them can slow down how quickly Snowpipe finds the events for your pipes. To limit the events that Amazon S3 sends, create one notification for each path or file extension that your pipes load. For more information, see [Event notification filtering](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html) in the Amazon S3 documentation.

Next, [test the pipe](#label-data-load-snowpipe-auto-s3-verify).

### Option 2: Send S3 event notifications through Amazon SNS

With this method, Amazon S3 sends event notifications to an Amazon SNS topic. Amazon SNS delivers each notification to every subscriber of the topic, including the Snowflake-managed SQS queue for your pipe, so other applications can receive the same notifications. Snowpipe supports SNS topics that are encrypted with AWS Key Management Service (KMS). If the topic uses a customer managed key, the key policy must let the service that publishes to the topic, such as Amazon S3 (`s3.amazonaws.com`) or EventBridge (`events.amazonaws.com`), use the `kms:GenerateDataKey` and `kms:Decrypt` actions. Don’t use the AWS managed key for Amazon SNS (`alias/aws/sns`), because you can’t change its key policy. For more information, see [Encryption at rest](https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html) in the Amazon SNS documentation.

#### Create the SNS topic and the S3 event notification

If your bucket already sends event notifications to an SNS topic for the path that the pipe loads, note the topic’s ARN. Make sure that the notification’s prefix, suffix, and event types cover the files that the pipe loads, as described in step 3 of [Configure event notifications](#label-data-load-snowpipe-auto-s3-configure-sqs), and edit it if they don’t. Then continue with [Let Snowflake subscribe to the topic](#label-create-sns-topic-subscription).

1. In the [Amazon SNS console](https://console.aws.amazon.com/sns/), create a standard topic in the same AWS region as your bucket. Note the topic’s ARN, such as `arn:aws:sns:us-west-2:001234567890:s3_mybucket`. For more information, see [Creating an Amazon SNS topic](https://docs.aws.amazon.com/sns/latest/dg/sns-create-topic.html) in the Amazon SNS documentation.
2. In the Amazon SNS console, open the topic, select **Edit**, and then expand **Access policy**. Add a statement to the `Statement` array that lets Amazon S3 publish to the topic, using your topic ARN and bucket name, and then select **Save changes**. For example:

   Copy code

   ```
   {
     "Sid": "s3-event-notifier",
     "Effect": "Allow",
     "Principal": {
       "Service": "s3.amazonaws.com"
     },
     "Action": "SNS:Publish",
     "Resource": "arn:aws:sns:us-west-2:001234567890:s3_mybucket",
     "Condition": {
       "ArnLike": {
         "aws:SourceArn": "arn:aws:s3:::mybucket"
       }
     }
   }
   ```
3. On the bucket, create an event notification for the path that the pipe loads, with **All object create events** as the event types and the SNS topic as the destination. Complete the fields as described in steps 2 and 3 of [Configure event notifications](#label-data-load-snowpipe-auto-s3-configure-sqs), but for **Destination**, select **SNS topic**, and then select your topic.

   If another notification on the bucket already sends the same events for an overlapping path, Amazon S3 doesn’t let you create a second one. What you do next depends on that notification’s destination:

   - **Another SNS topic**: Don’t change the notification’s destination. Use that topic instead of the one that you created in step 1, as described at the beginning of this section.
   - **A Snowflake-managed SQS queue**, which has `sf-snowpipe-` in its ARN: Follow the steps after this list.
   - **Any other destination**, such as an application’s SQS queue or AWS Lambda function: Subscribe the destination to the topic, as described in step 4, so that the application keeps receiving the notifications. Then change the notification’s destination to the SNS topic, and make sure that its prefix, suffix, and event types cover the files that the pipe loads. If you widen the prefix or suffix, the topic also sends the application the events for the pipe’s files. To keep sending the application only the events that it received before, add a [subscription filter policy](https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html) with the `MessageBody` scope to its subscription. Amazon S3 event notifications don’t have message attributes, so a filter policy with the default `MessageAttributes` scope blocks every notification.

   If the destination is a Snowflake-managed SQS queue, don’t change the notification’s destination yet, because the pipes that use the queue would stop loading files. Instead, complete the following steps:

   1. Check whether the queue belongs to your Snowflake account. Use a role that can see every pipe, external table, and stage in the account. For pipes, a role that has the `MONITOR EXECUTION` privilege can see every pipe. The queue belongs to your account if its ARN appears in any of the following places:

      - The `notification_channel` column in the output of [SHOW PIPES](/sql-reference/sql/show-pipes) with `IN ACCOUNT`. Check every pipe, not only the pipes that load from this bucket, because pipes that load from other buckets in the same AWS region can use the same queue. For a pipe that already uses an SNS topic, this column shows the topic ARN instead. For those pipes, call [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) with the same role, and check the `notificationChannelName` value, which shows the ARN of the SQS queue that the pipe uses.
      - The `notification_channel` column in the output of [SHOW EXTERNAL TABLES](/sql-reference/sql/show-external-tables) with `IN ACCOUNT`, for external tables that refresh automatically. This column is empty for external tables that [SYSTEM$CONVERT\_PIPES\_SQS\_TO\_SNS](/sql-reference/functions/system_convert_pipes_sqs_to_sns) already moved to an SNS topic.
      - The `DIRECTORY_NOTIFICATION_CHANNEL` property in the `DIRECTORY` group for each stage that has a directory table that refreshes automatically. To find these stages, run [SHOW STAGES](/sql-reference/sql/show-stages) with `IN ACCOUNT`, and look for `Y` in the `directory_enabled` column. Then run [DESCRIBE STAGE](/sql-reference/sql/desc-stage) for each of those stages, and check the property for each stage where `AUTO_REFRESH` is `true`.

      If the ARN doesn’t appear in any of these places, the queue belongs to another Snowflake account, or no object in your account uses it anymore. If you know which account uses the queue, send its administrator the bucket name and the topic’s ARN, and ask them to complete the next three steps in their account. Because the topic is in your AWS account, they send you the statement that [SYSTEM$GET\_AWS\_SNS\_IAM\_POLICY](/sql-reference/functions/system_get_aws_sns_iam_policy) returns in their account, and you add it to the topic’s access policy, as described in [Let Snowflake subscribe to the topic](#label-create-sns-topic-subscription). If their pipes already use a different topic, use that topic instead. Its access policy must include the statement from step 2 for your bucket and, before you create your pipe, the statement that `SYSTEM$GET_AWS_SNS_IAM_POLICY` returns in your account. When they finish, change the notification’s destination, as described in the final step of this list. If you can’t find out which Snowflake account uses the queue, contact [Snowflake Support](/user-guide/contacting-support) before you change the notification’s destination.
   2. Find out whether any pipe or directory table that loads from the bucket already uses an SNS topic:

      - For each pipe that loads from the bucket, run [DESCRIBE PIPE](/sql-reference/sql/desc-pipe), and check whether `notification_channel` shows a topic ARN.
      - For each stage whose directory table refreshes from the bucket, run [DESCRIBE STAGE](/sql-reference/sql/desc-stage), and check the `AWS_SNS_TOPIC` property in the `DIRECTORY` group.
      - For each external table that refreshes automatically from the bucket, check whether it was created with the `AWS_SNS_TOPIC` parameter.

      If any of them use a topic, use that topic instead of the one that you created in step 1 for the rest of this procedure, including in the function call and in the `AWS_SNS_TOPIC` parameter when you create the pipe. If you use a different topic, the pipes that use the existing topic stop loading files after you change the notification’s destination. Make sure that the topic’s access policy includes the statement from step 2, with that topic’s ARN. Then, in the Amazon SNS console, check that the topic has a subscription for the SQS queue that those objects use. For a pipe, that queue is in the `notificationChannelName` value that `SYSTEM$PIPE_STATUS` returns. For a directory table, it’s in the `DIRECTORY_NOTIFICATION_CHANNEL` property in the `DESC STAGE` output. For an external table, look for a subscription whose endpoint is a Snowflake-managed SQS queue, which has `sf-snowpipe-` in its ARN. If they use more than one topic, or if the topic has no subscription for that queue, contact [Snowflake Support](/user-guide/contacting-support) before you change the notification’s destination.
   3. Complete the steps in [Let Snowflake subscribe to the topic](#label-create-sns-topic-subscription) for the topic, and then return here and continue with the next step.
   4. With `ACCOUNTADMIN` as your primary role, call [SYSTEM$CONVERT\_PIPES\_SQS\_TO\_SNS](/sql-reference/functions/system_convert_pipes_sqs_to_sns) with the bucket name and the topic’s ARN to move the pipes that load from the bucket to the topic. The function also subscribes the queue to the topic, and it moves to the topic any external tables that refresh automatically from the bucket. Then confirm that every pipe that loads from the bucket and every directory table that refreshes from it moved to the topic, as described in the function’s usage notes.

      If the function returns an `Unrecognized bucket name` error, check the bucket name. If the name is correct, nothing in your account uses only the queue for this bucket. If you found the topic that the bucket’s pipes or directory tables use, or if no pipe, directory table, or external table in your account loads or refreshes from the bucket, continue with the next step. If only external tables refresh from the bucket, contact [Snowflake Support](/user-guide/contacting-support) before you change the notification’s destination. For other errors, see the **Returns** section of [SYSTEM$CONVERT\_PIPES\_SQS\_TO\_SNS](/sql-reference/functions/system_convert_pipes_sqs_to_sns).
   5. Change the notification’s destination to the topic, and make sure that its prefix, suffix, and event types cover the files that the pipe loads. While Amazon S3 switches to the new destination, the queue can receive two notifications for the same file, but Snowpipe doesn’t load the file twice.
4. If other applications need the event notifications, subscribe their endpoints, such as their SQS queues or AWS Lambda functions, to the topic. Make sure that each endpoint accepts messages from the topic:

   - **SQS queue**: Enable raw message delivery on the subscription so that the queue receives S3 event notifications in their original format. The queue’s access policy must let Amazon SNS (`sns.amazonaws.com`) send messages to the queue from the topic. If you subscribe the queue in the Amazon SQS console with **Subscribe to Amazon SNS topic**, the console adds this statement for you. If the queue is encrypted with a customer managed KMS key, the key policy must also let Amazon SNS use the key.
   - **AWS Lambda function**: Raw message delivery isn’t available for Lambda functions, so the function receives each S3 event notification inside an SNS message, in the `Sns.Message` field of each record. Update the function to read the event from that field. The function’s resource-based policy must also let Amazon SNS invoke the function. If you add the topic as a trigger in the Lambda console, the console adds this permission for you.

   For more information, see [Fanout to Amazon SQS queues](https://docs.aws.amazon.com/sns/latest/dg/sns-sqs-as-subscriber.html) and [Fanout to Lambda functions](https://docs.aws.amazon.com/sns/latest/dg/sns-lambda-as-subscriber.html) in the Amazon SNS documentation.

#### Let Snowflake subscribe to the topic

Before you create the pipe, allow the Snowflake-managed SQS queue to subscribe to the topic:

1. In Snowflake, call [SYSTEM$GET\_AWS\_SNS\_IAM\_POLICY](/sql-reference/functions/system_get_aws_sns_iam_policy) with the topic’s ARN:

   Copy code

   ```
   SELECT SYSTEM$GET_AWS_SNS_IAM_POLICY('arn:aws:sns:us-west-2:001234567890:s3_mybucket');
   ```

   The function returns a policy with a statement that lets the Snowflake IAM user for your account subscribe to the topic. For example:

   Copy code

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "1",
         "Effect": "Allow",
         "Principal": {
           "AWS": "arn:aws:iam::123456789001:user/vj4g-a-abcd1234"
         },
         "Action": ["sns:Subscribe"],
         "Resource": ["arn:aws:sns:us-west-2:001234567890:s3_mybucket"]
       }
     ]
   }
   ```
2. In the Amazon SNS console, open the topic, select **Edit**, and then expand **Access policy**.
3. Add the statement from the `Statement` array in the function’s output to the `Statement` array in the topic’s access policy. Keep the existing statements, including the one that lets Amazon S3 or EventBridge publish to the topic. If the policy already has the same statement, don’t add it again. If another statement in the policy has the same `Sid` value, such as `"1"`, change the `Sid` of the statement that you add to a unique value. Then select **Save changes**.

   For example, after you add the statement, the access policy contains statements similar to the following:

   Copy code

   ```
   {
     "Version": "2008-10-17",
     "Id": "__default_policy_ID",
     "Statement": [
       {
         "Sid": "__default_statement_ID",
         ...
       },
       {
         "Sid": "s3-event-notifier",
         ...
       },
       {
         "Sid": "1",
         "Effect": "Allow",
         "Principal": {
           "AWS": "arn:aws:iam::123456789001:user/vj4g-a-abcd1234"
         },
         "Action": ["sns:Subscribe"],
         "Resource": ["arn:aws:sns:us-west-2:001234567890:s3_mybucket"]
       }
     ]
   }
   ```

#### Create the pipe that uses the topic

Create the pipe with `AUTO_INGEST = TRUE` and the `AWS_SNS_TOPIC` parameter set to the topic’s ARN. When you create the first pipe that references the topic, Snowflake subscribes its SQS queue to the topic. If Snowflake can’t subscribe, the `CREATE PIPE` statement fails with a `Pipe Notifications bind failure` error. For example, Snowflake can’t subscribe if the topic’s access policy is missing the statement from [Let Snowflake subscribe to the topic](#label-create-sns-topic-subscription), or if the topic is in a different AWS region from the bucket. If the topic is in a different region, the error message includes the error from Amazon SNS, such as `Invalid parameter: TopicArn`.

Before you create the pipe, check that its location doesn’t overlap the location of another pipe, as described in [Give each pipe its own location](/user-guide/data-load-snowpipe-auto#label-snowpipe-auto-pipe-paths). The following statement creates a pipe that uses the topic:

Copy code

```
USE ROLE orders_pipe_owner;

CREATE PIPE mydb.myschema.orders_pipe
  AUTO_INGEST = TRUE
  AWS_SNS_TOPIC = 'arn:aws:sns:us-west-2:001234567890:s3_mybucket'
  AS
  COPY INTO mydb.myschema.orders
    FROM @mydb.myschema.orders_stage
    FILE_FORMAT = (TYPE = 'JSON')
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

Important

Don’t delete the subscription that Snowflake creates on the topic. If the subscription is deleted, every pipe that references the topic stops receiving event notifications. To recover, see [Snowpipe stops loading after an Amazon SNS subscription is deleted](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-sns-subscription-deleted).

Next, [test the pipe](#label-data-load-snowpipe-auto-s3-verify).

### Option 3: Send S3 events through Amazon EventBridge

With this method, Amazon S3 sends events to Amazon EventBridge, and an EventBridge rule forwards them to an SNS topic. From the topic onward, the setup is the same as for [Amazon SNS](#label-configuring-amazon-sns-for-snowpipe).

1. [Enable Amazon EventBridge](https://docs.aws.amazon.com/AmazonS3/latest/userguide/enable-event-notifications-eventbridge.html) on your bucket.
2. Create an SNS topic in the same AWS region as the bucket, as described in step 1 of [Create the SNS topic and the S3 event notification](#label-data-load-snowpipe-auto-s3-sns-topic). You don’t need the statement that lets Amazon S3 publish to the topic, or an S3 event notification.
3. Create an EventBridge rule on the default event bus in the bucket’s AWS region that matches object-created events for your bucket and path, and that has the SNS topic as its target. For example, the following event pattern matches new objects under the `orders/` path in `mybucket`:

   Copy code

   ```
   {
     "source": ["aws.s3"],
     "detail-type": ["Object Created"],
     "detail": {
       "bucket": { "name": ["mybucket"] },
       "object": { "key": [{ "prefix": "orders/" }] }
     }
   }
   ```

   Add a statement to the topic’s access policy that lets EventBridge publish to the topic. The statement is similar to the Amazon S3 statement in step 2 of [Create the SNS topic and the S3 event notification](#label-data-load-snowpipe-auto-s3-sns-topic). For example:

   Copy code

   ```
   {
     "Sid": "eventbridge-publish",
     "Effect": "Allow",
     "Principal": {
       "Service": "events.amazonaws.com"
     },
     "Action": "SNS:Publish",
     "Resource": "arn:aws:sns:us-west-2:001234567890:s3_mybucket"
   }
   ```

   For more information, see [Creating rules that react to events](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule.html) and [Amazon SNS permissions](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-use-resource-based.html#eb-sns-permissions) in the Amazon EventBridge documentation.
4. Complete the steps in [Let Snowflake subscribe to the topic](#label-create-sns-topic-subscription). Then [create the pipe with the `AWS_SNS_TOPIC` parameter](#label-data-load-snowpipe-auto-s3-sns-pipe).

Next, [test the pipe](#label-data-load-snowpipe-auto-s3-verify).

## Step 3: Test the pipe

1. Check that the pipe is running:

   Copy code

   ```
   SELECT SYSTEM$PIPE_STATUS('mydb.myschema.orders_pipe');
   ```

   The `executionState` field should be `RUNNING`. If it isn’t, see [Pipe execution states](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-execution-states).
2. Upload a test file to the path that the pipe loads. For example, with the AWS CLI:

   Copy code

   ```
   aws s3 cp orders_test.json s3://mybucket/orders/
   ```
3. After about a minute, check whether the file loaded by running the following query. Snowpipe doesn’t need a warehouse, but this query does. Replace `mywh` with a warehouse that your current role has the `USAGE` privilege on. If the `orders_pipe_owner` role can’t use a warehouse, grant it the `USAGE` privilege on one, or switch to a role that can use a warehouse and see the table’s load history. For the privileges that the query needs, see the usage notes for [COPY\_HISTORY](/sql-reference/functions/copy_history).

   Copy code

   ```
   USE WAREHOUSE mywh;

   SELECT file_name, status, row_count, first_error_message, last_load_time
     FROM TABLE(mydb.INFORMATION_SCHEMA.COPY_HISTORY(
       TABLE_NAME => 'mydb.myschema.orders',
       START_TIME => DATEADD(HOUR, -1, CURRENT_TIMESTAMP())));
   ```

   If the file has the `Loaded` status, the pipe is working. If it has the `Load in progress` status, wait, and then run the query again. If it has the `Load failed` or `Partially loaded` status, the pipe received the notification, but the file has errors. The `first_error_message` column shows the first error. For more information, see [Step 3: Get details about load errors](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-check-files).

   If the file isn’t listed, call `SYSTEM$PIPE_STATUS` again. If `lastReceivedMessageTimestamp` is missing or older than your upload, event notifications aren’t reaching Snowflake. If it’s newer than your upload but `lastForwardedMessageTimestamp` is missing or older than your upload, event notifications arrive, but none of them are for the pipe’s path. For the steps to fix these and other problems, see [Files don’t load with automated loading](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-auto-ingest).

## Step 4: Load files that are already in the bucket

The pipe loads only files that arrive after you configure event notifications. To load the files that were already in the stage, run the following command:

Copy code

```
ALTER PIPE mydb.myschema.orders_pipe REFRESH;
```

`REFRESH` queues only files that were staged within the last 7 days and that the pipe hasn’t already processed. Files that failed to load count as processed, so `REFRESH` doesn’t queue them again. To reload them, see [Reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files). To load older files, see [Files staged more than 7 days ago](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-backfill).

## After you set up the pipe

- **Add more pipes.** If you use Amazon SQS, other pipes that load from the same bucket usually use the same SQS queue. For each new pipe, compare its `notification_channel` value with the queue ARN in your event notification, as described in [Configure event notifications](#label-data-load-snowpipe-auto-s3-configure-sqs), and make sure that a notification covers the files that the new pipe loads. If the ARN is different and an existing notification for an overlapping path sends events to another queue, Amazon S3 doesn’t let you add a notification for the new ARN. In that case, drop the new pipe, and create it with [Amazon SNS](#label-configuring-amazon-sns-for-snowpipe) or [Amazon EventBridge](#label-data-load-snowpipe-auto-s3-eventbridge) instead. If you use Amazon SNS or Amazon EventBridge, create each new pipe with the same `AWS_SNS_TOPIC` value. Then make sure that the S3 event notification or EventBridge rule that publishes to the topic covers the files that the new pipe loads.
- **Let other roles monitor or operate the pipe.** To check the pipe’s status, a role needs the `USAGE` privilege on the database and schema and the `MONITOR` privilege on the pipe. To pause or resume the pipe, it also needs the `OPERATE` privilege. To refresh the pipe, it also needs privileges on the stage and the target table, as listed in the **Refresh a pipe** column of [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control). For example, run the following statements with a role that has the `MANAGE GRANTS` privilege, such as `SECURITYADMIN`:

  Copy code

  ```
  USE ROLE SECURITYADMIN;

  GRANT USAGE ON DATABASE mydb TO ROLE data_engineer;
  GRANT USAGE ON SCHEMA mydb.myschema TO ROLE data_engineer;
  GRANT MONITOR, OPERATE ON PIPE mydb.myschema.orders_pipe TO ROLE data_engineer;
  ```
- **Get notified about failed loads.** Set up [error notifications](/user-guide/data-load-snowpipe-errors) to receive a message in the messaging service on your Snowflake account’s cloud platform when a file fails to load. Set up an [alert](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-alerts) to find out when the pipe stops loading.
- **Clean up loaded files.** Snowpipe doesn’t delete files after it loads them. To manage storage costs, see [Delete files after Snowpipe loads them](/user-guide/data-load-snowpipe-manage#label-snowpipe-delete-data-files).
- **Change the notification method.** You can’t change or remove `AWS_SNS_TOPIC` with `ALTER PIPE`. To move pipes from Amazon SQS to Amazon SNS, use [SYSTEM$CONVERT\_PIPES\_SQS\_TO\_SNS](/sql-reference/functions/system_convert_pipes_sqs_to_sns), which moves every pipe for the bucket at once, as described in [Create the SNS topic and the S3 event notification](#label-data-load-snowpipe-auto-s3-sns-topic). If you instead recreate one pipe with `AWS_SNS_TOPIC`, don’t change the bucket’s event notification to send to the topic while other pipes on the bucket use only Amazon SQS, because those pipes would stop loading files. To move a pipe from Amazon SNS to Amazon SQS, recreate it without `AWS_SNS_TOPIC`, as described in [Recreate a pipe safely](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps). The recreated pipe loads files only after an event notification sends events directly to its queue. If you change a notification’s destination from the topic to the queue, the topic’s other subscribers, including pipes that use the topic, stop receiving those events.
