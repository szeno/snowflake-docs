Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$AUTO\_REFRESH\_STATUS

Returns the automated refresh status for an externally managed [Iceberg table](/user-guide/tables-iceberg).

Note

To return this refresh status for all applicable externally managed Apache Iceberg™ tables for which you have access privileges, run the [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables)
command and see the `auto_refresh_status` column in the output.

## Syntax

Copy code

```
SYSTEM$AUTO_REFRESH_STATUS('<table_name>')
```

## Arguments

`'table_name'`
:   The name of the Iceberg table for which you want to retrieve the current automated refresh status.

    If using the fully qualified name, enclose the entire name in single quotes, including the database and schema.
    If the table name is case-sensitive or includes any special characters or spaces, you must use double quotes.
    Enclose the double quotes within the single quotes, for example, `'"Table_Name"'`.

## Returns

The function returns a JSON object containing the following name/value pairs:

Copy code

```
{
  "executionState":"<value>",
  "invalidExecutionStateReason":"<value>",
  "pendingSnapshotCount":"<value>",
  "oldestSnapshotTime":"<value>",
  "currentSnapshotId":"<value>",
  "currentSnapshotSummary":"<value>",
  "lastSnapshotTime":"<value>",
  "lastUpdatedTime":"<value>",
  "currentMetadataFile":"<value>",
  "currentSchemaId":"<value>"
}
```

Where:

> `executionState`
> :   Current execution state of the pipe that Snowflake uses to automate metadata refreshes for the table.
>
>     Values:
>
>     - `RUNNING`: Automated refresh is running as expected. This status doesn’t indicate whether Snowflake is actively processing
>       event messages for the pipe.
>     - `STALLED`: Automated refresh encountered an error and is attempting to recover.
>     - `STOPPED`: Automated refresh encountered an unrecoverable error and is stopped unless you take further action. For more information,
>       see [Error recovery](/user-guide/tables-iceberg-auto-refresh#label-tables-iceberg-auto-refresh-error-recovery).
>     - `ICEBERG_TABLE_NOT_INITIALIZED`: Automated refresh isn’t initialized because an error occurred when Snowflake attempted to create the table.
>       To run automated refresh, you must resolve the error, and then [enable automated refresh for the table](/user-guide/tables-iceberg-auto-refresh#label-tables-iceberg-auto-refresh-update).
>       This execution state only occurs for tables in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database).
>
> `invalidExecutionStateReason`
> :   Error message associated with a `STALLED` or `STOPPED` execution state.
>
> `pendingSnapshotCount`
> :   Number of snapshots queued for automated refresh.
>
> `oldestSnapshotTime`
> :   Earliest timestamp among queued snapshots. Snowflake sets the timestamp for a snapshot when the snapshot is added to the queue.
>
> `currentSnapshotId`
> :   ID of the current snapshot that Snowflake is tracking. This represents the snapshot that the current table data corresponds to.
>
> `currentSnapshotSummary`
> :   The Iceberg snapshot summary from the `metadata.json` file. NULL if not present in the metadata file.
>
> `lastSnapshotTime`
> :   Creation timestamp for the current snapshot according to Iceberg metadata.
>     This timestamp corresponds to when the current snapshot was generated in the external catalog.
>
> `lastUpdatedTime`
> :   Timestamp that indicates when Snowflake successfully processed the current snapshot.
>     The difference between this value and the `lastSnapshotTime` indicates the latency between when snapshots
>     are created in the external catalog and when Snowflake successfully refreshes the table metadata.
>
>     To decrease the latency, adjust the `REFRESH_INTERVAL_SECONDS` parameter for the catalog integration associated with the table.
>
> `currentMetadataFile`
> :   The full path to the current metadata file.
>
> `currentSchemaId`
> :   ID of the current schema.

## Usage notes

- Calling this function requires a role that has the OWNERSHIP privilege on the Iceberg table.
- For Delta-based tables, note the following:
  - In the context of this function and automated refresh in Snowflake, the term “snapshot” refers to a Delta commit.
  - The function doesn’t return a value for `lastSnapshotTime`.

## Examples

Retrieve the automated refresh status for the table `my_iceberg_table` in the schema `db1.schema1`:

Copy code

```
SELECT SYSTEM$AUTO_REFRESH_STATUS('db1.schema1.my_iceberg_table');
```
