Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TRY\_TO\_DOUBLE

A special version of [TO\_DOUBLE](/sql-reference/functions/to_double) that performs the same operation (that is,
converts an input expression to a double-precision floating-point number), but
with error-handling support (that is, if the conversion can’t be performed, it
returns a NULL value instead of raising an error).

For more information, see [Error-handling conversion functions](/sql-reference/functions-conversion#label-try-conversion-functions).

## Syntax

Copy code

```
TRY_TO_DOUBLE( <string_expr> [, '<format>' ] )
```

## Arguments

`expr`
:   An expression of a character type.

`format`
:   If the expression evaluates to a string, then the function accepts
    an optional format model. Format models are described at
    [SQL format models](/sql-reference/sql-format-models). The format model
    specifies the format of the input string, not the format of the
    output value.

## Usage notes

- The function only accepts string expressions.
- Strings are converted as decimal integer or fractional numbers,
  scientific notation and special values (**nan**, **inf**, **infinity**)
  are accepted.

## Returns

This function returns a value of FLOAT data type.

If there is a conversion error, the function returns NULL.

## Examples

This example uses the TRY\_TO\_DOUBLE function:

Copy code

```
SELECT TRY_TO_DOUBLE('3.1415926'), TRY_TO_DOUBLE('Invalid');
```

```
+----------------------------+--------------------------+
| TRY_TO_DOUBLE('3.1415926') | TRY_TO_DOUBLE('INVALID') |
|----------------------------+--------------------------|
|                  3.1415926 |                     NULL |
+----------------------------+--------------------------+
```

For additional examples, see [TO\_DOUBLE](/sql-reference/functions/to_double).
