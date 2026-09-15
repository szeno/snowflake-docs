Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# WAREHOUSE\_METERING\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to return the hourly credit usage for one or more warehouses across all the accounts in your organization
within the last 365 days (1 year).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization where the usage took place. |
| ACCOUNT\_NAME | VARCHAR | Name of the account where the usage took place. |
| REGION | VARCHAR | Name of the region where the account is located. |
| SERVICE\_TYPE | VARCHAR | The type of service, which identifies whether the usage is for a standard or reader account. Valid values: WAREHOUSE\_METERING or WAREHOUSE\_METERING\_READER. |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the warehouse usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the warehouse usage took place. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse. |
| CREDITS\_USED | NUMBER | Total number of credits used by the warehouse in the hour. This is the sum of CREDITS\_USED\_COMPUTE and CREDITS\_USED\_CLOUD\_SERVICES. This value does not take into account the [adjustment for cloud services](/user-guide/cost-understanding-compute#label-understanding-billing-for-cloud-services-usage), and may therefore be greater than the credits that are billed. To determine how many credits were actually billed, run queries against the [METERING\_DAILY\_HISTORY view](/sql-reference/organization-usage/metering_daily_history). |
| CREDITS\_USED\_COMPUTE | NUMBER | Number of credits used for the warehouse in the hour. |
| CREDITS\_USED\_CLOUD\_SERVICES | NUMBER | Number of credits used for cloud services in the hour. |
| ACCOUNT\_LOCATOR | VARCHAR | Locator for the account where the usage took place. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 1440 minutes (24 hours).
