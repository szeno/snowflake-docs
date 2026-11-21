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
- [Salesforce Analytics](/user-guide/snowflake-horizon/connectors/salesforce-analytics)
- [Sigma](/user-guide/snowflake-horizon/connectors/sigma)
- [Tableau](/user-guide/snowflake-horizon/connectors/tableau)
- [ThoughtSpot](/user-guide/snowflake-horizon/connectors/thoughtspot)

## Source data connectors

- [Amazon Redshift](/user-guide/snowflake-horizon/connectors/amazon-redshift)
- [BigQuery](/user-guide/snowflake-horizon/connectors/bigquery)
- [Databricks](/user-guide/snowflake-horizon/connectors/databricks)
- [IBM Db2](/user-guide/snowflake-horizon/connectors/db2)
- [MySQL](/user-guide/snowflake-horizon/connectors/mysql)
- [Oracle](/user-guide/snowflake-horizon/connectors/oracle)
- [PostgreSQL](/user-guide/snowflake-horizon/connectors/postgres)
- [Salesforce](/user-guide/snowflake-horizon/connectors/salesforce)
- [SQL Server](/user-guide/snowflake-horizon/connectors/sqlserver)

## Data pipeline tools

- [dbt](/user-guide/snowflake-horizon/connectors/dbt)

## Query collected metadata with Account Usage views

The objects that connectors collect from external systems are available as rows in views in the ACCOUNT\_USAGE schema of the
shared SNOWFLAKE database. Use these views to inventory your external objects, track changes, and find objects that were removed
from the source system.

- The [EXTERNAL\_DWH\_OBJECTS view](/sql-reference/account-usage/external_dwh_objects) contains objects collected from databases, data warehouses, and data
  pipeline tools, including databases, schemas, tables, views, and dbt models, seeds, and sources.
- The [EXTERNAL\_BI\_OBJECTS view](/sql-reference/account-usage/external_bi_objects) contains objects collected from BI tools, including folders, projects,
  datasets, dashboards, and charts.

Each row is one collected object. Both leaf objects and the containers that hold them are rows, and the `OBJECT_TYPE` column tells
them apart. The `PARENT_REFERENCE_ID` column points to the `REFERENCE_ID` of an object’s parent in the same view, so you can walk the
hierarchy without relying on names. The `CONNECTOR` and `CONNECTOR_TYPE` columns identify which connector collected each object.

For example, to list the current tables and views that a connector collected, largest first:

Copy code

```
SELECT name, object_type, database_name, schema_name, row_count, bytes, last_altered
  FROM snowflake.account_usage.external_dwh_objects
  WHERE connector_type = 'BIGQUERY'
    AND object_type IN ('TABLE', 'VIEW')
    AND deleted IS NULL
  ORDER BY bytes DESC;
```

To list the dashboards that changed in the last 7 days, together with their parent folders:

Copy code

```
SELECT d.name, d.folder_path, d.url, d.last_altered, f.name AS folder_name
  FROM snowflake.account_usage.external_bi_objects d
  LEFT JOIN snowflake.account_usage.external_bi_objects f
    ON f.reference_id = d.parent_reference_id
  WHERE d.object_type = 'DASHBOARD'
    AND d.last_altered > DATEADD('day', -7, CURRENT_TIMESTAMP())
    AND d.deleted IS NULL;
```

For the full list of columns, see the reference pages for each view.
