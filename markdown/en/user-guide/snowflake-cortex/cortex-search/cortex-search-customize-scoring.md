# Customizing Cortex Search scoring

By default, queries to Cortex Search Services leverage vector similarity, text matching, and reranking
to determine the relevance of each result. You can customize the scoring of search results in several ways:

- Apply [numeric boosts](#label-cortex-search-boosts-decays) based on numeric metadata columns.
- Apply [time decays](#label-cortex-search-boosts-decays) based on timestamp metadata columns.
- Disable [reranking](#label-cortex-search-reranking) to reduce query latency.
- Modify [component weights](#label-cortex-search-weights) to adjust the weight of individual scoring components (vector, text, reranking) in the overall search ranking.
- Disable the [query prefix for vector embeddings](#label-cortex-search-disable-query-prefix) for advanced use cases.
- Modify [index-specific boosts](#label-cortex-search-index-boosts) to adjust the weight of individual indices in a multi-index search.

## Numeric boosts and time decays

You can boost or apply decays search results based on numeric or timestamp metadata. This feature is useful
when you have structured metadata, such as popularity or recency signals, for each result that can help determine the relevance of documents
at query time. You can specify two categories of ranking signals when making a query:

| Type | Description | Applicable column types | Example metadata fields (illustrative) |
| --- | --- | --- | --- |
| Numeric boost | Numeric metadata that boosts results having more attention or activity. | [Numeric data type](/sql-reference/data-types-numeric) | `clicks`, `likes`, `comments` |
| Time decay | Date or time metadata that boosts more recent results. The influence of recency signals decays over time. | [Date and time data type](/sql-reference/data-types-datetime) | `created_timestamp`, `last_opened_timestamp`, `action_date` |

Expand

Show lessSee more

Boost and decay metadata come from columns in the source table from which a Cortex Search Service is created. You
specify the metadata columns to use for boosting or decaying when you make the query, but those columns must be included
when creating the Cortex Search service.

When querying a Cortex Search Service, specify the columns to use for boosting or decaying in the optional
`numeric_boosts` and `time_decays` fields in the `scoring_config.functions` field. You can also specify the weight
for each boost or decay.

Copy code

```
{
  "scoring_config": {
    "functions": {
      "numeric_boosts": [
        {
          "column": "column_name",
          "weight": 1
        },
        /* ... */
      ],
      "time_decays": [
        {
          "column": "column_name",
          "weight": 1,
          "limit_hours": 120
        },
        /* ... */
      ]
    }
  }
}
```

### Properties

- `numeric_boosts` (array, optional):

  - `<numeric_boost_object>` (object, optional):
    - `column_name` (string): Specifies the numeric column to which the boost should be applied.
    - `weight` (float): Specifies the weight or importance assigned to the boosted column in the ranking process. When multiple columns are specified, a higher weight increases the influence of the field.
- `time_decays` (array, optional):

  - `<time_decay_object>` (object, optional):
    - `column_name` (string): Specifies the time or date column to which the decay should be applied.
    - `weight` (float): Specifies the weight or importance assigned to the decayed column in the ranking process. When multiple columns are specified, a higher weight increases the influence of the field.
    - `limit_hours` (float): Sets the boundary after which time starts to have less effect on the relevance or importance of the document. For example,
      a `limit_hours` value of 240 indicates that documents with timestamps greater than 240 hours (10 days) in the past from the `now` timestamp do not receive significant boosting,
      while documents with a timestamp within the last 240 hours should receive a more significant boost.
    - `now` (string, optional): Optional reference timestamp from which decays are calculated in ISO-8601 format `yyyy-MM-dd'T'HH:mm:ss.SSSXXX`.
      For example, `"2025-02-19T14:30:45.123-08:00"`. Defaults to the current timestamp if not specified.

Note

Numeric boosts are applied as weighted averages to the returned fields, while decays leverage a log-smoothed function to
demote less recent values.

Weights are relative across the specified boost or decay fields. If only a single field is provided within a `boosts` or
`decays` array, the value of its weight is irrelevant.

If more than one field is provided, the weights are applied relative to each other. A field with a weight of 10, for
example, affects the record’s ranking twice as much as a field with a weight of 5.

## Reranking

By default, queries to Cortex Search Services leverage *semantic reranking* to improve search result relevance.
While reranking can measurably increase result relevance, it can also noticeably increase query latency.
You can disable reranking in any Cortex Search query if you’ve found that
the quality benefit that reranking provides can be sacrificed for faster query speeds in your business use case.

Note

Disabling reranking reduces query latency by 100-300ms on average, but the exact reduction in latency, as
well as the magnitude of the quality degradation, varies across workloads.
Evaluate results side-by-side, with and without reranking, before you decide to disable it in queries.

Reranking is not supported for [batch search](/user-guide/snowflake-cortex/cortex-search/batch-cortex-search) queries. Any reranker settings in `scoring_config` are ignored when using `CORTEX_SEARCH_BATCH`.

You can disable the reranker for an individual query at query time in the `scoring_config.reranker` field in the
following format:

Copy code

```
{
  "scoring_config": {
      "reranker": "none"
  }
}
```

### Properties

- `reranker` (string, optional): Parameter that can be set to “none” if the reranker should be turned off. If excluded or null, the default reranker is used.

## Component weights

The `weights` field in the `scoring_config` object allows you to specify the
weights of individual scoring components (`vectors`, `texts`, `reranker`) in the overall
score for each result. By default, the weights are set to 1.0 for each component, with
an equal contribution to the overall scoring.

You can specify weights in the following format:

Copy code

```
{
  "scoring_config": {
    "weights": {
      "texts": 3,
      "vectors": 2,
      "reranker": 1
    },
    "functions": {
      // ...
    }
  }
}
```

### Properties

- `weights` (object, optional): Specifies weights for combining text, vector, and
  reranker scores for each document. Weights are applied relative to one another within this field.

For example, the following specifies that text scores should be weighted 3 times more than vector scores,
and reranker scores should be weighted 2 times more than vector scores:

Copy code

```
{
  "scoring_config": {
    "weights": {
      "texts": 3,
      "vectors": 1,
      "reranker": 2
    }
  }
}
```

## Disabling query prefix for vector embeddings

By default, Cortex Search adds a prefix to queries before computing vector embeddings. This prefix varies by model, but generally has the following format: `Represent this sentence for searching relevant passages: query`. This improves search quality in many cases by providing context to the embedding model, which helps differentiate search queries from other texts you have stored in the Cortex Search service.

However, you might want to disable this prefix in some cases such as the following scenario:

- When you want to use similarity search without the prefix. For example, if you want to search “what is the best data cloud” and you want to get “Snowflake” as a result, then use the default prefix. However, if you want to search “what is the data cloud” and you want to get “which is the best data cloud” as a result, then you can disable the prefix.

You can disable the query prefix for an individual query at query time using the `disable_vector_embedding_query_prefix` parameter in the `scoring_config` field:

Copy code

```
{
  "scoring_config": {
    "disable_vector_embedding_query_prefix": true
  }
}
```

### Properties

- `disable_vector_embedding_query_prefix` (boolean, optional): When set to `true`, a search prefix is not added automatically to the query before computing vector embeddings. Defaults to `false`.

Note

Disabling the query prefix might reduce search quality in most cases because the prefix helps the embedding model understand that the text is a search query. Only disable this if you have a specific reason to do so and have evaluated the impact on your search results.

## Named scoring profiles

Boosts/decays and reranker settings together form a *scoring configuration*, which can be specified in the `scoring_config` parameter
when making a query. Scoring configurations can also be given a name and attached to the Cortex Search service.

Using a named scoring profile lets you easily use a scoring configuration across applications and queries without having
to specify the full scoring configuration each time. If you change the scoring configuration, you only need to update it
in one place, not in every query.

To add a scoring profile to your Cortex Search Service, use the [ALTER CORTEX SEARCH SERVICE … ADD SCORING PROFILE](/sql-reference/sql/alter-cortex-search) command,
as shown in the following example:

Copy code

```
ALTER CORTEX SEARCH SERVICE my_search_service
  ADD SCORING PROFILE IF NOT EXISTS heavy_comments_with_likes
  '{
    "functions": {
            "numeric_boosts": [
                { "column": "comments", "weight": 6 },
                { "column": "likes", "weight": 1 }
            ]
    }
  }'
```

The syntax of the scoring profile definition is the same schema used in the `scoring_config` parameter when making a query.

Scoring profiles can’t be modified after being created; to change a profile, drop it and recreate it with the new scoring configuration.
To delete a named scoring profile, use [ALTER CORTEX SEARCH SERVICE … DROP SCORING PROFILE](/sql-reference/sql/alter-cortex-search).

To query a Cortex Search Service using a named scoring profile, specify the profile name in the `scoring_profile` parameter when making a query,
as shown in the following examples:

PythonREST APISQL

Copy code

```
results = svc.search(
    query="technology",
    columns=["comments", "likes"],
    scoring_profile="heavy_comments_with_likes",
    limit=10
)
```

Copy code

```
curl --location https://<account_url>/api/v2/databases/<db_name>/schemas/<schema_name>/cortex-search-services/<service_name>:query \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header "Authorization: Bearer $PAT" \
--data '{
  "query": "technology",
  "columns": ["DOCUMENT_CONTENTS", "LIKES", "COMMENTS"],
  "scoring_profile": "heavy_comments_with_likes",
  "limit": 10
}'
```

Copy code

```
SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
  'my_search_service',
  '{
    "query": "technology",
    "columns": ["comments", "likes"],
    "scoring_profile": "heavy_comments_with_likes",
    "limit": 10
  }'
);
```

To see a service’s stored scoring profiles, query the `CORTEX_SEARCH_SERVICE_SCORING_PROFILES` view in the
`INFORMATION_SCHEMA` schema, as shown in the following example:

Copy code

```
SELECT *
  FROM my_db.INFORMATION_SCHEMA.CORTEX_SEARCH_SERVICE_SCORING_PROFILES
  WHERE service_name = 'my_search_service';
```

Note

The DESCRIBE CORTEX SEARCH SERVICE and SHOW CORTEX SEARCH SERVICE results contain a column
named `scoring_profile_count` that indicates the number of scoring profiles for each service.

## Component Scores

Component Scores provide detailed scoring information for search results. They allow developers to understand how search rankings are determined and debug search performance.
Scores for each result are returned in the `@scores` field for each retrieval “component” (text, vector).
Component scores are useful in scenarios where there is a need to:

- **Establish thresholds:** Use component scores to determine when to pass results on to a downstream process, like an agent.
- **Debug search rankings:** Understand why certain documents rank higher than others in search results.

### Understanding Component Scores

Component scores provide detailed breakdowns of how Cortex Search calculates the final relevance score
for each search result. The scoring system consists of multiple components:

**Cosine Similarity**
:   Scores based on semantic similarity between the query and vector indexes. Higher scores indicate
    stronger conceptual or meaning-based matches using vector embeddings.

**Text Match**
:   Scores based on keyword/lexical similarity between the query and text indexes. Higher scores indicate
    stronger exact or fuzzy keyword matches.

**Reranker Score**
:   Scores based on meaning-based matches between the query and the value in the text index. Higher scores indicate stronger conceptual or meaning-based matches using reranker. Scores are provided only for the top results which are reranked.

**Function Scores**
:   Additional detailed scoring information from boost functions when applied (such as `text_boosts`, `vector_boosts`,
    numeric boosts, time decay). Contains nested objects for each boost type (such as `text_boost` and `vector_boost`)
    showing individual column scores, weights, and weighted totals. Useful for understanding how matches in different fields contribute
    to the final scoring of the document.

### Response format

With component scores enabled, the following scoring information is returned for all your Cortex Search queries.
For more information on Cortex Search Query syntax, see [Query a Cortex Search Service](/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service).

```
{
  "results": [
    {
      "@scores": {
        "cosine_similarity": <cosine_similarity_score>,
        "text_match": <text_match_score>
      }
    }
  ]
}
```

#### Score fields

- `@scores.cosine_similarity`: Cosine similarity score between the query and the value in the vector index, in the range [-1, 1].
- `@scores.text_match`: Text match score between the query and the value in the text index. This score is unbounded and its range
  depends on the query.
- `@scores.reranker_score`: Reranker score between the query and the value in the text index. This score is unbounded and its range
  depends on the query.
- `@scores.function_scores`: Nested object containing detailed boost function scoring (only present when `functions` are specified in the query):
  - `text_boost.column_scores.column_name.score`: Individual score for the specified column from text boost.
  - `text_boost.column_scores.column_name.weight`: Applied weight for the specified column from text boost.
  - `text_boost.weighted_score`: Final weighted score from text boost function.
  - `vector_boost.column_scores.column_name.score`: Individual score for the specified column from vector boost.
  - `vector_boost.column_scores.column_name.weight`: Applied weight for the specified column from vector boost.
  - `vector_boost.weighted_score`: Final weighted score from vector boost function.
  - `numeric_boost.column_scores.column_name.score`: Individual score for the specified column from numeric boost.
  - `numeric_boost.column_scores.column_name.weight`: Applied weight for the specified column from numeric boost.
  - `numeric_boost.weighted_score`: Final weighted score from numeric boost function.
  - `time_decay.column_scores.column_name.score`: Individual score for the specified column from time decay.
  - `time_decay.column_scores.column_name.weight`: Applied weight for the specified column from time decay.
  - `time_decay.weighted_score`: Final weighted score from time decay function.

#### Usage Notes

- `cosine_similarity` scores are:

  - Returned for any query that includes a VECTOR INDEX.
  - Bounded in the range [-1, 1] and comparable across different queries.
  - Computed assuming normalized vectors.
  - Subject to minor precision loss due to compression in the vector index, which means that
    `cosine_similarity(v, v)` might return `1.0 +/- epsilon` rather than exactly `1.0`.
    Compression details might vary over time, and epsilon might not be stable.
  - Computed after prepending each query with a prefix that increases search quality in many cases.
    This prefix varies per model, but generally looks like: `Represent this sentence for searching relevant passages: {query}`.
    The returned cosine similarity score is the cosine similarity between the query with the prefix and the value in the vector index.
- `text_match` scores are:

  - Returned for any query that includes a TEXT INDEX. `text_match` scores are unbounded.
  - Not comparable across different queries. For example, a text match score of 0.95 on a result for a given query is not comparable to a
    text match score of 0.95 on a result for a different query to the same service.
- `@scores` values are not affected by the `weights` parameter. The weights only affect the final ordering of the results.

## Index-specific boosts

Index-specific boosts adjust the weight of influence for indexes in a [multi-index Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-multi-index-search). You can adjust the text matching and vector matching weights, which are applied relative to the other provided weights. Higher values take priority over lower values, using the same behavior as component weights.

### Properties

- `text_boosts` (array, optional): Index-specific weights to be applied to text index columns. When this value is present, you’re required to include a weight for all text columns. Column weights are applied relative to one another.
- `vector_boosts` (array, optional): Index-specific weights to be applied to vector columns. When this value is present, you’re required to include a weight for all vector columns. Column weights are applied relative to one another.

Index-specific weights are objects containing `column` and `weight` keys:

```
{
  "column": "<column name>",
  "weight": <weight>
}
```

As an example, consider the following table indexed for search:

Copy code

```
CREATE TABLE feedback_info (
  id VARCHAR,
  comment VARCHAR,
  support_note VARCHAR,
  sentiment VECTOR(FLOAT, 3),
  issue_category VECTOR(FLOAT, 3)
);
```

The following JSON shows a `scoring_config` for a multi-index Cortex Search service that de-ranks the `id` text column while boosting the `comment` text column, and adjusting the vector rankings of `sentiment` to be twice as important as other vector columns.

Copy code

```
{
  "scoring_config": {
    "functions": {
      "text_boosts": [
        { "column": "id", "weight": 1 },
        { "column": "support_note", "weight": 2},
        { "column": "comment", "weight": 3},
      ],
      "vector_boosts": [
        { "column": "issue_category", "weight": 1 },
        { "column": "sentiment", "weight": 2 }
      ]
    }
  }
}
```

## Diversity

In some cases, one type of result may return more results than others. To prevent a certain type of result from dominating the search results, use the `diversity` parameter.

For example, if a Cortex Search Service is created using long documents and these documents are indexed by chunking, the `diversity` parameter can be used to ensure that multiple chunks from the same document are not surfaced in the final result set.

You can enable diversity for an individual query at query time in the `scoring_config.diversity` field in the following format:

Copy code

```
{
  "scoring_config": {
    "diversity": {
      "group_by": <array_of_columns_to_group_by>,
      "max_results": <num_results_for_each_group>,
    }
  }
}
```

### Properties

- `diversity` (object, optional): Parameter that can be set to “none” if result diversity should be turned off.
  - `group_by` (array): Columns to group by.
  - `max_results` (integer): Maximum number of results for each group.
