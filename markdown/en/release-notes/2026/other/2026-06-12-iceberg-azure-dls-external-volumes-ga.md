# Jun 12, 2026: Apache Iceberg™ tables: Azure Data Lake Storage Gen2 support (*General availability*)

Support for Azure Data Lake Storage Gen2 (Azure Data Lake Storage) for Apache Iceberg™ tables is now generally available.

With this release, you can use Snowflake to read and write externally managed Iceberg tables when the underlying storage is on Azure Data Lake Storage.
You can connect to this storage by using catalog-vended credentials from your external catalog or by configuring an external volume.

This update enables interoperability between Snowflake and remote catalogs that are only configured to use Data Lake Storage, such as Unity Catalog hosted on Azure.

For more information, see the following topics:

- [Configure an external volume for Azure](/user-guide/tables-iceberg-configure-external-volume-azure)
- [Use catalog-vended credentials for Apache Iceberg™ tables](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials)
- [Write support for externally managed Apache Iceberg™ tables](/user-guide/tables-iceberg-externally-managed-writes)
