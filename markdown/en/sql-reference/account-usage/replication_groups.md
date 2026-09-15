Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# REPLICATION\_GROUPS view

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view displays a row for each
[replication group and failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups) in the account.

The returned results include details such as the replication or failover group name,
the types of objects that it applies to, and its schedule for replication refresh operations.

## Columns

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

- Latency for the view may be up to 120 minutes (2 hours).

## Examples

The following example returns the active failover groups for your Snowflake account:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.REPLICATION_GROUPS
  WHERE type = 'FAILOVER' AND deleted IS NULL
  ORDER BY name;
```
