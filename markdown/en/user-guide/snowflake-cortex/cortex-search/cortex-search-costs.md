# Understanding cost for Cortex Search Services

Preview Feature

Support for this feature is available to accounts in most Snowflake regions.
See the [Regional availability](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-overview-regional-availability) section for a full list of regions.

## Cost categories

Cortex Search Services incur the following types of costs:

| Category | Description |
| --- | --- |
| Virtual warehouse compute | A Cortex Search Service requires a [virtual warehouse](/user-guide/cost-understanding-compute#label-virtual-warehouse-credit-usage) to refresh the service: to run queries against base objects when they are initialized and refreshed, including orchestrating text embedding jobs and building the search index. These operations use compute resources, which consume [credits](/user-guide/cost-understanding-compute#label-what-are-credits). If no changes are identified during a refresh, virtual warehouse credits aren’t consumed since there’s no new data to refresh. |
| EMBED\_TEXT tokens compute | A Cortex Search Service automatically embeds each text row in the search column specified in the `ON` parameter into vector space to enable semantic search, which incurs a credit cost per token embedded. This involves calling [EMBED\_TEXT\_768](/sql-reference/functions/embed_text-snowflake-cortex) or [EMBED\_TEXT\_1024](/sql-reference/functions/embed_text_1024-snowflake-cortex) to convert each document as a series of numbers that encodes its meaning. Embeddings are computed each time a row is inserted or updated. Embeddings are processed incrementally in the evaluation of the source query, so the embedding cost is only incurred for added or changed documents. See [Vector Embeddings](/user-guide/snowflake-cortex/vector-embeddings) for more information on vector embedding costs. |
| Multi-index Cortex Search | Multi-index Cortex Search Services have costs dependent on how you embed tokens and the number of columns you index. Larger embedding vectors or higher numbers of index columns incur higher costs. Embeddings are computed each time a row is inserted or updated. Embeddings are processed incrementally in the evaluation of the source query, so the embedding cost is only incurred for added or changed documents. |
| Serving compute | A Cortex Search Service uses multi-tenant serving compute, separate from a user-provided Virtual Warehouse, to establish a low-latency, high-throughput service. The compute cost for this component is incurred per GB per month (GB/mo) of uncompressed indexed data, where indexed data is the user-provided data in the Cortex Search source query, plus vector embeddings computed on the user’s behalf. You incur these costs while the service is available to respond to queries, even if no queries are served during a given period. For the Cortex Search Serving credit rate per GB/mo of indexed data, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf). |
| Storage | Cortex Search Services materialize the source query into a table stored in your account. This table is transformed into data structures that are optimized for low-latency serving, also stored in your account. Storage for the table and intermediate data structures are based on a flat rate per terabyte (TB). |
| Cloud services compute | Cortex Search Services use [Cloud Services compute](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage) to identify changes in underlying base objects and whether the virtual warehouse needs to be invoked. Cloud services compute cost is subject to the constraint that Snowflake only bills if the daily cloud services cost is greater than 10% of the daily warehouse cost for the account. |

Expand

Show lessSee more

This topic provides information on these costs, as well as recommendations for managing these costs effectively.

## Managing indexing costs

You may find the following tips useful in managing the indexing costs of a Cortex Search Service:

Minimize warehouse size
:   Most services do not see improved indexing performance beyond a LARGE warehouse and many need only MEDIUM. Most of the
    compute time used in building an index is consumed by the text embedding function, which does not benefit from more
    cores or additional memory when it already has sufficient resources.

Suspend indexing when freshness isn’t important
:   [Suspend indexing](/sql-reference/sql/alter-cortex-search) (or increase target lag) when you don’t need changes
    in your documents to be immediately propagated to the search service (that is, when freshness isn’t as important
    during some period).

Set target lag according to business requirements
:   Not every search application requires real-time indexing. A target lag that is too low may cause your index to be
    refreshed more frequently than necessary. For example, if your source data updates every five minutes, but the
    consumer of the data only queries the search service once an hour, set the target lag to one hour, not five minutes.

Define primary keys
:   Defining primary keys on your Cortex Search Service can result in significant reductions to both the cost and latency
    of indexing. Services with primary keys can make use of an optimized refresh path when the underlying data
    changes, particularly when the number of changes since the last refresh is small and the last refresh occurred within
    the previous week. For more information on defining primary keys, see [Primary keys](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys).

Bundle changes together
:   There is a fixed component to the cost of an update, so fewer, bigger updates are less expensive than more frequent,
    smaller updates. Likewise, any change to any value within a row triggers the search column in that row to be
    embedded again, even if the data within that search column is unchanged, so it is better to accumulate all the changes
    to a row into a single update. For more information about vector embedding costs, see [Vector Embeddings](/user-guide/snowflake-cortex/vector-embeddings).

Minimize changes to the source data
:   Any change to the schema of the source query causes a full refresh of the service, including vector embeddings and
    indexes. When you create a large service, consider including extra payload columns for later use, so you don’t need to
    trigger a full refresh by changing the schema when you need to add a column. The cost of the additional columns is low.

    Tip

    Materializing data in a table in the source query with a CREATE OR REPLACE command causes the service to fully
    refresh and embed all vectors again. It’s better to update the source table incrementally (for example, with MERGE INTO). For more information about vector embedding costs, see [Vector Embeddings](/user-guide/snowflake-cortex/vector-embeddings).

Keep the source query as simple as possible
:   Joins or other complex operations can add to indexing cost (and may be better to apply during ETL or at another
    stage). Refer to the Dynamic Tables Best Practices for more information on optimizing pipelines.

## Managing serving costs

You may find the following tips useful in managing the serving costs of a Cortex Search Service:

Suspend serving when it isn’t in use
:   A running search service incurs costs even when it isn’t serving queries. For predictable idle
    periods (for example, during development),
    [suspend the service manually](/sql-reference/sql/alter-cortex-search). For services with
    intermittent traffic, set the `AUTO_SUSPEND` property so that serving is suspended after a
    period of inactivity and resumed when the next query arrives. For more information, see
    [Auto-suspend serving on inactivity](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-auto-suspend-serving).

## Observing costs

To learn more about the costs of your Cortex Search services, use the following [Account Usage](/sql-reference/account-usage) views.

- [CORTEX\_SEARCH\_DAILY\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_search_daily_usage_history) contains daily totals for EMBED\_TEXT tokens compute and serving credit compute usage per service. Snowflake
  intends to also provide virtual warehouse usage in this view in the future.
- [CORTEX\_SEARCH\_SERVING\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_search_serving_usage_history) includes hourly serving credits per service.

Snowflake intends to make this information available in the Cortex Search administration interface in the future.

## Estimating costs

### EMBED\_TEXT tokens compute

EMBED\_TEXT tokens compute is charged per token of text in the search column, per document, charged in to
on the cost of the credit rate of the selected embedding model. This compute cost
is incurred for each row that is inserted or updated, including for each row in the ON column during the initialization
of the service and every insert or update thereafter. For information on the per-token
cost of each embedding model, see [Cortex Search Embedding Models](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-embedding-models):

For example, if you create a service on a source query with 10 million rows, each with 500 tokens, and the selected embedding model incurs
0.05 credits per 1 million tokens, you would expect to pay the following for the initial refresh:

> (0.05 credits per 1 million tokens) \* (10,000,000 rows) \* (500 tokens per row) / (1,000,000 tokens)
>
> = **250 credits**

For each row inserted or updated thereafter, you’d incur a cost of 0.05 credits per 1 million tokens.

Tip

As an approximation, one token is equivalent to about 3/4 of an English word, or around 4 characters.
To get an accurate estimate of tokens per row, use the [COUNT\_TOKENS](/sql-reference/functions/count_tokens-snowflake-cortex)
function with a representative sample of your actual data.

### Serving compute

Serving compute is charged per gigabyte-month of indexed data, where indexed data is the user-provided data
in the Cortex Search source query, plus vector embeddings computed on the user’s behalf. This is an ongoing cost
that is incurred as long as the service’s serving status is resumed. This cost is based on the number of rows indexed,
the size of the total indexed data, and the dimensionality of the selected vector embedding model. For information on the dimensionality
of each embedding model, see [Cortex Search Embedding Models](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-embedding-models):

For example, if you have a service with 10 million rows, the selected embedding model has dimension of 768, each row
in the source query is around 1,000 bytes (including the search column), and the credit cost per GB/mo of indexed data is 6.3,
you would expect to pay the following cost per month:

> (6.3 credits per GB) \* (10,000,000 rows) \* (768 dimensions \* 4 bytes per dimension + 1,000 bytes per row) / (1,000,000,000 bytes per GB)
>
> = **256.5 credits monthly**

Note

The size of the data per row varies by use case and increases with the amount of data (number of rows and columns) indexed by the service,
regardless of a column’s designation as a search or attribute column.

#### Multi-index Cortex Search

Multi-index search services often store more data per row to account for the additional index columns. The total data used depends on the number of indices in addition to the table size.

To estimate the monthly serving cost for a multi-index service, use the following formula, where `n` is the number
of vector index columns, `d` is the average number of vector dimensions, and `r` is the number of rows:

> (6.3 credits per GB) \* r \* (n \* d \* (4 bytes per dimension) + 1,000 bytes per row) / (1,000,000,000 bytes per GB)

For example, if you have a service with 10 million rows and 2 vector indexes each of 768 dimensional vectors, you would expect to pay the following cost per month:

> (6.3 credits per GB) \* (10,000,000 rows) \* ((2 vector index columns) \* (768 vector dimensions) \* (4 bytes per dimension) + 1,000 bytes per row) / (1,000,000,000 bytes per GB)
>
> = **448.1 credits monthly**

### Warehouse compute

The [virtual warehouse](/user-guide/cost-understanding-compute#label-virtual-warehouse-credit-usage) compute cost for Cortex Search Services can vary based on the change rate of your data, target lag, and warehouse size.
In general, Cortex Search Services with lower target lag values and higher change rates on underlying data will incur higher Warehouse-related
compute costs.

> Tip
>
> To get a clear understanding of Warehouse costs related to your Cortex Search pipelines, test
> Cortex Search using dedicated warehouses so that the virtual warehouse consumption attributed to Cortex Search refreshes
> can be isolated. You can move your Cortex Search Service to a shared warehouse after you establish a cost
> baseline.

### Storage

Cortex Search Services require storage to store the materialized results of the source query, as well as the search index.
The size of the data stored can be estimated by materializing the source query into a table using the
[CORTEX\_SEARCH\_DATA\_SCAN](/sql-reference/functions/cortex_search_data_scan) table function, and then examining the size of that table.

For detailed information about how this storage incurs cost, see [Understanding storage cost](/user-guide/cost-understanding-data-storage).

### Cloud Services

Cortex Search Services use [Cloud Services compute](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage) to trigger refreshes when an underlying base object has changed. These costs
can vary based on the change rate of your data, target lag, and warehouse size. Cloud services
cost for change tracking in Cortex Search tend to be lower for use-cases with low change rates. Cloud services compute cost
is subject to the constraint that Snowflake only bills if the daily cloud services cost is greater than 10% of the daily warehouse
cost for the account.
