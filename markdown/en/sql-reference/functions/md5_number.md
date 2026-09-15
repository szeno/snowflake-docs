Categories:
:   [String & binary functions](/sql-reference/functions-string) (Checksum)

# MD5\_NUMBER — *Obsoleted*

Obsoleted Feature

This function has been obsoleted.

To get the message digest as a 32-character hex-encoded string or binary value, use [MD5 , MD5\_HEX](/sql-reference/functions/md5) or [MD5\_BINARY](/sql-reference/functions/md5_binary)
instead.

To get the lower 64 bits or upper 64 bits of the MD5 message digest as a signed number, use [MD5\_NUMBER\_LOWER64](/sql-reference/functions/md5_number_lower64) or
[MD5\_NUMBER\_UPPER64](/sql-reference/functions/md5_number_upper64) instead.

Returns the 128-bit MD5 message digest interpreted as a signed 128-bit big
endian number. This representation is useful for maximally efficient storage
and comparison of MD5 digests.

See also:
:   [MD5 , MD5\_HEX](/sql-reference/functions/md5), [MD5\_BINARY](/sql-reference/functions/md5_binary), [MD5\_NUMBER\_LOWER64](/sql-reference/functions/md5_number_lower64), [MD5\_NUMBER\_UPPER64](/sql-reference/functions/md5_number_upper64)

## Syntax

Copy code

```
MD5_NUMBER(<msg>)
```

## Arguments

`msg`
:   A string expression, the message to be hashed.

## Returns

A signed integer (`NUMERIC(38, 0)`).

This integer can be outside the range stored by `NUMERIC(38, 0)`, so this function has been obsoleted.

## Usage notes

Although the `MD5`, `MD5_BINARY`, and `MD5_NUMBER` functions
were originally developed as cryptographic functions, they are now
obsolete for cryptography and should not be used for that purpose.
They can be used for other purposes, for example as “checksum”
functions to detect accidental data corruption.

## Examples

Copy code

```
SELECT md5_number('Snowflake');

-----------------------------------------+
         MD5_NUMBER('SNOWFLAKE')         |
-----------------------------------------+
 -24002618010294540563082926240470284066 |
-----------------------------------------+
```
