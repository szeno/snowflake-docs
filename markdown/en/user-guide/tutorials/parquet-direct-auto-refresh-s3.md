# Tutorial: Auto-refresh a Parquet Direct table from Amazon S3

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

## Introduction

This tutorial shows you how to create a [Parquet Direct](/user-guide/tables-iceberg-parquet-direct) table: a read-only
Apache Iceberg™ table in Snowflake that queries Apache Parquet™ files in your Amazon S3 bucket in place. You configure
Amazon Simple Notification Service (SNS) so that Snowflake receives an event notification whenever files are added to or
deleted from the bucket, and refreshes the table automatically.

### What you’ll learn

In this tutorial, you’ll learn how to do the following:

- Configure an Amazon SNS topic to deliver S3 event notifications to Snowflake.
- Create an external volume that uses the SNS topic.
- Create a catalog integration for Parquet files.
- Create a Parquet Direct table with schema inference, schema evolution, and auto-refresh.
- Verify that new files are registered automatically, and monitor auto-refresh.

### Prerequisites

- A Snowflake role with the following privileges:

  - CREATE EXTERNAL VOLUME on the account.
  - CREATE INTEGRATION on the account, to create the catalog integration.
  - CREATE ICEBERG TABLE on the schema where you create the table.
  - USAGE on a warehouse to query the table.
- An Amazon S3 bucket that contains, or will contain, your Parquet files.
- Administrative access to AWS, to create an SNS topic, configure S3 event notifications, and create IAM roles and policies.
  If you aren’t an AWS administrator, ask your administrator to complete the AWS steps.

Note

Auto-refresh is billed as serverless compute, and each refresh incurs data registration charges for the files it adds.
For more information, see [Billing](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-billing).

## Step 1: Create an Amazon SNS topic and subscription

1. Create an SNS topic in your AWS account to handle all messages for the Snowflake external volume location in your S3
   bucket. For instructions, see the [Amazon SNS documentation](https://aws.amazon.com/documentation/sns/).
2. Configure event notifications on the S3 bucket to publish object create and delete events to the SNS topic.
3. Optional: Subscribe other target destinations for the S3 event notifications (for example, other Amazon SQS queues or AWS
   Lambda workloads) to this topic. SNS publishes event notifications for your bucket to all subscribers to the topic.

## Step 2: Allow S3 to publish to the SNS topic

1. Sign in to the AWS Management Console.
2. From the home dashboard, select **Simple Notification Service** (SNS).
3. In the left navigation pane, select **Topics**.
4. Select the topic for your S3 bucket, then select **Edit**.
5. Select **Access policy - Optional** to expand this area of the page.
6. Merge the IAM policy addition below into the JSON document.

   Copy code

   ```
   {
     "Sid":"s3-event-notifier",
     "Effect":"Allow",
     "Principal":{
       "Service":"s3.amazonaws.com"
     },
     "Action":"SNS:Publish",
     "Resource":"arn:aws:sns:us-west-2:001234567890:s3_mybucket",
     "Condition":{
       "ArnLike":{
         "aws:SourceArn":"arn:aws:s3:*:*:s3_mybucket"
       }
     }
   }
   ```

## Step 3: Subscribe the Snowflake SQS queue to your SNS topic

1. From the SNS Topic page for your S3 bucket, note the topic ARN.
2. In Snowflake, call the [SYSTEM$GET\_AWS\_SNS\_IAM\_POLICY](/sql-reference/functions/system_get_aws_sns_iam_policy) system function with your SNS topic
   ARN:

   Copy code

   ```
   SELECT SYSTEM$GET_AWS_SNS_IAM_POLICY('<sns_topic_arn>');
   ```

   The function returns an IAM policy that grants a Snowflake SQS queue permission to subscribe to the SNS topic.
3. Return to the AWS Management Console page for your S3 bucket’s SNS Topic.
4. Select **Access policy - Optional** to expand this area of the page.
5. Merge the IAM policy addition from the SYSTEM$GET\_AWS\_SNS\_IAM\_POLICY function results into the JSON document. This allows Snowflake to subscribe to your SNS topic.

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
         "Action": [
           "sns:Subscribe"
         ],
         "Resource": [
           "arn:aws:sns:us-west-2:001234567890:s3_mybucket"
         ]
       }
     ]
   }
   ```

   The final policy will look similar to the following, which both allows S3 to publish to the SNS topic and allows Snowflake to subscribe to the topic:

   Copy code

   ```
   {
     "Version":"2008-10-17",
     "Id":"__default_policy_ID",
     "Statement":[
       {
         "Sid":"__default_statement_ID",
         "Effect":"Allow",
         "Principal":{
           "AWS":"*"
         }
         ..
       },
       {
         "Sid":"1",
         "Effect":"Allow",
         "Principal":{
           "AWS":"arn:aws:iam::123456789001:user/vj4g-a-abcd1234"
         },
         "Action":[
           "sns:Subscribe"
         ],
         "Resource":[
           "arn:aws:sns:us-west-2:001234567890:s3_mybucket"
         ]
       },
       {
         "Sid":"s3-event-notifier",
         "Effect":"Allow",
         "Principal":{
           "Service":"s3.amazonaws.com"
         },
         "Action":"SNS:Publish",
         "Resource":"arn:aws:sns:us-west-2:001234567890:s3_mybucket",
         "Condition":{
           "ArnLike":{
             "aws:SourceArn":"arn:aws:s3:*:*:s3_mybucket"
           }
         }
       }
     ]
   }
   ```
6. Select **Save changes**.

## Step 4: Create an external volume with your SNS topic

Complete the instructions in [Configure an external volume for Amazon S3](/user-guide/tables-iceberg-configure-external-volume-s3) to create the IAM policy and role
that give Snowflake read access to your bucket. When you create the external volume in Snowflake, specify the following
additional parameter on the storage location:

`AWS_SNS_TOPIC = 'sns_topic_arn'`
:   Specifies the Amazon Resource Name (ARN) of the Amazon SNS topic that handles all messages for your external volume location.

For example:

Copy code

```
CREATE OR REPLACE EXTERNAL VOLUME parquet_s3_exvol
  STORAGE_LOCATIONS = (
    (
      NAME = 'my-s3-us-east-1'
      STORAGE_PROVIDER = 'S3'
      STORAGE_BASE_URL = 's3://s3_mybucket/'
      STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::0123456789102:role/my-role'
      AWS_SNS_TOPIC = 'arn:aws:sns:us-east-1:0123456789102:sns_topic'
    )
  );
```

Parquet Direct only reads from your storage, so a read-only permission set is sufficient. For the read-only
permissions for each cloud provider, see [Read-only vs write access for Delta Direct on each storage provider](/user-guide/tables-iceberg-metadata#label-tables-iceberg-ev-delta-read-write-options).

## Step 5: Create a catalog integration

Create a catalog integration by using the [CREATE CATALOG INTEGRATION (Object storage)](/sql-reference/sql/create-catalog-integration-object-storage) command. Choose
the table format that matches how your files are organized:

- If your files use Hive-style `key=value` partitioning (for example, `orders/year=2024/month=01/part-0000.parquet`), use
  `TABLE_FORMAT = HIVE` so that Snowflake infers partition columns from the paths:

  Copy code

  ```
  CREATE OR REPLACE CATALOG INTEGRATION hive_catalog_int
    CATALOG_SOURCE = OBJECT_STORE
    TABLE_FORMAT = HIVE
    ENABLED = TRUE;
  ```
- Otherwise, use `TABLE_FORMAT = NONE`:

  Copy code

  ```
  CREATE OR REPLACE CATALOG INTEGRATION parquet_catalog_int
    CATALOG_SOURCE = OBJECT_STORE
    TABLE_FORMAT = NONE
    ENABLED = TRUE;
  ```

## Step 6: Create a Parquet Direct table

Create a table by using the [CREATE ICEBERG TABLE (Parquet files in object storage)](/sql-reference/sql/create-iceberg-table-parquet) command with `AUTO_REFRESH = TRUE`.
The following example omits the column list, so Snowflake infers the schema from your Parquet files. It also sets
`ENABLE_SCHEMA_EVOLUTION = TRUE` so that Snowflake evolves the schema on later refreshes:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE orders
  EXTERNAL_VOLUME = 'parquet_s3_exvol'
  CATALOG = 'hive_catalog_int'
  BASE_LOCATION = 'inbound/orders/'
  ENABLE_SCHEMA_EVOLUTION = TRUE
  AUTO_REFRESH = TRUE;
```

Give each table its own `BASE_LOCATION` that doesn’t overlap with other tables. For more information, see
[Give each table its own storage folder](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-best-practices-disjoint).

Tip

If the base location already contains a very large number of files, create the table with `REFRESH_ON_CREATE = FALSE` and
`AUTO_REFRESH = FALSE`, then enable auto-refresh, so the table is queryable immediately while existing files register in
the background. For more information, see [Use auto-refresh when creating large tables](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-best-practices-create).

## Step 7: Verify auto-refresh

1. Query the table to confirm that Snowflake registered the existing files:

   Copy code

   ```
   SELECT COUNT(*) FROM orders;
   ```
2. Add a new Parquet file to the table’s base location; for example, by using the AWS CLI:

   Copy code

   ```
   aws s3 cp part-0002.parquet s3://s3_mybucket/inbound/orders/year=2025/month=02/
   ```
3. Check the auto-refresh status. An `executionState` of `RUNNING` means auto-refresh is healthy:

   Copy code

   ```
   SELECT SYSTEM$PARQUET_DIRECT_AUTO_REFRESH_STATUS('orders');
   ```

   For a description of each field, see [SYSTEM$PARQUET\_DIRECT\_AUTO\_REFRESH\_STATUS](/sql-reference/functions/system_parquet_direct_auto_refresh_status).
4. After a short time, confirm that the new file was registered:

   Copy code

   ```
   SELECT operation_time, file_name, operation_status, message
     FROM TABLE(INFORMATION_SCHEMA.ICEBERG_TABLE_FILE_REGISTRATION_HISTORY(TABLE_NAME => 'orders'))
     ORDER BY operation_time DESC
     LIMIT 10;
   ```

   Query the table again to see the new rows.

If the file doesn’t appear, see [Troubleshooting](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-troubleshooting). To set up ongoing monitoring and
alerts, see [Monitor refresh](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-monitoring).

## Clean up

To remove the objects that you created in this tutorial, run the following commands. Dropping the table doesn’t delete
your Parquet files in Amazon S3.

Copy code

```
DROP ICEBERG TABLE orders;
DROP CATALOG INTEGRATION hive_catalog_int;
DROP CATALOG INTEGRATION parquet_catalog_int;
DROP EXTERNAL VOLUME parquet_s3_exvol;
```

If you no longer need them, also remove the SNS topic, the S3 event notification configuration, and the IAM role and
policy in AWS.

## What’s next

- Learn about best practices, monitoring, troubleshooting, and billing in [Parquet Direct](/user-guide/tables-iceberg-parquet-direct).
- See all parameters in [CREATE ICEBERG TABLE (Parquet files in object storage)](/sql-reference/sql/create-iceberg-table-parquet).
