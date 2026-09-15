Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# STAGES view

This Account Usage view displays a row for each stage defined in the account.

Stages are named objects that can be used for loading/unloading data. For more information, see [CREATE STAGE](/sql-reference/sql/create-stage).

## Columns

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

- Latency for the view may be up to 120 minutes (2 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view does not recognize the MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command
  executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
