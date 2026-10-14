Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_UK\_POSTAL\_CODE\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-`NULL` column values that are not a UK postcode in the outward and inward form.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_UK_POSTAL_CODE_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `NUMBER` value. `NULL` values are not counted.

## Usage notes

- The value must be an outward code (`A9`, `A99`, `AA9`, `AA99`, `A9A`, or `AA9A`), an optional single space, and an inward
  code (a
  digit and two letters).
- The first letter cannot be Q, V, or X, and the second letter cannot be I, J, or Z. The third letter of an `A9A` outward code
  is one
  of A to H, J, K, P, S, T, U, or W. The fourth letter of an `AA9A` outward code is one of A, B, E, H, M, N, P, R, V, W, X, or
  Y.
  The two letters of the inward code cannot be C, I, K, M, O, or V.
- The special postcodes `GIR 0AA` and `XM4 5HQ` are valid.
- Letters are matched case-insensitively.
- The whole value must match. A value with leading or trailing whitespace, or with separators other than the ones described
  here, is
  counted.
- The function checks the format only; it does not verify that the postcode is assigned.

## Example

Measure the number of invalid UK postcodes in the `postcode` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_UK_POSTAL_CODE_COUNT(
  SELECT
    postcode
  FROM crm.tables.addresses
);
```
