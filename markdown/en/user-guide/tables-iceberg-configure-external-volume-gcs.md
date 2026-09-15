# Configure an external volume for Google Cloud Storage

Grant Snowflake restricted access to a Google Cloud Storage (GCS) bucket
using an external volume. To configure an external volume for Google Cloud Storage, you can [use SQL](#label-configure-external-volume-gcs-create-sql) or
[use Snowsight](#label-configure-external-volume-gcs-create-snowsight).

## Prerequisites

Before you configure an external volume, you need the following:

- A Google Cloud Storage bucket.

  - To use the external volume for externally managed Iceberg tables, all of your table data and metadata files must
    be located in the bucket.
  - To support data recovery, [enable versioning for your external cloud storage location](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-enable-storage-versioning).
- Permissions in Google Cloud to create and manage IAM policies and roles. If you aren’t a Google Cloud administrator,
  ask your Google Cloud administrator to perform these tasks.

To configure an external volume, you can use SQL or Snowsight:

- [Configure an external volume by using SQL](#label-configure-external-volume-gcs-create-sql)
- [Configure an external volume in Snowsight](#label-configure-external-volume-gcs-create-snowsight)

## Configure an external volume by using SQL

### Step 1: Create an external volume in Snowflake

Create an external volume using the [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) command.

Note

Only account administrators (users with the ACCOUNTADMIN role) can execute this SQL command.

The following example creates an external volume that defines a single GCS storage location with encryption:

Copy code

```
CREATE EXTERNAL VOLUME my_gcs_external_volume
  STORAGE_LOCATIONS =
    (
      (
        NAME = 'my-us-west-2'
        STORAGE_PROVIDER = 'GCS'
        STORAGE_BASE_URL = 'gcs://mybucket1/path1/'
        ENCRYPTION=(TYPE='GCS_SSE_KMS' KMS_KEY_ID = '1234abcd-12ab-34cd-56ef-1234567890ab')
      )
    );
```

### Step 2: Retrieve the GCS service account for your Snowflake account

To retrieve the ID for the GCS service account that was created automatically
for your Snowflake account, use the [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume) command.
Specify the name of the external volume that you created previously.

For example:

> Copy code
>
> ```
> DESC EXTERNAL VOLUME my_gcs_external_volume;
> ```

Record the value of the `STORAGE_GCP_SERVICE_ACCOUNT` property in the output
(for example, `service-account-id@project1-123456.iam.gserviceaccount.com`).

Snowflake provisions a single GCS service account for your entire Snowflake account.
All GCS external volumes use that service account.

### Step 3: Grant the service account permissions to access bucket objects

In this step, you configure IAM access permissions for Snowflake in your Google Cloud console.

#### Create a custom IAM role

Create a custom role that has the permissions required to access the bucket and get objects.

1. Log in to the Google Cloud console as a project editor.
2. From the home dashboard, select **IAM & Admin** » **Roles**.
3. Select **Create Role**.
4. Enter a **Title** and optional **Description** for the custom role.
5. Select **Add Permissions**.
6. In **Filter**, select **Service** and then select **storage**.
7. Filter the list of permissions, and add the following from the list:

   - `storage.buckets.get`
   - `storage.objects.create`
   - `storage.objects.delete`
   - `storage.objects.get`
   - `storage.objects.list`
8. Select **Add**.
9. Select **Create**.

Note

For **Iceberg tables created from Delta table files**, often called **Delta Direct**, create the role with only `storage.buckets.get`, `storage.objects.get`, and `storage.objects.list` (omit `storage.objects.create` and `storage.objects.delete`). For the full comparison with write access on every storage provider, see [Read-only vs write access for Delta Direct on each storage provider](/user-guide/tables-iceberg-metadata#label-tables-iceberg-ev-delta-read-write-options).

#### Assign the custom role to the GCS service account

1. Log in to the Google Cloud console as a project editor.
2. From the home dashboard, select **Cloud Storage** » **Buckets**.
3. Filter the list of buckets, and select the bucket that you specified when you created an external volume.
4. Select **Permissions** » **View by principals**, then select **Grant access**.
5. Under **Add principals**, paste the name of the service account name from the
   output in [Step 2: Retrieve the GCS service account for your Snowflake account](#label-tables-iceberg-configure-external-volume-gcs-retrieve-service-account).
6. Under **Assign roles**, select the custom IAM role that you created previously, then select **Save**.

#### Grant the GCS service account permissions on the Google Cloud Key Management Service keys

Note

This step is required only if your GCS bucket is encrypted using a key stored in the
Google Cloud Key Management Service (Cloud KMS).

1. Log in to the Google Cloud console as a project editor.
2. From the home dashboard, search for and select **Security** » **Key Management**.
3. Select the key ring that is assigned to your GCS bucket.
4. In the upper-right corner, select **SHOW INFO PANEL**. The information panel for the key ring appears.
5. In the **Add members** field, search for the service account name from the DESCRIBE EXTERNAL VOLUME output
   in [Step 2: Retrieve the GCS service account for your Snowflake account](#label-tables-iceberg-configure-external-volume-gcs-retrieve-service-account).
6. From the **Select a role** dropdown, select the **Cloud KMS CryptoKey Encrypter/Decrypter** role.
7. Select **Add**. The service account name is added to the **Cloud KMS CryptoKey Encrypter/Decrypter**
   role drop-down in the information panel.

### Step 4: Verify storage access

To check that Snowflake can successfully authenticate to your storage provider, call the [SYSTEM$VERIFY\_EXTERNAL\_VOLUME](/sql-reference/functions/system_verify_external_volume)
function.

Copy code

```
SELECT SYSTEM$VERIFY_EXTERNAL_VOLUME('my_external_volume');
```

Note

If you receive the following error, your account administrator must activate AWS STS in the Snowflake deployment region.
For instructions, see
[Manage AWS STS in an AWS Region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html)
in the AWS documentation.

```
Error assuming AWS_ROLE:
STS is not activated in this region for account:<external volume id>. Your account administrator can activate STS in this region using the IAM Console.
```

## Configure an external volume in Snowsight

### Step 1: Retrieve the GCS service account for your Snowflake account

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Switch role**, and then select **ACCOUNTADMIN** or a role that has the CREATE EXTERNAL VOLUME privilege.

   For more information, see [Switch your primary role](/user-guide/ui-snowsight-gs#label-switching-your-active-role).
3. In the navigation menu, select **Catalog** » **External data**.
4. Select the **External volumes** tab.
5. Select **+ Create**.
6. Select **Google Cloud Storage** and then select **Next**.
7. From the **Grant storage access** page, copy the value of the **GCS service account** into a text editor.

   Snowflake provisions a single GCS service account for your entire Snowflake account. All GCS external volumes use that service account.

### Step 2: Grant the service account permissions to access bucket objects

In this step, you configure IAM access permissions for Snowflake in your Google Cloud console.

#### Create a custom IAM role

Create a custom role that has the permissions required to access the bucket and get objects.

1. Log in to the Google Cloud console as a project editor.
2. From the home dashboard, select **IAM & Admin** » **Roles**.
3. Select **Create Role**.
4. Enter a **Title** and optional **Description** for the custom role.
5. Select **Add Permissions**.
6. In **Filter**, select **Service** and then select **storage**.
7. Filter the list of permissions, and add the following from the list:

   - `storage.buckets.get`
   - `storage.objects.create`
   - `storage.objects.delete`
   - `storage.objects.get`
   - `storage.objects.list`
8. Select **Add**.
9. Select **Create**.

#### Assign the custom role to the GCS service account

1. Log in to the Google Cloud console as a project editor.
2. From the home dashboard, select **Cloud Storage** » **Buckets**.
3. Filter the list of buckets, and select the bucket that you specified when you created an external volume.
4. Select **Permissions** » **View by principals**, then select **Grant access**.
5. Under **Add principals**, paste the name of the service account name from the
   output in [Configure an external volume in Snowsight](#label-tables-iceberg-configure-external-volume-gcs-retrieve-service-account-snowsight).
6. Under **Assign roles**, select the custom IAM role that you created previously, then select **Save**.

### Step 3: Create an external volume

To create an external volume in Snowflake by using Snowsight, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Switch role**, and then select **ACCOUNTADMIN** or a role that has the CREATE EXTERNAL VOLUME privilege.

   For instructions, see [Switch your primary role](/user-guide/ui-snowsight-gs#label-switching-your-active-role).
3. In the navigation menu, select **Catalog** » **External data**.
4. Select the **External volumes** tab.
5. Select **+ Create**.
6. Select **Google Cloud Storage** and then select **Next**.
7. Select **Next**.

   Note

   You already granted storage access earlier when you [retrieved the GCS service account for your Snowflake account](#label-tables-iceberg-configure-external-volume-gcs-retrieve-service-account-snowsight) and
   [assigned the custom role to the GCS service account](#label-configure-external-volume-gcs-assign-the-custom-role-snowsight).
8. To configure your external volume, from the **Configure external volume** page, complete the fields:

   | Field | Description |
   | --- | --- |
   | **External volume name** | Enter a name for your external volume. |
   | **Storage base URL** | Specifies the base URL for your cloud storage location. |
   | **Encryption (optional)** | Specifies the encryption type used. Possible values are:  - **None (default)**: No encryption. - **SSE-KMS (enter key)**: Server-side encryption using keys stored in KMS. For more information,   see [customer-managed encryption keys](https://cloud.google.com/storage/docs/encryption/customer-managed-keys). |
   | **Access scope** | Specifies whether write operations are allowed for the external volume; must be set to **Allow writes** for the following tables:  - Iceberg tables that use Snowflake as the catalog. - Iceberg tables that use an external catalog and are writable. Externally managed Iceberg tables are writable when you access them   through a catalog-linked database that has the ALLOWED\_WRITE\_OPERATIONS parameter set to TRUE. For Iceberg tables created from Delta table files, setting this parameter to **Allow writes** enables Snowflake to write Iceberg metadata to your external storage. For more information, see [Delta-based tables](/user-guide/tables-iceberg-metadata#label-tables-iceberg-metadata-delta).  The value of this field must also match the permissions that you set on the cloud storage account for each specified storage location.  Note  You can configure storage permissions so **Access scope** matches **read and write** or **read-only** use, depending on your use case. For comparison tables and **Delta Direct** guidance, see [Read-only vs write access for Delta Direct on each storage provider](/user-guide/tables-iceberg-metadata#label-tables-iceberg-ev-delta-read-write-options). |
   | **Scope** | Choose where this external volume should become the default location for future Iceberg tables. Possible values are:  - **Do not set a default**: Don’t set the external volume as a default anywhere. - **Account**: Set the external volume as the default for Iceberg tables that are created under the entire account. - **Specific database**: Set the external volume as the default for Iceberg tables that are created under the database you   specify. To specify this database, use the **Database** drop-down that appears when you select **Specific database**. - **Specific schema**: Set the external volume as the default for Iceberg tables that are created under the schema you specify.   To specify this schema, use the **Database** drop-down that appears to first select   the parent database of the schema and then select the schema. |
   | **Comment (optional)** | Specifies a comment for the external volume. |
   | **Connectivity** | Specifies whether to use outbound private connectivity to harden your security posture. For information about using this parameter, see [Private connectivity to external volumes for Google Cloud](/user-guide/tables-iceberg-configure-external-volume-gcs-private). Possible values are:  - **Public (default)**: Use the public internet. - **Private (Private Service Connect)**: Use outbound private connectivity. |

   Expand

   Show lessSee more
9. Select **Next**.

   On the **Verify connection & create volume** page, Snowflake verifies your connection to Google Cloud Storage and then displays
   a “Successfully connected” message.

   Note

   If Snowflake is unable to verify your connection, check your permission or external volume configuration and then select
   **Verify again**.
10. Select **Create**.

# Next steps

After you configure an external volume, you can create an Iceberg table.

- To create a read-only Iceberg table that uses an external catalog, see
  [Configure a catalog integration](/user-guide/tables-iceberg-configure-catalog-integration).
- To create an Iceberg table with full Snowflake platform support,
  see [Create a Snowflake-managed table](/user-guide/tables-iceberg-create#label-tables-iceberg-create-snowflake-catalog).
