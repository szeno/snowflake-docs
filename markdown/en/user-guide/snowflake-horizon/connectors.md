# Horizon Catalog connectors

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Horizon Catalog provides connectors for collecting metadata, lineage, and popularity data from
external data sources and BI tools.

We recommend that you manage metadata access separately from
your data access roles. See [Metadata access control](/user-guide/snowflake-horizon/connectors/access-control)
for more information.

For information about encryption, network security, credentials management, and the
shared-responsibility model,
see [Security and data protection](/user-guide/snowflake-horizon/connectors/security).

## Cost and refresh schedule

There’s no charge for adding connectors, for ingesting metadata from connected sources, or for
storing the metadata, lineage, and popularity data that connectors collect.

### Refresh schedule

Horizon Catalog refreshes the metadata from each connected source every 24 hours.

### Costs that still apply

- **Your warehouse:** Snowsight uses your active warehouse for some steps, such as checking your
  privileges when you create a connection. These queries consume credits at standard warehouse
  rates.
- **The external source:** Connectors run metadata and lineage queries against the source system,
  for example on a Databricks SQL warehouse. The provider of that system bills for any compute
  that these queries use.

## BI connectors

- [Amazon QuickSight](/user-guide/snowflake-horizon/connectors/quicksight)
- [Hex](/user-guide/snowflake-horizon/connectors/hex)
- [Looker](/user-guide/snowflake-horizon/connectors/looker)
- [Metabase](/user-guide/snowflake-horizon/connectors/metabase)
- [Microsoft Power BI](/user-guide/snowflake-horizon/connectors/powerbi)
- [Omni](/user-guide/snowflake-horizon/connectors/omni)
- [Sigma](/user-guide/snowflake-horizon/connectors/sigma)
- [Tableau](/user-guide/snowflake-horizon/connectors/tableau)
- [ThoughtSpot](/user-guide/snowflake-horizon/connectors/thoughtspot)

## Database connectors

- [Amazon Redshift](/user-guide/snowflake-horizon/connectors/amazon-redshift)
- [BigQuery](/user-guide/snowflake-horizon/connectors/bigquery)
- [Databricks](/user-guide/snowflake-horizon/connectors/databricks)
- [IBM Db2](/user-guide/snowflake-horizon/connectors/db2)
- [MySQL](/user-guide/snowflake-horizon/connectors/mysql)
- [Oracle](/user-guide/snowflake-horizon/connectors/oracle)
- [PostgreSQL](/user-guide/snowflake-horizon/connectors/postgres)
- [SQL Server](/user-guide/snowflake-horizon/connectors/sqlserver)

## Data pipeline tools

- [dbt](/user-guide/snowflake-horizon/connectors/dbt)
