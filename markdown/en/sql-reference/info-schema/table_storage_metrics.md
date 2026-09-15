# TABLE\_STORAGE\_METRICS view

This view displays table-level storage utilization information, which is used to calculate the storage billing for each table in the account, including tables that have been dropped, but are still incurring
storage costs.

In addition to table metadata, the view displays the number of storage bytes billed for each table. Snowflake breaks down the bytes into the following categories:

- Active bytes, representing data in the table that can be queried.
- Deleted bytes that are still accruing storage charges because they have not been purged yet from the system. These bytes are classified into the following sub-categories:
  - Bytes in Time Travel (recently deleted, but still within the Time Travel retention period for the table).
  - Bytes in Fail-safe (deleted bytes that are past the Time Travel retention period, but within the Fail-safe period for the table).
  - Bytes retained for clones (deleted bytes that are no longer in Time Travel or Fail-safe, but are still retained because clones of the table reference the bytes).

In other words, rows are maintained in this view for at least as long as the corresponding tables are billed for storage, regardless of various states that the data in the tables may be in (active, Time Travel, Fail-safe, or retained for clones).

For more details about data storage in tables, see [Data storage considerations](/user-guide/tables-storage-considerations).

Note

To query this view, you must use the ACCOUNTADMIN role. The view is visible to other views and can be queried, but the queries will return no rows.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| TABLE\_CATALOG | VARCHAR | Database that the table belongs to. |
| TABLE\_SCHEMA | VARCHAR | Schema that the table belongs to. |
| TABLE\_NAME | VARCHAR | Name of the table. |
| ID | NUMBER | Unique identifier for the table. |
| CLONE\_GROUP\_ID | NUMBER | Unique identifier for the oldest clone ancestor of this table. Same as ID if the table is not a clone. |
| IS\_TRANSIENT | VARCHAR | ‘YES’ if table is transient or temporary, otherwise ‘NO’. Transient and temporary tables have no Fail-safe period. |
| ACTIVE\_BYTES | NUMBER | Bytes owned by (and billed to) this table that are in the active state for the table. For Iceberg table storage, active bytes aren’t billed to *Iceberg* tables. For more information, see [Iceberg table billing](/user-guide/tables-iceberg#label-tables-iceberg-billing). |
| TIME\_TRAVEL\_BYTES | NUMBER | Bytes owned by (and billed to) this table that are in the Time Travel state for the table. |
| FAILSAFE\_BYTES | NUMBER | Bytes owned by (and billed to) this table that are in the Fail-safe state for the table. |
| RETAINED\_FOR\_CLONE\_BYTES | NUMBER | Bytes owned by (and billed to) this table that are retained after deletion because they are referenced by one or more clones of this table, or by [WORM backups](/user-guide/backups) that contain the table. |
| TABLE\_CREATED | TIMESTAMP\_LTZ | Date and time at which the table was created. |
| TABLE\_DROPPED | TIMESTAMP\_LTZ | Date and time at which the table was dropped. NULL if table has not been dropped. |
| TABLE\_ENTERED\_FAILSAFE | TIMESTAMP\_LTZ | Date and time at which the table, if dropped, entered the Fail-safe state, or NULL. In this state, the table cannot be restored using UNDROP. |
| CATALOG\_CREATED | TIMESTAMP\_LTZ | Date and time at which the database containing the table was created. |
| CATALOG\_DROPPED | TIMESTAMP\_LTZ | Date and time at which the database containing the table was dropped. |
| SCHEMA\_CREATED | TIMESTAMP\_LTZ | Date and time at which the schema containing the table was created. |
| SCHEMA\_DROPPED | TIMESTAMP\_LTZ | Date and time at which the schema containing the table was dropped. |
| COMMENT | VARCHAR | Comment for the table. |

Expand

Show lessSee more

## Usage notes

- There may be a 1-2 hour delay in updating storage related statistics for `active_bytes`, `time_travel_bytes`,
  `failsafe_bytes`, and `retained_for_clone_bytes`.
- ID and CLONE\_GROUP\_ID:

  - ID does not change for a table throughout its lifecycle, including if the table is renamed or dropped.
  - CLONE\_GROUP\_ID is the ID of the oldest ancestor of a clone, including if the table has been dropped, but is still accruing storage costs. For example:

    - Table `t2` is cloned from `t1`.
    - Table `t3` is cloned from `t2`.

    All three tables list the ID for `t1` as their CLONE\_GROUP\_ID, even if `t1` is dropped and eventually purged from Snowflake.
  - If ID and CLONE\_GROUP\_ID are identical, the table is not a clone.
  - Storage bytes are always owned by, and therefore billed to, the table where the bytes were initially added. If the table is then cloned, storage metrics for these initial bytes never transfer
    to the clones, even if the bytes are deleted from the source table.
- Cloned tables share the same underlying storage (at the micro-partition level) until either the original table or cloned table is modified. With each change made to either table, the table takes
  “ownership” of the changed bytes.
- Dropped tables are displayed in the view for at least as long as they incur storage costs:

  - Dropped tables retain their active storage metrics, indicating how many bytes will be active if the table is restored.
  - Dropped tables in the Time Travel retention period for the table can be restored using UNDROP.
  - Dropped tables in Fail-safe (TABLE\_ENTERED\_FAILSAFE not NULL) will potentially display NULL values in most columns, except for:

    ID columns:
    :   ID , CLONE\_GROUP\_ID

    Bytes columns:
    :   ACTIVE\_BYTES , TIME\_TRAVEL\_BYTES , FAILSAFE\_BYTES , RETAINED\_FOR\_CLONE\_BYTES

    These tables cannot be restored using UNDROP.
- The view can include rows for dropped tables where `ACTIVE_BYTES`, `TIME_TRAVEL_BYTES`, `FAILSAFE_BYTES`, and `RETAINED_FOR_CLONE_BYTES` are all `0`. These rows don’t incur storage costs.
- When data is deleted from a table with a Time Travel retention period of 0 days, asynchronous background processes purge the active bytes
  or move them directly into Fail-safe storage, depending on the table type. This may take a short time to complete. During that time, the
  `TIME_TRAVEL_BYTES` column may contain a non-zero value even when the Time Travel retention period is 0 days.
- `FAILSAFE_BYTES` denotes bytes that have passed beyond Time Travel. All such bytes are billed to the current table.
- If multiple rows have the same value in the TABLE\_NAME column, this indicates that multiple versions of the table exist. A version is created each time a table is dropped and a new table with the same
  name is created, including when a [CREATE OR REPLACE TABLE](/sql-reference/sql/create-table) command is issued on an existing table. Note that the current version will have a NULL value for the
  TABLE\_DROPPED column; all other versions will have a timestamp value. This is important to note because each version of a table incurs storage costs associated with Time Travel (and Fail-safe, if the
  table is permanent).
- In some cases, active bytes might include bytes for data in a dropped column. For more information,
  see the [usage notes](/sql-reference/sql/alter-table#label-dropping-column-and-storage) for ALTER TABLE.
- For Iceberg tables:

  - Snowflake doesn’t bill for [Iceberg table](/user-guide/tables-iceberg) storage when the table uses
    an external volume that you manage. However, if the table uses
    [Snowflake Storage](/user-guide/tables-iceberg-internal-storage) (`EXTERNAL_VOLUME = SNOWFLAKE_MANAGED`),
    Snowflake charges for the storage.
    For more information, see [Iceberg table billing](/user-guide/tables-iceberg#label-tables-iceberg-billing).
  - If the table is externally managed,
    this view might display inaccurate storage utilization information.
