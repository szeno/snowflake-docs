# About Openflow Connector for Meta Ads

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for Meta Ads,
its workflow, and limitations.

[Meta Ads](https://www.facebook.com/business/ads) is an online advertising platform, which you can use to create and run ads to promote your
products or services on Meta products, such as Facebook and Instagram.
The Openflow Connector for Meta Ads automatically ingests Meta Ads data into your Snowflake account
by using [Meta Ads Insights API](https://developers.facebook.com/docs/marketing-api/insights).
Insights API enables you to configure custom reports with selected fields, [breakdowns](https://developers.facebook.com/docs/marketing-api/insights/breakdowns), and other aggregations.

Use this connector if you’re looking to do the following:

- Bring Meta Ads data to unify and analyze your marketing performance

## Workflow

1. A **Meta Ads administrator** performs the following:

   1. [Creates a Meta Ads app](https://developers.facebook.com/docs/development/create-an-app/).
   2. [Enables Marketing API](https://developers.facebook.com/docs/marketing-api/get-started).
   3. [Acquires a long-lived token](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/).
2. A **Snowflake account administrator** performs the following:

   1. Installs the connector.
   2. Configures the connector with the required parameters, for example long-lived token, report configuration, and database and schema names.
   3. Runs the connector flow. The connector does the following:
      1. Fetches the specified report as specified in the connector configuration.
      2. Creates a temporary table and puts the report chunks in it.
      3. Creates a table in the provided destination schema.
      4. Synchronises data from the temporary table to the destination table.
      5. Removes the temporary table.
3. **Marketing users** with Snowflake access can view and perform operations on the data downloaded from Meta Ads to destination tables.

## Limitations

- The connector supports incremental ingestion only for the daily value of `Report Time Increment` parameter.
- Modification of the report definition when the processors are running might lead to data inconsistencies.
  To ensure consistency, stop the processors and clear the queues before updating the configuration.
- If the Meta Ads API [rate limit](https://developers.facebook.com/docs/graph-api/overview/rate-limiting/#ads-insights)
  is reached, the data doesn’t get ingested even though the connector continues attempting to pull data from the source system.
  To increase the rate limit, [change the app access type](https://developers.facebook.com/docs/marketing-api/overview/rate-limiting) from `Standard access` to `Advanced access` of the Ads Management Standard Access, and enable the `ads_read` and `ads_management` [permissions](https://developers.facebook.com/docs/permissions/).
- Data can be fetched only from the past 37 months, as defined by Meta Ads.

## Next steps

[Set up the Openflow Connector for Meta Ads](/user-guide/data-integration/openflow/connectors/meta-ads/setup)
