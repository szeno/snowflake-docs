# Creating semantic views

You can create a [semantic view](/user-guide/views-semantic/overview) in Snowsight with Semantic View
Autopilot, by writing code (SQL or YAML), or by importing a model you already maintain. Use this page to choose an
approach; each option links to detailed instructions.

## Create with Semantic View Autopilot

Semantic View Autopilot is the AI-assisted creation wizard in Snowsight. You reach it from Semantic Studio: in
**Workspaces**, select **Add new** » **Semantic View**. The wizard offers several options to get started, and
Snowflake recommends CoCo, which guides you through creating the view conversationally. See
[Semantic View Autopilot](/user-guide/views-semantic/autopilot).

You can also seed the view from a file or from example queries:

- Import a Tableau workbook or data source. See [Tableau ingestion feature support](/user-guide/views-semantic/tableau-ingestion).
- Import a Power BI semantic model. See [Power BI ingestion feature support](/user-guide/views-semantic/power-bi-ingestion).
- Upload a YAML specification, or provide example SQL queries. See
  [Options for providing context](/user-guide/views-semantic/autopilot#label-semantic-view-autopilot-options-for-providing-context).

After the view exists, refine and deploy it in [Semantic Studio](/user-guide/views-semantic/semantic-studio).

## Create with code

Define semantic views as code for version control and automated deployment:

- Use DDL (SQL). See [Using SQL commands to create and manage semantic views](/user-guide/views-semantic/sql).
- Use YAML. See [YAML specification for semantic views](/user-guide/views-semantic/semantic-view-yaml-spec).
- Decide which to use. See [YAML vs DDL authoring for semantic views](/user-guide/views-semantic/yaml-vs-ddl).

## Migrate an existing model

Move from the legacy stage-based semantic models to native semantic views. See
[Migrating from the legacy stage API to semantic views](/user-guide/views-semantic/semantic-models-vs-views).
