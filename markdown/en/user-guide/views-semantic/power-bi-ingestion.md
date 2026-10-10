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
- **Relationships** (joins between tables) are preserved as semantic view relationships, except where a semantic view cannot represent one; those are removed and named in the response.
- **DAX measures** are registered as **metrics** in the semantic view. Single-table measures, cross-table measures, and derived metrics are all converted. For example, a DAX measure like `Total Revenue = SUM(Sales[Amount])` becomes a metric in the semantic view.
- **Calculated columns** (DAX-defined virtual columns) are included as dimensions in the semantic view, for single-table calculations.
- **Renamed tables and columns** from M query transformations (`Table.RenameColumns`) are honored. The semantic view uses the renamed display names.
- **Primary keys** are detected automatically, including composite keys where two or more columns together have unique values.

**Exceptions**: Measures saved in the report rather than in the data model are not read, and some DAX does not convert — time intelligence, statistical aggregates, and anything that depends on what the report reader selected. A measure can also convert and still be rejected as a metric. See the feature tables below, and [Why a measure was not converted](#label-power-bi-ingestion-measure-not-converted).

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
| Parameterized Snowflake connections | Supported. A table whose parameters are left null is named in the response rather than dropped silently. |
| Primary key detection | Primary keys are detected automatically, including cases where two or more columns have unique values. |
| Metric descriptions | Generated automatically for up to 60 metrics. A model with more keeps the rest without a generated description. |
| Columns added in Power Query | A `Table.AddColumn` step becomes a dimension when its expression can be expressed in SQL, and is named in the response when it cannot. |

Expand

Show lessSee more

## Partially supported features

| Feature | Details |
| --- | --- |
| Window function metrics | Filter functions (CALCULATE, FILTER, ALL, ALLEXCEPT, REMOVEFILTERS) are supported. KEEPFILTERS and the time intelligence functions (PREVIOUSMONTH, SAMEPERIODLASTYEAR, TOTALYTD) are not. |
| DAX measures | Most single-table and cross-table measures convert, but not every DAX function has a SQL equivalent, and not every valid DAX expression is valid as a semantic view metric. See the two sections below. |
| Relationships | A many-to-many relationship is kept only when one side has the unique key a semantic view requires. Without it the relationship is removed and the response says so. |

Expand

Show lessSee more

## Unsupported features

The following features are not yet supported:

- **Report-level measures**: Measures saved in the report rather than in the data model, as happens with a live connection. Ingestion reads the data model (DataModelSchema/DataModel), not the report layer (Report/Layout). This is about where the measure is stored in Power BI; measures that read more than one table are still converted, as top-level metrics on the semantic view.
- **Time intelligence functions**: Functions like PREVIOUSMONTH, SAMEPERIODLASTYEAR, and TOTALYTD require report-level date context that is not available during ingestion.
- **Other functions that depend on report or selection context**: SELECTEDVALUE, ALLSELECTED, and ISFILTERED describe what the reader clicked, which a stored query cannot know.
- **Statistical aggregates**: MEDIAN, PERCENTILE, and the STDEV and VAR families.
- **Table-valued functions used inside a measure**: SUMMARIZE, TOPN, RANKX, CONTAINS, ISEMPTY, and COUNTROWS over VALUES.
- **RELATEDTABLE**: RELATED is supported; RELATEDTABLE is not.
- **DAX calculated tables and calculation groups**: These have no Snowflake table behind them, so they are dropped along with any measure that reads them.
- **Tables whose rows are stored in the file**: Data entered directly in Power BI, rather than read from Snowflake, has no table to point at.
- **Dashboard-scoped ingestion**: Currently, the full Power BI semantic model is ingested rather than only the tables and columns used by a specific dashboard or report.

## Why a measure was not converted

When some measures do not convert, the response names them and groups them by cause. There are five causes, and they call for different fixes:

| Cause | What it means | What to do |
| --- | --- | --- |
| `missing table or column` | The measure reads a table or column that is not in the imported model, usually because that table was itself dropped. | Fix the table first; the measures that read it convert on the next import. |
| `unsupported DAX` | The expression uses a function with no SQL equivalent. | Rewrite the measure using supported functions, or add it to the semantic view by hand. |
| `not valid as a semantic-view metric` | The DAX converted, but the resulting SQL is not a valid metric. A metric must be a single aggregate over its own table’s rows, so an expression with no aggregate at all (for example `TODAY()`), with one aggregate nested inside another, with a subquery, or with a column left outside the aggregate is rejected. | Express the value as a metric over one table, or model it as a dimension instead. |
| `metric table could not be determined` | The expression does not name a table clearly enough to attach the metric to one. | Qualify the columns the measure reads. |
| `DAX transpilation failed` | The expression could not be read at all. | Report it; this one is ours to fix. |

Expand

Show lessSee more

## Why a table was not imported

Tables that do not reach the semantic view are named in the response with a reason:

| Reason | What to do |
| --- | --- |
| `UNBOUND_PARAMETERS` | The connection uses parameters for the database or schema and they have no values. Fill them in and export again. |
| `NON_SNOWFLAKE_SOURCE` | The table reads from something other than Snowflake. Only Snowflake-backed tables can be mapped. |
| `NO_SNOWFLAKE_REFERENCE` | The table does not read from Snowflake directly. Either it is built inside Power BI — combined, entered, or derived from another query — or it is a composite model chained to another dataset, which is the most common case. |
| `CALCULATED_TABLE` | A DAX calculated table or calculation group, which has no Snowflake table behind it. |
| `PARSER_FAILURE` | A Snowflake connection we could not read. This is a gap on our side, not something to change in the file. Report it with the request ID. |

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

If your Power BI semantic model uses parameters for database or schema names, make sure those parameter values are filled in before exporting. Snowflake uses these values to match tables in your account. Tables whose parameters are blank are dropped and listed in the response as `UNBOUND_PARAMETERS`; if that leaves no tables at all, generation fails.
