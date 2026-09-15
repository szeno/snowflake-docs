# INDEXES view

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

This Information Schema view displays a row for each index defined in the specified (or current) database.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| TABLE\_CATALOG | TEXT | Database to which the hybrid table belongs. |
| TABLE\_SCHEMA | TEXT | Schema to which the hybrid table belongs. |
| TABLE\_NAME | TEXT | Name of the hybrid table where the index is defined. |
| NAME | TEXT | Name of the index on the hybrid table. |
| OWNER | TEXT | Owner of the index. |
| IS\_UNIQUE | TEXT | With `YES` or `NO`, indicates whether this index is a unique index. |
| CONSTRAINT\_NAME | TEXT | Name of the constraint that is associated with this index. |
| STATUS | TEXT | Status of this index. |
| CREATED | TIMESTAMP\_LTZ | Time of creation for this index. |

Expand

Show lessSee more
