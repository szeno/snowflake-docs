# Aug 26, 2026: Cortex Agents Coding Agent (*General availability*)

The Cortex Agents Coding Agent is now generally available. Add the `code_toolset_all` tool type to a Cortex Agent, and Snowflake provisions and manages a sandbox backed by the same runtime that powers Snowflake CoCo: bash, file read/write/edit, grep, glob, web search, SQL execution, and skills. Snowflake executes the tools and streams results back to your application, so you don’t build or host an agent loop yourself.

`code_toolset_all` and `code_execution` are mutually exclusive, so a single request can declare at most one of them.

For more information, see [Coding Agent](/user-guide/snowflake-cortex/cortex-agents-coding-agent).
