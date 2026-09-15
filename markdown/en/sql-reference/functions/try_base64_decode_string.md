Categories:
:   [String & binary functions](/sql-reference/functions-string) (Encoding/Decoding)

# TRY\_BASE64\_DECODE\_STRING

A special version of [BASE64\_DECODE\_STRING](/sql-reference/functions/base64_decode_string) that
returns a NULL value if an error occurs during decoding.

`BASE64_DECODE_STRING` and `TRY_BASE64_DECODE_STRING` are “reciprocal”
(or “converse”) functions of `BASE64_ENCODE`.

## Syntax

Copy code

```
TRY_BASE64_DECODE_STRING(<input> [, <alphabet>])
```

## Arguments

`input`
:   The base64-encoded string to decode to a normal string.

`alphabet`
:   A string consisting of up to three ASCII characters:

    - The first two characters in the string specify the last two characters (indexes 62 and 63) in the alphabet used to encode the input:

      - `A` to `Z` (indexes 0-25).
      - `a` to `z` (indexes 26-51).
      - `0` to `9` (indexes 52-61).
      - `+` and `/` (indexes 62, 63).

      Defaults: `+` and `/`
    - The third character in the string specifies the character used for padding.

      Default: `=`

## Returns

A string.

## Usage notes

For more information about base64 format, see [base64](/sql-reference/binary-input-output#label-base64-format).

## Examples

This shows how to use the function and demonstrates that
`TRY_BASE64_DECODE_STRING` is the converse of `BASE64_ENCODE`:

> Copy code
>
> ```
> SELECT TRY_BASE64_DECODE_STRING(BASE64_ENCODE('HELLO'));
> +--------------------------------------------------+
> | TRY_BASE64_DECODE_STRING(BASE64_ENCODE('HELLO')) |
> |--------------------------------------------------|
> | HELLO                                            |
> +--------------------------------------------------+
> ```

This shows a more realistic example:

> Create a table and data:
>
> > Copy code
> >
> > ```
> > CREATE TABLE base64 (v VARCHAR, base64_string VARCHAR, garbage VARCHAR);
> > INSERT INTO base64 (v, base64_string, garbage) 
> >   SELECT 'HELLO', BASE64_ENCODE('HELLO'), '127';
> > ```
>
> Query the data using the `TRY_BASE64_DECODE_STRING` function:
>
> > Copy code
> >
> > ```
> > SELECT v, base64_string, TRY_BASE64_DECODE_STRING(base64_string), TRY_BASE64_DECODE_STRING(garbage) FROM base64;
> > +-------+---------------+-----------------------------------------+-----------------------------------+
> > | V     | BASE64_STRING | TRY_BASE64_DECODE_STRING(BASE64_STRING) | TRY_BASE64_DECODE_STRING(GARBAGE) |
> > |-------+---------------+-----------------------------------------+-----------------------------------|
> > | HELLO | SEVMTE8=      | HELLO                                   | NULL                              |
> > +-------+---------------+-----------------------------------------+-----------------------------------+
> > ```
