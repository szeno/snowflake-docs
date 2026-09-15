# Private connectivity to external stages and Snowpipe automation for Microsoft Azure

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides configuration details to set up [outbound private connectivity](/user-guide/private-connectivity-outbound) for the
following Snowflake features:

- Bulk loading from Microsoft Azure using an external stage.
- Automating Snowpipe for Microsoft Azure Blob Storage.

The differences between configuring bulk loading and Snowpipe automation for private connectivity and configuring them for public network
traffic consists of the following:

- Setting `USE_PRIVATELINK_ENDPOINT = TRUE` for the required storage integration, stage, or notification integration.
- Creating a private connectivity endpoint for the external stage (bulk loading and Snowpipe automation).
- Creating a private connectivity endpoint for the notification integration (Snowpipe automation only).

## Outbound private connectivity costs

You pay for each private connectivity endpoint along with total data processed. For pricing of these items, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You can explore the cost of these items by filtering on the following service types when querying billing views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas:

- OUTBOUND\_PRIVATELINK\_ENDPOINT
- OUTBOUND\_PRIVATELINK\_DATA\_PROCESSED

For example, you can query the [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) view and filter on these service types.

## Considerations

Note

Private connectivity isn’t supported for Microsoft Fabric OneLake storage.

You can configure outbound public connectivity and outbound private connectivity for the same storage account. If you want to do this,
create a dedicated storage integration for outbound public connectivity and specify `USE_PRIVATELINK_ENDPOINT = FALSE`.

## Private connectivity property

The `USE_PRIVATELINK_ENDPOINT` property of a storage integration or external stage determines whether it is accessed through private
connectivity or by traversing the public network. To use private connectivity, set `USE_PRIVATELINK_ENDPOINT = TRUE`.

A stage that references a storage integration that specifies `USE_PRIVATELINK_ENDPOINT = TRUE` inherits the private endpoint
configuration. As a result, if you are using a storage integration that is configured to use private connectivity, you do not need to
specify the `USE_PRIVATELINK_ENDPOINT` property in the stage, and you cannot modify the stage to set the
`USE_PRIVATELINK_ENDPOINT` property.

## Configure external stage access

These steps are unique to using outbound private connectivity with a storage integration to unload data to an external stage on Microsoft Azure.
You need to modify the flow if you are using the stage’s `CREDENTIALS` property instead of referencing a storage integration.

These steps are required for both bulk loading and Snowpipe automation.

1. In Snowflake, call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision a
   private connectivity endpoint in your Snowflake VNet to enable Snowflake to connect to your external Blob storage account using private
   connectivity:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     '/subscriptions/cc2909f2-ed22-4c89-8e5d-bdc40e5eac26/resourceGroups/mystorage/providers/Microsoft.Storage/storageAccounts/storagedemo',
     'mystorageaccount.blob.core.windows.net',
     'blob'
   );
   ```

   This function binds the private endpoint to the hostname, which enables the storage integration to use the private endpoint to connect
   to the storage location.
2. In the Azure Portal and as the owner of the Microsoft Azure Blob storage resource, approve the private endpoint. For details, see the
   [approval process](https://learn.microsoft.com/en-us/azure/private-link/manage-private-endpoint?tabs=manage-private-link-powershell#private-endpoint-connections).
3. In Snowflake, call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) function.

   When the output of the function includes `"status": "APPROVED"`, your connection from Snowflake to your storage account will be
   able to use private connectivity (after the other necessary Snowflake objects are enabled for outbound private connectivity).

   You can continue with the next steps while waiting for the `"APPROVED"` status.
4. Create a storage integration and be sure to specify the `USE_PRIVATELINK_ENDPOINT` property:

   Copy code

   ```
   CREATE OR REPLACE STORAGE INTEGRATION outbound_private_link_int
     TYPE = EXTERNAL_STAGE
     STORAGE_PROVIDER = AZURE
     AZURE_TENANT_ID = 'cc2909f2-ed22-4c89-8e5d-bdc40e5eac26'
     STORAGE_ALLOWED_LOCATIONS = ('azure://mystorageaccount.blob.core.windows.net/mycontainer/snowflake_privatelink_external_stage_test/')
     USE_PRIVATELINK_ENDPOINT = TRUE
     ENABLED = TRUE;
   ```

   Note

   After you create the storage integration, you must grant Snowflake access to your storage locations. For more information, see
   [Configuring a Snowflake storage integration](/user-guide/data-load-azure-config#label-configuring-azure-storage-integration).
5. Create an external stage that references the storage integration:

   Copy code

   ```
   CREATE OR REPLACE STAGE my_storage_private_stage
     URL = 'azure://mystorageaccount.blob.core.windows.net/mycontainer/snowflake_privatelink_external_stage_test/'
     STORAGE_INTEGRATION = outbound_private_link_int;
   ```
6. After the private endpoint has an `"APPROVED"` status, test unloading data from Snowflake to the external stage:

   Copy code

   ```
   COPY INTO @my_storage_private_stage
     FROM mytable
     FILE_FORMAT = (FORMAT_NAME = my_csv_format);
   ```
7. View the result in your Microsoft Azure stage.

## Syntax update for notification integrations

Automating Snowpipe for Microsoft Azure Blob Storage requires you to create a notification integration. The following syntax update allows
you to configure the notification integration for private connectivity.

Copy code

```
CREATE [ OR REPLACE ] NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
  ...
  USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }
```

## Configure Snowpipe automation

This section modifies the procedures described in [Automating Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure) to highlight how to implement Snowpipe
automation with private connectivity. The only differences are provisioning private connectivity endpoints and configuring the
`USE_PRIVATELINK_ENDPOINT` property of the storage integration and notification integration.

1. Create a storage integration and stage, along with its dedicated private connectivity endpoint, as described
   [earlier in this document](#label-private-connectivity-azure-configure-stage).
2. [Grant Snowflake access to the storage locations](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-auto-azure#step-2-grant-snowflake-access-to-the-storage-locations),
   as described in the Automating Snowpipe for Microsoft Azure Blob Storage topic.
3. [Configure the Event Grid Subscription](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-auto-azure#step-1-configuring-the-event-grid-subscription),
   as described in the Automating Snowpipe for Microsoft Azure Blob Storage topic.
4. In Snowflake, call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision a
   private endpoint in your Snowflake VNet to enable Snowflake to connect to your Azure queue using private
   connectivity:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     '/subscriptions/cc2909f2-ed22-4c89-8e5d-bdc40e5eac26/resourceGroups/mystorage/providers/Microsoft.Storage/storageAccounts/mystorageaccount',
    'mystorageaccount.queue.core.windows.net',
    'queue'
   );
   ```
5. In the Azure Portal and as the owner of the Microsoft Azure Storage resource, approve the private endpoint. For information, see the
   [approval process](https://learn.microsoft.com/en-us/azure/private-link/manage-private-endpoint?tabs=manage-private-link-powershell#private-endpoint-connections).
6. In Snowflake, call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) function.

   When the output of the function includes `"status": "APPROVED"`, your connection from Snowflake to your storage account will be
   able to use private connectivity (after the other necessary Snowflake objects are enabled for outbound private connectivity).

   Important

   You must wait until the status is `APPROVED` before continuing with the next step.
7. [Retrieve the storage queue URL and tenant ID](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-auto-azure#retrieve-the-storage-queue-url-and-tenant-id),
   as described in the Automating Snowpipe for Microsoft Azure Blob Storage topic.
8. Create a notification integration and be sure to specify the `USE_PRIVATELINK_ENDPOINT` property:

   Copy code

   ```
   CREATE OR REPLACE NOTIFICATION INTEGRATION ni_pl
     ENABLED = TRUE
     TYPE = QUEUE
     NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE
     AZURE_STORAGE_QUEUE_PRIMARY_URI = "https://storageaccount.queue.core.windows.net/queuename"
     AZURE_TENANT_ID = '00000000-0000-0000-0000-000000000000'
     USE_PRIVATELINK_ENDPOINT = TRUE;
   ```
9. [Grant Snowflake access to the storage queue](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-auto-azure#grant-snowflake-access-to-the-storage-queue),
   as described in the Automating Snowpipe for Microsoft Azure Blob Storage topic.
10. [Create a pipe with auto-ingest enabled](/user-guide/data-load-snowpipe-auto-azure#label-snowpipe-automation-azure-create-pipe), as described in the Automating Snowpipe for
    Microsoft Azure Blob Storage topic.

## Disable private connectivity

The process of disabling private connectivity varies depending on whether the endpoint was provisioned for a storage integration, an
external stage, or a notification integration.

Storage integration/external stage
:   If you no longer need the private connectivity endpoint for the external stage, unset the
    `USE_PRIVATELINK_ENDPOINT` property on the stage or storage integration, and then call the
    [SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) system function.

Notification integration
:   Unlike storage integrations and external stages, you cannot unset the `USE_PRIVATELINK_ENDPOINT` property of a notification
    integration. If you no longer need private connectivity, you need to drop the notification integration, then create a new one. After
    recreating the notification integration, you can call the SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT system function to deprovision the
    endpoint.
