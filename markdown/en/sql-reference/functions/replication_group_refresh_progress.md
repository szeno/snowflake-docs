Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# REPLICATION\_GROUP\_REFRESH\_PROGRESS, REPLICATION\_GROUP\_REFRESH\_PROGRESS\_BY\_JOB, REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

You can use the REPLICATION\_GROUP\_REFRESH\_PROGRESS family of table functions to query the status of refresh operations
for replication or failover groups:

- REPLICATION\_GROUP\_REFRESH\_PROGRESS returns a JSON object indicating the refresh status for a secondary replication or failover group by
  name.
- REPLICATION\_GROUP\_REFRESH\_PROGRESS\_BY\_JOB returns a JSON object indicating the refresh status for a secondary replication
  or failover group by query ID.
- REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL returns a JSON object indicating the refresh status for all the secondary replication
  and failover groups.

Note

- REPLICATION\_GROUP\_REFRESH\_PROGRESS only returns the replication or failover group refresh activity for the most recent refresh if it
  occurred within the last 14 days.
- REPLICATION\_GROUP\_REFRESH\_PROGRESS\_BY\_JOB and REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL return replication or failover group
  refresh activity within the last 14 days. By default (when no date-range arguments are provided),
  REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL returns data for the last 12 hours. Use the optional
  `DATE_RANGE_START` and `DATE_RANGE_END` arguments to query a custom range within the 14-day
  retention window.

## Syntax

Copy code

```
REPLICATION_GROUP_REFRESH_PROGRESS( '<secondary_group_name>' )

REPLICATION_GROUP_REFRESH_PROGRESS_BY_JOB( '<query_id>' )

REPLICATION_GROUP_REFRESH_PROGRESS_ALL(
      [ DATE_RANGE_START => <constant_expr> ]
      [ , DATE_RANGE_END => <constant_expr> ] )
```

## Arguments

`'secondary_group_name'`
:   Name of the secondary replication or failover group. Note that the entire name must be enclosed in single quotes.

`'query_id'`
:   ID of the replication group refresh query. The query ID can be obtained from the **History** [![History tab](/static/images/screens/ui-navigation-history-icon.svg)](/static/images/screens/ui-navigation-history-icon.svg) page in the web
    interface.

The following arguments are optional for REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   The date/time range for which to return replication refresh progress.

    - If neither a start date nor an end date is specified, the default is the last 12 hours.
    - If a start date is specified but no end date, [CURRENT\_DATE](/sql-reference/functions/current_date)
      at midnight is used as the end of the range.
    - If an end date is specified but no start date, the range starts 12 hours prior to the start
      of `DATE_RANGE_END`.

    Data is retained for 14 days. If the requested range extends beyond the 14-day retention window,
    the function returns an error.

## Output

The function returns the following columns. REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL has additional
columns that are the first two columns in the result set.

| Column Name | Data Type | Description |
| --- | --- | --- |
| GROUP\_NAME | TEXT | Specifies which secondary replication or failover group corresponds to this row in the result set. Only applies to REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL. |
| GROUP\_TYPE | TEXT | Specifies whether the group corresponding to this row in the result set is a failover group or a replication group. The value is either `FAILOVER` or `REPLICATION`. Only applies to REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL. |
| PHASE\_NAME | TEXT | Name of the replication phases completed (or in progress) so far. For the list of phases, see the usage notes. |
| START\_TIME | TIMESTAMP\_LTZ | Time when the replication phase began. |
| END\_TIME | TIMESTAMP\_LTZ | Time when the phase finished, if applicable. `NULL` if the phase is in progress or is the terminating phase (`COMPLETED`/`FAILED`/`CANCELED`). |
| PROGRESS | TEXT | - `PRIMARY_UPLOADING_DATA`: Percentage of total bytes replicated. - `SECONDARY_DOWNLOADING_METADATA`: Percentage of the total number of objects replicated. - `SECONDARY_DOWNLOADING_DATA`: Percentage of total bytes replicated. - `SECONDARY_COMMITTING`: Percentage of tables that finished replicating.   Empty for remaining phases |
| DETAILS | VARIANT | - For phase `PRIMARY_UPLOADING_METADATA`:    - `primarySnapshotTimestamp`: Time when the primary snapshot was created. Format is epoch time. - For phase `PRIMARY_UPLOADING_DATA`:    - `totalBytesToReplicate`: Total number of bytes expected to be uploaded.   - `totalBytesToUpload`: Total number of bytes to required to be uploaded.   - `bytesUploaded`: Total number of bytes uploaded so far.   - `databases`: List of JSON objects containing the following fields for each member database:     - `name`: Database name.     - `totalBytesToReplicate`: Total bytes expected to be uploaded for the database. - For phase `SECONDARY_DOWNLOADING_DATA`:    - `totalBytesToReplicate`: Total number of bytes expected to be downloaded.   - `totalBytesToDownload`: Actual number of bytes required to be downloaded.   - `bytesDownloaded`: Actual number of bytes downloaded so far.   - `databases`: List of JSON objects containing the following fields for each member database:     - `name`: Database name.     - `totalBytesToReplicate`: Total bytes expected to be downloaded for the database. - For phase `SECONDARY_DOWNLOADING_METADATA`:    - `totalObjects`: Total number of objects to download.   - `completedObjects`: Total number of objects downloaded so far.   - `objectTypes`: List of JSON objects containing the following fields for each object type:     - `objectType`: Type of object (for example, users, roles, grants, warehouses, schemas, tables, columns, etc).     - `totalObjects`: Total number of objects of this type.     - `completedObjects`: Number of completed objects of this type. - For phase `SECONDARY_COMMITTING`:    - `totalObjects`: Total number of tables to process.   - `completedObjects`: Total number of tables processed so far.   - `objectTypes`: List of JSON objects containing the following fields for each object type:     - `objectType`: Type of object.     - `totalObjects`: Total number of objects of this type.     - `completedObjects`: Number of completed objects of this type. - For phase `FAILED`:    - `errorCode`: Error code of the failure.   - `errorMessage`: Error message of the failure. |

Expand

Show lessSee more

## Usage notes

- When no `DATE_RANGE_START` or `DATE_RANGE_END` arguments are provided,
  REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL returns data for the last 12 hours.
  To retrieve data beyond the last 12 hours, specify the date range explicitly.
  Data is available for up to 14 days.
- Only returns rows for a role with any privilege on the replication or failover group.
- Only returns rows for a secondary replication or failover group in the current account.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name
  must be fully-qualified. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).

- Following is the list of phases in the order processed:

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
- In the `PRIMARY_UPLOADING_DATA` and `SECONDARY_DOWNLOADING_DATA` phases, the `totalBytesToReplicate` value is estimated prior
  to the replication operation. This value may differ from the `totalBytesToUpload` or `totalBytesToDownload` value in
  the respective phase.

  For example, if during the `PRIMARY_UPLOADING_DATA` phase, a previous replication operation uploaded some
  bytes but was canceled before the operation completed, those bytes would not be uploaded again. In that case, `totalBytesToUpload`
  would be lower than `totalBytesToReplicate`.

## Examples

To retrieve the current refresh progress for replication group `rg1`, execute the following
statement:

Copy code

```
SELECT phase_name, start_time, end_time, progress, details
  FROM TABLE(INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_PROGRESS('rg1'));
```

To retrieve the replication group refresh progress by query ID, replace the query ID in
the example and execute the following statement:

Copy code

```
SELECT phase_name, start_time, end_time, progress, details
  FROM TABLE(
    INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_PROGRESS_BY_JOB(
      '012a3b45-1234-a12b-0000-1aa200012345'));
```

To retrieve the refresh progress for the last 12 hours (default) for all failover groups and replication groups,
execute the following statement:

Copy code

```
SELECT phase_name, start_time, end_time, progress, details
  FROM TABLE(INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_PROGRESS_ALL());
```

To retrieve the refresh progress for the last 7 days for all groups:

Copy code

```
SELECT phase_name, start_time, end_time, progress, details
  FROM TABLE(
    INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_PROGRESS_ALL(
        DATE_RANGE_START => DATEADD(D, -7, CURRENT_DATE),
        DATE_RANGE_END => CURRENT_DATE));
```
