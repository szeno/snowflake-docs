# Use catalog-vended credentials for Apache Iceberg™ tables

Vended credential support for Iceberg tables lets you give Snowflake access to your table data and
metadata in cloud storage without using an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def).

Instead, you configure and delegate access control with your third-party Iceberg REST catalog (such as [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview)), then create a
catalog integration in Snowflake configured for vended credentials. For any Iceberg table associated
with the catalog integration, Snowflake uses credentials vended by your catalog provider to securely connect to your external cloud storage.

Note

Using catalog-vended credentials is supported for [externally managed Iceberg tables](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration)
that use a [REST catalog integration](/sql-reference/sql/create-catalog-integration-rest).
To use this feature, your external catalog must also support credential vending.

## Considerations

Consider the following when you use catalog-vended credentials for Iceberg tables:

- This feature is supported for tables that store their data and metadata in Amazon S3, Azure Storage, or Google Cloud Storage.
- **Google Cloud Storage:** For improved query performance with tables backed by Google Cloud
  Storage, set the
  `VENDED_CREDENTIAL_STORAGE_REGION` parameter to the
  [location](https://cloud.google.com/storage/docs/locations) of your Google Cloud Storage bucket.
  You can set this at the table, schema, or database level:

  Copy code

  ```
  ALTER TABLE <table_name>
    SET VENDED_CREDENTIAL_STORAGE_REGION = '<gcs_region>';
  ```

  For multi-region buckets, use the multi-region identifier, for example, `'us'`.
  Contact Snowflake Support to enable this feature for your account.
- Table files must be stored in a single bucket; they can’t be spread across multiple buckets.

  However, you can spread your tables across multiple buckets if each table is stored in one bucket.
- The service principal configured with your REST catalog must have permission to read from *all* of the locations that contain your
  table files in your bucket. If you use AWS Lake Formation with AWS Glue, you might need to take extra steps to enable this access. For more information,
  see [(Optional) Configure Lake Formation access control](/user-guide/tables-iceberg-configure-catalog-integration-rest-glue#label-tables-iceberg-glue-rest-lf-config).
- Snowflake expects your catalog to provide one of the following tokens, based on your cloud storage provider:

  - AWS: An expiration time for the AWS session token. Snowflake searches for a key-value pair where the key is
    `s3.session-token-expires-at-ms`, and the value is a timestamp that specifies the expiration time in milliseconds.
  - Azure: An expiration time for the SAS token. Snowflake searches for a key-value pair where the key is
    `adls.sas-token-expires-at-ms`, and the value is a timestamp that specifies the expiration time in milliseconds.
  - Google Cloud Storage: An expiration time for the OAuth 2.0 access token. Snowflake searches for a key-value pair where the key is
    `gcs.oauth2.token-expires-at`, and the value is a timestamp that specifies the expiration time in milliseconds.

  If your catalog doesn’t provide a token, Snowflake expects your catalog to provide an expiration time for vended credentials, and searches for a key-value pair
  where the key is `expiration-time`,
  and the value is a timestamp that specifies the expiration time in milliseconds; for example, `1730234407000`.

  If your catalog doesn’t provide an expiration time, Snowflake assumes that the credentials expire 60 minutes after
  receipt.
- Table creation fails if your catalog provides credentials that aren’t valid.
- The CREATE ICEBERG TABLE … AS SELECT command isn’t supported.
- To use private connectivity with vended credentials, see [Configure private connectivity to storage for catalog-vended credentials](/user-guide/tables-iceberg-vended-credentials-private-connectivity).

## Required storage permissions

Your external catalog controls the permissions that it grants to Snowflake in a vended credential.
Configure your catalog to vend credentials that grant at least the following permissions on the
locations that contain your table files.

| Cloud storage | Read access | Read and write access |
| --- | --- | --- |
| Amazon S3 | `s3:GetObject` | `s3:GetObject`, `s3:PutObject` |
| Azure Storage | Shared access signature (SAS) permission `r` (read) | SAS permissions `r` (read) and `c` (create) |
| Google Cloud Storage | `storage.objects.get` | `storage.objects.get`, `storage.objects.create` |

Expand

Show lessSee more

Note the following:

- Read access is sufficient to query a table with `SELECT`. Grant write access if you also run DML
  statements such as `INSERT`, `UPDATE`, `DELETE`, or `MERGE` against the table.
- Snowflake needs these permissions on every location that contains files for the table, not only
  on the location of the current metadata file.
- Your catalog can vend broader permissions than the ones listed here. Snowflake uses only the
  permissions in this table to read and write table data.

## Create a catalog integration for vended credentials

To create a catalog integration for vended credentials, use the [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest)
command with the `ACCESS_DELEGATION_MODE` property set to `VENDED_CREDENTIALS`.

Where:

`ACCESS_DELEGATION_MODE = { VENDED_CREDENTIALS | EXTERNAL_VOLUME_CREDENTIALS }`
:   Specifies the access delegation mode to use for accessing Iceberg table files in your external cloud storage.

    - `VENDED_CREDENTIALS` specifies that Snowflake should use vended credentials.
    - `EXTERNAL_VOLUME_CREDENTIALS` specifies that Snowflake should use an external volume.

    Default: `EXTERNAL_VOLUME_CREDENTIALS`

You can specify the `ACCESS_DELEGATION_MODE` property in the list of `REST_CONFIG` properties in any
[CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest) statement.

Important

If you use AWS Lake Formation for access control, you must ensure that Snowflake can access your
AWS Glue catalog or Amazon S3 table. For more information, see
[(Optional) Configure Lake Formation access control](/user-guide/tables-iceberg-configure-catalog-integration-rest-glue#label-tables-iceberg-glue-rest-lf-config).

### Example: AWS Glue

The following example creates a catalog integration for AWS Glue that uses vended credentials. For more information,
see [Configure a catalog integration for AWS Glue Iceberg REST](/user-guide/tables-iceberg-configure-catalog-integration-rest-glue).

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
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = SIGV4
    SIGV4_IAM_ROLE = 'arn:aws:iam::123456789012:role/my-role'
    SIGV4_SIGNING_REGION = 'us-west-2'
  )
  ENABLED = TRUE;
```

### Example: Amazon S3 Tables

You can connect Snowflake to
[Amazon S3 tables](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-tables.html)
using either of two routes:

- Through the AWS Glue Iceberg REST endpoint, which integrates S3 Tables with AWS Lake Formation for unified governance.
- Directly through the Amazon S3 Tables Iceberg REST endpoint.

Both routes use catalog-vended credentials with SigV4 authentication.

#### Through AWS Glue (Lake Formation)

This example creates a catalog integration that accesses S3 Tables through the AWS Glue Iceberg REST endpoint with SigV4 credential
vending enabled using Lake Formation.

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION my_s3_tables_catalog_integration
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'my_namespace'
  REST_CONFIG = (
    CATALOG_URI = 'https://glue.us-west-2.amazonaws.com/iceberg'
    CATALOG_API_TYPE = AWS_GLUE
    CATALOG_NAME = '123456789012:S3tablescatalog/my_table_bucket'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = SIGV4
    SIGV4_IAM_ROLE = 'arn:aws:iam::123456789012:role/my_api_permissions_role'
  )
  ENABLED = TRUE;
```

Where:

> `CATALOG_URI = 'https://glue.us-west-2.amazonaws.com/iceberg'`
> :   Specifies the [AWS Glue Iceberg REST endpoint](https://docs.aws.amazon.com/glue/latest/dg/connect-glu-iceberg-rest.html).
>
> `CATALOG_NAME = 'aws_account_id:s3tablescatalog/s3_table_bucket`
> :   Specifies an S3 table bucket in your AWS account.

#### Direct access through the S3 Tables Iceberg REST endpoint

This example creates a catalog integration that connects directly to the
[Amazon S3 Tables Iceberg REST endpoint](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-integrating-open-source.html)
without going through AWS Glue. Use `CATALOG_API_TYPE = AWS_S3TABLES` and set `CATALOG_NAME` to the S3 Tables bucket ARN.

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

> `CATALOG_URI = 'https://s3tables.<region>.amazonaws.com/iceberg'`
> :   Specifies the Amazon S3 Tables Iceberg REST endpoint for your AWS Region.
>
> `CATALOG_NAME = 'arn:aws:s3tables:<region>:<aws_account_id>:bucket/<s3_table_bucket>'`
> :   Specifies the ARN of your S3 Tables bucket.

For the full setup, including IAM policy, trust policy, and optional private connectivity, see
[Configure a catalog integration for Amazon S3 Tables](/user-guide/tables-iceberg-configure-catalog-integration-rest-s3tables).

## Create an Iceberg table that uses vended credentials

After you set up access control with your third-party Iceberg REST catalog and create a catalog integration for vended credentials,
you can create an Iceberg table.

When you create an Iceberg table that uses vended credentials, you specify a catalog integration configured with
`ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS` and exclude the `EXTERNAL_VOLUME` parameter from the
[CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest) statement.

For example:

Copy code

```
CREATE ICEBERG TABLE my_iceberg_table
  CATALOG = open_catalog_int_vended_credentials
  CATALOG_TABLE_NAME = 'my_table'
  AUTO_REFRESH = TRUE;
```

Note

If you’ve set a default external volume at the account, database, or schema level, Snowflake ignores the default external volume during
table creation as long as you specify a catalog integration configured to use vended credentials.

## Google Cloud Storage requirements

When your table files are in Google Cloud Storage, Snowflake accesses your bucket using the access
token that your catalog vends. Configure your catalog with a Google Cloud service account, then
grant that service account access to the bucket that contains your table files.

### Grant object-level permissions

Snowflake reads and writes the objects in your bucket, so a vended token needs object-level
permissions only:

- `storage.objects.get` to query a table.
- `storage.objects.get` and `storage.objects.create` to also run DML statements against a table.

Grant these permissions with a
[custom role](https://cloud.google.com/iam/docs/creating-custom-roles), or with a predefined role
that includes them. For the equivalent permissions on other cloud storage providers, see
[Required storage permissions](#label-tables-iceberg-vended-credentials-permissions).

You don’t need to grant a role on the bucket resource itself, such as Storage Admin.

### Declare the bucket location

For tables backed by Google Cloud Storage, you must set the `VENDED_CREDENTIAL_STORAGE_REGION`
parameter to your bucket’s location. This can significantly reduce query latency. You can set this
parameter at the table, schema, or database level. For more information, see
[Considerations](#label-tables-iceberg-vended-credentials-considerations).
