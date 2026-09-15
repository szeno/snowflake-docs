# Storage for Apache Iceberg™ tables

Apache Iceberg™ tables in Snowflake support two storage options for table data and metadata. Choose the one that
matches how you want to manage table files.

## Storage options

- **Snowflake storage (recommended)** — Snowflake stores and manages the Iceberg table files for you. You don’t
  configure or grant access to any external cloud storage. Set `EXTERNAL_VOLUME = SNOWFLAKE_MANAGED`
  on `CREATE ICEBERG TABLE`, or rely on schema, database, or account defaults. For details, see
  [Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage).
- **External volume storage** — Snowflake reads and writes Iceberg table files in your own cloud storage
  through an external volume that you create and configure. Use this option when you need to keep table
  files in your cloud account or when you use an external Iceberg catalog. For details, see
  [External volume storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-managing-external-volumes).

The following table compares the two options:

|  | Snowflake storage | External volume storage |
| --- | --- | --- |
| **Setup** | None. Set `EXTERNAL_VOLUME = SNOWFLAKE_MANAGED` or rely on defaults. | Configure cloud storage access and create an [external volume](/sql-reference/sql/create-external-volume) object. |
| **Where table files live** | In Snowflake-provided storage. | In your cloud storage account (Amazon S3, Google Cloud Storage, Azure, or S3-compatible). |
| **Supported Iceberg catalogs** | Snowflake-managed only. | Snowflake-managed or external (for example, AWS Glue, Iceberg REST, Snowflake Open Catalog). |
| **Bucket management** | Not required. Snowflake provides and manages the storage. | You create and manage the cloud storage buckets that hold table files. |
| **Bucket security, IAM, and lifecycle policies** | Handled automatically by Snowflake. | You configure these separately for each storage account or bucket. |
| **File sharding across partitions** | Handled automatically by Snowflake. | You manage how data files are sharded across partitions. |
| **Fail-safe protection** | Yes for permanent tables. Transient tables are also supported. | Not provided. You’re responsible for protecting files in your cloud storage. |
| **Best for** | Zero-ops setup for new or existing workloads. | Existing data on cloud buckets or tables that use an external Iceberg catalog. |

Expand

Show lessSee more

## Cost considerations

The two storage options have different cost structures. The following table summarizes the differences.

|  | Snowflake storage | External volume storage |
| --- | --- | --- |
| **Cloud storage API request cost** | No charges when you use the Snowflake engine. Billed when you use an external engine. | Billed by your cloud provider at standard API rates (for example, S3 GET, PUT, and LIST). Can be a notable portion of total storage cost. |
| **Data compaction** | Handled automatically and free when Snowflake writes to the table. | Additional charge that varies with the workload. |
| **Orphan files** | Snowflake manages cleanup. You don’t pay for orphan files. | You’re responsible for detecting and cleaning up orphan files. Cloud storage for orphan files is billed by your cloud provider. |

Expand

Show lessSee more

## Snowflake storage

Iceberg tables can use Snowflake-provided storage with no external configuration. Set
`EXTERNAL_VOLUME = SNOWFLAKE_MANAGED` on `CREATE ICEBERG TABLE`, or rely on schema, database, or account defaults.
Snowflake stores and manages the Iceberg table data and metadata files for you and supports Fail-safe data
protection for permanent tables.

For details, including how to create tables that use Snowflake storage, replication considerations, and billing,
see [Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage).

## External volume storage

External volume storage uses your own cloud storage. You create an external volume that points to a location in
Amazon S3, Google Cloud Storage, Azure Storage, or an S3-compatible storage system, and grant Snowflake access
through a cloud principal. Tables that use an external Iceberg catalog must use external volume storage.

For details, including how to grant Snowflake access to your storage, how Snowflake organizes table files in your
storage, encryption, replication, and how to protect files with versioning, see
[External volume storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-managing-external-volumes).
