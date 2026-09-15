Categories:
:   [Encryption functions](/sql-reference/functions-encryption)

# DECRYPT

Decrypts a BINARY value using a VARCHAR passphrase.

See also:
:   [ENCRYPT](/sql-reference/functions/encrypt) , [ENCRYPT\_RAW](/sql-reference/functions/encrypt_raw) , [DECRYPT\_RAW](/sql-reference/functions/decrypt_raw) , [TRY\_DECRYPT](/sql-reference/functions/try_decrypt) , [TRY\_DECRYPT\_RAW](/sql-reference/functions/try_decrypt_raw)

## Syntax

Copy code

```
DECRYPT( <value_to_decrypt> , <passphrase> ,
         [ [ <additional_authenticated_data> , ] <encryption_method> ]
       )
```

## Arguments

**Required:**

`value_to_decrypt`
:   The BINARY value to decrypt.

`passphrase`
:   The passphrase to use to encrypt/decrypt the data. The passphrase is a VARCHAR.

**Optional:**

`additional_authenticated_data`
:   Additional authenticated data (AAD) is additional data whose confidentiality and authenticity is assured during the
    decryption process. However, this AAD is not encrypted and is not included as a field in the returned value from the
    ENCRYPT or ENCRYPT\_RAW function.

    If AAD is passed to the encryption function (ENCRYPT or ENCRYPT\_RAW), then the same AAD must be passed to the
    decryption function (DECRYPT or DECRYPT\_RAW). If the AAD passed to the decryption function does not match the
    AAD passed to the encryption function, then decryption fails.

    The difference between the AAD and the `passphrase` is that the passphrase is intended to be kept
    secret (otherwise, the encryption is essentially worthless) while the AAD can be left public. The AAD helps
    authenticate that a public piece of information and an encrypted value are associated with each other. The
    examples section in the [ENCRYPT](/sql-reference/functions/encrypt) function includes an example showing the behavior
    when the AAD matches and the behavior when it doesn’t match.

    For ENCRYPT\_RAW and DECRYPT\_RAW, the data type of the AAD should be BINARY.
    For ENCRYPT and DECRYPT, the data type of the AAD can be either VARCHAR or BINARY, and does not need to match
    the data type of the value that was encrypted.

    AAD is supported only by AEAD-enabled encryption modes like GCM (default).

`encryption_method`
:   This string specifies the method to use for encrypting/decrypting the data. This string contains subfields:

    Copy code

    ```
    <algorithm>-<mode> [ /pad: <padding> ]
    ```

    The `algorithm` is currently limited to:

    > - `'AES'`: When a passphrase is passed (e.g. to ENCRYPT), the function uses AES-256 encryption (256 bits). When a key
    >   is passed (e.g. to ENCRYPT\_RAW), the function uses 128, 192, or 256-bit encryption, depending upon the key
    >   length.

    The `algorithm` is case-insensitive.

    The `mode` specifies which block cipher mode should be used to encrypt messages.
    The following table shows which modes are supported, and which of those modes support padding:

    | Mode | Padding | Description |
    | --- | --- | --- |
    | `'ECB'` | Yes | Encrypt every block individually with the key. This mode is generally discouraged and is included only for compatibility with external implementations. |
    | `'CBC'` | Yes | The encrypted block is XORed with the previous block. |
    | `'GCM'` | No | Galois/Counter Mode is a high-performance encryption mode that is AEAD-enabled. AEAD additionally assures the authenticity and confidentiality of the encrypted data by generating an AEAD tag. Moreover, AEAD supports AAD (additional authenticated data). |
    | `'CTR'` | No | Counter mode. |
    | `'OFB'` | No | Output feedback. The ciphertext is XORed with the plaintext of a block. |
    | `'CFB'` | No | Cipher feedback is a combination of OFB and CBC. |

    Expand

    Show lessSee more

    The `mode` is case-insensitive.

    The `padding` specifies how to pad messages whose length is not a multiple of the block size. Padding is
    applicable only for ECB and CBC modes; padding is ignored for other modes. The possible values for padding are:

    > - `'PKCS'`: Uses PKCS5 for block padding.
    > - `'NONE'`: No padding. The user needs to take care of the padding when using ECB or CBC mode.

    The `padding` is case-insensitive.

    Default setting: `'AES-GCM'`.

    If the `mode` is not specified, GCM is used.

    If the `padding` is not specified, PKCS is used.

## Returns

Returns the decrypted value as a BINARY value. If the original value before encryption was VARCHAR, you must
explicitly convert the returned BINARY back to VARCHAR. For example:

Copy code

```
... TO_VARCHAR(DECRYPT(ENCRYPT('secret', 'key'), 'key'), 'utf-8') ...
```

For more complete examples, see the [Examples](#examples) below.

## Usage notes

- To decrypt data encrypted by `ENCRYPT()`, use `DECRYPT()`. Do not use `DECRYPT_RAW()`.
- To decrypt data encrypted by `ENCRYPT_RAW()`, use `DECRYPT_RAW()`. Do not use `DECRYPT()`.
- The function’s parameters are masked for security. Sensitive information such as the following is
  not visible in the query log and is not visible to Snowflake:

  - The string or binary value to encrypt or decrypt.
  - The passphrase or key.
- The functions use a FIPS-compliant cryptographic library to effectively perform the encryption and decryption.
- The passphrase or key used to decrypt a piece of data must be the same as the passphrase or key used to encrypt that
  data.

- The passphrase can be of arbitrary length, even 0 (the empty string). However, Snowflake
  strongly recommends using a passphrase that is at least 8 bytes.
- Snowflake recommends that the passphrase follow general best practices for passwords, such as using a mix of
  uppercase letters, lowercase letters, numbers, and punctuation.
- The passphrase is not used directly to encrypt/decrypt the input. Instead, the passphrase is used to derive an
  encryption/decryption key, which is always the same for the same passphrase. Snowflake uses the
  <https://en.wikipedia.org/wiki/PBKDF2> key-derivation function with a Snowflake-internal seed to compute the
  encryption/decryption key from the given passphrase.

  Because of this key derivation, the encrypt/decrypt function cannot be used to:

  - Decrypt data that was externally encrypted.
  - Encrypt data that will be externally decrypted.

  To do either of these, use [ENCRYPT\_RAW](/sql-reference/functions/encrypt_raw) or [DECRYPT\_RAW](/sql-reference/functions/decrypt_raw).

## Examples

The code below shows a simple example of encryption and decryption:

> Copy code
>
> ```
> SET passphrase='poiuqewjlkfsd';
> ```
>
> Copy code
>
> ```
> SELECT
>     TO_VARCHAR(
>         DECRYPT(
>             ENCRYPT('Patient tested positive for COVID-19', $passphrase),
>             $passphrase),
>         'utf-8')
>         AS decrypted
>     ;
> +--------------------------------------+
> | DECRYPTED                            |
> |--------------------------------------|
> | Patient tested positive for COVID-19 |
> +--------------------------------------+
> ```

This example decrypts a BINARY value with a simple passphrase. In this example, binary values are shown in
[hexadecimal](/sql-reference/binary-input-output#label-hexadecimal-format-for-binary-data) format. The value of the encrypted data
might vary due to the randomness of the initialization vector (described briefly in [ENCRYPT](/sql-reference/functions/encrypt)).

> Copy code
>
> ```
> ALTER SESSION SET BINARY_OUTPUT_FORMAT='hex';
> ```
>
> Copy code
>
> ```
> CREATE TABLE binary_table (
>     binary_column BINARY,
>     encrypted_binary_column BINARY);
> INSERT INTO binary_table (binary_column)
>     SELECT (TO_BINARY(HEX_ENCODE('Hello')));
> UPDATE binary_table
>     SET encrypted_binary_column = ENCRYPT(binary_column, 'SamplePassphrase');
> ```
>
> Copy code
>
> ```
> SELECT 'Hello' as original_value,
>        binary_column,
>        hex_decode_string(to_varchar(binary_column)) as decoded,
>        -- encrypted_binary_column,
>        decrypt(encrypted_binary_column, 'SamplePassphrase') as decrypted,
>        hex_decode_string(to_varchar(decrypt(encrypted_binary_column, 'SamplePassphrase'))) as decrypted_and_decoded
>     FROM binary_table;
> +----------------+---------------+---------+------------+-----------------------+
> | ORIGINAL_VALUE | BINARY_COLUMN | DECODED | DECRYPTED  | DECRYPTED_AND_DECODED |
> |----------------+---------------+---------+------------+-----------------------|
> | Hello          | 48656C6C6F    | Hello   | 48656C6C6F | Hello                 |
> +----------------+---------------+---------+------------+-----------------------+
> ```

This example shows how to use an alternative mode (`CBC`) as part of the specifier for the encryption method.
This encryption method also specifies a padding rule (`PKCS`). In this example, the AAD parameter is NULL.

> Copy code
>
> ```
> select encrypt(to_binary(hex_encode('secret!')), 'sample_passphrase', NULL, 'aes-cbc/pad:pkcs') as encrypted_data;
> ```

This example shows how to use the AAD:

Copy code

```
SELECT
    TO_VARCHAR(
        DECRYPT(
            ENCRYPT('penicillin', $passphrase, 'John Dough AAD', 'aes-gcm'),
            $passphrase, 'John Dough AAD', 'aes-gcm'),
        'utf-8')
        AS medicine
    ;
+------------+
| MEDICINE   |
|------------|
| penicillin |
+------------+
```

If you pass the wrong AAD, decryption fails:

Copy code

```
SELECT
    DECRYPT(
        ENCRYPT('penicillin', $passphrase, 'John Dough AAD', 'aes-gcm'),
        $passphrase, 'wrong patient AAD', 'aes-gcm') AS medicine
    ;
```

Copy code

```
100311 (22023): Decryption failed. Check encrypted data, key, AAD, or AEAD tag.
```
