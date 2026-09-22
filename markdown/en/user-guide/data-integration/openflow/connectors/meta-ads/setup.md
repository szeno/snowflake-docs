# Set up the Openflow Connector for Meta Ads

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Meta Ads.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Meta Ads](/user-guide/data-integration/openflow/connectors/meta-ads/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Meta Ads](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-meta-ads) connector.

## Get the credentials

As a Meta Ads administrator, perform the following actions in your Meta Ads account:

1. [Create a Meta App](https://developers.facebook.com/docs/development/create-an-app/) or ensure that you have access to one.
2. Enable [Marketing API](https://developers.facebook.com/docs/marketing-api/get-started) in the [App dashboard](https://developers.facebook.com/apps).
3. Generate a [long-lived token](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/).
4. Optional: Increase the rate limit by [changing the app access type](https://developers.facebook.com/docs/marketing-api/overview/rate-limiting) from `Standard access` to `Advanced access` of the Ads Management Standard Access. Enable the `ads_read` and `ads_management` [permissions](https://developers.facebook.com/docs/permissions/).

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

As a data engineer, perform the following tasks to install and configure the connector:

### Install the connector

1. Create a database and schema in Snowflake for the connector to store ingested data. Grant required [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges) to the execute-as role, as described in [Set up Snowflake account](#label-meta-ads-set-up-snowflake-account).

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
2. Populate the required parameter values as described in [Flow parameters](#label-meta-ads-flow-parameters).

### Flow parameters

This section describes the flow parameters that you can configure based on the following parameter contexts:

- [Meta Ads Source Parameters](#label-meta-ads-source-parameters): Used to establish connection with MetaAds API.
- [Meta Ads Destination Parameters](#label-meta-ads-destination-parameters): Used to establish connection with Snowflake.
- [Meta Ads Ingestion Parameters](#label-meta-ads-ingestion-parameters): Used to define the configuration of data downloaded from Meta Ads.

#### Meta Ads Source Parameters

| Parameter | Description |
| --- | --- |
| Access Token | Token required to request Meta Ads Insights API |

Expand

Show lessSee more

#### Meta Ads Destination Parameters

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

#### Meta Ads Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Report Name | Name of the report to be used as a destination table name. The name must be unique within the destination schema. |
| Report Object Id | Identifier of the downloaded object from Meta Ads.  Reference to API listing different object ids:  - [Ad Accounts](https://developers.facebook.com/docs/graph-api/reference/user/adaccounts) - [Ad Sets](https://developers.facebook.com/docs/marketing-api/reference/ad-account/adsets/) - [Ads](https://developers.facebook.com/docs/marketing-api/reference/ad-account/ads/) - [Campaigns](https://developers.facebook.com/docs/marketing-api/reference/ad-account/campaigns/) |
| Report Ingestion Strategy | Mode in which data is fetched, either snapshot or incremental |
| Meta Ads Version | Version of Meta Ads API used for downloading reports. Allowed value: `v22.0`. |
| Report Level | Presents the aggregation level of the result.  Possible values:  - `account` - `campaign` - `ad` - `adset`. |
| Report Fields | Comma separated list of report fields |
| Report Breakdowns | Comma separated list of report breakdowns. Full list of available breakdowns can be found [here](https://developers.facebook.com/docs/marketing-api/insights/breakdowns). |
| Report Time Increment | Level of aggregation based on the day count  Possible values:  - `1` - Daily - `3` - Every 3 days - `7` - Weekly - `monthly` - Monthly - `90` - Quarterly - `all_days` - All days; do not slice the result |
| Report Action Time | Time of action stats  Possible values:  - `conversion` - Reports action based on conversion date - `impression` - Reports action based on impression date - `mixed` - Mixed approach between conversion and impression |
| Report Click Attribution Window | Attribution window for the click action  Possible values:  - `1d_click` - `7d_click` - `28d_click` |
| Report View Attribution Window | Attribution window for the view action  Possible values:  - `1d_view` - `7d_view` - `28d_view` |
| Report Schedule | Schedule time for processor creating reports |
| Report Start Date | Start date from which the ingestion should happen. The date format is YYYY-MM-DD. |

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

   1. Right click on the processor `Create Meta Ads Report` and select **View State**.
   2. Select the option **Clear State**. This resets the state of the processor.
4. Drop the destination table in Snowflake.
