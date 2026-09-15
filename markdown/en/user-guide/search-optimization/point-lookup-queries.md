# Speeding up point lookup queries with search optimization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Point lookup queries are queries that are expected to return a small number of rows. The search optimization service can
improve the performance of point lookup queries that use:

- Equality predicates (for example, `column_name = constant`).
- Predicates that use [IN](/sql-reference/functions/in) (see [example](#label-search-optimization-example-in-clause)).

The following sections provide more information about search optimization support for point lookup queries:

- [Enabling search optimization for point lookup queries](#label-search-optimization-service-point-lookup-support-setup)
- [Examples of supported point lookup queries](#label-search-optimization-example-in-clause)

## Enabling search optimization for point lookup queries

Point lookup queries aren’t improved unless you enable search optimization for the columns referenced by the predicate of
the query. To improve the performance of point lookup queries on a table, use the
[ALTER TABLE … ADD SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add) command to:

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

## Examples of supported point lookup queries

The search optimization service can improve the performance of the following query that uses an equality predicate:

Copy code

```
SELECT * FROM test_table WHERE id = 3;
```

The [IN](/sql-reference/functions/in) clause is supported by the search optimization service:

Copy code

```
SELECT id, c1, c2, c3
  FROM test_table
  WHERE id IN (2, 3)
  ORDER BY id;
```
