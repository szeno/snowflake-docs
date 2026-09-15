# Mar 02, 2026: Query Delta-based Apache Iceberg™ tables with deletion vectors

You can now query Delta-based Apache Iceberg™ tables that contain deletion vectors and use liquid clustering. With this update, Snowflake
now supports minReaderVersion 3 and can read tables written by engines that use Delta Lake version 4.0.0, which is the latest version.

Previously, you could only query Delta-based Iceberg tables that used copy-on-write because Snowflake supported minReaderVersion 2 and
tables written by engines that use Delta Lake version 2.2.0.

For more information, see [CREATE ICEBERG TABLE (Delta files in object storage)](/sql-reference/sql/create-iceberg-table-delta).
