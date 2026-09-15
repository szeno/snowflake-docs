# Configure a catalog integration for AWS Glue Iceberg REST

Follow the steps in this topic to create a catalog integration for the
[AWS Glue Iceberg REST endpoint](https://docs.aws.amazon.com/glue/latest/dg/connect-glu-iceberg-rest.html)
with [Signature Version 4 (SigV4)](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html) authentication.

Note

To configure a catalog integration for connecting to AWS Glue Data Catalog through a private IP address instead of over the public internet,
see [Configure an Apache Iceberg™ REST catalog integration with outbound private connectivity](/user-guide/tables-iceberg-configure-catalog-integration-rest-private).

## Step 1: Configure access permissions for the AWS Glue Data Catalog

Create an IAM policy for Snowflake to access the AWS Glue Data Catalog.
Attach the policy to an IAM role, which you specify when you create a catalog integration. For instructions, see
[Creating IAM policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html) and
[Modifying a role permissions policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-modify_permissions-policy)
in the AWS Identity and Access Management User Guide.

### Read-only example policy

At a minimum, Snowflake requires the following permissions on the AWS Glue Data Catalog to access information using the Glue Iceberg REST catalog.

- `glue:GetCatalog`
- `glue:GetDatabase`
- `glue:GetDatabases`
- `glue:GetTable`
- `glue:GetTables`

The following example policy (in JSON format) provides the required permissions
to access all of the tables in a specified database.

Copy code

```
{
   "Version": "2012-10-17",
   "Statement": [
      {
         "Sid": "AllowGlueCatalogTableAccess",
         "Effect": "Allow",
         "Action": [
           "glue:GetCatalog",
           "glue:GetDatabase",
           "glue:GetDatabases",
           "glue:GetTable",
           "glue:GetTables"
         ],
         "Resource": [
            "arn:aws:glue:*:<accountid>:table/*/*",
            "arn:aws:glue:*:<accountid>:catalog",
            "arn:aws:glue:*:<accountid>:database/<database-name>"
         ]
      }
   ]
}
```

Note

- You can modify the `Resource` element of this policy to further restrict the allowed resources
  (for example, catalog, databases, or tables). For more information, see
  [Resource types defined by AWS Glue](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsglue.html#awsglue-resources-for-iam-policies).
- If you use encryption for AWS Glue, you must modify the policy to add AWS Key Management Service (AWS KMS) permissions.
  For more information, see [Setting up encryption in AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/set-up-encryption.html).

### Read and write example policy

The following example policy (in JSON format) provides the required permissions
for read and write access to all of the tables in all databases.
To configure [write access for externally managed tables](/user-guide/tables-iceberg-externally-managed-writes),
use this policy as an example.

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowGlueCatalogTableAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "glue:GetCatalog",
        "glue:GetDatabase",
        "glue:GetDatabases",
        "glue:CreateDatabase",
        "glue:DeleteDatabase",
        "glue:GetTable",
        "glue:GetTables",
        "glue:CreateTable",
        "glue:UpdateTable",
        "glue:DeleteTable"
      ],
      "Resource": [
        "arn:aws:glue:*:<accountid>:table/*/*",
        "arn:aws:glue:*:<accountid>:catalog",
        "arn:aws:glue:*:<accountid>:database/*",
        "arn:aws:s3:<external_volume_path>"
      ]
    }
  ]
}
```

Note

- The policy must provide access to your storage location in order for AWS Glue catalog to write metadata to the table location.
- The `"arn:aws:glue:*:<accountid>:database/*"` line in the `Resource` element of this policy specifies all databases. This is required
  if you want to create a new database in Glue from Snowflake with the [CREATE SCHEMA](/user-guide/tables-iceberg-externally-managed-writes#label-tables-iceberg-externally-managed-writes-create-schema)
  command. To limit access to a single database, you can specify the database by name. For more information about defining resources, see
  [Resource types defined by AWS Glue](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsglue.html#awsglue-resources-for-iam-policies).
- If you use encryption for AWS Glue, you must modify the policy to add AWS Key Management Service (AWS KMS) permissions.
  For more information, see [Setting up encryption in AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/set-up-encryption.html).

### (Optional) Configure Lake Formation access control

If you use AWS Lake Formation for fine-grained access control, ensure that your Lake Formation configuration
allows Snowflake to access your catalog objects and underlying data.

The IAM role that you created in the previous step — the role that you specify in Snowflake when you create a catalog integration — must
have the `lakeformation:GetDataAccess` IAM permission. This permission grants read and write access to underlying data:

Copy code

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "lakeformation:GetDataAccess",
            "Resource": "*"
        }
    ]
}
```

For more information, see [Underlying data access control](https://docs.aws.amazon.com/lake-formation/latest/dg/access-control-underlying-data.html)
in the Lake Formation documentation.

You must also grant data permissions to the IAM role. The method that you use to grant data permissions depends on your Lake Formation setup.
For example, you might use the named resources method to grant permissions to AWS Glue objects, or you might use tag-based access control. For more information
and instructions, see the [AWS Lake Formation documentation](https://docs.aws.amazon.com/lake-formation/latest/dg/granting-catalog-permissions.html).

## Step 2: Create a catalog integration in Snowflake

Create a catalog integration for the
[AWS Glue Iceberg REST endpoint](https://docs.aws.amazon.com/glue/latest/dg/connect-glu-iceberg-rest.html)
using the [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest) command.
Specify the IAM role that you configured. For `CATALOG_NAME`, use your AWS account ID.

Copy code

```
CREATE CATALOG INTEGRATION glue_rest_catalog_int
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'rest_catalog_integration'
  REST_CONFIG = (
    CATALOG_URI = 'https://glue.us-west-2.amazonaws.com/iceberg'
    CATALOG_API_TYPE = AWS_GLUE
    CATALOG_NAME = '123456789012'
  )
  REST_AUTHENTICATION = (
    TYPE = SIGV4
    SIGV4_IAM_ROLE = 'arn:aws:iam::123456789012:role/my-role'
    SIGV4_SIGNING_REGION = 'us-west-2'
  )
  ENABLED = TRUE;
```

Where:

- `CATALOG_URI` is the service endpoint for the AWS Glue Iceberg REST catalog.
- `CATALOG_NAME` is the ID of your AWS account.

For more information, see [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest),
which includes instructions for configuring a catalog integration for AWS Glue.

## Step 3: Retrieve the AWS IAM user and external ID for your Snowflake account

To retrieve information about the AWS IAM user and the external ID for your Snowflake account,
run the [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration) command.
You provide this information to AWS in the next step to establish a trust relationship.

Copy code

```
DESCRIBE CATALOG INTEGRATION glue_rest_catalog_int;
```

Record the following values:

> | Value | Description |
> | --- | --- |
> | `GLUE_AWS_IAM_USER_ARN` | The AWS IAM user created for your Snowflake account, for example, `arn:aws:iam::123456789001:user/abc1-b-self1234`. Snowflake provisions a single IAM user for your entire Snowflake account. All Glue catalog integrations in your account use that IAM user. |
> | `GLUE_AWS_EXTERNAL_ID` | An external ID for establishing a trust relationship. |
>
> Expand
>
> Show lessSee more

## Step 4: Grant the IAM user access to the AWS Glue Data Catalog

Update the trust policy for the same IAM role that you specified with the ARN when you created the
catalog integration (`GLUE_AWS_ROLE_ARN`). Add the values that you recorded in the
previous step to the trust policy.

For instructions, see [Modifying a trust policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-managingrole_edit-trust-policy).

The following example policy shows where to specify the `GLUE_AWS_IAM_USER_ARN` and `GLUE_AWS_EXTERNAL_ID` values:

Copy code

```
{
   "Version": "2012-10-17",
   "Statement": [
      {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
         "AWS": "<glue_iam_user_arn>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
         "StringEquals": {
            "sts:ExternalId": "<glue_aws_external_id>"
         }
      }
      }
   ]
}
```

Where:

> - `glue_iam_user_arn` is the `GLUE_IAM_USER_ARN` value that you recorded.
> - `glue_aws_external_id` is the `GLUE_AWS_EXTERNAL_ID` value that you recorded.

Note

- For security reasons, if you create a new catalog integration (or recreate an existing catalog integration by using the CREATE OR
  REPLACE CATALOG INTEGRATION syntax), the new catalog integration has a different external ID and can’t resolve the trust
  relationship unless you modify the trust policy with the new external ID.
- To verify that your permissions are configured correctly, [create an Iceberg table](/user-guide/tables-iceberg-create)
  that uses this catalog integration. Snowflake doesn’t verify that your permissions are set correctly until you create
  an Iceberg table that references this catalog integration.

## Next steps

After you configure a catalog integration for AWS Glue Iceberg REST, you can [create a catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database).
Specify the name of your catalog integration as the catalog when you create your catalog-linked database.

A catalog-linked database brings your external data from a remote Iceberg REST catalog into Snowflake by automatically discovering and
staying in sync with the namespaces and tables in your remote catalog.
