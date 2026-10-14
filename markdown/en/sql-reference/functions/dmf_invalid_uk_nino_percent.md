Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_UK\_NINO\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are not a UK National Insurance number: two letters, six digits, and a letter
from A to
D. The percentage is computed over the total row count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_UK_NINO_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- The value must be two prefix letters, six digits, and a suffix letter from A to D, written either without spaces
  (`AB123456C`) or
  in the printed form `AB 12 34 56 C`.
- The first prefix letter cannot be D, F, I, Q, U, or V, and the second cannot be D, F, I, O, Q, U, or V. The prefixes BG, GB,
  KN, NK,
  NT, TN, and ZZ are never allocated and are counted.
- Letters are matched case-insensitively.
- The whole value must match. A value with leading or trailing whitespace, or with separators other than the ones described
  here, is
  counted.
- The function checks the format only; it does not verify that the number was issued.

## Example

Measure the percentage of invalid UK National Insurance numbers in the `ni_number` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_UK_NINO_PERCENT(
  SELECT
    ni_number
  FROM hr.tables.employees
);
```
