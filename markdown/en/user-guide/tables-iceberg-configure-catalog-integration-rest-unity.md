# Configure a catalog integration for Unity Catalog

Use the [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest) command to create a REST catalog integration that uses
[vended credentials](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials)
or an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) to connect to Databricks Unity Catalog.

Note

- To configure a catalog integration for connecting to Databricks Unity Catalog through a private IP address instead of over the public internet,
  see [Configure an Apache Iceberg™ REST catalog integration with outbound private connectivity](/user-guide/tables-iceberg-configure-catalog-integration-rest-private).
- For a tutorial that covers how to connect Snowflake to a catalog in Databricks Unity Catalog by using a writable
  catalog-linked database with catalog-vended credentials, see [Tutorial: Set up bidirectional access to Apache Iceberg™ tables in Databricks Unity Catalog](/user-guide/tutorials/tables-iceberg-set-up-bidirectional-access-to-unity-catalog).

You can create a catalog integration for Unity Catalog where the Databricks workspace is hosted on one of the following cloud providers:

- AWS
- Azure
- Google Cloud

You can configure a catalog integration for Unity Catalog that uses OAuth or bearer authentication:

- [Configure an OAuth catalog integration](#label-tables-iceberg-configure-catalog-integration-rest-unity-oauth)
- [Configure a bearer token catalog integration](#label-tables-iceberg-configure-catalog-integration-rest-unity-bearer)

## Configure an OAuth catalog integration

### Step 1: Find your Databricks workspace URL

Your Databricks workspace URL is the URL that you use to access your Databricks workspace. You need to find this URL because you specify
it later when you create a catalog integration.

1. Find your Databricks workspace URL.

   For instructions on how to find this URL, see the topic for where your Databricks account is hosted:

   - **Databricks on AWS**: [Databricks on AWS: Workspace instance names, URLs, and IDs](https://docs.databricks.com/aws/workspace/workspace-details#workspace-instance-names-urls-and-ids)
   - **Azure Databricks**: [Azure Databricks: Determine per-workspace URL](https://learn.microsoft.com/azure/databricks/workspace/workspace-details#determine-per-workspace-url)
   - **Databricks on Google Cloud**: [Databricks on Google Cloud: Workspace instance names, URLs, and IDs](https://docs.databricks.com/gcp/workspace/workspace-details#workspace-instance-names-urls-and-ids)
2. Copy your Databricks workspace URL into a text editor.

### Step 2: Add a service principal in Databricks

1. To add a service principal, see the topic for where your Databricks account is hosted:

   - **Databricks on AWS**: [Databricks on AWS: Add service principals to your account](https://docs.databricks.com/aws/admin/users-groups/manage-service-principals?language=Account%C2%A0console#-add-service-principals-to-your-account)
   - **Azure Databricks**: [Azure Databricks: Add service principals to your account](https://learn.microsoft.com/azure/databricks/admin/users-groups/manage-service-principals#-add-service-principals-to-your-account)
   - **Databricks on Google Cloud**: [Databricks on Google Cloud: Add service principals to your account](https://docs.databricks.com/gcp/admin/users-groups/manage-service-principals#-add-service-principals-to-your-account)
2. Copy the *Application ID* value for your service principal into a text editor and store it securely. You specify this value later
   when you create a catalog integration in Snowflake.

### Step 3: Create an OAuth secret for your service principal

1. To create an OAuth secret for your service principal, see the topic for where your Databricks account is hosted:

   - **Databricks on AWS**: [Databricks on AWS: Create an OAuth secret](https://docs.databricks.com/aws/dev-tools/auth/oauth-m2m#-step-1-create-an-oauth-secret)
   - **Azure Databricks**: [Azure Databricks: Create an OAuth secret](https://learn.microsoft.com/azure/databricks/dev-tools/auth/oauth-m2m#-step-1-create-an-oauth-secret)
   - **Databricks on Google Cloud**: [Databricks on Google Cloud: Create an OAuth secret](https://docs.databricks.com/gcp/dev-tools/auth/oauth-m2m#-step-1-create-an-oauth-secret)
2. Copy the *Secret* value that you generated into a text editor and store it securely. You specify this value later when you create a
   catalog integration in Snowflake.

   Important

   The client secret is only displayed once. Make sure to copy it before closing the dialog.

### Step 4: Enable Snowflake access to your catalog in Unity Catalog

In this step, you use Databricks to enable Snowflake access to your catalog in Unity Catalog.

To enable Snowflake access to your catalog in Unity Catalog through vended credentials, first, at the metastore level, you must enable
external data access on the metastore. Next, you need to grant your service principal Unity Catalog privileges to your catalog.

#### Enable external data access on the metastore (vended credentials only)

If you’re creating a catalog integration that uses vended credentials, you must enable external data access on the metastore in Databricks.
If you’re creating a catalog integration that uses an external volume, you can skip this step.

For instructions on how to enable external data access on the metastore, see the topic for where your Databricks account is hosted:

- **Databricks on AWS**: [Databricks on AWS: Enable external data access on the metastore](https://docs.databricks.com/aws/en/external-access/admin#enable-external-data-access-on-the-metastore)
- **Azure Databricks**: [Azure Databricks: Enable external data access on the metastore](https://learn.microsoft.com/en-us/azure/databricks/external-access/admin#enable-external-data-access-on-the-metastore)
- **Databricks on Google Cloud**: [Databricks on Google Cloud: Enable external data access on the metastore](https://docs.databricks.com/gcp/en/external-access/admin#enable-external-data-access-on-the-metastore)

#### Assign your service principal to a workspace

Next, you need to assign your service principal to your Databricks workspace.

For instructions, see the topic for where your Databricks account is hosted:

- **Databricks on AWS**: [Databricks on AWS: Assign a service principal to a workspace](https://docs.databricks.com/aws/en/admin/users-groups/manage-service-principals?language=Account%C2%A0console#assign-a-service-principal-to-a-workspace)
- **Azure Databricks**: [Azure Databricks: Assign a service principal to a workspace](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-service-principals#assign-a-service-principal-to-a-workspace)
- **Databricks on Google Cloud**: [Databricks on Google Cloud: Assign a service principal to a workspace](https://docs.databricks.com/gcp/en/admin/users-groups/manage-service-principals#assign-a-service-principal-to-a-workspace)

#### Grant your service principal access to your catalog

Next, you must grant your service principal Unity Catalog privileges. You need to grant these privileges to your service principal to allow
Snowflake to access the catalog based on the privileges that you specify.

##### Privileges for full functionality

To enable full functionality in Snowflake, you must grant the following privileges:

Note

If you want to restrict Snowflake access, see [Unity Catalog privileges and securable objects](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/privileges)
in the Databricks documentation.

| Privilege | Description |
| --- | --- |
| `ALL PRIVILEGES` | Grants all privileges on the catalog, including the ability to create tables. Required together with `EXTERNAL USE SCHEMA` to enable creating tables from Snowflake. |
| `EXTERNAL USE SCHEMA` | Allows Unity Catalog to generate and provide temporary, scoped credentials to Snowflake for accessing table data in cloud storage. Note This privilege is only required when you create a catalog integration that uses vended credentials; it’s not required when you create a catalog integration that uses an external volume, so if you’re using an external volume, remove it from the example code block. |
| `MODIFY` | Allows Snowflake to add, update, and delete data in a table. |
| `SELECT` | Allows Snowflake to query tables and access table metadata. Required for all operations in Snowflake, including reading data and discovering tables in the catalog-linked database. |
| `USE CATALOG` | Allows Snowflake to access the catalog. Required to connect to and interact with any objects in the Unity Catalog. |
| `USE SCHEMA` | Allows Snowflake access to schemas (namespaces) within the catalog. Required to view and work with tables in specific schemas. |

Expand

Show lessSee more

##### Grant privileges

You can grant privileges by using Catalog Explorer or SQL.

Catalog ExplorerSQL

To grant permissions by using the Databricks Catalog Explorer, see the topic for where your Databricks account is hosted:

- **Databricks on AWS**: [Databricks on AWS: Grant permissions on an object](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges#-grant-permissions-on-an-object)
- **Azure Databricks**: [Azure Databricks: Grant permissions on an object](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges#-grant-permissions-on-an-object)
- **Databricks on Google Cloud**: [Databricks on Google Cloud: Grant permissions on an object](https://docs.databricks.com/gcp/en/data-governance/unity-catalog/manage-privileges#-grant-permissions-on-an-object)

Important

In the **Principals** field, you must enter the name of your service principal, not the email address for a user or the
name of a group.

To grant your service principal Unity Catalog privileges, you must specify the Application ID for your service principal.

For example, the following statement grants `example_sales_catalog` catalog privileges to a service principal with an
Application ID of `1aaa1a1a-11a1-1111-1111-1a11111aaa1a`.

Copy code

```
GRANT EXTERNAL USE SCHEMA ON CATALOG example_sales_catalog TO `1aaa1a1a-11a1-1111-1111-1a11111aaa1a`;
GRANT MODIFY ON CATALOG example_sales_catalog TO `1aaa1a1a-11a1-1111-1111-1a11111aaa1a`;
GRANT SELECT ON CATALOG example_sales_catalog TO `1aaa1a1a-11a1-1111-1111-1a11111aaa1a`;
GRANT USE CATALOG ON CATALOG example_sales_catalog TO `1aaa1a1a-11a1-1111-1111-1a11111aaa1a`;
GRANT USE SCHEMA ON CATALOG example_sales_catalog TO `1aaa1a1a-11a1-1111-1111-1a11111aaa1a`;
```

For more information on how to grant your service principal Unity Catalog privileges, see the topic for where your Databricks account is hosted:

- **Databricks on AWS**: [Databricks on AWS: Grant a principal Unity Catalog privileges](https://docs.databricks.com/aws/en/external-access/admin#grant-a-principal-unity-catalog-privileges) and [Databricks on AWS: Grant permissions on an object by using SQL](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges?language=SQL#-grant-permissions-on-an-object)
- **Azure Databricks**: [Azure Databricks: Grant a principal Unity Catalog privileges](https://learn.microsoft.com/en-us/azure/databricks/external-access/admin#external-schema) and [Azure Databricks: Grant permissions on an object by using SQL](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/#sql-2)
- **Databricks on Google Cloud**: [Databricks on Google Cloud: Grant a principal Unity Catalog privileges](https://docs.databricks.com/gcp/en/external-access/admin#grant-a-principal-unity-catalog-privileges) and [Databricks on Google Cloud: Grant permissions on an object by using SQL](https://docs.databricks.com/gcp/en/data-governance/unity-catalog/manage-privileges?language=SQL#-grant-permissions-on-an-object)

### Step 5: Create a catalog integration

The following example creates a REST catalog integration that uses OAuth:

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION unity_catalog_int_oauth_vended_credentials
CATALOG_SOURCE = ICEBERG_REST
TABLE_FORMAT = ICEBERG
REST_CONFIG = (
  CATALOG_URI = '<databricks_workspace_url>/api/2.1/unity-catalog/iceberg-rest'
  CATALOG_NAME = '<catalog_name>'
  ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
)
REST_AUTHENTICATION = (
  TYPE = OAUTH
  OAUTH_TOKEN_URI = '<databricks_workspace_url>/oidc/v1/token'
  OAUTH_CLIENT_ID = '<client_id>'
  OAUTH_CLIENT_SECRET = '<oauth_secret>'
  OAUTH_ALLOWED_SCOPES = ('all-apis')
)
ENABLED = TRUE;
```

Where:

- `<databricks_workspace_url>` specifies the URL for your Databricks workspace. To find this URL, see
  [Configure an OAuth catalog integration](#label-tables-iceberg-configure-catalog-integration-rest-unity-oauth-find-workspace-url).

  Here is an example of a Databricks workspace URL for each cloud platform:

  - **Databricks on AWS**: `https://dbc-a1a1a1a1-a1a1.cloud.databricks.com`
  - **Azure Databricks**: `https://adb-1111111111111111.1.azuredatabricks.net`
  - **Databricks on Google Cloud**: `https://1111111111111111.1.gcp.databricks.com`
- `<catalog_name>` specifies the name of your catalog in Unity Catalog that you want to connect Snowflake to. You can find this name in the Databricks workspace
  under **Data** > **Catalogs**.
- `ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS` configures the catalog integration to use vended credentials from Unity Catalog.

  Note

  If you’re creating a catalog integration that uses an external volume, you must exclude the `ACCESS_DELEGATION_MODE` parameter.
- `<client_id>` specifies the OAuth client ID for your Databricks service principal. You copied this value when you
  [added a service principal in Databricks](#label-tables-iceberg-configure-catalog-integration-rest-unity-oauth-add-service-principal).

  Note

  In Databricks, this value is called the *Application ID*, not the Client ID.
- `<oauth_secret>` specifies the OAuth secret for your Databricks service principal. You copied this value when you
  [created an OAuth secret for your service principal](#label-tables-iceberg-configure-catalog-integration-rest-unity-oauth-add-oauth-secret).

### Step 6: Verify your catalog integration

- To verify the configuration for your catalog integration, call the SYSTEM$VERIFY\_CATALOG\_INTEGRATION function.

  For more information, including an example, see [Use SYSTEM$VERIFY\_CATALOG\_INTEGRATION to check your catalog integration configuration](/user-guide/tables-iceberg-configure-catalog-integration-rest-check-config#label-tables-iceberg-rest-catalog-integration-verify-system-function).

### Next steps

After you configure a catalog integration for your catalog in Unity Catalog, use the [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked)
command to create a catalog-linked database by specifying the catalog integration that you created. Snowflake then automatically syncs
with your catalog in Unity Catalog to detect schemas and
Iceberg tables, and registers the remote tables to the catalog-linked database.

When you create your catalog-linked database, you specify the catalog integration.

For example:

Copy code

```
CREATE OR REPLACE DATABASE my_linked_db
   LINKED_CATALOG = (
      CATALOG = 'unity_catalog_int_oauth_vended_credentials'
   );
```

By default, catalog-linked databases support both read and write operations. You can use Snowflake to insert data into, update, and
create Iceberg tables in your catalog in Unity Catalog. For more information, see
[Write support for externally managed Apache Iceberg™ tables](/user-guide/tables-iceberg-externally-managed-writes).

Note

- If you’re using an external volume, you must include the `EXTERNAL_VOLUME` parameter with your CREATE DATABASE statement. For more
  information, see [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked).
- For more information on working with catalog-linked databases, see [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).

## Configure a bearer token catalog integration

### Step 1: Find your Databricks workspace URL

Your Databricks workspace URL is the URL that you use to access your Databricks workspace. You need to find this URL because you specify
it later when you create a catalog integration.

1. Find your Databricks workspace URL.

   For instructions on how to find this URL, see the topic for where your Databricks account is hosted:

   - **Databricks on AWS**: [Databricks on AWS: Workspace instance names, URLs, and IDs](https://docs.databricks.com/aws/workspace/workspace-details#workspace-instance-names-urls-and-ids)
   - **Azure Databricks**: [Azure Databricks: Determine per-workspace URL](https://learn.microsoft.com/azure/databricks/workspace/workspace-details#determine-per-workspace-url)
   - **Databricks on Google Cloud**: [Databricks on Google Cloud: Workspace instance names, URLs, and IDs](https://docs.databricks.com/gcp/workspace/workspace-details#workspace-instance-names-urls-and-ids)
2. Copy your Databricks workspace URL into a text editor.

### Step 2: Add a personal access token (PAT) in Databricks

You need to add a personal access token (PAT) because you must specify it when you create a catalog integration that uses a bearer token
for authentication.

1. To add a PAT in Databricks, see the topic for where your Databricks account is hosted:

   - **Databricks on AWS**: [Databricks on AWS: Authenticate with Databricks personal access tokens (legacy)](https://docs.databricks.com/aws/en/dev-tools/auth/pat)
   - **Azure Databricks**: [Azure Databricks: Authenticate with Azure Databricks personal access tokens (legacy)](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth/pat)
   - **Databricks on Google Cloud**: [Databricks on Google Cloud: Authenticate with Databricks personal access tokens (legacy)](https://docs.databricks.com/gcp/en/dev-tools/auth/pat)
2. Copy the value for your PAT into a text editor and store it securely. You specify this value later when you create a catalog integration in Snowflake.

### Step 3: Enable Snowflake access to your catalog in Unity Catalog

In this step, you use Databricks to enable Snowflake access to your catalog in Unity Catalog.

To enable Snowflake access to your catalog in Unity Catalog through vended credentials, first, at the metastore level, you must enable
external data access on the metastore. Next, you need to grant your Databricks user Unity Catalog privileges to your catalog, which your PAT
inherits.

#### Enable external data access on the metastore (vended credentials only)

If you’re creating a catalog integration that uses vended credentials, you must enable external data access on the metastore in Databricks.
If you’re creating a catalog integration that uses an external volume, you can skip this step.

For instructions on how to enable external data access on the metastore, see the topic for where your Databricks account is hosted:

- **Databricks on AWS**: [Databricks on AWS: Enable external data access on the metastore](https://docs.databricks.com/aws/en/external-access/admin#enable-external-data-access-on-the-metastore)
- **Azure Databricks**: [Azure Databricks: Enable external data access on the metastore](https://learn.microsoft.com/en-us/azure/databricks/external-access/admin#enable-external-data-access-on-the-metastore)
- **Databricks on Google Cloud**: [Databricks on Google Cloud: Enable external data access on the metastore](https://docs.databricks.com/gcp/en/external-access/admin#enable-external-data-access-on-the-metastore)

#### Grant your Databricks user access to your catalog

Next, you must grant your Databricks user Unity Catalog privileges. You need to grant these privileges to your Databricks user to allow
Snowflake access to the catalog based on the privileges that you specify. When you use a PAT for authentication, it inherits all the
privileges granted on the Databricks user who created the PAT.

##### Privileges for full functionality

To enable full functionality in Snowflake, you must grant the following privileges:

Note

If you want to restrict Snowflake access, see [Unity Catalog privileges and securable objects](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/privileges)
in the Databricks documentation.

| Privilege | Description |
| --- | --- |
| `ALL PRIVILEGES` | Grants all privileges on the catalog, including the ability to create tables. Required together with `EXTERNAL USE SCHEMA` to enable creating tables from Snowflake. |
| `EXTERNAL USE SCHEMA` | Allows Unity Catalog to generate and provide temporary, scoped credentials to Snowflake for accessing table data in cloud storage. Note This privilege is only required when you create a catalog integration that uses vended credentials; it’s not required when you create a catalog integration that uses an external volume, so if you’re using an external volume, remove it from the example code block. |
| `MODIFY` | Allows Snowflake to add, update, and delete data in a table. |
| `SELECT` | Allows Snowflake to query tables and access table metadata. Required for all operations in Snowflake, including reading data and discovering tables in the catalog-linked database. |
| `USE CATALOG` | Allows Snowflake to access the catalog. Required to connect to and interact with any objects in the Unity Catalog. |
| `USE SCHEMA` | Allows Snowflake access to schemas (namespaces) within the catalog. Required to view and work with tables in specific schemas. |

Expand

Show lessSee more

##### Grant privileges

You can grant privileges by using Catalog Explorer or SQL.

Catalog ExplorerSQL

To grant permissions by using the Databricks Catalog Explorer, see the topic for where your Databricks account is hosted:

- **Databricks on AWS**: [Databricks on AWS: Grant permissions on an object](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges#-grant-permissions-on-an-object)
- **Azure Databricks**: [Azure Databricks: Grant permissions on an object](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges#-grant-permissions-on-an-object)
- **Databricks on Google Cloud**: [Databricks on Google Cloud: Grant permissions on an object](https://docs.databricks.com/gcp/en/data-governance/unity-catalog/manage-privileges#-grant-permissions-on-an-object)

To grant your Databricks user Unity Catalog privileges, you must specify the user ID for that Databricks user.

For example, the following statement grants `example_sales_catalog` catalog privileges to the `j.smith@example.com` Databricks user.

Copy code

```
GRANT EXTERNAL USE SCHEMA ON CATALOG example_sales_catalog TO `j.smith@example.com`;
GRANT MODIFY ON CATALOG example_sales_catalog TO `j.smith@example.com`;
GRANT SELECT ON CATALOG example_sales_catalog TO `j.smith@example.com`;
GRANT USE CATALOG ON CATALOG example_sales_catalog TO `j.smith@example.com`;
GRANT USE SCHEMA ON CATALOG example_sales_catalog TO `j.smith@example.com`;
```

For more information on how to grant your Databricks user Unity Catalog privileges, see the topic for where your Databricks account is hosted:

- **Databricks on AWS**: [Databricks on AWS: Grant a principal Unity Catalog privileges](https://docs.databricks.com/aws/en/external-access/admin#grant-a-principal-unity-catalog-privileges) and [Databricks on AWS: Grant permissions on an object by using SQL](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges?language=SQL#-grant-permissions-on-an-object)
- **Azure Databricks**: [Azure Databricks: Grant a principal Unity Catalog privileges](https://learn.microsoft.com/en-us/azure/databricks/external-access/admin#external-schema) and [Azure Databricks: Grant permissions on an object by using SQL](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/#sql-2)
- **Databricks on Google Cloud**: [Databricks on Google Cloud: Grant a principal Unity Catalog privileges](https://docs.databricks.com/gcp/en/external-access/admin#grant-a-principal-unity-catalog-privileges) and [Databricks on Google Cloud: Grant permissions on an object by using SQL](https://docs.databricks.com/gcp/en/data-governance/unity-catalog/manage-privileges?language=SQL#-grant-permissions-on-an-object)

### Step 4: Create a catalog integration

The following example creates a REST catalog integration that uses a bearer token with vended credentials:

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION unity_catalog_int_bearer_vended_credentials
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = '<databricks_workspace_url>/api/2.1/unity-catalog/iceberg-rest'
    CATALOG_NAME = '<catalog_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = BEARER
    BEARER_TOKEN = '<personal_access_token>'
  )
  ENABLED = TRUE;
```

Where:

- `<databricks_workspace_url>` specifies the URL for your Databricks workspace. To find this URL, see
  [Configure a bearer token catalog integration](#label-tables-iceberg-configure-catalog-integration-rest-unity-bearer-find-workspace-url).

  Here is an example of a Databricks workspace URL for each cloud platform:

  - **Databricks on AWS**: `https://dbc-a1a1a1a1-a1a1.cloud.databricks.com`
  - **Azure Databricks**: `https://adb-1111111111111111.1.azuredatabricks.net`
  - **Databricks on Google Cloud**: `https://1111111111111111.1.gcp.databricks.com`
- `<catalog_name>` specifies the name of your catalog in Unity Catalog that you want to connect Snowflake to. You can find this name in the Databricks workspace
  under **Data** > **Catalogs**.
- `ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS` configures the catalog integration to use vended credentials from Unity Catalog.

  Note

  If you’re creating a catalog integration that uses an external volume, you must exclude the `ACCESS_DELEGATION_MODE` parameter.
- `<personal_access_token>` specifies your Databricks personal access token (PAT). An example of a PAT is `aaaa111aaaa111a1a1a1a111111a111a1111`.

### Step 5: Verify your catalog integration

- To verify the configuration for your catalog integration, call the SYSTEM$VERIFY\_CATALOG\_INTEGRATION function.

  For more information, see [Use SYSTEM$VERIFY\_CATALOG\_INTEGRATION to check your catalog integration configuration](/user-guide/tables-iceberg-configure-catalog-integration-rest-check-config#label-tables-iceberg-rest-catalog-integration-verify-system-function).

### Next steps

After you configure a catalog integration for your catalog in Unity Catalog, use the [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked)
command to create a catalog-linked database by specifying the catalog integration that you created. Snowflake then automatically syncs
with your catalog in Unity Catalog to detect schemas and
Iceberg tables, and registers the remote tables to the catalog-linked database.

When you create your catalog-linked database, you specify the catalog integration.

For example:

Copy code

```
CREATE OR REPLACE DATABASE my_linked_db
   LINKED_CATALOG = (
      CATALOG = 'unity_catalog_int_bearer_vended_credentials'
   );
```

By default, catalog-linked databases support both read and write operations. You can use Snowflake to insert data into, update, and
create Iceberg tables in your catalog in Unity Catalog. For more information, see
[Write support for externally managed Apache Iceberg™ tables](/user-guide/tables-iceberg-externally-managed-writes).

Note

- If you’re using an external volume, you must include the `EXTERNAL_VOLUME` parameter with your CREATE DATABASE statement. For more
  information, see [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked).
- For more information on working with catalog-linked databases, see [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).
