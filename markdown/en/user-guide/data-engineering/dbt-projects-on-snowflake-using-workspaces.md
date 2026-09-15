# Workspaces for dbt Projects on Snowflake

Workspaces in Snowsight offer a web-based integrated development environment (IDE) for dbt projects that can connect and sync to a Git repository. Each workspace for dbt Projects on Snowflake can represent a single dbt project or multiple dbt projects, depending on how you organize your files and folders.

You can use a workspace for dbt Projects on Snowflake to visualize, test, and run dbt projects directly in Snowflake, including viewing column-level lineage powered by Horizon Catalog on models materialized in your dev schema. Workspaces provide a quick way to start a new dbt project via templates, connecting to an existing Git repository, or directly importing a deployed dbt project object into your workspace.

Workspaces also provide a unified editor for you to create, organize, and manage code across multiple file types and projects within Snowflake. For more information, see [Workspaces](/user-guide/ui-snowsight/workspaces).

If your project defines an `env.yml` file, Workspaces resolves it before each run and injects the environment variables into the run. Choose the active environment with the environment selector in the run panel, and override individual variables for a single run. For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

## Configure and run dbt models from the editor

You can run your complete dbt project or an individual model directly from the workspace editor.

Snowflake uses the `model-paths` setting in your `dbt_project.yml` file to identify which files are models. If `model-paths` isn’t set, Snowflake falls back to the default `/models` directory. Setting `model-paths` explicitly ensures Snowflake treats the files you intend as models.

### Run a single model

To run an individual model, open its `.sql` file and select the play button, or press `Cmd+Enter` (Mac) or `Ctrl+Enter` (Windows/Linux). For files under `model-paths` (or the `/models` fallback), Snowflake runs `dbt run --select <model_name>` instead of running the file as raw SQL. This compiles the model and propagates the changes to the `target` folder, so you can iterate on a model and review the compiled output without running the entire project.

This behavior is distinct from compiled SQL files. When you run a file that dbt has already compiled (for example, a file in the `target` folder), Snowflake runs it as raw SQL.

### Defer to production during development

Use native defer to production to run selected models in your workspace while resolving references to unbuilt upstream models from a production dbt project object.

To defer to production:

1. In the execution pane, select **Advanced options**.
2. Enable **Defer to Production**.
3. Select the database and schema that contain the production dbt project object, and then select the object.

   A dbt project object appears only if you have the `MONITOR` privilege on it.
   The object must also have at least one qualifying execution within the previous 7 days.
4. Select the target artifacts to use as state:

   - **Last Successful Run** (default)
   - **Last Failed Run Target**
   - **Last Run Target**
5. Add `--select state:modified+` to the dbt arguments to process changed nodes and their downstream dependencies.
6. Run the dbt command.

Workspaces imports the selected target artifacts under `./imports/state` and automatically adds `--defer` and `--state ./imports/state` to the command. The selected option determines which recent-run system function Workspaces uses. For example, with **Last Successful Run** selected, the generated SQL can resemble the following:

Copy code

```
EXECUTE DBT PROJECT FROM WORKSPACE "USER$"."PUBLIC"."my_dbt_projects"
  ARGS = 'run --defer --state ./imports/state --select state:modified+'
  IMPORTS = (
    SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET(
      'sales_db.sales_schema.prod_sales_project'
    ) AS 'state'
  );
```

For details about state artifacts, selectors, and defer, see [Use dbt artifacts for Slim CI and defer to production](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod).

### View compiled SQL

The **View Compiled SQL** button appears on `.sql` files inside the `model-paths` directory, or the `/models` fallback when `model-paths` isn’t set in `dbt_project.yml`. Select it to see the SQL that dbt generates for the model, with references and macros resolved.

## Explore the DAG from a workspace

The workspace DAG supports the same search bar, depth controls, and column-level lineage as the project details DAG. As you
iterate on your project and run models, the workspace DAG automatically reflects the latest results: the side panel for each
model node is populated with runtime data from the most recent `manifest.json` and `run_results.json` artifacts, including
start time, end time, and duration for the last run. This makes it easy to spot slow or failing models without leaving your
workspace.

When a workspace is connected to a dbt project object, you can explore the project’s DAG directly from the workspace by selecting
**Connect** » **View project** to open the project details page, then selecting the **Graph** tab.

For full details on searching the DAG, controlling depth, and viewing column-level lineage, see
[View and manage dbt project objects](/user-guide/data-engineering/dbt-projects-on-snowflake-manage).

## Limitations, requirements, and considerations for using workspaces with dbt projects

The following requirements, considerations, and limitations apply to workspaces for dbt Projects on Snowflake:

- Each dbt project folder in your Snowflake workspace must contain a [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` file that specifies a target `warehouse`, `database`, `schema`, and `role` in Snowflake for the project.
  - The `type` must be set to `snowflake`.
  - Unlike dbt Core, you don’t need valid `account` and `user` values. Because the dbt project runs in Snowflake under your current account and user context, you can omit these fields or set them to an empty or arbitrary string.
- When you deploy a specific dbt project folder as a dbt project object, that folder can contain at most 100,000 files across all folders, including generated `target`, `dbt_packages` (external packages and macros installed by `dbt deps`), and `logs` directories.
  - For very large projects approaching this limit, consider splitting into logical sub-projects, or contact your Snowflake account representative if you need more capacity.

### Personal database requirement

Workspaces are created within a personal database and cannot be shared with other users. Personal databases must be enabled at the account level, which requires ACCOUNTADMIN privileges. For more information, see [Manage access and behavior](/user-guide/ui-snowsight/workspaces#label-manage-access-and-behavior).

Shared workspaces are created within a specific database and schema, which grants access to multiple authenticated users. Users assigned specific roles can then contribute, edit, and modify code and files simultaneously within the environment. For more information, see [Shared workspaces](/user-guide/ui-snowsight/workspaces-shared).

### Git repositories

For requirements, considerations, and limitations that apply when you connect a workspace for dbt Projects on Snowflake to a Git repository, see
[Git in Snowflake limitations](/developer-guide/git/git-limitations).

Git repositories accessed through PrivateLink must be configured beforehand. For more information, see [Connect to a Git repository over a public network](/developer-guide/git/git-setting-up-public#label-git-setup-public-network).
