Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# PROCEDURES view

This Account Usage view displays a row for each stored procedure defined in the account.

For more information about stored procedures, see [Stored procedures overview](/developer-guide/stored-procedure/stored-procedures-overview).

## Columns

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
