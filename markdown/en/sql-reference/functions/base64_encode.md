Categories:
:   [String & binary functions](/sql-reference/functions-string) (Encoding/Decoding)

# BASE64\_ENCODE

Encodes the input (string or binary) using Base64 encoding.

See also:
:   [BASE64\_DECODE\_BINARY](/sql-reference/functions/base64_decode_binary) , [BASE64\_DECODE\_STRING](/sql-reference/functions/base64_decode_string)

## Syntax

Copy code

```
BASE64_ENCODE( <input> [ , <max_line_length> ] [ , <alphabet> ] )
```

## Arguments

**Required:**

`input`
:   A string or binary expression to be encoded.

**Optional:**

`max_line_length`
:   A positive integer that specifies the maximum number of characters in a single line of the output.

    Default: `0` (specifies that no line breaks are inserted (i.e. the maximum line length is infinite))

`alphabet`
:   A string consisting of up to three ASCII characters:

    - The first two characters in the string specify the last two characters (indexes 62 and 63) in the alphabet used to encode the input:

      - `A` to `Z` (indexes 0-25)
      - `a` to `z` (indexes 26-51)
      - `0` to `9` (indexes 52-61)
      - `+` and `/` (indexes 62, 63)

      Defaults: `+` and `/`
    - The third character in the string specifies the character used for padding.

      Default: `=`

## Returns

Returns a string (regardless of whether the input was a string or `BINARY`).

## Usage notes

- The characters in the `alphabet` string are positionally parsed; to specify different characters in the second or third positions in the string, you must explicitly specify all preceding characters
  even if you wish to use the defaults.

  For example:

  - `+$` specifies the default (`+`) for index 62 and a different character (`$`) for index 63; no character is explicitly specified for padding so the default character (`=`) is used.
  - `+/%` specifies the defaults (`+` and `/`) for indexes 62 and 63, and specifies a different character (`%`) for padding.
- If you specify an `alphabet` string to encode `input`, the same string must be used to decode `input`.

For more information about base64 format, see [base64](/sql-reference/binary-input-output#label-base64-format).

## Returns

This returns a string that contains only the characters used for the base64
encoding.

## Examples

Encode a string using Base64:

Copy code

```
SELECT BASE64_ENCODE('Snowflake');

----------------------------+
 BASE64_ENCODE('SNOWFLAKE') |
----------------------------+
 U25vd2ZsYWtl               |
----------------------------+
```

Encode a string containing non-ASCII characters using Base64 with
‘$’ in place of ‘+’ for encoding, and output the string
with a maximum line length of 32:

Copy code

```
SELECT BASE64_ENCODE('Snowflake ❄❄❄ Snowman ☃☃☃',32,'$');

---------------------------------------------------+
 BASE64_ENCODE('SNOWFLAKE ❄❄❄ SNOWMAN ☃☃☃',32,'$') |
---------------------------------------------------+
 U25vd2ZsYWtlIOKdhOKdhOKdhCBTbm93                  |
 bWFuIOKYg$KYg$KYgw==                              |
---------------------------------------------------+
```

This shows another example of using `BASE64_ENCODE` (and also
`BASE64_DECODE_STRING`):

> Create a table and data:
>
> > Copy code
> >
> > ```
> > CREATE OR REPLACE TABLE base64_table (v VARCHAR, base64_string VARCHAR);
> > INSERT INTO base64_table (v) VALUES ('HELLO');
> > UPDATE base64_table SET base64_string = BASE64_ENCODE(v);
> > ```
>
> Now run a query using `BASE64_DECODE_STRING`:
>
> > Copy code
> >
> > ```
> > SELECT v, base64_string, BASE64_DECODE_STRING(base64_string) 
> >     FROM base64_table;
> > +-------+---------------+-------------------------------------+
> > | V     | BASE64_STRING | BASE64_DECODE_STRING(BASE64_STRING) |
> > |-------+---------------+-------------------------------------|
> > | HELLO | SEVMTE8=      | HELLO                               |
> > +-------+---------------+-------------------------------------+
> > ```
