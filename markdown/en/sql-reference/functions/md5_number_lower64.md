Categories:
:   [String & binary functions](/sql-reference/functions-string) (Checksum)

# MD5\_NUMBER\_LOWER64

Calculates the 128-bit MD5 message digest, interprets it as a signed 128-bit big endian number, and returns the lower 64 bits of
the number as an unsigned integer. This representation is useful for maximally efficient storage and comparison of MD5 digests.

See also:
:   [MD5 , MD5\_HEX](/sql-reference/functions/md5), [MD5\_BINARY](/sql-reference/functions/md5_binary), [MD5\_NUMBER\_UPPER64](/sql-reference/functions/md5_number_upper64)

## Syntax

Copy code

```
MD5_NUMBER_LOWER64(<msg>)
```

## Arguments

`msg`
:   A string expression, the message to be hashed.

## Returns

A 64 bit unsigned integer that represents the lower 64 bits of the message digest.

## Usage notes

- Although the MD5\* functions were originally developed as cryptographic functions, they are now
  obsolete for cryptography and should not be used for that purpose. They can be used for other purposes
  (for example, as “checksum” functions to detect accidental data corruption).

  If you need to encrypt and decrypt data, use the following functions:

  - [ENCRYPT](/sql-reference/functions/encrypt) and [DECRYPT](/sql-reference/functions/decrypt)
  - [ENCRYPT\_RAW](/sql-reference/functions/encrypt_raw) and [DECRYPT\_RAW](/sql-reference/functions/decrypt_raw)

## Examples

Copy code

```
select md5_number_lower64('Snowflake');

+---------------------------------+
| MD5_NUMBER_LOWER64('SNOWFLAKE') |
|---------------------------------|
|             9203306159527282910 |
+---------------------------------+
```
