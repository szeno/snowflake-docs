# Oct 23, 2026: Retrieve Cortex Search (*Public Preview*)

Retrieve Cortex Search is now available in Public Preview. The `CORTEX_SEARCH_RETRIEVE` table
function lets you run low-latency Cortex Search queries directly from SQL, either one query
at a time or one query per input row with a `LATERAL` join.

Use it for real-time workloads such as retrieval-augmented generation, chatbots, and in-app
search. Queries reuse the service’s existing serving resources, and because the function is
a table function you can combine search results with joins, aggregations, and other SQL.

For more information, see [Retrieve Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-retrieve).
