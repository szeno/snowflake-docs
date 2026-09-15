# Speeding up queries with scalar subqueries using search optimization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

A scalar subquery returns a single value (one column of one row). If no rows qualify to be returned, the subquery
returns NULL. The search optimization service can improve the performance of queries with scalar subqueries. For
more information about subqueries, see [Working with Subqueries](/user-guide/querying-subqueries).

The following sections provide more information about search optimization support for queries with subqueries:

- [Enabling search optimization for queries with scalar subqueries](#label-search-optimization-service-scalar-subqueries-support-setup)
- [Supported data types](#label-search-optimization-service-scalar-subqueries-data-types)
- [Examples of supported queries with scalar subqueries](#label-search-optimization-service-scalar-subqueries-examples)

## Enabling search optimization for queries with scalar subqueries

Queries with subqueries aren’t improved unless you enable search optimization for the column that is
equal to the result of the subquery. To improve the performance of queries with scalar subqueries on a table, use the
[ALTER TABLE … ADD SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add) command to
do either of the following:

- Enable search optimization for specific columns.
- Enable search optimization for all columns of the table.

In general, enabling search optimization only for specific columns is the best practice. Use the ON EQUALITY clause
to specify the columns. This example enables search optimization for a specific column:

Copy code

```
ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON EQUALITY(mycol);
```

To specify EQUALITY for all columns of the supported data types (except for
[semi-structured](/sql-reference/data-types-semistructured) and [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography)):

Copy code

```
ALTER TABLE mytable ADD SEARCH OPTIMIZATION;
```

For more information, see [Enabling and disabling search optimization](/user-guide/search-optimization/enabling).

## Supported data types

The search optimization service can improve the performance of scalar subqueries on columns of the following
data types:

- [Data types for fixed-point numbers](/sql-reference/data-types-numeric#label-data-types-for-fixed-point-numbers), including the following:

  - All INTEGER data types, which have a scale of 0.
  - Fixed-point non-integers, which have a scale other than 0 (such as `NUMBER(10,2)`).
  - [Casts](/sql-reference/data-type-conversion) of fixed-point numbers (for example,
    `NUMBER(30, 2)::NUMBER(30, 5)`).
- [String & binary data types](/sql-reference/data-types-text) (for example, VARCHAR and BINARY).
- [Date & time data types](/sql-reference/data-types-datetime) (for example, DATE, TIME, and TIMESTAMP).

Subqueries that involve other types of values (for example, VARIANT, FLOAT, GEOGRAPHY, or GEOMETRY) don’t benefit.

## Examples of supported queries with scalar subqueries

The following queries are examples of queries with scalar subqueries that are supported by the search
optimization service.

This query has a scalar subquery that queries the same table as the table in the outer query. To improve performance,
make sure search optimization is enabled for the `salary` column in the `employees` table.

Copy code

```
SELECT employee_id
  FROM employees
  WHERE salary = (
    SELECT MAX(salary)
      FROM employees
      WHERE department = 'Engineering');
```

This query has a scalar subquery that queries a table that is different from the table in the outer query. To improve
performance, make sure search optimization is enabled for the `product_id` column in the `products` table.

Copy code

```
SELECT *
  FROM products
  WHERE products.product_id = (
    SELECT product_id
      FROM sales
      GROUP BY product_id
      ORDER BY COUNT(product_id) DESC
      LIMIT 1);
```
