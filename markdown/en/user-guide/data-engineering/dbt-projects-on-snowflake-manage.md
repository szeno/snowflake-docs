# View and manage dbt project objects

This topic covers how to explore the structure and metadata of an existing dbt project object. This includes viewing the project’s DAG,
inspecting model and source details, and executing dbt project objects.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

## Explore the dbt project object details page

The dbt project object details page in Snowsight is your primary place to explore and manage a deployed dbt project object. It always reflects the currently deployed version of your project, so there’s no generated site to maintain. From this page, you can access:

- A full, interactive project DAG with search and depth controls.
- Model, source, test, snapshot, and macro details, including compiled SQL and configuration.
- Column-level lineage powered by Snowflake Horizon Catalog.
- A Markdown-rendered project overview for projects that define an overview docs block. For more information, see [Maintain a project overview](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-project-overview-docs-block).
- One-off and partial DAG execution of the deployed dbt project object.
- Schedule management, including viewing and creating schedules.
- [Run history](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability) with logs, tracing, and downloadable build artifacts for each individual run.

The deployed dbt project object and its artifact files are part of the Snowflake Horizon Catalog. This means you can query them directly, or ask CoCo to inspect them when generating documentation, debugging a failure, or answering questions about your pipeline.

You can open the project details page in Snowsight in the following ways:

- **dbt Projects on Snowflake home page**: In the navigation menu, select **Transformations** » **dbt Projects**, then select a deployed dbt project object from the list.
- **Object Explorer**: In the navigation menu, select **Databases** » your database » your schema » **dbt Projects**, then select your project.
- **Workspace editor**: With a project open, select **Connect** » **View project**. For more information, see [Workspaces for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces).

## Browse the project DAG to see model lineage and dependencies

The Directed Acyclic Graph (DAG) shows how dbt models depend on each other, visualizing data lineage so you can:

- Verify where a model is built (database.schema), how it materializes, and which upstream and downstream dependencies it has.
- Spot and improve inefficient model designs to support better performance and scalability.

To browse the project DAG in Snowsight, navigate to **Databases** » your database » your schema »
**dbt Projects** and select your project. The project details page displays the **Graph** of your models and their
relationships, along with a **Description** of your project, the **dbt Project definition**, and **Privileges**.

In the **Graph**, click a model node to inspect model, source, or test details (such as compiled SQL and configuration) directly from the DAG.

### DAG node legend

The following table describes each node type in the DAG:

| Node type | Description |
| --- | --- |
| **Model** | A SQL or Python file in your `models/` directory that defines a table or view. This is the most common node type. |
| **Source** | An external table or view declared in a `sources:` block in your YAML files. Sources are inputs to your models, not built by dbt. |
| **Seed** | A CSV file in your `seeds/` directory that dbt loads as a table. |
| **Test** | A data quality check (singular or generic) defined in your project. Test nodes are connected to the models they validate in the DAG. |
| **Snapshot** | A dbt snapshot that captures slowly changing dimension data over time. Defined in your `snapshots/` directory. |

Expand

Show lessSee more

### Search the DAG

Use the search bar in the DAG to find a model by name. Selecting a model will anchor that model as the focal point of the graph. To change the anchor
node, use the search bar to search for a different model.

### Control DAG depth

Use the upstream and downstream depth controls to change how many levels of the graph are visible relative to the anchor node. When you
first anchor a model, the DAG defaults to showing 2 levels upstream and 2 levels downstream. Depth settings carry over when you
anchor a different model.

The DAG displays up to 300 models at a time. If your project has more models, use search and depth controls to navigate to the part
of the graph you need.

### Inspect model details from the DAG

When you select a model node in the DAG, a side panel opens, showing:

- The model’s type, file path, and a link to the target object in the database.
- The row count and column count, with a list of column names.
- A description of the model (if one is defined in the dbt project).
- Model lineage, listing upstream and downstream dependencies with links to navigate between them.
- The source and compiled SQL for the model.

On the **Graph** tab of the project details page, select **View in Details** in the side panel to open the complete model
details in the object details page. From the model details view, select **Show in graph** to return to the **Graph** tab with that model anchored as the focal point.

Tip

The query history DAG and the workspace DAG share the same search, depth controls, and column-level lineage described on this
page, and additionally inject runtime data (start time, end time, duration) from `manifest.json` and `run_results.json`
into each model’s side panel. For more information, see
[Monitor dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability) and
[Workspaces for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces).

#### View column-level lineage

Each model node in the DAG supports column-level lineage powered by Snowflake Horizon Catalog. Select **Show columns** on any model
node to expand its column list. Selecting a column highlights all upstream and downstream models in the DAG that use that column, so
you can trace how data flows through your pipeline.

Note

The project must be run at least once before column-level lineage is available. For more information, see
[Limitations for column-level lineage](/user-guide/data-engineering/dbt-projects-on-snowflake-limitations#label-dbt-limitations-column-lineage).

### Execute models from the DAG

You can execute a subset of your dbt project object directly from the DAG by selecting the **…** menu on a model node. The
following execution options are available:

| Menu option | What it executes | Equivalent `--select` flag |
| --- | --- | --- |
| **Execute model** | Only the selected model | `--select model_name` |
| **Execute model+** | The model and all downstream dependents | `--select model_name+` |
| **Execute +model** | The model and all upstream parents | `--select +model_name` |
| **Execute +model+** | The model, its parents, and its children | `--select +model_name+` |

Expand

Show lessSee more

Selecting any option opens the **Execute dbt project** dialog with the **Additional flags** field pre-filled with the corresponding
`--select` value. From the dialog, you can:

- Choose the operation, such as **Run**, **Test**, or **Build**.
- Choose the profile target (for example, **dev** or **prod**).
- Edit the flags before executing if you want to refine the selection.

You can use the same `--select` syntax with the `+` graph operators in SQL and the Snowflake CLI:

Copy code

```
EXECUTE DBT PROJECT my_dbt_project
  ARGS = 'build --select +stg_customers+ --target dev';
```

For more information about supported dbt commands and flags, see [Supported dbt commands and flags](/user-guide/data-engineering/dbt-projects-on-snowflake-supported-commands).

## View dbt project object properties

View the metadata Snowflake stores about a dbt project object to see what it’s called, who owns it, and where the files in its mutable
`live` version are stored in Snowflake’s internal `snow://dbt/...` stage.

To view the properties (such as name, owner, comment) of a specific dbt project object, use the DESCRIBE DBT PROJECT command, as shown in the
following example:

Copy code

```
DESCRIBE DBT PROJECT my_dbt_project;
```

The output shows the object’s name, owner, comment, live version metadata, and external access integration. For more information, see
[DESCRIBE DBT PROJECT](/sql-reference/sql/desc-dbt-project).

### View all dbt projects

Use SHOW DBT PROJECTS when you want to see all dbt project objects you can access, plus key metadata.

Copy code

```
SHOW DBT PROJECTS IN DATABASE mydb;
```

The output shows each object’s database, schema, owner, comment, when it was created and last updated, live version metadata, default
environment, and external access integration. For more information, see [SHOW DBT PROJECTS](/sql-reference/sql/show-dbt-projects).

Alternatively, use the [snow dbt list](/developer-guide/snowflake-cli/command-reference/dbt-commands/list) command. For more information, see
[Listing all available dbt project objects](/developer-guide/snowflake-cli/data-pipelines/dbt-projects#label-snowcli-snow-dbt-list).

## Access dbt project documentation and artifacts

Instead of generating and hosting classic `dbt docs`, we recommend using the dbt project object details page in Snowsight as your primary documentation experience. It provides virtually everything `dbt docs` offers, and more. For everything you can do from this page, see [Explore the dbt project object details page](#label-dbt-project-details-page).

If you still need the static docs site, use one of the following options.

### Option 1: Download artifacts from a deployed dbt project object

Run `dbt docs generate --static` on a deployed dbt project object with `EXECUTE DBT PROJECT` or by choosing the **docs generate** operation
in Snowsight. The `WRITEBACK` setting controls whether an execution writes its generated target and log artifacts to the live
version. The following example generates the static site and writes it to the live version:

Copy code

```
EXECUTE DBT PROJECT my_db.my_schema.my_dbt_project
  ARGS = 'docs generate --static'
  WRITEBACK = TRUE;
```

After the execution completes, you can download the generated artifacts in the following ways:

- To download the artifacts written to the live version, open the dbt project object details page from **Databases** » your database
  » your schema » **dbt Projects** » your project, then use the project page to download the artifacts from the live version.
- To download the artifacts for that individual execution, open the execution under **Run History** or **Query History** »
  **Query Details**, then select **Download Build Artifacts** under **dbt Output**. Snowflake stores these per-query result artifacts and
  their archive regardless of the `WRITEBACK` setting.
- To download per-query artifacts programmatically, use the `SYSTEM$LOCATE_DBT_ARTIFACTS` function to locate the files, then fetch them with
  `GET` or `COPY FILES`.

For the full steps and examples, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).

### Option 2: Generate a static docs site in a workspace

If you want the classic single-file `dbt docs` site, run `dbt docs generate --static` from a workspace. This produces a self-contained
`target/static_index.html` file that bundles the documentation site so you can view it without hosting anything. Download
`target/static_index.html` from the workspace to your local machine, then open it in a browser.

Note

dbt Projects on Snowflake don’t support `dbt docs serve`. Use the project details page in Snowsight for an interactive experience, or generate
`target/static_index.html` with `dbt docs generate --static`.
