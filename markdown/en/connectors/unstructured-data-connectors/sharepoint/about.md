# About the Snowflake Connector for SharePoint

[Preview Feature](/release-notes/preview-features) — Open

Support for this feature is available to accounts in most Snowflake regions. See [Regional availability](/connectors/unstructured-data-connectors/sharepoint/about#label-sharepoint-regional-availability) for a full list of regions.

Note

The Snowflake Connector for SharePoint is subject to the [Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Important

Thank you for your interest in the Snowflake Connector for SharePoint.
We’re now focused on a next-generation solution that will offer a significantly
improved experience; therefore, moving this connector to the general availability
status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements is not guaranteed. The new solution is available as [Openflow Connector for SharePoint](/user-guide/data-integration/openflow/connectors/sharepoint/about) and
includes better performance, customizability, and enhanced deployment options.

This topic describes the basic concepts of Snowflake Connector for SharePoint, its use cases and benefits, key features,
how it works, and limitations.

The Snowflake Connector for SharePoint connector connects a Microsoft 365 SharePoint site and Snowflake to ingest
files and user permissions and keeps them up to date.
Snowflake Connector for SharePoint also supports the Cortex Search service and can make ingested files ready for conversational
analysis for use in AI Assistants using SQL, Python or REST APIs.

## Benefits

- Frictionless ingestion: The connector is easy to set up and configure. You can use files from SharePoint
  with Cortex Search in your chat interface of choice.
- Secure by default: The connector adheres to end-user access controls in SharePoint through Cortex Search filters.
- Scalable by design: Built on the Snowflake Native App framework, the connector leverages Snowflake’s built-in security,
  scalability and reliability capabilities.
- Saves costs: The connector saves you cost by eliminating the need to manually
  transfer files or integrate against API endpoints or manage third-party solutions.

## Use cases

Use this connector if you’re looking to do the following:

- [Create AI assistants for public documents within your organization’s SharePoint site](#label-create-ai-assistants)
- [Enable your AI assistants to adhere to access controls specified in your organization’s SharePoint site](#label-create-ai-assistants-access-control)

## How it works

This section describes how this connector works with respect to the two use cases mentioned earlier.

### Create AI assistants for public documents within your organization’s SharePoint site

Working with Snowflake Connector for SharePoint for this use case can be broadly divided into four phases,
each associated with a specific user persona. The following workflow describes these phases,
the associated user journey, and how this connector works:

![Workflow for creating AI assistants for public documents within your organization's SharePoint site](/static/images/screens/sharepoint-use-case1.png)

1. An [Azure or Office 365 account administrator](https://learn.microsoft.com/en-us/microsoft-365/admin/add-users/about-admin-roles) in your organization configures [Microsoft Graph](https://learn.microsoft.com/en-us/graph/overview)
   to enable OAuth authentication as described in [Get access without a user](https://learn.microsoft.com/en-us/graph/auth-v2-service?tabs=http).
   They then share the required credentials with the organization’s data engineer.
2. A **data engineer or data scientist** in your organization installs the SharePoint Connector for Snowflake
   from the Snowflake marketplace into their Snowflake account. They then configure the connector with the following information:

   - Specifying the SharePoint OAuth credentials (ClientID, Client Secret and TenantID) obtained from step 1.
   - Specifying the URL of their SharePoint site. Typically, this is a specific subsite within your SharePoint site.
   - Choosing whether to ingest files from all folders or a specific folder in the SharePoint URL.
     Note that the files from subfolders are always included.

   After the connector validates the configuration, it does the following:

   1. Ingests supported files and user permissions from the specified source.
   2. Uses the [PARSE\_DOCUMENT function](/user-guide/snowflake-cortex/parse-document) of Cortex AI to parse and chunk the ingested files.
   3. Creates a [Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) to serve as a RAG engine for your own AI assistants with your parsed and chunked data.
3. An **IT developer** in the organization creates a chatbot in their chat interface of choice,
   such as bot extensions in Slack, Teams or a web page, and hosts it as appropriate within their environment.
   The IT Developer configures roles, permissions and authentication in Snowflake to use the Cortex Search
   REST API endpoint available in the suite of [Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api).
4. After your AI assistant is up and running, **business users** in your organization can interact with
   it to ask questions and see responses based on the files ingested from your SharePoint site into your
   Snowflake account. All responses have citations that are links to the source documents from your SharePoint site.

### Enable your AI assistants to adhere to access controls specified in your organization’s SharePoint site

Working with Snowflake Connector for SharePoint for this use case can be broadly divided into four phases,
each associated with a specific user persona. The following workflow describes these phases, the associated user journey,
and how this connector works:

![Workflow for enabling your AI assistants to adhere to access controls specified in your organization's SharePoint site](/static/images/screens/sharepoint-use-case2.png)

1. An [Azure or Office 365 account administrator](https://learn.microsoft.com/en-us/microsoft-365/admin/add-users/about-admin-roles) in your organization configures [Microsoft Graph](https://learn.microsoft.com/en-us/graph/overview)
   to enable OAuth authentication as described in [Get access without a user](https://learn.microsoft.com/en-us/graph/auth-v2-service?tabs=http).
   They then share the required credentials with the organization’s data engineer or data scientist.
2. A **data engineer or data scientist** in your organization installs the SharePoint Connector for Snowflake
   from the Snowflake marketplace into their Snowflake account. They then configure the connector by:

   - Specifying the SharePoint OAuth credentials (client ID, client secret and tenant ID) obtained in step 1.
   - Specifying the URL of their SharePoint site. Typically, this is a specific subsite within your SharePoint site.
   - Choosing whether to ingest files from all folders or a specific folder in the SharePoint URL.
     Note that the files from subfolders are always included.

   After the connector validates the configuration, it does the following:

   1. Ingests supported files and user permissions from the specified source.
   2. Uses the PARSE\_DOCUMENT function of Cortex AI to parse and chunk the ingested files.
   3. Creates a Cortex Search service to serve as a RAG engine for your own AI assistants with your parsed and chunked data.
3. An **IT developer** in the organization creates a chatbot in their chat interface of choice,
   such as bot extensions in Slack, Teams or a web page, and hosts it as appropriate within their environment.

   1. They configure roles, permissions, and authentication in Snowflake to use the Cortex Search REST API endpoint available in the suite of Snowflake REST APIs.
   2. They specify a filter containing the email ID of the SharePoint user when the AI assistant queries the Cortex Search REST API, for example `filter.@contains.user_ids` or `filter.@contains.user_emails`. This restricts responses from Cortex Search to documents that the specified business user has access to in your organization’s SharePoint.
4. After your AI assistant is up and running, when **business users** in your organization interact with it to
   ask questions, they will only see information from files in your SharePoint they have access to because of the filter specified in Step 3(b).
   All responses have citations that are links to the source documents from your SharePoint site.

## Limitations

- [Cortex Parse Document limitations and requirements](/user-guide/snowflake-cortex/parse-document#label-parse-document-requirements)
- [Cortex Search limitations](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-overview-limitations)
- Changes caused by moving or renaming folders aren’t captured during incremental ingestion.
- The connector supports only Microsoft 365 groups.
- The connector ingests only the supported file types and ignores others.

## Regional availability

The Snowflake Connector for SharePoint depends on
[Cortex Parse document](/user-guide/snowflake-cortex/parse-document) and
[Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview).

The Snowflake Connector for SharePoint is currently available in the regions listed in [Cortex Parse Document regional availability](/user-guide/snowflake-cortex/parse-document#label-parse-document-regional-availability).

## Next step

[Set up the Snowflake Connector for SharePoint](/connectors/unstructured-data-connectors/sharepoint/setup).
