Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SESSION\_POLICIES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view provides the [session policies](/user-guide/session-policies) in your account.

Each row in this view corresponds to a different session policy.

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
| ID | NUMBER | Internal/system-generated identifier for the session policy. |
| NAME | VARCHAR | Name of the session policy. |
| SCHEMA\_ID | VARCHAR | Internal/system-generated identifier for the schema in which the policy resides. |
| SCHEMA | VARCHAR | Schema to which the session policy belongs. |
| DATABASE\_ID | VARCHAR | Internal/system-generated identifier for the database in which the policy resides. |
| DATABASE | VARCHAR | Database to which the session policy belongs. |
| OWNER | VARCHAR | Name of the role that owns the session policy. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| SESSION\_IDLE\_TIMEOUT\_MINS | NUMBER | Session idle timeout in minutes for the policy. |
| SESSION\_UI\_IDLE\_TIMEOUT\_MINS | NUMBER | UI session idle timeout in minutes for the policy. |
| SESSION\_MAX\_LIFESPAN\_MINS | NUMBER | Maximum session lifespan in minutes for the policy. |
| SESSION\_UI\_MAX\_LIFESPAN\_MINS | NUMBER | Maximum UI session lifespan in minutes for the policy. |
| COMMENT | VARCHAR | Comments entered for the session policy (if any). |
| CREATED | TIMESTAMP\_LTZ | Date and time when the session policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the session policy was dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
