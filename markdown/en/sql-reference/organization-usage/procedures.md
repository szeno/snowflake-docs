Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# PROCEDURES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each stored procedure defined in each account.

For more information about stored procedures, see [Stored procedures overview](/developer-guide/stored-procedure/stored-procedures-overview).

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
| PROCEDURE\_CATALOG | VARCHAR | Database to which the stored procedure belongs. |
| PROCEDURE\_SCHEMA | VARCHAR | Schema to which the stored procedure belongs. |
| PROCEDURE\_NAME | VARCHAR | Name of the stored procedure. |
| PROCEDURE\_OWNER | VARCHAR | Name of the role that owns the stored procedure. |
| ARGUMENT\_SIGNATURE | VARCHAR | Type signature of the stored procedure’s arguments. |
| DATA\_TYPE | VARCHAR | Return value data type. |
| CHARACTER\_MAXIMUM\_LENGTH | NUMBER | Maximum length in characters of string return value. |
| CHARACTER\_OCTET\_LENGTH | NUMBER | Maximum length in bytes of string return value. |
| NUMERIC\_PRECISION | NUMBER | Numeric precision of numeric return value. |
| NUMERIC\_PRECISION\_RADIX | NUMBER | Radix of precision of numeric return value. |
| NUMERIC\_SCALE | NUMBER | Scale of numeric return value. |
| PROCEDURE\_LANGUAGE | VARCHAR | Language of the stored procedure. |
| PROCEDURE\_DEFINITION | VARCHAR | Stored procedure definition. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the stored procedure. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| COMMENT | VARCHAR | Comment for this stored procedure. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the procedure was dropped. |
| RUNTIME\_VERSION | VARCHAR | Runtime version of the language used by the procedure. |
| PACKAGES | VARCHAR | Packages requested by the procedure. |
| INSTALLED\_PACKAGES | VARCHAR | All packages installed by the function. Output for Python procedures only. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| PROCEDURE\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier of the schema to which the stored procedure belongs. |
| PROCEDURE\_CATALOG\_ID | NUMBER | Internal/system-generated identifier of the database to which the stored procedure belongs. |
| SECRETS | JSON map | Map of [secrets](/sql-reference/sql/create-secret) specified by the function’s SECRETS parameter, where map keys are secret variable names and map values are secret object names. |
| EXTERNAL\_ACCESS\_INTEGRATIONS | VARCHAR | Names of [external access integrations](/developer-guide/external-network-access/external-network-access-overview) specified by the function’s EXTERNAL\_ACCESS\_INTEGRATION parameter. |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view does not honor the MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command when both are
  executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
