# Logical operators

Logical operators return the result of a particular Boolean operation on one or two input expressions. Logical operators are also
referred to as Boolean operators.

Logical operators can only be used as a predicate (for example, in the [WHERE](/sql-reference/constructs/where) clause). Input expressions must be predicates.

See also:
:   [BOOLAND](/sql-reference/functions/booland) , [BOOLNOT](/sql-reference/functions/boolnot) , [BOOLOR](/sql-reference/functions/boolor) , [BOOLXOR](/sql-reference/functions/boolxor)

## List of logical operators

| Operator | Syntax example | Description |
| --- | --- | --- |
| `AND` | `a AND b` | Matches both expressions (`a` and `b`). |
| `NOT` | `NOT a` | Doesn’t match the expression. |
| `OR` | `a OR b` | Matches either expression. |

Expand

Show lessSee more

The order of precedence of these operators is shown below (from highest to
lowest):

- NOT
- AND
- OR

## Examples

The following examples use logical operators:

- [Use logical operators in queries on table data](#label-operators-logical-examples-table-data)
- [Use logical operators in queries on Boolean values](#label-operators-logical-examples-boolean-values)
- [Show “truth tables” for the logical operators](#label-operators-logical-examples-truth-tables)

### Use logical operators in queries on table data

Create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE logical_test1 (id INT, a INT, b VARCHAR);

INSERT INTO logical_test1 (id, a, b) VALUES (1, 8, 'Up');
INSERT INTO logical_test1 (id, a, b) VALUES (2, 25, 'Down');
INSERT INTO logical_test1 (id, a, b) VALUES (3, 15, 'Down');
INSERT INTO logical_test1 (id, a, b) VALUES (4, 47, 'Up');

SELECT * FROM logical_test1;
```

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  1 |  8 | Up   |
|  2 | 25 | Down |
|  3 | 15 | Down |
|  4 | 47 | Up   |
+----+----+------+
```

#### Execute queries that use a single logical operator

Use a single logical operator in the WHERE clause of various queries:

Copy code

```
SELECT *
  FROM logical_test1
  WHERE a > 20 AND
        b = 'Down';
```

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  2 | 25 | Down |
+----+----+------+
```

Copy code

```
SELECT *
  FROM logical_test1
  WHERE a > 20 OR
        b = 'Down';
```

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  2 | 25 | Down |
|  3 | 15 | Down |
|  4 | 47 | Up   |
+----+----+------+
```

Copy code

```
SELECT *
  FROM logical_test1
  WHERE a > 20 OR
        b = 'Up';
```

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  1 |  8 | Up   |
|  2 | 25 | Down |
|  4 | 47 | Up   |
+----+----+------+
```

Copy code

```
SELECT *
  FROM logical_test1
  WHERE NOT a > 20;
```

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  1 |  8 | Up   |
|  3 | 15 | Down |
+----+----+------+
```

#### Show the precedence of logical operators

The following examples show the precedence of the logical operators.

The first example shows that the precedence of AND is higher than the
precedence of OR. The query returns the rows that match these conditions:

- `b` equals `Down`.

OR

- `a` equals `8` AND `b` equals `Up`.

Copy code

```
SELECT *
  FROM logical_test1
  WHERE b = 'Down' OR
        a = 8 AND b = 'Up';
```

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  1 |  8 | Up   |
|  2 | 25 | Down |
|  3 | 15 | Down |
+----+----+------+
```

You can use parentheses in the WHERE clause to change the precedence. For example,
the following query returns the rows that match these conditions:

- `b` equals `Down` OR `a` equals `8`.

AND

- `b` equals `Up`.

Copy code

```
SELECT *
  FROM logical_test1
  WHERE (b = 'Down' OR a = 8) AND b = 'Up';
```

```
+----+---+----+
| ID | A | B  |
|----+---+----|
|  1 | 8 | Up |
+----+---+----+
```

The next example shows that the precedence of NOT is higher than the precedence of AND. For example,
the following query returns the rows that match these conditions:

- `a` does NOT equal *15*.

AND

- `b` equals `Down`.

Copy code

```
SELECT *
  FROM logical_test1
  WHERE NOT a = 15 AND b = 'Down';
```

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  2 | 25 | Down |
+----+----+------+
```

You can use parentheses in the WHERE clause to change the precedence. For example,
the following query returns the rows that do NOT match both of these conditions:

- `a` equals *15*.

AND

- `b` equals `Down`.

Copy code

```
SELECT *
  FROM logical_test1
  WHERE NOT (a = 15 AND b = 'Down');
```

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  1 |  8 | Up   |
|  2 | 25 | Down |
|  4 | 47 | Up   |
+----+----+------+
```

### Use logical operators in queries on Boolean values

Create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE logical_test2 (a BOOLEAN, b BOOLEAN);

INSERT INTO logical_test2 VALUES (0, 1);

SELECT * FROM logical_test2;
```

```
+-------+------+
| A     | B    |
|-------+------|
| False | True |
+-------+------+
```

The following query uses the OR operator to return rows where either `a` or `b`
is TRUE:

Copy code

```
SELECT a, b FROM logical_test2 WHERE a OR b;
```

```
+-------+------+
| A     | B    |
|-------+------|
| False | True |
+-------+------+
```

The following query uses the AND operator to return rows where both `a` and `b`
are both TRUE:

Copy code

```
SELECT a, b FROM logical_test2 WHERE a AND b;
```

```
+---+---+
| A | B |
|---+---|
+---+---+
```

The following query uses the AND operator and the NOT operator to return rows where
`b` is TRUE and `a` is FALSE:

Copy code

```
SELECT a, b FROM logical_test2 WHERE b AND NOT a;
```

```
+-------+------+
| A     | B    |
|-------+------|
| False | True |
+-------+------+
```

The following query uses the AND operator and the NOT operator to return rows where
`a` is TRUE and `b` is FALSE:

Copy code

```
SELECT a, b FROM logical_test2 WHERE a AND NOT b;
```

```
+---+---+
| A | B |
|---+---|
+---+---+
```

### Show “truth tables” for the logical operators

The next few examples show “truth tables” for the logical operators on a Boolean column. For more information about the
behavior of Boolean values in Snowflake, see [Ternary logic](/sql-reference/ternary-logic).

Create a new table and data:

Copy code

```
CREATE OR REPLACE TABLE logical_test3 (x BOOLEAN);

INSERT INTO logical_test3 (x) VALUES
  (False),
  (True),
  (NULL);
```

This shows the truth table for the OR operator:

Copy code

```
SELECT x AS "OR",
       x OR False AS "FALSE",
       x OR True AS "TRUE",
       x OR NULL AS "NULL"
  FROM logical_test3;
```

```
+-------+-------+------+------+
| OR    | FALSE | TRUE | NULL |
|-------+-------+------+------|
| False | False | True | NULL |
| True  | True  | True | True |
| NULL  | NULL  | True | NULL |
+-------+-------+------+------+
```

This shows the truth table for the AND operator:

Copy code

```
SELECT x AS "AND",
       x AND False AS "FALSE",
       x AND True AS "TRUE",
       x AND NULL AS "NULL"
  FROM logical_test3;
```

```
+-------+-------+-------+-------+
| AND   | FALSE | TRUE  | NULL  |
|-------+-------+-------+-------|
| False | False | False | False |
| True  | False | True  | NULL  |
| NULL  | False | NULL  | NULL  |
+-------+-------+-------+-------+
```
