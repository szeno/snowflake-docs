# CompressContent 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Compresses or decompresses the contents of FlowFiles using a user-specified compression algorithm and updates the mime.type attribute as appropriate. A common idiom is to precede CompressContent with IdentifyMimeType and configure Mode=’decompress’ AND Compression Format=’use mime.type attribute’. When used in this manner, the MIME type is automatically detected and the data is decompressed, if necessary. If decompression is unnecessary, the data is passed through to the ‘success’ relationship. This processor operates in a very memory efficient way so very large objects well beyond the heap size are generally fine to process.

## Tags

brotli, bzip2, compress, content, decompress, deflate, gzip, lz4-framed, lzma, snappy, snappy framed, snappy-hadoop, xz-lzma2, zstd

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Compression Format | The compression format to use. Valid values are: GZIP, Deflate, ZSTD, BZIP2, XZ-LZMA2, LZMA, Brotli, Snappy, Snappy Hadoop, Snappy Framed, and LZ4-Framed |
| Compression Level | The compression level to use; this is valid only when using gzip, deflate or xz-lzma2 compression. A lower value results in faster processing but less compression; a value of 0 indicates no (that is, simple archiving) for gzip or minimal for xz-lzma2 compression. Higher levels can mean much larger memory usage such as the case with levels 7-9 for xz-lzma/2 so be careful relative to heap size. |
| Mode | Indicates whether the processor should compress content or decompress content. Must be either ‘compress’ or ‘decompress’ |
| Update Filename | If true, will remove the filename extension when decompressing data (only if the extension indicates the appropriate compression format) and add the appropriate extension when compressing data |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles will be transferred to the failure relationship if they fail to compress/decompress |
| success | FlowFiles will be transferred to the success relationship after successfully being compressed or decompressed |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | If the Mode property is set to compress, the appropriate MIME Type is set. If the Mode property is set to decompress and the file is successfully decompressed, this attribute is removed, as the MIME Type is no longer known. |

Expand

Show lessSee more

## Use cases

| Compress the contents of a FlowFile |
| --- |
| Decompress the contents of a FlowFile |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Check whether or not a FlowFile is compressed and if so, decompress it. |
| --- |

Expand

Show lessSee more
