# ChunkText 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-chunking-nar

## Description

Chunks text with options for recursively splitting by delimiters and max character length. Each chunk is given the following attributes: fragment.identifier, fragment.index, fragment.count, segment.original.filename; these attributes can then be used by the MergeContent processor in order to reconstitute the original FlowFile

## Tags

chunk, openflow, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Chunk Delimiters | Specifies a comma-separated list of character sequences. Meta-characters n, r and t are automatically un-escaped. Delimiters are recursively applied in order to chunk the text. |
| Chunk Overlap | The max number of characters to include from preceding and subsequent chunks. |
| Chunking Strategy | Strategy to chunk text. ‘Recursive Delimiters’ will chunk text according to the recursive split by character algorithm. In this algorithm input text is split by the first delimiter and merged back into chunks that do not exceed the ‘Max Chunk Length’. Any splits that exceed ‘Max Chunk Length’ are then recursively split using the next delimiter. ‘Max Chunk Length’ will chunk text by creating chunks that are ‘Max Chunk Length’ in size. |
| Language | Language to use for parsing sentences. |
| Max Chunk Length | Maximum number of characters to include in output chunk. Setting this number too high can result in an out of memory error. |
| Sentence Similarity Threshold | Threshold for determining if two sentences are similar enough to occupy the same chunk. A value of 1.0 indicates the sentences are identical. A value of 0.0 indicates the sentences are completely dissimilar. |
| Trim Whitespace | Trim whitespace surrounding the output text chunk. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If any error during parsing occurs, the input Flow File will be routed to the failure relationship. |
| original | The input Flow File is routed to the original relationship. |
| success | Text chunks are routed to the success relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| segment.original.filename | Original filename of the input Flow File. |
| fragment.identifier | ID of the parent Flow File used to generate each chunk. |
| fragment.index | Index of the current Flow File chunk, starting at 0. |
| fragment.count | The total count of Flow File chunks produced. |
| chunk.start.offsets | The chunk.start.offsets attribute is added only to the original incoming FlowFile. It is a comma-separated list of start offsets for each chunk that gets generated. For example, if the FlowFile is chunked into 3 child FlowFiles, it might have a value of *0,183,365* indicating that the first chunk starts at offset 0, the second chunk starts at offset 183, and the third chunk starts at offset 365. Offsets are based on the number of characters. |
| chunk.end.offsets | The chunk.end.offsets attribute is added only to the original incoming FlowFile. It is a comma-separated list of end offsets for each chunk that gets generated. For example, if the FlowFile is chunked into 3 child FlowFiles, it might have a value of *183,365,548* indicating that the first chunk ends at offset 183, the second chunk ends at offset 365, and the third chunk ends at offset 548. Offsets are based on the number of characters. |
| chunk.strategy | Strategy used to chunk text. One of ‘Max Chunk Length’, ‘Recursive Delimiters’, ‘Sentence’, ‘Semantic’. |
| chunk.semantic.threshold | Threshold for determining if two sentences are similar enough to occupy the same chunk. This attribute is added only when the ‘Semantic’ chunking strategy is used. |
| chunk.language | Language used for parsing sentences. This attribute is added only when the ‘Sentence’ or ‘Semantic’ chunking strategy is used. |
| chunk.delimiters | Comma-separated list of delimiters used to chunk text. This attribute is added only when the ‘Recursive Delimiters’ chunking strategy is used. |
| chunk.max.chars | Maximum number of characters to include in each chunk. |

Expand

Show lessSee more
