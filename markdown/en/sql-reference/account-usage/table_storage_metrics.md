Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# TABLE\_STORAGE\_METRICS view

This Account Usage view displays table-level storage utilization information, which is used to calculate the storage billing for each table in the account, including tables that have been dropped, but are still incurring storage costs.

In addition to table metadata, the view displays the number of storage bytes billed for each table. Snowflake breaks down the bytes into the following categories:

- Active bytes, representing data in the table that can be queried.
- Deleted bytes that are still accruing storage charges because they have not been purged yet from the system. These bytes are classified into the following sub-categories:
  - Bytes in Time Travel (recently deleted, but still within the Time Travel retention period for the table).
  - Bytes in Fail-safe (deleted bytes that are past the Time Travel retention period, but within the Fail-safe period for the table).
  - Bytes retained for clones (deleted bytes that are no longer in Time Travel or Fail-safe, but are still retained because clones of the table reference the bytes).

In other words, rows are maintained in this view for at least as long as the corresponding tables are billed for storage, regardless of various states that the data in the tables may be in (active, Time Travel, Fail-safe, or retained for clones).

For more details about data storage in tables, see [Data storage considerations](/user-guide/tables-storage-considerations).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal/system-generated identifier for the table. |
| TABLE\_NAME | VARCHAR | Name of the table. |
| TABLE\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the table. |
| TABLE\_SCHEMA | VARCHAR | Schema that the table belongs to. |
| TABLE\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the table. |
| TABLE\_CATALOG | VARCHAR | Database that the table belongs to. |
| CLONE\_GROUP\_ID | NUMBER | Unique identifier for the oldest clone ancestor of this table. Same as ID if the table is not a clone. |
| IS\_TRANSIENT | VARCHAR | ‘YES’ if table is transient or temporary, otherwise ‘NO’. Transient and temporary tables have no Fail-safe period. |
| ACTIVE\_BYTES | NUMBER | Bytes owned by (and billed to) this table that are in the active state for the table. For Iceberg table storage, active bytes aren’t billed to *Iceberg* tables. For more information, see [Iceberg table billing](/user-guide/tables-iceberg#label-tables-iceberg-billing). |
| TIME\_TRAVEL\_BYTES | NUMBER | Bytes owned by (and billed to) this table that are in the Time Travel state for the table. |
| FAILSAFE\_BYTES | NUMBER | Bytes owned by (and billed to) this table that are in the Fail-safe state for the table. |
| RETAINED\_FOR\_CLONE\_BYTES | NUMBER | Bytes owned by (and billed to) this table that are retained after deletion because they are referenced by one or more clones of this table, or by [WORM backups](/user-guide/backups) that contain the table. |
| DELETED | BOOLEAN | TRUE if table has been dropped or recreated. |
| TABLE\_CREATED | TIMESTAMP\_LTZ | Date and time when the table was created. |
| TABLE\_DROPPED | TIMESTAMP\_LTZ | Date and time when the table was dropped. NULL if table has not been dropped. |
| TABLE\_ENTERED\_FAILSAFE | TIMESTAMP\_LTZ | Date and time when the table, if dropped, entered the Fail-safe state, or NULL. In this state, the table cannot be restored using UNDROP. For transient tables, which aren’t recoverable using Fail-safe, this column indicates when the time travel retention period has passed. |
| SCHEMA\_CREATED | TIMESTAMP\_LTZ | Date and time when the schema for the table was created. |
| SCHEMA\_DROPPED | TIMESTAMP\_LTZ | Date and time when the schema for the table was dropped. |
| CATALOG\_CREATED | TIMESTAMP\_LTZ | Date and time when the database for the table was created. |
| CATALOG\_DROPPED | TIMESTAMP\_LTZ | Date and time when the database for the table was dropped. |
| COMMENT | VARCHAR | Comment for the table. |
| INSTANCE\_ID | NUMBER | Internal/system-generated identifier for the instance which the object belongs to. |
| ARCHIVE\_STORAGE\_COOL\_ACTIVE\_BYTES | NUMBER | The number of bytes in the cool storage tier owned by (and billed to) this table that are in the active state for the table. |
| ARCHIVE\_STORAGE\_COLD\_ACTIVE\_BYTES | NUMBER | The number of bytes in the cold storage tier owned by (and billed to) this table that are in the active state for the table. |
| ARCHIVE\_STORAGE\_COOL\_TIME\_TRAVEL\_BYTES | NUMBER | The number of bytes in the cool storage tier owned by (and billed to) this table that are in the Time Travel state for the table. |
| ARCHIVE\_STORAGE\_COLD\_TIME\_TRAVEL\_BYTES | NUMBER | The number of bytes in the cold storage tier owned by (and billed to) this table that are in the Time Travel state for the table. |
| ARCHIVE\_STORAGE\_COOL\_FAILSAFE\_BYTES | NUMBER | The number of bytes owned by (and billed to) this table in the COOL storage tier that are in the Fail-safe state for the table. |
| ARCHIVE\_STORAGE\_COLD\_FAILSAFE\_BYTES | NUMBER | The number of bytes owned by (and billed to) this table in the COLD storage tier that are in the Fail-safe state for the table. |
| ARCHIVE\_STORAGE\_COOL\_EARLY\_DELETION\_PENALTY\_BYTES | NUMBER | The number of penalty bytes deleted early and billed for) that are in the COOL storage tier. For more information, see [minimum storage duration charges](/user-guide/storage-management/storage-lifecycle-policies-billing#label-slp-billing-penalty-bytes). |
| ARCHIVE\_STORAGE\_COLD\_EARLY\_DELETION\_PENALTY\_BYTES | NUMBER | The number of penalty bytes deleted early and billed for) that are in the COLD storage tier. For more information, see [minimum storage duration charges](/user-guide/storage-management/storage-lifecycle-policies-billing#label-slp-billing-penalty-bytes). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 90 minutes.
- Storage metrics for hybrid tables are not tracked in this view. For information about storage consumption for hybrid tables,
  see [Evaluate cost for hybrid tables](/user-guide/tables-hybrid-cost).
- Note

  With [BCR-2127](/release-notes/bcr-bundles/2025_07/bcr-2127),
  this view includes new columns for storage lifecycle policies.
  To view storage lifecycle policy columns, you must enable the 2025\_07 behavior change bundle
  in your account.

  To [enable this bundle in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-enable-bundle),
  execute the following statement:

  Copy code

  ```
  SELECT SYSTEM$ENABLE_BEHAVIOR_CHANGE_BUNDLE('2025_07');
  ```

- `ID` and `CLONE_GROUP_ID`:

  - `ID` does not change for a table throughout its lifecycle, including if the table is renamed or dropped.
  - `CLONE_GROUP_ID` is the ID of the oldest ancestor of a clone, including if the table has been dropped, but is still accruing storage costs. For example:

    1. Table `t2` is cloned from `t1`.
    2. Table `t3` is cloned from `t2`.

    All three tables list the `ID` for `t1` as their `CLONE_GROUP_ID`, even if `t1` is dropped and eventually purged from Snowflake.
  - If the IDs are identical, the table is not a clone.
  - Storage bytes are always owned by, and therefore billed to, the table where the bytes were initially added. If the table is then cloned, storage metrics for these initial bytes never transfer
    to the clones, even if the bytes are deleted from the source table.
- Cloned tables share the same underlying storage (at the micro-partition level) until either the original table or cloned table is modified. With each change made to either table, the table takes
  “ownership” of the changed bytes.
- Dropped tables are displayed in the view for at least as long as they incur storage costs:

  - Dropped tables retain their active storage metrics, indicating how many bytes will be active if the table is restored.
  - Dropped tables in the Time Travel retention period for the table can be restored using the UNDROP command.
  - Dropped tables in Fail-safe (`TABLE_ENTERED_FAILSAFE` is not `NULL`) will potentially display `NULL` values in most columns, except for:

    ID columns:
    :   `ID` , `CLONE_GROUP_ID`

    Bytes columns:
    :   `ACTIVE_BYTES` , `TIME_TRAVEL_BYTES` , `FAILSAFE_BYTES` , `RETAINED_FOR_CLONE_BYTES`

    These tables cannot be restored using the UNDROP command.
- The view can include rows for dropped tables where `ACTIVE_BYTES`, `TIME_TRAVEL_BYTES`, `FAILSAFE_BYTES`, and `RETAINED_FOR_CLONE_BYTES` are all `0`. These rows don’t incur storage costs.
- When data is deleted from a table with a Time Travel retention period of 0 days, asynchronous background processes purge the active bytes
  or move them directly into Fail-safe storage, depending on the table type. This may take a short time to complete. During that time, the
  `TIME_TRAVEL_BYTES` column may contain a non-zero value even when the Time Travel retention period is 0 days.
- `FAILSAFE_BYTES` denotes bytes that have passed beyond Time Travel. All such bytes are billed to the current table.
- If multiple rows have the same value in the `TABLE_NAME` column, this indicates that multiple versions of the table exist. A version is created each time a table is dropped and a new table
  with the same name is created, including when a [CREATE OR REPLACE TABLE](/sql-reference/sql/create-table) command is issued on an existing table. Note that the current version will have a
  `NULL` value for the `TABLE_DROPPED` column; all other versions will have a timestamp value. This is important to note because each version of a table incurs storage costs associated with
  Time Travel (and Fail-safe, if the table is permanent).
- Any data in the `DELETED` column prior to August 2018 may not be accurate.
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
