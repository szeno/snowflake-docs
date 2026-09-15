Categories:
:   [String & binary functions](/sql-reference/functions-string) (Cryptographic Hash)

# SHA1\_BINARY

Returns a 20-byte binary containing the 160-bit SHA-1 message digest.

## Syntax

Copy code

```
SHA1_BINARY(<msg>)
```

## Arguments

`msg`
:   A string expression, the message to be hashed.

## Returns

The data type of the returned value is BINARY.

## Usage notes

- The SHA1 family of functions is provided primarily for backwards compatibility with other systems.
  For more secure encryption, Snowflake recommends using the SHA2 family of functions.

- Do not use this function to encrypt a message that you need to decrypt. This function has no corresponding decryption function.
  (The length of the output is independent of the length of the input. The output does not necessarily have enough bits to hold
  all of the information from the input, so it is not possible to write a function that can decrypt all possible valid inputs.)

  This function is intended for other purposes, such as calculating a checksum to detect data corruption.

  If you need to encrypt and decrypt data, use the following functions:

  - [ENCRYPT](/sql-reference/functions/encrypt) and [DECRYPT](/sql-reference/functions/decrypt)
  - [ENCRYPT\_RAW](/sql-reference/functions/encrypt_raw) and [DECRYPT\_RAW](/sql-reference/functions/decrypt_raw)

## Examples

Copy code

```
SELECT sha1_binary('Snowflake');

------------------------------------------+
         SHA1_BINARY('SNOWFLAKE')         |
------------------------------------------+
 FDA76B0BCC1E87CF259B1D1E3271D76F590FB5DD |
------------------------------------------+
```

The data type of the output is `BINARY` and can be stored in a `BINARY`
column:

> Create and fill a table:
>
> > Copy code
> >
> > ```
> > CREATE TABLE sha_table(
> >     v VARCHAR, 
> >     v_as_sha1 VARCHAR,
> >     v_as_sha1_hex VARCHAR,
> >     v_as_sha1_binary BINARY,
> >     v_as_sha2 VARCHAR,
> >     v_as_sha2_hex VARCHAR,
> >     v_as_sha2_binary BINARY
> >     );
> > INSERT INTO sha_table(v) VALUES ('AbCd0');
> > UPDATE sha_table SET 
> >     v_as_sha1 = SHA1(v),
> >     v_as_sha1_hex = SHA1_HEX(v),
> >     v_as_sha1_binary = SHA1_BINARY(v),
> >     v_as_sha2 = SHA2(v),
> >     v_as_sha2_hex = SHA2_HEX(v),
> >     v_as_sha2_binary = SHA2_BINARY(v)
> >     ;
> > ```
>
> Here are the query and output (note that for display, the output is
> implicitly cast to a user-readable form, which in this case is a string of
> hexadecimal digits):
>
> > Copy code
> >
> > ```
> > SELECT v, v_as_sha1_binary
> >   FROM sha_table
> >   ORDER BY v;
> > +-------+------------------------------------------+
> > | V     | V_AS_SHA1_BINARY                         |
> > |-------+------------------------------------------|
> > | AbCd0 | 9DDB991863D53B35A52C490DB256207C776AB8D8 |
> > +-------+------------------------------------------+
> > ```
