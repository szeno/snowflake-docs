# Power BI ingestion feature support

You can upload a Power BI file to Semantic View Autopilot and have a semantic view created automatically from your existing data model. This preserves the business logic you’ve already built in Power BI, including metric definitions, table relationships, and column descriptions, and makes it available to Cortex Analyst and other Snowflake tools.

You provide the Power BI file as [context in the Autopilot wizard](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-option-2-upload-power-bi-file).

## Prerequisites

In addition to the [Autopilot prerequisites](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-prerequisites),
the Power BI ingestion feature requires:

- A stage where you have write permissions.
- Read access to the underlying tables and columns that your Power BI file references.

The file must be under 250 MB.

## How Power BI models map to Snowflake

When you upload a Power BI file, Snowflake translates your Power BI semantic model into a semantic view:

- **Tables and columns** in your Power BI model are matched to the corresponding tables and columns in Snowflake. The table names, column names, and data types carry over directly.
- **Relationships** (joins between tables) are preserved as semantic view relationships.
- **DAX measures** are registered as **metrics** in the semantic view. Single-table measures, cross-table measures, and derived metrics are all supported. For example, a DAX measure like `Total Revenue = SUM(Sales[Amount])` becomes a metric in the semantic view.
- **Calculated columns** (DAX-defined virtual columns) are included as dimensions in the semantic view, for single-table calculations.
- **Renamed tables and columns** from M query transformations (`Table.RenameColumns`) are honored. The semantic view uses the renamed display names.
- **Primary keys** are detected automatically, including composite keys where two or more columns together have unique values.

**Exceptions**: Report-level measures and time intelligence functions (such as PREVIOUSMONTH, SAMEPERIODLASTYEAR, TOTALYTD) are not yet fully supported. See the feature tables below for details.

## Supported features

The following table describes the Power BI features that are fully supported:

| Feature | Details |
| --- | --- |
| `.pbit` files | Template files without embedded data. |
| `.pbix` files | Report files with embedded data. |
| Table relationships | Mapped to semantic view relationships. |
| Single-table DAX measures | Converted to semantic view metrics. Most single-table measures are supported. |
| Cross-table measures | Emitted as top-level metrics on the semantic view. For example, `SUMX(ORDERS, ORDERS[AMT] * RELATED(CUSTOMERS[SPEND]))` works. |
| Derived metrics | Metrics that reference other metrics resolve recursively, with cycle detection. |
| Calculated columns | DAX-defined virtual columns, single-table only. |
| Renamed tables and columns | M query `Table.RenameColumns` transformations are honored. |
| Parameterized Snowflake connections | Supported, with a clear error surfaced if parameters are left null. |
| Primary key detection | Primary keys are detected automatically, including cases where two or more columns have unique values. |
| Metric descriptions | Descriptions are automatically generated for ingested metrics. |

Expand

Show lessSee more

## Partially supported features

| Feature | Details |
| --- | --- |
| Window function metrics | Filter functions (CALCULATE, FILTER, ALL, ALLEXCEPT, REMOVEFILTERS) are supported. Time intelligence functions (PREVIOUSMONTH, SAMEPERIODLASTYEAR, TOTALYTD) are not yet supported because they require report-level date context. |

Expand

Show lessSee more

## Unsupported features

The following features are not yet supported:

- **Report-level measures**: The ingestion reads DataModelSchema/DataModel, not Report/Layout.
- **Time intelligence functions**: Functions like PREVIOUSMONTH, SAMEPERIODLASTYEAR, and TOTALYTD require report-level date context that is not available during ingestion.
- **Dashboard-scoped ingestion**: Currently, the full Power BI semantic model is ingested rather than only the tables and columns used by a specific dashboard or report.

## Preparing your Power BI file

You can upload either a `.pbit` (template) or `.pbix` (report) file.

### Exporting a .pbit file from Power BI Desktop

If you want to export a template file without embedded data:

1. Open your report in Power BI Desktop.
2. Go to **File** > **Export** > **Power BI template**.
3. Save the `.pbit` file to your local machine.

The `.pbit` file contains your data model in a structured format (tables, relationships, DAX calculations, and measures) without the underlying data.

### Using a .pbix file directly

You can also upload a `.pbix` file directly. This is the standard Power BI Desktop file format and contains the data model along with embedded data.

Caution

If your Power BI semantic model uses parameters for database or schema names, make sure those parameter values are filled in before exporting. Snowflake uses these values to match tables in your account. If the parameters are left blank, table matching fails and semantic view generation does not complete.
