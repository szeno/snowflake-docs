# Snowflake CoCo for Microsoft Excel

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

## Overview

Snowflake CoCo for Microsoft Excel brings CoCo directly into Microsoft Excel. It adds CoCo as a chat pane inside the
workbook you already use, connected to your live Snowflake data. From the pane you can query data, build PivotTables and
charts, and write formulas using natural language, without exporting data out of Snowflake and without learning a
separate tool. In cells, `CORTEX` functions call Snowflake Cortex directly. The add-in also extends Snowflake governance
into Microsoft Excel: queries run under your own role, so access control, masking, and row access policies continue to
apply to the data that reaches your workbook.

The add-in is part of Snowflake CoCo. For an overview of the other CoCo experiences, see
[CoCo](/user-guide/cortex-code/cortex-code).

## Requirements

- Microsoft Excel for Microsoft 365 on Windows, Mac, or the web.
- A Snowflake account with Snowflake Cortex and [CoCo](/user-guide/cortex-code/cortex-code) enabled.
  [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) is required only when the model you
  select isn’t available in your region.

## Key capabilities

- **Query with natural language or SQL:** Describe the data you want in plain language and CoCo generates and runs
  the query, loading live results into your worksheet. Power users can provide SQL and CoCo runs it as written.
- **Explore your data without SQL:** Browse the databases, schemas, tables, and
  [semantic views](/user-guide/views-semantic/overview) your role can access, or describe what you are looking for,
  and CoCo finds the matching objects and pulls the data into your worksheet. Enter `/catalog` in the pane to browse the
  catalog and pick columns. See [Browse the catalog](#label-cortex-code-excel-catalog).
- **Build pivots, charts, and formulas:** Ask CoCo to pivot a result set, add a chart, or construct a formula, and
  CoCo creates the corresponding Microsoft Excel objects so you can keep working in familiar spreadsheet tools. To pivot
  a Snowflake table, view, or semantic view without loading its rows into the workbook, use a
  [live pivot](#label-cortex-code-excel-live-pivot): Snowflake computes the pivot, and CoCo draws the result in the sheet.
- **Use governed objects and semantic views:** Query the tables, views, and semantic views you are permissioned for.
  Metric definitions come from Snowflake semantic views rather than being recreated per workbook, so results stay
  consistent across users and reports.
- **Intelligently refresh data:** Re-run the queries to get the latest data, either on demand or each time the workbook
  opens, and review the new results before they’re applied. See
  [Intelligent refresh](#label-cortex-code-excel-refresh).
- **Call CORTEX functions in cells:** Use the seven functions in the `CORTEX` namespace, such as `=CORTEX.ASK()`,
  `=CORTEX.SUMMARIZE()`, and `=CORTEX.SENTIMENT()`, as Microsoft Excel formulas to enrich your data alongside your other
  formulas. See [Use CORTEX functions in cells](#label-cortex-code-excel-functions).
- **Run commands and CoCo skills:** Use skills such as report generation, analysis, and summaries from inside the
  workbook. Enter `/` in the pane to see the built-in commands `/catalog`, `/feedback`, `/pivot`, and `/refresh`,
  followed by the available skills. See [Commands and skills in the `/` menu](#label-cortex-code-excel-slash-menu).
- **Use MCP connectors:** Let CoCo use the tools of the external MCP servers you’ve connected, and choose which ones it
  uses. See [Use MCP connectors](#label-cortex-code-excel-mcp).
- **Attach files:** Add images, PDFs, SQL scripts, spreadsheets, and other files to a message for CoCo to read. See
  [Attach files](#label-cortex-code-excel-attachments).
- **Preview before every change:** See a clear before-and-after of every write and accept or reject it before it is
  applied. See [Review changes and track sources](#label-cortex-code-excel-review).
- **Trace every written cell:** Follow the citation attached to each value back to the query or metric that produced
  it, so any number in the workbook can be verified.

## How it works

Snowflake CoCo for Microsoft Excel installs as a Microsoft Excel add-in that opens a CoCo pane next to your worksheet.
When you make a request, CoCo interprets it, runs the corresponding query or action against your Snowflake account using
your privileges, and writes the results into the sheet. Data is read from Snowflake at query time, so the workbook
reflects live data rather than a static export.

A single import or refresh writes up to 1,048,575 data rows, which is the most a Microsoft Excel sheet holds below a
header row. If a query returns more rows, CoCo writes the first 1,048,575 rows and says so on the preview: “The query
has N rows. Only the first M are imported.” The full limit fits only when the data starts in row 1. Lower on the
sheet, a refresh or a [`/catalog` pull](#label-cortex-code-excel-catalog) writes only the rows that fit, and an import
that CoCo proposes in chat is refused before CoCo writes anything. Rows arrive in batches after you accept, so undoing a
large import can take several undo steps.

Before CoCo writes anything to your workbook, it shows a preview of the change and annotates each written value with
a citation to its source. For more information about these behaviors, see
[Review changes and track sources](#label-cortex-code-excel-review).

The add-in brings the same capabilities as other CoCo experiences into Microsoft Excel. For background on how CoCo
works, see [CoCo](/user-guide/cortex-code/cortex-code).

## Install the add-in

During the current stage of the preview, Snowflake CoCo for Microsoft Excel is distributed as an add-in manifest that
you sideload into Microsoft Excel. You sideload the manifest once for your own user account on each machine where you
use the add-in. The add-in is available for Microsoft Excel on Mac and Windows, and the steps differ by platform.

A Microsoft 365 administrator can instead install the add-in for everyone in your organization, so users don’t sideload
the manifest themselves. See [Install the add-in for your organization](#label-cortex-code-excel-admin-install).

Sideloading the manifest only makes the add-in available in Microsoft Excel. Before you can sign in from the pane, an
account administrator creates an OAuth security integration and gives you the resulting client ID. See
[Create a security integration for OAuth](#label-cortex-code-excel-oauth).

### macOS

1. Quit Microsoft Excel.
2. Create the Microsoft Excel add-in folder, if it doesn’t already exist:

   Copy code

   ```
   mkdir -p "$HOME/Library/Containers/com.microsoft.Excel/Data/Documents/wef"
   ```
3. Download the manifest into that folder:

   Copy code

   ```
   curl -sS https://ai.snowflake.com/static/excel/releases/prod/manifest.xml \
     -o "$HOME/Library/Containers/com.microsoft.Excel/Data/Documents/wef/snowflake-coco-excel.xml"
   ```
4. Open Microsoft Excel and create a new blank workbook.
5. On the **Home** tab, select **Add-ins**, then select **Snowflake CoCo**. If the add-in isn’t listed, restart
   Microsoft Excel.

### Windows

Important

Use only one of the sideload methods described in this section on a given machine. Both methods register the same
manifest, and the manifest carries a fixed add-in ID, so registering it twice makes **Snowflake CoCo** appear in two
places in the **Add-ins** dialog and leaves it ambiguous which copy of the manifest Microsoft Excel loads. That
ambiguity matters when the two copies differ, because the add-in can silently load an older manifest. If you already
tried one method, remove its registration before you use the other. See
[Remove the add-in from Windows](#label-cortex-code-excel-windows-remove).

Microsoft Excel on Windows can load a sideloaded add-in in two ways:

- [Use a trusted add-in catalog](#label-cortex-code-excel-windows-catalog): Point Microsoft Excel at a folder that holds
  the manifest. The folder has to be on a network file share.
- [Register the manifest with PowerShell](#label-cortex-code-excel-windows-registry): Add the manifest to a registry
  key for your Windows user account on one machine. This method needs no network share.

#### Use a trusted add-in catalog

Important

Microsoft Excel accepts only a network file share as an add-in catalog. A local folder path such as `C:\CoCoExcel`
doesn’t work with this method, and entering one is a common reason the add-in never appears in the **Add-ins** dialog.
If you don’t have a share you can use,
[register the manifest with PowerShell](#label-cortex-code-excel-windows-registry) instead.

1. Download the manifest from `https://ai.snowflake.com/static/excel/releases/prod/manifest.xml` and save it to a
   folder on a network file share. Don’t save it to a local folder.
2. In Microsoft Excel, select **File** > **Options** > **Trust Center** > **Trust Center Settings** >
   **Trusted Add-in Catalogs**.
3. Enter the full network path to the shared folder, such as `\\server\share\coco`. Select **Show in Menu**, then
   select **OK**.
4. Restart Microsoft Excel.
5. On the **Home** or **Insert** tab, select **Add-ins** > **My Add-ins** > **Shared Folder**, then select
   **Snowflake CoCo**.

#### Register the manifest with PowerShell

Microsoft Excel loads sideloaded add-ins listed under the `WEF\Developer` registry key for the current Windows user. The
following steps download the manifest to a per-user folder and add it to that key.

1. Quit Microsoft Excel. Confirm that no Microsoft Excel process is still running in the background, because
   Microsoft Excel reads the registry key only at startup.
2. In Windows PowerShell, run the following commands to download the manifest and register it:

   Copy code

   ```
   $manifestDir  = "$env:LOCALAPPDATA\Snowflake\CoCoExcel"
   $manifestPath = "$manifestDir\snowflake-coco-excel.xml"
   $developerKey = "HKCU:\Software\Microsoft\Office\16.0\WEF\Developer"

   New-Item -Path $manifestDir -ItemType Directory -Force | Out-Null
   Invoke-WebRequest -Uri "https://ai.snowflake.com/static/excel/releases/prod/manifest.xml" -OutFile $manifestPath

   if (-not (Test-Path $developerKey)) { New-Item -Path $developerKey -Force | Out-Null }
   Set-ItemProperty -Path $developerKey -Name "SnowflakeCoCoExcel" -Value $manifestPath
   ```
3. Confirm that the entry exists and points at the manifest:

   Copy code

   ```
   Get-ItemProperty -Path "HKCU:\Software\Microsoft\Office\16.0\WEF\Developer"
   ```
4. Open Microsoft Excel and create a new blank workbook.
5. On the **Home** tab, select **Add-ins**, then select **Snowflake CoCo** under **Developer Add-ins**.

Note the following about this method:

- `16.0` in the registry path is the Office major version, and it is the correct value for Office 2016 and all later
  builds, including Microsoft 365. Don’t replace it with a year.
- The entry applies to your Windows user account only, because it is written under `HKEY_CURRENT_USER`. Each person who
  uses the add-in on a shared machine runs the commands under their own account.
- The commands in step 2 run in Windows PowerShell 5.1 and in PowerShell 7, and they don’t require administrator rights.
  Snowflake recommends the `%LOCALAPPDATA%` folder used in the example for that reason: creating a folder at the root of
  the `C:` drive prompts for elevation in many configurations.
- The `Developer` key can hold an entry for each sideloaded add-in, so the example adds a single value rather than
  re-creating the key. Re-creating the key would unregister any other add-ins already listed there. The value name must
  be unique among sideloaded add-ins, because reusing a name replaces the earlier entry.
- Microsoft Excel reads the manifest from the registered path every time it starts, so keep the file at that path. If
  you move or delete the file, or if you save it to a folder that gets cleaned up, such as your Downloads folder, the
  add-in stops loading.
- A permissions error from `Set-ItemProperty` indicates that your organization might restrict registry changes.
  [Use a trusted add-in catalog](#label-cortex-code-excel-windows-catalog) instead, or ask your IT administrators to
  make the change.
- This method applies only to Microsoft Excel for Windows on the desktop. It has no effect on Microsoft Excel for Mac
  or Microsoft Excel on the web.

#### Remove the add-in from Windows

To remove a trusted add-in catalog, select **File** > **Options** > **Trust Center** > **Trust Center Settings** >
**Trusted Add-in Catalogs**, select the catalog, then select **Remove**.

To remove a registry entry created by
[Register the manifest with PowerShell](#label-cortex-code-excel-windows-registry), quit Microsoft Excel and run the
following:

Copy code

```
Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Office\16.0\WEF\Developer" -Name "SnowflakeCoCoExcel"
```

Restart Microsoft Excel after either change.

## Install the add-in for your organization

A Microsoft 365 administrator can install Snowflake CoCo for Microsoft Excel for everyone in the organization, or for
specific users and groups, from the Microsoft 365 admin center. This method uses the Microsoft 365 centralized
deployment feature. Assigned users get the add-in in Microsoft Excel for Windows, Mac, and the web, and they don’t need
to sideload the manifest.

During the current stage of the preview, Snowflake CoCo for Microsoft Excel isn’t listed on Microsoft Marketplace, so
you deploy it as a custom add-in from its manifest. Snowflake plans to make the add-in available on Microsoft
Marketplace in a later stage of the preview.

Before you begin, confirm the following:

- Your organization meets the Microsoft requirements for centralized deployment. For example, users need Exchange
  Online mailboxes. See
  [Determine if centralized deployment of Office Add-ins works for your organization](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/centralized-deployment-of-add-ins).
- You have a Microsoft 365 administrator role that can deploy add-ins. The same Microsoft article lists the required
  roles.

To install the add-in for your organization, follow these steps:

1. Sign in to the [Microsoft 365 admin center](https://admin.microsoft.com).
2. In the left navigation, select **Show all**, then select **Settings** > **Integrated apps**.
3. Near the top of the **Integrated apps** page, select **Add-ins**.
4. Select **Deploy Add-in**, then select **Next**.
5. Select the option to upload a custom add-in. If the wizard asks for an app type, select **Office Add-in**.
6. Provide the manifest in one of the following ways, then select **Upload**:

   - Select the option to provide a URL for the manifest, and enter
     `https://ai.snowflake.com/static/excel/releases/prod/manifest.xml`.
   - Download the manifest from `https://ai.snowflake.com/static/excel/releases/prod/manifest.xml`, select the option
     to upload the manifest file, and then select the file you downloaded.
7. Choose who gets the add-in: **Everyone**, **Specific users/groups**, or **Just me**. To test the add-in before a
   wider rollout, select **Just me** first.
8. Select **Deploy**.

Note the following about this method:

- Microsoft notes that a deployed add-in can take up to 72 hours to appear for every user. Users might need to restart
  Microsoft Excel. After the add-in appears, users open the pane as described in
  [Getting started](#label-cortex-code-excel-start).
- Deploying the add-in doesn’t connect it to your Snowflake account. An account administrator still creates an OAuth
  security integration and shares the client ID with users. See
  [Create a security integration for OAuth](#label-cortex-code-excel-oauth).
- If users already sideloaded the manifest, have them remove the sideloaded copy, because both copies register the same
  add-in ID. On Windows, see [Remove the add-in from Windows](#label-cortex-code-excel-windows-remove). On macOS, delete
  `snowflake-coco-excel.xml` from the `wef` folder and restart Microsoft Excel.
- Microsoft treats an add-in that you deploy from your own manifest as a line-of-business add-in. If the manifest
  changes, deploy the update yourself: select the add-in on the **Add-ins** page, then select **Update**.
- To change who has the add-in, or to remove it, see
  [Manage add-ins in the Microsoft 365 admin center](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/manage-addins-in-the-admin-center).

## Getting started

1. **Install Snowflake CoCo for Microsoft Excel.** See [Install the add-in](#label-cortex-code-excel-install). If your
   Microsoft 365 administrator installed the add-in for your organization, skip this step.
2. **Open the pane.** On the Microsoft Excel **Home** tab, select **Add-ins**, then select **Snowflake CoCo**.
3. **Sign in.** In the pane, enter your Snowflake [account identifier](/user-guide/admin-account-identifier) and the
   OAuth client ID for your account, then select **Sign in with Snowflake**. Your account administrator provides the
   client ID. See [Sign in from the pane](#label-cortex-code-excel-sign-in).
4. **Choose a role (optional).** Your session uses the role you entered when you signed in, or your default role. To
   use a different role, in the pane header select **More** (…) > **Settings**, then select it under **Role**.
   Changing the role signs you in again as that role.
5. **Start asking.** Describe what you want in the pane, and CoCo returns the result in your worksheet. Refine,
   pivot, chart, or add `CORTEX` formulas from the same conversation.

The following table lists example prompts for common tasks. For accurate results, include the context CoCo needs,
such as the database, schema, and objects you want to work with:

| Task | Example prompt |
| --- | --- |
| Load data | “Show last quarter’s revenue by region.” |
| Explore without SQL | “Find tables related to customer churn and pull in the churn rate by month.” |
| Pivot | “Pivot these results by product line and quarter.” |
| Chart | “Add a bar chart of total sales by month.” |
| Formula | “Add a column that calculates margin as profit divided by revenue.” |
| Enrich with Cortex AI | “Summarize the feedback column for each row.” |
| Consistent metrics | “Using the revenue semantic view, show revenue by segment for last quarter.” |

Expand

Show lessSee more

### Sign in from the pane

1. In the pane, enter your account identifier in **Account identifier** and the client ID in **OAuth client ID**.
   Optionally, enter a role in **Role**. If you leave **Role** empty, your session uses your default role.
2. Select **Sign in with Snowflake**. A sign-in page opens in your web browser.
3. In the browser, sign in with your own Snowflake credentials. The page then shows a sign-in code.
4. Select **Copy code**. The code can be used only once, and it expires in about a minute.
5. Return to the pane, paste the code in **Paste your sign-in code** or select **Paste**, and then select
   **Finish sign-in**.

### Explain cells with CoCo

You can also start a conversation from the worksheet. Select cells, right-click the selection, and select **CoCo** >
**Explain with CoCo**. The menu item’s tooltip reads “Ask CoCo to explain the selected cells — what they contain, how
any formulas compute, and where the data came from.” CoCo opens the pane and starts a conversation that reads the
selection and explains what it contains and what it’s for. For formulas, CoCo walks the formula chain and names the
precedents. For values, CoCo describes what the data represents and flags anything inconsistent, such as wrong types,
gaps, or outliers. CoCo reads and explains the selection, and any change it proposes is still previewed before it’s
applied.

[![The Microsoft Excel cell context menu for a selected range of totals, with the CoCo submenu open and Explain with CoCo in the submenu.](/static/images/screens/cortex-code-excel-explain-with-coco.png)](/static/images/screens/cortex-code-excel-explain-with-coco.png)

### Commands and skills in the `/` menu

Enter `/` in the pane to open a menu of commands and skills. The built-in commands come first, and each runs as soon as
you select it:

- `/catalog`: “Browse the Snowflake catalog to pick columns.” See
  [Browse the catalog](#label-cortex-code-excel-catalog).
- `/feedback`: “Send feedback to the Snowflake team.” See [Feedback](#label-cortex-code-excel-feedback).
- `/pivot`: “Pivot a Snowflake table or semantic view live in the sheet.” See
  [Live pivots](#label-cortex-code-excel-live-pivot).
- `/refresh`: “Re-run the Snowflake queries behind data on this sheet.” See
  [Intelligent refresh](#label-cortex-code-excel-refresh).

Your own skills follow the commands, then the skills available in your account, in alphabetical order within each
group.

[![The / menu in the CoCo pane listing the built-in commands Catalog, Feedback, Pivot, and Refresh with their descriptions.](/static/images/screens/cortex-code-excel-slash-menu.png)](/static/images/screens/cortex-code-excel-slash-menu.png)

### Attach files

To add files to a message, in the composer select **Add context** (+) > **Upload files**. You can also paste files into
the composer or drag them onto it.

You can attach images to any message. A message can hold up to 20 images, each up to 5 MB.

You can also attach documents when you’re signed in with Snowflake OAuth and a workspace is selected. In that case, the
**Upload files** item reads “Attach images, PDFs, SQL, text and other files.” Otherwise it reads “Attach images to your
message,” and only images can be attached. Each document can be up to 10 MB, and the following types are accepted:

- PDF (`.pdf`), PowerPoint (`.pptx`), and Microsoft Excel (`.xlsx`) files.
- CSV (`.csv`), JSON (`.json`), YAML (`.yaml` and `.yml`), SQL (`.sql`), and text (`.txt`) files.
- Tableau (`.twb`, `.twbx`, `.tds`, and `.tdsx`) and Power BI (`.pbix` and `.pbit`) files.

Other types, such as `.docx` and `.md`, can’t be attached. A message with documents also needs typed text.

CoCo uploads each document to your personal workspace and reads it from there while it works on your request. If you
reopen the chat later, the message text is shown, but the attached document isn’t.

[![The CoCo message box in Microsoft Excel with an attached top_customers.sql file above the prompt, and the Add context button and model picker below it.](/static/images/screens/cortex-code-excel-attachments.png)](/static/images/screens/cortex-code-excel-attachments.png)

### Follow-up suggestions

After CoCo answers, it can suggest up to three likely next requests under its latest answer. The first suggestion is
shown, and **See more** shows the others. Select a suggestion to send it as your next message.

### Send a message while CoCo works

You can keep typing while CoCo works on a request. When you send a message during a request, CoCo queues it and runs it
as the next request. The pane holds up to five queued messages, which you can edit, remove, or drag to reorder.

To steer the request that’s running instead of waiting, select **Send now** on a queued message. CoCo reads the message
between steps of the running request, and nothing is stopped. If CoCo doesn’t read the message in time, it runs as the
next request instead.

## Review changes and track sources

CoCo previews every change before it is written to your workbook. When CoCo proposes a write, it shows a
before-and-after of the affected cells so you can accept or reject the change. Accepted changes are applied together.

[![A CoCo preview in the Microsoft Excel pane that stages a margin formula and a percent format for column E, with Reject and Accept buttons.](/static/images/screens/cortex-code-excel-preview.png)](/static/images/screens/cortex-code-excel-preview.png)

You can undo an accepted change, but one change often takes more than one undo step, and the first undo might not
change anything visible. Undo again until the change is reversed. The following changes can’t be fully reversed:

- **Copying or deleting a sheet:** Microsoft Excel can’t undo these changes, and they clear the earlier undo history, so
  changes made before them can’t be undone either. In Microsoft Excel for Windows and Mac, renaming, moving, hiding, or
  unhiding a sheet has the same effect.
- **[Refreshing a table](#label-cortex-code-excel-refresh):** Undo doesn’t restore the table’s data from before the
  refresh. If PivotTables were refreshed along with the table, undo can revert the PivotTables without reverting the
  table, which leaves the PivotTables out of step with the table’s data.

Every value CoCo writes back carries a citation to the query or metric that produced it. Citations let you trace any
number in the workbook back to its source in Snowflake, so results can be verified rather than taken on trust.

## Browse the catalog

To pick data without writing SQL or a prompt, enter `/catalog` in the pane. The **Pull data** dialog opens. To close it
without pulling data, select **Cancel**, select the close button, or press Esc.

To pull data with `/catalog`, follow these steps:

1. Under **Database**, select a database. Under **Schema**, select a schema.
2. Under **Table / View**, select a table, a view, or a semantic view.
3. Choose the data to pull:

   - For a table or view, select columns under **Columns**. Use the search box to find columns, or use the select-all
     toggle to pick every column.
   - For a semantic view, select **Add** under **Dimensions**, **Metrics**, or **Facts**. In the dialog that opens,
     search for fields and select the ones you want. **Select all** picks every field that the search shows, and it
     changes to **Clear all** when they’re all picked. Fields you already added are tagged **added** and can’t be
     selected again.
4. Optionally, choose **Unique values** to return only distinct rows, or **All rows** to return every row.
5. Optionally, filter a field. The filter follows the column’s type:

   - Text and `BOOLEAN` columns: pick values from a list. To match text beyond the loaded values, search and select the
     option to match rows that contain your text in Snowflake.
   - Date and timestamp columns: enter a range of dates.
   - Time columns: enter a range of times.
   - Number columns: enter a minimum, a maximum, or both.
   - Semantic view metrics: enter a range for the metric’s total.
   - `VARIANT`, `OBJECT`, `ARRAY`, `BINARY`, `GEOGRAPHY`, `GEOMETRY`, and `VECTOR` columns can’t be filtered.
6. Select **Pull data**. The dialog closes, and the query runs in the chat. The result appears as a preview that you
   accept or reject.

The dialog remembers the last database and schema you picked while you’re signed in. It doesn’t remember the fields.

Pulled data goes into a Microsoft Excel table, and CoCo saves the query so that you can
[refresh](#label-cortex-code-excel-refresh) it later. Where the data lands depends on the cell you select before you pull:

- If the selected cell is below the sheet’s data, or to the right of it past a blank column, and the area the data needs
  is clear of tables, merged cells, and live pivots, the data lands at that cell.
- Otherwise, the data lands below the sheet’s existing data.

If the result has more rows than fit where it lands, CoCo asks before it writes anything: “The query has N rows, which
is more than can fit. Click Accept to import the first M, or Reject to import nothing.”

[![The Pull data dialog opened from /catalog in Microsoft Excel, with a database, schema, and table selected and two of the table's four columns checked.](/static/images/screens/cortex-code-excel-catalog.png)](/static/images/screens/cortex-code-excel-catalog.png)

## Live pivots

A live pivot is a pivot of a Snowflake table, view, or semantic view that Snowflake computes and CoCo draws as cells in
your sheet. The source rows stay in Snowflake, and only the pivot’s cells are written to the workbook. Each time you
change the layout, CoCo queries Snowflake again and redraws the pivot, so every total, including each subtotal, comes
from Snowflake.

A live pivot isn’t a Microsoft Excel PivotTable. It’s a block of ordinary cells that CoCo manages, so the Microsoft
Excel **PivotTable Fields** pane and PivotTable commands don’t apply to it. CoCo can also build a native PivotTable,
either from data that’s already in the workbook or by loading Snowflake data into the sheet first.

A live pivot also differs from a PivotTable in the following ways:

- Every layout change and every refresh is a Snowflake query that uses warehouse compute.
- A collapsed group isn’t fetched from Snowflake. Expanding it runs a query.
- **Expand all** and **Collapse all** open or close every level at once.

### Create a live pivot

1. Select the cell where you want the pivot to go.
2. Enter `/pivot` in the pane. The **Pull data** dialog opens, the same dialog that `/catalog` uses, without the
   **Pull data** button.
3. Select a database and a schema, then select a table, a view, or a semantic view. The pivot panel opens in the pane.
4. Add fields to the **Rows**, **Columns**, **Values**, and **Filters** zones. Until you pull the pivot, changes only
   edit the layout, and no query runs.
5. Select **Pull**. CoCo runs the query once. In **Manual** mode, the default permission mode, CoCo then asks you to
   confirm the range where the pivot will go: select **Accept** to draw the pivot, or **Cancel** to go back to the
   layout. In **Bypass** mode, CoCo draws the pivot without asking.

After the pivot is placed, each change to the layout re-queries Snowflake and redraws the pivot. While a query runs, the
panel shows its progress. Select **Stop** to cancel it: if you stop the first pull, nothing is placed and the layout is
kept; if you stop a change to a placed pivot, the last layout that was drawn is put back.

You can also ask CoCo in chat to create or change a live pivot. In **Manual** mode, CoCo shows a preview first, and the
pivot is drawn only when you accept it.

To reopen the panel for a placed pivot, select a cell in the pivot. The panel closes when you move to a sheet that
doesn’t hold that pivot.

### The pivot panel

The pivot panel has the following parts:

- **Header:** **Back to chat** returns to the conversation. The header also shows the source’s name and fully qualified
  name, and **Refresh from Snowflake** re-runs the pivot’s query.
- **Focus card:** After the pivot is placed, shows where the selected row or column heading sits in the pivot, with a
  plus or minus sign to expand or collapse each level.
- **Field list:** For a semantic view, lists the fields under **Dimensions** and **Metrics**. For a table or view,
  lists the columns under **Fields**. Select a field to add it to the layout or remove it, or drag it to a zone. Use the
  search box to find a field; press Enter to add the first match.
- **Zones:** **Filters**, **Columns**, **Rows**, and **Values**. A semantic view’s metrics go only in **Values**, and
  its dimensions never go in **Values**. A table or view column can go in any zone.

Select a field in a zone to open its menu. From the menu, you can move the field to another zone, remove it, change a
value’s aggregation, or sort. For a field in **Rows**, **Columns**, or **Filters**, select **Filter** to choose which
members to show. In the filter, select **Only these** or **Exclude these**, then pick the members. The list shows the
first 500 members, and you can search to find the others. A live pivot filters by the members you pick; it doesn’t
filter by ranges or text matches.

[![A live pivot in a Microsoft Excel sheet showing a sum of order totals by order priority and order status, next to the pivot panel with its field list and the Filters, Columns, Rows, and Values zones.](/static/images/screens/cortex-code-excel-pivot-panel.png)](/static/images/screens/cortex-code-excel-pivot-panel.png)

### Values and aggregations

A field in **Values** shows its aggregation, such as “Sum of AMOUNT”. A number column can use **Sum**, **Count**,
**Average**, **Min**, **Max**, or **Distinct count**. A text column or another non-numeric column can use **Count**,
**Distinct count**, **Min**, or **Max**. A semantic view’s metric is already defined in the semantic view, so it has no
aggregation to choose.

The same column can appear in **Values** more than once with different aggregations, such as “Sum of AMOUNT” and
“Max of AMOUNT”. To add a second value for a column, ask CoCo in chat. In the panel, each value’s menu changes only
that value, and it can’t change a value to an aggregation that the column already has.

### Expand and collapse rows and columns

A new live pivot opens collapsed at the outermost row field and the first column field. When you add a field to a
placed pivot, the new field arrives collapsed under the groups you already opened. A collapsed group still shows its
subtotal.

To expand or collapse a row or column heading, select a cell in it and use any of the following:

- The plus and minus signs on the focus card.
- The cell’s context menu: right-click the cell, then select **CoCo** > **Expand** or **CoCo** > **Collapse**.
- The keyboard: Ctrl+Alt+Shift+Right arrow to expand and Ctrl+Alt+Shift+Left arrow to collapse on Windows, or
  Control+Option+Shift+Right arrow and Control+Option+Shift+Left arrow on Mac.

To open or close every level at once, select **Expand all** or **Collapse all** in the header of the **Rows** or
**Columns** zone. These links appear when the zone holds two or more fields. **Collapse all** returns to the outermost
field. When you reopen a group, it shows what was open under it before.

### Where a live pivot goes

A live pivot goes at the selected cell, but never on top of a Microsoft Excel table or another live pivot. If the
selected cell is on one of them, the pivot goes one blank column to its right, level with its top, or below it if
there’s no room to the right. If no spot fits, CoCo asks you to select an empty area and pull again.

If the area holds other data, the confirmation says how many cells will be replaced. When a layout change makes a placed
pivot grow over other data, CoCo asks you to select **Undo the change** or **Overwrite**. A change that would make the
pivot run into a table or another live pivot is refused, and the earlier layout is put back.

To remove a live pivot, clear or delete its cells.

### What the workbook stores

The workbook stores each live pivot’s layout: its source and its fields. Unlike a
[CoCo table](#label-cortex-code-excel-refresh-pane), whose saved query is stored with the workbook, a live pivot
doesn’t store its SQL. The workbook doesn’t store data credentials. CoCo rebuilds the query from the layout each time,
using the fields that the source still has, and the query runs with the Snowflake access of whoever opens or
refreshes the pivot.

### Live pivot limits

- **Warehouse:** A live pivot runs on your current warehouse. If none is selected, CoCo shows “No warehouse is currently
  selected. Please select a warehouse with /warehouse and try again.” To select a warehouse, in the pane header select
  **More** (…) > **Settings**, and then choose one under **Warehouse**.
- **Too many rows:** A sheet ends at row 1,048,576. If a pivot with nothing expanded by hand needs more rows than that,
  for example after **Expand all** or after its source grows, CoCo collapses it at the deepest level that fits and says
  so. If you expanded groups yourself, CoCo refuses the change and suggests filtering the pivot, moving a field to
  **Columns**, or adding a field above it so that it can fold.
- **Too many columns:** If a pivot needs more columns than a sheet has, CoCo refuses the change before it downloads any
  data, and suggests filtering the pivot or moving a field from **Columns** to **Rows**.

## Intelligent refresh

CoCo can re-run the Snowflake queries behind the tables it loaded and the
[live pivots](#label-cortex-code-excel-live-pivot) it drew, so you can bring a workbook up to date without asking for
the data again.

### Refresh tables from the pane

When CoCo loads the results of a Snowflake query into your worksheet, it creates a Microsoft Excel table and saves the
query with the workbook. CoCo finds the data later through the Microsoft Excel table, not through a cell address, so
moving the table, inserting rows above it, or renaming the sheet doesn’t break refresh.

To start a refresh, use any of the following. All three run the same refresh:

- In the pane header, select **Refresh data**.
- On an empty chat, select **Refresh sheet data**.
- In the pane, enter `/refresh`. The `/` menu describes the command as “Re-run the Snowflake queries behind data on
  this sheet.”

[![The CoCo pane header in Microsoft Excel, with the Refresh data button highlighted between the All chats and More buttons.](/static/images/screens/cortex-code-excel-refresh-data.png)](/static/images/screens/cortex-code-excel-refresh-data.png)

By default, a refresh covers the CoCo tables and live pivots on the active sheet. To refresh specific tables or live
pivots, select cells that overlap them before you start the refresh. CoCo refreshes each table and live pivot that the
selection touches, always in full. Selecting a single cell doesn’t narrow the refresh. If the selected cells don’t
touch a CoCo table or a live pivot, nothing is refreshed.

A refresh also redraws each live pivot in its scope by re-running the pivot’s query. CoCo rewrites the pivot’s own cells
without a preview, the way Microsoft Excel refreshes a PivotTable. A live pivot uses warehouse compute on every
refresh.

CoCo re-runs each saved query directly, without a request to the model, under your current role and warehouse. It
then shows the new results as a preview that you accept or reject. When a refresh covers more than one table, you
choose which results to apply. Only read-only queries run: if a table’s saved query isn’t read-only, CoCo skips that
table and tells you. You can’t start a refresh while another preview is waiting for you to accept or reject it.

Refresh has the following limits:

- If a table has a total row and the refresh would change the table’s row count, CoCo doesn’t refresh that table, and
  it still refreshes the other tables. To refresh the table, turn off **Total Row** on the **Table Design** tab.
- A refresh writes up to 1,048,575 data rows per table. If a table starts below row 1, the refresh writes only the
  rows that fit below the table’s header. Above the limit, CoCo writes the first rows and tells you: “The query has N
  rows. Only the first M are imported.”
- If a refresh stops partway, for example because you stop it or the connection to Snowflake is lost, the table can
  hold a mix of old and new rows. CoCo reports how many rows it wrote and doesn’t retry. Run the refresh again to
  finish it.

### PivotTables and live pivots over a refreshed table

When you accept a refresh, CoCo also refreshes each PivotTable whose source is the refreshed table. This applies when
the PivotTable was built over the whole table, which is how CoCo creates PivotTables. A PivotTable built over a fixed
cell range isn’t refreshed, even if the range is inside the table, because the range doesn’t grow or shrink with the
table.

If a refreshed PivotTable needs more room than it has, it shows `#SPILL!` instead of the new numbers, and CoCo names
the PivotTable and its sheet. Clear or move what’s below or beside the PivotTable, and it redraws.

When a refreshed table grows, CoCo moves a PivotTable or a live pivot below the table down as a whole, so the table
doesn’t run into it.

### Refresh when the workbook opens

You can have CoCo refresh a workbook each time it opens. To turn this on, in the pane header select **More** (…) >
**Settings**, then under **Auto-refresh**, turn on **Refresh when opening**. The setting’s description reads:
“Re-runs every CoCo table on every sheet when you open this file. Each run uses warehouse credits.”

[![The Auto-refresh section of CoCo Settings, showing the Refresh when opening switch and its description.](/static/images/screens/cortex-code-excel-refresh-on-open.png)](/static/images/screens/cortex-code-excel-refresh-on-open.png)

The workbook stores its request to refresh on open in the file, along with its saved queries, so anyone who opens a
copy receives both. Your agreement to run those queries isn’t stored in the file. It applies only to you, for the
Snowflake account you’re signed in to, on the computer where you turned on the setting. Keeping the agreement out of
the file protects you: a workbook that someone sends you can’t run its queries as you until you turn on the setting
yourself. If a workbook already refreshes on open for other people, the setting stays off for you, and Settings says
that turning it on runs the workbook’s saved queries as you each time it opens.

Refresh on open runs only the queries you agreed to:

- When you turn on the setting, you agree to the queries that the workbook holds at that time.
- While the setting is on, when you accept a refresh or add a table, CoCo adds that table’s query to your agreement.
- If someone edits a saved query or adds one, that query doesn’t run when the workbook opens. CoCo names its table
  instead. To run the query, enter `/refresh` on that sheet. When you accept the result, the query runs on open from
  then on.

Your agreement covers the queries, not one particular file. A copy of the workbook, such as one made with **Save As**,
also refreshes as you when it opens, as long as its queries are unchanged.

Refresh on open runs after you sign in from the pane. It’s skipped while the workbook is open read-only or while
someone else is editing it, and CoCo tells you why. When it runs, CoCo opens the pane and shows the new results as a
preview to accept or reject, like any other refresh.

Turning off the setting removes your agreement. It also stops the workbook from refreshing on open for everyone who
opens it, because the request is stored in the workbook.

## Use CORTEX functions in cells

Snowflake CoCo for Microsoft Excel adds seven custom functions to Microsoft Excel in the `CORTEX` namespace. Enter them
in a cell like any other Microsoft Excel formula, with text or cell references as arguments. The following table lists
the functions:

| Function | Description |
| --- | --- |
| `=CORTEX.ASK(prompt, [context])` | Asks Cortex a question. The response streams into the cell. Use the optional `context` argument to give Cortex text to answer from. |
| `=CORTEX.COMPLETE(prompt)` | A shorter form of `CORTEX.ASK` that takes only a prompt. The response streams into the cell. |
| `=CORTEX.SUMMARIZE(text)` | Summarizes text or a range of cells. |
| `=CORTEX.SENTIMENT(text)` | Returns a sentiment score from -1.0 to 1.0. |
| `=CORTEX.CLASSIFY(text, labels, ...)` | Classifies text into one of the labels that you provide. Provide at least two labels, as separate arguments or as a range. |
| `=CORTEX.TRANSLATE(text, targetLanguage, [sourceLanguage])` | Translates text into the target language. Use the optional `sourceLanguage` argument to name the language of the original text. |
| `=CORTEX.FILTER(text, question)` | Answers a yes-or-no question about the text and returns `TRUE` or `FALSE`. |

Expand

Show lessSee more

The functions send each prompt to a model through the [Cortex REST API](/user-guide/snowflake-cortex/cortex-rest-api).

The functions work only after you sign in from the pane. If you aren’t signed in when a function runs, for example
just after you open a workbook, the cell waits up to 30 seconds for you to sign in, then shows an error that asks you to
open the CoCo pane and sign in to Snowflake.

## Use MCP connectors

When your account has external MCP servers that your role can use, and you’ve connected them, CoCo can use their tools
from the pane. The pane can’t connect a server itself. For how administrators set up MCP servers and how users connect
them, see [MCP Connectors](/user-guide/cortex-code/cortex-code-snowsight/mcp-connectors).

To see your connectors and choose which ones CoCo uses, follow these steps:

1. In the pane header, select **More** (…) > **Capabilities**.
2. Select **MCP Connectors**. The page lists each connected server by its name and fully qualified name.
3. Turn the switch for a server off to leave it out of your chats, or on to use it. A server is on by default, including
   one you connect later.

A server whose sign-in expired shows **Needs reconnecting**, and CoCo can’t use it until you reconnect it. Servers that
you haven’t connected aren’t listed. If you have no connected servers, the page shows “No connectors available.”

The list can take a couple of minutes to load the first time you open the pane. CoCo then keeps the list for your
account and role, so your chats don’t wait for it. To check for changes, such as a server you just connected, select
**Refresh**.

To use a server, your active role needs the `USAGE` privilege on it, and you need to have signed in to the server.

[![The Capabilities page in the CoCo pane showing MCP Connectors, with a Refresh button and an on switch for each connected server.](/static/images/screens/cortex-code-capabilities-mcp-connectors.png)](/static/images/screens/cortex-code-capabilities-mcp-connectors.png)

## Authentication and access control

You sign in to Snowflake from the pane using OAuth. CoCo authenticates with your own Snowflake identity and operates
under Snowflake [role-based access control (RBAC)](/user-guide/security-access-control-overview). It doesn’t store or
modify your credentials, and it performs only the actions your active role permits. For the steps to sign in, see
[Sign in from the pane](#label-cortex-code-excel-sign-in).

Before you can use OAuth, an account administrator creates a security integration for your account. See
[Create a security integration for OAuth](#label-cortex-code-excel-oauth).

### Create a security integration for OAuth

Before anyone can sign in from the pane with OAuth, an account administrator creates a Snowflake OAuth security
integration for a custom client. You create the integration once per Snowflake account, not once per user. Only users
with the `ACCOUNTADMIN` role, or a role with the global `CREATE INTEGRATION` privilege, can run this command.

Register the add-in as a public client. The pane runs in the Microsoft Excel browser runtime, so it can’t store a client
secret, and the add-in uses Proof Key for Code Exchange (PKCE) instead. The following example creates an integration for
Snowflake CoCo for Microsoft Excel:

Copy code

```
CREATE OR REPLACE SECURITY INTEGRATION coco_excel_oauth
  TYPE = OAUTH
  OAUTH_CLIENT = CUSTOM
  OAUTH_CLIENT_TYPE = 'PUBLIC'
  OAUTH_REDIRECT_URI = 'https://ai.snowflake.com/static/excel/oauth/callback.html'
  OAUTH_ENFORCE_PKCE = TRUE
  OAUTH_ISSUE_REFRESH_TOKENS = TRUE
  OAUTH_REFRESH_TOKEN_VALIDITY = 86400
  ENABLED = TRUE
  COMMENT = 'Snowflake CoCo for Microsoft Excel add-in';
```

Important

Set `OAUTH_REDIRECT_URI` to exactly `https://ai.snowflake.com/static/excel/oauth/callback.html`. Snowflake
compares this value to the one the add-in sends, so any difference, such as a trailing slash or a different host,
makes sign-in fail. That URL is the OAuth callback page for the add-in manifest at
`https://ai.snowflake.com/static/excel/releases/prod/manifest.xml`, which you sideload in
[Install the add-in](#label-cortex-code-excel-install).

`OAUTH_ENFORCE_PKCE = TRUE` requires PKCE on every authorization. PKCE is optional by default, and Snowflake
recommends requiring it to make the OAuth flow more secure. The refresh token settings keep users signed in across
Microsoft Excel sessions: `OAUTH_REFRESH_TOKEN_VALIDITY` is in seconds, so `86400` is one day.

To get the client ID that the add-in uses, call
[SYSTEM$SHOW\_OAUTH\_CLIENT\_SECRETS](/sql-reference/functions/system_show_oauth_client_secrets). The integration name is
case-sensitive and must be uppercase:

Copy code

```
SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS('COCO_EXCEL_OAUTH');
```

Snowflake generates the client ID when you create the integration, so the value is unique to your account. Share the
client ID with the people who use the add-in. After they install the add-in and open the pane, they paste the client ID
and your account identifier, then sign in with their own Snowflake credentials. See
[Sign in from the pane](#label-cortex-code-excel-sign-in).

By default, Snowflake blocks the `ACCOUNTADMIN`, `ORGADMIN`, `GLOBALORGADMIN`, and `SECURITYADMIN` roles from
authenticating through OAuth, so users sign in with a non-privileged role. To limit the integration to specific roles,
add `ALLOWED_ROLES_LIST`. For the full set of parameters, see
[CREATE SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/create-security-integration-oauth-snowflake). For
more information about custom clients, see
[Snowflake OAuth for custom clients](/user-guide/oauth-custom).

### Access control requirements

Because queries run under your role, CoCo can read only the databases, schemas, tables, views, and semantic views
that your active role is authorized to access, and masking and row access policies apply automatically. Query results
are written into your workbook, but the underlying data remains governed by Snowflake.

## Feedback

To report a bug or send feedback to Snowflake, enter `/feedback` in the pane. In the **Send feedback** dialog, choose a
type of feedback, describe it, optionally attach images, and select **Send**.

## Cost

Snowflake CoCo for Microsoft Excel is billed based on token consumption, consistent with other CoCo experiences, and
doesn’t require a separate per-seat license. Pricing details are provided in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

Any Snowflake compute or storage consumed separately from CoCo usage is billed at standard Snowflake on-demand rates,
as described in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf). Examples
include virtual warehouse compute used to run your queries and storage costs. A
[live pivot](#label-cortex-code-excel-live-pivot) runs a query on your warehouse each time you pull it, change its
layout, expand or collapse it, or refresh it.

[Refreshing data](#label-cortex-code-excel-refresh) from the pane doesn’t consume CoCo tokens. The workbook stores the
SQL behind each CoCo table, and a refresh runs that saved SQL directly, without a request to the model. This applies
to **Refresh data**, **Refresh sheet data**, `/refresh`, and refresh when the workbook opens. Each refresh still uses
virtual warehouse compute to run the queries. If you ask CoCo in a chat message to refresh data, that request
consumes CoCo tokens like any other CoCo request.

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
