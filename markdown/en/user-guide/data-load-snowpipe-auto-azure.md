# Automate Snowpipe for Microsoft Azure Blob Storage

This topic describes how to set up a pipe that loads files from Microsoft Azure storage as soon as they arrive. When a file is created in your container, [Microsoft Azure Event Grid](https://learn.microsoft.com/en-us/azure/event-grid/overview) sends an event message to an Azure Queue Storage queue. Snowflake reads the message from the queue, and Snowpipe loads the file into your target table. For an overview of automated loading on every cloud provider, see [Automate Snowpipe with cloud event notifications](/user-guide/data-load-snowpipe-auto).

To have [CoCo](/user-guide/cortex-code/cortex-code) set up the pipeline from your Azure storage path instead, see [Set up continuous file ingestion with CoCo](/user-guide/data-load-snowpipe-auto-coco). Depending on the setup option you choose, CoCo creates the Snowflake objects (such as the integrations, stage, and pipe), generates Terraform or an ARM template for your team to deploy, or does some of each. CoCo also guides you through any follow-up authorization and notification steps, so that you don’t need to follow the steps in this topic manually.

To set up automated loading from Microsoft Azure storage, complete the following steps:

1. [Create a storage integration and an external stage](#label-data-load-snowpipe-azure-storage) so that Snowflake can read the container.
2. [Create a storage queue and an Event Grid subscription](#label-azure-configuring-automation) that sends events about new files to the queue.
3. [Create a notification integration](#label-data-load-snowpipe-auto-azure-integration) that points to the queue.
4. [Grant Snowflake access to the storage queue](#label-data-load-snowpipe-auto-azure-grant-queue).
5. [Create the pipe](#label-snowpipe-automation-azure-create-pipe).
6. [Test the pipe](#label-data-load-snowpipe-auto-azure-verify).
7. [Load the files that are already in the container](#label-data-load-snowpipe-auto-azure-existing-files).

The examples in this topic load JSON files from the `orders/` path in the `mycontainer` container of the `mydataaccount` storage account into the `mydb.myschema.orders` table. They use the `orders_pipe_owner` role from [Create a role to own the pipe (recommended)](#label-data-load-snowpipe-auto-azure-owner-role). If you skip that section, use a role that has the required privileges. The storage queue is in the `myqueueaccount` storage account, and both storage accounts are in the `myresourcegroup` resource group.

To keep traffic between Snowflake and your storage queue off the public internet, you can use private connectivity. For more information, see [Private connectivity to external stages and Snowpipe automation for Microsoft Azure](/user-guide/data-load-azure-private).

## Supported storage and events

Snowpipe supports automated loading from Blob Storage, Data Lake Storage Gen2, and general-purpose v2 storage accounts. It doesn’t support Microsoft Fabric OneLake: you can create a pipe for a OneLake stage, but the pipe doesn’t load any files, and Snowflake doesn’t report an error. For the storage services that automated loading supports on every cloud provider, see [Supported storage and accounts](/user-guide/data-load-snowpipe-auto#label-snowpipe-auto-supported).

Snowpipe loads a file when it receives a `Microsoft.Storage.BlobCreated` event for one of the following API operations:

| Operation | When Azure sends it |
| --- | --- |
| `PutBlob` | A client uploads a blob in a single request. |
| `PutBlockList` | A client commits a blob that it uploaded in blocks. |
| `CopyBlob` | A client copies a blob into the container. |
| `FlushWithClose` | A Data Lake Storage Gen2 client finishes writing a file. A `CreateFile` operation alone doesn’t mean that the file is complete, so Snowpipe waits for `FlushWithClose`. |
| `SftpCommit` | An SSH File Transfer Protocol (SFTP) client finishes writing a file. An `SftpCreate` operation alone doesn’t mean that the file is complete, so Snowpipe waits for `SftpCommit`. |

Expand

Show lessSee more

Renaming a file or directory doesn’t send these events, so Snowpipe doesn’t load renamed files. If a client doesn’t send the final operation for a file, such as `FlushWithClose`, Snowpipe doesn’t load the file. For more information, see [Files in Azure Data Lake Storage Gen2 don’t load](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-adls-gen2).

Snowflake supports only the [Event Grid event schema](https://learn.microsoft.com/en-us/azure/event-grid/event-schema). It doesn’t support the [CloudEvents schema](https://learn.microsoft.com/en-us/azure/event-grid/cloud-event-schema). If an event subscription uses the CloudEvents schema, Snowpipe ignores its messages without reporting an error, and files don’t load.

## Before you begin

Make sure that you have the following:

- **A target table.** Snowpipe loads files into an existing standard table or [Apache Iceberg™ table](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-iceberg).
- **Snowflake privileges.** The role that creates the pipe needs the privileges in the **Create a pipe** column of [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control), including the `USAGE` privilege on the notification integration. Creating the storage integration and the notification integration requires the `CREATE INTEGRATION` privilege on the account, which only the `ACCOUNTADMIN` role has by default.
- **Azure permissions.** You need permission to create storage queues and Event Grid subscriptions, to grant consent to applications in your Microsoft Entra ID tenant, and to assign roles on the storage queue.
- **The Azure CLI.** The examples in this topic use the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli). You can also complete the steps in the Azure portal.

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

Snowpipe reads files through an external stage that points to your container. If you already have an external stage for the path that you want to load, make sure that its URL ends with a forward slash (`/`). If you created a role to own the pipe, grant it the `USAGE` privilege on the stage, as shown at the end of this step. Then continue with [Step 2](#label-azure-configuring-automation).

Snowflake recommends that the stage use a storage integration, so that you don’t store a shared access signature (SAS) token in Snowflake. To create a storage integration, grant Snowflake access to the storage account, and create a stage, follow the steps in [Configure a Snowflake storage integration](/user-guide/data-load-azure-config#label-configuring-azure-storage-integration). Creating a stage that uses a storage integration requires the `CREATE STAGE` privilege on the schema and the `USAGE` privilege on the integration. If you just created the pipe owner role, switch from the `SECURITYADMIN` role to a role that has these privileges. For example:

Copy code

```
CREATE STAGE mydb.myschema.orders_stage
  URL = 'azure://mydataaccount.blob.core.windows.net/mycontainer/orders/'
  STORAGE_INTEGRATION = my_azure_int;
```

Use the `blob.core.windows.net` endpoint in the URL for every supported type of storage account, including Data Lake Storage Gen2.

Important

End the stage URL with a forward slash (`/`). Without it, the stage also includes every folder and file whose name starts with the same characters. For example, a URL that ends in `orders` also includes `orders_archive/`, so the pipe loads files that you didn’t intend.

To confirm that Snowflake can read the container, list the files in the stage:

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

## Step 2: Create a storage queue and an Event Grid subscription

Event Grid sends an event message to a storage queue each time a file is created in the storage account that holds your data. Snowflake reads the messages from the queue.

If you already have a storage queue and a notification integration for Snowflake, you can reuse them. Create an Event Grid subscription that sends events to that queue, as shown in the last step of this section, and then continue with [Step 5](#label-snowpipe-automation-azure-create-pipe). If you created a role to own the pipe, first grant it the `USAGE` privilege on the existing integration, as shown at the end of [Step 3](#label-data-load-snowpipe-auto-azure-integration). Use a role that owns the integration or has the `MANAGE GRANTS` privilege, such as `SECURITYADMIN`.

1. If you haven’t used Event Grid in your Azure subscription before, register the Event Grid resource provider:

   Copy code

   ```
   az provider register --namespace Microsoft.EventGrid
   ```

   Registration can take a few minutes. To check its status, run `az provider show --namespace Microsoft.EventGrid --query registrationState`.
2. Choose a storage account for the queue. The account that hosts the queue must be a general-purpose v2 (`StorageV2`) account. If your data is already in a general-purpose v2 account, you can create the queue in the same account. Otherwise, create a general-purpose v2 account for the queue:

   Copy code

   ```
   az storage account create --name myqueueaccount --resource-group myresourcegroup --location eastus --kind StorageV2 --sku Standard_LRS
   ```
3. Create the storage queue:

   Copy code

   ```
   az storage queue create --name snowpipe-orders --account-name myqueueaccount
   ```

   One storage queue can collect the event messages from many Event Grid subscriptions. For best performance, Snowflake recommends one storage queue for all of the Event Grid subscriptions that you create for Snowflake.

   Use this queue only for Snowflake. If another application also reads messages from it, Snowflake doesn’t receive those messages, and the pipe misses files. If other applications need the same events, create a separate Event Grid subscription and storage queue for each of them.
4. Create an Event Grid subscription on the storage account that holds your data. The subscription sends `Microsoft.Storage.BlobCreated` events to the storage queue, filtered to the [supported operations](#label-data-load-snowpipe-auto-azure-supported) and to files under the path that the pipe loads. Choose the tab for your shell:

   BashPowerShell

   Copy code

   ```
   storageid=$(az storage account show --name mydataaccount --resource-group myresourcegroup --query id --output tsv)
   queuestorageid=$(az storage account show --name myqueueaccount --resource-group myresourcegroup --query id --output tsv)
   queueid="$queuestorageid/queueservices/default/queues/snowpipe-orders"

   az eventgrid event-subscription create \
     --name snowpipe-orders \
     --source-resource-id "$storageid" \
     --endpoint-type storagequeue \
     --endpoint "$queueid" \
     --included-event-types Microsoft.Storage.BlobCreated \
     --subject-begins-with /blobServices/default/containers/mycontainer/blobs/orders/ \
     --advanced-filter data.api stringin CopyBlob PutBlob PutBlockList FlushWithClose SftpCommit
   ```

   Copy code

   ```
   $storageid = az storage account show --name mydataaccount --resource-group myresourcegroup --query id --output tsv
   $queuestorageid = az storage account show --name myqueueaccount --resource-group myresourcegroup --query id --output tsv
   $queueid = "$queuestorageid/queueservices/default/queues/snowpipe-orders"

   az eventgrid event-subscription create `
     --name snowpipe-orders `
     --source-resource-id $storageid `
     --endpoint-type storagequeue `
     --endpoint $queueid `
     --included-event-types Microsoft.Storage.BlobCreated `
     --subject-begins-with /blobServices/default/containers/mycontainer/blobs/orders/ `
     --advanced-filter data.api stringin CopyBlob PutBlob PutBlockList FlushWithClose SftpCommit
   ```

   The `--subject-begins-with` filter limits events to the `orders/` path in the container. To cover every pipe that loads from the storage account, omit it. Don’t change the event delivery schema from the default Event Grid schema. For more information, see [Filter events for Event Grid](https://learn.microsoft.com/en-us/azure/event-grid/event-filtering) in the Azure documentation.

## Step 3: Create a notification integration

A notification integration is a Snowflake object that stores the URL of your storage queue and identifies the Azure application that Snowflake uses to read it.

1. Get the URL of the storage queue and the ID of your Microsoft Entra ID tenant:

   Copy code

   ```
   az storage account show --name myqueueaccount --resource-group myresourcegroup --query primaryEndpoints.queue --output tsv
   az account show --query tenantId --output tsv
   ```

   The queue URL is the queue endpoint followed by the queue name, such as `https://myqueueaccount.queue.core.windows.net/snowpipe-orders`.
2. Create the integration with the [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration-queue-inbound-azure) command:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   CREATE NOTIFICATION INTEGRATION my_azure_notification_int
     ENABLED = TRUE
     TYPE = QUEUE
     NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE
     AZURE_STORAGE_QUEUE_PRIMARY_URI = 'https://myqueueaccount.queue.core.windows.net/snowpipe-orders'
     AZURE_TENANT_ID = 'a123bcde-1234-5678-abc1-9abc12345678';
   ```

Keep the following in mind:

- The Azure application for notification integrations is different from the application that your storage integration uses, so you grant access to each one separately.
- Each notification integration reads from one storage queue. Several pipes can use the same notification integration, but you can’t create a pipe that uses a different integration for a queue that another pipe already reads.

If you created a role to own the pipe, grant it the `USAGE` privilege on the integration. The role needs this privilege to create a pipe that uses the integration:

Copy code

```
GRANT USAGE ON INTEGRATION my_azure_notification_int TO ROLE orders_pipe_owner;
```

## Step 4: Grant Snowflake access to the storage queue

1. Get the consent URL and the name of the Snowflake application from the `AZURE_CONSENT_URL` and `AZURE_MULTI_TENANT_APP_NAME` properties in the output of [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration):

   Copy code

   ```
   DESC NOTIFICATION INTEGRATION my_azure_notification_int;
   ```
2. In a web browser, open the URL from `AZURE_CONSENT_URL`, and then select **Accept**. Azure starts creating a service principal for the Snowflake application in your tenant, and the page redirects to the Snowflake website.
3. In the Azure portal, go to **Microsoft Entra ID** » **Enterprise applications**, and search for the part of the `AZURE_MULTI_TENANT_APP_NAME` value before the underscore to confirm that the Snowflake application is listed.

   It can take an hour or longer for Azure to create the service principal. If the application isn’t listed yet, wait, and then search again.
4. Open the storage account that hosts the queue, such as `myqueueaccount`, and then select **Data storage** » **Queues** » **snowpipe-orders** » **Access control (IAM)** » **Add** » **Add role assignment**.
5. On the **Role** tab, select **Storage Queue Data Contributor**, and then select **Next**. On the **Members** tab, choose **Select members**, search for the part of the `AZURE_MULTI_TENANT_APP_NAME` value before the underscore, select the Snowflake application, and then choose **Select**. Select **Review + assign**.

   Role assignments can take a few minutes to take effect.

Important

If you delete the Snowflake application from your tenant, or remove its role assignment, the notification integration stops working, and pipes that use it stop loading files.

## Step 5: Create the pipe

Create the pipe with the [CREATE PIPE](/sql-reference/sql/create-pipe) command. Set `AUTO_INGEST = TRUE`, and set `INTEGRATION` to the name of your notification integration as a string. The string must match the name exactly as Snowflake stores it, which is in uppercase letters unless you enclosed the name in double quotes when you created the integration. Before you create the pipe, check that its location doesn’t overlap the location of another pipe, as described in [Give each pipe its own location](/user-guide/data-load-snowpipe-auto#label-snowpipe-auto-pipe-paths). For example, the following statement creates a pipe named `orders_pipe` that loads JSON files from the `orders_stage` stage into the `orders` table:

Copy code

```
USE ROLE orders_pipe_owner;

CREATE PIPE mydb.myschema.orders_pipe
  AUTO_INGEST = TRUE
  INTEGRATION = 'MY_AZURE_NOTIFICATION_INT'
  AS
  COPY INTO mydb.myschema.orders
    FROM @mydb.myschema.orders_stage
    FILE_FORMAT = (TYPE = 'JSON')
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

If the `CREATE PIPE` statement fails with a `Could not access queue` error, Snowflake can’t read the storage queue. Check that the Snowflake application is listed in your tenant and has the Storage Queue Data Contributor role on the queue, as described in [Step 4](#label-data-load-snowpipe-auto-azure-grant-queue). Role assignments can take a few minutes to take effect, so wait, and then run the statement again. If the queue URL in the notification integration is wrong, you can’t change it with [ALTER NOTIFICATION INTEGRATION](/sql-reference/sql/alter-notification-integration-queue-inbound-azure). Instead, create a notification integration with the correct URL, as described in [Step 3](#label-data-load-snowpipe-auto-azure-integration), grant the `USAGE` privilege on it to the role that creates the pipe, and then create the pipe with the new integration.

To load only part of the stage, add a path after the stage name in the `FROM` clause, such as `@mydb.myschema.orders_stage/2026/`. End the path with a forward slash (`/`).

## Step 6: Test the pipe

1. Check that the pipe is running and that Snowflake can read the storage queue:

   Copy code

   ```
   SELECT SYSTEM$PIPE_STATUS('mydb.myschema.orders_pipe');
   ```

   The `executionState` field should be `RUNNING`. If it isn’t, see [Pipe execution states](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-execution-states). If the output includes a `channelErrorMessage` field, Snowflake can’t read the queue, and the pipe doesn’t load files. Check that the queue still exists and that the Snowflake application still has the role assignment from [Step 4](#label-data-load-snowpipe-auto-azure-grant-queue).
2. Upload a test file to the path that the pipe loads:

   Copy code

   ```
   az storage blob upload --account-name mydataaccount --container-name mycontainer --name orders/orders_test.json --file orders_test.json
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

   If the file isn’t listed, call `SYSTEM$PIPE_STATUS` again. If `lastReceivedMessageTimestamp` is missing or older than your upload, event messages aren’t reaching Snowflake. If it’s newer than your upload but `lastForwardedMessageTimestamp` is missing or older than your upload, event messages arrive, but none of them are for the pipe’s path. For the steps to fix these and other problems, see [Files don’t load with automated loading](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-auto-ingest).

## Step 7: Load files that are already in the container

The pipe loads only files that arrive after you create the Event Grid subscription. To load the files that were already in the stage, run the following command:

Copy code

```
ALTER PIPE mydb.myschema.orders_pipe REFRESH;
```

`REFRESH` queues only files that were staged within the last 7 days and that the pipe hasn’t already processed. Files that failed to load count as processed, so `REFRESH` doesn’t queue them again. To reload them, see [Reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files). To load older files, see [Files staged more than 7 days ago](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-backfill).

## After you set up the pipe

- **Add more pipes.** Other pipes can use the same notification integration if the Event Grid subscription covers their paths. To load from another storage account, create a stage for it, and make sure that the stage’s storage integration can access the account, as described in [Step 1](#label-data-load-snowpipe-azure-storage). Then create an Event Grid subscription on that account that sends events to the same storage queue, as described in [Step 2](#label-data-load-snowpipe-auto-azure-event-grid). If a different role creates the new pipe, grant that role the `USAGE` privilege on the notification integration, as shown at the end of [Step 3](#label-data-load-snowpipe-auto-azure-integration). Use a role that owns the integration or has the `MANAGE GRANTS` privilege, such as `SECURITYADMIN`.
- **Let other roles monitor or operate the pipe.** To check the pipe’s status, a role needs the `USAGE` privilege on the database and schema and the `MONITOR` privilege on the pipe. To pause or resume the pipe, it also needs the `OPERATE` privilege. To refresh the pipe, it also needs privileges on the stage and the target table, as listed in the **Refresh a pipe** column of [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control). For example, run the following statements with a role that has the `MANAGE GRANTS` privilege, such as `SECURITYADMIN`:

  Copy code

  ```
  USE ROLE SECURITYADMIN;

  GRANT USAGE ON DATABASE mydb TO ROLE data_engineer;
  GRANT USAGE ON SCHEMA mydb.myschema TO ROLE data_engineer;
  GRANT MONITOR, OPERATE ON PIPE mydb.myschema.orders_pipe TO ROLE data_engineer;
  ```
- **Get notified about failed loads.** Set up [error notifications](/user-guide/data-load-snowpipe-errors) to receive a message in the messaging service on your Snowflake account’s cloud platform when a file fails to load. Set up an [alert](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-alerts) to find out when the pipe stops loading or Snowflake can’t read the storage queue.
- **Clean up loaded files.** Snowpipe doesn’t delete files after it loads them. To manage storage costs, see [Delete files after Snowpipe loads them](/user-guide/data-load-snowpipe-manage#label-snowpipe-delete-data-files).
