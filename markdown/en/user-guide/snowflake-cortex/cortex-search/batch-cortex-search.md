# Batch Cortex Search

The Batch Cortex Search function is a table function that lets you submit a batch of queries to a Cortex Search Service. It is intended for offline use cases with high throughput requirements, such as entity resolution, deduplication, or clustering tasks.

Jobs submitted to a Cortex Search Service with the `CORTEX_SEARCH_BATCH` function leverage additional compute resources to provide significantly higher throughput (queries per second) than the interactive (Python, REST, or SEARCH\_PREVIEW) API search query surfaces.

Common use cases for batch search include:

- **Entity resolution**: Match messy or inconsistent records (such as product names, company names, or addresses) against a canonical reference dataset.
- **Audience matching**: Link customer identities across datasets by fuzzy-matching names, emails, or other attributes.
- **Deduplication**: Identify and merge near-duplicate records within a single dataset.
- **Clustering and categorization**: Assign unstructured items to the closest categories or groups in a taxonomy.
- **Bulk enrichment**: Augment large tables with related content retrieved from a knowledge base.

## Syntax

Use the following syntax to query a Cortex Search Service in batch mode using the `CORTEX_SEARCH_BATCH`
table function:

Copy code

```
SELECT
    q.query,
    r.*
FROM query_table AS q,
LATERAL CORTEX_SEARCH_BATCH(
    service_name => '<database>.<schema>.<cortex_search_service>',
    query => q.query,                   -- optional STRING
    multi_index_query => q.miq,         -- optional VARIANT
    filter => q.filter,                 -- optional VARIANT
    limit => 10,                        -- optional INT
    options => q.options                -- optional VARIANT
) AS r;
```

## Parameters

The `CORTEX_SEARCH_BATCH` function supports the following parameters:

`service_name` (string, required)
:   Fully-qualified name of the Cortex Search Service to query.

`query` (string, optional)
:   Column containing query string for searching the service.

`multi_index_query` (variant, optional)
:   An object that specifies one or more vector or keyword query inputs to search against the service index. See [multi\_index\_query](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-multi-index-search) for details on how to construct this parameter.

    Note

    For performance reasons, `multi_index_query` currently supports at most one vector index entry in the query array.

`filter` (variant, optional)
:   Column containing filter objects to apply to the search results.

`limit` (integer, optional)
:   Maximum number of results to return per query. Default: 10.

`options` (variant, optional)
:   Column containing a VARIANT object with optional per-query settings. Supported top-level keys include:

    - `scoring_config` (object, optional): Same structure as the `scoring_config` parameter for interactive Cortex Search queries (Python, REST, or `SEARCH_PREVIEW`). Use it to customize ranking for that row’s batch query. See [Customizing Cortex Search scoring](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-customize-scoring).
    - `replicas` (integer, optional): How many copies of the search index serve that row’s batch query. Default: 2. Higher values can improve throughput by completing the job faster.

Note

At least one of `query`, `multi_index_query`, or `filter` must be specified.

## Usage notes

- The throughput of the batch search function might vary depending on the amount of data indexed in the queried Cortex Search Service and the complexity of the search queries. Run the function on a small number of queries to measure the throughput for your specific workload. In general, queries to larger services with more filter conditions see lower throughput.
- The throughput of the batch search function, the number of search queries processed per second, is not influenced by the size of the warehouse used to query it.
- Because batch search spins up dedicated resources to serve each job, it incurs additional startup latency. If you need to run fewer than 2,000 queries, you’ll typically get faster results using the interactive Cortex Search API (Python or REST API) rather than batch search.
- Unlike the interactive Cortex Search API, the batch search function can query services that are currently suspended in serving.
- A single Cortex Search Service can be queried in interactive and batch mode concurrently without any degradation to interactive query performance or throughput. Separate compute resources are used to serve interactive and batch queries.
- Reranking is not supported for batch search queries. If your `scoring_config` includes reranker settings, they are ignored.

## Cost considerations

Batch search has three cost components:

**Serving cost**
:   A charge based on the size of the search index data and the duration of the batch search job, excluding the startup time. Higher `replicas` values complete jobs faster but don’t increase total serving cost because the same machine hours are consumed over a shorter duration.

**Query embedding cost**
:   A charge for the number of tokens embedded as a result of the input queries. Unlike interactive Cortex Search, query embedding is not free for batch search.

**Virtual warehouse cost**
:   A charge for the virtual warehouse compute used to run the batch job.

For usage tracking, see the [CORTEX\_SEARCH\_BATCH\_QUERY\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_search_batch_query_usage_history) Account Usage view.
For more information on Cortex Search costs, see [Cost considerations](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-cost-considerations).

## Regional availability

Batch search is available in all regions where Cortex Search is available.
See [Regional availability](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-overview-regional-availability) for a full list of supported regions.

## Example Usage

In this example, match products in a user-submitted order form to a “golden” product catalog.
The `CORTEX_SEARCH_BATCH` call uses `options` so embeddings are computed without the default search query prefix; see [Disabling query prefix for vector embeddings](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-disable-query-prefix).
Use that setting only when you have evaluated the impact on result quality.

Copy code

```
-- Create the golden product catalog with canonical product names
CREATE OR REPLACE TABLE golden_catalog (product_name TEXT);
INSERT INTO golden_catalog VALUES
  ('Wireless Bluetooth Headphones'),
  ('Wireless Noise-Canceling Earbuds'),
  ('USB-C Charging Cable 6ft'),
  ('Portable Power Bank 10000mAh');

-- Create Cortex Search Service on the golden catalog
CREATE CORTEX SEARCH SERVICE golden_product_service
ON product_name
WAREHOUSE = <warehouse_name>
TARGET_LAG = '1 day'
AS
SELECT product_name FROM golden_catalog;

-- Create a table of user-submitted products (may contain variations or typos)
CREATE OR REPLACE TABLE submitted_products (product TEXT);
INSERT INTO submitted_products VALUES
  ('bluetooth headphones wireless'),
  ('usb c cable');

-- For each user-submitted product, query the service for the two closest golden results
SELECT
  q.product, s.*
FROM submitted_products AS q,
LATERAL CORTEX_SEARCH_BATCH(
    service_name => 'golden_product_service',
    query => q.product,
    limit => 2,
    options => OBJECT_CONSTRUCT(
        'scoring_config', OBJECT_CONSTRUCT(
            'disable_vector_embedding_query_prefix', true
        )
    )
) AS s;
```

The following example uses `multi_index_query` to submit precomputed embeddings as the query input instead of raw text. Here, the source table `my_db.my_schema.product_embeddings` contains a column `embedding` with precomputed vectors, and the Cortex Search Service `my_db.my_schema.golden_product_service` was created with a bring-your-own-vector (BYOV) configuration. For details on constructing `multi_index_query`, see [multi\_index\_query](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-multi-index-search).

Copy code

```
SELECT
    q.product_name,
    s.*
FROM (
    SELECT
        product_name,
        embedding::ARRAY AS emb_arr
    FROM my_db.my_schema.product_embeddings
    LIMIT 100000
) q,
LATERAL CORTEX_SEARCH_BATCH(
    service_name => 'my_db.my_schema.golden_product_service',
    multi_index_query => OBJECT_CONSTRUCT(
        'EMBEDDING', ARRAY_CONSTRUCT(
            OBJECT_CONSTRUCT('vector', q.emb_arr)
        )
    ),
    limit => 5
) s;
```
