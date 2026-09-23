# snow dbt execute commands

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

The `snow dbt execute` command executes one of the following [dbt commands](https://docs.getdbt.com/reference/dbt-commands) on Snowflake:

- [build](https://docs.getdbt.com/reference/commands/build)
- [clean](https://docs.getdbt.com/reference/commands/clean)
- [compile](https://docs.getdbt.com/reference/commands/compile)
- [deps](https://docs.getdbt.com/reference/commands/deps)
- [list](https://docs.getdbt.com/reference/commands/list)
- [parse](https://docs.getdbt.com/reference/commands/parse)
- [retry](https://docs.getdbt.com/reference/commands/retry)
- [run](https://docs.getdbt.com/reference/commands/run)
- [run-operation](https://docs.getdbt.com/reference/commands/run-operation)
- [seed](https://docs.getdbt.com/reference/commands/seed)
- [show](https://docs.getdbt.com/reference/commands/show)
- [snapshot](https://docs.getdbt.com/reference/commands/snapshot)
- [source freshness](https://docs.getdbt.com/reference/commands/source)
- [test](https://docs.getdbt.com/reference/commands/test)

For more information about using dbt commands, see the [dbt Command reference](https://docs.getdbt.com/reference/dbt-commands).

## Examples

The following examples show how to invoke `snow dbt execute`. The NAME argument identifies the dbt project object you want to run.

- Execute the `build` dbt command using a fully qualified object name:

  Copy code

  ```
  snow dbt execute uche_db.public.my_dbt_project build
  ```
- Execute the `test` dbt command, select a specific model subset, and override the dbt version for this run:

  Copy code

  ```
  snow dbt execute --dbt-version '1.11.11' my_dbt_project test --select my_model+
  ```
- Execute the `run` dbt command with inline environment variable overrides for this run:

  Copy code

  ```
  snow dbt execute --env-vars '{"DBT_DATABASE": "tasty_bytes_db", "DBT_SCHEMA": "analytics"}' \
    my_dbt_project run
  ```
- Execute the `run` dbt command, pulling `DBT_`-prefixed variables (excluding `DBT_ENV_SECRET_*` variables) from your shell environment:

  Copy code

  ```
  snow dbt execute --use-shell-env-vars my_dbt_project run
  ```

  `--env-vars` applies inline `DBT_`-prefixed overrides for a single execution, and `--use-shell-env-vars` pulls `DBT_`-prefixed shell variables into the run (excluding `DBT_ENV_SECRET_*` variables). To select an environment defined in the project’s `env.yml` file, add the `--env` flag. These flags require Snowflake CLI 3.21 or later. For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).
- Run without writing generated target and log files back to the live version:

  Copy code

  ```
  snow dbt execute --no-writeback my_dbt_project run --target dev
  ```

  Place `--writeback` or `--no-writeback` before the dbt command. If you omit the option, the execution uses the object’s `DEFAULT_WRITEBACK`
  setting. For concurrent executions of the same dbt project object, Snowflake recommends `--no-writeback` when target and log artifacts
  don’t need to persist to the live version. Using `--no-writeback` avoids conflicts during concurrent executions by preventing writes to
  overlapping target and log directories. If writeback is required, use distinct, non-overlapping target and log directories for each execution.
  Snowflake stores the per-query result artifacts and archive regardless of this setting.
  For retrieval instructions, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs). For examples, see
  [Run a dbt project object concurrently](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod#label-dbt-project-concurrent-executions).
- Run only models that changed since the last successful production execution, along with their downstream dependencies:

  Copy code

  ```
  snow dbt execute \
    --import "SYSTEM\$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET('prod_db.analytics.production_dbt_project') as state" \
    my_dbt_project \
    run --state ./imports/state --defer --select state:modified+
  ```

  `SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET` returns the manifest.json and run\_results.json from most recent successful execution in the results folder of the production dbt project object. The `state` alias mounts it under `./imports/state`, which is the path passed to dbt with `--state`. For prerequisites and a complete Slim CI workflow, see [Use dbt artifacts for Slim CI and defer to production](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod).

  Repeat `--import` to mount files from multiple locations. Each alias determines the directory name under `./imports`. Imports make files
  available only to that execution. They don’t permanently copy the files into the dbt project object’s live version. To copy files into or
  out of the live version, use [snow dbt copy](/developer-guide/snowflake-cli/command-reference/dbt-commands/copy).

For more examples and workflow guidance, see [Managing dbt Projects on Snowflake using Snowflake CLI](/developer-guide/snowflake-cli/data-pipelines/dbt-projects).
