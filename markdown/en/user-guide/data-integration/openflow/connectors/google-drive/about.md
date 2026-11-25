# About Openflow Connector for Google Drive

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

The Openflow Connector for Google Drive connects a Google Workspace Shared Drive and Snowflake to ingest
files and, depending on the connector variant, user permissions. It keeps that
content up to date. Openflow Connector for Google Drive also supports the Cortex Search service and can make ingested
files ready for conversational analysis for use in AI assistants using SQL,
Python or REST APIs.

Use this connector if you’re looking to do the following:

- Ingest Google Drive content for your own custom processing in Snowflake
- Ingest Google Drive content and make it ready for chat in your AI assistants with Snowflake Cortex

## Variants of the Openflow Connector for Google Drive

The Openflow Connector for Google Drive includes variants that optionally index data into Snowflake Cortex
Search and optionally ingest document permissions (ACLs). Some variants skip
domain-wide delegation in Google Workspace.

| Variant | Description |
| --- | --- |
| Google Drive (Simple Ingest) | Ingests files and their permissions (ACLs) into a Snowflake stage. Requires domain-wide delegation. See [Set up the Openflow Connector for Google Drive](/user-guide/data-integration/openflow/connectors/google-drive/setup). |
| Google Drive (Cortex Connect) | Indexes files and their permissions (ACLs) into Snowflake Cortex Search. Requires domain-wide delegation. See [Set up the Openflow Connector for Google Drive](/user-guide/data-integration/openflow/connectors/google-drive/setup). |
| Google Drive (Simple Ingest, No Domain-wide authority, no ACLs) | Ingests files into a Snowflake stage without permissions (ACLs). Doesn’t require domain-wide delegation. This variant is in preview. See [Set up the Openflow Connector for Google Drive without domain-wide delegation (Preview)](/user-guide/data-integration/openflow/connectors/google-drive/setup-simple-ingest). |
| Google Drive (Cortex Connect, No Domain-wide authority, no ACLs) | Indexes files without permissions (ACLs) into Snowflake Cortex Search. Doesn’t require domain-wide delegation. This variant is in preview. For Google Cloud access, Snowflake setup (including Cortex Search grants), and connector parameters, see [Set up the Openflow Connector for Google Drive without domain-wide delegation (Preview)](/user-guide/data-integration/openflow/connectors/google-drive/setup-simple-ingest). |

Expand

Show lessSee more

These variants appear as separate connectors in the Openflow catalog. When you
install the connector, choose the variant that meets your requirements.

## Limitations

1. [Cortex Parse Document limitations and requirements](/user-guide/snowflake-cortex/parse-document#label-parse-document-requirements).
2. [Cortex Search limitations](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-overview-limitations).
3. Changes caused by moving or renaming folders aren’t captured during
   incremental ingestion.
4. For variants that ingest permissions (ACLs), the connector supports
   only explicit Google Permissions for Users and Groups. It doesn’t
   currently support authentication models for links shared with Anyone.
5. The connector ingests only the supported file types and ignores
   others.

Please note, the limitations are listed for the predefined versioned
flow. If the flow was customized, and it doesn’t use some of the
predefined components, the limitations related to these components won’t
apply.

## Next steps

- [Set up the Openflow Connector for Google Drive](/user-guide/data-integration/openflow/connectors/google-drive/setup)
- [Set up the Openflow Connector for Google Drive without domain-wide delegation (Preview)](/user-guide/data-integration/openflow/connectors/google-drive/setup-simple-ingest)
