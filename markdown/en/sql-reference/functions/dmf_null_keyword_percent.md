Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# NULL\_KEYWORD\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are a text placeholder for a missing value, such as `'null'` or `'n/a'`, rather
than a
SQL `NULL`. The percentage is computed over the total row count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.NULL_KEYWORD_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- The function counts the values `none`, `null`, `nil`, `nothing`, and `n/a`. Matching is case-insensitive and ignores leading
  and
  trailing whitespace, including no-break spaces.
- SQL `NULL` values, empty strings, and other placeholders such as `na` or `-` are not counted. To count SQL `NULL` values, use
  [NULL\_PERCENT](/sql-reference/functions/dmf_null_percent).

## Example

Measure the percentage of text placeholders for missing values in the `middle_name` column:

Copy code

```
SELECT SNOWFLAKE.CORE.NULL_KEYWORD_PERCENT(
  SELECT
    middle_name
  FROM hr.tables.employees
);
```
