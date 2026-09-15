# How Snowflake validates semantic views

Snowflake verifies that a semantic view complies with a set of validation rules when you define it. These rules ensure your
semantic model is well-formed and will function correctly.

These rules are explained in the next sections:

- [General validation rules](#label-semantic-views-validation-general)
- [Validation rules for relationships](#label-semantic-views-validation-relationship)
- [Expression validation rules](#label-semantic-views-validation-expression)
  - [General rules about expressions](#label-semantic-views-validation-expression-general)
  - [Rules for row-level expressions (dimensions and facts)](#label-semantic-views-validation-expression-row-level)
  - [Rules for aggregate-level expressions (metrics)](#label-semantic-views-validation-expression-aggregate)
  - [Rules for window function metrics](#label-semantic-views-validation-expression-window)

## General validation rules

The following rules apply to semantic views in general:

- **Required elements:** A semantic view must define at least one dimension or metric.

  For example, your TPC-H semantic view needs at least one dimension (like `customer_name`) or a metric (like
  `order_average_value`).
- **Primary and foreign keys:** In the primary and foreign key definitions, you must use physical base table columns or
  expressions defined in logical tables that directly refer to a base table column (for example, `t1.fact AS t1.col`).

  For example, in the TPC-H schema, you can use `c_custkey` as the primary key for the `customer` table and `o_custkey` as
  the foreign key in the `orders` table. `c_custkey` and `o_custkey` are columns in the physical base tables.
- **Table alias references:** When referring to tables in relationships or expressions, you must use their defined aliases.

  For example, if you define the table alias `orders AS snowflake_sample_data.tpch.orders_table`, you must use the table
  alias `orders` (not `orders_table`) in the definitions of your metrics.

  If you don’t specify an alias for a logical table, you must use the logical table name in any expressions.

## Validation rules for relationships

The following rules apply to relationships in semantic views:

- **Many-to-one relationships and one-to-one relationships:** Relationships work like foreign key constraints.

  Suppose that the logical table `table_1` identifies `col_1` as a primary key:

  Copy code

  ```
  TABLES (
    table_1 AS my_table_1 PRIMARY KEY (col_1)
    ...
  ```

  When you define a relationship as `table_2 (col_2) REFERENCES table_1 (col_1)`, `col_1` must be a primary key, and
  `col_2` must serve as a foreign key:

  - If multiple rows in `table_2` use the same value in `col_2`, you’re creating a many-to-one relationship from `table_2`
    to `table_1`.

    For example, `orders (o_custkey) REFERENCES customers (c_custkey)` creates a many-to-one relationship from `orders`
    to `customers` (many orders can belong to one customer with the key `c_custkey`).
  - If each row in `table_2` has a unique value in `col_2`, you’re creating a one-to-one relationship from `table_2` to
    `table_1`.

    For example, `customer_details_extended (e_custkey) REFERENCES customer_details (c_custkey)` creates a one-to-one
    relationship from `customer_details_extended` to `customer_details` (one row of extended details for a customer belongs
    to one row of customer details with the key `c_custkey`).
- **Validations performed on one-to-one relationships:**

  - [Row-level expressions](#label-semantic-views-validation-expression-row-level) can refer to other row-level expressions
    at the same (or lower) granularity.

    For example, `customer_details` and `customer_details_extended` have a one-to-one relationship, where one row in
    `customer_details` is related to one row in `customer_details_extended`. A row-level expression on each of these tables
    refers to one specific customer. Each can refer directly to the other in row-level expressions because the row-level
    expressions are at the same granularity.

    As a corollary, a row-level expression on `customer_details` cannot reference a metric or aggregation of a
    row-level expression on `customer_details_extended` (and vice versa).
  - [Aggregate-level expressions](#label-semantic-views-validation-expression-aggregate) must refer to row-level expressions
    at the same granularity using a single aggregate.

    For example, aggregate-level expressions on `customer_details` or `customer_details_extended` must use a single aggregate
    when referencing the other entity. In addition, metrics on `customer_details` and `customer_details_extended` should
    refer to other metrics on the two entities directly, without any aggregation.

  These rules apply whether the relationship between the entities is defined as
  `customer_details REFERENCES customer_details_extended` or
  `customer_details_extended REFERENCES customer_details`.
- **Transitive relationships:** Snowflake automatically derives indirect relationships.

  For example, if you define a relationship between `line_items` and `orders` and another relationship between `orders` and
  `customer`, Snowflake understands there’s also a relationship between `line_items` and `customer`.

  Note that one-to-one relationships respect transitivity when interacting with other one-to-one and many-to-one relationships:

  - If logical tables `customers` and `customer_details` have a one-to-one relationship and logical tables
    `customer_details` and `customer_details_extended` have a one-to-one relationship, logical tables `customers` and
    `customer_details_extended` are automatically inferred to have a one-to-one relationship and are treated as such during
    validation.
  - If logical tables `customers` and `customer_details` have a one-to-one relationship and logical tables
    `customer_details` and `regions` have a many-to-one relationship, `customers` is inferred to be transitively
    many-to-one to `regions`, which gives `customers` a higher granularity than `regions` during expression validation.
- **No circular relationships:** You cannot define circular relationships, even through transitive paths.

  For example, you cannot define a relationship from `orders` to `customer` and another relationship from `customer` to
  `orders`.
- **No self-references:** Currently, a table cannot reference itself (like an employee manager hierarchy where employees can
  reference other employees as their manager).
- **Multi-path relationship restrictions:** You can define multiple relationships between two tables, but there are limitations.

  For example, if `line_items` is related to `orders` through both `order_key` and another column, those tables cannot
  refer to each other’s semantic expressions.

  Note

  If there are multiple paths that can be used to join two tables, you should define these relationships and specify which path
  to use when defining a metric. For information, see [Specifying the relationship for a metric when multiple relationship paths exist](/user-guide/views-semantic/sql#label-semantic-views-create-logical-tables-relations).

## Expression validation rules

The following rules apply to semantic expressions in facts, dimensions, and metrics:

- [General rules about expressions](#label-semantic-views-validation-expression-general)
- [Rules for row-level expressions (dimensions and facts)](#label-semantic-views-validation-expression-row-level)
- [Rules for aggregate-level expressions (metrics)](#label-semantic-views-validation-expression-aggregate)

### General rules about expressions

The following rules apply to semantic expressions in general:

- **Expression types:** Dimensions and facts are row-level expressions (unaggregated), while metrics are aggregate-level
  expressions.

  For example, `customer_name` is a dimension (row-level), while `order_average_value` is a metric (aggregate-level).
- **Table association:** Every semantic expression must be associated with a table.

  For example, `customer_name` must be defined as `customer.customer_name` and `order_average_value` as
  `orders.order_average_value`.
- **Same-table references:** Expressions can refer to base table columns or other expressions on the same logical table using
  either qualified or unqualified names.

  For example, in the `orders` table, you could define `orders.shipping_month` as

  - `MONTH(o_shipdate)` (using the unqualified column name)
  - `MONTH(orders.o_shipdate)` (using the qualified name)
- **Cross-table limitations:** Expressions cannot refer to base table columns from other tables or expressions from unrelated
  logical tables.

  For example, `customer.customer_name` cannot directly reference an expression from the `orders` table unless there’s a
  relationship between them. To work with data across tables, you must:

  1. Define relationships between logical tables (for example, between `customer` and `orders` through `c_custkey`).
  2. Define a fact on the source table (for example, `orders.total_value`).
  3. Refer to these expressions from a connected logical table (for example, `customer.order_value` can refer to
     `orders.total_value`).
- **Name resolution:** If both a semantic expression and a column have the same name, references to that name resolve to the
  semantic expression.

  For example, if you define a `region` dimension and there’s also a `region` column, `region` in expressions resolves to
  the dimension, not the column. An exception is when an expression refers to the same name in its definition (for example,
  `customer.c_name AS customers.c_name`). The reference resolves to the column, rather than to the defining expression itself.
- **Expression reference cycles:** You cannot create circular references between expressions.

  For example, you cannot define `customer.total_value` based on `orders.customer_value` and then define
  `orders.customer_value` based on `customer.total_value`.
- **Table reference cycles:** You cannot create circular references between logical tables in expression definitions.

  For example, you cannot define `customer.total_value` based on `orders.customer_value` and then define
  `orders.customer_count` based on `customer.c_custkey`.
- **Function usage:** You can use scalar functions like [YEAR\* / DAY\* / WEEK\* / MONTH / QUARTER](/sql-reference/functions/year) in dimensions, but table functions
  are not allowed.

### Rules for row-level expressions (dimensions and facts)

The following rules apply to row-level expressions in dimensions and facts:

- **Same-table references:** A row-level expression can directly refer to columns from its own table.

  For example, `customers.customer_name` can be defined as `customers.c_name` directly.
- **Equal or lower granularity:** A row-level expression can directly refer to other row-level expressions at the same or
  lower granularity.

  For example, `orders.order_details` can refer to `customer.customer_name` because `customer` is at a lower granularity
  than `orders` (one customer can have many orders).
- **Higher granularity references:** When referencing row-level expressions at higher granularity, a row-level expression must
  use aggregation.

  For example, `customer.total_orders` must use `COUNT(orders.o_orderkey)` because `orders` is at a higher granularity
  than `customer` (one customer can have many orders).
- **Aggregate references:** A dimension like `orders.order_type` cannot refer to a metric like `orders.order_average_value`,
  but `customer.customer_segment` can refer to `orders.order_average_value` because `customer` is at a lower granularity
  than orders.

### Rules for aggregate-level expressions (metrics)

The following rules apply to aggregate-level expressions in metrics:

- **Basic aggregation:** A metric that is not a derived metric must use an aggregate function.

  For example, `orders.order_average_value` must use `AVG(orders.o_totalprice)`.
- **Equal or lower granularity:** When referring to row-level expressions at equal or lower granularity, a metric must use a
  single aggregate.

  For example, `orders.total_value` can use `SUM(line_items.discounted_price)` because `line_items` is at lower
  granularity than orders.
- **Higher granularity references:** When referring to row-level expressions at higher granularity, a metric must use nested
  aggregation.

  For example, `customer.average_order_value` must use `AVG(SUM(orders.o_totalprice))` because `orders` is at higher
  granularity than `customer`.
- **Other aggregate references:** A metric can directly refer to other metrics at equal or lower granularity without aggregation.

  For example, `orders.profit_margin` can be defined as `orders.total_revenue / orders.total_cost` without additional
  aggregation. However, when referring to metrics at higher granularity, an aggregation is required.

### Rules for window function metrics

These rules apply to [window function metrics](/user-guide/views-semantic/querying#label-semantic-views-querying-window):

- Window function metrics cannot be used by row-level calculations (facts and dimensions).
- Window function metrics cannot be used in the definitions of other metrics.
