[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# REPLICATION\_GROUPS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Organization Usage view displays a row for each
[replication group and failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups) in each account in your organization.

The returned results include details such as the replication or failover group name,
the types of objects that it applies to, and its schedule for replication refresh operations.

## Columns

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
| CREATED | TIMESTAMP\_LTZ | Date and time the replication or failover group was created. |
| DELETED | TIMESTAMP\_LTZ | Date and time the replication or failover group was deleted. |
| NAME | VARCHAR | Name of the replication or failover group. |
| TYPE | VARCHAR | Type of group. Valid values are REPLICATION or FAILOVER. |
| COMMENT | VARCHAR | Comment string. |
| OBJECT\_TYPES | VARCHAR | List of specified object types enabled for replication (and failover in the case of a FAILOVER group). |
| ALLOWED\_INTEGRATION\_TYPES | VARCHAR | List of integration types that are enabled for replication. Snowflake always includes this column in the output, even if integrations weren’t specified in the CREATE or ALTER command. |
| REPLICATION\_SCHEDULE | VARCHAR | Scheduled interval for refresh; NULL if no replication schedule is set. |
| OWNER | VARCHAR | Name of the role with the OWNERSHIP privilege on the replication or failover group. |
| IS\_LISTING\_AUTO\_FULFILLMENT\_GROUP | BOOLEAN | TRUE if the replication group is used for Cross-Cloud Auto-Fulfillment. FALSE otherwise. |
| ERROR\_INTEGRATION | VARCHAR | The name of the notification integration for the replication group or failover group to which the error notification is sent in cases of refresh failures. |
| IS\_OPTIMIZED\_REFRESH\_ENABLED | BOOLEAN | [Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open  Available to all Business Critical Edition (or higher) accounts.  TRUE if [optimized refresh](/user-guide/account-replication-config#label-optimized-refresh) is enabled for the group. FALSE otherwise. Only failover groups support optimized refresh; for replication groups the column is always FALSE. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 240 minutes (4 hours).
