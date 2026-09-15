# Inline Stored Procedures for hybrid tables

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Inline Stored Procedures are a new type of
[Snowflake stored procedure](/developer-guide/stored-procedure/stored-procedures-overview)
designed specifically for operational workloads on [hybrid tables](/user-guide/tables-hybrid).
By executing the entire procedure body as a single atomic unit pushed directly to the query processing
layer, Inline Stored Procedures reduce per-statement overhead and deliver significantly lower latency
for OLTP-style workloads. In benchmarks using the TPROC-C workload, Inline Stored Procedures achieve over
7,000 transactions per minute (TPM) on a single XSMALL warehouse, more than a 10x improvement
compared to standard Snowflake stored procedures.

## Prerequisites

This public preview is available on any Snowflake account and warehouse. No request is required.

For the best performance, set the `ENABLE_USE_STABLE_PATH` parameter to `TRUE` on the warehouse
that runs your Inline Stored Procedures. For details, see
[Relationship to operational query performance](#label-isproc-operational-query-performance).

## Relationship to operational query performance

Inline Stored Procedures build on the
[operational query performance improvements](/user-guide/hybrid-tables-operational-query-performance)
available for hybrid tables. Those improvements automatically recognize recurring, short-running
queries on hybrid tables and optimize their execution by reducing the per-query overhead from
parsing, plan compilation, and scheduling.

To get the best performance, set the `ENABLE_USE_STABLE_PATH` parameter to `TRUE` on the warehouse
that runs your Inline Stored Procedures. This is the same parameter that enables the operational
query performance improvements, and it applies those optimizations to the individual statements
inside the procedure body. Enabling this parameter also optimizes single-statement queries on the
same warehouse, so both workload types benefit. These optimizations are transparent: Snowflake
applies them automatically when eligible queries are detected.

For more details on eligible query patterns and how the optimizations work, see
[Performance improvements for operational queries on hybrid tables](/user-guide/hybrid-tables-operational-query-performance).

## Overview

An Inline Stored Procedure is declared with `CREATE INLINE PROCEDURE` and uses a
`BEGIN ATOMIC` block as its body. The `ATOMIC` keyword signals to Snowflake that all
statements in the procedure should be compiled together, pushed to the execution layer as a
single unit, and run as one atomic block.

Inline Stored Procedures differ from standard stored procedures in the following key ways:

- **Execution model**: The entire procedure body is pre-compiled as a unit and dispatched to the
  query processing layer in a single step, avoiding the per-statement overhead of standard stored
  procedures.
- **Atomic execution**: Each invocation is treated as an [atomic block](#label-isproc-atomic-blocks).
  If any statement fails, all prior changes in the same invocation are rolled back automatically.
  You can’t use explicit `BEGIN`, `COMMIT`, or `ROLLBACK` inside an Inline Stored Procedure.
- **Hybrid tables only**: Inline Stored Procedures operate exclusively on hybrid tables. Statements
  that access standard Snowflake tables or other table types aren’t supported within Inline Stored
  Procedures.
- **OLTP-oriented**: Inline Stored Procedures are designed for short-running, low-latency operations.
  Each invocation should touch a small number of rows and aim to complete in a few hundred milliseconds.

### Use cases

Inline Stored Procedures are best suited for high-throughput, OLTP-style workloads where low
latency and reduced round-trip overhead matter:

- **Single-statement procedures that wrap a DML operation**. A common pattern is to wrap a single
  `INSERT`, `UPDATE`, or `DELETE` in a stored procedure for abstraction or access control.
  With a standard stored procedure, each statement in the body incurs its own round trip between
  Snowflake layers. An Inline Stored Procedure executes the entire body as one unit, reducing that
  overhead and significantly lowering latency.
- **Multi-statement OLTP transactions**. Procedures that perform several related DML operations,
  such as reading a row to compute a value and then writing it back, or updating one row and
  recording an audit entry, avoid multiple per-statement round trips and run as a single atomic
  unit.
- **Scheduled maintenance from a task**. Invoke an Inline Stored Procedure from a
  [Snowflake task](/user-guide/tasks-intro) to run recurring DML on hybrid tables. A `CALL`
  statement is a standard SQL statement, so it works in a task definition the same way as other
  supported SQL.

Note

Inline Stored Procedures are compiled at `CALL` time, not at `CREATE` time. This is the
same behavior as standard Snowflake stored procedures. However, because Inline Stored Procedures
don’t yet support some constructs (see [Current limitations](#label-isproc-limitations)),
you may encounter errors only at runtime even though the `CREATE` statement succeeds.

For example, the following `CREATE` statement succeeds, but the `CALL` fails because the
`INSERT` is compiled independently and can’t see the table created by the preceding
`CREATE HYBRID TABLE`:

Copy code

```
-- CREATE succeeds: the body isn't compiled yet.
CREATE OR REPLACE INLINE PROCEDURE bad_example()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN ATOMIC
  CREATE HYBRID TABLE t1 (id NUMBER PRIMARY KEY);
  INSERT INTO t1 VALUES (1);
  RETURN 'done';
END;
$$;

-- CALL fails: DDL isn't supported inside an Inline Stored Procedure,
-- and the INSERT can't resolve t1 because each statement is compiled in isolation.
CALL bad_example();
```

To avoid this class of error, ensure that all tables referenced in the procedure already exist
before creating the procedure, and don’t include DDL inside Inline Stored Procedures. Because
unsupported constructs are only detected at `CALL` time, Snowflake recommends invoking a
newly created Inline Stored Procedure in a test environment to surface any
incompatible features before deploying it to a production workload.

## Atomic blocks

Every Inline Stored Procedure body is an `ATOMIC` block. An atomic block is a group of SQL
statements that Snowflake compiles and executes as a single unit. The block uses the following
syntax:

Copy code

```
BEGIN ATOMIC
  <sql_statement> ;
  [ <sql_statement> ; ... ]
END ;
```

### Execution

When an Inline Stored Procedure is called, Snowflake acquires a single read timestamp at the
start of the atomic block. All statements in the block share that timestamp, so every read sees
a consistent snapshot of the data.

Within the block, statements run sequentially and each statement can see the writes made by
earlier statements in the same block (read-your-own-writes). Outside the block, no other session
can see the block’s writes until the block completes successfully.

### Error handling

Either all statements in the block succeed, or the entire block is rolled back:

- If all statements complete without an unhandled error, the block’s changes commit together.
- If any statement raises an unhandled error, all changes made by prior statements in the same
  block are rolled back automatically.
- You can use `EXCEPTION` handlers (with `WHEN ... THEN`) inside the block to catch errors
  and return a controlled result instead of rolling back. See the
  [error handling example](#label-isproc-example-exception) for a working demonstration.

Explicit [BEGIN](/sql-reference/sql/begin), [COMMIT](/sql-reference/sql/commit),
and [ROLLBACK](/sql-reference/sql/rollback) statements aren’t allowed inside an atomic
block.

The entire body of an Inline Stored Procedure is an atomic block.

## Syntax

### CREATE INLINE PROCEDURE

Copy code

```
CREATE [ OR REPLACE ] INLINE PROCEDURE <name> (
    [ <arg_name> <arg_data_type> [ , ... ] ] )
  RETURNS { <result_data_type>
          | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE SQL
  AS
  $$
  BEGIN ATOMIC
    <sql_statement> ;
    [ <sql_statement> ; ... ]
    RETURN <value> ;
  END ;
  $$
```

Note

When creating an Inline Stored Procedure in [SnowSQL](/user-guide/snowsql) or
[Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), use `$$` as the string literal delimiter around the procedure body.

When writing the procedure body:

- Reference procedure arguments inside SQL statements using a colon prefix: `:arg_name`.
- You can declare `RETURNS TABLE()` with an empty column list. Snowflake infers the column names
  and types from the returned `RESULTSET` when you `CALL` the procedure.
- To use the procedure as a table source, for example `SELECT ... FROM TABLE(proc())`, declare an
  explicit column list. `RETURNS TABLE()` without columns fails in that context because the return
  table must declare a nonzero number of columns.
- When you declare columns in `RETURNS TABLE`, the column types must match the types returned by
  the query exactly.

### CALL

To invoke an Inline Stored Procedure, use the [CALL](/sql-reference/sql/call) command:

Copy code

```
CALL <name> ( [ <arg> [ , ... ] ] )
```

### Compilation

Inline Stored Procedures compile the entire body up front at `CALL` time. This eager compilation
differs from standard stored procedures, which compile statements as they run.

The following effects are expected:

- Statically decidable errors are reported at `CALL` time, before any statement in the body runs.
  Examples include an unknown column or table, the wrong number of function arguments or `INSERT`
  columns, and a `RETURN` type that doesn’t match the declared return type.
- Those compilation errors aren’t catchable by an `EXCEPTION` handler. The handler runs only for
  errors that occur after compilation succeeds.
- A compilation error in a branch is reported even if that branch wouldn’t execute at runtime.
- Snowflake type-checks every `RETURN` path against the declared return type, regardless of which
  branch runs.

## Examples

The following examples use these hybrid tables:

Copy code

```
CREATE OR REPLACE HYBRID TABLE orders (
  order_id    NUMBER(18,0) NOT NULL,
  customer_id NUMBER(18,0) NOT NULL,
  product     VARCHAR(50)  NOT NULL,
  quantity    NUMBER(10,0) NOT NULL DEFAULT 1,
  status      VARCHAR(20)  NOT NULL DEFAULT 'PENDING',
  PRIMARY KEY (order_id)
);

CREATE OR REPLACE HYBRID TABLE order_audit (
  audit_id   NUMBER(18,0) NOT NULL,
  order_id   NUMBER(18,0) NOT NULL,
  old_status VARCHAR(20)  NOT NULL,
  new_status VARCHAR(20)  NOT NULL,
  PRIMARY KEY (audit_id)
);
```

### Insert a row

This procedure inserts a new order into the `orders` table and returns a status string:

Copy code

```
CREATE OR REPLACE INLINE PROCEDURE place_order(
  order_id    NUMBER(18,0),
  customer_id NUMBER(18,0),
  product     VARCHAR,
  quantity    NUMBER(10,0)
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN ATOMIC
  INSERT INTO orders (order_id, customer_id, product, quantity, status)
    VALUES (:order_id, :customer_id, :product, :quantity, 'PENDING');
  RETURN 'OK';
END;
$$;

CALL place_order(1001, 42, 'Snowboard', 2);
```

### Insert a row using a sequence

Inline Stored Procedures can use sequences, including `NEXTVAL` and auto-increment columns. This
procedure inserts a new order and lets a sequence generate the primary key:

Copy code

```
CREATE OR REPLACE SEQUENCE order_id_seq START = 2000 INCREMENT = 1;

CREATE OR REPLACE INLINE PROCEDURE place_order_seq(
  customer_id NUMBER(18,0),
  product     VARCHAR,
  quantity    NUMBER(10,0)
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN ATOMIC
  INSERT INTO orders (order_id, customer_id, product, quantity, status)
    VALUES (order_id_seq.NEXTVAL, :customer_id, :product, :quantity, 'PENDING');
  RETURN 'OK';
END;
$$;

CALL place_order_seq(42, 'Helmet', 1);
```

### Update a row

This procedure updates the status of an existing order:

Copy code

```
CREATE OR REPLACE INLINE PROCEDURE fulfill_order(
  order_id   NUMBER(18,0),
  new_status VARCHAR
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN ATOMIC
  UPDATE orders
    SET status = :new_status
    WHERE order_id = :order_id;
  RETURN :new_status;
END;
$$;

CALL fulfill_order(1001, 'SHIPPED');
```

### Delete a row

This procedure deletes an order by primary key:

Copy code

```
CREATE OR REPLACE INLINE PROCEDURE cancel_order(order_id NUMBER(18,0))
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN ATOMIC
  DELETE FROM orders
    WHERE order_id = :order_id;
  RETURN 'Canceled order ' || :order_id;
END;
$$;

CALL cancel_order(8001);
```

### Retrieve a row

This procedure performs a point lookup and returns the matching row. The column types in
`RETURNS TABLE` must match the table column types exactly:

Copy code

```
CREATE OR REPLACE INLINE PROCEDURE get_order(order_id NUMBER(18,0))
RETURNS TABLE(
  order_id    NUMBER(18,0),
  customer_id NUMBER(18,0),
  product     VARCHAR(50),
  quantity    NUMBER(10,0),
  status      VARCHAR(20)
)
LANGUAGE SQL
AS
$$
BEGIN ATOMIC
  LET res RESULTSET := (
    SELECT order_id, customer_id, product, quantity, status
      FROM orders
      WHERE order_id = :order_id
  );
  RETURN TABLE(res);
END;
$$;

CALL get_order(1001);
```

### Return a table without declaring columns

You can declare `RETURNS TABLE()` with an empty column list. `CALL` infers the columns from the
returned `RESULTSET`. You can’t use that procedure as a table source in a `FROM` clause unless you
declare an explicit schema:

Copy code

```
CREATE OR REPLACE INLINE PROCEDURE list_orders()
RETURNS TABLE()
LANGUAGE SQL
AS
$$
BEGIN ATOMIC
  LET res RESULTSET := (
    SELECT order_id, customer_id, product, quantity, status
      FROM orders
  );
  RETURN TABLE(res);
END;
$$;

-- CALL succeeds and infers columns from the RESULTSET.
CALL list_orders();

-- Fails: 001175 Return table must declare a nonzero number of columns.
SELECT * FROM TABLE(list_orders());
```

### Atomic multi-statement updates

The procedure body runs as a single atomic unit: if any statement fails, all prior changes in the
same invocation are rolled back. This procedure updates an order’s status and writes an audit
record in one call. Both the `UPDATE` and the `INSERT` succeed together, or neither takes effect:

Copy code

```
CREATE OR REPLACE INLINE PROCEDURE update_order_status(
  p_order_id   NUMBER(18,0),
  p_new_status VARCHAR,
  p_audit_id   NUMBER(18,0)
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
  v_old_status VARCHAR;
BEGIN ATOMIC
  -- Capture the current status.
  SELECT status INTO :v_old_status
    FROM orders
    WHERE order_id = :p_order_id;

  -- Update the order.
  UPDATE orders
    SET status = :p_new_status
    WHERE order_id = :p_order_id;

  -- Write the audit record.
  INSERT INTO order_audit (audit_id, order_id, old_status, new_status)
    VALUES (:p_audit_id, :p_order_id, :v_old_status, :p_new_status);

  RETURN 'Updated order ' || :p_order_id
         || ' from ' || :v_old_status
         || ' to ' || :p_new_status;
END;
$$;

-- First call succeeds: orders.status is updated and an audit row is inserted.
CALL update_order_status(1001, 'DELIVERED', 9001);

-- Second call uses the same audit_id, so the INSERT fails with a duplicate key error.
-- Because the procedure is atomic, the UPDATE is also rolled back: orders.status
-- remains 'DELIVERED' rather than becoming 'RETURNED'.
CALL update_order_status(1001, 'RETURNED', 9001);
```

### Handle errors

This procedure catches a duplicate primary key error and returns a message instead of raising an
exception to the caller:

Copy code

```
CREATE OR REPLACE INLINE PROCEDURE safe_insert_order(
  order_id    NUMBER(18,0),
  customer_id NUMBER(18,0),
  product     VARCHAR,
  quantity    NUMBER(10,0)
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN ATOMIC
  INSERT INTO orders (order_id, customer_id, product, quantity, status)
    VALUES (:order_id, :customer_id, :product, :quantity, 'PENDING');
  RETURN 'OK';
EXCEPTION
  WHEN OTHER THEN
    RETURN 'ERROR: ' || SQLERRM;
END;
$$;

-- First call succeeds:
CALL safe_insert_order(1002, 55, 'Ski Boots', 1);

-- Second call with the same primary key returns an error message:
CALL safe_insert_order(1002, 55, 'Ski Boots', 1);
```

### Call from a task

You can schedule an Inline Stored Procedure to run on a recurring basis by defining a
[Snowflake task](/user-guide/tasks-intro) whose SQL body is a `CALL` statement.

This example creates a counter table, defines an Inline Stored Procedure that increments the
counter, schedules a task to call the procedure every minute, and shows how to test and resume
the task:

Copy code

```
CREATE OR REPLACE HYBRID TABLE counter (
  k NUMBER PRIMARY KEY,
  v NUMBER NOT NULL
);

INSERT INTO counter VALUES (1, 0);

CREATE OR REPLACE INLINE PROCEDURE increment_counter()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN ATOMIC
  UPDATE counter SET v = v + 1 WHERE k = 1;
  RETURN 'completed';
END;
$$;

-- Verify the procedure when called directly:
CALL increment_counter();
SELECT * FROM counter;

CREATE OR REPLACE TASK increment_counter_task
  WAREHOUSE = my_warehouse
  SCHEDULE = '1 MINUTE'
  AS
    CALL increment_counter();

-- Test the task with a manual run:
EXECUTE TASK increment_counter_task;
SELECT * FROM counter;

ALTER TASK increment_counter_task RESUME;

-- After subsequent scheduled runs, the counter increases on each execution:
SELECT * FROM counter;
```

### Complex multi-table procedure

The following example shows a more complex Inline Stored Procedure that reads from three tables,
increments a counter, uses `IF` / `ELSEIF` / `ELSE` branching with nested `BEGIN ... END`
blocks, and inserts into two tables, all within a single atomic block. If any step fails, every
change is rolled back.

The procedure uses these tables:

Copy code

```
CREATE OR REPLACE HYBRID TABLE warehouse (
  w_id   NUMBER(10,0) NOT NULL,
  w_name VARCHAR(10)  NOT NULL,
  w_tax  NUMBER(4,4)  NOT NULL DEFAULT 0.08,
  PRIMARY KEY (w_id)
);

CREATE OR REPLACE HYBRID TABLE district (
  d_id         NUMBER(10,0) NOT NULL,
  d_w_id       NUMBER(10,0) NOT NULL,
  d_name       VARCHAR(10)  NOT NULL,
  d_tax        NUMBER(4,4)  NOT NULL DEFAULT 0.05,
  d_next_o_id  NUMBER(10,0) NOT NULL DEFAULT 1,
  PRIMARY KEY (d_id, d_w_id)
);

CREATE OR REPLACE HYBRID TABLE customer (
  c_id       NUMBER(10,0) NOT NULL,
  c_d_id     NUMBER(10,0) NOT NULL,
  c_w_id     NUMBER(10,0) NOT NULL,
  c_name     VARCHAR(30)  NOT NULL,
  c_discount NUMBER(4,4)  NOT NULL DEFAULT 0.00,
  PRIMARY KEY (c_id, c_d_id, c_w_id)
);

CREATE OR REPLACE HYBRID TABLE new_order (
  no_o_id NUMBER(10,0) NOT NULL,
  no_d_id NUMBER(10,0) NOT NULL,
  no_w_id NUMBER(10,0) NOT NULL,
  PRIMARY KEY (no_o_id, no_d_id, no_w_id)
);
```

The procedure reads the warehouse tax rate, retrieves and increments the district’s next order
ID, looks up the customer discount, determines the initial order status based on a priority
argument, and then inserts both a new order record and an audit record:

Copy code

```
CREATE OR REPLACE INLINE PROCEDURE process_order(
  p_w_id     NUMBER(10,0),
  p_d_id     NUMBER(10,0),
  p_c_id     NUMBER(10,0),
  p_priority VARCHAR
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
  v_d_next_o_id NUMBER(10,0);
  v_d_tax       NUMBER(4,4);
  v_w_tax       NUMBER(4,4);
  v_c_discount  NUMBER(4,4);
  v_c_name      VARCHAR(30);
  v_status      VARCHAR(20);
BEGIN ATOMIC
  -- Step 1: Look up the warehouse tax rate.
  SELECT w_tax INTO :v_w_tax
    FROM warehouse
    WHERE w_id = :p_w_id;

  -- Step 2: Get the next order ID and increment the counter.
  SELECT d_next_o_id, d_tax INTO :v_d_next_o_id, :v_d_tax
    FROM district
    WHERE d_id = :p_d_id AND d_w_id = :p_w_id;

  UPDATE district
    SET d_next_o_id = d_next_o_id + 1
    WHERE d_id = :p_d_id AND d_w_id = :p_w_id;

  -- Step 3: Look up the customer discount.
  SELECT c_name, c_discount INTO :v_c_name, :v_c_discount
    FROM customer
    WHERE c_id = :p_c_id AND c_d_id = :p_d_id AND c_w_id = :p_w_id;

  -- Step 4: Determine the initial status based on priority.
  IF (:p_priority = 'EXPRESS') THEN
    BEGIN
      v_status := 'SHIPPED';
    END;
  ELSEIF (:p_priority = 'STANDARD') THEN
    BEGIN
      v_status := 'PENDING';
    END;
  ELSE
    BEGIN
      v_status := 'BACKORDER';
    END;
  END IF;

  -- Step 5: Insert the new order.
  INSERT INTO new_order (no_o_id, no_d_id, no_w_id)
    VALUES (:v_d_next_o_id, :p_d_id, :p_w_id);

  -- Step 6: Write an audit record with the computed status.
  INSERT INTO order_audit (audit_id, order_id, old_status, new_status)
    VALUES (:v_d_next_o_id, :v_d_next_o_id, 'NEW', :v_status);

  RETURN 'Order ' || :v_d_next_o_id
         || ' for ' || :v_c_name
         || ' [' || :v_status || ']'
         || ' (w_tax=' || :v_w_tax
         || ', d_tax=' || :v_d_tax
         || ', discount=' || :v_c_discount || ')';
END;
$$;

-- EXPRESS priority: order ships immediately.
CALL process_order(1, 1, 1, 'EXPRESS');

-- STANDARD priority: order is pending.
CALL process_order(1, 1, 1, 'STANDARD');
```

## Performance best practices

To get the best performance from Inline Stored Procedures, apply the following practices:

- **Enable the operational query performance optimizations**. Set the `ENABLE_USE_STABLE_PATH` parameter to `TRUE` on
  the warehouse that runs your Inline Stored Procedures. This parameter enables the
  [operational query performance improvements for hybrid tables](/user-guide/hybrid-tables-operational-query-performance),
  which optimize the individual statements inside the procedure body:

  Copy code

  ```
  ALTER WAREHOUSE <warehouse_name> SET ENABLE_USE_STABLE_PATH = TRUE;
  ```
- **Use bind variables (prepared statements)**. Call the procedure with bound parameters from your
  application code instead of string-interpolating values into the `CALL` statement. Most
  Snowflake drivers use bind variables automatically when you use prepared statements. Bind
  variables allow Snowflake to reuse the compiled plan across invocations, which significantly
  reduces per-call latency.
- **Use a multi-cluster XSMALL warehouse for high concurrency**. For high-throughput OLTP
  workloads, a multi-cluster warehouse with an `XSMALL` cluster size delivers the best
  price-performance. Scale out by increasing the maximum cluster count rather than scaling up to
  a larger size.
- **Benchmark from a client in the same region as your Snowflake deployment**. Network latency
  between the client and Snowflake has a direct impact on observed procedure latency and
  throughput. Run your benchmark or application from a VM or service in the same cloud region as
  your Snowflake account to measure the actual performance of Inline Stored Procedures rather
  than cross-region network overhead.

## Observability

Both the parent procedure call and its child statements appear in
[QUERY\_HISTORY](/sql-reference/account-usage/query_history). Query profiles are also available
for Inline Stored Procedures. For more information, see
[Analyze query profiles for hybrid tables](/user-guide/tables-hybrid-read-query-profiles).

## Current limitations

The following limitations apply to Inline Stored Procedures.

| Limitation | Description | Workaround |
| --- | --- | --- |
| Hybrid tables only | Inline Stored Procedures can only access hybrid tables. Statements that reference standard Snowflake tables, Iceberg tables, or other table types aren’t supported. | Use standard stored procedures for workloads that mix table types. |
| No DDL statements | Statements such as `CREATE TABLE`, `ALTER TABLE`, and `ALTER SESSION` aren’t supported. Because all statements are pre-compiled independently, DDL and metadata-affecting statements would produce incorrect compilation results. | Perform schema changes outside the procedure before invoking it. |
| No dynamic SQL | `EXECUTE IMMEDIATE` and other dynamic SQL constructs aren’t supported. All statements must be fully formed at compile time. | Rewrite logic using static SQL with conditional branching. |
| No explicit transactions | `BEGIN TRANSACTION`, `COMMIT`, and `ROLLBACK` aren’t allowed inside an Inline Stored Procedure. The procedure body runs as a single atomic block that either commits or rolls back in full. | Use `EXCEPTION` handlers to manage error cases within the atomic block. |
| No nested stored procedures | Calling another stored procedure from within an Inline Stored Procedure isn’t supported. | Consolidate logic into a single procedure. |
| Supported statement types only | Only `SELECT`, `INSERT`, `UPDATE`, `DELETE`, and `MERGE` are supported. Bulk load operations and other statement types aren’t allowed. | Use standard stored procedures or run unsupported statements outside the procedure. |
| No nested atomic blocks | The `ATOMIC` keyword can only appear on the top-level `BEGIN` block. Nesting `BEGIN ATOMIC` inside another `BEGIN ATOMIC` isn’t allowed. | Use plain `BEGIN ... END` blocks for control flow grouping inside the outer atomic block. |
| Can’t be called in an open transaction | Inline Stored Procedures can’t be invoked from within an existing transaction. They must be called with autocommit enabled. | Commit or roll back any open transaction before calling an Inline Stored Procedure. |
| At most one database | A procedure body can reference at most one database. That database doesn’t have to be the database that contains the procedure. Referencing two or more databases isn’t supported. | Keep all table references in a single database, or split the work across separate procedure calls. |
| No OUT arguments | `OUT` and `OUTPUT` parameters aren’t supported. | Return values using `RETURN` or `RETURNS TABLE`. |
| No CONTINUE exception handler | The `CONTINUE` exception handler type isn’t supported. Only `EXIT` (default) handlers are available. | Use `EXIT` exception handlers and restructure the control flow accordingly. |
| No caller context | Inline Stored Procedures run with owner’s rights only. Caller’s rights execution isn’t supported. | Design procedures so that the owner role has the necessary privileges. |
| No session variables | Session variables set outside the procedure aren’t accessible inside it. | Pass values as explicit procedure arguments instead. |
| No query ID for nested statements | The query ID of a statement executed inside an Inline Stored Procedure isn’t exposed to the caller. Results are still accessible using `CURSOR` or `RESULTSET`. | Use `RESULTSET` to capture and work with query results inside the procedure. |
| No dynamic context functions | The following dynamic context functions aren’t supported inside Inline Stored Procedures: `CURRENT_TIMESTAMP`, `CURRENT_TIME`, `CURRENT_DATE`, `SYSDATE`, `SYSTIMESTAMP`, `GETDATE`, `LOCALTIME`, and `LOCALTIMESTAMP`. | Compute the value in the caller and pass it as an explicit argument to the procedure. |
| No table functions | Table functions such as `FLATTEN`, `LATERAL FLATTEN`, `GENERATOR`, and `SPLIT_TO_TABLE` aren’t supported. The call fails with an error that the procedure is accessing a non-hybrid table. | Rewrite the query to use hybrid tables only, or run the table-function work outside the procedure. |
| UDF calls in scripting expressions | You can call a user-defined function (UDF) inside a SQL statement in the procedure body. Calling a UDF in a scripting expression, such as `LET` or `RETURN`, isn’t supported. | Call the UDF from a SQL statement, for example `SELECT my_udf(...) INTO :var FROM hybrid_table ...`. |
| Queries must involve a hybrid table | A query that doesn’t involve a hybrid table isn’t supported. Examples include `SELECT 1+2 INTO :v`, a `VALUES` source, and a constant CTE. Direct assignment is supported: `LET v := 1 + 2`. This restriction doesn’t apply to DML sources such as `INSERT ... SELECT 1`. | Use `LET` for constants and computed values instead of `SELECT ... INTO`. |
| No SQLROWCOUNT | The `SQLROWCOUNT` variable isn’t available, so you can’t drive control flow from the number of rows affected by DML. | Run `SELECT COUNT(*) INTO :n ...` against the hybrid table before or after the DML statement. |

Expand

Show lessSee more
