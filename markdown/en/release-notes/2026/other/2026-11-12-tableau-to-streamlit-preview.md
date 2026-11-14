# Nov 12, 2026: Convert Tableau workbooks to Streamlit in Snowflake apps with CoCo (*Preview*)

The `tableau-to-streamlit-in-snowflake` skill for Cortex Code (CoCo) is now available in preview. The skill
converts a Tableau workbook into a multipage Streamlit in Snowflake app, with one app page for each Tableau dashboard.
Worksheets become native Streamlit charts and tables, calculations become Snowflake SQL, and dashboard
filters, parameters, and actions become Streamlit widgets and chart selections.

You review the app on synthetic data first. CoCo switches the same app to your Snowflake tables only after
you approve the UI and the real-data mapping, and it asks for your approval before it queries real tables.
In CoCo CLI and CoCo Desktop, it also asks before it deploys the app or grants roles access to the app; in
CoCo in Snowsight, you run the app yourself. Roles that you give access to the synthetic preview
keep that access after the switch, so share the preview only with roles that are allowed to see the real data.

The skill is bundled with CoCo CLI version 1.2.33 or later, CoCo Desktop version 1.23.1 or later, and CoCo in
Snowsight. To start, type
`/tableau-to-streamlit-in-snowflake` in the CoCo chat, or ask CoCo to convert a Tableau workbook to a
Streamlit in Snowflake app.

For more information, see the following topics:

- [Convert Tableau workbooks to Streamlit in Snowflake apps with CoCo](/developer-guide/streamlit/migrations-and-upgrades/tableau-to-streamlit)
- [tableau-to-streamlit-in-snowflake](/user-guide/cortex-code/bundled-skills#label-bundled-skill-tableau-to-streamlit-in-snowflake)
