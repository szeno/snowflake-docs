# Tableau Server

## Overview

Horizon Catalog ingests Tableau Server metadata (workbooks, projects, data sources, fields, and
lineage), along with user information, through the REST API and the Metadata API. By the time you
finish this guide you’ll have:

1. Confirmed your server version and enabled the Metadata API.
2. A Tableau Connected App that Horizon Catalog uses to authenticate.
3. (Optional) Prepared to enable view and workbook usage/popularity data.
4. An active Tableau connection in the Horizon Catalog UI, with usage data flowing in
   automatically if you completed step 3.

View and workbook usage requires an optional setup step

Unlike Tableau Cloud, Tableau Server has no platform-provided “Admin Insights” project, so Horizon
Catalog can’t ingest view and workbook usage/popularity data out of the box. Step 3 below walks
through a one-time, self-serve setup: install a driver and retrieve one extra credential to enter
when you create your connection in Step 4. After that, Horizon Catalog publishes two small views
over your server’s own repository database, and usage ingests through the exact same path
used for Tableau Cloud. Metadata and user information are ingested today regardless of whether you
complete this step.

## Prerequisites

- Tableau Server version **2022.1** or later, so you can create a Connected App with direct
  trust. For metadata and user ingestion (steps 1, 2, and 4), Tableau Server 2022.1 is the
  minimum. If you also want view and workbook usage/popularity data (step 3, optional), you need
  **Tableau Server 2025.1 or later**. The VizQL Data Service (VDS) that step relies on was only
  made generally available for Tableau Server starting with that release. If you need to upgrade
  your Tableau Server, see:
  - [Preparing for Upgrade](https://help.tableau.com/current/server-linux/en-us/server-upgrade-prepare.htm)
  - [Upgrading from 2018.1 and Later (Linux)](https://help.tableau.com/current/server-linux/en-us/sug_plan.htm)
- A Tableau Server user with the **Site Administrator Explorer** site role at minimum. Horizon
  Catalog signs in as this user through the Connected App.
- Permission to create and enable a Connected App. On Tableau Server this is typically a server
  administrator.
- Admin access to Tableau Services Manager (TSM) on the initial node, to enable the Metadata API.
- A Tableau Server URL that is reachable from the internet over HTTPS, either directly or
  through an internet-facing load balancer or proxy you control. Horizon Catalog doesn’t
  guarantee stable egress IPs, so an IP allowlist can stop working without notice. For details,
  see
  [Horizon Catalog egress](/user-guide/snowflake-horizon/connectors/security#horizon-catalog-egress).
- Access to the Horizon Catalog connector wizard: sign in to Snowflake, open
  **Catalog > Connections**, and select **Tableau**.

Complete the following steps to connect Tableau Server to Horizon Catalog:

1. [Enable the REST API and Metadata API](#1-enable-the-rest-api-and-metadata-api).
2. [Create and enable a Connected App](#2-create-and-enable-a-connected-app).
3. [(Optional) Enable view and workbook usage](#3-optional-enable-view-and-workbook-usage).
4. [Create the Tableau connection](#4-create-the-tableau-connection).
5. [Set up metadata access](#5-set-up-metadata-access).

## 1. Enable the REST API and Metadata API

The REST API is enabled by default on all supported versions of Tableau Server.

The Metadata API ships with Tableau Server but is disabled by default. A server admin must enable
it from the command line:

1. Open a command prompt as an admin on the initial node (where TSM is installed) in the cluster.
2. Run:

   Copy code

   ```
   tsm maintenance metadata-services enable
   ```

   This starts an initial metadata ingestion and temporarily restarts some Tableau Server
   services. For more information, see
   [Enable the Tableau Metadata API for Tableau Server](https://help.tableau.com/current/api/metadata_api/en-us/docs/meta_api_start.html#enable-the-tableau-metadata-api-for-tableau-server).

Horizon Catalog also relies on Tableau’s derived-permissions setting to read database and table
metadata for the content it indexes:

1. Sign in to Tableau Server as a site admin.
2. From the left navigation pane, select **Settings**, then open the **General** tab.
3. Scroll to **Automatic Access to Metadata about Databases and Tables** and select the checkbox
   labeled **Automatically grant authorized users access to metadata about databases and tables**.
4. Select **Save**.

## 2. Create and enable a Connected App

Horizon Catalog authenticates with a Tableau Connected App that uses direct trust. You create the
Connected App in Tableau; Horizon Catalog signs a short-lived token with the app’s secret. You
don’t create that token yourself.

1. Sign in to Tableau Server as a server admin.
2. From the left pane, select **Settings > Connected Apps**.
3. Select the **New Connected App** drop-down arrow, then select **Direct Trust**. If you use
   Tableau Server 2023.3 or earlier, select **New Connected App**.
4. Enter a name for the Connected App, then select **Create**. You can ignore **Access level** and
   **Domain allowlist**. Those settings apply only to embedding workflows.
5. Next to the Connected App name, select the actions menu, then select **Enable**. Tableau creates
   Connected Apps as disabled.
6. Note the Connected App ID, also called the **Client ID**.
7. On the Connected App detail page, select **Generate New Secret**.
8. Copy the **Secret ID** and **Secret Value**, and store them somewhere safe. Tableau shows the
   secret value only once.

Note

The **Username** you enter in Horizon Catalog must be an existing Tableau Server user, identified
by username, with the **Site Administrator Explorer** site role at minimum. Horizon Catalog signs
in as that user so it can retrieve metadata from the Tableau API. The Connected App name is not a
Tableau user.

For details, see
[Configure Connected Apps with Direct Trust](https://help.tableau.com/current/server/en-us/connected_apps_direct.htm)
in the Tableau documentation.

## 3. (Optional) Enable view and workbook usage

Tableau Cloud has a built-in “Admin Insights” project with prebuilt `TS Events` and `TS Users`
data sources that Horizon Catalog queries for usage/popularity data. Tableau Server has no
equivalent out of the box, but Horizon Catalog can create one for you: complete the two steps
below (install a driver, retrieve a credential) before creating your connection in Step 4, and
Horizon Catalog publishes two small, read-only data sources (`TS Events` and `TS Users`) backed
by Tableau Server’s own repository database, into a dedicated project, then queries them through
the same VizQL Data Service (VDS) API path used for Tableau Cloud. This is entirely self-contained
(no external services, no new inbound firewall rules) and safe to skip. Metadata and user
ingestion work identically either way.

Note

This step is optional. If you skip it, Horizon Catalog logs a non-blocking warning on each
ingestion run and continues normally without usage data.

Requires **Tableau Server 2025.1 or later**. The VizQL Data Service (VDS) this step relies on is
only available on Tableau Server starting with that release (it’s been available on Tableau Cloud
for longer). We validated this end-to-end setup against Tableau Server 2026.2.0 (build
20262.26.0603.1643), the latest release available at the time of writing; earlier 2025.1+ releases
should work the same way since the REST/VDS endpoints this step uses haven’t changed since GA.

Horizon Catalog attempts provisioning automatically on every connection validation and ingestion
run once you’ve entered the workgroup database password when creating your connection (Step 4),
but never blocks metadata, user, or usage ingestion if it fails. See
[Troubleshooting](#troubleshooting) if the usage warning persists.

### 3.1 Install the PostgreSQL driver (skip if already installed)

Tableau Server needs its own PostgreSQL JDBC driver to query any PostgreSQL-backed data source.
This is the same driver required for the built-in [Administrative Views](https://help.tableau.com/current/server-linux/en-us/adminview.htm), so many servers already
have it. If `/opt/tableau/tableau_driver/jdbc/` doesn’t already contain a `postgresql-*.jar`, install
it:

Copy code

```
sudo mkdir -p /opt/tableau/tableau_driver/jdbc
sudo curl -fsSL -o /opt/tableau/tableau_driver/jdbc/postgresql-42.2.14.jar \
  https://downloads.tableau.com/drivers/linux/postgresql/postgresql-42.2.14.jar
tsm restart
```

See Tableau’s [Database Drivers](https://help.tableau.com/current/server-linux/en-us/dbdriver.htm)
page for the current recommended driver version and multi-node install notes (the driver must be
present on every node running Application Server, Backgrounder, Data Server, or VizQL Server).

### 3.2 Retrieve the workgroup database password

Horizon Catalog can publish `TS Events` and `TS Users` for you, with no script to run. All it needs is
your server’s workgroup database `readonly` password, read straight from TSM on the initial node
(nothing leaves your network beyond this one read):

Copy code

```
tsm configuration get -k pgsql.readonly_password
```

Copy this value. You’ll enter it in the **Workgroup Database Password** field when creating your
Tableau connection in Step 4.

Note

This field is optional. Leave it blank to skip view and workbook usage ingestion. Metadata and
user ingestion are unaffected.

## 4. Create the Tableau connection

In Snowflake, open **Catalog > Connections** and select **Tableau** from the Metadata connections
section. Fill out the setup form with the following fields:

| Field | Value |
| --- | --- |
| Display Name | A name for this data source (for example, `Tableau Server`) |
| Deployment type | Select **Tableau Server** |
| Base URL | The URL of your Tableau Server instance (for example, `https://tableau.mycompany.com`) |
| Site ID | The name of your site, if your server hosts more than one. Extract it from the URL you use to access Tableau. For example, `analytics` is the site ID for `https://tableau.mycompany.com/#/site/analytics/home`. Use `default` for the default site. |
| Client ID | The Connected App ID from Step 2 |
| Secret ID | The secret ID from Step 2. A Connected App can have more than one secret; Horizon Catalog uses this value to select the correct one |
| Secret Value | The secret value from Step 2 |
| Username | The Tableau Server username of a user with the **Site Administrator Explorer** site role at minimum |
| Workgroup Database Password | Optional. The password you retrieved in Step 3.2, if you completed it. This enables automatic view and workbook usage ingestion. Leave blank to skip usage ingestion (see Step 3). |
| Snowflake Database | The Snowflake database where metadata is stored (for example, `CONNECTORS`) |
| Snowflake Schema | The Snowflake schema where metadata is stored (for example, `METADATA`) |

Expand

Show lessSee more

Select **Connect**.

Your metadata should start loading automatically. Allow 24–48 hours to fully populate lineage.

If you provided the Workgroup Database Password, Horizon Catalog also checks whether the
`TS Events`/`TS Users` usage data sources already exist under the `HorizonStar Admin Insights`
project and, if not, creates the project (if needed) and publishes both, typically within a few
seconds of the next connection validation or ingestion run, with no further action from you. To
verify, open Tableau Server in your browser and confirm the project and data sources appear; usage
then flows in automatically on the next ingestion run.

## 5. Set up metadata access

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
| No metadata appears after connecting | The Metadata API was never enabled, or the derived-permissions setting isn’t enabled on the site | Step 1 |
| Connection fails with an authentication error | The Connected App is disabled, the Client ID is for a different site, the secret is wrong, or the Username isn’t an existing Tableau Server user on this site | Step 2 |
| Sign-in reports that the Connected App is disabled | The Connected App was created but never enabled | Step 2 |
| Sign-in reports that the Client ID doesn’t match the Tableau site | The Client ID was generated on a different Tableau site than the **Base URL** and **Site ID** | Step 2 |
| No view or workbook usage/popularity data, and Horizon Catalog logs a non-blocking “usage datasources not found” warning | The workgroup database password (Step 3.2) wasn’t entered when creating the connection, or auto-provisioning hasn’t run yet; it happens on the next connection validation/ingestion, not immediately after connecting | Steps 3-4 |
| Usage warning persists even after providing the workgroup database password | The PostgreSQL JDBC driver isn’t installed (or `tsm restart` wasn’t run after installing it), the password is incorrect, or the site’s Tableau user lacks permission to create/publish to projects. Check Tableau Server’s logs for the underlying error | Step 3.1 |

Expand

Show lessSee more

## Connection security

All communication between Horizon Catalog and Tableau Server uses HTTPS (TLS 1.2 or higher), and
Horizon Catalog verifies your server’s TLS certificate by default. Authentication uses a Tableau
Connected App (direct trust). Horizon Catalog stores the Client ID, Secret ID, Secret Value, and
Username as encrypted secrets. The optional Workgroup Database Password, if you provide it, is
also stored as an encrypted secret.

For more details, see
[Security and data protection](/user-guide/snowflake-horizon/connectors/security).
