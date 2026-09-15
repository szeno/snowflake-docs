# Configure a catalog integration for AWS Glue

Important

To integrate with AWS Glue, we recommend that you instead configure a catalog integration for the AWS Glue Iceberg REST endpoint, which supports
additional Iceberg table features such as catalog-vended credentials.

For instructions, see [Configure a catalog integration for AWS Glue Iceberg REST](/user-guide/tables-iceberg-configure-catalog-integration-rest-glue).

Create a catalog integration for AWS Glue and grant Snowflake restricted access
to the AWS Glue Data Catalog.

Note

- To complete the instructions in this section, you must have permissions in Amazon Web Services (AWS)
  to create and manage IAM policies and roles.
  If you are not an AWS administrator, ask your AWS administrator to perform these tasks.
- To migrate an Iceberg table in a standard Snowflake database from an AWS Glue catalog integration to an AWS Glue Iceberg REST catalog integration,
  see [SYSTEM$SET\_CATALOG\_INTEGRATION](/sql-reference/functions/system_set_catalog_integration).

## Step 1: Configure access permissions for the AWS Glue Data Catalog

As a best practice, create a new IAM policy for Snowflake to access the AWS Glue Data Catalog.
You can then attach the policy to an IAM role and use the security credentials that AWS generates
for that role to access files in the catalog. For instructions, see
[Creating IAM policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html) and
[Modifying a role permissions policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-modify_permissions-policy)
in the AWS Identity and Access Management User Guide.

At a minimum, Snowflake requires the following permissions on the AWS Glue Data Catalog to access information about tables.

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

## Step 2: Create a catalog integration in Snowflake

Create a catalog integration for the AWS Glue Data Catalog using the [CREATE CATALOG INTEGRATION (AWS Glue)](/sql-reference/sql/create-catalog-integration-glue) command.

The following example creates a catalog integration that uses an AWS Glue Data Catalog source.
The example specifies a value for the optional `GLUE_REGION` parameter.

Copy code

```
CREATE CATALOG INTEGRATION glueCatalogInt
  CATALOG_SOURCE = GLUE
  CATALOG_NAMESPACE = 'my.catalogdb'
  TABLE_FORMAT = ICEBERG
  GLUE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/myGlueRole'
  GLUE_CATALOG_ID = '123456789012'
  GLUE_REGION = 'us-east-2'
  ENABLED = TRUE;
```

## Step 3: Retrieve the AWS IAM user and external ID for your Snowflake account

To retrieve information about the AWS IAM user and the external ID
that were created for your Snowflake account when you created the catalog integration, execute the [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration) command.
You provide this information to AWS in the next section to establish a trust relationship.

The following example command describes the catalog integration created in the previous step:

Copy code

```
DESCRIBE CATALOG INTEGRATION glueCatalogInt;
```

Record the following values:

> | Value | Description |
> | --- | --- |
> | `GLUE_AWS_IAM_USER_ARN` | The AWS IAM user created for your Snowflake account, for example, `arn:aws:iam::123456789001:user/abc1-b-self1234`. Snowflake provisions a single IAM user for your entire Snowflake account. All Glue catalog integrations in your account use that IAM user. |
> | `GLUE_AWS_EXTERNAL_ID` | The external ID that is needed to establish a trust relationship. |
>
> Expand
>
> Show lessSee more

You will provide these values in the next section.

## Step 4: Grant the IAM user permissions to access the AWS Glue Data Catalog

Update the trust policy for the same IAM role that you specified with the ARN when you created the
catalog integration (`GLUE_AWS_ROLE_ARN`). Add the values that you recorded in
[Step 3: Retrieve the AWS IAM user and external ID for your Snowflake account](#label-tables-iceberg-configure-catalog-integration-glue-retrieve-user) to the trust policy.

For instructions, see [Modifying a trust policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-managingrole_edit-trust-policy).

The following example trust policy demonstrates where to specify the `GLUE_AWS_IAM_USER_ARN` and `GLUE_AWS_EXTERNAL_ID` values:

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

- For security reasons, if you create a new catalog integration (or recreate an existing catalog integration using the CREATE OR
  REPLACE CATALOG INTEGRATION syntax), the new catalog integration has a different external ID and cannot resolve the trust
  relationship unless you modify the trust policy with the new external ID.
- To verify that your permissions are configured correctly, [create an Iceberg table](/user-guide/tables-iceberg-create)
  using this catalog integration. Snowflake doesn’t verify that your permissions are set correctly until you create
  an Iceberg table that references this catalog integration.

## Next steps

After you configure a catalog integration for AWS Glue, you can create an Iceberg table.

To update the table and keep it in sync with changes in AWS Glue, use an
[ALTER ICEBERG TABLE … REFRESH](/sql-reference/sql/alter-iceberg-table-refresh) statement. For more information, see
[Refresh the metadata for a table](/user-guide/tables-iceberg-manage#label-tables-iceberg-refresh-metadata-general).
