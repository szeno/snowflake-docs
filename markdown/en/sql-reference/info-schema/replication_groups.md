# REPLICATION\_GROUPS view

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Information Schema view displays a row for each primary and secondary replication and/or failover group in your organization.

Note

This view uses Snowflake terminology of “database”, whereas other Information Schema views use the standard INFORMATION\_SCHEMA
terminology of “catalog”. The two terms have the same meaning.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| REGION\_GROUP | VARCHAR | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the account that stores the replication or failover group is located. |
| SNOWFLAKE\_REGION | VARCHAR | Snowflake Region where the account is located. A Snowflake Region is a distinct location within a cloud platform region that is isolated from other Snowflake Regions. A Snowflake Region can be either multi-tenant or single-tenant (for a Virtual Private Snowflake account). |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time replication or failover group was created. |
| ACCOUNT\_NAME | VARCHAR | Name of the account. |
| NAME | VARCHAR | Name of the replication or failover group. |
| TYPE | VARCHAR | Type of group. Valid values are `REPLICATION` or `FAILOVER`. |
| COMMENT | VARCHAR | Comment string. |
| IS\_PRIMARY | VARCHAR | Indicates whether the replication or failover group is the primary group. |
| PRIMARY | VARCHAR | Name of the primary group. |
| OBJECT\_TYPES | VARCHAR | List of specified object types enabled for replication (and failover in the case of a `FAILOVER` group). |
| ALLOWED\_INTEGRATION\_TYPES | VARCHAR | List of integration types that are enabled for replication. Snowflake always includes this column in the output even if integrations were not specified in the CREATE *<object>* or ALTER *<object>* command. |
| ALLOWED\_ACCOUNTS | VARCHAR | List of accounts enabled for replication and failover. |
| ORGANIZATION\_NAME | VARCHAR | Name of your Snowflake organization. |
| ACCOUNT\_LOCATOR | VARCHAR | Account locator in a region. |
| REPLICATION\_SCHEDULE | VARCHAR | Scheduled interval for refresh; NULL if no replication schedule is set. |
| SECONDARY\_STATE | VARCHAR | Current state of scheduled refresh. Valid values are `started` or `suspended`. NULL if no replication schedule is set. |
| NEXT\_SCHEDULED\_REFRESH | TIMESTAMP\_LTZ | Date and time of the next scheduled refresh. |
| OWNER | VARCHAR | Name of the role with the OWNERSHIP privilege on the replication or failover group. NULL if the replication or failover group is in a different region. |
| IS\_LISTING\_AUTO\_FULFILLMENT\_GROUP | BOOLEAN | TRUE if the replication group is used for [Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment). FALSE otherwise. |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges. The view does not honor the MANAGE GRANTS privilege and consequently may show less
  information compared to a SHOW command when both are executed by a user who holds the MANAGE GRANTS privilege.
