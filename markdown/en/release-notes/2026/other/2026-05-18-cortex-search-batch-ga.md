# May 18, 2026: Batch Cortex Search (*General availability*)

Batch Cortex Search is now generally available. The `CORTEX_SEARCH_BATCH` table function
lets you run millions of fuzzy-match queries against a Cortex Search Service in a single
SQL statement, with no infrastructure to manage.

Use batch search for high-throughput offline workloads such as entity resolution, audience
matching, deduplication, and clustering. It uses dedicated serverless compute that spins up
automatically and scales independently of your interactive search traffic, so batch and
real-time queries never compete for resources. You can even query services that are
currently suspended in serving, so there’s no need to keep an index actively running just
for batch jobs.

To get started, use a `LATERAL` join with `CORTEX_SEARCH_BATCH`, point it at any
existing Cortex Search Service, pass a column of queries, and get ranked results back as a
table.

For more information, see [Batch Cortex Search](/user-guide/snowflake-cortex/cortex-search/batch-cortex-search).
