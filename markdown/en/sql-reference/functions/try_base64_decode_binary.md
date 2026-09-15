Categories:
:   [String & binary functions](/sql-reference/functions-string) (Encoding/Decoding)

# TRY\_BASE64\_DECODE\_BINARY

A special version of [BASE64\_DECODE\_BINARY](/sql-reference/functions/base64_decode_binary) that
returns a NULL value if an error occurs during decoding.

## Syntax

Copy code

```
TRY_BASE64_DECODE_BINARY(<input> [, <alphabet>])
```

## Arguments

`input`
:   The base64-encoded string to convert to BINARY data type.

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

This returns a `BINARY` value. The value can be inserted into a column of
type `BINARY`, for example.

## Usage notes

For more information about base64 format, see [base64](/sql-reference/binary-input-output#label-base64-format).

## Examples

This shows how to use the function `TRY_BASE64_DECODE_BINARY`. The function
is used in the `INSERT` statement to decode a base64-encoded string
into a BINARY field; the function is not used in the `SELECT`
statement.

> Create a table and insert data:
>
> > Copy code
> >
> > ```
> > CREATE TABLE base64 (v VARCHAR, base64_encoded_varchar VARCHAR, b BINARY);
> > INSERT INTO base64 (v, base64_encoded_varchar, b)
> >    SELECT 'HELP', BASE64_ENCODE('HELP'),
> >       TRY_BASE64_DECODE_BINARY(BASE64_ENCODE('HELP'));
> > ```
>
> Now run a query to show that we can retrieve the data intact:
>
> > Copy code
> >
> > ```
> > SELECT v, base64_encoded_varchar, 
> >     -- Convert binary -> base64-encoded-string
> >     TO_VARCHAR(b, 'BASE64'),
> >     -- Convert binary back to original value
> >     TO_VARCHAR(b, 'UTF-8')
> >   FROM base64;
> > +------+------------------------+-------------------------+------------------------+
> > | V    | BASE64_ENCODED_VARCHAR | TO_VARCHAR(B, 'BASE64') | TO_VARCHAR(B, 'UTF-8') |
> > |------+------------------------+-------------------------+------------------------|
> > | HELP | SEVMUA==               | SEVMUA==                | HELP                   |
> > +------+------------------------+-------------------------+------------------------+
> > ```
