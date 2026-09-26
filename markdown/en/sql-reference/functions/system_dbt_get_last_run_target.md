Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$DBT\_GET\_LAST\_RUN\_TARGET

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

Returns the location of dbt artifacts from the most recent completed execution of a dbt project object within the previous 7 days, whether the execution succeeded or failed. You can import these artifacts into another dbt project execution and use them with `--state`.

## Syntax

Copy code

```
SYSTEM$DBT_GET_LAST_RUN_TARGET (
  '<object_name>'
  [ , '<commands>' [ , '<target_path>' ] ]
)
```

## Arguments

`object_name`
:   String that specifies the fully qualified name of the dbt project object whose dbt artifacts you want to retrieve.

`commands`
:   Optional comma-separated list of dbt commands to include when searching execution history. The default list is `compile`, `build`, `run`, and `docs generate`.

    For a compound command, specify the command and its subcommand, such as `docs generate` or `source freshness`. To retrieve source
    freshness results, pass `source freshness` explicitly. For an example, see
    [Retrieve source freshness results](#label-dbt-get-last-run-source-freshness).

`target_path`
:   Optional target path to match. When specified, the function considers only executions that used that target path.

## Returns

Returns the location of dbt artifacts produced by the object’s most recent completed qualifying execution. Use the location with the `IMPORTS` parameter of [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project) or the Snowflake CLI `--import` option.

Returns `NULL` if no qualifying completed execution with a populated target directory is available in the lookback window.

The location contains standalone target artifacts such as `manifest.json`, `run_results.json`, and `sources.json` when present. The
function doesn’t generate missing files or return `dbt_artifacts.zip`. When you import the location `AS 'state'`, Snowflake mounts the
target artifacts at `./imports/state`. For the full archive from a known query, use [SYSTEM$LOCATE\_DBT\_ARCHIVE](/sql-reference/functions/system_locate_dbt_archive).

## Access control requirements

The role used to call this function must have the `MONITOR` privilege on the dbt project object.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The dbt project object must have a completed execution with a populated target directory within the previous 7 days.
- Deployment-time auto compile doesn’t create dbt artifacts for this function. Complete a qualifying execution after deployment.
- This function can return dbt artifacts from either a successful or failed execution. Use [SYSTEM$DBT\_GET\_LAST\_SUCCESSFUL\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_successful_run_target) or [SYSTEM$DBT\_GET\_LAST\_FAILED\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_failed_run_target) when the execution status matters.
- `--import` or `IMPORTS` makes the returned dbt artifacts available to an execution. You must also point dbt to the mounted directory with `--state`.
- To retrieve dbt artifacts for a specific query ID instead, use [SYSTEM$LOCATE\_DBT\_ARTIFACTS](/sql-reference/functions/system_locate_dbt_artifacts) or [SYSTEM$LOCATE\_DBT\_ARCHIVE](/sql-reference/functions/system_locate_dbt_archive).

## Examples

### Import artifacts from a recent execution

Return the location of dbt artifacts from the most recent completed execution:

Copy code

```
SELECT SYSTEM$DBT_GET_LAST_RUN_TARGET(
  'prod_database.dbt_projects.production_project'
);
```

Import dbt artifacts from the most recent completed `run` or `build` execution and use them for a
Slim CI run:

Copy code

```
EXECUTE DBT PROJECT ci_database.dbt_projects.pr_test_project
  ARGS = 'run --state ./imports/state --defer --select state:modified+'
  IMPORTS = (
    SYSTEM$DBT_GET_LAST_RUN_TARGET(
      'prod_database.dbt_projects.production_project',
      'run,build'
    ) AS 'state'
  );
```

Import dbt artifacts from the most recent completed execution that used `--target-path my_target` and
use them for a Slim CI run. To retain the default command filter when you specify a target path, pass
the default command list as the second argument:

Copy code

```
EXECUTE DBT PROJECT ci_database.dbt_projects.pr_test_project
  ARGS = 'run --state ./imports/state --defer --select state:modified+'
  IMPORTS = (
    SYSTEM$DBT_GET_LAST_RUN_TARGET(
      'prod_database.dbt_projects.production_project',
      'compile,build,run,docs generate',
      'my_target'
    ) AS 'state'
  );
```

### Retrieve source freshness results

The `source_status:fresher+` selector compares current and previous `sources.json` files. It selects sources with newer data along with
their downstream resources. In the following CI/CD example, you run source freshness on a tester object to create the current file, then
import the production object’s source freshness results as the previous state. Both objects must configure freshness for the sources
being compared, and the execution role must be able to query those sources. For comparison behavior, see
[Source status selection](https://docs.getdbt.com/reference/node-selection/methods#source_status). For configuration, see
[Source freshness](https://docs.getdbt.com/docs/deploy/source-freshness).

First, run source freshness on the production object to create the previous results:

Copy code

```
EXECUTE DBT PROJECT my_db.my_schema.production_dbt_project
  ARGS = 'source freshness';
```

Snowflake stores the generated `sources.json` in the production execution’s
[results directory](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-results-directory-contents).

After source data changes, run source freshness on the tester object and write the current `sources.json` file to its live version:

Copy code

```
EXECUTE DBT PROJECT my_db.my_schema.tester_dbt_project
  ARGS = 'source freshness'
  WRITEBACK = TRUE;
```

`WRITEBACK = TRUE` persists the current `sources.json` in the tester object’s live `target` directory so the next execution can use it.
Snowflake also stores the file in the tester execution’s results directory.

Import the production object’s previous freshness results `AS 'state'`. Snowflake mounts the production target at `./imports/state`.
The build uses the tester object’s current `target/sources.json` file and the previous `./imports/state/sources.json` file for the
comparison. These files record source freshness results, not the contents of the source tables:

Copy code

```
EXECUTE DBT PROJECT my_db.my_schema.tester_dbt_project
  ARGS = 'build --state ./imports/state --select source_status:fresher+'
  IMPORTS = (
    SYSTEM$DBT_GET_LAST_RUN_TARGET(
      'my_db.my_schema.production_dbt_project',
      'source freshness'
    ) AS 'state'
  );
```

This function includes failed freshness executions as well as successful ones, so it can locate results when a freshness threshold is
exceeded. To select only a successful freshness execution, call
[SYSTEM$DBT\_GET\_LAST\_SUCCESSFUL\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_successful_run_target):
`SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET('my_db.my_schema.production_dbt_project', 'source freshness')`.
If the object has multiple qualifying executions and you need artifacts from one exact run, pass that execution’s query ID to
[SYSTEM$LOCATE\_DBT\_ARTIFACTS](/sql-reference/functions/system_locate_dbt_artifacts).
