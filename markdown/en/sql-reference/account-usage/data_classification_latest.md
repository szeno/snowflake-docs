Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DATA\_CLASSIFICATION\_LATEST view

This Account Usage view displays one row for the most recent result of a classified table for each classified table. Each row corresponds
to a different table.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| TABLE\_ID | Number | Internal/system-generated identifier for the table that was classified. |
| TABLE\_NAME | VARCHAR | Name of the table. |
| SCHEMA\_ID | Number | Internal/system-generated identifier for the schema that contains the table. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table. |
| DATABASE\_ID | Number | Internal/system-generated identifier for the database that contains the table. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table. |
| RESULT | VARIANT | Latest classification result. For a description of the JSON object, see the output of the [SYSTEM$GET\_CLASSIFICATION\_RESULT](/sql-reference/functions/system_get_classification_result) function. |
| STATUS | VARCHAR | One of the following: `CLASSIFIED` or `REVIEWED`. |
| TRIGGER\_TYPE | VARCHAR | Mode of the classification trigger: `MANUAL` or `AUTO CLASSIFICATION`, where `MANUAL` indicates that someone called a system function to initiate the classification process. |
| LAST\_CLASSIFIED\_ON | TIMESTAMP\_LTZ | Time when the table was last successfully classified. |
| LAST\_CLASSIFICATION\_ATTEMPT | TIMESTAMP\_LTZ | Timestamp of the last sensitive data classification attempt. If the value is greater than `LAST_CLASSIFIED_ON`, it indicates that the last sensitive data classification attempt resulted in a failure. |
| ERROR\_MESSAGE | VARCHAR | Error message from the last sensitive data classification attempt, if it resulted in a failure. |

Expand

Show lessSee more

## Usage notes

- Latency for this view might be up to three hours.
- This view retains data for as long as the table exists.
- A row in the view is removed when the following occur:
  - A table is dropped or renamed.
  - The table is reclassified.
