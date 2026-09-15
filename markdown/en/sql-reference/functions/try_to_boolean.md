Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TRY\_TO\_BOOLEAN

A special version of [TO\_BOOLEAN](/sql-reference/functions/to_boolean) that performs the same operation
(that is, converts an input expression to a Boolean value), but with error-handling
support. If the conversion can’t be performed, TRY\_TO\_BOOLEAN returns a NULL value
instead of raising an error.

For more information, see [Error-handling conversion functions](/sql-reference/functions-conversion#label-try-conversion-functions).

## Syntax

Copy code

```
TRY_TO_BOOLEAN( <string_expr> )
```

## Arguments

`string_expr`
:   A string expression that can be evaluated to a BOOLEAN value.

## Returns

This function returns a value of type [BOOLEAN](/sql-reference/data-types-logical#label-data-type-boolean).

## Usage notes

The input argument must be a string expression. The function evaluates the string expression
in the following way:

- `'true'`, `'t'`, `'yes'`, `'y'`, `'on'`, `'1'` return TRUE.
- `'false'`, `'f'`, `'no'`, `'n'`, `'off'`, `'0'` return FALSE.
- All other strings return NULL.

The evaluations of the strings are case-insensitive.

## Examples

This example uses the TRY\_TO\_BOOLEAN function:

Copy code

```
SELECT TRY_TO_BOOLEAN('True')  AS "T",
       TRY_TO_BOOLEAN('False') AS "F",
       TRY_TO_BOOLEAN('Not valid')  AS "N";
```

```
+------+-------+------+
| T    | F     | N    |
|------+-------+------|
| True | False | NULL |
+------+-------+------+
```

For more examples, see [TO\_BOOLEAN](/sql-reference/functions/to_boolean).
