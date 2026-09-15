# Refresh external tables automatically for Google Cloud Storage

You can trigger external table metadata refreshes by using
[Google Cloud Pub/Sub](https://cloud.google.com/storage/docs/reporting-changes) messages for Google Cloud Storage (GCS) events.

## Prerequisites

Before you proceed, ensure you meet the following prerequisites:

> - A role that has the CREATE STAGE and CREATE EXTERNAL TABLE privileges on a schema.
> - Administrative access to Google Cloud (GC). If you aren’t a GC administrator, ask your GC
>   administrator to complete the prerequisite steps.
> - Only `OBJECT_DELETE` and `OBJECT_FINALIZE` events trigger refreshes for external table metadata.
>   To reduce costs, event noise, and latency, send only supported events for external tables.
> - External tables don’t support storage versioning (S3 versioning, Object Versioning in Google Cloud Storage, or versioning for Azure Storage).

## Cloud platform support

Triggering automated external metadata refreshes by using GCS Pub/Sub event messages is supported by Snowflake accounts
hosted on Google Cloud (GC).

## Configure secure access to Cloud Storage

Important

If you have already configured secure access to the GCS bucket that stores your data files, you can skip this section and proceed to [Configure automation using GCS Pub/Sub](#configure-automation-using-gcs-pubsub).

You must configure a Snowflake storage integration object to delegate authentication responsibility for cloud storage
to a Snowflake identity and access management (IAM) entity.

This section describes how to use storage integrations to allow Snowflake to read data from and write to a Google Cloud Storage bucket referenced in an external
(that is, Cloud Storage) stage. Integrations are named, first-class Snowflake objects that avoid the need for passing explicit cloud provider credentials such as
secret keys or access tokens; instead, integration objects reference a Cloud Storage service account. An administrator in your organization grants the service
account permissions in the Cloud Storage account.

Administrators can also restrict users to a specific set of Cloud Storage buckets (and optional paths) accessed by external stages that use the integration.

Note

- Completing the instructions in this section requires access to your Cloud Storage project as a project editor. If you are not a project
  editor, ask your Cloud Storage administrator to perform these tasks.
- Confirm that Snowflake supports the Google Cloud Storage region that your storage is hosted in. For more information, see
  [Supported cloud regions](/user-guide/intro-regions).

The following diagram shows the integration flow for a Cloud Storage stage:

![Google Cloud Storage Stage Integration Flow](/static/images/storage-integration-gcs.png)

1. An external (that is, Cloud Storage) stage references a storage integration object in its definition.
2. Snowflake automatically associates the storage integration with a Cloud Storage service account created for your account. Snowflake creates a single service account that is referenced by all GCS storage integrations in your Snowflake account.
3. A project editor for your Cloud Storage project grants permissions to the service account to access the bucket referenced in the stage definition. Note that many external stage objects can reference different buckets and paths and use the same integration for authentication.

When a user loads or unloads data from or to a stage, Snowflake verifies the permissions granted to the service account on the bucket before allowing or denying access.

**In this Section:**

## Step 1: Create a Cloud Storage integration in Snowflake

Create an integration using the [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration) command. An integration is a Snowflake object that delegates authentication responsibility for external cloud storage to a Snowflake-generated entity (that is, a Cloud Storage service account). For accessing Cloud Storage buckets, Snowflake creates a service account that can be granted permissions to access the bucket(s) that store your data files.

A single storage integration can support multiple external (that is, GCS) stages. The URL in the stage definition must align with the GCS buckets (and optional paths) specified for the STORAGE\_ALLOWED\_LOCATIONS parameter.

Note

Only account administrators (users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute this SQL command.

Copy code

```
CREATE STORAGE INTEGRATION <integration_name>
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'GCS'
  ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('gcs://<bucket>/<path>/', 'gcs://<bucket>/<path>/')
  [ STORAGE_BLOCKED_LOCATIONS = ('gcs://<bucket>/<path>/', 'gcs://<bucket>/<path>/') ]
```

Where:

- `integration_name` is the name of the new integration.
- `bucket` is the name of a Cloud Storage bucket that stores your data files (for example, `mybucket`). The required STORAGE\_ALLOWED\_LOCATIONS parameter and optional STORAGE\_BLOCKED\_LOCATIONS parameter restrict or block access to these buckets, respectively, when stages that reference this integration are created or modified.
- `path` is an optional path that can be used to provide granular control over objects in the bucket.

The following example creates an integration that explicitly limits external stages that use the integration to reference either of two buckets and paths. In a later step, we will create an external stage that references one of these buckets and paths.

Additional external stages that also use this integration can reference the allowed buckets and paths:

> Copy code
>
> ```
> CREATE STORAGE INTEGRATION gcs_int
>   TYPE = EXTERNAL_STAGE
>   STORAGE_PROVIDER = 'GCS'
>   ENABLED = TRUE
>   STORAGE_ALLOWED_LOCATIONS = ('gcs://mybucket1/path1/', 'gcs://mybucket2/path2/')
>   STORAGE_BLOCKED_LOCATIONS = ('gcs://mybucket1/path1/sensitivedata/', 'gcs://mybucket2/path2/sensitivedata/');
> ```

## Step 2: Retrieve the Cloud Storage service account for your Snowflake account

Execute the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command to retrieve the ID for the Cloud Storage service account that was created automatically for your Snowflake account:

Copy code

```
DESC STORAGE INTEGRATION <integration_name>;
```

Where:

> - `integration_name` is the name of the integration you created in [Step 1: Create a Cloud Storage integration in Snowflake](#step-1-create-a-cloud-storage-integration-in-snowflake) (in this topic).

For example:

> Copy code
>
> ```
> DESC STORAGE INTEGRATION gcs_int;
>
> +-----------------------------+---------------+-----------------------------------------------------------------------------+------------------+
> | property                    | property_type | property_value                                                              | property_default |
> +-----------------------------+---------------+-----------------------------------------------------------------------------+------------------|
> | ENABLED                     | Boolean       | true                                                                        | false            |
> | STORAGE_ALLOWED_LOCATIONS   | List          | gcs://mybucket1/path1/,gcs://mybucket2/path2/                               | []               |
> | STORAGE_BLOCKED_LOCATIONS   | List          | gcs://mybucket1/path1/sensitivedata/,gcs://mybucket2/path2/sensitivedata/   | []               |
> | STORAGE_GCP_SERVICE_ACCOUNT | String        | service-account-id@project1-123456.iam.gserviceaccount.com                  |                  |
> +-----------------------------+---------------+-----------------------------------------------------------------------------+------------------+
> ```

The STORAGE\_GCP\_SERVICE\_ACCOUNT property in the output shows the Cloud Storage service account created for your Snowflake account (that is, `service-account-id@project1-123456.iam.gserviceaccount.com`). We provision a single Cloud Storage service account for your entire Snowflake account. All Cloud Storage integrations use that service account.

## Step 3: Grant the service account permissions to access bucket objects

The following step-by-step instructions describe how to configure IAM access permissions for Snowflake in your Google Cloud console so that you can use a Cloud Storage bucket to load and unload data:

### Create a custom IAM role

Create a custom role that has the permissions required to access the bucket and get objects.

1. Sign in to the Google Cloud console as a project editor.
2. From the home dashboard, select **IAM & Admin** » **Roles**.
3. Select **Create Role**.
4. Enter a **Title** and optional **Description** for the custom role.
5. Select **Add Permissions**.
6. Filter the list of permissions, and add the following from the list:

   > | Action(s) | Required permissions |
   > | --- | --- |
   > | Data loading only | - `storage.buckets.get` - `storage.objects.get` - `storage.objects.list` |
   > | Data loading with purge option, executing the REMOVE command on the stage | - `storage.buckets.get` - `storage.objects.delete` - `storage.objects.get` - `storage.objects.list` |
   > | Data loading and unloading | - `storage.buckets.get` (for calculating data transfer costs) - `storage.objects.create` - `storage.objects.delete` - `storage.objects.get` - `storage.objects.list` |
   > | Data unloading only | - `storage.buckets.get` - `storage.objects.create` - `storage.objects.delete` - `storage.objects.list` |
   > | Using [COPY FILES](/sql-reference/sql/copy-files) to copy files to an external stage | You must have the following additional permissions:  - `storage.multipartUploads.abort` - `storage.multipartUploads.create` - `storage.multipartUploads.list` - `storage.multipartUploads.listParts` |
   >
   > Expand
   >
   > Show lessSee more
7. Select **Add**.
8. Select **Create**.

### Assign the custom role to the Cloud Storage Service Account

1. Sign in to the Google Cloud console as a project editor.
2. From the home dashboard, select **Cloud Storage** » **Buckets**.
3. Filter the list of buckets, and select the bucket that you specified when you created your storage integration.
4. Select **Permissions** » **View by principals**, then select **Grant access**.
5. Under **Add principals**, paste the name of the service account name that you retrieved from the DESC STORAGE INTEGRATION command output.
6. Under **Assign roles**, select the custom IAM role that you created previously, then select **Save**.

Important

If your Google Cloud organization was created on or after May 3, 2024, Google Cloud enforces a
[domain restriction constraint](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-domains)
in project organization policies. The default constraint lists your domain as the only allowed value.

To allow the Snowflake service account access to your storage, you must
[update the domain restriction](/user-guide/data-load-gcs-allow).

### Grant the Cloud Storage service account permissions on the Cloud Key Management Service cryptographic keys

Note

This step is required only if your GCS bucket is encrypted using a key stored in the Google Cloud Key Management Service (Cloud KMS).

1. Sign in to the Google Cloud console as a project editor.
2. From the home dashboard, search for and select **Security** » **Key Management**.
3. Select the key ring that is assigned to your GCS bucket.
4. Click **SHOW INFO PANEL** in the upper-right corner. The information panel for the key ring slides out.
5. Click the **ADD PRINCIPAL** button.
6. In the **New principals** field, search for the service account name from the DESCRIBE INTEGRATION output in [Step 2: Retrieve the Cloud Storage service account for your Snowflake account](#step-2-retrieve-the-cloud-storage-service-account-for-your-snowflake-account) (in this topic).
7. From the **Select a role** dropdown, select the `Cloud KMS CrytoKey Encryptor/Decryptor` role.
8. Click the **Save** button. The service account name is added to the **Cloud KMS CrytoKey Encryptor/Decryptor** role dropdown in the information panel.

Note

You can use the [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](/sql-reference/functions/system_validate_storage_integration)
function to validate the configuration for your storage integration.

# Configure automation using GCS Pub/Sub

## Prerequisites

The instructions in this topic assume the following items have been created and configured:

GCP account:
:   - Pub/Sub topic that receives event messages from the GCS bucket. For more information, see [Create the Pub/Sub topic](#create-the-pub-sub-topic) (in this topic).
    - Subscription that receives event messages from the Pub/Sub topic. For more information, see [Create the Pub/Sub subscription](#create-the-pub-sub-subscription) (in this topic).

    For instructions, see the [Pub/Sub documentation](https://cloud.google.com/pubsub/docs).

Snowflake:
:   - Target table in the Snowflake database where your data will be loaded.

### Create the Pub/Sub topic

Create a Pub/Sub topic using [Cloud Shell](https://cloud.google.com/shell) or [Cloud SDK](https://cloud.google.com/sdk).

Execute the following command to create the topic and enable it to listen for activity in the specified GCS bucket:

Copy code

```
$ gsutil notification create -t <topic> -f json -e OBJECT_FINALIZE -e OBJECT_DELETE gs://<bucket-name>
```

Where:

- `topic` is the name for the topic.
- `bucket-name` is the name of your GCS bucket.

If the topic already exists, the command uses it; otherwise, a new topic is created.

For more information, see [Using Pub/Sub notifications for Cloud Storage](https://cloud.google.com/storage/docs/reporting-changes) in the Pub/Sub documentation.

### Create the Pub/Sub subscription

Create a subscription with pull delivery to the Pub/Sub topic using the Cloud Console, `gcloud` command-line tool, or the Cloud Pub/Sub API. For instructions, see [Managing topics and subscriptions](https://cloud.google.com/pubsub/docs/admin) in the Pub/Sub documentation.

Note

- Only Pub/Sub subscriptions that use the default pull delivery are supported with Snowflake. Push delivery is not supported.

### Retrieve the Pub/Sub subscription ID

The Pub/Sub topic subscription ID is used in these instructions to allow Snowflake access to event messages.

1. Log into the Google Cloud Platform Console as a project editor.
2. From the home dashboard, choose **Big Data** » **Pub/Sub** » **Subscriptions**.
3. Copy the ID in the **Subscription ID** column for the topic subscription

## Step 1: Create a notification integration in Snowflake

Create a notification integration using the
[CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration-queue-inbound-gcp) command.

The notification integration references your Pub/Sub subscription. Snowflake associates the notification integration with a GCS
service account created for your account. Snowflake creates a single service account that is referenced by all GCS notification
integrations in your Snowflake account.

Note

- Only account administrators (users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute this SQL command.
- The GCS service account for notification integrations is different from the service account created for storage integrations.
- A single notification integration supports a single Google Cloud Pub/Sub subscription. Referencing the same Pub/Sub subscription in multiple notification integrations can result in missing data in target tables because event notifications are split between notification integrations.

Copy code

```
CREATE NOTIFICATION INTEGRATION <integration_name>
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = GCP_PUBSUB
  ENABLED = true
  GCP_PUBSUB_SUBSCRIPTION_NAME = '<subscription_id>';
```

Where:

- `integration_name` is the name of the new integration.
- `subscription_id` is the subscription name you recorded in [Retrieve the Pub/Sub subscription ID](#retrieve-the-pub-sub-subscription-id).

For example:

Copy code

```
CREATE NOTIFICATION INTEGRATION my_notification_int
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = GCP_PUBSUB
  ENABLED = true
  GCP_PUBSUB_SUBSCRIPTION_NAME = 'projects/project-1234/subscriptions/sub2';
```

## Step 2: Grant Snowflake access to the Pub/Sub subscription

1. Execute the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command to retrieve the Snowflake service account ID:

   Copy code

   ```
   DESC NOTIFICATION INTEGRATION <integration_name>;
   ```

   Where:

   - `integration_name` is the name of the integration you created in [Step 1: Create a Notification Integration in Snowflake](#step-1-create-a-notification-integration-in-snowflake).

   For example:

   > Copy code
   >
   > ```
   > DESC NOTIFICATION INTEGRATION my_notification_int;
   > ```
2. Record the service account name in the GCP\_PUBSUB\_SERVICE\_ACCOUNT column, which has the following format:

   Copy code

   ```
   <service_account>@<project_id>.iam.gserviceaccount.com
   ```
3. Log into the Google Cloud Platform Console as a project editor.
4. From the home dashboard, choose **Big Data** » **Pub/Sub** » **Subscriptions**.
5. Select the subscription to configure for access.
6. Click **SHOW INFO PANEL** in the upper-right corner. The information panel for the subscription slides out.
7. Click the **ADD PRINCIPAL** button.
8. In the **New principals** field, search for the service account name you recorded.
9. From the **Select a role** dropdown, select **Pub/Sub Subscriber**.
10. Click the **Save** button. The service account name is added to the **Pub/Sub Subscriber** role dropdown in the information panel.
11. Navigate to the **Dashboard** page in the Cloud Console, and select your project from the dropdown list.
12. Click the **ADD PEOPLE TO THIS PROJECT** button.
13. Add the service account name you recorded.
14. From the **Select a role** dropdown, select **Monitoring Viewer**.
15. Click the **Save** button. The service account name is added to the **Monitoring Viewer** role.

### (Optional) Step 3: Create a stage

Create an external stage that references your GCS bucket by using the [CREATE STAGE](/sql-reference/sql/create-stage) command. Snowflake reads your
staged data files into the external table metadata. Alternatively, you can use an existing external stage.

Note

- To configure secure access to the cloud storage location, see [Configure secure access to Cloud Storage](#configure-secure-access-to-cloud-storage) earlier in this topic.
- To reference a storage integration in the CREATE STAGE statement, the role must have the USAGE privilege on the storage integration
  object.

The following example creates a stage named `mystage` in the active schema for the user session. The cloud storage URL includes the
path `files`. The stage references a storage integration named `my_storage_int`:

> Copy code
>
> ```
> USE SCHEMA mydb.public;
>
> CREATE STAGE mystage
>   URL='gcs://load/files/'
>   STORAGE_INTEGRATION = my_storage_int;
> ```

### Step 4: Create an external table

Create an external table by using the [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table) command.

For example, create an external table in the `mydb.public` schema that reads JSON data from files staged in the `mystage` stage with
the `path1/` path.

The INTEGRATION parameter references the `my_notification_int` notification integration you created in
[Step 1: Create a notification integration in Snowflake](#step-1-create-a-notification-integration-in-snowflake). You must enter the integration name in all uppercase letters.

The `AUTO_REFRESH` parameter is `TRUE` by default:

Copy code

```
CREATE OR REPLACE EXTERNAL TABLE ext_table
 INTEGRATION = 'MY_NOTIFICATION_INT'
 WITH LOCATION = @mystage/path1/
 FILE_FORMAT = (TYPE = JSON);
```

After you complete this step, the external stage with auto-refresh is configured.

When new or updated data files are added to the GCS bucket, the event notification informs Snowflake to scan them into the external
table metadata.

### Step 5: Manually refresh the external table metadata

Manually refresh the external table metadata once by using [ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table) with the REFRESH parameter; for example:

> Copy code
>
> ```
> ALTER EXTERNAL TABLE ext_table REFRESH;
>
> +---------------------------------------------+----------------+-------------------------------+
> | file                                        | status         | description                   |
> |---------------------------------------------+----------------+-------------------------------|
> | files/path1/file1.json                      | REGISTERED_NEW | File registered successfully. |
> | files/path1/file2.json                      | REGISTERED_NEW | File registered successfully. |
> | files/path1/file3.json                      | REGISTERED_NEW | File registered successfully. |
> +---------------------------------------------+----------------+-------------------------------+
> ```

This step synchronizes the metadata with the list of files in the stage and path in the external table definition. Also, this step ensures
that the external table can read the data files in the specified stage and path, and that no files were missed in the external table definition.

If the list of files in the `file` column doesn’t match your expectations, verify the paths in the external table definition and
external stage definition. Any path in the external table definition is appended to any path specified in the stage definition. For more
information, see [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table).

Important

If this step is not completed successfully at least once after the external table is created, querying the external table returns no
results until a Pub/Sub notification refreshes the external table metadata automatically for the first time.

This step ensures that the metadata is synchronized with any changes to the file list that occurred after Step 4. Thereafter, Pub/Sub
notifications trigger the metadata refresh automatically.

### Step 6: Configure security

For each additional role that you will use to query the external table, grant sufficient access control privileges on the various
objects (that is, the databases, schemas, stage, and table) by using [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege):

| Object | Privilege | Notes |
| --- | --- | --- |
| Database | USAGE |  |
| Schema | USAGE |  |
| Named stage | USAGE , READ |  |
| Named file format | USAGE | Optional; only needed if the stage you created in [(Optional) Step 3: Create a stage](#optional-step-3-create-a-stage) references a named file format. |
| External table | SELECT |  |

Expand

Show lessSee more
