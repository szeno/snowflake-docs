# Refresh directory tables automatically for Azure Blob Storage

This topic provides instructions for creating directory tables and refreshing the directory table metadata automatically using
[Microsoft Azure Event Grid](https://azure.microsoft.com/en-us/services/event-grid/) notifications for an Azure container. This operation
synchronizes the metadata with the latest set of associated files in the external stage and path, i.e.:

> - New files in the path are added to the table metadata.
> - Changes to files in the path are updated in the table metadata.
> - Files no longer in the path are removed from the table metadata.

Snowflake supports the following types of blob storage accounts:

- Blob storage
- Data Lake Storage Gen2
- General-purpose v2

Automatic refresh isn’t supported for Microsoft Fabric OneLake.

Note

Only `Microsoft.Storage.BlobCreated` and `Microsoft.Storage.BlobDeleted` events trigger refreshes for directory tables. Adding new objects to blob storage
triggers these events. Renaming a directory or object doesn’t trigger these events. Snowflake recommends that you only send supported events for directory tables to reduce costs, event noise, and latency.

Snowflake supports the following `Microsoft.Storage.BlobCreated` APIs:

- `CopyBlob`
- `PutBlob`
- `PutBlockList`
- `FlushWithClose`
- `SftpCommit`

Snowflake supports the following `Microsoft.Storage.BlobDeleted` APIs:

- `DeleteBlob`
- `DeleteFile`
- `SftpRemove`

For Data Lake Storage Gen2 storage accounts, `Microsoft.Storage.BlobCreated` events are triggered when clients use the `CreateFile`
and `FlushWithClose` operations. If the SSH File Transfer Protocol (SFTP) is used, `Microsoft.Storage.BlobCreated` events are triggered with `SftpCreate` and `SftpCommit` operations. The `CreateFile` or `SftpCreate` API alone does not indicate a commit of a file in the storage account. If the
`FlushWithClose` or `SftpCommit` message is not sent, Snowflake does not refresh the directory table.

Note

To perform the tasks described in this topic, you must use a role that has the CREATE STAGE privilege on a schema.

In addition, you must have administrative access to Microsoft Azure. If you are not an Azure administrator, ask your Azure
administrator to complete the steps in [Step 1: Configure the Event Grid subscription](#step-1-configure-the-event-grid-subscription).

Snowflake only supports the [Azure Event Grid event schema](https://learn.microsoft.com/en-us/azure/event-grid/event-schema); it doesn’t support the [CloudEvents schema with Azure Event Grid](https://learn.microsoft.com/en-us/azure/event-grid/cloud-event-schema).

## Cloud platform support

Triggering automated refreshes using Azure Event Grid messages is supported for Snowflake accounts hosted on any of the
[supported cloud platforms](/user-guide/intro-cloud-platforms).

## Configure secure access to cloud storage

Note

If you have already configured secure access to the Azure blob storage container that stores your data files, you can skip this section.

This section describes how to configure a Snowflake storage integration object to delegate authentication responsibility for cloud storage
to a Snowflake identity and access management (IAM) entity.

Note

We highly recommend this option, which avoids the need to supply IAM credentials when accessing cloud storage. See
[Configure an Azure container for loading data](/user-guide/data-load-azure-config) for additional storage access options.

This section describes how to use storage integrations to allow Snowflake to read data from and write data to an Azure container referenced in an external (Azure) stage. Integrations are named, first-class Snowflake objects that avoid the need for passing explicit cloud provider credentials such as secret keys or access tokens. Integration objects store an Azure identity and access management (IAM) user ID called the *app registration*. An administrator in your organization grants this app the necessary permissions in the Azure account.

An integration must also specify containers (and optional paths) that limit the locations users can specify when creating external stages that use the integration.

Note

Completing the instructions in this section requires permissions in Azure to manage storage accounts. If you are not an Azure administrator, ask your Azure administrator to perform these tasks.

**In this Section:**

## Step 1: Create a cloud storage integration in Snowflake

Create a storage integration using the [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration) command. A storage integration is a Snowflake object that stores a generated service principal for your Azure cloud storage, along with an optional set of allowed or blocked storage locations (that is, containers). Cloud provider administrators in your organization grant permissions on the storage locations to the generated service principal. This option allows users to avoid supplying credentials when creating stages or loading data.

A single storage integration can support multiple external (that is, Azure) stages. The URL in the stage definition must align with the Azure containers (and optional paths) specified for the STORAGE\_ALLOWED\_LOCATIONS parameter.

Note

Only account administrators (users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute this SQL command.

Copy code

```
CREATE STORAGE INTEGRATION <integration_name>
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'AZURE'
  ENABLED = TRUE
  AZURE_TENANT_ID = '<tenant_id>'
  STORAGE_ALLOWED_LOCATIONS = ('azure://<account>.blob.core.windows.net/<container>/<path>/', 'azure://<account>.blob.core.windows.net/<container>/<path>/')
  [ STORAGE_BLOCKED_LOCATIONS = ('azure://<account>.blob.core.windows.net/<container>/<path>/', 'azure://<account>.blob.core.windows.net/<container>/<path>/') ]
```

Where:

- `integration_name` is the name of the new integration.
- `tenant_id` is the ID for your Office 365 tenant that the allowed and blocked storage accounts belong to. A storage integration can authenticate to only one tenant, so the allowed and blocked storage locations must refer to storage accounts that all belong this tenant.

  To find your tenant ID, sign in to the Azure portal and click **Azure Active Directory** » **Properties**. The tenant ID is displayed in the **Tenant ID** field.
- `container` is the name of an Azure container that stores your data files (for example, `mycontainer`). The STORAGE\_ALLOWED\_LOCATIONS and STORAGE\_BLOCKED\_LOCATIONS parameters allow or block access to these containers, respectively, when stages that reference this integration are created or modified.
- `path` is an optional path that can be used to provide granular control over logical directories in the container.

The following example creates an integration that explicitly limits external stages that use the integration to reference either of two containers and paths. In a later step, we will create an external stage that references one of these containers and paths. Multiple external stages that use this integration can reference the allowed containers and paths:

> Copy code
>
> ```
> CREATE STORAGE INTEGRATION azure_int
>   TYPE = EXTERNAL_STAGE
>   STORAGE_PROVIDER = 'AZURE'
>   ENABLED = TRUE
>   AZURE_TENANT_ID = 'a123b4c5-1234-123a-a12b-1a23b45678c9'
>   STORAGE_ALLOWED_LOCATIONS = ('azure://myaccount.blob.core.windows.net/mycontainer1/mypath1/', 'azure://myaccount.blob.core.windows.net/mycontainer2/mypath2/')
>   STORAGE_BLOCKED_LOCATIONS = ('azure://myaccount.blob.core.windows.net/mycontainer1/mypath1/sensitivedata/', 'azure://myaccount.blob.core.windows.net/mycontainer2/mypath2/sensitivedata/');
> ```

## Step 2: Grant Snowflake Access to the Storage Locations

1. Execute the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command to retrieve the consent URL:

   Copy code

   ```
   DESC STORAGE INTEGRATION <integration_name>;
   ```

   Where:

   - `integration_name` is the name of the integration you created in [Step 1: Create a Cloud Storage Integration in Snowflake](#step-1-create-a-cloud-storage-integration-in-snowflake).

   Note the values in the following columns:

   AZURE\_CONSENT\_URL:
   :   URL to the Microsoft permissions request page.

   AZURE\_MULTI\_TENANT\_APP\_NAME:
   :   Name of the Snowflake client application created for your account. In a later step in this section, you will need to grant this
       application the permissions necessary to obtain an access token on your allowed storage locations.
2. In a web browser, navigate to the URL in the AZURE\_CONSENT\_URL column. The page displays a Microsoft permissions request page.
3. Click the **Accept** button. This action allows the Azure service principal created for your Snowflake account to be granted an access token on specified resources inside your tenant. Obtaining an access token succeeds only if you grant the service principal the appropriate permissions on the container (see the next step).

   The Microsoft permissions request page redirects to the Snowflake corporate site (snowflake.com).
4. Sign in to the Microsoft Azure portal.
5. Navigate to **Azure Services** » **Storage Accounts**. Click the name of the storage account you are granting the Snowflake service principal access to.
6. Click **Access Control (IAM)** » **Add role assignment**.
7. Select the desired role to grant to the Snowflake service principal:

   - `Storage Blob Data Reader` grants read access only. This allows loading data from files staged in the storage account.
   - `Storage Blob Data Contributor` grants read and write access. This allows loading data from or unloading data to files staged in
     the storage account. The role also allows executing the [REMOVE](/sql-reference/sql/remove) command to remove files staged in the
     storage account.
8. Search for the Snowflake service principal. This is the identity in the AZURE\_MULTI\_TENANT\_APP\_NAME property in the DESC STORAGE INTEGRATION output (in Step 1). Search for the string before the underscore in the AZURE\_MULTI\_TENANT\_APP\_NAME property.

   Important

   - It can take an hour or longer for Azure to create the Snowflake service principal requested through the Microsoft request page in this section. If the service principal is not available immediately, we recommend waiting an hour or two and then searching again.
   - If you delete the service principal, the storage integration stops working.

   ![Add role assignment in Azure Storage Console](/static/images/screens/azure-storage-add-role-assignment.png)
9. Click the **Review + assign** button.

   Note

   - According to the Microsoft Azure documentation, role assignments may take up to five minutes to propagate.
   - Snowflake caches the temporary credentials for a period that cannot exceed the 60 minute expiration time. If you revoke access from Snowflake, users might be able to list files and load data from the cloud storage location until the cache expires.

Note

You can use the [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](/sql-reference/functions/system_validate_storage_integration)
function to validate the configuration for your storage integration.

## Configure automation with Azure Event Grid

### Step 1: Configure the Event Grid subscription

This section describes how to set up an Event Grid subscription for Azure Storage events using the Azure CLI. For more information about the steps described in this section, see the following articles in the Azure documentation:

- <https://docs.microsoft.com/en-us/azure/event-grid/custom-event-to-queue-storage>
- <https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-event-quickstart>

#### Create a resource group

An Event Grid *topic* provides an endpoint where the source (that is, Azure Storage) sends events. A topic is used for a collection of related events. Event Grid topics are Azure resources, and must be placed in an Azure resource group.

Execute the following command to create a resource group:

Copy code

```
az group create --name <resource_group_name> --location <location>
```

Where:

- `resource_group_name` is the name of the new resource group.
- `location` is the location, or *region* in Snowflake terminology, of your Azure Storage account.

#### Enable the Event Grid resource provider

Execute the following command to register the Event Grid resource provider. Note that this step is only required if you have not previously used Event Grid with your Azure account:

Copy code

```
az provider register --namespace Microsoft.EventGrid
az provider show --namespace Microsoft.EventGrid --query "registrationState"
```

#### Create a storage account for data files

Execute the following command to create a storage account to store your data files. This account must be either a Blob storage (that is, a `BlobStorage` kind) or GPv2 (that is, a `StorageV2` kind) account, because only these two account types support event messages.

Note

If you already have a Blob storage or GPv2 account, you can use that account instead.

For example, create a Blob storage account:

Copy code

```
az storage account create --resource-group <resource_group_name> --name <storage_account_name> --sku Standard_LRS --location <location> --kind BlobStorage --access-tier Hot
```

Where:

- `resource_group_name` is the name of the resource group you created in [Create a Resource Group](#create-a-resource-group).
- `storage_account_name` is the name of the new storage account.
- `location` is the location of your Azure Storage account.

#### Create a storage account for the storage queue

Execute the following command to create a storage account to host your storage queue. This account must be a GPv2 account, because only this kind of account supports event messages to a storage queue.

Note

If you already have a GPv2 account, you can use that account to host both your data files and your storage queue.

For example, create a GPv2 account:

Copy code

```
az storage account create --resource-group <resource_group_name> --name <storage_account_name> --sku Standard_LRS --location <location> --kind StorageV2
```

Where:

- `resource_group_name` is the name of the resource group you created in [Create a resource group](#create-a-resource-group).
- `storage_account_name` is the name of the new storage account.
- `location` is the location of your Azure Storage account.

#### Create a storage queue

A single Azure Queue Storage queue can collect the event messages for many Event Grid subscriptions. For best performance, Snowflake recommends creating a single storage queue to accommodate all of your subscriptions related to Snowflake.

Execute the following command to create a storage queue. A storage queue stores a set of messages, in this case event messages from Event Grid:

Copy code

```
az storage queue create --name <storage_queue_name> --account-name <storage_account_name>
```

Where:

- `storage_queue_name` is the name of the new storage queue.
- `storage_account_name` is the name of the storage account you created in [Create a storage account for the storage queue](#create-a-storage-account-for-the-storage-queue).

#### Export the storage account and queue IDs for Reference

Execute the following commands to set environment variables for the storage account and queue IDs that will be requested later in these instructions:

- Linux or macOS:

  Copy code

  ```
  export storageid=$(az storage account show --name <data_storage_account_name> --resource-group <resource_group_name> --query id --output tsv)
  export queuestorageid=$(az storage account show --name <queue_storage_account_name> --resource-group <resource_group_name> --query id --output tsv)
  export queueid="$queuestorageid/queueservices/default/queues/<storage_queue_name>"
  ```
- Windows:

  Copy code

  ```
  set storageid=$(az storage account show --name <data_storage_account_name> --resource-group <resource_group_name> --query id --output tsv)
  set queuestorageid=$(az storage account show --name <queue_storage_account_name> --resource-group <resource_group_name> --query id --output tsv)
  set queueid="%queuestorageid%/queueservices/default/queues/<storage_queue_name>"
  ```

Where:

- `data_storage_account_name` is the name of the storage account you created in [Create a storage account for data files](#create-a-storage-account-for-data-files).
- `queue_storage_account_name` is the name of the storage account you created in [Create a storage account for the storage queue](#create-a-storage-account-for-the-storage-queue).
- `resource_group_name` is the name of the resource group you created in [Create a resource group](#create-a-resource-group).
- `storage_queue_name` is the name of the storage queue you created in [Create a storage queue](#create-a-storage-queue).

#### Install the Event Grid extension

Execute the following command to install the Event Grid extension for Azure CLI:

Copy code

```
az extension add --name eventgrid
```

#### Create the Event Grid subscription

Execute the following command to create the Event Grid subscription. Subscribing to a topic informs Event Grid which events to track:

- Linux or macOS:

  Copy code

  ```
  az eventgrid event-subscription create \
  --source-resource-id $storageid \
  --name <subscription_name> --endpoint-type storagequeue \
  --endpoint $queueid \
  --advanced-filter data.api stringin CopyBlob PutBlob PutBlockList FlushWithClose SftpCommit DeleteBlob DeleteFile SftpRemove
  ```
- Windows:

  Copy code

  ```
  az eventgrid event-subscription create \
  --source-resource-id %storageid% \
  --name <subscription_name> --endpoint-type storagequeue \
  --endpoint %queueid% \
  -advanced-filter data.api stringin CopyBlob PutBlob PutBlockList FlushWithClose SftpCommit DeleteBlob DeleteFile SftpRemove
  ```

Where:

- `storageid` and `queueid` are the storage account and queue ID environment variables you set in [Export the storage account and queue IDs for reference](#export-the-storage-account-and-queue-ids-for-reference).
- `subscription_name` is the name of the new Event Grid subscription.

### Step 2: Create the notification integration

A *notification integration* is a Snowflake object that provides an interface between Snowflake and a third-party cloud message queuing service such as Azure Event Grid.

Note

A single notification integration supports a single Azure Storage queue. Referencing the same storage queue in multiple notification integrations can result in missing data in target tables because event notifications are split between notification integrations.

#### Retrieve the storage queue URL and tenant ID

1. Sign in to the Microsoft Azure portal.
2. Navigate to **Storage account** » **Queue service** » **Queues**. Record the URL for the queue you created in [Create a storage queue](#create-a-storage-queue) for reference later. The URL has the following format:

   Copy code

   ```
   https://<storage_account_name>.queue.core.windows.net/<storage_queue_name>
   ```
3. Navigate to **Azure Active Directory** » **Properties**. Record the **Tenant ID** value for reference later. The directory ID, or *tenant ID*, is needed to generate the consent URL that grants Snowflake access to the Event Grid subscription.

#### Create the notification integration

Create a notification integration using the
[CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration-queue-inbound-azure) command.

Note

- Only account administrators (users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute this SQL command.
- The Azure service principal for notification integrations is different from the service principal created for storage integrations.

Copy code

```
CREATE NOTIFICATION INTEGRATION <integration_name>
  ENABLED = true
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE
  AZURE_STORAGE_QUEUE_PRIMARY_URI = '<queue_URL>'
  AZURE_TENANT_ID = '<directory_ID>';
```

Where:

- `integration_name` is the name of the new integration.
- `queue_URL` and `directory_ID` are the queue URL and tenant ID you recorded in [Retrieve the storage queue URL and tenant ID](#retrieve-the-storage-queue-url-and-tenant-id).

For example:

Copy code

```
CREATE NOTIFICATION INTEGRATION my_notification_int
  ENABLED = true
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE
  AZURE_STORAGE_QUEUE_PRIMARY_URI = 'https://myqueue.queue.core.windows.net/mystoragequeue'
  AZURE_TENANT_ID = 'a123bcde-1234-5678-abc1-9abc12345678';
```

#### Grant Snowflake access to the storage queue

Note that specific steps in this section require a local installation of the Azure CLI.

1. Execute the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command to retrieve the consent URL:

   Copy code

   ```
   DESC NOTIFICATION INTEGRATION <integration_name>;
   ```

   Where:

   - `integration_name` is the name of the integration you created in [Create the notification integration](#create-the-notification-integration).

   Note the values in the following columns:

   AZURE\_CONSENT\_URL:
   :   URL to the Microsoft permissions request page.

   AZURE\_MULTI\_TENANT\_APP\_NAME:
   :   Name of the Snowflake client application created for your account. In a later step in this section, you will need to grant this
       application the permissions necessary to obtain an access token on your allowed topic.
2. In a web browser, navigate to the URL in the AZURE\_CONSENT\_URL column. The page displays a Microsoft permissions request page.
3. Click the **Accept** button. This action allows the Azure service principal created for your Snowflake account to obtain an access
   token on any resource inside your tenant. Obtaining an access token succeeds only if you grant the service principal the appropriate
   permissions on the container (see the next step).

   The Microsoft permissions request page redirects to the Snowflake corporate site (snowflake.com).
4. Sign in to the Microsoft Azure portal.
5. Navigate to **Azure Active Directory** » **Enterprise applications**. Verify that the Snowflake application identifier you
   recorded in Step 2 in this section is listed.

   Important

   If you delete the Snowflake application in Azure Active Directory at a later time, the notification integration stops working.
6. Navigate to **Queues** » `storage_queue_name`, where `storage_queue_name` is the name of the storage queue you created in [Create a storage queue](#create-a-storage-queue).
7. Click **Access Control (IAM)** » **Add role assignment**.
8. Search for the Snowflake service principal. This is the identity in the AZURE\_MULTI\_TENANT\_APP\_NAME property in the DESC NOTIFICATION
   INTEGRATION output (in Step 1). Search for the string before the underscore in the AZURE\_MULTI\_TENANT\_APP\_NAME property.

   Important

   - It can take an hour or longer for Azure to create the Snowflake service principal requested through the Microsoft request page in
     this section. If the service principal is not available immediately, we recommend waiting an hour or two and then searching again.
   - If you delete the service principal, the notification integration stops working.
9. Grant the Snowflake app the following permissions:

   - **Role:** Storage Queue Data Message Processor (the minimum required role), or Storage Queue Data Contributor.
   - **Assign access to:** Azure AD user, group, or service principal.
   - **Select:** The `appDisplayName` value.

   The Snowflake application identifier should now be listed under **Storage Queue Data Message Processor** or **Storage Queue Data Contributor** (on the same dialog).

### Step 3: Create a stage with an included directory table

Create an external stage that references your Azure container using the [CREATE STAGE](/sql-reference/sql/create-stage) command. Snowflake reads
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
> directoryTable (for Microsoft Azure) ::=
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

**Microsoft Azure**

> `NOTIFICATION_INTEGRATION = '<notification_integration_name>'`
> :   Specifies the name of the notification integration used to automatically refresh the directory table metadata using Azure Event Grid
>     notifications. A notification integration is a Snowflake object that provides an interface between Snowflake and third-party cloud
>     message queuing services.

The following example creates a stage named `mystage` in the active schema for the user session. The cloud storage URL includes the
path `files`. The stage references a storage integration named `my_storage_int`.

> Copy code
>
> ```
> USE SCHEMA mydb.public;
> ```

Copy code

```
CREATE STAGE mystage
  URL='azure://myaccount.blob.core.windows.net/load/files/'
  STORAGE_INTEGRATION = my_storage_int
  DIRECTORY = (
    ENABLE = true
    AUTO_REFRESH = true
    NOTIFICATION_INTEGRATION = 'MY_NOTIFICATION_INT'
  );
```

Note

- Use the `blob.core.windows.net` endpoint for all supported types of Azure blob storage accounts, including Data Lake Storage Gen2.
- The storage location in the URL value must end in a forward slash (`/`).

The NOTIFICATION\_INTEGRATION parameter references the `my_notification_int` integration you created in
[Step 2: Create the notification integration](#step-2-create-the-notification-integration). The integration name must be provided in all uppercase.

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
(i.e. the database(s), schema(s), stage, and table) using [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege):

| Object | Privilege | Notes |
| --- | --- | --- |
| Database | USAGE |  |
| Schema | USAGE |  |
| Named stage | USAGE , READ |  |
| Named file format | USAGE | Optional; only needed if the stage you created references a named file format. |

Expand

Show lessSee more
