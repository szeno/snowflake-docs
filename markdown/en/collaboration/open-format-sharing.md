# Open format sharing

Snowflake supports sharing open table formats — including Apache Iceberg™ tables and Delta Lake tables — across
regions, clouds, and engines, without requiring you to build ETL pipelines or duplicate data. Data stays in place
while Snowflake handles governance, replication, and access control.

Open format sharing supports the following use cases:

- **Access Iceberg data in Snowflake.** Bring external Iceberg tables into Snowflake using a catalog-linked
  database or an external volume. Query tables managed by external catalogs such as Apache Polaris™, Databricks
  Unity Catalog, or AWS Glue directly from Snowflake. For more information, see
  [Access Iceberg data in Snowflake](/collaboration/open-format-sharing-access-iceberg).
- **Share open table formats with Snowflake consumers.** Share Iceberg and Delta Lake tables with other Snowflake
  accounts using direct shares, listings, or Cross-Cloud Auto-Fulfillment. Snowflake manages replication and
  storage across regions and clouds. For more information, see
  [Using auto-fulfillment with open table formats](/collaboration/use-auto-fulfillment-with-open-table-formats).
- **Share data with non-Snowflake consumers.** Share live, read-only Iceberg table data with consumers outside
  Snowflake using standard Iceberg REST Catalog APIs. External consumers connect using any IRC-compatible engine
  or tool. For more information, see [Share data with non-Snowflake consumers](/user-guide/open-data-sharing).

[![Zero-ETL sharing for open table formats — register data in Snowflake Horizon Catalog, then share cross-region and cross-cloud to commercial and government cloud consumers](/static/images/collaboration/open-format-sharing-zero-etl.png)](/static/images/collaboration/open-format-sharing-zero-etl.png)
