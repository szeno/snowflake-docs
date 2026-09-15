Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SHARES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view returns the shares owned by the accounts in your organization, including dropped shares.

Each row in this view corresponds to a different share.

This view is available only in the [organization account](/user-guide/organization-accounts). Users with the GLOBALORGADMIN role, or users granted the SNOWFLAKE.ORGANIZATION\_SECURITY\_VIEWER application role, can access it. For details, see [Accessing the ORGANIZATION\_USAGE schema](/sql-reference/organization-usage#label-org-usage-access-org-account).

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
| CREATED\_ON | TIMESTAMP\_LTZ | The timestamp when the share was created. |
| MODIFIED\_ON | TIMESTAMP\_LTZ | The timestamp when the share was last updated. |
| DELETED\_ON | TIMESTAMP\_LTZ | The timestamp when the share was deleted. This value is NULL if the share hasn’t been deleted. |
| NAME | VARCHAR | The name of the share. |
| OWNER | VARCHAR | The name of the role that owns the share. |
| COMMENT | VARCHAR | Comment associated with the share, if any. |
| DATABASE\_NAME | VARCHAR | The name of the primary database associated with the share. This field is empty if no database has been granted to the share. |
| SECURE\_OBJECTS\_ONLY | BOOLEAN | Indicates whether the share can only have secure objects granted to it. |
| TARGET\_ACCOUNTS | VARCHAR | A comma-separated list of target accounts the share is shared with (outbound). This field is empty if the share has no target accounts. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global unique name of the listing associated with the share, if any. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
