# Selecting from a stored procedure

Some stored procedures return tabular data. To select and manipulate this tabular data, you can call these
stored procedures in the [FROM](/sql-reference/constructs/from) clause of a SELECT statement.

## Run a SELECT statement with the TABLE keyword

When calling the stored procedure, omit the [CALL](/sql-reference/sql/call) command. Instead, use the TABLE keyword,
and name the procedure inside parentheses:

Copy code

```
SELECT ... FROM TABLE( <stored_procedure_name>( <arg> [ , <arg> ... ] ) );
```

## Example that selects from a stored procedure

This example uses the data in the following table:

Copy code

```
CREATE OR REPLACE TABLE orders (
  order_id INT,
  u_id VARCHAR,
  order_date DATE,
  order_amount NUMBER(12,2));

INSERT INTO orders VALUES (1, 'user_id_001', current_date, 500.00);
INSERT INTO orders VALUES (2, 'user_id_003', current_date, 225.00);
INSERT INTO orders VALUES (3, 'user_id_001', current_date, 725.00);
INSERT INTO orders VALUES (4, 'user_id_002', current_date, 150.00);
INSERT INTO orders VALUES (5, 'user_id_002', current_date, 900.00);
```

The following stored procedure returns order information based on a user ID:

Copy code

```
CREATE OR REPLACE PROCEDURE find_orders_by_user_id(user_id VARCHAR)
RETURNS TABLE (
  order_id INT, order_date DATE, order_amount NUMBER(12,2)
)
LANGUAGE SQL AS
DECLARE
  res RESULTSET;
BEGIN
  res := (SELECT order_id, order_date, order_amount FROM orders WHERE u_id = :user_id);
  RETURN TABLE(res);
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE find_orders_by_user_id(user_id VARCHAR)
RETURNS TABLE (
  order_id INT, order_date DATE, order_amount NUMBER(12,2)
)
LANGUAGE SQL AS
$$
DECLARE
  res RESULTSET;
BEGIN
  res := (SELECT order_id, order_date, order_amount FROM orders WHERE u_id = :user_id);
  RETURN TABLE(res);
END;
$$
;
```

The following SELECT statement retrieves the stored procedure’s results:

Copy code

```
SELECT * FROM TABLE(find_orders_by_user_id('user_id_001'));
```

```
+----------+------------+--------------+
| ORDER_ID | ORDER_DATE | ORDER_AMOUNT |
|----------+------------+--------------|
|        1 | 2024-08-30 |       500.00 |
|        3 | 2024-08-30 |       725.00 |
+----------+------------+--------------+
```

## Limitations for selecting from a stored procedure

The following limitations apply to selecting from a stored procedure:

- Only stored procedures that perform SELECT, SHOW, DESCRIBE, or CALL statements can be placed in the FROM clause
  of a SELECT statement. Stored procedures that make modifications using DDL or DML operations aren’t allowed.
  For stored procedures that issue CALL statements, these limitations apply to the stored procedures that are called.
- Only stored procedures that return tabular data with a static output schema can be placed in the FROM clause
  of a SELECT statement. The output columns must be named and typed. For example, a stored procedure with the
  following RETURNS clause is supported:

  Copy code

  ```
  RETURNS TABLE (col1 INT, col2 STRING)
  ```

  A stored procedure with the following RETURNS clause is not supported because it doesn’t return tabular data:

  Copy code

  ```
  RETURNS STRING
  ```

  A stored procedure with the following RETURNS clause is not supported because it doesn’t provide
  a fixed output schema:

  Copy code

  ```
  RETURNS TABLE()
  ```
- The stored procedure must be called in the FROM clause of a SELECT block in one of the following statements:

  - [SELECT](/sql-reference/sql/select)
  - [INSERT](/sql-reference/sql/insert), [UPDATE](/sql-reference/sql/update), [DELETE](/sql-reference/sql/delete), or [MERGE](/sql-reference/sql/merge)
  - [CREATE TABLE AS SELECT](/sql-reference/sql/create-table#label-ctas-syntax)
- The stored procedure can’t accept correlated input arguments from their outer scope, such as a reference to any
  [CTE](/user-guide/queries-cte) defined outside of the SELECT statement.
- If an argument contains a subquery, then that subquery can’t use a CTE defined by the WITH clause.
- A SELECT statement containing a stored procedure call can’t be used in the body of a view, a user-defined function (UDF),
  a user-defined table function (UDTF), or in objects such as [row access policies](/user-guide/security-row-intro) and
  [data masking policies](/user-guide/security-column-intro).
- You can’t use [bind variables](/sql-reference/bind-variables) in a SELECT statement that calls a stored
  procedure. For example, the following SELECT statements aren’t allowed:

  Copy code

  ```
  SELECT * FROM TABLE(my_stored_procedure(?));

  SELECT * FROM TABLE(my_stored_procedure('a')) WHERE my_var = :var2;
  ```
