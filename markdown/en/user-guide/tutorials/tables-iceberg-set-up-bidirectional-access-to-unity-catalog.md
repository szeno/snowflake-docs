# Tutorial: Set up bidirectional access to Apache Iceberg™ tables in Databricks Unity Catalog

## Introduction

This tutorial covers how to connect Snowflake to a catalog in Databricks Unity Catalog by using a writable
catalog-linked database with catalog-vended credentials. This setup enables bidirectional data collaboration between Snowflake and
Databricks.

A [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database) is a Snowflake database connected to an external
Iceberg REST catalog, such as a catalog in Unity Catalog. Snowflake automatically syncs with the external catalog to detect namespaces
and Iceberg tables, and registers the remote tables to the catalog-linked database. When a catalog-linked database is writable, it also
supports creating and dropping schemas or Iceberg tables.

[Catalog-vended credentials for Iceberg tables](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials) let you
give Snowflake access to your table data and metadata in cloud storage without using an external volume. When you connect Snowflake to a
catalog in Unity Catalog by using catalog-vended credentials, Unity
Catalog provides temporary credentials to Snowflake for accessing your table data in cloud storage.

With this setup, you can perform the following tasks:

- Use Snowflake to query Iceberg tables that are managed by Unity Catalog.
- Use Snowflake to insert data into Iceberg tables that are managed by Unity Catalog.
- Use Snowflake to create Iceberg tables that are managed by Unity Catalog.
- Use Databricks to work with Unity Catalog-managed Iceberg tables that you created or modified from Snowflake.

To complete the steps in this tutorial for working with Snowflake, use a worksheet in Snowsight or use a Snowflake client such
as [SnowSQL](/user-guide/snowsql).
You can copy and paste the code examples, and then run them. To complete the steps in this tutorial for working with Databricks,
use your Databricks workspace to copy and paste the code examples or follow the instructions in the linked Databricks documentation.

### What you’ll learn

In this tutorial, you’ll learn how to do the following:

- Create a catalog in Unity Catalog.
- Configure authentication credentials for Snowflake to use by adding a service principal and OAuth secret in Databricks.
- Use Databricks to enable Snowflake access to your catalog in Unity Catalog.
- Create a catalog integration in Snowflake that uses vended credentials to connect Snowflake to your catalog in Unity Catalog.
- Create a writable catalog-linked database in Snowflake that syncs with your catalog in Unity Catalog and allows you to write
  to your catalog in Unity Catalog from Snowflake.
- Work with Unity Catalog-managed Iceberg tables from Snowflake, which includes querying and inserting data into these tables and
  creating a Unity Catalog-managed Iceberg table from Snowflake.
- Work with Unity Catalog-managed Iceberg tables from Databricks.

### Prerequisites

Before you start, you should be familiar with the following concepts:

- Snowflake [object identifiers](/sql-reference/identifiers) and their requirements.
- Apache Iceberg and Iceberg tables in Snowflake. For more information, see [Apache Iceberg™ tables](/user-guide/tables-iceberg).
- Databricks Unity Catalog. For more information, see
  [What is Unity Catalog?](https://docs.databricks.com/aws/data-governance/unity-catalog)
  in the Databricks documentation.

You need:

**Databricks**

- A Databricks account hosted on AWS, Azure, or Google Cloud.
- A Databricks workspace with Unity Catalog enabled.

  For instructions on how to enable a workspace for Unity Catalog, see the topic for where your Databricks account is hosted:

  - **Databricks on AWS**: [Databricks on AWS: Enable a workspace for Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/enable-workspaces)
  - **Azure Databricks**: [Azure Databricks: Enable a workspace for Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/enable-workspaces)
  - **Databricks on Google Cloud**: [Databricks on Google Cloud: Enable a workspace for Unity Catalog](https://docs.databricks.com/gcp/en/data-governance/unity-catalog/enable-workspaces)
- Required access:

  - Metastore admin privilege or the CREATE CATALOG privilege on the metastore to create a catalog in Unity Catalog.

    Note

    In this tutorial, you’ll create a catalog in Unity Catalog, which makes you an owner of the catalog. As a catalog owner, you can
    grant a Databricks service principal privileges to your catalog, which you’ll do in this tutorial.
  - Account admin or workspace admin privilege to your Databricks workspace to create a service principal and OAuth secret
  - Metastore admin privilege to enable external data access on the metastore

**Snowflake**

- A Snowflake user with a role that has the privileges to perform the following actions:

  - [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest#label-create-catalog-integration-rest-access-control-requirement)
  - [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked#label-create-catalog-linked-database-access-control-requirements)
  - [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table-rest#label-create-catalog-table-rest-access-control-requirements)
  - [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse#label-create-warehouse-access-control-requirements)

  If using a 30-day trial account, you can log in as the user that was created for the account.
  This user has the role with the privileges needed to create the objects.

  If you don’t have a user with the necessary permissions, ask someone who does to create one for you.
  Users with the ACCOUNTADMIN role can create new users and grant them the required privileges.

## Step 1: Create a catalog in Databricks Unity Catalog

In Databricks, run the following statements to create an `example_sales_catalog` catalog in Unity Catalog with the following objects:

- A `customers` schema
- A `customer_accounts` table with some sample data, which is nested under the `customers` schema

Copy code

```
CREATE CATALOG example_sales_catalog;

CREATE SCHEMA example_sales_catalog.customers;

CREATE TABLE example_sales_catalog.customers.customer_accounts (
  customer_account_id INT,
  customer_id INT,
  account_status STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
) USING ICEBERG;

INSERT INTO example_sales_catalog.customers.customer_accounts VALUES
  (1, 1001, 'Active', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  (2, 1002, 'Active', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  (3, 1003, 'Inactive', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  (4, 1004, 'Active', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  (5, 1005, 'Pending', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());
```

## Step 2: Add a service principal in Databricks

In this step, you’ll add a service principal in Databricks.

To allow Snowflake to authenticate with Unity Catalog, you need to add a service principal
in Databricks and then create an OAuth secret for your service principal in Databricks.

### Add a service principal in Databricks

1. To add a service principal, see the topic for where your Databricks account is hosted:

   - **Databricks on AWS**: [Databricks on AWS: Add service principals to your account](https://docs.databricks.com/aws/admin/users-groups/manage-service-principals?language=Account%C2%A0console#-add-service-principals-to-your-account)
   - **Azure Databricks**: [Azure Databricks: Add service principals to your account](https://learn.microsoft.com/azure/databricks/admin/users-groups/manage-service-principals#-add-service-principals-to-your-account)
   - **Databricks on Google Cloud**: [Databricks on Google Cloud: Add service principals to your account](https://docs.databricks.com/gcp/admin/users-groups/manage-service-principals#-add-service-principals-to-your-account)
2. Copy the *Application ID* value for your service principal into a text editor and store it securely. You specify this value later
   when you create a catalog integration in Snowflake.

### Create an OAuth secret for your service principal

1. To create an OAuth secret for your service principal, see the topic for where your Databricks account is hosted:

   - **Databricks on AWS**: [Databricks on AWS: Create an OAuth secret](https://docs.databricks.com/aws/dev-tools/auth/oauth-m2m#-step-1-create-an-oauth-secret)
   - **Azure Databricks**: [Azure Databricks: Create an OAuth secret](https://learn.microsoft.com/azure/databricks/dev-tools/auth/oauth-m2m#-step-1-create-an-oauth-secret)
   - **Databricks on Google Cloud**: [Databricks on Google Cloud: Create an OAuth secret](https://docs.databricks.com/gcp/dev-tools/auth/oauth-m2m#-step-1-create-an-oauth-secret)
2. Copy the *Secret* value that you generated into a text editor and store it securely. You specify this value later when you create a
   catalog integration in Snowflake.

   Important

   The client secret is only displayed once. Make sure to copy it before closing the dialog.

In the next step, you’ll grant privileges to the service principal that you created, which enables Snowflake access to your
`example_sales_catalog` catalog in Unity Catalog.

## Step 3: Enable Snowflake access to Unity Catalog

In this step, you use Databricks to enable Snowflake access to your catalog in Unity Catalog.

To enable Snowflake access to your catalog in Unity Catalog through vended credentials, first, at the metastore level, you must enable
external data access on the metastore. Next, you need to grant your service principal Unity Catalog
privileges to your catalog.

### Enable external data access on the metastore

First, enable external data access on the metastore.

For instructions on how to enable external data access on the metastore, see the topic for where your Databricks account is hosted:

- **Databricks on AWS**: [Databricks on AWS: Enable external data access on the metastore](https://docs.databricks.com/aws/en/external-access/admin#enable-external-data-access-on-the-metastore)
- **Azure Databricks**: [Azure Databricks: Enable external data access on the metastore](https://learn.microsoft.com/en-us/azure/databricks/external-access/admin#enable-external-data-access-on-the-metastore)
- **Databricks on Google Cloud**: [Databricks on Google Cloud: Enable external data access on the metastore](https://docs.databricks.com/gcp/en/external-access/admin#enable-external-data-access-on-the-metastore)

### Grant your service principal access to your catalog

Next, you must grant your service principal Unity Catalog privileges. You need to grant
these privileges to your service principal to allow Snowflake access to the catalog based on the privileges that you specify.

Catalog ExplorerSQL

Use the Catalog Explorer to select the `example_sales_catalog` catalog and then grant the following privileges to your service
principal at the catalog level:

- `CREATE TABLE`
- `EXTERNAL USE SCHEMA`
- `MODIFY`
- `SELECT`
- `USE CATALOG`
- `USE SCHEMA`

To grant permissions by using the Databricks Catalog Explorer, see the topic for where your Databricks account is hosted:

- **Databricks on AWS**: [Databricks on AWS: Grant permissions on an object](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges#-grant-permissions-on-an-object)
- **Azure Databricks**: [Azure Databricks: Grant permissions on an object](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges#-grant-permissions-on-an-object)
- **Databricks on Google Cloud**: [Databricks on Google Cloud: Grant permissions on an object](https://docs.databricks.com/gcp/en/data-governance/unity-catalog/manage-privileges#-grant-permissions-on-an-object)

Important

In the **Principals** field, you must enter the name of your service principal, not the email address for a user or the
name of a group.

Run the following statements to grant your service principal the privileges needed to complete this tutorial. See
for a description of each privilege.

Copy code

```
GRANT CREATE TABLE ON CATALOG example_sales_catalog TO `<application_id>`;
GRANT EXTERNAL USE SCHEMA ON CATALOG example_sales_catalog TO `<application_id>`;
GRANT MODIFY ON CATALOG example_sales_catalog TO `<application_id>`;
GRANT SELECT ON CATALOG example_sales_catalog TO `<application_id>`;
GRANT USE CATALOG ON CATALOG example_sales_catalog TO `<application_id>`;
GRANT USE SCHEMA ON CATALOG example_sales_catalog TO `<application_id>`;
```

Where:

- `<application_id>` is the *Application ID* for your service principal, which you copied in a previous step.
  `1aaa1a1a-11a1-1111-1111-1a11111aaa1a` is an example of an Application ID for a service principal.

#### Description of the privileges

The following table describes each Unity Catalog privilege that you granted to your service principal and what access each privilege
gives Snowflake:

| Privilege | Description |
| --- | --- |
| `CREATE TABLE` | Allows Snowflake to create new Iceberg tables in the catalog. Required to create Unity Catalog-managed Iceberg tables from Snowflake. |
| `EXTERNAL USE SCHEMA` | Allows Unity Catalog to generate and provide temporary, scoped credentials to Snowflake for accessing table data in cloud storage. Important This privilege is required when you use vended credentials with a catalog-linked database. |
| `MODIFY` | Allows Snowflake to insert, update, or delete data in existing tables. Required to write data to Unity Catalog-managed Iceberg tables from Snowflake. |
| `SELECT` | Allows Snowflake to query tables and access table metadata. Required for all operations in Snowflake, including reading data and discovering tables in the catalog-linked database. |
| `USE CATALOG` | Allows Snowflake to access the catalog. Required to connect to and interact with any objects in the Unity Catalog. |
| `USE SCHEMA` | Allows Snowflake access to schemas (namespaces) within the catalog. Required to view and work with tables in specific schemas. |

Expand

Show lessSee more

## Step 4: Gather your Databricks workspace information

In this step, you use Databricks to gather information about your workspace. You need this information to specify it later when you create
a catalog integration in Snowflake.

Gather the following information from your Databricks workspace:

1. **Databricks workspace URL**: This is the URL you use to access your Databricks workspace.

   For instructions on how to find this URL, see the topic for where your Databricks account is hosted:

   - **Databricks on AWS**: [Databricks on AWS: Workspace instance names, URLs, and IDs](https://docs.databricks.com/aws/workspace/workspace-details#workspace-instance-names-urls-and-ids)
   - **Azure Databricks**: [Azure Databricks: Determine per-workspace URL](https://learn.microsoft.com/azure/databricks/workspace/workspace-details#determine-per-workspace-url)
   - **Databricks on Google Cloud**: [Databricks on Google Cloud: Workspace instance names, URLs, and IDs](https://docs.databricks.com/gcp/workspace/workspace-details#workspace-instance-names-urls-and-ids)

   Here is an example of a Databricks workspace URL for each cloud platform:

   - **Databricks on AWS**: `https://dbc-a1a1a1a1-a1a1.cloud.databricks.com`
   - **Azure Databricks**: `https://adb-1111111111111111.1.azuredatabricks.net`
   - **Databricks on Google Cloud**: `https://1111111111111111.1.gcp.databricks.com`
2. **Catalog name in Unity Catalog**: The name of the catalog in Unity Catalog that you want to access from Snowflake,
   which is `example_sales_catalog`.
3. **Application ID**: The Application ID for the service principal that you added in Databricks.
4. **OAuth secret**: The OAuth secret for the service principal that you added in Databricks.

Copy these values into a text editor. You’ll use them when you create a catalog integration in Snowflake.

## Step 5: Set up a warehouse and catalog integration in Snowflake

In Snowflake, set up your environment by creating a warehouse and catalog integration for this tutorial.

### Create a warehouse

Run the following statements to create a warehouse.

Copy code

```
CREATE WAREHOUSE catalog_linked_database_tutorial_wh
  WAREHOUSE_TYPE = STANDARD
  WAREHOUSE_SIZE = XSMALL;

USE WAREHOUSE catalog_linked_database_tutorial_wh;
```

### Create a catalog integration

In Snowflake, create a catalog integration that connects Snowflake to your `example_sales_catalog` catalog in Unity Catalog
by using OAuth authentication and vended credentials.

To create a catalog integration for the Databricks Unity Catalog, use
the [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest) command.

The following example creates a REST catalog integration for connecting to your `example_sales_catalog` catalog by using OAuth:

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION my_unity_catalog_int_vended_creds
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = '<databricks_workspace_url>/api/2.1/unity-catalog/iceberg-rest'
    CATALOG_NAME = 'example_sales_catalog'
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

- `<databricks_workspace_url>` is your Databricks workspace URL, which you found in the previous step.
- `example_sales_catalog` is the name of your catalog in Unity Catalog that you want to connect to.
- `<client_id>` is the OAuth client ID for the service principal that you created in Databricks.

  Important

  In Databricks, this value is called the *Application ID*, not Client ID.
- `<oauth_secret>` is the OAuth secret that you generated for the service principal that you created in Databricks.

### Verify your catalog integration

- To verify the configuration for your catalog integration, call the SYSTEM$VERIFY\_CATALOG\_INTEGRATION function.

  For more information, including an example, see [Use SYSTEM$VERIFY\_CATALOG\_INTEGRATION to check your catalog integration configuration](/user-guide/tables-iceberg-configure-catalog-integration-rest-check-config#label-tables-iceberg-rest-catalog-integration-verify-system-function).

Next, you’ll specify the catalog integration that you created when you create a catalog-linked database that discovers and syncs with your
`example_sales_catalog` catalog in Unity Catalog.

## Step 6: Create a catalog-linked database

In this step, you create a catalog-linked database that connects to your `example_sales_catalog` catalog in Unity Catalog by using the catalog
integration you created in the previous step.

To create a catalog-linked database, use the [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked) command.

The following example creates a catalog-linked database that is writable, uses vended credentials, and specifies one blocked namespace.

Copy code

```
CREATE DATABASE unity_linked_db
  LINKED_CATALOG = (
    CATALOG = 'my_unity_catalog_int_vended_creds'
    BLOCKED_NAMESPACES = ('information_schema')
  );
```

Where:

- `my_unity_catalog_int_vended_creds` is the name of the catalog integration that you created in the previous step.

Note

- You don’t need to specify the `ALLOWED_WRITE_OPERATIONS` parameter to create a catalog-linked database that is writable.
  The reason is that the default for this parameter is `ALL`, which means that your catalog-linked database is writable.
- `BLOCKED_NAMESPACES = ('information_schema')` prevents Snowflake from syncing with the `information_schema` schema in
  your Unity Catalog. Otherwise, this schema returns irrelevant SQL execution errors when you check the catalog sync status later.
  These errors are irrelevant because the tables nested under this schema aren’t compatible with Iceberg.

  The tables and views nested under the `information_schema` schema are built-in Databricks tables and views; they aren’t Iceberg tables.
- The example code configures your catalog-linked database with vended credentials, so you don’t need to specify an external volume.
- The default for the `ALLOWED_WRITE_OPERATIONS` parameter is `ALL`, which means that your catalog-linked database supports read
  and write operations.

Now that you’ve created a catalog-linked database, Snowflake automatically syncs with your Unity Catalog
to discover namespaces and Iceberg tables. The default sync interval is 30 seconds.

## Step 7: Check the catalog sync status

To verify that Snowflake has successfully linked your catalog in Unity Catalog to your database,
use the [SYSTEM$CATALOG\_LINK\_STATUS](/sql-reference/functions/system_catalog_link_status) function:

Copy code

```
SELECT SYSTEM$CATALOG_LINK_STATUS('unity_linked_db');
```

The function returns information about the sync status, including any tables that failed to sync.

If the sync is successful, you should see your Unity Catalog namespaces appear as schemas
in the catalog-linked database, and Iceberg tables appear under their respective schemas.

Note

To identify tables that Snowflake created but couldn’t initialize, use the
[SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) command. For more information, see [Identify tables that were created but couldn’t be initialized](/user-guide/tables-iceberg-catalog-linked-database#label-catalog-linked-db-identify-tables-not-initialized).

## Step 8: Work with Iceberg tables

After the catalog sync completes, you can query and insert data into your Unity Catalog-managed Iceberg tables
directly from Snowflake and create a Unity Catalog-managed Iceberg table from Snowflake.

You can then use Databricks to work with the tables that you created or modified from Snowflake.

### Query Iceberg tables from Snowflake

To query a Unity Catalog-managed Iceberg table, follow these steps:

1. Select your catalog-linked database.

   Copy code

   ```
   USE DATABASE unity_linked_db;
   ```
2. Query a table in your catalog in Unity Catalog.

   The following example queries the `customer_accounts` table, which is nested under the top-level `customers` schema
   in the `example_sales_catalog` catalog in Unity Catalog.

   Copy code

   ```
   SELECT * FROM customers.customer_accounts
     LIMIT 20;
   ```

Note

For requirements about identifying objects in a catalog-linked database,
see [Requirements for identifier resolution in a catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database#label-catalog-linked-identifier-requirements).

### Insert data into Iceberg tables from Snowflake

With a catalog-linked database, you can use Snowflake to insert data into your Unity Catalog-managed Iceberg tables.

To insert data into a Unity Catalog-managed Iceberg table from Snowflake, follow these steps:

1. Select your catalog-linked database.

   Copy code

   ```
   USE DATABASE unity_linked_db;
   ```
2. Insert data into the `customer_accounts` table.

   Copy code

   ```
   INSERT INTO customers.customer_accounts (
     customer_account_id,
     customer_id,
     account_status,
     created_at,
     updated_at
   )
     VALUES
    (6, 1006, 'ACTIVE', '2025-12-15 10:23:45', '2025-12-15 10:23:45');
   ```

### Create a new Iceberg table from Snowflake

With a catalog-linked database, you can also use Snowflake to create a Unity Catalog-managed Iceberg table.

To create a Unity Catalog-managed Iceberg table from Snowflake, follow these steps:

1. Select your catalog-linked database.

   Copy code

   ```
   USE DATABASE unity_linked_db;
   ```
2. Select the schema in your catalog in Unity Catalog where you want to create an Iceberg table.

   Copy code

   ```
   USE SCHEMA customers;
   ```
3. Create an Iceberg table.

   Copy code

   ```
   CREATE ICEBERG TABLE table_created_from_snowflake (
     id INT,
     name STRING,
     created_date DATE
   );
   ```

   When you create a table in a catalog-linked database, Snowflake creates the table both in
   Snowflake and in your catalog in Unity Catalog. As you update the table by using either Snowflake or Databricks,
   Snowflake keeps both table instances in sync.

### Drop an Iceberg table from Snowflake

Because your catalog-linked database is writable, you can use the [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) command to
drop an Iceberg table from Snowflake. To drop a table from Snowflake, your Databricks service principal must be granted the MANAGE
privilege.

Warning

When your catalog-linked database has write permissions enabled, Snowflake propagates table drops to the remote catalog, which removes
the table and data from both systems.

### Work with Iceberg tables from Databricks

In Databricks, try the following tasks:

- Insert data into the `table_created_from_snowflake` Iceberg table that you created from Snowflake.

  Copy code

  ```
  USE CATALOG example_sales_catalog;
  USE SCHEMA customers;
  INSERT INTO table_created_from_snowflake VALUES
    (1, 'John', CURRENT_TIMESTAMP());
  ```

  Note

  If you receive a PERMISSION\_DENIED error, you might need to first grant the MODIFY and SELECT privileges for the table to your Databricks user.
- Query the `customer_accounts` table to view the data that you inserted from Snowflake.

  Copy code

  ```
  USE CATALOG example_sales_catalog;
  USE SCHEMA customers;
  SELECT * FROM customer_accounts;
  ```

### Automated refresh for your Iceberg tables

[Automated refresh](/user-guide/tables-iceberg-auto-refresh) is enabled by default for Iceberg tables in your catalog-linked database.
As a result, when you update your Iceberg table from Databricks, the corresponding Iceberg table in Snowflake is automatically refreshed
with the updates.

To check the automated refresh status for your Unity Catalog-managed Iceberg tables, use the [SYSTEM$AUTO\_REFRESH\_STATUS](/sql-reference/functions/system_auto_refresh_status)
system function in Snowflake.

## Clean up

### Clean up in Snowflake

To delete the objects that you created for this tutorial, run the following DROP statements.

Replace the following values:

- `my_other_database` with the name of a database to use so that you can drop the one that you created for this tutorial.
- `my_other_warehouse` with the name of a warehouse to use so that you can drop the one that you created for this tutorial.

Copy code

```
USE DATABASE <my_other_database>;
DROP DATABASE unity_linked_db;
DROP CATALOG INTEGRATION my_unity_catalog_int_vended_creds;
USE WAREHOUSE <my_other_warehouse>;
DROP WAREHOUSE catalog_linked_database_tutorial_wh;
```

### Clean up in Databricks

1. Drop the `example_sales_catalog` catalog.

   Copy code

   ```
   DROP CATALOG example_sales_catalog cascade;
   ```
2. Remove your service principal.

   For instructions, see the topic for where your Databricks account is hosted:

   - **Databricks on AWS**: [Databricks on AWS: Manage service principals](https://docs.databricks.com/aws/en/admin/users-groups/manage-service-principals)
   - **Azure Databricks**: [Azure Databricks: Manage service principals](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-service-principals)
   - **Databricks on Google Cloud**: [Databricks on Google Cloud: Manage service principals](https://docs.databricks.com/gcp/en/admin/users-groups/manage-service-principals)

## Summary and additional resources

In this tutorial, you followed an end-to-end workflow to set up bidirectional access to Unity Catalog
by using a catalog-linked database with vended credentials.

Along the way, you completed the following tasks:

- **Created a catalog in Unity Catalog** with a Unity Catalog-managed Iceberg table.
- **Created OAuth credentials in Databricks** for Snowflake to authenticate with Unity Catalog by adding a service principal and OAuth secret.
- **Enabled Snowflake access to your catalog in Unity Catalog**, which
  included granting your service principal with Unity Catalog privileges.

  In the tutorial, we granted privileges at the catalog level. However, for more granular control, you can grant privileges at the schema
  or table level.

  Here’s an example of granting privileges at the schema level:

  Copy code

  ```
  GRANT CREATE TABLE ON SCHEMA example_sales_catalog.customers TO `<application_id>`;
  GRANT EXTERNAL USE SCHEMA ON SCHEMA example_sales_catalog.customers TO `<application_id>`;
  GRANT MODIFY ON SCHEMA example_sales_catalog.customers TO `<application_id>`;
  GRANT SELECT ON SCHEMA example_sales_catalog.customers TO `<application_id>`;
  GRANT USE CATALOG ON CATALOG example_sales_catalog TO `<application_id>`;
  GRANT USE SCHEMA ON SCHEMA example_sales_catalog.customers TO `<application_id>`;
  ```

  For more information about service principals and OAuth in Databricks, see
  [Authentication using OAuth tokens for service principals](https://docs.databricks.com/aws/dev-tools/authentication-oauth)
  in the Databricks documentation. For more information about Unity Catalog privileges, see [Manage privileges in Unity Catalog](https://docs.databricks.com/aws/data-governance/unity-catalog/manage-privileges).
- **Created an OAuth catalog integration with vended credentials** to connect Snowflake to your catalog in Unity Catalog.
  For more information about vended credentials in Snowflake, see [Use catalog-vended credentials for Apache Iceberg™ tables](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials).

  Note

  Alternatively, you can create a bearer catalog integration. For instructions, see [Configure a bearer token catalog integration](/user-guide/tables-iceberg-configure-catalog-integration-rest-unity#label-tables-iceberg-configure-catalog-integration-rest-unity-bearer).
  With a bearer catalog integration, you specify a personal access token (PAT) in the catalog integration for authentication. For more information
  about PATs in Databricks, see [Authenticate with Databricks personal access tokens (legacy)](https://docs.databricks.com/aws/en/dev-tools/auth/pat)
  in the Databricks documentation.
- **Created a catalog-linked database** that automatically syncs with your catalog in Unity Catalog.
  For more information about using catalog-linked databases, see [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).

  In the tutorial, you blocked a set of namespaces from your catalog-linked databases by using the BLOCKED\_NAMESPACES parameter.
  Alternatively, to instead limit automatic table discovery to a specific set of namespaces, use the ALLOWED\_NAMESPACES parameter
  when you create or modify a catalog-linked database.

  In the tutorial, you used the default sync interval that Snowflake uses to automatically discover schemas and tables in your remote catalog,
  which is 30 seconds. However, you can change this interval by using the SYNC\_INTERVAL\_SECONDS parameter when you create or modify your catalog-linked
  database. For example, you might want to decrease the sync interval to prevent rate limit issues.

  For more information, see the following topics:

  - [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked)
  - [ALTER DATABASE (catalog-linked)](/sql-reference/sql/alter-database-catalog-linked)
- **Worked with Unity Catalog-managed Iceberg tables** by using Snowflake and Databricks.

  In the tutorial, in Snowflake, you used an INSERT INTO statement to insert data into the `customer_accounts` table from Snowflake.

  However, you have other options for inserting data into Unity Catalog-managed Iceberg tables from Snowflake. For example, you can use
  an INSERT INTO … SELECT FROM command. For more information about write support for externally managed Iceberg tables,
  see [Write support for externally managed Apache Iceberg™ tables](/user-guide/tables-iceberg-externally-managed-writes), including [Writing to externally managed Iceberg tables](/user-guide/tables-iceberg-externally-managed-writes#label-tables-iceberg-externally-managed-write-operations).

To learn more about Iceberg tables for Snowflake, see the [Iceberg tables documentation](/user-guide/tables-iceberg).
