Categories:
:   [File functions](/sql-reference/functions-file) (AI Functions)

# PARSE\_DOCUMENT (SNOWFLAKE.CORTEX)

Notice

This page is provided for backward compatibility. For new use cases, start with
[AI\_PARSE\_DOCUMENT](/sql-reference/functions/ai_parse_document), which is the canonical surface going forward.
This legacy function will be deprecated by the end of 2026.

Returns the extracted content from a document on a Snowflake stage as a JSON-formatted string. This
function supports two types of extraction, Optical Character Recognition (OCR), and layout. For more
information, see [Parsing documents with AI\_PARSE\_DOCUMENT](/user-guide/snowflake-cortex/parse-document#label-what-is-parse-document).

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.PARSE_DOCUMENT( '@<stage>', '<path>', [ <options> ] )
```

## Arguments

**Required:**

`stage`
:   Name of the Snowflake stage.

`path`
:   Relative path to the document on the Snowflake stage.

**Optional:**

`options`
:   An OBJECT value that contains options for parsing documents. The supported keys are shown below. All are optional.

    - `'mode'`: Specifies the parsing mode. The supported modes are:

      - `'OCR'`: The function extracts text only. This is the default mode.
      - `'LAYOUT'`: The function extracts layout as well as text, including structural content such as tables.
    - `'page_split'`: If set to TRUE, the function splits the output of the function to return content per page.
      Only PDF, PowerPoint (`.pptx`), and Word (`.docx`) documents are supported.
      Documents in other formats return an error. The default is FALSE.

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
>
> > - `"errorInformation"`: Contains error information if document can’t be parsed.
> > - `"metadata"`: Contains metadata about the document, such as page count.
>
> Note
>
> The `"pages"` and `"metadata"` fields are present in the output when parsing succeeds.
> `"errorInformation"` is present only if parsing fails.

If `'page_split'` is FALSE or is not present, the output has the following structure:

> > - `"content"`: Plain text (in OCR mode) or Markdown-formatted text (in LAYOUT mode).
> > - `"errorInformation"`: Contains error information if the document can’t be parsed.
> > - `"metadata"`: Contains metadata about the document, such as page count.
>
> Note
>
> The `"content"` and `"metadata"` fields are present in the output when parsing succeeds.
> `"errorInformation"` is present only if parsing fails.
