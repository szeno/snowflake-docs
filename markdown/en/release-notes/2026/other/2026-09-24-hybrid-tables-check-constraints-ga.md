# Sep 24, 2026: CHECK constraints on hybrid tables (*General availability*)

With this release, [hybrid tables](/user-guide/tables-hybrid) support
[CHECK constraints](/sql-reference/constraints-overview#label-constraints-check). Previously, CHECK constraints were
limited to standard tables and Snowflake-managed Iceberg tables, so a hybrid table workload had to enforce
value-level rules in application code.

Define the constraint when you create the table, either inline on a single column or out of line across several
columns:

Copy code

```
CREATE OR REPLACE HYBRID TABLE orders (
  order_id INTEGER PRIMARY KEY,
  quantity INTEGER CHECK (quantity > 0),
  list_price NUMBER(10,2),
  sale_price NUMBER(10,2),
  CONSTRAINT check_sale_price CHECK (sale_price <= list_price)
  );
```

Snowflake enforces the constraint on every write, including INSERT, UPDATE, MERGE, and
CREATE HYBRID TABLE … AS SELECT. A statement that violates the constraint fails, and the row isn’t written.

The following limitations apply:

- You can define a CHECK constraint only when you create the table. Adding one to an existing hybrid table with
  ALTER TABLE … ADD CONSTRAINT isn’t supported.
- You can’t use [COPY INTO <table>](/sql-reference/sql/copy-into-table) to load a hybrid table that has a CHECK constraint. The
  operation fails. Use [INSERT](/sql-reference/sql/insert) or
  [CREATE HYBRID TABLE … AS SELECT](/sql-reference/sql/create-hybrid-table#label-create-hybrid-table-as) instead.

For more information, see
[CHECK constraints on hybrid tables](/sql-reference/sql/create-hybrid-table#label-hybrid-table-check-constraints).
