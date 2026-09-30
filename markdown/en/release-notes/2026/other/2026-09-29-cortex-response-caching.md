# Sep 29, 2026: Response caching for Cortex AI Functions

Snowflake Cortex now automatically caches and reuses the results of AI function calls. When a query makes an identical
AI\_COMPLETE call more than once, Snowflake can return the stored result instead of running inference again,
which lowers cost and speeds up query execution.

Caching is best effort and applied automatically within a single query. Cache hits are not billed, so queries
with identical rows consume fewer tokens and credits. Customers running queries with large numbers of identical rows can
benefit from significant cost savings and latency reductions.

Response caching is available for AI\_COMPLETE text calls. No action is required to benefit from it.

For more information, see [Caching for Cortex AI Functions](/user-guide/snowflake-cortex/aisql-caching).
