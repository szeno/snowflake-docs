# Manage private connectivity endpoints for Snowflake Open Catalog: AWS

[Business Critical Feature](https://docs.snowflake.com/en/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Feature — Generally Available

Not available in government regions.

When the data for your catalogs in your Snowflake Open Catalog account is stored in Amazon Simple Storage Service (Amazon S3) storage buckets,
follow these steps to set up private connectivity for outbound network traffic.

To enable private connectivity for your Open Catalog *account*, you typically only need to complete the
[setup steps](#set-up-private-connectivity-for-your-account) in this topic one time. After that, you enable outbound private
connectivity for each *catalog* in your Open Catalog account.

For example, if you completed the setup steps and then later create a new `catalog1` catalog, you typically only need to enable outbound private
connectivity for `catalog1`. For instructions on how to enable private connectivity for a catalog, see
[Enable outbound private connectivity for a catalog](#enable-outbound-private-connectivity-for-a-catalog).
However, if `catalog1` uses a storage bucket for which you haven’t updated
its bucket policy, you also need to [update the bucket policy](#step-3-update-your-bucket-policy) for the bucket.
When you update a bucket policy, you restrict network access for the bucket to a private connectivity endpoint.

## Prerequisites

- Your Open Catalog account and external cloud storage must both be hosted in the same AWS region.
- You need the IAM permissions in AWS that allow you to modify the bucket policy for your AWS storage bucket where your Iceberg tables
  are stored. For details, see [Bucket policies for Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html)
  in the AWS documentation.
- Your third-party query engine or Snowflake engine must have access to your storage bucket through AWS PrivateLink or S3 Gateway
  Endpoint. For details, see [Configure an interface endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/interface-endpoints.html)
  in the AWS documentation. Otherwise, when you enable outbound private connectivity, the engine can’t read or write to tables stored in
  the bucket, but Open Catalog can read or write metadata to the bucket.

## Set up private connectivity for your account

Follow these steps to set up private connectivity for your Open Catalog account.

### Step 1: Create a Snowflake CLI connection for Open Catalog

To set up private connectivity in Open Catalog, you need a Snowflake CLI connection for Open Catalog. Follow these steps to create this
connection. If you don’t already have Snowflake CLI installed, see [Installing Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation).

#### Before you begin

To create a Snowflake CLI connection for Open Catalog, you need your full Open Catalog account identifier. The account identifier includes your Snowflake
organization name and your Open Catalog account name; for example, `<orgname>.<my-snowflake-open-catalog-account-name>`.

- To find your *Snowflake* organization name (`<orgname>`), see [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).
- To find your *Snowflake Open Catalog* account name (`<my-snowflake-open-catalog-account-name>`), see
  [Find the account name for a Snowflake Open Catalog account](/user-guide/opencatalog/find-account-name).

Important

To create this connection, you must be an Open Catalog user with service admin privileges. For information about service admin privileges, see
[Service admin role](https://other-docs.snowflake.com/opencatalog/access-control.html#service-admin-role).

#### Add a Snowflake CLI connection for Snowflake Open Catalog

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

#### Test the Snowflake CLI connection

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

#### Set your Snowflake CLI connection for Snowflake Open Catalog as the default

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

### Step 2: Provision a private connectivity endpoint

Use your Snowflake CLI connection for Open Catalog to call the following system functions:

1. To provision a private connectivity endpoint for your storage buckets, call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](https://docs.snowflake.com/en/sql-reference/functions/system_provision_privatelink_endpoint) system function.
2. To confirm that the private connectivity endpoint is ready to use, call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](https://docs.snowflake.com/en/sql-reference/functions/system_get_privatelink_endpoints_info) system function.

For instructions, see [Provision private connectivity endpoints](https://docs.snowflake.com/en/user-guide/private-manage-endpoints-aws#provision-private-connectivity-endpoints) in the Snowflake documentation. Remember that the instructions
refer to a Snowflake account instead of a Snowflake Open Catalog account, but the process is the same in Open Catalog.

Important

- You must use the POLARIS\_ACCOUNT\_ADMIN role instead of the ACCOUNTADMIN role mentioned in the instructions.
- If the default Snowflake CLI connection that you set doesn’t have the POLARIS\_ACCOUNT\_ADMIN role granted to it, you must include the
  following statement with your command: `USE ROLE POLARIS_ACCOUNT_ADMIN;`
- With your command, you must insert a forward slash immediately before `$` to escape it. For example, `snow sql -q "SELECT SYSTEM\$GET_PRIVATELINK_CONFIG();"`.

Note

You can use this private connectivity endpoint that you provision to grant access to all storage buckets located in the same AWS region
where your Open Catalog account is hosted; you can’t use it to grant access to a bucket located in a different region.

#### Example: Provision a private connectivity endpoint

The following example creates a PrivateLink with external access to Amazon S3 to configure an endpoint for the `us-west-2` region:

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  'com.amazonaws.us-west-2.s3',
  '*.s3.us-west-2.amazonaws.com'
);
```

### Step 3: Update your bucket policy

To restrict network access to your storage bucket to the private connectivity endpoint you created in the previous step, in AWS, update
the bucket policy for your storage bucket. For instructions, see [Restricting access to a specific VPCendpoint](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies-vpc-endpoint.html#example-bucket-policies-restrict-accesss-vpc-endpoint)
in the AWS documentation. For `<vpce-id>` in the bucket policy, specify the ID of the private connectivity endpoint you created in the previous
step.

If needed, repeat this step for any additional buckets you want to connect to Open Catalog.

Important

Ensure your bucket policy includes privileges that allow you to access
the bucket and bucket policy from the browser after you add it.
Otherwise, after you update your bucket policy, you won’t be able to
access the bucket or bucket policy from the browser.

This example bucket policy allows you to access the bucket and bucket policy from the browser:

Copy code

```
{
    "Version": "2012-10-17",
    "Id": "Policy1234567890123",
    "Statement": [
        {
            "Sid": "Deny public access",
            "Effect": "Deny",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
            ],
            "Resource": [
                "arn:aws:s3:::my-bucket",
                "arn:aws:s3:::my-bucket/*"
            ],
            "Condition": {
                "StringNotLike": {
                    "aws:SourceVpc": "vpc-*"
                }
            }
        },
        {
            "Sid": "Access-to-specific-VPCE-only",
            "Effect": "Deny",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
            ],
            "Resource": [
                "arn:aws:s3:::my-bucket",
                "arn:aws:s3:::my-bucket/*"
            ],
            "Condition": {
                "StringNotEquals": {
                    "aws:SourceVpce": "vpce-xxxxxxxxxxx"
                }
            }
        }
    ]
}
```

## Enable outbound private connectivity for a catalog

This section describes how to enable outbound private connectivity for a catalog in your Open Catalog account.

### Step 1: Enable private connectivity

You can enable private connectivity for a new or existing catalog:

- [Enable private connectivity for a new catalog](#enable-private-connectivity-for-a-new-catalog)
- [Enable private connectivity for an existing catalog](#enable-private-connectivity-for-an-existing-catalog)

#### Enable private connectivity for a new catalog

Follow the instructions in [Create a catalog using Amazon Simple Storage Service (Amazon S3)](create-catalog#create-a-catalog-using-amazon-simple-storage-service-amazon-s3).
Ensure that, for the catalog, the **Private Link** toggle is **Enabled**.

Note

If you haven’t updated the bucket policy for the bucket where the catalog’s tables are stored, see [Update your bucket policy](#step-3-update-your-bucket-policy). When you update a bucket policy, you restrict network access to your storage bucket to your private
connectivity endpoint.

#### Enable private connectivity for an existing catalog

1. Sign in to Open Catalog.
2. In the navigation menu, select **Catalogs**.
3. In the list of catalogs, select the catalog for which you want to enable private connectivity.
4. On the **Catalog Details** tab, set the **PrivateLink** toggle to **Enabled**.

### Step 2: Create a table by using the query engine

To verify that your query engine is connected to your catalog through AWS PrivateLink, use your query engine to create a table and insert data
into it. If you can’t insert data into the table, you might not have configured AWS PrivateLink for the query engine.

## Troubleshooting

This section provides troubleshooting for issues with outbound private connectivity for network traffic.

### Can’t view the schema for a table in Open Catalog

**Symptom**

In Open Catalog, you select a table in your catalog (for example, `catalog1`) but receive the following error message: “No permissions to
access this resource.”

**Cause**

In AWS, you successfully updated your bucket policy to route network traffic through your VPC endpoint. However, in Open Catalog, you haven’t
enabled private connectivity for this catalog, so Open Catalog can’t access your bucket.

**Solution**

Enable private connectivity for the catalog (for example, `catalog1`). For details, see
[Enable private connectivity for a catalog](#enable-outbound-private-connectivity-for-a-catalog).

### ‘Business Critical’ error when running the SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT command

**Symptom**

In your Snowflake CLI connection, you run the `SYSTEM\$PROVISION_PRIVATELINK_ENDPOINT` command, but it fails with the following error message:
“Business Critical or higher edition is required for this operation. Please upgrade to the valid edition and then retry.”

**Cause**

The edition for your Open Catalog account isn’t Business Critical.

To enable private connectivity for outbound network traffic, which includes provisioning a private connectivity endpoint, the
[edition](https://docs.snowflake.com/en/user-guide/intro-editions) for your Snowflake Open Catalog account must be Business Critical.

**Solution**

Contact [Snowflake support](https://docs.snowflake.com/en/user-guide/contacting-support) for assistance with upgrading your Open Catalog account to Business Critical.
