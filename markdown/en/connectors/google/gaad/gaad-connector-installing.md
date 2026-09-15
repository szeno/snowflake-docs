# Install and configure the

This topic provides information about installing and configuring the
through Snowsight.

## Install the

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
3. Search for the , and then select the tile for the connector.
4. On the page for the , select **Get**.

   A dialog box is displayed.
5. Under **Options**, for **Application name**, enter a name for the database to use for the connector instance.

   This database is created for you automatically.
6. For **Warehouse used for installation**, select the warehouse to use for installing the connector.

   > Note
   >
   > This is not the same warehouse that is used by the connector to synchronize data from Google Analytics.
   > In a later procedure, you create a separate warehouse for this purpose.

## Configure the

Note

can also be configured using SQL. Configuration using SQL is considered
an advanced topic. For more information see [Configure the using SQL](/connectors/google/gaad/gaad-connector-configuring-sql).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with either the ACCOUNTADMIN role or any other role that meets the following requirements:

   - You must have these account-level privileges:

     - EXECUTE TASK with the grant option
     - EXECUTE MANAGED TASK with the grant option
   - EVENT\_TABLE must be enabled on the account.
   - For warehouse access, you must have at least one of the following privileges:

     - The CREATE WAREHOUSE privilege on the account
     - The OWNERSHIP privilege on the warehouse
     - The USAGE privilege on the warehouse (with the grant option)
   - For database access, you must have at least one of the following privileges:

     - The CREATE DATABASE privilege on the account
     - The OWNERSHIP privilege on the database
     - The USAGE privilege on the database (with the grant option)
   - For schema access, you must have at least one of the following privileges:

     - The CREATE DATABASE privilege on the account
     - The OWNERSHIP privilege on the database
     - The USAGE privilege on the database (with the grant option)
     - The CREATE SCHEMA privilege on the database
     - The USAGE, CREATE TABLE, CREATE VIEW privileges on the schema (with the grant option)
   - Optional: For role access, you can create a new or select an existing role that will be
     assigned the DATA\_READER application role. If you want to create a new role, then you need the CREATE ROLE privilege on your account.
     However, this is not necessary to complete the configuration.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select the .

   The configuration wizard starts.
4. Ensure that all prerequisites on the list are met, and mark them as done.
5. Click **Start configuration**.
6. Populate the following fields:

   Note

   By default, the fields are set to the names of objects that are created when you configure the connector.
   Snowflake recommends using new objects for these fields. However, you can specify the names of existing objects (for example, if you are reinstalling the connector).

   | Field | Description |
   | --- | --- |
   | **Warehouse** | Enter the identifier for a new, dedicated virtual warehouse for the connector.  Specify a name that is unique for your account. The name of the warehouse must be a valid [object identifier](/sql-reference/identifiers-syntax).  The configuration process creates a new `X-Small` warehouse with the specified name. |
   | **Destination Database** | Enter the identifier for a new database that will contain the schema with the tables for the Google Analytics data in Snowflake. Data downloaded from Google Analytics will be stored here.  Specify a name that is unique for your account. The name of the database must be a valid [object identifier](/sql-reference/identifiers-syntax).  The configuration process creates a new database with the specified name. |
   | **Destination Schema** | Enter the identifier for a new schema that will contain the Google Analytics data in Snowflake.  The ingests Google Analytics data into tables in this schema.  The name of the schema must be a valid [object identifier](/sql-reference/identifiers-syntax).  The configuration process creates a new schema with the specified name. |
   | **Role** | Enter the identifier for a new custom role for the connector.  This role is granted read access to tables and views that contain the Google Analytics data ingested by the connector.  The name of the role must be a valid [object identifier](/sql-reference/identifiers-syntax).  The configuration process creates a new role with the specified name. |

   Expand

   Show lessSee more
7. Select **Configure** at the bottom of the screen.

   The configuration process can take several minutes. When it is finished, the wizard advances to **Authentication**.
8. To specify authentication, follow one of these options:

   Note

   The supports two methods of authenticating in Google Analytics: **service accounts** and **OAuth2**. Each method requires
   additional configuration in your Google Cloud project. For more information, see [Configure service account authentication for Google Cloud](/connectors/google/gaad/gaad-connector-create-service-account-key) and [Configure OAuth authentication for Google Cloud](/connectors/google/gaad/gaad-connector-create-client-id).

   - For a **service account**, populate the following fields:

   | Field | Description |
   | --- | --- |
   | **Client email** | Google service account email that was generated during service account creation in your Google Cloud project |
   | **Private key** | Private key that was generated during service account creation in your Google Cloud project  Ensure that the **—BEGIN PRIVATE KEY—**, **—END PRIVATE KEY—**, and **\n** symbols are removed. |

   Expand

   Show lessSee more

   - For **Oauth2**, populate the following fields:

   | Field | Description |
   | --- | --- |
   | **Client id** | Client ID that was generated in your Google Cloud project |
   | **Client secret** | Client secret that was generated for the client ID |

   Expand

   Show lessSee more

   If you’re not signed in as a user with the ACCOUNTADMIN role, ensure that you meet the following requirements:

   - You must have the CREATE INTEGRATION privilege.
   - If integrations were previously created by other roles, then the ownership of those integrations must be transferred to your role.
   - If the CONNECTORS\_SECRET database doesn’t exist, then you need the CREATE DATABASE privilege.
   - If CONNECTORS\_SECRET database exists but was created by another role, then you need these privileges:

     - USAGE WITH GRANT OPTION
     - CREATE SCHEMA WITH GRANT OPTION
   - If CONNECTORS\_SECRET.APP\_NAME schema exists but was created by another role, then you need these privileges:

     - USAGE WITH GRANT OPTION
     - CREATE SECRET
     - CREATE NETWORK RULE
   - If CONNECTORS\_SECRET.APP\_NAME.SECRET exists but was created by another role, then its ownership needs to be transferred to your role.
   - If CONNECTORS\_SECRET.APP\_NAME.NETWORK\_RULE exists but was created by another role, then its ownership needs to be transferred to your role.
9. Select **Connect**.

   If you selected **Oauth2** authentication, the Google OAuth authentication dialog will open.
10. Optional: Complete the Google OAuth authentication dialog.

After successfully connecting, the connector verifies whether it can access Google Analytics data. If there are any errors, you will be provided with additional instructions.

After the process is completed successfully, ingestion configuration can begin. For more information, see [Set up data ingestion for your instance](/connectors/google/gaad/gaad-connector-setting-up-data).
