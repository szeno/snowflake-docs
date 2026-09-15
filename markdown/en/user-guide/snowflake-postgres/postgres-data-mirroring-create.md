[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.
Currently, this feature is only available on Amazon Web Services (AWS) and Microsoft Azure.

# Create a mirror

Follow these steps to create a mirror from Snowflake Postgres to a Snowflake analytics database.

## Step 1: Prepare your Postgres instance

Mirroring requires the latest Postgres extensions on the source instance. Follow the path that
applies to you.

### Create a new instance

Create a new Snowflake Postgres instance from Snowsight or SQL. See
[Create a Snowflake Postgres instance](/user-guide/snowflake-postgres/postgres-create-instance)
for detailed instructions. New instances include the required extensions automatically, so no
refresh is needed.

### Refresh an existing instance

If you have an existing instance that was created before the mirroring feature was available,
refresh the instance from the Postgres **Manage** options in Snowsight before creating a mirror.
Refreshing picks up the latest Snowflake Postgres software patch, which is required for
mirroring.

### Sizing your instance

Size your Postgres instance for your workload plus mirroring. Mirroring continuously
captures changes and temporarily retains them until they’re copied out. This uses some
additional compute and storage alongside your normal traffic. On smaller instances this
matters most, so for sustained high write throughput use STANDARD\_L or larger with extra
disk (for example, >250 GB) to absorb load spikes without the mirror falling behind.

Disk size also affects write-ahead log (WAL) retention: `max_slot_wal_keep_size` defaults to one-tenth of the
allocated disk. If apply lag causes the WAL backlog to exceed that limit, Postgres invalidates
the replication slot and mirroring automatically re-snapshots all tables after 10 minutes. See
[Mirror re-snapshots all tables after a WAL-lag spike](/user-guide/snowflake-postgres/postgres-data-mirroring-manage#mirror-re-snapshots-all-tables-after-a-wal-lag-spike)
for details.

Note

The BURSTABLE tier isn’t supported for mirroring. Use STANDARD or HIGH MEMORY.

### Replication slot limit

Each mirror uses one PostgreSQL replication slot. The default `max_replication_slots` is 10,
which limits the total number of mirrors (and any other logical replication subscribers) on a
single instance. If you plan to run many mirrors, see
[CREATE MIRROR fails if max\_replication\_slots is too low](/user-guide/snowflake-postgres/postgres-data-mirroring-troubleshooting#label-replication-slot-limit)
for how to increase the limit before you reach it.

### Source table requirements

To be mirrored, a source table must meet these requirements:

- **Ordinary table or partitioned table.** Views, materialized views, foreign tables, sequences,
  and other relation kinds aren’t replicable. Temporary tables are never replicated because Postgres logical replication excludes them.
- **Logged (not UNLOGGED).** Unlogged tables generate no WAL and can’t participate in logical
  replication.
- **Not owned by an extension.** Extension-owned tables (including the CDC metalog itself) are
  filtered out.
- **No virtual generated columns.** Tables containing virtual generated columns can’t be
  mirrored. `create_mirror` fails with an error:

  Copy code

  ```
  Error from Postgres: ERROR: snowflake_cdc: table <schema>.<table> cannot be replicated: virtual generated column "<column>" (SQLSTATE 0A000).
  ```
- **No ANSI-reserved column names.** Tables containing columns whose names are ANSI-reserved
  keywords are rejected at publication time.
- **No nested UUID.** `uuid` is supported as a standalone column but is rejected at publication
  time when nested inside an array or composite type (for example, `uuid[]` or a composite
  with a `uuid` field). See [Nested type handling](/user-guide/snowflake-postgres/postgres-data-mirroring-type-mapping#nested-type-handling)
  for details.
- **Unique table names.** The case-insensitive `schema.table` must be unique
  among mirrored tables, and the table name can’t end in `$changes` or `$live` (reserved for
  companion objects).

#### Primary key and UPDATE/DELETE support

Tables without a primary key are mirrored as **insert-only**: the CDC extension sets
`REPLICA IDENTITY NOTHING` on them, which causes Postgres to reject `UPDATE` and `DELETE` on the
source. Add a primary key before mirroring if the table needs to support `UPDATE` or `DELETE`.

## Step 2: Grant permissions (SQL only)

If you’re creating a mirror using the Snowflake UI, skip this step — the UI grants these
permissions automatically. If you’re using SQL, grant the `postgres_mirror_admin` application
role to the role that will manage mirrors, and grant `USAGE` on the Postgres instance to the
`snowflake` application:

Copy code

```
GRANT APPLICATION ROLE snowflake.postgres_mirror_admin TO ROLE "my_role";
GRANT USAGE ON POSTGRES INSTANCE "my_instance" TO APPLICATION snowflake;
```

Replace `"my_instance"` with the name of your Postgres instance,
and replace `"my_role"` with the name of the role that will manage mirrors.

Caution

Don’t revoke USAGE from the snowflake application, because doing so breaks active mirrors.

## Step 3: Create the mirror

You can create a mirror using SQL or the Snowflake UI.

**Using SQL:**

Use the `snowflake.postgres.create_mirror` procedure to specify which Postgres tables to replicate
and how often to sync:

Copy code

```
CALL SNOWFLAKE.POSTGRES.CREATE_MIRROR(
    mirror_name         => 'orders_mirror',
    postgres_instance   => 'mirror-test-sql',
    postgres_database   => 'postgres',
    target_database     => 'POSTGRESMIRRORTOSNOWFLAKE',
    postgres_tables     => ['public.devices', 'public.sensors', 'public.readings'],
    postgres_schemas    => NULL,
    refresh_interval    => '1 minute'
);
```

You must specify either `postgres_tables` or `postgres_schemas`, but not both. The
`refresh_interval` defaults to `'10 minutes'` and accepts values like `'30 seconds'`, `'1 minute'`,
`'1 hour'`, or `'1 day'` (maximum). For full parameter details, see
[create\_mirror](/user-guide/snowflake-postgres/postgres-data-mirroring-reference#label-mirror-management-procedures).

By default, `CREATE_MIRROR` creates standard Snowflake tables as the target. To mirror into
Snowflake-managed Iceberg tables instead, add `target_table_type => 'ICEBERG'`:

Copy code

```
CALL SNOWFLAKE.POSTGRES.CREATE_MIRROR(
    mirror_name         => 'orders_mirror',
    postgres_instance   => 'mirror-test-sql',
    postgres_database   => 'postgres',
    target_database     => 'POSTGRESMIRRORTOSNOWFLAKE',
    postgres_tables     => ['public.devices', 'public.sensors', 'public.readings'],
    postgres_schemas    => NULL,
    refresh_interval    => '1 minute',
    target_table_type   => 'ICEBERG'
);
```

Iceberg target tables use Snowflake-managed storage. External catalogs and external storage are
not supported.

**Using the Snowflake UI:**

Navigate to your Postgres instance in Snowsight and select **Manage** to configure mirroring.
Enter a mirror name, select the source database, provide a destination database name, and set the
refresh frequency.

![Mirror data dialog in Snowsight showing fields for mirror name, source database, destination database, and refresh frequency](/static/images/snowflake-postgres/postgres-mirror-creation-screen.png)

Important

The target database must not already exist. The mirror creates it automatically. You can’t reuse a
target database that was previously used by a mirror, even if that mirror was dropped.

## Step 4: Verify data in Snowflake

Once the mirror is created and the initial sync completes, verify that the data has arrived in
Snowflake:

Copy code

```
SELECT COUNT(*) FROM POSTGRESMIRRORTOSNOWFLAKE.PUBLIC.READINGS;
```

The count should match the source table in Postgres. You can also check the `$live` view, which
includes any changes that haven’t been merged yet:

Copy code

```
SELECT COUNT(*) FROM POSTGRESMIRRORTOSNOWFLAKE.PUBLIC.READINGS$live;
```

Use `list_mirrored_tables` to check the replication state of each table. Tables show as
`SNAPSHOTTING` during the initial copy and `REPLICATING` once caught up:

Copy code

```
CALL SNOWFLAKE.POSTGRES.LIST_MIRRORED_TABLES('orders_mirror');
```

From this point on, any inserts, updates, or deletes in Postgres automatically replicate to
Snowflake on the configured refresh interval. A **Mirroring** tab on the Postgres landing page in
Snowsight shows your existing mirrors. This tab may take a few minutes to populate after your
first mirror creation.

## Next steps

For a richer end-to-end walkthrough with example data, see the
[Snowflake Postgres mirroring quickstart](https://www.snowflake.com/en/developers/guides/snowflake-postgres-mirror-to-snowflake).

## Cloud and region availability

Note

Mirroring is currently available only on Amazon Web Services (AWS) and Microsoft Azure. Mirrors can’t be created between different accounts, regions, or cloud providers.
