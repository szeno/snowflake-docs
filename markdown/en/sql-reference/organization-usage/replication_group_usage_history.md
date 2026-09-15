Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# REPLICATION\_GROUP\_USAGE\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The REPLICATION\_GROUP\_USAGE\_HISTORY view in the ORGANIZATION\_USAGE schema can be used to query the replication history for
replication and failover groups in your organization within a specified date range. The view includes the name of the
replication or failover group, credits consumed, and bytes transferred for replication.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization where the usage took place. |
| ACCOUNT\_NAME | VARCHAR | Name of the account where the usage took place. |
| ACCOUNT\_LOCATOR | VARCHAR | Name of the account locator. |
| REGION | VARCHAR | Name of the region where the account is located. |
| USAGE\_DATE | DATE | Date (in the UTC time zone) of this usage record. |
| REPLICATION\_GROUP\_NAME | VARCHAR | Name of the replication or failover group. |
| REPLICATION\_GROUP\_ID | NUMBER | Internal/system-generated identifier for the replication or failover group. |
| CREDITS\_USED | NUMBER | Total number of credits used for replication during the USAGE\_DATE. |
| BYTES\_TRANSFERRED | NUMBER | Number of bytes transferred for replication during the USAGE\_DATE. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours (1 day).
- The data is retained for 365 days (1 year).
