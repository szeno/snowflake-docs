# TABLES view

This Information Schema view displays a row for each table and view in the specified (or current) database, including the views in the INFORMATION\_SCHEMA schema itself.

See also:
:   [COLUMNS view](/sql-reference/info-schema/columns) , [VIEWS view](/sql-reference/info-schema/views) , [TABLES view](/sql-reference/account-usage/tables) (Account Usage)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| TABLE\_CATALOG | VARCHAR | Database that the table belongs to. |
| TABLE\_SCHEMA | VARCHAR | Schema that the table belongs to. |
| TABLE\_NAME | VARCHAR | Name of the table. |
| TABLE\_OWNER | VARCHAR | Name of the role that owns the table. |
| TABLE\_TYPE | VARCHAR | Indicates the table type. Valid values are `BASE TABLE`, `TEMPORARY TABLE`, `EXTERNAL TABLE`, `EVENT TABLE`, `VIEW`, or `MATERIALIZED VIEW`. |
| IS\_TRANSIENT | VARCHAR | Indicates whether this is a transient table. |
| CLUSTERING\_KEY | VARCHAR | Clustering key for the table. |
| ROW\_COUNT | NUMBER | Number of rows in the table. |
| BYTES | NUMBER | Number of bytes accessed by a scan of the table. |
| RETENTION\_TIME | NUMBER | Number of days that historical data is retained for Time Travel. |
| SELF\_REFERENCING\_COLUMN\_NAME | VARCHAR | Not applicable for Snowflake. |
| REFERENCE\_GENERATION | VARCHAR | Not applicable for Snowflake. |
| USER\_DEFINED\_TYPE\_CATALOG | VARCHAR | Not applicable for Snowflake. |
| USER\_DEFINED\_TYPE\_SCHEMA | VARCHAR | Not applicable for Snowflake. |
| USER\_DEFINED\_TYPE\_NAME | VARCHAR | Not applicable for Snowflake. |
| IS\_INSERTABLE\_INTO | VARCHAR | Not applicable for Snowflake. |
| IS\_TYPED | VARCHAR | Not applicable for Snowflake. |
| COMMIT\_ACTION | VARCHAR | Not applicable for Snowflake. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the table. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| LAST\_DDL | TIMESTAMP\_LTZ | Timestamp of the last DDL operation performed on the table or view.  All supported table/view DDL operations update this field:   - { CREATE | ALTER | DROP | UNDROP } TABLE - { CREATE | ALTER | DROP } VIEW   All ALTER TABLE operations update this field, including setting or unsetting a table parameter (for example, COMMENT, DATA\_RETENTION\_TIME, etc.) and changes to table columns (ADD / MODIFY / RENAME / DROP).  For more information, see the [Usage Notes](#usage-notes). |
| LAST\_DDL\_BY | VARCHAR | The current username for the user who executed the last DDL operation. If the user has been dropped, shows `DROPPED_USER(<id>)`.  For dropped users, you can join the `<id>` with the USER\_ID column in the USERS view of the ACCOUNT\_USAGE or ORGANIZATION\_USAGE schema. |
| AUTO\_CLUSTERING\_ON | BOOLEAN | Indicates whether automatic clustering is enabled for the table. |
| COMMENT | VARCHAR | Comment for this table. |
| IS\_TEMPORARY | VARCHAR | Indicates whether this is a temporary table. Valid values are `YES` and `NO`. |
| IS\_ICEBERG | VARCHAR | Indicates whether the table is an [Iceberg table](/user-guide/tables-iceberg). Valid values are `YES` or `NO`. |
| IS\_DYNAMIC | VARCHAR | Indicates whether the table is a [dynamic table](/user-guide/dynamic-tables/overview). Valid values are `YES` or `NO`. |
| IS\_IMMUTABLE | VARCHAR | Indicates whether the table was created with the [READ ONLY](/sql-reference/sql/create-table#label-create-table-read-only) property. Valid values are `YES` or `NO`. |
| IS\_HYBRID | VARCHAR | Indicates whether the table is a [hybrid table](/user-guide/tables-hybrid). Valid values are `YES` or `NO`. |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges. The view does not honor the
  MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command when both are executed with a role that was
  granted the MANAGE GRANTS privilege.

  This behavior also applies to other account-level [privileges](/user-guide/security-access-control-privileges) and Information
  Schema views for which there is a corresponding SHOW command.
- Querying the sum(bytes) for a table does not represent the total storage usage, because the amount does not include Time Travel and Fail-safe usage.
- The view does not include tables that have been dropped. To view dropped tables, use [SHOW TABLES](/sql-reference/sql/show-tables) instead.
- To view only tables in your queries, filter using a WHERE clause, e.g.:
  `... WHERE table_schema != 'INFORMATION_SCHEMA'`
- Using the value in the LAST\_ALTERED column for Time Travel is \_not\_ recommended and can return unexpected results for the following
  reaons:

  - Time Travel can only be used to query historical data modified by a [DML operation](/user-guide/data-time-travel#label-time-travel-querying).
  - The LAST\_ALTERED column inludes both DML and DDL operations (see the next usage note).
  - For DML operations, the value in the LAST\_ALTERED column is the timestamp at the beginning of the statement execution rather than
    the time of the commit of the transaction containing this statement.
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
- The LAST\_ALTERED column does not necessarily indicate the last refreshed time for external tables.
  To retrieve the last refreshed time for an auto-refreshed external table, you can use the
  [SYSTEM$EXTERNAL\_TABLE\_PIPE\_STATUS](/sql-reference/functions/system_external_table_pipe_status) function, which returns
  information such as the timestamp of the last file Snowflake has registered.

## Examples

Retrieve the size (in bytes) of all tables in all schemas in the `mydatabase` database:

Copy code

```
SELECT table_schema, SUM(bytes)
  FROM mydatabase.INFORMATION_SCHEMA.TABLES
  GROUP BY TABLE_SCHEMA;
```
