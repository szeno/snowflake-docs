# HYBRID\_TABLES view

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

This Information Schema view displays a row for each hybrid table defined in the specified (or current) database.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| CATALOG | TEXT | Database to which the hybrid table belongs. |
| SCHEMA | TEXT | Schema to which the hybrid table belongs. |
| NAME | TEXT | Name of the hybrid table. |
| OWNER | TEXT | Owner of the hybrid table. |
| ROW\_COUNT | NUMBER | Approximate row count of the hybrid table. |
| BYTES | NUMBER | Approximate size in bytes of the row store of the hybrid table. |
| RETENTION\_TIME | NUMBER | Retention time for data in the hybrid table. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the hybrid table. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | The last time this hybrid table was altered by a DDL statement, a TRUNCATE or INSERT OVERWRITE statement, or a compaction job. Note that regular DML operations are not recorded here. |
| COMMENT | TEXT | Comment for the hybrid table. |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges. The view does not honor the MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command when both are executed with a role that was granted the MANAGE GRANTS privilege.
- Just as with SHOW TABLES and SHOW HYBRID TABLES, the bytes and row count are approximate.
