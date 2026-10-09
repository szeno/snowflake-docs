# Apache Iceberg tables with Snowpark Connect for Spark

Snowpark Connect for Spark supports reading and writing [Apache Iceberg™ tables](/user-guide/tables-iceberg)
through the standard Spark DataFrame read/write and Spark SQL APIs. It supports working
with both Snowflake-managed and externally managed Iceberg tables. For general information
about Iceberg tables in Snowflake, see [Apache Iceberg™ tables](/user-guide/tables-iceberg).

Snowpark Connect for Spark executes the standard Spark/Iceberg DataFrame and SQL APIs on Snowflake using
Spark Connect. Your Spark client code stays the same; Snowflake becomes the execution engine.

## Iceberg table types

Snowpark Connect for Spark supports working with both Snowflake-managed and externally managed Iceberg
tables.

| Table type | What it is | Examples in this guide |
| --- | --- | --- |
| **Snowflake-managed Iceberg** | Snowflake-native Iceberg table created using `CREATE ICEBERG TABLE` | `MY_DB.MY_SCHEMA.my_table` |
| **Externally managed Iceberg / CLD** | Iceberg table linked to a table in a remote catalog via a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database) | Unity (`cldUnity`), AWS Glue (`cldglue`) |

Expand

Show lessSee more

Not every feature is available on every table type. The matrix in each section calls out
supported deployments.

## Install Iceberg SQL plugin

Copy code

```
pip install 'snowpark-connect[iceberg]'
```

This installs Iceberg Spark SQL extension JARs. This plugin is required to use Iceberg SQL
such as time-travel parsing on the Spark client. Snowpark Connect for Spark executes natively on Snowflake.

## Session parameters

The following parameters are required on the Snowpark Connect for Spark session to enable Iceberg features
to work end-to-end:

**Client / session (Snowpark Connect for Spark)**

| Config | Required for | How to set |
| --- | --- | --- |
| `spark.sql.extensions` includes `org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions` | Iceberg Spark SQL such as `VERSION AS OF` / `TIMESTAMP AS OF` | `spark.conf.set("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")` |

Expand

Show lessSee more

## Working with Snowflake-managed Iceberg tables

A managed Iceberg table uses Snowflake as the Iceberg catalog.

**Step 1:** You can choose where the table data and metadata files are stored:

- **Snowflake storage:** Snowflake stores and manages the Iceberg table files for you, so
  you don’t need to configure or grant access to external cloud storage.
- **External cloud storage** that you manage, which Snowflake accesses using an
  [external volume](/sql-reference/sql/create-external-volume).

To use Snowflake-managed Iceberg tables with external cloud storage, configure an external
volume and link it to your Spark session in one of the following ways:

- Set the `EXTERNAL_VOLUME` property on the database.
- Set `snowpark.connect.iceberg.external_volume` in your Spark configuration:

Copy code

```
spark.conf.set("snowpark.connect.iceberg.external_volume", "<your_volume>")
```

**Step 2:** Once you have set up an external volume, you can read and write to
Snowflake-managed Iceberg tables as shown in the examples below.

**Example — reading from a Snowflake-managed table**

Copy code

```
df = spark.read.format("iceberg").load("my_iceberg_table")

df = spark.read.table("my_iceberg_table")
```

The argument to `load()` is a Snowflake table identifier (for example,
`my_database.my_schema.my_table`), not a file path or catalog URI.

**Example — writing to a Snowflake-managed table using DataFrameWriter V1**

Copy code

```
df.write.format("iceberg").saveAsTable("my_iceberg_table")
```

**Example — writing to a Snowflake-managed table using Spark SQL**

Copy code

```
INSERT INTO prod.db.events SELECT * FROM staging.raw_events;
```

**Example — create a Snowflake-managed Iceberg table using Spark SQL**

Copy code

```
spark.sql(
    """
    CREATE TABLE my_db.my_schema.events (
      id INT,
      payload STRING
    )
    USING iceberg
    """
)
```

**Example — append to an existing Iceberg table without restating the format**

When the target already exists as Iceberg, you do not need `.format("iceberg")` on append.
Creating a new Iceberg table still requires an explicit Iceberg provider.

Copy code

```
# table already exists as Iceberg
df.write.mode("append").saveAsTable("my_db.my_schema.events")
df.write.insertInto("my_db.my_schema.events")
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.43.0

**Refresh Iceberg metadata**

`spark.sql("REFRESH TABLE t")` and `spark.catalog.refreshTable("t")` emit
`ALTER ICEBERG TABLE t REFRESH` so Snowflake re-reads Iceberg catalog metadata that changed
outside the session. Standard (non-Iceberg) Snowflake tables do not emit `REFRESH` DDL.

Copy code

```
spark.sql("REFRESH TABLE my_db.my_schema.events")
spark.catalog.refreshTable("my_db.my_schema.events")
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.44.0

**ALTER TABLE**

Spark SQL `ALTER TABLE` against a Snowflake-managed Iceberg table is executed as
`ALTER ICEBERG TABLE` so Snowflake applies the change on the Iceberg table.

**Iceberg reference:** [Spark DDL](https://iceberg.apache.org/docs/latest/spark-ddl/)

**Snowflake reference:** [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table)

Copy code

```
spark.sql("ALTER TABLE my_db.my_schema.events RENAME COLUMN old_name TO new_name")
spark.sql("ALTER TABLE my_db.my_schema.events DROP COLUMN to_drop")
spark.sql("ALTER TABLE my_db.my_schema.events RENAME TO my_db.my_schema.events_v2")
```

DataFrame `withColumnRenamed()` and `drop()` still only project columns. Use `ALTER TABLE` to
change the stored Iceberg schema.

| Capability | Managed | CLD |
| --- | --- | --- |
| `ALTER TABLE t RENAME TO t2` | ✅ | Use catalog-native rename |
| `ALTER TABLE t RENAME COLUMN old TO new` | ✅ | Use catalog-native rename |
| `ALTER TABLE t DROP COLUMN col` | ✅ | Use catalog-native drop |
| DataFrame `withColumnRenamed` / `drop` (projection only) | ✅ | ✅ |

Expand

Show lessSee more

Tip

**Minimum Snowpark Connect for Spark version:** 1.42.0

**Snapshot ancestry (`CALL system.ancestors_of`)**

`CALL system.ancestors_of` returns the live snapshot ancestry (`snapshot_id` and `timestamp`
in epoch milliseconds) for a Snowflake-managed Iceberg table.

Copy code

```
spark.sql("CALL my_db.system.ancestors_of('my_db.my_schema.events')").show()
```

Catalog-linked databases are not supported.

Tip

**Minimum Snowpark Connect for Spark version:** 1.40.0

## Working with externally managed Iceberg tables

You need to create a catalog-linked database to work with externally managed tables. A
[catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database) (CLD) is a
Snowflake database connected to an external Iceberg REST catalog. With a catalog-linked
database, you can access multiple remote Iceberg tables from Snowflake without creating
individual externally managed tables.

**What it does:** Read and write Iceberg tables in Snowflake databases linked to external
catalogs (Unity Catalog, AWS Glue). Snowpark Connect for Spark maps Spark `format("iceberg")` reads/writes
and `DataFrameWriterV2` to Snowflake `CREATE ICEBERG TABLE` / DML against the linked
catalog.

**Iceberg reference:** [Spark configuration — catalogs](https://iceberg.apache.org/docs/latest/spark-configuration/#catalogs)

To use externally managed Iceberg tables with Snowpark Connect for Spark, do the following:

**Step 1:** Configure an [external volume](/sql-reference/sql/create-external-volume) for
your cloud storage, and then create a catalog integration for your remote Iceberg catalog.

Alternatively, if your Iceberg catalog uses vended credentials, you do not need to create
an external volume. You can directly create a catalog integration using vended credentials
to your remote Iceberg catalog.

**Step 2:** Create a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database).

**Step 3:** Once a catalog-linked database has been created, you can use it for reads and
writes to externally managed Iceberg tables using Snowpark Connect for Spark. In the examples below,
`cldglue` is the catalog-linked database for Glue.

**Example — reading a Glue CLD table:**

Copy code

```
df = spark.read.format("iceberg").load("cldglue.my_schema.sales")
```

**Example — writing to a Glue CLD table using DataFrameWriter V1:**

Copy code

```
df.write.format("iceberg").saveAsTable("cldglue.my_schema.sales")
```

**Example — create a Glue CLD table using DataFrameWriter V2:**

Copy code

```
(
    source_df.writeTo("cldglue.my_schema.new_table")
    .using("iceberg")
    .create()
)
```

**Prerequisites:** CLD database and schema provisioned in Snowflake; grants on the linked
catalog schema.

Tip

**Minimum Snowpark Connect for Spark version with CLD support:** 1.27.0

**Example — create and drop a catalog-linked Iceberg table**

Create a CLD Iceberg table with DataFrameWriterV2 (the recommended create path on CLD).
Spark SQL `DROP TABLE … PURGE` is translated to `DROP ICEBERG TABLE … PURGE` so data files
in the linked catalog can be purged. Requires `DROP` privilege on the CLD schema.

For Snowflake-managed Iceberg tables, you can also create the table with Spark SQL
`CREATE TABLE … USING iceberg` as shown in
[Working with Snowflake-managed Iceberg tables](#working-with-snowflake-managed-iceberg-tables).
On CLD, prefer WriterV2 `create()`; Spark SQL `CREATE TABLE … USING iceberg` still has gaps.

Copy code

```
(
    source_df.writeTo("cldglue.my_schema.events")
    .using("iceberg")
    .create()
)

spark.sql("DROP TABLE cldglue.my_schema.events PURGE")
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.37.0 (`DROP TABLE PURGE`); 1.29.0 (WriterV2 `create`)

**Refresh Iceberg metadata**

`spark.sql("REFRESH TABLE t")` and `spark.catalog.refreshTable("t")` emit
`ALTER ICEBERG TABLE t REFRESH` so Snowflake re-reads Iceberg catalog metadata that changed
outside the session, including metadata updates in the external catalog. Standard
(non-Iceberg) Snowflake tables do not emit `REFRESH` DDL.

Copy code

```
spark.sql("REFRESH TABLE cldglue.my_schema.sales")
spark.catalog.refreshTable("cldglue.my_schema.sales")
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.44.0

| Capability | Managed | CLD (Unity/Glue) |
| --- | --- | --- |
| `spark.read.format("iceberg").load("table")` | ✅ | ✅ |
| `df.write.format("iceberg").save(...)` | ✅ | ✅ |
| `df.writeTo("table").using("iceberg").create()` | ✅ | ✅ |

Expand

Show lessSee more

## DataFrameWriterV2 — Iceberg writes

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

**Spark reference:**
[DataFrameWriterV2](https://spark.apache.org/docs/3.5.6/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriterV2.html)

In addition to DataFrameWriter V1 and Spark SQL APIs, Snowpark Connect for Spark supports writing using the
new DataFrameWriterV2 API. The V2 API handles Iceberg create, replace, append, and
conditional overwrite — including partition transforms and table properties — without
explicit SQL DDL.

**Iceberg reference:** [Spark writes](https://iceberg.apache.org/docs/latest/spark-writes/)

### Supported operations

| Method | Description |
| --- | --- |
| `using(provider)` | Sets the table provider. Use `iceberg` for a Snowflake-managed Iceberg table; otherwise a standard Snowflake table is used. |
| `option(key, value)` | Sets a write option, such as `check-ordering`, `check-nullability`, or `mergeSchema`. |
| `options(**options)` | Sets multiple write options at once. |
| `tableProperty(property, value)` | Sets a property on the new table, such as `comment`, `format-version`, or external volume location. |
| `partitionedBy(col, *cols)` | Partitions a created or replaced table by identity columns or the `years`, `months`, `days`, `hours`, and `bucket` transforms. |
| `create()` | Creates a new table from the DataFrame. Fails if the table already exists. |
| `replace()` | Replaces an existing table’s schema, properties, and data with the DataFrame. |
| `createOrReplace()` | Creates the table, or replaces it if it already exists. |
| `append()` | Appends the DataFrame’s rows to an existing table. |
| `overwrite(condition)` | Overwrites the rows matching the condition with the DataFrame’s rows. |
| `overwritePartitions()` | Overwrites the partitions present in the DataFrame and leaves the rest unchanged. |

Expand

Show lessSee more

### Infer Iceberg targets in CLD

For existing CLD Iceberg tables, `append`, `overwrite`, `overwritePartitions`, and `replace`
no longer require `.using("iceberg")`. Snowpark Connect for Spark infers the Iceberg path from the
catalog-linked target (matching Spark Connect behavior).

Create modes still require an explicit provider:

Copy code

```
# Existing CLD table — .using("iceberg") optional
(
    new_rows.writeTo("cldglue.my_schema.sales")
    .append()
)

# New CLD table — provider required
(
    new_rows.writeTo("cldglue.my_schema.sales_new")
    .using("iceberg")
    .create()
)
```

Appending with DataFrameWriter V1 also works without restating `.format("iceberg")` when the
CLD table already exists as Iceberg (`insertInto` / `mode("append").saveAsTable`). Creating a
new table still requires `.format("iceberg")` or `.using("iceberg")`.

Tip

**Minimum Snowpark Connect for Spark version:** 1.30.0

### CLD create / replace with correct identifier casing

Glue and Unity catalogs are case-insensitive. Snowpark Connect for Spark now emits explicit
`CREATE ICEBERG TABLE` DDL (not quoted mixed-case column names) for `create`,
`createOrReplace`, and `replace` on CLD targets. `createOrReplace` / `replace` drop the
existing table first because CLDs reject `CREATE OR REPLACE` for externally managed Iceberg
tables.

Copy code

```
(
    df.writeTo("cldglue.my_schema.events")
    .using("iceberg")
    .partitionedBy("days(event_ts)")
    .createOrReplace()
)
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.33.0

### `partitionedBy` with Iceberg transforms

Supports Iceberg partition transforms in `partitionedBy()`: `years`, `months`, `days`,
`hours`, `bucket`.

Copy code

```
(
    df.writeTo("my_db.my_schema.events")
    .using("iceberg")
    .partitionedBy(
        "days(event_date)",
    )
    .create()
)
```

Note

`partitionedBy` on standard (non-Iceberg) Snowflake tables is rejected in all WriterV2 modes.
Bucket transform is not currently supported.

| Capability | Managed | CLD |
| --- | --- | --- |
| `partitionedBy` identity columns | ✅ | ✅ |
| `partitionedBy` transforms | ✅ | ✅ |
| `partitionedBy` on Snowflake native tables | ❌ (error) | N/A |

Expand

Show lessSee more

Tip

**Minimum Snowpark Connect for Spark version:** 1.33.0

### `overwrite(condition)` — conditional row overwrite

Row-level conditional overwrite via `DELETE WHERE …` + `INSERT`:

Copy code

```
(
    df.writeTo("my_db.my_schema.events")
    .overwrite(F.col("region") == "US")
)
```

Works on both Iceberg and standard Snowflake tables.

Tip

**Minimum Snowpark Connect for Spark version:** 1.36.0

### `overwritePartitions()`

Dynamic partition-level overwrite for Iceberg tables for transformed partitions (identity,
`days`, `hours`, `months`, `years`).

Copy code

```
(
    df.writeTo("my_db.my_schema.events")
    .overwritePartitions()
)
```

Only the partitions present in the incoming DataFrame are replaced in the target Iceberg
table; all other partitions are preserved.

Tip

**Minimum Snowpark Connect for Spark version:** 1.34.0

### Iceberg table properties

Set Iceberg table properties through DataFrameWriterV2 `.tableProperty(...)` and through
Spark SQL `TBLPROPERTIES` on `CREATE TABLE`, `CREATE TABLE … AS SELECT`, and
`ALTER TABLE … SET / UNSET TBLPROPERTIES`. Known keys such as `comment`, `format-version`,
`max-snapshot-age.ms`, and `location` map to Snowflake Iceberg DDL. Additional Iceberg keys
(for example `write.delete.mode`) are forwarded as table properties. Unknown keys may be
ignored or rejected by Snowflake or the external catalog.

Copy code

```
(
    df.writeTo("my_db.my_schema.events")
    .using("iceberg")
    .tableProperty("comment", "Daily events")
    .tableProperty("format-version", "2")
    .tableProperty("max-snapshot-age.ms", "86400000")  # ms
    .tableProperty("write.delete.mode", "merge-on-read")
    .create()
)

spark.sql(
    "ALTER TABLE my_db.my_schema.events SET TBLPROPERTIES "
    "('read.split.target-size' = '268435456')"
)
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.35.0 (`comment` / `format-version`); 1.36.0
(`max-snapshot-age`); 1.42.0 (Spark SQL `TBLPROPERTIES` / extra Iceberg keys); 1.43.0
(managed `ALTER TABLE … TBLPROPERTIES`)

Note

`max-snapshot-age` is not supported on CLDs.

### Glue CLD `LOCATION` / `BASE_LOCATION`

When creating Iceberg tables in Glue-backed CLDs, pass the S3 prefix via Spark’s `LOCATION`
table property. Snowpark Connect for Spark maps it to Snowflake `BASE_LOCATION`:

Copy code

```
(
    df.writeTo("cldglue.my_schema.events")
    .using("iceberg")
    .tableProperty("location", "s3://my-bucket/prefix/events/")
    .create()
)
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.33.0

| Table property (DFWv2) | Accepted keys | Managed | CLD (Unity/Glue) |
| --- | --- | --- | --- |
| Table comment (1.35.0) | `comment` | ✅ | ✅ |
| Iceberg format version (1.35.0) | `format-version`, `iceberg.format-version` | ✅ | ✅ |
| Data retention (1.36.0) | `max-snapshot-age.ms`, `iceberg.max-snapshot-age.ms` | ✅ | ❌ |
| S3/GCS prefix (1.29.0) | `location`, `base_location`, `iceberg.base_location` | ✅ | ✅ |
| External volume (1.14.0) | `external_volume`, `iceberg.external_volume` | ✅ | ✅ (1.36.0) |
| Storage serialization (1.14.0) | `storage_serialization_policy`, `iceberg.storage_serialization_policy` | ✅ | ✅ (1.36.0) |
| Target file size (1.14.0) | `write.target-file-size`, `target_file_size` | ✅ | ✅ (1.36.0) |
| Spark SQL `TBLPROPERTIES` / extra Iceberg keys (1.42.0) | `write.delete.mode` and other leftover Iceberg keys | ✅ (1.43.0 for ALTER) | ✅ |

Expand

Show lessSee more

### Iceberg write options

Pass per-write DataFrame `.option(key, value)` settings on `append`, `overwrite`, or
`overwritePartitions`.

- **merge-schema** (`mergeSchema` / `merge-schema` / `merge_schema`) — evolve the Iceberg
  table schema. Supported on `append`, `overwrite`, and `overwritePartitions`, including
  CLD-backed tables.
- **check-ordering** (default `true`) — verifies the data’s column order matches the target
  table. Iceberg only; ignored on standard Snowflake tables.
- **check-nullability** (default follows `snowpark.connect.nullability.trackColumns`, that
  is, off) — blocks writing a nullable column into a NOT NULL column. Set
  `snowpark.connect.nullability.trackColumns=true` or pass `check-nullability=true`
  explicitly.
- **Other Iceberg write options** such as `target-file-size-bytes` are forwarded to
  Snowflake. Unrecognized keys are ignored (Spark-compatible). `check-ordering` and
  `check-nullability` stay local to Snowpark Connect for Spark and are not forwarded.

Copy code

```
(
    df.writeTo("my_db.my_schema.events")
    .option("merge-schema", "true")
    .option("target-file-size-bytes", "67108864")
    .option("check-ordering", "false")
    .option("check-nullability", "false")
    .append()
)
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.35.0 (`merge-schema`); 1.36.0 (`check-ordering` /
`check-nullability`); 1.42.0 (additional forwarded write options)

| Write option | Accepted key | Default | Managed | CLD |
| --- | --- | --- | --- | --- |
| Schema evolution | `merge-schema`, `mergeSchema`, `merge_schema` | off | ✅ | ✅ |
| Column-order check | `check-ordering` | `true` | ✅ | ✅ |
| Nullability check | `check-nullability` | off (`trackColumns`) | ✅ | ✅ |
| Other Iceberg write options | `target-file-size-bytes`, and so on | — | ✅ | ✅ |

Expand

Show lessSee more

## Tags

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Create named tags on a Snowflake-managed Iceberg table before you use those tags for
time travel. A tag is an immutable pointer to one snapshot (like a Git tag). You cannot
write DML against a tag; use the table (or a branch, where supported) for writes.

**Iceberg reference:**
[Historical tags](https://iceberg.apache.org/docs/latest/branching/#historical-tags)

| Capability | Managed | CLD |
| --- | --- | --- |
| `ALTER TABLE … CREATE TAG` (current snapshot) | ✅ (1.41.0) | Create the tag in the external catalog |
| `ALTER TABLE … CREATE TAG … AS OF VERSION` | ✅ (1.31.0) | External catalog |
| `ALTER TABLE … REPLACE TAG` / `RETAIN N DAYS` / `DROP TAG` | ✅ (1.41.0) | External catalog |

Expand

Show lessSee more

Copy code

```
spark.sql("ALTER TABLE my_db.my_schema.events CREATE TAG release_v1")
spark.sql(
    "ALTER TABLE my_db.my_schema.events CREATE TAG release_v1 "
    "AS OF VERSION 5129038471029384756 RETAIN 30 DAYS"
)
spark.sql(
    "ALTER TABLE my_db.my_schema.events REPLACE TAG release_v1 "
    "AS OF VERSION 5129038471029384756"
)
spark.sql("ALTER TABLE my_db.my_schema.events DROP TAG release_v1")
```

Note

On catalog-linked tables, create and manage tags in Glue or Unity (or with OSS Spark Iceberg)
before you read the tag through Snowpark Connect for Spark.

Tip

**Minimum Snowpark Connect for Spark version:** 1.31.0 (tag DDL); 1.41.0 (bare `CREATE TAG`, `REPLACE TAG`,
`RETAIN`)

## Time travel

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

### Snapshot-id based time travel

**What it does:** Read an Iceberg table as it existed at a specific snapshot ID. Maps to
Snowflake `AT(VERSION => <snapshot_id>)`.

**Iceberg reference:**
[Spark queries — time travel](https://iceberg.apache.org/docs/latest/spark-queries/#time-travel)

| Capability | Managed | CLD |
| --- | --- | --- |
| `option("snapshot-id", N)` | ✅ | ✅ |

Expand

Show lessSee more

**Example:**

Copy code

```
df = (
    spark.read
    .format("iceberg")
    .option("snapshot-id", 5129038471029384756)
    .load("my_db.my_schema.my_table")
)
```

**Aliases accepted:** `snapshot_id`, numeric `versionAsOf`.

**Snowflake SQL generated:**

Copy code

```
SELECT * FROM my_db.my_schema.my_table
  AT(VERSION => 5129038471029384756);
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.29.0

### Timestamp-based time travel

(DataFrame `as-of-timestamp`; 1.30.0 for SQL `TIMESTAMP AS OF`.)

**What it does:** Read the Iceberg snapshot that was current at a wall-clock timestamp.
Maps to Snowflake `AT(TIMESTAMP => ...)`.

**Iceberg reference:**
[Spark queries — time travel](https://iceberg.apache.org/docs/latest/spark-queries/#time-travel)

| Capability | Managed | CLD |
| --- | --- | --- |
| `option("as-of-timestamp", millis)` | ✅ | ✅ |
| `SELECT * FROM t TIMESTAMP AS OF '...'` | ✅ (needs `[iceberg]` + extensions) | ✅ |
| `SELECT * FROM t TIMESTAMP AS OF <millis>` | ✅ | ✅ |

Expand

Show lessSee more

**Example — DataFrame:**

Copy code

```
import time

# millis since Unix epoch
ts_millis = int(time.time() * 1000)

df = (
    spark.read
    .format("iceberg")
    .option("as-of-timestamp", ts_millis)
    .load("my_db.my_schema.my_table")
)
```

**Example — Spark SQL** (requires Iceberg SQL extensions on the session):

Copy code

```
spark.conf.set(
    "spark.sql.extensions",
    "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
)

spark.sql(
    "SELECT * FROM my_db.my_schema.my_table "
    "TIMESTAMP AS OF '2026-06-15 10:30:00'"
).show()
```

**CLD setup** (one-time per table):

Copy code

```
ALTER ICEBERG TABLE cldglue.my_schema.my_table
  SET TIME_TRAVEL_TIMESTAMP_SOURCE = 'ICEBERG_METADATA';
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.29.0 (DataFrame); 1.30.0 (SQL)

### Version tag-based time travel

After you create a tag (see [Tags](#tags)), you can time travel to that snapshot.

**What it does:** Read an Iceberg table at a named version tag. Maps to Snowflake
`AT(VERSION_TAG => '<name>')`.

**Iceberg reference:**
[Spark queries — time travel](https://iceberg.apache.org/docs/latest/spark-queries/#time-travel)
(tags are a named ref type)

| Capability | Managed | CLD |
| --- | --- | --- |
| `option("tag", "release_v1")` | ✅ | ✅ (tag must exist in catalog) |
| `SELECT * FROM t VERSION AS OF 'release_v1'` | ✅ | ✅ |

Expand

Show lessSee more

**Example — DataFrame:**

Copy code

```
df = (
    spark.read
    .format("iceberg")
    .option("tag", "release_v1")
    .load("my_db.my_schema.my_table")
)
```

**Example — Spark SQL:**

Copy code

```
spark.sql(
    "SELECT * FROM my_db.my_schema.my_table VERSION AS OF 'release_v1'"
).show()
```

Note

On CLD tables, the tag must already exist in Glue or Unity before you read it through
Snowpark Connect for Spark.

Tip

**Minimum Snowpark Connect for Spark version:** 1.30.0 (reads)

## Incremental reads

To read appended data incrementally, use:

- **start-snapshot-id** — Start snapshot ID used in incremental scans (exclusive).
- **end-snapshot-id** — End snapshot ID used in incremental scans (inclusive).

Snowpark Connect for Spark 1.34.0.

**What it does:** Read only rows appended between two Iceberg snapshots (CDC style). Maps to
Snowflake `CHANGES (INFORMATION => APPEND_ONLY) AT (VERSION => ...) [END (VERSION => ...)]`.

**Iceberg reference:**
[Spark queries — incremental read](https://iceberg.apache.org/docs/latest/spark-queries/#incremental-read)

| Capability | Managed | CLD |
| --- | --- | --- |
| `start-snapshot-id` / `end-snapshot-id` | ✅ (`CHANGE_TRACKING`) | ✅ |

Expand

Show lessSee more

**Example:**

Copy code

```
df = (
    spark.read
    .format("iceberg")
    .option("start-snapshot-id", 1001)
    .option("end-snapshot-id", 1005)  # optional — omit for "from S1 to head"
    .load("my_db.my_schema.my_table")
)
df.show()
```

**Managed table setup:**

Copy code

```
CREATE ICEBERG TABLE my_db.my_schema.events (
  id INT, payload STRING
) CHANGE_TRACKING = TRUE;
```

The same `start-snapshot-id` / `end-snapshot-id` options work on catalog-linked (Glue /
Unity) Iceberg tables. `CHANGE_TRACKING` is required only for Snowflake-managed tables.

Tip

**Minimum Snowpark Connect for Spark version:** 1.34.0 (managed); CLD incremental reads use the same
options

### Changelog reads (`.changes`)

Read Iceberg row-level changes (inserts and deletes) through the Spark metadata-table suffix
`table.changes`. This is the changelog / CDC surface. Append-only incremental reads via
`start-snapshot-id` / `end-snapshot-id` on the base table remain as documented above.

| Capability | Managed | CLD |
| --- | --- | --- |
| `spark.table("t.changes")` / `SELECT * FROM t.changes` | ✅ | ❌ Not supported |
| `start-snapshot-id` / `end-snapshot-id` bounds on `.changes` | ✅ | ❌ Not supported |

Expand

Show lessSee more

Copy code

```
# Full changelog
spark.sql("SELECT * FROM my_db.my_schema.events.changes").show()

# Bounded changelog (exclusive start, inclusive end)
(
    spark.read.format("iceberg")
    .option("start-snapshot-id", 1001)
    .option("end-snapshot-id", 1005)
    .table("my_db.my_schema.events.changes")
    .filter("_change_type = 'INSERT'")
    .show()
)
```

Managed Iceberg only. Requires a Snowflake release that supports Iceberg changelog scan
(10.34.100 or later). Version tags and branch refs are not valid bounds on `.changes`.

Tip

**Minimum Snowpark Connect for Spark version:** 1.43.0

## Iceberg metadata sub-tables

Read Iceberg inspection tables through Spark SQL the same way OSS Iceberg does
(`table.files`, `table.partitions`, and so on). These queries work on Snowflake-managed
Iceberg tables. Catalog-linked tables follow the same functions when the catalog can
resolve Iceberg metadata.

**Supported:** `.files`, `.snapshots`, `.manifests`, `.refs`, `.history`,
`.metadata_log_entries`, `.entries`, `.data_files`, `.delete_files`, `.all_entries`,
`.all_data_files`, `.all_manifests`, `.all_delete_files`, `.all_files`, `.partitions`,
and so on

**Unsupported:** `.position_deletes`

Copy code

```
spark.sql("SELECT file_path, record_count FROM my_db.my_schema.events.files").show()
spark.sql("SELECT * FROM my_db.my_schema.events.partitions").show()
spark.sql("SELECT snapshot_id, operation FROM my_db.my_schema.events.snapshots").show()
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.35.0–1.36.0 (original tables); 1.37.0–1.39.0
(additional metadata tables)

**Iceberg reference:** [Inspecting tables](https://iceberg.apache.org/docs/latest/spark-queries/#inspecting-tables)

## Iceberg V3 VARIANT columns (Spark 3.5)

Spark 3.5 (Snowpark Connect V1) has no `VariantType`, so you cannot declare `VARIANT` in Spark
SQL DDL. Create the Iceberg V3 table on Snowflake with `ICEBERG_VERSION = 3`, then read the
column through Snowpark Connect for Spark as JSON text (`StringType`). Wrap JSON text in `PARSE_JSON` on
write so the value is stored as an object, not a string.

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_db.my_schema.t (
    id INT,
    payload VARIANT
)
CATALOG = 'SNOWFLAKE'
EXTERNAL_VOLUME = '<your external volume>'
BASE_LOCATION = 'v3_variant/'
ICEBERG_VERSION = 3;
```

Copy code

```
df = spark.read.table("my_db.my_schema.t")
# payload is string (JSON text)
spark.sql("""
    INSERT INTO my_db.my_schema.t
    SELECT 2, PARSE_JSON('{"name": "bob", "age": 25}')
""")
```

You can use Spark JSON functions such as `from_json` and `get_json_object` on the string
column. Native Spark 4 Variant APIs (`variant_get`, `parse_json`, `schema_of_variant`) remain
a later Spark 4 / Snowpark Connect V2 surface.

Tip

**Minimum Snowpark Connect for Spark version:** 1.44.0

## Support matrix (summary)

| Feature | Managed | CLD (Unity/Glue) | Minimum Snowpark Connect for Spark version |
| --- | --- | --- | --- |
| Basic Iceberg read/write using DataFrame V1 and Spark SQL APIs | ✅ | ✅ | 1.27.0 |
| DataFrameWriterV2 create/replace/append/createOrReplace | ✅ | ✅ | 1.29.0 |
| Writer V2 infer Iceberg on existing CLD | ✅ | ✅ | 1.30.0 |
| `partitionedBy` transforms | ✅ | ✅ | 1.33.0 |
| `overwrite(condition)` | ✅ | ✅ | 1.36.0 |
| `overwritePartitions` | ✅ | ✅ | 1.34.0 |
| Iceberg table properties | ✅ | ✅ (`max-snapshot-age` ❌) | 1.35.0 / 1.42.0 |
| Snapshot-id | ✅ | ✅ | 1.29.0 |
| Timestamp (DataFrame) | ✅ | ✅ + `TIME_TRAVEL_TIMESTAMP_SOURCE` | 1.29.0 |
| Timestamp (SQL) | ✅ | ✅ + table param | 1.30.0 |
| Version tag read | ✅ | ✅ | 1.30.0 |
| Tag DDL | ✅ | external catalog | 1.31.0 |
| Incremental read | ✅ + `CHANGE_TRACKING` | ✅ | 1.34.0 |
| Changelog read (`.changes`) | ✅ | ❌ Not supported | 1.43.0 |
| Bare `CREATE TAG` / `REPLACE TAG` / `RETAIN` | ✅ | external catalog | 1.41.0 |
| Iceberg metadata sub-tables | ✅ | ✅ when the catalog can resolve Iceberg metadata | 1.37.0–1.39.0 |
| `CALL system.ancestors_of` | ✅ | ❌ Not supported | 1.40.0 |
| `ALTER TABLE` rename / drop column | ✅ | catalog-native | 1.42.0 |
| Iceberg write options | ✅ | ✅ | 1.35.0 / 1.42.0 |
| `insertInto` / append without restating format | ✅ | ✅ | 1.43.0 |
| `DROP TABLE PURGE` | ✅ | ✅ | 1.37.0 |
| `REFRESH TABLE` | ✅ | ✅ | 1.44.0 |
| Iceberg V3 `VARIANT` as JSON string (Spark 3.5) | ✅ | — | 1.44.0 |

Expand

Show lessSee more

## Version requirements (all features)

To use every feature in this guide, install:

| Component | Minimum version |
| --- | --- |
| `snowpark-connect` | 1.44.0 |
| `snowflake-snowpark-python` | >= 1.53.1 |
| `snowpark-connect-deps-iceberg` (optional extra) | >= 1.0.2 for SQL VERSION/TIMESTAMP AS OF client parsing |

Expand

Show lessSee more

**Install example:**

Copy code

```
pip install 'snowpark-connect[iceberg]>=1.44.0'
# snowflake-snowpark-python>=1.53.1 is pulled in as a dependency
```

## Known limitations

Most read and DataFrameWriterV2 write paths are closed as of Snowpark Connect for Spark version 1.44.0.
The items below are the main customer-visible limitations still worth knowing.

### Prefer DataFrameWriterV2 over Spark SQL DDL on CLD

| Surface | CLD status | Recommendation |
| --- | --- | --- |
| `df.writeTo(...).using("iceberg").create()` | ✅ Supported | Use this for CLD creates |
| `spark.sql("CREATE TABLE … USING iceberg")` | ⚠️ Gaps remain (temp-stage / DDL translation) | Avoid on CLD; use WriterV2 |
| `spark.sql("CREATE VIEW …")` on CLD | ❌ Not supported | Snowpark Connect for Spark returns an actionable error |
| `CREATE NAMESPACE` on CLD | ⚠️ Partial (`IF NOT EXISTS` honored; other edge cases documented in errors) | Use Snowflake catalog APIs where possible |

Expand

Show lessSee more

### Schema evolution on CLD

Nested struct schema evolution (adding nested fields) on CLD Iceberg tables is not supported.

### Format version 3

Iceberg `format-version` V3 on Unity CLD is not fully functional. Use `format-version` 2
unless your account team confirms V3 support for your catalog type.

Deletion vectors remain a later Spark 4 / Snowpark Connect V2 surface.
