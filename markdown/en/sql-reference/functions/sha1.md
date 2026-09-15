Categories:
:   [String & binary functions](/sql-reference/functions-string) (Cryptographic Hash)

# SHA1 , SHA1\_HEX

Returns a 40-character hex-encoded string containing the 160-bit SHA-1
message digest.

These functions are synonymous.

## Syntax

Copy code

```
SHA1(<msg>)

SHA1_HEX(<msg>)
```

## Arguments

`msg`
:   A string expression, the message to be hashed.

## Returns

The data type of the returned value is VARCHAR.

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
SELECT sha1('Snowflake');

------------------------------------------+
            SHA1('SNOWFLAKE')             |
------------------------------------------+
 fda76b0bcc1e87cf259b1d1e3271d76f590fb5dd |
------------------------------------------+
```

The data type of the output is string (`VARCHAR`) and can be stored in a
`VARCHAR` column:

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
> Here are the query and output:
>
> > Copy code
> >
> > ```
> > SELECT v, v_as_sha1, v_as_sha1_hex
> >   FROM sha_table
> >   ORDER BY v;
> > +-------+------------------------------------------+------------------------------------------+
> > | V     | V_AS_SHA1                                | V_AS_SHA1_HEX                            |
> > |-------+------------------------------------------+------------------------------------------|
> > | AbCd0 | 9ddb991863d53b35a52c490db256207c776ab8d8 | 9ddb991863d53b35a52c490db256207c776ab8d8 |
> > +-------+------------------------------------------+------------------------------------------+
> > ```
