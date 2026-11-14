# Convert Tableau workbooks to Streamlit in Snowflake apps with CoCo

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

## Overview

The `tableau-to-streamlit-in-snowflake` skill for Cortex Code (CoCo) converts a Tableau workbook
into a multipage Streamlit in Snowflake app. CoCo reads the workbook’s saved definitions and builds one app page
for each Tableau dashboard. Worksheets become native Streamlit charts and tables, calculations
become Snowflake SQL, and dashboard filters, parameters, and actions become Streamlit widgets
and chart selections.

You review the app on synthetic data first. CoCo switches it to your Snowflake tables only after
you approve the UI and the real-data mapping. To get started, see
[Migrate in CoCo CLI or CoCo Desktop](#label-streamlit-tableau-cli-desktop) or [Migrate in CoCo in Snowsight](#label-streamlit-tableau-snowsight).

The skill is bundled with CoCo CLI, CoCo Desktop, and CoCo in Snowsight. You don’t need
to download, copy, or install the skill. To start a migration, type
`/tableau-to-streamlit-in-snowflake` in the CoCo chat, or describe the task, for example
“convert this Tableau workbook to a Streamlit in Snowflake app.” To create semantic views from
Tableau files instead, use the
[`agent-studio` skill](/user-guide/cortex-code/bundled-skills#label-bundled-skill-agent-studio).

## How a migration works

A migration has four phases. The example prompts on this page use the same phases. The
following table describes what CoCo does in each phase and where it stops for your approval:

| Phase | What CoCo does | Where CoCo stops for your approval |
| --- | --- | --- |
| 1. Analyze the workbook | Inventories the workbook’s saved definitions: data sources, fields, calculations, worksheets, dashboards, filters, parameters, and actions. It doesn’t read data rows. For each worksheet in scope, CoCo writes parameterized SQL that returns the same level of detail as the worksheet (its grain), for example one row per region and month, or reports why it can’t. | The scope and data mode, before CoCo writes SQL. If either is unclear, CoCo returns the inventory and its open questions instead of guessing. For a synthetic preview that CoCo deploys, keep the full workbook in scope. Then the file plan, before CoCo writes any file: the in-scope dashboards and worksheets, the destination folder, the exact files, the dashboard-to-page mapping, how each action is handled, and any known partial items. |
| 2. Build the synthetic preview | Builds the app on synthetic data that matches the workbook’s fields and grain, so you can review the UI before any real data is involved. In CoCo CLI and CoCo Desktop, CoCo deploys the preview. In Snowsight, you run it. | In CoCo CLI and CoCo Desktop, the deployment target, before the first deployment. |
| 3. Iterate on the UI | Applies the UI changes you request to the same app. | Any new package dependency, external access integration, or change to the approved target. |
| 4. Cut over to real data | Replaces the synthetic data layer with real Snowflake queries in the same app. | The [real-data details](#label-streamlit-tableau-cutover), and then the real-data mapping and file changes. |

Expand

Show lessSee more

### Data modes

CoCo needs an explicit data mode before it writes SQL. A full migration uses two modes in order:
it starts in `prototype_synthetic` and switches to `real` in the same app. CoCo moves an app to
`real` only by cutting over a synthetic preview. `code_only` is a separate option for building
the app without Snowflake access. The following table describes each data mode:

| Mode | What CoCo builds | Reads Snowflake data | Deploys the app |
| --- | --- | --- | --- |
| `code_only` | The app and its parameterized SQL, written against the exact tables and columns you supply. For an example, see [Build the app without Snowflake access](#label-streamlit-tableau-code-only). | No. CoCo doesn’t inspect, compile, or run anything in Snowflake. | No. You deploy the app yourself. |
| `prototype_synthetic` | The app, running on synthetic data stored in the app’s files. | No. | In CoCo CLI and CoCo Desktop, only to a target that you approve. In Snowsight, you run the app yourself. |
| `real` | The same app, with SQL that reads the tables and columns you confirm and follows the joins and security rules you confirm. | Only the read-only metadata, compile, and result checks that you approve. CoCo doesn’t write to source tables. | Only by cutting over a synthetic preview of the same app. In CoCo CLI and CoCo Desktop, CoCo redeploys it to the approved target. In Snowsight, you run it yourself. |

Expand

Show lessSee more

### Approval rules

CoCo asks for your explicit approval before it queries real tables, deploys an app, or grants
access to the app. Exact values that you give in your prompt count as approval. Defaults and
inferred values don’t.

- Approving the file plan doesn’t approve any query, Snowflake object, or deployment.
- In CoCo CLI and CoCo Desktop, the deployment target is the set of values in the
  `Approved Snowflake target` block of the [prompt](#label-streamlit-tableau-cli-desktop).
  Before the first deployment, CoCo confirms that the connection’s account and role match the
  target. If an app with the same name already exists, CoCo reports its owner and asks before
  replacing it.

## Prerequisites

For every CoCo surface, you need:

- A Tableau workbook or data source file. For more information about supported formats, see
  [Prepare the Tableau source](#label-streamlit-tableau-prepare-source). In CoCo CLI and CoCo Desktop, you can instead use
  a Tableau Model Context Protocol (MCP) server connected to CoCo.
- A role with `USAGE` on the target database, schema, query warehouse, and compute pool, and the
  `CREATE STREAMLIT` privilege on the schema. For more information, see
  [Privileges required to create a Streamlit app](/developer-guide/streamlit/object-management/privileges#label-streamlit-access-privs-create).
- A query warehouse and a compute pool. The app runs in a container runtime. For more
  information, see [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments).

In CoCo in Snowsight, the
[Streamlit in Snowflake in Workspaces prerequisites](/developer-guide/streamlit/streamlit-in-workspaces/streamlit-in-workspaces-overview#label-streamlit-in-workspaces-prereqs)
also apply. The account must have a default compute pool, and your user must have a default
warehouse.

In CoCo CLI and CoCo Desktop, you also need:

- CoCo CLI version 1.2.33 or later, or CoCo Desktop version 1.23.1 or later. Earlier versions
  don’t include the skill. To check your CoCo CLI version, run `cortex --version`, and to update
  it, run `cortex update`. To update CoCo Desktop, select **Check for Updates** in the app menu.
- Python 3.11 or later. You don’t need to install any Python packages: the skill’s workbook
  inspector uses only the Python standard library. To check your version, run
  `python3 --version`, or `py -3.11 --version` on Windows.
- Snowflake CLI version 3.14 or later, or [uv](https://docs.astral.sh/uv/). If
  `snow --version` doesn’t report Snowflake CLI version 3.14 or later, CoCo runs the current
  Snowflake CLI release with `uvx`. For installation instructions, see
  [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation).
- A Snowflake CLI connection profile for the account that holds the data behind the Tableau
  dashboard. To check the profile, run `snow connection test -c <CONNECTION_NAME>`. For more
  information, see [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections).

For the real-data cutover, you also need:

- The source tables in Snowflake, in the same account as the app.
- A decision about how the app runs its queries:
  - With owner’s rights, every query runs as the app owner role, which is the deployment role
    in CoCo CLI and CoCo Desktop. Every viewer sees the data that this role can read, at the
    grain that the app displays. The role needs `SELECT` on the source tables. Use a role that
    has only the privileges that the app needs. For more information, see
    [Understanding owner’s rights and Streamlit in Snowflake apps](/developer-guide/streamlit/object-management/owners-rights).
  - With restricted caller’s rights, each query runs as the viewer, so Snowflake applies that
    viewer’s grants and policies. Use restricted caller’s rights if each viewer must see only
    the data that their own grants and policies allow. An administrator with the
    `MANAGE CALLER GRANTS` privilege must give the app owner role caller grants on the source
    database, schema, and tables, and each viewer’s default role needs access to the source
    tables. CoCo doesn’t create caller grants. For more information, see
    [Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights).

## Prepare the Tableau source

Export the workbook or data source from Tableau. CoCo supports these file formats:

| Extension | Contents | What CoCo reads |
| --- | --- | --- |
| `.twb` | Workbook XML: data sources, fields, formulas, worksheets, dashboards, filters, and actions. | All workbook definitions. |
| `.twbx` | A packaged workbook: a `.twb` file plus supporting files such as extracts and images. | The workbook definitions. Other files in the package are listed but not read. |
| `.tds` | A data source definition without data rows. | The data source definitions. A data source file has no worksheets or dashboards. |
| `.tdsx` | A packaged data source: a `.tds` file plus local supporting files. | The data source definitions. Other files in the package are listed but not read. |
| `.hyper`, `.tde` | Tableau extract databases. | Not supported. CoCo doesn’t read extract data. |

Expand

Show lessSee more

Keep the following in mind:

- Prefer an unpackaged `.twb` file when a `.twbx` file contains a large extract. CoCo refuses
  packages larger than 512 MiB unless you explicitly agree to inspect one larger package, up to
  4 GiB.
- Don’t use a screenshot, PDF, or CSV export in place of the workbook file. These exports don’t
  contain the workbook’s calculations or structure. You can add dashboard screenshots to refine
  the app’s appearance.
- In CoCo CLI and CoCo Desktop, you can let CoCo find and download the workbook for you through a
  Tableau MCP server connected to CoCo. CoCo uses only the server’s read-only search, metadata,
  and download tools, and doesn’t query Tableau data sources or export view data. To enforce
  this, allow only those tools in CoCo’s MCP permissions, and connect the server with a Tableau
  token that can only find and download the workbooks that you’re migrating. For more
  information, see [CoCo CLI Model Context Protocol (MCP) support](/user-guide/cortex-code/cortex-code-mcp) and
  [MCP support in CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop/mcp-support).
- Keep workbook files, extracts, CoCo’s inventory reports, and credentials out of version
  control. Don’t paste tokens or passwords into the chat.

CoCo treats all text in the workbook, including names, captions, formulas, and annotations, as
untrusted data, and the skill instructs CoCo not to follow instructions or links found in the
workbook. Migrate only workbooks from sources that you trust, and review each action that CoCo
proposes before you approve it.

## Migrate a workbook

Follow the procedure for your CoCo surface. Both procedures end with the same real-data cutover
and checks.

### Migrate in CoCo CLI or CoCo Desktop

In CoCo CLI and CoCo Desktop, CoCo builds the app on your machine and deploys it to Snowflake
with the Snowflake CLI.

1. Save the exported workbook on your machine and note its absolute path.
2. Start CoCo CLI in the folder where you want to work, or open that folder in CoCo Desktop. To
   confirm that the skill is available, type `/tableau` in the chat and check that
   `tableau-to-streamlit-in-snowflake` appears. In CoCo CLI, you can also run `/skill list`.
3. Copy the following prompt, replace the placeholders in the `Workbook`, `Output directory`,
   and `Approved Snowflake target` lines, and send it. Send the rest of the prompt as is.

   - `<CONNECTION_NAME>`: A profile from `snow connection list` for the account that holds the
     data behind the Tableau dashboard.
   - `<ORGANIZATION_NAME>` and `<ACCOUNT_NAME>`: Run
     `SELECT CURRENT_ORGANIZATION_NAME(), CURRENT_ACCOUNT_NAME();` with that connection.
   - `<ABSOLUTE_OUTPUT_DIRECTORY>`: A new, empty folder. CoCo writes the app to its `app`
     subfolder.
   - `<AUDIENCE_ROLES>`: A comma-separated list of roles, or `none`. List only audience roles
     that are allowed to see the real data: the cutover replaces the data in the same app, so
     these roles keep access to the real-data version. To check the real-data app before anyone
     else sees it, use `none` and share the app after you check it. To change the audience
     during the migration, ask CoCo and approve the updated target. If you grant access to the
     app yourself, CoCo stops at its next deployment and reports the extra role.

   If you don’t know a value, delete its line. CoCo asks for any missing value before the first
   deployment and doesn’t fill one in from defaults.

   ```
   Use /tableau-to-streamlit-in-snowflake to migrate this workbook.

   Workbook: <ABSOLUTE_WORKBOOK_PATH>
   Output directory: <ABSOLUTE_OUTPUT_DIRECTORY>
   Data mode: prototype_synthetic first, then real after I approve the UI.

   Approved Snowflake target:
   - Connection profile: <CONNECTION_NAME>
   - Organization: <ORGANIZATION_NAME>
   - Account: <ACCOUNT_NAME>
   - Role: <DEPLOYMENT_ROLE>
   - Database: <DATABASE>
   - Schema: <SCHEMA>
   - App name: <APP_NAME>
   - Query warehouse: <QUERY_WAREHOUSE>
   - Compute pool: <COMPUTE_POOL>
   - Audience roles: <AUDIENCE_ROLES>
   - External access integrations: none

   I approve these values for the first synthetic deployment and for later
   synthetic revisions to the same target, including USAGE grants on the
   app to the listed audience roles. Summarize the target before the first
   deployment. Don't ask me to approve it again unless a value doesn't
   match my connection, a value must change, or an app with this name
   already exists. Ask for approval before you add any new dependency or
   external access integration.

   Phase 1: Analyze the workbook
   Inventory the workbook from its saved Tableau definitions. Build one
   multipage Streamlit app with one page per Tableau dashboard, and include
   every worksheet that appears on a dashboard. Preserve calculations,
   number formats, aliases, colors, filters, parameters, tooltips, layout
   proportions, visual hierarchy, and filter and highlight actions. Don't
   silently omit, replace, or approximate behavior. List anything that's
   blocked or intentionally omitted, with the reason.

   Phase 2: Build and deploy the synthetic app
   Build the complete app with deterministic synthetic data first. Use the
   same pages, visuals, calculations, filters, interactions, and layout
   that the real-data app will have. Don't query real source tables yet.
   Deploy the synthetic app to the approved target, verify the live app and
   its grants, list every check you couldn't run, and return the Snowflake
   URL. Keep the synthetic-data warning on every page, and ask me to test
   every page, filter, parameter, tooltip, label, and layout, and every
   click or hover action, including how its selection clears.

   Phase 3: Iterate on the UI
   Wait for my feedback. Apply the UI or interaction changes I request, and
   redeploy each synthetic revision to the same target. Continue until I
   approve the UI. Don't access real data until I reply
   "UI approved. Proceed with real-data queries."

   Phase 4: Cut over to real data
   After that approval, ask me for the exact Snowflake tables and columns,
   the role and query warehouse that read them, owner's or caller's
   rights, and the read-only checks you may run. Don't search the account
   or infer tables from the workbook's connection metadata. Then map the
   workbook's relationships, joins, calculations, LOD expressions, filter
   order, query grain, and security rules to those tables. Preserve or
   accurately translate custom SQL. Where Tableau generated queries
   dynamically, build equivalent Snowflake SQL from the data source model,
   shelves, calculations, filters, and aggregation grain.

   Never guess an ambiguous mapping. If you can't confirm a source object,
   column, join, permission, or security rule, keep the synthetic app
   deployed and ask me to choose from concrete options.

   Replace only the synthetic data layer and keep the approved UI. Use
   parameterized Snowflake queries, and push aggregation into Snowflake.
   Remove the synthetic-data warnings that the migration added. Then
   redeploy to the same target, verify the live app and its grants, and
   return the Snowflake URL.
   ```

   The approval paragraph lets CoCo deploy the app and grant `USAGE` to the audience roles
   without asking again, so check every value before you send the prompt. To have CoCo ask
   before the first deployment, change `Approved Snowflake target:` to `Snowflake target:` and
   delete the paragraph after the list.
4. CoCo inspects the workbook, asks any open questions, and shows a file plan. Depending on your
   permission settings, CoCo CLI and CoCo Desktop ask for your permission before they run a
   command or SQL statement. Review and allow each one. Because the workbook is untrusted input,
   don’t use a mode that approves commands automatically. Review the file plan, then reply with
   an explicit approval, for example `Approve the file plan.`
5. Open the app URL that CoCo returns. CoCo reports the deployment as an unverified synthetic
   preview: the app runs on synthetic data, and CoCo hasn’t confirmed that it matches the
   Tableau dashboard. CoCo also lists the checks it couldn’t run. Every page shows the warning
   `Synthetic data - Tableau parity not verified`. Review the disposition summary in CoCo’s
   report. For more information about each status and what to do about it, see
   [Disposition summary](#label-streamlit-tableau-statuses).

   When the workbook doesn’t store the members of a dimension, the synthetic data invents them.
   CoCo tells you which labels and colors change when the app switches to real members.
6. Test every page and interaction, and describe the changes you want. CoCo redeploys each
   revision to the same app.
7. When the UI is ready, cut over the same app to real data. For more information, see
   [Cut over to real data](#label-streamlit-tableau-cutover).
8. Check the real-data app before you share it. For more information, see
   [Check and share the app](#label-streamlit-tableau-check-share).

### Migrate in CoCo in Snowsight

In Snowsight, CoCo builds the app in your workspace. CoCo doesn’t deploy the app or
change grants. You run the app yourself.

1. Open a private workspace in Snowsight.
2. Select the CoCo icon [![Cortex Code icon](/static/images/cortex-code/cortex-code-icon.png)](/static/images/cortex-code/cortex-code-icon.png) in the lower-right corner to open the CoCo panel.
3. Upload the workbook in the CoCo chat. Alternatively, add the workbook to the workspace and
   name its path in your prompt. Don’t add a workbook to a shared workspace or commit it from a
   Git-backed workspace.
4. Copy the following prompt, replace the placeholders in the first lines, and send it. For
   `<NEW_APP_FOLDER_NAME>`, use the name of a new top-level folder in the workspace. If you don’t
   know the query warehouse or compute pool yet, delete those lines. You can set them later in
   the project’s **Settings**. For more information, see
   [App settings](/developer-guide/streamlit/streamlit-in-workspaces/streamlit-in-workspaces-create-run#label-streamlit-in-workspaces-settings).

   ```
   Use /tableau-to-streamlit-in-snowflake to migrate this workbook.

   Workbook: <UPLOADED_FILE_NAME_OR_WORKSPACE_PATH>
   App folder: <NEW_APP_FOLDER_NAME>
   Query warehouse: <QUERY_WAREHOUSE>
   Compute pool: <COMPUTE_POOL>
   Data mode: prototype_synthetic first, then real after I approve the UI.

   Phase 1: Analyze the workbook
   Inventory the workbook from its saved Tableau definitions. Build one
   multipage Streamlit app with one page per Tableau dashboard, and include
   every worksheet that appears on a dashboard. Preserve calculations,
   number formats, aliases, colors, filters, parameters, tooltips, layout
   proportions, visual hierarchy, and filter and highlight actions. Don't
   silently omit, replace, or approximate behavior. List anything that's
   blocked or intentionally omitted, with the reason.

   Phase 2: Build the synthetic app
   Build the complete app with deterministic synthetic data first. Use the
   same pages, visuals, calculations, filters, interactions, and layout
   that the real-data app will have. Don't query real source tables yet.
   I'll click Run myself, so don't deploy or change grants. Keep the
   synthetic-data warning on every page, and ask me to test every page,
   filter, parameter, tooltip, label, and layout, and every click or hover
   action, including how its selection clears.

   Phase 3: Iterate on the UI
   Wait for my feedback. Apply the UI or interaction changes I request, and
   I'll click Run again to review each revision. Continue until I approve
   the UI. Don't access real data until I reply
   "UI approved. Proceed with real-data queries."

   Phase 4: Cut over to real data
   After that approval, ask me for the exact Snowflake tables and columns,
   the role and query warehouse that read them, owner's or caller's
   rights, and the read-only checks you may run. Don't search the account
   or infer tables from the workbook's connection metadata. Then map the
   workbook's relationships, joins, calculations, LOD expressions, filter
   order, query grain, and security rules to those tables. Preserve or
   accurately translate custom SQL. Where Tableau generated queries
   dynamically, build equivalent Snowflake SQL from the data source model,
   shelves, calculations, filters, and aggregation grain.

   Never guess an ambiguous mapping. If you can't confirm a source object,
   column, join, permission, or security rule, keep the synthetic app and
   ask me to choose from concrete options.

   Replace only the synthetic data layer in the same app folder and keep
   the approved UI. Use parameterized Snowflake queries, and push
   aggregation into Snowflake. Remove the synthetic-data warnings that the
   migration added, and I'll click Run again.
   ```
5. CoCo inspects the workbook, asks any open questions, and shows a file plan. Review the file
   plan, then reply with an explicit approval, for example `Approve the file plan.` CoCo creates
   the app in a dedicated folder in the workspace, with a `snowflake.yml` file that configures
   **Run**.
6. CoCo reports the app as an unverified synthetic preview: the app runs on synthetic data, and
   CoCo hasn’t confirmed that it matches the Tableau dashboard. CoCo also lists the checks it
   couldn’t run. Open `streamlit_app.py` in the app folder and select **Run**. Every page shows
   the warning `Synthetic data - Tableau parity not verified`. Review the disposition summary in
   CoCo’s report. For more information about each status and what to do about it, see
   [Disposition summary](#label-streamlit-tableau-statuses).
7. Test every page and interaction, and describe the changes you want. After each revision,
   select **Run** again.
8. When the UI is ready, cut over the same app to real data. For more information, see
   [Cut over to real data](#label-streamlit-tableau-cutover).
9. Check the real-data app before you share it. For more information, see
   [Check and share the app](#label-streamlit-tableau-check-share).

### Cut over to real data

When the synthetic preview looks right, switch the same app to your Snowflake tables. Before you
start, gather the values listed for the real-data cutover in
[Prerequisites](#label-streamlit-tableau-prerequisites).

1. Send a reply like the following, with the placeholders replaced:

   ```
   UI approved. Proceed with real-data queries.

   Source tables, in the same account as the app:
   - <TABLEAU_DATA_SOURCE_NAME>: <DATABASE.SCHEMA.TABLE>
   Execution rights: <owner's rights or caller's rights>
   Execution role: <ROLE>
   Query warehouse: <QUERY_WAREHOUSE>
   Read-only checks you can run: <for example, describe the tables,
   compile each query, and run each query once to confirm its columns
   and grain>
   ```

   CoCo asks for any value that’s missing. A compile check doesn’t read data. A result check
   runs the query, so CoCo sees its results. CoCo also reads the real members of any dimension
   whose synthetic members it invented, and lists the members that changed. If CoCo shouldn’t
   see the data, approve only compile checks, and CoCo lists the checks it didn’t run.
2. Review the real-data mapping and file changes that CoCo shows, and approve them. CoCo runs the
   read-only checks that you approved and replaces the synthetic data layer with parameterized
   queries in the same app:

   - In CoCo CLI and CoCo Desktop, CoCo redeploys the same app to the approved target and
     returns the same URL.
   - In Snowsight, CoCo updates the files in the same app folder. Select **Run** again
     to review the real-data version.

The real-data version contains no synthetic rows or synthetic-data warnings. A failed query shows
an error, and the app doesn’t fall back to synthetic data.

### Check and share the app

CoCo doesn’t claim that the app matches Tableau. Compiling a query doesn’t prove that its
results match the workbook. In its report, CoCo states its security assumption and lists every
check that it didn’t run. Before you share the real-data app, check it:

1. Apply the same filters in the app and the Tableau dashboard, and compare key numbers. You can
   also ask CoCo to reconcile the app against Tableau results that you provide.
2. If the app shows viewer-specific data, open it as at least two test users whose default roles
   should see different rows, and confirm that each user sees only their own rows. CoCo’s checks
   run with your connection’s role, so they don’t show what other viewers see.

Then share the app:

- In CoCo CLI and CoCo Desktop, the audience roles that you approved can already open the app.
  To add roles, ask CoCo to add them to the audience roles and approve the updated target. Each
  audience role also needs `USAGE` on the app’s database and schema. For more information, see
  [Privileges required to view a Streamlit app](/developer-guide/streamlit/object-management/privileges#label-streamlit-access-privs-view).
- In Snowsight, the running app is a private development app that only you can see. To
  share it with other users, deploy it from the workspace and share it. If you deployed and shared
  the synthetic version earlier, deploy again so that the deployed app uses real data. The roles
  and users that you shared it with then see the real data. For more information, see
  [Deploy your app](/developer-guide/streamlit/streamlit-in-workspaces/streamlit-in-workspaces-create-run#label-streamlit-in-workspaces-deploy)
  and
  [Share with roles and users](/developer-guide/streamlit/streamlit-in-workspaces/streamlit-in-workspaces-create-run#label-streamlit-in-workspaces-deploy-sharing).

## Other ways to use the skill

In addition to a full migration, you can use the skill to build an app without Snowflake access,
limit the migration to specific dashboards or worksheets, or inventory several workbooks.

### Build the app without Snowflake access

If you know the exact Snowflake tables and columns behind the workbook and want to deploy the
app yourself, use the `code_only` [data mode](#label-streamlit-tableau-data-modes), and name the
mode in your prompt. CoCo writes static parameterized SQL against the tables and columns you
name, but doesn’t compile or run it, and doesn’t deploy the app. For example:

```
Use /tableau-to-streamlit-in-snowflake to convert the <DASHBOARD_NAME>
dashboard in <ABSOLUTE_WORKBOOK_PATH> into a Streamlit in Snowflake app.

Data mode: code_only
Output directory: <ABSOLUTE_OUTPUT_DIRECTORY>
Source table: <DATABASE.SCHEMA.TABLE>
Column mapping: <ABSOLUTE_MAPPING_FILE_PATH>
Worksheets to include: <WORKSHEET_1>, <WORKSHEET_2>
Filters to include: <FILTER_1>, <FILTER_2>

The app reads real data from the source table, not synthetic data. I'll
deploy it myself, so don't query Snowflake, deploy, or change grants
while building it. Flag anything you couldn't verify.
```

The mapping file is a text or Markdown file that lists each Tableau field with its Snowflake
column and data type, and states the table’s row grain, for example “one row per order line.”
In CoCo in Snowsight, name the uploaded workbook instead of a path, and replace
“I’ll deploy it myself” with “I’ll click Run myself.”

CoCo’s report lists every query that wasn’t compiled or run, and any workbook security rule
that’s still open. Because you deploy the app, CoCo doesn’t check the app’s rights or grants, and
CoCo CLI and CoCo Desktop don’t create a `snowflake.yml` file in this mode. If the workbook has
user filters or user functions, enforce them in Snowflake and use restricted caller’s rights
before you share the app. For more information, see [Security](#label-streamlit-tableau-security). Test
the app against your data before you share it.

### Limit the migration to specific dashboards or worksheets

Name the dashboards, worksheets, filters, and measures to include. CoCo builds only what you
list, at the grain you state, and records every omitted workbook element as out of scope. For
example, if your scope includes only `SUM(Sales)`, CoCo doesn’t implement a table calculation,
Top N filter, parameter, or action that’s outside that scope.

A synthetic preview that CoCo deploys requires the full workbook in scope. If you limit the
scope, CoCo builds the app files and asks how you want to proceed: include the full workbook so
that CoCo can deploy a synthetic preview, or keep the files and deploy them yourself, as in
[Build the app without Snowflake access](#label-streamlit-tableau-code-only).

### Inventory several workbooks

Before you choose what to migrate, you can ask CoCo to inventory a folder of workbooks and data
source files. For example:

```
Use /tableau-to-streamlit-in-snowflake to inventory the workbooks in
<ABSOLUTE_DIRECTORY>. Compare calculations, shared fields, and data source
connections. Don't build an app.
```

CoCo reports the dashboards in each file, duplicate or conflicting calculations, fields that
the workbooks share, and how each data source connects to Snowflake. A single inventory covers
up to 500 files. If CoCo can’t inspect every file, it says that the results are partial.

## What CoCo creates

CoCo creates the app files and a disposition summary that records the status of each workbook
element.

### App files

In CoCo CLI and CoCo Desktop, the app files are in the `app` folder of the output directory, and
the migration records are in the `migration` folder beside it. In Snowsight, both are in
the app folder in your workspace. CoCo creates the following files for the app:

| File or folder | Contents |
| --- | --- |
| `streamlit_app.py` | The app’s entry point: page navigation and controls shared across pages. |
| `app_pages/` | One page file for each Tableau dashboard in scope. |
| `sql/` | The parameterized Snowflake SQL for each worksheet. |
| `helpers.py` | Shared functions that load query results, and constants for the workbook’s formats. |
| `tableau_*.py` | Helper modules copied from the skill, for displaying workbook text, formatting numbers, and reading chart selections. CoCo copies only the modules that the app needs. |
| `workbook_map.json` | A record of how each dashboard, worksheet, and action maps to the app, with each element’s status and the reason for any gap. |
| `snowflake.yml` | In CoCo CLI and CoCo Desktop, the Snowflake CLI project definition for the approved target, created when CoCo deploys the synthetic preview. A code-only build doesn’t include one. In Snowsight, the configuration that **Run** uses. It lists only the files that the app needs, and doesn’t list the workbook or the `migration/` folder. |
| `pyproject.toml`, `.streamlit/config.toml` | In Snowsight only, copied unchanged from the workspace’s default Streamlit app template. |
| `migration/` | Records that CoCo keeps for the migration, such as the real-data mapping in `real-data.json`. These files aren’t deployed. |

Expand

Show lessSee more

During the synthetic preview, the app also contains the synthetic data layer: the code and files
that supply synthetic rows to each page. The real-data cutover replaces this layer with code that
queries Snowflake.

### Disposition summary

When CoCo finishes a build, it returns a report in the chat and saves the same information in
`workbook_map.json`. The report includes a disposition summary, which lists every dashboard,
worksheet, and action in the workbook with its status and the reason for any gap. The following
table describes each status:

| Status | Meaning |
| --- | --- |
| `implemented` | Built from the workbook’s definitions. |
| `partial` | Built, but some behavior differs from the workbook or couldn’t be confirmed. The reason explains what’s missing. |
| `blocked` | Not built, because information is missing or the behavior isn’t supported. The reason explains what’s needed. |
| `out_of_scope` | Excluded by the scope that you approved. |

Expand

Show lessSee more

Review the disposition summary before you test the synthetic preview:

- `partial`: Read the reason. If the difference matters, describe the behavior that you want,
  and CoCo revises the app.
- `blocked`: Supply what the reason asks for, such as how an action activates and clears, a
  translation for an analytics extension calculation, or a set’s list of members. CoCo doesn’t
  cut over to real data while a calculation that the app needs is blocked.
- `out_of_scope`: To include the element, ask CoCo to widen the scope. CoCo shows a new file plan
  for your approval.

## Supported Tableau features and limitations

The following sections describe how CoCo handles each part of a Tableau workbook and the
limitations that apply.

### Charts and layout

- CoCo maps each worksheet to the closest native Streamlit chart, `st.dataframe`, or
  `st.metric`. It uses an Altair chart only when a worksheet needs something native charts
  can’t express, such as a selection that drives an action, highlight dimming, or a dual axis,
  and records the reason in `workbook_map.json`.
- Point maps with latitude and longitude map to `st.map` and are marked `partial`.
- Filled maps, treemaps, sunbursts, Sankey diagrams, and radial gauges need a charting library
  beyond native Streamlit charts and Altair, such as Plotly. In CoCo CLI and CoCo Desktop, CoCo
  asks you to approve any package dependency and external access integration that these charts
  require. In Snowsight, a package beyond the workspace defaults needs an external
  access integration that you add in the app settings. For more information, see
  [External network access in Streamlit in Snowflake](/developer-guide/streamlit/features/external-access).
- When no chart mapping fits, CoCo shows the worksheet’s data as a table and marks the worksheet
  `partial`.
- Each dashboard in scope becomes an app page. Horizontal layout proportions become column
  widths, and sheet-selector tabs become tabs on the page. Absolute positions and floating
  objects don’t carry over: CoCo moves them into the page flow and tells you what changed.
  Heights are approximate.
- CoCo uses the workbook’s colors, member aliases, and number formats.

### Filters, parameters, and actions

- Each approved dashboard filter and parameter becomes its own labeled widget. Supported controls
  include single-value and multiple-value filters, date and numeric ranges, parameters with a
  fixed set of values, and Top N filters.
- CoCo preserves Tableau’s filter order in SQL. For example, a context filter applies before a
  `FIXED` level of detail expression, and an ordinary dimension filter doesn’t.
- Filter and highlight actions map to chart selections. If the workbook doesn’t define how an
  action activates or clears, CoCo marks the action `blocked` until you supply that behavior.
  A highlight that spans several separate charts might be `partial`.
- CoCo reports other action types, such as URL, go-to-sheet, set, and parameter actions,
  individually in the disposition summary.

### Calculations

- CoCo translates the following into Snowflake SQL:
  - Row-level and aggregate calculations.
  - Level of detail expressions (`FIXED`, `INCLUDE`, and `EXCLUDE`).
  - Table calculations, such as running totals, window functions, `LOOKUP`, and `RANK`.
  - Sets, groups, and bins.
- CoCo translates only the calculations that the approved scope needs.
- CoCo blocks the following until you supply a translation or decision:
  - Analytics extension functions (`SCRIPT_*`), predictive modeling functions (`MODEL_*`), and
    the calculations that depend on them.
  - `PREVIOUS_VALUE`.
  - `WINDOW_MEDIAN` and `WINDOW_PERCENTILE` with a bounded window.
  - Table calculations whose padding or addressing isn’t defined in the workbook.
  - Sets without a saved list of members.
  - Functions without a Snowflake equivalent.

### Data sources

- CoCo doesn’t read extract rows or load extracts into Snowflake. For the real-data cutover, the
  data must already be in Snowflake, in the same account as the app.
- CoCo flags data sources that don’t connect to Snowflake, data blending, and initial SQL that
  could change session settings.
- The inventory contains only a shortened preview of custom SQL. CoCo asks for the complete
  statement before it uses or translates the custom SQL.
- For queries that Tableau generates dynamically, no literal original query exists. CoCo builds
  equivalent SQL from the data source model, shelves, calculations, filters, and grain.

### Security

- CoCo treats user filters, connections that pass the viewer’s identity, and user functions
  such as `USERNAME()` and `ISMEMBEROF()` as security requirements. It doesn’t reimplement
  them as filters in the app. Enforce these requirements in Snowflake, for example with a row
  access policy or secure view, and have the app read through a restricted caller’s rights
  connection, so Snowflake applies each viewer’s grants and policies. For more information, see
  [Understanding row access policies](/user-guide/security-row-intro).
- In an owner’s rights app, context functions such as `CURRENT_USER()` return the owner’s
  context, so a row access policy can’t tell viewers apart. If the app would show
  viewer-specific data with owner’s rights, CoCo stops the cutover. For more information, see
  [Row access policies in Streamlit in Snowflake](/developer-guide/streamlit/features/row-access).
- CoCo doesn’t cache query results in the real-data app, so viewers don’t share results. Each
  page load and widget change runs the page’s queries on the query warehouse. If you add caching
  later to an app that uses restricted caller’s rights, set `scope="session"` so that results
  aren’t shared between viewers.
- Tableau filter actions are presentation features, not security. CoCo doesn’t treat them as
  row-level security.
- CoCo doesn’t grant `SELECT` on source tables, create policies, or widen access to make a query
  work. In CoCo CLI and CoCo Desktop, it grants `USAGE` on the app only to the audience roles you
  list. In Snowsight, it doesn’t grant any roles.

## Troubleshoot a migration

The following table describes common problems and how to resolve them:

| Problem | What to do |
| --- | --- |
| The skill doesn’t appear when you type `/tableau`. | Update to CoCo CLI 1.2.33 or later, for example with `cortex update`, or to CoCo Desktop 1.23.1 or later, and start a new session. |
| CoCo refuses a `.twbx` file larger than 512 MiB. | Save the workbook as a `.twb` file in Tableau, or extract the `.twb` file from the `.twbx` package, which is a zip archive. Give CoCo that file instead. To inspect the package anyway, tell CoCo that you agree to inspect this one larger package, up to 4 GiB. |
| A deployment fails. | Read the error that CoCo reports, and check the privileges in [Prerequisites](#label-streamlit-tableau-prerequisites). CoCo doesn’t roll back a failed deployment, and it reports anything that it might have changed. After you fix the cause, ask CoCo to deploy again to the same target. |
| CoCo stops because the app has a `USAGE` grantee that you didn’t list. | Someone shared the app outside CoCo. CoCo doesn’t revoke the grant. Revoke it, or ask CoCo to add the role to the audience roles and approve the updated target. |
| The real-data deployment fails. | The app might already serve the real-data version. CoCo reports the last state that it observed and doesn’t roll back. Open the app, then tell CoCo whether to retry the cutover or redeploy the synthetic preview. |
| A page shows a query error after the cutover. | With owner’s rights, check that the app owner role has `SELECT` on the source tables and `USAGE` on the query warehouse. With restricted caller’s rights, check the caller grants and each viewer’s default role. For more information, see [Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights). |
| You closed CoCo CLI before the migration finished. | In the same folder, run `cortex --continue`, or run `/resume` in a session. |

Expand

Show lessSee more

## Give feedback

To share feedback on this preview, contact your Snowflake account team. In CoCo CLI, you can
also run `/feedback` to save the session feedback as a file that you can send to your account
team. In CoCo in Snowsight, you can rate each response with a thumbs-up or
thumbs-down.
