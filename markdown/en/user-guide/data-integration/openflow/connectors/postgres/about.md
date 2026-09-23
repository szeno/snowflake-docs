# About Openflow Connector for PostgreSQL

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for PostgreSQL, its workflow, and limitations.

## About Openflow Connector for PostgreSQL

The Openflow Connector for PostgreSQL connects a PostgreSQL database instance to Snowflake and replicates data from selected tables in near real-time or on a schedule.
The connector also creates a log of all data changes, available along with the current state of the replicated tables.

## Use cases

Use this connector if you’re looking to do the following:

- CDC replication of PostgreSQL data to Snowflake for comprehensive, centralized reporting.

## Supported PostgreSQL versions

The following are the supported PostgreSQL versions.

**Supported PostgreSQL versions**

|  | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Standard](https://www.postgresql.org/) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| [AWS RDS](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/Welcome.html) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| [Amazon Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraPostgreSQLReleaseNotes/Welcome.html) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| [GCP Cloud SQL](https://cloud.google.com/sql/docs/postgres/) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| [Azure Database](https://learn.microsoft.com/en-us/azure/postgresql/) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

Expand

Show lessSee more

## Openflow requirements

- Choose the runtime size based on the sustained replication workload. For sizing guidance and how to run multiple connectors on one runtime, see [Runtime sizing](/user-guide/data-integration/openflow/connectors/cdc-runtime-sizing).
- The connector doesn’t support multi-node Openflow runtimes. Configure the runtime for this connector with **Min nodes** and **Max nodes** set to `1`.

## Limitations

- The connector supports PostgreSQL version 11 or later.
- The connector supports only username and password authentication with PostgreSQL.
- The connector doesn’t replicate tables with data that exceeds [Snowflake’s type limitations](/sql-reference/intro-summary-data-types).
  An exception to this rule is date and time data type columns that contain out-of-range values. For more information, see [Out of range value support](#label-supported-pg-date-time-data-type-value).
- The connector requires every replicated table to have a supported identity key
  configuration: either a primary key with replica identity `DEFAULT`, a unique
  index with replica identity `USING INDEX` (see
  [Configure replica identity for tables without a primary key](/user-guide/data-integration/openflow/connectors/postgres/setup#label-postgres-configure-replica-identity-using-index)), or a
  user-declared logical key with `REPLICA IDENTITY FULL`. Tables with no
  supported identity key configuration can replicate INSERT operations only.
  UPDATE and DELETE require an identity key. For more information, see
  [Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/postgres/setup#label-postgres-logical-key).
- The connector supports common source table schema changes during replication, such as adding, dropping, and renaming columns. See [Schema changes](#label-database-schema-changes) for the full list and a few unsupported change types.
- When using incremental replication without snapshots, if a row was inserted before incremental replication started, any subsequent update to that row will produce a destination row with missing values in VARCHAR, VARIANT, BINARY, and ARRAY columns.
- The connector doesn’t support the truncate table operation. `TRUNCATE` statements on the source are ignored, and the corresponding row deletions are not applied to the destination table.

Note

Limitations affecting certain table columns can be bypassed by excluding these specific columns from replication.

## Workflow

1. A **Database administrator** configures PostgreSQL replication settings, creates a
   publication, and credentials for the connector. Optionally, they deliver the SSL certificate.
2. An **Openflow administrator** creates a warehouse for the connector and a destination database
   to replicate into.
3. An **Openflow administrator** or a **data engineer** performs the following tasks:

   1. Installs the connector.
   2. Specifies the required parameters for the flow template.
   3. Runs the flow. The connector performs the following tasks when run in Openflow:
      1. Creates a schema for journal tables.
      2. Creates the schemas and destination tables matching the source tables configured for replication.
      3. Starts replication following the table replication lifecycle.

## How the connector works

The following sections describe how the connector works in various scenarios, including replication, changes in schema, and data retention.

### Data replication

The name of the destination schema is determined by the `Destination Schema Pattern` parameter. For more information, see [PostgreSQL Destination Parameters](/user-guide/data-integration/openflow/connectors/postgres/setup#label-of-postgres-destination-parameters). By default, the destination schema name matches the source schema name, so the fully qualified name of a destination table is:

`<destination_database>.<source_schema_name>.<source_table_name>`

### How tables are replicated

The tables are replicated in the following stages:

1. Schema introspection: The connector discovers the columns in the source table, their names, and types,
   and then validates them against Snowflake’s and the connector’s limitations. Validation failures cause
   this stage to fail, and the cycle completes. After successful completion of Schema Introspection, the connector creates an empty destination table.
2. Snapshot load: The connector copies all data available in the
   source table into the destination table. Failure of this stage finishes the cycle, and
   no more data is replicated. After successful completion, the whole set of data from the source table is available in the destination table.
3. Incremental load: The connector keeps tracking
   changes in the source table and copying them into the destination table.
   This continues until the table is removed from replication. Failure at this stage
   permanently stops replication of the source table until the issue is resolved.

   Note

   This connector can be configured to immediately start replicating incremental changes for newly added tables,
   bypassing the snapshot load phase. This option is often useful when reinstalling the connector
   in an account where previously replicated data exists and you want to continue replication without having to re-snapshot tables.

   For details on bypassing the snapshot load and using the incremental load process, see [Incremental replication](/user-guide/data-integration/openflow/connectors/postgres/incremental-replication).

Important

Interim failures, such as connection errors, do not prevent tables from being replicated.
Permanent failures, such as unsupported data types, do prevent tables from being replicated.
If a permanent failure prevents a table from being replicated, remove the table from the list of replicated tables.
After you address the problem that caused the failure, you can add the table back to the list of replicated tables.

### Schema changes

During incremental replication, the connector may detect source table schema changes and update the destination table automatically. Unsupported changes stop replication for the affected table until you restart it.

#### Supported changes

The connector supports the following schema changes:

- **Add column.** The connector adds the column to the destination table and replicates values for new and updated rows. Existing rows aren’t backfilled; the new column is NULL for rows that existed before the change.
- **Drop column.** The connector renames the destination column with a `__SNOWFLAKE_DELETED` suffix to preserve historical values. For details, see [Dropped columns](#dropped-columns).
- **Rename column.** The connector treats a rename as dropping the original column and adding a new one. The connector retains the original column under a suffixed name; for example, a column named `A` becomes `A__SNOWFLAKE_DELETED`. For query patterns, see [Renamed columns](#renamed-columns).
- **Compatible type change.** The connector keeps replication running with the destination column type unchanged when you change a column to a source type that maps to the same Snowflake data type (for example, `INT` to `BIGINT`, both mapped to `NUMBER`).
- **Re-add a previously dropped column.** The connector adds the column as a new destination column alongside the existing soft-deleted column (for example, `A` and `A__SNOWFLAKE_DELETED`).
- **Primary key definition change.** The connector supports adding or removing primary key columns, or changing which columns form the primary key, as long as the table still has a valid replication key after the change. If you drop the primary key and no other valid replication key remains (for example, a qualifying unique index or a configured logical key), replication for the affected table fails and the table is marked `FAILED`.

If you drop a column that was previously dropped and soft-deleted, replication for the affected table fails because the soft-deleted column name is already taken.

#### Unsupported changes

The connector doesn’t support the following schema changes. When one occurs, replication stops for the affected table:

- **Incompatible type change.** When the new source type maps to a different Snowflake data type (for example, `INT` to `VARCHAR`, mapped to `NUMBER` and `TEXT` respectively).
- **Numeric precision or scale change.** For example, changing `NUMERIC(7,2)` to `NUMERIC(6,3)`.
- **Character column length change.** For example, changing `VARCHAR(50)` to `VARCHAR(100)`.

To recover, restart replication for the affected table: see [Restart table replication](/user-guide/data-integration/openflow/connectors/postgres/maintenance#label-of-postgres-restart-table-replication).

The same soft-delete mechanism applies when you change a table’s Column Filter JSON. For details, see [Replicate a subset of columns in a table](/user-guide/data-integration/openflow/connectors/postgres/setup#label-postgres-connector-replication-subset-of-columns).

### Replicate tables from a PostgreSQL replica server

The connector can ingest data from a primary server, a [hot standby replica](https://www.postgresql.org/docs/current/hot-standby.html),
or subscriber server using [logical replication](https://www.postgresql.org/docs/current/logical-replication.html).
Before configuring the connector to connect to a PostgreSQL replica, ensure that replication between primary and replica
nodes works correctly. When investigating issues with missing data in the connector, first ensure that missing rows are
present in the replica server used by the connector.

Additional considerations when connecting to a standby replica:

> - PostgreSQL version of the server must be >= 16. Amazon Aurora is not supported because it [doesn’t offer logical decoding from read replicas](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Replication.Logical.html).
> - Only connecting to a hot standby replica is supported. Note that warm standby replicas can’t accept connections
>   from clients until they are promoted to a primary instance.
> - [The publication](/user-guide/data-integration/openflow/connectors/postgres/setup#label-postgres-connector-create-a-publication) needed by the connector must be created on
>   the primary server, not the standby server. The standby server is read-only and doesn’t let you create a publication.

If you connect to a hot standby instance and see
**Trying to create the replication slot ‘<replication slot>’ timed out. If connecting to a standby instance, ensure there is some traffic on the primary PostgreSQL instance, otherwise the call to create a replication slot will never return.**
error in the Openflow bulletin, or the **Read PostgreSQL CDC Stream** processor isn’t starting, log in to the primary PostgreSQL instance and
execute the following query:

Copy code

```
SELECT pg_log_standby_snapshot();
```

The error occurs when there are no data changes in the primary server. As such, the connector can stall while
creating a replication slot on the replica server. This results from the replica server requiring information about
running transactions from the primary server to be able to create a replication slot. Primary servers won’t send the
information while idle. The `pg_log_standby_snapshot()` function forces the primary server to send information
about running transactions to the replica server.

On PostgreSQL 17 and later, if you want the replication slot to survive a primary failover, the connector must connect to the primary rather than a standby. See [PostgreSQL 17+ failover slot support](/user-guide/data-integration/openflow/connectors/postgres/failover).

### Track data changes in tables

The connector replicates not only the current state of data from the source tables, but also every
state of every row from every changeset. This data is stored in journal tables created in the same
schema as the destination table.

The journal table names are formatted as `<source_table_name>_JOURNAL_<timestamp>_<schema_generation>`,
where `<timestamp>` is the value of epoch seconds when the source table was added to replication, and
`<schema_generation>` is an integer increasing with every schema change on the source table. As a
result, source tables that undergo schema changes will have multiple journal tables.

When a table is removed from replication, then added back, the `<timestamp>` value will change, and
`<schema_generation>` will start again from `1`.

Important

Snowflake recommends that you don’t alter the structure of journal tables in any way. They are used
by the connector to update the destination table as part of the replication process.

### How the connector chooses a replication key

The connector uses one column or set of columns from each source table as the
replication key. The replication key uniquely identifies a row and drives the
MERGE operation that applies CDC changes to the destination.

For each table, the connector resolves the replication key in this order:

1. **User-declared logical key.** If the connector is configured with a Table
   Key Configuration Service that lists the table, the connector uses those
   columns as the replication key, overriding any primary key or unique index on
   the table. For more information, see [Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/postgres/setup#label-postgres-logical-key).
2. **Primary key.** The columns of the table’s primary key constraint when
   `REPLICA IDENTITY` is `DEFAULT` (the PostgreSQL default for tables with a
   primary key).
3. **Unique index.** If the table has no primary key, the connector uses the
   unique index designated with `REPLICA IDENTITY USING INDEX`. For setup
   instructions and index requirements, see
   [Configure replica identity for tables without a primary key](/user-guide/data-integration/openflow/connectors/postgres/setup#label-postgres-configure-replica-identity-using-index).
4. **None.** If no qualifying key is found, the connector can replicate INSERT
   operations only. UPDATE and DELETE require an identity key. To enable full
   CDC for the table, add a primary key, configure `REPLICA IDENTITY USING INDEX` on a qualifying unique index, or declare a logical key.

The following examples illustrate each replication key scenario:

A table with a primary key (no special setup required):

Copy code

```
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    customer_id INT,
    total NUMERIC(10, 2)
);
```

The connector uses `order_id` as the replication key.

A table without a primary key, replicated using a unique index:

Copy code

```
CREATE TABLE sessions (
    session_token VARCHAR(64) NOT NULL,
    user_id INT,
    created_at TIMESTAMPTZ
);

CREATE UNIQUE INDEX idx_sessions_token ON sessions (session_token);
ALTER TABLE sessions REPLICA IDENTITY USING INDEX idx_sessions_token;
```

The connector uses `session_token` as the replication key.

A table without a primary key or qualifying index, replicated using a logical key:

Copy code

```
CREATE TABLE audit_events (
    event_id UUID NOT NULL,
    event_type TEXT,
    payload JSONB
);

ALTER TABLE audit_events REPLICA IDENTITY FULL;
```

Configure a logical key on `event_id` in the Table Key Configuration JSON.
For setup instructions, see [Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/postgres/setup#label-postgres-logical-key).

### Changes to a replication key value

When a source update changes the replication key value of an existing row, the
connector can’t update the destination row in place because the row’s identity
changes. Instead, it splits the source update into two operations on the
destination table:

1. The destination row keyed by the **old** value is soft-deleted: its
   `_SNOWFLAKE_DELETED` metadata column is set to `TRUE`.
2. A new destination row is inserted keyed by the **new** value, with the
   updated payload and `_SNOWFLAKE_DELETED` set to `FALSE`.

The destination table therefore contains two rows after the change: the
original row, soft-deleted, and a new row under the new key value. To query only
current rows, filter on `_SNOWFLAKE_DELETED = FALSE`.

This behavior applies when the replication key is a primary key, an
auto-detected unique index, or a user-declared logical key.

### Oversized values

By default, the connector replicates individual values up to **16 MB**. When the connector encounters a larger value, it marks the associated table as permanently failed and stops replicating it. To change how the connector handles oversized values (for example, to replace them with `NULL` instead), modify the **Oversized Value Strategy** destination parameter.

If your Snowflake account has the `ENABLE_OPENFLOW_CDC_POSTGRES_SSV2` parameter set to `true`, the per-value limit can be raised from 16 MB to **128 MB**.

For details and instructions on enabling the 128 MB per-value limit, see [Increase the oversized value limit](/user-guide/data-integration/openflow/connectors/postgres/maintenance#label-of-postgres-increase-oversized-value-limit).

### Error handling for invalid rows

An *invalid row* is a row that Snowflake rejects during ingestion because it can’t be written to the destination table, for example a value that can’t be converted to the destination column’s type, or a missing required column. The **Error Handling Strategy** parameter controls what the connector does when it encounters an invalid row:

- **Fail Table** (default): On the first invalid row, the connector marks the table as permanently failed and stops replicating it, preserving strict, all-or-nothing replication. After you fix the source data, resume replication as described in [Restart table replication](/user-guide/data-integration/openflow/connectors/postgres/maintenance#label-of-postgres-restart-table-replication).
- **Log Errors and Continue**: The connector keeps replicating the valid rows and records each rejected row, together with its original payload and error details, in the table’s *error table*. The table isn’t marked as failed.

To change the strategy, set the **Error Handling Strategy** parameter. For more information, see [PostgreSQL Destination Parameters](/user-guide/data-integration/openflow/connectors/postgres/setup#label-of-postgres-destination-parameters).

#### How rejected rows are captured

The connector loads data with Snowpipe Streaming, so error logging behaves exactly as described in [Error logging in Snowpipe Streaming](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables). When you select **Log Errors and Continue**, the connector creates new destination and journal tables with the [`ERROR_LOGGING`](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables#turn-on-error-logging) property set to `TRUE`, so rejected rows are captured in a dedicated error table instead of aborting the load. The error table stores the original payload sent to Snowflake before any transformation, along with error details.

Query a table’s error table with the `ERROR_TABLE` table function:

Copy code

```
SELECT * FROM ERROR_TABLE(<destination_database>.<schema>.<table>) ORDER BY timestamp;
```

Where a rejected row lands depends on the replication stage:

- **Snapshot load**: The rejected row is written to the destination table’s error table.
- **Incremental (CDC) load**: The rejected row is written to the journal table’s error table, because CDC changes are first written to the journal table. For more information about journal tables, see [Track data changes in tables](#track-data-changes-in-tables).

The connector enables error logging only on tables that it creates after you select **Log Errors and Continue**. To capture rejected rows for tables that were already being replicated, enable error logging on their existing destination and journal tables with the stored procedure in [Enable error logging on an existing schema](/user-guide/data-integration/openflow/connectors/postgres/maintenance#label-of-postgres-enable-error-logging-existing-schema).

Note

When the connector encounters invalid rows, it emits a `WARN` log entry that includes the number of rejected rows. Use these entries to monitor rejected-row activity.

#### Consume rejected rows

To process rejected rows programmatically, create a stream on the error table and consume it like any other Snowflake stream. For more information, see [Streams on error tables](/user-guide/data-load-overview#streams-on-error-tables).

### TOASTed value support

The connector supports replicating tables with [TOAST values](https://www.postgresql.org/docs/current/storage-toast.html) for columns of types: `array`, `bytea`, `json`, `jsonb`, `text`, `varchar`, `xml`.

Whenever the connector encounters a TOASTed value in the CDC stream, it substitutes a default placeholder of `__previous_value_unchanged`, formatted for the given column type, and stores it in the journal table. The `MERGE` query then accounts for placeholder values, so that the destination table always contains the last non-TOASTed value.

### Out of range value support

The connector supports replicating tables with columns of types `date`, `timestamp`, and `timestamptz` that contain out-of-range values.
If the connector encounters an out-of-range value in the CDC stream, it substitutes a default placeholder based on the type of the column.

**Placeholder values for out-of-range values**

| Column type | Placeholder value |
| --- | --- |
| `date` | `-9999-01-01` through `9999-12-31`. |
| `timestamp` | `0001-01-01 00:00:00` through `9999-12-31 23:59:59.999999999`. |
| `timestamptz` | `0001-01-01 00:00:00+00` through `9999-12-31 23:59:59.999999999+00`. |

Expand

Show lessSee more

Note

`-Infinity` and `Infinity` values are also replaced with the respective placeholders for all three types.

# Understanding data retention

The connector follows a data retention philosophy where customer data is never automatically deleted.
You maintain full ownership and control over your replicated data, and the connector preserves historical
information rather than permanently removing it.

This approach has the following implications:

- Rows deleted from the source table are soft-deleted in the destination table rather than physically removed.
- Columns dropped from the source table are renamed in the destination table rather than dropped.
- Journal tables are retained indefinitely and are not automatically cleaned up.

## Destination table metadata columns

Each destination table includes the following metadata columns that track replication information:

| Column name | Type | Description |
| --- | --- | --- |
| `_SNOWFLAKE_INSERTED_AT` | TIMESTAMP\_NTZ | The timestamp when the row was originally inserted into the destination table. |
| `_SNOWFLAKE_UPDATED_AT` | TIMESTAMP\_NTZ | The timestamp when the row was last updated in the destination table. |
| `_SNOWFLAKE_DELETED` | BOOLEAN | Indicates whether the row was deleted from the source table. When `true`, the row has been soft-deleted and no longer exists in the source. |

Expand

Show lessSee more

## Soft-deleted rows

When a row is deleted from the source table, the connector does not physically remove it from the
destination table. Instead, the row is marked as deleted by setting the `_SNOWFLAKE_DELETED` metadata
column to `true`.

This approach allows you to:

- Retain historical data for auditing or compliance purposes.
- Query deleted records when needed.
- Decide when and how to permanently remove data based on your requirements.

To query only active (non-deleted) rows, filter on the `_SNOWFLAKE_DELETED` column:

Copy code

```
SELECT * FROM my_table WHERE _SNOWFLAKE_DELETED = FALSE;
```

To query deleted rows:

Copy code

```
SELECT * FROM my_table WHERE _SNOWFLAKE_DELETED = TRUE;
```

## Dropped columns

When a column is dropped from the source table, the connector does not drop the corresponding column
from the destination table. Instead, the column is renamed by appending the `__SNOWFLAKE_DELETED` suffix
to preserve historical values.

For example, if a column named `EMAIL` is dropped from the source table, it is renamed to
`EMAIL__SNOWFLAKE_DELETED` in the destination table. Rows that existed before the column was dropped
retain their original values, while rows added after the drop have `NULL` in this column.

You can still query historical values from the renamed column:

Copy code

```
SELECT EMAIL__SNOWFLAKE_DELETED FROM my_table;
```

## Renamed columns

Due to limitations in CDC (Change Data Capture) mechanisms, the connector cannot distinguish between
a column being renamed and a column being dropped followed by a new column being added. As a result,
when you rename a column in the source table, the connector treats this as two separate operations:
dropping the original column and adding a new column with the new name.

For example, if you rename a column from `A` to `B` in the source table, the destination table
will contain:

- `A__SNOWFLAKE_DELETED`: Contains values from before the rename. Rows added after the rename have
  `NULL` in this column.
- `B`: Contains values from after the rename. Rows that existed before the rename have `NULL`
  in this column.

### Querying renamed columns

To retrieve data from both the original and renamed columns as a single unified column, use a
`COALESCE` or `CASE` expression:

Copy code

```
SELECT
    COALESCE(B, A__SNOWFLAKE_DELETED) AS A_RENAMED_TO_B
FROM my_table;
```

Alternatively, using a `CASE` expression:

Copy code

```
SELECT
    CASE
        WHEN B IS NOT NULL THEN B
        ELSE A__SNOWFLAKE_DELETED
    END AS A_RENAMED_TO_B
FROM my_table;
```

### Creating a view for renamed columns

Rather than manually modifying the destination table, you can create a view that presents the renamed
column as a single unified column. This approach is recommended because it preserves the original data
and avoids potential issues with ongoing replication.

Copy code

```
CREATE VIEW my_table_unified AS
SELECT
    *,
    COALESCE(B, A__SNOWFLAKE_DELETED) AS A_RENAMED_TO_B
FROM my_table;
```

Important

Manually modifying the destination table structure (such as dropping or renaming columns) is not
recommended, as it may interfere with ongoing replication and cause data inconsistencies.

## Journal tables

During incremental replication, changes from the source database are first written to journal tables
before being merged into the destination tables. The connector does not automatically remove data from
journal tables, as this data may be useful for auditing, debugging, or reprocessing purposes.

Journal tables are created in the same schema as their corresponding destination tables and follow
this naming convention:

`<TABLE_NAME>_JOURNAL_<timestamp>_<number>`

Where:

- `<TABLE_NAME>` is the name of the destination table.
- `<timestamp>` is the creation timestamp in Unix epoch format (seconds since January 1, 1970),
  ensuring uniqueness.
- `<number>` starts at 1 and increments whenever the destination table schema changes, either due to
  schema changes in the source table or modifications to column filters.

For example, if your destination table is `SALES.ORDERS`, the journal table might be named
`SALES.ORDERS_JOURNAL_1705320000_1`.

Important

Do not drop journal tables while replication is in progress. Removing an active journal table may
cause data loss or replication failures. Only drop journal tables after the corresponding source
table has been fully removed from replication.

### Managing journal table storage

If you need to manage storage costs by removing old journal data, you can create a Snowflake task
that periodically cleans up journal tables for tables that are no longer being replicated.

Before implementing journal cleanup, verify that:

- The corresponding source tables have been fully removed from replication.
- You no longer need the journal data for auditing or processing purposes.

For information on creating and managing tasks for automated cleanup, see
[Introduction to tasks](/user-guide/tasks-intro).

## Next steps

Review [Openflow Connector for PostgreSQL: Data mapping](/user-guide/data-integration/openflow/connectors/postgres/data-mapping) to understand how the connector maps data types to Snowflake data types.
Review [Set up the Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/setup) to set up the connector.
