# Upgrade an Apache Iceberg™ table from version 2 to version 3

You can upgrade an existing Apache Iceberg™ table from Iceberg version 2 (v2) to version 3 (v3) so that the table conforms to
version 3 of the Apache Iceberg™ table specification. Snowflake performs the upgrade in place, so you don’t have to recreate the table.
The upgraded table keeps the same name, privileges, policies, and downstream references that it had before the upgrade.

Upgrade a table to use Iceberg v3 features with it, such as default values, row lineage, deletion vectors, or v3 data types.
For more information about the Iceberg v3 features that Snowflake supports, see [Apache Iceberg™ tables: Support for Apache Iceberg™ v3](/user-guide/tables-iceberg-v3-specification-support).

Important

The upgrade is permanent. The Apache Iceberg™ specification doesn’t allow you to downgrade a table from v3 to v2.
Before you upgrade a production table, [test the upgrade on a clone](#label-tables-iceberg-upgrade-version-testing-setup).
For a Snowflake-managed table, you can still restore the pre-upgrade v2 table within the Time Travel retention period.
See [Restore the pre-upgrade v2 table](#label-tables-iceberg-upgrade-version-restore-v2).

Note

If you haven’t created your table yet, create it as an Iceberg v3 table instead. For more information, see
[Configure the default Iceberg version](/user-guide/tables-iceberg-v3-specification-support#tables-iceberg-configuring-default-version).

## Supported tables

You can upgrade the following tables:

- Snowflake-managed Apache Iceberg™ tables, including
  [Snowflake-managed tables loaded with Iceberg-compatible Parquet files](/user-guide/tables-iceberg-load#label-tables-iceberg-load-add-files-copy-example).
- Externally managed Apache Iceberg™ tables with `CATALOG_SOURCE = ICEBERG_REST`, including tables in a
  [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database). For more information, see
  [Upgrade externally managed tables](#label-tables-iceberg-upgrade-version-externally-managed).

You can’t upgrade the following tables:

- Externally managed tables that use a native AWS Glue or object storage catalog source.
- [Apache Iceberg™ tables created from Delta files](/sql-reference/sql/create-iceberg-table-delta) (Delta Direct).
- [Parquet Direct tables](/user-guide/tables-iceberg-parquet-direct).
- v2 tables with positional delete files, including tables that use merge-on-read with positional delete files for row-level deletes.
- Snowflake-managed tables whose external volume doesn’t allow writes.

## Upgrade a table to Iceberg v3

1. Verify that the table is an Iceberg v2 table:

   Copy code

   ```
   SHOW PARAMETERS LIKE 'ICEBERG_VERSION' IN TABLE my_v2_iceberg_table;
   ```

   The `value` column in the output is `2` for a v2 table. For other ways to check the version, see
   [Get the format version for Iceberg tables](/user-guide/tables-iceberg-v3-specification-support#label-tables-iceberg-get-format-version).
2. Upgrade the table by using the [ALTER ICEBERG TABLE … UPGRADE TO ICEBERG VERSION 3](/sql-reference/sql/alter-iceberg-table) command:

   Copy code

   ```
   ALTER ICEBERG TABLE my_v2_iceberg_table UPGRADE TO ICEBERG VERSION 3;
   ```
3. Verify the upgrade by running the SHOW PARAMETERS command again. The `value` column in the output is `3`.

## Test the upgrade on a clone

Before you upgrade a production table, test the upgrade on a clone. This approach lets you validate that your queries, pipelines,
and external engines work correctly with Iceberg v3 without affecting your production data.

1. Clone the Iceberg table that you want to upgrade:

   Copy code

   ```
   CREATE ICEBERG TABLE my_table_clone CLONE my_v2_iceberg_table;
   ```
2. Upgrade the clone to v3:

   Copy code

   ```
   ALTER ICEBERG TABLE my_table_clone UPGRADE TO ICEBERG VERSION 3;
   ```
3. Run your tests against the upgraded clone. For example, verify that:

   - Your existing queries return expected results.
   - Pipelines or ETL processes that write to the table work correctly.
   - External engines, such as Apache Spark™ or Trino, can read and write to the table if you use them
     through [Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).

After you validate your workloads against the clone, upgrade your production table.

## Best practices for upgrading tables

- **Confirm that every engine supports v3.** All engines that read from or write to an upgraded table must support Iceberg v3.
  If you use external engines through
  [Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon),
  validate that they support Iceberg v3 before you upgrade.
- **Use a larger warehouse for large tables.** On a smaller warehouse, upgrading a very large table might take minutes.
  For more information about warehouse sizes, see [Warehouse size](/user-guide/warehouses-overview#label-warehouse-size).
- **Plan for a rollback.** Before you upgrade a Snowflake-managed table, record the time and make sure the table’s
  [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days) covers your validation period. If you need to return to v2,
  you can [restore the pre-upgrade v2 table](#label-tables-iceberg-upgrade-version-restore-v2) by using Time Travel within that period.

## Considerations for upgrading tables

### Behavior during the upgrade

Snowflake upgrades each table as an atomic transaction. While the upgrade runs:

- UPDATE, DELETE, and MERGE operations are blocked.
- Snowflake automatically retries INSERT and COPY operations, including Snowpipe, that commit during the upgrade.
- SELECT operations succeed.

If a DML operation starts after an upgrade begins, the operation waits up to the [LOCK\_TIMEOUT](/sql-reference/parameters#label-lock-timeout) limit
before timing out.

### Behavior after the upgrade

- All table properties remain intact, including grants and policies.
- Most objects built on the table continue to work, such as views.
- Streams that don’t reference `METADATA$ROW_ID` continue to work. Streams that reference `METADATA$ROW_ID` stop working,
  and you must recreate them.
- If a dynamic table uses the upgraded table as a source, Snowflake reinitializes the dynamic table with a one-time full refresh.
  Subsequent refreshes resume as incremental.
- Per the Apache Iceberg specification, Snowflake supports the following data type promotions on an upgraded v3 table:
  - `int` to `long`
  - `date` to `timestamp` or `timestamp_ns`
  - `float` to `double`
  - Widening `decimal` precision

### Column defaults

How the upgrade handles column defaults on the v2 table depends on the default type:

- **Literal constant defaults:** Snowflake migrates literal constants, such as `DEFAULT 1`, to Iceberg initial and write defaults.
- **Foldable expression defaults:** When Snowflake can evaluate the complete expression at compile time to a non-`NULL` constant,
  it writes that value as the Iceberg initial and write defaults. Snowflake retains the original expression as the column default.
- **Snowflake-only defaults:** Expressions that Snowflake can’t evaluate to a non-`NULL` constant, sequences, and identity columns
  remain Snowflake-only and aren’t written to Iceberg metadata.

For a Snowflake-managed table that has a Snowflake-only default, Snowflake automatically sets `ALLOW_V3_EXPRESSION_DEFAULTS = TRUE`
on the upgraded table. You don’t need to set the parameter before the upgrade. For more information, see
[Use expression defaults with Snowflake-managed tables](/user-guide/tables-iceberg-default-values#label-tables-iceberg-expression-defaults).

For externally managed tables, defaults must be literal constants, as the Iceberg v3 specification requires. If an externally
managed v2 table has an expression, sequence, or identity default, the upgrade fails.

### Cloning

- You can clone a table while it’s being upgraded, but the clone is a v2 table.
- You can clone an upgraded v3 table, including with Time Travel, when the clone references a table version from at or after the
  time the upgrade completed. A Time Travel clone of a version from before the upgrade completed is a v2 table. You can use this behavior to
  [restore the pre-upgrade v2 table](#label-tables-iceberg-upgrade-version-restore-v2).
- You can’t clone a v2 table directly as a v3 table. Clone the v2 table, and then upgrade the clone.

### Replication

While an Iceberg table is still v2, the following limitations apply to streams and dynamic tables in replication scenarios:

- A stream on a v2 table can’t be replicated.
- You can’t create a stream on a replicated v2 table.
- You can’t create a dynamic table that uses a replicated v2 table as a source.

After you upgrade a Snowflake-managed table to v3, these limitations no longer apply.

If the table is part of a replication or failover group, upgrade it in the source account. The next replication refresh propagates
the upgraded v3 table to target accounts, so you don’t upgrade the table in target accounts. If you fail over before a replication
refresh delivers the upgraded table to target accounts, the replication refresh that runs after failover fails.

For more information, see [Configure replication for Snowflake-managed Apache Iceberg™ tables](/user-guide/tables-iceberg-replication).

## Restore the pre-upgrade v2 table

You can’t downgrade a v3 table to v2. For a Snowflake-managed table, you can instead use Time Travel to clone the table as it existed
before the upgrade. When the clone points to a time before the upgrade completed, the clone is a v2 table that contains the data as of
that time. You can then bring any changes made after the upgrade into the clone and replace the upgraded table with it.

This approach has the following requirements and limitations:

- It’s available only for Snowflake-managed tables, because you can’t clone externally managed Iceberg tables.
- The point in time must be within the table’s [Time Travel retention period](/user-guide/data-time-travel).
- The clone doesn’t include changes made after that point in time. You must apply them to the clone yourself.
- Streams on the upgraded table don’t move to the restored table. You must recreate them.

The following example restores a table named `my_table`:

1. Pause the workloads that write to `my_table`, so that no changes are made while you restore it.
2. Find the time of the upgrade. For example, query the query history for the upgrade statement:

   Copy code

   ```
   SELECT query_id, start_time
     FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
     WHERE query_text ILIKE '%my_table%UPGRADE TO ICEBERG VERSION 3%'
     ORDER BY start_time DESC;
   ```

   Choose a point in time before the upgrade started. In the following steps, replace `<pre_upgrade_timestamp>` with that time.
3. Clone the table as of that point in time. To copy the privileges granted on the table, include COPY GRANTS. To copy tags, include
   COPY TAGS.

   Copy code

   ```
   CREATE ICEBERG TABLE my_table_v2
     CLONE my_table AT (TIMESTAMP => '<pre_upgrade_timestamp>'::TIMESTAMP_LTZ)
     COPY GRANTS COPY TAGS;
   ```

   COPY GRANTS copies all privileges on `my_table` except OWNERSHIP. The role that runs the statement owns the clone, and future grants
   aren’t applied. For more information, see [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake).
4. Verify that the clone is a v2 table. The `value` column in the output is `2`.

   Copy code

   ```
   SHOW PARAMETERS LIKE 'ICEBERG_VERSION' IN TABLE my_table_v2;
   ```
5. Find the changes made after the upgrade, and apply the ones you need to keep to `my_table_v2`. For example, compare the current table
   with the pre-upgrade version:

   Copy code

   ```
   -- Rows that were added or changed after the upgrade
   SELECT * FROM my_table
   MINUS
   SELECT * FROM my_table AT (TIMESTAMP => '<pre_upgrade_timestamp>'::TIMESTAMP_LTZ);

   -- Rows that were deleted or changed after the upgrade
   SELECT * FROM my_table AT (TIMESTAMP => '<pre_upgrade_timestamp>'::TIMESTAMP_LTZ)
   MINUS
   SELECT * FROM my_table;
   ```

   Use these results to apply the changes, for example with a [MERGE](/sql-reference/sql/merge) statement on the table’s key columns.
   MINUS removes duplicate rows, so if the table can contain identical rows, compare row counts by key instead.
6. Replace the upgraded table with the clone by renaming both tables:

   Copy code

   ```
   ALTER ICEBERG TABLE my_table RENAME TO my_table_v3_backup;
   ALTER ICEBERG TABLE my_table_v2 RENAME TO my_table;
   ```

   Grants, policies, tags, and streams stay with the table object when you rename it. As a result, the restored `my_table` has the
   grants that you copied in step 3, and existing streams still point to `my_table_v3_backup`.
7. Recreate the streams that you need on the restored table. A new stream starts tracking changes from the time you create it, so make
   sure that consumers have processed the changes they need from the old streams first.

   Copy code

   ```
   CREATE OR REPLACE STREAM my_stream ON TABLE my_table;
   ```
8. Verify ownership, grants, masking and row access policies, and any dynamic tables or views that use `my_table`. Then resume your
   workloads.
9. After you confirm that you no longer need it, drop the backup table:

   Copy code

   ```
   DROP ICEBERG TABLE my_table_v3_backup;
   ```

## Upgrade externally managed tables

You can upgrade an externally managed Apache Iceberg™ table to v3 in two ways:

- **From Snowflake:** Run `ALTER ICEBERG TABLE <table_name> UPGRADE TO ICEBERG VERSION 3`. This command is supported only for tables
  with `CATALOG_SOURCE = ICEBERG_REST`, both in and outside of a catalog-linked database.
- **From an external engine:** After an external engine upgrades the table to v3, the external engine must also create a new snapshot
  that contains row lineage information, for example by running a DML operation. Until that snapshot exists, Snowflake refreshes of the
  table fail. After a valid snapshot exists, Snowflake picks up the upgraded version on the next automatic or manual refresh. You don’t
  need to drop and recreate the table. After the refresh, `SHOW PARAMETERS LIKE 'ICEBERG_VERSION' IN TABLE <table_name>` returns `3`.

  Updating table properties to change the format version doesn’t create a new snapshot by itself. For example, the following
  Apache Spark statements upgrade a table and then create a new snapshot with an empty insert:

  Copy code

  ```
  ALTER TABLE table_name SET TBLPROPERTIES('format-version'='3');
  INSERT INTO table_name SELECT * FROM table_name LIMIT 0;
  ```

After an upgrade by either method, the same downstream behaviors apply as for Snowflake-managed tables: dynamic tables that use the
upgraded table are reinitialized with a one-time full refresh, and streams that reference `METADATA$ROW_ID` must be recreated.

### Rollbacks and downgrades by external engines

After an externally managed table is upgraded to v3, if an external engine rolls back or downgrades the table, the result of the next
Snowflake refresh depends on the resulting table state:

| State | Description | Refresh result |
| --- | --- | --- |
| Format downgrade (v3 to v2) | The external engine downgrades the table format version from v3 to v2. | Refresh fails. The Iceberg specification doesn’t permit downgrading the table format version, so this state isn’t supported. |
| Snapshot rollback | The table format remains v3, but the external engine rolls back to a pre-upgrade snapshot that lacks row lineage. | Refresh fails. To resolve it, create a new v3 snapshot by running `ALTER ICEBERG TABLE ... UPGRADE TO ICEBERG VERSION 3` from Snowflake or by running a DML operation from an external engine. |
| Re-upgrade | The table format is v3 and a new v3 snapshot exists, created by a Snowflake upgrade command or an external DML operation after the rollback. | Refresh succeeds. |

Expand

Show lessSee more
