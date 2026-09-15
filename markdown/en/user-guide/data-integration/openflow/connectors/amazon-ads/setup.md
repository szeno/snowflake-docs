# Set up the Openflow Connector for Amazon Ads

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Amazon Ads.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Amazon Ads](/user-guide/data-integration/openflow/connectors/amazon-ads/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you have reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Amazon Ads](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-amazon-ads) connector.

## Get the credentials

As an Amazon Ads administrator, perform the following actions:

1. Make sure that you have access to an [Amazon Ads account](https://advertising.amazon.com/).
2. [Acquire Access to Amazon Ads API](https://advertising.amazon.com/API/docs/en-us/guides/onboarding/overview) and complete the onboarding process.
3. [Get client ID and client secret](https://advertising.amazon.com/API/docs/en-us/guides/get-started/retrieve-access-token).
4. [Create an authorization grant](https://advertising.amazon.com/API/docs/en-us/guides/get-started/create-authorization-grant)
   and [retrieve a refresh token](https://advertising.amazon.com/API/docs/en-us/guides/get-started/retrieve-access-token).
5. Review the [available regions](https://advertising.amazon.com/API/docs/en-us/reference/api-overview#api-endpoints)
   and get a base URL used for requests based on the region in which you are advertising.
6. [Fetch profile IDs](https://advertising.amazon.com/API/docs/en-us/guides/get-started/retrieve-profiles) for report configuration.

## Set up Snowflake account

As a Snowflake account administrator, perform the following tasks:

1. Create a new role or use an existing role and grant the [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges).
2. Create a new Snowflake service user with the type as [SERVICE](/sql-reference/sql/create-user#label-user-type-property).
3. Grant the Snowflake service user the role you created in the previous steps.
4. Configure with [key-pair auth](/user-guide/key-pair-auth) for the Snowflake SERVICE user from step 2.
5. Snowflake strongly recommends this step. Configure a secrets manager supported by Openflow,
   for example, AWS, Azure, and Hashicorp, and store the public and private keys in the secret store.

   Note

   If for any reason, you do not wish to use a secrets manager, then you are responsible for safeguarding the
   public key and private key files used for key-pair authentication according to the security policies of your organization.

   1. Once the secrets manager is configured, determine how you will authenticate to it. On AWS, it’s recommended that you the
      EC2 instance role associated with Openflow as this way no other secrets have to be persisted.
   2. In Openflow, configure a Parameter Provider associated with this Secrets Manager, from the hamburger menu in the upper right.
      Navigate to **Controller Settings** » **Parameter Provider** and then fetch your parameter values.
   3. At this point all credentials can be referenced with the associated parameter paths and no sensitive values need to be persisted within Openflow.
6. If any other Snowflake users require access to the raw ingested documents and tables ingested by the connector (for example, for custom processing in Snowflake),
   then grant those users the role created in step 1.
7. Designate a warehouse for the connector to use. Start with the smallest warehouse size, then experiment with size depending on the number of tables being replicated,
   and the amount of data transferred. Large table numbers typically scale better with
   [multi-cluster warehouses](/user-guide/warehouses-multicluster), rather than larger warehouse sizes.

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

- [Amazon Ads source parameters](#amazon-ads-source-parameters): Used to establish connection with Amazon Ads API.
- [Amazon Ads destination parameters](#amazon-ads-destination-parameters): Used to establish connection with Snowflake.
- [Amazon Ads ingestion parameters](#amazon-ads-ingestion-parameters): Used to define the configuration of data downloaded from Amazon Ads.

#### Amazon Ads source parameters

| Parameter | Description |
| --- | --- |
| Client ID | Client ID of the Amazon Advertising account |
| Client Secret | Client secret of the Amazon Advertising account |
| OAuth Base URL | The URL of the authorization server that issues the access token  Possible values:  - <https://api.amazon.com/auth/o2/token> - <https://api.amazon.co.uk/auth/o2/token> - <https://api.amazon.co.jp/auth/o2/token> |
| Refresh Token | Refresh Token for Amazon Ads API |
| Region | Environment from which the advertising data is downloaded  Possible values:  - NA - EU - FE |

Expand

Show lessSee more

#### Amazon Ads destination parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Destination Database | The database where data will be persisted. It must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase. | Yes |
| Destination Schema | The schema where data will be persisted, which must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase.  See the following examples:  - `CREATE SCHEMA SCHEMA_NAME` or `CREATE SCHEMA schema_name`: use `SCHEMA_NAME` - `CREATE SCHEMA "schema_name"` or `CREATE SCHEMA "SCHEMA_NAME"`: use `schema_name` or `SCHEMA_NAME`, respectively | Yes |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/setup-openflow-byoc#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. | Yes |
| Snowflake Account Identifier | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Snowflake account name formatted as [organization-name]-[account-name]. | Yes |
| Snowflake Private Key | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank.   **KEY\_PAIR**: Must be the RSA private key used for authentication.  The RSA key must be formatted according to PKCS8 standards and have standard PEM headers and footers. Note that either a Snowflake Private Key File or a Snowflake Private Key must be defined. | No |
| Snowflake Private Key File | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: The private key file must be blank. - **KEY\_PAIR**: Upload the file that contains the RSA private key used for authentication to Snowflake,   formatted according to PKCS8 standards and including standard PEM headers and footers.   The header line begins with `-----BEGIN PRIVATE`.   To upload the private key file, select the **Reference asset** checkbox. | No |
| Snowflake Private Key Password | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the password associated with the Snowflake private key file. | No |
| Snowflake Role | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Use the runtime’s execute-as role (or a child role granted to it).   You can find your execute-as role in the Openflow UI by navigating to **View Details** for your runtime. - **KEY\_PAIR**: Use a valid role configured for your service user. | Yes |
| Snowflake Username | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the username used to connect to the Snowflake instance. | Yes |
| Snowflake Warehouse | Snowflake warehouse used to run queries. | Yes |

Expand

Show lessSee more

#### Amazon Ads Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Report Name | Name of the report to be used as a destination table name. The name must be unique within the destination schema. |
| Report Ad Product | Type of advertising product being reported  Possible values:  - SPONSORED\_PRODUCTS - SPONSORED\_BRANDS - SPONSORED\_DISPLAY - SPONSORED\_TELEVISION - DEMAND\_SIDE\_PLATFORM |
| Report Columns | Set of columns which will be present in the end report. The list of available columns depends on the report type and can be found in the [Amazon Ads API documentation](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/overview). For example, for the `spCampaigns` report type, the list of available columns can be found in the [Sponsored Products documentation](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/campaign#sponsored-products). |
| Report Filters | Set of filters used to trim the data returned. The list of available filters depends on the report type and can be found in the [Amazon Ads API documentation](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/overview). For example, for the `spCampaigns` report type, the list of available filters can be found in the [Sponsored Products documentation](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/campaign#sponsored-products). Filters must be in the format of `columnName=filterValue` and values must separated by a comma (`,`). For example, `campaignStatus=ENABLED,PAUSED`. |
| Report Group By | Determines the level of granularity and how the data within the report will be aggregated and presented. The list of available group by columns depends on the report type and can be found in the [Amazon Ads API documentation](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/overview). For example, for the `spCampaigns` report type, the list of available group by columns can be found in the [Sponsored Products documentation](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/campaign#sponsored-products). |
| Report Ingestion Strategy | Mode in which data is fetched, either snapshot or incremental  Possible values:  - `SNAPSHOT` - `INCREMENTAL` |
| Report Ingestion Window | Specifies the number of days, data from which should be downloaded during incremental ingestion. For example, with a 30-day report ingestion window, an incremental load starts ingestion from 30 days prior to the last successful ingestion date, unless this calculated date falls before the overall start date, in which case ingestion begins from the overall start date. If the `SNAPSHOT` ingestion strategy is used, all available data from the start date to the present is downloaded, so there is no need to use a report ingestion window. |
| Report Profile ID | The [profile ID](https://advertising.amazon.com/API/docs/en-us/guides/get-started/retrieve-profiles) associated with an advertising account in a specific marketplace |
| Report Time Unit | Date aggregation  Possible values:  - `DAILY`: Each day is represented by a one row - `SUMMARY`: The whole ingested date period is represented as one row |
| Report Type | The Amazon Ads API supports a number of [report types](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/overview). For example: [sbAds](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/ad) and [spCampaigns](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/campaign). Copy value of `reportTypeId` from the documentation and paste it into the parameter value. |
| Report Start Date | Start date from which the ingestion should happen. The date format is YYYY-MM-DD. |
| Report Schedule | Schedule time for processor creating reports. For example: `8 h` or `1 d`. The `h` represents hours and `d` days. |

Expand

Show lessSee more

Note

Data retention in the Amazon Ads API is a specific timeframe, ranging from 60
to 365 days depending on the report type, during which historical advertising
performance data is stored and accessible for retrieval.
After this period, older data may no longer be available.

## Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**.

   The connector starts the data ingestion.
