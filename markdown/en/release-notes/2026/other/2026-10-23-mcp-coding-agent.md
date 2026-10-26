# October 23, 2026: Coding agent MCP tool

Snowflake-managed MCP servers can expose a coding agent that does not require a stored agent object. Add a tool with type `CODING_AGENT` to the MCP server specification. The specification holds the agent configuration, and each call sends the user message. Snowflake adds the `code_toolset_all` tool on every run, which gives the agent a managed coding sandbox attached to the conversation thread. A call can pass `thread_id` to continue the same conversation.

For more information, see [Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp) and [CREATE MCP SERVER](/sql-reference/sql/create-mcp-server).
