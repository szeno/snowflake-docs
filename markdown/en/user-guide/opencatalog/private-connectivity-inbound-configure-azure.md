# Azure Private Link and Snowflake Open Catalog

[Business Critical Feature](https://docs.snowflake.com/en/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To ask about upgrading, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Feature — Generally Available

Not available in government regions.

This topic describes how to configure Azure Private Link to directly connect your Snowflake Open Catalog account to your query engine by
using inbound private connectivity.

## Prerequisites

- Your Snowflake Open Catalog account is hosted on Azure.
- You have the necessary permissions to configure your DNS service with the private connectivity URL for your Open Catalog account.

## Step 1: Retrieve your Open Catalog account settings

Retrieve the following settings for configuring access to Open Catalog with Azure Private Link.

1. Sign in to Snowflake Open Catalog.
2. In the navigation menu, select **Settings**.
3. On the Settings page, copy the values for the following settings into a text editor:

   - PrivateLink Account URL
   - Regionless PrivateLink Account URL
   - PrivateLink OCSP URL
   - Regionless PrivateLink OCSP URL
   - Private Link Service ID

You paste these values when you [Configure access to Open Catalog with Azure Private Link](#step-2-configure-access-to-open-catalog-with-azure-private-link) and
[Connect to Open Catalog through Azure Private Link](#step-3-connect-to-open-catalog-through-azure-private-link).

For descriptions of each setting, see
[Return values for the SYSTEM$GET\_PRIVATELINK\_CONFIG system function](https://docs.snowflake.com/en/sql-reference/functions/system_get_privatelink_config#returns) in the Snowflake documentation. In this topic, the names of the account settings are in JSON format.

Note

Remember that, where applicable, the description refers to a Snowflake account but your value is actually for your Snowflake Open
Catalog account. For example, the `privatelink-account-url` is the URL for your Snowflake Open Catalog account.

- Optional: To retrieve these values in JSON format, [Create a Snowflake CLI connection for Open Catalog](private-connectivity-outbound-manage-endpoints-aws#step-1-create-a-snowflake-cli-connection-for-open-catalog),
  and then call the SYSTEM$GET\_PRIVATELINK\_CONFIG system function.

## Step 2: Configure access to Open Catalog with Azure Private Link

Attention

This section only covers the Open Catalog–specific details for configuring your VNet environment. Also, note that Snowflake is not
responsible for the actual configuration of the required firewall updates and DNS records. If you have issues with any of these
configuration tasks, contact Microsoft Support directly.

This section describes how to connect your VNet to the Open Catalog VNet using Azure Private Link.

To complete the instructions, you need to use the Azure CLI or Azure PowerShell. For installation help, see the Microsoft documentation
for the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
or [Azure PowerShell](https://learn.microsoft.com/en-us/powershell/azure/install-azure-powershell?view=azps-13.4.0&viewFallbackFrom=azps-2.6.0).

After initiating the connection to Snowflake Open Catalog using Azure Private Link, you can determine the approval state of the connection
in the Azure portal.

### Create a private endpoint

Note

If you already created a private endpoint for your Snowflake account, and the account is in the same deployment as your Open Catalog account,
creating a new private endpoint for your Open Catalog account isn’t required. You can optionally skip this step.

1. Retrieve your Azure account details. The following example uses the Azure CLI’s `az account list` command.

   ```
   Name     CloudName   SubscriptionId                        State    IsDefault
   -------  ----------  ------------------------------------  -------  ----------
   MyCloud  AzureCloud  13c...                                Enabled  True
   ```
2. In the Azure portal, search for **Private Link**, and then select **Private Link** in the results.

   [![Conceptual diagram of Open Catalog.](/static/images/user-guide/opencatalog/img/private-connectivity-inbound-azure-privatelink-preview.png)](/static/images/user-guide/opencatalog/img/private-connectivity-inbound-azure-privatelink-preview.png)
3. Click **Private endpoints**, and then click **Add**.

   [![Conceptual diagram of Open Catalog.](/static/images/user-guide/opencatalog/img/private-connectivity-inbound-azure-privatelink-endpoint.png)](/static/images/user-guide/opencatalog/img/private-connectivity-inbound-azure-privatelink-endpoint.png)
4. On the **Basics** tab, complete the **Subscription**, **Resource group**, **Name**, and **Region** fields for your
   environment and then click **Next: Resource**.
5. On the **Resource** tab, for **Connection Method**, select **Connect to an Azure resource by resource ID or alias**.
6. For **Resource ID or alias**, enter the value for `Private Link Service ID` that you obtained when you  
   [retrieved your Open Catalog account settings for private connectivity](#step-1-retrieve-your-open-catalog-account-settings).

   If you receive an error message regarding the alias value, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support)
   for the resource ID value, and then repeat this step using that value.

When the private endpoint is approved, the **CONNECTION STATE** in the Private endpoints section on the Private Link Center page displays
the value *Pending*. This value changes to *Approved* when you complete the authorization in the next procedure.

### Enable inbound private connectivity

In this procedure, you enable Azure Private Link for your Open Catalog account. This configuration allows the query engine to connect to
Open Catalog through private connectivity. You will need your private endpoint resource ID, a subscription ID, and the federated token value
that contains access credentials for a federated user.

1. To obtain these values, execute the following commands in the Azure CLI:
   1. To obtain your private endpoint resource ID, execute the following command, and copy the value into a text editor:

      Copy code

      ```
      az network private-endpoint show
      ```
   2. To obtain the subscription ID, execute the following command, and note the value in the SubscriptionID column in the output:

      Copy code

      ```
      az account list --output table
      ```
   3. To obtain the federated token value, execute the following command, and copy the accessToken value into a text editor:

      Copy code

      ```
      az account get-access-token --subscription <SubscriptionID>
      ```

      - Where: `SubscriptionID` is the unique identifier you obtained in the previous step.

Important

The user generating the Azure access Token must have Read permissions on the Subscription. The least privilege permission is
[Microsoft.Subscription/subscriptions/acceptOwnershipStatus/read](https://docs.microsoft.com/en-us/azure/role-based-access-control/resource-provider-operations#microsoftsubscription).
Alternatively, the default role `Reader` grants more coarse-grained permissions.

The `accessToken` value is sensitive information and should be treated like a password value — do *not* share this value.

If it is necessary to contact Snowflake Support, redact the access token from any commands and URLs before creating a support ticket.

1. Sign in to Snowflake Open Catalog.
2. In the navigation menu, select **Settings**.
3. Select **Authorize**.
4. In the Authorize Private Link dialog, enable private connectivity for your account:
   1. For **ID**, enter the private endpoint resource ID that you copied to a text editor.
   2. For **Federated token**, enter the federated token value that you copied to a text editor.
   3. Select **Save**.

### Verify that your account is authorized

Follow these steps to verify whether your Open Catalog account is authorized for private connectivity to the Snowflake Open Catalog service.

1. Sign in to Snowflake Open Catalog.
2. In the navigation menu, select **Settings**.
3. Select **Get**.
4. In the Get Private Link authorization dialog, verify your account:
   1. In the **ID** field, enter your private endpoint resource ID. You retrieved this value when you
      [enabled inbound private connectivity](#enable-inbound-private-connectivity).
   2. In the **Federated token** field, enter the federated token value.
      You retrieved this value when you
      [enabled inbound private connectivity](#enable-inbound-private-connectivity).
   3. Select **Save**. A message appears, which states whether your account is authorized.

### Set up DNS

All requests to Open Catalog must be routed through the private endpoint. To resolve the Open Catalog account and OCSP URLs to the private IP address of your private endpoint, update your DNS.

1. To get the endpoint IP address, in the Azure portal search bar, enter the name of the private endpoint you created.
2. Select the Network Interface result.

   [![Conceptual diagram of Open Catalog.](/static/images/user-guide/opencatalog/img/private-connectivity-inbound-azure-privatelink-dns-endpoint.png)](/static/images/user-guide/opencatalog/img/private-connectivity-inbound-azure-privatelink-dns-endpoint.png)
3. Copy the value for the **Private IP address**.

   [![Conceptual diagram of Open Catalog.](/static/images/user-guide/opencatalog/img/private-connectivity-inbound-azure-privatelink-dns-private-ip.png)](/static/images/user-guide/opencatalog/img/private-connectivity-inbound-azure-privatelink-dns-private-ip.png)
4. Configure your DNS to have the appropriate endpoint values from your [Open Catalog account settings for private connectivity](#step-1-retrieve-your-open-catalog-account-settings)
   resolve to the private IP address.

## Step 3: Connect to Open Catalog through Azure Private Link

- To register a service connection and connect your query engine to Open Catalog through Azure Private Link, use the following code:

  Copy code

  ```
  import pyspark
  from pyspark.sql import SparkSession

  spark = SparkSession.builder.appName('iceberg_lab') \
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.1,<maven_coordinate>') \
    .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
    .config('spark.sql.defaultCatalog', 'opencatalog') \
    .config('spark.sql.catalog.opencatalog', 'org.apache.iceberg.spark.SparkCatalog') \
    .config('spark.sql.catalog.opencatalog.type', 'rest') \
    .config('spark.sql.catalog.opencatalog.uri','https://<open_catalog_privatelink_account_url>/polaris/api/catalog') \
    .config('spark.sql.catalog.opencatalog.header.X-Iceberg-Access-Delegation','vended-credentials') \
    .config('spark.sql.catalog.opencatalog.credential','<client_id>:<client_secret>') \
    .config('spark.sql.catalog.opencatalog.warehouse','<catalog_name>') \
    .config('spark.sql.catalog.opencatalog.scope','PRINCIPAL_ROLE:<principal_role_name>') \
    .getOrCreate()
  ```

### Parameters

Note

Ensure that you set up your DNS service to match the value you specify for `<open_catalog_account_identifier>`.

| Parameter | Description |
| --- | --- |
| <catalog\_name> | Specifies the name of the catalog to connect to. <br /><br />**Important**:<br /><catalog\_name> is case sensitive. |
| <maven\_coordinate> | Specifies the Maven coordinate for your external cloud storage provider:<ul><li>**S3:** software.amazon.awssdk:bundle:2.20.160</li><li>**Cloud Storage (from Google):** org.apache.iceberg:iceberg-gcp-bundle:1.5.2</li><li>**Azure:** org.apache.iceberg:iceberg-azure-bundle:1.5.2</li></ul> If you don’t see this parameter, the correct value is already specified in the code sample. |
| <client\_id> | Specifies the client ID for the service principal to use. <br /><br />Enter the **Client ID** that you copied when you configured a new service connection. |
| <client\_secret> | Specifies the client secret for the service principal to use. <br /><br />Enter the **Secret** that you copied when you configured a new service connection. |
| <open\_catalog\_privatelink\_account\_url> | Specifies the URL to connect to your Snowflake account using AWS PrivateLink or Azure Private Link. <br /><br />Enter one of the following values, which you copied when you retrieved your Open Catalog account settings:<ul><li>**PrivateLink Account URL**</li><li>**Regionless PrivateLink Account URL**</li></ul> For details on retrieving your Open Catalog account settings, see the instructions for the cloud platform where your Open Catalog account is hosted:<br /><br /><ul><li>[AWS](private-connectivity-inbound-configure-aws.md#step-3-retrieve-your-open-catalog-account-settings)</li><li>[Azure](private-connectivity-inbound-configure-azure.md#step-1-retrieve-your-open-catalog-account-settings)</li></ul> |
| <principal\_role\_name> | Specifies the principal role that is granted to the service principal.<br /><br />To view this principal role, in Open Catalog, select the **Connections** page, select your service connection, and in the **Principal Details** dialog, refer to **Principal Roles.** |

Expand

Show lessSee more

## Step 4 (Optional): Create a catalog integration for Snowflake

If you’re using Snowflake to query Open Catalog-managed tables, create a catalog for Snowflake that uses a private IP address. To create
this catalog integration, your Snowflake account must be in the same deployment as your Open Catalog account.

For an example, see [label-example\_catalog\_integration\_private\_ip\_address](/user-guide/tables-iceberg-open-catalog-query#label-example-catalog-integration-private-ip-address) in the Snowflake documentation.

Note

You can also configure private connectivity for the Snowflake Open Catalog UI. This configuration, combined with configuring private
connectivity for your Open Catalog account, allows you to access the Open Catalog UI through private connectivity instead of over the public
internet.

To configure this access, see
[Configure private connectivity for the Snowflake Open Catalog UI](private-connectivity-ui-configure.md).
