Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TO\_BOOLEAN

Converts the input text or numeric expression to a [BOOLEAN](/sql-reference/data-types-logical#label-data-type-boolean) value.

See also:
:   [TRY\_TO\_BOOLEAN](/sql-reference/functions/try_to_boolean)

## Syntax

Copy code

```
TO_BOOLEAN( <string_or_numeric_expr> )
```

## Arguments

`string_or_numeric_expr`
:   A string expression or numeric expression that can be evaluated to a BOOLEAN value.

## Returns

Returns a BOOLEAN value or NULL.

- Returns TRUE if `string_or_numeric_expr` evaluates to TRUE.
- Returns FALSE if `string_or_numeric_expr` evaluates to FALSE.
- If the input is NULL, returns NULL without reporting an error.

## Usage notes

- For a string expression:

  - `'true'`, `'t'`, `'yes'`, `'y'`, `'on'`, `'1'` return TRUE.
  - `'false'`, `'f'`, `'no'`, `'n'`, `'off'`, `'0'` return FALSE.
  - All other strings return an error.

  The evaluations of the strings are case-insensitive.
- For a numeric expression:

  - `0` returns FALSE.
  - All non-zero numeric values return TRUE.
  - When converting from the [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) data type, non-numeric values, such as
    `NaN` (not a number) and `INF` (infinity), return an error.

## Examples

The following examples use the TO\_BOOLEAN function.

Create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE test_boolean(
  b BOOLEAN,
  n NUMBER,
  s STRING);

INSERT INTO test_boolean VALUES
  (true, 1, 'yes'),
  (false, 0, 'no'),
  (null, null, null);

SELECT * FROM test_boolean;
```

```
+-------+------+------+
| B     |    N | S    |
|-------+------+------|
| True  |    1 | yes  |
| False |    0 | no   |
| NULL  | NULL | NULL |
+-------+------+------+
```

Convert a text string to a BOOLEAN value:

Copy code

```
SELECT s, TO_BOOLEAN(s) FROM test_boolean;
```

```
+------+---------------+
| S    | TO_BOOLEAN(S) |
|------+---------------|
| yes  | True          |
| no   | False         |
| NULL | NULL          |
+------+---------------+
```

Convert a number to a BOOLEAN value:

Copy code

```
SELECT n, TO_BOOLEAN(n) FROM test_boolean;
```

```
+------+---------------+
|    N | TO_BOOLEAN(N) |
|------+---------------|
|    1 | True          |
|    0 | False         |
| NULL | NULL          |
+------+---------------+
```
