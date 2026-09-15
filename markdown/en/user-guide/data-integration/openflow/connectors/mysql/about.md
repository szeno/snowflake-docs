# About Openflow Connector for MySQL

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for MySQL,
its workflow, and limitations.

## About the Openflow Connector for MySQL

The Openflow Connector for MySQL connects a MySQL database instance to Snowflake and replicates data from selected tables in near real-time or on a specified schedule.
The connector also creates a log of all data changes, which is available along with the current state of the replicated tables.

The connector also supports MariaDB as a source database.

## Use cases

Use this connector if you’re looking to do the following:

- CDC replication of MySQL or MariaDB tables into Snowflake for comprehensive, centralized reporting

## Supported MySQL versions

The following table lists the tested and officially supported MySQL versions.

|  | 8.0 | 8.4 |
| --- | --- | --- |
| [Standard MySQL](https://www.mysql.com/) | Yes | Yes |
| [AWS RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html) | Yes | Yes |
| [Amazon Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraMySQLReleaseNotes/Welcome.html) | Yes, as Version 3 | Not applicable. Aurora 8.4 isn’t currently supported. |
| [GCP Cloud SQL](https://cloud.google.com/sql/mysql?hl=en) | Yes | Yes |
| [Azure Database](https://azure.microsoft.com/en-us/products/mysql/) | Yes | Yes |
| [Percona Server](https://www.percona.com/software/mysql-database/percona-server) | Yes | Yes |

Expand

Show lessSee more

## Supported MariaDB versions

The following table lists the tested and officially supported MariaDB versions.

|  | 11.4 or later |
| --- | --- |
| [Standard MariaDB](https://mariadb.org/) | Yes |
| [AWS RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MariaDB.html) | Not applicable. AWS RDS for MariaDB isn’t currently supported. |

Expand

Show lessSee more

## Openflow requirements

- Choose the runtime size based on the sustained replication workload. For sizing guidance and how to run multiple connectors on one runtime, see [Runtime sizing](/user-guide/data-integration/openflow/connectors/cdc-runtime-sizing).
- The connector doesn’t support multi-node Openflow runtimes. Configure the runtime for this connector with **Min nodes** and **Max nodes** set to `1`.

## Limitations

- The connector supports MySQL version 8 or later and MariaDB version 11.4 or later.
- The connector supports only username and password authentication with MySQL or MariaDB.
- Only database tables that have a primary key, a NOT NULL unique index, or a
  configured logical key can be replicated. When no primary key is defined,
  MySQL’s InnoDB storage engine automatically promotes the first NOT NULL unique
  index to act as the primary key, and the connector uses it as the replication
  key. For tables with neither a primary key nor a qualifying unique index, you
  can configure a logical key as the replication key. For more information, see
  [Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/mysql/setup#label-mysql-logical-key).
- The connector doesn’t replicate tables with data that exceeds
  [Snowflake’s type limitations](/sql-reference/intro-summary-data-types).
- The connector doesn’t replicate columns of types GEOMETRY, GEOMETRYCOLLECTION, LINESTRING, MULTILINESTRING, MULTIPOINT, MULTIPOLYGON, POINT, and POLYGON.
- The connector is subject to the [Group Replication limitations of MySQL](https://dev.mysql.com/doc/refman/8.4/en/group-replication-limitations.html#group-replication-limitations-transaction-size).
  This means that a single transaction must fit into a binary log message of size no more than 4 GB.
- The connector doesn’t support replicating tables from a reader instance in Amazon Aurora as Aurora reader instances don’t maintain their own binary logs.
- The connector supports common source table schema changes during replication, such as adding, dropping, and renaming columns. See [Schema changes](#label-database-schema-changes) for the full list and a few unsupported change types.
- For `DATE` and `DATETIME` types in MySQL or MariaDB, any values that contain a zero month or day
  are mapped to the Unix epoch (’1970-01-01’ or ’1970-01-01T00:00’). Date zero (’0000-00-00’)
  is also mapped to the Unix epoch. Values with a zero year are converted to year one, for
  example, ’0000-05-30 7:59:59’ becomes ’0001-05-30T7:59:59’. The remaining date and time
  components are unchanged.
- For `TIMESTAMP` types in MySQL or MariaDB, value ’0000-00-00 00:00:00’ is mapped to the Unix epoch (’1970-01-01T00:00Z’).
- The connector doesn’t capture cascade delete operations (ON DELETE CASCADE).
  Foreign key cascade deletions are executed internally by InnoDB (the storage engine used by MySQL and MariaDB) and aren’t recorded in the binary log,
  resulting in incomplete replication of dependent table deletions to Snowflake.
- The connector doesn’t support the truncate table operation. `TRUNCATE` statements on the source are ignored, and the corresponding row deletions are not applied to the destination table.

Note

Limitations affecting certain table columns can be bypassed by excluding these specific columns from replication.

## Workflow

1. A **MySQL or MariaDB database administrator** performs the following tasks:

   - Configure MySQL or MariaDB replication settings
   - Create credentials for the connector
   - (Optionally) Provide the SSL certificate
2. An **Openflow administrator** creates a warehouse for the connector and a destination database
   for the replicated data.
3. An **Openflow administrator** or a **data engineer** performs the following tasks:

   1. Installs the connector.
   2. Specifies the required parameters for the flow template.
   3. Runs the flow. The connector performs the following tasks when run in Openflow:
      1. Creates a schema for journal tables.
      2. Creates the schemas and destination tables matching the source tables configured for replication.
      3. Starts replicating the tables. For details on the replication process, see [How tables are replicated](#how-tables-are-replicated).

## How the connector works

The following sections describe how the connector works in various scenarios, including replication, changes in schema, and data retention.

### Data replication

The name of the destination schema is determined by the `Destination Schema Pattern` parameter. For more information, see [MySQL Destination Parameters](/user-guide/data-integration/openflow/connectors/mysql/setup#label-of-mysql-destination-parameters). By default, the destination schema name matches the source database name, so the fully qualified name of a destination table is:

`<destination_database>.<source_database_name>.<source_table_name>`

### How tables are replicated

The tables are replicated in the following stages:

1. Schema introspection: The connector discovers the columns in the source table, including the column names and types,
   then validates them against Snowflake’s and the connector’s [Limitations](#limitations). Validation failures cause
   this stage to fail, and the cycle completes. After successful completion of this stage, the connector creates an empty destination table.
2. Snapshot load: The connector copies all data available in the
   source table into the destination table. If this stage fails, then
   no more data is replicated. After successful completion, the data from the source table is available in the destination table.
3. Incremental load: The connector tracks
   changes in the source table and applies those changes to the destination table.
   This process continues until the table is removed from replication. Failure at this stage
   permanently stops replication of the source table, until the issue is resolved.

   Note

   This connector can be configured to immediately start replicating incremental changes for newly added tables,
   bypassing the snapshot load phase. This option is often useful when reinstalling the connector
   in an account where previously replicated data exists and you want to continue replication without having to re-snapshot tables.

   For details on bypassing the snapshot load and using the incremental load process, see [Incremental replication](/user-guide/data-integration/openflow/connectors/mysql/incremental-replication).

Important

Interim failures, such as connection errors, do not prevent tables from being replicated.
Permanent failures, such as unsupported data types, do prevent tables from being replicated.
If a permanent failure prevents a table from being replicated, remove the table from the list of replicated tables.
After you address the problem that caused the failure, you can add the table back to the list of replicated tables.

### Schema changes

During incremental replication, the connector detects many source table schema changes and updates the destination table automatically. Unsupported changes stop replication for the affected table until you restart it.

#### Supported changes

The connector supports the following schema changes:

- **Add column.** The connector adds the column to the destination table and replicates values for new and updated rows. Existing rows aren’t backfilled; the new column is NULL for rows that existed before the change.
- **Drop column.** The connector renames the destination column with a `__SNOWFLAKE_DELETED` suffix to preserve historical values. For details, see [Dropped columns](#dropped-columns).
- **Rename column.** The connector treats a rename as dropping the original column and adding a new one. The connector retains the original column under a suffixed name; for example, a column named `A` becomes `A__SNOWFLAKE_DELETED`. For query patterns, see [Renamed columns](#renamed-columns).
- **Compatible type change.** The connector keeps replication running with the destination column type unchanged when you change a column to a source type that maps to the same Snowflake data type (for example, `INT` to `BIGINT`, both mapped to `NUMBER`).
- **Re-add a previously dropped column.** The connector adds the column as a new destination column alongside the existing soft-deleted column (for example, `A` and `A__SNOWFLAKE_DELETED`).

If you drop a column that was previously dropped and soft-deleted, replication for the affected table fails because the soft-deleted column name is already taken.

#### Unsupported changes

The connector doesn’t support the following schema changes. When one occurs, replication stops for the affected table:

- **Primary key definition change.** Adding or removing primary key columns, or changing which columns form the primary key.
- **Incompatible type change.** When the new source type maps to a different Snowflake data type (for example, `INT` to `VARCHAR`, mapped to `NUMBER` and `TEXT` respectively).
- **Numeric precision or scale change.** For example, changing `NUMERIC(7,2)` to `NUMERIC(6,3)`.
- **Character column length change.** For example, changing `VARCHAR(50)` to `VARCHAR(100)`.

To recover, restart replication for the affected table: see [Restart table replication](/user-guide/data-integration/openflow/connectors/mysql/maintenance#label-of-mysql-restart-table-replication).

The same soft-delete mechanism applies when you change a table’s Column Filter JSON. For details, see [Replicate a subset of columns in a table](/user-guide/data-integration/openflow/connectors/mysql/setup#label-mysql-connector-replication-subset-of-columns).

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
   columns as the replication key, overriding any primary key. For more
   information, see [Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/mysql/setup#label-mysql-logical-key).
2. **Primary key.** The columns of the table’s primary key constraint. When no
   explicit primary key is defined, MySQL’s InnoDB storage engine automatically
   promotes the first NOT NULL unique index to act as the primary key, and the
   connector uses it as the replication key.
3. **None.** If no primary key or qualifying unique index exists, the connector
   can’t replicate the table. To enable replication, add a primary key, add a
   NOT NULL unique index, or declare a logical key. For more information, see
   [Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/mysql/setup#label-mysql-logical-key).

The following examples illustrate each replication key scenario:

A table with an explicit primary key (no special setup required):

Copy code

```
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    customer_id INT,
    total DECIMAL(10, 2)
);
```

The connector uses `order_id` as the replication key.

A table without an explicit primary key, where InnoDB promotes a NOT NULL unique
index to act as the primary key:

Copy code

```
CREATE TABLE sessions (
    session_token VARCHAR(64) NOT NULL,
    user_id INT,
    created_at DATETIME,
    UNIQUE KEY idx_session_token (session_token)
);
```

InnoDB promotes `session_token` to act as the primary key, and the connector
uses it as the replication key.

A table with no primary key or qualifying unique index, replicated using a
logical key:

Copy code

```
CREATE TABLE audit_events (
    event_id CHAR(36) NOT NULL,
    event_type VARCHAR(100),
    payload JSON
);
```

Configure a logical key on `event_id` in the Table Key Configuration JSON.
For setup instructions, see [Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/mysql/setup#label-mysql-logical-key).

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

This behavior applies when the replication key is a primary key or a
user-declared logical key.

### Oversized values

By default, the connector replicates individual values up to **16 MB**. When the connector encounters a larger value, it marks the associated table as permanently failed and stops replicating it. To change how the connector handles oversized values (for example, to replace them with `NULL` instead), modify the **Oversized Value Strategy** destination parameter.

If your Snowflake account has the `ENABLE_OPENFLOW_CDC_MYSQL_SSV2` parameter set to `true`, the per-value limit can be raised from 16 MB to **128 MB**.

For details and instructions on enabling the 128 MB per-value limit, see [Increase the oversized value limit](/user-guide/data-integration/openflow/connectors/mysql/maintenance#label-of-mysql-increase-oversized-value-limit).

### Error handling for invalid rows

An *invalid row* is a row that Snowflake rejects during ingestion because it can’t be written to the destination table, for example a value that can’t be converted to the destination column’s type, or a missing required column. The **Error Handling Strategy** parameter controls what the connector does when it encounters an invalid row:

- **Fail Table** (default): On the first invalid row, the connector marks the table as permanently failed and stops replicating it, preserving strict, all-or-nothing replication. After you fix the source data, resume replication as described in [Restart table replication](/user-guide/data-integration/openflow/connectors/mysql/maintenance#label-of-mysql-restart-table-replication).
- **Log Errors and Continue**: The connector keeps replicating the valid rows and records each rejected row, together with its original payload and error details, in the table’s *error table*. The table isn’t marked as failed.

To change the strategy, set the **Error Handling Strategy** parameter. For more information, see [MySQL Destination Parameters](/user-guide/data-integration/openflow/connectors/mysql/setup#label-of-mysql-destination-parameters).

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

The connector enables error logging only on tables that it creates after you select **Log Errors and Continue**. To capture rejected rows for tables that were already being replicated, enable error logging on their existing destination and journal tables with the stored procedure in [Enable error logging on an existing schema](/user-guide/data-integration/openflow/connectors/mysql/maintenance#label-of-mysql-enable-error-logging-existing-schema).

Note

When the connector encounters invalid rows, it emits a `WARN` log entry that includes the number of rejected rows. Use these entries to monitor rejected-row activity.

#### Consume rejected rows

To process rejected rows programmatically, create a stream on the error table and consume it like any other Snowflake stream. For more information, see [Streams on error tables](/user-guide/data-load-overview#streams-on-error-tables).

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

Review [Openflow Connector for MySQL: Data mapping](/user-guide/data-integration/openflow/connectors/mysql/data-mapping) to understand how the connector maps data types to Snowflake data types.

Review [Set up the Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/setup) to set up the connector.
