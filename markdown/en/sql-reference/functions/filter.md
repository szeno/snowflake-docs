Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Higher-order)

# FILTER

Filters an [array](/sql-reference/data-types-semistructured#label-data-type-array) based on the logic in a lambda expression.

See also:
:   [Use lambda functions on data with Snowflake higher-order functions](/user-guide/querying-semistructured#label-higher-order-functions)

## Syntax

Copy code

```
FILTER( <array> , <lambda_expression> )
```

## Arguments

`array`
:   The array that contains the elements to be filtered. The array can be semi-structured or structured.

`lambda_expression`
:   A [lambda expression](/user-guide/querying-semistructured#label-higher-order-functions-lambda-expressions) that defines the filter
    condition on each array element.

    The lambda expression must have only one argument specified in the following syntax:

    Copy code

    ```
    <arg> [ <datatype> ] -> <expr>
    ```

## Returns

The return type of this function is an array of the same type as the input array. The returned array contains the elements
for which the filter condition returns TRUE.

If either argument is NULL, the function returns NULL without reporting an error.

## Usage notes

- When the data type for the lambda argument is explicitly specified, the array element is coerced into the specified type
  before lambda invocation. For information about coercion, see [Data type conversion](/sql-reference/data-type-conversion).
- If the filter condition evaluates to NULL, the corresponding array element is filtered out.

## Examples

The following examples use the FILTER function.

### Filter for array elements greater than a value

Use the FILTER function to return objects in an array that have a value greater than or equal to 50:

Copy code

```
SELECT FILTER(
  [
    {'name':'Pat', 'value': 50},
    {'name':'Terry', 'value': 75},
    {'name':'Dana', 'value': 25}
  ],
  a -> a:value >= 50
) AS "Filter >= 50";
```

```
+----------------------+
| Filter >= 50         |
|----------------------|
| [                    |
|   {                  |
|     "name": "Pat",   |
|     "value": 50      |
|   },                 |
|   {                  |
|     "name": "Terry", |
|     "value": 75      |
|   }                  |
| ]                    |
+----------------------+
```

### Filter for array elements that are not NULL

Use the FILTER function to return array elements that are not NULL:

Copy code

```
SELECT FILTER([1, NULL, 3, 5, NULL], a -> a IS NOT NULL) AS "Not NULL Elements";
```

```
+-------------------+
| Not NULL Elements |
|-------------------|
| [                 |
|   1,              |
|   3,              |
|   5               |
| ]                 |
+-------------------+
```

### Filter for array elements in a table that are greater than or equal to a value

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

Use the FILTER function to return orders with subtotals that are greater than or equal to 1500:

Copy code

```
SELECT order_id,
       order_date,
       FILTER(o.order_detail, i -> i:subtotal >= 1500) AS order_detail_gt_equal_1500
  FROM orders o;
```

```
+----------+------------+----------------------------+
| ORDER_ID | ORDER_DATE | ORDER_DETAIL_GT_EQUAL_1500 |
|----------+------------+----------------------------|
|        1 | 2024-01-01 | [                          |
|          |            |   {                        |
|          |            |     "item": "UHD Monitor", |
|          |            |     "quantity": 3,         |
|          |            |     "subtotal": 1500       |
|          |            |   }                        |
|          |            | ]                          |
|        2 | 2024-01-02 | [                          |
|          |            |   {                        |
|          |            |     "item": "Laptop",      |
|          |            |     "quantity": 5,         |
|          |            |     "subtotal": 7500       |
|          |            |   }                        |
|          |            | ]                          |
+----------+------------+----------------------------+
```

### Reference a table column in a lambda expression to filter array elements in table data

Create a table with one column of type ARRAY and another column of type INT:

Copy code

```
CREATE OR REPLACE TABLE filter_column_ref_demo AS
  SELECT [ 10, 15, 20 ] AS col1, 18 AS col2
  UNION
  SELECT [ 30, 50, 70 ] AS col1, 40 AS col2;

SELECT * FROM filter_column_ref_demo;
```

```
+-------+------+
| COL1  | COL2 |
|-------+------|
| [     |   18 |
|   10, |      |
|   15, |      |
|   20  |      |
| ]     |      |
| [     |   40 |
|   30, |      |
|   50, |      |
|   70  |      |
| ]     |      |
+-------+------+
```

Use the FILTER function to return the values of array element values in each row that are lower
than the value in `col2`:

Copy code

```
SELECT FILTER(col1, v -> v < col2) AS filter_col_ref
  FROM filter_column_ref_demo;
```

```
+----------------+
| FILTER_COL_REF |
|----------------|
| [              |
|   10,          |
|   15           |
| ]              |
| [              |
|   30           |
| ]              |
+----------------+
```
