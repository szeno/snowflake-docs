# Validating Data from Google BigQuery

This page covers Google BigQuery-specific setup for [Data validation](./data-validation). For workflow field definitions, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

## Prerequisites

- **Worker client**: Same pre-installed `google-cloud-bigquery` client as [Migrating Data from Google BigQuery](./migrate-bigquery). You don’t install an ODBC or JDBC driver.
- **Authentication**: A service-account key file or Application Default Credentials, the same as migration.
- **Live BigQuery access** for L1 and L2. Schema and metrics validation always run SQL against BigQuery.
- **L3 object storage (Recommended)**: Use **EXPORT DATA** (`extraction.strategy: export_data`) so signatures land on **GCS**, with the same Worker `export_data_*` TOML and Snowflake external stage as migration. See [Object storage backends](../manual-migration/data-validation-configuration-reference#l3-extraction-object-storage) and [Google Cloud Storage](./required-privileges#l3-extraction-gcs-iam).
- **Privileges**: Read access on the dataset and `bigquery.jobs.create` in the billing project. See [Google BigQuery](./required-privileges#google-bigquery).

## Connectivity

Reuse `[connections.source.bigquery]` Worker TOML from data migration:

Copy code

```
[connections.source.bigquery]
project_id = "my-gcp-project"
dataset = "sales"
location = "US"
credentials_file = "/secrets/bigquery-sa.json"
export_data_gcs_bucket = "my-migration-bucket"
export_data_gcs_prefix = "bigquery-validation"
```

Set `source_platform: bigquery` in the validation workflow YAML.

Row validation supports `export_data` and `regular`. With a GCS bucket, prefer `export_data` and set `extraction.externalStage` to a stage on the same prefix. Without a bucket, `regular` extracts the signatures through the Worker to the internal stage. `cloud_direct` isn’t supported. See [L3 extraction](../manual-migration/data-validation-configuration-reference#l3-extraction).

**Example workflow excerpt:**

Copy code

```
source_platform: bigquery
target_database: TARGET_DB
schema_mappings:
  sales: PUBLIC
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false
  extraction:
    strategy: export_data
    externalStage: TARGET_DB.PUBLIC.GCS_EXPORT_STAGE
tables:
  - fully_qualified_name: sales.customers
    column_names_to_partition_by:
      - customer_id
  - fully_qualified_name: sales.orders
    column_names_to_partition_by:
      - order_id
    validation_configuration:
      row_validation: true
```

## Data type mappings

The target types are the same as [Migrating Data from Google BigQuery](./migrate-bigquery#data-type-mappings). L3 compares each value in a canonical text form, so the notes below describe how a value has to match.

| BigQuery type | Snowflake type | Supported for validation | Notes |
| --- | --- | --- | --- |
| `INT64` and its aliases | `INT` | Yes |  |
| `NUMERIC`, `DECIMAL` | `NUMBER(p,s)` | Yes | Compared at the column’s scale |
| `BIGNUMERIC`, `BIGDECIMAL` | `DECFLOAT` or `NUMBER(p,s)` | Yes | A `DECFLOAT` target is compared as exact decimal text. A value past 38 digits is a mismatch. Precision above 38 or scale above 37 is an L1 warning, not a failure |
| `FLOAT64` | `FLOAT` | Yes | Compared as the IEEE-754 value. A difference that survives in the binary value is a mismatch |
| `BOOL` | `BOOLEAN` | Yes |  |
| `STRING` | `VARCHAR` | Yes |  |
| `BYTES` | `BINARY` | Yes | Compared as uppercase hex |
| `DATE` | `DATE` | Yes |  |
| `TIME` | `TIME` | Yes | Compared at the fractional precision both sides keep |
| `DATETIME` | `TIMESTAMP_NTZ` | Yes |  |
| `TIMESTAMP` | `TIMESTAMP_TZ` | Yes | Compared as the UTC instant |
| `JSON`, `STRUCT`, `ARRAY` | `VARIANT`, `ARRAY` | Yes | Compared as JSON text with object keys sorted, so key order doesn’t cause a mismatch |
| `GEOGRAPHY` | `GEOGRAPHY` | Yes | Compared as WKT, with spacing differences between BigQuery and Snowflake removed |
| `INTERVAL` | `VARCHAR` | Yes | Compared as text |

Expand

Show lessSee more

Numeric values with more than 28 integer digits can’t be rendered in the shared comparison format and report as a mismatch. This limit applies to every source platform.

## Validation levels

| Level | Google BigQuery behavior |
| --- | --- |
| L1 schema | Compares the mapped Snowflake type. BigQuery doesn’t expose numeric precision and scale as columns, so AIM DMV parses them from the declared type. |
| L2 metrics | Column metrics for every mapped type, including `JSON`, `STRUCT`, `ARRAY`, `GEOGRAPHY`, and `INTERVAL`. |
| L3 rows | Supported, including hybrid mode: a row hash, then cell drill-down only where the hash mismatches. `FLOAT64` uses IEEE-754. A `DECFLOAT` target uses exact decimal text. |

Expand

Show lessSee more

## Platform-specific considerations

- Reuse the same `[connections.source.bigquery]` Worker block as migration.
- Set `source_platform: bigquery`.
- Schema, metrics, and row validation are all available. Ask for row validation per table.
- Prefer `export_data` for row validation when a GCS bucket and a matching external stage exist. Otherwise use `regular`.
- Validation queries run and are billed in `project_id`.
- **Anti-locking**: BigQuery reads don’t take locks, so no hint is added.

**Prompt:**

Copy code

```
Run cloud data validation for my BigQuery tables, with schema and metrics validation on all tables and row-level validation on orders using export_data
```

## Related content

- [Data validation](./data-validation)
- [Migrating Data from Google BigQuery](./migrate-bigquery)
- [Required privileges](./required-privileges#google-bigquery)
- [BigQuery translation reference](../code-conversion/translation-references/bigquery/README)
- [Manual Migration: Data validation](../manual-migration/data-validation)
