Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_PARSE\_DOCUMENT

Regional Availability

Available natively to accounts in [select regions](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).
Available through [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) to accounts in all regions.

Returns document content from a Snowflake stage as a JSON-formatted string. Supports text extraction (OCR), text and
layout extraction (LAYOUT), and text, layout, and visual content extraction (AGENTIC). For more information, see
[Parsing documents with AI\_PARSE\_DOCUMENT](/user-guide/snowflake-cortex/parse-document).

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
      - `'AGENTIC'`: The function goes beyond text and layout extraction to interpret visual elements, generate semantic summaries, and extract structured data from charts, diagrams, tables, and other visuals. For more information, see [Agentic mode](/user-guide/snowflake-cortex/parse-document#label-parse-document-agentic-mode).
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
    data, the `error` field contains the error message (or NULL on success), and `metadata` is returned alongside
    `value` and `error`. `value` uses the shape in [Returns](#label-ai-parse-document-returns). See
    [Error behavior](#error-behavior) for details.

## Returns

By default the function returns the JSON as a string, so use
[PARSE\_JSON](/sql-reference/functions/parse_json) to read the fields in SQL. If parsing fails, the function returns NULL. Every
successful result includes `metadata.pageCount`.

Page splitting is on when `'page_split'` is TRUE or `'page_filter'` is specified.

**Page splitting off.** The document is one `content` string: plain text in OCR mode, or Markdown in LAYOUT mode.

Copy code

```
{
  "content": "Document text.",
  "metadata": {
    "pageCount": 1
  }
}
```

**Page splitting on.** `pages` is an array of page objects, including for a one-page file. With `'page_filter'`, the
array contains only the selected pages. `index` is the zero-based position in the original file. Printed page numbers
are ignored. `dimensions` has `height` and `width`.

Copy code

```
{
  "metadata": {
    "pageCount": 140
  },
  "pages": [
    {
      "content": "Page text.",
      "index": 0
    }
  ]
}
```

**Images.** `images` is included when `'mode'` is `'LAYOUT'` and `'extract_images'` is TRUE, or when `'mode'` is
`'AGENTIC'`. It is a top-level array when page splitting is off, and an array on each page when page splitting is on.
The array is `[]` when there are no images. Markdown in `content` refers to an image by `id`, for example
`![img-0.jpeg](img-0.jpeg)`.

In AGENTIC mode, each image entry contains a `results` object with the semantic summary and structured details for
that visual. For field definitions, see [Expected image result schemas for AGENTIC mode](#label-parse-document-agentic-schemas).

| Field | Description |
| --- | --- |
| `id` | Image identifier, such as `img-0.jpeg`. |
| `top_left_x`, `top_left_y` | Upper-left corner on the page. |
| `bottom_right_x`, `bottom_right_y` | Lower-right corner on the page. |
| `image_base64` | Image data encoded as a base64 string. Returned in LAYOUT mode when `'extract_images'` is TRUE. |
| `results` | In AGENTIC mode, contains the results for the image, such as its image type, a semantic summary, and structured details. If processing fails for the image, contains an error marker instead. |

Expand

Show lessSee more

Copy code

```
{
  "id": "img-0.jpeg",
  "top_left_x": 666,
  "top_left_y": 697,
  "bottom_right_x": 1026,
  "bottom_right_y": 816,
  "image_base64": "data:image/jpeg;base64,..."
}
```

### Expected image result schemas for AGENTIC mode

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Important

AGENTIC mode generates image results on a best-effort basis. The schemas in this section describe the expected
structure of the model-generated `results` object, but schema conformance isn’t enforced or guaranteed. Returned
fields, types, and values can vary. Validate the fields your application requires, and handle missing, null, or
unexpected values.

These schemas describe the results for images that are processed successfully. If processing fails for an image, its
`results` object contains the error marker described in [Partial results in AGENTIC mode](#label-parse-document-agentic-partial-failures), which also
includes an example response.

#### Common fields

The expected `results` object contains these fields:

| Field | Expected type | Description |
| --- | --- | --- |
| `image_type` | String | Image classification: `chart`, `table`, `diagram`, `screenshot`, `document_page`, `infographic`, `photo_with_text`, or `other`. |
| `summary` | String | A short paragraph describing the image and the information it conveys. |
| `details` | Object | Image-type-specific fields, described in the following sections. |

Expand

Show lessSee more

All field paths in the following sections are relative to `details`. The notation `[]` refers to an element of an
array.

#### Chart

The following fields are expected when `image_type` is `chart`:

| Field | Expected type | Description |
| --- | --- | --- |
| `chart_type` | String | `bar`, `line`, `pie`, `scatter`, `area`, `heatmap`, `multi_panel`, or `other`. |
| `title` | String or null | Chart title, when available. |
| `x_axis` | Object | Horizontal-axis information, with `label` and `units` fields. Each field is a string or null. |
| `y_axis` | Object | Vertical-axis information, with `label` and `units` fields. Each field is a string or null. |
| `series` | Array of objects | Data series identified in the chart. |
| `series[].name` | String | Series name. |
| `series[].unit` | String or null | Unit and scale used for numeric values in the series, such as `USD millions`. |
| `series[].points` | Array of objects | Data points in the series. |
| `series[].points[].label` | String | Category, time period, or other point label. |
| `series[].points[].value` | Number or string | Extracted or estimated value. A string can preserve a printed unit or scale suffix. |
| `key_values` | Array of strings | Notable values or facts from the chart. |
| `notes` | String | Trends, outliers, multi-panel layout, footnotes, estimation caveats, or other relevant context. |

Expand

Show lessSee more

##### Units and scale

When printed values with unit or scale suffixes are returned as bare numbers, the expected output uses one consistent
unit for the entire series and records it in `series[].unit`.

For example, values printed as `$97B` and `$1.08T` can be represented as:

Copy code

```
{
  "name": "Market value",
  "unit": "USD billions",
  "points": [
    {
      "label": "A",
      "value": 97
    },
    {
      "label": "B",
      "value": 1080
    }
  ]
}
```

Alternatively, values can retain their original strings, such as `"$97B"` and `"$1.08T"`. In that representation,
each value carries its own unit and scale, and `series[].unit` is expected to be null.

##### Stacked charts

Category-level series depend on a readable mapping between segments and category names, such as a clear legend or
directly labeled segments. When that mapping is ambiguous, the expected output is a single series representing total
stacked heights, with an explanation in `notes`, rather than an inferred category breakdown.

#### Table

The following fields are expected when `image_type` is `table`:

| Field | Expected type | Description |
| --- | --- | --- |
| `title` | String or null | Table title, when available. |
| `columns` | Array of strings | Column headers in order. |
| `rows` | Array of arrays of strings | Table rows. Each inner array contains cell values in column order. |
| `key_values` | Array of strings | Notable cells or facts from the table. |

Expand

Show lessSee more

#### Diagram

The following fields are expected when `image_type` is `diagram`:

| Field | Expected type | Description |
| --- | --- | --- |
| `diagram_type` | String | `flowchart`, `block_diagram`, `architecture`, `schematic`, `tree`, `network`, or `other`. |
| `components` | Array of objects | Components identified in the diagram. |
| `components[].id` | String | Component identifier used by connections. |
| `components[].label` | String | Visible component label. |
| `components[].role` | String or null | Component role, when identifiable. |
| `connections` | Array of objects | Relationships or connections between components. |
| `connections[].from` | String | Source component identifier. |
| `connections[].to` | String | Destination component identifier. |
| `connections[].label` | String or null | Visible connection or edge label, when available. |
| `purpose` | String | One sentence describing what the diagram conveys. |

Expand

Show lessSee more

#### Screenshot

The following fields are expected when `image_type` is `screenshot`:

| Field | Expected type | Description |
| --- | --- | --- |
| `app_or_page` | String or null | Product or page name, when visible. |
| `visible_text` | Array of strings | Meaningful visible text in reading order. |
| `state_signals` | Array of strings | Errors, warnings, statuses, badges, selected options, or disabled controls. |
| `purpose` | String | One sentence describing what a user would do on the screen. |

Expand

Show lessSee more

#### Document page

The following fields are expected when `image_type` is `document_page`:

| Field | Expected type | Description |
| --- | --- | --- |
| `headings` | Array of strings | Headings in reading order. |
| `body` | String | Transcribed body text, preserving reading order. |
| `callouts` | Array of strings | Sidebars, highlighted text, footnotes, or image captions. |

Expand

Show lessSee more

#### Infographic

The following fields are expected when `image_type` is `infographic`:

| Field | Expected type | Description |
| --- | --- | --- |
| `title` | String or null | Infographic title, when available. |
| `sections` | Array of objects | Sections identified in the infographic. |
| `sections[].heading` | String | Section heading. |
| `sections[].key_facts` | Array of strings | Facts presented in the section. |
| `key_values` | Array of strings | Notable numbers or facts from the infographic. |

Expand

Show lessSee more

#### Photo with text

The following fields are expected when `image_type` is `photo_with_text`:

| Field | Expected type | Description |
| --- | --- | --- |
| `visible_text` | Array of strings | Meaningful visible text in reading order. |
| `scene_description` | String | One sentence describing what the photograph shows. |

Expand

Show lessSee more

#### Other

The following fields are expected when `image_type` is `other`:

| Field | Expected type | Description |
| --- | --- | --- |
| `visible_text` | Array of strings | Meaningful visible text. Expected to be an empty array when no text is present. |
| `description` | String | A paragraph describing the image. |

Expand

Show lessSee more

## Usage notes

- AGENTIC mode supports up to 2,000 images per document. This limit applies to the document, not to each page.
- AGENTIC mode doesn’t support the `'extract_images'` option. If you set `'extract_images'` to TRUE in AGENTIC mode,
  the function returns an error. To extract embedded images as base64-encoded data, use LAYOUT mode with `'extract_images'` set to TRUE.

## Error behavior

By default, if AI\_PARSE\_DOCUMENT can’t process the input, the function returns NULL. If the query processes multiple
rows, rows with errors return NULL and don’t prevent the query from completing.

The following table shows the return value based on the `return_error_details` argument:

> | `return_error_details` | Return value | Description |
> | --- | --- | --- |
> | FALSE Not passed | NULL |  |
> | TRUE | OBJECT with `value`, `error`, and `metadata` fields | `value`: An OBJECT containing the parsed document data, or NULL if an error occurred. `error`: A VARCHAR value that contains the error message if an error occurred, or NULL if the function succeeded. The `error` field inside `value` (renamed from `errorInformation`) contains per-document error details when present. `metadata`: An OBJECT containing document metadata such as page count. This field is returned alongside `value` and `error`. |
>
> Expand
>
> Show lessSee more

For more information about error handling for AI functions, see [Snowflake Cortex AI Function: Multirow error handling improvements](/release-notes/bcr-bundles/2026_02/bcr-2184).

### Partial results in AGENTIC mode

If processing fails for an image, AI\_PARSE\_DOCUMENT still returns the parsed document content and the available
results for other images. The affected image entry contains the following error marker:

Copy code

```
{
  "id": "img-1.jpeg",
  "results": {
    "description": "error"
  }
}
```

This marker indicates a processing failure for that image, not a failure to parse the entire document. Check
image-level results before using them in downstream processing.

The following illustrative response contains successfully extracted details for one chart and one image that couldn’t
be processed. Image coordinates are omitted for brevity.

Copy code

```
{
  "metadata": {
    "pageCount": 1
  },
  "pages": [
    {
      "index": 0,
      "content": "## Quarterly revenue\n\n![img-0.jpeg](img-0.jpeg)\n\n![img-1.jpeg](img-1.jpeg)",
      "images": [
        {
          "id": "img-0.jpeg",
          "results": {
            "image_type": "chart",
            "summary": "Bar chart comparing revenue for two quarters.",
            "details": {
              "chart_type": "bar",
              "title": "Quarterly revenue",
              "x_axis": {
                "label": "Quarter",
                "units": null
              },
              "y_axis": {
                "label": "Revenue",
                "units": "USD millions"
              },
              "series": [
                {
                  "name": "Revenue",
                  "unit": "USD millions",
                  "points": [
                    {
                      "label": "Q1",
                      "value": 100
                    },
                    {
                      "label": "Q2",
                      "value": 113
                    }
                  ]
                }
              ],
              "key_values": [
                "Q1 revenue: USD 100 million",
                "Q2 revenue: approximately USD 113 million"
              ],
              "notes": "Q1 has a printed value. Q2 is estimated from the bar height."
            }
          }
        },
        {
          "id": "img-1.jpeg",
          "results": {
            "description": "error"
          }
        }
      ]
    }
  ]
}
```

## Examples

For examples, see [AI\_PARSE\_DOCUMENT examples](/user-guide/snowflake-cortex/parse-document#label-parse-document-examples).

Note

AI\_PARSE\_DOCUMENT is the updated version of [PARSE\_DOCUMENT](/sql-reference/functions/parse_document-snowflake-cortex).
For the latest functionality, use AI\_PARSE\_DOCUMENT.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features) for legal notices.
