Categories:
:   [Table functions](/sql-reference/functions-table)

# CORTEX\_SEARCH\_BATCH

This table function submits a batch of queries to a [Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview)
for high-throughput offline use cases such as entity resolution, deduplication, audience matching, or clustering.

Batch search uses dedicated serverless compute that scales independently of interactive search traffic.
For a full guide including cost considerations, usage notes, and examples, see
[Batch Cortex Search](/user-guide/snowflake-cortex/cortex-search/batch-cortex-search).

## Syntax

Copy code

```
CORTEX_SEARCH_BATCH(
      SERVICE_NAME => '<string>'
      [, QUERY => <string_column> ]
      [, MULTI_INDEX_QUERY => <variant_column> ]
      [, FILTER => <variant_column> ]
      [, LIMIT => <integer> ]
      [, OPTIONS => <variant_column> ]
)
```

## Arguments

**Required:**

`SERVICE_NAME => 'string'`
:   Fully-qualified name of the Cortex Search service to query.

    You can specify any of the following:

    - Unqualified name (`service_name`)
    - Partially qualified name (`schema_name.service_name`)
    - Fully qualified name (`database_name.schema_name.service_name`)

**Optional:**

`QUERY => string_column`
:   Column containing query strings for searching the service.

`MULTI_INDEX_QUERY => variant_column`
:   Column containing an object that specifies one or more vector or keyword query inputs to search against
    the service index. See [multi\_index\_query](/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service#label-cortex-search-multi-query) for details.

`FILTER => variant_column`
:   Column containing filter objects to apply to the search results.

`LIMIT => integer`
:   Maximum number of results to return per query. Default: 10.

`OPTIONS => variant_column`
:   Column containing a VARIANT object with optional per-query settings. Supported keys:

    - `scoring_config`: Customize ranking for the query. See [Customize scoring](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring).
    - `replicas`: Number of index copies serving the query (default: 2). Higher values complete jobs faster.

Note

At least one of `QUERY`, `MULTI_INDEX_QUERY`, or `FILTER` must be specified.

## Output

The function returns columns from the indexed service data that match each query, including relevance scores.

## Usage notes

- Use with a `LATERAL` join to pass a column of queries from a source table.
- Reranking is not supported for batch search queries. Any reranker settings in `scoring_config` are ignored.
- Batch search can query services that are currently suspended in serving.
- Batch and interactive queries use separate compute and don’t compete for resources.
- For fewer than 2,000 queries, the interactive Cortex Search API typically provides faster results.
- Requires the same privileges as querying the Cortex Search service interactively.

For detailed usage notes and cost information, see [Batch Cortex Search](/user-guide/snowflake-cortex/cortex-search/batch-cortex-search).

## Examples

Match user-submitted product names against a golden catalog:

Copy code

```
SELECT
  q.product, s.*
FROM submitted_products AS q,
LATERAL CORTEX_SEARCH_BATCH(
    SERVICE_NAME => 'my_db.my_schema.golden_product_service',
    QUERY => q.product,
    LIMIT => 2
) AS s;
```
