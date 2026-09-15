# Sep 12, 2025: Support for position row-level deletes when writing to externally managed Apache Iceberg™ tables or catalog-linked databases on Amazon S3 or Google Cloud (*Preview*)

Snowflake now supports position row-level deletes when writing to externally managed Apache Iceberg™ or Iceberg tables in catalog-linked
databases when the tables are stored on Amazon S3 or Google Cloud. These deletes are supported when Snowflake performs update, delete, and
merge operations on the tables. This feature is a performance improvement for these operations.

For more information, see [Write support for externally managed Apache Iceberg™ tables](/user-guide/tables-iceberg-externally-managed-writes) and [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).
