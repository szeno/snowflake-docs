Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_FR\_INSEE\_CODE\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are not a French INSEE commune code. The percentage is computed over the total row
count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_FR_INSEE_CODE_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- The value must be a department code (`01` to `19`, `2A`, `2B`, or `21` to `95`) followed by three digits, or an overseas code
  (`971` to `978` or `986` to `988`) followed by two digits.
- Letters are matched case-insensitively.
- The whole value must match. A value with leading or trailing whitespace, or with separators other than the ones described
  here, is
  counted.
- An INSEE commune code is not a postal code. To check postal codes, use
  [INVALID\_FR\_POSTAL\_CODE\_PERCENT](/sql-reference/functions/dmf_invalid_fr_postal_code_percent).
- The function checks the format only; it does not verify that the commune exists.

## Example

Measure the percentage of invalid French INSEE commune codes in the `insee_code` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_FR_INSEE_CODE_PERCENT(
  SELECT
    insee_code
  FROM crm.tables.addresses
);
```
