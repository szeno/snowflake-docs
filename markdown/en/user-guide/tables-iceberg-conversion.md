# Convert an Apache Iceberg™ table to use Snowflake as the catalog

Convert an [Apache Iceberg™ table](/user-guide/tables-iceberg) that Snowflake doesn’t manage into a
table that uses Snowflake as the Iceberg catalog.

You might choose to convert a table when you want full Snowflake platform support,
including support for the [Snowflake Catalog SDK](/user-guide/tables-iceberg-catalog).

To learn about the differences between Iceberg table types, see [Catalog options](/user-guide/tables-iceberg#label-tables-iceberg-catalog-options).

## Before and after table conversion

When you convert an Iceberg table to use Snowflake as the catalog, the table becomes writable and Snowflake assumes life-cycle management
for it.

The following table compares Iceberg tables before and after conversion:

|  | Before conversion | After conversion |
| --- | --- | --- |
| Iceberg catalog | An external catalog (such as AWS Glue), or no catalog at all. Requires a catalog integration. | Snowflake. Snowflake registers changes to the source data and registers the changes in the Snowflake catalog. Snowflake then updates the table metadata on your external volume.  Does not require a catalog integration. |
| Snowflake read operations | ✔ | ✔ |
| Snowflake write operations | ❌ | ✔ |
| Storage location for table data and metadata | External volume (external cloud storage). | External volume (external cloud storage) under a base location that you specify. |
| Data and metadata cleanup | Managed by you or your external catalog. | Managed by Snowflake. Snowflake never deletes any metadata, manifest lists, or manifests created before conversion from your external storage. Snowflake doesn’t rewrite any Parquet data files during conversion. *After* you convert a table, Snowflake might rewrite some of the data files as part of regular table maintenance. |
| Accessible from the Snowflake Catalog SDK | ❌ | ✔ |

Expand

Show lessSee more

Important

When you convert an Iceberg table, Snowflake doesn’t lock down or assume sole access to your external storage.
To prevent table corruption, ensure that you monitor or stop any non-Snowflake writes
(such as automated maintenance jobs) to your external storage location.

Note

Iceberg partitioning is removed when you convert a table.

## Requirements

Before you convert an Iceberg table, ensure that Snowflake can write to your external volume.

For Snowflake to write to your external volume, the following conditions must be met:

> - Use the ALTER ICEBERG TABLE … REFRESH command to manually refresh the table before you convert it.
> - The `ALLOW_WRITES` property for your external volume is set to `TRUE`. To update the value of this property for an existing
>   external volume, use the [ALTER EXTERNAL VOLUME](/sql-reference/sql/alter-external-volume) command.
>   For example: `ALTER EXTERNAL VOLUME my_ext_vol SET ALLOW_WRITES=TRUE`.
> - The access control permissions that you set on the cloud storage account must allow write access. For example,
>   if you use an external volume configured for Amazon S3, your IAM role must have the `s3:PutObject` permission for your S3 location.

Note

Converting a table that has an un-materialized identity partition column isn’t supported.
An un-materialized identity partition column is created when a table defines an identity transform
using a source column that doesn’t exist in a Parquet file.

## Example: Convert a table

Important

When you convert an Iceberg table, Snowflake doesn’t lock down or assume sole access to your external storage.
To prevent table corruption, ensure that you monitor or stop any non-Snowflake writes
(such as automated maintenance jobs) to your external storage location.

This example starts by creating an Iceberg table from Iceberg files in object storage.
Snowflake uses the `METADATA_FILE_PATH` value to look for the table metadata in the following location for column definitions:
`<ext-vol-storage-base-url>/path/to/metadata/v1.metadata.json`.

Copy code

```
CREATE ICEBERG TABLE myIcebergTable
  EXTERNAL_VOLUME='icebergMetadataVolume'
  CATALOG='icebergCatalogInt'
  METADATA_FILE_PATH='path/to/metadata/v1.metadata.json';
```

Next, use the ALTER ICEBERG TABLE … REFRESH command to synchronize the table metadata with the latest metadata file.
The following example command refreshes the table by specifying a metadata file path.

Copy code

```
ALTER ICEBERG TABLE myIcebergTable REFRESH 'metadata/v2.metadata.json';
```

Finally, convert the table to use Snowflake as the Iceberg catalog by using the
[ALTER ICEBERG TABLE … CONVERT TO MANAGED](/sql-reference/sql/alter-iceberg-table-convert-to-managed) command.

Copy code

```
ALTER ICEBERG TABLE myIcebergTable CONVERT TO MANAGED
  BASE_LOCATION = 'my/relative/path/from/external_volume';
```

Note

In this example, the ALTER statement must specify a `BASE_LOCATION` because the table was created
from Iceberg files in object storage and `BASE_LOCATION` was not part of the original CREATE ICEBERG TABLE statement.
The `BASE_LOCATION` defines the relative path from your external
volume to a directory where Snowflake writes table data and metadata for the converted table.

Otherwise, if `BASE_LOCATION` was specified in the original CREATE ICEBERG TABLE statement, you don’t need to include it in your
ALTER ICEBERG TABLE … CONVERT TO MANAGED command.

For example, Snowflake writes table data to
`<ext-vol-storage-base-url>/myBaseLocation/data/`.

Snowflake writes metadata for the converted table to `<ext-vol-storage-base-url>/myBaseLocation/metadata/`.

## Conversion and data types

Note

You can’t convert a table that uses the `fixed(L)` Iceberg data type.

Snowflake uses Snowflake data types to process and return values,
but writes the original Iceberg types to table data files.

For data types such as `int` and `long`, the Snowflake data type supports a larger range of values than the Iceberg data type.
To stay consistent with the source data type, Snowflake does not allow inserting values outside the range that the
source data type supports. For more information, see [Approximate types](/user-guide/tables-iceberg-data-types#label-tables-iceberg-approximate-types).
