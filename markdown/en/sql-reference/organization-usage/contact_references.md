[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# CONTACT\_REFERENCES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to identify the associations between [contacts](/user-guide/contacts-using) and the objects to
which they have been added.

Contact lineage is not included in this view. For example, if a contact is associated with a schema, the view does not have records for
associations between the contact and all the tables in the schema even though the tables inherit the association from the schema.

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

| Column name | Data type | Description |
| --- | --- | --- |
| CONTACT\_DATABASE | VARCHAR | Name of the database in which the contact exists. |
| CONTACT\_SCHEMA | VARCHAR | Name of schema in which the contact exists. |
| CONTACT\_ID | NUMBER | Internal/system-generated identifier for the contact. |
| CONTACT\_NAME | VARCHAR | Name of a contact. |
| CONTACT\_PURPOSE | VARCHAR | Purpose that was specified when the contact was associated with the object. |
| OBJECT\_DATABASE | VARCHAR | Name of the database that contains the referenced object. If the object is not a database or schema object, the value is empty. |
| OBJECT\_SCHEMA | VARCHAR | Name of the schema that contains the referenced object. If the referenced object is not a schema object (for example, a warehouse), the value is empty. |
| OBJECT\_ID | NUMBER | Internal/system-generated identifier of the referenced object. |
| OBJECT\_NAME | VARCHAR | Name of the referenced object. |
| OBJECT\_DELETED | TIMESTAMP\_LTZ | Date and time when the referenced object was dropped or when its parent object was dropped. |
| OBJECT\_DOMAIN | VARCHAR | Type of the referenced object. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 240 minutes (4 hours).
