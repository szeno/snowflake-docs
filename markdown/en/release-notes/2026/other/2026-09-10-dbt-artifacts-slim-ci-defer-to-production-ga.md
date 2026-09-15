# Sep 10, 2026: Using dbt artifacts for Slim CI and defer to production in dbt Projects on Snowflake (*General availability*)

Slim CI, defer to production, failed-execution recovery, and concurrent
execution are now generally available for dbt Projects on Snowflake. Reuse dbt artifacts from recent production
executions to accelerate development, streamline CI/CD workflows, and recover from failed
production runs without maintaining a separate artifact store.

With this release, you can:

- **Run Slim CI:** Import dbt artifacts from the latest successful production execution, then use
  `--state` and `--select state:modified+` to validate only changed resources and their downstream
  dependencies. This reduces CI execution time and warehouse use.
- **Defer to production:** Use defer to production in Snowflake Workspaces or with Snowflake CLI to
  resolve unbuilt upstream references to existing production relations instead of rebuilding
  unchanged models in an isolated development or CI target.
- **Build complete CI/CD workflows on Snowflake:** Use Snowflake CLI and Snowflake system functions
  to separate deployment from execution, create an isolated database for each pull request, and
  retrieve recent or query-specific dbt artifacts. Record the Git branch and commit for each
  deployment so that a dbt project object remains traceable to its source.
- **Run one project concurrently:** Execute independent slices of the same deployed dbt project
  object at different cadences without maintaining duplicate objects. Use `DEFAULT_WRITEBACK` or
  the per-execution `WRITEBACK` setting to prevent concurrent executions from writing to shared
  live target and log paths. Alternatively, give each concurrent execution a distinct
  `--target-path` and `--log-path`.
- **Recover efficiently from failed executions:** Reuse artifacts from the latest failed run with
  selectors such as `result:error+`, so you can rerun errored resources and their downstream
  dependencies without repeating work that already succeeded.
- **Choose when and how to compile:** Skip automatic compilation during deployment with
  `AUTO_COMPILE = FALSE` or Snowflake CLI `--no-auto-compile` to take advantage of Slim CI and
  simplify governance with a deploy-only role.

These workflows require dbt project objects to use a
[single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362). Until the 2026\_06
behavior change bundle is generally enabled, enable the bundle in your account to opt in. When
enabled, new and recreated objects use the live version, and you can migrate existing versioned
objects with [`SYSTEM$MIGRATE_DBT_PROJECT`](/sql-reference/functions/system_migrate_dbt_project).
Once the bundle is generally enabled, Snowflake will automatically migrate all remaining versioned
objects.

For more information, see:

- [Use dbt artifacts for Slim CI and defer to production](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod)
- [Tutorial: Set up CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-advanced-ci-cd-tutorial)
- [Best practices for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices)
- [Live version for dbt project objects and files](/user-guide/data-engineering/dbt-projects-on-snowflake-live-version)
