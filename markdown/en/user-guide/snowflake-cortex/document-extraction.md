# Extracting information from documents with AI\_EXTRACT

Regional Availability

Available natively to accounts in [select regions](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).
Available through [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) to accounts in all regions.

AI\_EXTRACT is a Cortex AI Function that lets you extract structured information, such as entities, lists, and tables,
from text or document files, by asking questions in natural language or by describing information to be extracted. It
can be used with other functions to create custom document processing pipelines for a variety of use cases (see
[Cortex AI Functions: Documents](/user-guide/snowflake-cortex/ai-documents)). You can request citations to identify the source locations that support
extracted values. Citations provide page numbers and bounding boxes for document input, or text offsets for text input.

AI\_EXTRACT can process documents of various formats in multiple languages and extract information from both text-heavy
paragraphs and content in a graphical form, such as logos, handwritten text (for example, signatures), tables, or checkmarks.
File extraction supports documents of up to 1,000 pages when [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) is enabled. Without cross-region inference, the limit is 125 pages.

To extract information from only part of a document, use `FL_FILTER_PAGES` to select the pages passed to `AI_EXTRACT`. You don’t need to create separate files for the selected pages.

AI\_EXTRACT can extract information in the following structured formats:

- Entity: Ask questions in natural language or describe the information to be extracted (such as city, street, or ZIP
  code).
- List (or array): You can provide a JSON schema to extract an array or list of information present in the document,
  such as the name of all account holders in a bank statement or a list of all addresses in a Document.
- Table: Provide a JSON schema to extract tabular data present in the document by specifying the table title
  and a list of columns that should be extracted.

AI\_EXTRACT scales automatically with your workload by processing multiple documents simultaneously. Documents can be
processed directly from object storage to avoid unnecessary data movement.

AI\_EXTRACT supports documents on stages that use client-side or server-side encryption, including in accounts that use
PrivateLink or other [network policies](/user-guide/network-policies) that restrict public network access to stages.

Tip

For more information on AI\_EXTRACT, including supported languages, regional availability, and cost, see [AI\_EXTRACT](/sql-reference/functions/ai_extract).

## Extract information from selected pages

When the information you need is in a known section of a document, use `FL_FILTER_PAGES` as the `file` argument to `AI_EXTRACT`. `AI_EXTRACT` uses only the selected pages as input. Keep the same `responseFormat` you would use for a whole-document request.

The following example assumes the contract’s signature section is on its last three pages. It extracts the signer’s name and the signing date from those pages:

Copy code

```
SELECT AI_EXTRACT(
  file => FL_FILTER_PAGES(
    TO_FILE('@document_stage', 'contract.pdf'),
    [{'start': -3}]
  ),
  responseFormat => {
    'signed_by': 'Who signed this contract?',
    'signed_on': 'What is the signing date?'
  }
) AS extracted_data;
```

A negative `start` counts backward from the end of the document. Omitting `end` includes all remaining pages, including the final page. You don’t need to know the document’s page count to select its last three pages.

For ranges measured from the beginning of the document, page indexes start at 0. `start` is inclusive and `end` is exclusive. For example, `{'start': 0, 'end': 3}` selects the first three pages.

Include all pages needed to interpret the requested information, such as table headers and related values. For complete range syntax and validation rules, see [FL\_FILTER\_PAGES](/sql-reference/functions/fl_filter_pages).

### Select different pages for each document

Both arguments to `FL_FILTER_PAGES` accept columns. In the following example, the `contracts` table contains a `contract_id` column, a `doc` column of type `FILE`, and a `page_ranges` column of type `ARRAY`:

Copy code

```
SELECT
  contract_id,
  AI_EXTRACT(
    file => FL_FILTER_PAGES(doc, page_ranges),
    responseFormat => {'signed_by': 'Who signed this contract?'}
  ) AS extracted_data
FROM contracts;
```

The page selection applies only to this `AI_EXTRACT` call. It does not change the stored document or persist on the `FILE` value.

## Extract information with citations

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

AI\_EXTRACT can return citations that identify the source locations supporting extracted values. Use citations to review
results in context and display supporting content alongside extracted fields in your applications.

The citation format depends on the input:

| Input | Citation format |
| --- | --- |
| Document | Page numbers and bounding boxes identifying supporting regions. Bounding-box coordinates are percentages of page width and page height. |
| Text | Start and end offsets identifying supporting passages in the input text. Offsets count Unicode characters from the start of the input. |

Expand

Show lessSee more

To request citations, use named arguments and set `citation => TRUE`. The result includes a `citations` object
alongside the extracted values in `response`.

Citations require [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) to be enabled for your
account. Requesting citations doesn’t incur additional cost beyond the standard AI\_EXTRACT call.

Citations are optimized to work with PDF, PNG, EML, JPEG, JPG, TEXT, TXT, TIF, TIFF, BMP, GIF, WEBP, and MD files. They
also work with text passed in the `text` argument. For the complete list, see [Citations](/sql-reference/functions/ai_extract#label-ai-extract-citations).

### Extract invoice information with citations

The following example extracts an invoice number, invoice date, total amount, recipient, and recipient address from a PDF.
It requests citations.

The example assumes that an invoice is available on a stage. Replace the stage path and file name with values for your
document.

Copy code

```
SELECT AI_EXTRACT(
  file => TO_FILE('@documents', 'invoice.pdf'),
  responseFormat => {
    'invoice_number': 'Invoice number',
    'invoice_date': 'Invoice date',
    'total_amount': 'Total amount due',
    'invoice_recipient': 'Invoice recipient',
    'invoice_address': 'The address of the invoice recipient'
  },
  citation => TRUE
) AS extracted;
```

Example output:

Copy code

```
{
  "citations": {
    "bounding_boxes": {
      "invoice_address": [
        {
          "lower_right": [64.83516693115234, 29.057334899902344],
          "page": 1,
          "upper_left": [7.829670429229736, 24.781341552734375]
        }
      ],
      "invoice_date": [
        {
          "lower_right": [91.8956069946289, 21.379980087280273],
          "page": 1,
          "upper_left": [82.28022003173828, 20.01943588256836]
        }
      ],
      "invoice_number": [
        {
          "lower_right": [91.75823974609375, 12.730807304382324],
          "page": 1,
          "upper_left": [79.53296661376953, 11.56462574005127]
        }
      ],
      "invoice_recipient": [
        {
          "lower_right": [31.73076820373535, 23.71234130859375],
          "page": 1,
          "upper_left": [7.829670429229736, 22.157434463500977]
        }
      ],
      "total_amount": [
        {
          "lower_right": [90.24725341796875, 77.7453842163086],
          "page": 1,
          "upper_left": [74.17581939697266, 75.60738372802734]
        }
      ]
    }
  },
  "error": null,
  "response": {
    "invoice_address": "Musterweg 8, 80331 Munich, Germany",
    "invoice_date": "17 Nov 2026",
    "invoice_number": "DEMO-2026-1042",
    "invoice_recipient": "Harborline Analytics GmbH",
    "total_amount": "EUR 1,547.00"
  }
}
```

![Sample invoice with colored bounding boxes around the invoice number, invoice date, recipient, recipient address, and total amount.](/static/images/cortex-document/ai_extract_citation_1.png)

The field names in `citations.bounding_boxes` correspond to the field names in `response`. Each field maps to an array
of bounding-box objects.

For example, the citation for `total_amount` identifies a region with a `page` value of `1`. The `upper_left` and
`lower_right` coordinates define the cited region as percentages of the page width and page height. An application can
use this information to display the supporting region alongside the extracted amount.

You can also set `scores => TRUE` in the same call to return extraction scores. Citations identify supporting source
locations. Extraction scores indicate the model’s certainty about extracted values and can help prioritize results for
review.

### Extract product information from text with citations

For text input, AI\_EXTRACT returns citations in `citations.text_spans`. Each field maps to an array of objects
containing `span-start` and `span-end` offsets.

The following example extracts a product code, package quantity, and warranty period from a text string.

Copy code

```
SELECT AI_EXTRACT(
  text => 'The product code is SKU-100. Each package contains 24 units. The warranty period is 12 months.',
  responseFormat => {
    'product_code': 'Product code',
    'units_per_package': 'Number of units in each package',
    'warranty_period': 'Duration of the product warranty'
  },
  citation => TRUE
) AS extracted;
```

Example output:

Copy code

```
{
  "citations": {
    "text_spans": {
      "product_code": [
        {
          "span-start": 20,
          "span-end": 27
        }
      ],
      "units_per_package": [
        {
          "span-start": 51,
          "span-end": 53
        }
      ],
      "warranty_period": [
        {
          "span-start": 84,
          "span-end": 93
        }
      ]
    }
  },
  "error": null,
  "response": {
    "product_code": "SKU-100",
    "units_per_package": "24",
    "warranty_period": "12 months"
  }
}
```

The field names in `citations.text_spans` correspond to the field names in `response`.

In this example, the range `[20, 27)` identifies `SKU-100`, and the range `[84, 93)` identifies `12 months`. These
ranges count Unicode characters from the start of the input text. They are zero-based and exclude the end position.

This example requests citations without extraction scores.

### Citations for extracted lists and tables

The citation key matches the list or table field name in `response`. Lists and tables don’t use the same citation
granularity:

- For a list, AI\_EXTRACT returns one citation per list item. The array index matches the extracted item.
- For a table, AI\_EXTRACT returns one citation for the table as a whole, not one citation per row, column, or cell.

The following example extracts an items table and a list of acceptance steps from a PDF. Replace the stage path and
file name with values for your document.

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

Copy code

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

![Sample equipment order with one bounding box around the items table and a separate bounding box around each acceptance step.](/static/images/cortex-document/ai_extract_citation_2.png)

The list `acceptance_steps` has three bounding boxes, one for each step. The table `items_ordered` has one bounding box
for the table. There is no citation for each SKU, quantity, or amount.

For the output format, see [Citations](/sql-reference/functions/ai_extract#label-ai-extract-citations).

### Use citations in review workflows

Store the original input text or a reference to the source document version alongside the extraction result. This keeps
citation locations associated with the content used for extraction.

For each extracted field, read its citation array and display the cited document region or text passage alongside the
value. Process the array rather than assuming that each field contains a single citation object.

Use citations to support validation against the source. The presence of a citation does not, by itself, establish that
an extracted value is correct.

For parameter details and citation output definitions, see [Citations](/sql-reference/functions/ai_extract#label-ai-extract-citations).

## Question optimization for extracting information

When you work with AI\_EXTRACT, use natural language to ask questions about your documents. To ask a question that
returns an accurate answer, follow these guidelines:

- Use plain English.
- For each question, know what answers you expect.
- Be specific; for example, if the document includes several dates (such as issuing date and signature date), do not ask
  “What is the date?” without including more details.
- Ask for a single value in each question.
- Do not expect AI\_EXTRACT to guess your intentions or have extended knowledge in a specific domain.

Consider the following document as an example. This purchase and sale agreement includes information such as the offer expiration date,
the names of the buyers and the seller, and the included items.

![Example document (condominium purchase and sale agreement).](/static/images/cortex-document/condo-agreement.png)

The following table provides examples of questions you can ask AI\_EXTRACT and the expected answers.

| Example question | Answer |
| --- | --- |
| What is the date of this agreement? | `'October 6, 2023'` |
| Who is the buyer of the condo? | `'John Davis', 'Jane Davis'` |
| What home appliances are included with the unit? | `'stove/range', 'refrigerator', 'washer', 'dishwasher', 'attached television(s)', 'microwave'` |
| What items are not included with the flat? | `'dryer', 'security system', 'satellite dish', 'wood stove', 'fireplace insert', 'hot tub', 'attached speaker(s)', 'generator'` |
| Is there a dryer in the flat? | `'No'` |
| What addenda are attached to this purchase and sale agreement? | `'22A (Financing)', '2AA (Appraisal)', '22FSBO (Owner Sale)'` |
| What is the seller’s fax number? | None |
| Is the buyer’s signature present on the form? | `'No'` |
| What is the MLS number? | `'59844680'` |
| What is the property’s address? | `'604 Bishop Crossing Land, Fort Lauderdale, Broward County, FL, 33338'` |

Expand

Show lessSee more

## Table extraction best practices

This section provides best practices when working with table extraction in AI\_EXTRACT.

### Use one schema for a specific type of document

Each extraction workload must contain documents of the same type, and the data that you want to extract should be similar for most
of the tables. If the number of columns in the source document differs from one document to another, but all documents contain
a defined subset of columns to be extracted and the common columns have the same or a similar name and location, then those common
columns can be extracted.

For example, invoices may have different numbers of columns with various data, but if all of the tables have the same first
three columns — `Item Description`, `Quantity`, and `Price` — that data can be extracted.

### Use natural language to define column names

You can copy the column names from the document so that they’re exactly the same.
For example, don’t name the columns `product_code` or `REPORT_DATE`; instead, name them `Product Code` or `Report Date`.

### Define the columns in the same order they appear in the document

To improve accuracy, define the columns in the same order as they appear in the document, which is usually from left to right,
or top to bottom for the [transposed tables](#label-ai-extract-table-extraction-best-practices-transpose-tables).

However, for columns where values are the same for multiple rows, such as `Invoice Number` and `Invoice Date`, add these columns at the beginning.
For example:

- `Invoice Number`
- `Invoice Date`
- `Item Code`
- `Item Name`
- `Quantity`

### Define values using casing from the document

When possible, define values using casing (uppercase and lowercase) from the document. If the casing in the document is varied, use
capitalization.

### Use the description field

The `description` field in the AI\_EXTRACT response format is optional; in most cases, you don’t have to fill it in. However, if there
are multiple similar tables in a document, the model might answer inaccurately. If the answers come from a different source table
than expected or the model can’t find the table, try using the `description` field. Add information that helps the model identify
the right table, such as the table title or number.

### Add a section column to describe the layout of the table

If the table is divided into multiple named sections, add a section column. This helps the model understand the layout better and
improve the accuracy. For example, you can name the column `Section`, `Item section`, or `Item category`. If there is a second
level of nesting in the sections, you can add two columns: `Section` and `Subsection`.

### To group values, create an additional column

You can add a column to the existing table to group values. In this way, you can join results from the whole document set in a single
table; for example:

| Invoice Number | Item Details | Item Price | Quantity |
| --- | --- | --- | --- |
| A | Item A1 | 10.00 | 1 |
| A | Item A2 | 20.00 | 1 |
| A | Item A3 | 30.00 | 1 |
| B | Item B1 | 15.00 | 1 |
| B | Item B2 | 25.00 | 1 |
| B | Item B3 | 35.00 | 1 |

Expand

Show lessSee more

Note that the value in the first column is repeated for corresponding items.

### Make the column names distinguishable between documents

Try to semantically distinguish a column. Don’t use names such as `col1`, `val1`, `item1`.

In some cases, transposition can work better, especially when the row names don’t differ between documents or differ slightly and
are within a closed set of values.

### Use the parent name as a prefix when working with hierarchical headers

To extract information from tables with hierarchical headers, join the header path using each parent name as a prefix. For example,
for the following table, define the columns as:

- `Category A Type X Column 1`
- `Category A Type Y Column 2`
- `Category A Type Y Column 3`
- `Category B Column 4`
- `Category B Column 5`

![A table with headers named Category A and Category B, where Category A includes subheaders: Type X and Type Y.](/static/images/cortex-document/hierarchical-table-example.png)

### Transpose the tables if needed

You can extract information from transposed tables by using values from the first column of the table in the document as column names
in the output table.

For example, for the following table, name the columns:

- `Type A: Item 1`
- `Type A: Item 2`
- `Type B: Item 3`
- `Type B: Item 4`

![An example of a table that can be transposed.](/static/images/cortex-document/transposing-table-example.png)

Note that this example includes [hierarchical headers](#label-ai-extract-table-extraction-best-practices-hierarchical).

### For large tables, extract page ranges separately

The model for table extraction returns answers that are up to 4096 tokens long. This means that the model stops extracting when it reaches
that limit. You can approach this in the following ways:

- If a table spans several pages, use separate `AI_EXTRACT` calls with `FL_FILTER_PAGES` to extract one page or a smaller page range at a time. Combine the results after extraction. You don’t need to create separate files. Specify each range in a separate call; multiple ranges in one `FL_FILTER_PAGES` call form a single combined page selection.
- If the table is so dense that the data can’t be extracted even from a single page, divide the table by columns.

  For example, if the table contains 10 columns, try defining two separate values: one with 5 columns from the left half, and the other
  with 5 columns from the right half of the table. You might need to experiment with the column choice for best results.

### Create names for the columns that don’t have a name in the document

If the first column in the document doesn’t have a name, you must create that name yourself when defining the value. You can approach it
in the following ways:

- Use the table title or a significant part of the title.
- Create a descriptive name that represents the data in the column; for example, `description`, `type of asset`, `year`, `category`.

### Compare data from two different periods of time

If you want to compare data from two different periods of time, for example, years 2023 and 2024 in financial documents such as annual reports,
you can prefix the columns with “current” and “previous”.

## Examples: Extract information from a purchase and sale agreement

The following examples extract information from the condominium purchase and sale agreement
which you can view in the [Question optimization for extracting information](#label-ai-extract-question-optimization) section.

### Extract an entity

Extract the seller name and the offer expiration date:

Copy code

```
SELECT AI_EXTRACT(
  file => TO_FILE('@db.schema.stage','document.pdf'),
  responseFormat => [['seller_name', 'What is the seller name?'], ['address', 'What is the offer expiration date?']]
);
```

Result:

Copy code

```
{
    "error": null,
    "response": {
        "address": "12/12/2023",
        "seller_name": "Paul Doyle"
    }
}
```

### Extract checkbox information

Extract information about items that are not included, based on the checkboxes marked in the document:

Copy code

```
SELECT AI_EXTRACT(
  file => TO_FILE('@db.schema.stage','document.pdf'),
  responseFormat => [['flat_items', 'What items are not included with the flat?'], ['default', 'What Default is selected?']]
);
```

Result:

Copy code

```
{
    "error": null,
    "response": {
        "default": "Forfeiture of Earnest Money",
        "flat_items": "dryer, security system, satellite dish, wood stove, fireplace insert, hot tub, attached speaker(s), generator, other"
    }
}
```

### Extract signature status

Extract information about whether the agreement has been signed:

Copy code

```
SELECT AI_EXTRACT(
    file => TO_FILE('@db.schema.stage','document.pdf'),
    responseFormat => [['signature', 'Is this document signed?']]
);
```

Result:

Copy code

```
{
  "error": null,
    "response": {
        "signature": "no"
    }
}
```

### Extract a list of entities

Extract a list of buyer names:

Copy code

```
SELECT AI_EXTRACT(
    file => TO_FILE('@db.schema.files', 'report.pdf'),
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
    }
);
```

Result:

Copy code

```
{
    "error": null,
    "response": {
        "buyer_list": [
        "John Davis",
        "Jane Davis"
        ]
    }
}
```

## Example: Extract information from a table

This example extracts information from the following document:

![Table: Granger Causality Tests - P-values](/static/images/cortex-document/granger-causality.png)

Copy code

```
SELECT AI_EXTRACT(
    file => TO_FILE('@db.schema.files', 'report.pdf'),
    responseFormat => {
        'schema': {
            'type': 'object',
            'properties': {
                'income_table': {
                'description': 'Table 2: Granger Causality Tests - P-values',
                'type': 'object',
                'column_ordering': ['description', 'countries','lags','z','z_approx'],
                'properties': {
                    'description': {
                        'description': 'Description',
                        'type': 'array'
                        },
                    'countries': {
                        'description': 'Countries',
                        'type': 'array'
                        },
                    'lags': {
                        'description': 'Lags',
                        'type': 'array'
                        },
                    'z': {
                        'description': 'Z',
                        'type': 'array'
                    },
                    'z_approx': {
                        'description': 'Z approx.',
                        'type': 'array'
                    }
                }
            }
        }
    }
);
```

Result:

Copy code

```
{
    "error": null,
    "response": {
        "income_table": {
            "countries": [
                "33","80","29","84","34"
            ],
            "description": [
                "Commodity exporters",
                "Non-commodity exporters",
                "AE",
                "EMDE",
                "Large or market-dominant countries"
            ],
            "lags": [
                "2","1","1","1","1"
            ],
            "z": [
                "0.11","0.08","0.89","0.12","0.07"
            ],
            "z_approx": [
                "0.25","0.19","0.95","0.25","0.14"
            ]
        }
    }
}
```

## Legal notices

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Generally available functions are Covered AI Features. Preview functions are Preview AI Features.  [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
