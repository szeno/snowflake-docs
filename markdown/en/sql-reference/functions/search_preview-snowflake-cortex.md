Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# SEARCH\_PREVIEW (SNOWFLAKE.CORTEX)

Given a Cortex Search service name, and a query, returns a response from the specified service.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    '<service_name>',
    '<query_parameters_object>'
)
```

## Arguments

`service_name`
:   Name of your Cortex Search service. Use the fully qualified name if the service is in a schema different from the current session.

`query_parameters_object`
:   A [STRING](/sql-reference/data-types-text#label-character-datatypes) that contains a JSON object that specifies the query parameters for invoking the service.

    | Key | Type | Description | Default |
    | --- | --- | --- | --- |
    | `query` | String | Your search query, to search over the text column in the service. | This is required. |
    | `columns` | Array | A comma-separated list of columns to return for each relevant result in the response. These columns must be included in the source query for the service. | Search column that was specified when the service was created. |
    | `filter` | Object | A filter object for filtering results based on data in the `ATTRIBUTES` columns. For detailed syntax, see [Filter syntax](#label-cortex-search-query-syntax-filters). | Empty object |
    | `limit` | Integer | Maximum number of results to return in the response. | 10 |

    Expand

    Show lessSee more

## Filter syntax

Cortex Search supports filtering on the ATTRIBUTES columns specified in the
[CREATE CORTEX SEARCH SERVICE](/sql-reference/sql/create-cortex-search) command.

Cortex Search supports five matching operators:

- [TEXT](/sql-reference/data-types-text) or [NUMERIC](/sql-reference/data-types-numeric) equality: `@eq`
- [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) contains: `@contains`
- [NUMERIC](/sql-reference/data-types-numeric) or [DATE/TIMESTAMP](/sql-reference/data-types-datetime) greater than or equal to: `@gte`
- [NUMERIC](/sql-reference/data-types-numeric) or [DATE/TIMESTAMP](/sql-reference/data-types-datetime) less than or equal to: `@lte`
- [primary key](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys) equality: `@primarykey`

These matching operators can be composed with various logical operators:

- `@and`
- `@or`
- `@not`

The following usage notes apply:

- Matching against `NaN` (‘not a number’) values in the source query are handled as described in [Special values](/sql-reference/data-types-numeric#label-data-type-float-special-values).
- [Fixed-point](/sql-reference/data-types-numeric#label-data-types-for-fixed-point-numbers) numeric values with more than 19 digits (not including leading zeroes) do not work with `@eq`, `@gte`, or `@lte` and will not be returned by these operators.

  - For example, if there is a large value in the source query, using `@eq` to match that exact value will return no results.
  - These large values could still be returned by the overall filter with the use of `@not` (e.g. while `@eq X` will return no values for some large X, `@not @eq Y` will return it).
- `TIMESTAMP` and `DATE` filters accept values of the form: `YYYY-MM-DD` and, for timezone aware dates: `YYYY-MM-DD+HH:MM`. If the timezone offset is not specified, the date is interpreted in UTC.
- `@primarykey` is only supported for services configured with a [primary key](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys). The value of the filter must be a JSON object mapping every primary key column to its corresponding value (or `NULL`).

These operators can be combined into a single filter object.

# Example

- Filtering on rows where string-like column `string_col` is equal to value `value`.

  Copy code

  ```
  { "@eq": { "string_col": "value" } }
  ```
- Filtering to a row with the specified primary key,

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
  { "@and": [
    { "@gte": { "numeric_col": 10.5 } },
    { "@lte": { "numeric_col": 12.5 } }
  ]}
  ```
- Filtering on rows where TIMESTAMP column `timestamp_col` is between `2024-11-19` and `2024-12-19` (inclusive).

  Copy code

  ```
  { "@and": [
    { "@gte": { "timestamp_col": "2024-11-19" } },
    { "@lte": { "timestamp_col": "2024-12-19" } }
  ]}
  ```
- Composing filters with logical operators:

  Copy code

  ```
  // Rows where the "array_col" column contains "arr_value" and the "string_col" column equals "value":
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
     { "@contains": { "array_col": "val1" } },
     { "@contains": { "array_col": "val1" } }
    ]
  }
  ```

## Returns

Returns an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) that contains the result of your query from your Cortex Search service and a unique
request ID. See example output in [Examples](#examples).

## Usage notes

- This function is designed for testing and validation, and incurs more latency than using the REST or Python APIs. Use other methods to serve search queries in an end-user application that requires low latency.
- This function only operates on constant arguments. It does not accept table columns as input.
- This function truncates search results if they exceed 300kB. The REST surface allows responses up to 10MB.

## Examples

This example queries a service named `sample_service` with a `test query`.
The example returns five results (at most) and includes the data from the `col1` and `col2` columns.

Copy code

```
SELECT
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW (
      'mydb.mysch.sample_service',
      '{
          "query": "test query",
          "columns": ["col1", "col2"],
          "limit": 3
      }'
  );
```

```
{
  "results":[
      {"col1":"text", "col2":"text"},
      {"col1":"text", "col2":"text"},
      {"col1":"text", "col2":"text"}
  ],
  "request_id":"a27d1d85-e02c-4730-b320-74bf94f72d0d"
}
```
