# External network access and private connectivity on Microsoft Azure

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides configuration details to set up outbound private connectivity to an external service by way of
[external network access](/developer-guide/external-network-access/external-network-access-overview). The primary differences between
the outbound public connectivity and outbound private connectivity configurations are that, with private connectivity, you must do the
following operations:

- Create a private connectivity endpoint. This step requires the ACCOUNTADMIN role.
- Create the network rule to use the `PRIVATE_HOST_PORT` property. This property includes the Azure URL and port number, which
  enables the connection from Snowflake to Microsoft Azure to go through the Microsoft Azure internal network, avoiding the public Internet.

## Outbound private connectivity costs

You pay for each private connectivity endpoint along with total data processed. For pricing of these items, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You can explore the cost of these items by filtering on the following service types when querying billing views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas:

- OUTBOUND\_PRIVATELINK\_ENDPOINT
- OUTBOUND\_PRIVATELINK\_DATA\_PROCESSED

For example, you can query the [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) view and filter on these service types.

## Configure external network access

These steps are unique to using outbound private connectivity with external network access on Microsoft Azure:

1. Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision a private
   connectivity endpoint in your Snowflake VNet to enable Snowflake to connect to an external service using private connectivity:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     '/subscriptions/1111-22-333-4444-55555/resourceGroups/external-access/providers/Microsoft.Sql/servers/externalaccessdemo',
     'externalaccessdemo.database.windows.net',
     'sqlServer'
   );
   ```
2. In the Azure Portal and as the owner of the Azure API Management resource, approve the private endpoint. For more information, see the
   [Microsoft Azure documentation](https://learn.microsoft.com/en-us/azure/private-link/manage-private-endpoint?tabs=manage-private-link-powershell#private-endpoint-connections).
3. Create a [database](/sql-reference/sql/create-database) and [schemas](/sql-reference/sql/create-schema) to store the network
   rule, secret, and procedure:

   Copy code

   ```
   CREATE DATABASE ext_network_access_db;
   CREATE SCHEMA secrets;
   CREATE SCHEMA network_rules;
   CREATE SCHEMA procedures;
   ```
4. Create a [network rule](/sql-reference/sql/create-network-rule), specifying the `PRIVATE_HOST_PORT` property to enable
   private connectivity:

   Copy code

   ```
   CREATE OR REPLACE NETWORK RULE ext_network_access_db.network_rules.azure_sql_private_rule
   MODE = EGRESS
   TYPE = PRIVATE_HOST_PORT
   VALUE_LIST = ('externalaccessdemo.database.windows.net');
   ```
5. Create a [secret](/sql-reference/sql/create-secret) to securely store the access credentials:

   Copy code

   ```
   CREATE OR REPLACE SECRET ext_network_access_db.secrets.secret_password
   TYPE = PASSWORD
   USERNAME = 'my-username'
   PASSWORD = 'my-password';
   ```
6. Create an [external access integration](/sql-reference/sql/create-external-access-integration), specifying the network rule from
   the previous step:

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION azure_private_access_sql_store_integration
   ALLOWED_NETWORK_RULES = (ext_network_access_db.network_rules.azure_sql_private_rule)
   ALLOWED_AUTHENTICATION_SECRETS = (ext_network_access_db.secrets.secret_password)
   ENABLED = TRUE;
   ```
7. Create a [procedure](/sql-reference/sql/create-procedure) to connect to the external service:

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE ext_network_access_db.procedures.connect_azure_sqlserver()
     RETURNS TABLE()
     LANGUAGE PYTHON
     RUNTIME_VERSION = 3.10
     HANDLER = 'connect_sqlserver'
     EXTERNAL_ACCESS_INTEGRATIONS = (azure_private_access_sql_store_integration)
     SECRETS = ('cred' = ext_network_access_db.secrets.secret_password)
     IMPORTS = ('@demo/pytds.zip')
     PACKAGES = ('snowflake-snowpark-python','pyopenssl','bitarray','certifi')
   AS $$
   import pytds
   import certifi
   import _snowflake
   from snowflake.snowpark import types as T

   def connect_sqlserver(session):
   server = 'externalaccessdemo.database.windows.net'
   database = 'externalaccess'
   username_password_object = _snowflake.get_username_password('cred');

   # Create a connection to the database
   with pytds.connect(server, database, username_password_object.username, username_password_object.password, cafile=certifi.where(), validate_host=False) as conn:
         with conn.cursor() as cur:
            cur.execute("""
            SELECT O.OrderId,
                  O.OrderDate,
                  O.SodName,
                  O.UnitPrice,
                  O.Quantity,
                  C.Region
            FROM Orders AS O
            INNER JOIN Customers AS C
               ON O.CustomerID = C.CustomerID;""")
            rows = cur.fetchall()

            schema = T.StructType([
                  T.StructField("ORDER_ID", T.LongType(), True),
                  T.StructField("ORDER_DATE", T.DateType(), True),
                  T.StructField("SOD_NAME", T.StringType(), True),
                  T.StructField("UNIT_PRICE", T.FloatType(), True),
                  T.StructField("QUANTITY", T.FloatType(), True),
                  T.StructField("REGION", T.StringType(), True)
               ])

            final_df = session.createDataFrame(rows, schema)

            return final_df
   $$;
   ```
8. Call the procedure to connect to the external service:

   Copy code

   ```
   CALL ext_network_access_db.procedures.connect_azure_sqlserver();
   ```

Repeat these steps for each external network access configuration that requires private connectivity.

If you no longer need the private connectivity endpoint for the external network access integration, call the
[SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) system function.
