# PROCEDURES view

This Information Schema view displays a row for each stored procedure defined in the specified (or current) database.

For more information about stored procedures, see [Stored procedures overview](/developer-guide/stored-procedure/stored-procedures-overview).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| PROCEDURE\_CATALOG | VARCHAR | Database that the stored procedure belongs to. |
| PROCEDURE\_SCHEMA | VARCHAR | Schema that the stored procedure belongs to. |
| PROCEDURE\_NAME | VARCHAR | Name of the stored procedure. |
| PROCEDURE\_OWNER | VARCHAR | Name of the role that owns the stored procedure. |
| ARGUMENT\_SIGNATURE | VARCHAR | Type signature of the stored procedure’s arguments. |
| DATA\_TYPE | VARCHAR | Return value data type. |
| CHARACTER\_MAXIMUM\_LENGTH | NUMBER | Maximum length of string return value, in characters. |
| CHARACTER\_OCTET\_LENGTH | NUMBER | Maximum length of string return value, in bytes. |
| NUMERIC\_PRECISION | NUMBER | Numeric precision of numeric return value. |
| NUMERIC\_PRECISION\_RADIX | NUMBER | Radix of precision of numeric return value. |
| NUMERIC\_SCALE | NUMBER | Scale of numeric return value. |
| PROCEDURE\_LANGUAGE | VARCHAR | Programming language of the stored procedure. |
| PROCEDURE\_DEFINITION | VARCHAR | Definition of the stored procedure. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the stored procedure. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| COMMENT | VARCHAR | Comment for this stored procedure. |
| EXTERNAL\_ACCESS\_INTEGRATIONS | VARCHAR | Names of [external access integrations](/developer-guide/external-network-access/external-network-access-overview) specified by the procedure’s EXTERNAL\_ACCESS\_INTEGRATION parameter. |
| SECRETS | JSON map | Map of [secrets](/sql-reference/sql/create-secret) specified by the procedure’s SECRETS parameter, where map keys are secret variable names and map values are secret object names. |
| RUNTIME\_VERSION | VARCHAR | Runtime version of the stored procedure’s handler language; NULL if the handler is written in SQL or JavaScript. |
| PACKAGES | VARCHAR | Names of packages specified in the PACKAGES clause of the [CREATE PROCEDURE](/sql-reference/sql/create-procedure) statement. Currently, this column applies only when the handler is written in Python, Java, or Scala. |
| INSTALLED\_PACKAGES | VARCHAR | Names of all packages installed by the stored procedure. This includes packages specified by the PACKAGES clause as well as their installed dependencies. Currently, this column applies only when the handler is written in Python. |
| ARTIFACT\_REPOSITORY | VARCHAR | Name of the artifact repository used to resolve packages for the stored procedure. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges. The
  view does not honor the MANAGE GRANTS privilege and consequently may show less
  information compared to a SHOW command when both are executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
