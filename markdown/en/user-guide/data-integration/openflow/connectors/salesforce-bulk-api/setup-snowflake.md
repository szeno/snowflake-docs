# Openflow Connector for Salesforce Bulk API: Set up Snowflake

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up Snowflake for the Openflow Connector for Salesforce Bulk API.

## Prerequisites

Before you begin, ensure you have completed the following:

- Install Openflow (either BYOC or SPCS). For more information, see [About Openflow](/user-guide/data-integration/openflow/about).
- Create an Openflow deployment. For more information, see [Set up Openflow - Snowflake Deployment: Create deployment](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment) or [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc).
- Create an Openflow runtime. For more information, see [Set up Openflow - Snowflake Deployment: Create runtime](/user-guide/data-integration/openflow/setup-openflow-spcs-create-runtime) or [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc).
- Review the known limitations of the connector in [About the Openflow Connector for Salesforce Bulk API](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/about).
- If you are using Openflow - Snowflake Deployments, ensure that you have reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list) and have granted access to the required domains for the [Salesforce Bulk API](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-salesforce-bulk-api) connector.

## Create objects and grant privileges

As an Openflow administrator, perform the following tasks. With the default `SNOWFLAKE_MANAGED`
authentication strategy, the runtime’s execute-as role is the identity the connector uses to access
Snowflake, so you grant it the privileges below.

1. Use a role with `ACCOUNTADMIN` privileges to set the role:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   ```
2. Create the destination Snowflake database, if it does not
   exist:

   Copy code

   ```
   CREATE DATABASE IF NOT EXISTS <my_salesforce_db>;
   ```
3. Create the destination schema in the database, if it does
   not exist:

   Copy code

   ```
   CREATE SCHEMA IF NOT EXISTS <my_salesforce_db>.<my_salesforce_schema>;
   ```
4. Grant the required privileges to the runtime’s execute-as role.

   Copy code

   ```
   GRANT USAGE ON DATABASE <my_salesforce_db> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT USAGE ON SCHEMA <my_salesforce_db>.<my_salesforce_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT CREATE TABLE, CREATE PIPE ON SCHEMA <my_salesforce_db>.<my_salesforce_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```
5. Create a warehouse for the connector (or use an existing one) and grant usage privileges to the execute-as role:

   Copy code

   ```
   -- Create a warehouse (skip if you wish to use an existing warehouse)
   CREATE OR REPLACE WAREHOUSE MY_WAREHOUSE WITH
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE;

   GRANT USAGE, OPERATE ON WAREHOUSE MY_WAREHOUSE TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```

Note

If you’re deploying the connector in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication
strategy instead of the recommended `SNOWFLAKE_MANAGED`, you’ll also grant this same execute-as
role to a service user rather than relying on the runtime’s managed token. See
[Set up key-pair authentication for Openflow - BYOC Deployments](/user-guide/data-integration/openflow/setup-openflow-byoc-key-pair-auth)
to create the service user.

## Next steps

Configure the connector in Openflow:

[Openflow Connector for Salesforce Bulk API: Configure the connector](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/configure-connector)

To use Iceberg tables as the destination, see [Openflow Connector for Salesforce Bulk API: Iceberg table destinations](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/iceberg).
