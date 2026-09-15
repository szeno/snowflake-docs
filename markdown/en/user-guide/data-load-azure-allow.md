# Allow the VNet subnet IDs

This topic provides guidance for explicitly granting Snowflake access to
your Microsoft Azure storage account (containers, the objects in those containers, and your storage queues).
The process involves allowing the Azure Virtual Network (VNet) subnet IDs for your Snowflake account.

Allowing VNet subnet IDs is required
only if [Azure storage firewall](https://docs.microsoft.com/en-us/azure/storage/common/storage-network-security) is configured
to block all unauthorized traffic to your Azure storage account.

Note

This process must be completed by an Azure administrator in your organization.

To allow the Snowflake VNet subnet IDs:

1. Log in to your Snowflake account using [any supported client](/guides-overview-connecting).
2. Run [USE ROLE](/sql-reference/sql/use-role) to set ACCOUNTADMIN as the active role for the user session.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   ```
3. Query the [SYSTEM$GET\_SNOWFLAKE\_PLATFORM\_INFO](/sql-reference/functions/system_get_snowflake_platform_info) function to retrieve the IDs of the VNet subnet
   in which your Snowflake account is located:

   Copy code

   ```
   SELECT SYSTEM$GET_SNOWFLAKE_PLATFORM_INFO();
   ```

   Record the VNet subnet IDs that the query returns.
4. Follow the instructions in
   [Managing virtual network rules](https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security?tabs=azure-portal#managing-virtual-network-rules)
   to add a network rule for each Snowflake VNet subnet ID. You must add a network rule for each of the subnet IDs returned
   by the SYSTEM$GET\_SNOWFLAKE\_PLATFORM\_INFO function.

   Note

   Azure might return an error similar to the following:

   Copy code

   ```
   Unable retrieve endpoint status for one or more subnets. Status 'insufficient permissions' indicates lack of subnet read permissions ('Microsoft.Network/virtualNetworks/subnets/read').
   ```

   The error indicates that your Azure storage account may not initiate connections to Snowflake because those permissions are not granted. You can ignore this error. It will not block the allow feature.

For additional options for managing virtual network rules, see the [Azure documentation](https://docs.microsoft.com/en-us/azure/storage/common/storage-network-security).

For help with this configuration process or any of the other Azure configuration steps, contact the Azure administrator for your organization.

**Next:** [Configure an Azure container for loading data](/user-guide/data-load-azure-config)
