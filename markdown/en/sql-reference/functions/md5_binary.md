Categories:
:   [String & binary functions](/sql-reference/functions-string) (Checksum)

# MD5\_BINARY

Returns a 16-byte `BINARY` value containing the 128-bit MD5 message digest.

See also:
:   [MD5 , MD5\_HEX](/sql-reference/functions/md5), [MD5\_NUMBER\_LOWER64](/sql-reference/functions/md5_number_lower64), [MD5\_NUMBER\_UPPER64](/sql-reference/functions/md5_number_upper64)

## Syntax

Copy code

```
MD5_BINARY(<msg>)
```

## Arguments

`msg`
:   A string expression, the message to be hashed.

## Returns

Returns a 16-byte `BINARY` value containing the MD5 message digest.

## Usage notes

- Although the MD5\* functions were originally developed as cryptographic functions, they are now
  obsolete for cryptography and should not be used for that purpose. They can be used for other purposes
  (for example, as “checksum” functions to detect accidental data corruption).

  If you need to encrypt and decrypt data, use the following functions:

  - [ENCRYPT](/sql-reference/functions/encrypt) and [DECRYPT](/sql-reference/functions/decrypt)
  - [ENCRYPT\_RAW](/sql-reference/functions/encrypt_raw) and [DECRYPT\_RAW](/sql-reference/functions/decrypt_raw)

## Examples

The example below shows a simple example of using the function. Note that
although the output is a 16-byte binary string, by default SNOWSQL displays
binary values as a series of hexadecimal digits, so the output below appears
as 32 hexadecimal digits, not as 16 one-byte characters.

> Copy code
>
> ```
> SELECT md5_binary('Snowflake');
> +----------------------------------+
> | MD5_BINARY('SNOWFLAKE')          |
> |----------------------------------|
> | EDF1439075A83A447FB8B630DDC9C8DE |
> +----------------------------------+
> ```

This example demonstrates using the function to insert into a table that
contains a column of type `BINARY`.

> Create and fill a table:
>
> > Copy code
> >
> > ```
> > CREATE TABLE binary_demo (b BINARY);
> > INSERT INTO binary_demo (b) SELECT MD5_BINARY('Snowflake');
> > ```
>
> Output:
>
> > Copy code
> >
> > ```
> > SELECT TO_VARCHAR(b, 'HEX') AS hex_representation
> >     FROM binary_demo;
> > +----------------------------------+
> > | HEX_REPRESENTATION               |
> > |----------------------------------|
> > | EDF1439075A83A447FB8B630DDC9C8DE |
> > +----------------------------------+
> > ```
