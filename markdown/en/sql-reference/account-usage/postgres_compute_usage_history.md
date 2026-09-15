Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# POSTGRES\_COMPUTE\_USAGE\_HISTORY view

This Account Usage view can be used to query the total hourly compute credit usage across all [Postgres instances](/user-guide/snowflake-postgres/about)
in the account for the last 365 days (1 year).

## Columns

The following table provides definitions for the POSTGRES\_COMPUTE\_USAGE\_HISTORY view columns.

| Column name | Data type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the usage took place. |
| CREDITS\_USED | NUMBER | Number of compute credits consumed by Postgres instances. |

Expand

Show lessSee more

## Usage notes

- The maximum latency for this view is three hours.
- The POSTGRES\_COMPUTE\_USAGE\_HISTORY view and the Snowsight cost management tools can return different daily compute usage
  values. This discrepancy is caused by the methods used to determine compute usage. To determine these values, the
  POSTGRES\_COMPUTE\_USAGE\_HISTORY view uses the current session’s [TIMEZONE](/sql-reference/parameters#label-timezone) parameter, and the Snowsight cost
  management tools use Coordinated Universal Time (UTC). To resolve any discrepancies, Snowflake recommends setting the TIMEZONE
  parameter to UTC.
