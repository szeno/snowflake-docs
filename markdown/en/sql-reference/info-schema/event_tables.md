# EVENT\_TABLES view

This Information Schema view displays a row for each event table and view in the specified (or current) database, including the views in
the INFORMATION\_SCHEMA schema itself.

See also:
:   [Event table overview](/developer-guide/logging-tracing/event-table-setting-up), [VIEWS view](/sql-reference/info-schema/views)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| TABLE\_CATALOG | VARCHAR | Database that the event table belongs to |
| TABLE\_SCHEMA | VARCHAR | Schema that the event table belongs to |
| TABLE\_NAME | VARCHAR | Name of the event table |
| TABLE\_OWNER | VARCHAR | Name of the role that owns the event table |
| CREATED | TIMESTAMP\_LTZ | Creation time of the event table |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| COMMENT | VARCHAR | Comment for this event table |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges. The view does not honor the
  MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command when both are executed with a role that was
  granted the MANAGE GRANTS privilege.

  This behavior also applies to other account-level [privileges](/user-guide/security-access-control-privileges) and Information
  Schema views for which there is a corresponding SHOW command.
- The view does not include event tables that have been dropped. To view dropped tables, use [SHOW EVENT TABLES](/sql-reference/sql/show-event-tables) instead.
- To view only event tables in your queries, filter using a WHERE clause, e.g.:
  `... WHERE table_schema != 'INFORMATION_SCHEMA'`
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve the names of all event tables in all schemas in the `mydatabase` database:

Copy code

```
SELECT TABLE_NAME
    FROM mydatabase.information_schema.event_tables;
```
