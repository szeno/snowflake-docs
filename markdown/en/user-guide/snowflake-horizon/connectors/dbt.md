# dbt

Horizon Catalog supports both dbt deployment types. Select your deployment type to get started:

## Supported deployments

- [dbt Cloud](/user-guide/snowflake-horizon/connectors/dbt/dbt-cloud)
- [dbt Core (open source)](/user-guide/snowflake-horizon/connectors/dbt/dbt-core)

## How the connector works

The dbt connector enriches the data sources already in Horizon Catalog with metadata from your dbt
project: model-to-model lineage for any connected warehouse, and model and column descriptions for
non-Snowflake warehouses such as BigQuery or Amazon Redshift. For Snowflake, Horizon Catalog uses
the native object descriptions instead. The connector doesn’t ingest data; it layers dbt
documentation and lineage on top of an existing warehouse data source.

Horizon Catalog reads the build artifacts that dbt produces rather than connecting to dbt itself. In
the connector wizard, you select your **dbt type** (dbt Cloud or dbt Core) up front. Select the
setup guide for your deployment to see the prerequisites and connection-form fields specific to it.

## Requirements

To connect dbt to Horizon Catalog, you need the following:

- A warehouse data source that is already connected in Horizon Catalog. The dbt connector attaches
  to it so that dbt models map to the corresponding warehouse tables and views.
- A built dbt project. Horizon Catalog never needs access to dbt directly, but it does need the
  build artifacts that dbt produces (for dbt Core) or access to a dbt Cloud job that produces them
  (for dbt Cloud).

## Choosing between dbt Cloud and dbt Core

|  | dbt Cloud | dbt Core (open source) |
| --- | --- | --- |
| **Model metadata, lineage** | Supported | Supported |
| **How Horizon Catalog gets the build artifacts** | Pulled from a scheduled dbt Cloud job through the dbt Cloud API | Uploaded as files when you create the connection |
| **Keeping metadata up to date** | Automatic after the initial connection | Manual. Regenerate and upload the artifacts again after your dbt project changes |
| **Credentials** | A dbt Cloud service token | None. Horizon Catalog doesn’t connect to dbt |

Expand

Show lessSee more

## Limitations

Each dbt connection is associated with a single dbt project (one dbt Cloud job, or one set of dbt
Core artifacts). Adding dependent dbt projects to the same connection so Horizon Catalog can stitch
cross-project lineage isn’t available yet. Connect each project as its own connection.
