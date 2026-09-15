Categories:
:   [String & binary functions](/sql-reference/functions-string) (Compression/Decompression)

# COMPRESS

Compresses the input string or binary value with a compression method.

See also:
:   [DECOMPRESS\_BINARY](/sql-reference/functions/decompress_binary) , [DECOMPRESS\_STRING](/sql-reference/functions/decompress_string)

## Syntax

Copy code

```
COMPRESS(<input>, <method>)
```

## Arguments

**Required:**

`input`
:   A `BINARY` or string value (or expression) to be compressed.

`method`
:   A string with compression method and optional compression level. Supported
    methods are:

    - `SNAPPY`.
    - `ZLIB`.
    - `ZSTD`.
    - `BZ2`.

    The compression level is specified in parentheses, for example:
    `zlib(1)`. The compression level is a non-negative integer. `0` means
    default level (same as omitting the compression level). The compression
    level is ignored if the method doesn’t support compression levels.

## Returns

A `BINARY` with compressed data.

## Usage notes

- If the compression method is unknown or invalid, the query fails.
- The compression method name (e.g. `ZLIB`) is case-insensitive.
- Not all inputs are compressible. For very short or difficult-to-compress
  input values, the output value might be the same length as, or even slightly
  longer than, the input value.

## Examples

The example below shows how to use the `COMPRESS` function with the
`SNAPPY` compression method.

The output of the function is `BINARY`, but SNOWSQL displays the output as a
string of hexadecimal characters for readability.

Copy code

```
SELECT COMPRESS('Snowflake', 'SNAPPY');
+---------------------------------+
| COMPRESS('SNOWFLAKE', 'SNAPPY') |
|---------------------------------|
| 0920536E6F77666C616B65          |
+---------------------------------+
```
