# Manage private connectivity endpoints for Snowflake Open Catalog: Azure

[Business Critical Feature](https://docs.snowflake.com/en/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Feature — Generally Available

Not available in government regions.

Follow these steps to set up outbound private connectivity for outbound network traffic where the data for your catalogs is stored in Azure
cloud storage.

## Prerequisites

- Your Open Catalog account and external cloud storage must both be hosted on Azure.
- You need permissions to set the firewall rules for your Azure storage accounts to allow requests that are routed through specific
  private connectivity endpoints.
- Your third-party query engine or Snowflake engine must have access to your Azure storage through Azure Private Link. Here are options
  for granting this access:

  - Use private endpoints for Azure Storage. For the instructions,
    see [Use private endpoints for Azure Storage](https://learn.microsoft.com/en-us/azure/storage/common/storage-private-endpoints)
    in the Azure documentation.
  - Use an Azure Service endpoint.
  - Change the firewall settings to whitelist the IP address for the machine that the query engine runs on.

  Otherwise, when you enable outbound private connectivity, the engine
  can’t read or write to tables stored in the bucket, and Open Catalog
  can’t read or write metadata to the bucket.

## Step 1: Create a Snowflake CLI connection for Open Catalog

To set up private connectivity in Open Catalog, you need a Snowflake CLI connection for Open Catalog. Follow these steps to create this
connection. If you don’t already have Snowflake CLI installed, see [Installing Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation).

### Before you begin

To create a Snowflake CLI connection for Open Catalog, you need your full Open Catalog account identifier. The account identifier includes your Snowflake
organization name and your Open Catalog account name; for example, `<orgname>.<my-snowflake-open-catalog-account-name>`.

- To find your *Snowflake* organization name (`<orgname>`), see [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).
- To find your *Snowflake Open Catalog* account name (`<my-snowflake-open-catalog-account-name>`), see
  [Find the account name for a Snowflake Open Catalog account](/user-guide/opencatalog/find-account-name).

Important

To create this connection, you must be an Open Catalog user with service admin privileges. For information about service admin privileges, see
[Service admin role](https://other-docs.snowflake.com/opencatalog/access-control.html#service-admin-role).

### Add a Snowflake CLI connection for Snowflake Open Catalog

Add a connection for the Snowflake Open Catalog account where you want to enable private connectivity.

- [Add a connection](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-snow-connection-command-add)
  with the following values. For all other parameters, press `Enter` to skip specifying a value for the parameter.

  | Connection configuration parameters | Value |
  | --- | --- |
  | **Name for this connection** | Specify a name for the connection; for example, `myopencatalogconnection`. |
  | **Account name** | Specify your Snowflake organization name, followed by your Open Catalog account name, in this format:  `<orgname>-<my-snowflake-open-catalog-account-name>`.  For example, `ABCDEFG-MYACCOUNT1`.  To find these names, see [Before you begin](#before-you-begin). |
  | **Username** | Specify your username for Open Catalog; for example, `jsmith`. |
  | **Password [optional]** | This parameter is *not* optional when you create a connection for Open Catalog.  Enter your password for Open Catalog; for example, `MyPassword123456789`. |
  | **Role for the connection [optional]** | This parameter is *not* optional when you create a connection for Open Catalog.  You must enter `POLARIS_ACCOUNT_ADMIN` |

  Expand

  Show lessSee more

### Test the Snowflake CLI connection

- To test your CLI connection, follow this example, which tests the connection for `myopencatalogconnection`:

  Copy code

  ```
  snow connection test -c myopencatalogconnection
  ```

  The response should look like this:

  Copy code

  ```
  +------------------------------------------------------------------------------+
  | key              | value                                                     |
  |----------------------------+-------------------------------------------------|
  | Connection name  | myopencatalogconnection                                   |
  | Status           | OK                                                        |
  | Host             | ABCDEFG-MYACCOUNT1.snowflakecomputing.com                 |
  | Account          | ABCDEFG-MYACCOUNT1                                        |
  | User             | jsmith                                                    |
  | Role             | POLARIS_ACCOUNT_ADMIN                                     |
  | Database         | not set                                                   |
  | Warehouse        | not set                                                   |
  +------------------------------------------------------------------------------+
  ```

### Set your Snowflake CLI connection for Snowflake Open Catalog as the default

To ensure that the connection you’re using always has the required POLARIS\_ACCOUNT\_ADMIN role granted to it, you can set the Snowflake CLI
connection you created for Open Catalog as the default connection. For more information about the default connection, see
[label-cli\_set\_default\_connection](/developer-guide/snowflake-cli/connecting/configure-connections#label-cli-set-default-connection).

1. Follow this example, which sets the `myopencatalogconnection` connection as the default:

   Copy code

   ```
   snow connection set-default myopencatalogconnection
   ```
2. To confirm that you’re using the correct user and role, run the following:

   Copy code

   ```
   snow sql -q "Select current_user(); select current_role();"
   ```

   The response should return your Open Catalog username and the CURRENT
   ROLE should be POLARIS\_ACCOUNT\_ADMIN.

   Copy code

   ```
   +----------------+
   | CURRENT_USER() |
   |----------------|
   | JSMITH        |
   +----------------+
   select current_role();
   +-----------------------+
   | CURRENT_ROLE()        |
   |-----------------------|
   | POLARIS_ACCOUNT_ADMIN |
   +-----------------------+
   ```

## Step 2: Provision a private connectivity endpoint for a storage account

You must provision a private connectivity endpoint for each storage account that you want to use with your Open Catalog account.

Note

If you’re provisioning a private connectivity endpoint for a Data Lake Storage storage account (not a blob storage account), you must provision
two private connectivity endpoints. One of these endpoints is for the DFS endpoint, and the other is for the blob endpoint. For an example, see
[Provision private connectivity endpoints for a Data Lake Storage storage account](#example-provision-private-connectivity-endpoints-for-a-data-lake-storage-storage-account).

Use your Snowflake CLI connection for Open Catalog to call the following system functions:

1. To provision a private connectivity endpoint for the storage account, call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](https://docs.snowflake.com/en/sql-reference/functions/system_provision_privatelink_endpoint) system function.
2. To confirm that the private connectivity endpoint is ready to use, call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](https://docs.snowflake.com/en/sql-reference/functions/system_get_privatelink_endpoints_info) system function.

For instructions, see [Manage private connectivity endpoints: Azure](https://docs.snowflake.com/en/user-guide/private-manage-endpoints-azure)
in the Snowflake documentation. Remember that the instructions refer to a Snowflake account instead of a Snowflake Open Catalog account,
but the process is the same in Open Catalog.

Important

- You must use the POLARIS\_ACCOUNT\_ADMIN role instead of the ACCOUNTADMIN role mentioned in the instructions.
- If the default Snowflake CLI connection that you set doesn’t have the POLARIS\_ACCOUNT\_ADMIN role granted to it, you must include the
  following statement with your command: `USE ROLE POLARIS_ACCOUNT_ADMIN;`
- With your command, you must insert a forward slash immediately before `$` to escape it. For example, `snow sql -q "SELECT SYSTEM\$GET_PRIVATELINK_CONFIG();"`.

### Example: Provision private connectivity endpoints for a Data Lake Storage storage account

If you’re using a Data Lake Storage storage account to store your Iceberg tables, you must provision two private connectivity endpoints
for the account. For more information, see
[Creating a private endpoint](https://learn.microsoft.com/en-us/azure/storage/common/storage-private-endpoints#creating-a-private-endpoint)
in the Azure documentation.

For example:

Provision a private endpoint for blob the endpoint

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
'/subscriptions/mysubscriptionid/resourceGroups/mystorage/providers/Microsoft.Storage/storageAccounts/storagedemo',
  'storagedemo.blob.core.windows.net',
  'blob'
);
```

Provision a private endpoint for the DFS endpoint

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
'/subscriptions/mysubscriptionid/resourceGroups/mystorage/providers/Microsoft.Storage/storageAccounts/storagedemo',
  'storagedemo.dfs.core.windows.net',
  'dfs'
);
```

## Step 3: Configure public network access to your storage account

In Azure, navigate to the networking settings in your storage account and configure the public network access to it. You can configure this
access as one of the following:

- Disable all public network access
- Disable all public network access except for the virtual networks and IP addresses that you specify

For more information, see [Configure Azure Storage firewalls and virtual networks](https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security?tabs=azure-portal)
in the Azure documentation.

## Step 4: Enable private connectivity for a catalog

In this step, you enable private connectivity for a catalog in your Open Catalog account. You can enable private connectivity for a new
or existing catalog:

- [Enable private connectivity for a new catalog](#enable-private-connectivity-for-a-new-catalog)
- [Enable private connectivity for an existing catalog](#enable-private-connectivity-for-an-existing-catalog)

### Enable private connectivity for a new catalog

Follow the instructions in [Create a catalog using Azure storage](create-catalog#create-a-catalog-using-azure-storage).
Ensure that, for the catalog, the **Private Link** toggle is **Enabled**.

### Enable private connectivity for an existing catalog

1. Sign in to Open Catalog.
2. In the navigation menu, select **Catalogs**.
3. In the list of catalogs, select the catalog for which you want to enable private connectivity.
4. On the Catalog Details tab, set the **PrivateLink** toggle to **Enabled**.

## Step 5: Approve a private endpoint connection to your storage account

To approve the connection, you must first either create or load a table in your catalog. Performing one of these actions generates a private
endpoint connection approval request in Azure.

1. Use your query engine to do one of the following:
   - If there aren’t any tables stored in your catalog, to create a table in your Open Catalog account , use your query engine and insert
     data into it.
   - If there is a table stored in your catalog, try to load the table.

Note

If you can’t insert data into the table, you might not have configured Azure Private Link for the query engine; if so, your query engine isn’t
connected to the catalog through Azure Private Link. To resolve this, configure Azure Private Link for the
query engine. For more information, see [Use private endpoints for Azure Storage](https://learn.microsoft.com/en-us/azure/storage/common/storage-private-endpoints)
and [Tutorial: Connect to a storage account using an Azure Private Endpoint](https://learn.microsoft.com/en-us/azure/private-link/tutorial-private-endpoint-storage-portal?tabs=dynamic-ip)
in the Azure documentation.

1. In Azure, follow these steps:
   1. Navigate to the networking settings for your storage account.
   2. Approve the connection request for the private endpoint connection. If you created a table, it is created in the Azure storage account
      when you approve the request.

## Troubleshooting

This section provides troubleshooting for issues with outbound private connectivity for network traffic.

### Can’t view the schema for a table in Open Catalog

**Symptom**

In Open Catalog, you select a table in your catalog (for example, `catalog1`) but receive the following error message: “No permissions to
access this resource.”

**Cause**

In Azure, you successfully updated the network settings for your storage account to route network traffic through your VPC endpoint. However, in
Open Catalog, you haven’t enabled private connectivity for this catalog, so Open Catalog can’t access your bucket.

**Solution**

Enable private connectivity for the catalog (for example, catalog1). For details, see
[Enable private connectivity for a catalog](#step-4-enable-private-connectivity-for-a-catalog).

### Received a “Failed to get subscoped credentials” error message in the query engine

**Symptom**

You attempt to read or write data to a table by using a query engine but receive the following error message: “Failed to get subscoped credentials.”

**Cause**

You locked down your storage account but haven’t provisioned the private connectivity endpoint or enabled private connectivity in your Open
Catalog account. As a result, Open Catalog can’t generate the subscoped credentials and return them to the query engine, so your query engine
can’t access the storage.

**Solution**

Follow these steps:

- If you haven’t provisioned the private connectivity endpoint yet, see
  [Provision a private connectivity endpoint for the storage account](#step-2-provision-a-private-connectivity-endpoint-for-a-storage-account).
- If you haven’t enabled private connectivity for the catalog yet, [Enable private connectivity for the catalog](#step-4-enable-private-connectivity-for-a-catalog).

### ‘Business Critical’ error when running the SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT command

**Symptom**

In your Snowflake CLI connection, you ran the `SYSTEM$PROVISION_PRIVATELINK_ENDPOINT` command but it fails with the following error message: “Business Critical or higher
edition is required for this operation. Please upgrade to the valid edition and then retry.”

**Cause**

The edition for your Open Catalog account isn’t Business Critical.

To enable private connectivity for outbound network traffic, which includes provisioning a private connectivity endpoint, the
[edition](https://docs.snowflake.com/en/user-guide/intro-editions) for your Snowflake Open Catalog account must be Business Critical.

**Solution**

Contact [Snowflake support](https://docs.snowflake.com/en/user-guide/contacting-support) for assistance with upgrading your Open Catalog account to Business Critical.
