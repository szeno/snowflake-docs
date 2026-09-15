Categories:
:   [Encryption functions](/sql-reference/functions-encryption)

# ENCRYPT\_RAW

Encrypts a BINARY value using a BINARY key.

See also:
:   [ENCRYPT](/sql-reference/functions/encrypt) , [DECRYPT](/sql-reference/functions/decrypt) , [DECRYPT\_RAW](/sql-reference/functions/decrypt_raw) , [TRY\_DECRYPT](/sql-reference/functions/try_decrypt) , [TRY\_DECRYPT\_RAW](/sql-reference/functions/try_decrypt_raw)

## Syntax

Copy code

```
ENCRYPT_RAW( <value_to_encrypt> , <key> , <iv> ,
         [ [ <additional_authenticated_data> , ] <encryption_method> ]
       )
```

## Arguments

**Required:**

`value_to_encrypt`
:   The binary value to encrypt.

`key`
:   The key to use to encrypt/decrypt the data. The key must be a BINARY value. The key can be any value as long as the
    length is correct. For example, for AES128, the key must be 128 bits (16 bytes), and for AES256, the key must be
    256 bits (32 bytes).

    The key used to encrypt the value must be used to decrypt the value.

`iv`
:   This parameter contains the Initialization Vector (IV) to use to encrypt and decrypt this piece of
    data. The IV must be a BINARY value of a specific length:

    - For GCM, this field must be 96 bits (12 bytes). While the GCM encryption method allows this field to be a different
      size, Snowflake currently only supports 96 bits.
    - For CCM, this should be 56 bits (7 bytes).
    - For ECB, this parameter is unneeded.
    - For all other supported encryption modes, this should be 128 bits (16 bytes).

    This value is used to initialize the first encryption round. You should never use the same IV and key combination
    more than once, especially for encryption modes like GCM.

    If this parameter is set to NULL, the implementation will choose a new pseudo-random IV during each call.

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

The function returns the encrypted value. The data type of the returned value is VARIANT.

Although only a single value is returned, that value contains two or three fields:

- The first field is the initialization vector (IV). Both encryption and decryption use the IV.
- The second field is the ciphertext (encrypted value) of the `value_to_encrypt`.
- If the encryption mode is AEAD-enabled, then the returned value also contains a third field, which is the AEAD tag.

The IV and tag size depend on the encryption mode.

All 3 fields within the VARIANT are of type BINARY.

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

## Examples

This example shows encryption and decryption.

> For readability, set the BINARY\_OUTPUT\_FORMAT to HEX:
>
> Copy code
>
> ```
> _to_hex
> ALTER SESSION SET BINARY_OUTPUT_FORMAT='HEX';
> ```
>
> Create a table and load it.
>
> Caution
>
> To simplify this example, the encryption/decryption key is stored in the table with the value that has
> been encrypted. This is insecure; the key should never be stored as an unencrypted value in the table
> that stores the encrypted data.
>
> Copy code
>
> ```
> CREATE OR REPLACE TABLE binary_table (
>     encryption_key BINARY,   -- DO NOT STORE REAL ENCRYPTION KEYS THIS WAY!
>     initialization_vector BINARY(12), -- DO NOT STORE REAL IV'S THIS WAY!!
>     binary_column BINARY,
>     encrypted_binary_column VARIANT,
>     aad_column BINARY);
>
> INSERT INTO binary_table (encryption_key,
>                           initialization_vector,
>                           binary_column,
>                           aad_column)
>     SELECT SHA2_BINARY('NotSecretEnough', 256),
>             SUBSTR(TO_BINARY(HEX_ENCODE('AlsoNotSecretEnough'), 'HEX'), 0, 12),
>             TO_BINARY(HEX_ENCODE('Bonjour'), 'HEX'),
>             TO_BINARY(HEX_ENCODE('additional data'), 'HEX')
>     ;
> ```
>
> Encrypt:
>
> Copy code
>
> ```
> UPDATE binary_table SET encrypted_binary_column =
>     ENCRYPT_RAW(binary_column, 
>         encryption_key, 
>         initialization_vector, 
>         aad_column,
>         'AES-GCM');
> +------------------------+-------------------------------------+
> | number of rows updated | number of multi-joined rows updated |
> |------------------------+-------------------------------------|
> |                      1 |                                   0 |
> +------------------------+-------------------------------------+
> ```
>
> This shows the corresponding call to the `DECRYPT_RAW()` function. The initialization vector (IV)
> is taken from the encrypted value; you do not need to store the initialization vector separately. Similarly,
> the AEAD tag is also read from the encrypted value.
>
> Caution
>
> To simplify this example, the encryption/decryption key is read from the table with the value that has
> been encrypted. This is insecure; the key should never be stored as an unencrypted value in the table
> that stores the encrypted data.
>
> Copy code
>
> ```
> SELECT 'Bonjour' as original_value,
>        binary_column,
>        hex_decode_string(to_varchar(binary_column)) as decoded,
>        encrypted_binary_column,
>        decrypt_raw(as_binary(get(encrypted_binary_column, 'ciphertext')),
>                   encryption_key,
>                   as_binary(get(encrypted_binary_column, 'iv')),
>                   aad_column,
>                   'AES-GCM',
>                   as_binary(get(encrypted_binary_column, 'tag')))
>            as decrypted,
>        hex_decode_string(to_varchar(decrypt_raw(as_binary(get(encrypted_binary_column, 'ciphertext')),
>                   encryption_key,
>                   as_binary(get(encrypted_binary_column, 'iv')),
>                   aad_column,
>                   'AES-GCM',
>                   as_binary(get(encrypted_binary_column, 'tag')))
>                   ))
>            as decrypted_and_decoded
>     FROM binary_table;
> +----------------+----------------+---------+---------------------------------------------+----------------+-----------------------+
> | ORIGINAL_VALUE | BINARY_COLUMN  | DECODED | ENCRYPTED_BINARY_COLUMN                     | DECRYPTED      | DECRYPTED_AND_DECODED |
> |----------------+----------------+---------+---------------------------------------------+----------------+-----------------------|
> | Bonjour        | 426F6E6A6F7572 | Bonjour | {                                           | 426F6E6A6F7572 | Bonjour               |
> |                |                |         |   "ciphertext": "CA2F4A383F6F55",           |                |                       |
> |                |                |         |   "iv": "416C736F4E6F745365637265",         |                |                       |
> |                |                |         |   "tag": "91F28FBC6A2FE9B213D1C44B8D75D147" |                |                       |
> |                |                |         | }                                           |                |                       |
> +----------------+----------------+---------+---------------------------------------------+----------------+-----------------------+
> ```
>
> The previous example duplicated a long call to `DECRYPT_RAW()`. You can use a WITH clause to reduce
> the duplication:
>
> Copy code
>
> ```
> WITH
>     decrypted_but_not_decoded as (
>         decrypt_raw(as_binary(get(encrypted_binary_column, 'ciphertext')),
>                       encryption_key,
>                       as_binary(get(encrypted_binary_column, 'iv')),
>                       aad_column,
>                       'AES-GCM',
>                       as_binary(get(encrypted_binary_column, 'tag')))
>     )
> SELECT 'Bonjour' as original_value,
>        binary_column,
>        hex_decode_string(to_varchar(binary_column)) as decoded,
>        encrypted_binary_column,
>        decrypted_but_not_decoded,
>        hex_decode_string(to_varchar(decrypted_but_not_decoded))
>            as decrypted_and_decoded
>     FROM binary_table;
> +----------------+----------------+---------+---------------------------------------------+---------------------------+-----------------------+
> | ORIGINAL_VALUE | BINARY_COLUMN  | DECODED | ENCRYPTED_BINARY_COLUMN                     | DECRYPTED_BUT_NOT_DECODED | DECRYPTED_AND_DECODED |
> |----------------+----------------+---------+---------------------------------------------+---------------------------+-----------------------|
> | Bonjour        | 426F6E6A6F7572 | Bonjour | {                                           | 426F6E6A6F7572            | Bonjour               |
> |                |                |         |   "ciphertext": "CA2F4A383F6F55",           |                           |                       |
> |                |                |         |   "iv": "416C736F4E6F745365637265",         |                           |                       |
> |                |                |         |   "tag": "91F28FBC6A2FE9B213D1C44B8D75D147" |                           |                       |
> |                |                |         | }                                           |                           |                       |
> +----------------+----------------+---------+---------------------------------------------+---------------------------+-----------------------+
> ```
