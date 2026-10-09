Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_EMAIL\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are not a valid email address. The percentage is computed over the total row count,
including NULL values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_EMAIL_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a FLOAT value.

## Usage notes

- The function applies a regular-expression format check; it does not verify that an address or domain exists.
- The function matches the whole string against a regular expression. The local part uses ASCII letters, digits, underscore, percent, plus, or hyphen; periods can separate non-empty local-part segments. Domain labels start and end with a letter or digit and can contain internal hyphens. The final domain label must contain at least two letters.

## Example

Measure the percentage of invalid email addresses in the `email` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_EMAIL_PERCENT(
  SELECT
    email
  FROM crm.tables.contacts
);
```
