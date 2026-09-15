# Query a Cortex Search Service

When you create a Cortex Search Service, the system provisions an API endpoint to serve queries at low latency.
You can use three APIs for querying a Cortex Search Service:

- The [Python API](#label-cortex-search-query-syntax-python)
- The [REST API](#label-cortex-search-query-syntax-rest)
- The [SQL SEARCH\_PREVIEW Function](#label-cortex-search-query-syntax-sql-preview)

## Parameters

All APIs support the same set of query parameters:

|  | Parameter | Description |
| --- | --- | --- |
| Required | `query` | The search query, to be searched for in the text column in the service. |
| Optional | `columns` | A comma-separated list of columns to return for each relevant result in the response. These columns must be included in the source query for the service.  If this parameter is not provided, only the search column is returned in the response. |
|  | `filter` | A filter object for filtering results based on data in the `ATTRIBUTES` columns. See [Filter syntax](#filter-syntax) for syntax. |
|  | `scoring_config` | Configuration object for customizing search ranking behavior. See [Customizing Cortex Search scoring](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-customize-scoring) for syntax. |
|  | `scoring_profile` | The named scoring profile to be used with the query, previously defined with [ALTER CORTEX SEARCH SERVICE … ADD SCORING PROFILE](/sql-reference/sql/alter-cortex-search). If `scoring_profile` is provided, any `scoring_config` provided is ignored. |
|  | `limit` | Maximum number of results to return in the response, up to 1000. The default limit is 10. |

Expand

Show lessSee more

### Multi-index search parameters

In addition, the SQL and Python APIs support [multi-index queries](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-multi-index-search). Using multi-index parameters allows for refining results from Cortex Search and reducing query cost by limiting the number of columns searched.

| Parameter | Description |
| --- | --- |
| `multi_index_query` | The map used to determine which indexes to query. Each key in the map is the name of an indexed column, and each value is an array containing maps that define the query:   - If the index is a text index or a managed vector index, the query array can contain:    - Text queries: `{"text": "search_text"}`   - Vector queries, as an embedding vector: `{"vector": [vector_values]}` - If the index is a user-provided vector embedding column, the query array can contain:    - If a `query_model` was specified at creation time for automatic embeddings, text queries: `{"text": "search_text"}`.   - Vector queries, as an embedding vector: `{"vector": [vector_values]}` |

Expand

Show lessSee more

Note

Multi-index Cortex Search services can still be searched through the REST API or without the `multi_index_query` parameter. This causes an unrestricted search over *all* indexed columns, which affects query cost. For details on estimating cost for multi-index query compute, see [Understanding cost for Cortex Search Services - Multi-index search](/user-guide/snowflake-cortex/cortex-search/cortex-search-costs#label-cortex-search-multi-index-estimate-cost).

## Syntax

Simple queries to a Cortex Search Service use the following syntax:

PythonREST APISQL

Copy code

```
import os
from snowflake.core import Root
from snowflake.snowpark import Session

# connect to Snowflake
CONNECTION_PARAMETERS = { ... }
session = Session.builder.configs(CONNECTION_PARAMETERS).create()
root = Root(session)

# fetch service
my_service = (root
    .databases["<service_database>"]
    .schemas["<service_schema>"]
    .cortex_search_services["<service_name>"]
)

# query service
resp = my_service.search(
    query="<query>",
    columns=["<col1>", "<col2>"],
    filter={"@eq": {"<column>": "<value>"} },
    limit=5
)
print(resp.to_json())
```

Copy code

```
curl --location https://<ACCOUNT_URL>/api/v2/databases/<DB_NAME>/schemas/<SCHEMA_NAME>/cortex-search-services/<SERVICE_NAME>:query \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header "Authorization: Bearer $PAT" \
--data '{
  "query": "<search_query>",
  "columns": ["col1", "col2"],
  "filter": <filter>,
  "limit": <limit>
}'
```

Copy code

```
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'my_search_service',
      '{
         "query": "preview query",
         "columns":[
            "col1",
            "col2"
         ],
         "filter": {"@eq": {"col1": "filter value"} },
         "limit":10
      }'
  )
)['results'] as results;
```

### Multi-index query syntax

Querying specific indices only or using a service with vector embeddings for a multi-index Cortex Search service uses the following syntax:

PythonSQL

Copy code

```
from snowflake.core import Root
from snowflake.snowpark import Session

session = Session.builder.configs( {...} ).create()
root = Root(session)

my_service = (root
  .databases["<service_database>"]
  .schemas["<service_schema>"]
  .cortex_search_services["<service_name>"]
)

resp = my_service.search(
    multi_index_query={
        "<index_name>": [
            {"text": "<search_text>"},
            {"vector": [<vector_values>]},
            ...
        ],
        ...
    },
    scoring_config={
        "weights": {
            "texts": <text_weight>,
            "vectors": <vector_weight>,
            "reranker": <reranker_weight>
        },
        "functions": {
            "vector_boosts": [
                {"weight": <weight>, "column": "<vector_column_name>"},
                ...
            ],
            "text_boosts": [
                {"weight": <weight>, "column": "<text_column_name>"},
                ...
            ]
        }
    },
    columns=["<column_name>", "<column_name>", ...],
    limit=<limit>
)
```

Copy code

```
SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      '<service_name>',
      '{
        "multi_index_query": {
          "<index_name>": [
            {"text": "<search_text>"},
            {"vector": [<vector_values>]},
            ...
          ],
          ...
        },
        "columns": ["<column_name>", "<column_name>", ...],
        "limit": <limit>,
        "scoring_config": {
          "weights": {
            "texts": <text_weight>,
            "vectors": <vector_weight>,
            "reranker": <reranker_weight>
          },
          "functions": {
            "vector_boosts": [
              {"weight": <weight>, "column": "<vector_column_name>"},
              ...
            ],
            "text_boosts": [
              {"weight": <weight>, "column": "<text_column_name>"}
              , ...
            ]
          }
        }
      }'
  );
```

## Setup and authentication

### Python API

Cortex Search Services may be queried using version 0.8.0 or later of the Snowflake Python APIs. See
[Snowflake Python APIs: Managing Snowflake objects with Python](/developer-guide/snowflake-python-api/snowflake-python-overview) for more information on the Snowflake
Python APIs.

#### Install the Snowflake Python API library

First, install the latest version of the Snowflake Python APIs package from PyPI.
See [Install the Snowflake Python APIs library](/developer-guide/snowflake-python-api/snowflake-python-installing)
for instructions on installing this package from PyPI.

Copy code

```
pip install snowflake -U
```

#### Connect to Snowflake

Connect to Snowflake using either a Snowpark `Session` or a Python Connector `Connection` and create a
`Root` object. See [Connect to Snowflake with the Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake) for more instructions on connecting
to Snowflake. The following example uses the Snowpark `Session` object and a Python dictionary for
configuration.

Copy code

```
import os
from snowflake.core import Root
from snowflake.snowpark import Session

CONNECTION_PARAMETERS = {
    "account": os.environ["snowflake_account_demo"],
    "user": os.environ["snowflake_user_demo"],
    "password": os.environ["snowflake_password_demo"],
    "role": "test_role",
    "database": "test_database",
    "warehouse": "test_warehouse",
    "schema": "test_schema",
}

session = Session.builder.configs(CONNECTION_PARAMETERS).create()
root = Root(session)
```

Note

Version 0.8.0 or later of the Snowflake Python APIs library is required to query a Cortex Search Service.

### REST API

Cortex Search exposes a REST API endpoint in the suite of [Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api). The REST endpoint
generated for a Cortex Search Service is of the following structure:

Copy code

```
https://<account_url>/api/v2/databases/<db_name>/schemas/<schema_name>/cortex-search-services/<service_name>:query
```

Where:

- `<account_url>`: Your Snowflake Account URL. See [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find) for instructions on finding your account URL.
- `<db_name>`: Database in which the service resides.
- `<schema_name>`: Schema in which the service resides.
- `<service_name>`: Name of the service.
- `:query`: The method to invoke on the service; in this case, the `query` method.

For additional details, see the REST API reference for [Cortex Search Service](https://docs.snowflake.com/developer-guide/snowflake-rest-api/reference/cortex-search-service).

#### Authentication

Snowflake REST APIs support authentication via programmatic access tokens (PATs), key pair authentication
using JSON Web Tokens (JWTs), and OAuth. For details, see
[Authenticating Snowflake REST APIs with Snowflake](/developer-guide/snowflake-rest-api/authentication).

### SQL SEARCH\_PREVIEW function

The [SNOWFLAKE.CORTEX.SEARCH\_PREVIEW](/sql-reference/functions/search_preview-snowflake-cortex) function allows you to preview the
results of individual queries to a Cortex Search Service from within a SQL environment such as a worksheet or Snowflake notebook cell.
This function makes it easy to interactively validate that a service has populated correctly and is serving reasonable results.

Important

> The `SEARCH_PREVIEW` function is provided for testing and validation of Cortex Search Services.
> It is not intended for serving search queries in an end-user application.

- The function operates only on string literals. It does not accept batch text data.
- The function has higher latency than the REST and Python APIs..

## Filter syntax

Cortex Search supports filtering on the ATTRIBUTES columns specified in the
[CREATE CORTEX SEARCH SERVICE](/sql-reference/sql/create-cortex-search) command.

Cortex Search supports five matching operators:

- [TEXT](/sql-reference/data-types-text) or [NUMERIC](/sql-reference/data-types-numeric) equality: `@eq`
- [ARRAY](/sql-reference/data-types-semistructured) contains: `@contains`
- [NUMERIC](/sql-reference/data-types-numeric) or [DATE/TIMESTAMP](/sql-reference/data-types-datetime) greater than or equal to: `@gte`
- [NUMERIC](/sql-reference/data-types-numeric) or [DATE/TIMESTAMP](/sql-reference/data-types-datetime) less than or equal to: `@lte`
- [Primary key](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys) equality: `@primarykey`

These matching operators can be composed with various logical operators:

- `@and`
- `@or`
- `@not`

### Usage notes

- Matching against `NaN` (‘not a number’) values in the source query is handled as described in
  [Special values](/sql-reference/data-types-numeric#label-data-type-float-special-values).
- Fixed-point numeric values with more than 19 digits (not including leading zeroes) do not work with `@eq`,
  `@gte`, or `@lte` and will not be returned by these operators (although they could still be returned by the
  overall query with the use of `@not`).
- `TIMESTAMP` filters accept values of the form: `YYYY-MM-DDTHH:MM:SS.sss+HH:MM`. If the timezone offset is not specified, the date is interpreted in UTC.
- `DATE` filters accept values of the form `YYYY-MM-DD`. If time or timezones are specified, they will be truncated.
- `@primarykey` is only supported for services configured with a [primary key](/sql-reference/constraints-overview). The value of the filter must be
  a JSON object mapping every primary key column to its corresponding value (or `NULL`).

These operators can be combined into a single filter object.

### Examples

- Filtering on rows where string-like column `string_col` is equal to value `value`.

  Copy code

  ```
  { "@eq": { "string_col": "value" } }
  ```
- Filtering to a row with the specified primary key values `us-west-1` in the `region` column and `abc123` in the `agent_id` column:

  Copy code

  ```
  { "@primarykey": { "region": "us-west-1", "agent_id": "abc123" } }
  ```
- Filtering on rows where ARRAY column `array_col` contains value `value`.

  Copy code

  ```
  { "@contains": { "array_col": "arr_value" } }
  ```
- Filtering on rows where NUMERIC column `numeric_col` is between 10.5 and 12.5 (inclusive):

  Copy code

  ```
  {
    "@and": [
   { "@gte": { "numeric_col": 10.5 } },
   { "@lte": { "numeric_col": 12.5 } }
    ]
  }
  ```
- Filtering on rows where TIMESTAMP column `timestamp_col` is between `2024-11-19` and `2024-12-19`
  (inclusive).

  Copy code

  ```
  {
    "@and": [
   { "@gte": { "timestamp_col": "2024-11-19" } },
   { "@lte": { "timestamp_col": "2024-12-19" } }
    ]
  }
  ```
- Composing filters with logical operators:

  Copy code

  ```
  // Rows where the "array_col" column contains "arr_value" and the "string_col" column equals "value"
  {
    "@and": [
   { "@contains": { "array_col": "arr_value" } },
   { "@eq": { "string_col": "value" } }
    ]
  }

  // Rows where the "string_col" column does not equal "value"
  {
    "@not": { "@eq": { "string_col": "value" } }
  }

  // Rows where the "array_col" column contains at least one of "val1", "val2", or "val3"
  {
    "@or": [
   { "@contains": { "array_col": "val1" } },
   { "@contains": { "array_col": "val2" } },
   { "@contains": { "array_col": "val3" } }
    ]
  }
  ```

## Multi-index queries

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

When created as a multi-index Cortex Search service with the [CREATE CORTEX SEARCH SERVICE … TEXT INDEXES … VECTOR INDEXES](/sql-reference/sql/create-cortex-search) syntax, the optional `multi_index_query` parameter is used. When omitting this parameter, all indices are used in the search.

### Usage notes

- Each index to query is represented as a key-value pair in the `multi_index_query` map.
- At least one vector index must be supplied in each query. Querying only text indexes is an error.
- When querying a multi-index Cortex Search Service, the following behaviors apply:

  - *AND across fields*: A match in all of the queried text or vector fields is required for a document to be returned.
  - *OR across terms within a text index field*: When a query contains multiple terms such as “wash fold”, a document
    is returned if *any* of the query terms are found within the document.
  - Text queries are automatically normalized using stemming, lemmatization, and domain-specific rewrites via Snowflake’s custom analyzer.
    This improves recall by matching related terms, such as linking “washing” to “wash” and “laundromat” to “laundry”.
- The `scoring_config.weights` field modifies the relative weight of each of the 3 high-level scoring techniques
  (vector, keyword, reranking) in a given query.

  Within this field, weights are applied *relative* to each other. For example,
  `{ "texts": 3, "vectors": 2, "reranker": 1 }` and `{ "texts": 30, "vectors": 20, "reranker": 10 }`
  are equivalent.
- Using the `scoring_config.functions.vector_boosts` and `scoring_config.functions.text_boosts` fields:

  - These fields allow users to modify the relative weight of each vector index and text index query,
    respectively, in a given query.
  - Within each field, weights are applied relative to each other, as in `scoring_config.weights`.
- Multi-index queries can be combined with numeric boosts, time decays, and queries that disable reranking.
  For information on using those features, see [Numeric boosts and time decays](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-boosts-decays)
  and [Reranking](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-reranking).
- When querying a multi-index service, the `query` parameter can be used to specify a query to be applied to all fields, unless
  the service contains a vector index with user-provided vector embeddings.
- To optimize search performance and latency, columns containing vector embeddings are not returned in results when issuing a query to a user-provided vector index.
- Snowflake recommends refining your queries to use the `multi_index_query` on multi-index Cortex Search services to reduce the amount of resources consumed, which affects cost.

  For information on estimating pricing for multi-index queries, see [Estimating costs for multi-index Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-costs#label-cortex-search-multi-index-estimate-cost).

## Access control requirements

The role that is querying the Cortex Search Service must have the following privileges to retrieve results:

| Privilege | Object |
| --- | --- |
| USAGE | The Cortex Search Service |
| USAGE | The database in which the Cortex Search Service resides |
| USAGE | The schema in which the Cortex Search Service resides |

Expand

Show lessSee more

### Querying with owner’s rights

Cortex Search Services perform searches with [owner’s rights](/developer-guide/stored-procedure/stored-procedures-rights) and follow the same security model as other
Snowflake objects that run with owner’s rights.

In particular, this means that any role with sufficient privileges to query a Cortex Search Service
may query any of the data the service has indexed, regardless of that role’s privileges on the
underlying objects (such as tables and views) referenced in the service’s source query.

For example, for a Cortex Search Service that references a table with row-level masking policies,
querying users of that service will be able to see search results from rows on which the owner’s role
has read permission, even if the querying user’s role cannot read those rows in the source table.

Use caution, for example, when granting a role with USAGE privileges on a Cortex Search Service to another
Snowflake user.

## Known limitations

Querying a Cortex Search Service is subject to the following limitations:

- **Response size**: The total size of the response payload returned from a search query
  to a Cortex Search Service must not exceed the following limits:
  - [REST API](https://docs.snowflake.com/developer-guide/snowflake-rest-api/reference/cortex-search-service) and [Python API](/developer-guide/snowflake-python-api/snowflake-python-overview): 10 Megabytes (MB)
  - [SQL SEARCH\_PREVIEW Function](/sql-reference/functions/search_preview-snowflake-cortex): 300 Kilobytes (KB)

Multi-index Cortex Search is subject to additional limitations, which may change during preview:

- The Cortex Search Playground in the Snowsight UI does not support queries to multi-index services. Queries to multi-index services in the Playground display the message “Unable to query search service. Invalid request parameters or filter syntax.”
- The multi-index serving query syntax with the `multi_index_query` parameter is supported only in versions 1.6.0 or later of the [Python API](#label-cortex-search-query-syntax-python).

## Examples

This section provides comprehensive examples for querying Cortex Search Services across all three API
methods.

### Setup for examples

The following examples use a table named `business_documents` with timestamp and numeric columns for
demonstrating various features:

Copy code

```
CREATE OR REPLACE TABLE business_documents (
    document_contents VARCHAR,
    last_modified_timestamp TIMESTAMP,
    created_timestamp TIMESTAMP,
    likes INT,
    comments INT
);

INSERT INTO business_documents (document_contents, last_modified_timestamp, created_timestamp, likes, comments)
VALUES
    ('Quarterly financial report for Q1 2024: Revenue increased by 15%, with expenses stable.',
     '2024-01-12 10:00:00', '2024-01-10 09:00:00', 10, 20),

    ('IT manual for employees: Instructions for usage of internal technologies, including hardware.',
     '2024-02-10 15:00:00', '2024-02-05 14:30:00', 85, 10),

    ('Employee handbook 2024: Updated policies on remote work, health benefits, and company culture.',
     '2024-02-10 15:00:00', '2024-02-05 14:30:00', 85, 10),

    ('Marketing strategy document: Target audience segmentation for upcoming product launch.',
     '2024-03-15 12:00:00', '2024-03-12 11:15:00', 150, 32),

    ('Product roadmap 2024: Key milestones for tech product development, including the launch.',
     '2024-04-22 17:30:00', '2024-04-20 16:00:00', 200, 45),

    ('Annual performance review process guidelines: Procedures for managers to conduct employee.',
     '2024-05-02 09:30:00', '2024-05-01 08:45:00', 60, 5);

CREATE OR REPLACE CORTEX SEARCH SERVICE business_documents_css
    ON document_contents
    WAREHOUSE = <warehouse_name>
    TARGET_LAG = '1 minute'
AS SELECT * FROM business_documents;
```

### Filter examples

#### Simple query with an equality filter

PythonREST APISQL

Copy code

```
resp = business_documents_css.search(
    query="technology",
    columns=["DOCUMENT_CONTENTS", "LIKES"],
    filter={"@eq": {"REGION": "US"}},
    limit=5
)
```

Copy code

```
curl --location https://<ACCOUNT_URL>/api/v2/databases/<DB_NAME>/schemas/<SCHEMA_NAME>/cortex-search-services/<SERVICE_NAME>:query \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header "Authorization: Bearer $PAT" \
--data '{
  "query": "technology",
  "columns": ["DOCUMENT_CONTENTS", "LIKES"],
  "filter": {"@eq": {"REGION": "US"}},
  "limit": 5
}'
```

Copy code

```
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'business_documents_css',
      '{
         "query": "technology",
         "columns": ["DOCUMENT_CONTENTS", "LIKES"],
         "filter": {"@eq": {"REGION": "US"}},
         "limit": 5
      }'
  )
)['results'] as results;
```

#### Range filter

PythonREST APISQL

Copy code

```
resp = business_documents_css.search(
    query="business",
    columns=["DOCUMENT_CONTENTS", "LIKES", "COMMENTS"],
    filter={"@and": [
        {"@gte": {"LIKES": 50}},
        {"@lte": {"COMMENTS": 50}}
    ]},
    limit=10
)
```

Copy code

```
curl --location https://<ACCOUNT_URL>/api/v2/databases/<DB_NAME>/schemas/<SCHEMA_NAME>/cortex-search-services/<SERVICE_NAME>:query \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header "Authorization: Bearer $PAT" \
--data '{
  "query": "business",
  "columns": ["DOCUMENT_CONTENTS", "LIKES", "COMMENTS"],
  "filter": {"@and": [
    {"@gte": {"LIKES": 50}},
    {"@lte": {"COMMENTS": 50}}
  ]},
  "limit": 10
}'
```

Copy code

```
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'business_documents_css',
      '{
         "query": "business",
         "columns": ["DOCUMENT_CONTENTS", "LIKES", "COMMENTS"],
         "filter": {"@and": [
           {"@gte": {"LIKES": 50}},
           {"@lte": {"COMMENTS": 50}}
         ]},
         "limit": 10
      }'
  )
)['results'] as results;
```

### Scoring examples

#### Numeric boosts

Apply numeric boosts to both the likes and comments columns, with twice the boost weight on
comments values relative to likes values.

PythonREST APISQL

Copy code

```
resp = business_documents_css.search(
    query="technology",
    columns=["DOCUMENT_CONTENTS", "LIKES", "COMMENTS"],
    scoring_config={
        "functions": {
            "numeric_boosts": [
                {"column": "comments", "weight": 2},
                {"column": "likes", "weight": 1}
            ]
        }
    }
)
```

Copy code

```
curl --location https://<ACCOUNT_URL>/api/v2/databases/<DB_NAME>/schemas/<SCHEMA_NAME>/cortex-search-services/<SERVICE_NAME>:query \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header "Authorization: Bearer $PAT" \
--data '{
  "query": "technology",
  "columns": ["DOCUMENT_CONTENTS", "LIKES", "COMMENTS"],
  "scoring_config": {
    "functions": {
      "numeric_boosts": [
        {"column": "comments", "weight": 2},
        {"column": "likes", "weight": 1}
      ]
    }
  }
}'
```

Copy code

```
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'business_documents_css',
      '{
         "query": "technology",
         "columns": ["DOCUMENT_CONTENTS", "LIKES", "COMMENTS"],
         "scoring_config": {
           "functions": {
             "numeric_boosts": [
               {"column": "comments", "weight": 2},
               {"column": "likes", "weight": 1}
             ]
           }
         }
      }'
  )
)['results'] as results;
```

In the results, note:

> - With the boosts, the “Product roadmap 2024:…” document is the top result because of its large number of likes and comments, even though it has slightly lower relevance to the query “technology”
> - Without any boosts, the top result for the query is “IT manual for employees:…”

#### Time decays

Apply time decays based on the LAST\_MODIFIED\_TIMESTAMP column, where:

> - Documents with more recent LAST\_MODIFIED\_TIMESTAMP values, relative to the now timestamp, are boosted
> - Documents with a LAST\_MODIFIED\_TIMESTAMP value greater than 240 hours from the now timestamp receive little boosting

PythonREST APISQL

Copy code

```
resp = business_documents_css.search(
    query="technology",
    columns=["DOCUMENT_CONTENTS", "LAST_MODIFIED_TIMESTAMP"],
    scoring_config={
        "functions": {
            "time_decays": [
                {"column": "LAST_MODIFIED_TIMESTAMP", "weight": 1, "limit_hours": 240, "now": "2024-04-23T00:00:00.000-08:00"}
            ]
        }
    }
)
```

Copy code

```
curl --location https://<ACCOUNT_URL>/api/v2/databases/<DB_NAME>/schemas/<SCHEMA_NAME>/cortex-search-services/<SERVICE_NAME>:query \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header "Authorization: Bearer $PAT" \
--data '{
  "query": "technology",
  "columns": ["DOCUMENT_CONTENTS", "LAST_MODIFIED_TIMESTAMP"],
  "scoring_config": {
    "functions": {
      "time_decays": [
        {"column": "LAST_MODIFIED_TIMESTAMP", "weight": 1, "limit_hours": 240, "now": "2024-04-23T00:00:00.000-08:00"}
      ]
    }
  }
}'
```

Copy code

```
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'business_documents_css',
      '{
         "query": "technology",
         "columns": ["DOCUMENT_CONTENTS", "LAST_MODIFIED_TIMESTAMP"],
         "scoring_config": {
           "functions": {
             "time_decays": [
               {"column": "LAST_MODIFIED_TIMESTAMP", "weight": 1, "limit_hours": 240, "now": "2024-04-23T00:00:00.000-08:00"}
             ]
           }
         }
      }'
  )
)['results'] as results;
```

In the results, note:

> - With the decays, the “Product roadmap 2024:…” document is the top result because of its recency to the now timestamp, even though it has slightly lower relevance to the query “technology”
> - Without any decays, the top result for the query is “IT manual for employees:…”

#### Disabling reranking

To disable reranking:

PythonREST APISQL

Copy code

```
resp = business_documents_css.search(
    query="technology",
    columns=["DOCUMENT_CONTENTS", "LAST_MODIFIED_TIMESTAMP"],
    limit=5,
    scoring_config={
        "reranker": "none"
    }
)
```

Copy code

```
curl --location https://<ACCOUNT_URL>/api/v2/databases/<DB_NAME>/schemas/<SCHEMA_NAME>/cortex-search-services/<SERVICE_NAME>:query \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header "Authorization: Bearer $PAT" \
--data '{
  "query": "technology",
  "columns": ["DOCUMENT_CONTENTS", "LAST_MODIFIED_TIMESTAMP"],
  "scoring_config": {
    "reranker": "none"
  }
}'
```

Copy code

```
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'business_documents_css',
      '{
         "query": "technology",
         "columns": ["DOCUMENT_CONTENTS", "LAST_MODIFIED_TIMESTAMP"],
         "scoring_config": {
           "reranker": "none"
         }
      }'
  )
)['results'] as results;
```

Tip

To query a service **with** the reranker, omit the `"reranker": "none"` parameter from the
`scoring_config` object, as reranking is the default behavior.

## Multi-index query examples

This section provides examples for querying multi-index Cortex Search Services with a restriction on which indices to search, for the Python and SQL APIs.

### Query a service with managed vector embeddings

Examples in this section use the following `business_directory` and `example_search_service` definitions:

Copy code

```
-- Search data
CREATE OR REPLACE TABLE business_directory (name TEXT, address TEXT, description TEXT);
INSERT INTO business_directory VALUES
    ('Joe''s Coffee', '123 Bean St, Brewtown','A cozy café known for artisan espresso and baked goods.'),
    ('Sparkle Wash', '456 Clean Ave, Sudsville', 'Eco-friendly car wash with free vacuum service.'),
    ('Tech Haven', '789 Circuit Blvd, Siliconia', 'Computer store offering the latest gadgets and tech repair services.'),
    ('Joe''s Wash n'' Fold', '456 Apple Ct, Sudsville', 'Laundromat offering coin laundry and premium wash and fold services.'),
    ('Circuit Town', '459 Electron Dr, Sudsville', 'Technology store selling used computer parts at discounted prices.')
;

-- Cortex Search Service
CREATE OR REPLACE CORTEX SEARCH SERVICE example_search_service
    TEXT INDEXES name, address
    VECTOR INDEXES description (model='snowflake-arctic-embed-m-v1.5')
    WAREHOUSE = example_wh
    TARGET_LAG = '1 hour'
    AS ( SELECT * FROM business_directory );
```

#### Query specific indexes

To query `example_search_service` over the `name` text field and `description` vector field:

PythonSQL

Copy code

```
resp = business_directory.search(
    query="tech repair shop",
    columns=["name", "description"],
    limit=2
)
```

Copy code

```
SELECT
  value['name']::text as name, value['address']::text as address, value['description']::text as description
FROM TABLE(FLATTEN(PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'business_search_service',
      '{
      "query": "tech repair shop",
        "columns": ["name", "description"],
        "limit": 2
      }'
  ))['results']));
```

```
+---------------------+-----------------------------+--------------------------------------------------------------------------+
|        NAME         |           ADDRESS           |                            DESCRIPTION                                   |
|---------------------+-----------------------------+--------------------------------------------------------------------------|
| Tech Haven          | 789 Circuit Blvd, Siliconia | Computer store offering the latest gadgets and tech repair services.     |
| Circuit Town        | 459 Electron Dr, Sudsville  | Technology store selling used computer parts at discounted prices.       |
+---------------------+-----------------------------+--------------------------------------------------------------------------+
```

#### Query a managed vector column only

To query `example_search_service` for “refurbished components for PCs” over the vector index `description`, using managed embeddings:

PythonSQL

Copy code

```
resp = business_directory.search(
    multi_index_query={
        "description": [
            {"text": "refurbished components for PCs"}
        ]
    },
    columns=["name", "address", "description"],
    limit=5
)
```

Copy code

```
SELECT
    value['name']::text as name, value['address']::text as address, value['description']::text as description
FROM TABLE(FLATTEN(PARSE_JSON(
    SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
        'business_search_service',
        '{
          "multi_index_query": {
            "description": [
              {"text": "refurbished components for PCs"}
            ]
          },
          "columns": ["name", "address", "description"],
          "limit": 5
        }'
    )
)['results']));
```

```
+---------------------+-----------------------------+--------------------------------------------------------------------------+
|        NAME         |           ADDRESS           |                            DESCRIPTION                                   |
|---------------------+-----------------------------+--------------------------------------------------------------------------|
| Circuit Town        | 459 Electron Dr, Sudsville  | Technology store selling used computer parts at discounted prices.       |
| Tech Haven          | 789 Circuit Blvd, Siliconia | Computer store offering the latest gadgets and tech repair services.     |
| Joe's Coffee        | 123 Bean St, Brewtown       | A cozy café known for artisan espresso and baked goods.                  |
| Joe's Wash n' Fold  | 456 Apple Ct, Sudsville    | Laundromat offering coin laundry and premium wash and fold services.      |
| Sparkle Wash        | 456 Clean Ave, Sudsville    | Eco-friendly car wash with free vacuum service.                          |
+---------------------+-----------------------------+--------------------------------------------------------------------------+
```

#### Query with index weights

To query the `example_search_service` for “sparkle” over the text index `name` and “clothing washing” over the vector index `description`, weighting vector scoring as four times more relevant than text or reranking:

PythonSQL

Copy code

```
resp = business_directory.search(
    multi_index_query={
        "name": [
            {"text": "sparkle"}
        ],
        "description": [
            {"text": "clothing washing"}
        ]
    },
    scoring_config={
        "weights": {
            "texts": 1,
            "vectors": 4,
            "reranker": 1
        }
    },
    columns=["name", "address", "description"],
    limit=2
)
```

Copy code

```
SELECT
    value['name']::text as name, value['address']::text as address, value['description']::text as description
FROM TABLE(FLATTEN(PARSE_JSON(
    SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
        'business_search_service',
        '{
          "multi_index_query": {
            "name": [
              {"text": "sparkle"}
            ],
            "description": [
              {"text": "clothing washing"}
            ]
          },
          "scoring_config": {
            "weights": {
              "texts": 1,
              "vectors": 4,
              "reranker": 1
            }
          },
          "columns": ["name", "address", "description"],
          "limit": 2
        }'
    )
)['results']));
```

```
+---------------------+-----------------------------+--------------------------------------------------------------------------+
|        NAME         |           ADDRESS           |                            DESCRIPTION                                   |
|---------------------+-----------------------------+--------------------------------------------------------------------------|
| Joe's Wash n' Fold  | 456 Apple Ct, Sudsville     | Laundromat offering coin laundry and premium wash and fold services.     |
| Sparkle Wash        | 456 Clean Ave, Sudsville    | Eco-friendly car wash with free vacuum service.                          |
+---------------------+-----------------------------+--------------------------------------------------------------------------+
```

Note that because the weight of the `description` vector index colum is higher than the weight of any `text` column, the business most associated with “clothes washing” appears above the business containing “sparkle” in its name.

#### Query with individually weighted indexes

To query `example_search_service` with “circuit” over all fields, applying a relative weight to boost matches in the `name` column over the `description` column:

PythonSQL

Copy code

```
resp = business_directory.search(
    multi_index_query={
        "name": [{"text": "circuit"}],
        "address": [{"text": "circuit"}],
        "description": [{"text": "circuit"}]
    },
    scoring_config={
        "functions": {
            "text_boosts": [
                {"column": "name", "weight": 2},
                {"column": "address", "weight": 1}
            ]
        }
    },
    columns=["name", "address", "description"],
    limit=3
)
```

Copy code

```
SELECT
    value['name']::text as name, value['address']::text as address, value['description']::text as description
FROM TABLE(FLATTEN(PARSE_JSON(
    SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
        'business_search_service',
        '{
          "multi_index_query": {
            "name": [ {"text": "circuit"} ],
            "address": [ {"text": "circuit"} ],
            "description": [ {"text": "circuit"} ]
          },
          "scoring_config": {
              "functions": {
                "text_boosts": [{"column":"name", "weight": 2}, {"column":"address", "weight": 1}]
                }
          },
          "columns": ["name", "address", "description"],
          "limit": 3
        }'
    )
)['results']));
```

```
+---------------------+-----------------------------+--------------------------------------------------------------------------+
|        NAME         |           ADDRESS           |                            DESCRIPTION                                   |
|---------------------+-----------------------------+--------------------------------------------------------------------------|
| Circuit Town        | 459 Electron Dr, Sudsville  | Technology store selling used computer parts at discounted prices.       |
| Tech Haven          | 789 Circuit Blvd, Siliconia | Computer store offering the latest gadgets and tech repair services.     |
| Joe's Coffee        | 123 Bean St, Brewtown       | A cozy café known for artisan espresso and baked goods.                  |
+---------------------+-----------------------------+--------------------------------------------------------------------------+
```

Note that boosting the name over address ranks the business named “Circuit Town” above the business located at an address on “Circuit Blvd”.

### Query a service with custom vector embeddings

Examples in this section use the following `business_documents` and `example_search_service` definitions:

Copy code

```
-- Search data with only custom embeddings
CREATE OR REPLACE TABLE business_documents (
  document_contents VARCHAR,
  document_embedding VECTOR(FLOAT, 3)
);
INSERT INTO business_documents VALUES
  ('Quarterly financial report for Q1 2024: Revenue increased by 15%, with expenses stable. Highlights include strategic investments in marketing and technology.', [1, 1, 1]::VECTOR(float, 3)),
  ('IT manual for employees: Instructions for usage of internal technologies, including hardware and software guides and commonly asked tech questions.', [2, 2, 2]::VECTOR(float, 3)),
  ('Employee handbook 2024: Updated policies on remote work, health benefits, and company culture initiatives.', [2, 3, 2]::VECTOR(float, 3)),
  ('Marketing strategy document: Target audience segmentation for upcoming product launch.', [1, -1, -1]::VECTOR(float, 3))
;

-- Cortex Search Service
CREATE OR REPLACE CORTEX SEARCH SERVICE example_search_service
  TEXT INDEXES (document_contents)
  VECTOR INDEXES (document_embedding)
  WAREHOUSE = example_wh
  TARGET_LAG = '1 minute'
  AS SELECT * FROM business_documents;
```

Note

These examples use mock embeddings for simplicity. In a production use-case, vectors should be generated through a [Snowflake vector embedding model](/user-guide/snowflake-cortex/vector-embeddings#label-cortex-create-llm-embed-text) or an externally-hosted embedding model.

#### Query an index with custom embeddings

To query `example_search_service` with “IT” and a corresponding embedding over the `document_contents` and `document_embedding` column:

PythonSQL

Copy code

```
resp = business_directory.search(
    multi_index_query={
        "document_embedding": [ {"vector": [1, 1, 1]} ],
        "document_contents": [ {"text": "IT"} ]
    },
    columns=["document_contents"],
    limit=2
)
```

Copy code

```
SELECT
    value['document_contents']::text as document_contents
FROM TABLE(FLATTEN(PARSE_JSON(
    SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
        'byov_search_service',
        '{
          "multi_index_query": {
                "document_embedding": [ {"vector": [1, 1, 1] } ],
                "document_contents": [ {"text": "IT"} ]
          },
          "columns": ["document_contents"],
          "limit": 2
        }'
    )
)['results']));
```

```
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                   DOCUMENT_CONTENTS                                                                                      |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| IT manual for employees: Instructions for usage of internal technologies, including hardware and software guides and commonly asked tech questions.                      |
| Quarterly financial report for Q1 2024: Revenue increased by 15%, with expenses stable. Highlights include strategic investments in marketing and technology.            |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```
