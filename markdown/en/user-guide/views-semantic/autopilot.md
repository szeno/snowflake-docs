# Semantic View Autopilot

Semantic View Autopilot is the AI-assisted way to create a [semantic view](/user-guide/views-semantic/overview) in
Snowsight. Instead of writing a [YAML specification](/user-guide/views-semantic/semantic-view-yaml-spec) by
hand, you describe what you want and Autopilot generates the logical tables, relationships, and metrics for you.

Autopilot covers creation. After the view exists, you refine and deploy it in
[Semantic Studio](/user-guide/views-semantic/semantic-studio).

## Open Semantic View Autopilot

You reach Autopilot through Semantic Studio:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Workspaces**.
3. Select **Add new** » **Semantic View**.

This opens the Autopilot wizard.

Note

You can use the instructions in this section to also create a semantic model, but we recommend using semantic views
instead. Semantic views provide the following features:

- Semantic views support advanced features such as Derived Metrics.
- Semantic views support access modification. They’re public by default, but you can make them private.
- Semantic views are schema objects that integrate with Snowflake’s privilege system, sharing mechanisms, and metadata
  catalog. Semantic models are YAML files stored in a stage and lack these native database integrations.

## Prerequisites

To create a semantic view, you must use a role with the following privileges:

- CREATE SEMANTIC VIEW on the schema where you are creating the semantic view.
- USAGE on the database and schema where you are creating the semantic view.
- SELECT on the tables and views used in the semantic view.

You can export a model from Tableau and use it to automatically generate a semantic view. In addition to the preceding
prerequisites, the Tableau ingestion feature requires:

- A stage where you have write permissions.
- The `CREATE VIEW` privilege on the schema, if your Tableau file contains Custom SQL or unions. Autopilot creates a
  regular Snowflake view for each one.

You can also upload a Power BI file (.pbit or .pbix) to automatically generate a semantic view. In addition to the
preceding prerequisites, the Power BI ingestion feature requires:

- A stage where you have write permissions.
- Read access to the underlying tables and columns that your Power BI file references.

You can also import a model from a Horizon Catalog connector, without exporting a file. This option is in preview and
is available to all accounts in AWS deployments. In addition to the preceding prerequisites for creating a semantic
view, importing from a Horizon Catalog connector requires:

- A [Horizon Catalog connector](/user-guide/snowflake-horizon/connectors) for a supported BI tool that has completed at
  least one full ingestion.
- A role with `READ EXTERNAL METADATA` or `USAGE` on the connector, and `USAGE` on the database and schema that contain
  it. For details, see [View metadata and lineage](/user-guide/snowflake-horizon/connectors/access-control#view-metadata-and-lineage).
- Lineage in Horizon Catalog from Snowflake tables to the model. At least one of the model’s tables must read from a
  single Snowflake table. Models without this lineage are marked **No Snowflake source** and can’t be imported.
- Read access to the Snowflake tables and columns that the model uses.

## Creating a semantic view

### Using Semantic View Autopilot to create a semantic view

Use the AI-assisted generator to create a semantic view that combines semantic information from multiple sources. Instead
of creating a semantic view manually with your own YAML specification, you can use the generator within Snowsight
to save time. The process of creating a semantic view requires the following information:

- A description with basic information about the view
- Context, such as example SQL queries
- The data source (at least one table or view) that you’re using
- The columns that you’re using

The AI-assisted generator handles inputs in the following ways:

- **Example SQL queries**

  - Validate the list of queries and throw out invalid queries.
  - Extract all tables and columns from the queries and present them for review before adding to the semantic view.
  - Extract relationships from the queries.
  - Add valid queries to the semantic view as verified queries.
- **Table metadata**

  - Extract all table and column descriptions.
  - Add primary and unique keys to the semantic view by analyzing metadata or counting distinct values to determine
    cardinality and relationship types.
- **Query history**

  - Surface historical SQL queries as suggestions to the semantic view. The generator identifies the most common types of
    queries that fit within the bounds of the selected tables and columns.
  - Find valid relationships and column types for the semantic view.
  - Cortex Analyst uses the query history accessible by the role used to create the semantic view to generate both
    relationships and verified query suggestions.

To create a semantic view with the generator:

1. [Open Semantic View Autopilot](#label-semantic-view-autopilot-entry-point).
2. Select a location to store the semantic view after creation.
3. Enter a name for the semantic view.
4. For **Description**, specify information about the semantic view. Use clear business terminology to help the AI
   understand the view’s purpose.
5. Select **Next**.
6. To provide context, add the following information:

   - For **SQL Queries**, provide example questions and their respective SQL queries that you want to use as part of the
     view.

   You can also provide context by uploading a Tableau file, a Power BI file, or a YAML specification. For details on
   each option, see [Options for providing context](#label-semantic-view-autopilot-options-for-providing-context).
   To import a model from a Horizon Catalog connector instead, see
   [Create a semantic view from a Horizon Catalog connector](#label-semantic-view-autopilot-connected-bi).
7. For **Select tables**, provide the data source that you’re using to create the semantic view.
   You must provide at least one table or view. For your first semantic view, Snowflake recommends using fewer than 10
   tables or views to keep it easy to understand and use. This is not a hard limit.
8. Select **Next**.
9. For **Select columns**, select the columns that you’re using to create the semantic view.

You can select all the columns or specific columns. For performance reasons, Snowflake recommends not using more than 50
columns.

10. Select whether you want to add sample values from each column to the semantic view. Sample values help improve the
    accuracy of Cortex Analyst’s results.
11. Select whether you want to add AI-generated descriptions for tables and columns to the semantic view. The AI-generated
    descriptions are based on the column names and sample values.
12. Select **Create and save**, and then select **Save and run**.
    You can view the progress of the view generation, including details about the steps that the view generator is taking,
    on the semantic view page. The process can take a few minutes.
13. Optional: To make additional modifications, refine the view in
    [Semantic Studio](/user-guide/views-semantic/semantic-studio), or edit the YAML file directly.

Cortex Analyst automatically generates suggestions to improve the semantic view after creation. After the suggestions
appear, which might take several minutes, you can review them and apply them to the view as needed.

### Create a semantic view from a Horizon Catalog connector

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts in AWS deployments.

If you have a [Horizon Catalog connector](/user-guide/snowflake-horizon/connectors) for a BI tool, you can create a
semantic view directly from one of the models that the connector ingests. You don’t export or upload a file, and you
don’t select tables and columns, because Autopilot reads the model’s tables, relationships, and measures from Horizon
Catalog. Before you start, check the
[prerequisites for importing from a Horizon Catalog connector](#label-semantic-view-autopilot-prerequisites).

You can start an import from Semantic View Autopilot or from Horizon Catalog.

#### Start from Semantic View Autopilot

1. [Open Semantic View Autopilot](#label-semantic-view-autopilot-entry-point).
2. Select your BI tool.
3. On the **Import from connected** tab, which is selected by default, select the model to import. To upload a file
   instead, select **Upload file**. The list contains the models from every connector for that tool that your role can
   see, and you can search it by name. Select a model to see its details, such as its project and when
   it was last updated.

   By default, the list shows only models that Autopilot can import. A model can’t be imported if none of its tables
   reads from a single Snowflake table. To see those models too, clear **Only show importable models**. Models that can’t
   be imported are marked **No Snowflake source** and can’t be selected.
4. Select **Next**.
5. On **Name your semantic view**, select a location to store the semantic view. The name is filled in from the model;
   change it if needed.
6. Complete the last step of the wizard to generate the semantic view. Generation can take a few minutes.

#### Start from Horizon Catalog

To open Semantic View Autopilot from Horizon Catalog with a connector or model already selected, do one of the
following:

- In the navigation menu, select **Catalog** » **Connections**. In the **Metadata connections** list, for a connector
  that has completed a full ingestion, select **Import with Cortex**. Autopilot opens with only
  that connector’s models listed.
- On the page for a model in Horizon Catalog, or on its node in a lineage graph, select **Create semantic view**. Autopilot opens with that model selected. **Create semantic view** is
  disabled for a model that has no lineage to Snowflake tables.

Then finish the import as described in [Start from Semantic View Autopilot](#label-semantic-view-autopilot-connected-bi-from-autopilot).

#### How models are converted

Autopilot converts a model from a Horizon Catalog connector with similar rules to an uploaded file. For the supported BI
tools, what is converted, and how an import from a connector differs, see
[Tableau](/user-guide/views-semantic/tableau-ingestion#label-tableau-ingestion-connected) and
[Power BI](/user-guide/views-semantic/power-bi-ingestion#label-power-bi-ingestion-connected).

### Using CoCo to create a semantic view

The wizard offers several options to get started, and Snowflake recommends CoCo, which guides you through creating the
view conversationally.

1. [Open Semantic View Autopilot](#label-semantic-view-autopilot-entry-point).
2. When the wizard offers the available options, choose CoCo.
3. Describe your data in natural language:
   - `Create a semantic view using the tables in ANALYTICS.SALES`
   - `I need a semantic view for customer support. We track ticket volume, resolution time, and CSAT.`
4. CoCo generates a YAML file with tables, relationships, and metrics.
5. Ask for changes. Each one appears as an inline diff that you can accept or reject:
   - `Add a profit margin metric`
   - `The join between ORDERS and RETURNS should use return_order_id`
   - `Rename DEMO to DEMOGRAPHICS everywhere`

**Example conversation:**

> **You:** Create a semantic view using the tables in ANALYTICS.SALES
>
> **CoCo:** I found 4 tables. I’ve created a semantic view with 5 relationships and 3 metrics: total\_revenue, total\_orders, average\_order\_value. Take a look and let me know what to change.
>
> **You:** The join between ORDERS and RETURNS should be on return\_order\_id. Also add a return rate metric.
>
> **CoCo:** Done. Here’s the diff: [inline diff in editor]

### Options for providing context

Providing context is optional, but it improves the quality of the semantic view. Without it, the
generator only uses the database schema information, which might lack business nuance. Snowflake supports the following
options for providing context:

#### Option 1: Upload Tableau file

Semantic View Autopilot supports using a file from Tableau to automatically generate a semantic view. This lets you
migrate your existing business logic and metadata directly into Snowflake. Autopilot supports the `TWB`, `TWBX`, `TDS`,
and `TDSX` formats, and extracts tables, columns, relationships, calculated fields, parameters, filters, and Custom SQL.
The tables in the file must resolve to a direct Snowflake connection.

For supported formats, file size, how to export a file from Tableau, how published data sources work, and the full
list of supported features, see [Tableau ingestion feature support](/user-guide/views-semantic/tableau-ingestion).

If you have a Horizon Catalog connector for Tableau, you can import a data source without exporting a file. See
[Create a semantic view from a Horizon Catalog connector](#label-semantic-view-autopilot-connected-bi).

#### Option 2: Upload Power BI file

Semantic View Autopilot supports using a Power BI file to automatically generate a semantic view. This lets you migrate
your existing DAX measures, table relationships, and column definitions directly into Snowflake. Autopilot supports the
`.pbit` and `.pbix` formats.

For supported formats, file size, how to export from Power BI Desktop, and detailed feature support, see
[Power BI ingestion feature support](/user-guide/views-semantic/power-bi-ingestion).

If you have a Horizon Catalog connector for Power BI, you can import a semantic model without exporting a file.
See [Create a semantic view from a Horizon Catalog connector](#label-semantic-view-autopilot-connected-bi).

#### Option 3: Provide SQL queries

You can add example natural language questions and their corresponding SQL queries. This helps the model learn your specific business logic and create relationships.

Snowflake uses these queries to pre-select tables and columns in later steps, and adds them to the semantic view as verified queries. Snowflake also adds any relationships that it can infer from the queries.

To provide queries as a file, use `.csv` format with two columns: a natural language question and its corresponding SQL query.

#### Option 4: Upload a YAML specification

If you already maintain a [YAML specification](/user-guide/views-semantic/semantic-view-yaml-spec), or a legacy semantic
model YAML file, you can upload it in the wizard instead of describing your data. Select the YAML file to upload, and
Autopilot converts the specification into a semantic view that you can then refine.

If you are creating the semantic view from a stage, first
[create a stage](/user-guide/data-load-local-file-system-stage-ui) for the YAML file. Under **Select database, schema and
stage**, select the database, schema, and stage where you want to upload the YAML file. If you want the YAML file
uploaded to a specific path in the stage, specify that path.

## After you create a semantic view

### Refine the view

Add or change logical tables, facts, dimensions, metrics, and relationships in
[Semantic Studio](/user-guide/views-semantic/semantic-studio).

### Grant access to the view

See [Grant access to a semantic view](/user-guide/views-semantic/semantic-studio#label-semantic-studio-sharing).

### Query the view

If you are viewing a semantic view in the Horizon Catalog Explorer, you can open a worksheet to construct a query for
that view by selecting [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Query with SQL**. For information on how to construct the query, see
[Querying semantic views](/user-guide/views-semantic/querying).

## Troubleshooting

- If your semantic view is not listed in the list of views, refresh the list of models (not the page itself).
- If no models are listed when you import from a Horizon Catalog connector, check that the connector has completed a full ingestion and that your role has `READ EXTERNAL METADATA` or `USAGE` on it. To
  continue without a connector, select **Upload file**.
- If a model is marked **No Snowflake source**, none of its tables reads from a single Snowflake table, so it
  can’t be imported. Check that the model connects to Snowflake directly.
- If errors occur with the relationships in the semantic view, ensure that these relationships match the actual data structure.
- If queries are slow, reduce the number of tables or columns.
- If Cortex Analyst produces unexpected results when using your semantic view, review the facts, dimensions, and metrics in the
  semantic view.

## Best practices

For comprehensive guidance on designing high-quality semantic views, including scoping, writing effective descriptions,
defining relationships and metrics, and improving accuracy with verified queries, custom instructions, and Cortex Search,
see [Best practices for modeling semantic views](/user-guide/views-semantic/best-practices-modeling).
