Categories:
:   [String & binary functions](/sql-reference/functions-string) (Cryptographic Hash)

# SHA2 , SHA2\_HEX

Returns a hex-encoded string containing the N-bit SHA-2 message digest,
where N is the specified output digest size.

These functions are synonymous.

## Syntax

Copy code

```
SHA2( <msg> [, <digest_size>] )

SHA2_HEX( <msg> [, <digest_size>] )
```

## Arguments

**Required:**

`msg`
:   A string expression, the message to be hashed

**Optional:**

`digest_size`
:   Size (in bits) of the output, corresponding to the
    specific SHA-2 function used to encrypt the string:

    > 224 = SHA-224
    >
    > 256 = SHA-256 (Default)
    >
    > 384 = SHA-384
    >
    > 512 = SHA-512

    SHA-512/224 and SHA-512/256 are not supported.

## Returns

The data type of the returned value is VARCHAR.

## Usage notes

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
SELECT sha2('Snowflake', 224);

----------------------------------------------------------+
                  SHA2('SNOWFLAKE', 224)                  |
----------------------------------------------------------+
 6267d3d7a59929e6864dd4b737d98e3ef8569d9f88a7466647838532 |
----------------------------------------------------------+
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
> > SELECT v, v_as_sha2, v_as_sha2_hex
> >   FROM sha_table
> >   ORDER BY v;
> > +-------+------------------------------------------------------------------+------------------------------------------------------------------+
> > | V     | V_AS_SHA2                                                        | V_AS_SHA2_HEX                                                    |
> > |-------+------------------------------------------------------------------+------------------------------------------------------------------|
> > | AbCd0 | e1d8ba27889d6782008f495473278c4f071995c5549a976e4d4f93863ce93643 | e1d8ba27889d6782008f495473278c4f071995c5549a976e4d4f93863ce93643 |
> > +-------+------------------------------------------------------------------+------------------------------------------------------------------+
> > ```
