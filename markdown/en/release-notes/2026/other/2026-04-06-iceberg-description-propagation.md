# Apr 20, 2026: Apache Iceberg™ tables: Table and column description propagation from external catalogs (*General availability*)

With this release, Snowflake bidirectionally syncs table and column descriptions between your external Iceberg REST catalog
and your catalog-linked database. Sync can update a description to a new value, but never replaces a non-empty description
with an empty one.

- If a table or column in the remote catalog has a description but the corresponding Snowflake object doesn’t, Snowflake
  copies the description from the catalog during refresh.
- If you set a description in Snowflake using COMMENT on an externally managed Iceberg table and the corresponding
  description in the remote catalog is empty, Snowflake propagates your description back to the catalog.
- If both sides have different non-empty descriptions, the most recent sync determines which value takes precedence.
  For example, when Snowflake refreshes from the catalog, the catalog’s description takes precedence. When Snowflake
  writes to the catalog, Snowflake’s description takes precedence.

Table and column descriptions are a key part of the semantic layer that AI features and data discovery tools rely on to
understand your data. With bidirectional sync, descriptions stay up to date across Snowflake and your external catalog,
so they’re available wherever your teams work.

This feature works with any REST catalog, including AWS Glue, Databricks Unity Catalog, and Apache Polaris.

For more information, see [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).
