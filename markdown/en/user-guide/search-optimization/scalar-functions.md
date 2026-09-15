# Speeding up queries with scalar functions using search optimization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

A scalar function returns a single value for each invocation. The search optimization service can improve the
performance of queries that use scalar functions in equality predicates. The scalar function can be a
[system-defined scalar function](/sql-reference/functions) or a
[user-defined scalar SQL function](/developer-guide/udf/sql/udf-sql-introduction).

The following sections provide more information about search optimization support for queries that use scalar
functions:

- [Enabling search optimization for queries that use scalar functions](#label-search-optimization-service-scalar-functions-support-setup)
- [Supported data types](#label-search-optimization-service-scalar-functions-data-types)
- [Examples of supported queries with scalar functions](#label-search-optimization-service-scalar-functions-examples)

## Enabling search optimization for queries that use scalar functions

Queries aren’t improved unless you enable search optimization for the columns that are specified in equality
predicates that use scalar function calls. To improve the performance of queries with scalar functions on a table,
use the [ALTER TABLE … ADD SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add)
command to do the following:

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

The search optimization service can improve the performance of queries that use columns of the following
data types in equality predicates that use scalar function calls:

- [Data types for fixed-point numbers](/sql-reference/data-types-numeric#label-data-types-for-fixed-point-numbers), including the following:

  - All INTEGER data types, which have a scale of 0.
  - Fixed-point non-integers, which have a scale other than 0 (such as `NUMBER(10,2)`).
  - [Casts](/sql-reference/data-type-conversion) of fixed-point numbers (for example,
    `NUMBER(30, 2)::NUMBER(30, 5)`).
- [String & binary data types](/sql-reference/data-types-text) (for example, VARCHAR and BINARY).
- [Date & time data types](/sql-reference/data-types-datetime) (for example, DATE, TIME, and TIMESTAMP).

Queries that involve other types of values (for example, VARIANT, FLOAT, GEOGRAPHY, or GEOMETRY) don’t benefit.

## Examples of supported queries with scalar functions

The following queries use scalar functions and are supported by the search optimization service.

### Use a system-defined scalar function in the predicate of a query

This query uses the [SHA2](/sql-reference/functions/sha2) system-defined scalar function in an
equality predicate. To improve performance, make sure the EQUALITY search method
is enabled for the `mycol` column in the `test_so_scalar_function_system` table.

Copy code

```
SELECT *
  FROM test_so_scalar_function_system
  WHERE mycol = SHA2('Snowflake');
```

### Use a user-defined scalar SQL function in the predicate of a query

Create a user-defined scalar function:

Copy code

```
CREATE OR REPLACE FUNCTION test_scalar_udf(x INTEGER)
RETURNS INTEGER
AS
$$
  SELECT x + POW(2, 3)::INTEGER + 2
$$
;
```

This query uses the `test_scalar_udf` function in an equality predicate. To improve performance,
make sure the EQUALITY search method is enabled for the `mycol` column in the
`test_so_scalar_function_udf` table.

Copy code

```
SELECT *
  FROM test_so_scalar_function_udf
  WHERE mycol = test_scalar_udf(15750);
```
