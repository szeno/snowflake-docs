# Tutorial: Auto-refresh a Parquet Direct table from Google Cloud Storage

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

## Introduction

This tutorial shows you how to create a [Parquet Direct](/user-guide/tables-iceberg-parquet-direct) table: a read-only
Apache Iceberg™ table in Snowflake that queries Apache Parquet™ files in your Google Cloud Storage (GCS) bucket in place.
You configure Google Cloud Pub/Sub so that Snowflake is notified when files are added to or removed from the bucket, and
refreshes the table automatically.

### What you’ll learn

In this tutorial, you’ll learn how to do the following:

- Create a Pub/Sub topic and subscription for GCS object events.
- Create a notification integration and grant Snowflake access to the subscription.
- Create an external volume that uses the subscription.
- Create a catalog integration for Parquet files.
- Create a Parquet Direct table with schema inference, schema evolution, and auto-refresh.
- Verify that new files are registered automatically, and monitor auto-refresh.

### Prerequisites

- A Snowflake role with the following privileges:

  - CREATE EXTERNAL VOLUME on the account.
  - CREATE INTEGRATION on the account, to create the notification integration and catalog integration.
  - CREATE ICEBERG TABLE on the schema where you create the table.
  - USAGE on a warehouse to query the table.
- A GCS bucket that contains, or will contain, your Parquet files.
- Administrative access to Google Cloud, to create a Pub/Sub topic and subscription and manage IAM permissions.
  If you aren’t a Google Cloud administrator, ask your administrator to complete the Google Cloud steps.

Note

Auto-refresh is billed as serverless compute, and each refresh incurs data registration charges for the files it adds.
For more information, see [Billing](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-billing).

## Step 1: Create a Pub/Sub topic and subscription

Set up Google Cloud Pub/Sub so that your GCS bucket sends event notifications to Snowflake.

### Create the Pub/Sub topic

Use [Cloud Shell](https://cloud.google.com/shell) or the [Cloud SDK](https://cloud.google.com/sdk) to create a Pub/Sub topic
that listens for object create and delete events in your bucket:

Copy code

```
gsutil notification create -t <topic> -f json -e OBJECT_FINALIZE -e OBJECT_DELETE gs://<bucket_name>
```

Where:

- `topic` is the name for the topic. If the topic already exists, the command uses it;
  otherwise, the command creates a new topic.
- `bucket_name` is the name of your GCS bucket.

For more information, see [Pub/Sub notifications for Cloud Storage](https://cloud.google.com/storage/docs/reporting-changes).

### Create the Pub/Sub subscription

Create a subscription with pull delivery to the Pub/Sub topic by using the Google Cloud console, the `gcloud` command-line
tool, or the Cloud Pub/Sub API. For instructions, see
[Managing topics and subscriptions](https://cloud.google.com/pubsub/docs/admin).

Note

Snowflake supports only Pub/Sub subscriptions that use the default pull delivery. Push delivery isn’t supported.

### Retrieve the Pub/Sub subscription ID

Record the subscription ID. You use it when you create the notification integration and the external volume.

1. Sign in to the Google Cloud console as a project editor.
2. Navigate to **Pub/Sub** » **Subscriptions**.
3. Copy the ID in the **Subscription ID** column for the topic subscription. The full name has the following format:

   ```
   projects/<project_id>/subscriptions/<subscription_name>
   ```

## Step 2: Create a notification integration

Create a notification integration by using the [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration) command. Use the
subscription ID that you recorded:

Copy code

```
CREATE NOTIFICATION INTEGRATION parquet_gcs_notification_int
  ENABLED = TRUE
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = GCP_PUBSUB
  GCP_PUBSUB_SUBSCRIPTION_NAME = 'projects/project-1234/subscriptions/sub2';
```

## Step 3: Grant Snowflake access to the Pub/Sub subscription

Grant the Snowflake service account permission to consume messages from your Pub/Sub subscription.

1. Run the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command:

   Copy code

   ```
   DESC NOTIFICATION INTEGRATION parquet_gcs_notification_int;
   ```

   Note the value in the `GCP_PUBSUB_SERVICE_ACCOUNT` column. This value is the email address of the Snowflake service
   account that you grant access to.
2. In the Google Cloud console, navigate to **Pub/Sub** » **Subscriptions**.
3. Select the subscription that you created, and select **Add Principal**.
4. Add the Snowflake service account email address from the `GCP_PUBSUB_SERVICE_ACCOUNT` column.
5. Grant the service account the **Pub/Sub Subscriber** role (`roles/pubsub.subscriber`).

## Step 4: Create an external volume with your Pub/Sub subscription

Complete the instructions in [Configure an external volume for Google Cloud Storage](/user-guide/tables-iceberg-configure-external-volume-gcs) to create an external volume and
grant Snowflake read access to your bucket. When you create the external volume, specify the following additional parameter
on the storage location:

`GCP_PUBSUB_SUBSCRIPTION_NAME = 'subscription_id'`
:   Specifies the Google Cloud Pub/Sub subscription that handles event messages for your external volume location.

For example:

Copy code

```
CREATE OR REPLACE EXTERNAL VOLUME parquet_gcs_exvol
  STORAGE_LOCATIONS = (
    (
      NAME = 'my-gcs-us-central1'
      STORAGE_PROVIDER = 'GCS'
      STORAGE_BASE_URL = 'gcs://my_parquet_bucket/'
      GCP_PUBSUB_SUBSCRIPTION_NAME = 'projects/project-1234/subscriptions/sub2'
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
  EXTERNAL_VOLUME = 'parquet_gcs_exvol'
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
2. Upload a new Parquet file to the table’s base location; for example, by using the Google Cloud CLI:

   Copy code

   ```
   gcloud storage cp part-0002.parquet gs://my_parquet_bucket/inbound/orders/year=2025/month=02/
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
your Parquet files in Google Cloud Storage.

Copy code

```
DROP ICEBERG TABLE orders;
DROP CATALOG INTEGRATION hive_catalog_int;
DROP CATALOG INTEGRATION parquet_catalog_int;
DROP EXTERNAL VOLUME parquet_gcs_exvol;
DROP NOTIFICATION INTEGRATION parquet_gcs_notification_int;
```

If you no longer need them, also delete the Pub/Sub subscription, the Pub/Sub topic, and the bucket notification
configuration in Google Cloud.

## What’s next

- Learn about best practices, monitoring, troubleshooting, and billing in [Parquet Direct](/user-guide/tables-iceberg-parquet-direct).
- Compare Parquet Direct with Delta Direct in [Direct Iceberg tables](/user-guide/tables-iceberg-direct).
- See all parameters in [CREATE ICEBERG TABLE (Parquet files in object storage)](/sql-reference/sql/create-iceberg-table-parquet).
