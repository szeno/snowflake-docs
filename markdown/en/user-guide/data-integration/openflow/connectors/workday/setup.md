# Set up the Openflow Connector for Workday

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Workday.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Workday](/user-guide/data-integration/openflow/connectors/workday/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Workday](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-workday) connector.

## Get the credentials

As a Workday administrator, perform the following actions:

1. Create a user in Workday:

   1. Go to Workday and log in as an administrator. In the Workday
      search bar, type **Create user**.
   2. Click **Create Integration System User: Task**.
   3. Enter a username and password.
2. Create a security group and add the user from step 1 to it:

   1. In the Workday search bar, type **Create Security Group**.
   2. Click **Create Security Group: Task**.
   3. Set the type to **Integration System Security Group (Unconstrained)**.
   4. Enter a Security Group Name and click **OK**.
   5. In the **Edit Integration System Security Group (Unconstrained)**
      window, add the integration system user created in Step 1 in the
      **Integration System Users** field.
3. Add domain security policies to the security group created on step 2:

   1. In the Workday search bar, type **View Security Group**.
   2. Go to **Security Group Settings** » **Maintain Domain Permissions for Security Group**.
   3. In the **Integration Permissions** section, in the Domain Security
      Policies permitting Get access field, select the security domains
      associated with the reports you want to sync.
   4. Go to the **Activate Pending Security Policy Changes** page and click
      **OK**.
4. Create an OAuth client app:

   1. In the Workday search bar, type **Register API Client**, and click
      **Register API Client for Integrations: Task**.
   2. Enter a Client Name.
   3. Click **Non-Expiring Refresh Token**.
   4. In the Scope search bar, type **System** and select it.
   5. Click **OK**.
   6. Copy the Client ID and Client Secret, then click **Done**.
5. In the **View Integration System Security Group** page, note the
   functional areas under Domain Security Policies. Then, add these as
   Scopes/Functional Areas in the API Client:

   1. In the search bar, type **View API Client**.
   2. Choose your API client from the list.
   3. In the top blue bar, click the three dots, then select **API Client** » **API Clients for Integrations**.
   4. In the **Scope (Functional Areas)** field, search for and add the
      functional areas that you noted.
6. In the same menu as before (5c), select **Manage Refresh Tokens for Integrations**.

   1. In the form, search for the ISU user and select it.
   2. Click **OK**.
   3. Click **Generate new token** and copy the refresh token details which will be used later.

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
   GRANT CREATE TABLE ON SCHEMA <destination_database>.<destination_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
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
5. If any other Snowflake users require access to the tables ingested by the
   connector (for example, for custom processing in Snowflake), grant those users the execute-as
   role.

Note

If you’re deploying the connector in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication
strategy instead of the recommended `SNOWFLAKE_MANAGED`, you’ll also grant this same execute-as
role to a service user rather than relying on the runtime’s managed token. See
[Set up key-pair authentication for Openflow - BYOC Deployments](/user-guide/data-integration/openflow/setup-openflow-byoc-key-pair-auth)
to create the service user.

## Set up the connector

As a data engineer, perform the following tasks to configure the connector:

### Install the connector

1. Create a database and schema in Snowflake for the connector to store ingested data. Grant required [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges) to the execute-as role, as described in [Set up Snowflake account](#label-workday-set-up-snowflake-account).

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
2. Populate the required parameter values as described in [Flow parameters](#label-workday-flow-parameters).

#### Flow parameters

The configuration is divided into three parameter contexts. The *Workday
Destination Parameters* and *Workday Source Parameters*
contexts are responsible for connecting with Snowflake and Workday. The
*Workday Ingestion Parameters* contains all parameters from both
configs and other parameters specific to a given report (e.g., *Report URL*).

Because the *Workday Ingestion Parameters* parameter context
contains report-specific details, new parameter contexts must be created
for each new report and process group. To create a new parameter
context, go to the menu, select **Parameter Contexts**, and add a new
context. It should inherit from both the *Workday Destination Parameters*
and *Workday Source Parameters* parameter contexts.

**Workday Destination Parameters** **parameter context**

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

**Workday Source Parameters** **parameter context**

| Parameter | Description |
| --- | --- |
| Authorization Type | Choose between *OAUTH* or *BASIC\_AUTH*. If *OAUTH* is chosen, then *OAuth Client ID, OAuth Client Secret, OAuth Refresh Token* and *OAuth Token Endpoint* must be defined. If *BASIC\_AUTH* is chosen, then *Workday Username* and *Workday Password* must be defined. |
| OAuth Client ID | The client ID of an application registered in Workday. |
| OAuth Client Secret | The client secret related to the Client ID. |
| OAuth Refresh Token | The refresh token is obtained by a user during the app registration process. It is used together with the client ID and the client secret to get an access token. |
| OAuth Token Endpoint | The token endpoint is obtained by a user during the app registration process. |
| Workday Username | The username is used to log into a Workday account. Must be set only when *BASIC\_AUTH* is chosen. |
| Workday Password | The password is associated with the Workday username. Must be set only when *BASIC\_AUTH* is chosen. |

Expand

Show lessSee more

**Workday Ingestion Parameters** **parameter context**

| Parameter | Description |
| --- | --- |
| Destination Table | The destination table where report data pulled from Workday is stored. It is created by the connector if it does not exist. |
| Report URL | A RaaS API URL to a report created in Workday. |
| Run Schedule | Run schedule on which data is retrieved from Workday and saved in Snowflake. This value is a time duration specified by a number followed by a time unit. For example, **1 second** or **5 mins**. |

Expand

Show lessSee more

## Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.
