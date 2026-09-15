Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# REPLICATION\_USAGE\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The REPLICATION\_USAGE\_HISTORY view in the ORGANIZATION\_USAGE schema can
be used to query the replication history for databases in your organization
within a specified date range. The view includes
the database name, credits consumed, and bytes transferred for replication.

Note

This view only displays replication usage for database replication.
To view usage for replication using [replication and failover groups](/user-guide/account-replication-intro#label-replication-and-failover-groups),
see the [REPLICATION\_GROUP\_USAGE\_HISTORY view](/sql-reference/organization-usage/replication_group_usage_history).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization where the usage took place. |
| ACCOUNT\_NAME | VARCHAR | Name of the account where the usage took place. |
| ACCOUNT\_LOCATOR | VARCHAR | Name of the account locator. |
| REGION | VARCHAR | Name of the region where the account is located. |
| USAGE\_DATE | DATE | Date (in the UTC time zone) of this usage record. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database. |
| DATABASE\_NAME | VARCHAR | Name of the database. |
| CREDITS\_USED | NUMBER | Total number of credits used for database replication during the USAGE\_DATE. |
| BYTES\_TRANSFERRED | VARCHAR | Number of bytes transferred for database replication during the USAGE\_DATE. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours (1 day).
- The data is retained for 365 days (1 year).
