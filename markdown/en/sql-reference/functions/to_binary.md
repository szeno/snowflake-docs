Categories:
:   [Conversion functions](/sql-reference/functions-conversion)

# TO\_BINARY

Converts the input expression to a binary value. For NULL input, the output is NULL.

See also:

- [TRY\_TO\_BINARY](/sql-reference/functions/try_to_binary).
- [Binary input and output](/sql-reference/binary-input-output).

## Syntax

Copy code

```
TO_BINARY( <string_expr> [, '<format>'] )
TO_BINARY( <variant_expr> )
```

## Returns

The return type is BINARY.

## Arguments

**Required:**

`string_expr`
:   A string expression.

**Optional:**

`format`
:   The binary format for conversion: HEX, BASE64, or UTF-8 (see [Binary input and output](/sql-reference/binary-input-output)). The default is the value of the
    BINARY\_INPUT\_FORMAT session parameter. If this parameter is not set, the
    default is HEX.

## Returns

Returns a value of type BINARY.

## Examples

These examples show the output when `TO_BINARY` is called.

This example shows how to convert a `VARCHAR` to `BINARY` and then get it
back in its original form (`VARCHAR`).

> Create and fill a table:
>
> > Copy code
> >
> > ```
> > CREATE TABLE binary_test (v VARCHAR, b BINARY);
> > INSERT INTO binary_test(v) VALUES ('SNOW');
> > ```
>
> Convert the `VARCHAR` to `BINARY`:
>
> > Copy code
> >
> > ```
> > UPDATE binary_test SET b = TO_BINARY(HEX_ENCODE(v), 'HEX');
> > ```
>
> Run a query and show the output:
>
> > Copy code
> >
> > ```
> > SELECT v, HEX_DECODE_STRING(TO_VARCHAR(b, 'HEX')) FROM binary_test;
> > +------+-----------------------------------------+
> > | V    | HEX_DECODE_STRING(TO_VARCHAR(B, 'HEX')) |
> > |------+-----------------------------------------|
> > | SNOW | SNOW                                    |
> > +------+-----------------------------------------+
> > ```

This example shows how to convert a string of UTF-8 characters into
`BINARY`. Note that by default SNOWSQL shows `BINARY` values as a string
of hexadecimal digits, not in UTF-8 and not in the internal `BINARY` format.

> Copy code
>
> ```
> SELECT TO_BINARY('SNOW', 'utf-8');
> +----------------------------+
> | TO_BINARY('SNOW', 'UTF-8') |
> |----------------------------|
> | 534E4F57                   |
> +----------------------------+
> ```

This example is the same as the preceding example, except that this example explicitly
converts the output to hexadecimal digits so that it is more obvious that the
output is a string containing hexadecimal digits:

> Copy code
>
> ```
> SELECT TO_VARCHAR(TO_BINARY('SNOW', 'utf-8'), 'HEX');
> +-----------------------------------------------+
> | TO_VARCHAR(TO_BINARY('SNOW', 'UTF-8'), 'HEX') |
> |-----------------------------------------------|
> | 534E4F57                                      |
> +-----------------------------------------------+
> ```
