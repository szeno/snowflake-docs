Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# ARCHIVE\_STORAGE\_DATA\_RETRIEVAL\_USAGE\_HISTORY view

This Account Usage view displays a history of archived data retrieval (in bytes) for your
account over the past 12 months (one year).

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the usage took place. |
| OBJECT\_TYPE | VARCHAR | The type of the retrieved object; for example, `TABLE`. |
| OBJECT\_ID | NUMBER | Internal or system-generated identifier for the retrieved object. |
| OBJECT\_NAME | VARCHAR | Name of the retrieved object. |
| SCHEMA\_ID | NUMBER | Internal, Snowflake-generated identifier of the schema for the retrieved object. |
| SCHEMA\_NAME | VARCHAR | Name of the schema for the retrieved object. |
| DATABASE\_ID | NUMBER | Internal, Snowflake-generated identifier of the database for the retrieved object. |
| DATABASE\_NAME | VARCHAR | Name of the database for the retrieved object. |
| BYTES | NUMBER | Bytes retrieved from archive storage. |
| ARCHIVE\_STORAGE\_TIER | VARCHAR | The archive storage tier from which Snowflake retrieved the object; for example, `COOL` or `COLD`. |

Expand

Show lessSee more

## Usage notes

- Latency for the view is up to 1 hour.
- The view contains historical data for the past 12 months (one year).
- For cost information related to data retrieval from archive storage,
  see [billing for storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies-billing).
