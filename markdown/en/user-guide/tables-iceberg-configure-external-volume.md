# Configure an external volume

An external volume is a named, account-level Snowflake object that you use to connect Snowflake to your
external cloud storage for Iceberg tables. An external volume stores an identity and access management (IAM) entity
for your storage location. Snowflake uses the IAM entity to securely connect to your storage for accessing
table data, Iceberg metadata, and manifest files that store the table schema, partitions, and other metadata.

A single external volume can support one or more Iceberg tables.

You must create an external volume before you can create an Apache Iceberg™ table in Snowflake.

## Create an external volume

The steps to create an external volume depend on your cloud storage provider.

For instructions, see the following topics:

- [Amazon S3](/user-guide/tables-iceberg-configure-external-volume-s3)
- [Google Cloud Storage](/user-guide/tables-iceberg-configure-external-volume-gcs)
- [Azure Storage](/user-guide/tables-iceberg-configure-external-volume-azure)
- [S3-compatible storage](/user-guide/tables-iceberg-s3-compatible)

Each external volume is associated with a particular [Active storage location](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-ext-vol-active-storage-location),
and a single external volume can support multiple Iceberg tables. However, the number of external volumes you need depends on how you want to store,
organize, and secure your table data.

You can use a single external volume if you want the data and metadata
for *all* of your Snowflake-Iceberg tables in subdirectories under the same storage location (for example, in the same S3 bucket).
To configure these directories for Snowflake-managed tables, see [Data and metadata directories](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location).

Alternatively, you can create multiple external volumes to secure various storage locations differently. For example,
you might create the following external volumes:

- A read-only external volume for externally managed Iceberg tables.
- An external volume configured with read and write access for Snowflake-managed tables.

## Verify an external volume

Verify an external volume to check that Snowflake can successfully authenticate to your storage provider using an external volume that
you’ve configured. You can verify an external volume by using SQL or Snowsight.

### Use SQL

To verify an external volume by using SQL,
call the [SYSTEM$VERIFY\_EXTERNAL\_VOLUME](/sql-reference/functions/system_verify_external_volume)
function.

Specify the name of the external volume that you want to verify.

Copy code

```
SELECT SYSTEM$VERIFY_EXTERNAL_VOLUME('my_s3_external_volume');
```

### Use Snowsight

To verify an external volume by using Snowsight, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **External data**.
3. Select the **External volumes** tab.
4. Select the external volume whose connection you want to verify.
5. Select **…** » **Verify connection**.

## Set a default external volume at the account, database, or schema level

You can either [set an existing external volume](#label-tables-iceberg-configure-external-volume-set-existing) as the default or
[set a new external volume](#label-tables-iceberg-configure-external-volume-set-new) as the default when you create it.

### Set an existing external volume as the default

To set an existing external volume as the default to use for Iceberg tables,
you can set the [EXTERNAL\_VOLUME](/sql-reference/parameters#label-external-volume) parameter at the following levels:

Account:
:   Account administrators can use the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command to set the parameter for the account.
    If the value is set for the account, all Iceberg tables created in the account read from and write to this external volume by default.

Object:
:   Users can execute the appropriate [CREATE <object>](/sql-reference/sql/create) or [ALTER <object>](/sql-reference/sql/alter) command
    to override the [EXTERNAL\_VOLUME](/sql-reference/parameters#label-external-volume) parameter value at the database or schema level.
    The lowest-scoped declaration is used: schema > database > account.

    In addition to the minimum privileges required to modify an object using the appropriate ALTER *<object\_type>* command,
    a role must have the USAGE privilege on the external volume.

Note

- Changes to the EXTERNAL\_VOLUME parameter only apply to tables created *after* the change. Existing tables continue to use the external
  volume specified when they were created.
- Alternatively, you can set a default external volume at the account, database, or schema level when you create the external volume by
  using Snowsight.

#### Example

The following statement sets an external volume (`my_s3_vol`) for a database named `my_database_1`:

Copy code

```
ALTER DATABASE my_database_1
  SET EXTERNAL_VOLUME = 'my_s3_vol';
```

After setting an external volume at the database level, you can create an Iceberg table in that database
without specifying an external volume. The following statement creates an Iceberg table in `my_database_1`
that uses Snowflake as the catalog and uses the default external volume (`my_s3_vol`) set for the database.

Copy code

```
CREATE ICEBERG TABLE iceberg_reviews_table (
  id STRING,
  product_name STRING,
  product_id STRING,
  reviewer_name STRING,
  review_date DATE,
  review STRING
)
CATALOG = 'SNOWFLAKE'
BASE_LOCATION = 'my/product_reviews/';
```

### Set a new external volume as the default

To set a new external volume as the default to use for Iceberg tables, when you create the external volume in Snowsight,
use the **Scope**
field in the configuration settings to set the external volume as the default at the account, database, or schema level.

For instructions on how to create an external volume in Snowsight, see the following sections:

- [Amazon S3](/user-guide/tables-iceberg-configure-external-volume-s3#label-configure-external-volume-snowsight)
- [Google Cloud Storage](/user-guide/tables-iceberg-configure-external-volume-gcs#label-configure-external-volume-gcs-create-snowsight)
- [Azure Storage](/user-guide/tables-iceberg-configure-external-volume-azure#label-configure-external-volume-azure-create-snowsight)
- [S3-compatible storage](/user-guide/tables-iceberg-s3-compatible#label-tables-iceberg-s3-compatible-snowsight)

## Grant USAGE privileges to an external volume by using Snowsight

The USAGE privilege grants the ability to reference the external volume and view details for the external volume. For more information,
see [External volume privileges](/user-guide/security-access-control-privileges#label-external-volume-privileges).

To grant USAGE privileges to an external volume by using Snowsight, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role that has OWNERSHIP privileges on the external volume that you want to grant USAGE privileges to.

   For instructions on switching a role, see [Switch your primary role](/user-guide/ui-snowsight-gs#label-switching-your-active-role). For more information on the OWNERSHIP privilege,
   see [External volume privileges](/user-guide/security-access-control-privileges#label-external-volume-privileges).
3. In the navigation menu, select **Catalog** » **External data**.
4. Select the **External volumes** tab.
5. Select the external volume that you want to grant USAGE privileges on.
6. Select **+ Privilege**.
7. From the **Roles** field, select the role that you want to grant the USAGE privilege for the external volume.
8. From the **Privileges** field, select **USAGE**.
9. Select **Grant privileges**.

## Add a storage location by using Snowsight

Note

To add a storage location to an external volume by using SQL, use the ADD STORAGE\_LOCATION parameter of the [ALTER EXTERNAL VOLUME](/sql-reference/sql/alter-external-volume) command.

To add a named storage location to an external volume by using Snowsight, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role that has OWNERSHIP privilege on the external volume for which you want to add a storage location.

   For instructions, see [Switch your primary role](/user-guide/ui-snowsight-gs#label-switching-your-active-role).
3. In the navigation menu, select **Catalog** » **External data**.
4. Select the **External volumes** tab.
5. Select the external volume that you want to add a storage location to.
6. Select **…** » **Add storage location**
7. Select your cloud storage provider and specify the configuration for the storage location that you’re adding:

   Amazon S3Microsoft AzureGoogle CloudS3 Compatible

   1. Select the **Amazon S3** tab.
   2. Specify the configuration for the storage location that you’re adding:

      | Field | Description |
      | --- | --- |
      | **Location name** | Enter a name for your additional storage location. |
      | **Region type** | Specifies the cloud storage provider that stores your data files.  - **Standard (default)**: S3 storage in public AWS regions outside of China. - **Government (GovCloud)**: S3 storage in AWS [government regions](/user-guide/intro-regions#label-us-gov-regions). |
      | **S3 role ARN** | Specifies the case-sensitive Amazon Resource Name (ARN) of the AWS identity and access management (IAM) role that grants privileges on the S3 bucket containing your data files.  You recorded this value when you [created an IAM role](/user-guide/tables-iceberg-configure-external-volume-s3#label-configure-external-volume-s3-create-iam-role). |
      | **Encryption (optional)** | Specifies the encryption type used. Possible values are:  - **None (default)**: No encryption. - **SSE-S3**: Server-side encryption using S3-managed encryption keys. For more information, see [Using server-side   encryption with Amazon S3-managed encryption keys (SSE-S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html). - **SSE-KMS (enter key)**: Server-side encryption using keys stored in KMS. For more information, see [Using server-side   encryption with AWS Key Management Service (SSE-KMS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html). |
      | **Connectivity** | Specifies whether to use outbound private connectivity to harden your security posture. For information about using this parameter, see [Private connectivity to external volumes for Amazon Web Services](/user-guide/tables-iceberg-configure-external-volume-s3-private). Possible values are:  - **Public (default)**: Use the public internet. - **Private (AWS PrivateLink)**: Use outbound private connectivity. |
      | **Storage base URL** | Specifies the base URL for your additional storage location. |

      Expand

      Show lessSee more

   1. Select the **Microsoft Azure** tab.
   2. Specify the configuration for the storage location that you’re adding:

      | Field | Description |
      | --- | --- |
      | **Location name** | Enter a name for your additional storage location. |
      | **Storage base URL** | Specifies the base URL for your additional storage location. |
      | **Azure tenant ID** | specify your Azure tenant ID.  To find your Azure tenant ID, see [How to find your Microsoft Entra tenant ID](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-find-tenant) in the Microsoft Entra documentation. |
      | **Use PrivateLink endpoint** | Specifies whether to use outbound private connectivity to harden your security posture. For information about using outbound private connectivity, see [Private connectivity to external volumes for Microsoft Azure](/user-guide/tables-iceberg-configure-external-volume-azure-private). |

      Expand

      Show lessSee more

   1. Select **Google Cloud** tab.
   2. Specify the configuration for the storage location that you’re adding:

   | Field | Description |
   | --- | --- |
   | **Location name** | Enter a name for your additional storage location. |
   | **Storage base URL** | Specifies the base URL for your additional storage location. |
   | **Encryption (optional)** | Specifies the encryption type used. Possible values are:  - **None (default)**: No encryption. - **SSE-KMS (enter key)**: Server-side encryption using keys stored in KMS. For more information,   see [customer-managed encryption keys](https://cloud.google.com/storage/docs/encryption/customer-managed-keys). |

   Expand

   Show lessSee more

   1. Select the **S3 Compatible** tab.
   2. Specify the configuration for the storage location that you’re adding:

      | Field | Description |
      | --- | --- |
      | **Location name** | Enter a name for your additional storage location. |
      | **Storage base URL** | Specifies the base URL for your cloud storage location. |
      | **AWS key ID** | Specifies the AWS key ID for connecting to and accessing your S3-compatible storage location. |
      | **AWS secret key** | Specifies the AWS secret key for connecting to and accessing your S3-compatible storage location. |
      | **Storage endpoint** | Specifies a fully qualified domain that points to your S3-compatible API endpoint. Note The storage endpoint should not include a bucket name; for example, specify `example.com` instead of `my_bucket.example.com`. |

      Expand

      Show lessSee more
8. Select **Add storage location**.
