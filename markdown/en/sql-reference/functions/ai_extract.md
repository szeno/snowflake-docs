Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_EXTRACT

Extracts information from an input string or file.

## Syntax

**Extract information from an input string:**

Copy code

```
AI_EXTRACT( <text>, <responseFormat> )
```

Copy code

```
AI_EXTRACT( text => <text>,
            responseFormat => <responseFormat>
            [, scores => TRUE | FALSE ]
            [, citation => TRUE | FALSE ] )
```

**Extract information from a file:**

Copy code

```
AI_EXTRACT( <file>, <responseFormat> )
```

Copy code

```
AI_EXTRACT( file => <file>,
            responseFormat => <responseFormat>
            [, scores => TRUE | FALSE ]
            [, citation => TRUE | FALSE ] )
```

## Arguments

`text`
:   An input string for extraction.

`file`
:   A [FILE](/sql-reference/data-types-unstructured#label-data-types-file) for extraction.

    Supported file formats:

    - PDF
    - PNG
    - PPTX, PPT
    - EML
    - DOC, DOCX
    - JPEG, JPG
    - HTM, HTML
    - TEXT, TXT
    - TIF, TIFF
    - BMP, GIF, WEBP
    - MD

    The files must be less than 100 MB in size.

    To extract information from selected pages of a paginated document, pass [`FL_FILTER_PAGES`](/sql-reference/functions/fl_filter_pages) as the `file` argument. `AI_EXTRACT` processes only the selected pages. For page-range syntax and restrictions, see [FL\_FILTER\_PAGES](/sql-reference/functions/fl_filter_pages).

`responseFormat`
:   Information to be extracted. The format depends on the type of extraction.

    **Entity extraction formats**

    Extract single values by providing one of the following formats:

    - Simple object schema that maps the label and information to be extracted:

      ```
      {'name': 'What is the last name of the employee?', 'address': 'What is the address of the employee?'}
      ```
    - An array of strings that contain the information to be extracted:

      ```
      ['What is the last name of the employee?', 'What is the address of the employee?']
      ```
    - An array of arrays that contain two strings (label and the information to be extracted):

      ```
      [['name', 'What is the last name of the employee?'], ['address', 'What is the address of the employee?']]
      ```
    - A JSON schema with `'type': 'string'` on the sub-object:

      ```
      {
        'schema': {
       'type': 'object',
       'properties': {
         'title': {
           'description': 'What is the title of the document?',
           'type': 'string'
         }
       }
        }
      }
      ```

    **List extraction format**

    Extract arrays of values using a JSON schema with `'type': 'array'` on the sub-object:

    ```
    {
      'schema': {
        'type': 'object',
        'properties': {
          'employees': {
            'description': 'What are the names of employees?',
            'type': 'array'
          }
        }
      }
    }
    ```

    **Table extraction format**

    Extract tabular data using a JSON schema with `'type': 'object'` and `column_ordering`. Each column is defined as a
    nested property with `'type': 'array'` and a `description` that matches the column name in the file:

    ```
    {
      'schema': {
        'type': 'object',
        'properties': {
          'income_table': {
            'description': 'Income for FY2026Q2',
            'type': 'object',
            'column_ordering': ['month', 'income'],
            'properties': {
              'month': {
                'description': 'Month',
                'type': 'array'
              },
              'income': {
                'description': 'Income',
                'type': 'array'
              }
            }
          }
        }
      }
    }
    ```

    Note

    - You can’t combine the JSON schema format with other response formats. If `responseFormat` contains the `schema` key,
      you must define all questions within the JSON schema. Additional keys are not supported.
    - The model only accepts certain shapes of JSON schema. Top level type must always be an object, which contains independently extracted sub-objects.
      Sub-objects may be a table (object of lists of strings representing columns), a list of strings, or a string.

      String is currently the only supported scalar type.
    - Use the `description` field to provide context to the model; for example, to help the model localize the right table in a document. You can enter the column header name,
      or describe the column in another way.
    - Use the `column_ordering` field to specify the order of all columns in the extracted table. The `column_ordering` field is case-sensitive and must match
      the column names defined in the `properties` field. The order should reflect the order of the columns in the document.

`scores => { boolean }`
:   Optional. Supported only in the named-argument syntax shown above. A BOOLEAN that controls whether the function returns
    scores for extracted values. The default is `FALSE`. When `TRUE`, the JSON result includes a `scoring`
    object in addition to `response`. For the output format, SQL examples, and limitations, see
    [Extraction scores](#label-ai-extract-scores).

`citation => { boolean }`
:   [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

    Optional. Specify this argument by using named-argument syntax. A BOOLEAN that controls whether AI\_EXTRACT requests
    source citations for extracted values. The default is `FALSE`. If you omit the argument, AI\_EXTRACT preserves the
    default behavior and doesn’t return a `citations` object.

    Set `citation => TRUE` to include a `citations` object in the returned JSON.

    The value must be the constant `TRUE` or `FALSE`. Passing `NULL` returns a SQL compilation error: `AI_EXTRACT citation must be the constant TRUE or FALSE.`

    For document input, citations contain page numbers and bounding boxes. For text input, citations contain offsets into
    the input text.

    Citations require [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) to be enabled for your account.

    You can request citations together with extraction scores by setting both `citation => TRUE` and `scores => TRUE`.

    For the output format and examples, see [Citations](#label-ai-extract-citations).

## Returns

A JSON object containing the extracted information. The structure of the response depends on the type of extraction.

When `citation => TRUE`, the returned JSON includes a `citations` object containing source locations associated with
extracted fields. Extracted values remain in the `response` object. When `scores => TRUE` is also specified, the result
includes the separate `scoring` object.

When [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) is enabled and AI\_EXTRACT can’t process a file, the `error` field contains the error for that document. The statement continues for
any other documents. This includes a document that exceeds the 1,000-page limit, a corrupted file, and a file that isn’t in a
supported format. Without cross-region inference, a file that AI\_EXTRACT can’t process fails the SQL statement. For the page limit in that case, see [Usage notes](#label-ai-extract-usage-notes).

### Entity extraction

Returns a JSON object with key-value pairs for each extracted entity:

```
{
  "error": null,
  "response": {
    "title": "Financial report"
  }
}
```

### List extraction

Returns a JSON object with arrays of extracted values:

```
{
  "error": null,
  "response": {
    "employees": [
      "Smith",
      "Johnson",
      "Doe"
    ]
  }
}
```

### Table extraction

Returns a JSON object with column arrays representing the extracted table:

```
{
  "error": null,
  "response": {
    "income_table": {
      "income": ["$120 678","$130 123","$150 998"],
      "month": ["February", "March", "April"]
    }
  }
}
```

### Combined extraction

When extracting entities, lists, and tables in a single call, the response contains all extraction types:

```
{
  "error": null,
  "response": {
    "employees": [
      "Smith",
      "Johnson",
      "Doe"
    ],
    "income_table": {
      "income": ["$120 678","$130 123","$150 998"],
      "month": ["February", "March", "April"]
    },
    "title": "Financial report"
  }
}
```

## Extraction scores

When you use AI\_EXTRACT, you can request scores that indicate the model’s certainty about each extracted value. You can
use these scores to set thresholds for business logic, such as flagging low-scoring extractions for human review.

A higher score indicates a higher likelihood that the extracted value is correct. You can compare scores for extracting a
given entity across different documents to identify which values are more or less reliable, and use them to build
deterministic processing logic such as thresholds, fallback mechanisms, and human-in-the-loop workflows.

### How scores work

When you set the `scores` parameter to `TRUE`, AI\_EXTRACT returns a `scoring` object alongside the standard
`response` object. The `scoring` object contains a score for each extracted field.

The `scores` parameter is optional, and it is set to `FALSE` by default. Use the optional `scores` argument in the
named-argument syntax shown in [Arguments](#label-ai-extract-arguments).

### Scoring output format

When `scores => TRUE`, the returned JSON includes a `scoring` object:

```
{
  "response": {
    "name": "John Smith",
    "address": "123 Main St, San Francisco"
  },
  "scoring": {
    "scores": {
      "name": {
        "score": 0.95
      },
      "address": {
        "score": 0.82
      }
    }
  },
  "error": null
}
```

Each field in `scoring.scores` corresponds to a field in `response` and contains a `score` value between 0 and 1.

For list extraction, the `scoring` object returns an aggregate score for the entire list:

```
{
  "response": {
    "employees": ["Smith", "Johnson", "Doe"]
  },
  "scoring": {
    "scores": {
      "employees": {
        "score": 0.77
      }
    }
  },
  "error": null
}
```

For table extraction, the `scoring` object returns an aggregate score for the entire table:

```
{
  "response": {
    "income_table": {
      "month": ["February", "March", "April"],
      "income": ["$120 678", "$130 123", "$150 998"]
    }
  },
  "scoring": {
    "scores": {
      "income_table": {
        "score": 0.85
      }
    }
  },
  "error": null
}
```

### Scoring usage notes

- Requesting scores does not incur additional cost. For general information on AI\_EXTRACT costs, see [Cost considerations](#label-ai-extract-cost).
- Per-element scores for individual list items and table cells are not available.
- Scores are supported for fine-tuned models.

### Examples with extraction scores

The following example extracts information from a file and returns scores for each extracted field:

Copy code

```
SELECT AI_EXTRACT(
  file => TO_FILE('@db.schema.files', 'document.pdf'),
  responseFormat => {'name': 'What is the last name of the employee?', 'date': 'What is the inspection date?'},
  scores => TRUE
);
```

Result:

```
{
  "response": {
    "date": "2022-04-01",
    "name": "Johnson"
  },
  "scoring": {
    "scores": {
      "date": {
        "score": 0.96
      },
      "name": {
        "score": 0.99
      }
    }
  },
  "error": null
}
```

The following example extracts a list of buyer names and returns an aggregate score:

Copy code

```
SELECT AI_EXTRACT(
  file => TO_FILE('@db.schema.files', 'agreement.pdf'),
  responseFormat => {
    'schema': {
      'type': 'object',
      'properties': {
        'buyer_list': {
          'description': 'What are the buyer names?',
          'type': 'array'
        }
      }
    }
  },
  scores => TRUE
);
```

Result:

```
{
  "response": {
    "buyer_list": [
      "John Davis",
      "Jane Davis"
    ]
  },
  "scoring": {
    "scores": {
      "buyer_list": {
        "score": 0.91
      }
    }
  },
  "error": null
}
```

The following example extracts a table and returns an aggregate score:

Copy code

```
SELECT AI_EXTRACT(
  file => TO_FILE('@db.schema.files', 'report.pdf'),
  responseFormat => {
    'schema': {
      'type': 'object',
      'properties': {
        'income_table': {
          'description': 'Income for FY2026Q2',
          'type': 'object',
          'column_ordering': ['month', 'income'],
          'properties': {
            'month': {
              'description': 'Month',
              'type': 'array'
            },
            'income': {
              'description': 'Income',
              'type': 'array'
            }
          }
        }
      }
    }
  },
  scores => TRUE
);
```

Result:

```
{
  "response": {
    "income_table": {
      "income": ["$120 678", "$130 123", "$150 998"],
      "month": ["February", "March", "April"]
    }
  },
  "scoring": {
    "scores": {
      "income_table": {
        "score": 0.88
      }
    }
  },
  "error": null
}
```

## Citations

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

When you set `citation => TRUE`, AI\_EXTRACT returns a `citations` object alongside the extracted values in `response`.
Use citations to identify the source locations that support extracted fields.

The citation format depends on the input:

- Document input returns citations in `citations.bounding_boxes`.
- Text input returns citations in `citations.text_spans`.

### Document citation output

Document citations are returned in `citations.bounding_boxes`. Each field name maps to an array of bounding-box objects.

Each bounding-box object contains the following properties:

| Property | Type | Description |
| --- | --- | --- |
| `page` | INTEGER | Page containing the cited region. Pages are numbered from 1 in the original document, even when `FL_FILTER_PAGES` selects a subset of pages. |
| `upper_left` | ARRAY of numbers | Coordinates of the upper-left corner of the cited region. The first value is a percentage of the page width. The second value is a percentage of the page height. |
| `lower_right` | ARRAY of numbers | Coordinates of the lower-right corner of the cited region. The first value is a percentage of the page width. The second value is a percentage of the page height. |

Expand

Show lessSee more

Bounding-box coordinates are measured from the top-left corner of the page, which is `(0, 0)`. Each pair is
`[width_percent, height_percent]`. Values are percentages of the page width and page height in the range 0 to 100. The
x value increases to the right, and the y value increases downward.

Example output for one invoice field:

```
{
  "citations": {
    "bounding_boxes": {
      "invoice_number": [
        {
          "page": 1,
          "upper_left": [65.0, 8.0],
          "lower_right": [85.0, 12.0]
        }
      ]
    }
  },
  "error": null,
  "response": {
    "invoice_number": "INV-1001"
  }
}
```

### List and table citation output

The citation key matches the list or table field name in `response`. How many citations are returned depends on the
extraction type:

- **Lists:** AI\_EXTRACT returns one citation per list item. The array index matches the extracted item. The bounding box
  at index `0` is the cited region for the first item, index `1` is the second item, and so on.
- **Tables:** AI\_EXTRACT returns one citation for the table as a whole. It doesn’t return a citation per table row,
  column, or cell.

The following example extracts an items table and a list of acceptance steps. The list `acceptance_steps` returns one
citation per item. The table `items_ordered` returns one citation for the table.

Copy code

```
SELECT AI_EXTRACT(
  file => TO_FILE('@documents', 'sample_table_and_list.pdf'),
  responseFormat => {
    'schema': {
      'type': 'object',
      'properties': {
        'items_ordered': {
          'description': 'Items ordered table. Extract item rows only, excluding the Total row.',
          'type': 'object',
          'column_ordering': [
            'sku',
            'item_description',
            'quantity',
            'unit_price_eur',
            'amount_eur'
          ],
          'properties': {
            'sku': {
              'description': 'SKU',
              'type': 'array'
            },
            'item_description': {
              'description': 'Item description',
              'type': 'array'
            },
            'quantity': {
              'description': 'Qty',
              'type': 'array'
            },
            'unit_price_eur': {
              'description': 'Unit price (EUR)',
              'type': 'array'
            },
            'amount_eur': {
              'description': 'Amount (EUR)',
              'type': 'array'
            }
          }
        },
        'acceptance_steps': {
          'description': 'What are the acceptance steps? Extract each numbered step as a separate list item in document order.',
          'type': 'array'
        }
      }
    }
  },
  citation => TRUE
);
```

Example output:

```
{
  "citations": {
    "bounding_boxes": {
      "acceptance_steps": [
        {
          "lower_right": [59.47801971435547, 77.93975067138672],
          "page": 1,
          "upper_left": [10.714285850524902, 76.28765869140625]
        },
        {
          "lower_right": [59.06593322753906, 80.27210998535156],
          "page": 1,
          "upper_left": [10.714285850524902, 78.71720123291016]
        },
        {
          "lower_right": [49.58790969848633, 82.70165252685547],
          "page": 1,
          "upper_left": [10.714285850524902, 81.14674377441406]
        }
      ],
      "items_ordered": [
        {
          "lower_right": [89.97252655029297, 52.18659210205078],
          "page": 1,
          "upper_left": [9.615385055541992, 35.2769660949707]
        }
      ]
    }
  },
  "error": null,
  "response": {
    "acceptance_steps": [
      "Count the delivered units and compare them with the items table.",
      "Check the equipment for visible damage and missing accessories.",
      "Record any discrepancies before confirming receipt."
    ],
    "items_ordered": {
      "amount_eur": ["498.00", "238.00", "260.00", "116.00", "75.00"],
      "item_description": [
        "27-inch office monitor",
        "USB-C docking station",
        "Wireless keyboard",
        "Wireless mouse",
        "USB-C cable, 2 m"
      ],
      "quantity": ["2", "2", "4", "4", "6"],
      "sku": ["MON-27", "DOCK-USBC", "KEY-WL", "MOUSE-WL", "CABLE-2M"],
      "unit_price_eur": ["249.00", "119.00", "65.00", "29.00", "12.50"]
    }
  }
}
```

### Text citation output

Text citations are returned in `citations.text_spans`. Each field name maps to an array of text-span objects.

Each text-span object contains the following properties:

| Property | Type | Description |
| --- | --- | --- |
| `span-start` | INTEGER | Start offset of the cited passage, counted as Unicode characters from the start of the input text. Offsets are zero-based. |
| `span-end` | INTEGER | End offset of the cited passage, counted as Unicode characters from the start of the input text. The end offset is exclusive. |

Expand

Show lessSee more

Example output for one product field:

```
{
  "citations": {
    "text_spans": {
      "product_code": [
        {
          "span-start": 20,
          "span-end": 27
        }
      ]
    }
  },
  "error": null,
  "response": {
    "product_code": "SKU-100"
  }
}
```

### Citation usage notes

- The input argument is named `citation` (singular). The returned object is named `citations` (plural).
- Citations for each field are represented as arrays. Process all returned entries rather than assuming that a field
  contains one citation.
- For lists, the citation array contains one citation per list item. For tables, the citation array contains one citation
  for the table as a whole, not one citation per row, column, or cell.
- When accessing `span-start` and `span-end` with SQL path notation, enclose the keys in double quotes because they
  contain hyphens.
- The `citation` argument is optional. The default is `FALSE`. If you omit the argument, AI\_EXTRACT doesn’t return a
  `citations` object.
- Citations require cross-region inference. For information about enabling it, see
  [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference).
- Requesting citations doesn’t incur additional cost beyond the standard AI\_EXTRACT call.

Citations are optimized to work with the following file formats:

- PDF
- PNG
- EML
- JPEG, JPG
- TEXT, TXT
- TIF, TIFF
- BMP, GIF, WEBP
- MD

### Example: Retrieve document citations

The following example extracts an invoice number and returns its citation locations as rows. `FLATTEN` produces one row
for each entry in the field’s citation array.

Copy code

```
WITH extraction AS (
  SELECT AI_EXTRACT(
    file => TO_FILE('@documents', 'invoice.pdf'),
    responseFormat => {
      'invoice_number': 'Invoice number'
    },
    citation => TRUE
  ) AS extracted
)
SELECT
  e.extracted:response.invoice_number::VARCHAR
    AS invoice_number,
  c.value:page::INTEGER AS page,
  c.value:upper_left AS upper_left,
  c.value:lower_right AS lower_right
FROM extraction AS e,
  LATERAL FLATTEN(
    INPUT => e.extracted:citations.bounding_boxes.invoice_number
  ) AS c;
```

For the example document citation above:

| INVOICE\_NUMBER | PAGE | UPPER\_LEFT | LOWER\_RIGHT |
| --- | --- | --- | --- |
| INV-1001 | 1 | [65.0, 8.0] | [85.0, 12.0] |

Expand

Show lessSee more

This query retrieves the citation metadata. Rendering a highlight in a document viewer is handled by the application.

### Example: Retrieve cited text

The following example extracts a product code and retrieves its cited passage from the original input.

Copy code

```
WITH input_text AS (
  SELECT
    'The product code is SKU-100. Each package contains 24 units. The warranty period is 12 months.'
      AS content
),
extraction AS (
  SELECT
    content,
    AI_EXTRACT(
      text => content,
      responseFormat => {
        'product_code': 'Product code'
      },
      citation => TRUE
    ) AS extracted
  FROM input_text
)
SELECT
  e.extracted:response.product_code::VARCHAR AS product_code,
  c.value:"span-start"::INTEGER AS span_start,
  c.value:"span-end"::INTEGER AS span_end,
  SUBSTR(
    e.content,
    c.value:"span-start"::INTEGER + 1,
    c.value:"span-end"::INTEGER
      - c.value:"span-start"::INTEGER
  ) AS cited_text
FROM extraction AS e,
  LATERAL FLATTEN(
    INPUT => e.extracted:citations.text_spans.product_code
  ) AS c;
```

For the example span `[20, 27)`:

| PRODUCT\_CODE | SPAN\_START | SPAN\_END | CITED\_TEXT |
| --- | --- | --- | --- |
| SKU-100 | 20 | 27 | SKU-100 |

Expand

Show lessSee more

The expression adds 1 to the zero-based start offset because Snowflake’s `SUBSTR` function uses one-based positions. The
substring length is the end offset minus the start offset.

Both SQL examples list returned citation entries. To retain an extraction row when the citation array can’t be expanded,
use `OUTER => TRUE` in `FLATTEN`.

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
For information about granting this privilege, see [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges).

## Usage notes

- AI\_EXTRACT is optimized for both digital-born and scanned documents.
- You can’t use both `text` and `file` parameters simultaneously in the same function call.
- Page selection with `FL_FILTER_PAGES` applies to the `file` argument, not the `text` argument. Files without pages, such as plain-text files, cannot be filtered by page.
- Use `FL_FILTER_PAGES` directly inside the `AI_EXTRACT` call. The selection applies only to that call; it is not stored on the `FILE` value and does not create a new document.
- Multiple ranges select pages from the original document. Overlapping ranges do not cause the same page to be processed more than once, and selected pages are processed in document order.
- When you use `citation => TRUE` with `FL_FILTER_PAGES`, citation `page` values refer to pages in the original document. They don’t restart at 1 for the selected pages. Citations only reference selected pages.
- A valid selection that resolves to no pages returns an empty result. For invalid selections and other page-selection errors, see [Error conditions](/sql-reference/functions/fl_filter_pages#label-fl-filter-pages-error-conditions).
- With [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) enabled:

  - File extraction supports documents of up to 1,000 pages. A document that exceeds the limit returns an error for that document.
  - A request that extracts many fields from a document returns one combined result.
  - If AI\_EXTRACT can’t process a file, the `error` field contains the error for that document and the statement continues. This includes a document that exceeds the page limit, a corrupted file, and a file that isn’t in a supported format.
  - `scale_factor` is no longer needed. AI\_EXTRACT now delivers improved extraction quality without manual scaling adjustments. Existing calls continue to work unchanged; any `scale_factor` value is ignored.
- Without cross-region inference:

  - File extraction supports documents of up to 125 pages.
  - A file that AI\_EXTRACT can’t process fails the SQL statement. This includes a corrupted file and a file that isn’t in a supported format.
  - The `scale_factor` parameter still applies. It scales pages of an input file before extraction, which can improve results for pages larger than A4, small text, or dense layouts. Set it to a numeric value from 1.0 through 4.0. The default is 1.0.
- You can either ask questions in natural language or describe information to be extracted (such as city, street, ZIP code); for example:

  ```
  {'address': 'City, street, ZIP', 'name': 'First and last name'}
  ```
- The following languages are supported:

- Arabic
- Bengali
- Burmese
- Cebuano
- Chinese
- Czech
- Dutch
- English
- French
- German
- Hebrew
- Hindi
- Indonesian
- Italian
- Japanese
- Khmer
- Korean
- Lao
- Malay
- Persian
- Polish
- Portuguese
- Russian
- Spanish
- Tagalog
- Thai
- Turkish
- Urdu
- Vietnamese

- In a single AI\_EXTRACT call, you can ask a maximum of 100 questions for entity extraction, and a maximum of 10 questions for table extraction.

  A table extraction question is equal to 10 entity extraction questions. For example, you can ask 4 table extraction questions and
  60 entity extraction questions in a single AI\_EXTRACT call.
- The maximum output length for entity extraction is 512 tokens per question. For table extraction, the model returns answers that are a maximum of 4096 tokens.
- You can request optional extraction scores by using named arguments and passing `scores => TRUE`.
  For details, see [Extraction scores](#label-ai-extract-scores).
- You can request optional citations by using named arguments and passing `citation => TRUE`.
  For details, see [Citations](#label-ai-extract-citations).

AI\_EXTRACT supports documents on stages that use client-side or server-side encryption, including in accounts that use
PrivateLink or other [network policies](/user-guide/network-policies) that restrict public network access to stages.
Files on external stages that use client-side encryption configured in Snowflake (for example, by using a COPY INTO
statement) are supported.

## Cost considerations

- The Cortex AI\_EXTRACT function incurs compute cost based on the number of pages per document, input prompt tokens, and
  output tokens processed.

  - For paged file formats (PDF, DOCX, TIF, TIFF), each page is counted as 970 tokens.
  - For image file formats (JPEG, JPG, PNG), each individual image file is billed as a page and counted as 970 tokens.
- Snowflake recommends executing queries that call the Cortex AI\_EXTRACT function in a smaller warehouse (no larger than
  MEDIUM). Larger warehouses don’t increase performance.
- Requesting citations (`citation => TRUE`) doesn’t incur additional cost beyond the standard AI\_EXTRACT call.

## Regional availability

AI\_EXTRACT is available to accounts in the following regions:

| Cloud platform | Region name |
| --- | --- |
| Amazon Web Services (AWS) | - US East (N. Virginia) - US West (Oregon) - Canada (Central) - South America (Sao Paulo) - EU (Ireland) - EU (Frankfurt) - Asia Pacific (Tokyo) - Asia Pacific (Sydney) |
| Microsoft Azure | - East US 2 (Virginia) - West US 2 (Washington) - South Central US (Texas) - North Europe (Ireland) - West Europe (Netherlands) - Southeast Asia (Singapore) - Australia East (New South Wales) - Central India (Pune) - Japan East (Tokyo) |
| Google Cloud Platform | - Middle East Central2 (Dammam) |

Expand

Show lessSee more

AI\_EXTRACT has cross-region support. For information on enabling Cortex AI cross-region support,
see [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference).

## Error conditions

AI\_EXTRACT can produce the following error messages:

| Message | Explanation |
| --- | --- |
| `Internal error.` | A system error occurred. Wait and try again. If the error persists, contact Snowflake support. |
| `Not found.` | The file was not found. |
| `Provided file cannot be found.` | The file was not found. |
| `Provided file cannot be accessed.` | The current user does not have sufficient privileges to access the file. |
| `The provided file format {file_extension} isn't supported.` | The document isn’t in a supported format. With cross-region inference enabled, AI\_EXTRACT returns this error for that document. Otherwise, the statement fails. |
| `The provided file isn't in the expected format or is corrupted.` | The document is corrupted or isn’t in a supported format. With cross-region inference enabled, AI\_EXTRACT returns this error for that document. Otherwise, the statement fails. |
| `Empty request.` | No parameters were provided. |
| `Missing or empty response format.` | No response format was provided. |
| `Invalid response format.` | The response format is not valid JSON. |
| `Duplicate feature name found: {feature_name}.` | The response format contains one or more duplicate feature names. |
| `Too many questions: {number} complex and {number} simple = {number} total, complex question weight {number}`. | The number of questions exceeds the allowed limit. |
| `Maximum number of 1000 pages exceeded. The document has {actual_pages} pages.` | Cross-region inference is enabled, and the document exceeds the 1,000-page limit. AI\_EXTRACT returns this error for that document. |
| `Maximum number of 125 pages exceeded. The document has {actual_pages} pages.` | Cross-region inference isn’t enabled, and the document exceeds the 125-page limit. |
| `Page size in pixels exceeds 10000x10000. The page size is {actual_px} pixels.` | Image input or a converted document page is larger than the supported dimensions. |
| `Page size in inches exceeds 50x50 (3600x3600 pt). The page size is {actual_in} inches ({actual_pt} pt).` | Page is larger than the supported dimensions. |
| `Maximum file size of 104857600 bytes exceeded. The file size is {actual_size} bytes.` | The document is larger than 100 MB. |

Expand

Show lessSee more

## Examples

### Entity extraction

- The following example extracts entities from the input text using a simple object schema:

  Copy code

  ```
  SELECT AI_EXTRACT(
    text => 'John Smith lives in San Francisco and works for Snowflake',
    responseFormat => {'name': 'What is the first name of the employee?', 'city': 'What is the address of the employee?'}
  );
  ```
- The following example extracts and parses entities from the input text:

  Copy code

  ```
  SELECT AI_EXTRACT(
    text => 'John Smith lives in San Francisco and works for Snowflake',
    responseFormat => PARSE_JSON('{"name": "What is the first name of the employee?", "address": "What is the address of the employee?"}')
  );
  ```
- The following example extracts entities from the `document.pdf` file:

  Copy code

  ```
  SELECT AI_EXTRACT(
    file => TO_FILE('@db.schema.files','document.pdf'),
    responseFormat => [['name', 'What is the first name of the employee?'], ['city', 'Where does the employee live?']]
  );
  ```
- The following example extracts entities from all files in a directory on a stage:

  Note

  Ensure that the directory table is enabled. For more information, see [Manage directory tables](/user-guide/data-load-dirtables-manage).

  Copy code

  ```
  SELECT AI_EXTRACT(
    file => TO_FILE('@db.schema.files', relative_path),
    responseFormat => [
   'What is the document ID?',
   'What is the address of the company?'
    ]
  ) FROM DIRECTORY (@db.schema.files);
  ```
- The following example extracts the `title` entity from the `report.pdf` file using a JSON schema:

  Copy code

  ```
  SELECT AI_EXTRACT(
    file => TO_FILE('@db.schema.files', 'report.pdf'),
    responseFormat => {
   'schema': {
     'type': 'object',
     'properties': {
       'title': {
         'description': 'What is the title of document?',
         'type': 'string'
       }
     }
   }
    }
  );
  ```

### List extraction

The following example extracts the `employees` list from the `report.pdf` file:

Copy code

```
SELECT AI_EXTRACT(
  file => TO_FILE('@db.schema.files', 'report.pdf'),
  responseFormat => {
    'schema': {
      'type': 'object',
      'properties': {
        'employees': {
          'description': 'What are the surnames of employees?',
          'type': 'array'
        }
      }
    }
  }
);
```

### Table extraction

The following example extracts the `income_table` table from the `report.pdf` file:

Copy code

```
SELECT AI_EXTRACT(
  file => TO_FILE('@db.schema.files', 'report.pdf'),
  responseFormat => {
    'schema': {
      'type': 'object',
      'properties': {
        'income_table': {
          'description': 'Income for FY2026Q2',
          'type': 'object',
          'column_ordering': ['month', 'income'],
          'properties': {
            'month': {
              'description': 'Month',
              'type': 'array'
            },
            'income': {
              'description': 'Income',
              'type': 'array'
            }
          }
        }
      }
    }
  }
);
```

### Extract information from the first and last pages

The following example selects the first and last pages of a contract:

Copy code

```
SELECT AI_EXTRACT(
  file => FL_FILTER_PAGES(
    TO_FILE('@document_stage', 'contract.pdf'),
    [{'end': 1}, {'start': -1}]
  ),
  responseFormat => {
    'agreement_title': 'What is the title of this agreement?',
    'signed_by': 'Who signed this agreement?'
  }
) AS extracted_data;
```

On a 10-page document, this selects pages with indexes 0 and 9. It does not process the intervening pages.

### Combined extraction

The following example extracts a table (`income_table`), entity (`title`), and list (`employees`) from the `report.pdf`
file in a single call:

Copy code

```
SELECT AI_EXTRACT(
  file => TO_FILE('@db.schema.files', 'report.pdf'),
  responseFormat => {
    'schema': {
      'type': 'object',
      'properties': {
        'income_table': {
          'description': 'Income for FY2026Q2',
          'type': 'object',
          'column_ordering': ['month', 'income'],
          'properties': {
            'month': {
              'description': 'Month',
              'type': 'array'
            },
            'income': {
              'description': 'Income',
              'type': 'array'
            }
          }
        },
        'title': {
          'description': 'What is the title of document?',
          'type': 'string'
        },
        'employees': {
          'description': 'What are the surnames of employees?',
          'type': 'array'
        }
      }
    }
  }
);
```

### Extraction using a fine-tuned `arctic-extract` model

To use the fine-tuned `arctic-extract` model for inference with the [AI\_EXTRACT](/sql-reference/functions/ai_extract) function,
specify the model using the `model` parameter as shown in the following example:

Copy code

```
SELECT AI_EXTRACT(
  model => 'db.schema.my_tuned_model',
  file => TO_FILE('@db.schema.files','document.pdf')
);
```

You can overwrite questions used for fine-tuning by using the `responseFormat` parameter as shown in the following example:

Copy code

```
SELECT AI_EXTRACT(
  model => 'db.schema.my_tuned_model',
  file => TO_FILE('@db.schema.files','document.pdf'),
  responseFormat => [['name', 'What is the first name of the employee?'], ['city', 'Where does the employee live?']]
);
```

For more information, see [Fine-tuning arctic-extract models](/user-guide/snowflake-cortex/arctic-extract-finetuning).

Note

AI\_EXTRACT is the updated version of [EXTRACT\_ANSWER](/sql-reference/functions/extract_answer-snowflake-cortex).
For the latest functionality, use AI\_EXTRACT.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features) for legal notices.
