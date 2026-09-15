Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# AUTOMATIC\_CLUSTERING\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The AUTOMATIC\_CLUSTERING\_HISTORY view in the ORGANIZATION\_USAGE schema
is used for querying the [Automatic Clustering](/user-guide/tables-auto-reclustering) history for
your organization’s tables within a specified date range. The information
returned by the view includes the credits consumed, bytes reclustered, and rows
reclustered each time a table is reclustered. Use the VERSION column to distinguish
Optima Clustering (`OPTIMA`) from Clustering Classic (`CLASSIC`).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization in which the usage took place. |
| ACCOUNT\_NAME | VARCHAR | Name of the account where the usage took place. |
| ACCOUNT\_LOCATOR | VARCHAR | Name of the account locator. |
| REGION | VARCHAR | Name of the region where the account is located. |
| USAGE\_DATE | DATE | Date when automatic clustering usage occurred. |
| CREDITS\_USED | NUMBER | Number of credits billed for automatic clustering during the day specified by the USAGE\_DATE value. |
| NUM\_BYTES\_RECLUSTERED | NUMBER | Number of bytes reclustered during the day specified by the USAGE\_DATE value. |
| NUM\_ROWS\_RECLUSTERED | NUMBER | Number of rows reclustered during the day specified by the USAGE\_DATE value. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table. |
| TABLE\_NAME | VARCHAR | Name of the table. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table. |
| VERSION | VARCHAR | Version of Automatic Clustering that produced the credits: `CLASSIC` for Clustering Classic, or `OPTIMA` for Optima Clustering. For more information, see [Optima Clustering](/user-guide/tables-auto-reclustering#label-optima-clustering). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours (1 day).
- The data is retained for 365 days (1 year).
- A row might be clustered multiple times, depending on data skew, clustering key distribution, and reordering required for micro-partitions. A large table with poor initial clustering might need multiple passes to reach an optimally clustered state. Therefore, the NUM\_ROWS\_RECLUSTERED value for a table could be as high as the total number of rows in the table or even higher.
