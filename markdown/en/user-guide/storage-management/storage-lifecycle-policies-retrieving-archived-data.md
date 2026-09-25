# Retrieve archived data

Read archived data by using the [CREATE TABLE … FROM ARCHIVE OF](/sql-reference/sql/create-table#label-create-table-from-archive-of-syntax) command.

For example, the following statement creates a new table from archived rows where the value in the `event_timestamp` column is between
January 15 and January 20 of 2023:

Copy code

```
CREATE TABLE my_table
  FROM ARCHIVE OF my_source_table AS st
  WHERE st.event_timestamp BETWEEN '01/15/2023' AND '01/20/2023';
```

For syntax details and parameter descriptions, see [CREATE TABLE … FROM ARCHIVE OF](/sql-reference/sql/create-table#label-create-table-from-archive-of-syntax)
in the [CREATE TABLE](/sql-reference/sql/create-table) documentation.

Note

- Using this command requires the OWNERSHIP privilege on the source table.
- Specifying column definitions, policies, tags, or other constraints isn’t supported. Snowflake automatically retrieves
  the table schema, policies, tags, and constraints from the source table. For details about how schema
  changes (column add or drop) on the source table affect restore, see
  [Schema evolution](/user-guide/storage-management/storage-lifecycle-policies-retrieving-archived-data#label-slp-schema-evolution).
- The WHERE clause is required. Reading archived data is expensive and should be performed infrequently.
  Filtering results using the WHERE clause helps you minimize costs by ensuring that Snowflake reads only the data that you
  require from archival storage.
- To estimate the number of files that Snowflake will retrieve from archive storage, run the [EXPLAIN](/sql-reference/sql/explain) command before
  this operation. The output includes a `createTableFromArchiveData` operation and displays `ARCHIVE OF table` in
  the `objects` column for the TableScan operation. For more information, see [Estimate retrieval costs with EXPLAIN](/user-guide/storage-management/storage-lifecycle-policies-retrieving-archived-data#label-slp-retrieve-explain).
- To see a history of data retrieval from archive storage, use the [ARCHIVE\_STORAGE\_DATA\_RETRIEVAL\_USAGE\_HISTORY view](/sql-reference/account-usage/archive_storage_data_retrieval_usage_history).
- When retrieving data from archive using CREATE TABLE … FROM ARCHIVE OF, if the source table inherits a
  tag-based masking policy from its parent schema or database, the target table must be created within the same
  schema or database from which the masking policy is inherited. Attempting to create the target table outside
  that boundary results in an error.
- To retrieve data from the COLD tier of archive storage, Snowflake must first restore the files from external cloud storage. This process
  can take up to 48 hours.

  To support this process, set the following parameters appropriately:

  - [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds) must be at least 48 hours.
  - [ABORT\_DETACHED\_QUERY](/sql-reference/parameters#label-abort-detached-query) must be FALSE.

  COLD storage tier restore operations support a maximum of 1 million files per restore operation.
- If you cancel a CREATE TABLE operation that retrieves data from archive storage, you might still incur retrieval costs.

## Schema evolution

Schema changes (column add or drop) on the source table after archival has begun don’t disrupt
archival. When you restore archived data with [CREATE TABLE … FROM ARCHIVE OF](/sql-reference/sql/create-table#label-create-table-from-archive-of-syntax),
the new table reflects the *current* schema of the source table, not the schema that was in
effect when each row was archived.

### Add a column

- Adding a column to the source table after archival has begun doesn’t cause archival to fail
  or produce schema conflicts. Archival continues normally.
- On restore (`CREATE TABLE ... FROM ARCHIVE OF`):
  - The restored table reflects the current schema of the source table, including the new
    column.
  - Rows archived *before* the column was added return NULL for the new column.
  - Rows archived *after* the column was added return the actual stored values.
  - No manual schema reconciliation is required.

### Drop a column

- Dropping a column from the source table after archival has begun doesn’t cause archival to
  fail.
- On restore (`CREATE TABLE ... FROM ARCHIVE OF`):
  - The restored table reflects the current schema. The dropped column isn’t present.
  - Historical values that existed in archived rows for the dropped column aren’t accessible
    through `CREATE TABLE ... FROM ARCHIVE OF`.
  - The restore silently excludes the dropped column from the output.
- Columns dropped from the source table are excluded from the restore regardless of whether
  archived data contained values for them.

## View archive metadata before retrieval

Before retrieving archived data, you can inspect metadata about the archive to understand what data
is available. Use the [SYSTEM$GET\_TABLE\_ARCHIVE\_METADATA](/sql-reference/functions/system_get_table_archive_metadata)
function to view:

- Total row count in the archive
- Column data types
- Minimum and maximum values for numeric and timestamp columns

This helps you decide which data to retrieve without incurring retrieval costs.

Note

The table owner or an account administrator (a user with the ACCOUNTADMIN role) who has
access to the table can execute this function.

## Estimate retrieval costs with EXPLAIN

To estimate how many files Snowflake will retrieve from archive storage, use the [EXPLAIN](/sql-reference/sql/explain) command.

The command output includes the following data:

- A `createTableFromArchiveData` operation in the `operation` column.
- `ARCHIVE OF <table>` in the `objects` column for the TableScan operation.
- The number of partitions that will be retrieved in the `assignedPartitions` column for the archive
  TableScan operation. This value indicates the number of partitions
  that Snowflake will restore from cold tier to retrieve the data from archive storage.
- The number of bytes that will be retrieved in the `bytesAssigned` column.

For example:

Copy code

```
EXPLAIN
CREATE TABLE my_table
  FROM ARCHIVE OF my_source_table AS st
  WHERE st.event_timestamp BETWEEN '01/15/2023' AND '01/20/2023';
```
