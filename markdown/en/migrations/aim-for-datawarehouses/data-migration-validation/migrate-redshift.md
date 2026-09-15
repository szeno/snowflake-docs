# Migrating Data from Amazon Redshift

This page covers Amazon Redshift-specific setup for [Data migration](./data-migration). For workflow and Worker field definitions, see [Data migration configuration reference](../manual-migration/data-migration-configuration-reference).

## Prerequisites

- **ODBC driver** on Worker hosts. Required for both **regular** and **UNLOAD** extraction.
- **S3 bucket and IAM role** when using **UNLOAD** extraction: configure `unload_s3_bucket`, `unload_s3_prefix`, and `unload_iam_role_arn` in Worker TOML so Redshift can write Parquet directly to S3. See [Using UNLOAD extraction](#using-unload-extraction).

## Connectivity and extraction strategies

Redshift supports two extraction strategies:

| Strategy | When to use | Worker requirements |
| --- | --- | --- |
| **`unload`** (recommended when prerequisites are met) | Redshift writes Parquet to S3; Snowflake loads from an external stage. Use for **all** tables once S3 and the external stage are set up. | `unload_s3_bucket`, `unload_iam_role_arn` in TOML; Snowflake external stage aligned with the bucket |
| **`regular`** | Worker pulls result sets over ODBC. Use when volume is genuinely small, or when UNLOAD prerequisites aren’t available yet. | Standard `[connections.source.redshift]` TOML only |

Expand

Show lessSee more

### Standard authentication

Copy code

```
[connections.source.redshift]
username = "myuser"
password = "mypassword"
database = "mydatabase"
host = "my-cluster.abcdef123456.us-west-2.redshift.amazonaws.com"
port = 5439
auth_method = "standard"
```

### IAM authentication (provisioned cluster)

Copy code

```
[connections.source.redshift]
username = "demo-user"
database = "demo_db"
auth_method = "iam-provisioned-cluster"
cluster_id = "my-aws-cluster"
region = "us-west-2"
access_key_id = "your-access-key-id"
secret_access_key = "your-secret-access-key"
```

### Iceberg targets

Redshift as a source doesn’t prevent **Apache Iceberg™** tables on Snowflake as targets. Set `target.tableType` to `"iceberg"` and supply `target.icebergConfig`. See [Data migration configuration reference](../manual-migration/data-migration-configuration-reference#iceberg-configuration-targeticebergconfig).

## Using UNLOAD extraction

UNLOAD is the recommended extraction strategy for Redshift when S3 and a Snowflake external stage are available. Instead of streaming result sets through the Worker over ODBC, Redshift writes Parquet files directly to S3. The Worker then stages those files into Snowflake from the external stage, skipping re-upload. Use UNLOAD for **all** tables from the source once setup is complete.

### When to use UNLOAD

Use UNLOAD (for all tables) when:

- Redshift has an IAM role with write access to an S3 bucket.
- You can create a Snowflake external stage pointing at the same S3 bucket.

Use **`regular`** only when data volume is genuinely small, or when those prerequisites aren’t in place yet.

**Prompt (when prerequisites are met):**

Copy code

```
Set up Redshift data migration using UNLOAD extraction for all tables and help me create the S3 storage integration and external stage
```

**Prompt (when S3 and the external stage aren’t ready yet, or volume is genuinely small):**

Copy code

```
Set up Redshift data migration for my project with regular extraction and the Worker connection
```

### Setup

**1. Grant Redshift permission to write to S3.**

Your Redshift cluster’s IAM role must have `s3:PutObject` and `s3:ListBucket` permissions on the target bucket.

**2. Create a Snowflake external stage** pointing at the same S3 path:

Copy code

```
CREATE STORAGE INTEGRATION my_s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/MySnowflakeRole'
  STORAGE_ALLOWED_LOCATIONS = ('s3://your-bucket/redshift-unload/');

CREATE OR REPLACE STAGE my_redshift_stage
  URL = 's3://your-bucket/redshift-unload/'
  STORAGE_INTEGRATION = my_s3_integration
  FILE_FORMAT = (TYPE = 'PARQUET');
```

**3. Add UNLOAD settings to Worker TOML:**

Copy code

```
[connections.source.redshift]
username = "myuser"
password = "mypassword"
database = "mydatabase"
host = "my-cluster.abcdef123456.us-west-2.redshift.amazonaws.com"
port = 5439
auth_method = "standard"
unload_s3_bucket = "your-bucket"
unload_s3_prefix = "redshift-unload/"
unload_iam_role_arn = "arn:aws:iam::123456789012:role/MyRole"
```

**4. Reference the stage in your workflow YAML:**

Copy code

```
tables:
  - source:
      databaseName: dev
      schemaName: public
      tableName: large_events
    target:
      databaseName: TARGET_DB
      schemaName: public
      tableName: large_events
    columnNamesToPartitionBy:
      - event_date
    extraction:
      strategy: unload
      externalStage: TARGET_DB.PUBLIC.MY_REDSHIFT_STAGE
```

## Data type mappings

| Redshift type | Snowflake target type | Supported for migration | Notes |
| --- | --- | --- | --- |
| SMALLINT, INTEGER, BIGINT | NUMBER | Yes |  |
| DECIMAL / NUMERIC | NUMBER | Yes |  |
| REAL | FLOAT | Yes |  |
| DOUBLE PRECISION | FLOAT | Yes |  |
| BOOLEAN | BOOLEAN | Yes |  |
| DATE | DATE | Yes |  |
| TIMESTAMP | TIMESTAMP\_NTZ | Yes |  |
| CHAR, VARCHAR | VARCHAR | Yes |  |
| VARBYTE / BINARY VARYING | BINARY | Yes |  |
| TIMESTAMPTZ | TIMESTAMP\_TZ | Yes |  |
| TIME | TIME | Yes |  |
| TIMETZ | TIMESTAMP\_TZ | Yes | The date component is set to `1970-01-01` |
| INTERVALY2M, INTERVALD2S | INTERVAL | Yes | Native `INTERVAL` by default. See [INTERVAL data type handling](../manual-migration/data-migration-configuration-reference#interval-data-type-handling). |
| GEOMETRY | GEOMETRY | Yes | Extracted as Well-Known Text |
| GEOGRAPHY | GEOGRAPHY | Yes | Extracted as Well-Known Text |
| HLLSKETCH |  | No |  |
| SUPER | VARIANT | Yes |  |

Expand

Show lessSee more

## Platform-specific considerations

- **Server-side export (UNLOAD)**: Prefer UNLOAD for all tables once S3, the Redshift IAM role, and the Snowflake external stage are in place. Reserve **`regular`** for genuinely small volume or when those prerequisites aren’t set up yet. See [Using UNLOAD extraction](#using-unload-extraction).
- Use UNLOAD + larger `partitionSize` targets when UNLOAD produces large Parquet files from wide tables. `partitionSize: "auto"` works well in most cases.
- When using IAM authentication, confirm the Redshift IAM role has both S3 write access and the correct trust relationship for your cluster.
- For tables migrated via UNLOAD, keep the source cluster accessible during validation. Cloud Data Validation runs SQL against live Redshift even when the original migration used UNLOAD.
- **Anti-locking**: No automatic hint is added on Redshift. Set `queryModifiers` only when you need custom source SQL hints. See [Anti-locking and query modifiers](../manual-migration/data-migration-configuration-reference#anti-locking-and-query-modifiers).

## Related content

- [Data migration](./data-migration)
- [Validating Data from Amazon Redshift](./validate-redshift)
- [Manual Migration: Data migration](../manual-migration/data-migration)
