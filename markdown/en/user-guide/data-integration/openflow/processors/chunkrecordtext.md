# ChunkRecordText 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-chunking-nar

## Description

Chunks text with options for recursively splitting by delimiters and max character length. The input text is expected to be in a record-oriented FlowFile that matches the configured Record Reader format.

## Tags

chunk, openflow, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Chunk Count Field Name | The field name in the record to write the total number of chunks created from the original record. |
| Chunk Delimiters | Specifies a comma-separated list of character sequences. Meta-characters n, r and t are automatically un-escaped. Delimiters are recursively applied in order to chunk the text. |
| Chunk Index Field Name | The field name in the record to write the chunk index. |
| Chunk Overlap | The max number of characters to include from preceding and subsequent chunks. |
| Chunking Strategy | Strategy to chunk text. ‘Recursive Delimiters’ will chunk text according to the recursive split by character algorithm. In this algorithm input text is split by the first delimiter and merged back into chunks that do not exceed the ‘Max Chunk Length’. Any splits that exceed ‘Max Chunk Length’ are then recursively split using the next delimiter. ‘Max Chunk Length’ will chunk text by creating chunks that are ‘Max Chunk Length’ in size. |
| Language | Language to use for parsing sentences. |
| Max Chunk Length | Maximum number of characters to include in output chunk. Setting this number too high can result in an out of memory error. |
| Record Reader | The Record Reader to use for reading the FlowFile. |
| Record Writer | The Record Writer to use for writing the results. |
| Sentence Similarity Threshold | Threshold for determining if two sentences are similar enough to occupy the same chunk. A value of 1.0 indicates the sentences are identical. A value of 0.0 indicates the sentences are completely dissimilar. |
| Text Record Path | The record path to a text field in the record. |
| Trim Whitespace | Trim whitespace surrounding the output text chunk. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| original | The input Flow File is routed to the original relationship. |
| success | Text chunks are routed to the success relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| chunk.strategy | Strategy used to chunk text. One of ‘Max Chunk Length’, ‘Recursive Delimiters’, ‘Sentence’, ‘Semantic’. |
| chunk.semantic.threshold | Threshold for determining if two sentences are similar enough to occupy the same chunk. This attribute is added only when the ‘Semantic’ chunking strategy is used. |
| chunk.language | Language used for parsing sentences. This attribute is added only when the ‘Sentence’ or ‘Semantic’ chunking strategy is used. |
| chunk.delimiters | Comma-separated list of delimiters used to chunk text. This attribute is added only when the ‘Recursive Delimiters’ chunking strategy is used. |
| chunk.max.chars | Maximum number of characters to include in each chunk. |

Expand

Show lessSee more
