# Apr 15, 2026: Snowflake documentation for AI agents and LLMs

Snowflake documentation is now easier for AI coding assistants, agents, and large language models
(LLMs) to discover and consume.

**Hierarchical llms.txt**

[docs.snowflake.com/llms.txt](https://docs.snowflake.com/llms.txt) now follows a hierarchical
structure. Instead of one large file containing every page, the root file links to section-level
indexes (for example, [SQL Commands](/sql-reference/sql/llms.txt)). Agents and tools can
fetch only the sections they need, reducing token usage and improving relevance.

**Markdown versions of every page**

Every documentation page is also available in Markdown by appending `.md` to the URL. For
example:

- [CREATE TABLE](/sql-reference/sql/create-table) has a corresponding Markdown page
  [create-table.md](/sql-reference/sql/create-table).
- [Virtual warehouses](/user-guide/warehouses-overview) has a corresponding Markdown page
  [warehouses-overview.md](/user-guide/warehouses-overview).

Markdown is smaller than the equivalent HTML and strips away navigation, scripts, and other
elements that aren’t useful for LLMs. Tools such as Cortex Code, Cursor, and Claude Code can use these
URLs directly as context.
