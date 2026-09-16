# Sep 1, 2026: Snowflake Native Apps: Code execution tools for Cortex Agents

Providers can now add the `code_execution` and `code_toolset_all` sandbox tools
to Cortex Agents created by a Snowflake Native App.

The following restrictions apply to every Cortex Agent that uses a sandbox
tool, not only to agents in a Snowflake Native App:

- Invoking the agent from an owner’s-rights stored procedure removes both
  sandbox tools, and no sandbox is created.
- The Python `code_execution` sandbox doesn’t run SQL. In
  `code_toolset_all`, `snowflake_sql_execute` supports only `SELECT` and
  `SHOW`.

The following restriction is specific to Snowflake Native Apps:

- Restricted caller’s rights apply for the whole lifecycle of the sandbox,
  from the workspace it mounts to the data it reads through SQL. Consumers
  grant caller access on the workspace and on the data objects the sandbox
  should access. The sandbox never runs with the app’s owner’s rights.

For more information, see
[Provider: Add a Sandbox tool for Python or SQL execution](/developer-guide/native-apps/agents-mcp-servers#label-native-apps-agent-code-execution).
