Categories:
:   [String & binary functions](/sql-reference/functions-string) (Compression/Decompression)

# DECOMPRESS\_BINARY

Decompresses the compressed `BINARY` input parameter.

See also:
:   [COMPRESS](/sql-reference/functions/compress) , [DECOMPRESS\_STRING](/sql-reference/functions/decompress_string)

## Syntax

Copy code

```
DECOMPRESS_BINARY(<input>, <method>)
```

## Arguments

**Required:**

`input`
:   A `BINARY` value (or expression) with data that was compressed using one
    of the compression methods specified in [COMPRESS](/sql-reference/functions/compress).

    If you attempt to decompress a compressed string, rather than a
    compressed `BINARY` value, you do not get an error; instead, the function
    returns a `BINARY` value. See the Usage Notes below for details.

`method`
:   The compression method originally used to compress the `input`.
    See [COMPRESS](/sql-reference/functions/compress) for a list of compression
    methods.

    The `DECOMPRESS_BINARY` method, unlike the `COMPRESS` method, does
    not require you to specify the compression level. If you do specify
    the compression level, `DECOMPRESS_BINARY` ignores it and uses the actual
    compression level.

## Returns

The data type of the returned value is `BINARY`.

## Usage notes

- If the compression method is unknown or invalid, the query fails.
- The compression method name (e.g. `ZLIB`) is case-insensitive.
- The `DECOMPRESS_BINARY` function can decompress data that was
  originally in string format. However, the output of `DECOMPRESS_BINARY`
  is still `BINARY`, not string. For example,
  `SELECT DECOMPRESS_BINARY(COMPRESS('Hello', 'SNAPPY), 'SNAPPY')` returns a
  `BINARY` value; if you display that value, it is shown as
  `48656C6C6F`, which is the hexadecimal representation of ‘Hello’.
  To avoid confusion, Snowflake recommends decompressing string data
  by using [DECOMPRESS\_STRING](/sql-reference/functions/decompress_string) rather than `DECOMPRESS_BINARY`.

## Returns

A `BINARY` value with decompressed data.

## Examples

This shows a simple example of decompressing `BINARY` data that contains
a compressed value.

Copy code

```
SELECT DECOMPRESS_BINARY(TO_BINARY('0920536E6F77666C616B65', 'HEX'), 'SNAPPY');
+-------------------------------------------------------------------------+
| DECOMPRESS_BINARY(TO_BINARY('0920536E6F77666C616B65', 'HEX'), 'SNAPPY') |
|-------------------------------------------------------------------------|
| 536E6F77666C616B65                                                      |
+-------------------------------------------------------------------------+
```
