Categories:
:   [String & binary functions](/sql-reference/functions-string) (Checksum)

# MD5 , MD5\_HEX

Returns a 32-character hex-encoded string containing the 128-bit MD5
message digest.

These functions are synonymous.

See also:
:   [MD5\_BINARY](/sql-reference/functions/md5_binary), [MD5\_NUMBER\_LOWER64](/sql-reference/functions/md5_number_lower64), [MD5\_NUMBER\_UPPER64](/sql-reference/functions/md5_number_upper64)

## Syntax

Copy code

```
MD5(<msg>)

MD5_HEX(<msg>)
```

## Arguments

`msg`
:   A string expression, the message to be hashed.

## Returns

Returns a 32-character hex-encoded string.

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
SELECT md5('Snowflake');

----------------------------------+
         MD5('SNOWFLAKE')         |
----------------------------------+
 edf1439075a83a447fb8b630ddc9c8de |
----------------------------------+
```
