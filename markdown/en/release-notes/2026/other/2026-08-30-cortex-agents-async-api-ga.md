# Aug 30, 2026: Cortex Agents asynchronous API (*General availability*)

The Cortex Agents asynchronous API is now generally available on AWS and Microsoft Azure.

Set the `background` field to `true` in an agent run request to start a long-running job that continues after the client disconnects, with a 6-hour timeout. You can reconnect to the run with the Stream Agent Run endpoint, or poll [THREAD\_MESSAGES (SNOWFLAKE.CORTEX)](/sql-reference/functions/thread_messages-snowflake-cortex) when you use SQL. Background runs require a thread.

For more information, see [Cortex Agents Run API](/user-guide/snowflake-cortex/cortex-agents-run).
