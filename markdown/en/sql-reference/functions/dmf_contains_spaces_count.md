Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# CONTAINS\_SPACES\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-`NULL` column values that contain at least one space, tab, or no-break space.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.CONTAINS_SPACES_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `NUMBER` value. `NULL` values are not counted.

## Usage notes

- The function counts a value that contains a space, a tab, or a no-break space (U+00A0) anywhere in the value. A value whose
  only
  whitespace is a line break is not counted.
- To count only values with leading or trailing whitespace, use
  [UNTRIMMED\_STRING\_COUNT](/sql-reference/functions/dmf_untrimmed_string_count).

## Example

Measure the number of values that contain spaces in the `username` column:

Copy code

```
SELECT SNOWFLAKE.CORE.CONTAINS_SPACES_COUNT(
  SELECT
    username
  FROM crm.tables.accounts
);
```
