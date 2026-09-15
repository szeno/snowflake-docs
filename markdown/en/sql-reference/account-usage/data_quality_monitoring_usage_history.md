Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DATA\_QUALITY\_MONITORING\_USAGE\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The DATA\_QUALITY\_MONITORING\_USAGE\_HISTORY view in the ACCOUNT\_USAGE schema records the daily credit consumption for data metric function
evaluations on tables in an account within the last 365 days (1 year).

See also:
:   [Introduction to data quality checks](/user-guide/data-quality-intro)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| CREDITS\_USED | NUMBER | Number of credits billed for data metric function evaluations on the table. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table monitored by data metric functions. |
| TABLE\_NAME | VARCHAR | Name of the table. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that stores the table. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that stores the table. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that stores the table. |
| DATABASE\_NAME | VARCHAR | Name of the database that stores the table. |

Expand

Show lessSee more

## Usage notes

Latency for the view may be up to 180 minutes (3 hours).
