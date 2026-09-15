# Oct 17, 2025: Set a target file size for Apache Iceberg™ tables (*General availability*)

Setting a target Parquet file size for Iceberg tables is now generally available. Doing so improves cross-engine query performance when you
use an external Iceberg engine such as Apache Spark, Delta, or Trino that’s optimized for larger file sizes. You can set the target file
size when you create a table, or update it later by using the [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) command.

For more information, see [Set a target file size](/user-guide/tables-iceberg-manage#label-tables-iceberg-target-file-size).
