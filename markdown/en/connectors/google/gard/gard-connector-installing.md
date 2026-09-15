# Installing and configuring the Snowflake Connector for Google Analytics Raw Data

This topic provides information on installing and configuring the Snowflake Connector for Google Analytics Raw Data
through Snowsight.

## Installing the Snowflake Connector for Google Analytics Raw Data

To install the connector, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
3. Search for the Snowflake Connector for Google Analytics Raw Data, then select the tile for the connector.
4. In the page for the Snowflake Connector for Google Analytics Raw Data, select **Get**.

   This displays a dialog box that you use to begin the initial part of the installation process.

   In the dialog box configure the following:

   1. In the **Options->Application name** field, enter the database to use as the database for the connector
      instance. This database is created for you automatically.
   2. In the **Warehouse used for installation** field, select the warehouse that you want to use for
      installing the connector.

      Note

      This is not the same warehouse that is used by the connector to synchronize data from Google Analytics.
      In a later step, you will create a separate warehouse for this purpose.
   3. Select **Get**.
5. Select **Open**.

   The dialog box closes, and the Snowflake Connector for Google Analytics Raw Data page displays the UI
   for configuring and managing the connector.

## Configuring the Snowflake Connector for Google Analytics Raw Data

Note

Snowflake Connector for Google Analytics Raw Data can also be configured using SQL. Configuration using SQL is considered
an advanced topic. For more information see [Configuring the Snowflake Connector for Google Analytics Raw Data using SQL](/connectors/google/gard/gard-connector-configuring-sql).

To configure the connector, do the following:

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
3. Select the Snowflake Connector for Google Analytics Raw Data.

   The configuration wizard starts.
4. Prerequisites

   1. Make sure all prerequisites from the list are met and mark them done.
   2. Select **Start configuration**.
5. Configure warehouse, database, schema and role

   Note

   By default, the fields are set to the names of objects that are created when you configure the connector.
   Snowflake recommends using new objects for these fields. However, you can specify the names of existing objects,
   if needed (for example, if you are reinstalling the connector).

   Populate the following fields and select **Configure** at the bottom of the screen:

   | Field | Description |
   | --- | --- |
   | **Warehouse** | Enter the identifier for a new, dedicated virtual warehouse for the connector or select an existing one.  Specify a name that is unique for your account. The name of the warehouse must be a valid [object identifier](/sql-reference/identifiers-syntax).  Note  Do not specify the same warehouse that you selected at the beginning of the connector installation.  The configuration process creates a new `X-Small` warehouse with the specified name.  Alternatively, you can select an existing warehouse. |
   | **Destination Database** | Identifier for a new database that will contain the schema with the tables for the Google Analytics data in Snowflake. Data downloaded from Google Analytics will land here.  Specify a name that is unique for your account. The name of the database must be a valid [object identifier](/sql-reference/identifiers-syntax).  The configuration process creates a new database with the specified name.  Alternatively, you can select an existing database. |
   | **Destination Schema** | Identifier for a new schema that will contain the Google Analytics data in Snowflake.  The Snowflake Connector for Google Analytics Raw Data ingests Google Analytics data into tables in this schema.  The name of the schema must be a valid [object identifier](/sql-reference/identifiers-syntax).  The configuration process creates a new schema with the specified name.  Alternatively, you can select an existing schema. |
   | **Role** | Identifier for a new custom role for the connector.  Specify a name that is unique for your account. The name of the role must be a valid [object identifier](/sql-reference/identifiers-syntax).  The role is an account-level role that will have read access to the ingested data.  Alternatively you can select an existing role. |

   Expand

   Show lessSee more

   If existing destination database and schema were provided, ownership of the
   existing regular tables and views will be transferred to the Snowflake Connector for Google Analytics Raw Data. That excludes, for example,
   external tables and materialized views. Moreover **nothing** will be transferred in managed schemas.

   It can take some time for the configuration process to complete. When the configuration process finishes successfully,
   the configuration wizard advances to `Authentication`.
6. Configure authentication

   The Snowflake Connector for Google Analytics Raw Data supports two authentication methods: **OAuth** and **Service Accounts**.
   Each of the methods requires additional configuration in your GCP project.

   For more information on how to configure each authentication see:

   - [Configuring service account authentication for Google Cloud Platform (GCP)](/connectors/google/gard/gard-connector-create-service-account-key)
   - [Configuring OAuth authentication for Google Cloud Platform (GCP)](/connectors/google/gard/gard-connector-create-client-id)

   If using authentication method **Service Account**, provide a JSON file with Service Account credentials.

   Alternatively you can populate the following fields:

   | Field | Description |
   | --- | --- |
   | **Client email** | Google service account email which was generated during service account creation process in Google Cloud Platform project. |
   | **Private key** | Private key which was generated during service account creation process in Google Cloud Platform project. |

   Expand

   Show lessSee more

   Ensure that you have removed `-----BEGIN PRIVATE KEY-----`, `-----END PRIVATE KEY-----`, and `\\n`.

   If using authentication method **Oauth2**, populate the following fields:

   | Field | Description |
   | --- | --- |
   | **Client id** | Client ID generated in Google Cloud Platform project. |
   | **Client secret** | Client secret ID generated in Google Cloud Platform project. |

   Expand

   Show lessSee more

   If you’re not signed in as a user with the ACCOUNTADMIN role, ensure that you meet the following requirements:

   - You must have the CREATE INTEGRATION privilege.
   - If integrations were previously created by other roles, then the ownership of those integrations must to be transferred to your role.
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

   Select **Connect**

   If you have selected **Oauth2** authentication, you will be presented with the Google OAuth2 authentication dialog flow.

   In the dialog, log in to Google to complete the Google OAuth2 authentication flow.

   It can take some time for the authentication process to complete.
7. Validate source

> After a successful connection, the connector will verify that it can access the Google Analytics data. On error, the connector will guide you with additional instruction.
>
> If the process completes successfully you can start configuring ingestion.
> For more information see [Setting up data ingestion for your Snowflake Connector for Google Analytics Raw Data](/connectors/google/gard/gard-connector-setting-up-data)
