Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# REPLICATION\_GROUP\_REFRESH\_HISTORY view

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view can be used to query the refresh history for a specified
[replication or failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups).

See also:
:   [REPLICATION\_GROUP\_REFRESH\_HISTORY, REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL](/sql-reference/functions/replication_group_refresh_history) (Information Schema table function)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| REPLICATION\_GROUP\_NAME | VARCHAR | Name of the secondary replication or failover group. |
| REPLICATION\_GROUP\_ID | NUMBER | Internal/system-generated identifier for the replication or failover group. |
| PHASE\_NAME | VARCHAR | Current phase in the replication operation. For the list of phases, see the [Usage notes](#usage-notes). |
| START\_TIME | TIMESTAMP\_LTZ | Time when the replication operation began. |
| END\_TIME | TIMESTAMP\_LTZ | Time when the replication operation finished, if applicable. `NULL` if it is in progress. |
| JOB\_UUID | VARCHAR | Query ID for the refresh job. |
| TOTAL\_BYTES | VARIANT | A JSON object that provides detailed information about refreshed databases:   - `totalBytesToReplicate`: Total number of bytes expected to be replicated. - `bytesUploaded`: Actual number of bytes uploaded. - `bytesDownloaded`: Actual number of bytes downloaded. - `databases`: List of JSON objects containing the following fields for each member database:   - `name`: Name of the database.   - `totalBytesToReplicate`: Total bytes expected to be replicated for the database. |
| OBJECT\_COUNT | VARIANT | A JSON object that provides detailed information about refreshed objects:   - `totalObjects`: Total number of objects in the replication or failover group. - `completedObjects`: Total number of objects completed. - `objectTypes`: List of JSON objects containing the following fields for each type:   - `objectType`: Type of object (for example users, roles, grants, warehouses, schemas, tables, columns, etc).   - `totalObjects`: Total number of objects of this type in the replication or failover group.   - `completedObjects`: Total number of objects of this type that were completed. |
| PRIMARY\_SNAPSHOT\_TIMESTAMP | TIMESTAMP\_LTZ | Timestamp when the primary snapshot was created. |
| ERROR | VARIANT | NULL if the refresh operation is successful. If the refresh operation fails, returns a JSON object that provides detailed information about the error:   - `errorCode`: Error code of the failure. - `errorMessage`: Error message of the failure. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (three hours).

  To view real-time refresh progress, use the [REPLICATION\_GROUP\_REFRESH\_HISTORY, REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL](/sql-reference/functions/replication_group_refresh_history) table function.

- Results are only returned for secondary failover or replication groups in the current account (the target account).
- The following is the list of phases in the order processed:

  | # | Phase name | Description |
  | --- | --- | --- |
  | 1 | `SECONDARY_SYNCHRONIZING_MEMBERSHIP` | The secondary replication or failover group receives information from the primary group about the objects included in the group, and updates its membership metadata. |
  | 2 | `SECONDARY_UPLOADING_INVENTORY` | The secondary replication or failover group sends an inventory of its objects in the target account to the primary group. |
  | 3 | `PRIMARY_UPLOADING_METADATA` | The primary replication or failover group creates a snapshot of metadata in the source account and sends it to the secondary group. |
  | 4 | `PRIMARY_UPLOADING_DATA` | The primary replication or failover group copies the files the secondary group needs to reconcile any deltas between the objects in the source and target accounts. |
  | 5 | `SECONDARY_DOWNLOADING_METADATA` | The secondary replication or failover group applies the snapshot of the metadata that was sent by the primary. The metadata updates are not applied atomically and instead applied over time. |
  | 6 | `SECONDARY_DOWNLOADING_DATA` | The secondary replication or failover group copies the files sent by the primary group to the target account. |
  | 7 | `SECONDARY_COMMITTING` | The secondary replication or failover group applies the data changes to tables from the files that were copied from the primary account. |
  | 8 | `COMPLETED` / `FAILED` / `CANCELED` | Refresh operation status. |

  Expand

  Show lessSee more

## Examples

To retrieve the refresh history for the secondary failover group `myfg`, execute the following statement:

Copy code

```
SELECT phase_name, start_time, end_time,
       total_bytes, object_count, error
  FROM SNOWFLAKE.ACCOUNT_USAGE.REPLICATION_GROUP_REFRESH_HISTORY
  WHERE replication_group_name = 'MYFG';
```

To retrieve the last refresh record for each replication or failover group, execute the following statement:

Copy code

```
SELECT replication_group_name, phase_name,
       start_time, end_time,
       total_bytes, object_count, error,
       ROW_NUMBER() OVER (
         PARTITION BY replication_group_name
         ORDER BY end_time DESC
       ) AS row_num
  FROM SNOWFLAKE.ACCOUNT_USAGE.REPLICATION_GROUP_REFRESH_HISTORY
  QUALIFY row_num = 1;
```
