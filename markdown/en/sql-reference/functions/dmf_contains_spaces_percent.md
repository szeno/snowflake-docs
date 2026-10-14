Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# CONTAINS\_SPACES\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that contain at least one space, tab, or no-break space. The percentage is computed
over the
total row count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.CONTAINS_SPACES_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- The function counts a value that contains a space, a tab, or a no-break space (U+00A0) anywhere in the value. A value whose
  only
  whitespace is a line break is not counted.
- To count only values with leading or trailing whitespace, use
  [UNTRIMMED\_STRING\_PERCENT](/sql-reference/functions/dmf_untrimmed_string_percent).

## Example

Measure the percentage of values that contain spaces in the `username` column:

Copy code

```
SELECT SNOWFLAKE.CORE.CONTAINS_SPACES_PERCENT(
  SELECT
    username
  FROM crm.tables.accounts
);
```
