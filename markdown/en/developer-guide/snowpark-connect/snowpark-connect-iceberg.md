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

| Capability | Managed | CLD (Unity/Glue) |
| --- | --- | --- |
| `spark.read.format("iceberg").load("table")` | ✅ | ✅ |
| `df.write.format("iceberg").save(...)` | ✅ | ✅ |
| `df.writeTo("table").using("iceberg").create()` | ✅ | ✅ |

Expand

Show lessSee more

## DataFrameWriterV2 — Iceberg writes

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

### Iceberg table properties: `comment`, `format-version`, `max-snapshot-age`

`tableProperty("comment", …)`, `tableProperty("format-version", "2")`, and
`tableProperty("max-snapshot-age.ms", "86400000")` are forwarded into
`CREATE ICEBERG TABLE` DDL.

Copy code

```
(
    df.writeTo("my_db.my_schema.events")
    .using("iceberg")
    .tableProperty("comment", "Daily events")
    .tableProperty("format-version", "2")
    .tableProperty("max-snapshot-age.ms", "86400000")  # ms
    .create()
)
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.35.0, 1.36.0 (`max-snapshot-age`)

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

Expand

Show lessSee more

### Iceberg write options: `merge-schema`

Pass `mergeSchema` or (`merge-schema` / `merge_schema`) to evolve the Iceberg table schema
during a V2 `overwrite()` or `partitionOverwrite()`:

Copy code

```
(
    df.writeTo("my_db.my_schema.events")
    .option("merge-schema", "true")
    .overwrite()
)
```

Previously only supported for `append()`. CLD-backed Iceberg tables (for example, Glue) are
supported.

Tip

**Minimum Snowpark Connect for Spark version:** 1.35.0

### Iceberg write options: `check-ordering`, `check-nullability`

Per-write validation for Iceberg V2 writes, passed via `.option(...)` on `append`,
`overwrite`, or `overwritePartitions`.

- **check-ordering** (default `true`) — verifies the data’s column order matches the target table.
- **check-nullability** (default follows `snowpark.connect.nullability.trackColumns`, i.e. off) — blocks writing a nullable column into a NOT NULL column.

Copy code

```
(
    df.writeTo("cldglue.my_schema.events")
    .option("check-ordering", "false")
    .option("check-nullability", "false")
    .append()
)
```

Tip

**Minimum Snowpark Connect for Spark version:** 1.36.0

| Write option | Accepted key | Default | Managed | CLD |
| --- | --- | --- | --- | --- |
| Column-order check | `check-ordering` | `true` | ✅ | ✅ |
| Nullability check | `check-nullability` | off (`trackColumns`) | ✅ | ✅ |

Expand

Show lessSee more

**Notes:**

- Iceberg only — both options are ignored on standard Snowflake tables.
- For `check-nullability` enforcement, set `snowpark.connect.nullability.trackColumns=true`
  or pass `check-nullability=true` explicitly.

## Time travel

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

Tags can be used for retaining important historical snapshots for auditing purposes.
Read about tags in the
[Iceberg branching documentation](https://iceberg.apache.org/docs/latest/branching/#historical-tags).

Snowpark Connect for Spark version 1.30.0 (tag reads); 1.31.0 (tag DDL mapping).

**What it does:** Read an Iceberg table at a named version tag. Maps to Snowflake
`AT(VERSION_TAG => '<name>')`.

**Iceberg reference:**
[Spark queries — time travel](https://iceberg.apache.org/docs/latest/spark-queries/#time-travel)
(tags are a named ref type)

| Capability | Managed | CLD |
| --- | --- | --- |
| `option("tag", "release_v1")` | ✅ | ✅ (tag must exist in catalog) |
| `SELECT * FROM t VERSION AS OF 'release_v1'` | ✅ | ✅ |
| `ALTER TABLE … CREATE TAG` (Spark SQL) | ✅ via Snowpark Connect for Spark DDL mapping (1.31+) | Tag created in external catalog |

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

On CLD tables, tags are catalog-side metadata. Create the tag in Glue/Unity (or via OSS
Spark Iceberg) before reading through Snowpark Connect for Spark.

Tip

**Minimum Snowpark Connect for Spark version:** 1.30.0 (reads); 1.31.0 (tag DDL)

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
| `start-snapshot-id` / `end-snapshot-id` | ✅ (`CHANGE_TRACKING`) | ❌ Not supported |

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

Tip

**Minimum Snowpark Connect for Spark version:** 1.34.0

## Support matrix (summary)

| Feature | Managed | CLD (Unity/Glue) | Minimum Snowpark Connect for Spark version |
| --- | --- | --- | --- |
| Basic Iceberg read/write using DataFrame V1 and Spark SQL APIs | ✅ | ✅ | 1.27.0 |
| DataFrameWriterV2 create/replace/append/createOrReplace | ✅ | ✅ | 1.29.0 |
| Writer V2 infer Iceberg on existing CLD | ✅ | ✅ | 1.30.0 |
| `partitionedBy` transforms | ✅ | ✅ | 1.33.0 |
| `overwrite(condition)` | ✅ | ✅ | 1.36.0 |
| `overwritePartitions` | ✅ | ✅ | 1.34.0 |
| `tableProperty` comment / format-version | ✅ | ✅ | 1.35.0 |
| Snapshot-id | ✅ | ✅ | 1.29.0 |
| Timestamp (DataFrame) | ✅ | ✅ + `TIME_TRAVEL_TIMESTAMP_SOURCE` | 1.29.0 |
| Timestamp (SQL) | ✅ | ✅ + table param | 1.30.0 |
| Version tag read | ✅ | ✅ | 1.30.0 |
| Tag DDL | ✅ | external catalog | 1.31.0 |
| Incremental read | ✅ + `CHANGE_TRACKING` | ❌ Not supported | 1.34.0 |

Expand

Show lessSee more

## Version requirements (all features)

To use every feature in this guide, install:

| Component | Minimum version |
| --- | --- |
| `snowpark-connect` | 1.35.0 |
| `snowflake-snowpark-python` | >= 1.53.1 |
| `snowpark-connect-deps-iceberg` (optional extra) | >= 1.0.2 for SQL VERSION/TIMESTAMP AS OF client parsing |

Expand

Show lessSee more

**Install example:**

Copy code

```
pip install 'snowpark-connect[iceberg]>=1.35.0'
# snowflake-snowpark-python>=1.53.1 is pulled in as a dependency
```

## Known limitations

Most read and DataFrameWriterV2 write paths are closed as of Snowpark Connect for Spark version 1.35.0.
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

### Iceberg metadata sub-tables (`.snapshots`, `.files`, `.manifests`, `.refs`)

`.snapshots`, `.files`, `.manifests`, and `.refs` are supported on Managed, Glue CLD,
Unity CLD, and Horizon. Other sub-tables (`.entries`, `.all_manifests`, etc.) return
`UNSUPPORTED_OPERATION`.

**Supported:** `.files`, `.snapshots`, `.manifests`, `.refs`, `.history`, `.metadata_log_entries`

**Unsupported:** `.all_data_files`, `.all_delete_files`, `.all_entries`, `.all_manifests`,
`.delete_files`, `.entries`, `.partitions`, `.position_deletes`

### Iceberg incremental and changelog reads

Reading catalog-linked (Glue / Unity) Iceberg tables is supported, including time travel
(`VERSION AS OF` / `TIMESTAMP AS OF`) and metadata tables. Incremental reads
(`start-snapshot-id` / `end-snapshot-id`) and changelog/CDC reads are not supported on
catalog-linked databases. They are only available on managed Iceberg tables.

Tip

**Minimum Snowpark Connect for Spark version:** 1.36.0

For sub-tables that remain unsupported (`.history`, `.entries`, etc.): read `metadata.json`
directly from object storage.

**Iceberg reference:** [Inspecting tables](https://iceberg.apache.org/docs/latest/spark-queries/#inspecting-tables)

### Schema evolution on CLD

Nested struct schema evolution (adding nested fields) on CLD Iceberg tables is not supported.

### SQL time-travel — extensions gate

SQL `VERSION AS OF` and `TIMESTAMP AS OF` require `spark.sql.extensions` to include
`org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions`. Install
`snowpark-connect[iceberg]` and set the config on the Snowpark Connect for Spark server. Snowpark Connect for Spark
implements execution natively on Snowflake; the config is the customer-visible support
contract.

### Tag writes

| Surface | Status |
| --- | --- |
| Tag create via Spark SQL on CLD | Create tags in Glue/Unity catalog externally |

Expand

Show lessSee more

### Format version 3

Iceberg `format-version` V3 on Unity CLD is not fully functional. Use `format-version` 2
unless your account team confirms V3 support for your catalog type.

Note

Iceberg V3-specific capabilities like `VARIANT` data type and deletion vectors need Spark v4
and will be supported in an upcoming release.
