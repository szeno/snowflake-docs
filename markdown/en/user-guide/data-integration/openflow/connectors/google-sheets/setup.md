# Set up the Openflow Connector for Google Sheets

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Google Sheets.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Google Sheets](/user-guide/data-integration/openflow/connectors/google-sheets/about).
2. Ensure that you have [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs) or [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc).
3. If using Openflow - Snowflake Deployments, ensure that you have reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Google Sheets](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-google-sheets) connector.

## Get the Google Cloud credentials and set up your Google Cloud Project

As a Google Cloud administrator, perform the following tasks:

1. Ensure that you have the following:

   - A Google user with [Super Admin permissions](https://support.google.com/a/answer/2405986?hl)
   - A [Google Cloud Project](https://developers.google.com/workspace/guides/create-project) with the following roles:
     - [Organization Policy Administrator](https://cloud.google.com/iam/docs/understanding-roles#orgpolicy.policyAdmin)
     - [Organization Administrator](https://cloud.google.com/iam/docs/understanding-roles#resourcemanager.organizationAdmin)
2. Enable service account key creation. Google disables service account key creation by default.

   This key creation policy must be turned off for Snowflake Openflow to use the service account JSON. To enable service account key creation, perform the following tasks:

   1. Log in to the [Google Cloud Console](https://console.cloud.google.com/) with a super admin account that has the Organizational Policy Admin role.
   2. Ensure that you are in the project associated with your organization, not the project in your organization.
   3. Select **Organization Policies**.
   4. Select the **Disable service account key creation** policy.
   5. Select **Manage Policy** and turn off enforcement.
   6. Select **Set Policy**.
3. [Create a service account and key](https://developers.google.com/workspace/guides/create-credentials#service-account).
4. Share the Google Sheets spreadsheet with the service account email address. The email address can be found in the service account JSON file under the *client\_email* field. Set the sharing permissions to *Viewer*.
5. Enable the Google Sheets API for your Google Cloud Project.

   For more information, see [Enable the Google Sheets API](https://developers.google.com/sheets/api/guides/concepts#enable_the_google_sheets_api).

## Set up Snowflake account

As an Openflow administrator, perform the following tasks to set up your Snowflake account. With the
default `SNOWFLAKE_MANAGED` authentication strategy, the runtime’s execute-as role is the identity
the connector uses to access Snowflake, so you grant it the following privileges.

Note

If you’re deploying the connector in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication
strategy instead of the recommended `SNOWFLAKE_MANAGED`, you’ll also grant this same execute-as
role to a service user rather than relying on the runtime’s managed token. See
[Set up key-pair authentication for Openflow - BYOC Deployments](/user-guide/data-integration/openflow/setup-openflow-byoc-key-pair-auth)
to create the service user.

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

The configuration of the connector definition is divided into three parameter contexts:

- [Google Sheets Source Parameters](#google-sheets-source-parameters): Used to establish connection with Google Sheets.
- [Google Sheets Destination Parameters](#google-sheets-destination-parameters): Used to establish connection with Snowflake.
- [Google Sheets Ingestion Parameters](#google-sheets-ingestion-parameters): Used to define the configuration of data downloaded from Google Sheets.

Note

The [Google Sheets Ingestion Parameters](#google-sheets-ingestion-parameters) parameter context contains spreadsheet-specific details,
so you must create new parameter contexts for each new spreadsheet and process group.

To create a new parameter context, go to the Openflow Canvas menu, select **Parameter Contexts** and add a new parameter context.
It inherits parameters from both the Google Sheets Destination Parameters and Google Sheets Source Parameters parameter contexts.

The following tables describe the flow parameters that you can configure based on the parameter contexts:

#### Google Sheets Destination Parameters

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

#### Google Sheets Source Parameters

| Parameter | Description |
| --- | --- |
| Service Account JSON | Contents of the file containing Service Account credentials, such as client\_id, client\_email, and private\_key. Copy the entire contents of the file. |

Expand

Show lessSee more

#### Google Sheets Ingestion Parameters

The following table lists only those parameters that are not inherited from other parameter contexts.

| Parameter | Description |
| --- | --- |
| Date Time Render Option | Determines how dates should be rendered in the output. You can select one of these options: `SERIAL_NUMBER` and `FORMATTED_STRING`. Select `SERIAL_NUMBER` only when the Value Render Option parameter is set to `UNFORMATTED_VALUE`. For more information, see [DateTimeRenderOption](https://developers.google.com/sheets/api/reference/rest/v4/DateTimeRenderOption). |
| Destination Database | The destination database in which the destination table is created. |
| Destination Schema | The destination schema in which the destination table is created. |
| Destination Table Prefix | The destination table prefix is where report data pulled from Google Sheets is stored. The connector creates one destination table for each range. If no ranges are provided then sheet names are used as table identifiers. The first row in a sheet represents the column names in the destination table. |
| Ranges | The list of ranges to retrieve from the spreadsheet. If no range is specified, all sheets in the specified spreadsheet will be downloaded. Provide each range in either [A1 or R1C1 notation](https://developers.google.com/sheets/api/guides/concepts#cell), separated by a comma. For example: `Sheet1!A1:B2,Sheet2!D4:E5,Sheet3`. |
| Run Schedule | Run schedule on which data is retrieved from Google Sheets and saved in Snowflake. By default, the timer-driven scheduling strategy is used and here the user specifies an interval, for example, `8h`. |
| Spreadsheet ID | The [unique identifier](https://developers.google.com/sheets/api/guides/concepts) for a spreadsheet. You can find it in the URL of the spreadsheet. |
| Value Render Option | Determines how values should be rendered in the output. You can select one of these options: `FORMATTED_VALUE` and `UNFORMATTED_VALUE`. If you select `FORMATTED_VALUE`, then all the columns in the destination table are of VARCHAR type. For more information, see [ValueRenderOption](https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption). |

Expand

Show lessSee more

Note

The destination table identifier is a combination of the destination table prefix and range name and must be unique.
If you download data from multiple spreadsheets, or single sheets, and ranges names are not unique, then you must specify unique destination table prefix for each flow.
The connector may fail, overwriting existing destination tables, if destination table names aren’t unique.

## Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

Note

Imported *.xlsx* must be in Google Sheets format.
If you import files, ensure that the file is converted to Google Sheets format before running flows.
Spreadsheets in any format other than Google Sheets cannot be read.
For more information, see [Convert files to Google Sheets format](https://support.google.com/docs/answer/9331167?hl=en#2.5).
