# VIEWS view

This Information Schema view displays a row for each view in the specified (or current) database, including the INFORMATION\_SCHEMA views for the database.

See also:
:   [TABLES view](/sql-reference/info-schema/tables)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| TABLE\_CATALOG | VARCHAR | Database that the view belongs to. |
| TABLE\_SCHEMA | VARCHAR | Schema that the view belongs to. |
| TABLE\_NAME | VARCHAR | Name of the view. |
| TABLE\_OWNER | VARCHAR | Name of the role that owns the view. |
| VIEW\_DEFINITION | VARCHAR | Text of the view’s query expression. |
| CHECK\_OPTION | VARCHAR | Not applicable for Snowflake. |
| IS\_UPDATABLE | VARCHAR | Not applicable for Snowflake. |
| INSERTABLE\_INTO | VARCHAR | Not applicable for Snowflake. |
| IS\_SECURE | VARCHAR | Specifies whether the view is secure. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the view. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| LAST\_DDL | TIMESTAMP\_LTZ | Timestamp of the last DDL operation performed on the table or view.  All supported table/view DDL operations update this field:   - { CREATE | ALTER | DROP | UNDROP } TABLE - { CREATE | ALTER | DROP } VIEW   All ALTER TABLE operations update this field, including setting or unsetting a table parameter (for example, COMMENT, DATA\_RETENTION\_TIME, etc.) and changes to table columns (ADD / MODIFY / RENAME / DROP).  For more information, see the [Usage Notes](#usage-notes). |
| LAST\_DDL\_BY | VARCHAR | The current username for the user who executed the last DDL operation. If the user has been dropped, shows `DROPPED_USER(<id>)`.  For dropped users, you can join the `<id>` with the USER\_ID column in the USERS view of the ACCOUNT\_USAGE or ORGANIZATION\_USAGE schema. |
| COMMENT | VARCHAR | Comment for this view. |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges. The view does not honor the
  MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command when both are executed with a role that was
  granted the MANAGE GRANTS privilege.

  This behavior also applies to other account-level [privileges](/user-guide/security-access-control-privileges) and Information
  Schema views for which there is a corresponding SHOW command.
- To remove the INFORMATION\_SCHEMA views from your queries, filter using a WHERE clause, e.g.:
  `... WHERE table_schema != 'INFORMATION_SCHEMA'`
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

  For views and tables, use the LAST\_DDL column for the last modification time for an object.
- The value in the LAST\_DDL column is updated as follows:

  > - When a table or view is created, the LAST\_DDL timestamp is the same as the CREATED timestamp.
  > - When a table or view is dropped, the LAST\_DDL timestamp is the same as the DELETED timestamp.
  > - Last DDL data is not available for operations that occurred before the columns were
  >   [added](/release-notes/bcr-bundles/2023_01/bcr-891). The new DDL fields contain `null` until a DDL operation is executed.
  > - For replicated databases, the LAST\_DDL and LAST\_DDL\_BY fields are only updated for objects in the primary database. After failover, the
  >   LAST\_DDL and LAST\_DDL\_BY fields are updated for DDL operations for the tables and views in the newly promoted primary database. These
  >   fields will remain unchanged for objects in the now secondary database.
  > - For objects in secondary databases that are newly created during a refresh operation, these fields are `null`.
