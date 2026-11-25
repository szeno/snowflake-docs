# Power BI ingestion feature support

You can upload a Power BI file to Semantic View Autopilot to generate a semantic view from your existing data model. This preserves the business logic you’ve already built in Power BI, including metric definitions, table relationships, and measure descriptions, and makes it available to Cortex Analyst and other Snowflake tools.

You provide the Power BI file as [context in the Autopilot wizard](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-option-2-upload-power-bi-file).

If you have a Horizon Catalog connector for Power BI, you can import a semantic model directly instead of uploading
a file. See [Create a semantic view from a Horizon Catalog connector](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-connected-bi).

## Prerequisites

In addition to the [Autopilot prerequisites](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-prerequisites),
uploading a Power BI file requires:

- A stage where you have write permissions.
- Read access to the underlying tables and columns that your Power BI file references.

The file must be under 250 MB.

## How Power BI models map to Snowflake

Snowflake translates your Power BI semantic model into a semantic view:

- **Tables and columns** in your Power BI model are matched to the corresponding tables and columns in Snowflake. The table names, column names, and data types carry over directly.
- **Relationships** (joins between tables) are preserved as semantic view relationships.
- **DAX measures** are registered as **metrics** in the semantic view. Single-table measures, cross-table measures, and derived metrics are all converted. For example, a DAX measure like `Total Revenue = SUM(Sales[Amount])` becomes a metric in the semantic view.
- **Calculated columns** (DAX-defined virtual columns) are included as dimensions in the semantic view, for single-table calculations.
- **Power Query steps** are honored: renamed tables and columns (`Table.RenameColumns`), row filters (`Table.SelectRows`), and added columns (`Table.AddColumn`) whose expression can be written in SQL.
- **Keys** that you marked in Power BI, and the column on the one side of each one-to-many relationship, become unique keys, including composite keys.
- **Descriptions** that you wrote for measures in Power BI are carried over. For an uploaded file, descriptions are generated for metrics that don’t have one.

Autopilot lists each measure and table that it couldn’t convert, with the reason. See
[Why a measure was not converted](#label-power-bi-ingestion-measure-not-converted) and
[Why a table was not imported](#label-power-bi-ingestion-table-not-imported).

## Supported features

The following table describes the Power BI features that Semantic View Autopilot supports:

| Feature | Details |
| --- | --- |
| `.pbit` files | Template files without embedded data. |
| `.pbix` files | Report files with embedded data. |
| Table relationships | Active relationships are mapped to semantic view relationships. |
| Single-table DAX measures | Converted to semantic view metrics. Most single-table measures are supported. |
| Cross-table measures | Converted to metrics on the semantic view. For example, `SUMX(ORDERS, ORDERS[AMT] * RELATED(CUSTOMERS[SPEND]))` is converted. |
| Derived metrics | Metrics that reference other metrics are converted. |
| Filter context in measures | `CALCULATE` with `FILTER`, `KEEPFILTERS`, and `ALL` or `REMOVEFILTERS` on a column is converted. Removing filters on a column becomes a window metric. |
| Calculated columns | DAX-defined virtual columns, single-table only. |
| Power Query steps | Renamed tables and columns, row filters, and added columns whose expression can be written in SQL. |
| Parameterized Snowflake connections | Supported. A table whose parameters have no values is listed as `UNBOUND_PARAMETERS`, so you can supply the values. |
| Hidden tables and columns | Imported the same way as visible tables and columns, if they read from Snowflake. |
| Keys | Key columns and the column on the one side of each one-to-many relationship become unique keys, including composite keys. |
| Descriptions | Measure descriptions from Power BI are carried over. For an uploaded file, descriptions are generated for metrics that don’t have one. |

Expand

Show lessSee more

## Import from a Horizon Catalog connector

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts in AWS deployments.

When you import a semantic model from a Horizon Catalog connector instead of uploading a file, Autopilot reads the
same model from Horizon Catalog, and native queries (`Value.NativeQuery`) are used directly as table definitions.

DAX measures, native queries, and Power Query steps are available only when the Power BI tenant setting **Enhance admin
APIs responses with DAX and mashup expressions** is turned on, as described in
.

To import a model, see
[Create a semantic view from a Horizon Catalog connector](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-connected-bi).

## Limitations

- Only tables that read from Snowflake are imported. DAX calculated tables, calculation groups, and data entered
  directly in Power BI have no Snowflake table behind them.
- Some DAX functions have no SQL equivalent, such as time intelligence functions, statistical aggregates, and table
  functions. Measures that use them aren’t converted.
- Inactive relationships, and measures that use `USERELATIONSHIP`, aren’t converted.
- Measures saved in the report rather than in the data model, as happens with a live connection, aren’t read.
- A many-to-many relationship is kept only when one side has a unique key.

## Why a measure was not converted

When some measures don’t convert, Autopilot lists them grouped by cause. Each cause calls for a different fix:

| Cause | What it means | What to do |
| --- | --- | --- |
| `missing table or column` | The measure reads a table or column that is not in the imported model, usually because that table wasn’t imported. | Resolve the issue with that table; the measures that read it convert on the next import. |
| `unsupported DAX` | The expression uses a function with no SQL equivalent. | Rewrite the measure using supported functions, or add it to the semantic view manually. |
| `not valid as a semantic-view metric` | The DAX converted, but the resulting SQL is not a valid metric. A metric must be a single aggregate over its own table’s rows, so an expression with no aggregate at all (for example `TODAY()`), with one aggregate nested inside another, with a subquery, or with a column left outside the aggregate is rejected. | Express the value as a metric over one table, or model it as a dimension instead. |
| `metric table could not be determined` | The expression does not name a table clearly enough to attach the metric to one. | Qualify the columns the measure reads. |
| `DAX transpilation failed` | The expression couldn’t be parsed. | Add the measure to the semantic view manually, or contact Snowflake Support. |

Expand

Show lessSee more

## Why a table was not imported

Autopilot lists each table that doesn’t reach the semantic view, with a reason:

| Reason | What to do |
| --- | --- |
| `UNBOUND_PARAMETERS` | The connection uses parameters for the database or schema and they have no values. Fill them in, and then upload the file again. |
| `NON_SNOWFLAKE_SOURCE` | The table reads from something other than Snowflake. Only Snowflake-backed tables can be mapped. |
| `NO_SNOWFLAKE_REFERENCE` | The table doesn’t read from Snowflake directly. It’s built inside Power BI: combined or derived from another query. |
| `EMBEDDED_ROWS` | The table’s rows are entered directly in Power BI, so there’s no Snowflake table behind it. |
| `MISSING_IN_SNOWFLAKE` | For an import from a Horizon Catalog connector, the Snowflake table doesn’t exist or your role can’t read it. Check the table and your privileges. |
| `CALCULATED_TABLE` | A DAX calculated table or calculation group, which has no Snowflake table behind it. |
| `PARSER_FAILURE` | Semantic View Autopilot couldn’t read the table’s Snowflake connection. Contact Snowflake Support. |

Expand

Show lessSee more

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

If your Power BI semantic model uses parameters for database or schema names, make sure those parameter values are filled in before exporting. Snowflake uses these values to match tables in your account. Tables whose parameters are blank aren’t imported and are listed as `UNBOUND_PARAMETERS`; if that leaves no tables at all, generation fails.
