# Semantic Studio

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Semantic Studio is the authoring environment for [semantic views](/user-guide/views-semantic/overview) inside Workspaces.
You define a semantic view as a YAML file and deploy it to a live Snowflake object, with Snowflake CoCo, an AI-driven
intelligent agent, available directly in the editing workflow. You can create, refine, and debug a semantic view through
conversation instead of configuring each element by hand.

Because Semantic Studio runs inside Workspaces, you get the same file-based workflow you use for SQL files and notebooks,
including optional Git integration. Monitoring dashboards are reachable anytime through a direct link from Semantic Studio.

To author Cortex Agents alongside semantic views, see [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage).

## Prerequisites

### Workspaces in Snowsight

Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) and confirm that you can access **Workspaces** from the navigation menu.

### Existing data to work with

Have one of the following ready:

- **Tables** that you want to build a semantic view from. You need read access to them.
- **An existing semantic view** that you want to refine or debug.

### Required privileges

To create a semantic view, you must use a role with the following privileges:

- CREATE SEMANTIC VIEW on the schema where you are creating the semantic view.
- USAGE on the database and schema where you are creating the semantic view.
- SELECT on the tables and views used in the semantic view.

You also need at least one supported large language model (LLM) available in your account. To check, run the following
command:

Copy code

```
SHOW MODELS LIKE 'claude-4-sonnet' IN SNOWFLAKE.MODELS;
```

If that returns no results, check for `claude-3-7-sonnet`, `mistral-large2`, or `openai-gpt-4.1`. At least one must be
available.

## Open a semantic view

You can open an existing semantic view in either of these ways:

- **Ask CoCo.** Name the view you want to work on, and CoCo opens it for you.
- **Use the semantic view list.** In Snowsight, select **AI & ML** » **Cortex Analyst** to list the semantic
  views that you have access to, then select the one you want to open.

The view opens as a YAML file in the editor, and the workspace file explorer shows your semantic view (`.sv.yaml`) and
project files.

Note

A `cortex-project.yaml` file appears automatically in your workspace. This is a project manifest that tracks which files
belong to the project and where they deploy to (target database and schema). You can ignore this file. It is auto-managed
by Semantic Studio and CoCo.

## Create a semantic view

To create a new semantic view, select **Add new** » **Semantic View**. This opens the Semantic View Autopilot wizard,
which generates the view for you. The wizard offers several options to get started, and Snowflake recommends CoCo, which
guides you through creating the view conversationally. You can also provide SQL queries, or upload a Tableau file, a
Power BI file, or a YAML specification.

For the full creation walkthrough, see [Semantic View Autopilot](/user-guide/views-semantic/autopilot).

Once the view exists, use the rest of this page to refine it.

Note

Editing a semantic view effectively replaces the existing view. To replace an existing semantic view, you must use a role
that has been granted the following privileges:

- CREATE SEMANTIC VIEW on the schema where you are creating the semantic view.
- USAGE on the database and schema where you are creating the semantic view.
- SELECT on the tables and views used in the semantic view.

## Set the name and description

The semantic view name and description help users discover and understand the purpose of the view. Both are top-level
fields in the YAML file, and you can ask CoCo to set them.

Note

If you use this semantic view as a tool in [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents), the view name is
used as the tool name, which must be between 1 and 64 characters.

Tip

Write clear, detailed descriptions that explain:

- What business questions this view can answer
- What data sources it includes
- Who should use this view

Example: “Revenue analysis across products and customers, including year-over-year trends. Use this view to analyze
sales performance by region, product category, and customer segment.”

To modify the name or description with the form:

1. Select **Edit** next to the name of the semantic view.
2. Make changes to the name or description.
3. Select **Apply**.

## Define logical tables

Logical tables represent business entities (such as customers, orders, or products) and map to physical database tables
or views. Each semantic view contains one or more logical tables.

For each logical table, define the following:

- **Name**: The business-friendly name for this table.
- **Description**: An explanation of what this table represents.
- **Synonyms**: Alternative names that users might use for this entity.
- **Primary key**: The columns that uniquely identify rows.

Ask CoCo to add a logical table from a physical table, and it generates the dimensions and facts for the columns you
name. For example: `Add ANALYTICS.SALES.CUSTOMERS as a logical table and set the primary key to customer_id`.

To add a logical table with the form:

1. Select **+ Logical Table**.
2. In the **Select a table** step in the wizard:

   1. Select the table or view that contains the data that you want to use in your semantic view.
   2. Select **Next**.
3. In the **Select columns** step in the wizard:

   1. Select the columns to include in the view.

      To select all columns in a table or view, select the table or view.
   2. Select **Generate logical table**.

To change the name, description, synonyms, or primary key of an existing logical table:

1. Select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Edit Logical Table** next to the logical table name.
2. Make your changes to the name, description, synonyms, and primary key.

   If you have not specified the description or synonyms, you can select **Generate fields** to fill in these fields
   automatically.
3. Select **Save**.

To define a logical table from a SQL query instead of a physical table, see [Using an SQL query as a logical table in a semantic view](/user-guide/views-semantic/inline-view).

## Define facts, dimensions, and metrics

Within each logical table, you define the business concepts that users can query:

- **Dimensions**: Categorical attributes that provide context, such as customer name, product category, or order date.
- **Facts**: Row-level quantitative data, such as sale amount, quantity, or unit price.
- **Metrics**: Aggregated measures calculated with functions like SUM, AVG, or COUNT, such as total revenue or average
  order value.

Each one needs a name, a SQL expression, and a data type. For a full description of these elements and how they relate,
see [Overview of semantic views](/user-guide/views-semantic/overview) and [YAML specification for semantic views](/user-guide/views-semantic/semantic-view-yaml-spec).

The following capabilities are also available:

- **Derived metrics**: View-level metrics that combine metrics from multiple tables. For more information, see
  [Defining derived metrics](/user-guide/views-semantic/sql#label-semantic-views-create-derived-metrics).
- **Private access modifiers**: Mark facts or metrics as private to hide them from queries while still using them in
  other calculations. For more information, see [Marking a fact or metric as private](/user-guide/views-semantic/sql#label-semantic-views-private).
- **Preferred join paths for metrics**: If there are
  [multiple relationship paths between two logical tables](/user-guide/views-semantic/sql#label-semantic-views-create-logical-tables-relations),
  you can choose which relationship a metric uses.

To define reusable named filters, see [Defining filters for logical tables in a semantic view](/user-guide/views-semantic/filters). To parameterize logic, see
[Using variables in a semantic view](/user-guide/views-semantic/variables).

To add a fact, dimension, or metric with the form:

1. Select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png), and select **Fact**, **Dimension**, or **Metric**.
2. Enter information about the new fact, dimension, or metric, and select **Add**.

To modify or remove a fact, dimension, or metric:

1. Select **Facts**, **Dimensions**, or **Metrics** to display the list of facts, dimensions, or metrics.
2. For the fact, dimension, or metric that you want to change:
   - Select **Edit** to modify the item.
   - Select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Remove fact**, **Remove dimension**, or **Remove metric** to remove the item.

## Define relationships

Relationships define how logical tables join together, enabling queries that span multiple tables. Each relationship
defines which columns in one table reference columns in another table:

- A **name** for the relationship, for example `orders_to_customers`.
- The **left table** (the table with the foreign key) and its join columns.
- The **right table** (the table being referenced) and its join columns.

Note

For semantic views, you typically don’t need to specify join types (left outer, inner) or relationship types
(one-to-one, many-to-one). These are automatically inferred from the data and primary key definitions at query time.

For the structural and semantic rules that a semantic view must satisfy, see
[How Snowflake validates semantic views](/user-guide/views-semantic/validation-rules).

To add a relationship with the form:

1. Select **+ Relationship**.
2. Enter a name for the relationship, select the tables in the relationship, and select the columns to use to join the
   tables.
3. Select **Add**.

After you finish making changes, select **Save**.

## Improve accuracy

To improve the accuracy and reliability of the answers that Cortex Agents generates, add context and guidance to the
semantic view.

### Verified queries

Add sample queries to the **Verified Queries** section:

- These are example queries that help Cortex Agents understand how to use the semantic view.
- Add queries that represent common use cases for your data.

For details, see [Cortex Analyst Verified Query Repository](/user-guide/views-semantic/verified-query-repository). To review and accept suggested verified queries
based on real usage, see [Suggestions for semantic models and views](/user-guide/views-semantic/verified-query-suggestions).

### Synonyms

Add synonyms for your tables, facts, dimensions, or metrics:

- These are alternative terms that users might use in queries.
- Synonyms help Cortex Agents correctly interpret user questions. For example, users might refer to “customers” as
  “clients” or “accounts.”

Note

Add synonyms manually rather than auto-generating them with AI. Focus on domain-specific alternatives like internal
terminology, abbreviations, or legacy names. Auto-generated synonyms often reduce semantic view quality.

### Custom instructions

Add custom instructions to steer SQL generation and question handling with natural-language guidance:

- These provide additional context about how the data should be interpreted.
- Include business rules or constraints that should be considered.

For details, see [Custom instructions in Cortex Analyst](/user-guide/views-semantic/custom-instructions).

For broader modeling guidance, see [Best practices for modeling semantic views](/user-guide/views-semantic/best-practices-modeling).

## Deploy

Deploy pushes your local YAML file directly to the live Snowflake object. This action does not use Git; deploying and
committing to Git are separate actions.

1. Select **Deploy** in the top bar.
2. Select your deploy target.
3. Review the diff preview, which shows what changed between your local file and the live object.
4. Confirm to deploy.

Note

Deploy does not know whether your local file is ahead of or behind the live object. If someone else updated the live
object since you last opened it, your deploy will overwrite their changes. Coordinate with your team before deploying, or
use Git workflows to manage changes.

## Version control with Git

Because Semantic Studio runs inside Workspaces, you can connect your workspace to a Git repository. This gives you
branch-based workflows, commit history, and the ability to review changes before they reach production, the same patterns
you’d use for SQL files or notebooks.

To set up a Git-connected workspace:

1. In the **Workspaces** menu, select **From Git repository**.
2. Paste your repository URL (for example, `https://github.com/my-org/my-repo`).
3. Select an API integration and authentication method (OAuth, personal access token, or public repo).

Once connected, you can create branches, pull changes, commit and push updates, and resolve conflicts directly in
Workspaces. Your semantic view YAML files are versioned alongside everything else in the repo.

For full setup instructions, see [Integrate workspaces with a Git repository](/user-guide/ui-snowsight/workspaces-git).

Note

Git integration is optional. Semantic Studio works in a local (non-Git) workspace; you can always add Git later.

For guidance on managing semantic views as part of a data engineering pipeline, including automated (CI/CD) deployment,
see [Best practices for developing and deploying semantic views](/user-guide/views-semantic/best-practices-dev).

## Debug a failing request

1. In the agent’s monitoring tab, find a request that returned incorrect results and copy its request ID.
2. In Semantic Studio, paste the request ID to CoCo:
   `This request returned the wrong revenue number. The correct answer is $12M.`
3. Review the explanation. CoCo traces the request through the pipeline (routing, tool selection, and SQL generation) and
   reports what went wrong.
4. Review the proposed fix, which appears as an inline diff, and accept it.

To monitor the requests that use your semantic view, see [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor).

## Grant access to a semantic view

To allow other users or roles to use your semantic view, grant them the appropriate privileges. Semantic views support
the standard Snowflake privilege model:

- **SELECT**: Required to query the semantic view and view its contents.
- **REFERENCES**: Required to use the semantic view with Cortex Agents and see its structure.
- **OWNERSHIP**: Full control over the semantic view.

To grant another role the privileges to view and query a semantic view:

1. Select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Share**.
2. Select the role that should be granted the privileges to view and query the semantic view.
3. Select **Done**.

This grants the SELECT and REFERENCES privileges on the semantic view to the selected role.

For more information about granting privileges on semantic views, including future grants and more complex scenarios,
see [Granting privileges on semantic views](/user-guide/views-semantic/sql#label-semantic-views-privileges).

To share a semantic view with other accounts, see [Sharing semantic views](/user-guide/views-semantic/sharing-semantic-views).

## Limitations

- **File ingestion.** To build a semantic view from a Tableau or Power BI model, use
  [Semantic View Autopilot](/user-guide/views-semantic/autopilot).
- **Monitoring and evaluation panels.** Semantic Studio links out to the monitoring dashboards rather than embedding
  them.
- **Stale-file detection.** Deploy overwrites the live object without checking whether it changed since you last opened
  it.
- **Multi-file editing.** CoCo works within the open file and does not navigate across semantic view and agent files.
