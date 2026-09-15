Schema:
:   [MONITORING](/sql-reference/monitoring#label-monitoring-views)

# ICEBERG\_ACCESS\_ERRORS view

This MONITORING schema view displays [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def)
access errors for the account.

Use the information in this view to search for and troubleshoot access errors, which can result from situations like the following:

- Snowflake loses privileges to access the external volume storage location.
- Snowflake tries to access files that have been deleted or overwritten.
- Snowflake encounters other storage access issues.

See also:
:   [Apache Iceberg™ tables](/user-guide/tables-iceberg)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| EXTERNAL\_VOLUME\_ID | NUMBER | The unique ID of the external volume associated with the error. |
| EXTERNAL\_VOLUME\_NAME | VARCHAR | The name of the external volume associated with the error. |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time when the error was raised. |
| EXTERNAL\_VOLUME\_PATH | VARCHAR | Full path to the file on the external volume associated with the error. |
| MESSAGE | VARCHAR | The Snowflake error message. |
| STORAGE\_METHOD\_NAME | VARCHAR | The method (action) tried against the storage location; for example, `findRegionForLocation` or `deleteCurrentFiles`. |
| STORAGE\_PROVIDER\_ERROR\_MESSAGE | VARCHAR | The error message received from your cloud service provider. |

Expand

Show lessSee more

## Examples

Retrieve all storage access errors for the external volume named `my_s3_external_volume`:

Copy code

```
SELECT * FROM snowflake.monitoring.iceberg_access_errors
  WHERE EXTERNAL_VOLUME_NAME ILIKE 'my_s3_external_volume';
```

Retrieve storage access errors that started within the last hour for the external volume named `my_external_volume`:

Copy code

```
SELECT * FROM snowflake.monitoring.iceberg_access_errors
  WHERE EXTERNAL_VOLUME_NAME ILIKE 'my_external_volume'
  AND CREATED_ON > DATEADD(HOUR, -1, CURRENT_TIMESTAMP());
```
