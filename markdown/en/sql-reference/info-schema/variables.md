# VARIABLES view

This Information Schema view displays a row for each [schema variable](/sql-reference/schema-variables)
defined in the specified (or current) database.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| VARIABLE\_CATALOG | VARCHAR | Database that the variable belongs to |
| VARIABLE\_SCHEMA | VARCHAR | Schema that the variable belongs to |
| VARIABLE\_NAME | VARCHAR | Name of the variable |
| VARIABLE\_OWNER | VARCHAR | Name of the role that owns the variable |
| DATA\_TYPE | VARCHAR | Declared data type of the variable |
| VALUE | VARCHAR | Current value of the variable, or NULL if no value has been set |
| DEFAULT\_VALUE | VARCHAR | Default value of the variable, or NULL if no default was declared |
| VERSION | NUMBER | Monotonically increasing version number; incremented each time the variable is set |
| CREATED | TIMESTAMP\_LTZ | Creation time of the variable |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the variable was last altered. See [Usage Notes](#usage-notes). |
| COMMENT | VARCHAR | Comment for the variable |

Expand

Show lessSee more

## Usage notes

- The view only displays variables for which the current role has been granted `OWNERSHIP`,
  `READ`, or `WRITE` privilege. The view does not honor the MANAGE GRANTS privilege and
  may show less information than `SHOW SCHEMA VARIABLES IN SCHEMA` when executed by a user
  who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
