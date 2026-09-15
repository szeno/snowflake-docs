# About Openflow Connector for LinkedIn Ads

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts, workflow, and limitations of Openflow Connector for LinkedIn Ads.

The Openflow Connector for LinkedIn Ads enables you to ingest LinkedIn Ads metrics into Snowflake.
This connector uses the [Reporting API](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting?view=li-lms-2025-02&tabs=http) to fetch data.
The connector persists data in a table dedicated to a given report. Each report can be configured to contain metrics, pivots, and facets chosen by the user.
The connector creates the destination table in the database and the schema provided in the configuration.

Use this connector if you’re looking to do the following:

- Import campaign performance data from LinkedIn Ads to Snowflake for reporting, analytics and insights

## Workflow

1. A **LinkedIn Ads user** obtains credentials required to connect to LinkedIn Ads API.
2. A **Snowflake account administrator** performs the following tasks:
   1. Installs the connector.
   2. Configures the connector with the required parameters.
   3. Runs the connector. The following happens when the connector is run in Openflow:
      1. Retrieves the data based on the specified configuration.
         :   If the Time Granularity parameter is set to `DAILY`, then the connector downloads only the data for a
             calculated timeframe. In other cases, the connector downloads all the data from the start date to the
             current time.
      2. Creates a temporary table and inserts the downloaded data into it.
      3. Recreates or updates the destination table to reflect the schema of data from LinkedIn Ads. If you change the schema, the connector drops the destination table and recreates it with a new schema.
         If `DAILY` time granularity is chosen in the Time Granularity parameter, then outdated data is deleted from the destination table.
      4. Inserts the data into the destination table with an additional insertion timestamp.
      5. Drops the temporary table.

## Limitations

- All metrics of type BigDecimal are saved as Strings. [Conversion functions](/sql-reference/functions-conversion) allow you to convert values manually to numeric types with chosen scale and precision.
- Some metrics and pivots return values that are IDs. The connector does not use the [URN resolution](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting?view=li-lms-2025-02&tabs=http#urn-resolution).
- The connector uses the [Authorization Code Flow](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow?context=linkedin%2Fcontext&tabs=HTTPS1) because the [Client Credentials Flow](https://learn.microsoft.com/en-us/linkedin/shared/authentication/client-credentials-flow?context=linkedin%2Fcontext&tabs=HTTPS1) is not available for Marketing API. This means that the refresh token must be refreshed manually every year.
