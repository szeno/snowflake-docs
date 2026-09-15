# Aug 27, 2026: CoCo in the Snowflake Extension for Visual Studio Code (*General availability*)

CoCo in the Snowflake Extension for Visual Studio Code is now generally available. CoCo runs in a side panel next to the extension’s
existing SQL and Snowpark Python workflows, so you can work locally while you stay connected to your
Snowflake account.

This release requires version 1.39 or later of the Snowflake Extension for Visual Studio Code.

## No separate CoCo installation

The extension includes everything CoCo needs to run, so no separate CoCo installation is required.
To have the extension use a specific CoCo executable instead, set **CoCo: CLI Path** to its full path.

## Start CoCo from where you’re working

- **Ask CoCo** appears above each SQL statement in the editor. Select it to open CoCo with that
  statement as context.
- **Fix with CoCo** appears with the error message in the query results pane when a query fails.
  Select it to open CoCo with the failed statement and its error.

## Extension settings for CoCo

You can control CoCo in the extension with the following settings. This release adds
`snowflake.coco.cliPath` and `snowflake.coco.showAskCocoAboveStatement`.

| Setting | Description | Default |
| --- | --- | --- |
| `snowflake.coco.cliPath` | Override the CoCo executable that the extension uses | Unset |
| `snowflake.coco.showAskCocoAboveStatement` | Show the **Ask CoCo** action above each SQL statement | Enabled |
| `snowflake.coco.enabled` | Enable or disable the CoCo side panel for all workspaces | Enabled |

Expand

Show lessSee more

## Snowsight results viewer enabled by default

The `snowflake.queryResults.snowsightResultsViewer` setting is now enabled by default. Query results
render with the Snowsight results viewer, the same component that renders results in
Snowsight. This supports the display of up to 1 million rows. To switch back to the legacy
results table, disable the setting.

For more information, see [CoCo in the Snowflake Extension for Visual Studio Code](/user-guide/vscode-ext#label-cortex-code-vscode-extension) and
[Start CoCo from the editor and query results](/user-guide/vscode-ext#label-cortex-code-vscode-shortcuts).
