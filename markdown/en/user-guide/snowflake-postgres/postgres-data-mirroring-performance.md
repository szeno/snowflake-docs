[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.
Currently, this feature is only available on Amazon Web Services (AWS) and Microsoft Azure.

# Postgres-to-Snowflake mirroring performance considerations

Mirroring runs alongside your transactional workload on your Snowflake Postgres instance and
continuously delivers changes to Snowflake. Understanding how mirroring interacts with your
workload helps you size your instance and configure your mirrors for optimal performance.

Performance has two distinct aspects, and this page covers them separately:

- **Resource use on your Postgres instance:** the CPU and memory that mirroring shares with your
  application workload on the source instance.
- **Mirroring pipeline performance:** how quickly existing data and ongoing changes arrive in
  your Snowflake target tables.

## How mirroring works

Mirroring has two phases:

- The **initial snapshot** copies the existing data in each mirrored table from Postgres to
  Snowflake.
- Ongoing **change data capture** (**CDC**) captures subsequent inserts, updates, and deletes
  and applies them to the target tables.

CDC runs in two decoupled stages, one on each side of the mirror:

- **Push, on your Postgres instance:** The `snowflake_cdc` extension runs a background process,
  the **CDC worker**, for each mirror. The CDC worker reads changes from a logical replication
  slot, where a Postgres walsender process decodes them from the write-ahead log (WAL). About every
  15 seconds, the CDC worker writes a batch of changes through pg\_lake to Iceberg change log tables
  (`$changes`) and records the batch in a metalog. The walsender and CDC worker run on your
  instance’s CPU and memory.
- **Apply, in Snowflake:** A Snowflake serverless task for each mirror reads the metalog and
  merges the accumulated changes from the change log tables into the target tables, at the cadence
  that you set with `refresh_interval`. The apply task runs on Snowflake compute, not on your
  Postgres instance.

For a diagram of this flow, see
[How mirroring works](/user-guide/snowflake-postgres/postgres-data-mirroring#how-mirroring-works).

With default settings, changes are visible in Snowflake within about 30 seconds through the
[`$live` view](/user-guide/snowflake-postgres/postgres-data-mirroring-query#query-at-low-latency-with-live), independent of
`refresh_interval`. The plain target tables reflect changes each time the apply task merges them.

## How mirroring uses your Postgres instance

Because the push stage runs directly on your Postgres instance, mirroring shares the instance’s CPU
and memory with your application. This design is what keeps mirroring efficient: changes are
captured where they’re written, using native Postgres logical decoding, without a separate
replication service to deploy or manage.

In practice, this means that your instance handles two kinds of work: your application’s queries and
transactions, and the decoding and batching of those changes for Snowflake. When the instance has
spare capacity, which is common for transactional workloads that don’t run at full utilization, both
kinds of work get the resources they need and mirroring runs comfortably alongside your application.
On smaller instances or on instances that already run close to full utilization, you’ll want to
account for mirroring when you plan your instance capacity. It’s always recommended to benchmark
your workload with mirroring before running it in production.

The following sections describe what shapes mirroring’s resource use on the instance. To see how
mirroring performs with your own workload, see [Benchmark your workload](#benchmark-your-workload).

### Write volume

Mirroring’s work on the instance grows with the volume of changes your application writes.
Read-only queries don’t generate changes, so they add no mirroring work. For most workloads, the
rate of inserts, updates, and deletes is the best guide to how much of the instance mirroring uses.

### Transaction size

Mirroring preserves your transactions: all the changes from a transaction arrive in Snowflake
together, after the transaction commits. To make that possible, mirroring holds each
transaction’s changes until commit.

This works smoothly for typical transactional workloads. Very large single transactions, such as a
bulk load that changes millions of rows in one statement, use more memory and disk on the instance
while mirroring processes them, and their changes appear in Snowflake only after the whole
transaction commits.

## Mirroring pipeline performance

Pipeline performance is about how quickly your data arrives in Snowflake: how long the initial
snapshot takes, and how closely your target tables track the source afterward. Because push and
apply are decoupled, each stage works at its own pace. The push stage keeps capturing changes on
your instance while the apply stage merges them in Snowflake on the schedule that you choose.

Pipeline performance depends mainly on the following factors:

- **Table count:** the most significant factor. The apply task processes schema and merge logic
  for each table with changes, so a workload spread across hundreds of tables behaves differently
  from the same number of rows in a few tables.
- **Change rate:** rows per second and bytes per second of inserts, updates, and deletes.
- **Table size and shape:** the amount and width of existing data, which drives snapshot time.
- **Transaction size and shape:** large or multi-table transactions compared with small,
  single-table changes.
- **Refresh interval:** how often the apply task merges changes into the target tables.
- **Instance resources:** the CPU, memory, and I/O available on the source instance.

### Initial snapshot

The initial snapshot is a one-time bulk copy that gives each target table its starting data. After
it completes, CDC takes over and applies only the changes. Because a snapshot reads a large
volume of data at once, it has a different performance profile from ongoing CDC.

Snapshot duration depends primarily on the amount and shape of existing data, the read and I/O
capacity of the source instance, and concurrent activity on the source. Creating or recreating a
mirror snapshots every table in the mirrored schemas.

### Refresh interval

The refresh interval gives you direct control over how your target tables balance freshness and
cost. Each apply run merges all changes that have accumulated since the previous run, so the
interval determines both how current the target tables are and how much work each run does:

- A shorter interval keeps the target tables more current, with more frequent, smaller apply runs.
- A longer interval combines more changes into each apply run, which lowers cost.

For low-latency reads with a longer interval, query the `$live` view, which shows recent changes
on top of the target table before they’re merged. The apply task checks for work at least every
two minutes, so schema changes are applied promptly regardless of the interval.

## Best practices

Mirroring works well with default settings for many workloads. As your data volume, table count,
or freshness requirements grow, the following practices help you get the best performance from
both your Postgres instance and the mirroring pipeline.

### Benchmark before production

Benchmark a representative workload on an instance of the size that you plan to use in
production, and use the results as a baseline for monitoring. For more information, see
[Benchmark your workload](#benchmark-your-workload).

### Size the Postgres instance for your workload plus mirroring

When you choose an instance size, you’re choosing capacity for everything the instance does. With
mirroring, that includes capturing your changes for Snowflake as well as serving your application.
Planning for both from the start gives your application the headroom it needs and keeps your
mirrored data current, even during peak write activity.

A STANDARD\_XL instance handles most mirroring workloads well and is a good starting point.
Snowflake recommends at least one core per mirror. As your workload grows, scale the instance up:
larger instances provide more cores and memory, which increase the throughput available to both
your application and mirroring.

For more information, see
[Sizing your instance](/user-guide/snowflake-postgres/postgres-data-mirroring-create#sizing-your-instance).

### Group tables into multiple mirrors

For best throughput, group tables into multiple mirrors rather than creating one large mirror
with many tables. In particular, limit the number of frequently changed tables in each mirror.

### Keep staging tables out of mirrors

Tables that are frequently dropped and re-created, such as staging tables, add work to the CDC
pipeline without providing useful mirrored data. Keep these tables in a schema that isn’t part of
a mirror.

### Choose a refresh interval for your freshness target

Set `refresh_interval` based on how current the target tables need to be. If readers need recent
changes but you want to keep apply costs low, use a longer interval and query the `$live` view.

### Keep transactions a manageable size

For bulk loads and bulk updates, split the work into multiple smaller transactions rather than
issuing one very large statement.

## Benchmark your workload

Every workload is different: the mix of tables, change rates, and transaction shapes that matters
for one application can look very different for another. Because mirroring performance depends on
these details, the most reliable way to set expectations is to benchmark a representative workload
on an instance of the size that you plan to use in production.

A benchmark shows you what normal looks like for your workload, confirms that your instance size
and mirror configuration meet your goals, and gives you a baseline to compare against when you
monitor mirrors in production.

Measure the initial snapshot and ongoing CDC separately. After the snapshot completes, wait until
all mirrored tables are healthy and CDC has caught up before you measure CDC.

### Record pipeline metrics

Record the following information for each run:

| Metric | Why it matters |
| --- | --- |
| Source data size and table count | Drive snapshot duration and apply work. |
| Change rate (rows/second, bytes/second) | Determines the CDC workload. |
| Refresh interval | Affects freshness and apply cost; results aren’t comparable without it. |
| Run duration | Shows whether the result reflects sustained behavior. |
| Lag over time | Shows whether lag stays steady or trends upward. |
| WAL and replication-slot headroom | Shows the capacity remaining on the source instance. |
| Catch-up after load stops | Confirms that the mirror drains any backlog. |

Expand

Show lessSee more

Tip

Run each benchmark for several refresh intervals, and look at the lag trend rather than a single
reading. A short run can look steady before lag begins to grow, and a source-side bottleneck, such
as lock contention or client scheduling, can limit throughput even when mirroring is healthy.

### Measure snapshot performance

To measure snapshot duration, query the task history for the first `APPLY_MIRROR` run for each
mirror. Querying task history requires the ACCOUNTADMIN role.

Copy code

```
SELECT
    name,
    state,
    scheduled_time,
    completed_time,
    DATEDIFF('second', query_start_time, completed_time) AS duration_seconds,
    ROUND(DATEDIFF('second', query_start_time, completed_time) / 60.0, 1) AS duration_minutes
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
    RESULT_LIMIT => 1000
))
WHERE name LIKE 'APPLY_MIRROR_%'
QUALIFY ROW_NUMBER() OVER (PARTITION BY name ORDER BY scheduled_time ASC) = 1
ORDER BY name;
```

## Monitor CDC performance

After your mirrors are running, monitoring lets you confirm that they’re keeping pace with your
workload and spot changes early, before they affect the freshness of your data. Compare what you
see against the baseline from your benchmarks.

Because push and apply are decoupled, each stage can keep up independently of the other. For
example, the push stage can be fully caught up while the apply stage is still merging a large
batch. Monitor each stage separately to see where any lag comes from.

### Push lag

Push lag measures how far the CDC worker on your Postgres instance is behind the source. To check
it from Snowflake, call the `DESCRIBE_MIRROR` procedure. The `postgres_status` column is read live
from the source, so you don’t need a separate connection to the Postgres instance.

Copy code

```
CALL SNOWFLAKE.POSTGRES.DESCRIBE_MIRROR('my_mirror');
```

In `postgres_status`, `cdc_flush_lag_seconds` shows push lag in seconds and `slot_lag_bytes`
shows it in WAL bytes. While the worker keeps up, `cdc_flush_lag_seconds` stays within one push
interval.

To check push lag from the source Postgres instance, query the `snowflake_cdc.publication_health`
view, which also includes the worker PID, error details, and per-table snapshot state:

Copy code

```
SELECT publication_name, status, slot_lag_bytes
FROM snowflake_cdc.publication_health;
```

### Apply lag

Apply lag measures how far the target tables are behind the changes that the source has pushed.
`DESCRIBE_MIRROR` reports it in `apply_lag_seconds`, `apply_lag_operations`, and
`apply_lag_bytes`. Each value is `0` when the mirror is caught up. The `recent_query_durations`
and `status` columns show recent apply runs.

For the full history of apply runs, query `INFORMATION_SCHEMA.TASK_HISTORY` for tasks named
`APPLY_MIRROR_%`.

### End-to-end lag

For the total time between a source commit and the change appearing in the target tables, add
`postgres_status:cdc_flush_lag_seconds` and `apply_lag_seconds`.

For more information about monitoring and alerting, see
[Monitor mirroring](/user-guide/snowflake-postgres/postgres-data-mirroring-manage#monitor-mirroring)
and
[Alert on mirror health](/user-guide/snowflake-postgres/postgres-data-mirroring-manage#alert-on-mirror-health).
