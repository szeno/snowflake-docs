Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SCHEMATA view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each schema in an account except the READER\_ACCOUNT\_USAGE, and
INFORMATION\_SCHEMA schemas.

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
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema. |
| SCHEMA\_NAME | VARCHAR | Name of the schema. |
| CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the schema. |
| CATALOG\_NAME | VARCHAR | Database that the schema belongs to. |
| SCHEMA\_OWNER | VARCHAR | Name of the role that owns the schema. |
| RETENTION\_TIME | NUMBER | Number of days that historical data is retained for Time Travel. |
| IS\_TRANSIENT | VARCHAR | Whether the schema is transient. |
| IS\_MANAGED\_ACCESS | VARCHAR | Whether the schema is a managed access schema. |
| DEFAULT\_CHARACTER\_SET\_CATALOG | VARCHAR | Not applicable for Snowflake. |
| DEFAULT\_CHARACTER\_SET\_SCHEMA | VARCHAR | Not applicable for Snowflake. |
| DEFAULT\_CHARACTER\_SET\_NAME | VARCHAR | Not applicable for Snowflake. |
| SQL\_PATH | VARCHAR | Not applicable for Snowflake. |
| COMMENT | VARCHAR | Comment for the schema. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the schema was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| DELETED | TIMESTAMP\_LTZ | Date and time when the schema was dropped. |
| SCHEMA\_TYPE | VARCHAR | Specifies the schema type. Valid values are:     - STANDARD: normal schema.   - VERSIONED: versioned schema. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| SCHEMA\_TYPE | VARCHAR | Type of schema. Possible values are `STANDARD` and `VERSIONED`. |
| VERSION\_NAME | VARCHAR | Name of the schema if it is a versioned schema. NULL otherwise. |
| VERSIONED\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier if the schema is a versioned schema. NULL, otherwise. |
| OBJECT\_VISIBILITY | OBJECT | `OBJECT_VISIBILITY`  [Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open  Available to all accounts.  This property controls the [discoverability of the objects](/user-guide/ui-snowsight/object-visibility-universal-search) in the account, enabling users without explicit access privileges to find objects and request access. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
