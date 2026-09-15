# Virtual Columns

A virtual column contains values that are calculated from an expression rather than stored in the table. The expression can reference other columns in the same table or use deterministic system-defined functions. When the column is queried, Snowflake computes its values from the expression at query time.

Virtual columns serve a similar purpose to a derived column in a [view](/sql-reference/sql/create-view), but live on the table itself, so a single table with virtual columns can replace a table-and-view pair when you only need to expose computed values. They have no storage cost (values are computed at query time), and queries can reference them directly without going through a separate object.

## Syntax

To define a virtual column, include an `AS` clause with an expression in a [CREATE TABLE](/sql-reference/sql/create-table) or [ALTER TABLE](/sql-reference/sql/alter-table) statement:

Copy code

```
CREATE OR REPLACE TABLE <table> ( <col_name> <col_type> [ GENERATED ALWAYS ] AS ( <expr> ) [ VIRTUAL ] )

ALTER TABLE <table> ADD [ COLUMN ] <col_name> <col_type> [ GENERATED ALWAYS ] AS ( <expr> ) [ VIRTUAL ]
```

`AS ( expr )` indicates that the column is virtual and defines the expression used to compute its values. The optional `GENERATED ALWAYS` prefix and `VIRTUAL` keyword are ANSI SQL syntax that Snowflake accepts for compatibility; neither changes the column’s behavior.

The column data type is required and must be compatible with the inferred type of the expression (see ).

## Usage notes

### Allowed expressions

Virtual column expressions support literals, operators, and deterministic system-defined functions. A function is deterministic if it always returns the same result when given the same input. For example:

Valid:
:   `col1 * 2`

Valid:
:   `SUBSTR(col1, 1, 4)`

    ([SUBSTR](/sql-reference/functions/substr) is a deterministic function)

Virtual columns can also reference other virtual columns in the same table, provided those virtual columns are defined earlier in the table definition:

Valid:
:   `CREATE OR REPLACE TABLE t (c NUMBER, c1 NUMBER AS (c + 1), c2 NUMBER AS (c1 + 1));`

    (virtual columns are defined in the correct order)

Invalid:
:   `CREATE OR REPLACE TABLE t (c NUMBER, c1 NUMBER AS (c2 + 1), c2 NUMBER AS (c + 1));`

    (`c1` references `c2`, which hasn’t been defined yet)

### Prohibited expressions

The following expression types aren’t allowed in virtual column definitions:

- **Non-deterministic functions**: functions whose output can differ across calls with the same input, such as [RANDOM](/sql-reference/functions/random), [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp), [CURRENT\_DATE](/sql-reference/functions/current_date), and [UUID\_STRING](/sql-reference/functions/uuid_string).
- **Aggregate functions**: functions such as `SUM`, `AVG`, and `COUNT`. Virtual columns are evaluated per row and don’t support aggregation.
- **Window functions**: functions that use an `OVER` clause.
- **Subqueries**: nested `SELECT` statements.
- **User-defined functions (UDFs)**: including SQL, JavaScript, and external UDFs.
- **Bind variables**: positional (`?`), numeric (`:1`), or named (`:value`) bind parameters.
- **Session variables**: variables set with `SET`.
- **Positional column references**: references using `$1`, `$2`, and so on.

  Note

  The `$1` pseudo-column (`VALUE`) is permitted in external table virtual columns.
- **Default value references**: a column with a `DEFAULT` value can’t be referenced in a virtual column expression, and a virtual column can’t be assigned a default value.

For the SQL compilation errors returned when a prohibited expression is used, see [Error reference](#error-reference).

### Data type requirements

The data type declared for a virtual column must be compatible with the inferred type of the expression. Snowflake enforces the following rules:

- **Numeric types**: the declared scale must exactly match the expression scale. The declared precision must be greater than or equal to the expression precision.
- **String types**: the declared length must be greater than or equal to the inferred length. Collation must match exactly.
- **Timestamp and time types**: the declared fractional seconds precision must exactly match the expression precision.

Note

For virtual columns on external tables, Snowflake checks only that the declared base type matches the inferred expression type. Precision, scale and length aren’t enforced.

Additionally, [ALTER TABLE … MODIFY COLUMN](/sql-reference/sql/alter-table) on a base column is blocked if the change would make the base column’s type incompatible with any dependent virtual column:

Copy code

```
CREATE OR REPLACE TABLE t (i NUMBER(10,2), j NUMBER(10,2) AS (i * 2));

ALTER TABLE t MODIFY COLUMN i TYPE NUMBER(10,4);
```

For the SQL compilation errors returned for type mismatches, see [Error reference](#error-reference).

### Constraints

`NOT NULL` and `CHECK` constraints can’t be set on virtual columns. This applies to inline column definitions (`CREATE TABLE`, `ALTER TABLE ADD COLUMN`) and post-creation modifications (`ALTER TABLE MODIFY`, `ALTER TABLE ADD CONSTRAINT`). Virtual columns also can’t be assigned a `DEFAULT` value (see [Prohibited expressions](#prohibited-expressions)).

Note

`NOT NULL` is permitted on external table virtual columns.

Attempting to set either constraint returns an error:

Copy code

```
CREATE OR REPLACE TABLE t (i INT, j INT AS (i * 2) NOT NULL);
```

Copy code

```
CREATE OR REPLACE TABLE t (i INT, j INT AS (i * 2) CHECK (j > 0));
```

For the SQL compilation errors returned, see [Error reference](#error-reference).

### Column dependencies and DROP COLUMN

[ALTER TABLE … DROP COLUMN](/sql-reference/sql/alter-table) is blocked if any virtual column in the table depends on the column being dropped. This includes:

- Dropping a base column that a virtual column references.
- Dropping a virtual column that another virtual column references.

Chained dependencies are fully protected. For example, if virtual column `b` depends on virtual column `a`, dropping either `a` or any base column that `a` references is blocked.

This behavior also applies to external tables.

Attempting to drop a column that a virtual column depends on returns an error:

Copy code

```
CREATE OR REPLACE TABLE t (i INT, j INT AS (i * 2));

ALTER TABLE t DROP COLUMN i;
```

For the SQL compilation error returned, see [Error reference](#error-reference).

### Additional limitations

- Virtual columns can’t be set as the [clustering key](/user-guide/tables-micro-partitions) for a table.
- Virtual columns aren’t supported in all table types. For more information, see the documentation for the specific table type.

### Known issues

When a virtual column expression turns a `NULL` value into a non-`NULL` value, and you use that virtual column in an outer join, unmatched rows on the preserved side of the join can return a non-`NULL` value for the virtual column instead of `NULL`. This known issue occurs when the expression substitutes a default for `NULL` inputs, such as with [COALESCE](/sql-reference/functions/coalesce).

For example, if a virtual column is defined as `COALESCE(<column>, 'none')`, selecting it after a `LEFT JOIN` can return `'none'` on preserved rows that have no match on the other table, even though other columns from the unmatched table are `NULL`.

As a workaround, remove the `COALESCE` (or similar) logic from the virtual column definition and apply it where needed (in the column list or `SELECT` statement, or in a `WHERE` predicate, for example).

Copy code

```
-- t1: virtual column replaces NULL color with the string 'none'.
CREATE OR REPLACE TEMPORARY TABLE t1 (
  id            INT,
  color         STRING,
  color_dark    STRING AS (COALESCE('dark ' || color, 'none'))
);
INSERT INTO t1 (id, color) VALUES (0, null), (1, 'red'), (2, 'blue'), (3, 'green');

-- t2: preserved side of the join. Rows 1 and 3 match t1; row 5 has no match in t1.
CREATE OR REPLACE TEMPORARY TABLE t2 (
  id INT
);
INSERT INTO t2 (id) VALUES (1), (3), (5);

-- Row 5 can incorrectly return 'none' for color_dark instead of using the SELECT default.
SELECT t2.id, t1.color, COALESCE(t1.color_dark, 'dark none')
FROM t2
LEFT JOIN t1 ON t1.id = t2.id;

-- Workaround: virtual column only concatenates; NULL color stays NULL on t1.
CREATE OR REPLACE TEMPORARY TABLE t1 (
  id            INT,
  color         STRING,
  color_dark    STRING AS ('dark ' || color)
);
INSERT INTO t1 (id, color) VALUES (0, null), (1, 'red'), (2, 'blue'), (3, 'green');

-- Row 5: color_dark is NULL after the join, so COALESCE applies the 'dark none' default in SELECT.
SELECT t2.id, t1.color, COALESCE(t1.color_dark, 'dark none')
FROM t2
LEFT JOIN t1 ON t1.id = t2.id;
```

### Error reference

The following table lists the SQL compilation errors that can be returned for operations on virtual columns:

| Error code | Cause | Example | Error message |
| --- | --- | --- | --- |
| 001482 | Declared virtual column type is incompatible with the inferred expression type | `CREATE OR REPLACE TABLE t (i NUMBER(10,2), j NUMBER(5,0) AS (i));` | `Data type of virtual column does not match the data type of its expression for column 'J'. Expected data type 'NUMBER(5,0)', found 'NUMBER(10,2)'.` |
| 011201 | Non-deterministic, aggregate, or window function in a virtual column expression | `CREATE OR REPLACE TABLE t (i INT, j INT AS (RANDOM()));` | `Invalid usage of non-deterministic RANDOM function in J virtual column definition.` |
| 011202 | Subquery in a virtual column expression | `CREATE OR REPLACE TABLE t (i INT, j INT AS ((SELECT 1)));` | `Invalid usage of subquery in J virtual column definition.` |
| 011203 | Bind variable in a virtual column expression | `CREATE OR REPLACE TABLE t (i INT, j INT AS (?));` | `Invalid usage of bind variable in J virtual column definition.` |
| 011204 | Session variable in a virtual column expression | `CREATE OR REPLACE TABLE t (i INT, j INT AS ($myvar));` | `Invalid usage of session variable in J virtual column definition.` |
| 011205 | Positional column reference in a virtual column expression | `CREATE OR REPLACE TABLE t (i INT, j INT AS ($1));` | `Invalid usage of column positional reference in J virtual column definition.` |
| 011206 | ALTER TABLE MODIFY COLUMN on a base column would make it incompatible with a dependent virtual column | `ALTER TABLE t MODIFY COLUMN i TYPE NUMBER(10,4);` (when `j` depends on `i`) | `Cannot change column I datatype. The dependent J virtual column has datatype NUMBER(10,2), which is incompatible with the new expression datatype NUMBER(10,4).` |
| 011207 | NOT NULL or CHECK constraint set on a virtual column | `CREATE OR REPLACE TABLE t (i INT, j INT AS (i * 2) NOT NULL);` | `Cannot set NOT NULL constraint on virtual column J.` |
| 011208 | DROP COLUMN on a column that a virtual column depends on | `ALTER TABLE t DROP COLUMN i;` (when `j` depends on `i`) | `Cannot drop column 'I' because virtual column J depends on it.` |

Expand

Show lessSee more

## Identifying virtual columns

In the output of the [DESC TABLE](/sql-reference/sql/desc-table) command, the `KIND` column identifies whether a column is a standard or virtual column. The `EXPRESSION` column shows the virtual column definition:

Copy code

```
CREATE OR REPLACE TABLE x (i INT, j INT AS (i * i));

DESC TABLE x;

+------+--------------+---------+-------+---------+-------------+------------+-------+------------+---------+
| name | type         | kind    | null? | default | primary key | unique key | check | expression | comment |
|------+--------------+---------+-------+---------+-------------+------------+-------+------------+---------|
| I    | NUMBER(38,0) | COLUMN  | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    |
| J    | NUMBER(38,0) | VIRTUAL | Y     | NULL    | N           | N          | NULL  | I * I      | NULL    |
+------+--------------+---------+-------+---------+-------------+------------+-------+------------+---------+
```

You can also use the [SHOW COLUMNS](/sql-reference/sql/show-columns) command to retrieve column metadata for a table, including whether each column is virtual. The `kind` column shows `VIRTUAL_COLUMN` for virtual columns, and the `expression` column shows the virtual column definition:

Copy code

```
CREATE OR REPLACE TABLE x (i INT, j INT AS (i * i));

SHOW COLUMNS IN TABLE x;

+------------+-------------+-------------+-----------------------------------------------+-----------------+-------+---------+----------------+------------+---------+
| table_name | schema_name | column_name | data_type                                     | database_name   | null? | default | kind           | expression | comment |
|------------+-------------+-------------+-----------------------------------------------+-----------------+-------+---------+----------------+------------+---------|
| X          | PUBLIC      | I           | {"type":"FIXED","precision":38,"scale":0,...} | <your_database> | true  |         | COLUMN         |            |         |
| X          | PUBLIC      | J           | {"type":"FIXED","precision":38,"scale":0,...} | <your_database> | true  |         | VIRTUAL_COLUMN | I * I      |         |
+------------+-------------+-------------+-----------------------------------------------+-----------------+-------+---------+----------------+------------+---------+
```

You can also query the [INFORMATION\_SCHEMA.COLUMNS](/sql-reference/info-schema/columns) view, which lets you filter directly for virtual columns by using the `KIND` column:

Copy code

```
SELECT TABLE_NAME, TABLE_SCHEMA, COLUMN_NAME, DATA_TYPE, EXPRESSION, KIND
  FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_NAME = 'X'
    AND KIND = 'VIRTUAL_COLUMN';

+------------+--------------+-------------+-----------+------------+----------------+
| TABLE_NAME | TABLE_SCHEMA | COLUMN_NAME | DATA_TYPE | EXPRESSION | KIND           |
|------------+--------------+-------------+-----------+------------+----------------|
| X          | PUBLIC       | J           | NUMBER    | I * I      | VIRTUAL_COLUMN |
+------------+--------------+-------------+-----------+------------+----------------+
```

## Examples

The following example creates a table with a virtual column `j` that squares the values in column `i`:

Copy code

```
CREATE OR REPLACE TABLE x (i INT, j INT AS (i * i));

INSERT INTO x VALUES (2);

SELECT * FROM x;

+---+---+
| I | J |
|---+---|
| 2 | 4 |
+---+---+
```

The following example creates a table with a virtual column `tax` defined inline in a CTAS statement. Because virtual columns are excluded from the column count, the SELECT clause only needs to provide values for the non-virtual columns (`vendor_name`, `vendor_city`, and `cost`):

Copy code

```
-- Create base tables
CREATE OR REPLACE TABLE vendors (
  id    INT,
  name  VARCHAR(255) DEFAULT NULL,
  phone VARCHAR(100) DEFAULT NULL,
  city  VARCHAR(255),
  zip   VARCHAR(10)  DEFAULT NULL
);

INSERT INTO vendors (id, name, phone, city, zip)
VALUES
  (1, 'Acme Corporation',    '1-619-437-8889', 'San Diego',     '22434'),
  (2, 'Soylent Corporation', '1-650-249-5198', 'San Francisco', '94115'),
  (3, 'Initech',             '1-323-859-3954', 'Los Angeles',   '90001');

CREATE OR REPLACE TABLE sales (
  vendor_id  INT,
  order_date DATE,
  cost       NUMBER
);

INSERT INTO sales (vendor_id, order_date, cost)
VALUES
  (3, CURRENT_DATE(),  45.50),
  (2, CURRENT_DATE() - INTERVAL '1 day', 132.00),
  (1, CURRENT_DATE() - INTERVAL '2 days', 115.75),
  (3, CURRENT_DATE(), 205.00);

-- Create table using CTAS
CREATE OR REPLACE TABLE today_sales (
  vendor_name VARCHAR(255),
  vendor_city VARCHAR(255),
  cost        NUMBER(16,3),
  tax         NUMBER(16,3) AS ((cost * 0.075)::NUMBER(16,3))
)
AS SELECT a.name, a.city, b.cost
   FROM vendors a LEFT JOIN sales b ON a.id = b.vendor_id
   WHERE order_date = CURRENT_DATE();

SELECT * FROM today_sales;

+--------------------+---------------+----------+--------+
| VENDOR_NAME        | VENDOR_CITY   |     COST |    TAX |
|--------------------+---------------+----------+--------|
| Initech            | Los Angeles   |   46.000 |  3.450 |
+--------------------+---------------+----------+--------+
| Initech            | Los Angeles   |  205.000 | 15.375 |
+--------------------+---------------+----------+--------+
```
