# Oct 20, 2026: dbt Projects on Snowflake updates

The following improvements are now available for dbt Projects on Snowflake:

- **dbt State integration**: Connect dbt project objects and Workspaces to dbt State, a dbt Labs service that decides which
  models need to be rebuilt and which models can be reused during an execution. Skipping models that don’t need to run aims to
  reduce execution runtime and warehouse compute. You connect your project to your dbt Platform account through an `env.yml`
  secret and an external access integration. For setup, supported dbt versions, and billing, see
  [Integrate dbt State with dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-state-integration).
- **Source freshness**: Source freshness builds on the same dbt artifact support that powers
  [Slim CI](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod). Run `source freshness` from the command
  list in Workspaces, from the dbt project object details page, and when you schedule a dbt project object. Snowflake CLI also
  supports `source freshness` with `snow dbt execute`. After a freshness check, source nodes in the Workspaces DAG and the dbt
  project object details DAG show a **Fresh**, **Expiring**, or **Stale** badge. The badge is recalculated from the last load
  time and the warn and error thresholds in your source YAML, so it reflects the current state rather than only the last check.
  Hover over a badge to see when the data was last loaded and the freshness rule, or select the source node to see the freshness
  rule in the side panel. To retrieve freshness results with SQL, see
  [Retrieve source freshness results](/sql-reference/functions/system_dbt_get_last_run_target#label-dbt-get-last-run-source-freshness).
- **Cross-project references in the DAG**: When your project pulls in another dbt project as a private Git package with
  `dbt deps`, such as a subfolder of a monorepo or another team’s repository, and references its models with the two-argument
  `ref('project', 'model')` syntax, the DAG now makes those cross-project dependencies visible. In the Workspaces, Query History,
  and dbt project object details DAGs, nodes from the imported project are labeled with their source project, and the DAG shows
  only the imported models that your project references instead of every model in the package. A filter in the DAG toolbar
  isolates cross-project nodes and their direct neighbors, and a project topology view shows which dbt projects your project
  depends on. To set up private Git packages, see
  [Admin setup](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables#admin-setup). For more information,
  see [Cross dbt project dependencies](/user-guide/data-engineering/dbt-projects-on-snowflake-dependencies#label-dbt-key-concepts-cross-project-deps) and
  [Explore the DAG from a workspace](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces#label-dbt-workspace-dag).
- **Re-run failed models from Query History**: In the **dbt Output** section of the query details for a failed dbt project
  object execution, select **Re-run** to rerun the models that errored and their downstream dependencies with
  `--select result:error+`. You can use the artifacts from that exact query or from the last failed run target, or run
  `dbt retry`. This option is available for dbt project objects that use the
  [live version](/user-guide/data-engineering/dbt-projects-on-snowflake-live-version). For more information, see
  [Recover from a failed execution](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod#label-dbt-project-failed-execution-recovery).
- **dbt Projects home page and templates**: The dbt Projects home page in Snowsight lists all of your dbt project
  objects, with filters for database, owner role, and name, and a **Run History** tab. From the home page, you can start a new
  project from a template, such as the Tasty Bytes sample project or a dbt with Cortex project that opens Cortex Code to help you
  build it. The Git-free
  [Getting started with dbt Projects template](https://app.snowflake.com/templates?template=getting_started_with_dbt_projects)
  is also available in the Snowsight templates gallery and from a tile on the Workspaces home page. It adds a ready-to-run
  Tasty Bytes dbt project to a workspace. For more information, see
  [Quick start: Use the Snowsight app template](/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial#label-dbt-get-started-app-template).
- **Environment in run history**: The dbt Projects run history in Snowsight shows the `env.yml` environment selected for
  each run. For more information, see
  [Monitor dbt project objects in Snowsight](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-monitoring).
