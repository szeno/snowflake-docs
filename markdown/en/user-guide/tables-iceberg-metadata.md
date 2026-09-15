# Metadata and retention for Apache Iceberg™ tables

Snowflake handles metadata for Apache Iceberg™ tables according to the type of catalog you use (Snowflake or external).

Note

Specifying the default minimum number of snapshots with the `history.expire.min-snapshots-to-keep`
[table property](https://iceberg.apache.org/docs/1.2.1/configuration/#table-behavior-properties) is not supported
for any type of Iceberg table.

## Tables that use Snowflake as the catalog

Snowflake manages the metadata life cycle for this table type,
and deletes old metadata, manifest lists, and manifest files based on the retention period for the table data and snapshots.

To set the retention period for table data and snapshots, set the [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days) parameter
at the account, database, schema, or table level.

### Creation

Snowflake generates metadata for version 2 or version 3 of the Apache Iceberg specification
on a periodic basis based on the table’s definition, and writes the metadata to files on your external volume.
Each new metadata file contains all DML or DDL changes since the last Snowflake-generated metadata file was created.

You can also create metadata on demand by using the [SYSTEM$GET\_ICEBERG\_TABLE\_INFORMATION](/sql-reference/functions/system_get_iceberg_table_information) function.
For instructions, see [Generate snapshots of DML changes](/user-guide/tables-iceberg-manage#label-tables-iceberg-generate-snapshots).

For information about locating metadata files, see [Data and metadata directories](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location).

### Viewing metadata creation history

To access a full history of metadata generation attempts, view the query history for your account and filter the results. Search for the
[SYSTEM$GET\_ICEBERG\_TABLE\_INFORMATION](/sql-reference/functions/system_get_iceberg_table_information) function name in the SQL text.

Snowflake internally uses the same SYSTEM$GET\_ICEBERG\_TABLE\_INFORMATION function to generate table metadata. Attempts made by Snowflake
appear under the user called `SYSTEM` in the query history. The `STATUS` column in the query history
indicates whether metadata was successfully generated.

For viewing options, see [Monitor query activity with Query History](/user-guide/ui-snowsight-activity).

### Deletion

Snowflake deletes Iceberg metadata from your external cloud storage when the following events occur:

- After you drop a table.
- When the Iceberg metadata refers to snapshots or table data that has expired.

Deletion doesn’t occur immediately after the data retention period expires.
As a result, metadata storage might incur costs with your cloud storage provider for longer than a table’s lifetime.

Warning

[Fail-safe](/user-guide/data-failsafe) depends on where the table stores its files, not on whether Snowflake is the Iceberg catalog:

- For Iceberg tables on [Snowflake storage](/user-guide/tables-iceberg-internal-storage)
  (`EXTERNAL_VOLUME = SNOWFLAKE_MANAGED`), permanent tables are protected by Fail-safe.
  Transient tables aren’t. For details, see
  [Permanent and transient tables](/user-guide/tables-iceberg-internal-storage#label-tables-iceberg-internal-storage-failsafe).
- For Iceberg tables on a customer-managed [external volume](/user-guide/tables-iceberg-storage),
  Snowflake doesn’t support Fail-safe, because the table data is in external cloud storage that you manage.
  To protect that data, configure data protection and recovery with your cloud provider.

#### After dropping a table

When you drop a table, you can use the [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table) command
to restore it within the data retention period.

When the retention period expires, Snowflake deletes table metadata and snapshots that it
has written from your external volume location. Deletion occurs asynchronously and can take a few
days to complete after the retention period has passed.

Note

For [converted tables](/user-guide/tables-iceberg-conversion),
Snowflake deletes only metadata that was generated *after* table conversion.

#### After snapshots expire

Snowflake deletes Iceberg metadata files related to expired snapshots after the data retention period passes.
Deletion usually occurs 7-14 days after a snapshot expires.

Only previous table snapshots can expire. Snowflake never deletes metadata files that represent the latest (current) state of a table from
your external cloud storage.

## Tables that use an external catalog

For tables that use an external catalog, Snowflake uses the value of the [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days)
parameter to set a retention period for Snowflake Time Travel and undropping the table. When the retention period expires,
Snowflake does not delete the Iceberg metadata or snapshots from your external cloud storage.

Snowflake sets DATA\_RETENTION\_TIME\_IN\_DAYS at the table level to the smaller of
the following values:

- The `history.expire.max-snapshot-age-ms` value in the current metadata file. Snowflake converts the value to days (rounding down).
- The following value, depending on your [Snowflake account edition](/user-guide/intro-editions):
  - Standard Edition: 1 day.
  - Enterprise Edition or higher: 5 days.

You can’t manually change the value of DATA\_RETENTION\_TIME\_IN\_DAYS in Snowflake. To change the value, you must update
`history.expire.max-snapshot-age-ms` in your metadata file and then [refresh the table](/user-guide/tables-iceberg-manage#label-tables-iceberg-refresh-metadata).

You can use the following table functions to retrieve information about the files registered to an externally managed Iceberg table or
the most recent snapshot refresh history:

- [ICEBERG\_TABLE\_FILES](/sql-reference/functions/iceberg_table_files)
- [ICEBERG\_TABLE\_SNAPSHOT\_REFRESH\_HISTORY](/sql-reference/functions/iceberg_table_snapshot_refresh_history)

### Delta-based tables

Note

If you want to use metadata writes for Delta-based Iceberg tables, the
[2025\_01 behavior change bundle](/release-notes/bcr-bundles/2025_01_bundle) must not be disabled in your account.

For Iceberg tables created from Delta table files, Snowflake can write Iceberg metadata to your external storage on a best-effort basis when
you configure your external volume with write access (`ALLOW_WRITES = TRUE`; see [ALLOW\_WRITES](/sql-reference/sql/create-external-volume#label-create-external-volume-allow-writes-param)).
For more information about the write location, see [Data and metadata directories](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location).

If you set `ALLOW_WRITES` to `FALSE`, Iceberg metadata generation for those Delta-based tables doesn’t run and Snowflake doesn’t write
Iceberg metadata files to your storage. That’s a supported configuration when you need read-only access (for example, another team owns the
bucket and won’t grant write permission). Grant your cloud identity only the read actions that match `ALLOW_WRITES = FALSE` on the external volume.

#### Read-only vs write access for Delta Direct on each storage provider

The following table summarizes how to align **Iceberg tables created from Delta table files**, often called **Delta Direct**, with your
external volume for read-only access compared to write access that enables Iceberg metadata generation. The **External volume** row applies
to every cloud. For step-by-step procedures, see the linked topics for each provider.

| Area | Read-only access | Write access (Iceberg metadata generation for Delta-based tables) |
| --- | --- | --- |
| Amazon S3 | In the IAM policy for your external volume role, allow `s3:GetBucketLocation`, `s3:ListBucket`, `s3:GetObject`, and `s3:GetObjectVersion`. Omit `s3:PutObject`, `s3:DeleteObject`, and `s3:DeleteObjectVersion`. Use the same bucket ARN, prefix conditions, and optional SSE-KMS steps as in [Configure an external volume by using SQL](/user-guide/tables-iceberg-configure-external-volume-s3#label-tables-iceberg-configure-external-volume-s3-iam-policy-sql). | Use the full policy in [Configure an external volume by using SQL](/user-guide/tables-iceberg-configure-external-volume-s3#label-tables-iceberg-configure-external-volume-s3-iam-policy-sql) (including `s3:PutObject` and delete actions on objects). |
| Google Cloud Storage | In the custom IAM role for the Snowflake service account, grant `storage.buckets.get`, `storage.objects.get`, and `storage.objects.list`. Omit `storage.objects.create` and `storage.objects.delete`. Follow [Step 3: Grant the service account permissions to access bucket objects](/user-guide/tables-iceberg-configure-external-volume-gcs#label-tables-iceberg-configure-external-volume-gcs-grant-permissions) for assigning the role to the bucket. | Add `storage.objects.create` and `storage.objects.delete` to that role as described in [Step 3: Grant the service account permissions to access bucket objects](/user-guide/tables-iceberg-configure-external-volume-gcs#label-tables-iceberg-configure-external-volume-gcs-grant-permissions). |
| Microsoft Azure | Assign the [Storage Blob Data Reader](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/storage#storage-blob-data-reader) role to the Snowflake service principal at **storage account** scope so the identity can generate a user delegation key. For scope details and container-only workarounds, see [Snowflake accesses blob data on Azure by using Microsoft Entra ID…](/user-guide/tables-iceberg-configure-external-volume-azure#label-tables-iceberg-azure-ev-user-delegation-key). | Assign the [Storage Blob Data Contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/storage#storage-blob-data-contributor) role on the storage account. For the portal flow, see [Azure roles and Delta Direct on this external volume](/user-guide/tables-iceberg-configure-external-volume-azure#label-tables-iceberg-azure-ev-delta-read-only). |
| External volume (all providers) | Set `ALLOW_WRITES` to `FALSE`. In Snowsight, set **Access scope** so that writes aren’t allowed (see your provider’s external volume topic). | Set `ALLOW_WRITES` to `TRUE` (the default). In Snowsight, set **Access scope** to **Allow writes**. |
| Iceberg metadata in your storage | Snowflake doesn’t generate or write Iceberg metadata files for Delta-based tables. You can still query the tables. | Snowflake can write Iceberg metadata on a best-effort basis. |

Expand

Show lessSee more

You can set `ALLOW_WRITES` to `FALSE` only when no Snowflake-managed Iceberg tables use the same external volume.

## Iceberg partitioning

This section describes Iceberg partitioning.

Snowflake supports the following partitioning use cases:

- Reading from and writing to partitioned Iceberg tables.
- Creating partitioned Iceberg tables
  that are Snowflake-managed or externally managed in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database)
  or [externally managed by an Iceberg REST catalog](/user-guide/tables-iceberg-externally-managed-writes).

  When you create a partitioned Iceberg table, you can enable [hidden partitioning](#label-tables-iceberg-partitioning-hidden) or
  [partitioning with hierarchical paths](#label-tables-iceberg-partitioning-hierarchical-paths), which is also called “Hive-style”
  partitioning.

### “Hidden” partitioning

[“Hidden” partitioning](https://iceberg.apache.org/docs/latest/partitioning/#icebergs-hidden-partitioning)
for Apache Iceberg™ is metadata-based and adaptable. Iceberg produces partition values
based on transforms that you define when you create a table. When they read from a partitioned table, Iceberg engines
use the partition values defined in your table metadata to efficiently identify relevant data.

This option is the default. With this option, Snowflake stores your Parquet data files by using a flat directory layout.

To create a partitioned Iceberg table that uses hidden partitioning, include the PARTITION BY clause with one or more [partition transforms](https://iceberg.apache.org/spec/#partition-transforms)
in your regular [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) statement.

Note

To create a partitioned Iceberg table that uses hidden partitioning, the PATH\_LAYOUT parameter must be set to FLAT, which is the
default, so you don’t need to specify this parameter in your CREATE ICEBERG TABLE statement.

For an example, see [Create an Iceberg table in a catalog-linked database](/user-guide/tables-iceberg-externally-managed-writes#label-tables-iceberg-external-writes-create-table-cld).

### Partitioning with hierarchical paths

With this option, Snowflake writes data to partitioned Iceberg tables by using a hierarchical path layout
for Parquet data files. Partitioning information is included in the file paths and the values are based on transforms that you define
when you create a table. This layout is also called
“Hive-style” partitioning. You might use this option for interoperability between Snowflake and external engines that support partitioned
writes with hierarchical paths.

Here’s an example of a data file stored under a hierarchical path:

`s3://my-bucket/iceberg/db_sales/orders/data/country=US/year=2025/month=02/day=21/part-00023.parquet`

For more information on the layout of the data and metadata directories for tables that use hierarchical paths,
see [File management](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-manage-files-in-storage).

#### Create a table with hierarchical paths

To create a partitioned Iceberg table with a hierarchical path layout, set the following properties in your regular [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) statement:

- Set PATH\_LAYOUT = HIERARCHICAL.
- Include the PARTITION BY clause with one or more [partition transforms](https://iceberg.apache.org/spec/#partition-transforms).

For an example of creating a partitioned Iceberg table with a hierarchical path layout in a catalog-linked database,
see [Create an Iceberg table in a catalog-linked database with hierarchical path layout](/user-guide/tables-iceberg-externally-managed-writes#label-tables-iceberg-external-writes-create-table-cld-hierarchical).

### Partitioning support matrix

The following table shows which features and actions are supported for each type of partitioned Iceberg table, and indicates compliance with
version 2 of the Apache Iceberg specification. The table shows support for both hidden partitioning and partitioning with hierarchical paths.

Note

- Snowflake supports version 3 of the Apache Iceberg™ specification, which includes support for using deletion
  vectors with partitioned tables. For more information, see [Apache Iceberg™ tables: Support for Apache Iceberg™ v3](/user-guide/tables-iceberg-v3-specification-support).
- CLD stands for catalog-linked database.

|  | Snowflake managed | Externally managed (CLD) | Externally managed (non-CLD) | Iceberg spec V2 compatibility | Comment |
| --- | --- | --- | --- | --- | --- |
| COPY commands with the ON\_ERROR = ABORT\_STATEMENT option | ❌ | ❌ | ❌ | ❌ |  |
| COPY INTO <table> | Limited support | Limited support | Limited support | Limited support | See [Usage notes](/sql-reference/sql/copy-into-table#label-copy-into-table-usage-notes). |
| CREATE ICEBERG TABLE … AS SELECT (CTAS) | ✔ | ✔ | ✔ | ✔ |  |
| Cloning | ✔ | ✔ | ✔ | ✔ | See usage notes:   - [Snowflake managed](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-snowflake-usage-notes) - [Externally managed](/sql-reference/sql/create-iceberg-table-rest#label-create-catalog-table-rest-usage-notes) |
| CREATE ICEBERG TABLE … LIKE | ✔ | ✔ | ✔ | ✔ | See usage notes:   - [Snowflake managed](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-snowflake-usage-notes) - [Externally managed](/sql-reference/sql/create-iceberg-table-rest#label-create-catalog-table-rest-usage-notes) |
| Deletion vectors | ✔ | ✔ | ✔ | N/A | Requires Iceberg v3. |
| Clustering | ❌ | ❌ | ❌ | ❌ |  |
| Partition evolution | ❌ | Limited support | Limited support | Limited support | We support partition evolution if it is done with an external engine. |
| Partition transforms | ✔ | ✔ | ✔ | ✔ | For the supported partition transforms, see:   - [Snowflake managed](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-snowflake-partitionexpressions) - [Externally managed](/sql-reference/sql/create-iceberg-table-rest#label-create-iceberg-table-rest-partitionexpressions) |
| Positional deletes | ✔ | ✔ | ✔ | ✔ |  |
| Snowpipe | Limited support | Limited support | Limited support | Limited support | - Currently in *Public Preview*. - See the [usage notes](/sql-reference/sql/copy-into-table#label-copy-into-table-usage-notes) for COPY INTO <table>. |
| Snowpipe Streaming | ❌ | ❌ | ❌ | ❌ |  |
| Sorting within partitions | ❌ | ❌ | ❌ | ❌ |  |
| TARGET\_FILE\_SIZE | ✔ | ✔ | ✔ | ✔ |  |

Expand

Show lessSee more

### Partitioning considerations

Consider the following before you use partitioned writes for Iceberg tables:

- If you use an external engine to add, drop, or replace a partition field in an externally managed table,
  Snowflake writes data according to the latest partition specification.
- The [GET\_DDL](/sql-reference/functions/get_ddl) function doesn’t include the PARTITION BY clause in its output.
- The sum of the sizes of the outputs for all partition transforms can’t exceed 1024 bytes for a single row.
- Because partition evolution isn’t supported for Snowflake-managed tables, you must drop the table and create a new one with partitioning.
- The DAY(), MONTH(), YEAR() partition transform parameters, which you specify within the PARTITION BY clause under table properties,
  are part of the Iceberg specification. For multiple days, months, or years, the partition expression parameter returns a partition for
  each calendar day, month, or year.
  For example, when the DAY() transform is used on a timestamp column that has 2 months of data, 61 partitions are created.

  In contrast, the [DAY(), MONTH(), YEAR() functions](/sql-reference/functions/year)
  in Snowflake are part of the SQL standard. For multiple days, months, or years, these functions extract the corresponding day, month, or
  year part from a date or timestamp. For example, when the DAY() function is used on a timestamp column that has multiple months of data,
  this function returns a day of the month ranging from 1 to 31.
- For partitioning with hierarchical paths:

  - For `float` values, Snowflake and external engines might behave differently.
  - Snowflake can’t guarantee that the paths Snowflake writes will match the paths that external query
    engines write.

    Snowflake can’t guarantee this because when a query engine writes a hierarchical path, the query engine must serialize values into a string
    and insert the resulting value into the path.
    The Apache Iceberg table specification doesn’t define a standard serialization method, so different engines might implement different
    methods.

    For example, Snowflake doesn’t encode the `~` character but Apache Spark™ encodes this character as `%7E`.
  - Snowflake always writes the hierarchical paths directly under the `/data` directory in your external cloud storage.
  - When writing delete files, Snowflake uses the following behavior:

    - Positional delete files are written into the same directory as the corresponding data file.
    - Puffin files containing deletion vectors are always written into the table `data/` directory.

## Time travel

With [Snowflake Time Travel](/user-guide/data-time-travel),
you can use Snowflake to query historical data for a table.

You can also use a third-party compute engine to perform time travel
queries on Snowflake-managed tables when you [Sync a Snowflake-managed table with Snowflake Open Catalog](/user-guide/tables-iceberg-open-catalog-sync) or
use the [Snowflake Catalog SDK](/user-guide/tables-iceberg-catalog).

You can query any snapshots that were committed within the data retention period.
To specify the data retention period, set the [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days) object parameter.

When you delete table data or drop a table, Snowflake deletes objects after the table retention period expires.
This might incur costs with your cloud storage provider for longer than the table’s lifetime.
