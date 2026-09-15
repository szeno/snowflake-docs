Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# CLASSES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each [class](/sql-reference/snowflake-db-classes)
in the account.

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
| ID | NUMBER | Internal/system-generated identifier for the class. |
| NAME | VARCHAR | Name of the class. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the class. |
| SCHEMA\_NAME | VARCHAR | Name of the schema the class belongs to. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database of the class. |
| DATABASE\_NAME | VARCHAR | Name of the database the class belongs to. |
| OWNER\_NAME | VARCHAR | Name of the role that owns the class. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the class was created. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the class was deleted. |
| COMMENT | VARCHAR | Comment for the class. |

Expand

Show lessSee more

## Usage notes

Latency for the view may be up to 180 minutes (3 hours).

## Examples

The following example finds all classes in the account:

Copy code

```
SELECT account_name, name, database_name, schema_name
  FROM snowflake.organization_usage.classes;
```
