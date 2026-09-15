[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# PRIVACY\_POLICIES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Organization Usage view provides the [privacy policies](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies) defined in each account in your organization.

Each row in this view corresponds to a different privacy policy.

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
| ID | NUMBER | Internal/system-generated identifier for the privacy policy. |
| NAME | VARCHAR | Name of the privacy policy. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the privacy policy. |
| SCHEMA | VARCHAR | Schema that contains the privacy policy. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the privacy policy. |
| DATABASE | VARCHAR | Database that contains the privacy policy. |
| OWNER | VARCHAR | Name of the role that owns the privacy policy. |
| COMMENT | VARCHAR | Comment for the privacy policy, if any. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the privacy policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the privacy policy was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the privacy policy was dropped. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 240 minutes (4 hours).
