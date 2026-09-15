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
- If your Tableau file contains Custom SQL, you must also have the CREATE VIEW privilege on the schema because the SQL is
  parsed into a regular Snowflake view.

You can also upload a Power BI file (.pbit or .pbix) to automatically generate a semantic view. In addition to the
preceding prerequisites, the Power BI ingestion feature requires:

- A stage where you have write permissions.
- Read access to the underlying tables and columns that your Power BI file references.

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

While providing context is optional, it’s extremely useful in creating a high-quality semantic view. Without it, the
generator only uses the database schema information, which might lack business nuance. Snowflake supports the following
options for providing context:

#### Option 1: Upload Tableau file

Semantic View Autopilot supports using a file from Tableau to automatically generate a semantic view. This lets you
migrate your existing business logic and metadata directly into Snowflake. Autopilot supports the `TWB`, `TWBX`, `TDS`,
and `TDSX` formats, and extracts tables, columns, relationships, calculated fields, parameters, filters, and Custom SQL.
The tables in the file must resolve to a direct Snowflake connection.

For supported formats, file constraints, how to export from Tableau Desktop or Tableau Online, how published data
sources work, and the full list of extracted metadata, see [Tableau ingestion feature support](/user-guide/views-semantic/tableau-ingestion).

#### Option 2: Upload Power BI file

Semantic View Autopilot supports using a Power BI file to automatically generate a semantic view. This lets you migrate
your existing DAX measures, table relationships, and column definitions directly into Snowflake. Autopilot supports the
`.pbit` and `.pbix` formats.

For supported formats, file constraints, how to export from Power BI Desktop, and detailed feature support, see
[Power BI ingestion feature support](/user-guide/views-semantic/power-bi-ingestion).

#### Option 3: Provide SQL queries

You can add example natural language questions and their corresponding SQL queries. This helps the model learn your specific business logic and create relationships.

Snowflake uses these queries to pre-select tables and columns in subsequent steps, and will also auto-add these queries as “verified queries” in the semantic view. Additionally, if valid relationships can be inferred, these will get added to the semantic view.

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

If you are viewing a semantic view in the database object explorer, you can open a worksheet to construct a query for
that view by selecting [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Query with SQL**. For information on how to construct the query, see
[Querying semantic views](/user-guide/views-semantic/querying).

## Troubleshooting

- If your semantic view is not listed in the list of views, refresh the list of models (not the page itself).
- If errors occur with the relationships in the semantic view, ensure that these relationships match the actual data structure.
- If queries are slow, reduce the number of tables or columns.
- If Cortex Analyst produces unexpected results when using your semantic view, review the facts, dimensions, and metrics in the
  semantic view.

## Best practices

For comprehensive guidance on designing high-quality semantic views, including scoping, writing effective descriptions,
defining relationships and metrics, and improving accuracy with verified queries, custom instructions, and Cortex Search,
see [Best practices for modeling semantic views](/user-guide/views-semantic/best-practices-modeling).
