Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$LOCATE\_DBT\_ARCHIVE

Returns the URL from which you can retrieve zipped dbt run artifacts for a specified dbt project object.

Use this function with the [DBT\_PROJECT\_EXECUTION\_HISTORY](/sql-reference/functions/dbt_project_execution_history) function to access dbt artifacts and logs programmatically.

## Syntax

Copy code

```
SYSTEM$LOCATE_DBT_ARCHIVE ( '<query_id>' )
```

## Arguments

`query_id`
:   The query ID of the dbt project object run whose files you want to locate.

## Returns

This function returns the URL of `dbt_artifacts.zip` for a specified dbt project object run. The archive contains the full target
directory, including compiled SQL and files that aren’t uploaded separately, plus execution logs.

Use `SYSTEM$LOCATE_DBT_ARCHIVE` directly when you need the archived target and logs, such as compiled SQL. When you import the
archive returned by this function `AS 'state'` in the `IMPORTS` clause of [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project), Snowflake extracts it
automatically at `./imports/state`, with the dbt artifacts in `./imports/state/target`. An execution can automatically extract at most one
ZIP file. Importing the full archive can take longer than importing standalone artifacts.

[SYSTEM$LOCATE\_DBT\_ARTIFACTS](/sql-reference/functions/system_locate_dbt_artifacts), on the other hand, returns the results directory. When used in `IMPORTS`,
`SYSTEM$LOCATE_DBT_ARTIFACTS` imports the results directory, including `dbt_artifacts.zip`, but doesn’t extract the ZIP file.

For more information and examples, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).

## Access control requirements

This function can only be used with dbt project objects, not Workspaces, when you have one of the following privileges:

- OWNERSHIP, USAGE, or MONITOR on the dbt project object

For details about these privileges, see [dbt project object privileges](/user-guide/security-access-control-privileges#label-access-control-privs-dbt).

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- This system function works only on dbt project objects and isn’t available for Workspaces.
- Query IDs generated from CREATE DBT PROJECT or ALTER DBT PROJECT … DEPLOY aren’t supported for this system function.
- Direct querying of file content (for example, [Query examples](/user-guide/querying-stage#label-querying-stage-query-examples)) isn’t supported.
- If `query_id` is NULL or not a dbt execution, you’ll get an error.
- dbt project results are available for up to 14 days.
- Files might be unavailable if a run times out, is canceled, or fails before they are uploaded. In such cases, runs appear as `UNHANDLED ERROR` in dbt history.
- You can’t use this function to locate the archive for runs that are in progress because the archive is only available after the run is complete.

## Examples

The following example returns the `snow://` URL of the zipped artifacts (for example, `dbt_artifacts.zip`) for the specified execution.

You can use this URL with GET to download the ZIP file (or COPY FILES to move it to your own stage). For the folder path instead of the ZIP, use
[SYSTEM$LOCATE\_DBT\_ARTIFACTS](/sql-reference/functions/system_locate_dbt_artifacts).

Copy code

```
SELECT SYSTEM$LOCATE_DBT_ARCHIVE($latest_query_id);
```

For more information, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).
