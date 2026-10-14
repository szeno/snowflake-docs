# Tableau Cloud

## Overview

Horizon Catalog ingests Tableau Cloud metadata (workbooks, data sources, fields, and lineage)
through the REST API and the Metadata API, and ingests view and workbook usage through the
[VizQL Data Service (VDS)](https://help.tableau.com/current/api/vizql-data-service/en-us/index.html),
using the platform **Admin Insights** data sources. By the time you finish this guide you’ll have:

1. Confirmed the metadata permissions setting that lets Horizon Catalog read database and table
   metadata.
2. A Tableau Connected App that Horizon Catalog uses to authenticate.
3. Confirmed Admin Insights is available for usage ingestion.
4. An active Tableau connection in the Horizon Catalog UI.

## Prerequisites

- A Tableau Cloud user with the **Site Administrator Explorer** site role at minimum, with access
  to the **Admin Insights** project. Horizon Catalog signs in as this user through the Connected
  App.
- Permission to create and enable a Connected App on the site.
- Admin Insights enabled on your site, with the platform-published data sources **TS Events** and
  **TS Users** available in the **Admin Insights** project.
- Access to the Horizon Catalog connector wizard: sign in to Snowflake, open
  **Catalog > Connections**, and select **Tableau**.

Complete the following steps to connect Tableau Cloud to Horizon Catalog:

1. [Enable metadata permissions](#1-enable-metadata-permissions).
2. [Create and enable a Connected App](#2-create-and-enable-a-connected-app).
3. [Verify Admin Insights access](#3-verify-admin-insights-access).
4. [Create the Tableau connection](#4-create-the-tableau-connection).
5. [Set up metadata access](#5-set-up-metadata-access).

## 1. Enable metadata permissions

The Metadata API is always enabled by default on Tableau Cloud. No action is required to turn it
on.

Horizon Catalog also relies on Tableau’s derived-permissions setting to read database and table
metadata for the content it indexes:

1. Sign in to Tableau Cloud as a site admin.
2. From the left navigation pane, select **Settings**, then open the **General** tab.
3. Scroll to **Automatic Access to Metadata about Databases and Tables** and select the checkbox
   labeled **Automatically grant authorized users access to metadata about databases and tables**.
4. Select **Save**.

Note

If your site has a large number of workbooks, Tableau Cloud can take some time to finish indexing
metadata after you enable this setting.

## 2. Create and enable a Connected App

Horizon Catalog authenticates with a Tableau Connected App that uses direct trust. You create the
Connected App in Tableau; Horizon Catalog signs a short-lived token with the app’s secret. You
don’t create that token yourself.

1. Sign in to Tableau Cloud as a site admin.
2. From the left pane, select **Settings > Connected Apps**.
3. Select the **New Connected App** drop-down arrow, then select **Direct Trust**.
4. Enter a name for the Connected App, then select **Create**. You can ignore **Access level** and
   **Domain allowlist**. Those settings apply only to embedding workflows.
5. Next to the Connected App name, select the actions menu, then select **Enable**. Tableau creates
   Connected Apps as disabled.
6. Note the Connected App ID, also called the **Client ID**.
7. On the Connected App detail page, select **Generate New Secret**.
8. Copy the **Secret ID** and **Secret Value**, and store them somewhere safe. Tableau shows the
   secret value only once.

Note

The **Username** you enter in Horizon Catalog must be an existing Tableau Cloud user, identified
by email address, with the **Site Administrator Explorer** site role at minimum. Horizon Catalog
signs in as that user so it can retrieve metadata from the Tableau API and access the
**Admin Insights** project. The Connected App name is not a Tableau user.

For details, see
[Configure Connected Apps with Direct Trust](https://help.tableau.com/current/online/en-us/connected_apps_direct.htm)
in the Tableau documentation.

## 3. Verify Admin Insights access

Horizon Catalog ingests view usage and user data through the platform **Admin Insights**
published data sources **TS Events** and **TS Users**.

Note

Admin Insights must be enabled on your Tableau Cloud site. Without access to **TS Events** and
**TS Users** in the **Admin Insights** project, Horizon Catalog cannot collect view popularity or
user information.

1. In the left navigation pane, select **Explore**, then open the **Admin Insights** project.
2. Confirm that the published data sources **TS Events** and **TS Users** are available.

These are platform data sources that Tableau Cloud provides when Admin Insights is enabled.
Horizon Catalog uses **TS Events** for view usage and **TS Users** for user information. If
either data source is missing, contact your Tableau Cloud administrator to enable Admin Insights
for your site. For more information, see
[Monitor site activity with Admin Insights](https://help.tableau.com/current/online/en-us/adminview_insights_events.htm).

## 4. Create the Tableau connection

In Snowflake, open **Catalog > Connections** and select **Tableau** from the Metadata connections
section. Fill out the setup form with the following fields:

| Field | Value |
| --- | --- |
| Display Name | A name for this data source (for example, `Tableau Cloud`) |
| Deployment type | Select **Tableau Cloud** |
| Base URL | The URL of your Tableau Cloud site (for example, `https://10ax.online.tableau.com`) |
| Site ID | The name of your site. Extract it from the URL you use to access Tableau. For example, `analytics` is the site ID for `https://10ax.online.tableau.com/#/site/analytics/home`. |
| Client ID | The Connected App ID from Step 2 |
| Secret ID | The secret ID from Step 2. A Connected App can have more than one secret; Horizon Catalog uses this value to select the correct one |
| Secret Value | The secret value from Step 2 |
| Username | The email address of a Tableau Cloud user with the **Site Administrator Explorer** site role at minimum |
| Snowflake Database | The Snowflake database where metadata is stored (for example, `CONNECTORS`) |
| Snowflake Schema | The Snowflake schema where metadata is stored (for example, `METADATA`) |

Expand

Show lessSee more

Select **Connect**.

Your metadata should start loading automatically. Allow 24–48 hours to fully populate view usage
and lineage.

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
| No metadata appears after connecting | The derived-permissions setting isn’t enabled on the site | Step 1 |
| Connection fails with an authentication error | The Connected App is disabled, the Client ID is for a different site, the secret is wrong, or the Username isn’t an existing Tableau Cloud user on this site | Step 2 |
| Sign-in reports that the Connected App is disabled | The Connected App was created but never enabled | Step 2 |
| Sign-in reports that the Client ID doesn’t match the Tableau site | The Client ID was generated on a different Tableau site than the **Base URL** and **Site ID** | Step 2 |
| View or user usage data is missing | Admin Insights isn’t enabled, or the TS Events / TS Users data sources are missing from the Admin Insights project | Step 3 |
| Metadata appears but takes a long time to fully populate | Large workbook counts slow down Tableau Cloud’s own metadata indexing. This is expected and doesn’t require action | Step 1 |

Expand

Show lessSee more

## Connection security

All communication between Horizon Catalog and Tableau Cloud uses HTTPS (TLS 1.2 or higher).
Tableau Cloud always terminates TLS with a publicly trusted certificate, so no additional
encryption configuration is required. Authentication uses a Tableau Connected App (direct trust).
Horizon Catalog stores the Client ID, Secret ID, Secret Value, and Username as encrypted secrets.

For more details, see
[Security and data protection](/user-guide/snowflake-horizon/connectors/security).
