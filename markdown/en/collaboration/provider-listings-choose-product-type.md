# Choose a product type for your Snowflake Marketplace listing

**On this page:**

1. [Overview of the Snowflake Marketplace and product types](#label-provider-listings-choose-product-type-snowflake-types)
2. [Considerations for product types](#label-provider-listings-choose-product-type-types)
3. [Match product types to use cases](#label-provider-listings-choose-product-type-use-cases)

## Overview of the Snowflake Marketplace and product types

On the Snowflake Marketplace, providers can share and monetize data, code and functions, applications, semantic views, and agents as one live, governed, zero-copy source of truth across clouds and regions.

The Snowflake Marketplace supports three product types in listings: **Secure Share**, **Native App**, and **Connected App**. Choose the product type that fits what your consumers need, your business goals, and your security model.

- A **Secure Share** delivers live data. Consumers see your updates automatically, without you resending or republishing anything.
- A **Native App** delivers data and code as a versioned, installable product. Within Native Apps, **Declarative Sharing** offers a simplified, YAML-configured way to package data with notebooks, stored procedures, UDFs, and Cortex Agents. A full Native App adds setup scripts, custom UIs, and container workloads.
- A **Connected App** is an external SaaS application that integrates with Snowflake.

The following table lists the product types permitted on the Snowflake Marketplace and their typical use cases:

| Product type | Description | Best for | AI-ready capabilities | Get started |
| --- | --- | --- | --- | --- |
| **Secure Share** | Live, read-only sharing of tables, views, semantic views, and secure UDFs. | Organizations beginning data monetization or with simple sharing needs. | Grant semantic views, Cortex Agents, or Cortex Knowledge Extensions (Cortex Search Services) to the share so consumers can ask questions in natural language through Cortex Code and Snowflake CoWork. | In Cortex Code, try:  `Help me create a data share listing for the Snowflake Marketplace for <USE_CASE>.`   - [Prepare data for a listing](/collaboration/provider-listings-preparing) - [Create and publish a listing](/collaboration/provider-listings-creating-publishing) |
| **Native App (Declarative Sharing)** | Tables, views, semantic views, stored procedures, UDFs, Cortex Agents, and workspaces with runnable notebooks, delivered as a single installable product. | Data providers ready to add value through guided experiences and documentation. | Package semantic views and Cortex Agents with your data so consumers can ask questions in natural language through Cortex Code and Snowflake CoWork. | In Cortex Code, try:  `Help me create a Native App (Declarative Sharing) listing for the Snowflake Marketplace for <USE_CASE>.`   - [About declarative sharing](/developer-guide/declarative-sharing/about) |
| **Native App** | Packaged applications created, owned, and maintained by the provider that get installed directly into the consumer account. | Organizations building complex products with advanced capabilities. | Include Cortex Agents and MCP servers that offer a conversational experience over shared data and functionality, and expose tools to other agents inside or outside Snowflake. | In Cortex Code, try:  `Help me create a Native App listing for the Snowflake Marketplace for <USE_CASE>.`   - [About the Native App Framework](/developer-guide/native-apps/native-apps-about) - [Native Apps workflow](/developer-guide/native-apps/native-apps-workflow) |
| **Connected App** | External SaaS applications that connect to a consumer’s Snowflake account to read or ingest data. | Existing SaaS products with a primary UI outside Snowflake; real-time or operational workflows. | Integrate Snowflake-hosted language models or Cortex Agents into your external SaaS application through REST APIs. See [Cortex REST API](/user-guide/snowflake-cortex/cortex-rest-api) and [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents). | In Cortex Code, try:  `Help me understand considerations if I want to create a Connected App listing for the Snowflake Marketplace for <APPLICATION_NAME>.`   - [How Connected Applications work](https://www.snowflake.com/en/blog/powered-by-snowflake-how-connected-applications-work/) |

Expand

Show lessSee more

Why make your listing AI-ready

Secure Share and Native App listings support AI products. Semantic views, Cortex Agents, and Cortex Knowledge Extensions let consumers ask questions in natural language through Cortex Code and Snowflake CoWork. Native Apps can also expose tools to other agents inside or outside of Snowflake through MCP servers. The power of AI unlocks new audiences, such as executives, product managers, marketers, and operations teams, and new use cases from the same dataset.

See [Make your listing AI-ready](/collaboration/provider-listings-ai-ready) for guidance by product type.

## Considerations for product types

Important

Choose your product type before you publish. You can’t replace the share or app attached to a published listing, but you can update the objects inside a share. Notify consumers before making changes that could break their workloads. See [Modify published listings](/collaboration/provider-listings-modifying).

| Product type | Security model | Provider builds | Considerations |
| --- | --- | --- | --- |
| **Secure Share** | Data remains in the provider’s account. No data is copied or transferred. Consumers access a read-only database through Snowflake’s services layer, governed by Snowflake access controls. | Secure share objects and grants | - One secure share per listing. For more information, see [Configure listings](/collaboration/provider-listings-reference#label-listings-data-product). - Read-only. Supports secure UDFs; stored procedures and runnable notebooks require Declarative Sharing or a Native App. You can still [attach a view-only notebook](/collaboration/provider-listings-creating-publishing#label-listings-attach-notebook-to-listing) to any listing as a quick start example. - Lowest ongoing maintenance. Consumers see your updates automatically, without you resending or republishing anything. |
| **Native App (Declarative Sharing)** | Provider owns and maintains the application package. The consumer installs it as a database object in their account, but the app runs in a strict sandbox. It’s scoped to the provider’s package data and can’t access any other consumer account data, system resources, or external integrations. | Application package and manifest | - Supports notebooks (shared through [workspaces](/developer-guide/declarative-sharing/workspaces)), stored procedures, UDFs, and Cortex Agents. Streamlit isn’t supported. See [limitations](/developer-guide/declarative-sharing/limitations). - Requires package versioning and testing, though lighter than a full Native App. |
| **Native App** | Provider owns and maintains the application package, including data, business logic, licensing, and entitlements, in their account. The consumer installs it as a database object in their account. Consumers can grant the app access to their own data and resources, configure external integrations, and enable event sharing. | Application package, setup scripts, optional SPCS services | - Highest build and operational cost: CI/CD, upgrades, consumer support, and [enforced listing requirements](/collaboration/guidelines-reqs-for-listing-apps#label-guidelines-reqs-application-types). - See [Native App limitations](/developer-guide/native-apps/limitations) for supported clouds, regions, and framework restrictions. |
| **Connected App** | Data and processing might occur outside the consumer account. Consumers grant access from their Snowflake account to your external service. | External application and Snowflake Partner Network requirements | - [Partner Network tier, CSID, and paid listing requirements](/collaboration/guidelines-reqs-for-listing-apps#label-guidelines-reqs-connected-apps-publish) - Not the same in-account sharing model as a Secure Share listing. - Requires ongoing maintenance of your external application and its Snowflake integration. |

Expand

Show lessSee more

## Match product types to use cases

Choose the product type that fits what your consumers need. Each type suits different use cases, and many providers offer more than one, such as a Connected App alongside a Secure Share listing.

| Consumers need | Product type | Why it fits |
| --- | --- | --- |
| Read-only queries, joins, and filters on shared tables and views | Secure Share | Live data with the lowest build and maintenance effort. |
| Your proprietary logic applied in their own queries | Secure Share | Secure views and secure UDFs expose your logic without revealing the code. |
| Multi-step business logic, guided notebooks, or stored procedures packaged with the data | Native App (Declarative Sharing) | Packages data and logic in one installable product without setup scripts or a custom UI. |
| A full application UI, containerized services, or access to their own data and integrations | Native App | Supports setup scripts, Streamlit, Snowpark Container Services, and consumer-granted access. Plan for CI/CD, versioning, and consumer support. |
| Your SaaS product, with its primary UI outside Snowflake, connected to their Snowflake account | Connected App | Your external application reads or ingests data from the consumer’s account. |

Expand

Show lessSee more
