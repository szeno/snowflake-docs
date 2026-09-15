Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TO\_DECFLOAT

Converts an expression to a decimal floating-point number ([DECFLOAT](/sql-reference/data-types-numeric#label-data-type-decfloat)).

See also:
:   [TRY\_TO\_DECFLOAT](/sql-reference/functions/try_to_decfloat)

## Syntax

Copy code

```
TO_DECFLOAT( <expr> [ , '<format>' ] )
```

## Arguments

**Required:**

`expr`
:   An expression of a numeric, character, or Boolean type.

**Optional:**

`'format'`
:   If the expression evaluates to a string, the function accepts
    an optional format model. For more information, see
    [SQL format models](/sql-reference/sql-format-models). The format model
    specifies the format of the input string, not the format of the
    output value.

## Returns

This function returns a value of DECFLOAT data type.

If `expr` is NULL, the function returns NULL.

## Usage notes

The special values `'NaN'` (not a number), `'inf'` (infinity),
and `'-inf'` (negative infinity) aren’t supported.

## Examples

After you create a table with columns of different data types, call the TO\_DECFLOAT
function to convert the values in each of those columns:

Copy code

```
CREATE OR REPLACE TABLE to_decfloat_demo (d DECIMAL(7, 2), v VARCHAR);
INSERT INTO to_decfloat_demo (d, v) SELECT 1.1, '2.2';
SELECT TO_DECFLOAT(d), TO_DECFLOAT(v) FROM to_decfloat_demo;
```

```
+----------------+----------------+
| TO_DECFLOAT(D) | TO_DECFLOAT(V) |
|----------------+----------------|
| 1.1            | 2.2            |
+----------------+----------------+
```
