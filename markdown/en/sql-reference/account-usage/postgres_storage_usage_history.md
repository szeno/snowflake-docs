Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# POSTGRES\_STORAGE\_USAGE\_HISTORY view

This Account Usage view can be used to query the hourly storage used in byte-months for [Postgres instances](/user-guide/snowflake-postgres/about)
in the account for the last 365 days (1 year). The data includes all data stored on the instance.

## Columns

The following table provides definitions for the POSTGRES\_STORAGE\_USAGE\_HISTORY view columns.

| Column name | Data type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the usage took place. |
| TOTAL\_BYTE\_MONTHS\_STANDARD | NUMBER | Number of byte-months of standard storage used by Postgres instances. |
| TOTAL\_BYTE\_MONTHS\_HA | NUMBER | Number of byte-months of high-availability storage used by Postgres instances. |

Expand

Show lessSee more

## Usage notes

- The maximum latency for this view is three hours.
- The POSTGRES\_STORAGE\_USAGE\_HISTORY view and the Snowsight cost management tools can return different daily storage usage
  values. This discrepancy is caused by the methods used to determine storage usage. To determine these values, the
  POSTGRES\_STORAGE\_USAGE\_HISTORY view uses the current session’s [TIMEZONE](/sql-reference/parameters#label-timezone) parameter and the Snowsight cost
  management tools use Coordinated Universal Time (UTC). To resolve any discrepancies, Snowflake recommends setting the TIMEZONE
  parameter to UTC.
