# Understand dbt project objects

A DBT PROJECT is a schema-level object that contains the source files and artifacts for a deployed dbt project in Snowflake. Its project directory contains a `dbt_project.yml` file at the root and the model files that define your data pipeline.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

A dbt project object has one mutable version named `live`. The files are available at a path in the following form:

```
snow://dbt/<database>.<schema>.<project>/versions/live
```

When you [deploy](/user-guide/data-engineering/dbt-projects-on-snowflake-deploy) a dbt project, Snowflake copies files from a workspace, Git repository stage, internal stage, or local directory into this live version. A workspace is a development environment where you can edit and debug dbt code before deploying it to a dbt project object through Snowsight or a CI/CD pipeline.

dbt project objects support role-based access control (RBAC). You can create, alter, and drop them like other schema-level objects in
Snowflake. You can use the [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project) command from a Snowflake warehouse to execute dbt commands such as
`test` and `run`. You can also use [tasks](/user-guide/tasks-intro) to schedule execution of these commands.

## Benefits of creating a dbt project object

- **Run from any orchestrator:** Use `EXECUTE DBT PROJECT` from any SQL client, Snowflake task, or external orchestrator such as Apache Airflow.
- **Monitoring and observability:** Each dbt project object execution sends OpenTelemetry-compatible logs and traces to the Snowflake Event Table. Users get programmatic access to query history details using `DBT_PROJECT_EXECUTION_HISTORY` and `SYSTEM$GET_DBT_LOG`. For more information, see [Monitor dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability).
- **CI/CD integration:** Use Snowflake CLI (`snow dbt deploy`) to update the live project automatically on every merge. For a full walkthrough, see [Tutorial: Set up CI/CD integrations on dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial).
- **Reusable execution artifacts:** Reuse dbt artifacts from earlier executions for Slim CI, defer to production, partial parsing, and failed-execution recovery. Retrieve them with execution-result system functions such as [SYSTEM$DBT\_GET\_LAST\_SUCCESSFUL\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_successful_run_target).
- **AI-assisted debugging with Cortex:** Cortex AI can inspect your deployed project files and lineage. When an execution fails, ask Cortex natural-language questions to diagnose the issue directly with the deployed object files.
- **Real-time project documentation:** The project details page is an in-product replacement for dbt docs, with an interactive DAG, column-level lineage, compiled SQL, and full run history. For more information, see [View and manage dbt project objects](/user-guide/data-engineering/dbt-projects-on-snowflake-manage).

## How dbt project objects get updated

dbt project objects don’t automatically update as you edit the source workspace or repository. To redeploy and update the object files, use
[`ALTER DBT PROJECT ... DEPLOY`](/sql-reference/sql/alter-dbt-project) or
[`snow dbt deploy`](/developer-guide/snowflake-cli/command-reference/dbt-commands/deploy).

To create a production pipeline, we recommend deploying the dbt project object and
[scheduling its execution with a task](/user-guide/data-engineering/dbt-projects-on-snowflake-schedule-project-execution).

The following example uses SQL:

Copy code

```
ALTER DBT PROJECT testdbt.public.my_dbt_project_object
  DEPLOY FROM 'snow://workspace/user$.public."all_my_dbt_projects"/versions/live';
```

For teams using Git-based workflows, Snowflake recommends using Snowflake CLI to deploy directly from a CI/CD pipeline such as GitHub
Actions. For example:

Warning

Don’t use `--force` unless you intentionally want to recreate the dbt project object. In `snow dbt deploy`, `--force` runs `CREATE OR REPLACE DBT PROJECT`, which may remove run history.

Copy code

```
snow dbt deploy my_dbt_project_object --source ./path/to/dbt/project
```

`--source` specifies the directory from which Snowflake CLI reads the dbt project files. When it points to a local path, such as
`./path/to/dbt/project`, Snowflake CLI reads the files from that directory on disk. In GitHub Actions, this directory is the checked-out code
repository and contains the committed project files.

If the dbt project object already exists, both `ALTER DBT PROJECT ... DEPLOY` and `snow dbt deploy` replace its live version in a single
operation. For a full CI/CD walkthrough, see [Tutorial: Set up CI/CD integrations on dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial).

## Files and artifacts in a dbt project object

A dbt project object stores several layers of files:

- **Project source files:** The live version contains `dbt_project.yml`, model files, profile configuration, and other files copied during deployment.
- **Deployment-time compile artifacts:** The `AUTO_COMPILE` property controls automatic dependency installation and compilation during
  creation and deployment. With `AUTO_COMPILE = TRUE`, Snowflake runs `dbt compile` during deployment. If an external access integration is
  configured, Snowflake first runs `dbt deps`, then `dbt compile`. Setting `AUTO_COMPILE = FALSE` skips both commands. Compiled artifacts, such
  as `target/manifest.json`, are written to the live version so that Snowflake can display project details.
- **Execution-time target and log artifacts:** A dbt command can update target and log paths in the live version. The object’s `DEFAULT_WRITEBACK` setting controls this behavior by default, and an individual execution can override it with `WRITEBACK`.
- **Per-query results:** Snowflake stores separate per-query result artifacts and an archive for each execution under the object’s `results`
  directory, regardless of the `WRITEBACK` setting.

Auto compile and writeback apply at different lifecycle moments. Auto compile runs during deployment. This automatic compilation doesn’t
store per-query result artifacts under the object’s `results` directory. As a result, automatic compilation doesn’t create an execution that
system functions can use to retrieve dbt artifacts from recent executions. Writeback applies when you execute the deployed project and
controls whether target and log artifacts from that execution update the live version.

Executions produce reusable artifacts for Slim CI with defer to production, partial parsing, source freshness, and failed-execution recovery.
Depending on the workflow, artifacts are available from per-query results or persist to the live version when writeback is enabled. For
concurrent executions, use separate, non-overlapping target and log directories or disable live writeback. For more information, see
[Use dbt artifacts for Slim CI and defer to production](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod).
