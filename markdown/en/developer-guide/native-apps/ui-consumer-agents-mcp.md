# Use app-created Cortex Agents and MCP servers

This topic describes what consumers should know when an installed Snowflake Native App
creates Cortex Agents or MCP servers in the consumer account. It covers the
consumer workflow, best practices for safely enabling app-created agents and
MCP servers, and how to block their creation entirely with feature policies.

## User flow

For the end-to-end provider and consumer-admin workflow (creating agents,
auditing them, granting caller access, delegating to user roles, and using
the agent through Snowflake CoWork, REST, or SQL), see
[Use Cortex Agents and MCP servers in an app](/developer-guide/native-apps/agents-mcp-servers).

## Best practices for consumers

When you install a Snowflake Native App that creates Cortex Agents or MCP servers,
follow these practices:

- **Audit agent and MCP server specifications before granting access.** Use
  `DESCRIBE AGENT <app>.<schema>.<agent>` to inspect the model, tools,
  system prompt, and referenced objects. For MCP servers, use
  `DESCRIBE MCP SERVER` or `DESCRIBE CUSTOM MCP SERVER` to review the
  available tools and their descriptions. Tool descriptions are visible to
  the LLM and can influence agent behavior.
- **Understand the trust boundary of an agent’s tool context.** RBAC and
  restricted caller’s rights control access to Snowflake objects, but they
  don’t isolate tools from each other inside the same agent invocation.
  When you connect multiple MCP servers to one Cortex Agent, tool
  descriptions and tool results share the same LLM context. A response from
  one MCP server might influence how the agent uses tools from another MCP
  server, even without direct access to the other server’s data.
- **Grant caller privileges based on the app’s trust boundary.** App-created
  agents are blocked from accessing consumer objects unless you explicitly
  grant caller access. Grant only the access that matches the app’s
  intended and reviewed behavior. For sandbox tools (`code_execution` and
  `code_toolset_all`), also grant caller access on the consumer workspace
  and on the data objects that the sandbox should access. See
  [Provider: Add a Sandbox tool for Python or SQL execution](/developer-guide/native-apps/agents-mcp-servers#label-native-apps-agent-code-execution)
  and [GRANT CALLER](/sql-reference/sql/grant-caller).
- **Monitor agent activity.** Review conversation threads, tool invocations,
  and execution traces in your account.
- **Use feature policies to control agent and MCP server creation.** If you
  don’t want apps to create agents or MCP servers, use feature policies to
  block those object types at the account level or application level. See
  [Block agent and MCP server creation with feature policies](#label-native-apps-consumer-agents-mcp-feature-policies) below.

## Block agent and MCP server creation with feature policies

A consumer can prevent apps from creating Cortex Agents or MCP servers by using
a feature policy. The following example blocks all apps in the account from
creating either kind of object:

Copy code

```
CREATE FEATURE POLICY no_app_agents
  BLOCKED_OBJECT_TYPES_FOR_CREATION = (AGENTS, MCP_SERVERS);

-- Apply the policy to all apps in the account.
ALTER ACCOUNT SET FEATURE POLICY no_app_agents FOR ALL APPLICATIONS;

-- Or apply the policy to a specific app.
ALTER ACCOUNT SET FEATURE POLICY no_app_agents FOR APPLICATION my_app;
```

A consumer can also attach a feature policy when installing the application:

Copy code

```
CREATE APPLICATION my_app ... WITH FEATURE POLICY no_app_agents;
```

Block selectively by listing only the object types that you want to block. For
example, allow agents but block MCP servers, or vice versa.

For more information about feature policies, see
[Use feature policies to limit the objects an app can create](/developer-guide/native-apps/ui-consumer-feature-policies).
