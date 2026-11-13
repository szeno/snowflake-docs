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

Snowflake can evaluate anomaly detection checks for multiple tables in a schema as a batch. This view attributes the batch’s compute
cost to the participating tables in proportion to the number of data metric function (DMF) associations for each table in the batch.
For example, if a batch contains two DMF associations for one table and one for another, approximately two-thirds of the batch’s compute
cost is attributed to the first table and one-third to the second. These proportions describe cost allocation within a batch. They don’t
imply that the batch costs the same as evaluating each DMF separately.

This allocation applies to [schema-level anomaly detection](/user-guide/data-quality-schema-level). It doesn’t change how costs are
attributed for individual table evaluations.
