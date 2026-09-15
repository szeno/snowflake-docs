Categories:
:   [String & binary functions](/sql-reference/functions-string) (Encoding/Decoding)

# HEX\_ENCODE

Encodes the input using hexadecimal (also ‘hex’ or ‘base16’) encoding.
The result is comprised of 16 different symbols: The numbers ’0’ to ’9’ as
well as the letters ‘A’ to ‘F’ (or ‘a’ to ‘f’, see below).

See also:
:   [HEX\_DECODE\_BINARY](/sql-reference/functions/hex_decode_binary) , [HEX\_DECODE\_STRING](/sql-reference/functions/hex_decode_string)

## Syntax

Copy code

```
HEX_ENCODE(<input> [, <case>])
```

## Arguments

**Required:**

`input`
:   A binary or string expression to be encoded.

**Optional:**

`case`
:   This optional boolean argument controls the case of the letters
    (‘A’, ‘B’, ‘C’, ‘D’, ‘E’ and ‘F’) used in the encoding.
    The default value is `1` and indicates that uppercase
    letters are used. The value `0` indicates that lowercase
    letters are used. All other values are illegal and result
    in an error.

## Returns

This returns a string that contains only hexadecimal digits.

## Examples

Encode a string:

Copy code

```
SELECT HEX_ENCODE('Snowflake');

-------------------------+
 HEX_ENCODE('SNOWFLAKE') |
-------------------------+
 536E6F77666C616B65      |
-------------------------+
```

Encode a string using lowercase letters:

Copy code

```
SELECT HEX_ENCODE('Snowflake',0);

---------------------------+
 HEX_ENCODE('SNOWFLAKE',0) |
---------------------------+
 536e6f77666c616b65        |
---------------------------+
```
