Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# INDEXES view

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

This Account Usage view displays a row for each index defined in the specified (or current) database.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ID | NUMBER | ID of the index. |
| NAME | TEXT | Name of the index. |
| TABLE\_ID | NUMBER | ID of the hybrid table. |
| TABLE\_NAME | TEXT | Name of the hybrid table. |
| SCHEMA\_ID | TEXT | ID of the schema to which the hybrid table belongs. |
| SCHEMA\_NAME | TEXT | Schema to which the hybrid table belongs. |
| DATABASE\_ID | NUMBER | ID of the database to which the hybrid table belongs. |
| DATABASE\_NAME | TEXT | Database to which the hybrid table belongs. |
| OWNER | TEXT | Owner of the hybrid table. |
| IS\_UNIQUE | TEXT | With `YES` or `NO`, indicates whether this index is a unique index. |
| CONSTRAINT\_NAME | TEXT | Name of the constraint that is associated with this index. |
| STATUS | TEXT | Latest status of this index. |
| CREATED | TIMESTAMP\_LTZ | Time of creation for this index. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the hybrid table was dropped. |
| OWNER\_ROLE\_TYPE | TEXT | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

Latency for the view may be up to 180 minutes (3 hours).
