# About Openflow Connector for HubSpot

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for HubSpot, its workflow, and limitations.

The Openflow Connector for HubSpot ingests HubSpot data into Snowflake. It uses the HubSpot API to retrieve data, which is then stored in a Snowflake table.
Data ingestion happens in the following two phases:

1. Initial load, where all data is retrieved during the first API call.
2. Incremental load, which merges the updates and new data into the destination table and uses timestamps from
   previous calls to limit the result to the issues that were updated since the last data load.

For more information about HubSpot private apps, see [Private apps](https://developers.hubspot.com/docs/guides/apps/private-apps/overview).

Use this connector if you’re looking to do the following:

- Get HubSpot CRM data into Snowflake for reporting, analytics, and insights

## Workflow

1. A HubSpot administrator performs the following tasks:

   1. Generates an API token within the HubSpot instance with the necessary scopes required for the API requests intended to make.
      This token is used by the connector for authentication.
   2. Defines the criteria to search objects like `Object Types` and `Updated After (optional)` fields.
2. A Snowflake account administrator performs the following tasks:

   1. Installs the connector.
   2. Configures the connector parameters:

      - Provides the HubSpot private app API token.
      - Defines the criteria for the objects being ingested by providing filters.
      - Sets the desired database and schema names within Snowflake.
   3. Runs the connector flow. Upon execution, the connector does the following:

      1. Creates an API call to fetch objects from the configured HubSpot instance.
      2. Extracts the relevant data.
      3. Creates the configured destination table in the Snowflake database if the API call returned at least one result.
      4. Loads raw data into the specified Snowflake table and creates a processed view on top of the raw data.

## Limitations

- When multiple object types are defined, filtering by ‘Updated After’ applies to all object types defined in the parameter context.
- Currently, the connector supports basic authentication using a HubSpot private app and API token.
  This means that the connector is only able to ingest data that is accessible to the owner of the API token.
- The processors are designed to work on the primary node only with one thread.
- The number of calls your private app can make is based on your account subscription. To learn more about HubSpot private app limits,
  see [Private app limits](https://developers.hubspot.com/docs/guides/apps/private-apps/overview#private-app-limits).

## Next steps

[Set up the Openflow Connector for HubSpot](/user-guide/data-integration/openflow/connectors/hubspot/setup)
