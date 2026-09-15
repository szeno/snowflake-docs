# Private connectivity to external volumes for Microsoft Azure

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides configuration details to set up outbound private connectivity to an external volume on Microsoft Azure. The primary difference
between outbound public connectivity and outbound private connectivity is how you set the `USE_PRIVATELINK_ENDPOINT` property for
the external volume.

When the external volume is configured to use private connectivity, your connection to the Microsoft Azure cloud storage services goes through the
Microsoft Azure internal network. By configuring your external volume to use outbound private connectivity, you add additional security to your
operations by blocking public access to the storage account.

For more information about using external volumes to connect to your external cloud storage for Iceberg tables, see
[Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

## Outbound private connectivity costs

You pay for each private connectivity endpoint along with total data processed. For pricing of these items, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You can explore the cost of these items by filtering on the following service types when querying billing views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas:

- OUTBOUND\_PRIVATELINK\_ENDPOINT
- OUTBOUND\_PRIVATELINK\_DATA\_PROCESSED

For example, you can query the [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) view and filter on these service types.

## Considerations and limitations

- You can use private connectivity to access Snowflake-managed Iceberg tables and Iceberg tables that use a catalog integration for object
  storage. In addition, you can use private connectivity to access externally managed Iceberg tables and Iceberg tables created from Delta files
  in object storage.
- You can configure outbound public connectivity and outbound private connectivity for the same cloud storage service. If you want to do
  this, create a dedicated external volume for outbound public connectivity and specify `USE_PRIVATELINK_ENDPOINT = FALSE`.

## Set up outbound private connectivity to an external volume

To set up outbound private connectivity to an external volume, you can [use SQL](#label-configure-external-volume-azure-private-sql) or
[use Snowsight](#label-configure-external-volume-azure-private-snowsight).

### Use SQL

#### Private connectivity property

The `USE_PRIVATELINK_ENDPOINT` property of an external volume determines whether it is accessed through private connectivity or
by traversing the public network. To use private connectivity, set `USE_PRIVATELINK_ENDPOINT = TRUE` when creating or modifying an external
volume.

#### Configure external volume access using private connectivity

Use the following steps to use outbound private connectivity to unload data to an external volume on Microsoft Azure:

1. In Snowflake, call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision a
   private connectivity endpoint in your Snowflake VNet to enable Snowflake to connect to your external Microsoft Azure cloud storage services using
   private connectivity:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     '/subscriptions/cc2909f2-ed22-4c89-8e5d-bdc40e5eac26/resourceGroups/mystorage/providers/Microsoft.Storage/storageAccounts/storagedemo',
     'mystorageaccount.blob.core.windows.net',
     'blob'
   );
   ```

   This function binds the private endpoint to the hostname, which enables the external volume to use the private endpoint to connect
   to the storage location.

   Note

   If you are using a Data Lake Storage storage account (with a DFS endpoint), you must provision two private connectivity endpoints
   for the storage account: one for the `blob` service and one for the `dfs` service. For an example, see
   .
2. In the Azure Portal and as the owner of the Microsoft Azure storage resource, approve the private endpoint. For details, see the
   [approval process](https://learn.microsoft.com/en-us/azure/private-link/manage-private-endpoint?tabs=manage-private-link-powershell#private-endpoint-connections).
3. In Snowflake, call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) function.

   When the output of the function includes `"status": "APPROVED"`, your connection from Snowflake to your storage account will be
   able to use private connectivity.

   You can continue with the next steps while waiting for the `"APPROVED"` status.
4. Create the external volume, being sure to set the `USE_PRIVATELINK_ENDPOINT` property to `TRUE`:

   Copy code

   ```
   CREATE EXTERNAL VOLUME exvol
     STORAGE_LOCATIONS =
    (
      (
        NAME = 'my-azure-northeurope'
        STORAGE_PROVIDER = 'AZURE'
        STORAGE_BASE_URL = 'azure://exampleacct.blob.core.windows.net/my_container_northeurope/'
        AZURE_TENANT_ID = 'a123b4c5-1234-123a-a12b-1a23b45678c9'
        USE_PRIVATELINK_ENDPOINT = TRUE
      )
    );
   ```
5. After the private endpoint has an `"APPROVED"` status, test accessing the external volume with a supported operation.

### Use Snowsight

To set up external volume access through private connectivity in Snowsight, follow these steps:

1. In Snowflake, call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision a
   private connectivity endpoint in your Snowflake VNet to enable Snowflake to connect to your external Microsoft Azure cloud storage services using
   private connectivity:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     '/subscriptions/cc2909f2-ed22-4c89-8e5d-bdc40e5eac26/resourceGroups/mystorage/providers/Microsoft.Storage/storageAccounts/storagedemo',
     'mystorageaccount.blob.core.windows.net',
     'blob'
   );
   ```

   This function binds the private endpoint to the hostname, which enables the external volume to use the private endpoint to connect
   to the storage location.

   Note

   If you are using a Data Lake Storage storage account (with a DFS endpoint), you must provision two private connectivity endpoints
   for the storage account: one for the `blob` service and one for the `dfs` service. For an example, see
   .
2. In the Azure Portal and as the owner of the Microsoft Azure storage resource, approve the private endpoint. For details, see the
   [approval process](https://learn.microsoft.com/en-us/azure/private-link/manage-private-endpoint?tabs=manage-private-link-powershell#private-endpoint-connections).
3. In Snowflake, call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) function.

   When the output of the function includes `"status": "APPROVED"`, your connection from Snowflake to your storage account will be
   able to use private connectivity.

   You can continue with the next steps while waiting for the `"APPROVED"` status.
4. Follow the steps to
   [Configure an external volume for Azure in Snowsight](/user-guide/tables-iceberg-configure-external-volume-azure#label-configure-external-volume-azure-create-snowsight)
   and enable private connectivity when you configure the external volume.

   Important

   To enable private connectivity, on the **Configure external volume** page, from the **Connectivity** field, you must select
   **Private (Azure Private Endpoint)**.
5. After the private endpoint has an `"APPROVED"` status, test accessing the external volume with a supported operation.

## Deprovision an endpoint

If you no longer need the private connectivity endpoint for the external volume, unset the
`USE_PRIVATELINK_ENDPOINT` property on the external volume, and then call the
[SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) system function.

**Next Topics:**

- [Manage private connectivity endpoints: Azure](/user-guide/private-manage-endpoints-azure)
