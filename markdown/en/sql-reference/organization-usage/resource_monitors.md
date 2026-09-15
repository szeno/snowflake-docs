Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# RESOURCE\_MONITORS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays the resource monitors that have been created in the accounts within the organization. It does not
include resource monitors from reader accounts.

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

| Column | Data Type | Description |
| --- | --- | --- |
| RESOURCE\_MONITOR\_ID | NUMBER | System identifier. |
| NAME | VARCHAR | Name of the resource monitor. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the resource monitor was created. |
| CREDIT\_QUOTA | VARIANT | Monthly credit quota for the resource monitor. |
| USED\_CREDITS | VARIANT | Number of credits used in the current monthly billing cycle by all the warehouses associated with the resource monitor. |
| REMAINING\_CREDITS | FLOAT | Number of credits still available to use in the current monthly billing cycle. |
| OWNER | VARCHAR | Name of the role that owns the resource monitor. |
| NOTIFY | NUMBER | Percentage of the credit quota. When consumption reaches this threshold, notifications are sent. |
| SUSPEND | NUMBER | Percentage of the credit quota. When consumption reaches this threshold, assigned warehouses are suspended but currently running queries are allowed to complete. |
| SUSPEND\_IMMEDIATE | NUMBER | Percentage of the credit quota. When consumption reaches this threshold, all assigned warehouses are suspended immediately, including those running queries. |
| WAREHOUSES | VARCHAR | Names of the warehouses that are associated with the resource monitor. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
