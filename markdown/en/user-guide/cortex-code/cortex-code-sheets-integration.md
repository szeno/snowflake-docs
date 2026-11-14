# Snowflake CoCo for Google Sheets

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

## Overview

Snowflake CoCo for Google Sheets™ brings CoCo directly into Google Sheets. It adds CoCo as a chat pane inside the
spreadsheet you already use, connected to your live Snowflake data. From the pane you can query data, build pivot
tables and charts, write formulas, and format your sheets using natural language, and then refresh that data later,
without exporting data out of Snowflake and without learning a separate tool. It also extends Snowflake governance into Google
Sheets: queries run under your own role, so access control, masking, and row access policies continue to apply to the
data that reaches your spreadsheet.

The add-on is part of Snowflake CoCo. For an overview of the other CoCo experiences, see
[CoCo](/user-guide/cortex-code/cortex-code).

## Requirements

- Google Sheets in a web browser on a computer. The add-on doesn’t run in the Google Sheets apps for Android or iOS.
- A Snowflake account with Snowflake Cortex and [CoCo](/user-guide/cortex-code/cortex-code) enabled.
  [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) is required only when the model you
  select isn’t available in your region.

## Key capabilities

- **Query with natural language or SQL:** Describe the data you want in plain language and CoCo generates and runs
  the query, loading live results into your sheet. Power users can provide SQL and CoCo runs it as written.
- **Explore your data without SQL:** Browse the databases, schemas, tables, and
  [semantic views](/user-guide/views-semantic/overview) your role can access, or describe what you are looking for,
  and CoCo finds the matching objects and pulls the data into your sheet. Enter `/catalog` in the pane to browse the
  catalog and pick columns.
- **Build pivots, charts, and formulas:** Ask CoCo to pivot a result set, add or change a chart, or construct a
  formula, and CoCo creates the corresponding Google Sheets objects so you can keep working in familiar spreadsheet
  tools.
- **Format and organize your sheets:** Ask CoCo to format cells, add conditional formatting or data validation rules,
  sort a range, find and replace text, fill a series, create named ranges, insert or delete rows and columns, and add
  or manage sheets.
- **Use governed objects and semantic views:** Query the tables, views, and semantic views you are permissioned for.
  Metric definitions come from Snowflake semantic views rather than being recreated per spreadsheet, so results stay
  consistent across users and reports.
- **Intelligently refresh data:** Re-run the queries to get the latest data on demand, and review the new results
  before they’re applied. See [Intelligent refresh](#label-cortex-code-sheets-refresh).
- **Run CoCo skills:** Use skills such as report generation, analysis, and summaries from inside the spreadsheet.
  Enter `/` in the pane to see and select the available skills.
- **Preview before every change:** See a clear before-and-after of every write and accept or reject it before it is
  applied. See [Review changes and track sources](#label-cortex-code-sheets-review).
- **Trace every written cell:** Follow the citation attached to each value back to the query or metric that produced
  it, so any number in the spreadsheet can be verified.

Some features of Snowflake CoCo for Microsoft Excel aren’t available in Google Sheets. See
[Limitations](#label-cortex-code-sheets-limitations).

## How it works

Snowflake CoCo for Google Sheets runs as an Apps Script project in your spreadsheet and opens a CoCo pane in a sidebar
next to your sheet. When you make a request, CoCo interprets it, runs the corresponding query or action against your
Snowflake account using your privileges, and writes the results into the sheet. Data is read from Snowflake at query
time, so the results reflect your live data when CoCo writes them. CoCo saves the query behind each result it loads,
so you can bring the data up to date later without asking for it again. See
[Intelligent refresh](#label-cortex-code-sheets-refresh).

The CoCo pane connects to Snowflake directly from your browser. The add-on’s Apps Script code, which runs on Google’s
servers, is the only part that reads and writes the spreadsheet. It never receives your Snowflake sign-in tokens, and
it has no permission to make network requests. The script asks Google for permission to see, edit, create, and delete
all your Google Sheets spreadsheets, plus permission to show its menu and sidebar. It needs the broader spreadsheet permission because
it creates and resizes tables through the Google Sheets API, which access to only the current spreadsheet doesn’t
allow. The script reads and writes only the spreadsheet that it’s copied into.

Before CoCo writes anything to your spreadsheet, it shows a preview of the change and records a citation to the source
of each written value. For more information about these behaviors, see
[Review changes and track sources](#label-cortex-code-sheets-review).

The add-on brings the same capabilities as other CoCo experiences into Google Sheets. For background on how CoCo works,
see [CoCo](/user-guide/cortex-code/cortex-code).

## Install the add-on

During the current stage of the preview, Snowflake CoCo for Google Sheets is distributed as an Apps Script file,
`Code.gs`, that you copy into a spreadsheet’s Apps Script project. You copy it once into each spreadsheet where you use
the add-on. Snowflake plans to make the add-on available on the Google Workspace Marketplace in a later stage of the
preview.

A Google Workspace administrator can instead install the add-on for everyone in your organization, so users don’t copy
the script themselves. See [Install the add-on for your organization](#label-cortex-code-sheets-admin-install).

Copying the script only makes the add-on available in the spreadsheet. Before you can sign in from the pane, an account
administrator creates a security integration for your Snowflake account and gives you the OAuth client ID. See
[Create a security integration for OAuth](#label-cortex-code-sheets-oauth).

To add the add-on to a spreadsheet, follow these steps:

1. Open the spreadsheet in Google Sheets.
2. Select **Extensions** > **Apps Script**. The Apps Script editor opens in a new browser tab.
3. Rename the project to `CoCo for Sheets`. Google Sheets shows the project name as the add-on’s submenu under
   **Extensions**.
4. Replace the contents of `Code.gs` with the file at `https://ai.snowflake.com/static/sheets/releases/prod/Code.gs`.
5. In **Project Settings**, turn on the setting that shows the manifest file, `appsscript.json`, in the editor. Then
   replace the contents of `appsscript.json` with the file at
   `https://ai.snowflake.com/static/sheets/releases/prod/appsscript.json`.
6. Save the project, then reload the spreadsheet.
7. Select **Extensions** > **CoCo for Sheets** > **Open Coco**. The first time you open the pane, Google asks you to
   authorize the script. After you authorize it, the **Snowflake CoCo** pane opens on the right side of the
   spreadsheet.

[![The Google Sheets Extensions menu with CoCo for Sheets selected, showing the Open Coco item in its submenu.](/static/images/screens/cortex-code-sheets-open-coco-menu.png)](/static/images/screens/cortex-code-sheets-open-coco-menu.png)

## Install the add-on for your organization

A Google Workspace administrator can install Snowflake CoCo for Google Sheets for everyone in the organization, or for
specific organizational units and groups, from the Google Admin console. The users you install it for get the add-on in
every spreadsheet, and they don’t need to copy the script.

During the current stage of the preview, Snowflake CoCo for Google Sheets isn’t listed on the Google Workspace
Marketplace, so you publish the add-on as a private app in your own Google Workspace organization, and then install it
from the Google Admin console. Google doesn’t review private apps, so you can install the app as soon as you publish it.
Only users in your organization can see it.

Before you begin, confirm the following:

- You’re signed in as a Google Workspace super administrator. See
  [Install Marketplace apps for your organization](https://support.google.com/a/answer/172482).
- You can create a Google Cloud project that belongs to your organization, and enable APIs in it. The OAuth consent
  screen offers the **Internal** user type only for a project that belongs to your organization.
- If you’re installing the add-on for only some users, their accounts are in an organizational unit or an access group.

### Publish the add-on privately

To publish the add-on as a private app, follow these steps:

1. Go to [Apps Script](https://script.google.com) and select **New project**. Don’t create the project from a
   spreadsheet: an add-on that you publish must be a standalone Apps Script project.
2. Replace the contents of `Code.gs` with the file at `https://ai.snowflake.com/static/sheets/releases/prod/Code.gs`.
3. In **Project Settings**, turn on the setting that shows the manifest file, `appsscript.json`, in the editor. Then
   replace the contents of `appsscript.json` with the file at
   `https://ai.snowflake.com/static/sheets/releases/prod/appsscript.json`. Save the project.
4. In the [Google Cloud console](https://console.cloud.google.com), create a Google Cloud project in your organization,
   and note its project number. You can’t publish from the default project that Apps Script creates. In the new
   project, do the following:

   - Configure the OAuth consent screen, and set its user type to **Internal**, so only users in your organization can
     authorize the add-on.
   - Enable the **Google Sheets API**. The add-on uses the Google Sheets advanced service, and a standard Google Cloud
     project doesn’t turn on that API for you.
   - Enable the **Google Workspace Marketplace SDK**.
5. In the Apps Script project, select **Project Settings**. Under **Google Cloud Project**, select **Change project**,
   enter the project number of the new project, and select **Set project**. Under **IDs**, copy the **Script ID**.
6. Select **Deploy** > **New deployment**, select **Add-on** as the type, and then select **Deploy**. Note the version
   number of the deployment.
7. In the Google Cloud console, open the **Google Workspace Marketplace SDK**. On the **App Configuration** page, set
   the following, and then save:

   - **App visibility:** **Private**.
   - **Installation settings:** **Admin Only Install**.
   - **App integrations:** the Editor add-on integration for Google Sheets, with the script ID from step 5 and the
     version number from step 6.
   - **OAuth scopes:** the two scopes listed in `appsscript.json`:
     `https://www.googleapis.com/auth/spreadsheets` and `https://www.googleapis.com/auth/script.container.ui`.
8. On the **Store Listing** page, fill in the required fields. Enter `CoCo for Sheets` as the app name: Google Sheets
   shows the app name as the add-on’s submenu under **Extensions**, so this name matches the menu paths in this topic.
   Then select **Publish**.

### Install the add-on from the Google Admin console

After you publish the add-on, follow these steps to install it for your organization:

1. In the Google Admin console, go to **Menu** > **Apps** > **Google Workspace Marketplace apps** > **Apps list**.
2. Select **Install app**. Find the add-on in the **Internal apps** section of the Google Workspace Marketplace, and
   select it.
3. Select **Admin install**, then select **Continue**. Review the data access requirements, developer terms, and
   developer policies.
4. Choose who gets the add-on:

   - To install it for everyone, select **Everyone at your organization**.
   - To install it for specific users, select **Certain groups or organizational units**, then select **Next**. Select
     the organizational units and groups, then select **Select**.
5. Select **Finish**.

Note the following about this method:

- Google notes that changes can take up to 24 hours to apply, though they typically apply sooner. After the add-on
  appears, users open the pane as described in [Get started](#label-cortex-code-sheets-start).
- Installing the add-on doesn’t connect it to your Snowflake account. An account administrator still creates an OAuth
  security integration and shares the client ID with users. See
  [Create a security integration for OAuth](#label-cortex-code-sheets-oauth).
- Your organization owns the private app, so Snowflake doesn’t update it for you. To pick up a new release, replace
  `Code.gs` and `appsscript.json` with the latest files, create a new deployment version, enter the new version number
  on the **App Configuration** page of the Google Workspace Marketplace SDK, and save.
- To change who has the add-on, or to uninstall it, see
  [Install Marketplace apps for your organization](https://support.google.com/a/answer/172482).

## Get started

1. **Add Snowflake CoCo for Google Sheets to your spreadsheet.** See
   [Install the add-on](#label-cortex-code-sheets-install). If your Google Workspace administrator installed the add-on
   for your organization, skip this step.
2. **Open the pane.** In your spreadsheet, select **Extensions** > **CoCo for Sheets** > **Open Coco**.
3. **Sign in.** In the pane, enter your Snowflake [account identifier](/user-guide/admin-account-identifier) and the
   OAuth client ID for your account, then select **Sign in with Snowflake**. Your account administrator provides the
   client ID. See [Sign in from the pane](#label-cortex-code-sheets-sign-in).
4. **Choose a role (optional).** Your session uses the role you entered when you signed in, or your default role. To
   use a different role, in the pane header select **More** (…) > **Settings**, then select it under **Role**.
   Changing the role signs you in again as that role.
5. **Start asking.** Describe what you want in the pane, and CoCo returns the result in your sheet. Refine, pivot,
   chart, or format the results from the same conversation.

The pane closes when you reload the spreadsheet. To open it again, select **Extensions** > **CoCo for Sheets** >
**Open Coco**.

### Example prompts

The following table lists example prompts for common tasks. For accurate results, include the context CoCo needs,
such as the database, schema, and objects you want to work with:

| Task | Example prompt |
| --- | --- |
| Load data | “Show last quarter’s revenue by region.” |
| Explore without SQL | “Find tables related to customer churn and pull in the churn rate by month.” |
| Pivot | “Pivot these results by product line and quarter.” |
| Chart | “Add a bar chart of total sales by month.” |
| Formula | “Add a column that calculates margin as profit divided by revenue.” |
| Format | “Highlight the rows where margin is below 10%.” |
| Consistent metrics | “Using the revenue semantic view, show revenue by segment for last quarter.” |

Expand

Show lessSee more

### Sign in from the pane

1. In the pane, enter your account identifier in **Account identifier** and the client ID in **OAuth client ID**.
   Optionally, enter a role in **Role**. If you leave **Role** empty, your session uses your default role.
2. Select **Sign in with Snowflake**. A sign-in page opens in a new browser tab.
3. In the browser tab, sign in with your own Snowflake credentials. The page then shows a sign-in code.
4. Select **Copy code**. The code can be used only once, and it expires in about a minute.
5. Return to the pane, paste the code in **Paste your sign-in code** or select **Paste**, and then select
   **Finish sign-in**.

## Review changes and track sources

CoCo previews every change before it is written to your spreadsheet. When CoCo proposes a write, it shows a
before-and-after of the affected cells so you can accept or reject the change. Nothing changes in the spreadsheet
until you select **Accept**.

[![A CoCo preview in the Google Sheets pane that stages a margin formula and a percent format for column E, with Reject and Accept buttons.](/static/images/screens/cortex-code-sheets-preview.png)](/static/images/screens/cortex-code-sheets-preview.png)

How many undo steps it takes to reverse an accepted change depends on the change:

- A change to cell values can be reversed with a single undo.
- A change that combines structural edits, such as cell formatting, frozen rows, and conditional formatting, can take
  several undo steps.
- A large query result is written in batches, so reversing it can take several undo steps.

Every value CoCo writes back carries a citation to the query or metric that produced it. Citations let you trace any
number in the spreadsheet back to its source in Snowflake, so results can be verified rather than taken on trust. CoCo
stores citations in a hidden sheet named `_CORTEX_CITATIONS` in the same spreadsheet.

## Intelligent refresh

CoCo can re-run the Snowflake queries behind the data it loaded, so you can bring a spreadsheet up to date without
asking for the data again. Snowflake CoCo for Google Sheets refreshes data only when you start a refresh. It doesn’t
refresh data when the spreadsheet opens.

### Refresh data from the pane

When CoCo loads the results of a Snowflake query into your sheet, it writes the results as plain cells, creates a named
range over them whose name starts with `CocoTable_`, and saves the query with the spreadsheet. CoCo finds the data
later by its named range, not by a cell address, so moving the data, inserting rows above it, or renaming the sheet
doesn’t break refresh. If you ask CoCo to turn the data into a Google Sheets table, or you convert it to a table
yourself, the table keeps the saved query.

To start a refresh, use any of the following. All three run the same refresh:

- In the pane header, select **Refresh data**.
- On an empty chat, select **Refresh sheet data**.
- In the pane, enter `/refresh`. The `/` menu describes the command as “Re-run the Snowflake queries behind data on
  this sheet.”

[![The CoCo pane header in Google Sheets, with the Refresh data button highlighted between the All chats and More buttons.](/static/images/screens/cortex-code-sheets-refresh-data.png)](/static/images/screens/cortex-code-sheets-refresh-data.png)

By default, a refresh covers the data on the active sheet that CoCo loaded from a query. To refresh specific results,
select cells that overlap them before you start the refresh. CoCo refreshes each result that the selection touches,
always in full. Selecting a single cell doesn’t narrow the refresh. If the selected cells don’t touch data that CoCo
loaded from a query, nothing is refreshed.

CoCo re-runs each saved query directly, without a request to the model, under your current role and warehouse. It
then shows the new results as a preview that you accept or reject. When a refresh covers more than one result, you
choose which results to apply. Only read-only queries run: if a saved query isn’t read-only, CoCo skips that result
and tells you. You can’t start a refresh while another preview is waiting for you to accept or reject it.

Refresh has the following limits:

- If the new results have more or fewer rows or columns than the data they replace, CoCo inserts or deletes cells only
  below or beside the data, and any table or named range in those cells moves with them. If the shift would split a
  table or named range, CoCo doesn’t refresh that data, and it names the table or named range that’s in the way. Move
  the data, or move the table or named range that’s in the way, and then run the refresh again.
- A refresh counts toward the Google Sheets cell limit like any other write. If the refreshed data doesn’t fit in the
  spreadsheet, CoCo doesn’t write it. See [Limitations](#label-cortex-code-sheets-limitations).
- If a refresh stops partway, for example because you stop it or the connection to Snowflake is lost, the data can
  hold a mix of old and new rows. CoCo reports how many rows it wrote and doesn’t retry. Run the refresh again to
  finish it.

## Authentication and access control

You sign in to Snowflake from the pane using OAuth. CoCo authenticates with your own Snowflake identity and operates
under Snowflake [role-based access control (RBAC)](/user-guide/security-access-control-overview). It doesn’t store or
modify your credentials, and it performs only the actions your active role permits. Snowflake CoCo for Google Sheets
supports OAuth sign-in only. It doesn’t support programmatic access tokens. For the steps to sign in, see
[Sign in from the pane](#label-cortex-code-sheets-sign-in).

Your sign-in tokens stay in the CoCo pane in your browser. Requests to Snowflake also come from your browser, so your
account’s [network policies](/user-guide/network-policies) evaluate your own IP address.

### Create a security integration for OAuth

Before anyone can sign in from the pane with OAuth, an account administrator creates a Snowflake OAuth security
integration for a custom client. You create the integration once per Snowflake account, not once per user. Only users
with the `ACCOUNTADMIN` role, or a role with the global `CREATE INTEGRATION` privilege, can run this command.

Snowflake CoCo for Google Sheets and Snowflake CoCo for Microsoft Excel use the same OAuth redirect URI. If your account
already has a security integration for Snowflake CoCo for Microsoft Excel, Snowflake CoCo for Google Sheets can use the
same integration and the same client ID, and you don’t need to create another one.

Register the add-on as a public client. The pane runs in your browser, so it can’t store a client secret, and the
add-on uses Proof Key for Code Exchange (PKCE) instead. The following example creates an integration for Snowflake
CoCo for Google Sheets:

Copy code

```
CREATE SECURITY INTEGRATION IF NOT EXISTS coco_sheets_oauth
  TYPE = OAUTH
  OAUTH_CLIENT = CUSTOM
  OAUTH_CLIENT_TYPE = 'PUBLIC'
  OAUTH_REDIRECT_URI = 'https://ai.snowflake.com/static/excel/oauth/callback.html'
  OAUTH_ENFORCE_PKCE = TRUE
  OAUTH_ISSUE_REFRESH_TOKENS = TRUE
  OAUTH_REFRESH_TOKEN_VALIDITY = 86400
  ENABLED = TRUE
  COMMENT = 'Snowflake CoCo for Google Sheets add-on';
```

Important

Set `OAUTH_REDIRECT_URI` to exactly `https://ai.snowflake.com/static/excel/oauth/callback.html`. Snowflake compares this
value to the one the add-on sends, so any difference, such as a trailing slash or a different host, makes sign-in fail.
The URL contains `excel` because Snowflake CoCo for Google Sheets and Snowflake CoCo for Microsoft Excel share the same
OAuth callback page.

`OAUTH_ENFORCE_PKCE = TRUE` requires PKCE on every authorization. PKCE is optional by default, and Snowflake
recommends requiring it to make the OAuth flow more secure. The refresh token settings keep users signed in across
sessions: `OAUTH_REFRESH_TOKEN_VALIDITY` is in seconds, so `86400` is one day.

The example uses `CREATE SECURITY INTEGRATION IF NOT EXISTS` rather than `CREATE OR REPLACE`. Replacing an existing
integration generates a new client ID and invalidates its refresh tokens, which signs out every user of the add-on. To
change the settings of an existing integration, use
[ALTER SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/alter-security-integration-oauth-snowflake).

To get the client ID that the add-on uses, call
[SYSTEM$SHOW\_OAUTH\_CLIENT\_SECRETS](/sql-reference/functions/system_show_oauth_client_secrets). The integration name is
case-sensitive and must be uppercase:

Copy code

```
SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS('COCO_SHEETS_OAUTH');
```

Snowflake generates the client ID when you create the integration, so the value is unique to your account. Share the
client ID with the people who use the add-on. After they add the add-on to a spreadsheet and open the pane, they enter
the client ID and your account identifier, then sign in with their own Snowflake credentials. See
[Sign in from the pane](#label-cortex-code-sheets-sign-in).

By default, Snowflake blocks the `ACCOUNTADMIN`, `ORGADMIN`, `GLOBALORGADMIN`, and `SECURITYADMIN` roles from
authenticating through OAuth, so users sign in with a non-privileged role. To limit the integration to specific roles,
add `ALLOWED_ROLES_LIST`. For the full set of parameters, see
[CREATE SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/create-security-integration-oauth-snowflake). For
more information about custom clients, see
[Snowflake OAuth for custom clients](/user-guide/oauth-custom).

### Access control requirements

Because queries run under your role, CoCo can read only the databases, schemas, tables, views, and semantic views
that your active role is authorized to access, and masking and row access policies apply automatically. Query results
are written into your spreadsheet, but the underlying data remains governed by Snowflake.

## Limitations

The following limits come from Google Sheets:

- The CoCo sidebar is a fixed 300 pixels wide, and you can’t resize it.
- The pane can’t open by itself. You open it from the **Extensions** menu each time, and you open it again after
  every reload of the spreadsheet.
- The add-on doesn’t run in the Google Sheets apps for Android or iOS.
- Google Sheets limits the total number of cells in a spreadsheet, and empty columns count toward that limit. CoCo
  checks a query result against the limit before it writes. If the result fits only without the destination sheet’s
  trailing empty columns, CoCo tells you in the preview that it will delete those columns when you accept. If the result
  doesn’t fit, CoCo refuses the import. CoCo applies the same check to a [refresh](#label-cortex-code-sheets-refresh).
  If the refreshed data fits only without the sheet’s trailing empty columns, CoCo deletes those columns when you
  accept the refresh. If the refreshed data doesn’t fit, CoCo doesn’t write it.

The following Snowflake CoCo for Microsoft Excel features aren’t available in Google Sheets:

- `CORTEX` functions in cells, such as `=CORTEX.ASK()`.
- [Refresh when the workbook opens](/user-guide/cortex-code/cortex-code-excel-integration#label-cortex-code-excel-refresh-on-open).
  In Google Sheets, CoCo refreshes data only when you start a refresh. See
  [Intelligent refresh](#label-cortex-code-sheets-refresh).

## Feedback

To report a bug or send feedback to Snowflake, enter `/feedback` in the pane.

## Cost

Snowflake CoCo for Google Sheets is billed based on token consumption, consistent with other CoCo experiences, and
doesn’t require a separate per-seat license. Pricing details are provided in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

Any Snowflake compute or storage consumed separately from CoCo usage is billed at standard Snowflake on-demand rates,
as described in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf). Examples
include virtual warehouse compute used to run your queries and storage costs.

[Refreshing data](#label-cortex-code-sheets-refresh) from the pane doesn’t consume CoCo tokens. The spreadsheet stores
the SQL behind each result that CoCo loaded, and a refresh runs that saved SQL directly, without a request to the
model. This applies to **Refresh data**, **Refresh sheet data**, and `/refresh`. Each refresh still uses virtual
warehouse compute to run the queries. If you ask CoCo in a chat message to refresh data, that request consumes CoCo
tokens like any other CoCo request.

To set daily credit usage limits for CoCo users, see
[Managing CoCo credit usage limits](/user-guide/cortex-code/credit-usage-limit).

## Legal notices

Where your configuration of Cortex Code uses a model provided on the
[Model and Service Pass-Through Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/model-pass-through-terms/),
your use of that model is further subject to the terms for that model on that page.

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Covered AI Features [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).

Snowflake’s use of raw or derived user data received from the Sheets API will adhere to the
[Google User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), including the Limited Use
requirements.

*Google Sheets is a trademark of Google LLC.*
