# Choose a data product for the Snowflake Marketplace

**On this page:**

1. [Overview of the Snowflake Marketplace and product types](#label-provider-listings-choose-data-product-snowflake-types)
2. [Why make your listing AI-ready](#label-provider-listings-choose-data-product-ai-ready)
3. [Considerations for data product types](#label-provider-listings-choose-data-product-types)
4. [Use cases and upgrade paths](#label-provider-listings-choose-data-product-use-cases)

## Overview of the Snowflake Marketplace and product types

On the Snowflake Marketplace, providers can share and monetize data, code and functions, applications, semantic views, and agents as one live, governed, zero-copy source of truth across clouds and regions. As enterprise AI adoption continues to accelerate, providers should make their data products AI-ready to drive deeper engagement with customers and reach new audiences. For more guidance, see [Make your listing AI-ready](/collaboration/provider-listings-ai-ready).

The Snowflake Marketplace supports three data product types in listings: Shares, Native Apps, and Connected Apps. Choosing the right product type depends on your business goals and security model. Start with the simplest type that meets your needs, then evolve as your customers and use cases grow.

**Share** and **Native App** are the two core packaging constructs on the Snowflake Marketplace. A Share delivers live data — changes in your account are immediately reflected for consumers. A Native App delivers code as a versioned, installable product. Within Native Apps, **Declarative Sharing** offers a simplified, YAML-configured path, while a full **Native App** provides setup scripts, custom UIs, and container workloads. **Connected Apps** are external SaaS applications that integrate with Snowflake.

The following table lists the available Snowflake data products permitted on the Snowflake Marketplace and provides their typical use cases:

| Data product | Description | Best for | AI-ready capabilities | Get started |
| --- | --- | --- | --- | --- |
| **Secure Data Share** | Traditional read-only sharing of tables and views. | Organizations beginning data monetization or with simple sharing needs. | Attach semantic models and Cortex Agents so consumers can ask questions in natural language via CoCo, CoWork, and AI-powered IDEs. | In Cortex Code, try:  `Help me create a data share listing for the Snowflake Marketplace for <USE_CASE>.`   - [Prepare data for a listing](/collaboration/provider-listings-preparing) - [Create and publish a listing](/collaboration/provider-listings-creating-publishing) |
| **Native App (Declarative Sharing)** | Notebooks, stored procedures, UDFs, tables, and views delivered as a single installable data product. | Data providers ready to add value through guided experiences and documentation. | Attach semantic models and Cortex Agents so consumers can ask questions in natural language via CoCo, CoWork, and AI-powered IDEs. | In Cortex Code, try:  `Create a declarative sharing application package with a manifest.yml for MY_DB.MY_SCHEMA.`   - [About declarative sharing](/developer-guide/declarative-sharing/about) |
| **Native App** | Packaged applications created, owned, and maintained by the provider that get installed directly into the consumer account. | Organizations building complex data products with advanced capabilities. | Include Cortex Agents and MCP servers that offer a conversational experience over shared data and functionality, and expose tools to other agents inside or outside Snowflake. | In Cortex Code, try:  `Help me create a Native App listing for the Snowflake Marketplace for <USE_CASE>.`   - [About the Native App Framework](/developer-guide/native-apps/native-apps-about) - [Native Apps workflow](/developer-guide/native-apps/native-apps-workflow) |
| **Connected App** | External SaaS applications that connect to a consumer’s Snowflake account to read or ingest data. | Existing SaaS products with a primary UI outside Snowflake; real-time or operational workflows. | Integrate Snowflake-hosted language models or Cortex Agents into your external SaaS application through REST APIs. See [Cortex REST API](/user-guide/snowflake-cortex/cortex-rest-api) and [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents). | In Cortex Code, try:  `Help me understand considerations if I want to create a Connected App listing for the Snowflake Marketplace for <APPLICATION_NAME>.`   - [How Connected Applications work](https://www.snowflake.com/en/blog/powered-by-snowflake-how-connected-applications-work/) |

Expand

Show lessSee more

Why make your listing AI-ready

Data Shares and Native Apps support AI objects. Attach semantic models and Cortex Agents to let consumers ask questions in natural language through Cortex Code (CoCo), CoWork, and AI-powered IDEs. Expose tools to other agents inside or outside of Snowflake with Native Apps. The power of AI unlocks new audiences — executives, product managers, marketers, and operations teams — and new use cases from the same dataset.

See [Make your listing AI-ready](/collaboration/provider-listings-ai-ready) for guidance by product type.

## Considerations for data product types

| Data product | Security model | Provider builds | Considerations |
| --- | --- | --- | --- |
| **Secure Share** | Data remains in the provider’s account. No data is copied or transferred — consumers access a read-only database through Snowflake’s services layer, governed by Snowflake access controls. | Secure share objects and grants | - One secure share per listing; you can’t swap shares after publish. For more information, see [Product type](/collaboration/provider-listings-reference#label-listings-data-product). - Read-only; stored procedures require a Declarative Sharing or Native App - Lowest ongoing maintenance — data changes in your account are immediately reflected for all consumers |
| **Native App (Declarative Sharing)** | Provider owns and maintains the application package. The consumer installs it as a database object in their account, but the app runs in a strict sandbox — scoped to the provider’s package data only and cannot access any other consumer account data, system resources, or external integrations. | Application package and manifest | - Functionality bounded to declarative primitives (notebooks, stored procedures, UDFs); Streamlit is not supported - Requires package versioning and testing, though lighter than a Native App |
| **Native App** | Provider owns and maintains the application package — including data, business logic, licensing, and entitlements — in their account. The consumer installs it as a database object in their account. Consumers can grant the app access to their own data and resources, configure external integrations, and enable event sharing. | Application package, setup scripts, optional SPCS services | - Highest build and operational cost: CI/CD, upgrades, consumer support, and [enforced listing requirements](/collaboration/guidelines-reqs-for-listing-apps#label-guidelines-reqs-application-types) - See [Native App limitations](/developer-guide/native-apps/limitations) for supported clouds, regions, and framework restrictions |
| **Connected App** | Data and processing might occur outside the consumer account. Consumers grant access from their Snowflake account to your external service. | External application, CSIDs, SPN validation | - [Partner Network tier, CSID, and paid listing requirements](/collaboration/guidelines-reqs-for-listing-apps#label-guidelines-reqs-connected-apps-publish) - Not the same in-account sharing model as a Secure Share listing - Requires ongoing maintenance of your external application and its Snowflake integration |

Expand

Show lessSee more

## Use cases and upgrade paths

Your listing product type depends on your security model, the build and maintenance effort relative to your available resources, and the considerations above.

Use the following table to match your use case to a product type. The **Upgrade path** column shows common next steps if your requirements expand:

| Use case | Start with | Upgrade path |
| --- | --- | --- |
| Read-only queries, joins, and filters on shared tables and views | Secure Share | Stay on a Secure Share unless consumers need stored procedures or notebooks alongside the data. Then consider a Native App (Declarative Sharing). |
| Simple functions or lightweight transforms exposed to consumers | Secure Share (views or UDFs) | Move to a Native App (Declarative Sharing) when you need stored procedures or notebooks packaged alongside the data. |
| Multi-step business logic, stateful workflows, or custom actions on shared data | Native App (Declarative Sharing) | Move to a Native App when logic outgrows declarative limits or you need a custom UI, containers, or packaged services. |
| Full application UI, containerized services, or a packaged product experience in the consumer account | Native App | Native App is typically the end state for in-account application products. Plan for CI/CD, versioning, and consumer support from the start. |
| Primary experience in an external SaaS UI with Snowflake connectivity | Connected App | If you also want in-account access to shared datasets, consider a complementary Secure Share listing alongside your Connected App. |

Expand

Show lessSee more
