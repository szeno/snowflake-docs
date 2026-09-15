Categories:
:   [Vector functions](/sql-reference/functions-vector) , [Aggregate functions](/sql-reference/functions-aggregation)

# VECTOR\_MIN

Computes the element-wise minimum of [vectors](/user-guide/snowflake-cortex/vector-embeddings) in an aggregate. Returns a vector where
each element is the minimum of the corresponding elements across all input vectors.

See also:
:   [VECTOR\_SUM](/sql-reference/functions/vector_sum) , [VECTOR\_MAX](/sql-reference/functions/vector_max) , [VECTOR\_AVG](/sql-reference/functions/vector_avg) , [MIN](/sql-reference/functions/min), [Vector Embeddings](/user-guide/snowflake-cortex/vector-embeddings)

## Syntax

Copy code

```
VECTOR_MIN( <vector_column> )
```

## Arguments

`vector_column`
:   A column containing [VECTOR](/sql-reference/data-types-vector) values. All vectors in the column must have the same element type and dimension.

## Returns

Returns a VECTOR value with the same element type and dimension as the input vectors. Each element in the result vector is the minimum of the corresponding elements across all input vectors.

## Usage notes

- NULL values are ignored in the aggregation.
- If all values in the group are NULL, the function returns NULL.
- All input vectors in the column must have the same dimension and element type.
- Vector functions are optimized in a way that can reduce floating point precision. This function’s results have a margin of error up to `1e-4`.

## Examples

This example demonstrates computing the element-wise minimum of vectors:

Copy code

```
CREATE OR REPLACE TABLE vector_data (
  id INT,
  category VARCHAR,
  embedding VECTOR(FLOAT, 3)
);

INSERT INTO vector_data
SELECT 1, 'A', [1.5, 8.0, 3.2]::VECTOR(FLOAT, 3)
UNION ALL SELECT 2, 'A', [4.1, 2.5, 6.7]::VECTOR(FLOAT, 3)
UNION ALL SELECT 3, 'B', [2.0, 1.0, 4.0]::VECTOR(FLOAT, 3)
UNION ALL SELECT 4, 'B', [3.0, 2.0, 1.0]::VECTOR(FLOAT, 3);

-- Compute minimum for each category
SELECT category, VECTOR_MIN(embedding) AS min_vector
  FROM vector_data
  GROUP BY category
  ORDER BY category;
```

```
+----------+------------------+
| CATEGORY | MIN_VECTOR       |
+----------+------------------+
| A        | [1.5, 2.5, 3.2] |
| B        | [2.0, 1.0, 1.0] |
+----------+------------------+
```

This example shows scalar aggregation (no GROUP BY):

Copy code

```
SELECT VECTOR_MIN(embedding) AS overall_min
  FROM vector_data;
```

```
+------------------+
| OVERALL_MIN      |
+------------------+
| [1.5, 1.0, 1.0]  |
+------------------+
```
