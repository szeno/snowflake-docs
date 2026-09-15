Categories:
:   [String & binary functions](/sql-reference/functions-string) (Encoding/Decoding)

# HEX\_DECODE\_STRING

Decodes a hex-encoded string to a string.

See also:
:   [TRY\_HEX\_DECODE\_STRING](/sql-reference/functions/try_hex_decode_string)

## Syntax

Copy code

```
HEX_DECODE_STRING(<input>)
```

## Arguments

`input`
:   A hex-encoded string expression. Typically the input was created by a
    call to [HEX\_ENCODE](/sql-reference/functions/hex_encode).

## Returns

The returned value is a string (VARCHAR).

## Examples

The following decodes a sequence of hexadecimal digits into the corresponding
word:

Copy code

```
SELECT HEX_DECODE_STRING('536E6F77666C616B65');

-----------------------------------------+
 HEX_DECODE_STRING('536E6F77666C616B65') |
-----------------------------------------+
 Snowflake                               |
-----------------------------------------+
```

The hexadecimal digits A-F can be uppercase or lowercase. The following
statement uses lowercase letters but produces the same result as the
preceding statement:

Copy code

```
SELECT HEX_DECODE_STRING('536e6f77666c616b65');

-----------------------------------------+
 HEX_DECODE_STRING('536E6F77666C616B65') |
-----------------------------------------+
 Snowflake                               |
-----------------------------------------+
```

This shows another example of using `HEX_DECODE_STRING`:

> Create a table and data:
>
> > Copy code
> >
> > ```
> > CREATE TABLE binary_table (v VARCHAR, b BINARY);
> > INSERT INTO binary_table (v, b) 
> >     SELECT 'HELLO', HEX_DECODE_BINARY(HEX_ENCODE('HELLO'));
> > ```
>
> Now run a query to show that we can retrieve the data:
>
> > Copy code
> >
> > ```
> > SELECT v, b, HEX_DECODE_STRING(TO_VARCHAR(b)) FROM binary_table;
> > +-------+------------+----------------------------------+
> > | V     | B          | HEX_DECODE_STRING(TO_VARCHAR(B)) |
> > |-------+------------+----------------------------------|
> > | HELLO | 48454C4C4F | HELLO                            |
> > +-------+------------+----------------------------------+
> > ```
