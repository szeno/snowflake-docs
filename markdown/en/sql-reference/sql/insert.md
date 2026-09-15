# INSERT

Updates a table by inserting one or more rows into the table. The values inserted into each column in the table can be explicitly-specified
or the results of a query.

See also:
:   [INSERT (multi-table)](/sql-reference/sql/insert-multi-table)

## Syntax

Copy code

```
INSERT [ OVERWRITE ] INTO <target_table> [ ( <target_col_name> [ , ... ] ) ]
       {
           VALUES ( { <value> | DEFAULT | NULL } [ , ... ] ) [ , ( ... ) ]
         | <query>
       }
```

## Required parameters

`target_table`
:   Specifies the target table into which to insert rows.

`VALUES ( value | DEFAULT | NULL [ , ... ] ) [ , ( ... ) ]`
:   Specifies one or more values to insert into the corresponding columns in the target table.

    In a `VALUES` clause, you can specify the following:

    - `value`: Inserts the explicitly-specified value. The value can be a literal or an expression
      that evaluates to a single value.
    - `DEFAULT`: Inserts the default value for the corresponding column in the target table.
    - `NULL`: Inserts a `NULL` value.

    Each value in the clause must be separated by a comma.

    You can insert multiple rows by specifying additional sets of values in the clause. For more information, see the
    [Usage notes](#label-insert-command-usage-notes) and the [Examples](#label-insert-command-examples).

`query`
:   Specify a [query](/sql-reference/constructs) statement that returns values to be inserted into the corresponding
    columns. This allows you to insert rows into a target table from one or more source tables.

## Optional parameters

`OVERWRITE`
:   Specifies that the target table should be truncated before inserting the values into the table. Note that specifying this option does
    not affect the access control privileges on the table.

    INSERT statements with `OVERWRITE` can be processed within the scope of the current transaction, which avoids DDL statements that
    commit a transaction, such as:

    > Copy code
    >
    > ```
    > DROP TABLE t;
    > CREATE TABLE t AS SELECT * FROM ... ;
    > ```

    Default: No value (the target table is not truncated before performing the inserts).

`( target_col_name [ , ... ] )`
:   Specifies one or more columns in the target table into which the corresponding values are inserted. The number of target columns specified
    must match the number of specified values or columns (if the values are the results of a query) in the `VALUES` clause.

    Default: No value (all the columns in the target table are updated).

## Usage notes

- Using a single INSERT command, you can insert multiple rows into a table by specifying additional sets of values separated by commas in
  the VALUES clause.

  For example, the following clause would insert 3 rows in a 3-column table, with values `1`, `2`, and `3` in the first two rows and
  values `2`, `3`, and `4` in the third row:

  Copy code

  ```
  VALUES ( 1, 2, 3 ) ,
      ( 1, 2, 3 ) ,
      ( 2, 3, 4 )
  ```
- To use the OVERWRITE option on INSERT, you must use a role that has DELETE privilege on the table because OVERWRITE will delete the
  existing records in the table.
- Some types of expressions can’t be specified in the VALUES clause, including the following expressions:

  - Subqueries

    For example:

    Copy code

    ```
    ... VALUES (SELECT id FROM other_table)
    ```
  - Values of the [semi-structured](/sql-reference/data-types-semistructured) or
    [structured](/sql-reference/data-types-structured) data type.

    For example:

    Copy code

    ```
    ... VALUES (ARRAY_CONSTRUCT(1, 2, 3))
    ```
  - [Window functions](/sql-reference/functions-window)

    For example:

    Copy code

    ```
    ... VALUES (ROW_NUMBER() OVER (...))
    ```
  - [Aggregate functions](/sql-reference/functions-aggregation)

    For example:

    Copy code

    ```
    ... VALUES (SUM(x))
    ```

  As an alternative to the VALUES clause, specify the expression in a `query` clause. For example, you
  can replace the following expression:

  Copy code

  ```
  INSERT INTO table1 (ID, varchar1, variant1)
   VALUES (4, 'Fourier', PARSE_JSON('{ "key1": "value1", "key2": "value2" }'));
  ```

  with this expression:

  Copy code

  ```
  INSERT INTO table1 (ID, varchar1, variant1)
   SELECT 4, 'Fourier', PARSE_JSON('{ "key1": "value1", "key2": "value2" }');
  ```
- The VALUES clause is limited to 200,000 rows. This limit applies to a single INSERT INTO … VALUES
  statement and a single INSERT INTO … SELECT … FROM VALUES statement. Consider using the
  [COPY INTO <table>](/sql-reference/sql/copy-into-table) command to perform a bulk data load. For more information
  about using the VALUES clause in a SELECT statement, see [VALUES](/sql-reference/constructs/values).
- For information about inserting data into hybrid tables, see [Loading data](/user-guide/tables-hybrid-create#label-create-loading-data).

## Examples

The following examples use the INSERT command.

### Single row insert using a query

Convert three string values to dates or timestamps and insert them into a single row in the `mytable` table:

Copy code

```
CREATE OR REPLACE TABLE mytable (
  col1 DATE,
  col2 TIMESTAMP_NTZ,
  col3 TIMESTAMP_NTZ);

DESC TABLE mytable;
```

```
+------+------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
| name | type             | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
|------+------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
| COL1 | DATE             | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| COL2 | TIMESTAMP_NTZ(9) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| COL3 | TIMESTAMP_NTZ(9) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
+------+------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
```

Copy code

```
INSERT INTO mytable
  SELECT
    TO_DATE('2013-05-08T23:39:20.123'),
    TO_TIMESTAMP('2013-05-08T23:39:20.123'),
    TO_TIMESTAMP('2013-05-08T23:39:20.123');

SELECT * FROM mytable;
```

```
+------------+-------------------------+-------------------------+
| COL1       | COL2                    | COL3                    |
|------------+-------------------------+-------------------------|
| 2013-05-08 | 2013-05-08 23:39:20.123 | 2013-05-08 23:39:20.123 |
+------------+-------------------------+-------------------------+
```

Similar to previous example, but specify to update only the first and third columns in the table:

Copy code

```
INSERT INTO mytable (col1, col3)
  SELECT
    TO_DATE('2013-05-08T23:39:20.123'),
    TO_TIMESTAMP('2013-05-08T23:39:20.123');

SELECT * FROM mytable;
```

```
+------------+-------------------------+-------------------------+
| COL1       | COL2                    | COL3                    |
|------------+-------------------------+-------------------------|
| 2013-05-08 | 2013-05-08 23:39:20.123 | 2013-05-08 23:39:20.123 |
| 2013-05-08 | NULL                    | 2013-05-08 23:39:20.123 |
+------------+-------------------------+-------------------------+
```

### Multi-row insert using explicitly-specified values

Create the `employees` table and insert four rows of data into it by providing sets of values in a
comma-separated list in the VALUES clause:

Copy code

```
CREATE TABLE employees (
  first_name VARCHAR,
  last_name VARCHAR,
  workphone VARCHAR,
  city VARCHAR,
  postal_code VARCHAR);

INSERT INTO employees
  VALUES
    ('May', 'Franklin', '1-650-249-5198', 'San Francisco', 94115),
    ('Gillian', 'Patterson', '1-650-859-3954', 'San Francisco', 94115),
    ('Lysandra', 'Reeves', '1-212-759-3751', 'New York', 10018),
    ('Michael', 'Arnett', '1-650-230-8467', 'San Francisco', 94116);

SELECT * FROM employees;
```

```
+------------+-----------+----------------+---------------+-------------+
| FIRST_NAME | LAST_NAME | WORKPHONE      | CITY          | POSTAL_CODE |
|------------+-----------+----------------+---------------+-------------|
| May        | Franklin  | 1-650-249-5198 | San Francisco | 94115       |
| Gillian    | Patterson | 1-650-859-3954 | San Francisco | 94115       |
| Lysandra   | Reeves    | 1-212-759-3751 | New York      | 10018       |
| Michael    | Arnett    | 1-650-230-8467 | San Francisco | 94116       |
+------------+-----------+----------------+---------------+-------------+
```

In multi-row inserts, make sure that the data types of the inserted values are consistent across the rows because the data type of the
first row is used as a guide. Create a table and insert two rows:

Copy code

```
CREATE OR REPLACE TABLE demo_insert_type_mismatch (v VARCHAR);
```

The first insert works as expected:

Copy code

```
INSERT INTO demo_insert_type_mismatch (v) VALUES
  ('three'),
  ('four');
```

```
+-------------------------+
| number of rows inserted |
|-------------------------|
|                       2 |
+-------------------------+
```

The second insert fails because the data type of the value in the second row (`'d'`) is a string, which is
different from the numeric data type of the value in the first row (`3`). The insert fails even though both values
can be [coerced](/sql-reference/data-type-conversion) to VARCHAR, which is the data type of the column in
the table. The insert fails even though the data type of the value `'d'` is the same as the data type of column `v`:

Copy code

```
INSERT INTO demo_insert_type_mismatch (v) VALUES
  (3),
  ('d');
```

```
100038 (22018): DML operation to table DEMO_INSERT_TYPE_MISMATCH failed on column V with error: Numeric value 'd' is not recognized
```

When the data types are consistent across the rows, the insert succeeds, and both numeric values are coerced to the VARCHAR data type:

Copy code

```
INSERT INTO demo_insert_type_mismatch (v) VALUES
  (3),
  (4);
```

```
+-------------------------+
| number of rows inserted |
|-------------------------|
|                       2 |
+-------------------------+
```

### Multi-row insert using query

Insert multiple rows of data from the `contractors` table into the `employees` table:

- Select only those rows where the `worknum` column contains area code `650`.
- Insert a NULL value in the `city` column.

Copy code

```
SELECT * FROM employees;
```

```
+------------+-----------+----------------+---------------+-------------+
| FIRST_NAME | LAST_NAME | WORKPHONE      | CITY          | POSTAL_CODE |
|------------+-----------+----------------+---------------+-------------|
| May        | Franklin  | 1-650-249-5198 | San Francisco | 94115       |
| Gillian    | Patterson | 1-650-859-3954 | San Francisco | 94115       |
| Lysandra   | Reeves    | 1-212-759-3751 | New York      | 10018       |
| Michael    | Arnett    | 1-650-230-8467 | San Francisco | 94116       |
+------------+-----------+----------------+---------------+-------------+
```

Copy code

```
CREATE TABLE contractors (
  contractor_first VARCHAR,
  contractor_last VARCHAR,
  worknum VARCHAR,
  city VARCHAR,
  zip_code VARCHAR);

INSERT INTO contractors
  VALUES
    ('Bradley', 'Greenbloom', '1-650-445-0676', 'San Francisco', 94110),
    ('Cole', 'Simpson', '1-212-285-8904', 'New York', 10001),
    ('Laurel', 'Slater', '1-650-633-4495', 'San Francisco', 94115);

SELECT * FROM contractors;
```

```
+------------------+-----------------+----------------+---------------+----------+
| CONTRACTOR_FIRST | CONTRACTOR_LAST | WORKNUM        | CITY          | ZIP_CODE |
|------------------+-----------------+----------------+---------------+----------|
| Bradley          | Greenbloom      | 1-650-445-0676 | San Francisco | 94110    |
| Cole             | Simpson         | 1-212-285-8904 | New York      | 10001    |
| Laurel           | Slater          | 1-650-633-4495 | San Francisco | 94115    |
+------------------+-----------------+----------------+---------------+----------+
```

Copy code

```
INSERT INTO employees(first_name, last_name, workphone, city, postal_code)
  SELECT contractor_first, contractor_last, worknum, NULL, zip_code
    FROM contractors
    WHERE CONTAINS(worknum,'650');

SELECT * FROM employees;
```

```
+------------+------------+----------------+---------------+-------------+
| FIRST_NAME | LAST_NAME  | WORKPHONE      | CITY          | POSTAL_CODE |
|------------+------------+----------------+---------------+-------------|
| May        | Franklin   | 1-650-249-5198 | San Francisco | 94115       |
| Gillian    | Patterson  | 1-650-859-3954 | San Francisco | 94115       |
| Lysandra   | Reeves     | 1-212-759-3751 | New York      | 10018       |
| Michael    | Arnett     | 1-650-230-8467 | San Francisco | 94116       |
| Bradley    | Greenbloom | 1-650-445-0676 | NULL          | 94110       |
| Laurel     | Slater     | 1-650-633-4495 | NULL          | 94115       |
+------------+------------+----------------+---------------+-------------+
```

Insert multiple rows of data from the `contractors` table into the `employees` table using a common table expression:

Copy code

```
INSERT INTO employees (first_name, last_name, workphone, city, postal_code)
  WITH cte AS
    (SELECT contractor_first AS first_name,
            contractor_last AS last_name,
            worknum AS workphone,
            city,
            zip_code AS postal_code
       FROM contractors)
  SELECT first_name, last_name, workphone, city, postal_code
    FROM cte;
```

Insert columns from two tables (`emp_addr`, `emp_ph`) into a third table (`emp`) using an INNER JOIN on the `id`
column in the source tables:

Copy code

```
INSERT INTO emp (id, first_name, last_name, city, postal_code, ph)
  SELECT a.id, a.first_name, a.last_name, a.city, a.postal_code, b.ph
    FROM emp_addr a
    INNER JOIN emp_ph b ON a.id = b.id;
```

### Multi-row insert for JSON data

Insert two JSON objects into a VARIANT column in a table:

Copy code

```
CREATE TABLE prospects (column1 VARIANT);

INSERT INTO prospects
  SELECT PARSE_JSON(column1)
  FROM VALUES
  ('{
    "_id": "57a37f7d9e2b478c2d8a608b",
    "name": {
      "first": "Lydia",
      "last": "Williamson"
    },
    "company": "Miralinz",
    "email": "lydia.williamson@miralinz.info",
    "phone": "+1 (914) 486-2525",
    "address": "268 Havens Place, Dunbar, Rhode Island, 02801"
  }')
  , ('{
    "_id": "57a37f7d622a2b1f90698c01",
    "name": {
      "first": "Denise",
      "last": "Holloway"
    },
    "company": "DIGIGEN",
    "email": "denise.holloway@digigen.net",
    "phone": "+1 (979) 587-3021",
    "address": "441 Dover Street, Ada, New Mexico, 87105"
  }');
```

### Insert using OVERWRITE

This example uses INSERT with OVERWRITE to rebuild the `sf_employees` table from `employees` after new records were added
to the `employees` table.

Here is the initial data for both tables:

Copy code

```
SELECT * FROM employees;
```

```
+------------+-----------+----------------+---------------+-------------+
| FIRST_NAME | LAST_NAME | WORKPHONE      | CITY          | POSTAL_CODE |
|------------+-----------+----------------+---------------+-------------|
| May        | Franklin  | 1-650-111-1111 | San Francisco | 94115       |
| Gillian    | Patterson | 1-650-222-2222 | San Francisco | 94115       |
| Lysandra   | Reeves    | 1-212-222-2222 | New York      | 10018       |
| Michael    | Arnett    | 1-650-333-3333 | San Francisco | 94116       |
+------------+-----------+----------------+---------------+-------------+
```

Copy code

```
SELECT * FROM sf_employees;
```

```
+------------+-----------+----------------+---------------+-------------+
| FIRST_NAME | LAST_NAME | WORKPHONE      | CITY          | POSTAL_CODE |
|------------+-----------+----------------+---------------+-------------|
| Mary       | Smith     | 1-650-999-9999 | San Francisco | 94115       |
+------------+-----------+----------------+---------------+-------------+
```

This statement inserts rows into the `sf_employees` table using the OVERWRITE clause:

Copy code

```
INSERT OVERWRITE INTO sf_employees
  SELECT * FROM employees
  WHERE city = 'San Francisco';
```

Because the INSERT used the OVERWRITE clause, the old rows from `sf_employees` are gone:

Copy code

```
SELECT * FROM sf_employees;
```

```
+------------+-----------+----------------+---------------+-------------+
| FIRST_NAME | LAST_NAME | WORKPHONE      | CITY          | POSTAL_CODE |
|------------+-----------+----------------+---------------+-------------|
| May        | Franklin  | 1-650-111-1111 | San Francisco | 94115       |
| Gillian    | Patterson | 1-650-222-2222 | San Francisco | 94115       |
| Michael    | Arnett    | 1-650-333-3333 | San Francisco | 94116       |
+------------+-----------+----------------+---------------+-------------+
```

### Write to a v3 Apache Iceberg™ table

Note

For more information about other Iceberg v3 features that Snowflake supports, see [Apache Iceberg™ tables: Support for Apache Iceberg™ v3](/user-guide/tables-iceberg-v3-specification-support).

The following example inserts a row into an Apache Iceberg™ table that conforms to v3 of the Apache Iceberg™ table specification:

Copy code

```
INSERT INTO my_v3_iceberg_table (id, payload) VALUES (1, PARSE_JSON('{"name": "Alice", "age": 30}'));
```
