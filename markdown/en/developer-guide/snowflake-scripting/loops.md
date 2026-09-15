# Working with loops

Snowflake Scripting supports the following types of loops:

- [FOR](#label-snowscript-loop-for)
- [WHILE](#label-snowscript-loop-while)
- [REPEAT](#label-snowscript-loop-repeat)
- [LOOP](#label-snowscript-loop-loop)

This topic explains how to use each of these types of loops.

## FOR loop

A [FOR](/sql-reference/snowflake-scripting/for) loop repeats a sequence of steps for a specified number of times or for each
row in a result set. Snowflake Scripting supports the following types of FOR loops:

- [Counter-based FOR loops](#label-snowscript-loop-for-counter)
- [Cursor-based FOR loops](#label-snowscript-loop-for-cursor)
- [RESULTSET-based FOR loops](#label-snowscript-loop-for-resultset)

The next sections explain how to use these types of FOR loops.

### Counter-based FOR loops

A counter-based FOR loop executes a specified number of times.

Use the following syntax for a counter-based FOR loop:

Copy code

```
FOR <counter_variable> IN [ REVERSE ] <start> TO <end> { DO | LOOP }
  <statement>;
  [ <statement>; ... ]
END { FOR | LOOP } [ <label> ] ;
```

For example, the following FOR loop executes five times:

Copy code

```
DECLARE
  counter INTEGER DEFAULT 0;
  maximum_count INTEGER default 5;
BEGIN
  FOR i IN 1 TO maximum_count DO
    counter := counter + 1;
  END FOR;
  RETURN counter;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  counter INTEGER DEFAULT 0;
  maximum_count INTEGER default 5;
BEGIN
  FOR i IN 1 TO maximum_count DO
    counter := counter + 1;
  END FOR;
  RETURN counter;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
|               5 |
+-----------------+
```

You can include SQL statements inside Snowflake Scripting loops. For example, the following FOR loop executes an INSERT
statement five times to insert the value of the counter into a table:

Copy code

```
DECLARE
  counter INTEGER DEFAULT 0;
  maximum_count INTEGER default 5;
BEGIN
  CREATE OR REPLACE TABLE test_for_loop_insert(i INTEGER);
  FOR i IN 1 TO maximum_count DO
    INSERT INTO test_for_loop_insert VALUES (:i);
    counter := counter + 1;
  END FOR;
  RETURN counter || ' rows inserted';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  counter INTEGER DEFAULT 0;
  maximum_count INTEGER default 5;
BEGIN
  CREATE OR REPLACE TABLE test_for_loop_insert(i INTEGER);
  FOR i IN 1 TO maximum_count DO
    INSERT INTO test_for_loop_insert VALUES (:i);
    counter := counter + 1;
  END FOR;
  RETURN counter || ' rows inserted';
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
| 5 rows inserted |
+-----------------+
```

Query the table to view the inserted rows:

Copy code

```
SELECT * FROM test_for_loop_insert;
```

```
+---+
| I |
|---|
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
+---+
```

The following example uses a counter-based FOR loop to populate a date dimension table, which is a common task when setting up
a data warehouse. The loop iterates over a range of days and inserts a row for each date with computed attributes:

Copy code

```
DECLARE
  start_date DATE DEFAULT '2025-01-01';
  current_date_val DATE;
BEGIN
  CREATE OR REPLACE TABLE date_dimension (
    date_key INTEGER,
    full_date DATE,
    day_of_week VARCHAR,
    month_name VARCHAR,
    quarter INTEGER,
    year INTEGER
  );
  FOR i IN 1 TO 7 DO
    current_date_val := DATEADD('day', :i - 1, :start_date);
    INSERT INTO date_dimension
      SELECT :i, :current_date_val, DAYNAME(:current_date_val),
        MONTHNAME(:current_date_val), QUARTER(:current_date_val),
        YEAR(:current_date_val);
  END FOR;
  RETURN 'Populated date dimension with 7 rows';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  start_date DATE DEFAULT '2025-01-01';
  current_date_val DATE;
BEGIN
  CREATE OR REPLACE TABLE date_dimension (
    date_key INTEGER,
    full_date DATE,
    day_of_week VARCHAR,
    month_name VARCHAR,
    quarter INTEGER,
    year INTEGER
  );
  FOR i IN 1 TO 7 DO
    current_date_val := DATEADD('day', :i - 1, :start_date);
    INSERT INTO date_dimension
      SELECT :i, :current_date_val, DAYNAME(:current_date_val),
        MONTHNAME(:current_date_val), QUARTER(:current_date_val),
        YEAR(:current_date_val);
  END FOR;
  RETURN 'Populated date dimension with 7 rows';
END;
$$
;
```

```
+----------------------------------------+
| anonymous block                        |
|----------------------------------------|
| Populated date dimension with 7 rows   |
+----------------------------------------+
```

To verify the results, query the table:

Copy code

```
SELECT * FROM date_dimension ORDER BY date_key;
```

```
+----------+------------+-------------+------------+---------+------+
| DATE_KEY | FULL_DATE  | DAY_OF_WEEK | MONTH_NAME | QUARTER | YEAR |
|----------+------------+-------------+------------+---------+------|
|        1 | 2025-01-01 | Wed         | Jan        |       1 | 2025 |
|        2 | 2025-01-02 | Thu         | Jan        |       1 | 2025 |
|        3 | 2025-01-03 | Fri         | Jan        |       1 | 2025 |
|        4 | 2025-01-04 | Sat         | Jan        |       1 | 2025 |
|        5 | 2025-01-05 | Sun         | Jan        |       1 | 2025 |
|        6 | 2025-01-06 | Mon         | Jan        |       1 | 2025 |
|        7 | 2025-01-07 | Tue         | Jan        |       1 | 2025 |
+----------+------------+-------------+------------+---------+------+
```

For the full syntax and details about FOR loops, see [FOR (Snowflake Scripting)](/sql-reference/snowflake-scripting/for).

### Cursor-based FOR loops

A cursor-based FOR loop iterates over a result set. The number of iterations is determined by the number of
rows in the [cursor](/developer-guide/snowflake-scripting/cursors).

The syntax for a cursor-based FOR loop is:

Copy code

```
FOR <row_variable> IN <cursor_name> DO
  <statement>;
  [ <statement>; ... ]
END FOR [ <label> ] ;
```

The first example in this section uses the data in the following `invoices` table:

Copy code

```
CREATE OR REPLACE TABLE invoices (price NUMBER(12, 2));

INSERT INTO invoices (price) VALUES
  (11.11),
  (22.22);
```

The following example uses a FOR loop to iterate over the rows in a cursor for the `invoices` table:

Copy code

```
DECLARE
  total_price FLOAT;
  c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
  total_price := 0.0;
  FOR record IN c1 DO
    total_price := total_price + record.price;
  END FOR;
  RETURN total_price;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  total_price FLOAT;
  c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
  total_price := 0.0;
  FOR record IN c1 DO
    total_price := total_price + record.price;
  END FOR;
  RETURN total_price;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
|           33.33 |
+-----------------+
```

The following example uses a cursor-based FOR loop to iterate over a table of employees, give each employee a raise based on
their department, and insert an audit record for each update:

Copy code

```
CREATE OR REPLACE TABLE loop_test_employees (
  emp_id INTEGER,
  name VARCHAR,
  department VARCHAR,
  salary NUMBER(12,2));

INSERT INTO loop_test_employees VALUES
  (1, 'Alice', 'Engineering', 90000),
  (2, 'Bob', 'Sales', 70000),
  (3, 'Carol', 'Engineering', 95000),
  (4, 'Dave', 'Sales', 72000);

CREATE OR REPLACE TABLE salary_audit (
  emp_id INTEGER,
  old_salary NUMBER(12,2),
  new_salary NUMBER(12,2),
  updated_on TIMESTAMP);
```

Copy code

```
DECLARE
  rows_updated INTEGER DEFAULT 0;
  raise_pct INTEGER;
  new_salary NUMBER(12,2);
  cur_emp_id INTEGER;
  cur_salary NUMBER(12,2);
  c1 CURSOR FOR SELECT emp_id, department, salary FROM loop_test_employees;
BEGIN
  FOR record IN c1 DO
    cur_emp_id := record.emp_id;
    cur_salary := record.salary;
    IF (record.department = 'Engineering') THEN
      raise_pct := 10;
    ELSE
      raise_pct := 5;
    END IF;
    new_salary := :cur_salary * (1 + :raise_pct / 100);
    UPDATE loop_test_employees SET salary = :new_salary WHERE emp_id = :cur_emp_id;
    INSERT INTO salary_audit
      SELECT :cur_emp_id, :cur_salary, :new_salary, CURRENT_TIMESTAMP();
    rows_updated := rows_updated + 1;
  END FOR;
  RETURN rows_updated || ' employees updated';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  rows_updated INTEGER DEFAULT 0;
  raise_pct INTEGER;
  new_salary NUMBER(12,2);
  cur_emp_id INTEGER;
  cur_salary NUMBER(12,2);
  c1 CURSOR FOR SELECT emp_id, department, salary FROM loop_test_employees;
BEGIN
  FOR record IN c1 DO
    cur_emp_id := record.emp_id;
    cur_salary := record.salary;
    IF (record.department = 'Engineering') THEN
      raise_pct := 10;
    ELSE
      raise_pct := 5;
    END IF;
    new_salary := :cur_salary * (1 + :raise_pct / 100);
    UPDATE loop_test_employees SET salary = :new_salary WHERE emp_id = :cur_emp_id;
    INSERT INTO salary_audit
      SELECT :cur_emp_id, :cur_salary, :new_salary, CURRENT_TIMESTAMP();
    rows_updated := rows_updated + 1;
  END FOR;
  RETURN rows_updated || ' employees updated';
END;
$$
;
```

```
+----------------------+
| anonymous block      |
|----------------------|
| 4 employees updated  |
+----------------------+
```

To verify the updates, query the tables:

Copy code

```
SELECT emp_id, name, department, salary FROM loop_test_employees ORDER BY emp_id;
```

```
+--------+-------+-------------+-----------+
| EMP_ID | NAME  | DEPARTMENT  |    SALARY |
|--------+-------+-------------+-----------|
|      1 | Alice | Engineering |  99000.00 |
|      2 | Bob   | Sales       |  73500.00 |
|      3 | Carol | Engineering | 104500.00 |
|      4 | Dave  | Sales       |  75600.00 |
+--------+-------+-------------+-----------+
```

Copy code

```
SELECT emp_id, old_salary, new_salary FROM salary_audit ORDER BY emp_id;
```

```
+--------+------------+------------+
| EMP_ID | OLD_SALARY | NEW_SALARY |
|--------+------------+------------|
|      1 |   90000.00 |   99000.00 |
|      2 |   70000.00 |   73500.00 |
|      3 |   95000.00 |  104500.00 |
|      4 |   72000.00 |   75600.00 |
+--------+------------+------------+
```

For the full syntax and details about FOR loops, see [FOR (Snowflake Scripting)](/sql-reference/snowflake-scripting/for).

### RESULTSET-based FOR loops

A RESULTSET-based FOR loop iterates over a result set. The number of iterations is determined by the number of
rows returned by the [RESULTSET](/developer-guide/snowflake-scripting/resultsets) query.

The syntax for a RESULTSET-based FOR loop is:

Copy code

```
FOR <row_variable> IN <RESULTSET_name> DO
  <statement>;
  [ <statement>; ... ]
END FOR [ <label> ] ;
```

The first example in this section uses the data in the following `invoices` table:

Copy code

```
CREATE OR REPLACE TABLE invoices (price NUMBER(12, 2));
INSERT INTO invoices (price) VALUES
  (11.11),
  (22.22);
```

The following example uses a FOR loop to iterate over the rows in a RESULTSET for the `invoices` table:

Copy code

```
DECLARE
  total_price FLOAT;
  rs RESULTSET;
BEGIN
  total_price := 0.0;
  rs := (SELECT price FROM invoices);
  FOR record IN rs DO
    total_price := total_price + record.price;
  END FOR;
  RETURN total_price;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  total_price FLOAT;
  rs RESULTSET;
BEGIN
  total_price := 0.0;
  rs := (SELECT price FROM invoices);
  FOR record IN rs DO
    total_price := total_price + record.price;
  END FOR;
  RETURN total_price;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
|           33.33 |
+-----------------+
```

The following example uses a RESULTSET-based FOR loop to validate customer records. It checks each record for required contact
information and updates the `status` column to mark each record as verified or incomplete. This type of data-quality check
is a common step in extract, transform, and load (ETL) pipelines:

Copy code

```
CREATE OR REPLACE TABLE loop_test_customers (
  customer_id INTEGER,
  customer_name VARCHAR,
  customer_email VARCHAR,
  customer_phone VARCHAR,
  status VARCHAR DEFAULT 'pending_review');

INSERT INTO loop_test_customers (customer_id, customer_name, customer_email, customer_phone) VALUES
  (1, 'Alice Smith', 'alice@example.com', '800-555-0101'),
  (2, 'Bob Jones', NULL, '800-555-0102'),
  (3, 'Carol White', 'carol@example.com', NULL),
  (4, 'Dave Brown', NULL, NULL),
  (5, 'Eve Davis', 'eve@example.com', '800-555-0105');
```

Copy code

```
DECLARE
  rs RESULTSET;
  valid_count INTEGER DEFAULT 0;
  invalid_count INTEGER DEFAULT 0;
  cur_customer_id INTEGER;
BEGIN
  rs := (SELECT customer_id, customer_email, customer_phone FROM loop_test_customers WHERE status = 'pending_review');
  FOR record IN rs DO
    cur_customer_id := record.customer_id;
    IF (record.customer_email IS NOT NULL AND record.customer_phone IS NOT NULL) THEN
      UPDATE loop_test_customers SET status = 'verified' WHERE customer_id = :cur_customer_id;
      valid_count := valid_count + 1;
    ELSE
      UPDATE loop_test_customers SET status = 'incomplete' WHERE customer_id = :cur_customer_id;
      invalid_count := invalid_count + 1;
    END IF;
  END FOR;
  RETURN 'Verified: ' || valid_count || ', Incomplete: ' || invalid_count;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  rs RESULTSET;
  valid_count INTEGER DEFAULT 0;
  invalid_count INTEGER DEFAULT 0;
  cur_customer_id INTEGER;
BEGIN
  rs := (SELECT customer_id, customer_email, customer_phone FROM loop_test_customers WHERE status = 'pending_review');
  FOR record IN rs DO
    cur_customer_id := record.customer_id;
    IF (record.customer_email IS NOT NULL AND record.customer_phone IS NOT NULL) THEN
      UPDATE loop_test_customers SET status = 'verified' WHERE customer_id = :cur_customer_id;
      valid_count := valid_count + 1;
    ELSE
      UPDATE loop_test_customers SET status = 'incomplete' WHERE customer_id = :cur_customer_id;
      invalid_count := invalid_count + 1;
    END IF;
  END FOR;
  RETURN 'Verified: ' || valid_count || ', Incomplete: ' || invalid_count;
END;
$$
;
```

```
+-------------------------------+
| anonymous block               |
|-------------------------------|
| Verified: 2, Incomplete: 3   |
+-------------------------------+
```

To verify the changes, query the table:

Copy code

```
SELECT * FROM loop_test_customers ORDER BY customer_id;
```

```
+-------------+-----------------+-------------------+----------------+------------+
| CUSTOMER_ID | CUSTOMER_NAME   | CUSTOMER_EMAIL    | CUSTOMER_PHONE | STATUS     |
|-------------+-----------------+-------------------+----------------+------------|
|           1 | Alice Smith     | alice@example.com | 800-555-0101   | verified   |
|           2 | Bob Jones       | NULL              | 800-555-0102   | incomplete |
|           3 | Carol White     | carol@example.com | NULL           | incomplete |
|           4 | Dave Brown      | NULL              | NULL           | incomplete |
|           5 | Eve Davis       | eve@example.com   | 800-555-0105   | verified   |
+-------------+-----------------+-------------------+----------------+------------+
```

For the full syntax and details about FOR loops, see [FOR (Snowflake Scripting)](/sql-reference/snowflake-scripting/for).

## WHILE loop

A [WHILE](/sql-reference/snowflake-scripting/while) loop iterates while a condition is true. In a WHILE
loop, the condition is tested immediately before executing the body of the loop. If the condition is false before the first
iteration, then the body of the loop does not execute even once.

The syntax for a WHILE loop is:

Copy code

```
WHILE ( <condition> ) { DO | LOOP }
  <statement>;
  [ <statement>; ... ]
END { WHILE | LOOP } [ <label> ] ;
```

For example:

Copy code

```
BEGIN
  LET counter := 0;
  WHILE (counter < 5) DO
    counter := counter + 1;
  END WHILE;
  RETURN counter;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
BEGIN
  LET counter := 0;
  WHILE (counter < 5) DO
    counter := counter + 1;
  END WHILE;
  RETURN counter;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
|               5 |
+-----------------+
```

The following example uses a WHILE loop to build a daily sales summary from raw transaction data. It processes one date at
a time, aggregating the transactions for that date into a summary row and marking them as loaded. This date-by-date
summarization pattern is common in extract, transform, and load (ETL) pipelines:

Copy code

```
CREATE OR REPLACE TABLE loop_test_raw_transactions (
  txn_id INTEGER,
  amount NUMBER(12,2),
  txn_date DATE,
  loaded BOOLEAN DEFAULT FALSE);

INSERT INTO loop_test_raw_transactions (txn_id, amount, txn_date) VALUES
  (1, 150.00, '2025-03-01'),
  (2, 230.50, '2025-03-01'),
  (3, 89.99, '2025-03-01'),
  (4, 412.00, '2025-03-02'),
  (5, 55.25, '2025-03-03'),
  (6, 178.75, '2025-03-03');

CREATE OR REPLACE TABLE loop_test_daily_sales_summary (
  summary_date DATE,
  total_sales NUMBER(12,2),
  txn_count INTEGER);
```

Copy code

```
DECLARE
  next_date DATE;
BEGIN
  next_date := (SELECT MIN(txn_date) FROM loop_test_raw_transactions WHERE NOT loaded);
  WHILE (next_date IS NOT NULL) DO
    INSERT INTO loop_test_daily_sales_summary
      SELECT txn_date, SUM(amount), COUNT(*)
      FROM loop_test_raw_transactions
      WHERE txn_date = :next_date AND NOT loaded
      GROUP BY txn_date;
    UPDATE loop_test_raw_transactions SET loaded = TRUE WHERE txn_date = :next_date;
    next_date := (SELECT MIN(txn_date) FROM loop_test_raw_transactions WHERE NOT loaded);
  END WHILE;
  RETURN 'Daily summaries created for all transaction dates';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  next_date DATE;
BEGIN
  next_date := (SELECT MIN(txn_date) FROM loop_test_raw_transactions WHERE NOT loaded);
  WHILE (next_date IS NOT NULL) DO
    INSERT INTO loop_test_daily_sales_summary
      SELECT txn_date, SUM(amount), COUNT(*)
      FROM loop_test_raw_transactions
      WHERE txn_date = :next_date AND NOT loaded
      GROUP BY txn_date;
    UPDATE loop_test_raw_transactions SET loaded = TRUE WHERE txn_date = :next_date;
    next_date := (SELECT MIN(txn_date) FROM loop_test_raw_transactions WHERE NOT loaded);
  END WHILE;
  RETURN 'Daily summaries created for all transaction dates';
END;
$$
;
```

```
+----------------------------------------------------+
| anonymous block                                    |
|----------------------------------------------------|
| Daily summaries created for all transaction dates  |
+----------------------------------------------------+
```

To verify the results, query the summary table:

Copy code

```
SELECT * FROM loop_test_daily_sales_summary ORDER BY summary_date;
```

```
+--------------+-------------+-----------+
| SUMMARY_DATE | TOTAL_SALES | TXN_COUNT |
|--------------+-------------+-----------|
| 2025-03-01   |      470.49 |         3 |
| 2025-03-02   |      412.00 |         1 |
| 2025-03-03   |      234.00 |         2 |
+--------------+-------------+-----------+
```

For the full syntax and details about WHILE loops, see [WHILE (Snowflake Scripting)](/sql-reference/snowflake-scripting/while).

## REPEAT loop

A [REPEAT](/sql-reference/snowflake-scripting/repeat) loop iterates until a condition is true. In a REPEAT
loop, the condition is tested immediately after executing the body of the loop. As a result, the body of the loop always executes
at least once.

The syntax for a REPEAT loop is:

Copy code

```
REPEAT
  <statement>;
  [ <statement>; ... ]
UNTIL ( <condition> )
END REPEAT [ <label> ] ;
```

For example:

Copy code

```
BEGIN
  LET counter := 5;
  LET number_of_iterations := 0;
  REPEAT
    counter := counter - 1;
    number_of_iterations := number_of_iterations + 1;
  UNTIL (counter = 0)
  END REPEAT;
  RETURN number_of_iterations;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
BEGIN
  LET counter := 5;
  LET number_of_iterations := 0;
  REPEAT
    counter := counter - 1;
    number_of_iterations := number_of_iterations + 1;
  UNTIL (counter = 0)
  END REPEAT;
  RETURN number_of_iterations;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
|               5 |
+-----------------+
```

The following example creates a staging table and a target table with an additional `batch_id` column. It then uses a
REPEAT loop to move rows in batches from the staging table to the target table, incrementing the batch ID after each
iteration, until no rows remain in the staging table:

Copy code

```
CREATE OR REPLACE TABLE loop_test_orders_staging (
  order_id INTEGER,
  customer VARCHAR,
  amount NUMBER(12,2));

INSERT INTO loop_test_orders_staging VALUES
  (101, 'TestA Corp', 500.00),
  (102, 'TestB Corp', 1200.00),
  (103, 'TestA Corp', 300.00),
  (104, 'TestC Corp', 750.00),
  (105, 'TestB Corp', 425.00),
  (106, 'TestC Corp', 980.00);

CREATE OR REPLACE TABLE loop_test_orders_processed (
    order_id INTEGER,
    customer VARCHAR,
    amount NUMBER(12,2),
    batch_id INTEGER);
```

Copy code

```
DECLARE
  batch_size INTEGER DEFAULT 2;
  batch_id INTEGER DEFAULT 1;
  remaining INTEGER;
BEGIN
  remaining := (SELECT COUNT(*) FROM loop_test_orders_staging);
  REPEAT
    INSERT INTO loop_test_orders_processed
      SELECT order_id, customer, amount, :batch_id
      FROM loop_test_orders_staging
      ORDER BY order_id
      LIMIT :batch_size;
    DELETE FROM loop_test_orders_staging WHERE order_id IN (
      SELECT order_id
        FROM loop_test_orders_processed
        WHERE batch_id = :batch_id
    );
    batch_id := batch_id + 1;
    remaining := (SELECT COUNT(*) FROM loop_test_orders_staging);
  UNTIL (remaining = 0)
  END REPEAT;
  RETURN 'Processed all orders in ' || (batch_id - 1) || ' batches';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  batch_size INTEGER DEFAULT 2;
  batch_id INTEGER DEFAULT 1;
  remaining INTEGER;
BEGIN
  remaining := (SELECT COUNT(*) FROM loop_test_orders_staging);
  REPEAT
    INSERT INTO loop_test_orders_processed
      SELECT order_id, customer, amount, :batch_id
      FROM loop_test_orders_staging
      ORDER BY order_id
      LIMIT :batch_size;
    DELETE FROM loop_test_orders_staging WHERE order_id IN (
      SELECT order_id
        FROM loop_test_orders_processed
        WHERE batch_id = :batch_id
    );
    batch_id := batch_id + 1;
    remaining := (SELECT COUNT(*) FROM loop_test_orders_staging);
  UNTIL (remaining = 0)
  END REPEAT;
  RETURN 'Processed all orders in ' || (batch_id - 1) || ' batches';
END;
$$
;
```

```
+------------------------------------+
| anonymous block                    |
|------------------------------------|
| Processed all orders in 3 batches  |
+------------------------------------+
```

To verify the results, query the target table:

Copy code

```
SELECT * FROM loop_test_orders_processed ORDER BY batch_id, order_id;
```

```
+----------+------------+---------+----------+
| ORDER_ID | CUSTOMER   |  AMOUNT | BATCH_ID |
|----------+------------+---------+----------|
|      101 | TestA Corp |  500.00 |        1 |
|      102 | TestB Corp | 1200.00 |        1 |
|      103 | TestA Corp |  300.00 |        2 |
|      104 | TestC Corp |  750.00 |        2 |
|      105 | TestB Corp |  425.00 |        3 |
|      106 | TestC Corp |  980.00 |        3 |
+----------+------------+---------+----------+
```

For the full syntax and details about REPEAT loops, see [REPEAT (Snowflake Scripting)](/sql-reference/snowflake-scripting/repeat).

## LOOP loop

A [LOOP](/sql-reference/snowflake-scripting/loop) loop executes until a [BREAK](#label-snowscript-loop-terminate)
command is executed. A BREAK command is normally embedded inside branching logic
(e.g. [IF statements](/developer-guide/snowflake-scripting/branch#label-snowscript-branch-if) or [CASE statements](/developer-guide/snowflake-scripting/branch#label-snowscript-branch-case)).

The syntax for a LOOP statement is:

Copy code

```
LOOP
  <statement>;
  [ <statement>; ... ]
END LOOP [ <label> ] ;
```

For example:

Copy code

```
BEGIN
  LET counter := 5;
  LOOP
    IF (counter = 0) THEN
      BREAK;
    END IF;
    counter := counter - 1;
  END LOOP;
  RETURN counter;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
BEGIN
  LET counter := 5;
  LOOP
    IF (counter = 0) THEN
      BREAK;
    END IF;
    counter := counter - 1;
  END LOOP;
  RETURN counter;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
|               0 |
+-----------------+
```

The following example creates a log table with entries spanning multiple dates. It uses a LOOP to archive rows older
than a cutoff date into an archive table and delete them from the source, processing one day at a time until no
qualifying rows remain:

Copy code

```
CREATE OR REPLACE TABLE loop_test_event_log (
  event_id INTEGER,
  event_date DATE,
  event_description VARCHAR);

INSERT INTO loop_test_event_log VALUES
  (1, DATEADD('month', -3, CURRENT_DATE()), 'User login'),
  (2, DATEADD('month', -3, CURRENT_DATE()), 'File upload'),
  (3, DATEADD('month', -2, CURRENT_DATE()), 'Password change'),
  (4, DATEADD('month', -1, CURRENT_DATE()), 'User login'),
  (5, DATEADD('month', -1, CURRENT_DATE()), 'Data export');

CREATE OR REPLACE TABLE loop_test_event_log_archive (
  event_id INTEGER,
  event_date DATE,
  event_description VARCHAR,
  archived_on DATE);
```

Copy code

```
DECLARE
  cutoff_date DATE DEFAULT DATEADD('month', -1, CURRENT_DATE());
  oldest_date DATE;
  archived_total INTEGER DEFAULT 0;
  batch_count INTEGER;
BEGIN
  LOOP
    oldest_date := (SELECT MIN(event_date)
                      FROM loop_test_event_log
                      WHERE event_date < :cutoff_date);
    IF (oldest_date IS NULL) THEN
      BREAK;
    END IF;
    batch_count := (SELECT COUNT(*)
                      FROM loop_test_event_log
                      WHERE event_date = :oldest_date);
    INSERT INTO loop_test_event_log_archive
      SELECT event_id, event_date, event_description, CURRENT_DATE()
        FROM loop_test_event_log
        WHERE event_date = :oldest_date;
    DELETE FROM loop_test_event_log WHERE event_date = :oldest_date;
    archived_total := archived_total + batch_count;
  END LOOP;
  RETURN 'Archived ' || archived_total || ' events';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  cutoff_date DATE DEFAULT DATEADD('month', -1, CURRENT_DATE());
  oldest_date DATE;
  archived_total INTEGER DEFAULT 0;
  batch_count INTEGER;
BEGIN
  LOOP
    oldest_date := (SELECT MIN(event_date)
                      FROM loop_test_event_log
                      WHERE event_date < :cutoff_date);
    IF (oldest_date IS NULL) THEN
      BREAK;
    END IF;
    batch_count := (SELECT COUNT(*)
                      FROM loop_test_event_log
                      WHERE event_date = :oldest_date);
    INSERT INTO loop_test_event_log_archive
      SELECT event_id, event_date, event_description, CURRENT_DATE()
        FROM loop_test_event_log
        WHERE event_date = :oldest_date;
    DELETE FROM loop_test_event_log WHERE event_date = :oldest_date;
    archived_total := archived_total + batch_count;
  END LOOP;
  RETURN 'Archived ' || archived_total || ' events';
END;
$$
;
```

```
+---------------------+
| anonymous block     |
|---------------------|
| Archived 3 events   |
+---------------------+
```

To verify the results, query both tables:

Copy code

```
SELECT * FROM loop_test_event_log ORDER BY event_id;
```

```
+----------+------------+-------------------+
| EVENT_ID | EVENT_DATE | EVENT_DESCRIPTION |
|----------+------------+-------------------|
|        4 | 2026-02-04 | User login        |
|        5 | 2026-02-04 | Data export       |
+----------+------------+-------------------+
```

Copy code

```
SELECT event_id,
       event_date,
       event_description
  FROM loop_test_event_log_archive
  ORDER BY event_id;
```

```
+----------+------------+-------------------+
| EVENT_ID | EVENT_DATE | EVENT_DESCRIPTION |
|----------+------------+-------------------|
|        1 | 2025-12-04 | User login        |
|        2 | 2025-12-04 | File upload       |
|        3 | 2026-01-04 | Password change   |
+----------+------------+-------------------+
```

For the full syntax and details about LOOP loops, see [LOOP (Snowflake Scripting)](/sql-reference/snowflake-scripting/loop).

## Terminating a loop or iteration

In a loop construct, you can specify when the loop or an iteration of the loop must terminate early. The next sections explain
this in more detail:

- [Terminating a loop](#label-snowscript-loop-terminate)
- [Terminating an iteration without terminating the loop](#label-snowscript-loop-continue)
- [Specifying where execution should continue after termination](#label-snowscript-loop-continue-label)

### Terminating a loop

You can explicitly terminate a loop early by executing the [BREAK](/sql-reference/snowflake-scripting/break) command.
BREAK (and its synonym EXIT) immediately stops the current iteration, and skips any remaining iterations.
You can think of BREAK as jumping to the first executable statement after the end of the loop.

BREAK is required in a LOOP loop but is not necessary in WHILE, FOR, and REPEAT loops. In most cases,
if you have statements that you want to skip, you can use the standard branching constructs ([IF statements](/developer-guide/snowflake-scripting/branch#label-snowscript-branch-if) and
[CASE statements](/developer-guide/snowflake-scripting/branch#label-snowscript-branch-case)) to control which statements inside a loop are executed.

A BREAK command itself is usually inside an IF or CASE statement.

### Terminating an iteration without terminating the loop

You can use the CONTINUE (or ITERATE) command to jump to the end of an iteration of a loop, skipping the
remaining statements in the loop. The loop continues at the start of the next iteration.

Such jumps are rarely necessary. In most cases, if you have statements that you want to skip, you can use the
standard branching constructs ([IF statements](/developer-guide/snowflake-scripting/branch#label-snowscript-branch-if) and [CASE statements](/developer-guide/snowflake-scripting/branch#label-snowscript-branch-case)) to control which
statements inside a loop are executed.

A CONTINUE or ITERATE command itself is usually inside an IF or CASE statement.

### Specifying where execution should continue after termination

In a BREAK or CONTINUE command, if you need to continue execution at a specific point in the code (e.g. the outer
loop in a nested loop), specify a label that identifies the point at which execution should continue.

The following example demonstrates this in a nested loop:

Copy code

```
BEGIN
  LET inner_counter := 0;
  LET outer_counter := 0;
  LOOP
    LOOP
      IF (inner_counter < 5) THEN
        inner_counter := inner_counter + 1;
        CONTINUE OUTER;
      ELSE
        BREAK OUTER;
      END IF;
    END LOOP INNER;
    outer_counter := outer_counter + 1;
    BREAK;
  END LOOP OUTER;
  RETURN ARRAY_CONSTRUCT(outer_counter, inner_counter);
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
BEGIN
  LET inner_counter := 0;
  LET outer_counter := 0;
  LOOP
    LOOP
      IF (inner_counter < 5) THEN
        inner_counter := inner_counter + 1;
        CONTINUE OUTER;
      ELSE
        BREAK OUTER;
      END IF;
    END LOOP INNER;
    outer_counter := outer_counter + 1;
    BREAK;
  END LOOP OUTER;
  RETURN ARRAY_CONSTRUCT(outer_counter, inner_counter);
END;
$$;
```

In this example:

- There is a loop labeled INNER that is nested in a loop labeled OUTER.
- CONTINUE OUTER starts another iteration of the loop with the label OUTER.
- BREAK OUTER terminates the inner loop and transfers control to the end of the outer loop (labeled OUTER).

The output of this command is:

```
+-----------------+
| anonymous block |
|-----------------|
| [               |
|   0,            |
|   5             |
| ]               |
+-----------------+
```

As shown in the output:

- `inner_counter` is incremented up to 5. CONTINUE OUTER starts a new iteration of the outer loop, which starts a new
  iteration of the inner loop, which increments this counter up to 5. These iterations continue until the value of
  `inner_counter` equals 5 and BREAK OUTER terminates the inner loop.
- `outer_counter` is never incremented. The statement that increments this counter is never reached because BREAK OUTER
  transfers control to the end of the outer loop.
