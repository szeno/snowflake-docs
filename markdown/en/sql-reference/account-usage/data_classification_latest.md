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
| ERROR\_MESSAGE | VARCHAR | Error message from the last sensitive data classification attempt, if it resulted in a failure. For the set of possible values, see [Error messages](#label-data-classification-latest-error-messages). |

Expand

Show lessSee more

## Error messages

The `ERROR_MESSAGE` column contains one of the following values:

| Message | Cause |
| --- | --- |
| `Failed to classify the view due to a SQL compilation error` | The view definition no longer compiles. For example, a column was renamed or dropped, a function is missing, or the column count doesn’t match. |
| `Failed to classify due to data format issues` | A value failed to cast during the scan. For example, an invalid timestamp, a number out of range, or an invalid variant or date value. |
| `Failed to classify the secure object` | The underlying error was redacted at a secure view or secure UDF boundary. |
| `Failed to classify the external table as it was marked invalid` | The external table is in the INVALID state. |
| `Failed to classify 'Iceberg External Table' as it has been deprecated` | This table type is deprecated. Migrate to [Apache Iceberg™ tables](/user-guide/tables-iceberg). |
| `Failed to classify as the data in the table was inaccessible` | Snowflake couldn’t read the data because of a storage or credential failure. For example, a stage blocked by an integration, a missing integration, or an unreadable Iceberg file. |
| `Failed to classify as one or more column(s) are mapped to multiple masking policies` | A tag-based masking policy mapping conflicts on a column. |
| `Failed to classify due to timeout while reading the data` | The scan exceeded its time budget. |
| `Failed to classify` | The failure doesn’t match a specific error category in this view. Use the appended error code to identify the failure. |

Expand

Show lessSee more

For the steps to resolve each error, see [Classification error messages](/user-guide/classify-troubleshooting#label-classify-troubleshooting-classification-error-messages) in
[Troubleshooting sensitive data classification](/user-guide/classify-troubleshooting).

Each message has the originating Snowflake error code appended in parentheses, using the format `<message> (<error_code>).`. For
example:

```
Failed to classify due to timeout while reading the data (000630).
```

The code is a standard Snowflake error code. When the code isn’t available, the value is just `<message>.` instead.

A `Failed to classify` message means that the failure doesn’t match a specific error category in this view. When present, the
parenthesized error code provides more information about the failure.

## Usage notes

- Latency for this view might be up to three hours.
- This view retains data for as long as the table exists.
- A row in the view is removed when the following occur:
  - A table is dropped or renamed.
  - The table is reclassified.
- The `ERROR_MESSAGE` value can differ from the `CLASSIFICATION_ERROR` event that Snowflake logs to the event table for the same
  table. The event table can provide a more specific error message. For details, see [Troubleshooting sensitive data classification](/user-guide/classify-troubleshooting).
