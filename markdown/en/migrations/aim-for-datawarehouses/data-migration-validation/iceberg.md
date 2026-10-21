# Migrating and validating Apache Iceberg™ tables (spec v2 and v3)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview covers migrating relational data into Snowflake-managed Apache Iceberg™ tables on spec v2 and spec v3, and validating those tables.

AIM DMV can land migrated data in Snowflake-managed [Apache Iceberg™ tables](https://docs.snowflake.com/en/user-guide/tables-iceberg). Spec v2 with a **compatible** storage layout is the default. Spec v3 supports a **compatible** layout and a **native** layout. Use the same profile on the validation workflow so schema and row checks expect the types migration actually wrote.

This page covers new Snowflake-managed Iceberg tables loaded from Parquet (`migrationStrategy: copy_files`, inferred when `catalog` is `SNOWFLAKE`). For the field list, see [Iceberg configuration](../manual-migration/data-migration-configuration-reference#iceberg-configuration-targeticebergconfig). For account grants, see [Iceberg table targets](./required-privileges#iceberg-table-targets).

## How a spec v2 load works

A spec v2 load turns a source table into a Snowflake-managed Iceberg table. The default profile is `icebergSpec: v2`, `storageMode: compatible`, and `loadMode: ADD_FILES_COPY`. A spec v3 load uses the same steps and adds `ICEBERG_VERSION = 3`. See [Spec v3 profiles](#spec-v3-profiles).

An extract strategy that writes Parquet to cloud storage is required. See [Supported extraction strategies](#supported-extraction-strategies). The source engine, or the Worker when the strategy is `cloud_direct`, writes that Parquet. Snowflake registers the files on the Iceberg table and does not rewrite them. `ADD_FILES_COPY` does not coerce types, so the Parquet footer must match the Iceberg column types in [Data types on spec v2](#data-types-on-spec-v2).

1. Parquet is written to a Snowflake external stage.
2. AIM DMV creates the Iceberg table (`CATALOG = 'SNOWFLAKE'`).
3. Snowflake copies the Parquet onto the external volume, stores the Iceberg metadata there, and registers the files in the Snowflake catalog with `COPY INTO` and `LOAD_MODE = ADD_FILES_COPY`.

If the Parquet files are already on a stage, set `sourceDataStage` and omit `extraction`. That path skips the source extract and registers the files that are already there. Do not set both.

## Supported extraction strategies

Iceberg spec v2 loads are supported from Amazon Redshift, SQL Server, and Teradata. Azure Synapse can use the same `cet_as` path as SQL Server. `extraction.strategy` decides who writes the Parquet and where it lands.

| Strategy | Source | Who writes the Parquet | Destination |
| --- | --- | --- | --- |
| `unload` | Amazon Redshift | Redshift `UNLOAD` | Amazon S3 |
| `write_nos` | Teradata | Teradata `WRITE_NOS` | Amazon S3, Azure Blob, or GCS |
| `cet_as` | SQL Server, Azure Synapse | `CREATE EXTERNAL TABLE AS SELECT` on the source | Azure Blob |
| `cloud_direct` | SQL Server, Teradata | The Worker reads rows from the source and writes Parquet | Amazon S3, Azure Blob, or GCS |

Expand

Show lessSee more

Prefer the source-engine strategy when the source has one: `unload` for Amazon Redshift, `write_nos` for Teradata, and `cet_as` for SQL Server and Azure Synapse. Use `cloud_direct` when that source-engine path is not available.

`unload`, `write_nos`, `cet_as`, and `cloud_direct` all require `extraction.externalStage`. SQL Server Iceberg extracts must use `cet_as` or `cloud_direct`.

Important

`regular` is not an Iceberg extract. Iceberg registration reads Parquet from an external stage. `regular` writes to a Snowflake internal stage.

The external stage and the external volume are different locations. `extraction.externalStage` is where the Parquet lands and where `ADD_FILES_COPY` reads it. `externalVolume` is where the Iceberg table stores its data and metadata. The stage URL has to match the path the extract writes. If it does not, registration finds no files and the table is created empty.

Worker TOML does not change for an Iceberg target. You still need a Worker when the workflow extracts from the source. See the platform migration pages linked from [Data migration](./data-migration).

## Spec v2 profile

When `tableType` is `"iceberg"` and you omit the profile fields, AIM DMV uses spec v2:

| Property | Default | What it does |
| --- | --- | --- |
| `icebergSpec` | `v2` | Logical type profile. Supported values are `v2` and `v3`. |
| `storageMode` | `compatible` | `compatible` writes `STORAGE_SERIALIZATION_POLICY = COMPATIBLE`. `native` is spec v3 only and writes `STORAGE_SERIALIZATION_POLICY = OPTIMIZED`. Spec v2 with `storageMode: native` is rejected. |
| `loadMode` | `ADD_FILES_COPY` | `ADD_FILES_COPY` registers staged Parquet without rewriting it. `FULL_INGEST` rewrites the staged files and can coerce values into native spec v3 types. |
| `externalEngineAccess` | `false` | Set to `true` when Spark, Trino, or another engine must read the same files. Allowed with `storageMode: compatible`. Rejected with `storageMode: native`. |
| `postLoadOptimize` | Derived | Defaults to `true` for `ADD_FILES_COPY` and `false` for `FULL_INGEST`. When enabled, it turns on data compaction after the first load. |
| `targetFileSize` | Unset | Optional target size: `AUTO`, `16MB`, `32MB`, `64MB`, or `128MB`. `FULL_INGEST` defaults to `128MB`. |

Expand

Show lessSee more

Note

The target name must not already exist. That includes a native table, a view, an Iceberg table, or any other object with that name. AIM DMV stops before creating or loading the Iceberg table, so it does not register files onto an existing catalog entry. Drop the object or choose another name. Native Snowflake tables can be reused. Iceberg targets cannot.

## Where the table is stored

Pick one store. The extract landing zone (the external stage or pre-staged Parquet) is separate from this choice.

| Store | `externalVolume` | `baseLocationPrefix` | Resulting DDL |
| --- | --- | --- | --- |
| Your bucket | Your external volume name | **Required.** `BASE_LOCATION` is `{prefix}/{database}/{schema}/{table}`. | `EXTERNAL_VOLUME` plus `BASE_LOCATION` |
| Snowflake storage | `SNOWFLAKE_MANAGED` | **Omit it.** Setting a prefix is a configuration error. | `EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'` and no `BASE_LOCATION` |

Expand

Show lessSee more

Snowflake storage (`SNOWFLAKE_MANAGED`) is available on AWS and Azure commercial accounts. GCP, government regions, and China regions are rejected before any extract or load task is created.

Create the external volume, catalog integration, and stage before the workflow. See [Configure an external volume](https://docs.snowflake.com/en/user-guide/tables-iceberg-configure-external-volume) and [Iceberg table targets](./required-privileges#iceberg-table-targets).

## Migration workflow

Set `tableType` and `icebergConfig` on `defaultTableConfiguration.target` so every table inherits them, or set them on a single table. A workflow can mix Iceberg and native targets: omit `tableType` (or set `"native"`) on the tables that should stay native Snowflake tables. When you override one table back to native, set `icebergConfig: null` so an inherited Iceberg block is cleared.

Land Parquet with the source platform’s server-side extract, **or** point `sourceDataStage` at Parquet that is already on a stage. Do not set both. `sourceDataStage` must start with `@`.

**Extract, then load** (customer external volume):

Copy code

```
defaultTableConfiguration:
  source:
    databaseName: analytics_db
    schemaName: public
  target:
    databaseName: TARGET_DB
    schemaName: public
    tableType: iceberg
    icebergConfig:
      catalog: SNOWFLAKE
      externalVolume: my_iceberg_ext_vol
      baseLocationPrefix: migrations/redshift
      icebergSpec: v2
      storageMode: compatible
      loadMode: ADD_FILES_COPY
  extraction:
    strategy: unload
    externalStage: TARGET_DB.PUBLIC.S3_EXTERNAL_STAGE
tables:
  - source:
      tableName: customers
    target:
      tableName: customers
    columnNamesToPartitionBy:
      - customer_id
```

**Snowflake storage** uses the same extract stage. Change only the volume, and leave the prefix out:

Copy code

```
icebergConfig:
  catalog: SNOWFLAKE
  externalVolume: SNOWFLAKE_MANAGED
  icebergSpec: v2
  storageMode: compatible
  loadMode: ADD_FILES_COPY
```

**Parquet already on a stage.** Set `sourceDataStage` and omit `extraction`:

Copy code

```
icebergConfig:
  catalog: SNOWFLAKE
  externalVolume: my_iceberg_ext_vol
  baseLocationPrefix: migrations/prestaged
  icebergSpec: v2
  storageMode: compatible
  sourceDataStage: "@TARGET_DB.PUBLIC.PRESTAGED_PARQUET"
```

**Prompt:**

Copy code

```
Migrate the SALES schema to Iceberg spec v2 tables on external volume MY_EXTERNAL_VOLUME, with base location prefix migrations/sales
```

## Data types on spec v2

`ADD_FILES_COPY` does not coerce types. AIM DMV rewrites the native Snowflake type map so the `CREATE ICEBERG TABLE` column types match the Parquet footers.

| Source type family | Native Snowflake type | Iceberg spec v2 (`storageMode: compatible`) |
| --- | --- | --- |
| `TINYINT`, `SMALLINT`, `INT` | `NUMBER` | `INTEGER` |
| `BIGINT` | `NUMBER(19,0)` | `BIGINT` |
| `FLOAT`, `REAL` | `FLOAT` | `DOUBLE` |
| `TIME`, timestamps, `DATETIME` | A temporal type | `VARCHAR` |
| `VARIANT`, `OBJECT`, `ARRAY`, `GEOGRAPHY`, `GEOMETRY`, JSON, XML | A complex type | `VARCHAR` |
| `BINARY(n)` | `BINARY(n)` | `BINARY` (length removed) |
| `DECIMAL` and character types | Unchanged | Unchanged. Character columns are unbounded `VARCHAR`. |
| `INTERVAL` | A day-time interval, or `VARCHAR` | `VARCHAR`, regardless of `intervalHandling` |

Expand

Show lessSee more

Amazon Redshift UNLOAD has its own Parquet encoding for a few types:

| Redshift type | Iceberg spec v2 type |
| --- | --- |
| `TIMESTAMP` | `VARCHAR` (UTC ISO text) |
| `TIMESTAMPTZ` | `VARCHAR` (UTC ISO text) |
| `TIME`, `TIMETZ` | `VARCHAR` |
| `REAL`, `FLOAT4` | `DOUBLE` (widened without loss) |
| `VARBYTE`, `VARBINARY` | `VARCHAR` (hexadecimal text) |
| `SUPER` | `VARCHAR` |
| `GEOMETRY` | `VARCHAR` |

Expand

Show lessSee more

`columnTypeMappings` still overrides a single source type when you need a different target type. See [ColumnTypeMapping and ColumnNameMapping models](../manual-migration/data-migration-configuration-reference#columntypemapping-model).

## Spec v3 profiles

Spec v3 uses the same extract path as spec v2. Set `icebergSpec: v3`. `CREATE ICEBERG TABLE` adds `ICEBERG_VERSION = 3`.

`storageMode` and `loadMode` control different behavior:

- `storageMode` selects the table’s serialization policy. `compatible` supports external readers. `native` uses Snowflake’s optimized layout and is available only on spec v3.
- `loadMode` selects how Snowflake loads the staged Parquet. `ADD_FILES_COPY` registers the files without rewriting them. `FULL_INGEST` rewrites the files and can coerce values into native spec v3 types.

### Compatible storage

`storageMode: compatible` is the default and uses `STORAGE_SERIALIZATION_POLICY = COMPATIBLE`, so other engines can read the files. With `ADD_FILES_COPY`, column types match [Data types on spec v2](#data-types-on-spec-v2).

Copy code

```
icebergConfig:
  catalog: SNOWFLAKE
  externalVolume: my_iceberg_ext_vol
  baseLocationPrefix: migrations/sales
  icebergSpec: v3
  storageMode: compatible
  loadMode: ADD_FILES_COPY
```

### Native storage

`storageMode: native` requires `icebergSpec: v3`. The table uses `STORAGE_SERIALIZATION_POLICY = OPTIMIZED`. Leave `externalEngineAccess` at `false`.

With `ADD_FILES_COPY`, Snowflake does not coerce types. The Iceberg types must match the staged Parquet footer. When the Worker writes native Parquet, as it does for SQL Server `cloud_direct`, `TIME` stays `TIME`, timestamps become `TIMESTAMP_NTZ(6)`, and arrays become `ARRAY(VARCHAR)`. SQL Server `cet_as`, Amazon Redshift `unload`, and Teradata `write_nos` write time and timestamps as text, so those columns stay `VARCHAR`.

Schemaless `VARIANT`, `OBJECT`, `SUPER`, JSON, and XML values stay `VARCHAR`. Geospatial values and `INTERVAL` also stay `VARCHAR` under `ADD_FILES_COPY`.

Copy code

```
icebergConfig:
  catalog: SNOWFLAKE
  externalVolume: my_iceberg_ext_vol
  baseLocationPrefix: migrations/sales
  icebergSpec: v3
  storageMode: native
  loadMode: ADD_FILES_COPY
```

### Full ingestion

Use `loadMode: FULL_INGEST` when Snowflake should rewrite the staged Parquet into the table’s own files. On spec v3, the transform `COPY INTO` coerces temporal and geospatial values into native types under either `storageMode: compatible` or `storageMode: native`.

| Source type family | Iceberg spec v3 with `FULL_INGEST` |
| --- | --- |
| `TIME` | `TIME(6)` |
| Timestamps, `DATETIME` | `TIMESTAMP_NTZ(6)` |
| Timestamps with an offset | `TIMESTAMP_LTZ(6)` |
| `TIME WITH TIME ZONE`, `TIMETZ` | `TIMESTAMP_LTZ(6)` |
| `GEOGRAPHY` | `GEOGRAPHY` |
| `GEOMETRY` | `GEOMETRY(4326)`, or its explicit non-zero SRID |
| `VARIANT`, `OBJECT`, `SUPER`, JSON, XML, `INTERVAL` | `VARCHAR` |
| Integers and per-source 64-bit floating-point families | `INTEGER`, `BIGINT`, or `DOUBLE`, matching the extract contract |

Expand

Show lessSee more

A timestamp with an offset, such as `TIMESTAMP WITH TIME ZONE` or `TIMESTAMPTZ`, becomes `TIMESTAMP_LTZ(6)`. Iceberg has no `TIMESTAMP_TZ` column.

`TIME WITH TIME ZONE` and `TIMETZ` also become `TIMESTAMP_LTZ(6)`. The staged value has a time and an offset but no date, so the load attaches it to `1970-01-01` and then stores the instant.

Warning

`TIMESTAMP_LTZ` stores the instant in UTC and shows it in the session time zone.

Spec v2 with `FULL_INGEST` keeps the spec v2 types, including temporal and geospatial values as `VARCHAR`. Pre-staged tables that use `sourceDataStage` take their column types from `INFER_SCHEMA` and are not retyped from a source mapping.

`FULL_INGEST` is supported for these Parquet-producing paths:

| Source | Extraction strategy |
| --- | --- |
| Amazon Redshift | `unload` |
| SQL Server | `cet_as`, `cloud_direct`, or `regular` with `use_bcp = false` |
| Teradata | `write_nos` |

Expand

Show lessSee more

Pre-staged Parquet in `sourceDataStage` is also supported for those sources. Other source and strategy combinations fail during configuration validation.

Copy code

```
icebergConfig:
  catalog: SNOWFLAKE
  externalVolume: my_iceberg_ext_vol
  baseLocationPrefix: migrations/sales
  icebergSpec: v3
  storageMode: native
  loadMode: FULL_INGEST
  targetFileSize: 128MB
```

With `FULL_INGEST`, `targetFileSize` defaults to `128MB` and `postLoadOptimize` defaults to `false`. With `ADD_FILES_COPY`, `postLoadOptimize` defaults to `true`.

## Limitations

- **No incremental sync.** `synchronization` does not apply to Iceberg targets. Each run performs the full load for that table. `full-replace` is rejected for Iceberg targets.
- **The target table is unpartitioned.** `CREATE ICEBERG TABLE` is emitted without `PARTITION BY`. `columnNamesToPartitionBy` only splits the source extract. To partition the migrated table, copy it into a new Iceberg table with a partition transform such as `MONTH(order_ts)` after migration. Prefer time transforms or `BUCKET(n, col)` over a raw high-cardinality column, because one statement that writes more than about 100,000 partitions can fail.
- **Row cap per extract partition.** The default cap of 500,000 rows per partition on Worker-side strategies, and the table-level `maxPartitionSizeRows` override, apply to Iceberg targets too.

## Validating spec v2 and spec v3 tables

Run validation after the migration. Declare the same profile on the validation workflow. If you omit `tableType` and `icebergConfig`, schema validation expects native Snowflake types and can disagree with the Iceberg table.

Set `tableType` and `icebergConfig` on `defaultTableConfiguration` or on each table entry. On a validation workflow these fields are siblings of `fullyQualifiedName`. They are not nested under `target`, which is the migration workflow shape. Validation only needs the profile fields (`icebergSpec`, `storageMode`, and `loadMode`). It does not create the table or read `externalVolume`.

Copy code

```
source_platform: redshift
validation_configuration:
  schema_validation: true
  row_validation: true
defaultTableConfiguration:
  tableType: iceberg
  icebergConfig:
    icebergSpec: v2
    storageMode: compatible
    loadMode: ADD_FILES_COPY
tables:
  - fullyQualifiedName: analytics_db.public.customers
    targetDatabase: TARGET_DB
    targetSchema: PUBLIC
    targetName: customers
    indexColumnList:
      - customer_id
    columnNamesToPartitionBy:
      - customer_id
```

What each level does against this profile:

- **Schema (L1)** checks names, types, and precision against the spec v2 types. Expected differences are widened integers, `FLOAT` and `REAL` as `DOUBLE`, and time, timestamps, and large character values as `VARCHAR`.
- **Metrics (L2)** does not run for Iceberg tables. It is not a setting on this profile. Use schema validation and row validation.
- **Rows (L3)** compares cells. Cell mismatches must not appear. A row-count or byte-size difference can be tolerated when the cells still match. Redshift `TIMESTAMP` and `TIMESTAMPTZ` are compared as the UTC ISO text UNLOAD wrote. Redshift `TIME`, `TIMETZ`, and `VARBYTE` source values are normalized to that same UNLOAD text. Semi-structured values stored as `VARCHAR` are compared as canonical JSON. Geospatial values stored as `VARCHAR` are compared as text.

Reuse the same L3 extract strategy and external stage you used for migration. See [L3 extraction](../manual-migration/data-validation-configuration-reference#l3-extraction).

For spec v3, declare `icebergSpec: v3` and the same `storageMode` and `loadMode` the migration used. Schema validation then expects that profile. With `ADD_FILES_COPY`, validation follows the staged Parquet footer. With `FULL_INGEST`, it expects native temporal and geospatial types. Metrics validation does not run.

**Prompt:**

Copy code

```
Validate the SALES Iceberg spec v2 tables with schema and row validation.
```

## Related content

- [Iceberg configuration](../manual-migration/data-migration-configuration-reference#iceberg-configuration-targeticebergconfig)
- [Data migration](./data-migration)
- [Data validation](./data-validation)
- [Required privileges](./required-privileges#iceberg-table-targets)
- [Data migration advanced configuration](./data-migration-advanced-configuration)
- [Data validation advanced configuration](./data-validation-advanced-configuration)
