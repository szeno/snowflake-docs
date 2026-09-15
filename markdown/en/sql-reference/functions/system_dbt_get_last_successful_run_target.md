Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$DBT\_GET\_LAST\_SUCCESSFUL\_RUN\_TARGET

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

Returns the location of dbt artifacts from the most recent successful
execution of a dbt project object within the previous 7 days. You can import these artifacts into
another dbt project execution and use them with `--state`.

## Syntax

Copy code

```
SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET (
  '<object_name>'
  [ , '<commands>' [ , '<target_path>' ] ]
)
```

## Arguments

`object_name`
:   String that specifies the fully qualified name of the dbt project object whose dbt artifacts you
    want to retrieve.

`commands`
:   Optional comma-separated list of dbt commands to include when searching execution history. The
    default list is `compile`, `build`, `run`, and `docs generate`.

    For a compound command, specify the command and its subcommand, such as `docs generate`.

`target_path`
:   Optional target path to match. When specified, the function considers only executions that used
    that target path.

## Returns

Returns the location of dbt artifacts produced by the object’s most recent successful qualifying
execution. Use the location with the `IMPORTS` parameter of
[EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project) or the Snowflake CLI `--import` option.

Returns `NULL` if no qualifying execution with a populated target directory is available in the
lookback window.

## Access control requirements

The role used to call this function must have the `MONITOR` privilege on the dbt project object.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The dbt project object must have completed a successful execution within the previous 7 days.
- Deployment-time auto compile doesn’t create dbt artifacts for this function. Complete a qualifying execution after deployment.
- This function locates reusable dbt artifacts by dbt project object and is the typical system function for Slim CI.
  [SYSTEM$LOCATE\_DBT\_ARTIFACTS](/sql-reference/functions/system_locate_dbt_artifacts) and
  [SYSTEM$LOCATE\_DBT\_ARCHIVE](/sql-reference/functions/system_locate_dbt_archive) locate artifacts or an archive for a
  specific query ID instead.
- `--import` or `IMPORTS` makes the returned dbt artifacts available to an execution. You must also
  point dbt to the mounted directory with `--state`.

## Examples

Return the location of dbt artifacts from the most recent successful execution of a production dbt
project object:

Copy code

```
SELECT SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET(
  'prod_database.dbt_projects.production_project'
);
```

Import the returned dbt artifacts as `state`, which mounts them at `./imports/state`, and use them
for a Slim CI run:

Copy code

```
EXECUTE DBT PROJECT ci_database.dbt_projects.pr_test_project
  ARGS = 'run --state ./imports/state --defer --select state:modified+'
  IMPORTS = (
    SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET(
      'prod_database.dbt_projects.production_project'
    ) AS 'state'
  );
```

Import dbt artifacts from the most recent successful execution that used `--target-path my_target`.
To retain the default command filter when you specify a target path, pass the default command list
as the second argument:

Copy code

```
EXECUTE DBT PROJECT ci_database.dbt_projects.pr_test_project
  ARGS = 'run --state ./imports/state --defer --select state:modified+'
  IMPORTS = (
    SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET(
      'prod_database.dbt_projects.production_project',
      'compile,build,run,docs generate',
      'my_target'
    ) AS 'state'
  );
```
