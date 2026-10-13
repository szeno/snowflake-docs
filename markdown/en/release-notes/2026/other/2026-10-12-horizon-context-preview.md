# Oct 12, 2026: Horizon Context (*Preview*)

We’re introducing Horizon Context in preview. Horizon Context extends Horizon Catalog with metadata from external systems and new ways to curate descriptions and preserve lineage, helping people and AI agents discover and understand data across your organization.

This release includes the following capabilities:

- **Metadata connectors for Horizon Catalog.** Connect to 18 supported sources, including Power BI, Tableau, dbt, SQL Server, Oracle, Databricks, BigQuery, MySQL, and PostgreSQL. Browse external assets, search metadata, explore cross-platform lineage, and update tags and descriptions in Horizon Catalog. For setup instructions and requirements, see [Horizon Catalog connectors](/user-guide/snowflake-horizon/connectors).
- **Metadata-only editing access.** Give data stewards permission to curate catalog descriptions without granting broader privileges such as MODIFY or OWNERSHIP. The APPLY COMMENT privilege provides targeted access to manage descriptions. For more information, see [Metadata access control](/user-guide/snowflake-horizon/connectors/access-control#apply-comment).
- **Lineage preserved through temporary tables (generally available).** Snowflake preserves table- and column-level lineage through intermediate temporary objects after they are dropped. For example, source and destination tables remain connected when dbt incremental models clean up temporary staging objects. This works automatically, with no additional configuration, and covers temporary tables and views, but not transient tables. For requirements and limitations, see [Preserving data lineage through temporary tables and views](/user-guide/lineage-temporary-objects).
- **Column description propagation.** Reduce repetitive documentation by propagating descriptions to supported downstream columns using column lineage. Descriptions propagate when data passes through unchanged. Propagation stops where values are transformed, combined, or aggregated, and doesn’t overwrite descriptions written directly on downstream columns. For more information, see [Column comment propagation](/user-guide/comment-propagation).

For more information, see [Horizon Context](/user-guide/snowflake-horizon/horizon-context).
