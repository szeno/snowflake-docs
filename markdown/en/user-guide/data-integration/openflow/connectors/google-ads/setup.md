# Set up the Openflow Connector for Google Ads

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Google Ads.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Google Ads](/user-guide/data-integration/openflow/connectors/google-ads/about).
2. Ensure that you have [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs) or [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Google Ads](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-google-ads) connector.

## Get the credentials

As a Google Ads administrator, perform the following steps:

- Ensure that you have access to a Google Cloud project or [create a new one](https://developers.google.com/workspace/guides/create-project).
- Ensure that the [Google Ads API](https://cloud.google.com/endpoints/docs/openapi/enable-api) is
  enabled for your Google Cloud project. Google Ads API access is
  required to ingest data.
- [Configure](https://developers.google.com/google-ads/api/docs/oauth/service-accounts)
  Service account authentication for Google Ads.
- Obtain developer token for your organization following
  [instructions](https://developers.google.com/google-ads/api/docs/get-started/dev-token).

Note

Developer token should have Access Level either Basic or Standard. For more information about Access Level please see [documentation](https://developers.google.com/google-ads/api/docs/access-levels).

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

1. Create a database and schema in Snowflake for the connector to store ingested data. Grant required [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges) to the execute-as role, as described in [Set up Snowflake account](#label-google-ads-set-up-snowflake-account).

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
2. Populate the required parameter values as described in [Flow parameters](#label-google-ads-flow-parameters).

#### Flow parameters

There are three parameter contexts. *Google Ads Destination Parameters* and
*Google Ads Source Parameters* are respectively responsible for allowing
connections with GoogleAds API and Snowflake. *Google Ads Ingestion Parameters*
is used to define the reconfiguration of data downloaded from Google
Ads. *Google Ads Parameters* aggregates all of them in one.

##### Google Ads Ingestion Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Client Account ID | ID of the account in the Google Ads for which given report should be ingested | true |
| Login Customer ID | Customer ID of the Google Ads manager account (MCC) for which the report should be ingested | false |
| Google Ads Resource Name | Name of the resource in Google Ads that is a source for the report | true |
| Report Attributes | Attributes of the selected resource | true |
| Report Metrics | Metrics collected in the context of a given resource | false |
| Report Segments | Buckets in which metrics should be grouped | false |
| Report Start Date | Start date from which the ingestion should happen. The date format is YYYY-MM-DD. | false |
| Schedule | Get Google Ads Report processor schedule | true |

Expand

Show lessSee more

Note

The easiest way to obtain proper combination of *Report Attributes*, *Report Metrics* and *Report Segments* is to use [Google Ads Query Builder](https://developers.google.com/google-ads/api/fields/v19/overview_query_builder).
Select the resource based on the one inserted into parameter *Google Ads Resource Name* and construct the query. Then copy and paste attributes, metrics and segments to corresponding parameters.

##### Google Ads Source Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Google Developer Token | Developer token required to query Google Ads API | true |
| Google Service Account JSON | Service Account JSON required for Google Ads authentication | true |

Expand

Show lessSee more

##### Google Ads Destination Parameters

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

## Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

## How to reset the connector

To fully reset connector to the initial state, do the following:

1. Ensure that there are no more flow files in the queues.
2. Stop all the processors.
3. Clear the state of the initial processor.

   1. Right click on the processor `Get Google Ads Report` and select **View State**.
   2. Select the option **Clear State**. This resets the state of the processor.
4. Drop the destination table in Snowflake.
