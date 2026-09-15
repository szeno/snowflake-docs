# Mar 31, 2026: CTAS support for Databricks Unity Catalog with external volumes (*General availability*)

You can now use CREATE ICEBERG TABLE … AS SELECT (CTAS) to create Apache Iceberg™ tables in
catalog-linked databases that use Databricks Unity Catalog as the remote catalog. Previously,
CTAS was not supported for Unity Catalog, and you had to create an empty table and then use
INSERT INTO … SELECT as a workaround.

For more information, see [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest).
