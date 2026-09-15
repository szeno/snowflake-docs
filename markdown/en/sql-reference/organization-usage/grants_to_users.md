Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# GRANTS\_TO\_USERS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to query the roles that have been granted to a user.

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
| CREATED\_ON | TIMESTAMP\_LTZ | Time and date (in the UTC time zone) when the role is granted. |
| DELETED\_ON | TIMESTAMP\_LTZ | Time and date (in the UTC time zone) when the role is revoked. |
| ROLE | VARCHAR | Identifier for the role granted to the user. |
| GRANTED\_TO | VARCHAR | For this view, the value is `USER`. |
| GRANTEE\_NAME | VARCHAR | Name of the user to whom the privilege is granted. |
| GRANTED\_BY | VARCHAR | Identifier for the role that granted the privilege. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The GRANTS\_TO\_USERS view **does not** include grants of privileges and non-account roles to users. For that information, see the
  [GRANTS\_TO\_ROLES view](/sql-reference/organization-usage/grants_to_roles).
- This view records current grants and historical grants, including grants that were revoked and granted again. When a single grant occurs
  and as long as it remains active (that is, not revoked):

  - The view includes one row for the grant of the same role to the same user.
  - A regrant of the same role to the same user is not recorded as a new row. Instead, the DELETED\_ON column remains NULL while the grant
    is active.
- When a grant is revoked from the user, the DELETED\_ON column for the grant is updated from NULL to the timestamp when the grant was
  revoked.
- After revoking the role from the user, a grant of the same role to the same user is recorded in a new row. In this new row, the
  DELETED\_ON column value is NULL because the grant is now active.
