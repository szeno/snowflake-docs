# Retrieve Cortex Search

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The Retrieve Cortex Search function is a table function that lets you run low-latency Cortex Search queries from a SQL statement. It is intended for real-time use cases, where you query a Cortex Search Service one query at a time, or one query per input row.

Queries submitted to a Cortex Search Service with the `CORTEX_SEARCH_RETRIEVE` function reuse the service’s existing serving resources, the same resources that serve the Python and REST API search query surfaces. This provides low latency for individual queries, with lower overall throughput than batch search.

Common use cases for `CORTEX_SEARCH_RETRIEVE` include:

- **Retrieval-augmented generation (RAG)**: Fetch the most relevant context for a single user prompt to ground a large language model’s response.
- **Conversational search and chatbots**: Look up relevant documents in real time as users ask questions in an application.
- **In-app search experiences**: Power a search bar or lookup feature that returns results to users with low latency.
- **On-demand enrichment**: Retrieve related content for a small set of rows as part of a SQL query.

Important

`CORTEX_SEARCH_RETRIEVE` is designed for low-latency querying of one or a few queries at a time. For high-throughput or large-volume workloads, such as bulk entity resolution, deduplication, or clustering, use [Batch Cortex Search](/user-guide/snowflake-cortex/cortex-search/batch-cortex-search) instead.

## Syntax

Use the following syntax to query a Cortex Search Service using the `CORTEX_SEARCH_RETRIEVE` table function:

Copy code

```
SELECT *
FROM TABLE(CORTEX_SEARCH_RETRIEVE(
    service_name => '<database>.<schema>.<cortex_search_service>',
    query => '<query_string>',           -- optional STRING
    multi_index_query => <object>,        -- optional VARIANT
    filter => <object>,                   -- optional VARIANT
    limit => 10,                          -- optional INT
    options => <object>,                  -- optional VARIANT
    query_options => <object>             -- optional VARIANT
));
```

To run one query per input row, join the function to a source table with `LATERAL`, as shown in the examples.

## Parameters

The `CORTEX_SEARCH_RETRIEVE` function supports the following parameters:

`service_name` (string, required)
:   Fully-qualified name of the Cortex Search Service to query.

`query` (string, optional)
:   Query string for searching the service. In a `LATERAL` join, this is a column containing the query string.

`multi_index_query` (variant, optional)
:   An object that specifies one or more vector or keyword query inputs to search against the service index. See [multi\_index\_query](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-multi-index-search) for details on how to construct this parameter.

`filter` (variant, optional)
:   Filter objects to apply to the search results.

`limit` (integer, optional)
:   Maximum number of results to return per query. Default: 10.

`options` (variant, optional)
:   An object with optional per-query settings. Supported top-level keys include:

    - `scoring_config` (object, optional): Same structure as the `scoring_config` parameter for Cortex Search queries (Python and REST). Use it to customize ranking for the query, including reranker settings. See [Customizing Cortex Search scoring](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-customize-scoring).
    - `scoring_profile` (string, optional): Name of a scoring profile added to the service with `ALTER CORTEX SEARCH SERVICE ... ADD SCORING PROFILE`. You can’t specify both `scoring_profile` and `scoring_config`.

`query_options` (variant, optional)
:   An object with per-row query settings. In a `LATERAL` join, this is typically a column, so each input row can use different settings. Supported top-level keys:

    - `scoring_config` (object, optional): Same structure as the `scoring_config` parameter for Cortex Search queries (Python and REST), for example to set per-row `weights`. See [Customizing Cortex Search scoring](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-customize-scoring).

      Reranker settings can’t be set in `query_options`; the reranker is a function-level setting. To configure it, use the `options` parameter.

      If the same field is set in both `options` and `query_options`, the value in `query_options` takes precedence.

Note

At least one of `query`, `multi_index_query`, or `filter` must be specified. You can specify either `query` or `multi_index_query`, but not both.

## Output

The function returns the columns from the Cortex Search Service’s source, followed by the metadata columns in the following table. Columns with the `VECTOR` data type are not returned.

| Column | Data type | Description |
| --- | --- | --- |
| `METADATA$REQUEST_ID` | `VARCHAR` | Identifier for the search request, useful for correlating and troubleshooting individual queries. |
| `METADATA$ERROR` | `VARCHAR` | Error message if the query failed; `NULL` on success. In a `LATERAL` join, a failure for one row doesn’t stop the other rows from returning results. |
| `METADATA$RESULT_DETAIL` | `VARCHAR` | A JSON string with additional detail about the result, including component scores. For example, you can extract a score with `PARSE_JSON(METADATA$RESULT_DETAIL):scores`. |

Expand

Show lessSee more

## Usage notes

- Reranking is supported. To enable it, include reranker settings in the `scoring_config` field of the `options` parameter.
- When you query the function with `LATERAL`, it runs once per input row. If the query for an individual row fails, the error appears in that row’s `METADATA$ERROR` column and the other rows still return results.
- A single Cortex Search Service can be queried with `CORTEX_SEARCH_RETRIEVE` and `CORTEX_SEARCH_BATCH` concurrently without any degradation to query performance or throughput. Separate compute resources are used to serve each type of query.
- To query a service, use a role that has the USAGE privilege on the Cortex Search Service. For more information, see [Access control privileges](/user-guide/security-access-control-privileges).
- The service’s serving layer must be running to query it. If serving was suspended automatically after inactivity, the next query resumes it, which adds latency to that first query. If serving was suspended manually, resume it with [`ALTER CORTEX SEARCH SERVICE ... RESUME SERVING`](/sql-reference/sql/alter-cortex-search) before querying. For more information, see [Auto-suspend serving on inactivity](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-auto-suspend-serving). (Batch search, by contrast, can query a service whose serving is suspended.)
- `CORTEX_SEARCH_RETRIEVE` isn’t supported for shared services (services accessed through a share, listing, or data application). For these services, use the per-query [Cortex Search Python or REST API](/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service) instead.

## Cost considerations

`CORTEX_SEARCH_RETRIEVE` reuses the Cortex Search Service’s existing serving resources, so it’s billed as part of your existing Cortex Search Service usage and doesn’t incur the separate serving cost or query embedding cost that batch search does. The SQL statement that runs the function also consumes virtual warehouse compute.

For more information on Cortex Search costs, see [Cost considerations](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-cost-considerations).

## Regional availability

`CORTEX_SEARCH_RETRIEVE` has the same regional availability as [Batch Cortex Search](/user-guide/snowflake-cortex/cortex-search/batch-cortex-search#regional-availability): it’s available in all regions where Cortex Search is available.
See [Regional availability](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-overview-regional-availability) for a full list of supported regions.

## Example Usage

The following example queries a Cortex Search Service for the 10 results most relevant to a single query:

Copy code

```
SELECT *
FROM TABLE(CORTEX_SEARCH_RETRIEVE(
    service_name => 'my_db.my_schema.my_search_service',
    query => 'how do I file an expense report',
    limit => 10
));
```

The following example runs a search for each row in a table of questions, returning the two closest results for each. The function is joined to the source table with `LATERAL`, so it runs once per input row:

Copy code

```
SELECT
    q.question_text,
    cs.*
FROM user_questions AS q,
LATERAL CORTEX_SEARCH_RETRIEVE(
    service_name => 'my_db.my_schema.my_search_service',
    query => q.question_text,
    limit => 2
) AS cs;
```

The following example uses `query_options` to apply different scoring weights to each row. Each row in `user_questions` has a `query_options` column that holds an object such as `{'scoring_config': {'weights': {'texts': 3, 'vectors': 1}}}`:

Copy code

```
SELECT
    q.question_text,
    cs.*
FROM user_questions AS q,
LATERAL CORTEX_SEARCH_RETRIEVE(
    service_name => 'my_db.my_schema.my_search_service',
    query => q.question_text,
    query_options => q.query_options,
    limit => 2
) AS cs;
```

Because `CORTEX_SEARCH_RETRIEVE` is a table function, you can combine it with standard SQL constructs such as `JOIN`, `GROUP BY`, and window functions. The following example searches a knowledge base for the best-matching article for each open support ticket, then joins the results with a `customers` table to count how many tickets per customer tier are covered by each article. This kind of per-tier aggregation isn’t possible with the REST or Python query APIs.

Copy code

```
SELECT
    cs.article_title,
    c.tier,
    COUNT(DISTINCT t.ticket_id) AS tickets_covered
FROM open_tickets AS t
JOIN customers AS c ON t.customer_id = c.customer_id,
LATERAL CORTEX_SEARCH_RETRIEVE(
    service_name => 'my_db.my_schema.knowledge_base_service',
    query => t.issue_description,
    limit => 1
) AS cs
GROUP BY cs.article_title, c.tier
ORDER BY tickets_covered DESC;
```
