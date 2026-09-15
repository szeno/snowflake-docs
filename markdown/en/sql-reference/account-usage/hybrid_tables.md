Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# HYBRID\_TABLES view

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

This Account Usage view displays a row for each hybrid table defined in the specified (or current) database.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ID | NUMBER | ID of the hybrid table. |
| NAME | TEXT | Name of the hybrid table. |
| SCHEMA\_ID | NUMBER | ID of the schema to which the hybrid table belongs. |
| SCHEMA\_NAME | TEXT | Schema to which the hybrid table belongs. |
| DATABASE\_ID | NUMBER | ID of the database to which the hybrid table belongs. |
| DATABASE\_NAME | TEXT | Database to which the hybrid table belongs. |
| OWNER | TEXT | Owner of the hybrid table. |
| ROW\_COUNT | NUMBER | Approximate row count of the hybrid table. |
| BYTES | NUMBER | Approximate size in bytes of the row store of the hybrid table. |
| RETENTION\_TIME | NUMBER | Retention time for data in the hybrid table. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the hybrid table. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Last time this hybrid table was altered by a DDL statement, a TRUNCATE or INSERT OVERWRITE statement, or a compaction job. Note that regular DML operations are not recorded here. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the hybrid table was dropped. |
| COMMENT | TEXT | Comment for the hybrid table. |
| OWNER\_ROLE\_TYPE | TEXT | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

Latency for the view may be up to 180 minutes (3 hours).
