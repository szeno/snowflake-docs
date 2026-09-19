# Sep 16, 2026: Cortex Agents object enhancements (*General availability*)

The following Cortex Agents object enhancements are now generally available:

- **Temporary agents**: Create session-scoped agents for testing, one-off workflows, and ephemeral pipelines by using `CREATE TEMPORARY AGENT` or `CREATE TEMP AGENT`.
- **Secure agents**: Prevent roles that can invoke or modify an agent, but don’t have its owner role activated, from retrieving the agent specification through metadata surfaces.
- **COPY GRANTS support**: Preserve explicit privileges, except OWNERSHIP, when replacing an agent with `CREATE OR REPLACE AGENT ... COPY GRANTS`.
- **Agents in Personal Databases**: Create and run an agent in the `PUBLIC` schema of your user-specific Personal Database.

For more information, see [Working with temporary agents](/user-guide/snowflake-cortex/cortex-agents-temporary), [Secure agents](/user-guide/snowflake-cortex/cortex-agents-secure), [COPY GRANTS](/sql-reference/sql/create-agent#label-create-agent-copy-grants), and [Create an agent in your Personal Database](/user-guide/snowflake-cortex/cortex-agents-manage#label-cortex-agents-personal-database).
