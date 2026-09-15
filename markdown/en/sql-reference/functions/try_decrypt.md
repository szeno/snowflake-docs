Categories:
:   [Encryption functions](/sql-reference/functions-encryption)

# TRY\_DECRYPT

A special version of [DECRYPT](/sql-reference/functions/decrypt) that returns a NULL
value if an error occurs during decryption.

See also:
:   [ENCRYPT](/sql-reference/functions/encrypt) , [ENCRYPT\_RAW](/sql-reference/functions/encrypt_raw) , [DECRYPT](/sql-reference/functions/decrypt) , [DECRYPT\_RAW](/sql-reference/functions/decrypt_raw) , [TRY\_DECRYPT\_RAW](/sql-reference/functions/try_decrypt_raw)

## Syntax

Copy code

```
TRY_DECRYPT( <value_to_decrypt> , <passphrase> ,
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

Returns the decrypted value as a BINARY value or a NULL value if any runtime
error occurs during decryption.

## Usage notes and examples

See the [DECRYPT](/sql-reference/functions/decrypt) function for the usage notes and examples.
