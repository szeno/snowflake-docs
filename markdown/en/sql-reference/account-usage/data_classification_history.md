Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DATA\_CLASSIFICATION\_HISTORY view

This Account Usage view displays all historical sensitive data classification results for each table in the account. Unlike
[DATA\_CLASSIFICATION\_LATEST view](/sql-reference/account-usage/data_classification_latest), which shows only the most recent classification per table,
this view shows all classification events over time, limited to the last 365 days.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table that was classified. |
| TABLE\_NAME | VARCHAR | Name of the table. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table. |
| RESULT | VARIANT | Classification result at the time of classification. For a description of the JSON object, see the output of the [SYSTEM$GET\_CLASSIFICATION\_RESULT](/sql-reference/functions/system_get_classification_result) function. |
| TRIGGER\_TYPE | VARCHAR | Mode of the classification trigger: `MANUAL` or `AUTO CLASSIFICATION`, where `MANUAL` indicates that someone called a system function to initiate the classification process. |
| CLASSIFIED\_ON | TIMESTAMP\_LTZ | Time when the classification was performed. |
| TABLE\_DELETED\_ON | TIMESTAMP\_LTZ | Date and time when the object or parent object was dropped. NULL if the object has not been deleted. |

Expand

Show lessSee more

## Usage notes

- Latency for this view might be up to three hours.
- Data is retained for 365 days (one year). Rows are removed only when a classification event is older than one year.
- Unlike [DATA\_CLASSIFICATION\_LATEST view](/sql-reference/account-usage/data_classification_latest), this view retains data for classification events
  even when the associated table, schema, or database is dropped. The `TABLE_NAME`, `SCHEMA_NAME`, and `DATABASE_NAME`
  columns reflect the table and its database/schema location recorded for that classification result, but do not preserve historical
  object names across subsequent rename operations. If a table is later moved to a different schema and reclassified, a new row
  reflects the new location. The `TABLE_DELETED_ON` column is non-null if the table has been dropped.

For more information on how to query this view, see [Query the classification history](/user-guide/classify-results#label-classify-view-history-sql).
