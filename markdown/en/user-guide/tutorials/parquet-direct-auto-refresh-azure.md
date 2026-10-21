# Tutorial: Auto-refresh a Parquet Direct table from Azure Blob Storage

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

## Introduction

This tutorial shows you how to create a [Parquet Direct](/user-guide/tables-iceberg-parquet-direct) table: a read-only
Apache Iceberg™ table in Snowflake that queries Apache Parquet™ files in your Azure storage account in place. You configure
Azure Event Grid to send blob events to an Azure Storage queue that Snowflake reads, so that Snowflake refreshes the table
automatically whenever files are added or deleted.

### What you’ll learn

In this tutorial, you’ll learn how to do the following:

- Configure an Azure Event Grid subscription and storage queue for blob events.
- Create a notification integration and grant Snowflake access to the storage queue.
- Create an external volume that uses the storage queue.
- Create a catalog integration for Parquet files.
- Create a Parquet Direct table with schema inference, schema evolution, and auto-refresh.
- Verify that new files are registered automatically, and monitor auto-refresh.

### Supported accounts, APIs, and schemas

- Auto-refresh using Azure Event Grid is supported for Snowflake accounts hosted on Microsoft Azure.
- Snowflake supports the following types of storage accounts:

  - Blob storage
  - Data Lake Storage Gen2
  - General-purpose v2
- Auto-refresh isn’t supported for Microsoft Fabric OneLake. For OneLake, refresh the table
  [manually](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-manual-refresh).
- Only `Microsoft.Storage.BlobCreated` and `Microsoft.Storage.BlobDeleted` events trigger a refresh. Renaming a directory or
  object doesn’t trigger these events. To reduce costs, event noise, and latency, send only these events.
- Snowflake supports the following `Microsoft.Storage.BlobCreated` APIs: `CopyBlob`, `PutBlob`, `PutBlockList`,
  `FlushWithClose`, and `SftpCommit`.
- Snowflake supports the following `Microsoft.Storage.BlobDeleted` APIs: `DeleteBlob`, `DeleteFile`, and `SftpRemove`.
- For Data Lake Storage Gen2 storage accounts, `Microsoft.Storage.BlobCreated` events are triggered when clients use the
  `CreateFile` and `FlushWithClose` operations. If clients use SSH File Transfer Protocol (SFTP), the events are triggered
  with the `SftpCreate` and `SftpCommit` operations. The `CreateFile` or `SftpCreate` API alone doesn’t indicate a committed
  file. If the `FlushWithClose` or `SftpCommit` message isn’t sent, Snowflake doesn’t register the file.
- Snowflake supports only the [Azure Event Grid event schema](https://learn.microsoft.com/en-us/azure/event-grid/event-schema).
  The [CloudEvents schema with Azure Event Grid](https://learn.microsoft.com/en-us/azure/event-grid/cloud-event-schema) isn’t
  supported.
- Storage versioning isn’t supported.

### Prerequisites

- A Snowflake role with the following privileges:

  - CREATE EXTERNAL VOLUME on the account.
  - CREATE INTEGRATION on the account, to create the notification integration and catalog integration.
  - CREATE ICEBERG TABLE on the schema where you create the table.
  - USAGE on a warehouse to query the table.
- The [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
- Administrative access to Microsoft Azure. If you aren’t an Azure administrator, ask your administrator to complete the
  Azure steps.

Note

Auto-refresh is billed as serverless compute, and each refresh incurs data registration charges for the files it adds.
For more information, see [Billing](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-billing).

## Step 1: Configure the Event Grid subscription

This step uses the Azure CLI to set up an Event Grid subscription for Azure Storage events.

### Create a resource group

An Event Grid *topic* provides an endpoint where the source (Azure Storage) sends events. Event Grid topics are Azure
resources, and must be placed in an Azure resource group.

Run the following command to create a resource group:

Copy code

```
az group create --name <resource_group_name> --location <location>
```

Where:

- `resource_group_name` is the name of the new resource group.
- `location` is the location, or *region* in Snowflake terminology, of your Azure
  Storage account.

### Enable the Event Grid resource provider

If you haven’t used Event Grid with your Azure account before, run the following commands to register the Event Grid
resource provider:

Copy code

```
az provider register --namespace Microsoft.EventGrid
az provider show --namespace Microsoft.EventGrid --query "registrationState"
```

### Create a storage account for data files

Run the following command to create a storage account for your Parquet files. The account must be a Blob storage
(`BlobStorage` kind) or general-purpose v2 (`StorageV2` kind) account, because only these account types support event
messages. If you already have one of these accounts, you can use it instead.

Copy code

```
az storage account create \
  --resource-group <resource_group_name> \
  --name <data_storage_account_name> \
  --sku Standard_LRS \
  --location <location> \
  --kind BlobStorage \
  --access-tier Hot
```

### Create a storage account for the storage queue

Run the following command to create a storage account to host your storage queue. The account must be a general-purpose v2
account, because only this kind of account supports event messages to a storage queue. If you already have a
general-purpose v2 account, you can use it to host both your data files and your storage queue.

Copy code

```
az storage account create \
  --resource-group <resource_group_name> \
  --name <queue_storage_account_name> \
  --sku Standard_LRS \
  --location <location> \
  --kind StorageV2
```

### Create a storage queue

A single Azure Queue Storage queue can collect the event messages for many Event Grid subscriptions. For best performance,
Snowflake recommends creating a single storage queue for all of your subscriptions related to Snowflake.

Run the following command to create a storage queue:

Copy code

```
az storage queue create \
  --name <storage_queue_name> \
  --account-name <queue_storage_account_name>
```

### Export the storage account and queue IDs

Set environment variables for the storage account and queue IDs, which you use in later commands.

Linux or macOS:

Copy code

```
export storageid=$(az storage account show \
  --name <data_storage_account_name> \
  --resource-group <resource_group_name> \
  --query id --output tsv)
export queuestorageid=$(az storage account show \
  --name <queue_storage_account_name> \
  --resource-group <resource_group_name> \
  --query id --output tsv)
export queueid="$queuestorageid/queueservices/default/queues/<storage_queue_name>"
```

Windows:

Copy code

```
set storageid=$(az storage account show \
  --name <data_storage_account_name> \
  --resource-group <resource_group_name> \
  --query id --output tsv)
set queuestorageid=$(az storage account show \
  --name <queue_storage_account_name> \
  --resource-group <resource_group_name> \
  --query id --output tsv)
set queueid="%queuestorageid%/queueservices/default/queues/<storage_queue_name>"
```

### Install the Event Grid extension

Run the following command to install the Event Grid extension for the Azure CLI:

Copy code

```
az extension add --name eventgrid
```

### Create the Event Grid subscription

Run the following command to create the Event Grid subscription. The advanced filter limits the subscription to the blob
APIs that Snowflake supports.

Linux or macOS:

Copy code

```
az eventgrid event-subscription create \
  --source-resource-id $storageid \
  --name <subscription_name> \
  --endpoint-type storagequeue \
  --endpoint $queueid \
  --advanced-filter data.api stringin CopyBlob PutBlob PutBlockList \
    FlushWithClose SftpCommit DeleteBlob DeleteFile SftpRemove
```

Windows:

Copy code

```
az eventgrid event-subscription create \
  --source-resource-id %storageid% \
  --name <subscription_name> \
  --endpoint-type storagequeue \
  --endpoint %queueid% \
  --advanced-filter data.api stringin CopyBlob PutBlob PutBlockList \
    FlushWithClose SftpCommit DeleteBlob DeleteFile SftpRemove
```

## Step 2: Create a notification integration

A *notification integration* is a Snowflake object that provides an interface between Snowflake and a cloud message queuing
service such as Azure Event Grid.

Note

A single notification integration supports a single Azure Storage queue. If you reference the same storage queue in multiple
notification integrations, event notifications are split between the integrations, which can result in missing data.

### Retrieve the storage queue URL and tenant ID

1. Sign in to the Microsoft Azure portal.
2. Navigate to **Storage account** » **Queue service** » **Queues**. Record the URL for the queue that you created in
   [Create a storage queue](#label-tutorial-parquet-direct-azure-queue). The URL has the following format:

   ```
   https://<queue_storage_account_name>.queue.core.windows.net/<storage_queue_name>
   ```
3. Navigate to **Microsoft Entra ID** » **Properties**. Record the **Tenant ID** value. You need the tenant ID to grant
   Snowflake access to the storage queue.

### Create the notification integration

Create a notification integration by using the [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration) command. Use the
queue URL and tenant ID that you recorded:

Copy code

```
CREATE NOTIFICATION INTEGRATION parquet_azure_notification_int
  ENABLED = TRUE
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE
  AZURE_STORAGE_QUEUE_PRIMARY_URI = 'https://myqueueaccount.queue.core.windows.net/mystoragequeue'
  AZURE_TENANT_ID = 'a123bcde-1234-5678-abc1-9abc12345678';
```

Note

The Azure service principal for notification integrations is different from the service principal created for storage
integrations and external volumes.

### Grant Snowflake access to the storage queue

1. Run the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command:

   Copy code

   ```
   DESC NOTIFICATION INTEGRATION parquet_azure_notification_int;
   ```

   Note the values in the following columns:

   - `AZURE_CONSENT_URL`: URL to the Microsoft permissions request page.
   - `AZURE_MULTI_TENANT_APP_NAME`: Name of the Snowflake client application created for your account.
2. In a web browser, navigate to the URL in the `AZURE_CONSENT_URL` column, and select **Accept**. This action allows the
   Azure service principal created for your Snowflake account to obtain an access token on resources in your tenant. Getting
   an access token succeeds only if you grant the service principal the appropriate permissions on the queue (see the
   following steps).

   The Microsoft permissions request page redirects to the Snowflake corporate site (snowflake.com).
3. Sign in to the Microsoft Azure portal.
4. Navigate to **Microsoft Entra ID** » **Enterprise applications**, and verify that the Snowflake application is listed.

   Important

   If you delete the Snowflake application in Microsoft Entra ID later, the notification integration stops working.
5. Navigate to **Queues** » `storage_queue_name`.
6. Select **Access Control (IAM)** » **Add role assignment**.
7. Search for the Snowflake service principal: the string *before* the underscore in the `AZURE_MULTI_TENANT_APP_NAME` value.

   Important

   It can take an hour or longer for Azure to create the Snowflake service principal that you requested through the
   Microsoft permissions request page. If the service principal isn’t available immediately, wait an hour or two and search
   again.
8. Grant the Snowflake application the **Storage Queue Data Message Processor** role (the minimum required role) or the
   **Storage Queue Data Contributor** role.

## Step 3: Create an external volume with your storage queue

Complete the instructions in [Configure an external volume for Azure](/user-guide/tables-iceberg-configure-external-volume-azure) to create an external volume
and grant Snowflake read access to your storage container. When you create the external volume, specify the following
additional parameter on the storage location:

`AZURE_STORAGE_QUEUE_PRIMARY_URI = 'queue_url'`
:   Specifies the URL of the Azure Storage queue that handles all messages for your external volume location.

For example:

Copy code

```
CREATE OR REPLACE EXTERNAL VOLUME parquet_azure_exvol
  STORAGE_LOCATIONS = (
    (
      NAME = 'my-azure-location'
      STORAGE_PROVIDER = 'AZURE'
      STORAGE_BASE_URL = 'azure://mydataaccount.blob.core.windows.net/mycontainer/'
      AZURE_TENANT_ID = 'a123bcde-1234-5678-abc1-9abc12345678'
      AZURE_STORAGE_QUEUE_PRIMARY_URI = 'https://myqueueaccount.queue.core.windows.net/mystoragequeue'
    )
  );
```

Parquet Direct only reads from your storage, so a read-only permission set is sufficient. For the read-only
permissions for each cloud provider, see [Read-only vs write access for Delta Direct on each storage provider](/user-guide/tables-iceberg-metadata#label-tables-iceberg-ev-delta-read-write-options).

## Step 4: Create a catalog integration

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

## Step 5: Create a Parquet Direct table

Create a table by using the [CREATE ICEBERG TABLE (Parquet files in object storage)](/sql-reference/sql/create-iceberg-table-parquet) command with `AUTO_REFRESH = TRUE`.
The following example omits the column list, so Snowflake infers the schema from your Parquet files. It also sets
`ENABLE_SCHEMA_EVOLUTION = TRUE` so that Snowflake evolves the schema on later refreshes:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE orders
  EXTERNAL_VOLUME = 'parquet_azure_exvol'
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

## Step 6: Verify auto-refresh

1. Query the table to confirm that Snowflake registered the existing files:

   Copy code

   ```
   SELECT COUNT(*) FROM orders;
   ```
2. Upload a new Parquet file to the table’s base location; for example, by using the Azure CLI:

   Copy code

   ```
   az storage blob upload \
     --account-name <data_storage_account_name> \
     --container-name mycontainer \
     --name inbound/orders/year=2025/month=02/part-0002.parquet \
     --file part-0002.parquet
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
your Parquet files in Azure.

Copy code

```
DROP ICEBERG TABLE orders;
DROP CATALOG INTEGRATION hive_catalog_int;
DROP CATALOG INTEGRATION parquet_catalog_int;
DROP EXTERNAL VOLUME parquet_azure_exvol;
DROP NOTIFICATION INTEGRATION parquet_azure_notification_int;
```

If you no longer need them, also delete the Event Grid subscription, storage queue, and resource group in Azure.

## What’s next

- Learn about best practices, monitoring, troubleshooting, and billing in [Parquet Direct](/user-guide/tables-iceberg-parquet-direct).
- Compare Parquet Direct with Delta Direct in [Direct Iceberg tables](/user-guide/tables-iceberg-direct).
- See all parameters in [CREATE ICEBERG TABLE (Parquet files in object storage)](/sql-reference/sql/create-iceberg-table-parquet).
