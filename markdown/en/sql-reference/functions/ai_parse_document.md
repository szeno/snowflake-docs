Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_PARSE\_DOCUMENT

Regional Availability

Available natively to accounts in [select regions](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).
Available through [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) to accounts in all regions.

Returns the extracted content from a document on a Snowflake stage as a JSON-formatted string. This
function supports two types of extraction: Optical Character Recognition (OCR) and layout. For more
information, see [Parsing documents with AI\_PARSE\_DOCUMENT](/user-guide/snowflake-cortex/parse-document).

## Syntax

Copy code

```
AI_PARSE_DOCUMENT( <file_object> [, <options> ] [, <return_error_details> ] )
```

## Arguments

**Required:**

`file_object`
:   A [FILE](/sql-reference/data-types-unstructured#label-data-types-file) object that specifies the document to parse, stored in a Snowflake stage. For
    information about creating file objects, see [TO\_FILE](/sql-reference/functions/to_file).

**Optional:**

`options`
:   An OBJECT value that contains options for parsing documents. The supported keys are shown below. All are optional.

    - `'extract_images'`: If set to TRUE, the function extracts images embedded in the document. Requires LAYOUT mode.
    - `'mode'`: Specifies the parsing mode. The supported modes are:

      - `'OCR'`: The function extracts text only. This is the default mode.
      - `'LAYOUT'`: The function extracts layout as well as text, including structural content such as tables.
    - `'page_split'`: If set to TRUE, the function splits the document into pages and processes each page
      separately. This feature supports only PDF, PowerPoint (`.pptx`), and Word (`.docx`) documents.
      Documents in other formats return an error. The default is FALSE.

      Tip

      To process long documents that exceed the token limit of AI\_PARSE\_DOCUMENT, set this option to TRUE.
    - `'page_filter'`: An array that specifies ranges of pages of a multi-page document to process. Each
      range is an object with `start` and `end` fields that specify the first (inclusive) and last (exclusive) page in
      the range. Page indexes start at 0. For example, `{'start': 0, 'end': 1}` specifies the first page of the
      document.

      Note

      Specifying `page_filter` implies `page_split`. If you specify page ranges, it is not necessary to also set
      `page_split`.

`return_error_details`
:   A BOOLEAN flag that indicates whether to return error details in case of error. When set to TRUE, the function returns
    an OBJECT that contains `value`, `error`, and `metadata` fields. The `value` field contains the parsed document
    data, the `error` field contains the error message (or NULL on success), and `metadata` is a top-level field
    rather than a subfield of the parsed output. See [Error behavior](#error-behavior) for details.

## Returns

A JSON object (as a string) that contains the extracted data and associated metadata. The `options` argument
determines the structure of the returned object.

Tip

To use the output in SQL, convert it to an OBJECT value using the [PARSE\_JSON](/sql-reference/functions/parse_json) function.

If the `'page_split'` option is set, the output has the following structure:

> - `"pages"`: An array of JSON objects, each containing text extracted from the document. If the document has only
>   one page, the output still contains a `"pages"` array (which contains a single object). Each page has the following fields:
>   - `"content"`: Plain text (in OCR mode) or Markdown-formatted text (in LAYOUT mode).
>   - `"index"`: The page index in the file, starting at 0. Page numbers and formats specified in the document are ignored.

If `'page_split'` is FALSE or is not present, the output has the following structure:

> - `"content"`: Plain text (in OCR mode) or Markdown-formatted text (in LAYOUT mode).

Note

Document metadata such as `pageCount` is not included in the output structures above. To return metadata, pass
`TRUE` as the `return_error_details` argument. The function then returns an OBJECT with top-level `value`, `error`,
and `metadata` fields; `metadata` contains fields such as `pageCount`.

If the `"extract_images"` option is set to TRUE, the output includes an additional field:

> - `"images"`: An array of JSON objects, each representing an extracted image. Each image object has the following fields:
>   - `"id"`: A unique identifier for the image.
>   - `"top_left_x"`, `"top_left_y"`, `"bottom_right_x"`, `"bottom_right_y"`: The coordinates of the bounding box of the image on the page.
>   - `"image_base64"`: The extracted image data encoded as a base64 string.

## Error behavior

By default, if AI\_PARSE\_DOCUMENT can’t process the input, the function returns NULL. If the query processes multiple
rows, rows with errors return NULL and don’t prevent the query from completing.

The return value on error depends on the `return_error_details`
argument. The following table shows the return value based on the `return_error_details` argument:

> | `return_error_details` | Return value | Description |
> | --- | --- | --- |
> | FALSE Not passed | NULL |  |
> | TRUE | OBJECT with `value`, `error`, and `metadata` fields | `value`: An OBJECT containing the parsed document data, or NULL if an error occurred. `error`: A VARCHAR value that contains the error message if an error occurred, or NULL if the function succeeded. The `error` field inside `value` (renamed from `errorInformation`) contains per-document error details when present. `metadata`: An OBJECT containing document metadata such as page count. This field is at the top level rather than inside the parsed output. |
>
> Expand
>
> Show lessSee more

For more information about error handling for AI functions, see [Snowflake Cortex AI Function: Multirow error handling improvements](/release-notes/bcr-bundles/2026_02/bcr-2184).

## Examples

For examples, see [AI\_PARSE\_DOCUMENT examples](/user-guide/snowflake-cortex/parse-document#label-parse-document-examples).

Note

AI\_PARSE\_DOCUMENT is the updated version of [PARSE\_DOCUMENT](/sql-reference/functions/parse_document-snowflake-cortex).
For the latest functionality, use AI\_PARSE\_DOCUMENT.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features) for legal notices.
