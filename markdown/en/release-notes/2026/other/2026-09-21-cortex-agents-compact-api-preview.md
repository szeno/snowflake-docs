# Sep 21, 2026: Cortex Agents Compact API (*Preview*)

The Cortex Agents Compact API is now available in preview. Use the `agent:compact` endpoint to summarize a conversation and pass the compact representation to subsequent `agent:run` requests. Compacting conversation history reduces token consumption and helps conversations stay within the model context window.

The endpoint supports transcripts supplied inline and conversations stored in Cortex Agent threads.

For more information, see [Compact a Cortex Agent conversation](/user-guide/snowflake-cortex/cortex-agents-compact).
