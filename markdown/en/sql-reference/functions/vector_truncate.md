Categories:
:   [Vector functions](/sql-reference/functions-vector)

# VECTOR\_TRUNCATE

Truncates a [VECTOR](/sql-reference/data-types-vector) to a smaller dimension.

This function can also be called through the alias VECTOR\_TRUNC.

See also:
:   [Vector Embeddings](/user-guide/snowflake-cortex/vector-embeddings), [VECTOR\_NORMALIZE](/sql-reference/functions/vector_normalize)

## Syntax

Copy code

```
VECTOR_TRUNCATE( <vector>, <dimension> )
```

## Arguments

`vector`
:   A single [VECTOR](/sql-reference/data-types-vector) value to truncate.

`dimension`
:   The number of elements that should be in the returned vector.

## Returns

Returns a VECTOR value with the same values and types for the first `dimension` entries, with the remainder discarded.

## Usage notes

- Returns NULL when any input is NULL.
- Using a `dimension` larger than the number of dimensions in the `vector` causes an error.
- Truncated vectors are not normalized.

## Examples

This example demonstrates truncating a 3-dimensional vector into a 2-dimensional vector:

Copy code

```
SELECT VECTOR_TRUNCATE([1, 2, 3]::VECTOR(INT, 3), 2);
```

```
[1,2]
```

This example demonstrates truncating a vector produced by [AI\_EMBED](/sql-reference/functions/ai_embed) for the text “Analytical databases are typically column-oriented rather than row-oriented” with the `snowflake-arctic-embed-m-v1.5` model from 768 elements to 256 elements:

Copy code

```
SELECT VECTOR_TRUNCATE(
    AI_EMBED(
        'snowflake-arctic-embed-m-v1.5',
        'Analytical databases are typically column-oriented rather than row-oriented'
    ),
    256)
;
```
