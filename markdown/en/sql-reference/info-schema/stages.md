# STAGES view

This Information Schema view displays a row for each stage defined in the specified (or current) database.

Stages are named objects that can be used for loading/unloading data. For more information, see [CREATE STAGE](/sql-reference/sql/create-stage).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| STAGE\_CATALOG | VARCHAR | Database that the stage belongs to. |
| STAGE\_SCHEMA | VARCHAR | Schema that the stage belongs to. |
| STAGE\_NAME | VARCHAR | Name of the stage. |
| STAGE\_URL | VARCHAR | Location of an external stage. |
| STAGE\_REGION | VARCHAR | Region where the stage resides. |
| STAGE\_TYPE | VARCHAR | Type of stage (`Internal Named`, or `External Named`). |
| STAGE\_OWNER | VARCHAR | Name of the role that owns the stage. |
| COMMENT | VARCHAR | Comment for this stage. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the stage. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges. The view does not honor the MANAGE GRANTS privilege and consequently may show less
  information compared to a SHOW command when both are executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
