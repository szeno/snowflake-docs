Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# REPLICATION\_GROUP\_REFRESH\_HISTORY, REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

You can use the REPLICATION\_GROUP\_REFRESH\_HISTORY family of table functions to query the replication history for
one secondary replication or failover group, or all such groups.

By default (when no date-range arguments are provided), these functions return data for the last 12 hours.
You can use the optional `DATE_RANGE_START` and `DATE_RANGE_END` arguments to query a custom range
within the 14-day retention window.

See also:
:   [REPLICATION\_GROUP\_REFRESH\_HISTORY view](/sql-reference/account-usage/replication_group_refresh_history)

## Syntax

Copy code

```
REPLICATION_GROUP_REFRESH_HISTORY(
      '<secondary_group_name>'
      [ , DATE_RANGE_START => <constant_expr> ]
      [ , DATE_RANGE_END => <constant_expr> ] )

REPLICATION_GROUP_REFRESH_HISTORY_ALL(
      [ DATE_RANGE_START => <constant_expr> ]
      [ , DATE_RANGE_END => <constant_expr> ] )
```

## Arguments

`'secondary_group_name'`
:   Name of the secondary group. The entire name must be enclosed in single quotes.
    Required for REPLICATION\_GROUP\_REFRESH\_HISTORY. Not used with REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL.

The following arguments are optional for both functions.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   The date/time range for which to return replication refresh history.

    - If neither a start date nor an end date is specified, the default is the last 12 hours.
    - If a start date is specified but no end date, [CURRENT\_DATE](/sql-reference/functions/current_date)
      at midnight is used as the end of the range.
    - If an end date is specified but no start date, the range starts 12 hours prior to the start
      of `DATE_RANGE_END`.

    Data is retained for 14 days. If the requested range extends beyond the 14-day retention window,
    the function returns an error.

## Output

The function returns the following columns. REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL has additional
columns that are the first two columns in the result set.

| Column Name | Data Type | Description |
| --- | --- | --- |
| GROUP\_NAME | TEXT | Specifies which secondary replication or failover group corresponds to this row in the result set. Only applies to REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL. |
| GROUP\_TYPE | TEXT | Specifies whether the group corresponding to this row in the result set is a failover group or a replication group. The value is either `FAILOVER` or `REPLICATION`. Only applies to REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL. |
| PHASE\_NAME | TEXT | Current phase in the replication operation. For the list of phases, see the [Usage Notes](#usage-notes). |
| START\_TIME | TIMESTAMP\_LTZ | Time when the replication operation began. |
| END\_TIME | TIMESTAMP\_LTZ | Time when the replication operation finished, if applicable. `NULL` if it is in progress. |
| JOB\_UUID | TEXT | Query ID for the refresh job. |
| TOTAL\_BYTES | VARIANT | A JSON object that provides detailed information about refreshed databases:   - `totalBytesToReplicate`: Total number of bytes expected to be replicated. - `bytesUploaded`: Actual number of bytes uploaded. - `bytesDownloaded`: Actual number of bytes downloaded. - `databases`: List of JSON objects containing the following fields for each member database:   - `name`: Name of the database.   - `totalBytesToReplicate`: Total bytes expected to be replicated for the database. |
| OBJECT\_COUNT | VARIANT | A JSON object that provides detailed information about refreshed objects:   - `totalObjects`: Total number of objects in the replication or failover group. - `completedObjects`: Total number of objects completed. - `objectTypes`: List of JSON objects containing the following fields for each type:   - `objectType`: Type of object (for example users, roles, grants, warehouses, schemas, tables, columns, etc).   - `totalObjects`: Total number of objects of this type in the replication or failover group.   - `completedObjects`: Total number of objects of this type that were completed. |
| COMMITTED\_OBJECT\_COUNT | VARIANT | A JSON object that represents the number of tables that have been processed during the `SECONDARY_COMMITTING` phase. The subfields have the same names as the subfields in the `OBJECT_COUNT` column:   - `totalObjects`: Total number of tables to process. - `completedObjects`: Total number of tables processed. - `objectTypes`: List of JSON objects containing the following fields for each type:   - `objectType`: Type of object.   - `totalObjects`: Total number of objects of this type.   - `completedObjects`: Total number of completed objects of this type. |
| PRIMARY\_SNAPSHOT\_TIMESTAMP | TIMESTAMP\_LTZ | Timestamp when the primary snapshot was created. |
| ERROR | VARIANT | NULL if the refresh operation is successful. If the refresh operation fails, returns a JSON object that provides detailed information about the error:   - `errorCode`: Error code of the failure. - `errorMessage`: Error message of the failure. |

Expand

Show lessSee more

## Usage notes

- When no `DATE_RANGE_START` or `DATE_RANGE_END` arguments are provided, the functions return data for
  the last 12 hours. To retrieve data beyond the last 12 hours, specify the date range explicitly.
  Data is available for up to 14 days.
- Only returns rows for a role with any privilege on the replication or failover group.
- Only returns rows for a secondary replication or failover group in the current account.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name
  must be fully-qualified. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).
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

To retrieve the refresh history for secondary group `myfg`,
execute the following statement.

Copy code

```
SELECT phase_name, start_time, end_time,
       total_bytes, object_count, error
  FROM TABLE(
      INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_HISTORY('myfg')
  );
```

To retrieve the refresh history for the last 12 hours (default) for all failover groups and replication groups,
execute the following statement:

Copy code

```
SELECT phase_name, start_time, end_time,
       total_bytes, object_count, error
  FROM TABLE(
      INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_HISTORY_ALL()
  );
```

To retrieve the refresh history for the last 7 days for all groups:

Copy code

```
SELECT phase_name, start_time, end_time,
       total_bytes, object_count, error
  FROM TABLE(
      INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_HISTORY_ALL(
          DATE_RANGE_START => DATEADD(D, -7, CURRENT_DATE),
          DATE_RANGE_END => CURRENT_DATE)
  );
```

To retrieve the refresh history for a specific date range for secondary group `myfg`:

Copy code

```
SELECT phase_name, start_time, end_time,
       total_bytes, object_count, error
  FROM TABLE(
      INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_HISTORY(
          'myfg',
          DATE_RANGE_START => '2025-04-01',
          DATE_RANGE_END => '2025-04-07')
  );
```
