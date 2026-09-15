# Snowflake Scripting UDFs

Snowflake supports SQL user-defined functions (UDFs) that contain Snowflake Scripting procedural language.
These UDFs are called *Snowflake Scripting UDFs*.

Snowflake Scripting UDFs can be called in a SQL statement, such as a SELECT statement or INSERT statement.
Therefore, they are more flexible than a Snowflake Scripting stored procedure, which can only be called in
a SQL [CALL](/sql-reference/sql/call) command.

## General usage

A Snowflake Scripting UDF evaluates procedural code and returns a scalar (that is, single) value.

You can use the following subset of [Snowflake Scripting](/developer-guide/snowflake-scripting/index)
syntax in Snowflake Scripting UDFs:

- [Blocks](/developer-guide/snowflake-scripting/blocks)
- [Variables](/developer-guide/snowflake-scripting/variables)
- [RETURN command](/developer-guide/snowflake-scripting/return)
- [Conditional logic](/developer-guide/snowflake-scripting/branch)
- [Loops](/developer-guide/snowflake-scripting/loops)
- [Exceptions](/developer-guide/snowflake-scripting/exceptions)

## Supported data types

Snowflake Scripting UDFs support the following data types for both input arguments and
return values:

- [Numeric data types](/sql-reference/data-types-numeric) (for example, INTEGER, NUMBER, and FLOAT)
- [String & binary data types](/sql-reference/data-types-text) (for example, VARCHAR and BINARY)
- [Date & time data types](/sql-reference/data-types-datetime) (for example, DATE, TIME, and TIMESTAMP)
- [Logical data types](/sql-reference/data-types-logical) (for example, BOOLEAN)

Snowflake Scripting UDFs support the following data types for input arguments only:

- [Semi-structured data types](/sql-reference/data-types-semistructured) (for example, VARIANT, OBJECT, and ARRAY)
- [Structured data types](/sql-reference/data-types-structured) (for example, ARRAY, OBJECT, and MAP)

## Limitations

The following limitations apply to Snowflake Scripting UDFs:

- The following types of Snowflake Scripting syntax aren’t supported in Snowflake Scripting UDFs:

  - [Cursors](/developer-guide/snowflake-scripting/cursors)
  - [RESULTSETs](/developer-guide/snowflake-scripting/resultsets)
  - [Asynchronous child jobs](/developer-guide/snowflake-scripting/asynchronous-child-jobs)
- SQL statements aren’t supported in Snowflake Scripting UDFs (including SELECT, INSERT, UPDATE, and so on).
- Snowflake Scripting UDFs can’t be defined as table functions.
- The following expression types aren’t supported in Snowflake Scripting UDFs:

  - User-defined functions
  - Aggregation functions
  - Window functions
- Snowflake Scripting UDFs can’t be used when creating a materialized view.
- Snowflake Scripting UDFs can’t be used when creating row access policies and masking policies.
- Snowflake Scripting UDFs can’t be used to specify a default column value.
- Snowflake Scripting UDFs can’t be used in a COPY INTO command for data loading and unloading.
- Snowflake Scripting UDFs can’t be memoizable.
- Snowflake Scripting UDFs have a limit of 500 input arguments.
- You can’t [log messages](/developer-guide/logging-tracing/logging) for Snowflake Scripting UDFs.

## Examples

The following examples create and call Snowflake Scripting UDFs:

- [Create a Snowflake Scripting UDF with variables](#label-udf-sql-snowflake-scripting-example-variables)
- [Create a Snowflake Scripting UDF with conditional logic](#label-udf-sql-snowflake-scripting-example-conditional-logic)
- [Create a Snowflake Scripting UDF with a loop](#label-udf-sql-snowflake-scripting-example-loop)
- [Create a Snowflake Scripting UDF with exception handling](#label-udf-sql-snowflake-scripting-example-exception-handling)
- [Create a Snowflake Scripting UDF that returns a value for an INSERT statement](#label-udf-sql-snowflake-scripting-example-insert-values)
- [Create a Snowflake Scripting UDF called in WHERE and ORDER BY clauses](#label-udf-sql-snowflake-scripting-example-use-in-clauses)

### Create a Snowflake Scripting UDF with variables

Create a Snowflake Scripting UDF that calculates profit based on the values of two arguments:

Copy code

```
CREATE OR REPLACE FUNCTION calculate_profit(
  cost NUMBER(38, 2),
  revenue NUMBER(38, 2))
RETURNS number(38, 2)
LANGUAGE SQL
AS
DECLARE
  profit NUMBER(38, 2) DEFAULT 0.0;
BEGIN
  profit := revenue - cost;
  RETURN profit;
END;
```

Note

If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql),
the Classic Console, or the `execute_stream` or `execute_string` method in
[Python Connector](/developer-guide/python-connector/python-connector) code, this example requires minor
changes. For more information, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples).

Call `calculate_profit` in a query:

Copy code

```
SELECT calculate_profit(100, 110);
```

```
+----------------------------+
| CALCULATE_PROFIT(100, 110) |
|----------------------------|
|                      10.00 |
+----------------------------+
```

You can use the same Snowflake Scripting UDF and specify columns for the arguments. First,
create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE snowflake_scripting_udf_profit(
  cost NUMBER(38, 2),
  revenue NUMBER(38, 2));

INSERT INTO snowflake_scripting_udf_profit VALUES
  (100, 200),
  (200, 190),
  (300, 500),
  (400, 401);
```

Call `calculate_profit` in a query and specify the columns for the arguments:

Copy code

```
SELECT calculate_profit(cost, revenue)
  FROM snowflake_scripting_udf_profit;
```

```
+---------------------------------+
| CALCULATE_PROFIT(COST, REVENUE) |
|---------------------------------|
|                          100.00 |
|                          -10.00 |
|                          200.00 |
|                            1.00 |
+---------------------------------+
```

### Create a Snowflake Scripting UDF with conditional logic

Create a Snowflake Scripting UDF that uses conditional logic to determine the department name
based on an input INTEGER value:

Copy code

```
CREATE OR REPLACE function check_dept(department_id INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
BEGIN
  IF (department_id < 3) THEN
    RETURN 'Engineering';
  ELSEIF (department_id = 3) THEN
    RETURN 'Tool Design';
  ELSE
    RETURN 'Marketing';
  END IF;
END;
```

Note

If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql),
the Classic Console, or the `execute_stream` or `execute_string` method in
[Python Connector](/developer-guide/python-connector/python-connector) code, this example requires minor
changes. For more information, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples).

Call `check_dept` in a query:

Copy code

```
SELECT check_dept(2);
```

```
+---------------+
| CHECK_DEPT(2) |
|---------------|
| Engineering   |
+---------------+
```

You can use a [SQL variable](/sql-reference/session-variables) in an argument when you
call a Snowflake Scripting UDF. The following example sets a SQL variable and then uses the
variable in a call to the `check_dept` UDF:

Copy code

```
SET my_variable = 3;

SELECT check_dept($my_variable);
```

```
+--------------------------+
| CHECK_DEPT($MY_VARIABLE) |
|--------------------------|
| Tool Design              |
+--------------------------+
```

### Create a Snowflake Scripting UDF with a loop

Create a Snowflake Scripting UDF that uses a loop to count all numbers up to a target number provided
in an argument and calculate the sum of all of the numbers counted:

Copy code

```
CREATE OR REPLACE function count_to(
  target_number INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
DECLARE
  counter INTEGER DEFAULT 0;
  sum_total INTEGER DEFAULT 0;
BEGIN
  WHILE (counter < target_number) DO
    counter := counter + 1;
    sum_total := sum_total + counter;
  END WHILE;
  RETURN 'Counted to ' || counter || '. Sum of all numbers: ' || sum_total;
END;
```

Note

If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql),
the Classic Console, or the `execute_stream` or `execute_string` method in
[Python Connector](/developer-guide/python-connector/python-connector) code, this example requires minor
changes. For more information, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples).

Call `count_to` in a query:

Copy code

```
SELECT count_to(10);
```

```
+---------------------------------------+
| COUNT_TO(10)                          |
|---------------------------------------|
| Counted to 10. Sum of all numbers: 55 |
+---------------------------------------+
```

### Create a Snowflake Scripting UDF with exception handling

Create a Snowflake Scripting UDF that declares an exception and then raises the exception:

Copy code

```
CREATE OR REPLACE FUNCTION raise_exception(input_value INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
DECLARE
  counter_val INTEGER DEFAULT 0;
  my_exception EXCEPTION (-20002, 'My exception text');
BEGIN
  WHILE (counter_val < 12) DO
    counter_val := counter_val + 1;
    IF (counter_val > 10) THEN
      RAISE my_exception;
    END IF;
  END WHILE;
  RETURN counter_val;
EXCEPTION
  WHEN my_exception THEN
    IF (input_value = 1) THEN
      RETURN 'My exception caught: ' || sqlcode;
    ELSEIF (input_value = 2) THEN
      RETURN 'My exception caught with different path: ' || sqlcode;
    END IF;
    RETURN 'Default exception handling path: ' || sqlcode;
END;
```

Note

If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql),
the Classic Console, or the `execute_stream` or `execute_string` method in
[Python Connector](/developer-guide/python-connector/python-connector) code, this example requires minor
changes. For more information, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples).

Call `raise_exception` in a query and specify `1` for the input value:

Copy code

```
SELECT raise_exception(1);
```

```
+-----------------------------+
| RAISE_EXCEPTION(1)          |
|-----------------------------|
| My exception caught: -20002 |
+-----------------------------+
```

Call `raise_exception` in a query and specify `2` for the input value:

Copy code

```
SELECT raise_exception(2);
```

```
+-------------------------------------------------+
| RAISE_EXCEPTION(2)                              |
|-------------------------------------------------|
| My exception caught with different path: -20002 |
+-------------------------------------------------+t
```

Call `raise_exception` in a query and specify `NULL` for the input value:

Copy code

```
SELECT raise_exception(NULL);
```

```
+-----------------------------------------+
| RAISE_EXCEPTION(NULL)                   |
|-----------------------------------------|
| Default exception handling path: -20002 |
+-----------------------------------------+
```

### Create a Snowflake Scripting UDF that returns a value for an INSERT statement

Create a Snowflake Scripting UDF that returns a value that is used in an INSERT statement. Create the table
that the values will be inserted into:

Copy code

```
CREATE OR REPLACE TABLE test_sql_udf_insert (num NUMBER);
```

Create a SQL UDF that returns a numeric value:

Copy code

```
CREATE OR REPLACE FUNCTION value_to_insert(l NUMBER, r NUMBER)
RETURNS number
LANGUAGE SQL
AS
BEGIN
  IF (r < 0) THEN
    RETURN l/r * -1;
  ELSEIF (r > 0) THEN
    RETURN l/r;
  ELSE
    RETURN 0;
END IF;
END;
```

Note

If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql),
the Classic Console, or the `execute_stream` or `execute_string` method in
[Python Connector](/developer-guide/python-connector/python-connector) code, this example requires minor
changes. For more information, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples).

Call `value_to_insert` in multiple INSERT statements:

Copy code

```
INSERT INTO test_sql_udf_insert SELECT value_to_insert(10, 2);
INSERT INTO test_sql_udf_insert SELECT value_to_insert(10, -2);
INSERT INTO test_sql_udf_insert SELECT value_to_insert(10, 0);
```

Query the table to view the inserted values:

Copy code

```
SELECT * FROM test_sql_udf_insert;
```

```
+-----+
| NUM |
|-----|
|   5 |
|   5 |
|   0 |
+-----+
```

### Create a Snowflake Scripting UDF called in WHERE and ORDER BY clauses

Create a Snowflake Scripting UDF that returns a value that is used in a WHERE or ORDER BY clause.
Create a table and insert values:

Copy code

```
CREATE OR REPLACE TABLE test_sql_udf_clauses (p1 INT, p2 INT);

INSERT INTO test_sql_udf_clauses VALUES
  (100, 7),
  (100, 3),
  (100, 4),
  (NULL, NULL);
```

Create a SQL UDF that returns a numeric value that is the product of the multiplication
of two input values:

Copy code

```
CREATE OR REPLACE FUNCTION get_product(a INTEGER, b INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
BEGIN
  RETURN a * b;
END;
```

Note

If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql),
the Classic Console, or the `execute_stream` or `execute_string` method in
[Python Connector](/developer-guide/python-connector/python-connector) code, this example requires minor
changes. For more information, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples).

Call `get_product` in the WHERE clause of a query to return the rows
where the product is greater than `350`:

Copy code

```
SELECT *
  FROM test_sql_udf_clauses
  WHERE get_product(p1, p2) > 350;
```

```
+-----+----+
|  P1 | P2 |
|-----+----|
| 100 |  7 |
| 100 |  4 |
+-----+----+
```

Call `get_product` in the ORDER BY clause of a query to order
the results from the lowest to the highest product returned by
the UDF:

Copy code

```
SELECT *
  FROM test_sql_udf_clauses
  ORDER BY get_product(p1, p2);
```

```
+------+------+
|  P1  | P2   |
|------+------|
| 100  | 3    |
| 100  | 4    |
| 100  | 7    |
| NULL | NULL |
+------+------+
```
