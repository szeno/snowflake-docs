# November 4, 2026: Background runs and additional supplementary tools for agents in the Snowflake-managed MCP server

In the Snowflake-managed MCP server, `CORTEX_AGENT_RUN` and `CODING_AGENT` tools now have a `"background"` boolean argument; if set to `true`, the tool returns immediately with a handle that can be polled.

In MCP servers which have at least one tool of the `CORTEX_AGENT_RUN` or `CODING_AGENT` types, Snowflake now automatically adds three supplementary tools. `ASYNC_AGENT_RUN_STATUS` and `ASYNC_AGENT_RUN_CANCEL` allow polling or canceling a run using its handle. `AGENT_RUN_RESULT` reads the reply of any agent run, using a run handle. With the `content_cel_filter` tool parameter (also newly added to `CORTEX_AGENT_RUN` and `CODING_AGENT`), a client can request an `outline` first and then read only the blocks it needs.

For more information, see [Cortex Agent supplementary tools](/user-guide/snowflake-cortex/cortex-agents-mcp#label-cortex-mcp-agent-supplementary-tools), [Run an agent tool in the background](/user-guide/snowflake-cortex/cortex-agents-mcp#label-cortex-mcp-background-agent-run), and [CREATE MCP SERVER](/sql-reference/sql/create-mcp-server).
