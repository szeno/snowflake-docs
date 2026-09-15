# Set up the Openflow Connector for LinkedIn Ads

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for LinkedIn Ads.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for LinkedIn Ads](/user-guide/data-integration/openflow/connectors/linkedin-ads/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [LinkedIn Ads](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-linkedinads) connector.

## Get the credentials

1. As a LinkedIn Ads user, perform the following tasks:
   1. Optional: If you don’t have an ad account to run and manage campaigns, [create one](https://www.linkedin.com/help/linkedin/answer/a426102/create-an-ad-account-in-campaign-manager-as-a-new-advertiser).
   2. Ensure that the [user account](https://www.linkedin.com/help/lms/answer/a417905?trk=hc-articlePage-peopleAlsoViewed) has at least a VIEWER role on the ad account.
   3. Use the user account to apply for Advertising API access.
      For more information, see the [Microsoft quick start](https://learn.microsoft.com/en-us/linkedin/marketing/quick-start?view=li-lms-2025-02#step-1-apply-for-api-access).
   4. Obtain a [refresh token](https://learn.microsoft.com/en-us/linkedin/shared/authentication/developer-portal-tools?context=linkedin%2Fcontext#generate-a-token-in-the-developer-portal). Use `3-legged oAuth` and the `r_ads_reporting` scope.
   5. Obtain the client ID and client secret from the LinkedIn Developer Portal. These credentials are available in the **Auth** tab in [App Details](https://www.linkedin.com/developers/apps).

## Set up Snowflake account

As a Snowflake account administrator, perform the following tasks:

1. Create a new role or use an existing role.
2. Create a new Snowflake service user with the type as [SERVICE](/sql-reference/sql/create-user#label-user-type-property).
3. Grant the Snowflake service user the role you created in the previous steps.
4. Configure with [key-pair auth](/user-guide/key-pair-auth) for the Snowflake SERVICE user from step 2.
5. Snowflake strongly recommends this step. Configure a secrets manager supported by Openflow, for example, AWS, Azure, and Hashicorp, and store the public and private keys in the secret store.

   Note

   If for any reason, you do not wish to use a secrets manager, then you are responsible for safeguarding the
   public key and private key files used for key-pair authentication according to the security policies of your organization.
6. Once the secrets manager is configured, determine how you will authenticate to it. On AWS, it’s recommended that you the
   EC2 instance role associated with Openflow as this way no other secrets have to be persisted.
7. In Openflow, configure a Parameter Provider associated with this Secrets Manager, from the hamburger menu in the upper right.
   Navigate to **Controller Settings** » **Parameter Provider** and then fetch your parameter values.
8. At this point all credentials can be referenced with the associated parameter paths and no sensitive values need to be persisted within Openflow.
9. If any other Snowflake users require access to the raw ingested documents and tables ingested by the connector (for example, for custom processing in Snowflake),
   then grant those users the role created in step 1.
10. Create a database and schema in Snowflake for the connector to store ingested data. Grant required [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges) to the role created in the first step. Substitute the role placeholder with the actual value and use the following sql commands:

Copy code

```
CREATE DATABASE linkedin_destination_db;
CREATE SCHEMA linkedin_destination_db.linkedin_destination_schema;
GRANT USAGE ON DATABASE linkedin_destination_db TO ROLE <linkedin_connector_role>;
GRANT USAGE ON SCHEMA linkedin_destination_db.linkedin_destination_schema TO ROLE <linkedin_connector_role>;
GRANT CREATE TABLE ON SCHEMA linkedin_destination_db.linkedin_destination_schema TO ROLE <linkedin_connector_role>;
```

11. Create a warehouse that will be used by the connector or use an existing one. Start with the smallest warehouse size, then experiment with size depending on the number of tables being replicated,
    and the amount of data transferred. Large table numbers typically scale better with
    [multi-cluster warehouses](/user-guide/warehouses-multicluster), rather than larger warehouse sizes.
12. Ensure that the user with role used by the connector has the required privileges to use the warehouse. If that’s not the case then grant the required privileges to the role.

Copy code

```
CREATE WAREHOUSE linkedin_connector_warehouse WITH WAREHOUSE_SIZE = 'X-Small';
GRANT USAGE ON WAREHOUSE linkedin_connector_warehouse TO ROLE <linkedin_connector_role>;
```

## Set up the connector

As a data engineer, perform the following tasks to install and configure the connector:

### Install the connector

1. Create a database and schema in Snowflake for the connector to store ingested data. Grant required [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges) to the role created in the first step. Substitute the role placeholder with the actual value and use the following SQL commands:

   Copy code

   ```
   CREATE DATABASE DESTINATION_DB;
   CREATE SCHEMA DESTINATION_DB.DESTINATION_SCHEMA;
   GRANT USAGE ON DATABASE DESTINATION_DB TO ROLE <CONNECTOR_ROLE>;
   GRANT USAGE ON SCHEMA DESTINATION_DB.DESTINATION_SCHEMA TO ROLE <CONNECTOR_ROLE>;
   GRANT CREATE TABLE, CREATE PIPE ON SCHEMA DESTINATION_DB.DESTINATION_SCHEMA TO ROLE <CONNECTOR_ROLE>;
   ```

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

Note

Each process group is responsible for fetching data for a single report configuration.
To use multiple configurations on a regular schedule, create a separate process group for each report configuration.

1. Right-click on the imported process group and select **Parameters**.
2. Populate the required parameter values as described in [Flow parameters](#flow-parameters).

### Flow parameters

This section describes the flow parameters that you can configure based on the following parameter contexts:

- [Linkedin Ads Source Parameters](#linkedin-ads-source-parameters): Used to establish connection with LinkedIn Ads API.
- [Linkedin Ads Destination Parameters](#linkedin-ads-destination-parameters): Used to establish connection with Snowflake.
- [Linkedin Ads Ingestion Parameters](#linkedin-ads-ingestion-parameters): Contains all parameters from the other two parameter contexts and additional parameters specific to a given process group.
  :   Because this parameter context contains ingestion-specific details, you must create new parameter contexts for each new report and process group.

#### Linkedin Ads Source Parameters

| Parameter | Description |
| --- | --- |
| Client ID | The client ID of an application registered on LinkedIn |
| Client Secret | The client secret related to the client ID |
| Refresh Token | A user obtains the refresh token after the app registration process. They use it together with the client ID and the client secret to get an access token. |
| Token Endpoint | The token endpoint is obtained by a user during the app registration process |

Expand

Show lessSee more

#### Linkedin Ads Destination Parameters

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

#### Linkedin Ads Ingestion Parameters

The following table lists parameters that are not inherited from the other parameter contexts:

| Parameter | Description |
| --- | --- |
| Report Name | The unique name of the report. It is uppercased and used as the destination table name. |
| Start Date | Start date from which ingestion should begin. Must be in the yyyy-MM-dd format. |
| Time Granularity | Time granularity of results. Possible values:   - `ALL`: Results grouped into a single result across the entire time range of the report. - `DAILY`: Results grouped by day. - `MONTHLY`: Results grouped by month. - `YEARLY`: Results grouped by year. |
| Conversion Window | The timeframe for which data is refreshed during incremental load when `DAILY` time granularity is chosen. For example, if the [conversion window](https://www.linkedin.com/help/lms/answer/a426359) is equal to 30 days, then during the INCREMENTAL load, the ingestion starts from the date of the last successful ingestion minus 30 days.  Required when `DAILY` time granularity is specified. For other possible time granularities, such as `ALL`, `MONTHLY`, and `YEARLY`, the SNAPSHOT ingestion strategy is used. Data from the start date to the present is always downloaded, so there is no need to use a conversion window.  The conversion window can be any number from 1 to 365. |
| Metrics | Comma-separated list of metrics. Metrics are case-sensitive. For more information, see [Reporting](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting?view=li-lms-2025-03&tabs=http#metrics-available).  The `pivotValues` and `dateRange` metrics are mandatory and are automatically included by the connector.  Up to 20 metrics can be specified, including the mandatory metrics. |
| Pivots | Comma-separated list of pivots. The available pivots are as follows:   - [Analytics Finder](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting?view=li-lms-2025-03&tabs=http#analytics-finder) - [Statistics Finder](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting?view=li-lms-2025-03&tabs=http#statistics-finder)   The connector uses the Analytics Finder when zero or one pivot is specified, and switches to the Statistics Finder when two or three pivots are selected. You can use a maximum of three pivots. |
| Shares | Comma-separated list of share IDs. This parameter can be used to filter results by share ID. |
| Campaigns | Comma-separated list of campaign IDs. This parameter can be used to filter results by campaign ID. |
| Campaign Groups | Comma-separated list of campaign group IDs. This parameter can be used to filter results by campaign group ID. |
| Accounts | Comma-separated list of account IDs. This parameter can be used to filter results by account ID. |
| Companies | Comma-separated list of company IDs. This parameter can be used to filter results by company ID. |

Expand

Show lessSee more

Note

You must specify at least one of the filters, that is shares, campaigns, campaign groups, accounts, or companies.

## Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**.
   :   The connector starts the data ingestion.
