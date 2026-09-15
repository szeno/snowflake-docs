# Aug 28, 2026: Snowflake recommends transitioning from Cortex Analyst to Cortex Agents

Snowflake recommends transitioning to [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents), which supports every
Cortex Analyst capability with higher answer quality. Snowflake adds new natural language analytics capabilities to
Cortex Agents.

Existing applications continue to work, and the
[Cortex Analyst REST API](/user-guide/snowflake-cortex/cortex-analyst/rest-api) remains available.

## What transitioning involves

Cortex Agents uses Cortex Analyst as its tool for querying structured data, so the transition is a change to how you invoke it
rather than a rebuild:

- Your [semantic views](/user-guide/views-semantic/overview) carry over unchanged. Cortex Agents uses the same semantic views for
  SQL generation, so you don’t need to rebuild your semantic layer.
- Your [verified queries](/user-guide/views-semantic/verified-query-repository) are stored in the semantic view, so they
  continue to apply.
- Cortex Agents adds capabilities that the standalone API doesn’t offer, including retrieval over unstructured data with Cortex
  Search, tool calling, threads that maintain conversation context, and orchestration across multiple steps.

For more information, see [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents) and
[Add tools](/user-guide/snowflake-cortex/cortex-agents-manage#label-snowflake-agents-modify-agents).
