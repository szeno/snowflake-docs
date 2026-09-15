# Configure private connectivity to storage for catalog-vended credentials

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

When you use [catalog-vended credentials](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials)
for Apache Iceberg™ tables, Snowflake accesses your cloud storage using temporary credentials provided by the catalog.
By default, this storage traffic traverses the public internet. For increased security, you can configure private connectivity
so that Snowflake accesses your storage through a private endpoint instead.

The following diagram shows how Snowflake reads data from cloud storage using catalog-vended credentials.

![How Iceberg tables that use a catalog integration work with vended credentials. Snowflake sends metadata requests to the external catalog, receives vended credentials, and reads data files from cloud storage.](/static/images/tables-iceberg-vended-credentials.svg)

Three network paths are involved in this architecture:

- **Snowflake to catalog:** Snowflake sends metadata requests to the external catalog. You can configure this path
  to use private connectivity. See [Step 4](#label-vended-creds-pl-optional-catalog-pl).
- **Catalog to storage:** The catalog reads metadata from cloud storage. You configure this on the catalog side.
  See [Step 1](#label-vended-creds-pl-step1).
- **Snowflake to storage:** Snowflake reads data and metadata files from cloud storage using vended credentials. You enable this
  by setting `USE_PRIVATELINK_ENDPOINT = TRUE` in the `DEFAULT_STORAGE_CONFIG` parameter of your catalog integration.
  This is the primary focus of this guide.

Note

If you use an [external volume](/user-guide/tables-iceberg-configure-external-volume) instead of vended credentials,
outbound private connectivity to storage is already supported. See [Private connectivity for outbound network traffic](/user-guide/private-connectivity-outbound).

For general information about outbound private connectivity in Snowflake, including
[outbound private connectivity costs](/user-guide/private-connectivity-outbound#label-private-connect-costs), see
[Private connectivity for outbound network traffic](/user-guide/private-connectivity-outbound).

## Considerations and limitations

- Private connectivity to storage with vended credentials is supported on AWS (using AWS PrivateLink)
  and Azure (using Azure Private Link). Google Cloud Platform (GCP) isn’t supported.
- With AWS Glue Data Catalog, Snowflake can route its storage traffic over PrivateLink using vended credentials,
  but you can’t fully enforce private-only access at the S3 bucket. For details, see the warning in
  [Step 2](#label-vended-creds-pl-step2).
- On AWS, your Snowflake account and storage buckets must be in the same region.
- This feature is supported for catalog integrations with `CATALOG_SOURCE = ICEBERG_REST` or `CATALOG_SOURCE = POLARIS`.
  `POLARIS` can refer to Snowflake Open Catalog or a self-hosted Polaris catalog.

## Step 1: Set up private storage access on the catalog side

Before you block public access to your storage, ensure that your catalog server can access storage through private connectivity.
This step is your responsibility to configure on the catalog side. The specific steps depend on your catalog vendor.

Generic Iceberg REST CatalogSnowflake Open CatalogAWS Glue Data CatalogDatabricks Unity CatalogAmazon S3 Tables

If your catalog is self-hosted or provided by a vendor that complies with the Apache Iceberg REST catalog specification,
you’re responsible for configuring private connectivity from your catalog to your storage. The setup depends on
your deployment environment and cloud provider.

AWSAzure

Provision a private connectivity endpoint for S3 in your Open Catalog account and enable the PrivateLink toggle
on the catalog.

For instructions, see
[Manage private connectivity endpoints for Snowflake Open Catalog: AWS](https://docs.snowflake.com/en/user-guide/opencatalog/private-connectivity-outbound-manage-endpoints-aws).

Provision private connectivity endpoints for your Azure Storage account in your Open Catalog account. If you use
Data Lake Storage (ADLS Gen2), you must provision both a `blob` endpoint and a `dfs` endpoint. After provisioning,
enable the PrivateLink toggle on the catalog.

For instructions, see
[Manage private connectivity endpoints for Snowflake Open Catalog: Azure](https://docs.snowflake.com/en/user-guide/opencatalog/private-connectivity-outbound-manage-endpoints-azure).

AWS Glue Data Catalog uses AWS Lake Formation to vend temporary credentials, and AWS Glue accesses your S3
storage as an AWS service, not from a VPC or VPC endpoint that you control. There’s no customer-managed private
connection from Glue to storage for you to configure in this step.

This also means that you can’t block public access to your bucket in [Step 2](#label-vended-creds-pl-step2)
without breaking Glue. See the warning in that step for details.

AWSAzure

Databricks Unity Catalog supports two types of compute: **Classic** (customer-managed VPC) and **Serverless**
(Databricks-managed).

- **Classic compute:** Configure an S3 Gateway endpoint or S3 Interface endpoint in your customer-managed VPC.
  For instructions, see
  [Configure PrivateLink for a workspace with classic compute](https://docs.databricks.com/aws/en/security/network/classic/privatelink)
  in the Databricks documentation.
- **Serverless compute:** Databricks manages the network configuration. For details, see
  [Serverless compute plane networking](https://docs.databricks.com/aws/en/security/network/serverless-network-security/)
  in the Databricks documentation.

Databricks Unity Catalog supports two types of compute: **Classic** (VNet-injected workspace) and **Serverless**
(Databricks-managed).

- **Classic compute:** Configure Azure Virtual Network service endpoints (`Microsoft.Storage`) on the workspace subnet
  to establish a private connection to Azure Storage. For instructions, see
  [Configure Azure virtual network service endpoint policies for storage access from classic compute](https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/service-endpoints)
  in the Azure Databricks documentation.
- **Serverless compute:** Databricks manages the network policies. For details, see
  [Serverless compute plane networking](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/)
  in the Azure Databricks documentation.

Amazon S3 Tables is a fully managed AWS service. AWS handles the network path between
the S3 Tables service and the underlying storage, so there’s no separate catalog server
for you to configure.

Action items:

- Confirm your S3 Tables bucket is in the same AWS region as your Snowflake account.
- Confirm the IAM role used by your catalog integration has the `s3tables:*` permissions
  listed in the S3 Tables topic.

For the full configuration, including the bucket policy that blocks public access and the
provisioning of two private connectivity endpoints (`s3tables` and `s3`), see
[Configure private connectivity (optional)](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables#label-s3tables-private-connectivity)
in [Configure a catalog integration for Amazon S3 Tables](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables).

## Step 2: Block public access to your storage

After your catalog has private access to storage ([Step 1](#label-vended-creds-pl-step1)), restrict your storage so that only authorized private traffic
is allowed.

Skip this step if you use AWS Glue Data Catalog

Don’t block public access to your storage when AWS Glue is your catalog. AWS provides no way to allowlist AWS
Glue’s traffic to your bucket: even when Glue routes its traffic to S3 privately, there’s no bucket-policy
condition that can identify and permit it. Any policy that locks the bucket down to Snowflake’s PrivateLink
endpoint therefore also blocks Glue and breaks table operations.

Setting `USE_PRIVATELINK_ENDPOINT = TRUE` ([Step 8](#label-vended-creds-pl-step8)) still routes Snowflake’s
storage traffic over PrivateLink, but you can’t enforce private-only access at the bucket. If that’s a
requirement, use a catalog whose storage traffic you can allowlist, such as Snowflake Horizon Catalog, Snowflake
Open Catalog, Databricks Unity Catalog, or a generic Iceberg REST catalog that you control.

AWSAzureAmazon S3 Tables

Configure an S3 bucket policy that denies access except from approved VPC endpoints and VPCs. Use the
`StringNotEqualsIfExists` condition with both `aws:SourceVpce` and `aws:SourceVpc` keys to allowlist multiple
sources. This NOR logic ensures that a request is denied only if it doesn’t come from any of the listed VPC endpoints
or VPCs.

In the bucket policy, include:

- Your catalog’s VPC endpoint IDs or VPC IDs (see [Step 3](#label-vended-creds-pl-step3) for catalog-specific details).
- Snowflake’s VPC endpoint IDs, which you obtain later in [Step 6](#label-vended-creds-pl-allowlist-snowflake).
  You can add them to the policy later.

The following example shows a bucket policy that allowlists both VPC endpoints (`aws:SourceVpce`) and VPCs
(`aws:SourceVpc`):

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyIfNotFromApprovedVpcsOrVpces",
      "Effect": "Deny",
      "Principal": "*",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:DeleteObject",
        "s3:DeleteObjectVersion",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::<your-bucket-name>",
        "arn:aws:s3:::<your-bucket-name>/*"
      ],
      "Condition": {
        "StringNotEqualsIfExists": {
          "aws:SourceVpce": [
            "<snowflake-vpce-id>",
            "<additional-vpce-ids>"
          ],
          "aws:SourceVpc": [
            "<catalog-vpc-id-1>",
            "<catalog-vpc-id-2>"
          ]
        }
      }
    }
  ]
}
```

For more information about S3 bucket policies with VPC endpoints, see
[Private connectivity to external stages for Amazon Web Services](/user-guide/data-load-aws-private) and
[Restricting access to a specific VPC endpoint](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies-vpc-endpoint.html)
in the AWS documentation.

In the Azure portal, navigate to your storage account’s networking settings and configure public network access:

- Disable all public network access, or
- Allow access only from specific virtual networks and IP addresses that you allowlist.

In your firewall rules, include:

- Your catalog’s access (service endpoints or control plane IP addresses). See [Step 3](#label-vended-creds-pl-step3) for catalog-specific details.
- Snowflake’s private endpoint, which you provision later in [Step 5](#label-vended-creds-pl-provision-storage).

For instructions, see
[Configure Azure Storage firewalls and virtual networks](https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security)
in the Azure documentation.

Configure an S3 Tables bucket policy that denies access unless the request originates from an approved VPC endpoint
*or* is mediated by the S3 Tables service itself. Use `aws:CalledVia = s3tables.amazonaws.com` to keep the
managed service paths working, and allowlist the VPC endpoint IDs for both the `s3tables` and `s3` endpoints
that you provision in [Step 5](#label-vended-creds-pl-provision-storage).

The following example blocks public access at the bucket level. Replace `<region>`, `<account_id>`, and
`<table_bucket_name>` with your values, and add the VPC endpoint IDs in the `aws:SourceVpce` list once you have
them from [Step 6](#label-vended-creds-pl-allowlist-snowflake).

Copy code

```
{
   "Version": "2012-10-17",
   "Statement": [
      {
         "Sid": "DenyUnlessFromSpecificVPCE",
         "Effect": "Deny",
         "Principal": "*",
         "Action": "s3tables:*",
         "Resource": [
            "arn:aws:s3tables:<region>:<account_id>:bucket/<table_bucket_name>",
            "arn:aws:s3tables:<region>:<account_id>:bucket/<table_bucket_name>/*"
         ],
         "Condition": {
            "ForAllValues:StringNotEquals": {
               "aws:CalledVia": "s3tables.amazonaws.com"
            },
            "StringNotEquals": {
               "aws:SourceVpce": [
                  "<s3tables_vpce_id>",
                  "<s3_vpce_id>"
               ]
            }
         }
      }
   ]
}
```

For an optional namespace-scoped variant and the full S3 Tables policy reference, see
[Configure private connectivity (optional)](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables#label-s3tables-private-connectivity)
in [Configure a catalog integration for Amazon S3 Tables](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables).

## Step 3: Verify the catalog can still access storage

After you block public access, confirm that your catalog can still read and write data. If access is broken, update
your storage access policy to allowlist the catalog’s network identity.

Generic Iceberg REST CatalogSnowflake Open CatalogAWS Glue Data CatalogDatabricks Unity CatalogAmazon S3 Tables

Verify that your catalog can still read and write data to storage after the firewall changes.
The verification method depends on your catalog deployment.

AWSAzure

Verify that the Open Catalog PrivateLink toggle is enabled for your catalog and that the bucket policy
allowlists the Open Catalog VPC endpoint.

You can verify by selecting a table in the Open Catalog UI. If the schema displays, storage access is working.
If you get a “No permissions to access this resource” error, review the troubleshooting section in
[Manage private connectivity endpoints for Snowflake Open Catalog: AWS](https://docs.snowflake.com/en/user-guide/opencatalog/private-connectivity-outbound-manage-endpoints-aws).

Verify that the Open Catalog PrivateLink toggle is enabled for your catalog and that you approved
the private endpoint connection in the Azure portal.

You can verify by selecting a table in the Open Catalog UI. If the schema displays, storage access is working.
If you get a “Failed to get subscoped credentials” error, review the troubleshooting section in
[Manage private connectivity endpoints for Snowflake Open Catalog: Azure](https://docs.snowflake.com/en/user-guide/opencatalog/private-connectivity-outbound-manage-endpoints-azure).

Not applicable. Because you skip [Step 2](#label-vended-creds-pl-step2) when AWS Glue is your catalog (see the
warning in that step), there’s no public-access block to verify.

AWSAzure

Unity Catalog’s control plane accesses S3 through an S3 Gateway endpoint from the control plane VPC.
You must allowlist the control plane VPC IDs in your S3 bucket policy using the `aws:SourceVpc` condition key.

To find the VPC IDs for each AWS region, see
[IP addresses and domains](https://docs.databricks.com/aws/en/resources/ip-domain-region#outbound-ips-from-databricks-control-plane)
in the Databricks documentation.

Ensure your bucket policy uses `StringNotEqualsIfExists` so that both the `aws:SourceVpce`
condition (for Snowflake) and the `aws:SourceVpc` condition (for Unity Catalog) are evaluated independently.

Unity Catalog classic compute uses Azure Virtual Network service endpoints (`Microsoft.Storage`) to access
storage over the Azure backbone. For more details, see
[Configure Azure virtual network service endpoint policies for storage access from classic compute](https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/service-endpoints)
in the Azure Databricks documentation.

You must add the Databricks control plane NAT IP addresses to the Azure Storage firewall rules.
To find the control plane NAT IPs for each Azure region, see
[IP addresses and domains](https://learn.microsoft.com/en-us/azure/databricks/resources/ip-domain-region)
in the Azure Databricks documentation.

No action is required. Amazon S3 Tables is a fully managed AWS service: AWS handles the network path
between the S3 Tables service and the underlying storage, and the `aws:CalledVia` condition in the
bucket policy from [Step 2](#label-vended-creds-pl-step2) keeps the service paths working.

For background, see
[Configure private connectivity (optional)](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables#label-s3tables-private-connectivity)
in [Configure a catalog integration for Amazon S3 Tables](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables).

## Step 4: Configure private connectivity from Snowflake to the catalog server (Optional, recommended)

For full end-to-end private connectivity, configure the connection from Snowflake to the catalog’s API endpoint
over PrivateLink. This covers the metadata path from Snowflake to the catalog server.

For complete instructions, see
[Configure an Apache Iceberg™ REST catalog integration with outbound private connectivity](/user-guide/tables-iceberg-configure-catalog-integration-rest-private).

The key steps are:

1. Gather private connectivity information for your catalog (endpoint service ID, host name, and similar details).
2. Provision a private connectivity endpoint for the catalog server in Snowflake using
   [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint).
3. Verify the endpoint status using
   [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info).
4. Complete any catalog-side approval (for example, register the VPC endpoint in Databricks or approve the
   private endpoint in the Azure portal).
5. Use `CATALOG_API_TYPE = PRIVATE` when creating or altering the catalog integration.

Note

This step is independent of the storage private connectivity configuration in
[Step 5](#label-vended-creds-pl-provision-storage) through [Step 9](#label-vended-creds-pl-step9).
You can configure catalog-server private connectivity, storage private connectivity, or both.

Note

For Amazon S3 Tables, this step is **required**. Provision a private connectivity endpoint for the S3 Tables
service (`com.amazonaws.<region>.s3tables`) and create the catalog integration with
`CATALOG_API_TYPE = AWS_PRIVATE_S3TABLES`. For the complete S3 Tables flow, see
[Configure a catalog integration for Amazon S3 Tables](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables).

## Step 5: Provision a private connectivity endpoint for storage

AWSAzureAmazon S3 Tables

Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision
a private connectivity endpoint for S3:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  'com.amazonaws.<region>.s3',
  '*.<region>.s3.amazonaws.com'
);
```

Replace `<region>` with your AWS region (for example, `us-west-2`).

One endpoint covers all S3 buckets in the same region. The wildcard (`*`) doesn’t mean all S3 buckets
are accessed over a private connection. Only buckets used by catalog integrations configured with
`USE_PRIVATELINK_ENDPOINT = TRUE` in the `DEFAULT_STORAGE_CONFIG` parameter are accessed through the VPC endpoint.

Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision
a private connectivity endpoint for your Azure Storage account.

The first argument is the full Azure resource ID of the storage account, the second is the hostname, and
the third is the sub-resource type (`blob`).

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  '/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Storage/storageAccounts/<storage_account>',
  '<storage_account>.blob.core.windows.net',
  'blob'
);
```

Important

If your catalog uses Data Lake Storage (ADLS Gen2) with a DFS endpoint, you must provision **two** private
connectivity endpoints: one for the `blob` sub-resource and one for the `dfs` sub-resource.

Copy code

```
-- Blob endpoint
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  '/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Storage/storageAccounts/<storage_account>',
  '<storage_account>.blob.core.windows.net',
  'blob'
);

-- DFS endpoint
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  '/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Storage/storageAccounts/<storage_account>',
  '<storage_account>.dfs.core.windows.net',
  'dfs'
);
```

For more information, see
[Manage private connectivity endpoints for Snowflake Open Catalog: Azure](https://docs.snowflake.com/en/user-guide/opencatalog/private-connectivity-outbound-manage-endpoints-azure).

Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision
a private connectivity endpoint for S3 storage:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  'com.amazonaws.<region>.s3',
  '*.<region>.s3.amazonaws.com'
);
```

Replace `<region>` with your AWS region (for example, `us-west-2`).

One endpoint covers all S3 buckets in the same region. Only buckets used by catalog integrations configured with
`USE_PRIVATELINK_ENDPOINT = TRUE` in the `DEFAULT_STORAGE_CONFIG` parameter are accessed through the VPC endpoint.

Note

For S3 Tables, you also need a private connectivity endpoint for the S3 Tables service. Provision that endpoint
in [Step 4](#label-vended-creds-pl-optional-catalog-pl), which is required for S3 Tables.

## Step 6: Allowlist Snowflake’s access on the storage side

After you provision the endpoint, allowlist Snowflake’s private endpoint on the storage side so that
your storage accepts traffic from Snowflake.

AWSAzureAmazon S3 Tables

1. In Snowflake, call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) system function
   to get the VPC endpoint ID for Snowflake:

   Copy code

   ```
   SELECT SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO();
   ```

   Copy the value for `snowflake_endpoint_name` from the response (for example, `vpce-01c31eb5f4a1e817d`).
2. In AWS, add this VPC endpoint ID to the `aws:SourceVpce` list in the S3 bucket policy that you configured
   in [Step 2](#label-vended-creds-pl-step2).

   For more information about configuring a bucket policy for private connectivity, see
   [Private connectivity to external stages for Amazon Web Services](/user-guide/data-load-aws-private).

1. In the Azure portal, navigate to your storage account.
2. Under **Networking**, click **Private endpoint connections**.
3. Find the pending connection from Snowflake and click **Approve**.

For more information, see
[Manage private endpoint connections](https://learn.microsoft.com/en-us/azure/private-link/manage-private-endpoint?tabs=manage-private-link-powershell#private-endpoint-connections)
in the Azure documentation.

No additional action is required in this step. Snowflake’s VPC endpoint IDs are added to the `aws:SourceVpce` list in
the S3 Tables bucket policy from [Step 2](#label-vended-creds-pl-step2).

For background, see
[Configure private connectivity (optional)](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables#label-s3tables-private-connectivity)
in [Configure a catalog integration for Amazon S3 Tables](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables).

## Step 7: Verify the endpoint status

Call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) system function to verify
the endpoint status:

Copy code

```
SELECT SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO();
```

AWSAzureAmazon S3 Tables

The endpoint is ready to use when the `status` changes from `pending` to `available`.

The endpoint is ready to use when the `status` changes to `APPROVED` (after you approve
the connection in the Azure portal in [Step 6](#label-vended-creds-pl-allowlist-snowflake)).

The endpoint is ready to use when the `status` changes from `pending` to `available`.
Verify both the `s3` storage endpoint provisioned in [Step 5](#label-vended-creds-pl-provision-storage)
and the `s3tables` service endpoint provisioned in [Step 4](#label-vended-creds-pl-optional-catalog-pl).

You can continue with the next steps while waiting for the endpoint to be ready.

## Step 8: Configure the catalog integration

Configure a catalog integration with `USE_PRIVATELINK_ENDPOINT = TRUE` in the `DEFAULT_STORAGE_CONFIG`
parameter to enable private connectivity for storage access with vended credentials.

Generic Iceberg REST CatalogSnowflake Open CatalogAWS Glue Data CatalogDatabricks Unity CatalogAmazon S3 Tables

This example applies to any catalog that complies with the Apache Iceberg REST catalog specification,
whether self-hosted or provided by a catalog vendor.

**Create a new catalog integration:**

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION rest_catalog_int_vended_creds_pl
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = '<rest_api_endpoint_url>'
    CATALOG_API_TYPE = PRIVATE
    CATALOG_NAME = '<catalog_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_TOKEN_URI = '<token_server_uri>'
    OAUTH_CLIENT_ID = '<oauth_client_id>'
    OAUTH_CLIENT_SECRET = '<oauth_client_secret>'
    OAUTH_ALLOWED_SCOPES = ('all-apis', 'sql')
  )
  DEFAULT_STORAGE_CONFIG = (
    USE_PRIVATELINK_ENDPOINT = TRUE
  )
  ENABLED = TRUE;
```

Note

If you didn’t configure private connectivity to the catalog server in [Step 4](#label-vended-creds-pl-optional-catalog-pl), omit
`CATALOG_API_TYPE = PRIVATE` from the `REST_CONFIG` parameters.

**Enable private storage access for an existing catalog integration:**

Copy code

```
ALTER CATALOG INTEGRATION <name>
  SET DEFAULT_STORAGE_CONFIG = (USE_PRIVATELINK_ENDPOINT = TRUE);
```

When using Snowflake Open Catalog with both catalog and storage private connectivity, use the
private endpoint URL for `CATALOG_URI` and `OAUTH_TOKEN_URI`, and set `CATALOG_API_TYPE = PRIVATE`.

**Create a new catalog integration:**

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION open_catalog_int_vended_creds_pl
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = '<open_catalog_private_endpoint_url>'
    CATALOG_API_TYPE = PRIVATE
    CATALOG_NAME = '<catalog_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_TOKEN_URI = '<open_catalog_private_endpoint_url>/oauth/token'
    OAUTH_CLIENT_ID = '<your_client_id>'
    OAUTH_CLIENT_SECRET = '<your_client_secret>'
    OAUTH_ALLOWED_SCOPES = ('PRINCIPAL_ROLE:ALL')
  )
  DEFAULT_STORAGE_CONFIG = (
    USE_PRIVATELINK_ENDPOINT = TRUE
  )
  ENABLED = TRUE;
```

Note

If you didn’t configure private connectivity to the catalog server in [Step 4](#label-vended-creds-pl-optional-catalog-pl), use the standard
Open Catalog account URL for `CATALOG_URI` and `OAUTH_TOKEN_URI` and omit `CATALOG_API_TYPE = PRIVATE`.

**Enable private storage access for an existing catalog integration:**

Copy code

```
ALTER CATALOG INTEGRATION <name>
  SET DEFAULT_STORAGE_CONFIG = (USE_PRIVATELINK_ENDPOINT = TRUE);
```

AWS Glue uses AWS Lake Formation to vend credentials with SigV4 authentication.

Warning

Setting `USE_PRIVATELINK_ENDPOINT = TRUE` routes Snowflake’s storage traffic over PrivateLink, but you can’t fully
enforce private-only access at the bucket, because a bucket policy that blocks public access also blocks Glue. For
details, see the warning in [Step 2](#label-vended-creds-pl-step2).

**Create a new catalog integration:**

Copy code

```
CREATE CATALOG INTEGRATION glue_catalog_int_vended_creds_pl
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'rest_catalog_integration'
  REST_CONFIG = (
    CATALOG_URI = 'https://glue.<region>.amazonaws.com/iceberg'
    CATALOG_API_TYPE = AWS_GLUE
    CATALOG_NAME = '<aws_account_id>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = SIGV4
    SIGV4_IAM_ROLE = 'arn:aws:iam::<aws_account_id>:role/<my-role>'
    SIGV4_SIGNING_REGION = '<region>'
  )
  DEFAULT_STORAGE_CONFIG = (
    USE_PRIVATELINK_ENDPOINT = TRUE
  )
  ENABLED = TRUE;
```

**Enable private storage access for an existing catalog integration:**

Copy code

```
ALTER CATALOG INTEGRATION <name>
  SET DEFAULT_STORAGE_CONFIG = (USE_PRIVATELINK_ENDPOINT = TRUE);
```

For more information about configuring a Glue catalog integration, see
[Configure a catalog integration for AWS Glue Iceberg REST](/user-guide/tables-iceberg-configure-catalog-integration-rest-glue).

**Create a new catalog integration:**

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION unity_catalog_int_vended_creds_pl
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = '<databricks_workspace_url>/api/2.1/unity-catalog/iceberg-rest'
    CATALOG_API_TYPE = PRIVATE
    CATALOG_NAME = '<catalog_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_TOKEN_URI = '<databricks_workspace_url>/oidc/v1/token'
    OAUTH_CLIENT_ID = '<your_databricks_client_id>'
    OAUTH_CLIENT_SECRET = '<your_databricks_client_secret>'
    OAUTH_ALLOWED_SCOPES = ('all-apis', 'sql')
  )
  DEFAULT_STORAGE_CONFIG = (
    USE_PRIVATELINK_ENDPOINT = TRUE
  )
  ENABLED = TRUE;
```

Note

If you didn’t configure private connectivity to the catalog server in [Step 4](#label-vended-creds-pl-optional-catalog-pl), omit
`CATALOG_API_TYPE = PRIVATE` from the `REST_CONFIG` parameters. When using `CATALOG_API_TYPE = PRIVATE`,
Snowflake routes traffic to the workspace URL through the provisioned private endpoint.

**Enable private storage access for an existing catalog integration:**

Copy code

```
ALTER CATALOG INTEGRATION <name>
  SET DEFAULT_STORAGE_CONFIG = (USE_PRIVATELINK_ENDPOINT = TRUE);
```

For Amazon S3 Tables, use `CATALOG_API_TYPE = AWS_PRIVATE_S3TABLES` and set
`USE_PRIVATELINK_ENDPOINT = TRUE` in the `DEFAULT_STORAGE_CONFIG` parameter.

**Create a new catalog integration:**

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION my_s3_tables_catalog_int
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://s3tables.<region>.amazonaws.com/iceberg'
    CATALOG_API_TYPE = AWS_PRIVATE_S3TABLES
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
    CATALOG_NAME = 'arn:aws:s3tables:<region>:<account_id>:bucket/<table_bucket_name>'
  )
  REST_AUTHENTICATION = (
    TYPE = SIGV4
    SIGV4_IAM_ROLE = 'arn:aws:iam::<account_id>:role/<role_name>'
    SIGV4_SIGNING_REGION = '<region>'
  )
  DEFAULT_STORAGE_CONFIG = (
    USE_PRIVATELINK_ENDPOINT = TRUE
  )
  ENABLED = TRUE;
```

**Enable private storage access for an existing catalog integration:**

Copy code

```
ALTER CATALOG INTEGRATION <name>
  SET DEFAULT_STORAGE_CONFIG = (USE_PRIVATELINK_ENDPOINT = TRUE);
```

For the full S3 Tables flow including IAM policy, trust policy, and endpoint provisioning, see
[Configure a catalog integration for Amazon S3 Tables](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables).

## Step 9: Create Iceberg tables

After you configure the catalog integration, you can create Iceberg tables or a catalog-linked database. Snowflake
uses the vended credentials from the catalog and accesses storage through the private connectivity endpoint.

**Create an Iceberg table:**

Don’t specify an `EXTERNAL_VOLUME` parameter when you use vended credentials.

Copy code

```
CREATE ICEBERG TABLE my_iceberg_table
  CATALOG = '<catalog_integration_name>'
  CATALOG_TABLE_NAME = 'my_table'
  AUTO_REFRESH = TRUE;
```

**Create a catalog-linked database:**

You can also create a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database#label-catalog-linked-db-create) to
automatically discover and sync multiple Iceberg tables from your external catalog.

Copy code

```
CREATE DATABASE my_catalog_linked_db
  LINKED_CATALOG = (
    CATALOG = '<catalog_integration_name>'
  );
```

For more information, see [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked).

## Next steps

### Monitor your private connectivity endpoints

- To monitor your private connectivity endpoints, see [OUTBOUND\_PRIVATELINK\_ENDPOINTS view](/sql-reference/account-usage/outbound_privatelink_endpoints)
  in the ACCOUNT\_USAGE schema.
- To explore the cost of your private connectivity endpoints, see [Outbound private connectivity costs](/user-guide/private-connectivity-outbound#label-private-connect-costs).
