# Set up the Openflow Connector for HubSpot

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for HubSpot.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for HubSpot](/user-guide/data-integration/openflow/connectors/hubspot/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Hubspot](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-hubspot) connector.

## Get the credentials

As a HubSpot administrator, generate a HubSpot private app token or create one in your HubSpot account. This lets you authenticate your requests to the HubSpot API.

1. Log in to your HubSpot account.
2. Navigate to **Settings** by selecting the gear icon in the top navigation bar.
3. In the left navigation, go to **Integrations** » **Private Apps**.
4. Select **Create a private app**.

   1. Enter a name for your app.
   2. Navigate to the **Scopes** tab.
   3. Select the scopes required for the API requests you intend to make. To find scopes required for the API requests, see [Scopes](https://developers.hubspot.com/docs/guides/apps/authentication/scopes).
   4. Select **Create app**.
   5. Set the required scopes for the API requests you intend to make for each endpoint.
5. Select **View access token** to view the access token. Paste the token in the connector parameters, or save it securely.

## Set up Snowflake account

As an Openflow administrator, perform the following tasks to set up your Snowflake account. With the
default `SNOWFLAKE_MANAGED` authentication strategy, the runtime’s execute-as role is the identity
the connector uses to access Snowflake, so you grant it the following privileges.

### Create database, schema, and warehouse

1. Create the destination database:

   Copy code

   ```
   USE ROLE OPENFLOW_ADMIN;
   CREATE DATABASE IF NOT EXISTS <destination_database>;
   ```
2. Create the destination schema:

   Copy code

   ```
   CREATE SCHEMA IF NOT EXISTS <destination_database>.<destination_schema>;
   ```
3. Grant the required privileges to the runtime’s execute-as role:

   Copy code

   ```
   GRANT USAGE ON DATABASE <destination_database> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT USAGE ON SCHEMA <destination_database>.<destination_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT CREATE TABLE, CREATE VIEW ON SCHEMA <destination_database>.<destination_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```
4. Create a warehouse (or use an existing one) and grant usage privileges:

   Copy code

   ```
   CREATE WAREHOUSE IF NOT EXISTS <openflow_warehouse>
     WITH
     WAREHOUSE_SIZE = 'XSMALL'
     AUTO_SUSPEND = 300
     AUTO_RESUME = TRUE;

   GRANT USAGE, OPERATE ON WAREHOUSE <openflow_warehouse> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```
5. If any other Snowflake users require access to the tables and views ingested by the
   connector (for example, for custom processing in Snowflake), grant those users the execute-as
   role.

Note

If you’re deploying the connector in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication
strategy instead of the recommended `SNOWFLAKE_MANAGED`, you’ll also grant this same execute-as
role to a service user rather than relying on the runtime’s managed token. See
[Set up key-pair authentication for Openflow - BYOC Deployments](/user-guide/data-integration/openflow/setup-openflow-byoc-key-pair-auth)
to create the service user.

## Set up the connector

As a data engineer, perform the following tasks to install and configure the connector:

### Install the connector

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list and click **Install**.

   Note

   Before you install the connector, ensure that you have created a database and schema in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

The Openflow canvas appears with the connector process group added to it.

### Configure the connector

1. Right-click on the imported process group and select **Parameters**.
2. Populate the required parameter values as described in [Flow parameters](#flow-parameters).

### Flow parameters

This section describes the flow parameters that you can configure based on the following parameter contexts:

- [HubSpot Source Parameters](#hubspot-source-parameters): Used to establish connection with HubSpot.
- [HubSpot Destination Parameters](#hubspot-destination-parameters): Used to establish connection with Snowflake.
- [HubSpot Ingestion Parameters](#hubspot-ingestion-parameters): Used to define the configuration of data downloaded from HubSpot.

#### HubSpot Source Parameters

| Parameter | Description |
| --- | --- |
| HubSpot Access Token | HubSpot Private Application access token. |

Expand

Show lessSee more

#### HubSpot Destination Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Destination Database | The database where data will be persisted. It must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase. | Yes |
| Destination Schema | The schema where data will be persisted, which must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase.  See the following examples:  - `CREATE SCHEMA SCHEMA_NAME` or `CREATE SCHEMA schema_name`: use `SCHEMA_NAME` - `CREATE SCHEMA "schema_name"` or `CREATE SCHEMA "SCHEMA_NAME"`: use `schema_name` or `SCHEMA_NAME`, respectively | Yes |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/setup-openflow-byoc#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. | Yes |
| Snowflake Account Identifier | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Snowflake account name formatted as [organization-name]-[account-name]. | Yes |
| Snowflake Private Key | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Must be the RSA private key used for authentication, formatted according to PKCS8   standards and including standard PEM headers and footers. Note that either a Snowflake Private   Key File or a Snowflake Private Key must be defined. | No |
| Snowflake Private Key File | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: The private key file must be blank. - **KEY\_PAIR**: Upload the file that contains the RSA private key used for authentication to Snowflake,   formatted according to PKCS8 standards and including standard PEM headers and footers.   The header line begins with `-----BEGIN PRIVATE`.   To upload the private key file, select the **Reference asset** checkbox. | No |
| Snowflake Private Key Password | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the password associated with the Snowflake private key file. | No |
| Snowflake Role | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Use the runtime’s execute-as role (or a child role granted to it).   You can find your execute-as role in the Openflow UI by navigating to **View Details** for your runtime. - **KEY\_PAIR**: Use a valid role configured for your service user. | Yes |
| Snowflake Username | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the username used to connect to the Snowflake instance. | Yes |
| Snowflake Warehouse | Snowflake warehouse used to run queries. | Yes |

Expand

Show lessSee more

#### HubSpot Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Object Types | List of comma-separated HubSpot object types to ingest.  Supported object type values are:  - Appointments - Calls - Campaigns - Carts - Commerce Payments - Communications - Companies - Contacts - Courses - Deals - Discounts - Emails - Fees - Feedback Submissions - Goals - Invoices - Leads - Line Items - Listings - Meetings - Notes - Orders - Postal Mail - Products - Quotes - Quote Templates - Services - Subscriptions - Tasks - Taxes - Tickets - Users |
| Updated After | Filter objects updated after specified date or time. This parameter is optional. |
| Data Ingestion Schedule | Time between the next schedule. It should have a valid time duration, such as 30 minutes or 1 hour. |

Expand

Show lessSee more

## Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

### Reconfigure the connector

You can modify the connector parameters after the connector has started ingesting data. If the issue query criteria changes, perform the following steps to make sure that the data in the destination table is consistent.

1. Stop the connector: Ensure that all Openflow processors are stopped.
2. Access configuration settings: Navigate to the connector’s configuration settings within the Snowflake Openflow interface.
3. Modify parameters: Adjust the parameters as required.
4. Clear processor state: If you are changing ingestion criteria, then Snowflake strongly recommends that you start ingestion from the beginning to keep the data in the destination table consistent. After clearing the state in the `List Fresh HubSpot Objects` processor, the connector will fetch all the objects from the beginning. Manual truncation of the destination table may be needed to prevent duplication of rows.

## Data structure and views

The connector stores data in the following two formats within your Snowflake database:

### Raw data storage

All raw HubSpot data is stored in tables with the exact names specified in the Object Types parameter. For example:

- If you configure `Products,Contacts,Companies` in the Object Types parameter, the connector creates three tables: `PRODUCTS`, `CONTACTS`, and `COMPANIES`.
- Each table contains the complete JSON payload from the HubSpot API responses.
- Raw data preserves the original structure and all metadata from HubSpot.

### Flattened views

For easier querying and analysis, the connector automatically creates flattened views for each object type:

- Each raw table has a corresponding view with the suffix `_VIEW`. For example: `PRODUCTS_VIEW`, `CONTACTS_VIEW`, and `COMPANIES_VIEW`.
- Views extract commonly used fields from the JSON payload into individual columns.
- Complex nested structures are flattened for simplified SQL queries.
