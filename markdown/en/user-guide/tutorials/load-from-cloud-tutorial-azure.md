# Load data from cloud storage: Microsoft Azure

## Introduction

This tutorial shows you how to load data from Microsoft Azure cloud storage into
Snowflake using SQL. You can access a pre-loaded [Snowsight template](/user-guide/ui-snowsight/snowsight-templates)
worksheet to complete these tasks.

Note

Snowflake bills a minimal amount for the on-disk storage used for any sample data in
this tutorial. The tutorial provides steps to drop objects and minimize storage
cost. Snowflake requires a [virtual warehouse](/user-guide/warehouses) to load the
data and execute queries. A running virtual warehouse consumes Snowflake credits.

If you are using a [30-day trial account](https://signup.snowflake.com/),
which provides free credits, you won’t incur any costs.

### What you will learn

In this tutorial you will learn how to:

- Use a role that has the privileges to create and use the Snowflake objects required by this tutorial.
- Use a warehouse to access resources.
- Select a database and schema to use for the session.
- Create a table.
- Create a storage integration for your cloud platform.
- Create a stage for your storage integration.
- Load data into the table from the stage.
- Query the data in the table.

## Prerequisites

This tutorial assumes the following:

- You have a [supported browser](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-supported-browsers).
- You have access to a Snowflake account and can log in as a user who has been granted the
  ACCOUNTADMIN system role. For more information, see
  [system-defined roles](/user-guide/security-access-control-overview#label-access-control-overview-roles-system).

  If you don’t have an account, you can sign up for a [free trial](https://signup.snowflake.com/)
  and choose any [Snowflake Cloud Region](/user-guide/intro-regions).
- You have a Microsoft Azure account that you can use to bulk load data from Microsoft Azure. See
  [Bulk loading from Microsoft Azure](/user-guide/data-load-azure).

# Step 1. Sign in using Snowsight

To access Snowsight over the public Internet, do the following:

1. In a supported web browser, navigate to <https://app.snowflake.com>.
2. Provide your [account identifier](/user-guide/admin-account-identifier) or account URL.
   If you’ve previously signed in to Snowsight, you might see an account name that you can select.
3. Sign in using your Snowflake account credentials.

## Step 2. Open the SQL worksheet for loading data from Microsoft Azure

You can use worksheets to write and run SQL commands on your database. You can access a
pre-loaded template worksheet for this tutorial. The worksheet has the SQL
commands that you will run to create database objects, load data, and query the
data. Because it is a template worksheet, you will be invited to enter your own values
for certain SQL parameters. For more information about worksheets,
see [Getting started with worksheets](/user-guide/ui-snowsight-worksheets-gs).

The worksheet for this tutorial is not pre-loaded into the trial account. To open
the worksheet for this tutorial, follow these steps:

To open the pre-loaded template worksheet, follow these steps:

1. In the navigation menu, select **Projects** » **Templates**.
2. Find and open **Load data from Microsoft Azure**.

   The beginning of your worksheet looks similar to the following image:

> ![SQL load from cloud template worksheet, which contains the SQL commands for this tutorial, along with descriptive comments.](/static/images/screens/load-data-from-microsoft-azure-worksheet.png)

## Step 3. Set the role and warehouse to use

The role you use determines the privileges you have. In this tutorial, use the
ACCOUNTADMIN system role so that you can view and manage objects in your account.
For more information, see [Using the ACCOUNTADMIN Role](/user-guide/security-access-control-considerations#label-security-accountadmin-role).

A warehouse provides the compute resources that you need to execute DML operations, load data,
and run queries. These resources include CPU, memory, and temporary storage. You can use the
`SNOWFLAKE_LEARNING_WH` warehouse for this tutorial. For more information,
see [Virtual warehouses](/user-guide/warehouses).

To set the role and warehouse to use, do the following:

1. In the open worksheet, place your cursor in the [USE ROLE](/sql-reference/sql/use-role) line.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   ```
2. At the top of the worksheet, select **Run**.

   Note

   In this tutorial, run SQL statements one at a time. Don’t select **Run all**.
3. Place your cursor in the [USE WAREHOUSE](/sql-reference/sql/use-warehouse) line, then select **Run**.

   Copy code

   ```
   USE WAREHOUSE SNOWFLAKE_LEARNING_WH;
   ```

## Step 4. Set up a table that you can load

A database is a repository for your data. The data is stored in tables that you can
manage and query. A schema is a logical grouping of database objects, such as tables
and views. For example, a schema might contain the database objects required for a
specific application. For more information, see [Databases, Tables and Views - Overview](/guides-overview-db).

In this tutorial, you use the database `SNOWFLAKE_LEARNING_DB`, a
schema that concatenates your username with `_LOAD_DATA_FROM_MICROSOFT_AZURE`, and a table
that you create named `calendar`.

To select this database and schema for use in the session and create the table, do the following:

1. In the open worksheet, place your cursor in the [USE DATABASE](/sql-reference/sql/use-database) line,
   then select **Run**.

   Copy code

   ```
   USE DATABASE SNOWFLAKE_LEARNING_DB;
   ```
2. Place your cursor in each SET line, then select **Run**.

   Copy code

   ```
   SET user_name = current_user();
   SET schema_name = CONCAT($user_name, '_LOAD_DATA_FROM_MICROSOFT_AZURE');
   ```
3. Place your cursor in the USE SCHEMA IDENTIFIER line, then select **Run**.

   Copy code

   ```
   USE SCHEMA IDENTIFIER($schema_name);
   ```
4. Place your cursor in the [CREATE TABLE](/sql-reference/sql/create-table) lines, complete the table
   definition, add an optional comment, and select **Run**. For example, the following
   table contains six columns:

   Copy code

   ```
   CREATE OR REPLACE TABLE calendar
     (
     full_date DATE
     ,day_name VARCHAR(10)
     ,month_name VARCHAR(10)
     ,day_number VARCHAR(2)
     ,full_year VARCHAR(4)
     ,holiday BOOLEAN
     )
     COMMENT = 'Table to be loaded from Azure calendar data file';
   ```
5. To confirm that the table was created successfully, place your cursor in the
   [SELECT](/sql-reference/sql/select) line, then select **Run**.

   Copy code

   ```
   SELECT * FROM calendar;
   ```

   The output shows the columns of the table you created. Currently, the table doesn’t have any rows.

## Step 5. Create a storage integration

Before you can load data from cloud storage, you must configure a storage integration that is
specific to your cloud provider. The following example is specific to Microsoft Azure storage.

Storage integrations are named, first-class Snowflake objects that avoid the need for passing explicit
cloud provider credentials such as secret keys or access tokens. Integration objects store an Azure
identity and access management (IAM) user ID called the app registration.

To create a storage integration for Azure, do the following:

1. Use the Azure portal to configure an Azure container for loading data. For details, see
   [Configure an Azure container for loading data](/user-guide/data-load-azure-config).
2. In the open worksheet, place your cursor in the in the [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration)
   lines, define the required parameters, and select **Run**. For example:

   Copy code

   ```
   CREATE OR REPLACE STORAGE INTEGRATION azure_data_integration
     TYPE = EXTERNAL_STAGE
     STORAGE_PROVIDER = 'AZURE'
     AZURE_TENANT_ID = '075f576e-6f9b-4955-8e99-4086736225d9'
     ENABLED = TRUE
     STORAGE_ALLOWED_LOCATIONS = ('azure://tutorial99.blob.core.windows.net/snow-tutorial-container/');
   ```

   Set AZURE\_TENANT\_ID to the Office 365 tenant ID for the storage account that contains the allowed storage
   locations that you want to use. You can find this ID in the Azure portal under
   **Microsoft Entra ID > Properties > Tenant ID**. (Microsoft Entra ID is the new name for Azure Active
   Directory.)

   Set STORAGE\_ALLOWED\_LOCATIONS to the path for the Azure container where your source data file is stored.
   Use the format shown in this example, where `tutorial99` is the storage account name and `snow-tutorial-container` is the container name.
3. Place your cursor in the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) line, specify the name of the storage
   integration you created, and select **Run**.

   Copy code

   ```
   DESCRIBE INTEGRATION azure_data_integration;
   ```

   This command retrieves the AZURE\_CONSENT\_URL and AZURE\_MULTI\_TENANT\_APP\_NAME for the client application
   that was created automatically for your Snowflake account. You will use these values to configure
   permissions for Snowflake in the Azure portal.

   The output for this command looks similar to the following:

   ![Output of DESCRIBE INTEGRATION command, with the following columns: property, property_type, property_value, property_default.](/static/images/screens/desc_storage_integration_azure_output.png)
4. Place your cursor in the [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) line and select **Run**. This command returns
   information about the storage integration you created.

   Copy code

   ```
   SHOW INTEGRATIONS;
   ```

   The output for this command looks similar to the following:

   ![Output of SHOW INTEGRATIONS command, with the following columns: name, type, category, enabled, comment, created_on.](/static/images/screens/show_storage_integration_azure_output.png)
5. Use the Azure portal to configure permissions for the client application (which was created
   automatically for your trial account) to access storage containers. Follow
   [Step 2: Grant Snowflake Access to the Storage Locations](/user-guide/data-load-azure-config)
   under [Configure an Azure container for loading data](/user-guide/data-load-azure-config).

## Step 6. Create a stage

A stage is a location that holds data files to load into a Snowflake database. This tutorial creates
a stage that can load data from a specific type of cloud storage, such as an Azure container.

To create a stage, do the following:

1. In the open worksheet, place your cursor in the [CREATE STAGE](/sql-reference/sql/create-stage) lines, specify a name,
   the storage integration you created, the bucket URL, and the correct file format, then select **Run**.
   For example:

   Copy code

   ```
   CREATE OR REPLACE STAGE cloud_data_db.azure_data.azuredata_stage
     STORAGE_INTEGRATION = azure_data_integration
     URL = 'azure://tutorial99.blob.core.windows.net/snow-tutorial-container/'
     FILE_FORMAT = (TYPE = CSV);
   ```
2. Return information about the stage you created:

   Copy code

   ```
   SHOW STAGES;
   ```

   The output for this command looks similar to the following:

   ![Output of SHOW STAGES command, with the following columns: created_on, name, database_name, schema_name, url.](/static/images/screens/show_stage_azure_output.png)

## Step 7. Load data from the stage

Load the table from the stage you created by using the [COPY INTO <table>](/sql-reference/sql/copy-into-table)
command. For more information about loading from Azure containers, see
[Copy data from an Azure stage](/user-guide/data-load-azure-copy).

To load the data into the table, place your cursor in the [COPY INTO](/sql-reference/sql/copy-into-table)
lines, specify the table name, the stage you created, and name of the file (or files) you want to load, then select
**Run**. For example:

> Copy code
>
> ```
> COPY INTO cloud_data_db.azure_data.calendar
>   FROM @cloud_data_db.azure_data.azuredata_stage
>     FILES = ('calendar.txt');
> ```

Your output looks similar to the following image:

![Five rows are copied into the table. The output has the following columns: file, status, rows_parsed, rows_loaded, error_limit.](/static/images/screens/load_from_cloud_azure_copy_results.png)

## Step 8. Query the table

Now that the data is loaded, you can run queries on the `calendar` table.

To run a query in the open worksheet, select the line or lines of the [SELECT](/sql-reference/sql/select)
command, and then select **Run**. For example, run the following query:

Copy code

```
SELECT * FROM calendar;
```

Your output looks similar to the following image:

![All the rows in the table are selected. This example has full_date, day_name, month_name, day_num, year_num, and holiday columns.](/static/images/screens/load_from_cloud_query_results.png)

## Step 9. Cleanup, summary, and additional resources

Congratulations! You have successfully completed this tutorial for trial accounts.

Take a few minutes to review a short summary and the key points covered in the tutorial.
You might also want to consider cleaning up by dropping any objects you created in the tutorial.
For example, you might want to drop the table you created and loaded:

Copy code

```
DROP TABLE calendar;
```

As long as they are no longer needed, you can also drop the other objects you created, such as
the storage integration and stage. For details, see [Data Definition Language (DDL) commands](/sql-reference/sql-ddl-summary).

### Summary and key points

In summary, you used a pre-loaded template worksheet in Snowsight to complete the following steps:

1. Set the role and warehouse to use.
2. Select a database and schema to use for the session.
3. Create a table.
4. Create a storage integration and configure permissions on cloud storage.
5. Create a stage and load the data from the stage into the table.
6. Query the data.

Here are some key points to remember about loading and querying data:

- You need the required permissions to create and manage objects in your account. In this tutorial,
  you use the ACCOUNTADMIN system role for these privileges.

  This role is not normally used to create objects. Instead, we recommend creating a hierarchy of
  roles aligned with business functions in your organization. For more information, see
  [Using the ACCOUNTADMIN Role](/user-guide/security-access-control-considerations#label-security-accountadmin-role).
- You need a warehouse for the resources required to create and manage objects and run SQL commands.
  This tutorial uses the `SNOWFLAKE_LEARNING_WH` warehouse included with the template environment.
- You used a database to store the data and a schema to group the database objects logically.
- You created a storage integration and a stage to load data from a CSV file stored in an Azure container.
- After the data was loaded into your database, you queried it using SELECT statements.

### What’s next?

Continue learning about Snowflake using the following resources:

- Complete the other tutorials provided by Snowflake:

  - [Tutorials to get started with Snowflake](/learn-tutorials)
- Familiarize yourself with key Snowflake concepts and features, as well as the SQL commands used to
  load tables from cloud storage:

  - [Get started with Snowflake for users](/getting-started-for-users)
  - [Load data into Snowflake](/guides-overview-loading-data)
  - [Data loading and unloading commands](/sql-reference/commands-data-loading)
- Try the Tasty Bytes Quickstarts provided by Snowflake:

  - [Tasty Bytes Quickstarts](https://www.snowflake.com/en/developers/guides/?searchTerm=tasty+bytes)
