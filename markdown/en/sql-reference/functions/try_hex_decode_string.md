Categories:
:   [String & binary functions](/sql-reference/functions-string) (Encoding/Decoding)

# TRY\_HEX\_DECODE\_STRING

A special version of [HEX\_DECODE\_STRING](/sql-reference/functions/hex_decode_string) that
returns a NULL value if an error occurs during decoding.

## Syntax

Copy code

```
TRY_HEX_DECODE_STRING(<input>)
```

## Arguments

`input`
:   A hex-encoded string expression. Typically the input was created by a
    call to [HEX\_ENCODE](/sql-reference/functions/hex_encode).

## Returns

The returned value is a string (VARCHAR).

## Examples

This shows how to use the function:

> Create a table and data:
>
> > Copy code
> >
> > ```
> > CREATE TABLE hex (v VARCHAR, hex_string VARCHAR, garbage VARCHAR);
> > INSERT INTO hex (v, hex_string, garbage) 
> >   SELECT 'AaBb', HEX_ENCODE('AaBb'), '127';
> > ```
>
> Now run the query:
>
> > Copy code
> >
> > ```
> > SELECT v, hex_string, TRY_HEX_DECODE_STRING(hex_string), TRY_HEX_DECODE_STRING(garbage) FROM hex;
> > ```
>
> Output:
>
> > Copy code
> >
> > ```
> > +------+------------+-----------------------------------+--------------------------------+
> > | V    | HEX_STRING | TRY_HEX_DECODE_STRING(HEX_STRING) | TRY_HEX_DECODE_STRING(GARBAGE) |
> > |------+------------+-----------------------------------+--------------------------------|
> > | AaBb | 41614262   | AaBb                              | NULL                           |
> > +------+------------+-----------------------------------+--------------------------------+
> > ```
