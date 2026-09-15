# Automating Snowpipe for Microsoft Azure Blob Storage

This topic provides instructions for triggering Snowpipe data loads from external stages on Azure Blob Storage automatically using [Microsoft Azure Event Grid](https://azure.microsoft.com/en-us/services/event-grid/) messages for Blob storage events. The instructions explain how to create an event message for the target path in Blob storage where your data files are stored.

Note

To harden your security posture, you can configure Snowpipe automation to use private connectivity rather than the public Internet for
network traffic. For more information, see [Private connectivity to external stages and Snowpipe automation for Microsoft Azure](/user-guide/data-load-azure-private).

Snowflake supports the following types of blob storage accounts:

- Blob storage
- Data Lake Storage Gen2
- General-purpose v2

Note

- Automated Snowpipe isn’t supported for Microsoft Fabric OneLake.
- Only `Microsoft.Storage.BlobCreated` events trigger Snowpipe to load files. Adding new objects to blob storage triggers these events. Renaming a directory or object does not trigger these events.

Snowflake supports the following `Microsoft.Storage.BlobCreated`
APIs:

- `CopyBlob`
- `PutBlob`
- `PutBlockList`
- `FlushWithClose`
- `SftpCommit`

Snowflake recommends that you only send supported events for Snowpipe to reduce costs, event noise, and latency.

For Data Lake Storage Gen2 storage accounts, `Microsoft.Storage.BlobCreated` events are triggered when clients use the `CreateFile`
and `FlushWithClose` operations. If the SSH File Transfer Protocol (SFTP) is used, `Microsoft.Storage.BlobCreated` events are triggered with `SftpCreate` and `SftpCommit` operations. The `CreateFile` or `SftpCreate` API alone does not indicate a commit of a file in the storage account. If the
`FlushWithClose` or `SftpCommit` message is not sent to the Snowflake queue, Snowpipe does not ingest the file.

Note

Snowflake only supports the [Azure Event Grid event schema](https://learn.microsoft.com/en-us/azure/event-grid/event-schema); it doesn’t support the [CloudEvents schema with Azure Event Grid](https://learn.microsoft.com/en-us/azure/event-grid/cloud-event-schema).

## Cloud platform support

Triggering automated Snowpipe data loads using Azure Event Grid messages is supported by Snowflake accounts hosted on [all supported cloud platforms](/user-guide/intro-cloud-platforms).

## Process flow

[Microsoft Azure Event Grid](https://azure.microsoft.com/en-us/services/event-grid/) notifications for an Azure container trigger Snowpipe data loads automatically.

The following diagram shows the Snowpipe auto-ingest process flow:

![Snowpipe Auto-ingest Process Flow](/static/images/data-load-snowpipe-azure.png)

1. Data files are loaded in a stage.
2. A blob storage event message informs Snowpipe via Event Grid that files are ready to load. Snowpipe copies the files into a queue.
3. A Snowflake-provided virtual warehouse loads data from the queued files into the target table based on parameters defined in the specified pipe.

For instructions, see [Automating Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure).

## Configuring secure access to Cloud Storage

Note

If you have already configured secure access to the Azure blob storage container that stores your data files, you can skip this section.

This section describes how to configure a Snowflake storage integration object to delegate authentication responsibility for cloud storage to a Snowflake identity and access management (IAM) entity.

Note

We highly recommend this option, which avoids the need to supply IAM credentials when accessing cloud storage. See [Configure an Azure container for loading data](/user-guide/data-load-azure-config) for additional storage access options.

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

## Configuring Automation With Azure Event Grid

### Step 1: Configuring the Event Grid Subscription

This section describes how to set up an Event Grid subscription for Azure Storage events using the Azure CLI. For more information about the steps described in this section, see the following articles in the Azure documentation:

- <https://docs.microsoft.com/en-us/azure/event-grid/custom-event-to-queue-storage>
- <https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-event-quickstart>

#### Create a Resource Group

An Event Grid *topic* provides an endpoint where the source (i.e. Azure Storage) sends events. A topic is used for a collection of related events. Event Grid topics are Azure resources, and must be placed in an Azure resource group.

Execute the following command to create a resource group:

Copy code

```
az group create --name <resource_group_name> --location <location>
```

Where:

- `resource_group_name` is the name of the new resource group.
- `location` is the location, or *region* in Snowflake terminology, of your Azure Storage account.

#### Enable the Event Grid Resource Provider

Execute the following command to register the Event Grid resource provider. Note that this step is only required if you have not previously used Event Grid with your Azure account:

Copy code

```
az provider register --namespace Microsoft.EventGrid
az provider show --namespace Microsoft.EventGrid --query "registrationState"
```

#### Create a Storage Account for Data Files

Execute the following command to create a storage account to store your data files. This account must be either a Blob storage (i.e. `BlobStorage` kind) or GPv2 (i.e. `StorageV2` kind) account, because only these two account types support event messages.

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

#### Create a Storage Account for the Storage Queue

Execute the following command to create a storage account to host your storage queue. This account must be a GPv2 account, because only this kind of account supports event messages to a storage queue.

Note

If you already have a GPv2 account, you can use that account to host both your data files and your storage queue.

For example, create a GPv2 account:

Copy code

```
az storage account create --resource-group <resource_group_name> --name <storage_account_name> --sku Standard_LRS --location <location> --kind StorageV2
```

Where:

- `resource_group_name` is the name of the resource group you created in [Create a Resource Group](#create-a-resource-group).
- `storage_account_name` is the name of the new storage account.
- `location` is the location of your Azure Storage account.

#### Create a Storage Queue

A single Azure Queue Storage queue can collect the event messages for many Event Grid subscriptions. For best performance, Snowflake recommends creating a single storage queue to accommodate all of your subscriptions related to Snowflake.

Execute the following command to create a storage queue. A storage queue stores a set of messages, in this case event messages from Event Grid:

Copy code

```
az storage queue create --name <storage_queue_name> --account-name <storage_account_name>
```

Where:

- `storage_queue_name` is the name of the new storage queue.
- `storage_account_name` is the name of the storage account you created in [Create a Storage Account for the Storage Queue](#create-a-storage-account-for-the-storage-queue).

#### Export the Storage Account and Queue IDs for Reference

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

- `data_storage_account_name` is the name of the storage account you created in [Create a Storage Account for Data Files](#create-a-storage-account-for-data-files).
- `queue_storage_account_name` is the name of the storage account you created in [Create a Storage Account for the Storage Queue](#create-a-storage-account-for-the-storage-queue).
- `resource_group_name` is the name of the resource group you created in [Create a Resource Group](#create-a-resource-group).
- `storage_queue_name` is the name of the storage queue you created in [Create a Storage Queue](#create-a-storage-queue).

#### Install the Event Grid Extension

Execute the following command to install the Event Grid extension for Azure CLI:

Copy code

```
az extension add --name eventgrid
```

#### Create the Event Grid Subscription

Execute the following command to create the Event Grid subscription. Subscribing to a topic informs Event Grid which events to track:

- Linux or macOS:

  Copy code

  ```
  az eventgrid event-subscription create \
  --source-resource-id $storageid \
  --name <subscription_name> --endpoint-type storagequeue \
  --endpoint $queueid \
  --advanced-filter data.api stringin CopyBlob PutBlob PutBlockList FlushWithClose SftpCommit
  ```
- Windows:

  Copy code

  ```
  az eventgrid event-subscription create \
  --source-resource-id %storageid% \
  --name <subscription_name> --endpoint-type storagequeue \
  --endpoint %queueid% \
  -advanced-filter data.api stringin CopyBlob PutBlob PutBlockList FlushWithClose SftpCommit
  ```

Where:

- `storageid` and `queueid` are the storage account and queue ID environment variables you set in [Export the Storage Account and Queue IDs for Reference](#export-the-storage-account-and-queue-ids-for-reference).
- `subscription_name` is the name of the new Event Grid subscription.

### Step 2: Creating the Notification Integration

A notification integration is a Snowflake object that provides an interface between Snowflake and a third-party cloud message queuing service such as Azure Event Grid.

Note

A single notification integration supports a single Azure Storage queue. Referencing the same storage queue in multiple notification integrations could result in missing data in target tables because event notifications are split between notification integrations. Therefore, pipe creation is blocked if a pipe references the same storage queue as an existing pipe.

#### Retrieve the Storage Queue URL and Tenant ID

1. Log into the Microsoft Azure portal.
2. Navigate to **Storage account** » **Queue service** » **Queues**. Record the URL for the queue you created in [Create a Storage Queue](#create-a-storage-queue) for reference later. The URL has the following format:

   Copy code

   ```
   https://<storage_account_name>.queue.core.windows.net/<storage_queue_name>
   ```
3. Navigate to **Azure Active Directory** » **Properties**. Record the **Tenant ID** value for reference later. The directory ID, or *tenant ID*, is needed to generate the consent URL that grants Snowflake access to the Event Grid subscription.

#### Create the Notification Integration

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
- `queue_URL` and `directory_ID` are the queue URL and tenant ID you recorded in [Retrieve the Storage Queue URL and Tenant ID](#retrieve-the-storage-queue-url-and-tenant-id).

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

#### Grant Snowflake Access to the Storage Queue

Note that specific steps in this section require a local installation of the Azure CLI.

1. Execute the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command to retrieve the consent URL:

   Copy code

   ```
   DESC NOTIFICATION INTEGRATION <integration_name>;
   ```

   Where:

   - `integration_name` is the name of the integration you created in [Create the Notification Integration](#create-the-notification-integration).

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
4. Log into the Microsoft Azure portal.
5. Navigate to **Azure Active Directory** » **Enterprise applications**. Verify the Snowflake application identifier you
   recorded in Step 2 in this section is listed.

   Important

   If you delete the Snowflake application in Azure Active Directory at a later time, the notification integration stops working.
6. Navigate to **Queues** » `storage_queue_name`, where `storage_queue_name` is the name of the storage queue you created in [Create a Storage Queue](#create-a-storage-queue).
7. Click **Access Control (IAM)** » **Add role assignment**.
8. Search for the Snowflake service principal. This is the identity in the AZURE\_MULTI\_TENANT\_APP\_NAME property in the DESC NOTIFICATION
   INTEGRATION output (in Step 1). Search for the string before the underscore in the AZURE\_MULTI\_TENANT\_APP\_NAME property.

   Important

   - It can take an hour or longer for Azure to create the Snowflake service principal requested through the Microsoft request page in
     this section. If the service principal is not available immediately, we recommend waiting an hour or two and then searching again.
   - If you delete the service principal, the notification integration stops working.
9. Grant the Snowflake app the following permissions:

   - **Role:** Storage Queue Data Contributor
   - **Assign access to:** Azure AD user, group, or service principal
   - **Select:** The `appDisplayName` value.

   The Snowflake application identifier should now be listed under **Storage Queue Data Contributor** (on the same dialog).

### Step 3: Create a stage (if needed)

Create an external stage that references your Azure container using the [CREATE STAGE](/sql-reference/sql/create-stage) command. Snowpipe fetches your data files from the stage and temporarily queues them before loading them into your target table.

Alternatively, you can use an existing external stage.

Note

- To configure secure access to the cloud storage location, see [Configuring Secure Access to Cloud Storage](#configuring-secure-access-to-cloud-storage) (in this topic).
- To reference a storage integration in the CREATE STAGE statement, the role must have the USAGE privilege on the storage integration object.

The following example creates a stage named `mystage` in the active schema for the user session. The cloud storage URL includes the path `load/files`. The stage references a storage integration named `my_storage_int`.

> Copy code
>
> ```
> USE SCHEMA snowpipe_db.public;
>
> CREATE STAGE mystage
>   URL = 'azure://myaccount.blob.core.windows.net/mycontainer/load/files/'
>   STORAGE_INTEGRATION = my_storage_int;
> ```

Note

Use the `blob.core.windows.net` endpoint for all supported types of Azure blob storage accounts, including Data Lake Storage Gen2.

### Step 4: Create a pipe with auto-ingest enabled

Create a pipe using the [CREATE PIPE](/sql-reference/sql/create-pipe) command. The pipe defines the [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement used by Snowpipe to load data from the ingestion queue into the target table.

For example, create a pipe in the `snowpipe_db.public` schema that loads the data from files staged in the `mystage` stage into the `mytable` table:

> Copy code
>
> ```
> CREATE PIPE snowpipe_db.public.mypipe
>   AUTO_INGEST = true
>   INTEGRATION = 'MY_NOTIFICATION_INT'
>   AS
>     COPY INTO snowpipe_db.public.mytable
>       FROM @snowpipe_db.public.mystage
>       FILE_FORMAT = (type = 'JSON');
> ```

Where:

- `MY_NOTIFICATION_INT` is the name of the notification integration you created in [Step 2: Creating the Notification Integration](#step-2-creating-the-notification-integration).

Important

- The integration name must be typed in all uppercase.
- Verify that the storage location reference in the COPY INTO *<table>* statement does not overlap with the reference in existing pipes
  in the account. Otherwise, multiple pipes could load the same set of data files into the target tables. For example, this situation can
  occur when multiple pipe definitions reference the same storage location with different levels of granularity, such as
  `<storage_location>/path1/` and `<storage_location>/path1/path2/`. In this example, if files are staged in
  `<storage_location>/path1/path2/`, both pipes would load a copy of the files.

  View the COPY INTO *<table>* statements in the definitions of all pipes in the account by executing [SHOW PIPES](/sql-reference/sql/show-pipes)
  or by querying either the [PIPES](/sql-reference/account-usage/pipes) view in Account Usage or the
  [PIPES](/sql-reference/info-schema/pipes) view in the Information Schema.

Snowpipe with auto-ingest is now configured!

When new data files are added to the Azure container, the event message informs Snowpipe to load them into the target table defined in the pipe.

### Step 5: Load historical files

To load any backlog of data files that existed in the external stage before Event Grid messages were configured, execute an [ALTER PIPE … REFRESH](/sql-reference/sql/alter-pipe) statement.

### Step 6: Delete staged files

Delete the staged files after you successfully load the data and no longer require the files. For instructions, see
[Deleting staged files after Snowpipe loads the data](/user-guide/data-load-snowpipe-manage#label-snowpipe-delete-data-files).

## SYSTEM$PIPE\_STATUS output

The [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) function retrieves a JSON representation of the current status of a pipe.

For pipes with AUTO\_INGEST set to TRUE, the function returns a JSON object containing the following name/value pairs (if applicable to the current pipe status):

> `{"executionState":"<value>","oldestFileTimestamp":<value>,"pendingFileCount":<value>,"notificationChannelName":"<value>","numOutstandingMessagesOnChannel":<value>,"lastReceivedMessageTimestamp":"<value>","lastForwardedMessageTimestamp":"<value>","error":<value>,"fault":<value>}`

For descriptions of the output values, see the reference topic for the SQL function.
