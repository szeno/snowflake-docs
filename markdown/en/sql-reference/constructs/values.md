Categories:
:   [Query syntax](/sql-reference/constructs)

# VALUES

In the SELECT statement, the VALUES subclause of the FROM clause lets you
specify a set of constants to form a finite set of rows.

For information about the VALUES clause in the INSERT statement, see
the documentation for the [INSERT](/sql-reference/sql/insert) statement.

## Syntax

Copy code

```
SELECT ...
FROM ( VALUES ( <expr> [ , <expr> [ , ... ] ] ) [ , ( ... ) ] )
  [ [ AS ] <table_alias> [ ( <column_alias> [ , ... ] ) ] ]
[ ... ]
```

## Parameters

`expr`
:   Each expression must be a constant, or an expression that can be evaluated as a constant during compilation of the
    SQL statement.

    Most simple arithmetic expressions and string functions can be evaluated at compile time, but most other expressions
    can’t.

`table_alias`
:   An optional alias to give the set of rows a name, as though the set of rows were a table.

`column_alias`
:   Optional column aliases can specify the columns names.

## Usage notes

- Inside a [FROM](/sql-reference/constructs/from) clause, a VALUES clause can’t contain the `DEFAULT` keyword. This limitation is in contrast
  to a VALUES clause in an [INSERT](/sql-reference/sql/insert) statement, which supports the use
  of `DEFAULT`; for example, `INSERT INTO table VALUES (10, DEFAULT, 'Name') ...`.
- When a VALUES clause includes multiple values of different data types for the same column, Snowflake determines a
  common data type that can encompass all values and implicitly converts each value to that common type. This conversion
  can produce unexpected results or errors if you aren’t aware of it.

  To avoid unexpected coercion, explicitly CAST each value to the desired type, separate the values into multiple SQL
  statements, or ensure that all values in a column share the same type.

  **Numeric example**

  When numeric values in the same column differ significantly in scale or precision, Snowflake might return an
  `out of range` error because a value doesn’t fit in the determined common numeric type.

  Copy code

  ```
  SELECT column1 FROM VALUES
    (3.469446951953614e-18),
    (115898.73);
  ```

  ```
  100039 (22003): Numeric value '115898.73' is out of range
  ```

  For numeric values specifically, you can also specify values as text strings in quotation marks and then convert them
  to numeric values as needed.

  **Timestamp example**

  When timestamp values of different types appear in the same column, Snowflake converts all values to a common
  timestamp type. In the following example, a TIMESTAMP\_NTZ value is coerced to TIMESTAMP\_LTZ:

  Copy code

  ```
  SELECT $1 AS a, SYSTEM$TYPEOF(a) FROM VALUES
    (TO_TIMESTAMP_LTZ('2025-03-24 01:37:00 -0700')),
    (TO_TIMESTAMP_NTZ('2025-03-24 08:37:00'));
  ```

  ```
  +-------------------------------+------------------+
  | A                             | SYSTEM$TYPEOF(A) |
  |-------------------------------+------------------|
  | 2025-03-24 01:37:00.000 -0700 | TIMESTAMP_LTZ(9) |
  | 2025-03-24 08:37:00.000 -0700 | TIMESTAMP_LTZ(9) |
  +-------------------------------+------------------+
  ```
- The VALUES clause is limited to 200,000 rows.

## Examples

The following examples use the VALUES clause to generate a fixed, known set of rows:

Copy code

```
SELECT * FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three'));
```

```
+---------+---------+
| COLUMN1 | COLUMN2 |
|---------+---------|
|       1 | one     |
|       2 | two     |
|       3 | three   |
+---------+---------+
```

You can reference values either by column name (implicit) or column position. The following
example references the second column by column position:

Copy code

```
SELECT column1, $2 FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three'));
```

```
+---------+-------+
| COLUMN1 | $2    |
|---------+-------|
|       1 | one   |
|       2 | two   |
|       3 | three |
+---------+-------+
```

The following example distinguishes multiple VALUES clauses by using aliases:

Copy code

```
SELECT v1.$2, v2.$2
  FROM (VALUES (1, 'one'), (2, 'two')) AS v1
        INNER JOIN (VALUES (1, 'One'), (3, 'three')) AS v2
  WHERE v2.$1 = v1.$1;
```

You can also specify aliases for the column names, as shown in the following example:

Copy code

```
SELECT c1, c2
  FROM (VALUES (1, 'one'), (2, 'two')) AS v1 (c1, c2);
```
