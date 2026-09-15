Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Higher-order)

# TRANSFORM

Transforms an [array](/sql-reference/data-types-semistructured#label-data-type-array) based on the logic in a lambda expression.

See also:
:   [Use lambda functions on data with Snowflake higher-order functions](/user-guide/querying-semistructured#label-higher-order-functions)

## Syntax

Copy code

```
TRANSFORM( <array> , <lambda_expression> )
```

## Arguments

`array`
:   The array that contains the elements to be transformed. The array can be semi-structured or structured.

`lambda_expression`
:   A [lambda expression](/user-guide/querying-semistructured#label-higher-order-functions-lambda-expressions) that defines the transformation
    logic on each array element.

    The lambda expression must have only one argument specified in the following syntax:

    Copy code

    ```
    <arg> [ <datatype> ] -> <expr>
    ```

## Returns

The return type of this function is a semi-structured or structured array of the lambda expression result.

If either argument is NULL, the function returns NULL without reporting an error.

## Usage notes

- When the data type for the lambda argument is explicitly specified, the array element is coerced into the specified type
  before lambda invocation. For information about coercion, see [Data type conversion](/sql-reference/data-type-conversion).
- When there is no data type specified for the lambda argument, its data type is derived from the input array as follows:

  - If the input array is semi-structured, the data type of the lambda argument is [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant).
  - If the input array is structured, the data type of the lambda argument is the data type of the array element.
- For semi-structured array input, a semi-structured array is returned. For structured array input, a structured array
  of the lambda expression result type is returned.

## Examples

The following examples use the TRANSFORM function.

### Multiply each element in an array by a value

Use the TRANSFORM function to multiply each element in an array by two:

Copy code

```
SELECT TRANSFORM([1, 2, 3], a INT -> a * 2) AS "Multiply by Two";
```

```
+-----------------+
| Multiply by Two |
|-----------------|
| [               |
|   2,            |
|   4,            |
|   6             |
| ]               |
+-----------------+
```

This example is the same as the previous example, but it specifies a structured array of type INT:

Copy code

```
SELECT TRANSFORM([1, 2, 3]::ARRAY(INT), a INT -> a * 2) AS "Multiply by Two (Structured)";
```

```
+------------------------------+
| Multiply by Two (Structured) |
|------------------------------|
| [                            |
|   2,                         |
|   4,                         |
|   6                          |
| ]                            |
+------------------------------+
```

### Return values in an array with added text

Use the TRANSFORM function to return the value of each object in an array, and add text to each one:

Copy code

```
SELECT TRANSFORM(
    [
      {'name':'Pat', 'value': 50},
      {'name':'Terry', 'value': 75},
      {'name':'Dana', 'value': 25}
    ],
    c -> c:value || ' is the number'
  ) AS "Return Values";
```

```
+-----------------------+
| Return Values         |
|-----------------------|
| [                     |
|   "50 is the number", |
|   "75 is the number", |
|   "25 is the number"  |
| ]                     |
+-----------------------+
```

### Transform array elements in table data

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

Use the TRANSFORM function to add a `unit_price` element to each array in the `orders` table:

Copy code

```
SELECT order_id,
       order_date,
       TRANSFORM(o.order_detail, i -> OBJECT_INSERT(
         i,
         'unit_price',
         (i:subtotal / i:quantity)::NUMERIC(10,2)
         )
       ) AS order_detail_with_unit_price
  FROM orders o;
```

```
+----------+------------+-------------------------------------------+
| ORDER_ID | ORDER_DATE | ORDER_DETAIL_WITH_UNIT_PRICE              |
|----------+------------+-------------------------------------------|
|        1 | 2024-01-01 | [                                         |
|          |            |   {                                       |
|          |            |     "item": "UHD Monitor",                |
|          |            |     "quantity": 3,                        |
|          |            |     "subtotal": 1500,                     |
|          |            |     "unit_price": 500                     |
|          |            |   },                                      |
|          |            |   {                                       |
|          |            |     "item": "Business Printer",           |
|          |            |     "quantity": 1,                        |
|          |            |     "subtotal": 1200,                     |
|          |            |     "unit_price": 1200                    |
|          |            |   }                                       |
|          |            | ]                                         |
|        2 | 2024-01-02 | [                                         |
|          |            |   {                                       |
|          |            |     "item": "Laptop",                     |
|          |            |     "quantity": 5,                        |
|          |            |     "subtotal": 7500,                     |
|          |            |     "unit_price": 1500                    |
|          |            |   },                                      |
|          |            |   {                                       |
|          |            |     "item": "Noise-canceling Headphones", |
|          |            |     "quantity": 5,                        |
|          |            |     "subtotal": 1000,                     |
|          |            |     "unit_price": 200                     |
|          |            |   }                                       |
|          |            | ]                                         |
+----------+------------+-------------------------------------------+
```

Use the TRANSFORM function along with the [OBJECT\_DELETE](/sql-reference/functions/object_delete) function in the logic of the
lambda expression to delete the `quantity` element in each array from the `orders` table:

Copy code

```
SELECT order_id,
       order_date,
       TRANSFORM(o.order_detail, i -> OBJECT_DELETE(
         i,
         'quantity'
         )
       ) AS order_detail_without_quantity
  FROM orders o;
```

```
+----------+------------+-------------------------------------------+
| ORDER_ID | ORDER_DATE | ORDER_DETAIL_WITHOUT_QUANTITY             |
|----------+------------+-------------------------------------------|
|        1 | 2024-01-01 | [                                         |
|          |            |   {                                       |
|          |            |     "item": "UHD Monitor",                |
|          |            |     "subtotal": 1500                      |
|          |            |   },                                      |
|          |            |   {                                       |
|          |            |     "item": "Business Printer",           |
|          |            |     "subtotal": 1200                      |
|          |            |   }                                       |
|          |            | ]                                         |
|        2 | 2024-01-02 | [                                         |
|          |            |   {                                       |
|          |            |     "item": "Laptop",                     |
|          |            |     "subtotal": 7500                      |
|          |            |   },                                      |
|          |            |   {                                       |
|          |            |     "item": "Noise-canceling Headphones", |
|          |            |     "subtotal": 1000                      |
|          |            |   }                                       |
|          |            | ]                                         |
+----------+------------+-------------------------------------------+
```

### Reference a table column in a lambda expression to transform array elements in table data

Create a table with one column of type ARRAY and another column of type INT:

Copy code

```
CREATE OR REPLACE TABLE transform_column_ref_demo AS
  SELECT [ 1, 2, 3 ] AS col1, 10 AS col2
  UNION
  SELECT [ 4, 5, 6 ] AS col1, -1 AS col2
  UNION
  SELECT [ 7, 8, 9 ] AS col1, NULL AS col2;

SELECT * FROM transform_column_ref_demo;
```

```
+------+------+
| COL1 | COL2 |
|------+------|
| [    |   10 |
|   1, |      |
|   2, |      |
|   3  |      |
| ]    |      |
| [    |   -1 |
|   4, |      |
|   5, |      |
|   6  |      |
| ]    |      |
| [    | NULL |
|   7, |      |
|   8, |      |
|   9  |      |
| ]    |      |
+------+------+
```

Use the TRANSFORM function to add the value in `col2` to the value of each array element in each row:

Copy code

```
SELECT TRANSFORM(col1, v INT -> v + col2) AS transform_col_ref
  FROM transform_column_ref_demo;
```

```
+-------------------+
| TRANSFORM_COL_REF |
|-------------------|
| [                 |
|   11,             |
|   12,             |
|   13              |
| ]                 |
| [                 |
|   3,              |
|   4,              |
|   5               |
| ]                 |
| [                 |
|   undefined,      |
|   undefined,      |
|   undefined       |
| ]                 |
+-------------------+
```
