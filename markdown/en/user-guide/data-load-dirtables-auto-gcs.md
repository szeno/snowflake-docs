# Refresh directory tables automatically for Google Cloud Storage

This topic provides instructions for triggering directory table metadata refreshes using
[Google Cloud Pub/Sub](https://cloud.google.com/storage/docs/reporting-changes) messages for Google Cloud Storage (GCS) events.

Note

To complete the steps described in this topic, you must use a role that has the CREATE STAGE privilege on a schema.

In addition, you must have administrative access to Google Cloud (GC). If you are not a GCP administrator, ask your GCP
administrator to complete the `Prerequisites`\_ steps.

Note that only `OBJECT_DELETE` and `OBJECT_FINALIZE` events trigger refreshes for directory tables. Snowflake recommends that you only send supported events for directory tables to reduce costs, event noise, and latency.

## Cloud platform support

Triggering automated refreshes using GCS Pub/Sub event messages is supported for Snowflake accounts hosted on any of the
[supported cloud platforms](/user-guide/intro-cloud-platforms).

## Configure secure access to Cloud Storage

Note

If you have already configured secure access to the GCS bucket that stores your data files, you can skip this section.

This section describes how to configure a Snowflake storage integration object to delegate authentication responsibility for cloud storage
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

### Step 3: Create a stage with an included directory table

Create an external stage that references your GCS bucket using the [CREATE STAGE](/sql-reference/sql/create-stage) command. Snowflake reads
your staged data files into the directory table metadata. Alternatively, you can use an existing external stage.

Note

- To configure secure access to the cloud storage location, see [Configure secure access to Cloud Storage](#configure-secure-access-to-cloud-storage) (in this topic).
- To reference a storage integration in the CREATE STAGE statement, the role must have the USAGE privilege on the storage integration
  object.

Copy code

```
-- External stage
CREATE [ OR REPLACE ] [ TEMPORARY ] STAGE [ IF NOT EXISTS ] <external_stage_name>
      <cloud_storage_access_settings>
    [ FILE_FORMAT = ( { FORMAT_NAME = '<file_format_name>' | TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML } [ formatTypeOptions ] } ) ]
    [ directoryTable ]
    [ COPY_OPTIONS = ( copyOptions ) ]
    [ COMMENT = '<string_literal>' ]
```

Where:

> Copy code
>
> ```
> directoryTable ::=
>   [ DIRECTORY = ( ENABLE = { TRUE | FALSE }
>                   [ AUTO_REFRESH = { TRUE | FALSE } ]
>                   [ NOTIFICATION_INTEGRATION = '<notification_integration_name>' ] ) ]
> ```

#### Directory table parameters (`directoryTable`)

`ENABLE = { TRUE | FALSE }`
:   Specifies whether to add a directory table to the stage. When the value is TRUE, a directory table is created with the stage.

    Default: `FALSE`

`AUTO_REFRESH = { TRUE | FALSE }`
:   Specifies whether Snowflake should enable triggering automatic refreshes of the directory table metadata when new or updated data
    files are available in the named external stage specified in the URL value.

    `TRUE`
    :   Snowflake enables triggering automatic refreshes of the directory table metadata.

    `FALSE`
    :   Snowflake does not enable triggering automatic refreshes of the directory table metadata. You must manually refresh the directory table
        metadata periodically using [ALTER STAGE](/sql-reference/sql/alter-stage) … REFRESH to synchronize the metadata with the current list of
        files in the stage path.

    Default: `FALSE`

`NOTIFICATION_INTEGRATION = '<notification_integration_name>'`
:   Specifies the name of the notification integration used to automatically refresh the directory table metadata using Pub/Sub
    notifications. A notification integration is a Snowflake object that provides an interface between Snowflake and third-party cloud
    message queuing services.

    The integration name must be provided in all uppercase.

The following example creates a stage named `mystage` in the active schema for the user session. The cloud storage URL includes the
path `files`. The stage references a storage integration named `my_storage_int`.

The NOTIFICATION\_INTEGRATION parameter references the `my_notification_int` integration you created in
[Step 1: Create a Notification Integration in Snowflake](#step-1-create-a-notification-integration-in-snowflake):

> Copy code
>
> ```
> USE SCHEMA mydb.public;
> ```

Copy code

```
CREATE STAGE mystage
  URL='gcs://mybucket/files/'
  STORAGE_INTEGRATION = my_storage_int
  DIRECTORY = (
    ENABLE = true
    AUTO_REFRESH = true
    NOTIFICATION_INTEGRATION = 'MY_NOTIFICATION_INT'
  );
```

Note

- The storage location in the URL value must end in a forward slash (`/`).
- The integration name must be provided in all uppercase.

When new or updated data files are added to the cloud storage location, the event notification informs Snowflake to scan them into the
directory table metadata.

### Step 4: Manually refresh the directory table metadata

Refresh the metadata in a directory table manually using the [ALTER STAGE](/sql-reference/sql/alter-stage) command.

#### Syntax

Copy code

```
ALTER STAGE [ IF EXISTS ] <name> REFRESH [ SUBPATH = '<relative-path>' ]
```

Where:

`REFRESH`
:   Accesses the staged data files referenced in the directory table definition and updates the table metadata:

    - New files in the path are added to the table metadata.
    - Changes to files in the path are updated in the table metadata.
    - Files no longer in the path are removed from the table metadata.

    Currently, it is necessary to execute this command each time files are added to the stage, updated, or dropped. This step synchronizes
    the metadata with the latest set of associated files in the stage definition for the directory table.

`SUBPATH = '<relative-path>'`
:   Optionally specify a relative path to refresh the metadata for a specific subset of the data files.

#### Examples

Manually refresh the directory table metadata in a stage named `mystage`:

Copy code

```
ALTER STAGE mystage REFRESH;
```

Important

If this step is not completed successfully at least once after the directory table is created, querying the directory table returns no
results until a notification event triggers the directory table metadata to refresh automatically for the first time.

### Step 5: Configure security

For each additional role that will be used to query the directory table, grant sufficient access control privileges on the various objects
(i.e. the database(s), schema(s), and stage) using [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege):

| Object | Privilege | Notes |
| --- | --- | --- |
| Database | USAGE |  |
| Schema | USAGE |  |
| Named stage | USAGE , READ |  |
| Named file format | USAGE | Optional; only needed if the stage you created references a named file format. |

Expand

Show lessSee more
