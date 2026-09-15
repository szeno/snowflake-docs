# Speeding up join queries with search optimization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The search optimization service can improve the performance of join queries that have a small number of distinct values on the
build side of the join.

For example, the search optimization service can improve the performance of these types of joins:

- Suppose that `products` is a table containing a row for each product, and `sales` is a table containing a row for
  each sale of a product. The `products` table contains fewer rows and is smaller than the `sales` table. To find all sales of
  a specific product, you join the `sales` table (the larger table) with the `products` table (the smaller table). Because
  the `products` table is small, there are few distinct values on the build side of the join.

  Note

  In data warehousing, the large table is often referred to as the [fact table](https://en.wikipedia.org/wiki/Fact_table). The small table is referred to as the
  [dimension table](https://en.wikipedia.org/wiki/Dimension_%28data_warehouse%29#Dimension_table). The rest of this topic uses these terms when referring to the large table and the small table in a join.
- Suppose that `customers` is a table containing a row for each customer, and `sales` is a table containing a row for
  each sale. Both tables are large. To find all sales for a specific customer, you join the `sales` table (the probe side)
  with the `customers` table (the build side) and use a filter so that there are a small number of distinct values on the
  build side of the join.

The following sections provide more information about search optimization support for join queries:

- [Enabling search optimization for join queries](#label-search-optimization-service-join-support-setup)
- [Supported join predicates](#label-search-optimization-service-join-support-predicates)
- [Examples of supported join queries](#label-search-optimization-service-join-support-examples)
- [Limitations](#label-search-optimization-service-join-support-limitations)

## Enabling search optimization for join queries

To improve the performance of join queries, make sure search optimization is enabled for columns in the join
predicate of the query. In addition, make sure the build side of the join has a small number of distinct values, either
because it’s a small dimension table or because of a selective filter. The search optimization runtime costs of a query
are proportionate to the number of distinct values that must be looked up on the build side of the join. If this number
is too large, Snowflake might decide against using the search access path and use the regular table access path instead.

To improve the performance of join queries, [enable search optimization](/user-guide/search-optimization/enabling)
for the table on the probe side of the join. This table is usually a large table that isn’t filtered in join queries,
such as a fact table.

Use the [ALTER TABLE … ADD SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add)
command to:

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

## Supported join predicates

The search optimization service can improve the performance of queries with the following types of join predicates:

- Equality predicates of the form `probe_side_table.column = build_side_table.column`.
- Transformations on the build-side operand of the predicate (for example, string concatenation, addition, and so on).
- Conjunctions (`AND`) of multiple equality predicates.

## Examples of supported join queries

This section shows examples of join queries that can benefit from search optimization.

### Example: Simple equality predicate

The following is an example of a supported query that uses a simple equality predicate as the join predicate. This query joins a
table named `sales` with a table named `customers`. The probe-side table `sales` is large and has search optimization
enabled. The build-side table `customers` is also large, but the input from this table is small, due to the selective filter on the
`customer_id` column.

Copy code

```
SELECT sales.date, customer.name
  FROM sales JOIN customers ON (sales.customer_id = customers.customer_id)
  WHERE customers.customer_id = 2094;
```

### Example: Predicate transformed on the dimension-side operand

The following query joins a fact table named `sales` with a dimension table named `products`. The fact table is large and
has search optimization enabled. The dimension table is small.

This query transforms the dimension-side operand of the predicate (for example, by multiplying values in the join condition)
and can benefit from search optimization:

Copy code

```
SELECT sales.date, product.name
  FROM sales JOIN products ON (sales.product_id = product.old_id * 100)
  WHERE product.category = 'Cutlery';
```

### Example: Predicate spanning multiple columns

Queries in which a join predicate spans multiple columns can benefit from search optimization:

Copy code

```
SELECT sales.date, product.name
  FROM sales JOIN products ON (sales.product_id = product.id and sales.location = product.place_of_production)
  WHERE product.category = 'Cutlery';
```

### Example: Query using point-lookup filters and join predicates

In a query that uses both regular point-lookup filters and join predicates, the search optimization service can improve the
performance of both. In the following query, the search optimization service can improve the `sales.location` point-lookup
predicate as well as the `product_id` join predicate:

Copy code

```
SELECT sales.date, product.name
  FROM sales JOIN products ON (sales.product_id = product.id)
  WHERE product.category = 'Cutlery'
  AND sales.location = 'Buenos Aires';
```

## Limitations

The following limitations apply to the search optimization service and join queries:

- Disjuncts (`OR`) in join predicates currently aren’t supported.
- LIKE, ILIKE, and RLIKE join predicates currently aren’t supported.
- Join predicates on VARIANT columns currently aren’t supported.
- [[ NOT ] EQUAL\_NULL](/sql-reference/functions/equal_null) equality predicates currently aren’t supported.
- The [current limitations of the search optimization service](/user-guide/search-optimization/queries-that-benefit#label-search-optimization-limitations) also apply to
  join queries.
