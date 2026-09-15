# Oct 09, 2025: dbt Projects on Snowflake: Recent improvements (*Preview*)

dbt Projects on Snowflake now support the following functionalities:

- [dbt Project failures show up as failed queries](#label-10-09-dbt-failed-queries)
- [Compile on create](#label-10-09-dbt-compile-on-create)
- [Install deps on compile](#label-10-09-dbt-deps-on-compile)
- [MONITOR privilege](#label-10-09-dbt-monitor-priv)
- [Accessing execution results is easier](#label-10-09-dbt-access-execution-results)

## dbt Project failures show up as failed queries

Any dbt Project errors — like compile or test failures — now appear as query failures. This makes it easier to handle them with tasks or
other orchestration tools. You can view detailed logs using `SELECT SYSTEM$get_dbt_log('<query_id>')`.

Important

This might cause a breaking change for anyone relying on the previous method of checking the return values to determine dbt Project
execution outcomes.

## Compile on create

Whenever you deploy or update a dbt Project object, it’s automatically compiled so build artifacts are up to date and Snowsight works
smoothly.

This could cause a breaking change if you’re deploying projects that fail during compilation.

Compilation currently uses the profile in your `profiles.yml` by default. As a workaround, you can update your `profiles.yml`
prior to deployment to point to the production target before deploying. In a future release, you’ll be able to override this with
`DEFAULT_TARGET` on the Project object.

## Install deps on compile

You can optionally run `dbt deps` during deployment to install project dependencies by setting `EXTERNAL_ACCESS_INTEGRATIONS=[...ext]`
on your deploy or update commands. This means you no longer need to include `/dbt_packages` when deploying projects with external
dependencies.

In a future release, compile on create will support the `local:` syntax.

## MONITOR privilege

dbt Projects now support the MONITOR privilege. This allows you to see the execution history, download the build artifacts of a dbt Project
object and download build artifacts of each dbt Project execution. This privilege can be granted at the DATABASE or SCHEMA level.

## Accessing execution results is easier

You can download build artifacts directly from the **Query History** page or use the following new system functions:

- *SELECT SYSTEM$LOCATE\_DBT\_ARTIFACTS($latest\_query\_id)*: Returns the file path for dbt Project artifacts from a run (for example, `snow://dbt/DB_TEST.PUBLIC.DBT_PROJECT_TEST/results/query_id_01bf3f5a-010b-4d87-0000-53493abb7cce/`).
- *SELECT SYSTEM$LOCATE\_DBT\_ARCHIVE($latest\_query\_id)*: Returns the location of the dbt Project output archive zip.
- *SELECT SYSTEM$GET\_DBT\_LOG($latest\_query\_id)*: Returns the last 1000 lines of the `dbt.log` file. For full logs, download the archive zip.

Use the Snowflake CLI to download these artifacts from the results stage, for example:

Copy code

```
snowsql -q “GET 'snow://dbt_project/DB_TEST.PUBLIC.DBT_PROJECT_TEST/results/query_id_01bf3f89-0300-0001-0000-0000000c1229/dbt_artifacts.zip' file:///Users/user_name/Code/temp"
```

This new approach replaces `OUTPUT_ARCHIVE_URL` and improves interoperability with Snowflake CLI and other services.

Important

dbt Project output logs from executions before this release won’t appear on the **Query History** page.

For more information, see [dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake).
