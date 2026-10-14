# Databricks

Connect Databricks to Horizon Catalog to collect metadata, lineage, and popularity. These instructions apply to Databricks on both AWS and Azure. Where a step differs between the two clouds, the difference is called out inline.

Horizon Catalog authenticates to Databricks using OAuth machine-to-machine (M2M) authentication with a service principal. You create a service principal, generate an OAuth secret, grant it read access, and provide the service principal’s client ID and secret when you create the connection.

## Before you start

Note

Ensure Unity Catalog is enabled for your Databricks instance. For details, see [Getting Started with Unity Catalog](https://docs.databricks.com/data-governance/unity-catalog/get-started.html).

To connect Databricks to Horizon Catalog, you will need:

- A Databricks instance on [AWS](https://www.databricks.com/product/aws) or [Azure](https://www.databricks.com/product/azure), with Unity Catalog enabled.
- Account admin permissions on the Databricks instance.
- Workspace admin permissions on the Databricks instance.

Complete all of the following steps to see Databricks metadata, lineage, and popularity in Horizon Catalog:

1. [Create a service principal in Databricks](#1-create-a-service-principal-in-databricks)
2. [Create an OAuth secret for the service principal](#2-create-an-oauth-secret-for-the-service-principal)
3. [Assign the service principal to a workspace and grant access](#3-assign-the-service-principal-to-a-workspace-and-grant-access)
4. [Grant catalog permissions to the service principal](#4-grant-catalog-permissions-to-the-service-principal)
5. [Grant workspace permissions to the service principal](#5-grant-workspace-permissions-to-the-service-principal)
6. [Configure system tables lineage (recommended)](#6-configure-system-tables-lineage-recommended)
7. [Create the Databricks connection](#7-create-the-databricks-connection)
8. [Choose catalogs and schemas](#8-choose-catalogs-and-schemas)
9. [Set up metadata access](#9-set-up-metadata-access)

## 1. Create a service principal in Databricks

A service principal is an identity that you create in Databricks for use with automated tools, jobs, and applications. Service principals give automated tools and scripts API-only access to Databricks resources, providing greater security than using users or groups.

You can add a service principal in one of two ways, depending on your access. Choose the method that matches your role, then follow those steps. You only need to complete one method.

- If you have **account admin** access, use [Option A: Account console](#option-a-account-console-account-admin).
- If you have **workspace admin** access, use [Option B: Workspace admin settings](#option-b-workspace-admin-settings-workspace-admin).

### Option A: Account console (account admin)

1. As an account admin, log in to the account console: [AWS](https://accounts.cloud.databricks.com/) or [Azure](https://accounts.azuredatabricks.net/).
2. In the sidebar, click **User management**.
3. On the **Service principals** tab, click **Add service principal**.
4. Enter a name for the service principal (for example, `SnowflakeHorizon`).
5. Click **Add**.

### Option B: Workspace admin settings (workspace admin)

This option creates the service principal, adds it to the current workspace, and sets its workspace entitlements in a single dialog. If you use this option, you can skip [Step 3](#3-assign-the-service-principal-to-a-workspace-and-grant-access).

1. As a workspace admin, log in to the Databricks workspace.
2. Click your username in the top bar and select **Settings**.
3. Click the **Identity and access** tab.
4. Next to **Service principals**, click **Manage**.
5. Click **Add service principal**, then click **Add new**.
6. Enter a name for the service principal (for example, `SnowflakeHorizon`).
7. Under **Workspace entitlements**, turn on **Databricks SQL access** and **Workspace access**.
8. Click **Add service principal**.

For details, including the Azure options for Databricks managed and Microsoft Entra ID managed service principals, see the Databricks documentation on managing service principals ([AWS](https://docs.databricks.com/aws/en/admin/users-groups/manage-service-principals) or [Azure](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-service-principals)).

## 2. Create an OAuth secret for the service principal

Horizon Catalog uses the service principal’s **client ID** and **secret** to authenticate with OAuth machine-to-machine (M2M) authentication.

### Generate an OAuth secret as a workspace admin

1. As a workspace admin, log in to the Databricks workspace.
2. Click your username in the top bar and select **Settings**.
3. Click the **Identity and access** tab.
4. Next to **Service principals**, click **Manage**.
5. Select the Horizon Catalog service principal.
6. Click the **Secrets** tab.
7. Click **Generate secret**.
8. Set the secret’s lifetime in days (maximum 730), and click **Generate**.
9. Copy the **Secret** and the **Client ID**, and click **Done**.

### Generate an OAuth secret as an account admin

Alternatively, account admins can generate an OAuth secret from the account console. On the **User management** tab, select the service principal, open the **Credentials & secrets** tab, and click **Generate secret**.

Warning

The secret is displayed only once. Store the **Client ID** and **Secret** securely (for example, in a password manager). You’ll enter both when you [create the Databricks connection](#7-create-the-databricks-connection) in Step 7. The client ID is the same as the service principal’s application ID.

For more details, see [Authorize service principal access to Databricks with OAuth](https://docs.databricks.com/dev-tools/auth/oauth-m2m).

## 3. Assign the service principal to a workspace and grant access

Note

If you created the service principal using [Option B: Workspace admin settings](#option-b-workspace-admin-settings-workspace-admin) in Step 1, it’s already added to this workspace with the required entitlements. Skip to [Step 4](#4-grant-catalog-permissions-to-the-service-principal).

If you created the service principal in the account console (Option A), assign it to the [identity-federated workspace](https://docs.databricks.com/administration-guide/users-groups/index.html#assign-users-to-workspaces) that’s linked to the metastore you want to catalog, and grant it the entitlements Horizon Catalog needs. The workspace must be enabled for identity federation.

1. As an account admin, log in to the account console.
2. Click **Workspaces**, and click your workspace name.
3. On the **Permissions** tab, click **Add permissions**.
4. Search for and select the service principal you created.
5. Select the **Workspace access** and **Databricks SQL access** entitlements, and click **Save**.

These are the minimum entitlements required for Horizon Catalog to collect basic metadata and query history.

## 4. Grant catalog permissions to the service principal

1. As a workspace admin, log in to a workspace that is linked to the metastore.
2. Click **Catalog**.
3. Click the catalog you want to grant access to, and select **Permissions**.
4. Click **Grant**.
5. Select the service principal and set the privilege preset to **Data Reader**, ensure the **USE CATALOG**, **USE SCHEMA**, and **SELECT** checkboxes are selected, and click **Grant**.

## 5. Grant workspace permissions to the service principal

This step is required to show notebooks in the catalog and to generate notebook lineage.

1. Log in to a workspace that is linked to the metastore.
2. Click **Workspace**, then select the top-level **Workspace** folder (the root that contains the **Shared** and **Users** folders, not your personal **Home** folder), so lineage covers all notebooks.
3. Click the **Share** button.
4. Select the service principal, select the **Can view** permission, and click **Add**.

## 6. Configure system tables lineage (recommended)

Note

This section is optional but recommended. System tables lineage provides better performance and scalability by using Databricks system tables instead of individual API calls. If you skip this section, Horizon Catalog uses API lineage collection.

System tables lineage requires additional permissions beyond the basic setup. These permissions allow Horizon Catalog to query Databricks system tables that contain lineage metadata, without accessing your actual data.

### Grant SQL warehouse access permissions

The service principal needs permission to use a specific SQL warehouse for executing lineage queries.

1. In your Databricks workspace, go to **SQL Warehouses**.
2. Select the SQL warehouse you want to use for Horizon Catalog.
3. Click the **Permissions** button.
4. Click **Add** and search for your Horizon Catalog service principal.
5. Grant the **Can use** permission and click **Add**.

Note

Note the **Warehouse ID** from the SQL warehouse details page. You’ll need it when connecting to Horizon Catalog.

### Grant system.access schema permissions

The service principal needs permissions to read lineage data from Databricks system tables.

1. In your Databricks workspace, select **Catalog**.
2. Select the **system** catalog, select the **Permissions** tab, then select **Grant**.
3. Search for and select your Horizon Catalog service principal, select **USE CATALOG**, then select
   **Grant**.
4. Expand the **system** catalog, select the **access** schema, select the **Permissions** tab, then
   select **Grant**.
5. Search for and select your Horizon Catalog service principal, select **USE SCHEMA** and
   **SELECT**, then select **Grant**.

Alternatively, grant SELECT on the specific system tables that Horizon Catalog reads by
running the following statements in a SQL editor, replacing
`<service-principal-application-id>` with the client ID from
[Step 2](#2-create-an-oauth-secret-for-the-service-principal):

Copy code

```
GRANT USE CATALOG ON CATALOG system TO `<service-principal-application-id>`;
GRANT USE SCHEMA ON SCHEMA system.access TO `<service-principal-application-id>`;
GRANT SELECT ON TABLE system.access.table_lineage TO `<service-principal-application-id>`;
GRANT SELECT ON TABLE system.access.column_lineage TO `<service-principal-application-id>`;
```

### Ensure SQL access entitlement is enabled

Verify that your service principal has the SQL access entitlement enabled:

1. In your Databricks workspace, click your username and select **Settings**.
2. Go to the **Identity and access** tab, and next to **Service principals**, click **Manage**.
3. Select your Horizon Catalog service principal.
4. Ensure **Databricks SQL access** is checked, and click **Update** if needed.

## 7. Create the Databricks connection

In Snowflake, open **Catalog > Connections** and select **Databricks** from the Metadata connections section.

Provide the following information:

**Display Name:** This value is `Databricks` by default, but you can override it if desired.

**Workspace URL:** The address of the workspace. Use the format for your deployment:

- **AWS:** `https://<deployment name>.cloud.databricks.com`. Find the deployment name in <https://accounts.cloud.databricks.com/workspaces>.
- **Azure:** `https://<identifier>.azuredatabricks.net`. Find the identifier in <https://accounts.azuredatabricks.net/workspaces>.

**Client ID:** The service principal’s client ID (application ID) from [Step 2](#2-create-an-oauth-secret-for-the-service-principal).

**Client Secret:** The OAuth secret you generated for the service principal in [Step 2](#2-create-an-oauth-secret-for-the-service-principal).

**Lineage Method:** Choose between System tables (recommended) or API lineage collection.

**SQL Warehouse ID:** Required when using System tables lineage. This is the Warehouse ID noted in [Step 6](#6-configure-system-tables-lineage-recommended). Not available for use with API lineage.

## 8. Choose catalogs and schemas

After you fill in the information, you’ll be asked to select the catalog you’d like to load into Horizon Catalog.

Note

Horizon Catalog will not read queries or metadata, or generate lineage, for catalogs, schemas, or tables that are not loaded. Load all data for which you expect to see lineage.

Select the catalogs and click **Next**. For each catalog you selected, you’ll be able to select the schemas.

Your metadata should start loading automatically. Allow 24 to 48 hours to completely generate popularity and lineage.

When the sync is complete, you’ll be able to explore Databricks in Horizon Catalog.

## 9. Set up metadata access

Other roles can’t see the metadata and lineage that this connector collects until you grant them
access. Grant `USAGE` on the connector, and on the database and schema that contain it, to each role
that needs to view the connector’s metadata and lineage:

Copy code

```
GRANT USAGE ON DATABASE CONNECTORS TO ROLE <role_name>;
GRANT USAGE ON SCHEMA CONNECTORS.METADATA TO ROLE <role_name>;
GRANT USAGE ON METADATA CONNECTOR CONNECTORS.METADATA.<connector_name> TO ROLE <role_name>;
```

If you stored the connector in a different database or schema, replace `CONNECTORS` and `METADATA`
with the actual database and schema names.

For more information about metadata access, see
[Metadata access control](/user-guide/snowflake-horizon/connectors/access-control).

## Connection security

All communication between Horizon Catalog and Databricks uses HTTPS (TLS 1.2 or higher). No additional encryption configuration is required.

For more details, see [Security and data protection](/user-guide/snowflake-horizon/connectors/security).
