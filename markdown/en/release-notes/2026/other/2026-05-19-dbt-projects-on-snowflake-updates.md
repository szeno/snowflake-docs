# May 19, 2026: dbt Projects on Snowflake updates

The following improvements are now available for dbt Projects on Snowflake:

- **Enhanced dbt DAG with column-level lineage**: The dbt DAG visualization is now significantly
  more capable across all three surfaces (Workspaces, dbt project object details, and Query
  History). Each model node displays its columns, powered by the Snowflake Horizon Catalog as the
  single source of truth. Selecting a column highlights all upstream and downstream models in the
  DAG that use that column. Additional improvements include an in-DAG search bar to find models
  by name, expandable upstream and downstream depth controls, a unified side panel showing row
  count, column count, compiled SQL, and runtime information, and an increased model display limit
  (up from 100 to 300). For more information, see
  [View and manage dbt project objects](/user-guide/data-engineering/dbt-projects-on-snowflake-manage).
- **dbt Fusion engine**: dbt Projects on Snowflake now supports the dbt Fusion engine, a ground-up rewrite of the
  dbt runtime in Rust that is designed to deliver improved compilation times as project complexity increases. No additional license or
  subscription is required. Fusion is available to all users of dbt Projects on Snowflake and
  Workspaces in Snowflake, with no user limit. For more information, see
  [Migrate to dbt Fusion](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions#label-dbt-fusion-migration).
- **Multi-version dbt support**: Pin a specific dbt version to a dbt project object at
  creation time using the `DBT_VERSION` parameter, or override it at runtime. This applies to
  both deployed dbt project objects and Workspaces. Supported versions include dbt Core 1.9.4 and 1.10.15
  as well as dbt Fusion 2.0.0-preview. Set an account-level default for all new projects using
  `DEFAULT_DBT_VERSION`. For more information, see
  [Supported dbt versions for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions).
- **Cortex Code for dbt**: Cortex Code supports the full dbt lifecycle within Workspaces and CLI,
  including scaffolding dbt models, adding tests, running dbt commands, generating documentation,
  and inspecting the files of deployed dbt project objects for exploration and debugging. For more
  information, see [CoCo in Snowsight](/user-guide/cortex-code/cortex-code-snowsight).
- **Run a single dbt file in Workspaces**: Use the run button on an individual model file in the
  Workspace editor to run or build that model without executing the entire project.
- **Partial dbt project execution from the DAG**: Select the **…** menu on a model node in the
  DAG to choose from targeted execution options, running only the selected model, its upstream
  parents, its downstream dependents, or all three. For more information, see
  [View and manage dbt project objects](/user-guide/data-engineering/dbt-projects-on-snowflake-manage).
- **Import a dbt project object into a Workspace**: From within a Workspace, import the contents
  of an existing deployed dbt project object as a new folder for editing and iteration.
- **SYSTEM$GET\_DBT\_LOG max\_num\_lines argument**: The
  [SYSTEM$GET\_DBT\_LOG](/sql-reference/functions/system_get_dbt_log) system function accepts an optional second
  argument, `max_num_lines`, that controls how many lines from the end of the `dbt.log` file are
  returned. The default is 1,000 lines. The result is capped at approximately 10 MB regardless of
  the value specified; if the cap is exceeded, the oldest lines are dropped so the most recent
  output is always returned. For more information, see
  [SYSTEM$GET\_DBT\_LOG](/sql-reference/functions/system_get_dbt_log).
