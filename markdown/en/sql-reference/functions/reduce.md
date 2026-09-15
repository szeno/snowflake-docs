Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Higher-order)

# REDUCE

Reduces an [array](/sql-reference/data-types-semistructured#label-data-type-array) to a single value based on the logic in a lambda expression.

The REDUCE function takes an array, an initial accumulator value, and a lambda function. It applies the lambda
function to each element of the array, updating the accumulator with each result. After processing all elements,
REDUCE returns the final accumulator value.

See also:
:   [Use lambda functions on data with Snowflake higher-order functions](/user-guide/querying-semistructured#label-higher-order-functions)

## Syntax

Copy code

```
REDUCE( <array> , <init> , <lambda_expression> )
```

## Arguments

`array`
:   The array that contains the elements to be reduced. The array can be semi-structured or structured.

`init`
:   The initial accumulator value.

`lambda_expression`
:   A [lambda expression](/user-guide/querying-semistructured#label-higher-order-functions-lambda-expressions) that defines the reduce
    logic on each array element.

    The lambda expression must be specified in the following syntax:

    Copy code

    ```
    <acc> [ <datatype> ] , <value> [ <datatype> ] -> <expr>
    ```

    The `acc` argument is the accumulator, and the `value` argument is the current element
    being processed in the array.

## Returns

This function can return a value of any data type.

If the input array is empty, then the function returns the initial value of the accumulator.

The function returns NULL in these cases:

- The input array is NULL.
- The initial value of the accumulator is NULL.
- The lambda function returns NULL.

## Usage notes

- When the data type for a lambda `value` argument is explicitly specified, the array element is coerced into the specified type
  before lambda invocation. For information about coercion, see [Data type conversion](/sql-reference/data-type-conversion).
- Type checking enforces that the initial value of the accumulator, the accumulator lambda argument, and the return value
  of the lambda execution all have the same logical and physical types. If [casting](/sql-reference/data-type-conversion)
  is used to meet this requirement, the largest physical type of the three is used.
- The `value` argument can have intermediate NULL values. For an example, see [Skip NULL values in an array](#label-reduce-function-skip-nulls).

## Examples

The following examples use the REDUCE function.

### Calculate the sum of the values in an array

Use the REDUCE function to return the sum of the values in an array and specify `0` for the initial
accumulator value:

Copy code

```
SELECT REDUCE([1,2,3],
              0,
              (acc, val) -> acc + val
       ) AS sum_of_values;
```

```
+---------------+
| SUM_OF_VALUES |
|---------------|
|             6 |
+---------------+
```

This example is the same as the previous example, but it specifies a structured array of type INT:

Copy code

```
SELECT REDUCE([1,2,3]::ARRAY(INT),
              0,
              (acc, val) -> acc + val
       ) AS sum_of_values_structured;
```

```
+--------------------------+
| SUM_OF_VALUES_STRUCTURED |
|--------------------------|
|                        6 |
+--------------------------+
```

Use the REDUCE function to return the sum of the values in an array and specify `10` for the initial
accumulator value:

Copy code

```
SELECT REDUCE([1,2,3],
              10,
              (acc, val) -> acc + val
       ) AS sum_of_values_plus_10;
```

```
+-----------------------+
| SUM_OF_VALUES_PLUS_10 |
|-----------------------|
|                    16 |
+-----------------------+
```

### Calculate the sum of the square of each value in an array

Use the REDUCE function to return the sum of the square of each value in the array, and specify `0`
for the initial accumulator value:

Copy code

```
SELECT REDUCE([1,2,3],
              0,
              (acc, val) -> acc + val * val
       ) AS sum_of_squares;
```

```
+----------------+
| SUM_OF_SQUARES |
|----------------|
|             14 |
+----------------+
```

### Skip NULL values in an array

In this example, the `array` argument includes NULL values. When this array is passed to
the REDUCE function, the accumulator will have intermediate NULL values.

Use the REDUCE function to return the sum of the values in the array, and use the
[ZEROIFNULL](/sql-reference/functions/zeroifnull) function in the logic of the lambda expression to skip
NULL values in the array. The lambda expression uses the ZEROIFNULL function to process each value
in the array using the following logic:

- If `val` is NULL, then the result of the lambda expression is `acc + 0`.
- If `val` is not NULL, then the result of the lambda expression is `acc + val`.

Run the query:

Copy code

```
SELECT REDUCE([1,NULL,2,NULL,3,4],
              0,
              (acc, val) -> acc + ZEROIFNULL(val))
  AS sum_of_values_skip_null;
```

```
+-------------------------+
| SUM_OF_VALUES_SKIP_NULL |
|-------------------------|
|                      10 |
+-------------------------+
```

### Generate string values

Use the REDUCE function to return a list of string values by concatenating each value
in the array:

Copy code

```
SELECT REDUCE(['a', 'b', 'c'],
              '',
              (acc, val) -> acc || ' ' || val
       ) AS string_values;
```

```
+---------------+
| STRING_VALUES |
|---------------|
|  a b c        |
+---------------+
```

### Use an array for the accumulator

Use the REDUCE function along with the [ARRAY\_PREPEND](/sql-reference/functions/array_prepend) function in the logic
of the lambda expression to return an array that reverses the order of the input array:

Copy code

```
SELECT REDUCE([1, 2, 3, 4],
              [],
              (acc, val) -> ARRAY_PREPEND(acc, val)
       ) AS reverse_order;
```

```
+---------------+
| REVERSE_ORDER |
|---------------|
| [             |
|   4,          |
|   3,          |
|   2,          |
|   1           |
| ]             |
+---------------+
```

### Use conditional logic

Use the REDUCE function along with the [IFF](/sql-reference/functions/iff) function in the logic
of the lambda expression to perform an action based on conditional logic similar to an `if-then`
expression. This example uses the following logic in the lambda expression:

- If the array value is less than seven, then square it and add it to the accumulator.
- If the array value is greater than or equal to seven, then add it to the accumulator without
  squaring it.

Copy code

```
SELECT REDUCE([5,10,15],
              0,
              (acc, val) -> IFF(val < 7, acc + val * val, acc + val)
       ) AS conditional_logic;
```

```
+-------------------+
| CONDITIONAL_LOGIC |
|-------------------|
|                50 |
+-------------------+
```

### Reduce an array of elements in a table to a single value

Assume you have a table named `orders` with the columns `order_id`, `order_date`, and `order_detail`. The
`order_detail` column is an array of the line items, their purchase quantity, and subtotal. The table contains
two rows of data. The following SQL statement creates this table and inserts the rows:

Copy code

```
CREATE OR REPLACE TABLE orders AS
  SELECT 1 AS order_id, '2024-01-01' AS order_date, [
    {'item':'UHD Monitor', 'quantity':3, 'subtotal':1500},
    {'item':'Business Printer', 'quantity':1, 'subtotal':1200}
  ] AS order_detail
  UNION
  SELECT 2 AS order_id, '2024-01-02' AS order_date, [
    {'item':'Laptop', 'quantity':5, 'subtotal':7500},
    {'item':'Noise-canceling Headphones', 'quantity':5, 'subtotal':1000}
  ] AS order_detail;

SELECT * FROM orders;
```

```
+----------+------------+-------------------------------------------+
| ORDER_ID | ORDER_DATE | ORDER_DETAIL                              |
|----------+------------+-------------------------------------------|
|        1 | 2024-01-01 | [                                         |
|          |            |   {                                       |
|          |            |     "item": "UHD Monitor",                |
|          |            |     "quantity": 3,                        |
|          |            |     "subtotal": 1500                      |
|          |            |   },                                      |
|          |            |   {                                       |
|          |            |     "item": "Business Printer",           |
|          |            |     "quantity": 1,                        |
|          |            |     "subtotal": 1200                      |
|          |            |   }                                       |
|          |            | ]                                         |
|        2 | 2024-01-02 | [                                         |
|          |            |   {                                       |
|          |            |     "item": "Laptop",                     |
|          |            |     "quantity": 5,                        |
|          |            |     "subtotal": 7500                      |
|          |            |   },                                      |
|          |            |   {                                       |
|          |            |     "item": "Noise-canceling Headphones", |
|          |            |     "quantity": 5,                        |
|          |            |     "subtotal": 1000                      |
|          |            |   }                                       |
|          |            | ]                                         |
+----------+------------+-------------------------------------------+
```

Use the REDUCE function to return the subtotal sum for all items in each order:

Copy code

```
SELECT order_id,
       order_date,
       REDUCE(o.order_detail,
              0,
              (acc, val) -> acc + val:subtotal
       ) AS subtotal_sum
  FROM orders o;
```

```
+----------+------------+--------------+
| ORDER_ID | ORDER_DATE | SUBTOTAL_SUM |
|----------+------------+--------------|
|        1 | 2024-01-01 |         2700 |
|        2 | 2024-01-02 |         8500 |
+----------+------------+--------------+
```

Use the REDUCE function to return a list of the items sold in each order:

Copy code

```
SELECT order_id,
       order_date,
       REDUCE(o.order_detail,
              '',
              (acc, val) -> val:item || '\n' || acc
       ) AS items_sold
  FROM orders o;
```

```
+----------+------------+-----------------------------+
| ORDER_ID | ORDER_DATE | ITEMS_SOLD                  |
|----------+------------+-----------------------------|
|        1 | 2024-01-01 | Business Printer            |
|          |            | UHD Monitor                 |
|          |            |                             |
|        2 | 2024-01-02 | Noise-canceling Headphones  |
|          |            | Laptop                      |
|          |            |                             |
+----------+------------+-----------------------------+
```

### Reference a table column in a lambda expression to reduce array elements in table data

Create a table with one column of type ARRAY and another column of type INT:

Copy code

```
CREATE OR REPLACE TABLE reduce_column_ref_demo AS
  SELECT [ 1, 2, 3 ] AS col1, 0 AS col2
  UNION
  SELECT [ 1, 2, 3 ] AS col1, 10 AS col2;

SELECT * FROM reduce_column_ref_demo;
```

```
+------+------+
| COL1 | COL2 |
|------+------|
| [    |    0 |
|   1, |      |
|   2, |      |
|   3  |      |
| ]    |      |
| [    |   10 |
|   1, |      |
|   2, |      |
|   3  |      |
| ]    |      |
+------+------+
```

Use the REDUCE function to return the sum of the values in the array in each row by adding the value
in `col2` to the accumulator value:

Copy code

```
SELECT REDUCE(col1,
              10,
              (acc, val) -> (acc + col2) + val
       ) AS reduce_col_ref
  FROM reduce_column_ref_demo;
```

```
+----------------+
| REDUCE_COL_REF |
|----------------|
|             16 |
|             46 |
+----------------+
```
