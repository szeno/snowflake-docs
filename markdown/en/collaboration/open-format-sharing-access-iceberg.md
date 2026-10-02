# Access Iceberg data in Snowflake

Snowflake lets you access Apache Iceberg™ tables managed by external catalogs directly, without moving or
duplicating data. You can query, govern, and share external Iceberg tables alongside your Snowflake-managed data.

## Approaches

Snowflake provides two approaches for accessing external Iceberg data:

### Catalog-linked database

A catalog-linked database connects Snowflake to an external Iceberg REST catalog. Snowflake automatically
discovers namespaces and tables in the remote catalog and makes them available for queries, governance, and
sharing.

Use a catalog-linked database when you have an existing Iceberg REST catalog (such as Apache Polaris™,
Databricks Unity Catalog, or AWS Glue) and want Snowflake to automatically sync and discover tables.

For more information, see [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).

### External volume with catalog integration

An external volume provides Snowflake with access to your cloud storage location, while a catalog integration
connects Snowflake to your external Iceberg catalog. Together, they let you create individual Iceberg table
objects in Snowflake that reference data managed by an external catalog.

Use an external volume with a catalog integration when you want to register specific tables rather than syncing
an entire catalog, or when your catalog does not support the Iceberg REST protocol.

For more information, see the following topics:

- [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume)
- [Configure a catalog integration](/user-guide/tables-iceberg-configure-catalog-integration)

## Supported catalogs

Snowflake supports the following external catalogs for accessing Iceberg data:

- Apache Polaris™ (Snowflake Open Catalog)
- Databricks Unity Catalog
- AWS Glue Data Catalog
- Any catalog that implements the Apache Iceberg REST Catalog specification

For a complete list of catalog integrations and configuration instructions, see
[Use an external catalog](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration).
