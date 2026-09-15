[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# CONTACTS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each [contact](/user-guide/contacts-using) in each account in your organization.

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
| CONTACT\_ID | NUMBER | Internal/system-generated identifier of the contact. |
| CONTACT\_NAME | VARCHAR | Name of the contact. |
| CONTACT\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier of the schema in which the contact exists. |
| CONTACT\_SCHEMA | VARCHAR | Name of the schema in which the contact exists. |
| CONTACT\_DATABASE\_ID | NUMBER | Internal/system-generated identifier of the database in which the contact exists. |
| CONTACT\_DATABASE | VARCHAR | Name of the database in which the contact exists. |
| CONTACT\_OWNER | VARCHAR | Name of the role that owns the contact. |
| COMMENT | VARCHAR | Comments for the contact, if any. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the contact was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the contact was dropped or the date and time when its parent was dropped. |
| CONTACT\_URL | VARCHAR | URL used to communicate with the contact. |
| CONTACT\_EMAIL\_DISTRIBUTION\_LIST | VARCHAR | Email address used to communicate with the contact. |
| CONTACT\_USERS | ARRAY | Array of Snowflake users to contact. |
| CONTACT\_EMAIL\_LIST | ARRAY | Array of email addresses associated with the contact. |
| CONTACT\_TYPE | VARCHAR | Type of the contact. |
| CONTACT\_VALUE | VARCHAR | Value associated with the contact. |
| CONTACT\_METADATA | VARIANT | Additional metadata for the contact, if any. |
| CONTACT\_OWNER\_ROLE\_TYPE | VARCHAR | Type of role that owns the object. Either ROLE, DATABASE\_ROLE, or APPLICATION (if a Snowflake Native App owns the object). Deleted contacts have a NULL value. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 240 minutes (4 hours).
