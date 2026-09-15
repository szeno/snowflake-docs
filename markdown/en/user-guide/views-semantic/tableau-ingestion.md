# Tableau ingestion feature support

Semantic View Autopilot supports using a file from Tableau to automatically generate a semantic view. This lets you
migrate your existing business logic and metadata directly into Snowflake.

You provide the Tableau file as [context in the Autopilot wizard](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-option-1-upload-tableau-file).

## Prerequisites

In addition to the [Autopilot prerequisites](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-prerequisites),
the Tableau ingestion feature requires:

- A stage where you have write permissions.
- If your Tableau file contains Custom SQL, you must also have the CREATE VIEW privilege on the schema because the SQL is
  parsed into a regular Snowflake view.

## Supported file formats

You can either use Tableau Desktop or Tableau Online to provide the file to Semantic View Autopilot. Semantic View
Autopilot supports the following file formats:

- `TWB`
- `TWBX`
- `TDS`
- `TDSX`

## File constraints

The file must meet the following constraints:

> - Snowflake Connections Only: The tables in the file must resolve to a direct Snowflake connection. Connections to other databases aren’t supported.
> - File Size: Must be under 250 MB.
> - No Large Extracts: If using a .twbx file, ensure it does not contain a large extract. If using a .twb file, ensure it does not contain large filters or parameters.
> - LOD Calculations: Level of Detail (LOD) calculations are not supported.

## Preparing your Tableau file

You can get the `TWB` or `TWBX` file from Tableau Desktop. If you can’t find it, you can go to `File | Save As` and choose to save as a `TWB`.

For information about getting a view or workbook from Tableau Online, see [Download Views and Workbooks](https://help.tableau.com/current/pro/desktop/en-us/export.htm).

## Published data sources and virtual connections

If a workbook connects to a data source published to Tableau Server or Tableau Cloud rather than embedding its own
connection, the file carries only a server-side reference, so Semantic View Autopilot can’t see the Snowflake tables.
Upload the workbook first. Autopilot detects the reference and prompts you for the published data source, which you
download from Tableau as a `TDS` or `TDSX` file and upload as a second file. Only one published data source per workbook
is supported.

Tableau virtual connections, part of Tableau Data Management, aren’t supported. Recreate the workbook against a direct
Snowflake connection instead.

## Extracted metadata

After you provide the Tableau file to Semantic View Autopilot, autopilot parses it to extract the following metadata:

> - Tables and Columns
> - Relationships between tables
> - Tableau calculated fields
> - Parameters and Filters
> - Custom SQL (parsed and turned into a regular Snowflake view)
