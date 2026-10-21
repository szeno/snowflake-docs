# Make your listing AI-ready

Trusted AI starts with current data, the right tools, and governed business context. Making your listing AI-ready gives consumers all three. It also differentiates your product, lowers the barrier to adoption, and reaches new audiences beyond SQL users.

**On this page:**

1. [Prerequisites](#label-provider-listings-ai-ready-prerequisites)
2. [Choose a path and build option](#label-provider-listings-ai-ready-deployment-paths)
3. [Add AI products to your listing](#label-provider-listings-ai-ready-publish)

## Prerequisites

Before you deploy AI features in a listing, you should:

- For publicly accessible listings, be set up as a Snowflake Marketplace provider. See [Become a provider](/collaboration/provider-becoming).
- For Secure Share listings (structured data or unstructured content): have a listing with a secure share, or be ready to [create and publish a listing](/collaboration/provider-listings-creating-publishing).
- For Native App listings: have an application package built with the [Native Apps Framework](/developer-guide/native-apps/native-apps-about) with its distribution set to `EXTERNAL` and a version that has passed the [automated security scan](/developer-guide/native-apps/security-run-scan). Marketplace listings must also meet [enforced requirements](/collaboration/guidelines-reqs-for-listing-apps#label-guidelines-reqs-application-types).
- Understand the [AI product requirements](/collaboration/provider-consumer-policies#ai-product-requirements) for listings that include AI products.

## Choose a path and build option

Choose a path based on your listing’s content, then choose how to build the AI products. Structured data and unstructured content apply to Secure Share listings. The Native App path applies to Native App listings.

| Path | Build option | Use when | What you deploy |
| --- | --- | --- | --- |
| **Structured data** Consumers ask natural language questions about your tables and views. | [Automatic Data Agents](/collaboration/auto-generated-data-agents) | You want the fastest setup, and your listing description clearly describes the data domain. | Provider Studio generates a semantic view and Cortex Agent from your listing description and table schemas. Test them, then grant them to the share. |
| [Cortex Code](/user-guide/cortex-code/cortex-code-snowsight) | You want Cortex Code to build the objects for you, with your input. | Ask Cortex Code to “Help me create a semantic view and agent for my Marketplace listing.” It creates the objects and grants them to the share. |
| Manual | You need full control over metrics, business logic, or agent instructions. | Create a [semantic view](/user-guide/views-semantic/overview) and a [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents) that uses it through [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst), then grant both to the share. |
| **Unstructured content** Consumers search and ask questions about your documents, or use them as a knowledge source in their own AI apps. | [Cortex Code](/user-guide/cortex-code/cortex-code-snowsight) | You want Cortex Code to build the objects for you, with your input. | Ask Cortex Code to “Help me create a CKE and optional agent for my Marketplace listing.” It creates the objects and grants them to the share. |
| Manual | You need full control over the search service and agent. | Create a [Cortex Knowledge Extension (CKE)](/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview), a Cortex Search Service over your text content. Optionally, create a Cortex Agent with a Cortex Search tool that uses it. Grant both to the share. See [Tutorial 1: Providers set up and test a CKE](/user-guide/snowflake-cortex/cortex-knowledge-extensions/tutorials/setup-test-cke-tutorial). |
| **Native App** Ship Cortex Agents, Snowflake-managed MCP servers, and Snowpark Container Services-hosted MCP servers with your app. Consumers use app-created agents in Snowflake CoWork or through the REST, Python, and SQL APIs. See [Use Cortex Agents and MCP servers in an app](/developer-guide/native-apps/agents-mcp-servers).  To use Cortex AI functions, request the `SNOWFLAKE.CORTEX_USER` database role in your app’s manifest. See [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user). | [Cortex Code](/user-guide/cortex-code/cortex-code-snowsight) | You want Cortex Code to build the objects for you, with your input. | Ask Cortex Code to:   - `Add a Cortex Agent to my native app <APP_PACKAGE_NAME> that answers questions over the semantic view <DATABASE.SCHEMA.SEMANTIC_VIEW>.` - `Add a Snowflake-managed MCP server to my native app <APP_PACKAGE_NAME> that exposes <TOOL_NAME> as a tool.`   It creates the objects in your application package. |
| Manual | You need full control over the agent, its tools, or where they run. | Create the agent or MCP server, its tools, and the application roles that grant access. See [Cortex Agents in a Native App](/developer-guide/native-apps/agents-mcp-servers#label-native-apps-create-cortex-agent) for step-by-step instructions. Consumers run [GRANT CALLER](/sql-reference/sql/grant-caller) on any of their own objects the agent needs to access. |

Expand

Show lessSee more

## Add AI products to your listing

After you build the AI products with the option you chose, test them, add them to the share or app behind your listing, and then update the listing. These steps are the same whether you’re creating a new listing or adding AI products to an existing one.

1. **Test your AI products.** Before consumers can use them, confirm that they answer questions correctly. Complete the required roles, privileges, and authentication setup first. See [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage).
2. **Add the AI products to your share or app.** How you do this depends on your listing type:

   - **Secure Share listings:** Grant the semantic views, agents, and CKEs to your listing’s share, either on the **Secure share** tab in Provider Studio or with SQL. Cortex Code can do this for you. See [Sharing semantic views](/user-guide/views-semantic/sharing-semantic-views) and [Share Cortex Agents](/user-guide/snowflake-cortex/cortex-agents-sharing).

     For CKEs, include a `SOURCE_URL` column to enable citations and attribution. To reach consumers in other regions, enable [auto-fulfillment](/collaboration/provider-listings-auto-fulfillment).

     Caution

     CKE listings aren’t compatible with Egress Cost Optimizer (ECO), so multi-region replication can be significantly more expensive. Get a cost estimate for Cortex Search hosting and replication before you offer a CKE in multiple regions.
   - **Native App listings:** Add the AI products to your application package using the [build option](#label-provider-listings-ai-ready-deployment-paths) you chose. Then release a new version or patch of your application package. For an existing listing, consumers receive the AI features when their app upgrades.
3. **Update your listing.** Tell consumers about the AI products, then publish:

   - Add the **Cortex AI ready** category so consumers can find your listing on Snowflake Marketplace. See [Listing practices](/collaboration/provider-consumer-policies#label-listing-practices).
   - Update the description to explain what consumers can do with the AI products.
   - Publish the new listing, or publish your changes to your existing listing.
