Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TRY\_TO\_DECFLOAT

A special version of [TO\_DECFLOAT](/sql-reference/functions/to_decfloat) that performs the same
operation — that is, converts an input expression to a [DECFLOAT](/sql-reference/data-types-numeric#label-data-type-decfloat) —
but with error-handling support. If the conversion can’t be performed, it returns a NULL
value instead of raising an error.

For more information, see [Error-handling conversion functions](/sql-reference/functions-conversion#label-try-conversion-functions).

## Syntax

Copy code

```
TRY_TO_DECFLOAT( <string_expr> [ , '<format>' ] )
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

## Usage notes

The special values `'NaN'` (not a number), `'inf'` (infinity),
and `'-inf'` (negative infinity) aren’t supported.

## Returns

This function returns a value of DECFLOAT data type.

If there is a conversion error, the function returns NULL.

## Examples

This example uses the TRY\_TO\_DECFLOAT function:

Copy code

```
SELECT TRY_TO_DECFLOAT('3.1415926'), TRY_TO_DECFLOAT('Invalid');
```

```
+------------------------------+----------------------------+
| TRY_TO_DECFLOAT('3.1415926') | TRY_TO_DECFLOAT('INVALID') |
|------------------------------+----------------------------|
| 3.1415926                    | NULL                       |
+------------------------------+----------------------------+
```

For additional examples, see [TO\_DECFLOAT](/sql-reference/functions/to_decfloat).
