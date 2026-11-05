# October 23, 2026: Coding agent MCP tool

Snowflake-managed MCP servers can expose a coding agent that does not require a stored agent object. Add a tool with type `CODING_AGENT` to the MCP server specification. The specification holds the agent configuration, and each call sends the user message. Snowflake adds the `code_toolset_all` tool on every run, which gives the agent a managed coding sandbox attached to the conversation thread. That tool defaults to `always_ask`. A later call passes the returned `thread_id` and `message_id` as `thread_id` and `parent_message_id` to continue the same conversation. `parent_message_id` is required whenever `thread_id` is set.

For more information, see [Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp) and [CREATE MCP SERVER](/sql-reference/sql/create-mcp-server).
