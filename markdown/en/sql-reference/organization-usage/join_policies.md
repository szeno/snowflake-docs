Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# JOIN\_POLICIES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view lists the [join policies](/user-guide/join-policies) defined in each account in your organization.

Each row in this view corresponds to a different join policy.

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
| POLICY\_ID | NUMBER | Internal/system-generated identifier for the policy. |
| POLICY\_NAME | VARCHAR | Name of the policy. |
| POLICY\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema in which the policy resides. |
| POLICY\_SCHEMA | VARCHAR | Schema that contains the policy. |
| POLICY\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database in which the policy resides. |
| POLICY\_CATALOG | VARCHAR | Database to which the policy belongs. |
| POLICY\_OWNER | VARCHAR | Name of the role that owns the policy. |
| POLICY\_SIGNATURE | VARCHAR | Type signature of the policy’s arguments. |
| POLICY\_RETURN\_TYPE | VARCHAR | Return value data type. |
| POLICY\_BODY | VARCHAR | Policy definition. |
| POLICY\_COMMENT | VARIANT | Comments entered for the policy (if any). |
| CREATED | TIMESTAMP\_LTZ | Date and time when the policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the policy was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the policy was dropped. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 240 minutes (4 hours).
