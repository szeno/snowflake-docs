# Migrating Data from IBM DB2

AIM DMV migrates and validates data from IBM DB2 for Linux, UNIX, and Windows (LUW).

This page covers IBM DB2-specific setup for [Data migration](./data-migration). For workflow and Worker field definitions, see [Data migration configuration reference](../manual-migration/data-migration-configuration-reference).

## Prerequisites

- **Worker driver**: The Worker image includes the native DB2 driver. You don’t install a DB2 ODBC driver.
- **Authentication**: Username and password only. SSL, LDAP, and Kerberos aren’t supported.
- **Network**: The Worker host must reach the DB2 host on the configured port. Default port is **50000**. A Worker on Snowpark Container Services needs an external access integration that allows that host. See [Deploying workers](./deploy-workers).
- **Privileges**: `SELECT` on every table being migrated. Catalog views used for schema and key discovery are readable by `PUBLIC` by default. See [IBM DB2](./required-privileges#ibm-db2).

## Connectivity and extraction

The database name is chosen when the session connects. SQL that AIM DMV generates is `schema.table`. The database isn’t a qualifier in that SQL. `[connections.source.db2].database` must match `source.databaseName` in the workflow.

Copy code

```
[connections.source.db2]
username = "myuser"
password = "your_password"
database = "SAMPLE"
host = "db2.example.com"
port = "50000"
```

AIM DMV accepts two extraction strategies. Both read rows through the Worker and write Parquet. There is no DB2 server-side export.

| Strategy | When to use |
| --- | --- |
| `regular` | Default when the workflow omits a strategy. The Worker reads the table, writes Parquet locally, and uploads it to a Snowflake internal stage with `PUT`. |
| `cloud_direct` | Preferred when you have Amazon S3, GCS, or Azure Blob and a Snowflake external stage on that same prefix. The Worker writes the same Parquet to object storage, and Snowflake loads it from the external stage. This skips the local file and the `PUT`. |

Expand

Show lessSee more

`cloud_direct` needs a Worker target section (`[connections.target.s3]`, `[connections.target.gcs]`, or `[connections.target.blob]`) and `extraction.externalStage` whose URL covers that bucket or container and prefix. When more than one of those target sections is present, the Worker prefers S3, then GCS, then Azure Blob, unless the workflow sets `storageBackend`. See [L3 extraction](../manual-migration/data-validation-configuration-reference#l3-extraction).

**Workflow example:**

Copy code

```
tables:
  - source:
      databaseName: SAMPLE
      schemaName: MYSCHEMA
      tableName: CUSTOMERS
    target:
      databaseName: TARGET_DB
      schemaName: PUBLIC
      tableName: CUSTOMERS
    columnNamesToPartitionBy:
      - CUSTOMER_ID
```

**`cloud_direct` excerpt:**

Copy code

```
extraction:
  strategy: cloud_direct
  externalStage: TARGET_DB.PUBLIC.DB2_STAGE
```

### Identifiers

Unquoted identifiers are folded to uppercase. Delimited identifiers use double quotes. An embedded quote is doubled (`"a""b"`).

A `whereClauseCriteria` value is DB2 SQL, written against the stored names:

Copy code

```
whereClauseCriteria: '"ID" > 1000'
```

### Partition keys

DB2 has no portable system row identifier. Don’t partition by `RID` or `ROWID`.

Use a monotonic integer primary key, or a timestamp with a narrow range. Omitting `columnNamesToPartitionBy` extracts the table as one partition.

If the key is omitted and inference runs, AIM DMV picks, in order: the primary-key index, a unique index, a non-unique index, then the first non-Boolean column. An index `INCLUDE` column is never chosen.

These types can’t be a partition key: `BLOB`, `CLOB`, `DBCLOB`, and `XML`.

DB2 migration reads ordinary base tables. External tables, Iceberg tables, and foreign tables aren’t accepted as source objects.

### Incremental sync

IBM DB2 supports [incremental sync](../manual-migration/data-migration-configuration-reference#synchronizationstrategy-model) with both the `watermark` and `checksum` strategies.

Checksum hashes column values. It skips `BLOB`, `CLOB`, `DBCLOB`, and `XML`. If every column is one of those types, the checksum is the partition row count, so a change that doesn’t change the row count isn’t detected. For those tables, use a watermark column. See [Changes a checksum may not detect](../manual-migration/data-migration-configuration-reference#changes-a-checksum-may-not-detect).

## Data type mappings

Targets match what SnowConvert emits for a DB2 table column, so a converted table, a migrated table, and validation schema comparison agree.

When `DECIMAL`, `DEC`, or `NUMERIC` has a precision, the target is `NUMBER` with that precision and scale. Scale is 0 when scale is absent. When precision isn’t in the catalog, the default is `NUMBER(20,10)`.

When `CHAR`, `CHARACTER`, `VARCHAR`, or `CHARACTER VARYING` has a length, the target is `VARCHAR` of that length. Otherwise it is `VARCHAR`.

| DB2 type | Snowflake type | Supported for migration | Notes |
| --- | --- | --- | --- |
| `SMALLINT` | `NUMBER(5,0)` | Yes |  |
| `INTEGER`, `INT` | `NUMBER(10,0)` | Yes |  |
| `BIGINT` | `NUMBER(19,0)` | Yes |  |
| `DECIMAL`, `DEC`, `NUMERIC` | `NUMBER(p,s)` | Yes | Default `NUMBER(20,10)` when precision isn’t in the catalog |
| `REAL`, `FLOAT`, `DOUBLE`, `DOUBLE PRECISION` | `FLOAT` | Yes | Row comparison uses the IEEE-754 value, so a difference that survives in the binary value is a mismatch |
| `DECFLOAT` | `DECFLOAT` | Yes | Compared as exact decimal text, not as `FLOAT`. A difference past digit 16 still mismatches. `DECFLOAT(16)` and `DECFLOAT(34)` use the same target |
| `CHAR`, `CHARACTER` | `VARCHAR` | Yes | See [Trailing blanks](#trailing-blanks) |
| `VARCHAR`, `CHARACTER VARYING` | `VARCHAR` | Yes |  |
| `CLOB`, `DBCLOB`, `NCLOB`, `LONG VARCHAR` | `VARCHAR` | Yes | See [Large values](#large-values) |
| `NCHAR` | `VARCHAR` | Yes | Blank-padded. Same trailing-blank rule as `CHAR` |
| `NVARCHAR` | `VARCHAR` | Yes |  |
| `GRAPHIC`, `VARGRAPHIC`, `LONG VARGRAPHIC` | `BINARY` | Yes | Double-byte data. Compared as bytes, not as text |
| `BINARY`, `VARBINARY`, `FOR BIT DATA` | `BINARY` | Yes |  |
| `BLOB` | `BINARY` | Yes | See [Large values](#large-values) |
| `BOOLEAN` | `BOOLEAN` | Yes |  |
| `DATE` | `DATE` | Yes |  |
| `TIME` | `TIME` | Yes | No fractional seconds. Compared as `hh:mm:ss` |
| `TIMESTAMP` | `TIMESTAMP_NTZ` | Yes | See [Fractional seconds](#fractional-seconds) |
| `XML` | `VARIANT` | Yes | Serialized to text and loaded as a string `VARIANT`. See [Large values](#large-values) |
| `ROWID` | none | No | Not mapped |

Expand

Show lessSee more

DB2 has no `INTERVAL` type. Subtracting date, time, or timestamp values produces a `DECIMAL` duration, which migrates as `NUMBER`.

### Trailing blanks

`CHAR(n)` and `NCHAR` are blank-padded. Migration reads that padded value and loads it into `VARCHAR`, so the Snowflake value keeps the trailing spaces. An empty string isn’t `NULL`. In a `CHAR` column it is stored as spaces.

Logical text comparison trims trailing blanks on the DB2 `CHAR` and `NCHAR` side before the compare. Snowflake `VARCHAR` is compared as stored. A migrated `CHAR` column isn’t guaranteed to pass logical row validation. Migration keeps the padding. Logical mode trims only the DB2 side.

Raw text comparison compares stored bytes and reports a trailing-blank or encoding difference. `GRAPHIC` isn’t part of text comparison. It is compared as binary.

Column collation is captured and can appear in schema (L1) results. Generated SQL doesn’t force a collation.

### Fractional seconds

`TIME` has no fractional seconds.

`TIMESTAMP` comparison keeps fractional digits 1 through 9, which is what Snowflake `TIMESTAMP_NTZ` stores. `TIMESTAMP(0)` through `TIMESTAMP(8)` are padded with zeros to that width. Digits 10 through 12 of `TIMESTAMP(10)` through `TIMESTAMP(12)` aren’t stored on Snowflake. A difference in digit 9 is a mismatch.

### Large values

| Type | Limit |
| --- | --- |
| `CLOB`, `LONG VARCHAR`, `NCLOB`, `DBCLOB` | Validation hashes the value. A value larger than 32,672 bytes (`CLOB`, `LONG VARCHAR`), or a `DBCLOB` or `NCLOB` that doesn’t fit in that cast, doesn’t match a truncated copy. It is reported as a mismatch. |
| `BLOB`, `LONG VARGRAPHIC` | Same limit, through a binary cast of 32,672 bytes. |
| `XML` | Migration serializes the document to text of at most 32,000 bytes and loads that text into `VARIANT`. A document whose serialization is longer isn’t a match. |

Expand

Show lessSee more

`CLOB` is excluded from column metrics (L2) because a LOB can’t be a scalar aggregate argument. Schema and row validation still include it.

## Platform-specific considerations

- The Worker uses the bundled DB2 driver. No ODBC install.
- Username and password only. Default port is 50000.
- `regular` is the default extract. Use `cloud_direct` when an object store and a matching external stage are available. Both write Parquet.
- Set an integer or timestamp partition column. DB2 has no system row id. `BLOB`, `CLOB`, `DBCLOB`, and `XML` can’t be the partition column.
- `CHAR` values keep their trailing spaces in the Snowflake `VARCHAR`.
- `XML` lands in `VARIANT` as text, up to 32,000 bytes of serialization.
- `ROWID` isn’t migrated.
- Checksum sync ignores `BLOB`, `CLOB`, `DBCLOB`, and `XML`.
- **Anti-locking**: No automatic hint is added on IBM DB2. Set `queryModifiers` only when you need a custom source SQL hint. See [Anti-locking and query modifiers](../manual-migration/data-migration-configuration-reference#anti-locking-and-query-modifiers).

**Prompt:**

Copy code

```
Set up IBM DB2 data migration for my project, and use cloud_direct when an external stage is available
```

## Related content

- [Data migration](./data-migration)
- [Validating Data from IBM DB2](./validate-db2)
- [Required privileges](./required-privileges#ibm-db2)
- [Deploying workers](./deploy-workers)
- [IBM DB2 translation reference](../code-conversion/translation-references/db2/README)
- [Manual Migration: Data migration](../manual-migration/data-migration)
