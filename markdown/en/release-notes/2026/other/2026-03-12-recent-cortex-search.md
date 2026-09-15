# Mar 12, 2026: Recent Cortex Search updates (*Generally Available*)

The following Cortex Search features, previously available in preview, are now generally available.

## Multi-index search

Cortex Search services now support multiple searchable columns within a single service, with targeted queries to specific indexes.
For more information, see [Multi-index Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-multi-index-search).

## Custom vector embeddings

You can now create Cortex Search services that use pre-computed vector embeddings instead of, or in addition to,
Snowflake-provided embeddings for hybrid retrieval with your own or third-party models. For more information, see
[Custom vector embeddings](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-multi-index-search).

## Enhanced Cortex Search tool for Cortex Agents and Snowflake CoWork

The Cortex Search tool now supports dynamic control over search behavior via the latest Cortex search API. Its capabilities include:

- **Search service selection**: Query a single search service based on tool descriptions rather than all services, reducing latency and cost.
- **Dynamic filters**: Apply filter conditions on each search call using attribute columns.
- **Dynamic columns**: Specify which metadata columns to retrieve per search call.
- **Dynamic result count**: Set the number of results per call, up to 500.
- **Multi-index query support**: Issue per-index queries to multi-index services.

To enable this functionality, configure column descriptions in the `columns_and_descriptions` field of the Cortex Search tool resource.

For more information, see [Add tools to agents](/user-guide/snowflake-cortex/cortex-agents-manage#label-snowflake-agents-modify-agents).
