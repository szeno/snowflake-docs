# External volume storage for Apache Iceberg™ tables

This topic describes how Iceberg tables work when they use *external volume storage*, which means
storage in your own cloud account that Snowflake accesses through an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def).
Use this storage option when you need to store your Iceberg table data in your own cloud storage
or when you use an external Iceberg catalog.

If you don’t have these requirements, consider using [Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage),
which removes the need to configure external volumes for tables that use Snowflake as the Iceberg catalog.

For an overview of both storage options, see [Storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-storage).

## Tasks

- [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume) — Configure an external volume so that Snowflake can read from and write to your cloud storage.
- [Drop an external volume by using Snowsight](/user-guide/tables-iceberg-drop-external-volume) — Drop an external volume that’s no longer in use.

## External volumes

Note

To connect Snowflake to your external cloud storage for Iceberg tables without using an external volume, use catalog-vended
credentials. This option is only available for externally managed Iceberg tables.
For more information, see [Use catalog-vended credentials for Apache Iceberg™ tables](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials).

An external volume is a named, account-level Snowflake object that you use to connect Snowflake to your
external cloud storage for Iceberg tables. An external volume stores an identity and access management (IAM) entity
for your storage location. Snowflake uses the IAM entity to securely connect to your storage for accessing
table data, Iceberg metadata, and manifest files that store the table schema, partitions, and other metadata.

A single external volume can support one or more Iceberg tables.

Each external volume is associated with a particular [Active storage location](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-ext-vol-active-storage-location),
and a single external volume can support multiple Iceberg tables. However, the number of external volumes you need depends on how you want to store,
organize, and secure your table data.

You can use a single external volume if you want the data and metadata
for *all* of your Snowflake-Iceberg tables in subdirectories under the same storage location (for example, in the same S3 bucket).
To configure these directories for Snowflake-managed tables, see [Data and metadata directories](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location).

Alternatively, you can create multiple external volumes to secure various storage locations differently. For example,
you might create the following external volumes:

- A read-only external volume for externally managed Iceberg tables.
- An external volume configured with read and write access for Snowflake-managed tables.

## Granting Snowflake access to your storage

### Cloud provider storage

To grant Snowflake access to your cloud storage locations for Iceberg tables,
you use the identity and access management service for your cloud provider.
You grant an identity, or principal, limited access to your storage without exchanging secrets.
This is the same access model that Snowflake uses for other integrations, including storage integrations.

Snowflake provisions a principal for your entire Snowflake account when you create an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def).
The principal is as follows, depending on your cloud provider:

| Cloud provider | Snowflake-provisioned principal |
| --- | --- |
| Amazon Web Services (AWS) | [IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-users) |
| Google Cloud | [Service account](https://cloud.google.com/iam/docs/overview#service_account) |
| Azure | [Service principal](https://learn.microsoft.com/en-us/entra/identity-platform/app-objects-and-service-principals?tabs=browser#service-principal-object) |

Expand

Show lessSee more

Snowflake authenticates directly with your storage provider, and the Snowflake-provisioned principal assumes a role that you specify.
The role must have permission to perform operations on your storage location.
For example, Snowflake can read from a storage location only if the role has permission to read from that storage location.

Snowflake requires permission to perform the following actions on Iceberg tables:

|  | Snowflake-managed tables | Tables that use an external Iceberg catalog |
| --- | --- | --- |
| **Amazon S3** | - `s3:GetBucketLocation` - `s3:GetObject` - `s3:ListBucket` - `s3:PutObject` - `s3:DeleteObject` - `s3:GetObjectVersion` - `s3:DeleteObjectVersion` | - `s3:GetBucketLocation` - `s3:GetObject` - `s3:ListBucket` - `s3:GetObjectVersion` |
| **Google Cloud Storage** | - `storage.objects.create` - `storage.objects.delete` - `storage.objects.get` - `storage.objects.list` | - `storage.buckets.get` - `storage.objects.get` - `storage.objects.list` |
| **Azure Storage** | All allowed actions for the [Storage Blob Data Contributor role](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/storage#storage-blob-data-contributor) | All allowed actions for the [Storage Blob Data Reader role](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/storage#storage-blob-data-reader) |

Expand

Show lessSee more

Note

For **Iceberg tables created from Delta table files (Delta Direct)** with read-only requirements, grant only the read actions for your cloud provider (for example `s3:GetObject` without `s3:PutObject` on Amazon S3) and set `ALLOW_WRITES` to `FALSE` on the external volume so that permissions match Snowflake behavior. For provider-specific action lists, see [Read-only vs write access for Delta Direct on each storage provider](/user-guide/tables-iceberg-metadata#label-tables-iceberg-ev-delta-read-write-options).

Note

The `s3:PutObject` permission grants write access to the external volume location.
To completely configure write access, you must set the `ALLOW_WRITES` parameter of the external volume to `TRUE` (the default value).

For full instructions on granting Snowflake access to your storage for Iceberg tables, see the following topics:

- [Configure an external volume for Amazon S3](/user-guide/tables-iceberg-configure-external-volume-s3)
- [Configure an external volume for Google Cloud Storage](/user-guide/tables-iceberg-configure-external-volume-gcs)
- [Configure an external volume for Azure](/user-guide/tables-iceberg-configure-external-volume-azure)

### S3-compatible storage

To grant Snowflake access to an [S3-compatible storage location](/user-guide/data-load-s3-compatible-storage) for Iceberg tables,
you specify an [S3-compatible storage endpoint](/user-guide/data-load-s3-compatible-storage#label-data-load-s3-compatible-storage-reqs) with credentials when you create an external volume.

For instructions, see [Configure an external volume for S3-compatible storage](/user-guide/tables-iceberg-s3-compatible).

## Active storage location

Each external volume supports a single active storage location.
If you specify multiple storage locations in a [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) statement,
Snowflake assigns one location as the active location.
The active location remains the same for the lifetime of the external volume.

Assignment occurs the first time you use the external volume in a CREATE ICEBERG TABLE statement.
Snowflake uses the following logic to choose an active location:

- If the `STORAGE_LOCATIONS` list contains one or more *local* storage locations, Snowflake uses the first local storage location in the list.
  A local storage location is one with the same cloud provider and in the same region as your Snowflake account.
- If the `STORAGE_LOCATIONS` list does not contain any local storage locations, Snowflake selects the first location in the list.

Note

External volumes that were created before Snowflake version 7.44 might have used different logic to select an active location.

## Verifying storage access

Note

To verify storage access by using Snowsight, see [Verify an external volume by using Snowsight](/user-guide/tables-iceberg-configure-external-volume#label-tables-iceberg-configure-external-volume-verify-snowsight)

To check that Snowflake can successfully authenticate to your storage provider, call the [SYSTEM$VERIFY\_EXTERNAL\_VOLUME](/sql-reference/functions/system_verify_external_volume)
function.

Copy code

```
SELECT SYSTEM$VERIFY_EXTERNAL_VOLUME('my_external_volume');
```

Note

If you receive the following error, your account administrator must activate AWS STS in the Snowflake deployment region.
For instructions, see
[Manage AWS STS in an AWS Region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html)
in the AWS documentation.

```
Error assuming AWS_ROLE:
STS is not activated in this region for account:<external volume id>. Your account administrator can activate STS in this region using the IAM Console.
```

For Snowflake-managed tables, Snowflake automatically verifies access to the [active storage location](#label-tables-iceberg-ext-vol-active-storage-location)
on your external volume in the following situations:

- The first time you specify that external volume in a CREATE ICEBERG TABLE statement for a Snowflake-managed table.
- The first time you convert a table to use Snowflake as the Iceberg catalog.

The `ALLOW_WRITES` property of the external volume must be set to `TRUE`.

Snowflake tries the following storage operations to verify the storage location.

1. Writing a test file.
2. Reading the file.
3. Listing the contents of the file’s path.
4. Deleting the file.

If any one of the operations fails,
the CREATE ICEBERG TABLE (or ALTER ICEBERG TABLE … CONVERT TO MANAGED) statement fails and you receive an error message.

## File management

This section explains how management of Iceberg table files in storage works, according to the type of Iceberg table.

### Snowflake-managed tables

Important

- Don’t allow other tools access to delete or overwrite objects that are associated with Snowflake-managed Iceberg tables.
- Ensure that the Snowflake principal maintains access to your table storage.
  For more information, see [Granting Snowflake access to your storage](#label-tables-iceberg-grant-access-to-storage).

Though *you* configure and manage storage locations for Iceberg tables, Snowflake exclusively operates on the objects
in your storage (data and metadata files) that belong to Snowflake-managed tables. Snowflake runs periodic maintenance
on these table objects to optimize query performance and clean up deleted data.

Queries might fail if other tools delete or overwrite Snowflake-managed table objects.
Similarly, queries on the table and Snowflake’s table maintenance operations will fail
if you revoke the Snowflake principal’s access to your storage.

Snowflake deletes objects after the table retention period expires when Snowflake-managed table data is deleted or the table is dropped.

To configure replication for Snowflake-managed Iceberg tables, see [Configure replication for Snowflake-managed Iceberg tables](#label-tables-iceberg-configure-replication-snowflake-managed-iceberg-tables).

#### Data and metadata directories

This section describes the data and metadata directories for Snowflake-managed tables.

These directories can either be organized in a flat or hierarchical layout:

- [Flat layout](#label-tables-iceberg-snowflake-managed-flat-layout)
- [Hierarchical layout](#label-tables-iceberg-snowflake-managed-hierarchical-layout)

Note

To find the data and metadata directories for any Iceberg table, you can use the [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) command.
The command output includes a `base_location` property that indicates the location of each table’s data and metadata files.

##### Flat layout

This section describes the flat layout in Snowflake for data and metadata directories for Snowflake-managed tables.

When you create a Snowflake-managed table that uses the default flat directory layout (PATH\_LAYOUT = FLAT), Snowflake writes all Parquet
data files under a single `data/` directory and all table metadata data files under a single `metadata/` directory. Snowflake also writes
metadata for [Delta-based tables](/user-guide/tables-iceberg-metadata#label-tables-iceberg-metadata-delta).

Snowflake constructs paths using the following patterns, depending on the values specified
for [BASE\_LOCATION](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-snowflake-base-location) or
the [BASE\_LOCATION\_PREFIX](/sql-reference/parameters#label-base-location-prefix) parameter.
If you specify a `BASE_LOCATION`, Snowflake does not use the BASE\_LOCATION\_PREFIX in the path.

Where:

- `STORAGE_BASE_URL` is the base URL for the active storage location associated with your external volume.
- `BASE_LOCATION` is the path for a directory where Snowflake should write the table files (specified in CREATE ICEBERG TABLE),
  relative to your external volume location. Specifying a BASE\_LOCATION is required for Delta-based tables.
- `randomId` is a random, Snowflake-generated 8-character string.

| BASE\_LOCATION defined | BASE\_LOCATION\_PREFIX defined | Path |
| --- | --- | --- |
| No | No | `STORAGE_BASE_URL/database/schema/table_name.randomId/[data | metadata]/` |
| No | Yes | `STORAGE_BASE_URL/BASE_LOCATION_PREFIX/table_name.randomId/[data | metadata]/` |
| Yes | N/A (ignored) | `STORAGE_BASE_URL/BASE_LOCATION.randomId/[data | metadata]/` |
| ‘’ (empty string) | N/A (ignored) | `STORAGE_BASE_URL/randomId/[data | metadata]/` |

Expand

Show lessSee more

**Organizing table storage with BASE\_LOCATION**

Note

We don’t recommend this option if you plan to rename tables in the future.

After you create a Snowflake-managed table,
the path to its files in external storage does not change, even if you rename the table.

To organize files in storage for multiple Iceberg tables under the same `STORAGE_BASE_URL`,
consider using the table name as the `BASE_LOCATION` in your CREATE ICEBERG TABLE statement. This way, Snowflake writes data and
metadata to a directory that includes the name of the table.

For example:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE iceberg_table_1 (
  col_1 int,
  col_2 string
)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'iceberg_external_volume'
  BASE_LOCATION = 'iceberg_table_1';

CREATE OR REPLACE ICEBERG TABLE iceberg_table_2 (
  col_1 int,
  col_2 string
)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'iceberg_external_volume'
  BASE_LOCATION = 'iceberg_table_2';
```

The statement results in the following directory structure in your external cloud storage:

Copy code

```
STORAGE_BASE_URL
|-- iceberg_table_1.<randomId>
|   |-- data/
|   |-- metadata/
|-- iceberg_table_2.<randomId>
|   |-- data/
|   |-- metadata/
```

##### Hierarchical layout

This section describes the hierarchical layout in Snowflake for data and metadata directories for Snowflake-managed tables.

When you create a Snowflake-managed table that uses the default flat directory layout (PATH\_LAYOUT = HIERARCHICAL), Snowflake writes all
Parquet data files by organizing them in a hierarchical directory structure under the `data/` directory that is based on transforms that
you define when you create a
table. For instructions on how to enable this layout, see [Partitioning with hierarchical paths](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning-hierarchical-paths). Snowflake writes all
table metadata data files under a single `metadata/` directory.

Snowflake constructs paths using the following patterns, depending on the values specified
for [BASE\_LOCATION](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-snowflake-base-location) or
the [BASE\_LOCATION\_PREFIX](/sql-reference/parameters#label-base-location-prefix) parameter.
If you specify a `BASE_LOCATION`, Snowflake does not use the BASE\_LOCATION\_PREFIX in the path.

Where:

- `STORAGE_BASE_URL` is the base URL for the active storage location associated with your external volume.
- `BASE_LOCATION` is the path for a directory where Snowflake should write the table files (specified in CREATE ICEBERG TABLE),
  relative to your external volume location. Specifying a BASE\_LOCATION is required for Delta-based tables.
- `randomId` is a random, Snowflake-generated 8-character string.

| BASE\_LOCATION defined | BASE\_LOCATION\_PREFIX defined | Path |
| --- | --- | --- |
| No | No | `STORAGE_BASE_URL/database/schema/table_name.randomId/[data/<hierarchical_layout> | metadata]/` |
| No | Yes | `STORAGE_BASE_URL/BASE_LOCATION_PREFIX/table_name.randomId/[data/<hierarchical_layout> | metadata]/` |
| Yes | N/A (ignored) | `STORAGE_BASE_URL/BASE_LOCATION.randomId/[data/<hierarchical_layout> | metadata]/` |
| ‘’ (empty string) | N/A (ignored) | `STORAGE_BASE_URL/randomId/[data/<hierarchical_layout> | metadata]/` |

Expand

Show lessSee more

**Organizing table storage with BASE\_LOCATION**

Note

We don’t recommend this option if you plan to rename tables in the future.

After you create a Snowflake-managed table,
the path to its files in external storage does not change, even if you rename the table.

To organize files in storage for multiple Iceberg tables under the same `STORAGE_BASE_URL`,
consider using the table name as the `BASE_LOCATION` in your CREATE ICEBERG TABLE statement. This way, Snowflake writes data and
metadata to a directory that includes the name of the table.

The following example creates `customer_region_summary` and `orders_by_status` tables, which each use a hierarchical path layout
for their data files based on the following transforms:

- The `customer_region_summary` table is partitioned by `region`
- the `orders_by_status` table is partitioned by `order_status`

Copy code

```
CREATE OR REPLACE ICEBERG TABLE customer_region_summary (
  customer_id int,
  region string
)
  PARTITION BY (region)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'iceberg_external_volume'
  PATH_LAYOUT = HIERARCHICAL
  BASE_LOCATION = 'customer_region_summary';

CREATE OR REPLACE ICEBERG TABLE orders_by_status (
  order_id int,
  order_status string
)
  PARTITION BY (order_status)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'iceberg_external_volume'
  PATH_LAYOUT = HIERARCHICAL
  BASE_LOCATION = 'orders_by_status';
```

The statement results in the following directory structure in your external cloud storage:

Copy code

```
STORAGE_BASE_URL
|-- customer_region_summary.<randomId>
|   |-- data/
|   |   |-- REGION=US/
|   |   |   |-- part-00001-abc123.parquet
|   |   |-- REGION=EU/
|   |       |-- part-00002-def456.parquet
|   |-- metadata/
|
|-- orders_by_status.<randomId>
    |-- data/
    |   |-- ORDER_STATUS=SHIPPED/
    |   |   |-- part-00001-ghi789.parquet
    |   |-- ORDER_STATUS=PENDING/
    |       |-- part-00002-jkl012.parquet
    |-- metadata/
```

### Tables that use an external catalog

Snowflake doesn’t write or delete storage objects for externally managed Iceberg tables
or on external volumes with the `ALLOW_WRITES` property set to `FALSE`.

For external catalogs that you connect to with an external volume, to access your table data and metadata, Snowflake assumes the
access control role that you configure for your external volume.
You grant the role permission to access a storage location (in a bucket or container). All of your table data and metadata files must
be in that location.
For example, if your storage location is an S3 bucket, all of your data and metadata files must exist somewhere in that bucket.

For external catalogs that you connect to by using catalog-vended credentials, Snowflake obtains short-lived, scoped credentials from the
external catalog that allow Snowflake access only to the paths that store the table’s data and metadata.
For more information, see [Use catalog-vended credentials for Apache Iceberg™ tables](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials).

Additionally, [converting a table](/user-guide/tables-iceberg-conversion) does not rewrite any data or metadata files.
Snowflake writes to an Iceberg table only after you convert a table to use Snowflake as the catalog.

#### Data and metadata directories

This section describes the data and metadata directories for externally managed tables that you create in a catalog-linked database.
These directories can either be organized in a flat or hierarchical layout:

- [Catalog-linked database: Flat layout](#label-tables-iceberg-catalog-linked-flat-layout)
- [Catalog-linked database: Hierarchical layout](#label-tables-iceberg-catalog-linked-hierarchical-layout)

Note

- To find the data and metadata directories for any Iceberg table that you specified a `base_location` for when you created it, you can use
  the [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) command.
  The command output includes a `base_location` property that indicates the location of each table’s data and metadata files.
- For externally managed tables in a standard Snowflake database, Snowflake infers the location of the table from the remote catalog
  metadata and then writes to the `/data` directory for the table.

##### Catalog-linked database: Flat layout

This section describes the flat layout for data and metadata directories for externally managed Iceberg tables that you create in a
catalog-linked database.

When you create an externally managed table in a catalog-linked database that uses the default flat directory layout (PATH\_LAYOUT = FLAT),
Snowflake writes all Parquet data files under a single `data/` directory and all table metadata data files under a
single `metadata/` directory.

Snowflake constructs paths using the following patterns, depending on the values specified
for [BASE\_LOCATION](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-snowflake-base-location) or
the [BASE\_LOCATION\_PREFIX](/sql-reference/parameters#label-base-location-prefix) parameter.
If you specify a `BASE_LOCATION`, Snowflake does not use the BASE\_LOCATION\_PREFIX in the path.

Note

The `BASE_LOCATION_PREFIX` parameter is only supported when you use an external volume to connect to your catalog-linked database.
The `BASE_LOCATION_PREFIX` parameter isn’t supported when you use catalog-vended credentials to connect to your catalog-linked database.

Where:

- `STORAGE_BASE_URL` is the base URL for the active storage location associated with your external volume or vended credentials.
- `BASE_LOCATION` is the path for a directory where Snowflake should write the table files (specified in CREATE ICEBERG TABLE),
  relative to your external volume location. If you’re using catalog-vended credentials, this must be an absolute path that points to
  an allowed location defined by the remote catalog. Specifying a BASE\_LOCATION is required for Delta-based tables.
- `randomId` is a random, Snowflake-generated 8-character string.

| BASE\_LOCATION defined | BASE\_LOCATION\_PREFIX defined | Path |
| --- | --- | --- |
| No | No | `STORAGE_BASE_URL/database/schema/table_name/[data | metadata]/` |
| No | Yes | `STORAGE_BASE_URL/BASE_LOCATION_PREFIX/table_name.randomId/[data | metadata]/` |
| Yes | N/A (ignored) | `STORAGE_BASE_URL/BASE_LOCATION.randomId/[data | metadata]/` |

Expand

Show lessSee more

**Organizing table storage with BASE\_LOCATION**

To organize files in storage for multiple Iceberg tables under the same `STORAGE_BASE_URL`,
consider using the table name as the `BASE_LOCATION` in your CREATE ICEBERG TABLE statement. This way, Snowflake writes data and
metadata to a directory that includes the name of the table.

For example:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE iceberg_table_1 (
  col_1 int,
  col_2 string
)
  BASE_LOCATION = 's3://my-bucket/customer_iceberg/my_base_location1';

CREATE OR REPLACE ICEBERG TABLE iceberg_table_2 (
  col_1 int,
  col_2 string
)
  BASE_LOCATION = 's3://my-bucket/customer_iceberg/my_base_location2';
```

The statement results in the following directory structure in your external cloud storage:

Copy code

```
STORAGE_BASE_URL
|-- iceberg_table_1.<randomId>
|   |-- data/
|   |-- metadata/
|-- iceberg_table_2.<randomId>
|   |-- data/
|   |-- metadata/
```

##### Catalog-linked database: Hierarchical layout

This section describes the hierarchical layout for data and metadata directories for externally managed Iceberg tables that you
create in a catalog-linked database.

When you create an externally managed Iceberg table in a catalog-linked database that uses the default flat directory layout
(PATH\_LAYOUT = HIERARCHICAL), Snowflake writes all
Parquet data files by organizing them in a hierarchical directory structure under the `data/` directory that is based on transforms that you
define when you create a table. For instructions on
how to enable this layout, see [Partitioning with hierarchical paths](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning-hierarchical-paths). Snowflake writes all table metadata data files
under a single `metadata/` directory.

Note

If you set PATH\_LAYOUT = HIERARCHICAL without specifying a PARTITION BY clause, Snowflake uses the
[flat layout](#label-tables-iceberg-catalog-linked-flat-layout) for the table. However, if you later
enable partitioning on the table, Snowflake begins using a hierarchical layout with partitioned writes.
For more information, see [Partitioning with hierarchical paths](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning-hierarchical-paths).

For externally managed tables with a hierarchical layout, Snowflake writes Parquet data files and table metadata to your external cloud
storage. The Parquet data files are organized in a hierarchical directory structure that is based
on transforms that you define when you create a table.

Snowflake constructs paths using the following patterns, depending on the values specified
for [BASE\_LOCATION](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-snowflake-base-location) or
the [BASE\_LOCATION\_PREFIX](/sql-reference/parameters#label-base-location-prefix) parameter.
If you specify a `BASE_LOCATION`, Snowflake does not use the BASE\_LOCATION\_PREFIX in the path.

Note

The `BASE_LOCATION_PREFIX` parameter is only supported when you use an external volume to connect to your catalog-linked database.
The `BASE_LOCATION_PREFIX` parameter isn’t supported when you use catalog-vended credentials to connect to your catalog-linked database.

Where:

- `STORAGE_BASE_URL` is the base URL for the active storage location associated with your external volume or vended credentials.
- `BASE_LOCATION` is the path for a directory where Snowflake should write the table files (specified in CREATE ICEBERG TABLE),
  relative to your external volume location. If you’re using catalog-vended credentials, this must be an absolute path that points to
  an allowed location defined by the remote catalog. Specifying a BASE\_LOCATION is required for Delta-based tables.
- `randomId` is a random, Snowflake-generated 8-character string.

| BASE\_LOCATION defined | BASE\_LOCATION\_PREFIX defined | Path |
| --- | --- | --- |
| No | No | `STORAGE_BASE_URL/database/schema/table_name.randomId/[data/<hierarchical_layout> | metadata]/` |
| No | Yes | `STORAGE_BASE_URL/BASE_LOCATION_PREFIX/table_name.randomId/[data/<hierarchical_layout> | metadata]/` |
| Yes | N/A (ignored) | `STORAGE_BASE_URL/BASE_LOCATION.randomId/[data/<hierarchical_layout> | metadata]/` |

Expand

Show lessSee more

**Organizing table storage with BASE\_LOCATION**

To organize files in storage for multiple Iceberg tables under the same `STORAGE_BASE_URL`,
consider using the table name as the `BASE_LOCATION` in your CREATE ICEBERG TABLE statement. This way, Snowflake writes data and
metadata to a directory that includes the name of the table.

The following example creates `customer_region_summary` and `orders_by_status` tables, which each use a hierarchical path layout
for their data files based on the following transforms:

- The `customer_region_summary` table is partitioned by `region`
- the `orders_by_status` table is partitioned by `order_status`

Copy code

```
CREATE OR REPLACE ICEBERG TABLE customer_region_summary (
  customer_id int,
  region string
)
  PARTITION BY (region)
  PATH_LAYOUT = HIERARCHICAL
  BASE_LOCATION = 's3://my-bucket/customer_iceberg/my_base_location1';

CREATE OR REPLACE ICEBERG TABLE orders_by_status (
  order_id int,
  order_status string
)
  PARTITION BY (order_status)
  BASE_LOCATION = 's3://my-bucket/customer_iceberg/my_base_location2';
```

The statement results in the following directory structure in your external cloud storage:

Copy code

```
STORAGE_BASE_URL
|-- customer_region_summary.<randomId>
|   |-- data/
|   |   |-- REGION=US/
|   |   |   |-- part-00001-abc123.parquet
|   |   |-- REGION=EU/
|   |       |-- part-00002-def456.parquet
|   |-- metadata/
|
|-- orders_by_status.<randomId>
    |-- data/
    |   |-- ORDER_STATUS=SHIPPED/
    |   |   |-- part-00001-ghi789.parquet
    |   |-- ORDER_STATUS=PENDING/
    |       |-- part-00002-jkl012.parquet
    |-- metadata/
```

## Enabling storage access logs

To diagnose issues and audit access to the storage locations associated with an external volume, you can enable storage logging.
Storage logs help you identify the cause of missing or corrupted files.

Enable logging with your storage provider. Because you own and manage storage for Iceberg tables,
Snowflake can’t enable logging or auditing on your Iceberg storage locations.

To learn about storage access logs for your storage provider, see the following external topics:

- [Logging options for Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/logging-with-S3.html)
- [Usage logs and storage logs for Google Cloud Storage](https://cloud.google.com/storage/docs/access-logs)
- [Azure Storage analytics logging](https://learn.microsoft.com/en-us/azure/storage/common/storage-analytics-logging)

## Protecting files with versioning and object retention

If your Iceberg table data is in a central data repository (or data lake) that is operated on by multiple tools and services,
accidental deletion or corruption might occur. To protect Iceberg table data and ensure retrieval
of accidentally deleted or overwritten data, use storage lifecycle management and versioning offered by your storage provider.

With lifecycle management, you can set retention and tracking rules for storage objects.
To learn about lifecycle management for your storage provider, see the following external topics:

- [Managing your storage lifecycle for Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [Object Lifecycle Management for Google Cloud Storage](https://cloud.google.com/storage/docs/lifecycle)
- [Lifecycle management policies in Azure](https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview)

To support object recovery, you can also enable versioning for your external cloud storage.

- To enable versioning for Amazon S3, see [Enabling versioning on buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/manage-versioning-examples.html).
- To enable versioning for Google Cloud Storage, see [Use Object Versioning](https://cloud.google.com/storage/docs/using-object-versioning).
- To enable versioning for Azure, see [Enable blob versioning](https://learn.microsoft.com/en-us/azure/storage/blobs/versioning-enable?tabs=portal#enable-blob-versioning).

## Encrypting table files

Snowflake can read Iceberg table files in storage that you encrypt using common server-side encryption (SSE) schemes.
You should use your cloud service provider to manage encryption keys,
and grant the Snowflake principal access to your keys if you use a customer-managed key.

For Amazon S3, Snowflake supports the following SSE options:

| SSE option | Configuration |
| --- | --- |
| SSE with Amazon S3 managed keys (SSE-S3) | Specify `ENCRYPTION = ( TYPE = 'AWS_SSE_S3' )` in the [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) command. |
| SSE with AWS KMS keys (SSE-KMS) | Specify `ENCRYPTION = ( TYPE = 'AWS_SSE_KMS' KMS_KEY_ID='my_key' )` in the [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) command.  You must also grant privileges required for SSE-KMS encryption. For instructions, see Step 3 in [Configure an external volume for Amazon S3](/user-guide/tables-iceberg-configure-external-volume-s3). |

Expand

Show lessSee more

For Google Cloud Storage, Snowflake supports the following SSE option:

| SSE option | Configuration |
| --- | --- |
| SSE using keys stored in Google Cloud KMS | Specify `ENCRYPTION = ( TYPE = 'GCS_SSE_KMS' KMS_KEY_ID = 'my_key' )` in the [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) command.  You must also [Grant the GCS service account permissions on the Google Cloud Key Management Service keys](/user-guide/tables-iceberg-configure-external-volume-gcs#label-tables-iceberg-configure-external-volume-gcs-kms). |

Expand

Show lessSee more

## Configure replication for Snowflake-managed Iceberg tables

You can replicate Snowflake-managed Iceberg tables by using a failover or replication group. Snowflake replicates
a Snowflake-managed Iceberg table when you add the following objects to a failover or replication group:

- The parent database for the table
- The external volume that the table uses

For more information, see [Configure replication for Snowflake-managed Apache Iceberg™ tables](/user-guide/tables-iceberg-replication).
