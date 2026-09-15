Categories:
:   [Vector functions](/sql-reference/functions-vector) , [Aggregate functions](/sql-reference/functions-aggregation)

# VECTOR\_AVG

Computes the element-wise average of [vectors](/user-guide/snowflake-cortex/vector-embeddings) in an aggregate. Returns a vector where
each element is the average of the corresponding elements across all input vectors. The output is always VECTOR(FLOAT, N) regardless of input type.

See also:
:   [VECTOR\_SUM](/sql-reference/functions/vector_sum) , [VECTOR\_MIN](/sql-reference/functions/vector_min) , [VECTOR\_MAX](/sql-reference/functions/vector_max) , [AVG](/sql-reference/functions/avg), [Vector Embeddings](/user-guide/snowflake-cortex/vector-embeddings)

## Syntax

Copy code

```
VECTOR_AVG( <vector_column> )
```

## Arguments

`vector_column`
:   A column containing [VECTOR](/sql-reference/data-types-vector) values. All vectors in the column must have the same element type and dimension.

## Returns

Returns a VECTOR(FLOAT, N) value where N is the dimension of the input vectors. Each element in the result vector is the average of the corresponding elements across all input vectors.

## Usage notes

- NULL values are ignored in the aggregation.
- If all values in the group are NULL, the function returns NULL.
- All input vectors in the column must have the same dimension and element type.
- The output is always VECTOR(FLOAT, N) regardless of the input’s type. For information on floating-point numbers in Snowflake, see [Floating-point data types](/sql-reference/data-types-numeric#label-data-type-float).
- Vector functions are optimized in a way that can reduce floating point precision. This function’s results have a margin of error up to `1e-4`.

## Examples

This example demonstrates computing the element-wise average of vectors:

Copy code

```
CREATE OR REPLACE TABLE vector_data (
  id INT,
  category VARCHAR,
  embedding VECTOR(FLOAT, 3)
);

INSERT INTO vector_data
SELECT 1, 'A', [2.0, 4.0, 6.0]::VECTOR(FLOAT, 3)
UNION ALL SELECT 2, 'A', [4.0, 8.0, 12.0]::VECTOR(FLOAT, 3)
UNION ALL SELECT 3, 'B', [1.0, 2.0, 3.0]::VECTOR(FLOAT, 3)
UNION ALL SELECT 4, 'B', [3.0, 6.0, 9.0]::VECTOR(FLOAT, 3);

-- Compute average for each category
SELECT category, VECTOR_AVG(embedding) AS avg_vector
  FROM vector_data
  GROUP BY category
  ORDER BY category;
```

```
+----------+------------------+
| CATEGORY | AVG_VECTOR       |
+----------+------------------+
| A        | [3.0, 6.0, 9.0] |
| B        | [2.0, 4.0, 6.0] |
+----------+------------------+
```

This example shows scalar aggregation (no GROUP BY):

Copy code

```
SELECT VECTOR_AVG(embedding) AS overall_avg
  FROM vector_data;
```

```
+------------------+
| OVERALL_AVG      |
+------------------+
| [2.5, 5.0, 7.5]  |
+------------------+
```

This example shows how integer vectors are converted to float output:

Copy code

```
CREATE OR REPLACE TABLE int_vector_data (
  id INT,
  vec VECTOR(INT, 2)
);

INSERT INTO int_vector_data
SELECT 1, [1, 3]::VECTOR(INT, 2)
UNION ALL SELECT 2, [2, 4]::VECTOR(INT, 2);

SELECT VECTOR_AVG(vec) AS avg_result
  FROM int_vector_data;
```

```
+-------------+
| AVG_RESULT  |
+-------------+
| [1.5, 3.5]  |
+-------------+
```
