# Oct 29, 2026: Access externally managed Apache Iceberg™ tables through Snowflake Horizon Catalog (*General availability*)

Access to externally managed Apache Iceberg™ tables through Snowflake Horizon Catalog is now generally available.

You can use the Horizon Iceberg REST Catalog API to read and write externally managed Iceberg tables from external
engines such as Apache Spark™, Trino, DuckDB, or PyIceberg. The tables can be in a catalog-linked database or in a
standard Snowflake database. Snowflake RBAC applies to both.

Access to an externally managed Iceberg table that has a Snowflake data protection policy remains in preview. Access
through Horizon Catalog isn’t available on FedRAMP (Moderate) or FedRAMP (High) deployments.

For more information, see [Access externally managed Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/externally-managed-iceberg-tables-access-horizon-irc).
