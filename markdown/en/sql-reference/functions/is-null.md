Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# IS [ NOT ] NULL

Determines whether an expression is NULL or is not NULL.

## Syntax

Copy code

```
<expr> IS [ NOT ] NULL
```

## Returns

Returns a BOOLEAN.

- When IS NULL is specified, the value is TRUE if the expression is NULL. Otherwise, returns FALSE.
- When IS NOT NULL is specified, the value is TRUE if the expression is not NULL. Otherwise, returns FALSE.

## Examples

Create the `test_is_not_null` table and load the data:

Copy code

```
CREATE OR REPLACE TABLE test_is_not_null (id NUMBER, col1 NUMBER, col2 NUMBER);
INSERT INTO test_is_not_null (id, col1, col2) VALUES 
  (1, 0, 5), 
  (2, 0, NULL), 
  (3, NULL, 5), 
  (4, NULL, NULL);
```

Show the data in the `test_is_not_null` table:

Copy code

```
SELECT * 
  FROM test_is_not_null
  ORDER BY id;
```

```
+----+------+------+
| ID | COL1 | COL2 |
|----+------+------|
|  1 |    0 |    5 |
|  2 |    0 | NULL |
|  3 | NULL |    5 |
|  4 | NULL | NULL |
+----+------+------+
```

Use IS NOT NULL to return the rows for which the values in `col1` are not NULL:

Copy code

```
SELECT * 
  FROM test_is_not_null 
  WHERE col1 IS NOT NULL
  ORDER BY id;
```

```
+----+------+------+
| ID | COL1 | COL2 |
|----+------+------|
|  1 |    0 |    5 |
|  2 |    0 | NULL |
+----+------+------+
```

Use IS NULL to return the rows for which the values in `col2` are NULL:

Copy code

```
SELECT * 
  FROM test_is_not_null 
  WHERE col2 IS NULL
  ORDER BY id;
```

```
+----+------+------+
| ID | COL1 | COL2 |
|----+------+------|
|  2 |    0 | NULL |
|  4 | NULL | NULL |
+----+------+------+
```

Use a combination of IS NOT NULL and IS NULL to return the rows for which *either* of
the following conditions is met:

- The values in `col1` are not NULL.
- The values in `col2` are NULL.

Copy code

```
SELECT * 
  FROM test_is_not_null 
  WHERE col1 IS NOT NULL OR col2 IS NULL
  ORDER BY id;
```

```
+----+------+------+
| ID | COL1 | COL2 |
|----+------+------|
|  1 |    0 |    5 |
|  2 |    0 | NULL |
|  4 | NULL | NULL |
+----+------+------+
```

Use a combination of IS NOT NULL and IS NULL to return the rows for which *both* of
the following conditions are met:

- The values in `col1` are not NULL.
- The values in `col2` are NULL.

Copy code

```
SELECT *
  FROM test_is_not_null
  WHERE col1 IS NOT NULL AND col2 IS NULL
  ORDER BY id;
```

```
+----+------+------+
| ID | COL1 | COL2 |
|----+------+------|
|  2 |    0 | NULL |
+----+------+------+
```
