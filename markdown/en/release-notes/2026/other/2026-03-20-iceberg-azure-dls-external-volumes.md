# Mar 20, 2026: Apache Iceberg™ tables: Support for the Azure Data Lake Storage Gen2 with external volumes (*Preview*)

Snowflake now supports specifying Azure Data Lake Storage Gen2 (Azure Data Lake Storage) when you configure
an external volume for Apache Iceberg™ tables on Azure.

This update enables interoperability between Snowflake and remote catalogs that are only configured to use Data Lake Storage, as follows:

- You can create Snowflake-managed Iceberg tables that the query engine for these remote catalogs can read and write to.
- You can use Snowflake to read and write to remote tables in these remote catalogs.

For example, this update enables interoperability with Unity Catalog hosted on Azure.

To specify Data Lake Storage when you configure a new external volume, specify
`azure://account.dfs.core.windows.net/container[/path/]` for the STORAGE\_BASE\_URL.
For more information, see [Configure an external volume for Azure](/user-guide/tables-iceberg-configure-external-volume-azure).

Note

To make your existing Iceberg tables in Blob Storage interoperable with catalogs that are only configured to use Data Lake Storage,
you can migrate the tables to Data Lake Storage. For instructions, see [Migrate an Iceberg table to Azure Data Lake Storage](/user-guide/tables-iceberg-manage#label-iceberg-migrate-azure-dls).
