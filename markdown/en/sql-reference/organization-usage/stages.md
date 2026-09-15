Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# STAGES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each stage defined in an account.

Stages are named objects that can be used for loading/unloading data. For more information, see [CREATE STAGE](/sql-reference/sql/create-stage).

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
| STAGE\_ID | NUMBER | Internal/system-generated identifier for the stage. |
| STAGE\_NAME | VARCHAR | Name of the stage. |
| STAGE\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the stage. |
| STAGE\_SCHEMA | VARCHAR | Schema that the stage belongs to. |
| STAGE\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the stage. |
| STAGE\_CATALOG | VARCHAR | Database that the stage belongs to. |
| STAGE\_URL | VARCHAR | If the stage is external, location of the stage; NULL if it is internal. |
| STAGE\_REGION | VARCHAR | If the stage is external, region where the stage resides; NULL if it is internal. |
| STAGE\_TYPE | VARCHAR | Type of stage (`Internal Named`, or `External Named`). |
| STAGE\_OWNER | VARCHAR | Name of the role that owns the stage; NULL if it has been dropped. |
| COMMENT | VARCHAR | Comment for the stage. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the stage was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| DELETED | TIMESTAMP\_LTZ | Date and time when the stage was dropped. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| INSTANCE\_ID | NUMBER | Internal/system-generated identifier for the instance which the object belongs to. |
| STORAGE\_INTEGRATION | VARCHAR | The name of the storage integration associated with the stage; NULL for internal stages or stages that do not use a storage integration. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view does not recognize the MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command
  executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
