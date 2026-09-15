Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# AUTOMATIC\_CLUSTERING\_HISTORY view

This Account Usage view can be used to query the [Automatic Clustering](/user-guide/tables-auto-reclustering) history. The information returned by the view includes the credits consumed, bytes updated, and rows updated each time a table is reclustered. Use the VERSION column to distinguish Optima Clustering (`OPTIMA`) from Clustering Classic (`CLASSIC`).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| CREDITS\_USED | NUMBER | Number of credits billed for automatic clustering during the START\_TIME and END\_TIME window. |
| NUM\_BYTES\_RECLUSTERED | NUMBER | Number of bytes reclustered during the START\_TIME and END\_TIME window. |
| NUM\_ROWS\_RECLUSTERED | NUMBER | Number of rows reclustered during the START\_TIME and END\_TIME window. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table. |
| TABLE\_NAME | VARCHAR | Name of the table. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table. |
| INSTANCE\_ID | NUMBER | Internal/system-generated identifier for the instance that the object belongs to. |
| VERSION | VARCHAR | Version of Automatic Clustering that produced the credits: `CLASSIC` for Clustering Classic, or `OPTIMA` for Optima Clustering. For more information, see [Optima Clustering](/user-guide/tables-auto-reclustering#label-optima-clustering). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- If you want to reconcile the data in this view with a corresponding view in the [ORGANIZATION USAGE schema](/sql-reference/organization-usage), you must first set the timezone of the session to UTC. Before querying the Account Usage view, execute:

  > Copy code
  >
  > ```
  > ALTER SESSION SET TIMEZONE = UTC;
  > ```
- A row might be clustered multiple times, depending on data skew, clustering key distribution, and reordering required for micro-partitions. A large table with poor initial clustering might need multiple passes to reach an optimally clustered state. Therefore, the NUM\_ROWS\_RECLUSTERED value for a table could be as high as the total number of rows in the table or even higher.
