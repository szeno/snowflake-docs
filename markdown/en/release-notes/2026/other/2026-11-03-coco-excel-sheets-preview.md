# Nov 03, 2026: Snowflake CoCo for Excel and Snowflake CoCo for Google Sheets (*Preview*)

Snowflake CoCo for Excel and Snowflake CoCo for Google Sheets are now available in preview. Each one adds
CoCo as a chat pane inside your spreadsheet, connected to your live Snowflake data. From the pane, you can
query data with natural language or SQL; build pivot tables, charts, and formulas; and use the semantic views
your role can access. Queries run under your own role, so access control, masking, and row access policies
apply to the data that reaches your spreadsheet. CoCo previews every change before it writes to the
spreadsheet, and it records a citation to the source of each written value.

With Snowflake CoCo for Excel, you can also do the following:

- Refresh the data that CoCo loaded, either on demand or each time the workbook opens, and review the new
  results before they’re applied.
- Call Snowflake Cortex from cells with the functions in the `CORTEX` namespace, such as `=CORTEX.ASK()`.

For more information, see the following topics:

- [Snowflake CoCo for Excel](/user-guide/cortex-code/cortex-code-excel-integration)
- [Snowflake CoCo for Google Sheets](/user-guide/cortex-code/cortex-code-sheets-integration)
