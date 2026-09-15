Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# WAREHOUSE\_LOAD\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to analyze the workload on your warehouse within a specified date range.

See also:
:   [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/organization-usage/warehouse_metering_history)

## Columns

Note

For the output columns of this view, the query load value is the ratio of the total execution time (in seconds) of all queries in a
specific state in an interval by the total time (in seconds) for that interval.

For example, if 276 seconds was the total time for 4 queries in a 5 minute (300 second) interval, then the query load value is
276 / 300 = 0.92.

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The start of the specified time range (in the UTC time zone) in which the warehouse usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The end of the specified time range (in the UTC time zone) in which the warehouse usage took place. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse. |
| AVG\_RUNNING | NUMBER(38,9) | Query load value for queries executed. |
| AVG\_QUEUED\_LOAD | NUMBER(38,9) | Query load value for queries queued because the warehouse was overloaded. |
| AVG\_QUEUED\_PROVISIONING | NUMBER(38,9) | Query load value for queries queued because the warehouse was being provisioned. |
| AVG\_BLOCKED | NUMBER(38,9) | Query load value for queries blocked by a transaction lock. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- Load history is shown in 5-minute intervals.
