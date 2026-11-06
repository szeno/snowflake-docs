# HTML reports (*Preview*)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

An HTML report is a self-contained HTML file you can create with CoCo in Snowsight Workspaces, CoCo Desktop, or Snowflake CoWork and publish as a shareable artifact. In Workspaces, the editable source file remains in your workspace.

Describe the data, structure, and charts you want, and CoCo writes the HTML for you. Published reports open in an artifact view. If you created the report in Workspaces, its source file remains there for editing and publishing updates.

Data access

Query results in an HTML report are embedded in the published artifact. Opening the report does not run those queries again with the viewer’s role or require a warehouse. A user who can view the report can see its embedded data even if that user can’t query the source data directly.

Review the report’s content and intended audience before you publish it.

## What you can build

Reports are well suited to narrative and presentation use cases where layout and design freedom matter:

- **Static reports for presentations.** Turn a SQL query or analysis into a presenter-ready document with charts and summary statistics: shareable before a meeting and viewable after.
- **Slide-deck-style reports.** Ask CoCo to format findings as a series of full-bleed sections that scroll like slides, which is useful for asynchronous executive updates.
- **Designed data narratives.** Replace a text-only page with a designed document, such as an onboarding guide, OKR page, or findings brief with interactive charts.

## Create an HTML report

Creating and refreshing an HTML report with CoCo in Snowsight requires access to CoCo. For access requirements, see [Access control requirements](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-snowsight-access-control).

To create an HTML report in Workspaces:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**, and open a workspace.
3. In the new file menu, select **Report**, or open a chat with CoCo in Snowsight.
4. Describe the report you want: the data to include, the structure, and any charts you need. For example:

   > Create an HTML report showing Q2 sales by region with a bar chart and a summary table.
5. Review the queries that CoCo runs and the generated report. CoCo generates an `.html` file and saves it to your workspace automatically.
6. Iterate before publishing: Change colors, restructure sections, add charts, or update the data.

You can also edit the report directly in Workspaces.

You can also [generate HTML in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/document-generation). To share a generated report from CoWork, publish it as an artifact; generation alone doesn’t share it.

## Edit an HTML report

Open an HTML report in Workspaces, and then select **Edit**. The editor provides the following modes for visual (WYSIWYG) and source editing:

- **Preview**: Edit text and other static content directly in the rendered report. JavaScript runs in this mode, so charts and other dynamic content are visible but can’t be edited directly.
- **No JavaScript**: Edit the report’s content without running its JavaScript. Use this mode to edit source content that JavaScript replaces when the report is rendered.
- **Code**: Edit the HTML, CSS, and JavaScript source.

Select **Save** to update the workspace file. Saving the file does not update a published artifact. To make your changes visible to report viewers, publish the report again.

## Refresh report data with CoCo

An HTML report contains a snapshot of query results. To refresh the results:

1. Open the report’s source file in Workspaces.
2. Select **Refresh report**.
3. Review or change the refresh instructions, and then select **Refresh**.
4. Review the updated report before publishing it again.

CoCo refreshes the report data and updates the source file. To update the published artifact, publish the report again. The artifact URL remains the same.

## Publish and share an HTML report

Publish an HTML report from the surface where you created it: Workspaces, Snowflake CoWork, or CoCo Desktop. Publishing creates a Report artifact from the current HTML. The same artifact grants govern who can access it regardless of where you publish. To share it or change who can view it, your role needs `MANAGE ACCESS ON REPORT ARTIFACTS` and authority to manage that artifact’s grants. For more information, see [Sharing privileges](/user-guide/snowflake-artifacts#label-snowflake-artifacts-sharing-privileges).

To publish or share a report from Workspaces:

1. Open the report’s source file in Workspaces. Select **Publish artifact**, or **Share** if you’ve already published it. The sharing dialog opens.
2. Under **Who has access**, review the roles and users who can view or publish the report. By default, only the owner has access. Add the intended roles or users and choose **Can view** (`READ`) or **Can publish** (`WRITE`). To find an individual user, search by Snowflake username.
3. If you’re publishing for the first time, select **Create**. The artifact link is copied to your clipboard. For an existing artifact, use the sharing dialog to publish an update or change access.
4. Send the link to the intended recipients.

To publish a report generated in CoWork, select **Publish artifact** on the HTML result and choose who can access it. To publish from CoCo Desktop, open the HTML file, select **Publish artifact**, and choose who can access it. See [Create and share a dashboard or HTML report](/user-guide/snowflake-artifacts-create-share) for the surface-specific procedures.

Once a report is published, its link stays the same when you update and republish it. The link points to the latest published version, not unpublished edits to the source.

Publishing creates one report artifact for the account, not a separate copy for each surface. Recipients with access can open it from supported surfaces, including Snowsight, Snowflake CoWork, and CoCo Desktop. The same role and user grants apply regardless of where they open it.

Recipients with access to the Report artifact can view its embedded data without access to the underlying source data.

A recipient must sign in to the same Snowflake account and have access through a role or an individual user grant. Granting `READ` to the `PUBLIC` role lets every user in the account view the report; an account-level `MANAGE ACCESS` grant to `PUBLIC` alone does not. You can search for an individual by Snowflake username.

Find accessible reports under **Projects** » **Artifacts**, or open a report from its shared link.

To update a published report, edit or regenerate the HTML in your source workflow and publish it again. Publishing an update replaces the displayed report but retains the existing artifact URL.

View access to the artifact does not grant edit access to the workspace source file.

## Print or save a report as PDF

Open the report in Workspaces or from **Projects** » **Artifacts**, and then select **Print**. In the browser print dialog, print the report or select the browser’s option to save it as a PDF.

## Supported libraries and report security

Reports run in a strict sandbox. Readers can open links to external sites, but the report itself can’t load CDN scripts, external APIs, or remote images. JavaScript is limited to the report’s own inline scripts plus Snowflake’s vendored libraries. These rules apply to all report HTML, whether generated by CoCo or uploaded directly.

The following libraries are available:

- Charts and visualizations: Chart.js, Plotly cartesian charts, D3, Vega, Vega-Lite, and Vega-Embed.
- Diagrams: Mermaid.
- 3D content: Three.js.
- Text, code, and math: Marked, highlight.js, and KaTeX.

Because reports run under a strict content security policy, requests to load external resources within a report are blocked. This does not prevent a reader from opening an external link. Inline event-handler attributes such as `onclick` and `onload` are also blocked. Use `addEventListener` in inline JavaScript when an event handler is required.

## Limitations

The following limitations apply during preview:

- **Snapshot data.** A report contains data from the last time it was created or refreshed. Reports do not refresh automatically. Use **Refresh report** to refresh the data with CoCo, and then publish the report again.
- **No scheduled refresh or delivery.** Scheduled refresh and scheduled delivery through Slack, Microsoft Teams, or email are not supported.
- **Vendored libraries only.** Reports can’t load external scripts, APIs, or images. Only Snowflake’s vendored libraries are available.
- **File size.** If an HTML report exceeds the account’s artifact file-size limit, reduce its size, for example by compressing embedded images, before publishing it.
- **Source editing.** A recipient with access to the artifact does not automatically have access to edit its Workspaces source file.
