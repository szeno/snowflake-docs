Categories:
:   [String & binary functions](/sql-reference/functions-string) (Encoding/Decoding)

# BASE64\_DECODE\_STRING

Decodes a Base64-encoded string to a string.

See also:
:   [TRY\_BASE64\_DECODE\_STRING](/sql-reference/functions/try_base64_decode_string)

    [BASE64\_DECODE\_BINARY](/sql-reference/functions/base64_decode_binary) , [BASE64\_ENCODE](/sql-reference/functions/base64_encode)

## Syntax

Copy code

```
BASE64_DECODE_STRING( <input> [ , <alphabet> ] )
```

## Arguments

**Required:**

`input`
:   A Base64-encoded string expression.

**Optional:**

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

A string.

## Usage notes

- The characters in the `alphabet` string are positionally parsed; to specify different characters in the second or third positions in the string, you must explicitly specify all preceding characters
  even if you wish to use the defaults.

  For example:

  - `+$` specifies the default (`+`) for index 62 and a different character (`$`) for index 63; no character is explicitly specified for padding so the default character (`=`) is used.
  - `+/%` specifies the defaults (`+` and `/`) for indexes 62 and 63, and specifies a different character (`%`) for padding.
- The `alphabet` string used to decode `input` must match the string originally used to encode `input`.

For more information about base64 format, see [base64](/sql-reference/binary-input-output#label-base64-format).

## Examples

This shows a simple example of using `BASE64_DECODE_STRING`:

> Copy code
>
> ```
> SELECT BASE64_DECODE_STRING('U25vd2ZsYWtl');
> +--------------------------------------+
> | BASE64_DECODE_STRING('U25VD2ZSYWTL') |
> |--------------------------------------|
> | Snowflake                            |
> +--------------------------------------+
> ```

This shows another example of using `BASE64_DECODE_STRING`:

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
