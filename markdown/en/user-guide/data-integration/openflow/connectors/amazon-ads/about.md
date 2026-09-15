# About Openflow Connector for Amazon Ads

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for Amazon Ads,
its workflow, and limitations.

The Openflow Connector for Amazon Ads automatically ingests [Amazon Ads](https://advertising.amazon.com/) data into your Snowflake account by using
Amazon Ads [Reporting API V3](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/overview). Reporting API enables you to configure custom reports with selected
[report types](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/overview),
[columns](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/columns), filters and other groupings.

Use this connector if you’re looking to do the following:

- Bring data from Amazon Ads for Ad performance statistics and insights

## Workflow

1. A **Amazon Ads administrator** gets access to Reporting API by following the [onboarding instructions](https://advertising.amazon.com/API/docs/en-us/guides/onboarding/overview),
   [generates a refresh token](https://advertising.amazon.com/API/docs/en-us/guides/get-started/retrieve-access-token)
   and [retrieves the client ID and client secret](https://advertising.amazon.com/API/docs/en-us/guides/onboarding/create-lwa-app#retrieve-your-security-credentials).
2. 1. A **Snowflake account administrator** performs the following:
3. Installs the connector.
4. Configures the connector with the required parameters, for example refresh token, report configuration, and database and schema names.
5. Runs the connector flow. The connector does the following:

   1. Fetches the specified report as specified in the connector configuration.
   2. Creates a temporary table and puts the report chunks in it.
   3. Creates a table in the provided destination schema.
   4. Synchronises data from the temporary table to the destination table.
   5. Removes the temporary table.
6. **Marketing users** with Snowflake access can view and perform operations on the data downloaded from Amazon Ads to destination tables.

## Limitations

- The connector supports incremental ingestion only for the daily value of `Report Time Increment` parameter.
- Modification of the report definition when the processors are running might lead to data inconsistencies.
  To ensure consistency, stop the processors and clear the queues before updating the configuration.
- If the Amazon Ads API [rate limit](https://advertising.amazon.com/API/docs/en-us/reference/concepts/rate-limiting)
  is reached, the data doesn’t get ingested despite the connector attempting to pull data from the source system.

## Next steps

[Set up the Openflow Connector for Amazon Ads](/user-guide/data-integration/openflow/connectors/amazon-ads/setup)
