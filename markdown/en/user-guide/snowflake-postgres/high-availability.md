# Snowflake Postgres High Availability

High Availability (HA) preserves the uptime of your instance by provisioning a secondary virtual machine in a separate
availability zone that receives the same writes as your primary. When HA is enabled, in the event your primary becomes
unavailable, we will automatically fail over to the secondary host by promoting the standby to replace the impacted host. You
don’t need to update your connection details. Once the promotion occurs, the original primary is destroyed and a new standby
host is created.

For instances that are sensitive to protracted downtime, we recommend using our HA feature. Without HA, if your instance becomes
unavailable, Snowflake attempts to provision a new host for your instance, and the control plane automatically restores your
instance using the most recent automated backup and all WAL (write-ahead-log) statements that have been generated since the
latest backup. For small, inactive clusters this could be a matter of minutes, but for larger or active clusters this could take
many hours.

To turn high availability on or off for your Snowflake Postgres instance, run the [ALTER POSTGRES INSTANCE](/sql-reference/sql/alter-postgres-instance) command with the
SET HIGH\_AVAILABILITY option. The following example shows how to turn high availability on or off:

Copy code

```
ALTER POSTGRES INSTANCE production_instance SET HIGH_AVAILABILITY = TRUE;
ALTER POSTGRES INSTANCE dev_test_instance SET HIGH_AVAILABILITY = FALSE;
```

## Synchronous commit and durability

With HA enabled, Postgres streams write-ahead log (WAL) records from the primary to the HA standby through replication. The
[`synchronous_commit`](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT) setting
determines whether a commit waits for the standby before returning success.

The Snowflake Postgres default is `local`. A commit returns success after the primary writes the transaction to its local WAL.
The standby receives the WAL asynchronously. If the primary fails before the standby receives a commit, that commit can be lost
even though the client received a success response.

To make commit success depend on the standby, set `synchronous_commit` to one of the following remote modes:

| Value | What the primary waits for before returning commit success |
| --- | --- |
| `remote_write` | The standby has received the WAL (written to the standby’s OS, not necessarily flushed to disk). |
| `on` | The standby has flushed the WAL to durable storage. |
| `remote_apply` | The standby has applied the WAL so the change is visible in queries on the standby. |

Expand

Show lessSee more

Postgres uses
[`synchronous_standby_names`](https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-SYNCHRONOUS-STANDBY-NAMES)
to determine which standbys must acknowledge a commit. Snowflake Postgres manages this setting. When HA is enabled, the list
includes the HA standby, so remote modes wait on that standby. For details, see the
[Postgres documentation](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT).

Important

Most workloads should keep the default (`local`). The HA standby is in a different availability zone, so remote modes can
substantially increase write latency and reduce throughput. If the standby is slow or unavailable, commits stall until the
standby acknowledges them. Use remote modes only when a commit must not be treated as durable until the standby has it.

`synchronous_commit` can also be set for a single session with `SET` or a single transaction with `SET LOCAL`. This makes it
possible to keep the instance default and require standby acknowledgment only for specific commits, or the reverse. The
following example requires standby acknowledgment for one transaction:

Copy code

```
BEGIN;
SET LOCAL synchronous_commit = remote_apply;
-- writes that must reach the standby before commit returns
COMMIT;
```

### Synchronous commit during failover

Immediately after a failover, and while Snowflake replaces the HA standby during maintenance, no standby is available to
acknowledge commits. By default, Snowflake Postgres prioritizes availability during these periods, and commits in remote modes
return success from the primary alone. To require standby acknowledgment during these periods, use the
`strict.synchronous_commit` setting. For details, see
[Strict synchronous commit](/user-guide/snowflake-postgres/postgres-server-settings#label-snowflake-postgres-strict-synchronous-commit).
