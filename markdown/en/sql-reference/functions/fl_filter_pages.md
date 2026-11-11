Categories:
:   [File functions](/sql-reference/functions-file) (AI Functions)

# FL\_FILTER\_PAGES

Selects pages of a multi-page document for processing by [Cortex AI Functions for document intelligence](/user-guide/snowflake-cortex/ai-documents).

Use this function as the file argument of AI\_EXTRACT or AI\_PARSE\_DOCUMENT when you only need part of a
document. The function processes the pages you select instead of the whole document.

See also:
:   [AI\_EXTRACT](/sql-reference/functions/ai_extract) , [AI\_PARSE\_DOCUMENT](/sql-reference/functions/ai_parse_document)

## Syntax

Copy code

```
FL_FILTER_PAGES( <file> , <pages> )
```

## Arguments

`file`
:   A [FILE](/sql-reference/data-types-unstructured#label-data-types-file) value that refers to a multi-page document.

`pages`
:   An [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) of objects, each of which selects a range of pages. The array must contain
    at least one object and at most 4,096.

    Each object can contain a `start` field, an `end` field, or both. Both fields are signed integers and
    specify the first (inclusive) and last (exclusive) page of the range. Page indexes start at 0. For example,
    `{'start': 0, 'end': 3}` selects the first three pages.

    Omit either field to leave that end of the range open. An omitted `start` means the first page of the
    document, and an omitted `end` means the last page. Use a negative value to count backward from the end of
    the document: `{'start': -3}` selects the last three pages, and `{'end': -1}` selects everything except the
    last page.

Both arguments accept columns, so you can select different pages for each row of a batch.

## Returns

A FILE value that carries the page selection. Pass it directly as the file argument of AI\_EXTRACT and
AI\_PARSE\_DOCUMENT functions, which then process only the selected pages.

## Usage notes

- FL\_FILTER\_PAGES is only meaningful as the file argument of a Cortex AI Function for document processing
  that supports page ranges. Today those functions are AI\_EXTRACT and AI\_PARSE\_DOCUMENT. Used anywhere else,
  the statement fails to compile.
- `end` is always exclusive, whether it’s positive, negative, or omitted. This is the same rule that
  [ARRAY\_SLICE](/sql-reference/functions/array_slice) uses.
- Ranges that reach past the document are clamped rather than rejected. On a 10-page document, both
  `[{'start': -100}]` and `[{'end': 100}]` select the whole document.
- Each object in the array selects pages from the original document, independently of the others. The
  result is the union of all the ranges: overlapping ranges don’t process a page twice, and pages are
  processed in document order no matter what order you write the objects in.
- To process the whole document, either omit FL\_FILTER\_PAGES or pass `[{}]`, which is an explicit
  “all pages” selection.
- You can’t select pages both with FL\_FILTER\_PAGES and with the `page_filter` option of the same call.
  There’s no precedence rule and the two selections aren’t merged, so specify the pages in one place only.
- A page selection applies only to the call you write it in. It isn’t stored on the FILE value, and later
  operations on that value don’t honor it.
- Page indexes in the result are indexes in the original document. Selecting pages 7, 8, and 9 doesn’t
  renumber them to 0, 1, and 2, and a selection with a gap in it doesn’t close that gap.
- Page counts in a response tell you how many pages were processed, not which ones. They aren’t a reliable
  way to confirm how a relative range resolved.
- An input that isn’t paginated, such as plain text, can’t be filtered by page and returns an error.

## Error conditions

Errors are reported per row: the offending row fails and the rest of the query continues.

| Condition | Result |
| --- | --- |
| The array is empty or isn’t an array. | Rejected. A selection, when you supply one, needs at least one object. |
| The array contains more than 4,096 objects. | Rejected. The whole call fails, so a selection is never silently narrowed to the first 4,096 ranges. |
| An item isn’t an object, or contains a field other than `start` and `end`. | Rejected. |
| `start` or `end` is present but isn’t an integer. This includes NULL, a decimal value, a string, and a value outside the range of a signed 32-bit integer. | Rejected. Omitting a field is valid; setting it to NULL isn’t. |
| Both fields are present, both are non-negative or both are negative, and `end` is less than or equal to `start`. | Rejected. Ranges such as `{'start': 3, 'end': 3}`, `{'start': 5, 'end': 2}`, and `{'start': -1, 'end': -2}` are empty for every document. |
| `end` is 0, whatever `start` is. | Rejected. Ranges such as `{'end': 0}` and `{'start': -3, 'end': 0}` are empty for every document. |
| The selection is valid but resolves to no pages for a particular document. | AI\_PARSE\_DOCUMENT fails the row. AI\_EXTRACT returns an empty result for the row. |

Expand

Show lessSee more

Any other range, including one that mixes a negative value with a non-negative one, is accepted and
resolved against the actual number of pages in each document.

## Examples

The examples in this section use a 10-page document, with pages numbered 0 through 9.

Parse the first three pages:

Copy code

```
SELECT AI_PARSE_DOCUMENT(
  FL_FILTER_PAGES(TO_FILE(BUILD_STAGE_FILE_URL('@mystage', 'contract.pdf')), [{'start': 0, 'end': 3}]),
  {'mode': 'LAYOUT'}
);
```

Extract from the last three pages, which is where signatures usually are:

Copy code

```
SELECT AI_EXTRACT(
  FL_FILTER_PAGES(TO_FILE(BUILD_STAGE_FILE_URL('@mystage', 'contract.pdf')), [{'start': -3}]),
  {'signed_by': 'Who signed this contract?'}
);
```

Skip the cover page and the back page:

Copy code

```
SELECT AI_PARSE_DOCUMENT(
  FL_FILTER_PAGES(TO_FILE(BUILD_STAGE_FILE_URL('@mystage', 'contract.pdf')), [{'start': 1, 'end': -1}]),
  {'mode': 'LAYOUT'}
);
```

Select the first page and the last page with two ranges. The result is pages 0 and 9:

Copy code

```
SELECT AI_PARSE_DOCUMENT(
  FL_FILTER_PAGES(TO_FILE(BUILD_STAGE_FILE_URL('@mystage', 'contract.pdf')), [{'end': 1}, {'start': -1}]),
  {'mode': 'LAYOUT'}
);
```

Select different pages for each row by passing columns as both arguments:

Copy code

```
SELECT AI_PARSE_DOCUMENT(FL_FILTER_PAGES(doc, page_ranges), {'mode': 'LAYOUT'})
  FROM contracts;
```
