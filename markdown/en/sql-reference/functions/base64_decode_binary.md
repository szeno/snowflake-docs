Categories:
:   [String & binary functions](/sql-reference/functions-string) (Encoding/Decoding)

# BASE64\_DECODE\_BINARY

Decodes a Base64-encoded string to a binary.

See also:
:   [TRY\_BASE64\_DECODE\_BINARY](/sql-reference/functions/try_base64_decode_binary)

    [BASE64\_DECODE\_STRING](/sql-reference/functions/base64_decode_string) , [BASE64\_ENCODE](/sql-reference/functions/base64_encode)

## Syntax

Copy code

```
BASE64_DECODE_BINARY( <input> [ , <alphabet> ] )
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

This returns a `BINARY` value. The value can be inserted into a column of
type `BINARY`, for example.

## Usage notes

- The characters in the `alphabet` string are positionally parsed; to specify different characters in the second or third positions in the string, you must explicitly specify all preceding characters
  even if you wish to use the defaults.

  For example:

  - `+$` specifies the default (`+`) for index 62 and a different character (`$`) for index 63; no character is explicitly specified for padding so the default character (`=`) is used.
  - `+/%` specifies the defaults (`+` and `/`) for indexes 62 and 63, and specifies a different character (`%`) for padding.
- The `alphabet` string used to decode `input` must match the string originally used to encode `input`.

For more information about base64 format, see [base64](/sql-reference/binary-input-output#label-base64-format).

## Examples

This example converts data from string to binary, then encodes from binary
to a BASE64 string. After that, it decodes the base64 string back to
binary, and then converts the binary back to a string.

> Create a table and data. This includes converting a string to
> binary and that binary into a BASE64 string:
>
> > Copy code
> >
> > ```
> > CREATE OR REPLACE TABLE binary_table (v VARCHAR, b BINARY, b64_string VARCHAR);
> > INSERT INTO binary_table (v) VALUES ('HELP');
> > UPDATE binary_table SET b = TO_BINARY(v, 'UTF-8');
> > UPDATE binary_table SET b64_string = BASE64_ENCODE(b);
> > ```
>
> Now display the original string, the binary form of the string
> (which is actually displayed as hexadecimal), and then the
> BASE64 form of the binary:
>
> > Copy code
> >
> > ```
> > -- Note that the binary data in column b is displayed in hexadecimal
> > --   format to make it human-readable.
> > SELECT v, b, b64_string FROM binary_table;
> > +------+----------+------------+
> > | V    | B        | B64_STRING |
> > |------+----------+------------|
> > | HELP | 48454C50 | SEVMUA==   |
> > +------+----------+------------+
> > ```
>
> Now retrieve the data and decode it back to its original form.
> Note again that the pure binary values in the 2nd and 4th
> columns are displayed as hexadecimal, not as the internal
> binary form:
>
> > Copy code
> >
> > ```
> > SELECT v, b, b64_string, 
> >         BASE64_DECODE_BINARY(b64_string) AS FROM_BASE64_BACK_TO_BINARY,
> >         TO_VARCHAR(BASE64_DECODE_BINARY(b64_string), 'UTF-8') AS BACK_TO_STRING
> >     FROM binary_table;
> > +------+----------+------------+----------------------------+----------------+
> > | V    | B        | B64_STRING | FROM_BASE64_BACK_TO_BINARY | BACK_TO_STRING |
> > |------+----------+------------+----------------------------+----------------|
> > | HELP | 48454C50 | SEVMUA==   | 48454C50                   | HELP           |
> > +------+----------+------------+----------------------------+----------------+
> > ```

The next example is similar to the preceding example, but specifies
the `alphabet` parameter to indicate that ‘$’ should be the encoding
character for index 62 in the BASE64 encoding. In order to have diverse
enough data to need index 62, the data string uses a larger number of
distinct characters.

> Create a table and data. This includes converting a string to
> binary and that binary into a BASE64 string:
>
> > Copy code
> >
> > ```
> > SET MY_STRING = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()abcdefghijklmnopqrstuvwzyz1234567890[]{};:,./<>?-=~';
> > CREATE OR REPLACE TABLE binary_table (v VARCHAR, b BINARY, b64_string VARCHAR);
> > INSERT INTO binary_table (v) VALUES ($MY_STRING);
> > UPDATE binary_table SET b = TO_BINARY(v, 'UTF-8');
> > UPDATE binary_table SET b64_string = BASE64_ENCODE(b, 0, '$');
> > ```
>
> Now retrieve the data and decode it back to its original form.
> Because this output columns are so wide, this example does five
> separate SELECT statements rather than one.
> Note again that the pure binary values are displayed as
> hexadecimal, not as the internal binary form.
> Note also the dollar sign (‘$’) in the BASE64 string (the
> third output below):
>
> > Copy code
> >
> > ```
> > SELECT v
> >     FROM binary_table;
> > +-----------------------------------------------------------------------------------------+
> > | V                                                                                       |
> > |-----------------------------------------------------------------------------------------|
> > | ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()abcdefghijklmnopqrstuvwzyz1234567890[]{};:,./<>?-=~ |
> > +-----------------------------------------------------------------------------------------+
> > SELECT b
> >     FROM binary_table;
> > +--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> > | B                                                                                                                                                                              |
> > |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
> > | 4142434445464748494A4B4C4D4E4F505152535455565758595A21402324255E262A28296162636465666768696A6B6C6D6E6F70717273747576777A797A313233343536373839305B5D7B7D3B3A2C2E2F3C3E3F2D3D7E |
> > +--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> > SELECT b64_string
> >     FROM binary_table;
> > +----------------------------------------------------------------------------------------------------------------------+
> > | B64_STRING                                                                                                           |
> > |----------------------------------------------------------------------------------------------------------------------|
> > | QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVohQCMkJV4mKigpYWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd6eXoxMjM0NTY3ODkwW117fTs6LC4vPD4/LT1$ |
> > +----------------------------------------------------------------------------------------------------------------------+
> > SELECT BASE64_DECODE_BINARY(b64_string, '$') AS FROM_BASE64_BACK_TO_BINARY
> >     FROM binary_table;
> > +--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> > | FROM_BASE64_BACK_TO_BINARY                                                                                                                                                     |
> > |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
> > | 4142434445464748494A4B4C4D4E4F505152535455565758595A21402324255E262A28296162636465666768696A6B6C6D6E6F70717273747576777A797A313233343536373839305B5D7B7D3B3A2C2E2F3C3E3F2D3D7E |
> > +--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> > SELECT TO_VARCHAR(BASE64_DECODE_BINARY(b64_string, '$'), 'UTF-8') AS BACK_TO_STRING
> >     FROM binary_table;
> > +-----------------------------------------------------------------------------------------+
> > | BACK_TO_STRING                                                                          |
> > |-----------------------------------------------------------------------------------------|
> > | ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()abcdefghijklmnopqrstuvwzyz1234567890[]{};:,./<>?-=~ |
> > +-----------------------------------------------------------------------------------------+
> > ```
