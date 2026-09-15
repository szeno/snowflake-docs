# ModifyCompression 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-compress-nar

## Description

Changes the compression algorithm used to compress the contents of a FlowFile by decompressing the contents of FlowFiles using a user-specified compression algorithm and recompressing the contents using the specified compression format properties. This processor operates in a very memory efficient way so very large objects well beyond the heap size are generally fine to process

## Tags

brotli, bzip2, compress, content, deflate, gzip, lz4-framed, lzma, recompress, snappy, snappy framed, snappy-hadoop, xz-lzma2, zstd

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Input Compression Strategy | The strategy to use for decompressing input FlowFiles |
| Output Compression Level | The compression level for output FlowFiles for supported formats. A lower value results in faster processing but less compression; a value of 0 indicates no (that is, simple archiving) for gzip or minimal for xz-lzma2 compression. Higher levels can mean much larger memory usage such as the case with levels 7-9 for xz-lzma/2 so be careful relative to heap size. |
| Output Compression Strategy | The strategy to use for compressing output FlowFiles |
| Output Filename Strategy | Processing strategy for filename attribute on output FlowFiles |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles will be transferred to the failure relationship on compression modification errors |
| success | FlowFiles will be transferred to the success relationship on compression modification success |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | The appropriate MIME Type is set based on the value of the Compression Format property. If the Compression Format is ‘no compression’ this attribute is removed as the MIME Type is no longer known. |

Expand

Show lessSee more
