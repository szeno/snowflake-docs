# Make your listing AI-ready

Trusted AI starts with current data, the right tools, and governed business context. Making your listing AI-ready gives consumers all three — and differentiates your product, lowers the barrier to adoption, and reaches new audiences beyond SQL users.

Tip

After you grant an agent, semantic view, or CKE to your listing’s secure share, add the **Cortex AI ready** category to your listing. This category makes it easier for consumers to discover your listing on Snowflake Marketplace. See [Listing practices](/collaboration/provider-consumer-policies#label-listing-practices) in the provider policies.

**On this page:**

1. [Prerequisites](#label-provider-listings-ai-ready-prerequisites)
2. [Deploy AI features in your listings](#label-provider-listings-ai-ready-deployment-paths)
3. [Path 1: Structured data](#label-provider-listings-ai-ready-structured-data)
4. [Path 2: Unstructured content](#label-provider-listings-ai-ready-unstructured-content)
5. [Path 3: Native Applications](#label-provider-listings-ai-ready-native-apps)
6. [Path 4: MCP Servers (Private Preview)](#label-provider-listings-ai-ready-mcp-servers)
   - [Sharing Snowflake-managed MCP](#label-provider-listings-ai-ready-managed-mcp-sharing)
   - [Remote MCP Server listing](#label-provider-listings-ai-ready-remote-mcp)
7. [Consumer experience](#label-provider-listings-ai-ready-consumer-experience)
   - [Extending to external AI tools with Snowflake-managed MCP](#label-provider-listings-ai-ready-consumer-mcp)

## Prerequisites

Before you deploy AI features in a listing, you should:

- For publicly accessible listings, be set up as a Snowflake Marketplace provider. See [Become a provider](/collaboration/provider-becoming).
- For data listings (Paths 1 and 2): have a listing with a secure share, or be ready to [create and publish a listing](/collaboration/provider-listings-creating-publishing).
- For Native App listings (Path 3): have a Native Application built with the [Native Apps Framework](/developer-guide/native-apps/native-apps-about), or be ready to create one. Marketplace listings must meet [enforced requirements](/collaboration/guidelines-reqs-for-listing-apps#label-guidelines-reqs-application-types).
- Understand the [AI product requirements](/collaboration/provider-consumer-policies#ai-product-requirements) for listings that include AI objects.

## Deploy AI features in your listings

The following table summarizes three recommended paths for deploying AI in listings. Paths 1 and 2 apply to **data listings** (secure shares). Path 3 applies to **Native Application** listings.

| Path | Listing type | Consumer outcome | What you deploy | Your responsibilities as a provider |
| --- | --- | --- | --- | --- |
| [Path 1: Structured data](#label-provider-listings-ai-ready-structured-data) | Data listing | Consumers ask natural-language questions about KPIs, financials, and time-series data — no SQL required. | Semantic view and Cortex Agent granted to the listing’s secure share | Create or generate a semantic view and agent, grant them to the listing’s secure share, and publish the listing. |
| [Path 2: Unstructured content](#label-provider-listings-ai-ready-unstructured-content) | Data listing | Consumers search and Q&A proprietary documents without accessing raw content; integrate as a knowledge source into their own AI apps or agents. | CKE (Cortex Search Service), optionally with a Cortex Agent | Upload text content, create a Cortex Search Service, and grant it to the secure share behind your listing. Optionally, create and grant a Cortex Agent that uses the CKE as a Cortex Search tool. |
| [Path 3: Native Applications](#label-provider-listings-ai-ready-native-apps) | Native App listing | Consumers interact with a packaged AI experience embedded in your app — available in CoWork, via REST API, or through your app’s own UI. | Cortex Agents, MCP servers, and Cortex functions | Build Cortex Agents and MCP servers in your app setup script. In the application package manifest, request the Cortex database roles your app needs (such as `SNOWFLAKE.CORTEX_USER`) to access Cortex functions. |

Expand

Show lessSee more

Note

Paths 1 and 2 grant AI objects to the secure share that backs a data listing. In Provider Studio, you manage grants on the listing’s **Secure share** tab. Path 3 embeds AI capabilities in a Native Application package. The setup steps and consumer experience differ for each path.

Important

Listings that include AI objects are subject to [AI product requirements](/collaboration/provider-consumer-policies#ai-product-requirements) and are evaluated during Snowflake’s listing review process.

## Path 1: Structured data

For listings with tables or views, the recommended AI objects to create and grant to your listing’s secure share in order to make your data AI ready are semantic views and Cortex Agents. The semantic view defines your business data model, and the agent orchestrates natural language queries over it (typically through Cortex Analyst).

See below for guidance on creating these AI objects.

### Option A: Auto-generated Data Agent & Semantic Views (fastest)

For agent creation, [Automatic Data Agents](/collaboration/auto-generated-data-agents) is the fastest path. From Provider Studio, Snowflake analyzes your listing description and table schemas to automatically generate both a semantic view and a Cortex Agent. You then test and grant them to the secure share in a few clicks.

Use this option when:

- You want to get AI-ready quickly with minimal configuration.
- Your listing description clearly describes the data domain (this improves the quality of the generated agent instructions).
- You don’t already have manually created semantic views, agents, or Cortex Search Services on the share.

Automatic Data Agents works with Snowflake Marketplace listings, [Internal Marketplace](/user-guide/collaboration/listings/organizational/org-listing-about) (organizational) listings, and direct shares.

For complete instructions, see [Automatic Data Agents for listings and shares](/collaboration/auto-generated-data-agents).

### Option B: CoCo-Guided Creation (fast & more control)

Ask [CoCo in Snowsight](/user-guide/cortex-code/cortex-code-snowsight) to “Help me create a semantic view and agent for my Marketplace listings”. CoCo references all documentation instructions and best practices, creates the AI objects based on your prompt and guidance, and grants them to the secure share.

### Option C: Manual creation (most control)

Build the semantic view and agent separately when you need more control over the output. For example, when you want to incorporate existing business logic, refine metric definitions, or use query history as context.

1. **Create a semantic view.** Model business metrics, dimensions, and relationships over the tables in your listing share so Cortex Analyst can generate accurate SQL. Create the view in Snowsight (wizard or YAML) or with SQL. Before you grant it to the share, configure role-based access and grants on the semantic view and its underlying tables. For more information, see [Overview of semantic views](/user-guide/views-semantic/overview) and [Best practices for semantic views](/user-guide/views-semantic/best-practices-dev).
2. **Create a Cortex Agent.** Define an agent that orchestrates natural language requests and calls tools such as Cortex Analyst over your semantic view. Create the agent in Snowsight, with SQL, or through the REST API, then configure its tools, [model](/user-guide/snowflake-cortex/cortex-agents#models), and instructions. Before you grant it to the share, complete the required roles, privileges, and authentication setup, and test the agent in Snowsight. For more information, see [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents) and [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage).
3. **Grant to your secure share.** In Provider Studio, open your listing’s **Secure share** tab and add the semantic view and agent to the share. You can also use SQL to grant objects to the share. For more information, see [Sharing semantic views](/user-guide/views-semantic/sharing-semantic-views) and [Share Cortex Agents](/user-guide/snowflake-cortex/cortex-agents-sharing).

## Path 2: Unstructured content

If your listing contains text-based content, such as articles, market research, books, regulatory filings, forum posts, or other documents, you can share it as a [Cortex Knowledge Extension (CKE)](/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview). Optionally, you can grant a Cortex Agent to the share that uses your CKE as a Cortex Search tool.

A CKE is a knowledge source that consumers can either use with provider-supplied agents or with **their own** Cortex AI applications.

Caution

CKE listings are not compatible with Egress Cost Optimizer (ECO). Without ECO, multi-region replication to serve consumers in different Snowflake regions can be significantly more expensive. Before committing to a multi-region CKE listing, get a cost estimate for Cortex Search hosting and replication.

### Option A: CoCo-Guided Creation (fast & more control)

Ask [CoCo in Snowsight](/user-guide/cortex-code/cortex-code-snowsight) to “Help me create a CKE (and optional agent) for my Marketplace listings”. CoCo references all documentation instructions and best practices, creates the AI objects based on your prompt and guidance, and grants them to the secure share.

### Option B: Manual creation (most control)

Build the CKE and optional agent yourself when you need full control over the setup.

1. **Create a CKE.** Upload text content into a table, create a Cortex Search Service on the table, and include a `SOURCE_URL` column to enable citations and attribution. For step-by-step instructions, see [Tutorial 1: Providers set up and test a CKE](/user-guide/snowflake-cortex/cortex-knowledge-extensions/tutorials/setup-test-cke-tutorial). For more information, see [Cortex Knowledge Extensions](/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview) and [How CKE works](/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview#label-how-cke-works).
2. **Optionally create a Cortex Agent.** Define an agent in Snowsight, with SQL, or through the REST API. Add a Cortex Search tool that points at your CKE’s Cortex Search Service, and configure its [model](/user-guide/snowflake-cortex/cortex-agents#models) and instructions. Before you grant it to the share, complete the required roles, privileges, and authentication setup, and test the agent. For more information, see [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents) and [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage).
3. **Grant to your secure share.** [Create and publish a listing](/collaboration/provider-listings-creating-publishing), grant the Cortex Search Service to the secure share as the data product, and grant the agent to the share if you created one. Enable [auto-fulfillment](/collaboration/provider-listings-auto-fulfillment) to replicate the CKE to remote consumer regions.

For additional information, see [Cortex Knowledge Extensions](/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview). For tutorials, see the [CKE tutorials](/user-guide/snowflake-cortex/cortex-knowledge-extensions/overview-tutorials).

Note

Cortex Knowledge Extensions can be monetized using the on-platform [Snowflake Marketplace Monetization](/collaboration/provider-becoming#label-monetization-provider-onboarding) capability via [subscriptions](/collaboration/provider-listings-pricing-model#label-listings-subscription-pricing-model) or through [off-platform monetization](/collaboration/provider-listings-creating-publishing#label-listings-free-private-create).

## Path 3: Native Applications

If you publish a **Native Application** on Snowflake Marketplace, there are a number of ways to incorporate Cortex AI, including agent and MCP Server creation as well as native Cortex functions accessed via database roles, which consumers can grant to the application during configuration.

Use this path when:

- You want a packaged conversational or agentic experience shipped with the app.
- You need MCP tools that wrap app-owned search services, semantic views, stored procedures, or custom Snowpark Container Services endpoints.
- Your native app would benefit from [native Cortex functions](/user-guide/snowflake-cortex/aisql).

In Cortex Code, try:

`Add a Cortex Agent to my native app <APP_PACKAGE_NAME> that answers questions over the semantic view <DATABASE.SCHEMA.SEMANTIC_VIEW>.`

`Add a Snowflake-managed MCP server to my native app <APP_PACKAGE_NAME> that exposes <TOOL_NAME> as a tool.`

For setup details, see [Use Cortex Agents and MCP servers in an app](/developer-guide/native-apps/agents-mcp-servers).

Snowflake-managed MCP servers keep queries and business context inside the consumer’s governed environment — security, lineage, and auditability extend across both data and tools.

### Pattern 3A: Snowflake-native tools

**Use case:** Ship a fully packaged conversational AI experience backed by your app’s own data and logic.

Deploy a Cortex Agent and semantic view, or a Snowflake-managed MCP server that wraps app-owned objects (Cortex Search services, semantic views, UDFs, and stored procedures) as MCP tools. App-created agents appear in Snowflake CoWork automatically and are callable from the Cortex Agents REST API, Python, and SQL. The Snowflake-managed MCP server also supports external MCP clients with OAuth — consumers can connect from Cursor, Claude, ChatGPT, and other MCP-compatible tools.

Note

Consumer admin must run `GRANT CALLER` on any consumer-owned objects the agent needs to access. Without this, the agent is scoped to app-owned objects only. For details, see [GRANT CALLER](/sql-reference/sql/grant-caller).

### Pattern 3B: External SaaS bridge

**Use case:** Surface an external SaaS platform (such as Salesforce, Jira, or your own product) as a Cortex Agent inside consumer Snowflake accounts.

Deploy a Cortex Agent whose tools are stored procedures that call the external API via an External Access Integration (EAI). OAuth credentials for the external platform are stored as Snowflake secrets inside the app. The agent appears in Snowflake CoWork automatically.

Caution

This pattern does **not** expose an MCP endpoint. External tools such as Cursor and Claude cannot connect to this pattern — consumer access is through Snowflake CoWork only. The external platform must support OAuth token exchange, and user identity mapping is implemented manually per ISV with no standard SDK.

### Pattern 3C: Custom compute

**Use case:** Run ML inference, proprietary algorithms, stateful services, or any workload requiring custom compute as MCP tools.

Deploy an Snowpark Container Services container (any language or framework) running an MCP server, then register it using `CREATE CUSTOM MCP SERVER`. This registers the Snowpark Container Services ingress endpoint as MCP-discoverable — it does not deploy the container itself. Consumer access is through a Cortex Agent in Snowflake CoWork today. External MCP clients can connect via the Snowpark Container Services ingress URL, but OAuth is not yet supported for this path — direct external client access is not production-ready until OAuth ships.

Caution

The Snowpark Container Services compute pool must stay active for reliable tool responses. `AUTO_SUSPEND` is possible but introduces cold-start latency. This is the most complex build and operations path.

### Cortex functions

Native Apps that call Cortex features must declare the required [SNOWFLAKE database roles](/sql-reference/snowflake-db-roles) in the application package manifest `snowflake_database` block. These roles enable AI features for consumers after they install the listing. Declare only the roles your app needs:

- **`SNOWFLAKE.CORTEX_AGENT_USER`:** Grants access to the Cortex Agents API. Use this role when your app includes Cortex Agents. See [SNOWFLAKE.CORTEX\_AGENT\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-agent-user).
- **`SNOWFLAKE.CORTEX_USER`:** Grants access to a broader set of Cortex features beyond agents alone. See [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
- **`SNOWFLAKE.AI_FUNCTIONS_USER`:** Grants access to scalar Cortex AI functions without granting access to Cortex services such as agents or search. See [SNOWFLAKE.AI\_FUNCTIONS\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-ai-functions-user).

For manifest syntax, see the [`snowflake_database` field](/developer-guide/native-apps/manifest-reference#label-manifest-native-app-manifest-fields-snowflake-database) in the manifest reference.

Important

Do not request broad `IMPORTED PRIVILEGES` on the `SNOWFLAKE` database. Declare the specific Cortex database roles your app requires instead. Snowflake denies listings that access Cortex through broad imported privileges on the `SNOWFLAKE` database.

## Path 4: MCP Servers (Private Preview)

Two options let you bring MCP servers to Snowflake Marketplace. Both are in Private Preview.

### Sharing Snowflake-managed MCP

Providers who have built a [Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp) can share it alongside their data listings, giving consumers a ready-to-use MCP endpoint backed by the provider’s semantic views, Cortex Search Services, or other Snowflake-native tools. The server runs inside Snowflake’s security perimeter.

Private Preview

Sharing Snowflake-managed MCP servers is in Private Preview. If you are interested, contact Marketplace Operations through the case form in the top right of Provider Studio.

### Remote MCP Server listing

If you have an existing externally-hosted MCP server, you will soon be able to list it directly on Snowflake Marketplace so Snowflake customers can discover and connect to it from Snowflake CoWork and Cortex Code.

This path is distinct from Native Apps — no Snowflake application package is required. You bring your own MCP server infrastructure; Snowflake handles discovery and governance through its MCP governance layer.

Private Preview

Remote MCP Server listings are in Private Preview. To apply for early access, contact your partner manager to express interest, or reach out to Marketplace Operations from Provider Studio.

## Consumer experience

After a consumer installs your listing, the experience depends on which path you followed.

### Extending to external AI tools with Snowflake-managed MCP

Consumers who receive a data listing (Paths 1 or 2) can extend their access beyond Snowflake by creating their own Snowflake-managed MCP server. They wrap your shared semantic view or Cortex Search Service as MCP tools, creating an endpoint that external AI tools — such as Cursor, Claude, and ChatGPT — can connect to. Prompts and queries stay inside Snowflake’s security perimeter.

No additional setup is required from the provider. The quality of the consumer’s MCP experience depends on the quality of the provider’s semantic view or Cortex Search Service.

For manual setup instructions, see [Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp). CoCo-guided configuration for Snowflake-managed MCP is coming soon.

### Structured data (semantic view + agent)

The consumer opens the listing and selects the agent name to launch a conversational interface. They can ask natural language questions about your data and receive SQL-backed answers with explanations, with no query writing required.

### Unstructured content (CKE)

After a consumer installs your listing, they get access to your CKE: a shared Cortex Search Service they can use as a knowledge source in their own Cortex AI applications. End users do not interact with the CKE directly; they interact with whatever application the consumer builds or configures.

Common integration patterns include:

- **Custom RAG application:** Build a chatbot or app that queries your CKE and generates answers with citations. See [Tutorial 2: Consumer interfaces with a CKE in a Streamlit chatbot](/user-guide/snowflake-cortex/cortex-knowledge-extensions/tutorials/query-cortex-search-service-tutorial).
- **Cortex Agent in Snowflake Intelligence:** Add your CKE as a Cortex Search tool on an agent and use it in Snowflake CoWork. See [Tutorial 3: Add a CKE to Snowflake Intelligence](/user-guide/snowflake-cortex/cortex-knowledge-extensions/tutorials/add-cke-to-snowflake-cowork-tutorial).

### Native Application (agents and MCP servers in-app)

After a consumer installs your Native App listing, app-created agents are available in Snowflake CoWork and through the Cortex Agents REST API and SQL, the same as standalone agents. The app’s own UI (for example, Streamlit or an Snowpark Container Services service) may provide the primary interface for end users.

For consumer-side setup (caller grants, auditing, and access control), see [Use Cortex Agents and MCP servers in an app](/developer-guide/native-apps/agents-mcp-servers) and [Use app-created Cortex Agents and MCP servers](/developer-guide/native-apps/ui-consumer-agents-mcp).
