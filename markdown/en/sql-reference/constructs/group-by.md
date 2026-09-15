Categories:
:   [Query syntax](/sql-reference/constructs)

# GROUP BY

Groups rows with the same group-by-item expressions and computes aggregate functions for the resulting group. A GROUP BY
expression can be:

- A column name.
- A number referencing a position in the [SELECT](/sql-reference/sql/select) list.
- A general expression.

## GROUP BY extensions

GROUP BY supports the following extensions that provide powerful aggregation capabilities:

- [GROUP BY GROUPING SETS](/sql-reference/constructs/group-by-grouping-sets): Compute multiple GROUP BY clauses in a single statement
- [GROUP BY ROLLUP](/sql-reference/constructs/group-by-rollup): Produce subtotal rows for hierarchical data
- [GROUP BY CUBE](/sql-reference/constructs/group-by-cube) : Produce subtotal rows for all combinations of dimensions

You can combine these extensions with regular GROUP BY columns. For example:

- `GROUP BY x, GROUPING SETS(y, z)`
- `GROUP BY x, ROLLUP(y, z)`
- `GROUP BY x, CUBE(y, z)`

For more information about interpreting NULL values in extension results, see the
[GROUPING](/sql-reference/functions/grouping) utility function.

## Syntax

Copy code

```
SELECT ...
  FROM ...
  [ ... ]
  GROUP BY groupItem [ , groupItem [ , ... ] ]
  [ ... ]
```

Copy code

```
SELECT ...
  FROM ...
  [ ... ]
  GROUP BY ALL
  [ ... ]
```

Where:

> Copy code
>
> ```
> groupItem ::= { <column_alias> | <position> | <expr> }
> ```

## Parameters

`column_alias`
:   Column alias appearing in the query block’s [SELECT](/sql-reference/sql/select) list.

`position`
:   Position of an expression in the [SELECT](/sql-reference/sql/select) list.

`expr`
:   Any expression on tables in the current scope.

`GROUP BY ALL`
:   Specifies that all items in the SELECT list that do not use aggregate functions should be used for grouping.

    For examples, refer to [Group by all columns](#label-group-by-all-columns).

## Usage notes

- A GROUP BY clause can reference expressions in the projection clause by name or by position.
  If the GROUP BY clause references by name, each reference is resolved as follows:

  - If the query contains a database object (for example, a table or view) with a matching column name, the reference is resolved to the
    column name.
  - Otherwise, if the projection clause of the SELECT contains an expression alias with a matching name, the reference is
    resolved to the alias.

  For an example, see [Precedence when a column name and an alias match](/sql-reference/constructs/group-by#label-group-by-precedence-when-shadowing).
- If all SELECT items use aggregate functions, specifying GROUP BY ALL is equivalent to specifying the statement without the
  GROUP BY clause.

  For example, the following statement only has SELECT items that use aggregate functions:

  Copy code

  ```
  SELECT SUM(amount)
    FROM mytable
    GROUP BY ALL;
  ```

  The statement above is equivalent to not specifying the GROUP by clause:

  Copy code

  ```
  SELECT SUM(amount)
    FROM mytable;
  ```

## Examples

The following sections provide examples of using the GROUP BY clause:

- [Group by one column](#label-group-by-one-column)
- [Group by multiple columns](#label-group-by-multiple-columns)
- [Group by all columns](#label-group-by-all-columns)
- [Precedence when a column name and an alias match](/sql-reference/constructs/group-by#label-group-by-precedence-when-shadowing)

Note that the examples in each section use the data that you set up in [Setting up the data for the examples](#label-group-by-sample-data-setup).

### Setting up the data for the examples

The examples in this section use a table named `sales` and a table named `product`. To create these tables and insert the
data needed for the example, run the following commands:

Copy code

```
CREATE TABLE sales (
  product_ID INTEGER,
  retail_price REAL,
  quantity INTEGER,
  city VARCHAR,
  state VARCHAR);

INSERT INTO sales (product_id, retail_price, quantity, city, state) VALUES
  (1, 2.00,  1, 'SF', 'CA'),
  (1, 2.00,  2, 'SJ', 'CA'),
  (2, 5.00,  4, 'SF', 'CA'),
  (2, 5.00,  8, 'SJ', 'CA'),
  (2, 5.00, 16, 'Miami', 'FL'),
  (2, 5.00, 32, 'Orlando', 'FL'),
  (2, 5.00, 64, 'SJ', 'PR');

CREATE TABLE products (
  product_ID INTEGER,
  wholesale_price REAL);
INSERT INTO products (product_ID, wholesale_price) VALUES (1, 1.00);
INSERT INTO products (product_ID, wholesale_price) VALUES (2, 2.00);
```

### Group by one column

This example shows the gross revenue per product, grouped by `product_id` (that is, the total amount of money received for
each product):

Copy code

```
SELECT product_ID, SUM(retail_price * quantity) AS gross_revenue
  FROM sales
  GROUP BY product_ID;
```

```
+------------+---------------+
| PRODUCT_ID | GROSS_REVENUE |
+------------+---------------+
|          1 |          6    |
|          2 |        620    |
+------------+---------------+
```

The following example builds on the previous example, showing the net profit per product, grouped by `product_id`:

Copy code

```
SELECT p.product_ID, SUM((s.retail_price - p.wholesale_price) * s.quantity) AS profit
  FROM products AS p, sales AS s
  WHERE s.product_ID = p.product_ID
  GROUP BY p.product_ID;
```

```
+------------+--------+
| PRODUCT_ID | PROFIT |
+------------+--------+
|          1 |      3 |
|          2 |    372 |
+------------+--------+
```

### Group by multiple columns

The following example demonstrates how to group by multiple columns:

Copy code

```
SELECT state, city, SUM(retail_price * quantity) AS gross_revenue
  FROM sales
  GROUP BY state, city;
```

```
+-------+---------+---------------+
| STATE |   CITY  | GROSS REVENUE |
+-------+---------+---------------+
|   CA  | SF      |            22 |
|   CA  | SJ      |            44 |
|   FL  | Miami   |            80 |
|   FL  | Orlando |           160 |
|   PR  | SJ      |           320 |
+-------+---------+---------------+
```

### Group by all columns

The following example is equivalent to the example used in [Group by multiple columns](#label-group-by-multiple-columns).

Copy code

```
SELECT state, city, SUM(retail_price * quantity) AS gross_revenue
  FROM sales
  GROUP BY ALL;
```

```
+-------+---------+---------------+
| STATE |   CITY  | GROSS REVENUE |
+-------+---------+---------------+
|   CA  | SF      |            22 |
|   CA  | SJ      |            44 |
|   FL  | Miami   |            80 |
|   FL  | Orlando |           160 |
|   PR  | SJ      |           320 |
+-------+---------+---------------+
```

# Precedence when a column name and an alias match

It is possible (but usually not recommended) to create a query that contains an alias that matches a column name:

Copy code

```
SELECT x, some_expression AS x
  FROM ...
```

If a clause contains a name that matches both a column name and an alias, then the clause uses the column name. The following example demonstrates this behavior using a GROUP BY clause:

Create a table and insert rows:

Copy code

```
CREATE TABLE employees (salary FLOAT, state VARCHAR, employment_state VARCHAR);
INSERT INTO employees (salary, state, employment_state) VALUES
  (60000, 'California', 'Active'),
  (70000, 'California', 'On leave'),
  (80000, 'Oregon', 'Active');
```

The following query returns the sum of the salaries of the employees who are active and the sum of the salaries of the employees who
are on leave:

Copy code

```
SELECT SUM(salary), ANY_VALUE(employment_state)
  FROM employees
  GROUP BY employment_state;
```

```
+-------------+-----------------------------+
| SUM(SALARY) | ANY_VALUE(EMPLOYMENT_STATE) |
|-------------+-----------------------------|
|      140000 | Active                      |
|       70000 | On leave                    |
+-------------+-----------------------------+
```

The next query uses the alias `state`, which matches the name of a column of the table in the query. When `state` is used in
the GROUP BY clause, Snowflake interprets it as a reference to the column name, not the alias. This query therefore returns the sum of
the salaries of the employees in the state of California and the sum of the salaries of the employees in the state of Oregon,
yet displays `employment_state` information, such as `Active`, rather than the names of states or provinces:

Copy code

```
SELECT SUM(salary), ANY_VALUE(employment_state) AS state
  FROM employees
  GROUP BY state;
```

```
+-------------+--------+
| SUM(SALARY) | STATE  |
|-------------+--------|
|      130000 | Active |
|       80000 | Active |
+-------------+--------+
```
