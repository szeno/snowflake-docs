# Configure a catalog integration for OneLake REST

Follow the steps in this topic to create a catalog integration for the OneLake REST API endpoint, which is an endpoint for OneLake
table APIs that you can use to interact with tables in Microsoft Fabric. For more information about this endpoint,
see [Getting started with OneLake table APIs for Iceberg](https://learn.microsoft.com/en-us/fabric/onelake/table-apis/iceberg-table-apis-get-started)
in the Microsoft Fabric documentation.

With this catalog integration, you can use Snowflake to read OneLake tables that have Iceberg metadata.

## Prerequisites

- Before you begin, you must find your workspace ID for your workspace in Fabric and the data item ID for your lakehouse in Fabric.
  You specify your workspace ID and data item ID later when you create a catalog integration for OneLake REST.

  - To find your workspace ID (`<workspaceID>`), refer to the URL of the Fabric site for an item in a workspace. For more information, see
    [Identify your workspace ID](https://learn.microsoft.com/en-us/fabric/admin/portal-workspace#identify-your-workspace-id) in the
    Microsoft Fabric documentation. Copy your workspace ID into a text editor.
  - To find your data item ID (`<dataItemID>`), open your lakehouse, and then refer to the value after `lakehouses` in the URL. For more information,
    see [Lakehouse source configuration](https://learn.microsoft.com/en-us/fabric/data-factory/connector-lakehouse-copy-activity#source)
    in the Microsoft Fabric documentation and see the Connection bullet point. Copy your data item ID into a text editor.
- In your Fabric workspace, make sure you have Iceberg tables in any data item, such as in a lakehouse.

## Step 1: Configure access permissions for OneLake

To configure access permissions for OneLake, you create an application registration in Microsoft Azure, add the user\_impersonation
permission to your application registration, and create a new client secret for your application registration.

1. In Azure, create an application registration.

   For details, see [Register an application in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)
   in the Microsoft Entra documentation.
2. In your application registration, add the user\_impersonation permission.

   To get started, follow the first four steps in [Use the Microsoft Entra admin center to find the APIs your organization uses](https://learn.microsoft.com/en-us/graph/migrate-azure-ad-graph-configure-permissions?tabs=http&pivots=entra-portal-api-permissions#use-the-microsoft-entra-admin-center-to-find-the-apis-your-organization-uses)
   in the Microsoft Graph documentation.

   Important

   Don’t switch to the **APIs my organization uses** tab as described in the steps. Instead, switch to the **Microsoft APIs** tab,
   select **Azure Storage**, and then add the **user\_impersonation** permission.
3. Create a new client secret for your application registration, and then copy the secret into a text editor.

   For instructions, see
   [Create a new client secret](https://learn.microsoft.com/en-us/entra/identity-platform/howto-create-service-principal-portal#option-3-create-a-new-client-secret)
   in the Microsoft Entra documentation. You specify this secret when you create a catalog integration.

   Important

   Remember to copy your secret to a text editor, because you can’t retrieve it later.
4. From the **Overview** page of your application registration, copy the **Display name**, **Application (client) ID**, and
   **Directory (tenant) ID** into a text editor.

   You specify these values when you create a catalog integration and external volume.

## Step 2: Grant your application registration access to your Fabric workspace

In this step, you give your application registration access to your workspace in Fabric.

1. Navigate to [Microsoft Fabric](https://app.fabric.microsoft.com/), and then sign in.
2. Open your Microsoft Fabric workspace.
3. Select **Manage access**.
4. Select **+ Add people or groups**.
5. In the **Enter name or email** field, paste the name of your application registration.

   This name is the **Display name** that
   you copied when you [configured access permissions for OneLake](#label-configure-access-permissions-onelake).
6. From the drop-down menu, select **Contributor** access or higher to allow the app to create the necessary Fabric item.
7. Select **Add**.

## Step 3: Create a catalog integration in Snowflake

Create a catalog integration for the REST API endpoint by using the [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest) command.

For example:

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION my_onelake_catalog_int
   CATALOG_SOURCE = ICEBERG_REST
   TABLE_FORMAT = ICEBERG
   REST_CONFIG = (
      CATALOG_URI = 'https://onelake.table.fabric.microsoft.com/iceberg'
      CATALOG_NAME = '<fabric_data_item_scope>'
   )
   REST_AUTHENTICATION = (
      TYPE = OAUTH
      OAUTH_TOKEN_URI = '<azure_active_directory_token_endpoint>'
      OAUTH_CLIENT_ID = '<entra_application_client_id>'
      OAUTH_CLIENT_SECRET = '<entra_application_client_secret>'
      OAUTH_ALLOWED_SCOPES = ('https://storage.azure.com/.default')
   )
   ENABLED = TRUE;
```

Where:

- `https://onelake.table.fabric.microsoft.com/iceberg` is the base URL at the OneLake table endpoint.
- `<fabric_data_item_scope>` is the Fabric data item scope, in the form `<workspaceID>`/`<dataItemID>`, such as
  `12345678-abcd-1abc-1a11-111111ab1111/11111111-abcd-1111-1ab1-1111a1a1ab91`. To find your `<workspaceID>` and `<dataItemID>`, see [Prerequisites](#label-tables-iceberg-configure-catalog-integration-rest-onelake-before-you-begin).
- `<azure_active_directory_token_endpoint_>` is your Azure Active Directory OAuth 2.0 token endpoint URL, in the form of `https://login.microsoftonline.com/<entra_tenant_id>/oauth2/v2.0/token`.
  For `<entra_tenant_id>` you specify your Entra tenant ID, which you copied when you [configured access permissions for OneLake](#label-configure-access-permissions-onelake).
- `<entra_application_client_id>` is your Entra application client ID, which you copied when you [configured access permissions for OneLake](#label-configure-access-permissions-onelake), such as `11111111-aabb-1a11-abc1-ab11111a11a1`.
- `<entra_application_client_secret>` is your application client secret, which you copied when you [configured access permissions for OneLake](#label-configure-access-permissions-onelake).
- `https://storage.azure.com/.default` is the storage token audience.

## Step 4: Configure an external volume

In this step, you configure an external volume for Azure with your Azure OneLake URL and your Entra tenant ID.

1. Create an external volume using the [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) command.

   For example:

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL VOLUME my_onelake_extvol
   STORAGE_LOCATIONS =
   (
      (
            NAME = 'my_onelake_extvol'
            STORAGE_PROVIDER = 'AZURE'
            STORAGE_BASE_URL = '<azure_onelake_url>'
            AZURE_TENANT_ID='<entra_tenant_id>'
      )
   )
   ALLOW_WRITES = FALSE;
   ```

   Where:

   - `<azure_onelake_url>` is your Azure OneLake URL, in the form of `azure://onelake.dfs.fabric.microsoft.com/<workspaceID>/<dataItemID>`, such as `azure://onelake.dfs.fabric.microsoft.com/12345678-abcd-1abc-1a11-111111ab1111/11111111-abcd-1111-1ab1-1111a1a1ab91`.
     To find your `<workspaceID>` and `<dataItemID>`, see [Prerequisites](#label-tables-iceberg-configure-catalog-integration-rest-onelake-before-you-begin).
   - `<entra_tenant_id>` is your Entra tenant ID, such as, `11111111-aabb-1a11-abc1-ab11111a11a1`. You copied your Entra tenant ID when you [configured access permissions for OneLake](#label-configure-access-permissions-onelake).
2. To retrieve a URL to the Microsoft permissions request page, use the [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume) command.
   Specify the name of the external volume that you created previously.

   Copy code

   ```
   DESC EXTERNAL VOLUME my_onelake_extvol;
   ```

   Record the values for the following properties:

   | Property | Description |
   | --- | --- |
   | `AZURE_CONSENT_URL` | URL to the Microsoft permissions request page. |
   | `AZURE_MULTI_TENANT_APP_NAME` | Name of the Snowflake client application created for your account. In a later step in this section, you grant this application permission to obtain an access token on your allowed storage location. |

   Expand

   Show lessSee more

   You use these values in the following steps.
3. In a web browser, navigate to the Microsoft permissions request page (the `AZURE_CONSENT_URL`).
4. Select **Accept**. This action allows the Azure service principal created for your Snowflake account to obtain an
   access token on a specified resource inside your tenant. Obtaining an access token succeeds only if you grant the service principal the
   appropriate permissions on the storage account level (see the next step).
5. Give the multi-tenant application permission to obtain an access token on your allowed storage location in Fabric.

   1. Navigate to [Microsoft Fabric](https://app.fabric.microsoft.com/), and then sign in.
   2. Open your Microsoft Fabric workspace.
   3. Select **Manage access**.
   4. Select **+ Add people or groups**.
   5. In the **Enter name or email** field, paste the value you recorded for AZURE\_MULTI\_TENANT\_APP\_NAME.
   6. From the drop-down menu, select **Contributor** access or higher to allow the app to create the necessary Fabric item.
   7. Select **Add**.

For more information, see [Example Snowflake catalog integration and external volume code for the REST endpoint in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/onelake/table-apis/iceberg-table-apis-get-started#snowflake)
in the Microsoft Fabric documentation.

## Next steps

After you configure a catalog integration for OneLake REST and an external volume, you can use the [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked)
command to create a catalog-linked database, and then read your tables from OneLake in Snowflake.

When you create your catalog-linked database, you specify the catalog integration and external volume that you created.

For example:

Copy code

```
CREATE OR REPLACE DATABASE my_linked_db
   LINKED_CATALOG = (
      CATALOG = 'my_onelake_catalog_int'
   )
   EXTERNAL_VOLUME = 'my_onelake_extvol';

SELECT SYSTEM$CATALOG_LINK_STATUS('IRC_CATALOG_LINKED');

SELECT * FROM my_linked_db."dbo"."sentiment";
```

Note

Snowflake only supports read operations for tables in OneLake.
