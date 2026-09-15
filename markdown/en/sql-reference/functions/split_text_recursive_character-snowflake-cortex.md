Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# SPLIT\_TEXT\_RECURSIVE\_CHARACTER (SNOWFLAKE.CORTEX)

The SPLIT\_TEXT\_RECURSIVE\_CHARACTER function splits a string into shorter stings, recursively, for preprocessing
text to be used with text embedding or search indexing functions. The function returns an array of text chunks, where the
chunks are derived from the original text based on the input parameters provided.

The splitting algorithm attempts to split text on separators in the order they are provided, either implicitly as defaults based on the
format, or explicitly in the `separators` argument. Splitting is then applied to each chunk that is longer than the specified
`chunk_size`, recursively, until all chunks no longer than the specified `chunk_size`.

For example, if format is set to `'none'`, the algorithm first splits on the “\n\n” sequences, which represent
paragraph breaks in most formats. Within any resulting chunk that is still longer than `chunk_size` characters, the
function splits on the “\n” characters, which represents line breaks. This process repeats until each of the chunks is less
than `chunk_size` characters.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER (
  '<text_to_split>',
  '<format>',
  <chunk_size>,
  [ <overlap> ],
  [ <separators> ]
)
```

## Arguments

**Required:**

`'text_to_split'`
:   The text to split.

`'format'`
:   The format of your input text, which determines the default separators in the splitting algorithm. Must be one of the following:

    > - `none`: No format-specific separators. Only the separators in the `separators` field are used for splitting.
    > - `markdown`: Separates on headers, code blocks, and tables, in addition to any separators in the separators field.

`chunk_size`
:   An integer specifying the maximum number of characters in each chunk. The value must be greater than zero.

**Optional:**

`overlap`
:   An integer that specifies the number of characters to overlap between consecutive chunks. By default, chunks have no overlap.
    If `overlap` is specified, it must be smaller than the `chunk_size` argument.

    Overlap is useful for ensuring that each chunk has some context about the previous chunk. This can help improve the quality of search
    results or other processing.

`separators`
:   An ordered list of character sequences to use as boundaries when determining where to split the text, in addition to
    any separators dictated by the `format` parameter. The last item in this list should be a general separator, such
    as an empty string (which allows a split to be made between any two characters), so that the algorithm is guaranteed to
    be able to split the text into chunks of the desired size.

    Default: [“\n\n”, “\n”, “ “, “”], meaning a paragraph break, a line break, a space, and between any two characters (the empty string).

## Returns

Returns an array of strings that contains text chunks extracted from the input string.

## Examples

### Simple usage

The following example directly calls the SPLIT\_TEXT\_RECURSIVE\_CHARACTER function with the input text `hello world are you here`.
The function splits the text into chunks of 15 characters each, with an overlap of 10 characters between chunks.

Copy code

```
SELECT SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER (
   'hello world are you here',
   'none',
   15,
   10
);
```

```
['hello world are', 'world are you', 'are you here']
```

### Example with Markdown formatting and flattening of chunks array into rows

The following example creates a table `sample_documents` containing a short Markdown document in each row, then
calls the SPLIT\_TEXT\_RECURSIVE\_CHARACTER function to split each document. The function splits the text into chunks of 25
characters each, with an overlap of 10 characters between chunks.

Copy code

```
-- Create sample markdown data table
CREATE OR REPLACE TABLE sample_documents (
   doc_id INT AUTOINCREMENT, -- Monotonically increasing integer
   document STRING
);

-- Insert sample data
INSERT INTO sample_documents (document)
VALUES
   ('### Heading 1\\nThis is a sample markdown document. It contains a list:\\n- Item 1\\n- Item 2\\n- Item 3\\n'),
   ('## Subheading\\nThis markdown contains a link [example](http://example.com) and some \**bold*\* text.'),
   ('### Heading 2\\nHere is a code snippet:\\n```\\ncode_block_here()\\n```\\nAnd some more regular text.'),
   ('## Another Subheading\\nMarkdown example with \_italic\_ text and a [second link](http://example.com).'),
   ('### Heading 3\\nText with an ordered list:\\n1. First item\\n2. Second item\\n3. Third item\\nMore text follows here.');

-- split text
SELECT
   doc_id,
   c.value
FROM
   sample_documents,
   LATERAL FLATTEN( input => SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER (
      document,
      'markdown',
      25,
      10
   )) c;
```
