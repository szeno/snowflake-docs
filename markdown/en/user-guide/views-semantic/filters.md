# Defining filters for logical tables in a semantic view

In a [semantic view](/user-guide/views-semantic/overview), you can define a filter for a logical table. A *filter* is a fact
or dimension that you can also use as a condition in the WHERE clause of a query. The fact or dimension must resolve to a BOOLEAN
value.

Cortex Analyst can use this filter when producing SQL queries.

## Defining a filter

Define a filter in the DIMENSIONS or FACTS clause of the [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) command. When you define a
filter, you specify LABELS = (FILTER) to indicate that the dimension or fact is also a filter:

Copy code

```
CREATE [ OR REPLACE ] SEMANTIC VIEW [ IF NOT EXISTS ] <name>
  ...
  FACTS (
    <table_alias>.<filter> LABELS = (FILTER) AS <sql_expr>
    [ , ... ]
  )
  DIMENSIONS (
    <table_alias>.<filter> LABELS = (FILTER) AS <sql_expr>
    [ , ... ]
  )
  ...
```

where `sql_expr` is a conditional expression for the filter.

For example, suppose that you want to create a semantic view for the following tables, which contain information about customers
and orders:

Copy code

```
CREATE OR REPLACE TABLE customers(
  customer_id NUMBER,
  name VARCHAR,
  loyalty_points NUMBER,
  status VARCHAR,
  region VARCHAR,
  is_active BOOLEAN,
  signup_date DATE
);

INSERT INTO customers VALUES
  (1, 'Alice', 150, 'ACTIVE', 'US', TRUE, '2023-01-15'),
  (2, 'Bob', 50, 'INACTIVE', 'EU', FALSE, '2022-06-20'),
  (3, 'Charlie', 200, 'ACTIVE', 'US', TRUE, '2023-03-10'),
  (4, 'Dave', 180, 'INACTIVE', 'US', FALSE, '2022-08-01');
```

Copy code

```
CREATE OR REPLACE TABLE orders(
  order_id NUMBER,
  customer_id NUMBER,
  order_date DATE,
  total_amount NUMBER,
  is_completed BOOLEAN,
  is_refunded BOOLEAN
);

INSERT INTO orders VALUES
  (101, 1, '2024-01-01', 100, TRUE, FALSE),
  (102, 1, '2024-02-15', 200, TRUE, FALSE),
  (103, 2, '2024-02-20', 50, FALSE, TRUE),
  (104, 3, '2024-03-01', 200, TRUE, FALSE),
  (105, 4, '2024-06-05', 1200, TRUE, FALSE);
```

Suppose that you want to set up the semantic view so that you can query the view and filter the results, based on the following
criteria:

- Orders that are completed
- High value orders (orders that amount to more than $100)
- Important customers that have 150 or more loyalty points and that have placed orders of more than $1000
- Customers that are active
- Customers in the United States

When you create the semantic view, you can define filters for these criteria:

Copy code

```
CREATE OR REPLACE SEMANTIC VIEW my_sv_orders
  TABLES (
    customers PRIMARY KEY (customer_id),
    orders PRIMARY KEY (order_id)
  )
  RELATIONSHIPS (
    orders(customer_id) REFERENCES customers
  )
  FACTS (
    orders.completed_only LABELS = (FILTER) AS orders.is_completed,
    orders.high_value_order LABELS = (FILTER) AS orders.total_amount > 100,
    customers.vip_customer LABELS = (FILTER) AS
      customers.loyalty_points >= 150 AND SUM(orders.order_amount) > 1000,
    orders.order_amount AS orders.total_amount
  )
  DIMENSIONS (
    customers.customer_name AS customers.name,
    customers.active_only LABELS = (FILTER) AS customers.status = 'ACTIVE',
    customers.region_us LABELS = (FILTER) AS customers.region IN ('US'),
    orders.order_date AS orders.order_date
  )
  METRICS (
    orders.total_revenue AS SUM(orders.total_amount),
    orders.order_count AS COUNT(*)
  );
```

In the example above, LABELS = (FILTER) indicates that the item is a fact or dimension that can also be used as a filter. The
example defines the following filters:

- Filters that are facts:

  - `orders.completed_only` is TRUE if an order has been completed.
  - `orders.high_value_order` is TRUE if the value is more than $100.
  - `customers.vip_customer` is TRUE if the customer has 150 or more loyalty points and has placed orders of more than $1000.
- Filters that are dimensions:

  - `customers.active_only` is TRUE if the customer is active.
  - `customers.region_us` is TRUE if the customer is in the United States.

## Specifying a filter in a query

When you query the semantic view, you can specify the name of the filter as a condition in the WHERE clause.

For example, to return rows for completed orders, specify the `orders.completed_only` filter in the WHERE clause. The following
example uses a [SEMANTIC\_VIEW](/user-guide/views-semantic/querying#label-semantic-views-querying-semantic-view-clause) clause:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
  my_sv_orders
  DIMENSIONS orders.order_date
  METRICS orders.total_revenue
  WHERE orders.completed_only
);
```

```
+------------+---------------+
| ORDER_DATE | TOTAL_REVENUE |
|------------+---------------|
| 2024-01-01 |           100 |
| 2024-03-01 |           200 |
| 2024-02-15 |           200 |
| 2024-06-05 |          1200 |
+------------+---------------+
```

The following example uses [standard clauses in a SELECT statement](/user-guide/views-semantic/querying#label-semantic-views-querying-standard-sql) to query the
view:

Copy code

```
SELECT
    order_date,
    AGG(total_revenue)
  FROM my_sv_orders
  WHERE completed_only
  GROUP BY order_date
  ORDER BY order_date;
```

```
+------------+--------------------+
| ORDER_DATE | AGG(TOTAL_REVENUE) |
|------------+--------------------|
| 2024-01-01 |                100 |
| 2024-02-15 |                200 |
| 2024-03-01 |                200 |
| 2024-06-05 |               1200 |
+------------+--------------------+
```

You can use these filters with the standard [logical operators (AND, OR, NOT)](/sql-reference/operators-logical) as well as
with other criteria. For example:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
  my_sv_orders
  DIMENSIONS customers.customer_name
  METRICS orders.total_revenue
  WHERE (customers.active_only OR customers.region_us)
    AND orders.completed_only
);
```

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    my_sv_orders
    DIMENSIONS customers.customer_name, orders.high_value_order, orders.order_date
  )
  orders WHERE orders.high_value_order AND orders.order_date >= '2024-02-01';
```

## Viewing information about filters

When you run the [DESCRIBE SEMANTIC VIEW](/sql-reference/sql/desc-semantic-view), [SHOW SEMANTIC FACTS](/sql-reference/sql/show-semantic-facts), and
[SHOW SEMANTIC DIMENSIONS](/sql-reference/sql/show-semantic-dimensions) commands, the output includes information about the filters:

- For facts and dimensions that are filters, the output of the DESC SEMANTIC VIEW command includes the `LABELS` property, which
  is set to `["filter"]`. The `EXPRESSION` property is set to the SQL expression for the filter.

  Copy code

  ```
  DESC SEMANTIC VIEW my_sv_orders;
  ```

  ```
  +--------------+-------------------------------------------------------+---------------+--------------------------+---------------------------------------------------------------------+
  | object_kind  | object_name                                           | parent_entity | property                 | property_value                                                      |
  |--------------+-------------------------------------------------------+---------------+--------------------------+---------------------------------------------------------------------|
  ...
  | DIMENSION    | ACTIVE_ONLY                                           | CUSTOMERS     | TABLE                    | CUSTOMERS                                                           |
  | DIMENSION    | ACTIVE_ONLY                                           | CUSTOMERS     | EXPRESSION               | customers.status = 'ACTIVE'                                         |
  | DIMENSION    | ACTIVE_ONLY                                           | CUSTOMERS     | DATA_TYPE                | BOOLEAN                                                             |
  | DIMENSION    | ACTIVE_ONLY                                           | CUSTOMERS     | ACCESS_MODIFIER          | PUBLIC                                                              |
  | DIMENSION    | ACTIVE_ONLY                                           | CUSTOMERS     | LABELS                   | ["filter"]                                                          |
  ...
  | FACT         | VIP_CUSTOMER                                          | CUSTOMERS     | TABLE                    | CUSTOMERS                                                           |
  | FACT         | VIP_CUSTOMER                                          | CUSTOMERS     | EXPRESSION               | customers.loyalty_points >= 150 AND SUM(orders.order_amount) > 1000 |
  | FACT         | VIP_CUSTOMER                                          | CUSTOMERS     | DATA_TYPE                | BOOLEAN                                                             |
  | FACT         | VIP_CUSTOMER                                          | CUSTOMERS     | ACCESS_MODIFIER          | PUBLIC                                                              |
  | FACT         | VIP_CUSTOMER                                          | CUSTOMERS     | LABELS                   | ["filter"]                                                          |
  ...
  +--------------+-------------------------------------------------------+---------------+--------------------------+---------------------------------------------------------------------+
  ```
- For facts and dimensions that are filters, the output of the SHOW SEMANTIC FACTS and SHOW SEMANTIC DIMENSIONS commands include
  the `labels` column, which contains `["filter"]`.

  Copy code

  ```
  SHOW SEMANTIC FACTS IN my_sv_orders;
  ```

  ```
  +---------------+-------------+--------------------+------------+------------------+--------------+----------+---------+------------+
  | database_name | schema_name | semantic_view_name | table_name | name             | data_type    | synonyms | comment | labels     |
  |---------------+-------------+--------------------+------------+------------------+--------------+----------+---------+------------|
  | MY_DB         | MY_SCHEMA   | MY_SV_ORDERS       | CUSTOMERS  | VIP_CUSTOMER     | BOOLEAN      | NULL     | NULL    | ["filter"] |
  | MY_DB         | MY_SCHEMA   | MY_SV_ORDERS       | ORDERS     | COMPLETED_ONLY   | BOOLEAN      | NULL     | NULL    | ["filter"] |
  | MY_DB         | MY_SCHEMA   | MY_SV_ORDERS       | ORDERS     | HIGH_VALUE_ORDER | BOOLEAN      | NULL     | NULL    | ["filter"] |
  | MY_DB         | MY_SCHEMA   | MY_SV_ORDERS       | ORDERS     | ORDER_AMOUNT     | NUMBER(38,0) | NULL     | NULL    | NULL       |
  +---------------+-------------+--------------------+------------+------------------+--------------+----------+---------+------------+
  ```

  Copy code

  ```
  SHOW SEMANTIC DIMENSIONS IN my_sv_orders;
  ```

  ```
  +---------------+-------------+--------------------+------------+---------------+--------------------+----------+---------+------------+
  | database_name | schema_name | semantic_view_name | table_name | name          | data_type          | synonyms | comment | labels     |
  |---------------+-------------+--------------------+------------+---------------+--------------------+----------+---------+------------|
  | MY_DB         | MY_SCHEMA   | MY_SV_ORDERS       | CUSTOMERS  | ACTIVE_ONLY   | BOOLEAN            | NULL     | NULL    | ["filter"] |
  | MY_DB         | MY_SCHEMA   | MY_SV_ORDERS       | CUSTOMERS  | CUSTOMER_NAME | VARCHAR(134217728) | NULL     | NULL    | NULL       |
  | MY_DB         | MY_SCHEMA   | MY_SV_ORDERS       | CUSTOMERS  | REGION_US     | BOOLEAN            | NULL     | NULL    | ["filter"] |
  | MY_DB         | MY_SCHEMA   | MY_SV_ORDERS       | ORDERS     | ORDER_DATE    | DATE               | NULL     | NULL    | NULL       |
  +---------------+-------------+--------------------+------------+---------------+--------------------+----------+---------+------------+
  ```

In addition, the INFORMATION\_SCHEMA [SEMANTIC\_DIMENSIONS](/sql-reference/info-schema/semantic_dimensions) and
[SEMANTIC\_FACTS](/sql-reference/info-schema/semantic_facts) views contain an additional VARIANT column named `labels`. The
column contains `"filter"` if the fact or dimension is a filter. For example:

Copy code

```
SELECT * FROM INFORMATION_SCHEMA.SEMANTIC_DIMENSIONS WHERE semantic_view_name = 'MY_SV_ORDERS';
```

```
+-----------------------+----------------------+--------------------+------------+---------------+--------------------+-----------------------------+----------+---------+-------------------------------------+-----------------------------------+----------------------------+-----------------------------------+------------+
| SEMANTIC_VIEW_CATALOG | SEMANTIC_VIEW_SCHEMA | SEMANTIC_VIEW_NAME | TABLE_NAME | NAME          | DATA_TYPE          | EXPRESSION                  | SYNONYMS | COMMENT | CORTEX_SEARCH_SERVICE_DATABASE_NAME | CORTEX_SEARCH_SERVICE_SCHEMA_NAME | CORTEX_SEARCH_SERVICE_NAME | CORTEX_SEARCH_SERVICE_COLUMN_NAME | LABELS     |
|-----------------------+----------------------+--------------------+------------+---------------+--------------------+-----------------------------+----------+---------+-------------------------------------+-----------------------------------+----------------------------+-----------------------------------+------------|
| MY_DB                 | MY_SCHEMA            | MY_SV_ORDERS       | CUSTOMERS  | ACTIVE_ONLY   | BOOLEAN            | customers.status = 'ACTIVE' | NULL     | NULL    | NULL                                | NULL                              | NULL                       | NULL                              | [          |
|                       |                      |                    |            |               |                    |                             |          |         |                                     |                                   |                            |                                   |   "filter" |
|                       |                      |                    |            |               |                    |                             |          |         |                                     |                                   |                            |                                   | ]          |
...
+-----------------------+----------------------+--------------------+------------+---------------+--------------------+-----------------------------+----------+---------+-------------------------------------+-----------------------------------+----------------------------+-----------------------------------+------------+
```
