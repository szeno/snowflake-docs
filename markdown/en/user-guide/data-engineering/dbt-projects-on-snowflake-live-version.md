# Live version for dbt project objects and files

A dbt project object has one mutable version named `live`. Creating an object creates the live version, and each later deployment replaces
the same live version.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

Note

The `live` object version is distinct from the dbt runtime version used for execution. For information about dbt Core and dbt Fusion runtime versions, see [Supported dbt versions for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions).

Snowflake stores the live version in the dbt project stage at a path in the following form:

```
snow://dbt/<database>.<schema>.<project>/versions/live
```

For example, the following path references the `dbt_project.yml` file in a project named `my_dbt_project_object`:

```
snow://dbt/my_db.my_schema.my_dbt_project_object/versions/live/dbt_project.yml
```

The `live` identifier always refers to the current contents of the object.

## Create or update the live version

The following operations create or update the live version:

- `CREATE DBT PROJECT` creates a new object and its live version.
- `ALTER DBT PROJECT ... DEPLOY` replaces the contents of an existing live version.
- `snow dbt deploy` creates the object if it doesn’t exist or updates its live version if it does.

Warning

Don’t use `--force` unless you intentionally want to recreate the dbt project object. In `snow dbt deploy`, `--force` runs `CREATE OR REPLACE DBT PROJECT`, which may remove run history.

Deployment replaces the entire live version in a single operation, including existing target and log artifacts. Executions see either the
complete previous deployment or the complete new deployment, never a partially updated project.

For deployment procedures, see [Deploy dbt project objects](/user-guide/data-engineering/dbt-projects-on-snowflake-deploy).

Writeback controls whether an execution writes generated target and log artifacts to the live version. An execution uses the object’s
`DEFAULT_WRITEBACK` setting unless you override it with `WRITEBACK`. Snowflake stores separate per-query result artifacts and their archive
under the object’s `results` directory regardless of the writeback setting.

## Copy files to or from the live version

Use [COPY FILES](/sql-reference/sql/copy-files) or [snow dbt copy](/developer-guide/snowflake-cli/command-reference/dbt-commands/copy) to copy files between an internal stage and the live version:

Copy code

```
COPY FILES
  INTO 'snow://dbt/my_db.my_schema.my_dbt_project/versions/live/state_backup/'
  FROM @my_db.my_schema.my_stage/state/;

COPY FILES
  INTO @my_db.my_schema.my_stage/project_backup/
  FROM 'snow://dbt/my_db.my_schema.my_dbt_project/versions/live/';
```

You can also use [GET](/sql-reference/sql/get) and [PUT](/sql-reference/sql/put) with a `versions/live` path to download or upload files.

These operations persistently modify or copy the live files. In contrast, the `IMPORTS` clause of `EXECUTE DBT PROJECT` and the Snowflake CLI `--import` option mount read-only files under `./imports` for one execution.
