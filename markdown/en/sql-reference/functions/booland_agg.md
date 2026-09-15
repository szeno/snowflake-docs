Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Boolean) , [Window functions](/sql-reference/functions-window) , [Conditional expression functions](/sql-reference/expressions-conditional)

# BOOLAND\_AGG

Returns TRUE if all non-NULL Boolean records in a group evaluate to TRUE.

If all records in the group are NULL, or if the group is empty, the function returns NULL.

See also:
:   [BOOLAND](/sql-reference/functions/booland) , [BOOLOR\_AGG](/sql-reference/functions/boolor_agg) , [BOOLXOR\_AGG](/sql-reference/functions/boolxor_agg)

## Syntax

**Aggregate function**

Copy code

```
BOOLAND_AGG( <expr> )
```

**Window function**

Copy code

```
BOOLAND_AGG( <expr> )  OVER ( [ PARTITION BY <partition_expr> ] )
```

## Arguments

`expr`
:   The input expression must be an expression that can be evaluated to a boolean or converted to a boolean.

`partition_expr`
:   This column or expression specifies how to separate the input into partitions (sub-windows).

## Returns

This function returns a value of type BOOLEAN.

## Usage notes

- [Numeric](/sql-reference/data-types-numeric) values are converted to `TRUE` if they are non-zero.
- [String and binary](/sql-reference/data-types-text) values aren’t supported because they can’t be converted to Boolean values.

- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

## Examples

**Aggregate function**

The following example shows that booland\_agg returns true when all of the input values are true.

Create and load the table:

Copy code

```
CREATE OR REPLACE TABLE test_boolean_agg (
  id INTEGER,
  c1 BOOLEAN,
  c2 BOOLEAN,
  c3 BOOLEAN,
  c4 BOOLEAN
);

INSERT INTO test_boolean_agg (id, c1, c2, c3, c4) VALUES
  (1, TRUE, TRUE,  TRUE,  FALSE),
  (2, TRUE, FALSE, FALSE, FALSE),
  (3, TRUE, TRUE,  FALSE, FALSE),
  (4, TRUE, FALSE, FALSE, FALSE);
```

Display the data:

Copy code

```
SELECT *
  FROM test_boolean_agg;
```

```
+----+------+-------+-------+-------+
| ID | C1   | C2    | C3    | C4    |
|----+------+-------+-------+-------|
|  1 | True | True  | True  | False |
|  2 | True | False | False | False |
|  3 | True | True  | False | False |
|  4 | True | False | False | False |
+----+------+-------+-------+-------+
```

Query the data:

Copy code

```
SELECT BOOLAND_AGG(c1), BOOLAND_AGG(c2), BOOLAND_AGG(c3), BOOLAND_AGG(c4)
  FROM test_boolean_agg;
```

```
+-----------------+-----------------+-----------------+-----------------+
| BOOLAND_AGG(C1) | BOOLAND_AGG(C2) | BOOLAND_AGG(C3) | BOOLAND_AGG(C4) |
|-----------------+-----------------+-----------------+-----------------|
| True            | False           | False           | False           |
+-----------------+-----------------+-----------------+-----------------+
```

**Window function**

This example is similar to the previous example, but it shows usage as a window function, with the input rows
split into two partitions (one for IDs greater than 0 and one for IDs less than or equal to 0). Additional data was
added to the table.

Add rows to the table:

Copy code

```
INSERT INTO test_boolean_agg (id, c1, c2, c3, c4) VALUES
  (-4, FALSE, FALSE, FALSE, TRUE),
  (-3, FALSE, TRUE,  TRUE,  TRUE),
  (-2, FALSE, FALSE, TRUE,  TRUE),
  (-1, FALSE, TRUE,  TRUE,  TRUE);
```

Display the data:

Copy code

```
SELECT *
  FROM test_boolean_agg
  ORDER BY id;
```

```
+----+-------+-------+-------+-------+
| ID | C1    | C2    | C3    | C4    |
|----+-------+-------+-------+-------|
| -4 | False | False | False | True  |
| -3 | False | True  | True  | True  |
| -2 | False | False | True  | True  |
| -1 | False | True  | True  | True  |
|  1 | True  | True  | True  | False |
|  2 | True  | False | False | False |
|  3 | True  | True  | False | False |
|  4 | True  | False | False | False |
+----+-------+-------+-------+-------+
```

Query the data:

Copy code

```
SELECT
    id,
    BOOLAND_AGG(c1) OVER (PARTITION BY (id > 0)),
    BOOLAND_AGG(c2) OVER (PARTITION BY (id > 0)),
    BOOLAND_AGG(c3) OVER (PARTITION BY (id > 0)),
    BOOLAND_AGG(c4) OVER (PARTITION BY (id > 0))
  FROM test_boolean_agg
  ORDER BY id;
```

```
+----+----------------------------------------------+----------------------------------------------+----------------------------------------------+----------------------------------------------+
| ID | BOOLAND_AGG(C1) OVER (PARTITION BY (ID > 0)) | BOOLAND_AGG(C2) OVER (PARTITION BY (ID > 0)) | BOOLAND_AGG(C3) OVER (PARTITION BY (ID > 0)) | BOOLAND_AGG(C4) OVER (PARTITION BY (ID > 0)) |
|----+----------------------------------------------+----------------------------------------------+----------------------------------------------+----------------------------------------------|
| -4 | False                                        | False                                        | False                                        | True                                         |
| -3 | False                                        | False                                        | False                                        | True                                         |
| -2 | False                                        | False                                        | False                                        | True                                         |
| -1 | False                                        | False                                        | False                                        | True                                         |
|  1 | True                                         | False                                        | False                                        | False                                        |
|  2 | True                                         | False                                        | False                                        | False                                        |
|  3 | True                                         | False                                        | False                                        | False                                        |
|  4 | True                                         | False                                        | False                                        | False                                        |
+----+----------------------------------------------+----------------------------------------------+----------------------------------------------+----------------------------------------------+
```

**Error example**

If this function is passed strings that can’t be converted to Boolean, the function returns an error:

Copy code

```
select booland_agg('invalid type');

100037 (22018): Boolean value 'invalid_type' is not recognized
```
