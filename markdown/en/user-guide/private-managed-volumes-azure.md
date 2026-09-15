# Azure private endpoints for Snowflake-managed storage volumes

This topic provides concepts and detailed instructions for connecting to Snowflake-managed storage volumes through Microsoft
Azure private endpoints. Snowflake-managed storage volumes are the storage locations for
[Apache Iceberg tables that use Snowflake as the catalog](/user-guide/tables-iceberg).

## Overview

When you use an external query engine such as Apache Spark or Databricks to read from or write to an iceberg table that uses
Snowflake-managed storage, the query engine communicates directly with the native iceberg volume hosted on Azure Storage. By
default, this traffic can traverse the public internet.

[Azure private endpoints](https://docs.microsoft.com/en-us/azure/private-link/private-endpoint-overview) and
[Azure Private Link](https://docs.microsoft.com/en-us/azure/private-link/private-link-overview) can be combined to provide
secure connectivity to Snowflake-managed storage volumes. This setup ensures that read and write operations from your external
query engine to the native iceberg volume use the Azure internal network instead of the public internet.

## Benefits

Implementing private endpoints to access Snowflake-managed storage volumes provides the following advantages:

- Data doesn’t traverse the public internet when external query engines read from or write to the native iceberg volume.
- Administrators can implement consistent security and monitoring for how query engines connect to storage accounts.
- Administrators aren’t required to modify firewall settings to access storage volume data.

## Limitations

Microsoft Azure defines how a private endpoint can interact with Snowflake:

- A single private endpoint can communicate to a single Snowflake Service Endpoint. You can have multiple one-to-one
  configurations that connect to the same managed storage volume.
- The maximum number of private endpoints in your storage account that can connect to a Snowflake-managed storage volume is fixed.
  For details, see
  [Standard storage account limits](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#standard-storage-account-limits).

## Configuring private endpoints to access Snowflake-managed storage volumes

To configure private endpoints to access Snowflake-managed storage volumes, you must have support from the following three roles in
your organization:

1. The Snowflake account administrator (that is, a user with the Snowflake ACCOUNTADMIN system role).
2. The Microsoft Azure administrator.
3. The network administrator.

Depending on the organization, it may be necessary to coordinate the configuration efforts with more than one person or team to
implement the following configuration steps.

Complete the following steps to configure and implement secure access to Snowflake-managed storage volumes through Azure private
endpoints:

1. Verify that your Azure subscription is registered with the Azure Storage resource manager. This step allows you to connect to
   the managed storage volume from a private endpoint.
2. As a Snowflake account administrator, run the following commands in your Snowflake account. Record the resource ID of your non-failsafe and failsafe
   Snowflake-managed storage volume’s storage account respectively defined by the `privatelink-snowflake-managed-storage-volume-nfs` and
   `privatelink-snowflake-managed-storage-volume-fs` keys. For more information, see
   [ENABLE\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PRIVATELINK](/sql-reference/parameters#label-enable-snowflake-managed-storage-volume-privatelink) and
   [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config).

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   ALTER ACCOUNT SET ENABLE_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PRIVATELINK = true;
   SELECT KEY, VALUE FROM TABLE(FLATTEN(input=>PARSE_JSON(SYSTEM$GET_PRIVATELINK_CONFIG())));
   ```
3. As the Azure administrator, create a private endpoint through the Azure portal to each of your Snowflake-managed storage volumes.

   View the private endpoint properties and record the resource ID value. You provide this value as the
   `privateEndpointResourceID` function argument in the next step.

   For more information, see the Microsoft Azure Private Link [documentation](https://docs.microsoft.com/en-us/azure/private-link/).

   Important

   Before you proceed with the next step to authorize the private endpoint, you should be aware of the Microsoft Azure DNS behavior
   when a private endpoint is authorized on a storage location *for the very first time*.

   When the first private endpoint is connected and authorized, Azure automatically creates a CNAME record in its public DNS.

   Under normal circumstances, this DNS update should not affect existing public connectivity to the storage account. However,
   if your environment already has private DNS zones configured, this DNS update can lead to unintended behavior.

   To avoid this issue, Microsoft recommends enabling the **Fallback to Internet** option in the private DNS zone
   configuration before authorizing the first private endpoint.
4. As the Snowflake administrator, call the
   [SYSTEM$AUTHORIZE\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_authorize_snowflake_managed_storage_volume_privatelink_access) function using the
   `privateEndpointResourceID` value as the function argument. This step authorizes access to the Snowflake-managed storage
   volume through the private endpoint.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   SELECT SYSTEM$AUTHORIZE_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PRIVATELINK_ACCESS('<privateEndpointResourceID>');
   ```

   If necessary, complete these steps to [revoke](#label-private-managed-volumes-azure-disable-endpoints) access to the
   Snowflake-managed storage volume.
5. Involve your network administrator to update the DNS settings in a private DNS zone. The settings must resolve the privatelink
   URL to the private IP addresses of the Azure private endpoint that connects to your Snowflake-managed storage volume’s storage account.

   For more information, see
   [Azure Private Endpoint DNS configuration](https://docs.microsoft.com/en-us/azure/private-link/private-endpoint-dns).

   Tip

   - Use a separate Snowflake account for testing, and configure a private DNS zone in a test VNet to test the feature so that
     the testing is isolated and doesn’t impact your other workloads.
   - If using a separate Snowflake account is not possible, use a test user to access Snowflake from a VNet where the DNS changes
     are made.
   - To test from on-premises applications, use DNS forwarding to forward requests to the Azure private DNS in the VNet where the
     DNS settings are made.

## Blocking public access

After you configure private endpoints to access the managed storage volume using Azure Private Link, you can optionally block
requests from public IP addresses to the managed storage volume. After blocking public access, all traffic must be through the
private endpoint.

Important

Confirm that traffic using private connectivity is successfully reaching the managed storage volume before blocking
public access. Blocking public access without configuring private connectivity can cause unintended disruptions.

To block all traffic from public IP addresses to the managed storage volume, call the following function:

Copy code

```
SELECT SYSTEM$BLOCK_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PUBLIC_ACCESS();
```

The function can take a few minutes to complete.

### Blocking public access with IP allowlist exceptions

The [SYSTEM$BLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS\_WITH\_EXCEPTION](/sql-reference/functions/system_block_snowflake_managed_storage_volume_public_access_with_exception) function lets you
block public access while maintaining an allowlist of IP addresses or CIDR blocks that are permitted to reach the managed storage
volume.

To block public access while allowing specific IP addresses or CIDR blocks:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SYSTEM$BLOCK_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PUBLIC_ACCESS_WITH_EXCEPTION('1.2.3.4/24, 100.0.0.1');
```

### Ensuring public access is blocked

To determine whether public IP addresses can access a Snowflake-managed storage volume, call the
[SYSTEM$SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS\_STATUS](/sql-reference/functions/system_snowflake_managed_storage_volume_public_access_status) function.

Copy code

```
SELECT SYSTEM$SNOWFLAKE_MANAGED_STORAGE_VOLUME_PUBLIC_ACCESS_STATUS();
```

### Unblocking public access

To allow public access to a Snowflake-managed storage volume that was previously blocked, call the
[SYSTEM$UNBLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS](/sql-reference/functions/system_unblock_snowflake_managed_storage_volume_public_access) function.

Copy code

```
SELECT SYSTEM$UNBLOCK_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PUBLIC_ACCESS();
```

## Revoking private endpoints to access Snowflake-managed storage volumes

To revoke access to Snowflake-managed storage volumes through Microsoft Azure private endpoints, complete the following steps:

1. As a Snowflake administrator, confirm that the
   [ENABLE\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PRIVATELINK](/sql-reference/parameters#label-enable-snowflake-managed-storage-volume-privatelink) parameter is set to `TRUE`. For example:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   SHOW PARAMETERS LIKE 'ENABLE_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PRIVATELINK' IN ACCOUNT;
   ```
2. As a Snowflake administrator, call the
   [SYSTEM$REVOKE\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_revoke_snowflake_managed_storage_volume_privatelink_access) function to revoke access to
   the private endpoint, using the same `privateEndpointResourceID` value that was used to originally authorize access.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   SELECT SYSTEM$REVOKE_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PRIVATELINK_ACCESS('<privateEndpointResourceID>');
   ```
3. As an Azure administrator, delete the private endpoint through the Azure portal.
4. As a network administrator, remove the DNS and alias records that were used to resolve the storage account URLs.
