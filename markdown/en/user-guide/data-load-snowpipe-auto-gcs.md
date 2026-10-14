# Automate Snowpipe for Google Cloud Storage

This topic describes how to set up a pipe that loads files from a Google Cloud Storage bucket as soon as they arrive. When a file lands in the bucket, Google Cloud Storage publishes a message to a [Google Cloud Pub/Sub](https://cloud.google.com/storage/docs/pubsub-notifications) topic. Snowflake reads the message from a subscription to that topic, and Snowpipe loads the file into your target table. For an overview of automated loading on every cloud provider, see [Automate Snowpipe with cloud event notifications](/user-guide/data-load-snowpipe-auto).

To set up automated loading from Google Cloud Storage, complete the following steps:

1. [Create a storage integration and an external stage](#label-data-load-snowpipe-auto-gcs-stage) so that Snowflake can read the bucket.
2. [Create a Pub/Sub topic and subscription](#label-gcp-pubsub-snowpipe) that receive messages about new files.
3. [Create a notification integration](#label-data-load-snowpipe-auto-gcs-integration) that points to the subscription.
4. [Grant Snowflake access to the subscription](#label-snowpipe-gcs-grant-pubsub-access).
5. [Create the pipe](#label-data-load-snowpipe-auto-gcs-pipe).
6. [Test the pipe](#label-data-load-snowpipe-auto-gcs-verify).
7. [Load the files that are already in the bucket](#label-data-load-snowpipe-auto-gcs-existing-files).

The examples in this topic load JSON files from the `gcs://mybucket/orders/` path into the `mydb.myschema.orders` table. They use the `orders_pipe_owner` role from [Create a role to own the pipe (recommended)](#label-data-load-snowpipe-auto-gcs-owner-role). If you skip that section, use a role that has the required privileges. The Google Cloud project is named `my-project`.

## Before you begin

Make sure that you have the following:

- **A target table.** Snowpipe loads files into an existing standard table or [Apache Iceberg™ table](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-iceberg).
- **Snowflake privileges.** The role that creates the pipe needs the privileges in the **Create a pipe** column of [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control), including the `USAGE` privilege on the notification integration. Creating the storage integration and the notification integration requires the `CREATE INTEGRATION` privilege on the account, which only the `ACCOUNTADMIN` role has by default.
- **Google Cloud permissions.** You need permission to create Pub/Sub topics and subscriptions, to configure notifications on the bucket, and to grant IAM roles on the subscription and the project.
- **The Google Cloud CLI.** The examples in this topic use the [gcloud CLI](https://cloud.google.com/sdk/docs/install). You can also complete the steps in the Google Cloud console.

## Create a role to own the pipe (recommended)

Snowpipe loads files with the privileges of the role that owns the pipe. To follow the principle of least privilege, create a role that has only the privileges that the pipe needs, and create the pipe with that role. If you create the pipe with a different role, you can [transfer ownership](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-transfer-ownership) later, but you must pause the pipe to do so.

For example, the following statements create a role named `orders_pipe_owner` that can create a pipe that loads the `orders` table. In later steps, you also grant the role privileges on the stage and the notification integration.

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

Snowpipe reads files through an external stage that points to your bucket. If you already have an external stage for the path that you want to load, make sure that its URL ends with a forward slash (`/`). If you created a role to own the pipe, grant it the `USAGE` privilege on the stage, as shown at the end of this step. Then continue with [Step 2](#label-gcp-pubsub-snowpipe).

To create a storage integration, grant its service account access to the bucket, and create a stage, follow the steps in [Configure an integration for Google Cloud Storage](/user-guide/data-load-gcs-config). Creating a stage that uses a storage integration requires the `CREATE STAGE` privilege on the schema and the `USAGE` privilege on the integration. If you just created the pipe owner role, switch from the `SECURITYADMIN` role to a role that has these privileges. For example:

Copy code

```
CREATE STAGE mydb.myschema.orders_stage
  URL = 'gcs://mybucket/orders/'
  STORAGE_INTEGRATION = my_gcs_int;
```

Important

End the stage URL with a forward slash (`/`). Without it, the stage also includes every folder and file whose name starts with the same characters. For example, `gcs://mybucket/orders` also includes `gcs://mybucket/orders_archive/`, so the pipe loads files that you didn’t intend.

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

## Step 2: Create a Pub/Sub topic and subscription

Google Cloud Storage publishes a message to a Pub/Sub topic when a file is created in the bucket, and Snowflake pulls the messages from a subscription to the topic.

If you already have a Pub/Sub subscription and a notification integration for Snowflake, you can reuse them. Create a notification on the bucket that publishes to that subscription’s topic, as shown in the first step of this section. Specify the topic by its full name, such as `--topic=projects/my-project/topics/snowpipe-orders`. If you specify only the topic ID, the command looks for the topic in your default Google Cloud project and creates it there if it doesn’t exist. Then continue with [Step 5](#label-data-load-snowpipe-auto-gcs-pipe). If you created a role to own the pipe, first grant it the `USAGE` privilege on the existing integration, as shown at the end of [Step 3](#label-data-load-snowpipe-auto-gcs-integration). Use a role that owns the integration or has the `MANAGE GRANTS` privilege, such as `SECURITYADMIN`.

The commands in this step and in Step 4 use your default Google Cloud project. To use the `my-project` project from the examples, first run `gcloud config set project my-project`.

1. Create a notification on the bucket that publishes `OBJECT_FINALIZE` events for the path that the pipe loads. If the topic doesn’t exist, the command creates it and lets Google Cloud Storage publish to it:

   Copy code

   ```
   gcloud storage buckets notifications create gs://mybucket \
     --topic=snowpipe-orders \
     --event-types=OBJECT_FINALIZE \
     --object-prefix=orders/ \
     --payload-format=json
   ```

   Snowpipe loads files only for `OBJECT_FINALIZE` events, which Google Cloud Storage sends when an object is created or overwritten. Send only this event type, and set `--object-prefix` to the path that your pipes load, to reduce event noise and latency. To cover every pipe on the bucket, omit `--object-prefix`. Keep `--payload-format=json`: Snowpipe reads the file details from the JSON message body. If a message has no payload, Snowpipe discards it without reporting an error, and the file never loads. For more information, see [Configure Pub/Sub notifications for Cloud Storage](https://cloud.google.com/storage/docs/reporting-changes) in the Google Cloud documentation.
2. Create a subscription to the topic. Snowflake supports only subscriptions that use the default pull delivery type. Push subscriptions aren’t supported. By default, Pub/Sub deletes a subscription that has no subscriber activity, such as pulls, for 31 days. The example sets `--expiration-period=never` so that the subscription isn’t deleted if no pipe reads from it for a while.

   Copy code

   ```
   gcloud pubsub subscriptions create snowpipe-orders-sub \
     --topic=snowpipe-orders \
     --expiration-period=never
   ```
3. Get the full name of the subscription, which you use in [Step 3](#label-data-load-snowpipe-auto-gcs-integration):

   Copy code

   ```
   gcloud pubsub subscriptions describe snowpipe-orders-sub --format="value(name)"
   ```

   The name has the form `projects/my-project/subscriptions/snowpipe-orders-sub`.

Use this subscription only for Snowflake. If another application also pulls messages from it, each consumer receives only some of the messages, and the pipe misses files. If other applications need the same messages, create a separate subscription to the topic for each of them.

## Step 3: Create a notification integration

A notification integration is a Snowflake object that stores the name of your subscription and identifies the Google Cloud service account that Snowflake uses to read it. Create the integration with the [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration-queue-inbound-gcp) command:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE NOTIFICATION INTEGRATION my_gcs_notification_int
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = GCP_PUBSUB
  ENABLED = TRUE
  GCP_PUBSUB_SUBSCRIPTION_NAME = 'projects/my-project/subscriptions/snowpipe-orders-sub';
```

Keep the following in mind:

- Snowflake uses one service account for all of the Pub/Sub notification integrations in your account. It’s different from the service account that your storage integration uses, so you grant access to each one separately.
- Each notification integration reads from one subscription. Several pipes can use the same notification integration, but you can’t create a pipe that uses a different integration for a subscription that another pipe already reads.

If you created a role to own the pipe, grant it the `USAGE` privilege on the integration. The role needs this privilege to create a pipe that uses the integration:

Copy code

```
GRANT USAGE ON INTEGRATION my_gcs_notification_int TO ROLE orders_pipe_owner;
```

## Step 4: Grant Snowflake access to the subscription

1. Get the name of the Snowflake service account for the integration from the `GCP_PUBSUB_SERVICE_ACCOUNT` property in the output of [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration):

   Copy code

   ```
   DESC NOTIFICATION INTEGRATION my_gcs_notification_int;
   ```

   The service account name has the form `service-account-id@project-id.iam.gserviceaccount.com`.
2. Grant the service account the following roles. Replace `<service_account>` with the name from the previous step.

   - **Pub/Sub Subscriber** on the subscription, so that Snowflake can pull and acknowledge messages:

     Copy code

     ```
     gcloud pubsub subscriptions add-iam-policy-binding snowpipe-orders-sub \
       --member="serviceAccount:<service_account>" \
       --role="roles/pubsub.subscriber"
     ```
   - **Monitoring Viewer** on the project that contains the subscription, so that Snowflake can read the subscription’s metrics, such as the number of messages that are waiting:

     Copy code

     ```
     gcloud projects add-iam-policy-binding my-project \
       --member="serviceAccount:<service_account>" \
       --role="roles/monitoring.viewer"
     ```

   To grant the roles in the Google Cloud console instead, add the service account as a principal with the Pub/Sub Subscriber role on the subscription’s **Permissions** tab, and with the Monitoring Viewer role on the project’s **IAM** page. For more information, see [Access control with IAM](https://cloud.google.com/pubsub/docs/access-control) in the Google Cloud documentation.

Important

Grant both roles before you create the pipe. When you create the pipe, Snowflake checks that it can pull from the subscription and read its metrics. If either role is missing, the `CREATE PIPE` statement fails, as described in [Step 5](#label-data-load-snowpipe-auto-gcs-pipe). If the Monitoring Viewer role is removed later, Snowpipe keeps loading files, but the `numOutstandingMessagesOnChannel` field in the output of [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) is no longer accurate, and the `channelErrorMessage` field reports `no monitoring permission`. Loading can also slow down when many messages are waiting in the subscription. For more information, see [Loads from Google Cloud Storage are delayed or files are missed](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-gcs-delayed).

If your organization restricts which identities you can grant roles to, for example with domain-restricted sharing, you might need to allow the Snowflake service account. For more information, see [Allow access to Google Cloud Storage](/user-guide/data-load-gcs-allow).

## Step 5: Create the pipe

Create the pipe with the [CREATE PIPE](/sql-reference/sql/create-pipe) command. Set `AUTO_INGEST = TRUE`, and set `INTEGRATION` to the name of your notification integration as a string. The string must match the name exactly as Snowflake stores it, which is in uppercase letters unless you enclosed the name in double quotes when you created the integration. Before you create the pipe, check that its location doesn’t overlap the location of another pipe, as described in [Give each pipe its own location](/user-guide/data-load-snowpipe-auto#label-snowpipe-auto-pipe-paths). For example, the following statement creates a pipe named `orders_pipe` that loads JSON files from the `orders_stage` stage into the `orders` table:

Copy code

```
USE ROLE orders_pipe_owner;

CREATE PIPE mydb.myschema.orders_pipe
  AUTO_INGEST = TRUE
  INTEGRATION = 'MY_GCS_NOTIFICATION_INT'
  AS
  COPY INTO mydb.myschema.orders
    FROM @mydb.myschema.orders_stage
    FILE_FORMAT = (TYPE = 'JSON')
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

If the `CREATE PIPE` statement fails, check the error message:

- `Could not pull` or `Could not monitor`: The Snowflake service account doesn’t have the Pub/Sub Subscriber role on the subscription or the Monitoring Viewer role on the project. Grant the roles, as described in [Step 4](#label-snowpipe-gcs-grant-pubsub-access). If you just granted them, wait a few minutes for the change to take effect, and then run the statement again.
- `Subscription not found`: The subscription name in the notification integration is wrong, or the subscription was deleted. If the subscription was deleted, recreate it, as described in [Step 2](#label-gcp-pubsub-snowpipe), and grant the Pub/Sub Subscriber role on it again. You can’t change the subscription name with [ALTER NOTIFICATION INTEGRATION](/sql-reference/sql/alter-notification-integration-queue-inbound-gcp). Instead, create a notification integration with the correct subscription name, as described in [Step 3](#label-data-load-snowpipe-auto-gcs-integration), grant the `USAGE` privilege on it to the role that creates the pipe, and then create the pipe with the new integration.
- `Subscription needs to have pull delivery type`: The subscription uses push delivery. Change its delivery type to pull, for example with `gcloud pubsub subscriptions modify-push-config snowpipe-orders-sub --push-endpoint=""`.

To load only part of the stage, add a path after the stage name in the `FROM` clause, such as `@mydb.myschema.orders_stage/2026/`. End the path with a forward slash (`/`).

## Step 6: Test the pipe

1. Check that the pipe is running and that Snowflake can read the subscription:

   Copy code

   ```
   SELECT SYSTEM$PIPE_STATUS('mydb.myschema.orders_pipe');
   ```

   The `executionState` field should be `RUNNING`. If it isn’t, see [Pipe execution states](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-execution-states). If the output includes a `channelErrorMessage` field, check its value. An error such as `PERMISSION_DENIED` means that Snowflake can’t pull messages from the subscription. Check that the subscription still exists and that the Snowflake service account still has the Pub/Sub Subscriber role on it, as described in [Step 4](#label-snowpipe-gcs-grant-pubsub-access). A value that starts with `no monitoring permission` means that Snowflake can’t read the subscription’s metrics, but Snowpipe still loads files. To restore the metrics, grant the Monitoring Viewer role, as described in Step 4.
2. Upload a test file to the path that the pipe loads:

   Copy code

   ```
   gcloud storage cp orders_test.json gs://mybucket/orders/
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

   If the file isn’t listed, call `SYSTEM$PIPE_STATUS` again. If `lastReceivedMessageTimestamp` is missing or older than your upload, messages aren’t reaching Snowflake. If it’s newer than your upload but `lastForwardedMessageTimestamp` is missing or older than your upload, messages arrive, but none of them are for the pipe’s path. For the steps to fix these and other problems, see [Files don’t load with automated loading](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-auto-ingest).

## Step 7: Load files that are already in the bucket

The pipe loads only files that arrive after you configure notifications. To load the files that were already in the stage, run the following command:

Copy code

```
ALTER PIPE mydb.myschema.orders_pipe REFRESH;
```

`REFRESH` queues only files that were staged within the last 7 days and that the pipe hasn’t already processed. Files that failed to load count as processed, so `REFRESH` doesn’t queue them again. To reload them, see [Reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files). To load older files, see [Files staged more than 7 days ago](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-backfill).

## After you set up the pipe

- **Add more pipes.** Other pipes can use the same notification integration if the bucket notification covers their paths. To load from another bucket, create a stage for it, and make sure that the stage’s storage integration can access the bucket. Then create a notification on that bucket that publishes `OBJECT_FINALIZE` events in the JSON payload format to the same topic, as described in [Step 2](#label-gcp-pubsub-snowpipe), so that the same subscription and notification integration serve both buckets. Specify the topic by its full name, such as `--topic=projects/my-project/topics/snowpipe-orders`, so that the command doesn’t create a new topic in your default Google Cloud project. If a different role creates the new pipe, grant that role the `USAGE` privilege on the notification integration, as shown at the end of [Step 3](#label-data-load-snowpipe-auto-gcs-integration). Use a role that owns the integration or has the `MANAGE GRANTS` privilege, such as `SECURITYADMIN`. To isolate quotas and failures, you can instead create a separate topic, subscription, and notification integration for each bucket.
- **Let other roles monitor or operate the pipe.** To check the pipe’s status, a role needs the `USAGE` privilege on the database and schema and the `MONITOR` privilege on the pipe. To pause or resume the pipe, it also needs the `OPERATE` privilege. To refresh the pipe, it also needs privileges on the stage and the target table, as listed in the **Refresh a pipe** column of [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control). For example, run the following statements with a role that has the `MANAGE GRANTS` privilege, such as `SECURITYADMIN`:

  Copy code

  ```
  USE ROLE SECURITYADMIN;

  GRANT USAGE ON DATABASE mydb TO ROLE data_engineer;
  GRANT USAGE ON SCHEMA mydb.myschema TO ROLE data_engineer;
  GRANT MONITOR, OPERATE ON PIPE mydb.myschema.orders_pipe TO ROLE data_engineer;
  ```
- **Get notified about failed loads.** Set up [error notifications](/user-guide/data-load-snowpipe-errors) to receive a message in the messaging service on your Snowflake account’s cloud platform when a file fails to load. Set up an [alert](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-alerts) to find out when the pipe stops loading or Snowflake can’t read the subscription.
- **Clean up loaded files.** Snowpipe doesn’t delete files after it loads them. To manage storage costs, see [Delete files after Snowpipe loads them](/user-guide/data-load-snowpipe-manage#label-snowpipe-delete-data-files).
