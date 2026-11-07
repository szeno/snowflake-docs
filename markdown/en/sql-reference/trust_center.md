# TRUST\_CENTER schema

In the SNOWFLAKE database, the TRUST\_CENTER schema contains views that contain data about the
[Trust Center extensions](/user-guide/trust-center/trust-center-extensions), and stored procedures for organization-level
scanner configuration.

## TRUST\_CENTER views

The TRUST\_CENTER schema provides the following views:

| View | Notes |
| --- | --- |
| [EXTENSIONS](/sql-reference/trust_center/extensions) | Data is retained for 14 days. |

Expand

Show lessSee more

## TRUST\_CENTER stored procedures

The TRUST\_CENTER schema also provides stored procedures that set organization-level scanner package and scanner defaults.
For syntax and examples, see [Trust Center organization-level configuration procedures](/sql-reference/trust_center/trust-center-org-config).

## Accessing views in the TRUST\_CENTER schema

The SNOWFLAKE.TRUST\_CENTER\_VIEWER or SNOWFLAKE.TRUST\_CENTER\_ADMIN application role can execute SELECT
operations on the views in this schema.

## General usage notes

- The Snowflake-specific views are subject to change. Avoid selecting all columns from these views. Instead, select the columns that you want.
  For example, if you want the `name` column, use `SELECT name`, rather than `SELECT *`.
- The rows that are returned in a query of a view depend on the privileges that are granted to the user’s current role.
  When you query a view in the TRUST\_CENTER schema, only objects for which the current role is granted access
  privileges are returned.
