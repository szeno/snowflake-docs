# Scalar SQL UDFs

This topic covers concepts and usage details that are specific to SQL UDFs (user-defined functions).

## General usage

A SQL UDF evaluates an arbitrary SQL expression and returns the result(s) of the expression.

The function definition can be a SQL expression that returns either a scalar (i.e. single) value or, if defined as a table function, a
set of rows. For example, here is a basic example of a scalar UDF that calculates the area of a circle:

Copy code

```
CREATE FUNCTION area_of_circle(radius FLOAT)
  RETURNS FLOAT
  AS
  $$
    pi() * radius * radius
  $$
  ;
```

Copy code

```
SELECT area_of_circle(1.0);
```

Output:

Copy code

```
SELECT area_of_circle(1.0);
+---------------------+
| AREA_OF_CIRCLE(1.0) |
|---------------------|
|         3.141592654 |
+---------------------+
```

The expression can be a query expression (a [SELECT](/sql-reference/sql/select) expression). For example:

Copy code

```
CREATE FUNCTION profit()
  RETURNS NUMERIC(11, 2)
  AS
  $$
    SELECT SUM((retail_price - wholesale_price) * number_sold)
        FROM purchases
  $$
  ;
```

When using a query expression in a SQL UDF, do not include a semicolon within the UDF body to terminate the query expression.

You can include only one query expression. The expression can include
UNION [ALL].

Note

Although the body of a UDF can contain a complete SELECT statement, it cannot contain DDL statements or any DML statement other
than SELECT.

Note

Scalar functions (UDFs) have a limit of 500 input arguments.

## Memoizable UDFs

A scalar SQL UDF can be memoizable. A memoizable function caches the result of calling a scalar SQL UDF and then returns the
cached result when the output is needed at a later time. The benefit of using a memoizable function is to improve performance for complex
queries, such as multiple column lookups in [mapping tables](https://en.wikipedia.org/wiki/Associative_entity) referenced within a row
access policy or masking policy.

Policy owners (e.g. the role with the OWNERSHIP privilege on the row access policy) can update their policy conditions to replace
subqueries that have mapping tables with a memoizable function. When users reference the policy-protected column in a query later, the
cached results from the memoizable function are available to use as needed.

Note

The [USE\_CACHED\_RESULT](/sql-reference/parameters#label-use-cached-result) session parameter must be set to TRUE to use memoizable functions.

### Create a memoizable function

You can define a scalar SQL UDF to be memoizable in the [CREATE FUNCTION](/sql-reference/sql/create-function) statement by specifying the
`MEMOIZABLE` keyword. You can create a memoizable function with or without arguments. By using arguments, you have more freedom to
define the SQL UDF. When you write a policy to call the memoizable function, you have more freedom in terms of how to define the policy.

If you specify arguments, the arguments must be constant values with one of the following data types:

- VARCHAR and other string data types.
- NUMBER and other numeric data types.
- TIMESTAMP and other date data types.
- BOOLEAN.

Nonconstant values and their data types, such as [semi-structured data types](/user-guide/semistructured-data-formats) and table
columns are not supported.

When you write a memoizable function:

- Specify BOOLEAN or other scalar data types as the `result_data_type`.

  Exercise caution when specifying ARRAY as the `result_data_type` because there are limits to cache size.
- Do not specify other data types such as OBJECT and VARIANT.
- Do not reference another memoizable function in any way.

### Call a memoizable function

A memoizable function can be called in a SELECT statement or be included in a policy definition, which then calls the memoizable function
based on the policy conditions.

When calling a memoizable function, note:

- For SQL UDFs that return the ARRAY data type or specify a non-scalar value, use the memoizable function as an argument in the
  [ARRAY\_CONTAINS](/sql-reference/functions/array_contains) function.
- Cache size limit:

  Each memoizable function has a 10 KB limit for the current Snowflake session.

  If the memoizable function exceeds this limit for result set cache, Snowflake does not cache the result of calling the
  memoizable function. Instead, the UDF acts as a normal scalar UDF based on how the function is written.
- Cache usage:

  Memoizable functions have a reusable result cache for different SQL statements when the query environment and context do not
  change. Generally, this means the result cache applies to different SQL statements provided that:

  - The access control authorization on objects and columns referenced in a query remain the same.
  - The objects referenced in the query are not modified (e.g. through DML statements).

  The CHILD\_QUERIES\_WAIT\_TIME column in the Account Usage [QUERY\_HISTORY](/sql-reference/account-usage/query_history) view records
  the time (in milliseconds) to complete the cached lookup when calling a memoizable function.
- Memoizable functions do not reuse cached results when:

  - The function references a table or other object and there is an update to the referenced table.
  - There is a change in access control to the table.
  - The function calls nondeterministic function.
  - The function calls an external function or a UDF that is not a SQL UDF.

## Examples

### Basic SQL scalar UDF example(s)

This example returns a hard-coded approximation of the mathematical constant pi.

Copy code

```
CREATE FUNCTION pi_udf()
  RETURNS FLOAT
  AS '3.141592654::FLOAT'
  ;
```

Copy code

```
SELECT pi_udf();
```

Output:

Copy code

```
SELECT pi_udf();
+-------------+
|    PI_UDF() |
|-------------|
| 3.141592654 |
+-------------+
```

### Common SQL examples

#### Query expression with [SELECT](/sql-reference/sql/select) statement

Create the table and data to use:

Copy code

```
CREATE TABLE purchases (number_sold INTEGER, wholesale_price NUMBER(7,2), retail_price NUMBER(7,2));
INSERT INTO purchases (number_sold, wholesale_price, retail_price) VALUES 
   (3,  10.00,  20.00),
   (5, 100.00, 200.00)
   ;
```

Create the UDF:

Copy code

```
CREATE FUNCTION profit()
  RETURNS NUMERIC(11, 2)
  AS
  $$
    SELECT SUM((retail_price - wholesale_price) * number_sold)
        FROM purchases
  $$
  ;
```

Call the UDF in a query:

Copy code

```
SELECT profit();
```

Output:

Copy code

```
SELECT profit();
+----------+
| PROFIT() |
|----------|
|   530.00 |
+----------+
```

#### UDF in a WITH clause

Copy code

```
CREATE TABLE circles (diameter FLOAT);

INSERT INTO circles (diameter) VALUES
    (2.0),
    (4.0);

CREATE FUNCTION diameter_to_radius(f FLOAT) 
  RETURNS FLOAT
  AS 
  $$ f / 2 $$
  ;
```

Copy code

```
WITH
    radii AS (SELECT diameter_to_radius(diameter) AS radius FROM circles)
  SELECT radius FROM radii
    ORDER BY radius
  ;
```

Output:

Copy code

```
+--------+
| RADIUS |
|--------|
|      1 |
|      2 |
+--------+
```

#### JOIN operation

This example uses a more complex query, which includes a JOIN operation:

Create the table and data to use:

Copy code

```
CREATE TABLE orders (product_ID varchar, quantity integer, price numeric(11, 2), buyer_info varchar);
CREATE TABLE inventory (product_ID varchar, quantity integer, price numeric(11, 2), vendor_info varchar);
INSERT INTO inventory (product_ID, quantity, price, vendor_info) VALUES 
  ('X24 Bicycle', 4, 1000.00, 'HelloVelo'),
  ('GreenStar Helmet', 8, 50.00, 'MellowVelo'),
  ('SoundFX', 5, 20.00, 'Annoying FX Corporation');
INSERT INTO orders (product_id, quantity, price, buyer_info) VALUES 
  ('X24 Bicycle', 1, 1500.00, 'Jennifer Juniper'),
  ('GreenStar Helmet', 1, 75.00, 'Donovan Liege'),
  ('GreenStar Helmet', 1, 75.00, 'Montgomery Python');
```

Create the UDF:

Copy code

```
CREATE FUNCTION store_profit()
  RETURNS NUMERIC(11, 2)
  AS
  $$
  SELECT SUM( (o.price - i.price) * o.quantity) 
    FROM orders AS o, inventory AS i 
    WHERE o.product_id = i.product_id
  $$
  ;
```

Call the UDF in a query:

Copy code

```
SELECT store_profit();
```

Output:

Copy code

```
SELECT store_profit();
+----------------+
| STORE_PROFIT() |
|----------------|
|         550.00 |
+----------------+
```

The topic [CREATE FUNCTION](/sql-reference/sql/create-function) contains additional examples.

### Using UDFs in different clauses

A scalar UDF can be used any place a scalar expression can be used. For example:

Copy code

```
-- ----- These examples show a UDF called from different clauses ----- --

select MyFunc(column1) from table1;

select * from table1 where column2 > MyFunc(column1);
```

### Using SQL variables in a UDF

This example shows how to set a SQL variable and use that variable inside a UDF:

Copy code

```
SET id_threshold = (SELECT COUNT(*)/2 FROM table1);
```

Copy code

```
CREATE OR REPLACE FUNCTION my_filter_function()
RETURNS TABLE (id int)
AS
$$
SELECT id FROM table1 WHERE id > $id_threshold
$$
;
```

### Memoizable functions

For examples, see:

- Memoizable function without arguments in a [row access policy](/user-guide/security-row-using#label-security-row-using-example-memoizable-function).
- Memoizable function with arguments in a [masking policy](/user-guide/security-column-ddm-use#label-security-column-memoizable-function).
