# Apr 6, 2026: Apache Iceberg™ tables: Write support for Databricks Unity Catalog on Azure (*General availability*)

Previously, write support for externally managed Apache Iceberg™ tables managed by Databricks Unity Catalog was limited to
workspaces where the underlying storage was on AWS. With this release, you can also write to externally managed
Iceberg tables managed by Unity Catalog when the underlying storage is on Azure.

This is made possible by the support for Azure Data Lake Storage Gen2 with external volumes. To write to Unity Catalog
tables on Azure, configure an external volume that connects to Data Lake Storage Gen2, then configure a catalog integration
for Unity Catalog.

For more information, see the following topics:

- [Configure an external volume for Azure](/user-guide/tables-iceberg-configure-external-volume-azure)
- [Configure a catalog integration for Unity Catalog](/user-guide/tables-iceberg-configure-catalog-integration-rest-unity)
- [Write support for externally managed Apache Iceberg™ tables](/user-guide/tables-iceberg-externally-managed-writes)
