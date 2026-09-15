Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# [ NOT ] IN

Tests whether its argument is or is not one of the members of an explicit list or the result of a subquery.

Note

In subquery form, IN is equivalent to `= ANY` and NOT IN is equivalent to `<> ALL`.

Tip

You can use the search optimization service to improve the performance of queries that call this function.
For details, see [Search optimization service](/user-guide/search-optimization-service).

## Syntax

To compare individual values:

Copy code

```
<value> [ NOT ] IN ( <value_1> [ , <value_2> ...  ] )
```

To compare *row constructors* (parenthesized lists of values):

Copy code

```
( <value_A> [, <value_B> ... ] ) [ NOT ] IN (  ( <value_1> [ , <value_2> ... ] )  [ , ( <value_3> [ , <value_4> ... ] )  ...  ]  )
```

To compare a value to the values returned by a subquery:

Copy code

```
<value> [ NOT ] IN ( <subquery> )
```

## Parameters

`value`
:   The value for which to search.

`value_A`, `value_B`
:   The elements of a row constructor for which to search.

    Ensure that each value on the right of IN (for example, `(value3, value4)`) has the same number of elements as the value on the
    left of IN (for example, `(value_A, value_B)`).

`value_#`
:   A value to which `value` should be compared.

    If the values to compare to are row constructors, then each `value_#` is an individual element of a row constructor.

`subquery`
:   A subquery that returns a list of values to which `value` can be compared.

## Usage notes

- As in most contexts, NULL is not equal to NULL. If `value` is NULL, then the
  return value of the function is NULL, whether or not the list or subquery
  contains NULL. See [Using NULL](#label-in-list-null-examples).
- Syntactically, IN is treated as an operator rather than a function. This example shows the difference between
  using IN as an operator and calling `f()` as a function:

  Copy code

  ```
  SELECT
   f(a, b),
   x IN (y, z) ...
  ```

  You *can’t* use function syntax with IN. For example, you can’t rewrite the preceding example as:

  Copy code

  ```
  SELECT
   f(a, b),
   IN(x, (y, z)) ...
  ```
- IN is also considered a [subquery operator](/sql-reference/operators-subquery).
- In a query that uses IN, you can expand an [array](/sql-reference/data-types-semistructured#label-data-type-array) into
  a list of individual values by using the spread operator (`**`). For more information and
  examples, see [Expansion operators](/sql-reference/operators-expansion).

## Collation details

Arguments with collation specifications currently aren’t supported.

## Examples

The following examples use the IN function.

### Using IN with simple literals

The following examples show how to use IN and NOT IN with simple literals:

Copy code

```
SELECT 1 IN (1, 2, 3) AS RESULT;
```

```
+--------+
| RESULT |
|--------|
| True   |
+--------+
```

Copy code

```
SELECT 4 NOT IN (1, 2, 3) AS RESULT;
```

```
+--------+
| RESULT |
|--------|
| True   |
+--------+
```

### Using IN with a subquery

This example shows how to use IN in a subquery.

Copy code

```
SELECT 'a' IN (
  SELECT column1 FROM VALUES ('b'), ('c'), ('d')
  ) AS RESULT;
```

```
+--------+
| RESULT |
|--------|
| False  |
+--------+
```

### Using IN with a table

These examples show how to use IN with a table. The statement below creates the table used in the examples.

Copy code

```
CREATE OR REPLACE TABLE in_function_demo (
  col_1 INTEGER,
  col_2 INTEGER,
  col_3 INTEGER);

INSERT INTO in_function_demo (col_1, col_2, col_3) VALUES
  (1, 1, 1),
  (1, 2, 3),
  (4, 5, NULL);
```

This example shows how to use IN with a single column of a table:

Copy code

```
SELECT col_1, col_2, col_3
  FROM in_function_demo
  WHERE (col_1) IN (1, 10, 100, 1000)
  ORDER BY col_1, col_2, col_3;
```

```
+-------+-------+-------+
| COL_1 | COL_2 | COL_3 |
|-------+-------+-------|
|     1 |     1 |     1 |
|     1 |     2 |     3 |
+-------+-------+-------+
```

This example shows how to use IN with multiple columns of a table:

Copy code

```
SELECT col_1, col_2, col_3
  FROM in_function_demo
  WHERE (col_1, col_2, col_3) IN (
    (1,2,3),
    (4,5,6));
```

```
+-------+-------+-------+
| COL_1 | COL_2 | COL_3 |
|-------+-------+-------|
|     1 |     2 |     3 |
+-------+-------+-------+
```

This example shows how to use IN with a subquery that reads multiple columns of a table:

Copy code

```
SELECT (1, 2, 3) IN (
  SELECT col_1, col_2, col_3 FROM in_function_demo
  ) AS RESULT;
```

```
+--------+
| RESULT |
|--------|
| True   |
+--------+
```

### Using NULL

Remember that NULL != NULL. IN and NOT IN lists that contain comparisons with NULL (including equality conditions) might produce unexpected
results because NULL represents an unknown value. Comparisons with NULL do not return TRUE or FALSE; they return NULL. See also
[Ternary logic](/sql-reference/ternary-logic).

For example, the following query returns NULL, not TRUE, because SQL cannot determine whether NULL equals any value, including another NULL.

Copy code

```
SELECT NULL IN (1, 2, NULL) AS RESULT;
```

```
+--------+
| RESULT |
|--------|
| NULL   |
+--------+
```

Note that if you change the query to select `1`, not NULL, it returns TRUE:

Copy code

```
SELECT 1 IN (1, 2, NULL) AS RESULT;
```

```
+--------+
| RESULT |
|--------|
| True   |
+--------+
```

In this case, the result is TRUE because `1` does have a match in the IN list. The fact that NULL also exists
in the IN list doesn’t affect the result.

Similarly, NOT IN comparisons with NULL also return NULL if any value in the list is NULL.

Copy code

```
SELECT 1 NOT IN (1, 2, NULL) AS RESULT;
```

```
+--------+
| RESULT |
|--------|
| NULL  |
+--------+
```

The same behavior is true for the following query, where the set of values `4, 5, NULL` *does not match* either `4, 5, NULL` or `7, 8, 9`:

Copy code

```
SELECT (4, 5, NULL) IN ( (4, 5, NULL), (7, 8, 9) ) AS RESULT;
```

The following example shows the same behavior with NULL comparisons but uses a subquery to define the IN list values that are compared:

Copy code

```
CREATE OR REPLACE TABLE in_list_table (
  val1 INTEGER,
  val2 INTEGER,
  val3 INTEGER
);

INSERT INTO in_list_table VALUES (1, 10, NULL), (2, 20, NULL), (NULL, NULL, NULL);

SELECT 1 IN (SELECT val1 FROM in_list_table) AS RESULT;
```

```
+--------+
| RESULT |
|--------|
| True   |
+--------+
```

Copy code

```
SELECT NULL IN (SELECT val1 FROM in_list_table) AS RESULT;
```

```
+--------+
| RESULT |
|--------|
| NULL   |
+--------+
```

Copy code

```
SELECT 3 IN (SELECT val1 FROM in_list_table) AS RESULT;
```

```
+--------+
| RESULT |
|--------|
| NULL   |
+--------+
```
