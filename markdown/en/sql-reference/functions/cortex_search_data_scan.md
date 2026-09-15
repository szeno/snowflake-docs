Categories:
:   [Table functions](/sql-reference/functions-table)

# CORTEX\_SEARCH\_DATA\_SCAN

This table function returns the data indexed by a [Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview),
including the columns defined in the source query and the computed vector embeddings for the search column.

## Syntax

Copy code

```
CORTEX_SEARCH_DATA_SCAN(
      SERVICE_NAME => '<string>' )
```

## Arguments

**Required:**

`SERVICE_NAME => 'string'`
:   The name of a Cortex Search service.

    You can specify any of the following:

    - Unqualified name (`service_name`)
    - Partially qualified name (`schema_name.service_name`)
    - Fully qualified name (`database_name.schema_name.service_name`)

    For more information on object name resolution, refer to [Object Name Resolution](/sql-reference/name-resolution).

## Output

The function returns all the columns specified in the source query and the embeddings for the search column. The embedding column is of [VECTOR data type](/sql-reference/data-types-vector) and is named `_GENERATED_EMBEDDINGS_{MODEL_NAME}`.

The order of the columns is the same as the order of the columns in the source query with the embedding column appended at the end.

## Usage notes

- Requires OPERATE privilege for Cortex Search. Refer to [Access control privileges](/user-guide/security-access-control-privileges) for more details.

## Examples

Suppose you have a Cortex Search service named `transcript_search_service` defined as follows:

Copy code

```
CREATE OR REPLACE CORTEX SEARCH SERVICE transcript_search_service
  ON transcript_text
  ATTRIBUTES region
  WAREHOUSE = cortex_search_wh
  TARGET_LAG = '1 day'
  AS (
    SELECT
        transcript_text,
        region,
        agent_id,
    FROM support_transcripts
);
```

For instructions about creating a Cortex Search service, see [Cortex Search Overview](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview).

You can use the table function to retrieve the contents for the Cortex Search service `transcript_search_service`:

Copy code

```
SELECT
  *
FROM
  TABLE (
    CORTEX_SEARCH_DATA_SCAN (
      SERVICE_NAME => 'transcript_search_service'
    )
  );
```

```
+ ---------------------------------------------------------- + --------------- + -------- + ------------------------------ +
|                      transcript_text                       |     region      | agent_id | _GENERATED_EMBEDDINGS_MY_MODEL |
| ---------------------------------------------------------- | --------------- | -------- | ------------------------------ |
| 'My internet has been down since yesterday, can you help?' | 'North America' | 'AG1001' | [0.1, 0.2, 0.3, 0.4]           |
| 'I was overcharged for my last bill, need an explanation.' | 'Europe'        | 'AG1002' | [0.1, 0.2, 0.3, 0.4]           |
+ ---------------------------------------------------------- + --------------- + -------- + ------------------------------ +
```
