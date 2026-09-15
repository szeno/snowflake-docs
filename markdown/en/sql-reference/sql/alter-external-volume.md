# ALTER EXTERNAL VOLUME

Modifies the properties for an existing [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def).

See also:
:   [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) , [DROP EXTERNAL VOLUME](/sql-reference/sql/drop-external-volume) , [SHOW EXTERNAL VOLUMES](/sql-reference/sql/show-external-volumes) , [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume)

## Syntax

Copy code

```
ALTER EXTERNAL VOLUME [ IF EXISTS ] <name> ADD STORAGE_LOCATION =
  (
    NAME = '<storage_location_name>'
    cloudProviderParams
  )

ALTER EXTERNAL VOLUME [ IF EXISTS ] <name> REMOVE STORAGE_LOCATION '<storage_location_name>'

ALTER EXTERNAL VOLUME [ IF EXISTS ] <name> UPDATE
  STORAGE_LOCATION = '<s3_compatible_storage_location_name>'
  CREDENTIALS = (
    AWS_KEY_ID = '<string>'
    AWS_SECRET_KEY = '<string>'
  )

ALTER EXTERNAL VOLUME [ IF EXISTS ] <name> SET ALLOW_WRITES = { TRUE | FALSE }

ALTER EXTERNAL VOLUME [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'
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
>   [ USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE } ]
>   STORAGE_BASE_URL = 'azure://<account>.blob.core.windows.net/<container>[/<path>/]'
> ```

## Parameters

`name`
:   Specifies the identifier for the external volume to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ADD STORAGE_LOCATION = ( NAME = 'storage_location_name' cloudProviderParams )`
:   Adds a named storage location to the external volume definition.
    To add multiple storage locations, execute an ALTER EXTERNAL VOLUME
    statement for each storage location.

    Note

    Apache Iceberg™ tables write to and read from the first storage location in the set that is located
    in the same region as your Snowflake account. To view the external volume definition and storage location regions,
    execute [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume).

`REMOVE STORAGE_LOCATION 'storage_location_name'`
:   Removes the specified storage location from the external volume definition. To remove multiple storage locations,
    execute an ALTER EXTERNAL VOLUME statement for each storage location.

    Note

    The ALTER EXTERNAL VOLUME statement fails if you attempt to remove the active storage location used by Iceberg tables in your account.

`UPDATE STORAGE_LOCATION = 's3_compatible_storage_location_name'`
:   Updates the specified S3-compatible storage location from the external volume definition.

`CREDENTIALS = ( AWS_KEY_ID = 'string' AWS_SECRET_KEY = 'string' )`
:   Specifies updated security credentials for connecting to and accessing an S3-compatible storage location.

`SET ...`
:   Specifies one or more properties/parameters to set for the external volume (separated by blank spaces, commas, or new lines):

    `ALLOW_WRITES = { TRUE | FALSE }`
    :   Specifies whether write operations are allowed for the external volume.

        - `TRUE` specifies that write operations are allowed. This parameter must be set to `TRUE` for the following tables:

          - Iceberg tables that use Snowflake as the catalog.
          - Iceberg tables that use an external catalog and are writable. Externally managed Iceberg tables are writable when you access them
            through a catalog-linked database that has the ALLOWED\_WRITE\_OPERATIONS parameter set to TRUE.
        - `FALSE` specifies that write operations aren’t allowed. You can’t change the value of this parameter to `FALSE` if
          there are Snowflake-managed Iceberg tables associated with the external volume.

    `COMMENT = 'string_literal'`
    :   String (literal) that specifies a comment for the external volume.

## Cloud provider parameters (`cloudProviderParams`)

**Amazon S3**

> `STORAGE_PROVIDER = 'S3'`
> :   Specifies the cloud storage provider that stores your data files.
>
> `STORAGE_AWS_ROLE_ARN = iam_role`
> :   Specifies the Amazon Resource Name (ARN) of the AWS identity and access management (IAM) role that grants privileges on the S3 bucket
>     containing your data files. For more information, see [Configuring secure access to Amazon S3](/user-guide/data-load-s3-config).
>
> `STORAGE_BASE_URL = 'protocol://bucket[/path/]'`
> :   Specifies the base URL for your cloud storage location, where:
>
>     - `protocol` is one of the following:
>
>       - `s3` refers to S3 storage in public AWS regions outside of China.
>       - `s3gov` refers to S3 storage in [government regions](/user-guide/intro-regions#label-us-gov-regions).
>     - `bucket` is the name of an S3 bucket that stores your data files or the [bucket-style alias](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-alias.html)
>       for an S3 bucket access point. For an S3 access point, you must also specify a value for the
>       `STORAGE_AWS_ACCESS_POINT_ARN` parameter.
>     - `path` is an optional path that can be used to provide granular control over objects in the bucket.
>
> `STORAGE_AWS_ACCESS_POINT_ARN = 'string'`
> :   Specifies the Amazon resource name (ARN) for your S3 access point. Required only when you specify an S3 access point alias
>     for your storage `STORAGE_BASE_URL`.
>
> `ENCRYPTION = ( [ TYPE = 'AWS_SSE_S3' ] | [ TYPE = 'AWS_SSE_KMS' [ KMS_KEY_ID = 'string' ] ] | [ TYPE = 'NONE' ] )`
> :   Specifies the properties needed to encrypt data on the external volume.
>
>     `TYPE = ...`
>     :   Specifies the encryption type used. Possible values are:
>
>         - `AWS_SSE_S3` : Server-side encryption using S3-managed encryption keys. For more information, see [Using server-side encryption with Amazon S3-managed encryption keys (SSE-S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html).
>         - `AWS_SSE_KMS` : Server-side encryption using keys stored in KMS. For more information, see [Using server-side encryption with AWS Key Management Service (SSE-KMS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html).
>         - `NONE`: No encryption.
>
>     `KMS_KEY_ID = 'string'` (applies to `AWS_SSE_KMS` encryption only)
>     :   Optionally specifies the ID for the AWS KMS-managed key used to encrypt files written to the bucket. If no value is provided, your default KMS key is used to encrypt files for writing data.
>
>         Note that this value is ignored when reading data.
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
> `ENCRYPTION = ( [ TYPE = 'GCS_SSE_KMS' ] [ KMS_KEY_ID = 'string' ] | [ TYPE = 'NONE' ] )`
> :   Specifies the properties needed to encrypt data on the external volume.
>
>     `TYPE = ...`
>     :   Specifies the encryption type used. Possible values are:
>
>         - `GCS_SSE_KMS`: Server-side encryption using keys stored in KMS. For more information, see [customer-managed encryption keys](https://cloud.google.com/storage/docs/encryption/customer-managed-keys).
>         - `NONE`: No encryption.
>
>     `KMS_KEY_ID = 'string'` (applies to `GCS_SSE_KMS` encryption only)
>     :   Specifies the ID for the Cloud KMS-managed key that is used to encrypt files written to the bucket.
>
>         This value is ignored when reading data. The read operation should succeed if the service account has sufficient permissions to the data and any specified KMS keys.

**Microsoft Azure**

> `STORAGE_PROVIDER = 'AZURE'`
> :   Specifies the cloud storage provider that stores your data files.
>
> `AZURE_TENANT_ID = 'tenant_id'`
> :   Specifies the ID for your Office 365 tenant that the allowed and blocked storage accounts belong to.
>     An external volume can authenticate to only one tenant,
>     so the allowed and blocked storage locations must refer to storage accounts that all belong to this tenant.
>
>     To find your tenant ID, log into the Azure portal and click **Azure Active Directory** » **Properties**. The tenant ID is
>     displayed in the **Tenant ID** field.
>
> `USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }`
> :   Specifies whether to use outbound private connectivity to harden your security posture. For information about using this parameter, see
>     [Private connectivity to external volumes for Microsoft Azure](/user-guide/tables-iceberg-configure-external-volume-azure-private).
>
> `STORAGE_BASE_URL = 'azure://account.blob.core.windows.net/container[/path/]'`
> :   Specifies the base URL for your cloud storage location, where:
>
>     - `account` is the name of your Azure account; for example, `myaccount`.
>     - `container` is the name of an Azure container that stores your data files.
>     - `path` is an optional path that can be used to provide granular control over logical directories in the container.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | External volume | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- For S3 external volumes that use an S3 access point:

  - You must configure the IAM policy for the external volume
    to grant permission to your S3 access point. For more information,
    see [Step 1: Create an IAM policy that grants access to your S3 location](/user-guide/tables-iceberg-configure-external-volume-s3#label-tables-iceberg-configure-external-volume-s3-iam-policy).
  - Multi-region access points aren’t supported.

Regarding metadata:

> Attention
>
> Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example removes the storage location named `my-us-east-1` from the `exvol1` external volume:

Copy code

```
ALTER EXTERNAL VOLUME exvol1 REMOVE STORAGE_LOCATION 'my-us-east-1';
```

The following examples add a storage location to an external volume:

**Amazon S3**

Copy code

```
ALTER EXTERNAL VOLUME exvol1
  ADD STORAGE_LOCATION =
    (
      NAME = 'my-s3-us-central-2'
      STORAGE_PROVIDER = 'S3'
      STORAGE_BASE_URL = 's3://my_bucket_us_central-1/'
      STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/myrole'
    );
```

**Google Cloud Storage**

Copy code

```
ALTER EXTERNAL VOLUME exvol2
  ADD STORAGE_LOCATION =
    (
      NAME = 'my-gcs-europe-west4'
      STORAGE_PROVIDER = 'GCS'
      STORAGE_BASE_URL = 'gcs://my_bucket_europe-west4/'
    );
```

**Microsoft Azure**

Copy code

```
ALTER EXTERNAL VOLUME exvol3
  ADD STORAGE_LOCATION =
    (
      NAME = 'my-azure-japaneast'
      STORAGE_PROVIDER = 'AZURE'
      STORAGE_BASE_URL = 'azure://sfcdev1.blob.core.windows.net/my_container_japaneast/'
      AZURE_TENANT_ID = 'a9876545-4321-987b-b23c-2kz436789d0'
    );
```

**S3-compatible storage**

Update the credentials for an S3-compatible external volume:

Copy code

```
ALTER EXTERNAL VOLUME ext_vol_s3_compat UPDATE
  STORAGE_LOCATION = 'my_s3_compat_storage_location'
  CREDENTIALS = (
    AWS_KEY_ID = '4d5e6f...'
    AWS_SECRET_KEY = '7g8h9i...'
  );
```
