# Set up the Openflow Connector for Shopify

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Shopify.

## Prerequisites

1. Review [About the Openflow Connector for Shopify](/user-guide/data-integration/openflow/connectors/shopify/about).
2. Set up your runtime deployment.

   - [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc)
   - [Set up Openflow - Snowflake Deployment - Task overview](/user-guide/data-integration/openflow/setup-openflow-spcs)
3. If you’re using Openflow - Snowflake Deployments, ensure that you have reviewed
   [the required domain configuration](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the [domains](#label-shopify-req-domains) required by the connector.
4. Ensure you have access to the Openflow admin role or a similar role you use to manage Openflow.
5. If you’re creating a Snowflake service user to manage the connector, set up key pair authentication. For more information, see [key pair authentication](/user-guide/key-pair-auth).

## Required endpoints

The following endpoints are required for the connector to function:

- `<your_store>.myshopify.com:443` (for example, `mystore.myshopify.com:443`): Shopify Admin GraphQL API
- `storage.googleapis.com:443`: Shopify bulk-operation result downloads. When a bulk query completes, Shopify returns a signed Google Cloud Storage URL for the JSONL result file. The connector must be able to reach this host to download the file.

If you’re using Openflow - BYOC Deployments, configure your cloud network egress to allow HTTPS (port 443) access to both endpoints.
If you’re using Openflow - Snowflake Deployments, you must create a network rule and an external access integration (EAI). For more information, see [Create a network rule (Openflow - Snowflake Deployments only)](#label-create-network-rule).

## Set up Shopify

A Shopify store administrator must create a Shopify dev app and configure API scopes for the
connector to authenticate.

1. Log in to the [Shopify Dev Dashboard](https://dev.shopify.com/dashboard/).
2. Select **Create app** and provide an app name.
3. In the **Access** section of your new app, select the `read_*` scopes for the objects
   you want to replicate:

   - `read_orders`: orders, transactions, fulfillments (access limited to the last 60 days
     by default; `read_all_orders` extends this to full order history but requires a
     separate Shopify access request; for details, see the note below)
   - `read_products`: products, product variants, collections
   - `read_customers`: customers, segments
   - `read_inventory`: inventory items, locations
   - `read_merchant_managed_fulfillment_orders`: fulfillment orders

   For the full list of available scopes, see the [Shopify access scopes reference](https://shopify.dev/docs/api/usage/access-scopes).

   Important

   Some scopes require Shopify approval before your app can use them:

   - **`read_all_orders`**: Required to access orders older than 60 days. Submit an access
     request through your app’s **API access** settings in the Dev Dashboard.
   - **Protected customer data**: The `read_customers` scope includes customer fields (name,
     address, email, and phone) that Shopify classifies as protected customer data. Apps
     that read these fields must request access to protected customer data and meet Shopify’s
     data protection requirements. Submit an access request through your app’s **API access**
     settings in the Dev Dashboard.

   For more information, see
   [Protected customer data](https://shopify.dev/docs/apps/launch/protected-customer-data)
   in the Shopify developer documentation.

   Note

   Grant only the scopes required for the objects you intend to replicate.

   Some GraphQL fields require write scopes to read (for example, `marketingUnsubscribeUrl`
   on the `Customer` object requires `write_customers`). If you don’t grant the corresponding
   write scope, the Shopify API returns an error for that field. To avoid this, either omit
   the field from the `graphqlFields` list in the **Object Definitions Override** parameter,
   or add it to `ignoredFields`. Note that `ignoredFields` works on top-level field names
   only. For nested fields, you must remove them from the `graphqlFields` sub-selection.
4. Select **Release**. Optionally provide a version name and message, then confirm by
   selecting **Release** again.
5. On the app **Overview** page, select **Install app**. You are redirected to your store.
   Select **Install** to confirm the installation.

   Note

   If you change the app’s scopes later, you must release a new app version and reinstall
   the app on your store to apply the updated permissions.
6. Navigate to **Settings** » **Credentials** to find your **Client ID** and **Client
   Secret**. Copy both values: you need them when configuring the **Shopify Client ID** and
   **Shopify Client Secret** connector parameters.

For more information, see [Client secrets](https://shopify.dev/docs/apps/build/authentication-authorization/client-secrets)
in the Shopify developer documentation.

## Set up your Snowflake account

As an Openflow administrator, perform the following tasks to set up your Snowflake account.

### Create a Snowflake service user (Openflow - BYOC Deployments only)

Note

This step is only required if you’re deploying the connector in Openflow - BYOC Deployments. It isn’t needed for Openflow - Snowflake Deployments.

1. Create a service user:

   Copy code

   ```
   USE ROLE USERADMIN;
   CREATE USER <openflow_service_user>
     TYPE=SERVICE
     COMMENT='Service user for the Shopify connector';
   ```
2. Store the private key in a file. When configuring the connector, specify the file path. For more information, see [key pair authentication](/user-guide/key-pair-auth).

   Copy code

   ```
   ALTER USER <openflow_service_user> SET RSA_PUBLIC_KEY = '<pubkey>';
   ```

### Create database, schema, and warehouse

1. Create the destination database:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   CREATE DATABASE IF NOT EXISTS <shopify_database>;
   ```
2. Create the destination schema:

   Copy code

   ```
   CREATE SCHEMA IF NOT EXISTS <shopify_database>.<shopify_schema>;
   ```
3. Create a role for the connector and grant the required privileges:

   Copy code

   ```
   CREATE ROLE IF NOT EXISTS <shopify_connector_role>;

   GRANT USAGE ON DATABASE <shopify_database> TO ROLE <shopify_connector_role>;
   GRANT USAGE ON SCHEMA <shopify_database>.<shopify_schema> TO ROLE <shopify_connector_role>;
   GRANT CREATE TABLE ON SCHEMA <shopify_database>.<shopify_schema> TO ROLE <shopify_connector_role>;
   ```
4. Create a warehouse (or use an existing one) and grant usage privileges:

   Copy code

   ```
   CREATE WAREHOUSE IF NOT EXISTS <shopify_warehouse>
     WITH
     WAREHOUSE_SIZE = 'SMALL'
     AUTO_SUSPEND = 300
     AUTO_RESUME = TRUE;

   GRANT USAGE, OPERATE ON WAREHOUSE <shopify_warehouse> TO ROLE <shopify_connector_role>;
   ```
5. If using Openflow - BYOC Deployments, assign the role to the service user:

   Copy code

   ```
   GRANT ROLE <shopify_connector_role> TO USER <openflow_service_user>;
   ALTER USER <openflow_service_user> SET DEFAULT_ROLE = <shopify_connector_role>;
   ```

### Create a network rule (Openflow - Snowflake Deployments only)

Note

If your runtime executes in Openflow - BYOC Deployments, you don’t need to create an External Access Integration (EAI). Instead, configure your cloud network egress to allow HTTPS (port 443) access to your Shopify store domain.

To allow the connector to call the Shopify API from a Snowflake-hosted runtime, create a
network rule and an external access integration (EAI), and then grant the execute-as role usage
privileges on the EAI.

1. Create a network rule:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   CREATE OR REPLACE NETWORK RULE openflow_<runtime_name>_shopify_network_rule
     TYPE = HOST_PORT
     MODE = EGRESS
     VALUE_LIST = (
       '<your_store>.myshopify.com:443',
       'storage.googleapis.com:443'
     );
   ```
2. Create an External Access Integration:

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION openflow_<runtime_name>_shopify_eai
     ALLOWED_NETWORK_RULES = (openflow_<runtime_name>_shopify_network_rule)
     ENABLED = TRUE;
   ```
3. Grant your execute-as role USAGE on the integration:

   Copy code

   ```
   GRANT USAGE ON INTEGRATION openflow_<runtime_name>_shopify_eai
     TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```

## Install the connector

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list and click **Install**.

   Note

   Before you install the connector, ensure that you have created a database and schema in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

The Openflow canvas appears with the connector process group added to it.

## Configure the connector

To configure the connector, perform the following steps:

1. Right-click on the added connector process group and select **Parameters**.
2. Populate the required parameter values as described in the following sections.

### Shopify parameters

The following parameters configure the Shopify source connection:

| Parameter | Description |
| --- | --- |
| Shop Domain | The `myshopify.com` domain for your store.  **Example:** `mystore.myshopify.com` |
| Shopify Client ID | Client ID from your Shopify dev app. |
| Shopify Client Secret | Client Secret from your Shopify dev app. Stored securely as a sensitive parameter. |
| Shopify API Version | The Shopify Admin API version to use for requests.  **Default:** `2026-04` |
| Objects to Sync | Comma-separated or newline-separated list of Shopify object types to replicate. Case-insensitive. Each value must correspond to a query endpoint in the Shopify Admin GraphQL API (for example, `orders` corresponds to the `orders` query, `products` to the `products` query). Types not found in the built-in catalog are skipped unless a custom definition is provided through the **Object Definitions Override** parameter or **Enable Introspection** is `true`.  **Default:** `orders,products,customers,productVariants,inventoryItems,collections` |
| Objects to Track for Deletes | Comma-separated or newline-separated list of Shopify object types to monitor for deletions through the Events API. Each type is polled independently. Types not found in the registry are skipped. Leave empty to disable delete tracking entirely.  **Example:** `products, customers, collections` |
| Sync Schedule | How frequently the connector polls Shopify for new or updated data. Uses NiFi scheduling syntax.  **Default:** `30 min` |
| Deletes Schedule | How frequently the connector polls the Shopify Events API for deletion events. Uses NiFi scheduling syntax. Increase this interval to reduce API cost if delete detection latency isn’t critical.  **Default:** `15 min` |
| Object Definitions Override | Optional JSON array to add new object definitions or override existing ones in the built-in catalog. Each element fully replaces the catalog entry for that `apiType`. Use this parameter to customize which fields are extracted, define promoted columns, or register custom object types.  For more information, see [Object definition overrides](/user-guide/data-integration/openflow/connectors/shopify/object-definitions#label-shopify-object-override). |
| Enable Introspection | When `true`, unknown object types are auto-discovered by querying the Shopify Admin GraphQL introspection endpoint. Discovered definitions are cached for 24 hours.  **Default:** `true` |
| Ignore Deprecated Fields | When `true`, deprecated GraphQL fields are excluded from introspection-generated queries. Only applicable when **Enable Introspection** is `true`.  **Default:** `true` |

Expand

Show lessSee more

### Snowflake destination parameters

The following parameters configure the Snowflake destination:

| Parameter | Description |
| --- | --- |
| Snowflake Authentication Strategy | Authentication strategy for the connector to connect to Snowflake.   - `SNOWFLAKE_MANAGED` (default): Uses the Snowflake-managed token associated with the runtime’s execute-as role. Snowflake recommends this option for both Openflow - Snowflake Deployments and Openflow - BYOC Deployments. - `KEY_PAIR`: Uses a user-provided RSA key pair. Available only on Openflow - BYOC Deployments, for cross-account scenarios. |
| Snowflake Account Identifier | Snowflake account identifier, formatted as `<organization>-<account>`. Required when the authentication strategy is `KEY_PAIR`.  **Example:** `MYORG-MYACCOUNT` |
| Snowflake Username | The Snowflake user for authentication. Required when the authentication strategy is `KEY_PAIR`. |
| Snowflake Private Key | PEM-encoded private key content (PKCS8 format) for Snowflake key pair authentication. Required when the authentication strategy is `KEY_PAIR`. Stored securely as a sensitive parameter.  Either this parameter or **Snowflake Private Key File** must be defined. |
| Snowflake Private Key File | Alternative to **Snowflake Private Key**. Upload the private key file by selecting the **Reference asset** checkbox, uploading the file as an asset, and selecting the asset as the value for the parameter.  Either this parameter or **Snowflake Private Key** must be defined. |
| Snowflake Private Key Password | Password to decrypt the Snowflake private key, if the key is encrypted. Only applicable when the authentication strategy is `KEY_PAIR`. |
| Snowflake Role | The execute-as role used for table creation, data ingestion, and access verification. |
| Destination Database | Name of the destination database in Snowflake. The database must already exist before starting the connector. |
| Destination Schema | Name of the destination schema in Snowflake. The schema must already exist before starting the connector. |
| Snowflake Warehouse | The Snowflake warehouse used for table management operations such as `CREATE TABLE` and `MERGE`. |

Expand

Show lessSee more

## Run the flow

1. Right-click on an empty area of the canvas and select **Enable all Controller Services**.
2. Right-click on the connector process group and select **Start**.

The connector starts querying the Shopify Admin API and loading data into Snowflake.

## Next steps

- For more information about customizing which fields are extracted and registering custom object
  types, see [Object definition overrides for the Openflow Connector for Shopify](/user-guide/data-integration/openflow/connectors/shopify/object-definitions).
- For more information about resetting connector state, see
  [Maintain the Openflow Connector for Shopify](/user-guide/data-integration/openflow/connectors/shopify/maintain).
- For more information about monitoring the flow, see
  [Monitor Openflow using telemetry data](/user-guide/data-integration/openflow/monitor).
