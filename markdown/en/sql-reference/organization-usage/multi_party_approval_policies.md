Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# MULTI\_PARTY\_APPROVAL\_POLICIES view

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view returns one row for each [Multi-party Approval](/user-guide/multi-party-approval)
policy in an account.

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
| ID | NUMBER | Internal/system-generated identifier for the Multi-party Approval policy. |
| NAME | VARCHAR | Name of the Multi-party Approval policy. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema in which the policy resides. |
| SCHEMA | VARCHAR | Schema to which the Multi-party Approval policy belongs. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database in which the policy resides. |
| DATABASE | VARCHAR | Database to which the Multi-party Approval policy belongs. |
| OWNER | VARCHAR | Name of the role that owns the Multi-party Approval policy. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| POLICY\_DEFINITION | VARCHAR | The full YAML body of the policy, including its rules, operations, and approvers. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the Multi-party Approval policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the Multi-party Approval policy was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the Multi-party Approval policy was dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
