[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.
Currently, this feature is only available on Amazon Web Services (AWS) and Microsoft Azure.

# Troubleshoot mirrors

The following are known issues and limitations, with workarounds.

### Postgres instance needs to be refreshed

[`create_mirror`](/user-guide/snowflake-postgres/postgres-data-mirroring-reference#create_mirror-parameters) can fail on an existing Postgres instance with an error similar to:

Copy code

```
Error from Postgres: ERROR: permission denied to create extension
```

This happens when the source instance predates the mirroring feature and doesn’t have the
Postgres extensions that mirroring depends on.

**Solution:** [Refresh the instance](/user-guide/snowflake-postgres/managing-instances#refresh) from the Postgres **Manage** options in Snowsight to install
the latest extensions, then retry `create_mirror`. See
[prepare your Postgres instance](/user-guide/snowflake-postgres/postgres-data-mirroring-create#step-1-prepare-your-postgres-instance)
for details.

### Mirror names are folded to lowercase

Mirror names containing uppercase letters are folded to lowercase.

Copy code

```
CREATE_MIRROR(mirror_name => 'UpperMirror', ...)
```

This call will succeed, but will silently fold the mirror name to `uppermirror`.

**Solution:** Prefer lowercase characters in mirror names. For example, use `mymirror` instead
of `MyMirror`.

### Target database names can’t be reused

After a database has been used as a mirror target, the same name can’t be reused for a new mirror,
even if the mirror is dropped and the database itself is dropped.

**Solution:** Pick a new `target_database` name when creating a replacement mirror.

### Active mirrors break if usage is revoked from the snowflake application

Apply runs will fail with error `POSTGRES INSTANCE ... does not exist or not authorized` if
the `USAGE` grant on the Postgres instance has been revoked from the `snowflake` application.
This can happen in two ways (see [Roles and permissions](/user-guide/snowflake-postgres/postgres-data-mirroring-manage#roles-and-permissions)):

- **Explicit revoke:** `REVOKE USAGE ON POSTGRES INSTANCE ... FROM APPLICATION SNOWFLAKE`
- **Ownership transfer with `REVOKE CURRENT GRANTS`:** Running
  `GRANT OWNERSHIP ON POSTGRES INSTANCE ... TO ROLE ... REVOKE CURRENT GRANTS` drops all
  existing grants on the instance, including the `USAGE` grant that mirroring depends on.

**Solution:** Re-grant the privilege:

Copy code

```
GRANT USAGE ON POSTGRES INSTANCE "my_instance" TO APPLICATION SNOWFLAKE;
```

### Changing a column type on a mirrored table fails

`ALTER TABLE ... ALTER COLUMN ... TYPE` is not supported on tables tracked by a mirror (see
[DDL updates in $changes](/user-guide/snowflake-postgres/postgres-data-mirroring-query#ddl-updates-in-changes)). Postgres rejects the statement with an error:

Copy code

```
ERROR:  cannot alter column type on table "<table_name>"
DETAIL:  Table is tracked by snowflake_cdc publication "<mirror_name>".
```

**Solution:** Build a new column in Postgres and migrate that data to the new type, instead of changing the column type.

### Adding a virtual generated column to a mirrored table fails

`ALTER TABLE ... ADD COLUMN ... GENERATED ALWAYS AS ...` is not supported on tables tracked by a
mirror (see [DDL updates in $changes](/user-guide/snowflake-postgres/postgres-data-mirroring-query#ddl-updates-in-changes)). Postgres rejects the statement with an error:

Copy code

```
ERROR:  cannot add generated column on table "<table_name>"
DETAIL:  Table "<table_name>" is tracked by a snowflake_cdc publication. ALTER TABLE ADD COLUMN does not populate generated columns on the mirror via WAL, so the mirror would diverge from the source.
```

**Solution:** To use a computed value alongside a mirrored table, create the equivalent expression as a view in
Snowflake against the target table rather than as a generated column in Postgres.

### CREATE MIRROR fails if max\_replication\_slots is too low

Each mirror uses one PostgreSQL replication slot. When the instance is close to the
[`max_replication_slots`](/user-guide/snowflake-postgres/postgres-server-settings) limit, which defaults to 10, `CREATE MIRROR` fails with:

Copy code

```
snowflake_cdc: cannot create publication "<mirror_name>" because the cluster is close to max_replication_slots
```

**Solution:** Increase `max_replication_slots` and `max_wal_senders` together (the latter should
be set to at least the same value) using
[server settings](/user-guide/snowflake-postgres/postgres-server-settings), then restart the instance:

Copy code

```
ALTER POSTGRES INSTANCE "my_instance"
    SET POSTGRES_SETTINGS = (
        'max_replication_slots' = '20',
        'max_wal_senders' = '20'
    );
```

### Mirroring setup fails on newly created Snowflake accounts

On newly created Snowflake accounts, the `snowflake` application might not be fully provisioned
immediately. Attempting to grant the
[`postgres_mirror_admin` role](/user-guide/snowflake-postgres/postgres-data-mirroring-manage#roles-and-permissions)
too soon fails with:

Copy code

```
SQL compilation error: Application role 'SNOWFLAKE.POSTGRES_MIRROR_ADMIN' does not exist or not authorized.
```

**Solution:** Wait up to one hour after account creation before setting up mirroring.

### Dropping the source Postgres database fails while mirrors are active

Postgres blocks dropping a database that has active `snowflake_cdc` replication slots:

Copy code

```
ERROR:  cannot drop database "<database_name>" because it has snowflake_cdc replication slots
HINT:  Drop the snowflake_cdc mirrors and publications in database "<database_name>" first.
```

**Solution:** Drop all mirrors on the database using [`drop_mirror`](/user-guide/snowflake-postgres/postgres-data-mirroring-manage#drop-a-mirror), then drop the database.

### Renaming the source database causes mirrors to fail

Renaming the source Postgres database on a mirrored instance is not supported. Doing
so will cause existing mirrors to fail.

**Solution:** If you need to rename the database, drop existing mirrors first,
rename the database, then create new mirrors.

### Mirror re-snapshots all tables after a WAL-lag spike

If the Snowflake apply procedure falls behind and the write-ahead log (WAL) backlog grows beyond
[`max_slot_wal_keep_size`](/user-guide/snowflake-postgres/postgres-server-settings), Postgres invalidates the replication slot to prevent the instance
disk from filling. Mirroring detects the invalidated slot and automatically re-snapshots all
tables 10 minutes later.

Symptoms:

- All mirrored tables revert to `SNAPSHOTTING` status without an explicit [`RESTART_MIRROR`](/user-guide/snowflake-postgres/postgres-data-mirroring-reference#label-mirror-management-procedures) call.
- The [`$changes` feed](/user-guide/snowflake-postgres/postgres-data-mirroring-query#query-changes-with-the-changes-table) is rebuilt from a fresh snapshot baseline, losing incremental change history.

**Solutions:**

- **Increase disk size.** `max_slot_wal_keep_size` defaults to one-tenth of the allocated disk.
  A larger disk raises the effective WAL retention limit without changing any parameter. See
  [Modify an instance](/user-guide/snowflake-postgres/managing-instances#label-sfpg-modify).
- **Increase `max_slot_wal_keep_size` directly.** Adjust the value using
  [server settings](/user-guide/snowflake-postgres/postgres-server-settings). Set it high enough
  to cover the longest expected apply lag for your workload.

## Alert debugging

### Alert doesn’t fire

The following conditions look correct but never match and therefore fail silently:

- **The owning role doesn’t own any Postgres instance**, so `list_mirrors` returns nothing.
- **`status` was `NULL` and the predicate used `<> 'ACTIVE'`** — `NULL <> 'ACTIVE'` evaluates
  to `NULL`, not `TRUE`.
- **`last_operation_time` was `NULL` and the predicate had only a time comparison** — without an
  `IS NULL` branch, the mirror that has been failing since creation is the one the alert can’t
  see.
- **The condition required consecutive failed task runs** — runs skipped by the failure backoff
  are recorded as successes and break the streak.
- **A `TIMESTAMP_NTZ` column was compared against `CURRENT_TIMESTAMP()`** — in a US-Pacific
  session this shifts the threshold by 420 minutes, so a 30-minute staleness test stays quiet
  for over seven hours. Use `SYSDATE()` instead.

Run the condition query on its own, as the owning role, before assuming the alert is at fault.

### Alert fires when the mirror is healthy

If the condition reads `last_apply_time` and something has called `refresh_mirror`,
the alert may fire on a healthy mirror. `refresh_mirror` sets `last_apply_time` to `NULL` on
purpose to force the next run past the refresh-interval gate, so a manual refresh makes a
healthy mirror look like it has never applied anything. Use `last_operation_time` instead.
