# Limitations, requirements, and considerations for dbt Projects on Snowflake

Before you use dbt Projects on Snowflake, review the requirements, considerations, and limitations:

- [Limitations, requirements, and considerations for stored procedures](#label-dbt-requirements-stored-procedures)
- [Limitations, requirements, and considerations for using workspaces with dbt projects](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces#label-dbt-requirements-workspaces)

  - [Personal database requirement](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces#label-dbt-requirements-workspaces-personal-database)
  - [Git repositories](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces#label-dbt-requirements-workspaces-git)
- [Limitations, requirements, and considerations for dbt dependencies](/user-guide/data-engineering/dbt-projects-on-snowflake-dependencies#label-dbt-requirements-deps)
- [Limitations, requirements, and considerations for telemetry, logging, and tracing](#label-dbt-requirements-telemetry)
- [Replication and dbt projects](/user-guide/account-replication-considerations#label-replication-and-dbt-projects)
- [Limitations for the dbt DAG](#label-dbt-dag-limitations)

  - [Limitations for the query history DAG](#label-dbt-limitations-query-history-dag)
  - [Limitations for column-level lineage](#label-dbt-limitations-column-lineage)

## Limitations, requirements, and considerations for dbt project configurations

The following requirements, considerations, and limitations apply to dbt project configurations that are supported by dbt Projects on Snowflake:

> - Only dbt Core and dbt Fusion projects are supported. dbt Cloud projects aren’t supported. When you migrate an existing dbt project to Snowflake, it
>   must be compatible with [supported dbt versions](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions).
> - Each dbt project folder in your Snowflake workspace must contain a [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` file that specifies a target `warehouse`,
>   `database`, `schema`, and `role` in Snowflake for the project. The `type` must be set to `snowflake`. dbt
>   requires an `account` and `user`, but these can be left with an empty or arbitrary string because the dbt project runs in
>   Snowflake under the current account and user context.
> - When you deploy a specific dbt project folder as a dbt project object, that folder can contain at most 100,000 files. This limit includes all files in the dbt project
>   directory and subdirectories, including generated `target`, `dbt_packages`, and `logs` directories.
> - Serverless tasks can’t be used to execute dbt project objects. When you create a task that executes the EXECUTE DBT PROJECT command, you must
>   specify a user-managed warehouse.

## Limitations, requirements, and considerations for stored procedures

When you use a stored procedure to call EXECUTE DBT PROJECT, use a caller’s rights stored procedure. For more information, see
[CREATE PROCEDURE](/sql-reference/sql/create-procedure) and [Creating a stored procedure](/developer-guide/stored-procedure/stored-procedures-creating).

## Limitations, requirements, and considerations for telemetry, logging, and tracing

The following requirements, considerations, and limitations apply to telemetry, logging, and tracing for dbt on Snowflake:

> - Workspaces for dbt Projects on Snowflake don’t stream stdout dynamically, and stdout is only viewable upon command completion.
> - Viewing logs and tracing requires that you set the LOG\_LEVEL and TRACE\_LEVEL on the dbt project object. For more information, see [Access control for dbt projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-access-control) and [Monitor dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability).
> - By default, Snowflake collects telemetry in the default SNOWFLAKE.TELEMETRY.EVENTS table. If you have a custom event table that is set as the event table for your account, telemetry data is collected there. If you use an Enterprise Edition account, you can create an event table to collect telemetry data and associate it with the database where the dbt project object is deployed. For more information, see [Event table overview](/developer-guide/logging-tracing/event-table-setting-up).

## Limitations for the dbt DAG

The following limitations apply to the dbt DAG across all surfaces (project details, query history, and workspaces):

- The DAG displays up to 300 models at a time. If your project has more models, use the search bar and depth controls to navigate
  to the part of the graph you need.

### Limitations for the query history DAG

The query history DAG requires both `manifest.json` and `run_results.json` artifacts to render the visualization. If a dbt
project object execution fails before `run_results.json` is generated, the **DAG** tab in **Query Details** shows “No data available”
instead.

Common causes of fast-failing executions that prevent `run_results.json` from being generated include:

- Insufficient privileges to execute the dbt project object.
- Invalid project configuration (for example, a missing or malformed `dbt_project.yml` file).
- Missing dependencies that haven’t been installed with `dbt deps`.

To resolve this, check the **dbt Output** section in the **Query Details** tab for error messages, fix the underlying issue, redeploy
the dbt project object, and re-execute it. For more information about monitoring dbt project object executions, see
[View the query history DAG](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-query-history-dag).

### Limitations for column-level lineage

Column-level lineage in the dbt DAG is powered by Snowflake Horizon Catalog, which tracks lineage on the underlying materialized tables and views.
The following limitations apply:

- Column-level lineage isn’t available until the project has been run at least once and the underlying objects have been materialized in a schema.
- Column-level lineage may show gaps in pipelines that use intermediary views that are dropped between materializations, which is a common dbt pattern. Table-level lineage is unaffected.
- If a node fails to materialize during a run, its column-level lineage may be stale or missing. The node could be absent from the Snowflake layer or materialized with a different set of columns from a previous run.
