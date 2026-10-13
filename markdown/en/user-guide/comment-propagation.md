# Column comment propagation

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Comment propagation uses the `BY_NAME` column lineage that Snowflake records for your objects. When you set or
unset a comment on a column, Snowflake finds the downstream columns that read it as-is and applies the same comment to
them. When you create an object, its columns inherit the comments that already exist upstream. Snowflake records how
each comment was applied, so you can distinguish a comment that a user wrote from one that propagation applied.

## Enable and disable comment propagation

Comment propagation is controlled by the account-level `FEATURE_COMMENT_PROPAGATION` parameter. The parameter is
`DISABLED` by default, so nothing propagates until an account administrator turns the feature on. After Snowflake enables
this preview for your account, use [ALTER ACCOUNT](/sql-reference/sql/alter-account) to set the parameter:

Copy code

```
USE ROLE ACCOUNTADMIN;
ALTER ACCOUNT SET FEATURE_COMMENT_PROPAGATION = 'ENABLED';
```

To check the current value:

Copy code

```
SHOW PARAMETERS LIKE 'FEATURE_COMMENT_PROPAGATION' IN ACCOUNT;
```

To turn the feature off for your account:

Copy code

```
ALTER ACCOUNT SET FEATURE_COMMENT_PROPAGATION = 'DISABLED';
```

Disabling the feature stops all future propagation. Comments that already propagated stay where they are, and they keep
their recorded apply method. To return the parameter to its default value, unset it:

Copy code

```
ALTER ACCOUNT UNSET FEATURE_COMMENT_PROPAGATION;
```

## Supported objects

Comment propagation supports every column that `BY_NAME` column lineage covers. The set of supported objects comes from
that lineage rather than from comment propagation:

| Object | Can be a source of a propagated comment | Can receive a propagated comment |
| --- | --- | --- |
| Table | Yes | No |
| View, including a secure view | Yes | Yes |
| Materialized view | Yes | Yes |
| Dynamic table | Yes | Yes |

Expand

Show lessSee more

## As-is lineage

Propagation follows *as-is* `BY_NAME` column lineage. For more information about `BY_NAME` dependencies, see
[Object Dependencies](/user-guide/object-dependencies).

A downstream column is as-is when it reproduces exactly one upstream column without changing its values. A comment is
only meaningful downstream when the values it describes are still the same values, which is why propagation stops at the
first column that transforms, combines, or aggregates its input.

The examples in this section read from a base table `t1` whose columns include `c1` and `c2`, a `c_num` column typed
`NUMBER(10,0)`, and a `c_str` column typed `VARCHAR(20)`.

### Relationships that are as-is

A bare projection of a single column
:   The column is selected directly, with or without an alias, and with or without a `WHERE` clause or a join:

    Copy code

    ```
    CREATE VIEW v1 AS SELECT c1 FROM t1;
    CREATE VIEW v2 AS SELECT c1 AS customer_id FROM t1 WHERE c1 IS NOT NULL;
    CREATE VIEW v3 AS SELECT t1.c1 FROM t1 JOIN t2 ON t1.c1 = t2.c1;
    ```

    Selecting with `SELECT *` is a bare projection of every column, so every column of the resulting object is as-is.

A lossless cast of a single column
:   The cast stays in the same type family and can’t lose any value, for example widening `NUMBER(10,0)` to
    `NUMBER(38,0)`, widening `VARCHAR(20)` to `VARCHAR(50)`, or changing only nullability:

    Copy code

    ```
    CREATE VIEW v4 AS SELECT c_num::NUMBER(38,0) AS amount FROM t1;   -- c_num is NUMBER(10,0)
    ```

A passthrough through a subquery or a common table expression
:   Snowflake follows the projection into derived tables and CTEs and classifies the relationship by what the innermost
    expression does:

    Copy code

    ```
    CREATE VIEW v5 AS SELECT c1 FROM (SELECT c1 FROM t1);
    ```

### Relationships that aren’t as-is

Any expression that alters the value
:   Scalar functions, arithmetic, `CASE` expressions, and concatenation all produce a new value:

    Copy code

    ```
    CREATE VIEW v6 AS SELECT UPPER(c1) AS c1 FROM t1;
    CREATE VIEW v7 AS SELECT c1 + 1 AS c1 FROM t1;
    CREATE VIEW v8 AS SELECT CASE WHEN c1 > 0 THEN c1 ELSE 0 END AS c1 FROM t1;
    ```

Any aggregation
:   An aggregate anywhere in the expression means the column describes many input rows instead of one:

    Copy code

    ```
    CREATE VIEW v9 AS SELECT SUM(c1) AS c1 FROM t1;
    ```

A combination of several columns
:   The output column has more than one upstream column, so no single comment describes it:

    Copy code

    ```
    CREATE VIEW v10 AS SELECT c1 || c2 AS c1 FROM t1;
    CREATE VIEW v11 AS SELECT c1 FROM t1 UNION ALL SELECT c1 FROM t2;
    ```

A cast that can lose information
:   Narrowing casts and casts across type families aren’t as-is:

    Copy code

    ```
    CREATE VIEW v12 AS SELECT c_str::VARCHAR(10) AS c_str FROM t1;   -- narrowing a VARCHAR(20)
    CREATE VIEW v13 AS SELECT c_num::VARCHAR AS c_num FROM t1;       -- NUMBER to VARCHAR crosses type families
    ```

A transformation hidden inside a subquery
:   Following the projection into a derived table means a transformation can’t be disguised as a passthrough:

    Copy code

    ```
    CREATE VIEW v14 AS SELECT c1 FROM (SELECT c1 + 1 AS c1 FROM t1);
    ```

## Statements that trigger propagation

The following statements start a propagation pass:

Setting a column comment
:   Copy code

    ```
    ALTER TABLE t1 ALTER COLUMN c1 COMMENT 'Customer identifier';
    ALTER TABLE t1 MODIFY COLUMN c1 COMMENT 'Customer identifier';
    ALTER DYNAMIC TABLE dt1 ALTER COLUMN c1 COMMENT 'Customer identifier';
    COMMENT ON COLUMN t1.c1 IS 'Customer identifier';
    ```

    The comment is applied to the as-is downstream columns that propagation reaches.

Unsetting a column comment
:   Copy code

    ```
    ALTER TABLE t1 ALTER COLUMN c1 UNSET COMMENT;
    ALTER DYNAMIC TABLE dt1 ALTER COLUMN c1 UNSET COMMENT;
    ```

    The copies that were propagated from this column downstream are cleared.

Creating a view, materialized view, or dynamic table
:   Copy code

    ```
    CREATE VIEW v1 AS SELECT c1 FROM t1;
    CREATE MATERIALIZED VIEW mv1 AS SELECT c1 FROM t1;
    CREATE DYNAMIC TABLE dt1 TARGET_LAG = '1 hour' WAREHOUSE = wh1 AS SELECT c1 FROM t1;
    ```

    Each column created without a comment inherits the comment of the nearest upstream column that has one. `CREATE OR REPLACE` re-runs this inheritance against the new definition.

Creating a view, materialized view, or dynamic table with an inline column comment
:   Copy code

    ```
    CREATE VIEW v1 (c1 COMMENT 'Customer identifier') AS SELECT c1 FROM t1;
    ```

    The column you comment inline becomes a source, and its comment propagates to the as-is columns downstream of it.

## Propagation behavior

- **Comments flow from upstream to downstream only.** Setting a comment on a column propagates to every as-is column
  downstream of it recursively.
- **A user-written comment is never overwritten.** Downstream propagation along a lineage path stops as soon as it
  reaches a column that carries a user comment.
- **A new user comment overrides the propagated comments downstream of it.** The column becomes the source for its own
  branch of the lineage graph.

## Find out where a comment came from

Every column comment carries an apply method that records whether a user wrote it or propagation applied it. You can
read it in Snowsight or with a system function.

### In Snowsight

Open the **Columns** tab for a table, view, or dynamic table. Each column’s description shows an icon that identifies
its origin:

- A user icon, with the tooltip **User generated**, means the comment was written on that column.
- A propagation icon, with the tooltip **Propagated from upstream**, means the comment arrived by propagation.

A column with no comment shows no icon. The **Columns** tab doesn’t show the icon for a materialized view, so use the
system function to inspect provenance for materialized view columns.

### With SQL

Call [SYSTEM$GET\_COLUMN\_COMMENT\_PROPAGATION\_SOURCE](/sql-reference/functions/system_get_column_comment_propagation_source) with the fully qualified name of a
column. It returns the column whose comment a user wrote, or NULL when the comment wasn’t propagated:

Copy code

```
SELECT SYSTEM$GET_COLUMN_COMMENT_PROPAGATION_SOURCE('my_db.my_schema.orders_v2.order_id');
```

For the cases that return NULL and the privileges the function requires, see
[SYSTEM$GET\_COLUMN\_COMMENT\_PROPAGATION\_SOURCE](/sql-reference/functions/system_get_column_comment_propagation_source).

## Usage notes

- **Propagation requires `BY_NAME` lineage recorded in October 2026 or later.** Comments don’t propagate along lineage
  that Snowflake recorded before this date, even after you enable the feature. To bring an existing view, materialized
  view, or dynamic table into propagation, re-create it with `CREATE OR REPLACE` so that Snowflake records its lineage
  again.
- **Propagation is asynchronous and best effort.** Propagated changes can take up to 10 minutes to appear on
  downstream columns. It runs after the transaction that sets or unsets a comment, so your DDL statement doesn’t wait
  for it and DDL latency stays the same.
- **A DDL statement can succeed even if propagation later fails.** Because propagation runs outside the transaction,
  Snowflake commits the comment you set before propagation runs. An internal error can then interrupt propagation
  without affecting the committed comment. To retry, rerun the DDL statement that sets or unsets the source comment.

## Examples

The following example builds a small lineage graph and walks a comment through it. Every column in the graph is an as-is
projection of `orders.order_id`.

1. Create a table, a dynamic table that reads it, a view on that dynamic table, and a second view that reads the table
   directly. The dynamic table needs an existing warehouse, named `my_wh` here:

   Copy code

   ```
   CREATE OR REPLACE TABLE orders (order_id NUMBER);

   CREATE OR REPLACE DYNAMIC TABLE orders_dt TARGET_LAG = '1 hour' WAREHOUSE = my_wh
     AS SELECT order_id FROM orders;

   CREATE OR REPLACE VIEW orders_v1 AS SELECT order_id FROM orders_dt;
   CREATE OR REPLACE VIEW orders_v2 AS SELECT order_id FROM orders;

   -- No column carries a comment yet.
   ```
2. Comment the column on the table:

   Copy code

   ```
   ALTER TABLE orders ALTER COLUMN order_id COMMENT 'Order identifier';

   -- After propagation finishes:
   --   orders.order_id     = 'Order identifier'   (you wrote it)
   --   orders_dt.order_id  = 'Order identifier'   (propagated from orders.order_id)
   --   orders_v1.order_id  = 'Order identifier'   (propagated from orders_dt.order_id)
   --   orders_v2.order_id  = 'Order identifier'   (propagated from orders.order_id)
   ```
3. Comment the same column on the intermediate dynamic table:

   Copy code

   ```
   ALTER DYNAMIC TABLE orders_dt ALTER COLUMN order_id COMMENT 'Order identifier, EU orders only';

   -- After propagation finishes:
   --   orders.order_id     = 'Order identifier'                   (unchanged; nothing propagates upstream)
   --   orders_dt.order_id  = 'Order identifier, EU orders only'   (you wrote it, replacing the propagated copy)
   --   orders_v1.order_id  = 'Order identifier, EU orders only'   (propagated from orders_dt.order_id)
   --   orders_v2.order_id  = 'Order identifier'                   (unchanged; on the other branch)
   ```
4. Change the comment on the table:

   Copy code

   ```
   ALTER TABLE orders ALTER COLUMN order_id COMMENT 'Unique order identifier';

   -- After propagation finishes:
   --   orders.order_id     = 'Unique order identifier'            (you wrote it)
   --   orders_dt.order_id  = 'Order identifier, EU orders only'   (unchanged; your comment stops propagation here)
   --   orders_v1.order_id  = 'Order identifier, EU orders only'   (unchanged; orders_dt.order_id shadows it)
   --   orders_v2.order_id  = 'Unique order identifier'            (propagated from orders.order_id)
   ```
5. Create another view on the table:

   Copy code

   ```
   CREATE OR REPLACE VIEW orders_v3 AS SELECT order_id FROM orders;

   -- After propagation finishes:
   --   orders_v3.order_id  = 'Unique order identifier'            (inherited from orders.order_id)
   ```
