Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# STORAGE\_LIFECYCLE\_POLICIES view

This Account Usage view displays [storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies).
Each row in this view corresponds to a different storage lifecycle policy.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| NAME | TEXT | Name of the storage lifecycle policy. |
| ID | NUMBER | Internal/system-generated identifier for the storage lifecycle policy. |
| SCHEMA\_ID | TEXT | Internal/system-generated identifier for the schema in which the policy resides. |
| SCHEMA | TEXT | Schema to which the storage lifecycle policy belongs. |
| DATABASE\_ID | TEXT | Internal/system-generated identifier for the database in which the policy resides. |
| DATABASE | TEXT | Database to which the storage lifecycle policy belongs. |
| OWNER | TEXT | Name of the role that owns the storage lifecycle policy. |
| SIGNATURE | TEXT | Type signature of the storage lifecycle policy’s arguments. |
| RETURN\_TYPE | TEXT | Return value data type. |
| BODY | TEXT | Storage lifecycle policy definition. |
| COMMENT | TEXT | Comments entered for the storage lifecycle policy. |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time when the storage lifecycle policy was created. |
| LAST\_ALTERED\_ON | TIMESTAMP\_LTZ | Date and time when the storage lifecycle policy was last altered. |
| DELETED\_ON | TIMESTAMP\_LTZ | Date and time when the storage lifecycle policy was dropped. |
| OPTIONS | OBJECT | Storage lifecycle policy options, including ARCHIVE\_FOR\_DAYS (number of days to keep data in current tier) and ARCHIVE\_TIER (target storage tier). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).
