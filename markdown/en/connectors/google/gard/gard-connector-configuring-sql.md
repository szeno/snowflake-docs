# Configuring the Snowflake Connector for Google Analytics Raw Data using SQL

This topic provides information on configuring the Snowflake Connector for Google Analytics Raw Data
through SQL.

Note

Snowflake Connector for Google Analytics Raw Data configuration is typically done using Snowsight. SQL configuration is
considered an advanced configuration method and should only be used by
those familiar with the underlying details of connector configuration.

To configure the connector using SQL statements, do the following:

- [Prepare a warehouse, data owner role and destination database](#label-gard-connector-prepare-warehouse-data-owner-role-and-destination-database).
- [Provision the connector](#label-gard-connector-provision-connector).
- [Create Snowflake objects required for connecting to the GCP](#label-gard-connector-snowflake-objects-for-gcp-connection).
- [Configure connection with the GCP](#label-gard-connector-configure-gcp-connection).

Note

In order to provision the connector and configure connection you will have to use stored procedures that are defined
in the PUBLIC schema of the database that serves as an instance of the connector installation database.

Before calling these stored procedures, select that database as the database to use for the session.

For example, if that database is named `snowflake_connector_for_google_analytics_raw_data`, run the following command:

Copy code

```
USE DATABASE snowflake_connector_for_google_analytics_raw_data;
```

## Prepare a warehouse, data owner role and destination database

1. Grant usage on specified warehouse and task execution permissions to the connector application.

   Copy code

   ```
   USE ROLE accountadmin;
   CREATE WAREHOUSE google_analytics_raw_data_warehouse with warehouse_size = 'X-Small';
   GRANT USAGE ON WAREHOUSE google_analytics_raw_data_warehouse TO APPLICATION snowflake_connector_for_google_analytics_raw_data;
   GRANT EXECUTE TASK ON ACCOUNT TO APPLICATION snowflake_connector_for_google_analytics_raw_data;
   GRANT EXECUTE MANAGED TASK ON ACCOUNT TO APPLICATION snowflake_connector_for_google_analytics_raw_data;
   ```
2. Create the data owner role.

   Copy code

   ```
   USE ROLE accountadmin;
   CREATE OR REPLACE ROLE google_analytics_raw_data_resources_provider;
   GRANT CREATE DATABASE ON ACCOUNT TO ROLE google_analytics_raw_data_resources_provider;
   GRANT USAGE ON WAREHOUSE google_analytics_raw_data_warehouse TO ROLE google_analytics_raw_data_resources_provider;
   GRANT ROLE google_analytics_raw_data_resources_provider TO USER ADMIN;
   ```
3. Create a destination database and schema.
   You may also use an existing destination database and schema – especially if you’re re-installing the connector.

   Copy code

   ```
   USE ROLE google_analytics_raw_data_resources_provider;
   CREATE DATABASE google_analytics_raw_data_dest_db;
   CREATE SCHEMA google_analytics_raw_data_dest_db.google_analytics_raw_data_dest_schema;
   ```
4. Add required grants on the destination database to the application.

   Copy code

   ```
   USE ROLE accountadmin;
   GRANT USAGE ON DATABASE google_analytics_raw_data_dest_db TO APPLICATION snowflake_connector_for_google_analytics_raw_data;
   GRANT USAGE ON SCHEMA google_analytics_raw_data_dest_db.google_analytics_raw_data_dest_schema TO APPLICATION snowflake_connector_for_google_analytics_raw_data;

   GRANT CREATE TABLE ON SCHEMA google_analytics_raw_data_dest_db.google_analytics_raw_data_dest_schema TO APPLICATION snowflake_connector_for_google_analytics_raw_data;
   GRANT CREATE VIEW ON SCHEMA google_analytics_raw_data_dest_db.google_analytics_raw_data_dest_schema TO APPLICATION snowflake_connector_for_google_analytics_raw_data;
   ```
5. (Optional) Transfer ownership of tables and views in the destination schema

   If the connector was reinstalled and a previous destination schema is reused, ownership of all tables and views in
   destination schema must be transferred to the connector. The connector requires ownership privilege to manage
   grants on objects in schema and to recreate flattened views when schema of ingested table is changed.

   To transfer the ownership call the `SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION` function.

   Copy code

   ```
   USE ROLE accountadmin;
   CALL SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION(<connector_app>, true, <destination_database>, <destination_schema>);
   ```

   The `SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION` is a system function provided by Snowflake that allows the transfer of
   ownership of tables and views in a specified database or schema to the application. Only the ownership of regular tables and
   regular views is transferred, e.g. ownership of dynamic tables, external tables, materialized views, etc. won’t be
   transferred.

   The function has the following signature:

   Copy code

   ```
   SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION(<to_app>, <should_copy_grants>, <from_database>, <from_schema>)
   ```

   Where:

   > `to_app`
   > :   Specifies the name of the application to which the ownership of objects should be transferred.
   >
   > `should_copy_grants`
   > :   If `TRUE` then copy existing grants, otherwise revoke. Copying grants requires `MANAGE GRANTS`
   >     permission on the caller.
   >
   > `from_database`
   > :   Name of the database containing objects whose ownership should be changed.
   >
   > `from_schema`
   > :   (Optional) name of the schema containing objects whose ownership should be changed. If no schema is specified,
   >     ownership is transferred on tables and views in all schemas in the provided database. Objects in managed schemas
   >     are omitted during ownership transfer.

   To execute the function the caller must meet one of the following conditions:

   - It has `MANAGE GRANTS` permission (e.g. ACCOUNTADMIN or SECURITYADMIN role), or
   - It contains role owning the application instance and role owning all objects to transfer the ownership. Objects on
     which the ownership is missing are omitted by the function.

   For example, to transfer ownership to the connector that:

   - Was installed as `snowflake_connector_for_google_analytics_raw_data`
   - Uses the schema named `dest_db.dest_schema` for the Google Analytics data in Snowflake

   Run the following command:

   Copy code

   ```
   USE ROLE accountadmin;
   CALL SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION('snowflake_connector_for_google_analytics_raw_data', true, 'dest_db', 'dest_schema');
   ```

   If needed, grant `DATA_READER` application role to the role previously owning the data to prevent
   disruptions of existing pipelines using the data:

   Copy code

   ```
   GRANT APPLICATION ROLE <connector_app>.DATA_READER TO ROLE <previous_data_owner_role>;
   ```

   Note that `DATA_READER` application role won’t have any grants on tables and views in destination schema until
   `PROVISION_CONNECTOR` procedure is run.

## Provision the connector

1. Call the `PROVISION_CONNECTOR` procedure.
   Pass the name of the warehouse, destination database and schema, and data owner role. These values are case-sensitive.

   Copy code

   ```
   CALL PROVISION_CONNECTOR(
    'GOOGLE_ANALYTICS_RAW_DATA_WAREHOUSE',
    'GOOGLE_ANALYTICS_RAW_DATA_DEST_DB.GOOGLE_ANALYTICS_RAW_DATA_DEST_SCHEMA',
    'GOOGLE_ANALYTICS_RAW_DATA_RESOURCES_PROVIDER'
   );
   ```

## Create Snowflake objects required for connecting to the GCP

1. Create a security integration for your service account.
   First, you need a service account key file. For details on how to create one see [Configuring service account authentication for Google Cloud Platform (GCP)](/connectors/google/gard/gard-connector-create-service-account-key)

   Copy code

   ```
   CREATE SECURITY INTEGRATION
   google_analytics_raw_data_security_integration
   type = api_authentication
   auth_type = oauth2
   oauth_client_id = '<value of client_id from the JSON key file>'
   oauth_token_endpoint = 'https://oauth2.googleapis.com/token'
   enabled = true
   oauth_allowed_scopes = (
    'https://www.googleapis.com/auth/bigquery.readonly',
    'https://www.googleapis.com/auth/cloudplatformprojects.readonly'
   )
   oauth_assertion_issuer = '<value of client_email from the JSON key file>'
   oauth_grant='JWT_BEARER'
   oauth_client_secret = '<value of private_key from the JSON key file with no delimiters or newlines>';
   ```
2. Create a secret using the security integration.

   Copy code

   ```
   CREATE DATABASE google_analytics_raw_data_connector_secret;
   CREATE SCHEMA google_analytics_raw_data_connector_secret.oauth;

   USE SCHEMA google_analytics_raw_data_connector_secret.oauth;

   CREATE OR REPLACE SECRET google_analytics_raw_data
   type = oauth2
   api_authentication = google_analytics_raw_data_security_integration;
   ```
3. Provide secret-related grants to the connector application.

   Copy code

   ```
   GRANT USAGE ON DATABASE google_analytics_raw_data_connector_secret TO APPLICATION snowflake_connector_for_google_analytics_raw_data;
   GRANT USAGE ON SCHEMA google_analytics_raw_data_connector_secret.oauth TO APPLICATION snowflake_connector_for_google_analytics_raw_data;
   GRANT READ ON SECRET google_analytics_raw_data_connector_secret.oauth.google_analytics_raw_data TO APPLICATION snowflake_connector_for_google_analytics_raw_data;
   ```
4. Configure external access.
   Keep in mind, that the path to the secret passed to `allowed_authentication_secrets` is case-sensitive.

   Copy code

   ```
   USE SCHEMA google_analytics_raw_data_connector_secret.oauth;

   CREATE NETWORK RULE
   google_analytics_raw_data_allow_rule
   mode = EGRESS
   type = HOST_PORT
   value_list = (
    'www.googleapis.com',
    'bigquery.googleapis.com',
    'bigquerystorage.googleapis.com',
    'cloudresourcemanager.googleapis.com',
    'oauth2.googleapis.com'
   );

   CREATE EXTERNAL ACCESS INTEGRATION
   google_analytics_raw_data_external_access_integration
   allowed_network_rules = (google_analytics_raw_data_allow_rule)
   allowed_authentication_secrets = ('GOOGLE_ANALYTICS_RAW_DATA_CONNECTOR_SECRET.OAUTH.GOOGLE_ANALYTICS_RAW_DATA')
   enabled = true;

   GRANT USAGE ON INTEGRATION google_analytics_raw_data_external_access_integration TO APPLICATION snowflake_connector_for_google_analytics_raw_data;
   ```

## Configure connection with the GCP

1. Call the `CONFIGURE_CONNECTION` procedure.
   Pass the name of the external access integration, the full path to the secret, and the name of the security integration. These values are case sensitive.

   Copy code

   ```
   CALL CONFIGURE_CONNECTION(
    'GOOGLE_ANALYTICS_RAW_DATA_EXTERNAL_ACCESS_INTEGRATION',
    'GOOGLE_ANALYTICS_RAW_DATA_CONNECTOR_SECRET.OAUTH.GOOGLE_ANALYTICS_RAW_DATA',
    'GOOGLE_ANALYTICS_RAW_DATA_SECURITY_INTEGRATION'
   );
   ```
2. Check the connection status.

   Copy code

   ```
   CALL CONNECTION_STATUS();
   ```

   If there are no errors, you can follow [Setting up data ingestion for your Snowflake Connector for Google Analytics Raw Data](/connectors/google/gard/gard-connector-setting-up-data) to enable your Google Analytics properties.
