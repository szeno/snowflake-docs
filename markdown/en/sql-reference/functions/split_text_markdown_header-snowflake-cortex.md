Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# SPLIT\_TEXT\_MARKDOWN\_HEADER (SNOWFLAKE.CORTEX)

The SPLIT\_TEXT\_MARKDOWN\_HEADER function splits a Markdown-formatted document into structured text chunks
based on header levels. The function returns an array of objects, where each object contains the text
chunk and the associated headers under which that chunk falls.

This function is useful for preserving document structure when chunking content for embedding,
retrieval-augmented generation (RAG), or search indexing.

The function first segments the input text using the specified Markdown headers, and then recursively
splits each segment using default plain text separators (e.g., *[“nn”, “n”, “ “, “”]*) to produce chunks
of the desired size.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.SPLIT_TEXT_MARKDOWN_HEADER (
  '<text_to_split>',
  '<headers_to_split_on>',
  <chunk_size>,
  [ <overlap> ]
)
```

## Arguments

**Required:**

`'text_to_split'`
:   A Markdown-formatted string to be split.

`'headers_to_split_on'`
:   A key-value map in which the keys are Markdown header syntax (e.g., *#*, *##*) and the values are metadata field names (e.g., *header\_1*, *header\_2*) to label the chunks. For example:

    Copy code

    ```
    {
      "#": "header_1",
      "##": "header_2"
    }
    ```

    This configuration will split the document on *#* and *##* headers. In the output, *header\_1* and *header\_2* fields will contain the corresponding header text values.

`chunk_size`
:   An integer specifying the maximum number of characters in each chunk. The value must be greater than zero.

**Optional:**

`overlap`
:   An integer specifying the number of characters to overlap between consecutive chunks. Defaults to 0 if not provided.

    Overlap is useful for maintaining context across chunks, which can improve performance in embedding and retrieval tasks.

## Returns

Returns an array of objects. Each object has the following structure:

- `chunk`: A string containing the extracted text.
- `headers`: A dictionary containing the Markdown header values under which the chunk is nested. Keys match those provided in the `headers_to_split_on` map.

## Examples

### Simple usage

The following example splits a Markdown string on both *#* and *##* headers, produces chunks of up to 12 characters, and applies a 5-character overlap between chunks.

Copy code

```
SELECT SNOWFLAKE.CORTEX.SPLIT_TEXT_MARKDOWN_HEADER(
  '# HEADER 1\nthis is text in header 1\n## HEADER 2\nthis is a subheading',
  OBJECT_CONSTRUCT('#', 'header_1', '##', 'header_2'),
  12,
  5
);
```

```
[
  {
    "chunk": "this is text",
    "headers": {
      "header_1": "HEADER 1"
    }
  },
  {
    "chunk": "text in",
    "headers": {
      "header_1": "HEADER 1"
    }
  },
  {
    "chunk": "in header 1",
    "headers": {
      "header_1": "HEADER 1"
    }
  },
  {
    "chunk": "this is a",
    "headers": {
      "header_1": "HEADER 1",
      "header_2": "HEADER 2"
    }
  },
  {
    "chunk": "subheading",
    "headers": {
      "header_1": "HEADER 1",
      "header_2": "HEADER 2"
    }
  }
]
```

### Example with Markdown formatting and flattening of results into rows

The following example creates a table `markdown_docs` containing a short Markdown document in each row, then
calls the SPLIT\_TEXT\_MARKDOWN\_HEADER function to segment each document on markdown headers ‘#’ and ‘##’. The function
then splits each segment into chunks of 20 characters each, with an overlap of 5 characters between chunks.

Copy code

```
CREATE OR REPLACE TABLE markdown_docs (doc VARCHAR);

INSERT INTO markdown_docs VALUES
('# Product Overview\nOur system is a high-performance data processing engine.\n\n## Architecture\nIt uses a distributed design optimized for analytics.\n\n## Key Benefits\n- Scalable\n- Cost-efficient\n- Secure'),
('# User Guide\nThis guide describes how to install and use the product.\n\n## Installation\nFollow the steps below to install.\n\n## Usage\nOnce installed, use the CLI or UI for operations.'),
('# FAQ\nHere are answers to commonly asked questions.\n\n## Pricing\nWe offer flexible pricing models.\n\n## Support\nContact our 24/7 support team anytime.');

SELECT
    c.value['chunk']::varchar as chunk,
    c.value['headers']::object as headers,
FROM
    markdown_docs,
    LATERAL FLATTEN(
        SNOWFLAKE.CORTEX.SPLIT_TEXT_MARKDOWN_HEADER(
        doc,
        OBJECT_CONSTRUCT('#', 'header_1', '##', 'header_2'),
        20,
        5
    )
    ) c;
```
