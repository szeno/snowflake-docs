# SCHEMATA view

This Information Schema view displays a row for each schema in the specified (or current) database, including the INFORMATION\_SCHEMA schema itself.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| CATALOG\_NAME | VARCHAR | Database that the schema belongs to |
| SCHEMA\_NAME | VARCHAR | Name of the schema |
| SCHEMA\_OWNER | VARCHAR | Name of the role that owns the schema |
| IS\_TRANSIENT | VARCHAR | Whether this is a transient schema |
| IS\_MANAGED\_ACCESS | VARCHAR | Whether the schema is a managed access schema |
| RETENTION\_TIME | NUMBER | Number of days that historical data is retained for Time Travel |
| DEFAULT\_CHARACTER\_SET\_CATALOG | VARCHAR | Not applicable for Snowflake. |
| DEFAULT\_CHARACTER\_SET\_SCHEMA | VARCHAR | Not applicable for Snowflake. |
| DEFAULT\_CHARACTER\_SET\_NAME | VARCHAR | Not applicable for Snowflake. |
| SQL\_PATH | VARCHAR | Not applicable for Snowflake. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the schema |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| COMMENT | VARCHAR | Comment for this schema |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
