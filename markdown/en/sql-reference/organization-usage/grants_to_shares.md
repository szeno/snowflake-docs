Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# GRANTS\_TO\_SHARES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to query access control privileges that have been granted to shares owned by the accounts in your organization.

Each row in this view corresponds to a privilege granted on an object to a share.

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
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time (in the UTC time zone) when the privilege is granted to the share. |
| MODIFIED\_ON | TIMESTAMP\_LTZ | Date and time (in the UTC time zone) when the privilege is updated. |
| DELETED\_ON | TIMESTAMP\_LTZ | Date and time (in the UTC time zone) when the privilege is revoked. |
| PRIVILEGE | VARCHAR | Name of the privilege granted on the object. |
| GRANTED\_ON | VARCHAR | Object kind, such as `TABLE` or `DATABASE`, on which the privilege is granted. |
| OBJECT\_NAME | VARCHAR | Name of the object on which the privilege is granted. |
| OBJECT\_DATABASE | VARCHAR | Name of the database that contains the object on which the privilege is granted. A null value indicates that the object is not database-scoped. |
| OBJECT\_SCHEMA | VARCHAR | Name of the schema that contains the object on which the privilege is granted. A null value indicates that the object is not schema-scoped. |
| SHARE\_NAME | VARCHAR | Name of the share to which the privilege is granted. |
| GRANTED\_BY | VARCHAR | Indicates the role that authorized a privilege grant to the share. `GRANTED_BY` displays empty for privileges granted by the SNOWFLAKE system role. |
| GRANTED\_BY\_ROLE\_TYPE | VARCHAR | Either `ROLE` or `DATABASE_ROLE`. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- This view doesn’t include access control privileges to shares that have been dropped.
- This view records current grants and historical grants, including grants that were revoked or granted again.
- This view supports common data object types that can be granted to a share, including Database, Schema, Table, View, Function, Database Role, and so on.
