Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_EMAIL\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-NULL column values that are not a valid email address.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_EMAIL_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a NUMBER value. NULL values are not counted.

## Usage notes

- The function applies a regular-expression format check; it does not verify that an address or domain exists.
- The function matches the whole string against a regular expression. The local part uses ASCII letters, digits, underscore, percent, plus, or hyphen; periods can separate non-empty local-part segments. Domain labels start and end with a letter or digit and can contain internal hyphens. The final domain label must contain at least two letters.

## Example

Measure the number of invalid email addresses in the `email` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_EMAIL_COUNT(
  SELECT
    email
  FROM crm.tables.contacts
);
```
