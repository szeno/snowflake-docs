# Configure an external volume for Azure

Grant Snowflake restricted access to your own Microsoft Azure container using an external
volume. Snowflake supports the following Azure cloud storage services for external volumes:

- Blob storage
- Data Lake Storage Gen2
- General-purpose v1
- General-purpose v2
- Microsoft Fabric OneLake

Important

Remote catalogs that are only configured to use Data Lake Storage, such as Unity Catalog hosted on Azure, require table data on Data Lake Storage
for interoperability. You can connect Snowflake to this storage by configuring a
[catalog integration with vended credentials](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials) or by configuring an
external volume that connects to Data Lake Storage. For more information, see
[Enable interoperability with remote catalogs that use Data Lake Storage](#label-tables-iceberg-configure-external-volume-azure-catalog-compatibility).

Note

To harden your security posture, you can configure an external volume to use private connectivity rather than the public Internet for
network traffic. For more information, see [Private connectivity to external volumes for Microsoft Azure](/user-guide/tables-iceberg-configure-external-volume-azure-private).

To configure an external volume for Azure,
you can [use SQL](#label-configure-external-volume-azure-create-sql) or [use Snowsight](#label-configure-external-volume-azure-create-snowsight).

## Prerequisites

Before you configure an external volume, you need the following:

- An Azure storage container.

  - To use the external volume for externally managed Iceberg tables, all of your table data and metadata files must
    be located in the container.
  - To support data recovery, [enable versioning for your external cloud storage location](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-enable-storage-versioning).
- Permissions in Azure to create and manage IAM policies and roles. If you aren’t an Azure administrator, ask your Azure administrator to perform these tasks.

If you use an Azure storage firewall to block unauthorized traffic to your storage account, follow the instructions in [Allow the VNet subnet IDs](/user-guide/data-load-azure-allow)
to explicitly grant Snowflake access to your Azure storage account.

## Enable interoperability with remote catalogs that use Data Lake Storage

This section describes how to configure Snowflake so that Iceberg tables you write to by using Snowflake are interoperable with remote
catalogs that are only configured to use Data Lake Storage. For example, Unity Catalog is configured to only use Data Lake Storage.

To enable interoperability with these catalogs, table data must be on Data Lake Storage. You can connect Snowflake to Data Lake Storage in either
of the following ways:

- Configure a [catalog integration with vended credentials](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials).
  When you use vended credentials, your external catalog provides credentials for Snowflake to access Data Lake Storage.
- [Configure an external volume that connects Snowflake to Data Lake Storage](#label-tables-iceberg-configure-external-volume-azure-dls),
  which uses the `dfs.core.windows.net` endpoint.

When you use Snowflake to write to Iceberg tables that are interoperable with a remote catalog that uses Data Lake
Storage, the following scenarios are supported:

- Use Snowflake to create Snowflake-managed Iceberg tables that the query engine for the remote catalog can read and write to.

  Note

  To enable interoperability with your existing Snowflake-managed Iceberg tables that are stored in Blob Storage, migrate them
  to Data Lake Storage. For instructions, see
  [Migrate an Iceberg table to Azure Data Lake Storage](/user-guide/tables-iceberg-manage#label-iceberg-migrate-azure-dls).
- Use Snowflake to read and write to remote tables in the remote catalog.

### Configure an external volume that connects Snowflake to Data Lake Storage

To configure an external volume that connects Snowflake to Data Lake Storage, when you [create an external volume in Snowflake](#label-configure-external-volume-azure-create),
you must specify a STORAGE\_BASE\_URL that points to an `dfs.core.windows.net` endpoint.

The following example creates an external volume named `exvoldfs` that is configured with a STORAGE\_BASE\_URL that points to a
`dfs.core.windows.net` endpoint.

> Copy code
>
> ```
> CREATE EXTERNAL VOLUME exvoldfs
>   STORAGE_LOCATIONS =
>     (
>       (
>         NAME = 'my-azure-northeurope'
>         STORAGE_PROVIDER = 'AZURE'
>         STORAGE_BASE_URL = 'azure://exampleacct.dfs.core.windows.net/my_container_northeurope/'
>         AZURE_TENANT_ID = 'a123b4c5-1234-123a-a12b-1a23b45678c9'
>       )
>     );
> ```

## Configure an external volume by using SQL

### Step 1: Create an external volume in Snowflake

Create an external volume using the [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) command.

Note

Only account administrators (users with the ACCOUNTADMIN role) can execute this SQL command.

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
    );
```

Note

- Use the `azure://` prefix and not `https://` when specifying a value for STORAGE\_BASE\_URL.
- For information about specifying a OneLake location (preview feature), see the [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume#label-create-external-volume-onelake) reference page.
- If you use a regional endpoint for a Microsoft Fabric OneLake storage location,
  use the same region as your Microsoft Fabric capacity. This must also be the same region that hosts your Snowflake account.

### Step 2: Grant Snowflake access to the storage location

1. To retrieve a URL to the Microsoft permissions request page, use the [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume) command.
   Specify the name of the external volume that you created previously.

   Copy code

   ```
   DESC EXTERNAL VOLUME exvol;
   ```

   Record the values for the following properties:

   | Property | Description |
   | --- | --- |
   | `AZURE_CONSENT_URL` | URL to the Microsoft permissions request page. |
   | `AZURE_MULTI_TENANT_APP_NAME` | Name of the Snowflake client application created for your account. In a later step in this section, you grant this application permission to obtain an access token on your allowed storage location. |

   Expand

   Show lessSee more

   You use these values in the following steps.
2. In a web browser, navigate to the Microsoft permissions request page (the `AZURE_CONSENT_URL`).
3. Select **Accept**. This action allows the Azure service principal created for your Snowflake account to obtain an
   access token on a specified resource inside your tenant. Obtaining an access token succeeds only if you grant the service principal the
   appropriate permissions on the storage account level (see the next step).

   The Microsoft permissions request page redirects to the Snowflake corporate site (snowflake.com).
4. Log in to the Microsoft Azure portal.
5. Go to **Azure Services** » **Storage Accounts**. Select the name of the storage account that the Snowflake service principal
   needs to access.

   > Note
   >
   > You must set IAM permissions for an external volume at the storage account level, not the container level.
6. Select **Access Control (IAM)** » **Add role assignment**.
7. Select the `Storage Blob Data Contributor` role to grant read and write access to the Snowflake service principal.

   > Note
   >
   > The `Storage Blob Data Contributor` role grants write access to the external volume location, which is necessary for generating Iceberg metadata.
   > To completely configure write access, set the `ALLOW_WRITES` parameter of the external volume
   > to `TRUE` (the default value).
   >
   > For read-only access to Delta Lake data on Azure, you can use `Storage Blob Data Reader` with
   > `ALLOW_WRITES = FALSE` instead. See [Azure roles and Delta Direct on this external volume](#label-tables-iceberg-azure-ev-delta-read-only) and
   > [Read-only vs write access for Delta Direct on each storage provider](/user-guide/tables-iceberg-metadata#label-tables-iceberg-ev-delta-read-write-options).
8. Select **+ Select members**.
9. Search for the Snowflake service principal. This is the identity in the AZURE\_MULTI\_TENANT\_APP\_NAME property in the
   DESC EXTERNAL VOLUME output (in Step 1). Search for the string before the underscore in the AZURE\_MULTI\_TENANT\_APP\_NAME property.

   Important

   - It can take an hour or longer for Azure to create the Snowflake service principal requested through the Microsoft
     request page in this section. If the service principal is not available immediately, wait an hour
     or two and then search again.
   - If you delete the service principal, the external volume stops working.

   ![Add role assignment in Azure Storage Console](/static/images/screens/azure-storage-add-role-assignment.png)
10. Select **Review + assign**.

Note

It can take up to 10 minutes for changes to take effect when you assign a role. For more information, see
[Symptom - Role assignment changes are not being detected](https://learn.microsoft.com/en-us/azure/role-based-access-control/troubleshooting?tabs=bicep#symptom---role-assignment-changes-are-not-being-detected)
in the Microsoft Azure documentation.

#### Azure roles and Delta Direct on this external volume

For **Iceberg tables created from Delta table files**, often called **Delta Direct**, choose an Azure built-in role that matches
`ALLOW_WRITES` on the external volume: use [Storage Blob Data Reader](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/storage#storage-blob-data-reader)
with `ALLOW_WRITES = FALSE`, or [Storage Blob Data Contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/storage#storage-blob-data-contributor)
with `ALLOW_WRITES = TRUE`. Follow the consent, IAM, and **Access scope** steps earlier in this topic for either combination.

Snowflake accesses blob data on Azure by using Microsoft Entra ID authentication and a [user delegation key](https://learn.microsoft.com/en-us/rest/api/storageservices/get-user-delegation-key).
The Snowflake service principal needs the `Microsoft.Storage/storageAccounts/blobServices/generateUserDelegationKey` action.
Both [Storage Blob Data Reader](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/storage#storage-blob-data-reader) and
[Storage Blob Data Contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/storage#storage-blob-data-contributor) include this action in their role definitions.

Because `generateUserDelegationKey` is a storage account-level operation, assign the blob data role at **storage account** scope (as described earlier in this topic).
With that scope, read-only Delta Direct (`ALLOW_WRITES = FALSE`) works when you assign only Storage Blob Data Reader.

If you assign Storage Blob Data Reader or Storage Blob Data Contributor only at **container** scope, the service principal might not be able to generate a user delegation key at the storage account.
In that case, either assign Storage Blob Data Reader (or Storage Blob Data Contributor) at storage account scope, or add an additional account-level role that grants `generateUserDelegationKey`, such as
[Storage Blob Delegator](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/storage#storage-blob-delegator), for the same Snowflake service principal.

For the same read-only and write patterns on Amazon S3 and Google Cloud Storage, see [Read-only vs write access for Delta Direct on each storage provider](/user-guide/tables-iceberg-metadata#label-tables-iceberg-ev-delta-read-write-options).

### Step 3: Verify storage access

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

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Switch role**, and then select **ACCOUNTADMIN** or a role that has the CREATE EXTERNAL VOLUME privilege.

   For more information, see [Switch your primary role](/user-guide/ui-snowsight-gs#label-switching-your-active-role).
3. In the navigation menu, select **Catalog** » **External data**.
4. Select the **External volumes** tab.
5. Select **+ Create**.
6. Select **Microsoft Azure & OneLake** and then select **Next**.
7. From the **Prerequisites** page, for **Azure tenant ID**, specify your Azure tenant ID.

   To find your Azure tenant ID, see [How to find your Microsoft Entra tenant ID](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-find-tenant)
   in the Microsoft Entra documentation.
8. Select **Next**.
9. From the **Grant storage access** page, to grant Snowflake access to the storage location, follow these steps:

   1. To provide consent for Snowflake to connect to your Azure storage or Microsoft OneLake,
      select **Provide consent**.

      The Microsoft permissions request page opens in a new browser tab.
   2. From the Microsoft permissions request page, select **Accept**. This action allows the Azure service principal created for your
      Snowflake account to obtain an access token on a specified resource inside your tenant. Obtaining an access token succeeds only if you
      grant the service principal the appropriate permissions on the storage account level (see the next step).

      The Microsoft permissions request page redirects to the Snowflake corporate site (snowflake.com).
   3. In Snowflake, from the **Multi-tenant app name** field, copy the name of the Snowflake client application created for your account
      into a text editor. In the next step, you grant this application permission to obtain an access token on your allowed storage location.
10. To grant your application permission to obtain an access token on your allowed storage location, follow these steps:
11. Log in to the Microsoft Azure portal.
12. Go to **Azure Services** » **Storage Accounts**. Select the name of the storage account that the Snowflake service principal
    needs to access.

    > Note
    >
    > You must set IAM permissions for an external volume at the storage account level, not the container level.
13. Select **Access Control (IAM)** » **Add role assignment**.
14. Select the `Storage Blob Data Contributor` role to grant read and write access to the Snowflake service principal.

    > Note
    >
    > The `Storage Blob Data Contributor` role grants write access to the external volume location.
    > To completely configure write access, set the `ALLOW_WRITES` parameter of the external volume
    > to `TRUE` (the default value).
    >
    > For read-only access to Delta data on Azure, you can use `Storage Blob Data Reader` with
    > `ALLOW_WRITES = FALSE` instead. See [Azure roles and Delta Direct on this external volume](#label-tables-iceberg-azure-ev-delta-read-only) and
    > [Read-only vs write access for Delta Direct on each storage provider](/user-guide/tables-iceberg-metadata#label-tables-iceberg-ev-delta-read-write-options).
15. Select **+ Select members**.
16. Search for the Snowflake service principal.

    This is the *Multi-tenant app name* that you copied from Snowflake in the previous step.

    Important

    - It can take an hour or longer for Azure to create the Snowflake service principal requested through the Microsoft
      request page in this section. If the service principal is not available immediately, wait an hour
      or two and then search again.
    - If you delete the service principal, the external volume stops working.

    ![Add role assignment in Azure Storage Console](/static/images/screens/azure-storage-add-role-assignment.png)
17. Select **Review + assign**.

    Note

    It can take up to 10 minutes for changes to take effect when you assign a role. For more information, see
    [Symptom - Role assignment changes are not being detected](https://learn.microsoft.com/en-us/azure/role-based-access-control/troubleshooting?tabs=bicep#symptom---role-assignment-changes-are-not-being-detected)
    in the Microsoft Azure documentation.
18. In Snowflake, select **Next**.
19. In Snowflake, to configure your external volume, from the **Configure external volume** page, complete the fields:

| Field | Description |
| --- | --- |
| **External volume name** | Enter a name for your external volume. |
| **Storage base URL** | Specifies the base URL for your cloud storage location. |
| **Access scope** | Specifies whether write operations are allowed for the external volume; must be set to **Allow writes** for the following tables:   - Iceberg tables that use Snowflake as the catalog. - Iceberg tables that use an external catalog and are writable. Externally managed Iceberg tables are writable when you access them   through a catalog-linked database that has the ALLOWED\_WRITE\_OPERATIONS parameter set to TRUE.   For Iceberg tables created from Delta table files, setting this parameter to **Allow writes** enables Snowflake to write Iceberg metadata to your external storage. For more information, see [Delta-based tables](/user-guide/tables-iceberg-metadata#label-tables-iceberg-metadata-delta).  The value of this parameter must also match the permissions that you set on the cloud storage account for each specified storage location.  Note  If you plan to use the external volume for only reading externally managed Iceberg tables or Delta Direct tables, you can set this field to Off. Snowflake doesn’t write data or Iceberg metadata files to your cloud storage when you read tables in an external Iceberg catalog. |
| **Scope** | Choose where this external volume should become the default location for future Iceberg tables. Possible values are:   - **Do not set a default**: Don’t set the external volume as a default anywhere. - **Account**: Set the external volume as the default for Iceberg tables that are created under the entire account. - **Specific database**: Set the external volume as the default for Iceberg tables that are created under the database you   specify. To specify this database, use the **Database** drop-down that appears when you select **Specific database**. - **Specific schema**: Set the external volume as the default for Iceberg tables that are created under the schema you specify.   To specify this schema, use the **Database** drop-down that appears to first select   the parent database of the schema and then select the schema. |
| **Comment (optional)** | Specifies a comment for the external volume. |
| **Connectivity** | Specifies whether to use outbound private connectivity to harden your security posture. For information about using outbound private connectivity, see [Private connectivity to external volumes for Microsoft Azure](/user-guide/tables-iceberg-configure-external-volume-azure-private). Possible values are:   - **Public (default)**: Use the public internet. - **Private (Azure Private Endpoint)**: Use outbound private connectivity. |

Expand

Show lessSee more

13. Select **Next**.

On the **Verify connection & create volume** page, Snowflake verifies your connection to Azure and then displays
a “Successfully connected” message.

Note

If Snowflake is unable to verify your connection, check your permission or external volume configuration and then select
**Verify again**.

14. Select **Create**.

# Next steps

After you configure an external volume, you can create an Iceberg table.

- To create a read-only Iceberg table that uses an external catalog, see
  [Configure a catalog integration](/user-guide/tables-iceberg-configure-catalog-integration).
- To create an Iceberg table with full Snowflake platform support,
  see [Create a Snowflake-managed table](/user-guide/tables-iceberg-create#label-tables-iceberg-create-snowflake-catalog).
