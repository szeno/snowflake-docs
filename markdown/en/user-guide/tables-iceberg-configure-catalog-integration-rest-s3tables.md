# Configure a catalog integration for Amazon S3 Tables

Follow the steps in this topic to create a catalog integration that connects directly to the
[Amazon S3 Tables Iceberg REST endpoint](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-integrating-open-source.html)
with [Signature Version 4 (SigV4)](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html) authentication
and catalog-vended credentials.

Tip

You can also access Amazon S3 Tables through the AWS Glue Iceberg REST endpoint, which provides unified table management,
centralized governance, and fine-grained access control through AWS Lake Formation. To use that approach, see
[Configure a catalog integration for AWS Glue Iceberg REST](/user-guide/tables-iceberg-configure-catalog-integration-rest-glue).

## Limitations

Be aware of the following limitations when you use Amazon S3 Tables with Snowflake:

- CREATE TABLE … AS SELECT (CTAS) isn’t supported for the Amazon S3 Tables Iceberg REST endpoint.
  For more information, see
  [Accessing tables using the Amazon S3 Tables Iceberg REST endpoint](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-integrating-open-source.html)
  in the Amazon S3 documentation.
- The only supported `ACCESS_DELEGATION_MODE` is `VENDED_CREDENTIALS`. You don’t use an
  external volume with S3 Tables.

## Step 1: Configure access permissions for Amazon S3 Tables

Create an IAM policy for Snowflake to access your S3 Tables bucket.
Attach the policy to an IAM role, which you specify when you create a catalog integration. For instructions, see
[Creating IAM policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html) and
[Modifying a role permissions policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-modify_permissions-policy)
in the AWS Identity and Access Management User Guide.

The following example policy (in JSON format) provides the required permissions
to access tables in a specified S3 Tables bucket.

Copy code

```
{
   "Version": "2012-10-17",
   "Statement": [
      {
         "Sid": "AllowS3TablesAccess",
         "Effect": "Allow",
         "Action": [
            "s3tables:GetTableBucket",
            "s3tables:ListNamespaces",
            "s3tables:GetNamespace",
            "s3tables:CreateNamespace",
            "s3tables:DeleteNamespace",
            "s3tables:ListTables",
            "s3tables:GetTable",
            "s3tables:GetTableMetadataLocation",
            "s3tables:UpdateTableMetadataLocation",
            "s3tables:GetTableData",
            "s3tables:PutTableData",
            "s3tables:CreateTable",
            "s3tables:DeleteTable",
            "s3tables:RenameTable"
         ],
         "Resource": [
            "arn:aws:s3tables:<region>:<account_id>:bucket/<table_bucket_name>",
            "arn:aws:s3tables:<region>:<account_id>:bucket/<table_bucket_name>/table/*"
         ]
      }
   ]
}
```

Note

You can modify the `Resource` element of this policy to further restrict the allowed resources.
For more information, see
[Access management for S3 Tables](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-setting-up.html)
in the Amazon S3 documentation.

## Step 2: Create a catalog integration in Snowflake

Create a catalog integration for the Amazon S3 Tables Iceberg REST endpoint
using the [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest) command.
Specify the IAM role that you configured.

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION my_s3_tables_catalog_int
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://s3tables.us-west-2.amazonaws.com/iceberg'
    CATALOG_API_TYPE = AWS_S3TABLES
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
    CATALOG_NAME = 'arn:aws:s3tables:us-west-2:123456789012:bucket/my_table_bucket'
  )
  REST_AUTHENTICATION = (
    TYPE = SIGV4
    SIGV4_IAM_ROLE = 'arn:aws:iam::123456789012:role/my-s3tables-role'
    SIGV4_SIGNING_REGION = 'us-west-2'
  )
  ENABLED = TRUE;
```

Where:

- `CATALOG_URI` is the S3 Tables Iceberg REST endpoint for your AWS region
  (for example, `https://s3tables.us-west-2.amazonaws.com/iceberg`).
- `CATALOG_API_TYPE = AWS_S3TABLES` specifies the Amazon S3 Tables catalog type.
- `ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS` is required for S3 Tables.
- `CATALOG_NAME` is the ARN of the S3 Tables bucket
  (for example, `arn:aws:s3tables:us-west-2:123456789012:bucket/my_table_bucket`).

For more information, see [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest).

## Step 3: Retrieve the AWS IAM user and external ID for your Snowflake account

To retrieve information about the AWS IAM user and the external ID for your Snowflake account,
run the [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration) command.
You provide this information to AWS in the next step to establish a trust relationship.

Copy code

```
DESCRIBE CATALOG INTEGRATION my_s3_tables_catalog_int;
```

Record the following values:

> | Value | Description |
> | --- | --- |
> | `AWS_IAM_USER_ARN` | The AWS IAM user created for your Snowflake account, for example, `arn:aws:iam::123456789001:user/abc1-b-self1234`. Snowflake provisions a single IAM user for your entire Snowflake account. All SigV4-based catalog integrations in your account use that IAM user. |
> | `AWS_EXTERNAL_ID` | An external ID for establishing a trust relationship. |
>
> Expand
>
> Show lessSee more

## Step 4: Grant the IAM user access to Amazon S3 Tables

Update the trust policy for the same IAM role that you specified with the ARN when you created the
catalog integration. Add the values that you recorded in the
previous step to the trust policy.

For instructions, see [Modifying a trust policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-managingrole_edit-trust-policy).

The following example trust policy shows where to specify the values from the DESCRIBE output:

Copy code

```
{
   "Version": "2012-10-17",
   "Statement": [
      {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
         "AWS": "<aws_iam_user_arn>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
         "StringEquals": {
            "sts:ExternalId": "<aws_external_id>"
         }
      }
      }
   ]
}
```

Where:

> - `aws_iam_user_arn` is the `AWS_IAM_USER_ARN` value that you recorded.
> - `aws_external_id` is the `AWS_EXTERNAL_ID` value that you recorded.

Note

For security reasons, if you create a new catalog integration (or recreate an existing catalog integration by using the CREATE OR
REPLACE CATALOG INTEGRATION syntax), the new catalog integration has a different external ID and can’t resolve the trust
relationship unless you modify the trust policy with the new external ID.

## Next steps

### Create a catalog-linked database

After you configure a catalog integration for Amazon S3 Tables, you can
[create a catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database).
Specify the name of your catalog integration as the catalog when you create your catalog-linked database.

Copy code

```
CREATE OR REPLACE DATABASE my_s3_tables_db
  LINKED_CATALOG = (
    CATALOG = 'my_s3_tables_catalog_int'
    ALLOWED_NAMESPACES = ('my_namespace')
  );
```

Because S3 Tables uses vended credentials, you don’t need to specify an external volume.

A catalog-linked database brings your external data from a remote Iceberg REST catalog into Snowflake by automatically discovering and
staying in sync with the namespaces and tables in your remote catalog. For more information, see
[Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).

### Configure private connectivity (optional)

For increased security, you can configure private connectivity so that Snowflake accesses Amazon S3 Tables
through private endpoints instead of the public internet. This involves two network paths:

- **Snowflake to the S3 Tables catalog endpoint:** Use `CATALOG_API_TYPE = AWS_PRIVATE_S3TABLES`
  to route catalog metadata requests through a private endpoint.
- **Snowflake to storage:** Set `USE_PRIVATELINK_ENDPOINT = TRUE` in the `DEFAULT_STORAGE_CONFIG`
  parameter so that Snowflake reads data files through a private endpoint.

For general information about outbound private connectivity in Snowflake, including
[outbound private connectivity costs](/user-guide/private-connectivity-outbound#label-private-connect-costs), see
[Private connectivity for outbound network traffic](/user-guide/private-connectivity-outbound).

1. **Provision private connectivity endpoints in Snowflake.**

   Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision
   endpoints for both the S3 Tables catalog service and S3 storage:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   -- Endpoint for the S3 Tables catalog service
   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     'com.amazonaws.<region>.s3tables',
     's3tables.<region>.amazonaws.com'
   );

   -- Endpoint for S3 storage
   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     'com.amazonaws.<region>.s3',
     '*.s3.<region>.amazonaws.com'
   );
   ```

   Replace `<region>` with your AWS region (for example, `us-west-2`).
2. **Retrieve the VPC endpoint IDs.**

   Call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) system function
   to get the VPC endpoint IDs for both endpoints:

   Copy code

   ```
   SELECT SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO();
   ```

   Record the `snowflake_endpoint_name` value for each endpoint. You need both VPC endpoint IDs
   in the next step. Wait until the `status` for each endpoint changes from `pending`
   to `available` before proceeding.
3. **Block public access in the S3 Tables bucket policy.**

   Configure a bucket policy on your S3 Tables bucket that denies access unless the request originates
   from one of the provisioned VPC endpoints. Include the VPC endpoint IDs for both the S3 Tables endpoint
   and the S3 endpoint.

   The following example blocks public access at the bucket level:

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

   To restrict access to a specific namespace instead of the entire bucket, add a `StringEquals`
   condition on `s3tables:namespace` and scope the `Resource` to the wildcard path only:

   Copy code

   ```
   {
   "Version": "2012-10-17",
   "Statement": [
      {
         "Sid": "DenyUnlessFromSpecificVPCE",
         "Effect": "Deny",
         "Principal": "*",
         "Action": [
            "s3tables:Get*",
            "s3tables:Put*",
            "s3tables:Update*",
            "s3tables:Delete*"
         ],
         "Resource": "arn:aws:s3tables:<region>:<account_id>:bucket/<table_bucket_name>/*",
         "Condition": {
            "StringEquals": {
               "s3tables:namespace": "<namespace>"
            },
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

   Where:

   - `s3tables_vpce_id` is the VPC endpoint ID for the S3 Tables catalog service.
   - `s3_vpce_id` is the VPC endpoint ID for S3 storage.

   For more examples, see
   [Resource-based policies for S3 Tables](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-resource-based-policies.html)
   and
   [IAM identity-based policies for S3 Tables](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-identity-based-policies.html)
   in the Amazon S3 documentation.
4. **Create the catalog integration with private connectivity.**

   Use `CATALOG_API_TYPE = AWS_PRIVATE_S3TABLES` and set `USE_PRIVATELINK_ENDPOINT = TRUE`
   in the `DEFAULT_STORAGE_CONFIG` parameter.

   **Create a new catalog integration with private connectivity:**

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
