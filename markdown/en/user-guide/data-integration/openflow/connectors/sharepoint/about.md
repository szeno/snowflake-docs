# About Openflow Connector for SharePoint

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for
SharePoint, its use cases and limitations.

The Openflow Connector for SharePoint connects a Microsoft 365
SharePoint site and Snowflake to ingest files and user permissions and
keeps them up to date. Openflow Connector for SharePoint also supports
the Cortex Search service and can make ingested files ready for
conversational analysis for use in AI Assistants using SQL, Python or
REST APIs.

## Variants of the Openflow Connector for SharePoint

The Openflow Connector for SharePoint contains four variants which allow you to, optionally, index data
into Snowflake Cortex Search and include document metadata (ACLs).

|  |  |
| --- | --- |
| Variant | Description |
| Microsoft SharePoint (Cortex Search, document ACLs) | Indexes files and their permissions (ACLs) into Snowflake Cortex Search. |
| Microsoft SharePoint (Cortex Search, no document ACLs) | Indexes files without their permissions (ACLs) into Snowflake Cortex Search. |
| Microsoft SharePoint (Simple Ingest, document ACLs) | Ingests files and their permissions (ACLs) into a Snowflake stage. |
| Microsoft SharePoint (Simple Ingest, no document ACLs) | Ingests files without their permissions (ACLs) into a Snowflake stage. |

Expand

Show lessSee more

These variants appear as separate connectors in Marketplace. When installing the
connector, choose the variant that meets your requirements.

## Rate limiting restrictions

[SharePoint API limits](https://learn.microsoft.com/en-us/sharepoint/dev/embedded/development/limits-calling#api-rate-limits) govern how many requests can be made within a given time frame. If your flow exceeds the allowed quota, syncs may slow down or fail with an error. This mostly occurs when your access token makes higher number of requests than the source typically allows. In such cases, Snowflake recommends applying for higher access quota (wherever applicable) or reducing the sync frequency.

### Limitations

- [Input requirements](/user-guide/snowflake-cortex/parse-document#label-parse-document-requirements).
- [Known limitations](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-overview-limitations).
- Changes caused by moving or renaming folders aren’t captured during
  incremental ingestion.
- The connector ingests only the supported file types and ignores
  others.

### Next steps

[Set up the Openflow Connector for SharePoint](/user-guide/data-integration/openflow/connectors/sharepoint/setup)
