# AWS PrivateLink and Snowflake Open Catalog

[Business Critical Feature](https://docs.snowflake.com/en/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To ask about upgrading, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Feature — Generally Available

Not available in government regions.

This topic describes how to configure AWS PrivateLink to directly connect your Snowflake Open Catalog account to your query engine by
using inbound private connectivity.

## Prerequisites

- Your Snowflake Open Catalog account is hosted on AWS.
- You have the necessary permissions to configure your AWS DNS service with the private connectivity URL for your Open Catalog account.
  For guidance, see [How to configure the AWS DNS service (Route 53) to access Snowflake via a PrivateLink](https://community.snowflake.com/s/article/How-to-configure-the-AWS-DNS-service-Route-53-to-access-Snowflake-via-a-PrivateLink) in the Snowflake Community.

## Step 1: Enable AWS PrivateLink

In this procedure, you enable AWS PrivateLink for your Open Catalog account. This configuration allows the query engine to connect to
Open Catalog through private connectivity. You will need the 12-digit identifier for your Amazon Web Services (AWS) account and
the federated token value that contains access credentials for a federated user.

1. To obtain the federated token value, execute the following command by using the AWS CLI and copy the value into a text editor:

   Copy code

   ```
   aws sts get-federation-token --name sam
   ```
2. Sign in to Snowflake Open Catalog.
3. In the navigation menu, select **Settings**.
4. Select **Authorize**.
5. In the **Authorize Private Link** dialog, enable private connectivity for your account:

   1. In the **ID** field, enter the 12-digit identifier for your Amazon Web Services (AWS) account.
   2. For **Federated token**, enter the federated token value that you copied to a text editor.
   3. Select **Save**.

## Step 2: Verify that your account is authorized

To verify whether your Open Catalog account is authorized for private connectivity to the Snowflake Open Catalog service, follow this procedure:

1. Sign in to Snowflake Open Catalog.
2. In the navigation menu, select **Settings**.
3. Select **Get**.
4. In the Get Private Link authorization dialog, verify your account:
   1. In the **ID** field, enter the 12-digit identifier for your Amazon Web Services (AWS) account.
   2. In the **Federated token** field, enter the federated token value.
      You retrieved this value when you [enabled AWS PrivateLink](#step-1-enable-aws-privatelink).
   3. Select **Save**. A message appears, which states whether your account is authorized.

## Step 3: Retrieve your Open Catalog account settings

Retrieve these settings, which you’ll need later to create and configure a VPC endpoint and your VPC network.

1. Sign in to Snowflake Open Catalog.
2. In the navigation menu, select **Settings**.
3. On the Settings page, copy the values for the following settings into a text editor:

   - PrivateLink Account URL
   - Regionless PrivateLink Account URL
   - PrivateLink OCSP URL
   - Regionless PrivateLink OCSP URL
   - VPCE Service ID

You paste these values when you [create and configure a VPC endpoint (VPCE)](#step-4-create-and-configure-a-vpc-endpoint),
[configure your VPC network](#step-5-configure-your-vpc-network), and [connect to Open Catalog through AWS PrivateLink](#step-6-connect-to-open-catalog-through-aws-privatelink).

For descriptions of each setting, see
[Return values for the SYSTEM$GET\_PRIVATELINK\_CONFIG system function](https://docs.snowflake.com/en/sql-reference/functions/system_get_privatelink_config#returns) in the Snowflake documentation. In this topic, the names of the account settings are in JSON format.

Note

Remember that, where applicable, the description refers to a Snowflake account but your value is actually for your Snowflake Open
Catalog account. For example, the `privatelink-account-url` is the URL for your Snowflake Open Catalog account.

- Optional: To retrieve these values in JSON format, [Create a Snowflake CLI connection for Open Catalog](private-connectivity-outbound-manage-endpoints-aws#step-1-create-a-snowflake-cli-connection-for-open-catalog),
  and then call the SYSTEM$GET\_PRIVATELINK\_CONFIG system function.
- In the Snowflake documentation, `privatelink-vpce-id` corresponds to the VPCE Service ID in Open Catalog.

## Step 4: Create and configure a VPC endpoint

In this procedure, you create and configure a corresponding VPC endpoint (VPCE) in your AWS VPC environment.

Note

If you already created a VPC endpoint for your Snowflake account, and the account is in the same deployment as your Open Catalog account,
creating a new VPC endpoint for your Open Catalog account isn’t required. You can optionally skip this step.

For instructions, see
[Create and configure a VPC endpoint (VPCE)](https://docs.snowflake.com/en/user-guide/admin-security-privatelink#create-and-configure-a-vpc-endpoint-vpce)
in the Snowflake documentation, starting with step 2.

## Step 5: Configure your VPC network

To configure your VPC network, create CNAME records in your DNS service to resolve the appropriate endpoint values from your
[Open Catalog account settings for private connectivity](#step-3-retrieve-your-open-catalog-account-settings) to the DNS name of your VPC Endpoint.

For instructions, see [Configure your VPC network](https://docs.snowflake.com/en/user-guide/admin-security-privatelink#configure-your-vpc-network)
in the Snowflake documentation. Remember that these instructions are for Snowflake, so some of the features mentioned in them don’t apply
to Open Catalog. For example, `regionless-snowsight-privatelink-url` is for Snowsight, which isn’t supported in Open Catalog.

For additional help with DNS configuration, contact your internal AWS administrator.

## Step 6: Connect to Open Catalog through AWS PrivateLink

- To register a service connection and connect your query engine to Snowflake Open Catalog through AWS PrivateLink, use the code:

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

## Step 7 (Optional): Create a catalog integration for Snowflake

If you’re using Snowflake to query Open Catalog-managed tables, create a catalog for Snowflake that uses a private IP address. To create
this catalog integration, your Snowflake account must be in the same deployment as your Open Catalog account.

For an example, see [label-example\_catalog\_integration\_private\_ip\_address](/user-guide/tables-iceberg-open-catalog-query#label-example-catalog-integration-private-ip-address) in the Snowflake documentation.

Note

You can also configure private connectivity for the Snowflake Open Catalog UI. This configuration, combined with configuring private
connectivity for your Open Catalog account, allows you to access the Open Catalog UI through private connectivity instead of over the public
internet.

To configure this access, see
[Configure private connectivity for the Snowflake Open Catalog UI](private-connectivity-ui-configure.md).
