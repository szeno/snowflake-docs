Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# ALL\_SPACE\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are not empty but contain only whitespace characters. The percentage is computed
over
the total row count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.ALL_SPACE_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- Whitespace characters are spaces, tabs, line breaks, other ASCII whitespace characters, and the no-break space (U+00A0). Other
  Unicode space characters, such as the ideographic space (U+3000), are not treated as whitespace.
- The empty string `''` is not counted. To count empty strings, use
  [EMPTY\_STRING\_PERCENT](/sql-reference/functions/dmf_empty_string_percent).

## Example

Measure the percentage of whitespace-only values in the `comment` column:

Copy code

```
SELECT SNOWFLAKE.CORE.ALL_SPACE_PERCENT(
  SELECT
    comment
  FROM crm.tables.tickets
);
```
