# Jul 18, 2025: Write support for externally managed Apache Iceberg™ tables and catalog-linked databases (*Preview*)

Snowflake now supports write operations for externally managed Iceberg tables and catalog-linked databases that connect
to external Iceberg REST catalogs. These features expand data engineering workflows between Snowflake and the broader Iceberg ecosystem.

Key capabilities:

- Create new Iceberg tables directly in your remote catalog using Snowflake.
- Perform full DML operations (INSERT, UPDATE, DELETE, MERGE) on externally managed tables.
- Create a Snowflake database that’s linked to your remote Iceberg REST catalog (AWS Glue, Snowflake Open Catalog, and others).
- Discover and access multiple remote Iceberg tables without individually defining them in Snowflake.

For more information, see [Write support for externally managed Apache Iceberg™ tables](/user-guide/tables-iceberg-externally-managed-writes)
and [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).
