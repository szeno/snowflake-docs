# INDEX\_COLUMNS view

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

This Information Schema view displays a row for each column in the indexes defined in the specified (or current) database.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| TABLE\_CATALOG | TEXT | Database to which the hybrid table belongs. |
| TABLE\_SCHEMA | TEXT | Schema to which the hybrid table belongs. |
| TABLE\_NAME | TEXT | Name of the hybrid table where the index is defined. |
| INDEX\_NAME | TEXT | Name of the index on the hybrid table. |
| NAME | TEXT | Name of the column that is participating in the index. |
| KEY\_SEQUENCE | NUMBER | Position of the column in the index, starting from 1. |
| INDEX\_OWNER | TEXT | Owner of the index. |
| IS\_UNIQUE | TEXT | With `YES` or `NO`, indicates whether this index is a unique index. |
| CONSTRAINT\_NAME | TEXT | Name of the constraint that is associated with this index. |
| STATUS | TEXT | Status of this index. |
| CREATED | TIMESTAMP\_LTZ | Time of creation for this index. |
| IS\_INCLUDED\_COLUMN | TEXT | With `YES` or `NO`, indicates whether this column is covered by an index. |

Expand

Show lessSee more
