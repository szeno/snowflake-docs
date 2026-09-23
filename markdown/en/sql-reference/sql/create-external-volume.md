# CREATE EXTERNAL VOLUME

Creates a new [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) for [Apache Iceberg™ tables](/user-guide/tables-iceberg)
in the account or replaces an existing external volume.

See also:
:   [ALTER EXTERNAL VOLUME](/sql-reference/sql/alter-external-volume) , [DROP EXTERNAL VOLUME](/sql-reference/sql/drop-external-volume) , [SHOW EXTERNAL VOLUMES](/sql-reference/sql/show-external-volumes), [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] EXTERNAL VOLUME [IF NOT EXISTS]
  <name>
  STORAGE_LOCATIONS =
    (
      (
        NAME = '<storage_location_name>'
        { cloudProviderParams | s3CompatibleStorageParams }
      )
      [, (...), ...]
    )
  [ ALLOW_WRITES = { TRUE | FALSE }]
  [ COMMENT = '<string_literal>' ]
```

Where:

> Copy code
>
> ```
> cloudProviderParams (for Amazon S3) ::=
>   STORAGE_PROVIDER = '{ S3 | S3GOV }'
>   STORAGE_AWS_ROLE_ARN = '<iam_role>'
>   STORAGE_BASE_URL = '<protocol>://<bucket>[/<path>/]'
>   [ STORAGE_AWS_ACCESS_POINT_ARN = '<string>' ]
>   [ STORAGE_AWS_EXTERNAL_ID = '<external_id>' ]
>   [ ENCRYPTION = ( [ TYPE = 'AWS_SSE_S3' ] |
>               [ TYPE = 'AWS_SSE_KMS' [ KMS_KEY_ID = '<string>' ] ] |
>               [ TYPE = 'NONE' ] ) ]
>   [ USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE } ]
> ```
>
> Copy code
>
> ```
> cloudProviderParams (for Google Cloud Storage) ::=
>   STORAGE_PROVIDER = 'GCS'
>   STORAGE_BASE_URL = 'gcs://<bucket>[/<path>/]'
>   [ ENCRYPTION = ( [ TYPE = 'GCS_SSE_KMS' ] [ KMS_KEY_ID = '<string>' ] |
>               [ TYPE = 'NONE' ] ) ]
> ```
>
> Copy code
>
> ```
> cloudProviderParams (for Microsoft Azure) ::=
>   STORAGE_PROVIDER = 'AZURE'
>   AZURE_TENANT_ID = '<tenant_id>'
>   STORAGE_BASE_URL = 'azure://...'
>   [ USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE } ]
> ```

> Copy code
>
> ```
> s3CompatibleStorageParams ::=
>   STORAGE_PROVIDER = 'S3COMPAT'
>   STORAGE_BASE_URL = 's3compat://<bucket>[/<path>/]'
>   CREDENTIALS = ( AWS_KEY_ID = '<string>' AWS_SECRET_KEY = '<string>' )
>   STORAGE_ENDPOINT = '<s3_api_compatible_endpoint>'
> ```

## Required parameters

`name`
:   String that specifies the identifier (the name) for the external volume; must be unique in your account.

    The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`STORAGE_LOCATIONS = ( ( NAME = 'storage_location_name' { cloudProviderParams | s3CompatibleStorageParams } ) [, (...), ...] )`
:   Set of named cloud storage locations in different regions and, optionally, cloud platforms.

    Note

    - Each external volume that you create supports a single
      [active storage location](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-ext-vol-active-storage-location).

## Optional parameters

`ALLOW_WRITES = '{ TRUE | FALSE }'`
:   Specifies whether write operations are allowed for the external volume; must be set to TRUE for the following tables:

    - Iceberg tables that use Snowflake as the catalog.
    - Iceberg tables that use an external catalog and are writable. Externally managed Iceberg tables are writable when you access them
      through a catalog-linked database that has the ALLOWED\_WRITE\_OPERATIONS parameter set to TRUE.

    For Iceberg tables created from Delta table files, setting this parameter to TRUE enables Snowflake to write Iceberg
    metadata to your external storage. For more information, see [Delta-based tables](/user-guide/tables-iceberg-metadata#label-tables-iceberg-metadata-delta).

    The value of this parameter must also match the permissions that you set on the cloud storage account for each specified storage location.
    For **Delta Direct** (Iceberg tables created from Delta table files in object storage), including read-only configuration with
    `ALLOW_WRITES = FALSE` (for example the `Storage Blob Data Reader` role on Microsoft Azure, or IAM on Amazon S3 and
    Google Cloud Storage without object write actions), see
    [Read-only vs write access for Delta Direct on each storage provider](/user-guide/tables-iceberg-metadata#label-tables-iceberg-ev-delta-read-write-options)
    in [Metadata and retention for Apache Iceberg™ tables](/user-guide/tables-iceberg-metadata). That section links to the step-by-step external volume topics for each provider.
    For the general action lists Snowflake expects by cloud provider and table type, see [Granting Snowflake access to your storage](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-grant-access-to-storage).
    For step-by-step IAM setup (for example policies and roles for Amazon S3, Google Cloud Storage, or Microsoft Azure), see
    [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

    Note

    If you plan to use the external volume for only reading externally managed Iceberg tables, you can set this parameter to FALSE and Snowflake will not write data or Iceberg metadata files to your cloud storage when you refresh tables.

    Default: TRUE

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the external volume.

    Default: No value

## Cloud provider parameters (`cloudProviderParams`)

Note

The KMS keys are managed by the storage owner in Amazon S3 or Google Cloud Storage instances. The service principals (IAM role and
GCS service account) must be granted privileges to use KMS keys.
For more information, see [Encrypting table files](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-encryption).

**Amazon S3**

> `STORAGE_PROVIDER = '{ S3 | S3GOV }'`
> :   Specifies the cloud storage provider that stores your data files.
>
>     - `'S3'`: S3 storage in public AWS regions outside of China.
>     - `'S3GOV'`: S3 storage in AWS [government regions](/user-guide/intro-regions#label-us-gov-regions).
>
> `STORAGE_AWS_ROLE_ARN = 'iam_role'`
> :   Specifies the case-sensitive Amazon Resource Name (ARN) of the AWS identity and access management (IAM) role that grants privileges on the S3 bucket
>     containing your data files. For more information, see [Configure an external volume for Amazon S3](/user-guide/tables-iceberg-configure-external-volume-s3).
>
> `STORAGE_BASE_URL = 'protocol://bucket[/path/]'`
> :   Specifies the base URL for your cloud storage location, where:
>
>     - `protocol` is one of the following:
>
>       - `s3` refers to S3 storage in public AWS regions outside of China.
>       - `s3gov` refers to S3 storage in [government regions](/user-guide/intro-regions#label-us-gov-regions).
>     - `bucket` is the name of an S3 bucket that stores your data files or the [bucket-style alias](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-alias.html)
>       for an S3 bucket access point. For an S3 access point, you must also specify a value for the `STORAGE_AWS_ACCESS_POINT_ARN` parameter.
>     - `path` is an optional path that can be used to provide granular control over objects in the bucket.
>
>     Note
>
>     Snowflake can’t support external volumes with S3 bucket names that contain dots (for example, `my.s3.bucket`).
>     S3 doesn’t support SSL for virtual-hosted-style buckets with dots in the name, and
>     Snowflake uses virtual-host-style paths and HTTPS to access data in S3.
>
>     Important
>
>     To create an Iceberg table that uses an external catalog, your Parquet data files
>     and Iceberg metadata files must be within the `STORAGE_BASE_URL` location.
>
> `STORAGE_AWS_ACCESS_POINT_ARN = 'string'`
> :   Specifies the Amazon resource name (ARN) for your S3 access point. Required only when you specify an S3 access point alias
>     for your storage `STORAGE_BASE_URL`.

> `STORAGE_AWS_EXTERNAL_ID = 'external_id'`
> :   Optionally specifies an external ID that Snowflake uses to establish a trust relationship with AWS.
>     You must specify the same external ID in the trust policy of the IAM role
>     that you configured for this external volume. For more information,
>     see
>     [How to use an external ID when granting access to your AWS resources to a third party](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).
>
>     If you don’t specify a value for this parameter, Snowflake automatically generates an external ID when you create the external volume.
>
> `ENCRYPTION = ( [ TYPE = 'AWS_SSE_S3' ] | [ TYPE = 'AWS_SSE_KMS' [ KMS_KEY_ID = 'string' ] ] | [ TYPE = 'NONE' ] )`
> :   Specifies the properties needed to encrypt data on the external volume.
>
>     `TYPE = ...`
>     :   Specifies the encryption type used. Possible values are:
>
>         - `'AWS_SSE_S3'` : Server-side encryption using S3-managed encryption keys. For more information, see [Using server-side encryption with Amazon S3-managed encryption keys (SSE-S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html).
>         - `'AWS_SSE_KMS'` : Server-side encryption using keys stored in KMS. For more information, see [Using server-side encryption with AWS Key Management Service (SSE-KMS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html).
>         - `'NONE'`: No encryption.
>
>     `KMS_KEY_ID = 'string'` (applies to `AWS_SSE_KMS` encryption only)
>     :   Optionally specifies the ID for the AWS KMS-managed key used to encrypt files written to the bucket. If no value is provided, your default KMS key is used to encrypt files for writing data.
>
>         Note that this value is ignored when reading data.
>
>         Note
>
>         To use this external volume with [Snowflake Horizon Catalog credential vending](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon),
>         set `KMS_KEY_ID` to the full key ARN, or grant the external volume’s IAM role the `kms:DescribeKey`
>         permission so that Snowflake can resolve the ARN for you. KMS key aliases aren’t supported for
>         credential vending.
>
> `USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }`
> :   Specifies whether to use outbound private connectivity to harden your security posture. For information about using this parameter, see
>     [Private connectivity to external volumes for Amazon Web Services](/user-guide/tables-iceberg-configure-external-volume-s3-private).

**Google Cloud Storage**

> `STORAGE_PROVIDER = 'GCS'`
> :   Specifies the cloud storage provider that stores your data files.
>
> `STORAGE_BASE_URL = 'gcs://bucket[/path/]'`
> :   Specifies the base URL for your cloud storage location, where:
>
>     - `bucket` is the name of a Cloud Storage bucket that stores your data files.
>     - `path` is an optional path that can be used to provide granular control over objects in the bucket.
>
>     Important
>
>     To create an Iceberg table that uses an external catalog, your Parquet data files
>     and Iceberg metadata files must be within the `STORAGE_BASE_URL` location.
>
> `ENCRYPTION = ( [ TYPE = 'GCS_SSE_KMS' ] [ KMS_KEY_ID = 'string' ] | [ TYPE = 'NONE' ] )`
> :   Specifies the properties needed to encrypt data on the external volume.
>
>     `TYPE = ...`
>     :   Specifies the encryption type used. Possible values are:
>
>         - `'GCS_SSE_KMS'`: Server-side encryption using keys stored in KMS. For more information, see [customer-managed encryption keys](https://cloud.google.com/storage/docs/encryption/customer-managed-keys).
>         - `'NONE'`: No encryption.
>
>     `KMS_KEY_ID = 'string'` (applies to `GCS_SSE_KMS` encryption only)
>     :   Specifies the ID for the Cloud KMS-managed key used to encrypt files written to the bucket.
>
>         Note that this value is ignored when reading data. The read operation should succeed if the service account has sufficient
>         permissions to the data and any specified KMS keys.

**Microsoft Azure**

> `STORAGE_PROVIDER = 'AZURE'`
> :   Specifies the cloud storage provider that stores your data files.
>
> `AZURE_TENANT_ID = 'tenant_id'`
> :   Specifies the ID for your Office 365 tenant that the storage location belongs to. An external volume can
>     authenticate to only one tenant, so the storage location must refer to a storage account
>     that belongs to this tenant.
>
>     To find your tenant ID, log into the Azure portal and select **Azure Active Directory** » **Properties**. The tenant ID is
>     displayed in the **Tenant ID** field.

> `STORAGE_BASE_URL = 'azure://...'`
> :   Specifies the base URL for your cloud storage location (case-sensitive).
>
>     - For Azure Blob Storage, specify `azure://account.blob.core.windows.net/container[/path/]`, where:
>
>       - `account` is the name of your Azure account; for example, `myaccount`.
>       - `container` is the name of an Azure container that stores your data files.
>       - `path` is an optional path that can be used to provide granular control over logical directories in the container.
>     - For Data Lake Storage, specify `azure://account.dfs.core.windows.net/container[/path/]`, where:
>
>       - `account` is the name of your Azure account; for example, `myaccount`.
>       - `container` is the name of an Azure container that stores your data files.
>       - `path` is an optional path that can be used to provide granular control over logical directories in the container.
>     - For Fabric OneLake, specify `azure://[region-]onelake.{dfs | blob}.fabric.microsoft.com/workspace/lakehouse/path/`, where:
>
>       - `region` optionally specifies the endpoint region; for example, `westus`. If specified, this must be the same region used
>         by your Microsoft Fabric capacity, and the same region in which your Snowflake account is hosted.
>       - `{dfs | blob}` specifies the endpoint type.
>       - `workspace` is either your Fabric workspace ID or workspace name; for example, `cfafbeb1-8037-4d0c-896e-a46fb27ff227` or `my_workspace`.
>         You must use the same type of identifier (ID or name) for both your workspace and Lakehouse.
>       - `lakehouse` is either your Lakehouse ID or Lakehouse name. You must use the same type of identifier (ID or name)
>         for both your workspace and Lakehouse; for example, `5b218778-e7a5-4d73-8187-f10824047715` or `my_lakehouse.Lakehouse`.
>       - `path` is a path to your storage location in the specified Lakehouse and Workspace.
>
>       [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) Preview Feature — Open
>
>       Available to all accounts
>
>     Note
>
>     Use the `azure://` prefix and not `https://`.
>
>     Important
>
>     To create an Iceberg table that uses an external catalog, your Parquet data files
>     and Iceberg metadata files must be within the `STORAGE_BASE_URL` location.
>
> `USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }`
> :   Specifies whether to use outbound private connectivity to harden your security posture. For information about using this parameter, see
>     [Private connectivity to external volumes for Microsoft Azure](/user-guide/tables-iceberg-configure-external-volume-azure-private).

## S3-compatible storage parameters (`s3CompatibleStorageParams`)

`STORAGE_PROVIDER = 'S3COMPAT'`
:   Specifies S3-compatible storage as your storage provider.

`STORAGE_BASE_URL = 's3compat://bucket[/path/]'`
:   Specifies the URL for the external location used to store data files (an existing bucket accessed using an S3-compatible API endpoint), where:

    - `bucket` is the name of the bucket.
    - `path` is an optional case-sensitive path (or *prefix* in S3 terminology) for files in the cloud storage location
      (files with names that begin with a common string).

`CREDENTIALS = ( AWS_KEY_ID = 'string' AWS_SECRET_KEY = 'string' )`
:   Specifies the security credentials for connecting to and accessing your S3-compatible storage location.

`STORAGE_ENDPOINT = 's3_api_compatible_endpoint'`
:   Specifies a fully qualified domain that points to your S3-compatible API endpoint.

    Note

    The storage endpoint should not include a bucket name; for example, specify `example.com` instead of `my_bucket.example.com`.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE EXTERNAL VOLUME | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Important

**External volumes in Amazon S3 storage only:** If you recreate an external volume (using the CREATE OR REPLACE EXTERNAL VOLUME syntax)
without specifying an external ID, you must repeat the steps to grant the AWS identity and access management (IAM) user
for your Snowflake account the access permissions required on the S3 storage location.
For more information, see the instructions for retrieving the AWS IAM user for your Snowflake
account in [Configure an external volume for Amazon S3](/user-guide/tables-iceberg-configure-external-volume-s3).

- You can’t drop or replace an external volume if one or more Iceberg tables
  are associated with the external volume.

  To view the tables that depend on an external volume,
  you can use the [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) command and
  a query using the [pipe operator](/sql-reference/operators-flow) (`->>`) that filters on
  the `external_volume_name` column.

  Note

  The column identifier (`external_volume_name`) is case-sensitive.
  Specify the column identifier exactly as it appears in the SHOW ICEBERG TABLES output.

  For example:

  Copy code

  ```
  SHOW ICEBERG TABLES
    ->> SELECT *
          FROM $1
          WHERE "external_volume_name" = 'my_external_volume_1';
  ```
- If you use a regional endpoint for a Microsoft Fabric OneLake storage location,
  use the same region as your Microsoft Fabric capacity. This must also be the same region that hosts your Snowflake account.
- For S3 external volumes that use an S3 access point:

  - You must configure the IAM policy for the external volume
    to grant permission to your S3 access point. For more information,
    see [Step 1: Create an IAM policy that grants access to your S3 location](/user-guide/tables-iceberg-configure-external-volume-s3#label-tables-iceberg-configure-external-volume-s3-iam-policy).
  - Multi-region access points aren’t supported.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

The following examples create external volumes that define writable storage locations with different cloud providers:

**Amazon S3**

The following example creates an external volume that defines an Amazon S3 storage location with encryption:

Copy code

```
CREATE OR REPLACE EXTERNAL VOLUME exvol
  STORAGE_LOCATIONS =
      (
        (
            NAME = 'my-s3-us-west-2'
            STORAGE_PROVIDER = 'S3'
            STORAGE_BASE_URL = 's3://my-example-bucket/'
            STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/myrole'
            ENCRYPTION = ( TYPE = 'AWS_SSE_KMS' KMS_KEY_ID = '1234abcd-12ab-34cd-56ef-1234567890ab' )
        )
      )
  ALLOW_WRITES = TRUE;
```

**Google Cloud Storage**

The following example creates an external volume that defines a GCS storage location with encryption:

Copy code

```
CREATE EXTERNAL VOLUME exvol
  STORAGE_LOCATIONS =
    (
      (
        NAME = 'my-us-east-1'
        STORAGE_PROVIDER = 'GCS'
        STORAGE_BASE_URL = 'gcs://mybucket1/path1/'
        ENCRYPTION=(TYPE='GCS_SSE_KMS' KMS_KEY_ID = '1234abcd-12ab-34cd-56ef-1234567890ab')
      )
    )
  ALLOW_WRITES = TRUE;
```

**Microsoft Azure**

The following example creates an external volume that defines an Azure storage location with encryption:

Copy code

```
CREATE EXTERNAL VOLUME exvol
  STORAGE_LOCATIONS =
    (
      (
        NAME = 'my-azure-northeurope'
        STORAGE_PROVIDER = 'AZURE'
        STORAGE_BASE_URL = 'azure://exampleacct.blob.core.windows.net/my_container_northeurope/'
        AZURE_TENANT_ID = 'a123b4c5-1234-123a-a12b-1a23b45678c9'
      )
    )
  ALLOW_WRITES = TRUE;
```

**S3-compatible storage**

Create an external volume that defines an S3-compatible storage location. For more information, see
[Configure an external volume for S3-compatible storage](/user-guide/tables-iceberg-s3-compatible).

Copy code

```
CREATE OR REPLACE EXTERNAL VOLUME ext_vol_s3_compat
  STORAGE_LOCATIONS = (
    (
      NAME = 'my_s3_compat_storage_location'
      STORAGE_PROVIDER = 'S3COMPAT'
      STORAGE_BASE_URL = 's3compat://mybucket/unload/mys3compatdata'
      CREDENTIALS = (
        AWS_KEY_ID = '1a2b3c...'
        AWS_SECRET_KEY = '4x5y6z...'
      )
      STORAGE_ENDPOINT = 'example.com'
    )
  );
```
