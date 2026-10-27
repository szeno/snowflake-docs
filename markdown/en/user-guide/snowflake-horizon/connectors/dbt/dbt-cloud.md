# dbt Cloud

## Overview

Horizon Catalog ingests dbt model metadata and model-to-model lineage from a scheduled dbt Cloud
job, through the dbt Cloud API. After the initial connection, the job keeps your metadata up to
date automatically. By the time you finish this guide you’ll have:

1. A dbt Cloud service token Horizon Catalog uses to authenticate.
2. A dbt Cloud job that generates the build artifacts on a daily schedule.
3. The job ID that tells Horizon Catalog which job to read.
4. An active dbt connection in the Horizon Catalog UI.

## Prerequisites

- A warehouse data source already connected in Horizon Catalog. The dbt connector enriches an
  existing data source rather than creating one.
- A dbt Cloud service token with **Metadata Only** and **Read Only** permissions. For dbt Enterprise
  accounts, the token needs the [Job Viewer](https://docs.getdbt.com/docs/cloud/manage-access/enterprise-permissions#job-viewer)
  and [Account Viewer](https://docs.getdbt.com/docs/cloud/manage-access/enterprise-permissions#account-viewer)
  permissions instead.
- Access to the Horizon Catalog connector wizard: sign in to Snowflake, open
  **Catalog > Connections**, and select **dbt** from the **Data pipeline tools** section.

## 1. Configure a dbt Cloud job

Horizon Catalog reads the build artifacts that a dbt Cloud job produces, so the job has to produce
a manifest, generate documentation, run tests, and run on a schedule:

1. In dbt Cloud, create a job and select the environment to run it in.
2. Enable **Generate docs on run**. Horizon Catalog uses this step for `catalog.json`.
3. Add the command `dbt compile`, unless the job already runs `dbt build` or `dbt run`. Horizon
   Catalog accepts `manifest.json` from a successful `dbt compile`, and from `dbt run` or `dbt build`.

   Note

   `dbt compile --full-refresh` is optional. It compiles incremental models as a full SELECT instead
   of a MERGE, which keeps upstream lineage in the compiled SQL. It doesn’t run the models. Leave
   the flag off for a project that rejects `flags.FULL_REFRESH`. Adding it fails the job, and
   Horizon Catalog then has no manifest.
4. Add the command `dbt test`. Horizon Catalog reads test outcomes from this step, including
   failures. `dbt compile` and **Generate docs on run** do not execute tests, so
   `run_results.json` either omits those tests or records synthetic success. Failed tests never
   appear unless `dbt test` or `dbt build` actually runs the tests.

   Note

   If the job already runs `dbt build`, omit a separate `dbt test` command. `dbt build` runs models
   and tests, and Horizon Catalog still ingests the manifest and failed tests when the job ends in
   Error.
5. Schedule the job to run daily at 4:00 a.m., so it finishes before the Horizon Catalog ingestion
   runs and your metadata stays current.
6. Save the job.
7. Select **Run now** and wait until the run finishes. A run that ends in Error because a test
   failed is still usable.

   Warning

   Don’t connect the job if compile failed. A truncated manifest can remove models from Horizon
   Catalog.

## 2. Get the job ID

Open the job in dbt Cloud and copy the job ID from the URL. The job ID is the last number in the
path:

Copy code

```
https://<access-url>/deploy/<account-id>/projects/<project-id>/jobs/<job-id>
```

Here `<access-url>` is your dbt Cloud access URL: `cloud.getdbt.com` for most accounts, or an
account-specific URL such as `ab123.us1.dbt.com` if your account has been migrated.

## 3. Create a dbt connection

In Snowflake, open **Catalog > Connections** and select **dbt** from the **Data pipeline tools**
section. Set **dbt type** to **dbt Cloud**, then fill out the setup form with the following fields:

| Field | Value |
| --- | --- |
| Display Name | A name for this data source, which defaults to `dbt` |
| dbt type | Select **dbt Cloud** |
| Connected Warehouse | The existing warehouse data source that your dbt models are built in (for example, Snowflake, BigQuery, or Amazon Redshift) |
| Access URL | The access URL for your dbt Cloud account, which defaults to `https://cloud.getdbt.com`. Update it if you use a region-specific or single-tenant account. |
| dbt Job ID | The job ID from [Step 2](#2-get-the-job-id) |
| API Key | Your dbt Cloud service token, from [Prerequisites](#prerequisites) |
| Snowflake Database | The Snowflake database where Horizon Catalog stores the connector metadata, which defaults to `CONNECTORS` |
| Snowflake Schema | The Snowflake schema where Horizon Catalog stores the connector metadata, which defaults to `METADATA` |

Expand

Show lessSee more

Select **Next** to continue to the **Load data** step, where Horizon Catalog ingests the dbt
metadata. After the initial connection, the scheduled dbt Cloud job keeps your metadata up to date.
No further action is required.

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
| The connection fails with an authentication error | The service token is expired, or it doesn’t have the Metadata Only and Read Only permissions | Prerequisites |
| The connection succeeds, but no dbt metadata appears | The job hasn’t completed a run that produced a compile or build `manifest.json` | Step 1 |
| Metadata stops reflecting changes to your dbt project | The job schedule is turned off, or recent runs are failing compile | Step 1 |
| dbt tests all show success, including tests that fail in dbt Cloud | The job doesn’t run `dbt test` or `dbt build`, so test outcomes are missing or recorded as synthetic success | Step 1 |
| Lineage appears, but model and column descriptions don’t | The connected warehouse is Snowflake, which uses its own native object descriptions instead | [How the connector works](/user-guide/snowflake-horizon/connectors/dbt) |

Expand

Show lessSee more

## Connection security

All communication between Horizon Catalog and dbt Cloud uses HTTPS (TLS 1.2 or higher).
Authentication uses a dbt Cloud service token, which is stored as an encrypted secret. No
additional encryption configuration is required.

For more details, see
[Security and data protection](/user-guide/snowflake-horizon/connectors/security).
