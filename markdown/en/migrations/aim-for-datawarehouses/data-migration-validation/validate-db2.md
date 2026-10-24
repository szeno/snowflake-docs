# Validating Data from IBM DB2

AIM DMV migrates and validates data from IBM DB2 for Linux, UNIX, and Windows (LUW).

This page covers IBM DB2-specific setup for [Data validation](./data-validation). For workflow field definitions, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

## Prerequisites

- **Worker driver**: Same bundled DB2 driver as [Migrating Data from IBM DB2](./migrate-db2). You don’t install a DB2 ODBC driver.
- **Authentication**: Username and password only. SSL, LDAP, and Kerberos aren’t supported.
- **Worker path**: IBM DB2 validation runs on the Worker. It doesn’t use the local in-process validation engine.
- **Privileges**: `SELECT` on every table or view being validated. See [IBM DB2](./required-privileges#ibm-db2).

## Connectivity

Reuse `[connections.source.db2]` Worker TOML from data migration. `[connections.source.db2].database` must match the database in the validation workflow.

Copy code

```
[connections.source.db2]
username = "myuser"
password = "your_password"
database = "SAMPLE"
host = "db2.example.com"
port = "50000"
```

Set `source_platform: db2` in the validation workflow YAML.

Row validation uses the same two transports as migration. With a bucket, prefer `cloud_direct`. Without a bucket, `regular` extracts through the Worker to an internal stage. `regular` doesn’t need an external stage. When row validation uses object storage, set `extraction.strategy` to `cloud_direct` and `extraction.externalStage` to the stage name. When more than one of `[connections.target.s3]`, `[connections.target.gcs]`, and `[connections.target.blob]` is present, the Worker prefers S3, then GCS, then Azure Blob, unless the workflow sets `storageBackend`. See [L3 extraction](../manual-migration/data-validation-configuration-reference#l3-extraction).

**Example workflow excerpt:**

Copy code

```
source_platform: db2
target_database: TARGET_DB
schema_mappings:
  MYSCHEMA: PUBLIC
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false
tables:
  - fully_qualified_name: MYSCHEMA.CUSTOMERS
    column_names_to_partition_by:
      - CUSTOMER_ID
  - fully_qualified_name: MYSCHEMA.ORDERS
    column_names_to_partition_by:
      - ORDER_ID
    validation_configuration:
      row_validation: true
```

Validation can compare a DB2 view with a Snowflake view. Ask for that the same way you ask for a table.

## Data type mappings

The target types are the same as [Migrating Data from IBM DB2](./migrate-db2#data-type-mappings). Schema comparison uses those mapped Snowflake types.

| DB2 type | Snowflake type | Supported for validation | Notes |
| --- | --- | --- | --- |
| `SMALLINT` | `NUMBER(5,0)` | Yes |  |
| `INTEGER`, `INT` | `NUMBER(10,0)` | Yes |  |
| `BIGINT` | `NUMBER(19,0)` | Yes |  |
| `DECIMAL`, `DEC`, `NUMERIC` | `NUMBER(p,s)` | Yes | Default `NUMBER(20,10)` when precision isn’t in the catalog |
| `REAL`, `FLOAT`, `DOUBLE`, `DOUBLE PRECISION` | `FLOAT` | Yes | Compared as the IEEE-754 value. A difference that survives in the binary value is a mismatch |
| `DECFLOAT` | `DECFLOAT` | Yes | Exact decimal text, not `FLOAT`. A difference past digit 16 still mismatches |
| `CHAR`, `CHARACTER`, `NCHAR` | `VARCHAR` | Yes | See [Trailing blanks](./migrate-db2#trailing-blanks). Logical mode trims the DB2 side. The migrated `VARCHAR` keeps trailing spaces |
| `VARCHAR`, `CHARACTER VARYING`, `NVARCHAR` | `VARCHAR` | Yes |  |
| `CLOB`, `DBCLOB`, `NCLOB`, `LONG VARCHAR` | `VARCHAR` | Yes | Hashed. A value larger than 32,672 bytes, or a `DBCLOB` or `NCLOB` that doesn’t fit in that cast, is a mismatch against a truncated copy. `CLOB` is omitted from L2 metrics |
| `GRAPHIC`, `VARGRAPHIC`, `LONG VARGRAPHIC` | `BINARY` | Yes | Compared as bytes, not as text |
| `BINARY`, `VARBINARY`, `FOR BIT DATA` | `BINARY` | Yes |  |
| `BLOB` | `BINARY` | Yes | Binary cast of 32,672 bytes. A larger value doesn’t match a truncated copy |
| `BOOLEAN` | `BOOLEAN` | Yes |  |
| `DATE` | `DATE` | Yes |  |
| `TIME` | `TIME` | Yes | No fractional seconds. Compared as `hh:mm:ss` |
| `TIMESTAMP` | `TIMESTAMP_NTZ` | Yes | Digits 1 through 9 are kept. Digits 10 through 12 aren’t stored on Snowflake. A difference in digit 9 is a mismatch |
| `XML` | `VARIANT` | Yes | Text serialization of at most 32,000 bytes, loaded as a string `VARIANT`. A longer serialization isn’t a match |
| `ROWID` | none | No | Not validated |

Expand

Show lessSee more

Text comparison mode accepts `logical` (default) and `raw`. Raw comparison compares stored bytes and reports a trailing-blank or encoding difference.

## Validation levels

| Level | IBM DB2 behavior |
| --- | --- |
| L1 schema | Compares the mapped Snowflake type. Collation can be reported. Generated SQL doesn’t force a collation. |
| L2 metrics | Numeric, character, datetime, and Boolean metrics. `CLOB` is omitted. Integer averages and character lengths are aligned with Snowflake. |
| L3 rows | Supported, including hybrid mode: a row hash, then cell drill-down only where the hash mismatches. `FLOAT` uses IEEE-754. `DECFLOAT` uses exact decimal text. |

Expand

Show lessSee more

## Platform-specific considerations

- Reuse the same `[connections.source.db2]` Worker block as migration.
- Set `source_platform: db2`.
- Schema, metrics, and row validation are all available. Ask for row validation per table.
- Prefer `cloud_direct` for row validation when a bucket and a matching external stage exist. Otherwise use `regular`.
- `ROWID` isn’t validated.
- **Anti-locking**: No automatic hint is added on IBM DB2. Set `queryModifiers` only when you need a custom source SQL hint. See [Anti-locking and query modifiers](../manual-migration/data-validation-configuration-reference#anti-locking-and-query-modifiers).

**Prompt:**

Copy code

```
Run cloud data validation for my IBM DB2 tables, with schema and metrics validation on all tables and row-level validation on CUSTOMERS
```

## Related content

- [Data validation](./data-validation)
- [Migrating Data from IBM DB2](./migrate-db2)
- [Required privileges](./required-privileges#ibm-db2)
- [IBM DB2 translation reference](../code-conversion/translation-references/db2/README)
- [Manual Migration: Data validation](../manual-migration/data-validation)
