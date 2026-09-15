# Supported dbt commands and flags

The following table shows the dbt commands that are supported in dbt Projects on Snowflake. Any [dbt command](https://docs.getdbt.com/reference/dbt-commands) that isn’t listed here isn’t supported.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

> **dbt Projects on Snowflake, supported dbt commands by execution method**
>
> | dbt command | Workspaces | EXECUTE DBT PROJECT | `snow dbt execute` (CLI) |
> | --- | --- | --- | --- |
> | [build](https://docs.getdbt.com/reference/commands/build) | ✔ | ✔ | ✔ |
> | [clean](https://docs.getdbt.com/reference/commands/clean) [3] | ✔ | ✔ | ✔ |
> | [compile](https://docs.getdbt.com/reference/commands/compile) | ✔ | ✔ | ✔ |
> | [deps](https://docs.getdbt.com/reference/commands/deps) [1] | ✔ | ✔ | ✔ |
> | [docs generate](https://docs.getdbt.com/reference/commands/cmd-docs#dbt-docs-generate)  [2] | ✔ | ✔ | ❌ |
> | [list](https://docs.getdbt.com/reference/commands/list) | ✔ | ✔ | ✔ |
> | [parse](https://docs.getdbt.com/reference/commands/parse) | ❌ | ✔ | ✔ |
> | [run](https://docs.getdbt.com/reference/commands/run) | ✔ | ✔ | ✔ |
> | [retry](https://docs.getdbt.com/reference/commands/retry) [3] | ✔ | ✔ | ✔ |
> | [run-operation](https://docs.getdbt.com/reference/commands/run-operation) | ✔ | ✔ | ✔ |
> | [seed](https://docs.getdbt.com/reference/commands/seed) | ✔ | ✔ | ✔ |
> | [show](../reference/java/com/snowflake/snowpark_java/DataFrame.html#show(int)) | ✔ | ✔ | ✔ |
> | [snapshot](https://docs.getdbt.com/reference/commands/snapshot) | ✔ | ✔ | ✔ |
> | [source freshness](https://docs.getdbt.com/reference/commands/source)  [3] | ✔ | ✔ | ✔ |
> | [test](https://docs.getdbt.com/reference/commands/test) | ✔ | ✔ | ✔ |
>
> Expand
>
> Show lessSee more

[1] With `AUTO_COMPILE = TRUE`, Snowflake runs `dbt compile` during deployment. If an external access integration is configured, Snowflake first runs `dbt deps`, then `dbt compile`. Setting `AUTO_COMPILE = FALSE` skips both commands.

[2] dbt Projects on Snowflake don’t support dbt docs serve. To view your project’s documentation, use the dbt project object details page in Snowsight, or generate a static site with `dbt docs generate --static`. For more information, see [Access dbt project documentation and artifacts](/user-guide/data-engineering/dbt-projects-on-snowflake-manage#label-dbt-project-documentation-artifacts).

[3] Requires a dbt project object that uses the mutable `live` version.

## About flags

In dbt Core, you run commands (for example, `dbt build`) and modify their behavior with flags. Flags are configuration options that modify how a command behaves; some are command-specific, others are global. For more information, see [flags](https://docs.getdbt.com/reference/global-configs/about-global-configs).

You always run a command, and you attach flags to scope or alter it. For example, to run only incremental models and rebuild them, you would run the following command and flags:

Copy code

```
dbt run --select config.materialized:incremental --full-refresh;
```

The [`--log-level-file`](https://docs.getdbt.com/reference/global-configs/logs#log-level) flag is supported and controls the verbosity of `dbt.log` which our Snowsight UI uses; it defaults to `debug`, so pass `--log-level-file info` for quieter output.

The following flags aren’t supported in dbt Projects on Snowflake:

- `--profiles-dir`
- `--project-dir`
- `--log-format`
- `--log-format-file`

The paths specified by `--target-path` and `--log-path` must point to directories inside the project. Snowflake recommends pointing to
dedicated subdirectories to avoid uploading unrelated project files with the execution results.
The `WRITEBACK` setting controls whether an execution writes target and log artifacts to the live version. For concurrent executions with
writeback enabled, use distinct, non-overlapping target and log directories. For details, see
[Use distinct target and log paths](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod#label-dbt-project-distinct-target-log-paths).

## Clean a dbt project object

The `clean` command removes selected target directories from the live version. Cleanup is all or nothing. If Snowflake detects a protected
path or files that change while cleanup is running, it stops, removes nothing, and returns an error.

The paths selected by `clean` depend on your dbt runtime and configuration:

- If `clean-targets` is configured and you don’t pass `--target-path`, dbt cleans the configured paths.
- If `clean-targets` isn’t configured, dbt uses its default clean targets and includes the path passed with `--target-path`.
- If both `clean-targets` and `--target-path` are set, dbt Core cleans only the paths in `clean-targets`. dbt Fusion cleans the union of `clean-targets` and `--target-path`.

If you execute `clean` with `WRITEBACK = FALSE`, the command doesn’t update files on the live version. This is effectively a no-op. Files removed by `clean` cannot be recovered.
