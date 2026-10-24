# Migrating Data from Google BigQuery

This page covers Google BigQuery-specific setup for [Data migration](./data-migration). For workflow and Worker field definitions, see [Data migration configuration reference](../manual-migration/data-migration-configuration-reference).

## Prerequisites

- **Worker client**: The Worker image includes the `google-cloud-bigquery` client. You don’t install an ODBC or JDBC driver.
- **Authentication**: A Google Cloud service-account key file, or Application Default Credentials on the Worker host. On Snowpark Container Services, pass the key as a Snowflake secret. See [Google BigQuery](../manual-migration/manual-spcs-worker-setup#google-bigquery).
- **Network**: The Worker must reach the BigQuery API. A Worker on Snowpark Container Services needs an external access integration that allows the BigQuery hosts. See [Deploying workers](./deploy-workers).
- **Privileges**: Read access on the dataset and permission to run query jobs in the billing project. `export_data` also needs write access to the GCS prefix. See [Google BigQuery](./required-privileges#google-bigquery).

## Connectivity and extraction

`project_id` is the Google Cloud project that runs the query jobs and is billed for them. `dataset` is the default dataset. `location` is the BigQuery job location, and defaults to `US`.

Copy code

```
[connections.source.bigquery]
project_id = "my-gcp-project"
dataset = "sales"
location = "US"
credentials_file = "/secrets/bigquery-sa.json"
```

When `credentials_file` is omitted, the Worker uses Application Default Credentials. Set `query_labels` (`"name=value;name2=value2"`) to tag every query job so you can find the migration’s jobs in `INFORMATION_SCHEMA.JOBS`.

In the workflow, `source.databaseName` is the project and `source.schemaName` is the dataset.

AIM DMV accepts two extraction strategies:

| Strategy | When to use |
| --- | --- |
| `regular` | Default when the workflow omits a strategy. The Worker runs the query through the BigQuery API, writes Parquet locally, and uploads it to a Snowflake internal stage. Doesn’t need GCS. |
| `export_data` | Recommended for large tables when you have a GCS bucket and a Snowflake external stage on the same prefix. BigQuery `EXPORT DATA` writes Parquet to GCS, and Snowflake loads it from the external stage. The rows don’t pass through the Worker. |

Expand

Show lessSee more

BigQuery doesn’t support `cloud_direct`.

**Workflow example:**

Copy code

```
tables:
  - source:
      databaseName: my-gcp-project
      schemaName: sales
      tableName: customers
    target:
      databaseName: TARGET_DB
      schemaName: PUBLIC
      tableName: CUSTOMERS
    columnNamesToPartitionBy:
      - customer_id
```

### Using EXPORT DATA

Add the GCS bucket to the Worker connection:

Copy code

```
[connections.source.bigquery]
project_id = "my-gcp-project"
dataset = "sales"
location = "US"
credentials_file = "/secrets/bigquery-sa.json"
export_data_gcs_bucket = "my-migration-bucket"
export_data_gcs_prefix = "bigquery-exports"
```

| Property | Description |
| --- | --- |
| `export_data_gcs_bucket` | Required for `export_data`. GCS bucket, without `gs://`. |
| `export_data_gcs_prefix` | Optional. Path prefix inside the bucket. |
| `export_data_file_format` | Optional. `parquet` (default) or `csv`. |
| `export_data_overwrite` | Optional. Defaults to `true`, so a rerun replaces earlier files under the same path. |

Expand

Show lessSee more

Then point the workflow at a Snowflake external stage whose URL covers that bucket and prefix:

Copy code

```
extraction:
  strategy: export_data
  externalStage: TARGET_DB.PUBLIC.GCS_EXPORT_STAGE
```

The identity that runs the BigQuery job needs `storage.objects.create` and `storage.objects.delete` on the prefix. The Snowflake storage integration needs read access to the same prefix. Stage URLs often use `gcs://` while the Worker uses `gs://`. Both refer to the same bucket. See [Google Cloud Storage](./required-privileges#l3-extraction-gcs-iam).

### Identifiers

BigQuery identifiers are case-preserving. Quoted identifiers use backticks. The fully qualified name is `project.dataset.table`.

A `whereClauseCriteria` value is BigQuery SQL, written against the stored names:

Copy code

```
whereClauseCriteria: 'order_date >= DATE "2024-01-01"'
```

### Partition keys

Use a monotonic integer key, or a date or timestamp with a narrow range. Omitting `columnNamesToPartitionBy` extracts the table as one partition.

If the key is omitted and inference runs, AIM DMV picks, in order: the clustering columns, the primary-key constraint columns, then the first non-Boolean column.

These types can’t be a partition key, because BigQuery can’t sort them: `ARRAY`, `STRUCT`, `JSON`, and `GEOGRAPHY`.

### Incremental sync

Google BigQuery supports [incremental sync](../manual-migration/data-migration-configuration-reference#synchronizationstrategy-model) with both the `watermark` and `checksum` strategies.

The default checksum fingerprints each row with `FARM_FINGERPRINT` and combines the fingerprints with `BIT_XOR`. Two identical rows cancel each other out, so adding or removing a pair of duplicate rows isn’t detected. For tables that can hold duplicate rows, use a watermark column or a custom `checksumExpression`. See [Changes a checksum may not detect](../manual-migration/data-migration-configuration-reference#changes-a-checksum-may-not-detect).

## Data type mappings

When `NUMERIC` or `DECIMAL` has a precision, the target is `NUMBER` with that precision and scale. When `STRING(n)` or `BYTES(n)` has a length, the target keeps that length.

| BigQuery type | Snowflake type | Supported for migration | Notes |
| --- | --- | --- | --- |
| `INT64`, `INT`, `INTEGER`, `SMALLINT`, `BIGINT`, `TINYINT`, `BYTEINT` | `INT` | Yes |  |
| `NUMERIC`, `DECIMAL` | `NUMBER(p,s)` | Yes |  |
| `BIGNUMERIC`, `BIGDECIMAL` | `DECFLOAT` or `NUMBER(p,s)` | Yes | A bare `BIGNUMERIC` becomes `DECFLOAT`. `BIGNUMERIC(p,s)` becomes `NUMBER(p,s)`, with precision clamped to 38. Extracted as text, so no digits are lost in transit |
| `FLOAT64` | `FLOAT` | Yes |  |
| `BOOL` | `BOOLEAN` | Yes |  |
| `STRING` | `VARCHAR` | Yes | `STRING(n)` becomes `VARCHAR(n)` |
| `BYTES` | `BINARY` | Yes | `BYTES(n)` becomes `BINARY(n)` |
| `DATE` | `DATE` | Yes |  |
| `TIME` | `TIME` | Yes |  |
| `DATETIME` | `TIMESTAMP_NTZ` | Yes | Extracted as ISO 8601 text with microseconds |
| `TIMESTAMP` | `TIMESTAMP_TZ` | Yes | Extracted as ISO 8601 text in UTC with microseconds |
| `JSON` | `VARIANT` | Yes | Extracted as JSON text |
| `STRUCT` | `VARIANT` | Yes | Extracted as JSON text |
| `ARRAY` | `ARRAY` | Yes | Extracted as JSON text |
| `GEOGRAPHY` | `GEOGRAPHY` | Yes | Extracted as WKT |
| `INTERVAL` | `VARCHAR` | Yes | Extracted as the canonical interval text (`Y-M D H:M:S[.F]`). The text can exceed 30 characters, so the target is unbounded |

Expand

Show lessSee more

To keep a different target type, set `columnTypeMappings` or a `customColumnTransforms` target type in the workflow. A type you choose wins over the `DECFLOAT` default for `BIGNUMERIC`.

## Platform-specific considerations

- The Worker uses the pre-installed `google-cloud-bigquery` client. No ODBC install.
- Authenticate with a service-account key or Application Default Credentials. On Snowpark Container Services, use the base64 secret `BIGQUERY_CREDENTIALS_JSON_BASE64`.
- `regular` is the default extract. Use `export_data` when a GCS bucket and a matching external stage are available. `cloud_direct` isn’t supported.
- Query jobs run and are billed in `project_id`.
- `ARRAY`, `STRUCT`, `JSON`, and `GEOGRAPHY` can’t be the partition column.
- A bare `BIGNUMERIC` lands in `DECFLOAT`.
- Checksum sync doesn’t detect a change that adds or removes a pair of identical rows.
- **Anti-locking**: BigQuery reads don’t take locks, so no hint is added.

**Prompt:**

Copy code

```
Set up Google BigQuery data migration for my project, and use export_data with my GCS bucket and external stage
```

## Related content

- [Data migration](./data-migration)
- [Validating Data from Google BigQuery](./validate-bigquery)
- [Required privileges](./required-privileges#google-bigquery)
- [Deploying workers](./deploy-workers)
- [BigQuery translation reference](../code-conversion/translation-references/bigquery/README)
- [Manual Migration: Data migration](../manual-migration/data-migration)
