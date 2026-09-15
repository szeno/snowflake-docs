Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# POSTGRES\_COMPUTE\_USAGE\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The POSTGRES\_COMPUTE\_USAGE\_HISTORY view in the ORGANIZATION\_USAGE schema can be
used to query the total hourly compute credit usage across all [Postgres instances](/user-guide/snowflake-postgres/about)
in your organization for the last 365 days (1 year).

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization where the usage took place. |
| ACCOUNT\_NAME | VARCHAR | Name of the account where the usage took place. |
| ACCOUNT\_LOCATOR | VARCHAR | Name of the account locator. |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the usage took place. |
| CREDITS\_USED | NUMBER | Number of compute credits consumed by Postgres instances. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours (1 day).
- The data is retained for 365 days (1 year).
- The POSTGRES\_COMPUTE\_USAGE\_HISTORY view and the Snowsight cost management tools can return different daily compute usage
  values. This discrepancy is caused by the methods used to determine compute usage. To determine these values, the
  POSTGRES\_COMPUTE\_USAGE\_HISTORY view uses the current session’s [TIMEZONE](/sql-reference/parameters#label-timezone) parameter and the Snowsight cost
  management tools use Coordinated Universal Time (UTC). To resolve any discrepancies, Snowflake recommends setting the TIMEZONE
  parameter to UTC.
