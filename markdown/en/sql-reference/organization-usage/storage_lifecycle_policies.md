Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# STORAGE\_LIFECYCLE\_POLICIES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays
[storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies)
in your organization.

Each row in this view corresponds to a different storage lifecycle policy.

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
| NAME | TEXT | Name of the storage lifecycle policy. |
| ID | NUMBER | Internal/system-generated identifier for the storage lifecycle policy. |
| SCHEMA\_ID | TEXT | Internal/system-generated identifier for the schema in which the policy resides. |
| SCHEMA | TEXT | Schema to which the storage lifecycle policy belongs. |
| DATABASE\_ID | TEXT | Internal/system-generated identifier for the database in which the policy resides. |
| DATABASE | TEXT | Database to which the storage lifecycle policy belongs. |
| OWNER | TEXT | Name of the role that owns the storage lifecycle policy. |
| SIGNATURE | TEXT | Type signature of the storage lifecycle policy’s arguments. |
| RETURN\_TYPE | TEXT | Return value data type. |
| BODY | TEXT | Storage lifecycle policy definition. |
| COMMENT | TEXT | Comments entered for the storage lifecycle policy (if any). |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time when the storage lifecycle policy was created. |
| LAST\_ALTERED\_ON | TIMESTAMP\_LTZ | Date and time when the storage lifecycle policy was last altered. |
| DELETED\_ON | TIMESTAMP\_LTZ | Date and time when the storage lifecycle policy was dropped. |
| OWNER\_ROLE\_TYPE | TEXT | The type of role that owns the object, either ROLE or DATABASE\_ROLE. |
| OPTIONS | OBJECT | Storage lifecycle policy options, including ARCHIVE\_FOR\_DAYS (number of days to keep data in current tier) and ARCHIVE\_TIER (target storage tier). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
