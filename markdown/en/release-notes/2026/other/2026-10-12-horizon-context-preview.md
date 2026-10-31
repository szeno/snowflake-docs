# Oct 12, 2026: Horizon Context (*Preview*)

We’re introducing Horizon Context in preview. Horizon Context extends Horizon Catalog beyond Snowflake. This preview includes the following capabilities:

- **Metadata connectors.** Connect Horizon Catalog to 18 sources, including Power BI, Tableau, dbt, Databricks, BigQuery, SQL Server, Oracle, and PostgreSQL. You can browse and search external assets, trace column-level lineage across platforms, and manage tags and descriptions in Horizon Catalog. For more information, see [Horizon Catalog connectors](/user-guide/snowflake-horizon/connectors).
- **External metadata management.** Manage external metadata natively in Horizon Catalog, such as editing descriptions and applying tags and contacts directly to Power BI and Tableau dashboards.
- **Metadata-only editing access.** The APPLY COMMENT privilege lets data stewards curate descriptions without MODIFY or OWNERSHIP. External metadata management has its own privileges and doesn’t require the ACCOUNTADMIN role. For more information, see [Metadata access control](/user-guide/snowflake-horizon/connectors/access-control).
- **Lineage through temporary tables (generally available).** Source and destination tables stay connected after intermediate temporary objects are dropped, such as in dbt incremental models. For more information, see [Preserving data lineage through temporary tables and views](/user-guide/lineage-temporary-objects).

Horizon Context is available in all AWS and Azure commercial regions. It isn’t available in government regions or in China. Connectors read metadata from your external systems, and nothing is connected until you create a connection.

For more information, see [Horizon Context](/user-guide/snowflake-horizon/horizon-context).
