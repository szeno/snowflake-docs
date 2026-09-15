# Configure the using SQL

This topic provides information about using SQL to configure the .

Note

The is typically configured using Snowsight. SQL configuration is
considered an advanced configuration method and should only be used by
those familiar with the underlying details of connector configuration.

Installation using SQL statements is not supported and must be done via Snowsight.

To configure the connector using SQL statements, complete these tasks:

- [Prepare a warehouse, data owner role, and destination database](#label-gaad-connector-prepare-warehouse-data-owner-role-and-destination-database).
- [Configure the connector](#label-gaad-configure-connector).
- [Create Snowflake objects required for connecting to GA4](#label-gaad-connector-snowflake-objects-for-ga-connection).
- [Set the connection configuration](#label-gaad-connector-provision-connector).
- [Finalize the connector configuration](#label-gaad-finalize-connector-configuration).

Note

In order to configure the connector, you must use stored procedures that are defined
in the PUBLIC schema of the connector’s installation database.

Before calling these stored procedures, select that database for the session.

For example, if that database is named `snowflake_connector_for_google_analytics_aggregate_data`, run the following command:

Copy code

```
USE DATABASE snowflake_connector_for_google_analytics_aggregate_data;
```

## Prepare a warehouse, data owner role, and destination database

1. Grant usage on a specified warehouse and task execution permissions to the connector application:

   Copy code

   ```
   USE ROLE accountadmin;
   CREATE WAREHOUSE google_analytics_aggregate_data_warehouse WITH WAREHOUSE_SIZE = 'X-Small';
   GRANT USAGE ON WAREHOUSE google_analytics_aggregate_data_warehouse TO APPLICATION snowflake_connector_for_google_analytics_aggregate_data;
   GRANT EXECUTE TASK, EXECUTE MANAGED TASK ON ACCOUNT TO APPLICATION snowflake_connector_for_google_analytics_aggregate_data;
   ```

   The connector needs these grants to perform ingestion.
2. Create a destination database and schema:

   Copy code

   ```
   CREATE DATABASE google_analytics_aggregate_data_dest_db;
   CREATE SCHEMA google_analytics_aggregate_data_dest_db.google_analytics_aggregate_data_dest_schema;
   ```

   Ingested data is stored in the destination schema. You can also use an existing database and schema.
3. Add required grants on the destination database to the application:

   Copy code

   ```
   USE ROLE accountadmin;
   GRANT USAGE ON DATABASE google_analytics_aggregate_data_dest_db TO APPLICATION snowflake_connector_for_google_analytics_aggregate_data;
   GRANT USAGE ON SCHEMA google_analytics_aggregate_data_dest_db.google_analytics_aggregate_data_dest_schema TO APPLICATION snowflake_connector_for_google_analytics_aggregate_data;
   GRANT CREATE TABLE ON SCHEMA google_analytics_aggregate_data_dest_db.google_analytics_aggregate_data_dest_schema TO APPLICATION snowflake_connector_for_google_analytics_aggregate_data;
   GRANT CREATE VIEW ON SCHEMA google_analytics_aggregate_data_dest_db.google_analytics_aggregate_data_dest_schema TO APPLICATION snowflake_connector_for_google_analytics_aggregate_data;
   ```

   The application needs the grants to create tables for reports data and to create the reports views.
4. Create the data owner role and add required grants:

   Copy code

   ```
   USE ROLE accountadmin;
   CREATE OR REPLACE ROLE google_analytics_aggregate_data_resources_provider;
   GRANT USAGE ON DATABASE google_analytics_aggregate_data_dest_db TO ROLE google_analytics_aggregate_data_resources_provider;
   GRANT USAGE ON SCHEMA google_analytics_aggregate_data_dest_db.google_analytics_aggregate_data_dest_schema TO ROLE google_analytics_aggregate_data_resources_provider;
   GRANT USAGE ON WAREHOUSE google_analytics_aggregate_data_warehouse TO ROLE google_analytics_aggregate_data_resources_provider;
   GRANT APPLICATION ROLE snowflake_connector_for_google_analytics_aggregate_data.data_reader TO ROLE google_analytics_aggregate_data_resources_provider;
   ```

## Configure the connector

- Call the `CONFIGURE_CONNECTOR` procedure, passing the name of the warehouse, destination database and schema, and data owner role:

  > Copy code
  >
  > ```
  > USE ROLE accountadmin;
  > CALL CONFIGURE_CONNECTOR(
  > PARSE_JSON('{"warehouse": "GOOGLE_ANALYTICS_AGGREGATE_DATA_WAREHOUSE", "destination_database": "GOOGLE_ANALYTICS_AGGREGATE_DATA_DEST_DB", "destination_schema": "GOOGLE_ANALYTICS_AGGREGATE_DATA_DEST_SCHEMA", "data_owner_role": "GOOGLE_ANALYTICS_AGGREGATE_DATA_RESOURCES_PROVIDER"}')
  > );
  > ```
  >
  > Note
  >
  > Values passed to CONFIGURE\_CONNECTOR are case-sensitive and should be passed as seen in the UI (for example, as seen in the SHOW command).

## Create Snowflake objects required for connecting to GA4

1. To create a security integration for your connection, follow one of these options:

   > Note
   >
   > Using a service account is a recommended option.
   >
   > If you are using a service account, then you need key file. For details on how to create one see [Configure service account authentication for Google Cloud](/connectors/google/gaad/gaad-connector-create-service-account-key).
   > Create a security integration using the details from the key file:
   >
   > Copy code
   >
   > ```
   > CREATE SECURITY INTEGRATION
   > snowflake_connector_for_google_analytics_aggregate_data_security_integration
   > type = api_authentication
   > auth_type = oauth2
   > oauth_client_id = '000000000000000000000'
   > oauth_token_endpoint = 'https://oauth2.googleapis.com/token'
   > enabled = true
   > oauth_allowed_scopes = ('https://www.googleapis.com/auth/analytics.readonly')
   > oauth_assertion_issuer = '<value of client_email from the JSON key file>'
   > oauth_grant='JWT_BEARER'
   > oauth_client_secret = '<value of private_key from the JSON key file with no delimiters or newlines>';
   > ```
   >
   > If you are using OAuth2, you need to configure a consent screen and client credentials. For details on how to do that, see [Configure OAuth authentication for Google Cloud](/connectors/google/gaad/gaad-connector-create-client-id).
   > Then you need to create security integration:
   >
   > Copy code
   >
   > ```
   > CREATE OR REPLACE SECURITY INTEGRATION
   > snowflake_connector_for_google_analytics_aggregate_data_security_integration
   > type = api_authentication
   > auth_type = oauth2
   > oauth_client_id = '<value of gcp oauth client_id>'
   > oauth_client_secret = '<value of gcp oauth secret>'
   > oauth_token_endpoint = 'https://oauth2.googleapis.com/token'
   > OAUTH_AUTHORIZATION_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth?access_type=offline&prompt=consent'
   > OAUTH_ALLOWED_SCOPES = ('https://www.googleapis.com/auth/analytics.readonly')
   > enabled = true;
   > ```
2. Create a secret using the security integration:

   > Copy code
   >
   > ```
   > USE ROLE accountadmin;
   >
   > CREATE DATABASE connectors_secret;
   > CREATE SCHEMA connectors_secret.snowflake_connector_for_google_analytics_aggregate_data;
   >
   > USE SCHEMA connectors_secret.snowflake_connector_for_google_analytics_aggregate_data;
   >
   > CREATE OR REPLACE SECRET secret
   > type = oauth2
   > api_authentication = snowflake_connector_for_google_analytics_aggregate_data_security_integration;
   > ```
   >
   > Note
   >
   > The secret will securely store the access token generated using the credentials from the security integration.
3. Provide secret-related grants to the connector application:

   Copy code

   ```
   USE ROLE accountadmin;

   GRANT USAGE ON DATABASE connectors_secret TO APPLICATION snowflake_connector_for_google_analytics_aggregate_data;
   GRANT USAGE ON SCHEMA connectors_secret.snowflake_connector_for_google_analytics_aggregate_data TO APPLICATION snowflake_connector_for_google_analytics_aggregate_data;
   GRANT READ ON SECRET connectors_secret.snowflake_connector_for_google_analytics_aggregate_data.secret TO APPLICATION snowflake_connector_for_google_analytics_aggregate_data;
   ```
4. If you are using oauth2 authorization, generate a token. Use the link generated by the following code:

   Copy code

   ```
   SELECT SYSTEM$START_OAUTH_FLOW('connectors_secret.snowflake_connector_for_google_analytics_aggregate_data.secret');
   ```

   You will be redirected to the oauth2 screen. After you accept the required grants, you will be redirected to the endpoint, which completes the oauth2 flow.
5. Configure external access:

   > Copy code
   >
   > ```
   > USE ROLE accountadmin;
   >
   > USE SCHEMA connectors_secret.snowflake_connector_for_google_analytics_aggregate_data;
   >
   > CREATE NETWORK RULE network_rule
   > mode = EGRESS
   > type = HOST_PORT
   > value_list = (
   >  'analyticsadmin.googleapis.com:443',
   >  'analyticsdata.googleapis.com:443'
   > );
   >
   > CREATE EXTERNAL ACCESS INTEGRATION google_analytics_aggregate_data_external_access_integration
   > allowed_network_rules = (connectors_secret.snowflake_connector_for_google_analytics_aggregate_data.network_rule)
   > allowed_authentication_secrets = ('CONNECTORS_SECRET.OAUTH.SNOWFLAKE_CONNECTOR_FOR_GOOGLE_ANALYTICS_AGGREGATE_DATA')
   > enabled = true;
   >
   > GRANT USAGE ON INTEGRATION snowflake_connector_for_google_analytics_aggregate_data_external_access_integration TO APPLICATION snowflake_connector_for_google_analytics_aggregate_data;
   > ```
   >
   > Note
   >
   > The connector uses the external access integration to communicate with Google Analytics APIs. The network rule controls the list of allowed hosts.

## Set the connection configuration

- Call the `SET_CONNECTION_CONFIGURATION` procedure, passing the external access integration, the full path to the secret, and the security integration:

  > Copy code
  >
  > ```
  > USE ROLE accountadmin;
  > CALL SET_CONNECTION_CONFIGURATION(
  >  PARSE_JSON('{"external_access_integration": "SNOWFLAKE_CONNECTOR_FOR_GOOGLE_ANALYTICS_AGGREGATE_DATA_EXTERNAL_ACCESS_INTEGRATION", "secret": "CONNECTORS_SECRET.SNOWFLAKE_CONNECTOR_FOR_GOOGLE_ANALYTICS_AGGREGATE_DATA.SECRET", "security_integration": "SNOWFLAKE_CONNECTOR_FOR_GOOGLE_ANALYTICS_AGGREGATE_DATA_SECURITY_INTEGRATION"}')
  > );
  > ```
  >
  > Note
  >
  > Values passed to SET\_CONNECTION\_CONFIGURATION should be unqualified, uppercase identifiers.

## Finalize the connector configuration

- Call the `FINALIZE_CONNECTOR_CONFIGURATION` procedure:

  Copy code

  ```
  USE ROLE accountadmin;
  CALL FINALIZE_CONNECTOR_CONFIGURATION(
    PARSE_JSON('{}')
  );
  ```

After the process is completed successfully, ingestion configuration can begin. For more information, see [Set up data ingestion for your instance](/connectors/google/gaad/gaad-connector-setting-up-data).
