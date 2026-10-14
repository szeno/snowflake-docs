# dbt Core (open source)

## Overview

Horizon Catalog ingests dbt model metadata and model-to-model lineage from the build artifacts that
dbt Core produces. You generate the artifacts locally or in your continuous integration (CI)
pipeline and upload them through a dbt connection, which enriches an existing warehouse data source
with lineage, and with model and column descriptions for non-Snowflake warehouses. By the time you
finish this guide you’ll have:

1. The build artifacts generated from your dbt project.
2. An active dbt connection in the Horizon Catalog UI, with the artifacts uploaded.
3. A routine for refreshing the artifacts when your dbt project changes.

## Prerequisites

- A warehouse data source already connected in Horizon Catalog. The dbt connector enriches an
  existing data source rather than creating one.
- A dbt project you can build, so that it produces the following artifacts:
  - `manifest.json` (required)
  - `catalog.json` (required)
  - `run_results.json` (optional, used to ingest dbt tests)
- Access to the Horizon Catalog connector wizard: sign in to Snowflake, open
  **Catalog > Connections**, and select **dbt** from the **Data pipeline tools** section.

## 1. Generate the build artifacts

Run the following commands in your dbt project and collect the artifacts from the `target`
directory.

Generate `manifest.json`:

Copy code

```
dbt compile --full-refresh
```

Warning

`dbt docs generate` also writes a `manifest.json`, but that file doesn’t contain enough lineage
information. Use the `manifest.json` produced by `dbt compile --full-refresh`, and copy it to
another location before running `dbt docs generate` so it isn’t overwritten.

Generate `catalog.json`:

Copy code

```
dbt docs generate
```

(Optional) Generate `run_results.json` for dbt tests:

Copy code

```
dbt test
```

## 2. Create a dbt connection

In Snowflake, open **Catalog > Connections** and select **dbt** from the **Data pipeline tools**
section. Set **dbt type** to **dbt Core (open source)**, then fill out the setup form with the
following fields:

| Field | Value |
| --- | --- |
| Display Name | A name for this data source, which defaults to `dbt` |
| dbt type | Select **dbt Core (open source)** |
| Connected Warehouse | The existing warehouse data source that your dbt models are built in (for example, Snowflake, BigQuery, or Amazon Redshift) |
| `manifest.json` | Drag and drop the `manifest.json` file from [Step 1](#1-generate-the-build-artifacts) |
| `catalog.json` | Drag and drop the `catalog.json` file from [Step 1](#1-generate-the-build-artifacts) |
| `run_results.json` | (Optional) Drag and drop the `run_results.json` file. Required only if you want to ingest dbt tests |
| Snowflake Database | The Snowflake database where Horizon Catalog stages the uploaded artifacts, which defaults to `CONNECTORS` |
| Snowflake Schema | The Snowflake schema where Horizon Catalog stages the uploaded artifacts, which defaults to `METADATA` |

Expand

Show lessSee more

Note

Each artifact file can be up to 250 MB.

Select **Next** to continue to the **Load data** step, where Horizon Catalog ingests the dbt
metadata.

## 3. Update the build artifacts

Unlike dbt Cloud, dbt Core doesn’t refresh automatically. To reflect changes in your dbt project,
regenerate the build artifacts (see [Step 1](#1-generate-the-build-artifacts)) and upload them
again:

1. In Snowflake, open **Catalog > Connections**, find your dbt data source, and select **Configure**.
2. Upload the updated `manifest.json`, `catalog.json`, and (optionally) `run_results.json` files.
3. Complete the wizard to apply your changes.

## 4. Set up metadata access

Other roles can’t see the metadata and lineage that this connector collects until you grant them
access. Grant `USAGE` on the connector, and on the database and schema that contain it, to each role
that needs to view the connector’s metadata and lineage:

Copy code

```
GRANT USAGE ON DATABASE CONNECTORS TO ROLE <role_name>;
GRANT USAGE ON SCHEMA CONNECTORS.METADATA TO ROLE <role_name>;
GRANT USAGE ON METADATA CONNECTOR CONNECTORS.METADATA.<connector_name> TO ROLE <role_name>;
```

If you stored the connector in a different database or schema, replace `CONNECTORS` and `METADATA`
with the actual database and schema names.

For more information about metadata access, see
[Metadata access control](/user-guide/snowflake-horizon/connectors/access-control).

## Troubleshooting

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| Lineage is missing or incomplete | The uploaded `manifest.json` came from `dbt docs generate`, which doesn’t contain enough lineage information | Step 1 |
| The file upload fails | One of the artifacts is larger than the 250 MB limit | Step 2 |
| dbt tests don’t appear | `run_results.json` wasn’t uploaded | Step 1 |
| Metadata stops reflecting changes to your dbt project | dbt Core artifacts don’t refresh on their own and have to be uploaded again | Step 3 |
| Lineage appears, but model and column descriptions don’t | The connected warehouse is Snowflake, which uses its own native object descriptions instead | [How the connector works](/user-guide/snowflake-horizon/connectors/dbt) |

Expand

Show lessSee more

## Connection security

Horizon Catalog doesn’t connect to dbt for a dbt Core connection, so no dbt credentials are
involved. The build artifacts you upload are staged in your own Snowflake account, in the database
and schema you select when you create the connection.

For more details, see
[Security and data protection](/user-guide/snowflake-horizon/connectors/security).
