# Use dbt artifacts for Slim CI and defer to production

dbt project objects let you reuse artifacts from recent production executions in development and CI workflows. Snowflake makes these artifacts directly available from the deployed production object, so you don’t need to maintain a separate artifact store. Slim CI uses the artifacts to process changed resources and their downstream dependencies, while defer resolves unbuilt upstream references to existing production relations. Together, these capabilities shorten dbt execution time and reduce warehouse use.

This guide explains how to:

- Choose state artifacts.
- Use Slim CI and defer from Snowflake Workspaces or Snowflake CLI.
- Recover from a failed execution.
- Run a dbt project object concurrently.
- Retrieve dbt artifacts for a specific query.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

## Concepts

### Slim CI and defer to production

dbt state selection compares the project you are executing with artifacts from an earlier execution. The most important state artifacts are:

- `manifest.json`, which describes the resources and relationships in the earlier project.
- `run_results.json`, which records the status of resources processed by an earlier command.
- `sources.json`, which records source freshness results, including source load timestamps.

The `--state <path>` option tells dbt where to read these artifacts. For a dbt project object, use an import to mount the artifacts under the execution’s `./imports` directory, then point `--state` at the mounted directory.

Different selectors need different artifacts. `state:modified+` uses `manifest.json`, `result:error+` uses `run_results.json`, and
`source_status:fresher+` compares current source freshness results with an earlier `sources.json`. A selector works only when the imported
results from the earlier execution contain the corresponding artifact. For source freshness prerequisites and comparison behavior, see
[Source status selection](https://docs.getdbt.com/reference/node-selection/methods#source_status).

Slim CI uses state selectors to limit the resources that CI processes. The selector `state:modified+` selects resources that changed relative to the state artifacts and also includes their downstream dependencies. Use Slim CI when you want to validate only changed resources and their downstream dependencies instead of rebuilding and retesting the entire project.

Slim CI differs from incremental models:

- Slim CI skips unchanged nodes in the project DAG.
- Incremental models process only new or changed rows when a selected model runs.

Slim CI also differs from dbt State Aware Orchestration. Slim CI uses dbt artifacts and selectors such as `--state` and `--select state:modified+`. State Aware Orchestration uses relation metadata to determine whether models need to run.

The `--defer` option controls how dbt resolves an upstream `ref()` when the referenced model isn’t selected for the current execution. With production artifacts mounted as a state reference, dbt can use the existing production relation instead of rebuilding that model in the CI target.

State selection and defer solve different problems:

- State selection determines which nodes CI processes.
- Defer determines where dbt finds unbuilt upstream relations.
- The selected target determines where CI writes the models that it does process.

### Understand auto compile and writeback

Auto compile applies to deployment. Writeback applies to executions:

- With `AUTO_COMPILE = TRUE`, Snowflake runs `dbt compile` during deployment. If an external access integration is configured, Snowflake first runs `dbt deps`, then `dbt compile`. Setting `AUTO_COMPILE = FALSE` skips both commands. Auto compile is enabled by default.
- `DEFAULT_WRITEBACK` controls whether later executions write target and log artifacts to the live version. An execution can override the object default with `WRITEBACK`.

Auto compile writes compile artifacts to the live version so that Snowflake can display project details. It doesn’t create an execution result that the `SYSTEM$DBT_GET_LAST_*_RUN_TARGET` functions can reuse.

Disabling writeback prevents an execution from writing target and log artifacts to the live version. If you plan to run your dbt project object concurrently, Snowflake recommends disabling writeback. Snowflake stores the per-query result artifacts and archive regardless of this setting.
For retrieval instructions, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).

### Choose state artifacts

Choose the system function that matches how you want to identify an earlier execution:

1. Use [`SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET`](/sql-reference/functions/system_dbt_get_last_successful_run_target) for the normal Slim CI workflow. When you import the result `AS 'state'`, Snowflake mounts the target artifacts at `./imports/state`.
2. Use [`SYSTEM$DBT_GET_LAST_FAILED_RUN_TARGET`](/sql-reference/functions/system_dbt_get_last_failed_run_target) to recover from the most recent failed qualifying execution.
3. Use [`SYSTEM$DBT_GET_LAST_RUN_TARGET`](/sql-reference/functions/system_dbt_get_last_run_target) when you need the most recent completed qualifying execution regardless of whether it succeeded or failed.
4. Use [`SYSTEM$LOCATE_DBT_ARTIFACTS`](/sql-reference/functions/system_locate_dbt_artifacts) or [`SYSTEM$LOCATE_DBT_ARCHIVE`](/sql-reference/functions/system_locate_dbt_archive) when you know the query ID of the execution you need. When you import the result `AS 'state'`, Snowflake mounts the query-scoped results under `./imports/state`, and the dbt artifacts are in `./imports/state/target`.

The `SYSTEM$DBT_GET_LAST_*_RUN_TARGET` functions select a recent execution by dbt project object, completion status, qualifying command filter, and target path. The `SYSTEM$LOCATE_DBT_*` functions require the query ID of a specific execution.

By default, the `SYSTEM$DBT_GET_LAST_*_RUN_TARGET` functions search for `compile`, `build`, `run`, and `docs generate` executions. Pass
`'source freshness'` as the command filter to find freshness results. These functions return the matching execution’s target location.
They don’t execute a dbt command or generate missing artifacts.

When used in `IMPORTS`, the `SYSTEM$DBT_GET_LAST_*_RUN_TARGET` functions import standalone target artifacts, including `manifest.json`,
`run_results.json`, and `sources.json` when present. `SYSTEM$LOCATE_DBT_ARTIFACTS` imports a specific query’s results directory,
including `dbt_artifacts.zip`, but doesn’t extract the ZIP file. Use `SYSTEM$LOCATE_DBT_ARCHIVE` directly when you need the archived target
and logs, such as compiled SQL. This function is the only way to extract a ZIP file into an execution, and an execution can extract at
most one ZIP file. Importing the full archive can take longer than importing standalone artifacts. For the results directory’s file list, see
[Results directory contents](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-results-directory-contents).

## Prerequisites for using dbt state artifacts

Before a CI job imports production dbt artifacts, you must have:

- A production dbt project object with at least one qualifying execution within the previous 7 days.
- A CI role with the `MONITOR` privilege on the production object.
- A separate database or schema where the CI job can create or update relations.
- The privileges required to deploy and execute the tester dbt project object.

Deployment-time auto compile doesn’t generate dbt artifacts that the `SYSTEM$DBT_GET_LAST_*_RUN_TARGET` system functions can use. Execute the production dbt project object after deployment and at least once every 7 days so that qualifying dbt artifacts remain available.

Grant the CI role monitoring access to the production object:

Copy code

```
GRANT MONITOR ON DBT PROJECT <database>.<schema>.<production_project>
  TO ROLE <ci_role>;
```

The role also needs access to the warehouse and to any production relations that unchanged upstream references resolve to.

## Use defer to production in Snowflake Workspaces

To use production artifacts as state during development:

1. In the execution pane, select **Advanced options**.
2. Enable **Defer to Production**.
3. Select the database and schema that contain the production dbt project object, and then select the object.

   A dbt project object appears only if you have the `MONITOR` privilege on it. The object must also have at least one qualifying execution within the previous 7 days.
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

## Use Slim CI with Snowflake CLI

The following pattern deploys a tester object with automatic compilation disabled, imports dbt artifacts from the last successful production execution, and uses one selective `dbt build` to run models and tests in DAG order:

Copy code

```
snow dbt deploy tester_dbt_project \
  --source ./path/to/dbt_project \
  --no-auto-compile

snow dbt execute \
  --import "SYSTEM\$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET('my_db.my_schema.production_dbt_project') AS 'state'" \
  tester_dbt_project \
  build --target dev --state ./imports/state --defer --select state:modified+
```

You can specify `--import` multiple times to mount files from multiple locations. Each alias names a subdirectory under `./imports`. For example, `AS 'state'` mounts the returned artifacts at `./imports/state`. The `--state` option reads the artifacts from that path.

When used with `--import`, `SYSTEM$LOCATE_DBT_ARTIFACTS` imports the results directory, including `dbt_artifacts.zip`, but doesn’t
extract the ZIP file. Use [`SYSTEM$LOCATE_DBT_ARCHIVE`](/sql-reference/functions/system_locate_dbt_archive) directly when you need the
archived target and logs, such as compiled SQL. Snowflake extracts the archive automatically. An execution can automatically
extract at most one ZIP file.

GitHub Actions automatically supplies repository URL, branch, and commit metadata when you deploy with Snowflake CLI. For other CI runners, explicitly pass `--git-url`, `--git-branch`, and `--git-commit` so the dbt project object remains traceable to its source.

For an end-to-end Slim CI example that uses `--env` and `--env-vars` with an isolated database for each pull request, see [Tutorial: Set up CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-advanced-ci-cd-tutorial).

## Recover from a failed execution

When a `run` or `build` fails partway through, rerunning the complete command repeats work that already succeeded. `dbt retry` can avoid a complete rerun, but it replays the previous invocation with inherited arguments and selected resources, giving you less control over what dbt reruns.

If you know the failed execution’s query ID, import its results with
[`SYSTEM$LOCATE_DBT_ARTIFACTS`](/sql-reference/functions/system_locate_dbt_artifacts), then use an explicit result selector:

Copy code

```
EXECUTE DBT PROJECT my_dbt_project
  ARGS = 'build --state ./imports/state/target --select result:error+'
  IMPORTS = (
    SYSTEM$LOCATE_DBT_ARTIFACTS('<query_id>') AS 'state'
  );
```

If you don’t know the query ID, import the most recent failed execution’s state with
[`SYSTEM$DBT_GET_LAST_FAILED_RUN_TARGET`](/sql-reference/functions/system_dbt_get_last_failed_run_target), then use an explicit result selector:

Copy code

```
EXECUTE DBT PROJECT my_dbt_project
  ARGS = 'build --state ./imports/state --select result:error+'
  IMPORTS = (
    SYSTEM$DBT_GET_LAST_FAILED_RUN_TARGET(
      'my_db.my_schema.production_dbt_project',
      'run,build'
    ) AS 'state'
  );
```

With Snowflake CLI:

Copy code

```
snow dbt execute \
  --import "SYSTEM\$DBT_GET_LAST_FAILED_RUN_TARGET('my_db.my_schema.production_dbt_project', 'run,build') AS 'state'" \
  my_dbt_project \
  build --state ./imports/state --select result:error+
```

The `result:error+` selector reruns resources that errored and their downstream dependencies. The `result:` selector requires `--state` to point to artifacts that contain `run_results.json`, such as artifacts from a `run` or `build` command.

For failed tests, use `1+result:fail+` to rerun the failed tests, their parent models, and downstream resources.

## Run a dbt project object concurrently

Data teams often need to run independent slices of a pipeline at different cadences. You can run the same dbt project object concurrently so that each slice stays fresh without requiring duplicate deployed objects.

By default, a dbt project object has `DEFAULT_WRITEBACK = TRUE`, so concurrent executions can write target and log artifacts to the same directories on the live version. These overlapping writes can cause an execution to fail. Use one of these isolation patterns:

1. Prefer disabling writeback when the executions don’t need to persist target and log artifacts to the live version. Set `DEFAULT_WRITEBACK = FALSE` on the dbt project object to disable writeback for subsequent executions by default, or override the object default for an individual execution with `WRITEBACK = FALSE` or `--no-writeback`.
2. If writeback is required, use distinct, non-overlapping target and log directories for each execution.

### Set the object default during deployment

With Snowflake CLI, use `--no-default-writeback` to create or update the project with writeback disabled for subsequent executions:

Copy code

```
snow dbt deploy my_db.my_schema.my_dbt_project \
  --source ./path/to/dbt_project \
  --no-default-writeback
```

This setting persists on the object. On later deployments, omitting the flag leaves the existing setting unchanged. Disabling default
writeback affects only execution-time artifact writeback. Automatic compilation can still write compiled artifacts to the live version
during creation or deployment. To disable automatic compilation, you can separately specify `--no-auto-compile`.

With SQL, set `DEFAULT_WRITEBACK = FALSE` when creating the object from a stage directory containing `dbt_project.yml` and the project files:

Copy code

```
CREATE OR REPLACE DBT PROJECT my_db.my_schema.my_dbt_project
  FROM '@my_db.my_schema.dbt_source_stage/my_dbt_project/'
  DEFAULT_WRITEBACK = FALSE;
```

`CREATE OR REPLACE DBT PROJECT` recreates an existing object and removes its run history. To change only the writeback default of an
existing object, use `ALTER DBT PROJECT ... SET` below. To update its source files without replacing the object, use
[`ALTER DBT PROJECT ... DEPLOY`](/sql-reference/sql/alter-dbt-project).

### Change the default on an existing object

To disable writeback for subsequent executions without redeploying the project:

Copy code

```
ALTER DBT PROJECT my_db.my_schema.my_dbt_project
  SET DEFAULT_WRITEBACK = FALSE;
```

### Override the default for one execution

To disable writeback for an individual SQL execution without changing the object default:

Copy code

```
EXECUTE DBT PROJECT my_db.my_schema.my_dbt_project
  ARGS = 'run'
  WRITEBACK = FALSE;
```

With Snowflake CLI, pass `--no-writeback` before the dbt project name:

Copy code

```
snow dbt execute --no-writeback my_dbt_project run
```

If an execution omits `WRITEBACK` or the CLI writeback flag, it uses the object’s `DEFAULT_WRITEBACK` value. You can also override a
disabled object default with `WRITEBACK = TRUE` or `--writeback` for a run that needs to persist artifacts to the live version.

Snowflake stores the per-query result artifacts and archive regardless of this setting.
For retrieval instructions, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).

### Use distinct target and log paths

If live writeback is required, specify distinct target and log directories for each execution:

Copy code

```
EXECUTE DBT PROJECT my_db.my_schema.my_dbt_project
  ARGS = 'run --target-path target/pr_123 --log-path logs/pr_123';
```

With Snowflake CLI:

Copy code

```
snow dbt execute my_dbt_project \
  run --target-path target/pr_123 --log-path logs/pr_123
```

The following restrictions apply:

- Target and log paths must point to directories inside the project. Snowflake recommends pointing to dedicated subdirectories to avoid
  uploading unrelated project files with the execution results.
- Snowflake uploads the complete contents of each target and log directory with the execution results. Uploading unrelated files can increase file counts and reduce performance.
- Target and log directories used by concurrent executions must not overlap. Overlapping writes can cause an execution to fail.

Deployment-time auto compile doesn’t support custom target or log paths defined through environment variables. To use these custom paths, deploy with `--no-auto-compile`, then run `compile` manually.

## Use dbt artifacts from a specific query

The `SYSTEM$DBT_GET_LAST_*_RUN_TARGET` functions are the simplest choice when the most recent qualifying execution has the dbt artifacts you need. If you must use dbt artifacts from a particular execution, use its query ID.

Import the query-scoped results directory with [`SYSTEM$LOCATE_DBT_ARTIFACTS`](/sql-reference/functions/system_locate_dbt_artifacts):

Copy code

```
EXECUTE DBT PROJECT my_db.my_schema.my_dbt_project
  ARGS = 'run --state ./imports/state/target --select result:error+'
  IMPORTS = (
    SYSTEM$LOCATE_DBT_ARTIFACTS('<query_id>') AS 'state'
  );
```

`SYSTEM$LOCATE_DBT_ARTIFACTS` imports the query-scoped results directory, including `dbt_artifacts.zip`, but doesn’t extract the
ZIP file. It mounts the results directory under `./imports/state`, and the dbt artifacts are in its `target` subdirectory.

Use [`SYSTEM$LOCATE_DBT_ARCHIVE`](/sql-reference/functions/system_locate_dbt_archive) directly when you need the archived target
and logs, such as compiled SQL:

Copy code

```
EXECUTE DBT PROJECT my_db.my_schema.my_dbt_project
  ARGS = 'run --state ./imports/state/target --select result:error+'
  IMPORTS = (
    SYSTEM$LOCATE_DBT_ARCHIVE('<query_id>') AS 'state'
  );
```

`SYSTEM$LOCATE_DBT_ARCHIVE` is the only way to extract a ZIP file into an execution. An execution can extract at most one ZIP file.
Importing the full archive can take longer than importing standalone artifacts.

## Use other artifact-based dbt workflows

The mutable live version also supports these workflows:

- **Partial parsing:** With writeback enabled, dbt can persist compatible parsing artifacts in the target path and reuse them during a later execution.
- **Source freshness:** Run `source freshness` to evaluate source freshness and write `sources.json` to the target path. For a SQL execution and retrieval example, see [Retrieve source freshness results](/sql-reference/functions/system_dbt_get_last_run_target#label-dbt-get-last-run-source-freshness).
- **Project cleanup:** Run `clean` to remove configured target directories. Cleanup is all or nothing. For more details, see [Clean a dbt project object](/user-guide/data-engineering/dbt-projects-on-snowflake-supported-commands#label-dbt-clean-project-object).

## Observability

Use Query History and dbt project execution history to inspect individual runs. The dbt project object’s live target and log paths contain artifacts when writeback is enabled, while per-query result directories contain separate execution artifacts regardless of writeback.

For monitoring procedures, artifact and log retrieval, and deployment metadata, see [Monitor dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability). For query-specific artifact locations, see [`SYSTEM$LOCATE_DBT_ARTIFACTS`](/sql-reference/functions/system_locate_dbt_artifacts) and [`SYSTEM$LOCATE_DBT_ARCHIVE`](/sql-reference/functions/system_locate_dbt_archive).

## Reference

The following options and system functions form the main artifact-based workflows:

| Option or system function | Scope and purpose |
| --- | --- |
| `AUTO_COMPILE` / `--no-auto-compile` | Controls whether Snowflake compiles the dbt project during deployment. |
| `DEFAULT_WRITEBACK` | Controls whether subsequent executions write target and log artifacts to the live version by default. |
| `WRITEBACK` / `--writeback` / `--no-writeback` | Overrides the object’s `DEFAULT_WRITEBACK` setting for an individual execution. |
| `--target-path` / `--log-path` | Specifies target and log directories. Use distinct directories for concurrent executions when writeback is required. |
| `--import` / `IMPORTS` | Mounts files or artifacts under the execution’s `./imports` directory. |
| `--state` | Identifies the directory that contains prior dbt artifacts. |
| `state:modified+` | Selects changed resources and their downstream dependencies. |
| `--defer` | Resolves unbuilt references by using relations described by the state artifacts. |
| [`SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET`](/sql-reference/functions/system_dbt_get_last_successful_run_target) | Returns object-scoped state from a recent successful execution. Import it at `./imports/state`. |
| [`SYSTEM$DBT_GET_LAST_FAILED_RUN_TARGET`](/sql-reference/functions/system_dbt_get_last_failed_run_target) | Returns object-scoped state from a recent failed execution for failed-execution recovery. Import it at `./imports/state`. |
| `result:error+` / `1+result:fail+` | Selects errored resources or failed tests and the related resources needed for failed-execution recovery. |
| [`SYSTEM$DBT_GET_LAST_RUN_TARGET`](/sql-reference/functions/system_dbt_get_last_run_target) | Returns object-scoped state from the most recent completed successful or failed execution. Import it at `./imports/state`. |
| [`SYSTEM$LOCATE_DBT_ARTIFACTS`](/sql-reference/functions/system_locate_dbt_artifacts) | Returns the query-scoped results directory for a known query ID. State is in `./imports/state/target`. |
| [`SYSTEM$LOCATE_DBT_ARCHIVE`](/sql-reference/functions/system_locate_dbt_archive) | Returns the complete query-scoped archive for a known query ID. Extracted state is in `./imports/state/target`. |

Expand

Show lessSee more
