# About Openflow Connector for Box

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for Box, its workflow, and limitations.

The Openflow Connector for Box connects a Box enterprise with Snowflake.

Use this connector to do the following:

- Ingest Box content for your own custom processing in Snowflake
- Ingest Box content and make it ready for chat in your AI assistants with Snowflake Cortex
- Use Box AI to extract metadata from Box content for enrichment in Snowflake
- Add enriched metadata from Snowflake to content in Box

## Workflow

1. A **Box developer** creates a Box Platform app and submits it for authorization.
2. A **Box administrator** authorizes the app.
3. The **Box developer** then performs the following tasks:

   1. Shares a Box folder with the app service account.
   2. Shares a Platform app configuration JSON file and a folder ID with a Snowflake account administrator.
4. A **Snowflake account administrator** performs the following tasks:

   1. Installs the connector.
   2. Configures the connector with Snowflake connection details and the data provided by the Box developer.
   3. Runs the connector flow. The connector does the following:
      1. Creates the required tables, stages, and a Cortex Search service in the specified Snowflake schema.
      2. Fetches Box file content and permissions from the folder specified in the connector configuration.
      3. Runs parsing and chunking on the fetched documents, and saves them in Snowflake tables. The saved chunks are automatically indexed by the Cortex Search service.
5. A **Chatbot developer** uses the Cortex Search service to build a chatbot application.

## Limitations

- [Cortex Parse Document limitations and requirements](/user-guide/snowflake-cortex/parse-document#label-parse-document-requirements)
- [Cortex Search limitations](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-overview-limitations)
- Changes caused by moving folders out of the specified root folder aren’t captured during incremental ingestion.
- The connector ingests only the supported file types and ignores others.

Note

These limitations apply to the predefined connector flow.
If the flow is customized and doesn’t use some or all of the predefined components, then these limitations may not apply.

## Next steps

[Set up the Openflow Connector for Box](/user-guide/data-integration/openflow/connectors/box/setup)
