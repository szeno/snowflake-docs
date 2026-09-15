# Query Snowflake-managed Apache Iceberg™ tables by using Microsoft Fabric

To view Snowflake-managed Iceberg tables in Microsoft Fabric, you can connect a standard Snowflake database to Fabric.

This topic provides the steps for you to connect a standard Snowflake database to Fabric, which syncs the database with Fabric. When you connect a
database, you can either select an existing database or create a new one.
You can then view any Snowflake-managed Iceberg tables in the database in Fabric.

For more information about
Microsoft OneLake Fabric, see
[OneLake in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/onelake/)
in the Microsoft Fabric documentation.

## Prerequisites

Before you begin, complete the following prerequisites for Microsoft Fabric and Snowflake.

**Microsoft Fabric**

- Create a Microsoft Fabric account. For more information, see [Get started with Microsoft Fabric](https://www.microsoft.com/microsoft-fabric/getting-started).
- Create a workspace in your Fabric account. For instructions, see [Create a workspace](https://learn.microsoft.com/en-us/fabric/fundamentals/create-workspaces)
  in the Microsoft Fabric documentation. You use this workspace to query Snowflake-managed Iceberg tables.

  Note

  We recommend that you name your Fabric workspace by using only alphanumeric characters. If your Fabric workspace name contains special
  characters or non-alphanumeric characters such as spaces, you will need to copy the ID of the workspace for specifying this ID later.
  To find your workspace ID, open your workspace in the Fabric UI, and then refer to the URL in your browser.
- You must be an administrator of the Fabric workspace.
- Your Fabric tenant administrator must enable the **Enable Snowflake database item (Preview)** tenant setting or delegate this decision
  to your Fabric capacity administrator. You can enable this setting in the admin portal of the Fabric web UI. To get to the admin portal,
  see [How to get to the admin portal](https://learn.microsoft.com/en-us/fabric/admin/admin-center#how-to-get-to-the-admin-portal) in the
  Microsoft Fabric documentation. You can enable this setting at the tenant level, have it delegated to Fabric capacity administrators, or have it enabled
  only for certain security groups.

**Snowflake**

- You must have access to the ACCOUNTADMIN role or another role in Snowflake with the CREATE USER privilege on the account.
- You must have access to the ACCOUNTADMIN role or another role in Snowflake with privileges to create an external volume.
- You must have a standard database in Snowflake. For instructions, see [CREATE DATABASE](/sql-reference/sql/create-database). This guide refers to an
  example standard database named `SnowflakeFabricIcebergDB`.

  Note

  To complete the steps in this topic, you should have an existing standard database. The topic includes steps for you to grant privileges to that database. However, you have the
  option to create a database when you [connect a Snowflake database to Fabric](#label-tables-iceberg-query-using-microsoft-fabric-connect-snowflake-standard-database).
  If you choose to create a new database when you connect a
  database to Fabric, you would then need to grant the necessary privileges to the database in Snowflake.

## Step 1: Find your Microsoft Fabric Tenant ID, Snowflake organization name, and Snowflake account name

To connect to Microsoft Fabric from Snowflake, you need your Microsoft Fabric Tenant ID. To connect to Microsoft OneLake from Snowflake,
you need your Snowflake organization name and Snowflake account name.

- To find your Microsoft Fabric Tenant ID, follow these steps:

  1. Navigate to [Microsoft Fabric](https://app.fabric.microsoft.com/) and sign in.
  2. Select **?**.
  3. From the **Help** pane, select **About Fabric**.
  4. From the **Fabric** window, see the value for **Tenant URL** and copy the portion of the URL after `ctid` into a text editor.

     For example: `a111a1a1-1111-111a-a11a-1a11a11111a1`
- To find your Snowflake organization name, (`<orgname>`), and Snowflake account name (`<accountname>`), see [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).

## Step 2: Create a role in Snowflake

In this step, you create a role in Snowflake, and then grant it the privileges required to use your standard database and execute
a SELECT statement on tables in the database. Later, you grant this role to a user.

Complete the following steps with the ACCOUNTADMIN role:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Create a worksheet in Snowsight. For more information, see [Create worksheets in Snowsight](/user-guide/ui-snowsight-worksheets-gs#label-snowsight-worksheets-create).
3. Use the [CREATE ROLE](/sql-reference/sql/create-role) command to create a role:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   CREATE ROLE IF NOT EXISTS R_ICEBERG_METADATA;
   ```
4. To grant the Iceberg metadata role privileges to a standard database, follow this example, which grants them to a
   `SnowflakeFabricIcebergDB` database:

   Copy code

   ```
   BEGIN
   LET db STRING := 'SnowflakeFabricIcebergDB';
   EXECUTE IMMEDIATE 'GRANT USAGE ON DATABASE ' || db || ' TO ROLE R_ICEBERG_METADATA';
   EXECUTE IMMEDIATE 'GRANT USAGE ON ALL SCHEMAS IN DATABASE ' || db || ' TO ROLE R_ICEBERG_METADATA';
   EXECUTE IMMEDIATE 'GRANT USAGE ON FUTURE SCHEMAS IN DATABASE ' || db || ' TO ROLE R_ICEBERG_METADATA';
   EXECUTE IMMEDIATE 'GRANT SELECT ON ALL ICEBERG TABLES IN DATABASE ' || db || ' TO ROLE R_ICEBERG_METADATA';
   EXECUTE IMMEDIATE 'GRANT SELECT ON FUTURE ICEBERG TABLES IN DATABASE ' || db || ' TO ROLE R_ICEBERG_METADATA';
   END;
   ```
5. To grant the role the permissions to run queries on an existing warehouse, follow this example, which grants the role
   permissions to run queries on a `COMPUTE_WH` warehouse:

   Copy code

   ```
   GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE R_ICEBERG_METADATA;
   ```

## Step 3: Create a user in Snowflake

In this step, you create a user in Snowflake, and then grant the user the role you created earlier. This grant allows the user to use
the standard database. Later, you specify this user’s credentials when you create a Snowflake connection in
Microsoft Fabric.

If you previously created a user in Snowflake, you can skip this step.

1. To create a user with the role you created as the default, use the [CREATE USER](/sql-reference/sql/create-user) command:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   CREATE USER IF NOT EXISTS SVC_FABRIC_ICEBERG_METADATA
   TYPE = LEGACY_SERVICE
   LOGIN_NAME = 'SVC_FABRIC_ICEBERG_METADATA'
   DISPLAY_NAME = 'Service - Fabric Iceberg Metadata'
   PASSWORD = '<strong_password>'
   MUST_CHANGE_PASSWORD = FALSE
   DEFAULT_ROLE = R_ICEBERG_METADATA;
   ```
2. Grant the role that you created to the user:

   Copy code

   ```
   GRANT ROLE R_ICEBERG_METADATA TO USER SVC_FABRIC_ICEBERG_METADATA;
   ```

## Step 4: Create a Snowflake connection in Microsoft Fabric

In this step you create a Snowflake connection in Microsoft Fabric, which allows you to connect your standard database in Snowflake to
Microsoft Fabric.

Important

If you already have an existing Snowflake connection configured in Microsoft Fabric that meets the following conditions, you can skip
this step:

> - It uses the correct Snowflake username and password credentials.
> - It has access to the required warehouse in Snowflake.

1. Navigate to [Microsoft Fabric](https://app.fabric.microsoft.com/), and then sign in.
2. Select the **Settings** icon.
3. In **Settings**, select **Manage connections and gateways**.
4. Select **+ New**.
5. In the **New connection** dialog, create a Snowflake connection:

   1. Select **Cloud**.
   2. For **Connection name**, enter a connection name.
   3. For **Connection type**, select **Snowflake**.
   4. For **Server**, enter your identifier for your Snowflake account:

      ```
      https://<orgname>-<accountname>.snowflakecomputing.com
      ```

      Where:

      - `<orgname>` is the name of your Snowflake organization and `<accountname>` is the name of your Snowflake account. To find
        these names, see [Step 1: Find your Microsoft Fabric Tenant ID, Snowflake organization name, and Snowflake account name](#label-tables-iceberg-query-using-microsoft-fabric-before-begin).
   5. For **Warehouse**, enter the name of the warehouse in Snowflake that you granted the R\_ICEBERG\_METADATA role usage access to, such
      as `COMPUTE_WH`, when you [created a role](#label-tables-iceberg-query-using-microsoft-fabric-create-user).
   6. For **Authentication method**, select **Snowflake**.
   7. For **Username**, enter the name of the user you [created in Snowflake](#label-tables-iceberg-query-using-microsoft-fabric-create-user).
   8. For **Password**, enter the password for the user that you [created in Snowflake](#label-tables-iceberg-query-using-microsoft-fabric-create-user).
   9. Select **Create**.

   Note

   For more information about creating a Snowflake connection in Microsoft Fabric,
   see [Set up your Snowflake database connection](https://learn.microsoft.com/fabric/data-factory/connector-snowflake) in the Microsoft Fabric documentation.
6. After your connection is created, copy the **Connection ID** for your connection into a text editor.

   For example: `1111a111-11a1-1111-11a1-11aa1111aaa1`. You must specify this Connection ID later in Snowflake when you
   connect your Snowflake standard database to Microsoft Fabric.

## Step 5: Retrieve your Azure multi-tenant application name

In this step, you use Snowflake to retrieve your Azure multi-tenant application name. You specify this application name later when you
[give your Azure multi-tenant application access to your Fabric workspace](#label-tables-iceberg-query-using-microsoft-fabric-multi-tenant-app-access).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Ingestion** » **Add Data**.
3. On the **Add Data** page, select **Microsoft OneLake**.
4. Enter your Fabric tenant ID, and then select **Continue**.
5. Near the top of the **Create an item in Microsoft Fabric** dialog, copy your **Multi-tenant app name** into a text editor.

## Step 6: Give your Azure multi-tenant application access to your workspace

In this step, you give Azure multi-tenant application access to your workspace in Fabric.

1. Navigate to [Microsoft Fabric](https://app.fabric.microsoft.com/), and then sign in.
2. Open your Microsoft Fabric workspace.

   To create a workspace, see [Prerequisites](#label-tables-iceberg-query-using-microsoft-fabric-prerequisites).
3. Select **Manage access**.
4. Select **+ Add people or groups**.
5. In the **Enter name or email** field, paste your Azure multi-tenant application name from Snowflake.

   To retrieve your Azure multi-tenant app
   name, see [Step 5: Retrieve your Azure multi-tenant application name](#label-tables-iceberg-query-using-microsoft-fabric-retrieve-azure-multi-tenant-app-name).
6. In the drop-down menu, select **Contributor** access or higher to allow the app to create the necessary Fabric item.
7. Select **Add**.
8. In the top-right area, select **Settings**, and then select **Manage connections and gateways**.
9. In the top-right area, search for your connection ID.

   You copied this connection ID when you [created a Snowflake connection in Microsoft Fabric](#label-tables-iceberg-query-using-microsoft-fabric-create-snowflake-connection).
10. On the **Connections** tab, hover on your connection, select the **…** icon for your connection, and then select **Manage users**.
11. In the **Search by name or email** field, search for your multi-tenant application name, and then select it.
12. Select the appropriate level of privileges for the user.
13. To allow the multi-tenant application to use the Snowflake connection, select **Share**.

## Step 7: Enable access to Fabric public APIs

In this step, you enable access to Fabric public APIs by allowing your Snowflake service principal to call the Fabric public APIs.

### Step 7.1: Allow your service principal to call the Fabric public APIs

To allow your Snowflake service principal to call Fabric public APIs, follow these steps:

1. Sign in to Microsoft Fabric.
2. Go to the tenant settings. For instructions, see [How to get to the tenant settings](https://learn.microsoft.com/fabric/admin/about-tenant-settings?source=recommendations#how-to-get-to-the-tenant-settings)
   in the Microsoft Fabric documentation.
3. From the tenant settings, enable the **Service principals can call Fabric public APIs** setting by selecting one of the following options:

   - **Entire organization**
   - **Specific security groups** and then select the security group that will contain your Snowflake service principal.

   For more information about this setting, see [Service principals can call Fabric public APIs](https://learn.microsoft.com/en-us/fabric/admin/service-admin-portal-developer#service-principals-can-call-fabric-public-apis).

### Step 7.2: Add your multi-tenant app to the allowed security group

Important

If you enabled the **Service principals can call Fabric public APIs** setting in Fabric for your *entire organization*,
you can skip this step.

In this section, you add your multi-tenant app as a member of the security group that you granted access to the Fabric public APIs.

- In the Microsoft Entra admin center, add your **multi-tenant app name** to the allowed security group. You copied your multi-tenant app
  name when you
  [retrieved your Azure multi-tenant application name](#label-tables-iceberg-query-using-microsoft-fabric-retrieve-azure-multi-tenant-app-name).

  For instructions, see
  [Add members or owners of a group](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-manage-groups#add-members-or-owners-of-a-group)
  in the Microsoft Entra documentation.

  Important

  When you add a member, search for and select your **multi-tenant app name**.

## Step 8: Connect your Snowflake standard database to Microsoft Fabric

In this step, you connect a standard Snowflake database to Microsoft Fabric.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Ingestion** » **Add Data**.
3. On the **Add Data** page, select **Microsoft OneLake**.
4. Enter your Fabric tenant ID and select **Continue**.

   To find your Fabric tenant ID, see [Step 1: Find your Microsoft Fabric Tenant ID, Snowflake organization name, and Snowflake account name](#label-tables-iceberg-query-using-microsoft-fabric-before-begin).
5. To provide consent to the use of your Snowflake account’s multi-tenant application in your Entra tenant, select **Provide consent**.

   - If you haven’t performed this step before, you should see a prompt to consent. Review the permissions, provide your consent, and then proceed to the next step.
   - It’s possible that this step is already completed for your Snowflake account. If so, close the pop-up that appears, and then proceed to the next step.
   - If you can’t complete the consent flow, ask your Entra tenant administrator to complete this step for you.
6. Select **Continue**.

   Note

   If you receive a “You have not consented to the application. Please provide the consent to continue” error message when you select
   **Continue**, make sure you have [enabled access to Fabric public APIs](#label-tables-iceberg-query-fabric-enable-fabric-apis)
7. In the **Create an item in Microsoft Fabric** dialog, fill in the fields:

   - For **Fabric workspace name**, enter the name of the workspace in Fabric where you want to view your Iceberg tables.
   - To validate that your connection ID is in the correct format, for **Snowflake connection ID in Fabric**, enter your
     Snowflake connection ID that you copied when you [created a Snowflake connection in Microsoft Fabric](#label-tables-iceberg-query-using-microsoft-fabric-create-snowflake-connection).

     Note

     You must create a Snowflake connection object in Fabric before you can read your Snowflake-managed tables.
   - For **Snowflake database**, select the Snowflake database that contains the Snowflake-managed Iceberg tables that you want to view in Fabric.

     Note

     If you want to create a new Snowflake database and connect it to Fabric, select **+ Create a new database**.
8. To create a Fabric item and database, select **Continue**.
9. In the **Create External Volume** dialog, to create an external volume, review the volume details, and then select **Create Volume**.

   A Fabric item is created in Microsoft Fabric and an external volume is created in Microsoft Fabric OneLake.

## Step 9: Verify your external volume

Verify the external volume you configured to check that Snowflake can successfully authenticate to your storage provider using the
external volume. For instructions, see [Verify an external volume](/user-guide/tables-iceberg-configure-external-volume#label-tables-iceberg-configure-external-volume-verify).

## Step 10: Create an Iceberg table

In this step, you create a Snowflake-managed Iceberg table in your standard database in Snowflake.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Open your worksheet in Snowsight.

   For more information, see [Opening worksheets in tabs](/user-guide/ui-snowsight-worksheets-gs#label-snowsight-open-worksheet).
3. In your standard database, create a sample Iceberg table:

   Copy code

   ```
   CREATE ICEBERG TABLE SnowflakeFabricIcebergDB.PUBLIC.SampleIcebergTable (
   id INT,
   name STRING
   )
   CATALOG = 'SNOWFLAKE';
   ```
4. In the sample Iceberg table, insert two rows:

   Copy code

   ```
   INSERT INTO SnowflakeFabricIcebergDB.PUBLIC.SampleIcebergTable VALUES
   (1, 'Alice'),
   (2, 'Bob');
   ```

## Step 11: View the Iceberg table in Fabric

1. Navigate to [Microsoft Fabric](https://app.fabric.microsoft.com/), and then sign in.
2. Open your workspace.

   You should see a new Snowflake database item named after your database. If needed, refresh the page.
3. Where you created your table in Snowflake, open the database item and schema.

   You should see the Iceberg table you created in Snowflake. As you update the table in Snowflake, you can refresh
   the table updates in Microsoft Fabric.
4. In the upper-right corner, select **SQL analytics endpoint**.

   You can use SQL to interact with your table or try using other Fabric workloads to query this table alongside your other Fabric data.
