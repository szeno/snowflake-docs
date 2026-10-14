Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_IT\_FISCAL\_CODE\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are not an Italian fiscal code (codice fiscale) in the sixteen-character form. The
percentage is computed over the total row count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_IT_FISCAL_CODE_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- The value must be six letters, a two-digit year, a month letter (A, B, C, D, E, H, L, M, P, R, S, or T), a two-digit day, a
  letter
  and three digits for the place of birth, and a final letter. The day is `01` to `31` for a male holder and `41` to `71` for a
  female holder.
- The day is not checked against the month; for example, day 31 with the February month letter is accepted.
- Omocodic codes, in which the tax office replaced digits with the letters L, M, N, or P to V, are valid.
- Letters are matched case-insensitively.
- The whole value must match. A value with leading or trailing whitespace, or with separators other than the ones described
  here, is
  counted.
- The function checks the format only; it does not validate the check character or verify the place-of-birth code.

## Example

Measure the percentage of invalid Italian fiscal codes in the `fiscal_code` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_IT_FISCAL_CODE_PERCENT(
  SELECT
    fiscal_code
  FROM hr.tables.employees
);
```
