# Tableau ingestion feature support

Semantic View Autopilot turns your Tableau data model into a semantic view. It carries over the business logic you’ve
already built in Tableau, including calculated fields and relationships, and, for uploaded files, parameters and filters,
and makes it available to
Cortex Analyst and other Snowflake tools.

You can provide the model in two ways:

- Upload a Tableau file as [context in the Autopilot wizard](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-option-1-upload-tableau-file).
- If you have a Horizon Catalog connector for Tableau, import a data source directly. See
  [Create a semantic view from a Horizon Catalog connector](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-connected-bi).

## Prerequisites

In addition to the [Autopilot prerequisites](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-prerequisites),
uploading a Tableau file requires:

- A stage where you have write permissions.
- The `CREATE VIEW` privilege on the schema, if your Tableau file contains Custom SQL or unions. Autopilot creates a
  regular Snowflake view for each one.
- Read access to the underlying tables and columns that your Tableau file references.

## How Tableau models map to Snowflake

When you provide a Tableau model, Snowflake translates it into a semantic view:

- **Tables and columns** in your Tableau data source are matched to the corresponding Snowflake tables and columns.
- **Relationships and joins**, from both the logical layer and the physical layer, become semantic view relationships.
- **Calculated fields** become facts, dimensions, or metrics. Aggregations become metrics, and row-level calculations
  become facts or dimensions. Table calculations that a worksheet uses become window functions.
- **Parameters** keep their current value in the calculations and Custom SQL that use them, and are described in the
  semantic view’s custom instructions.
- **Filters** on categorical values, quantitative ranges, and relative dates become named filters in the semantic view.
  Data source filters also become named filters, and custom instructions direct Cortex Analyst to apply them to every
  query.
- **Aliases** for column values are carried over, so the semantic view returns the same labels as Tableau.
- **Custom SQL and unions** become regular Snowflake views that the semantic view reads from.
- **Descriptions** are generated for metrics and filters, based on how the workbook uses them.

## Supported features

The following table describes the Tableau features that Semantic View Autopilot supports:

| Feature | Details |
| --- | --- |
| `TWB` and `TWBX` workbooks | Workbook files. Autopilot reads the Snowflake tables directly, so packaged extracts aren’t needed. |
| `TDS` and `TDSX` data sources | Data source files, including published data sources downloaded from Tableau Server or Tableau Cloud. |
| Relationships and joins | Logical-layer relationships and physical-layer joins become semantic view relationships. |
| Calculated fields | Single-table calculations become facts, dimensions, and metrics. More than 100 Tableau functions are converted to SQL. |
| Table calculations | Converted to window functions when a worksheet in the workbook uses them. |
| Parameters | Current values are applied in calculations and Custom SQL, and each parameter is described in the custom instructions. |
| Filters | Categorical, range, and relative-date filters become named filters. Data source filters are applied to every query. |
| Aliases | Value aliases are applied, so results use the same labels as Tableau. |
| Custom SQL and unions | Each becomes a regular Snowflake view. |
| Multiple data sources | All data sources that the workbook’s worksheets use are combined into one semantic view. |
| Descriptions | Generated for metrics and filters from how the workbook uses them. |

Expand

Show lessSee more

## Import from a Horizon Catalog connector

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts in AWS deployments.

When you import a data source from a Horizon Catalog connector instead of uploading a file, Autopilot reads the same model
from Horizon Catalog. The following differences apply:

- Field descriptions that you wrote in Tableau are carried over, and relationships keep their cardinality.
- Measures that read columns from related tables become metrics on the semantic view.
- Level of Detail (LOD) expressions are converted: `INCLUDE` and `EXCLUDE` measures, and `FIXED` dimensions. This
  requires [LOD metrics](/user-guide/views-semantic/querying#label-semantic-views-querying-lod) in semantic views, which
  are in preview.
- Custom SQL that Horizon Catalog provides is used directly in the semantic view, so no view is created and you don’t
  need the `CREATE VIEW` privilege.

To import a model, see
[Create a semantic view from a Horizon Catalog connector](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-connected-bi).

## Limitations

- The tables must resolve to a Snowflake connection. Tables from other databases, text files, or Microsoft Excel
  workbooks aren’t imported.
- In an uploaded file, calculations that read columns from more than one table and LOD expressions aren’t converted.
- In an import from a Horizon Catalog connector, parameters, table calculations, filters, aliases, and generated descriptions aren’t carried
  over.
- Condition, Top N, wildcard, and action filters aren’t converted, and neither are exclude-mode categorical filters or
  categorical filters with more than 100 values.

Autopilot lists each item that it couldn’t convert, with the reason.

## Preparing your Tableau file

You can upload a `TWB`, `TWBX`, `TDS`, or `TDSX` file. The workbook or data source definition in the file must be under
250 MB.

You can get the `TWB` or `TWBX` file from Tableau Desktop. If you can’t find it, select **File** > **Save As** and save
the workbook as a `TWB` file.

For information about getting a view or workbook from Tableau Cloud, see
[Download Views and Workbooks](https://help.tableau.com/current/pro/desktop/en-us/export.htm).

## Published data sources

If a workbook connects to a data source published to Tableau Server or Tableau Cloud rather than embedding its own
connection, the file carries only a server-side reference, so Semantic View Autopilot can’t see the Snowflake tables. To
provide the published data source:

1. Upload the workbook. Autopilot detects the reference and prompts you for the published data source.
2. Download the published data source from Tableau as a `TDS` or `TDSX` file.
3. Upload the `TDS` or `TDSX` file as a second file.

Only one published data source per workbook is supported. If you have a Horizon Catalog connector for Tableau, you can
import the published data source directly instead.
