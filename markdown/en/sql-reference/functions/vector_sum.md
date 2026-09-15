Categories:
:   [Vector functions](/sql-reference/functions-vector) , [Aggregate functions](/sql-reference/functions-aggregation)

# VECTOR\_SUM

Computes the element-wise sum of [vectors](/user-guide/snowflake-cortex/vector-embeddings) in an aggregate. Returns a vector where
each element is the sum of the corresponding elements across all input vectors.

See also:
:   [VECTOR\_MIN](/sql-reference/functions/vector_min) , [VECTOR\_MAX](/sql-reference/functions/vector_max) , [VECTOR\_AVG](/sql-reference/functions/vector_avg) , [SUM](/sql-reference/functions/sum), [Vector Embeddings](/user-guide/snowflake-cortex/vector-embeddings)

## Syntax

Copy code

```
VECTOR_SUM( <vector_column> )
```

## Arguments

`vector_column`
:   A column containing [VECTOR](/sql-reference/data-types-vector) values. All vectors in the column must have the same element type and dimension.

## Returns

Returns a VECTOR value with the same element type and dimension as the input vectors. Each element in the result vector is the sum of the corresponding elements across all input vectors.

## Usage notes

- NULL values are ignored in the aggregation.
- If all values in the group are NULL, the function returns NULL.
- All input vectors in the column must have the same dimension and element type.
- Vector functions are optimized in a way that can reduce floating point precision. This function’s results have a margin of error up to `1e-4`.

## Examples

This example demonstrates computing the element-wise sum of vectors:

Copy code

```
CREATE OR REPLACE TABLE vector_data (
  id INT,
  category VARCHAR,
  embedding VECTOR(FLOAT, 3)
);

INSERT INTO vector_data
SELECT 1, 'A', [1.0, 2.0, 3.0]::VECTOR(FLOAT, 3)
UNION ALL SELECT 2, 'A', [4.0, 5.0, 6.0]::VECTOR(FLOAT, 3)
UNION ALL SELECT 3, 'B', [2.0, 1.0, 4.0]::VECTOR(FLOAT, 3)
UNION ALL SELECT 4, 'B', [3.0, 2.0, 1.0]::VECTOR(FLOAT, 3);

-- Compute sum for each category
SELECT category, VECTOR_SUM(embedding) AS sum_vector
  FROM vector_data
  GROUP BY category
  ORDER BY category;
```

```
+----------+------------------+
| CATEGORY | SUM_VECTOR       |
+----------+------------------+
| A        | [5.0, 7.0, 9.0]  |
| B        | [5.0, 3.0, 5.0]  |
+----------+------------------+
```

This example shows scalar aggregation (no GROUP BY):

Copy code

```
SELECT VECTOR_SUM(embedding) AS total_sum
  FROM vector_data;
```

```
+--------------------+
| TOTAL_SUM          |
+--------------------+
| [10.0, 10.0, 14.0] |
+--------------------+
```
