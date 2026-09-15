# SHOW CORTEX BASE MODELS

Lists the Cortex Base Models available to your current role, along with their lifecycle
status, in-region and cross-region availability, legacy date, and end-of-life date.

Cortex Base Models are the LLMs that Snowflake provides for use with
[Cortex AI Functions](/user-guide/snowflake-cortex/aisql) and related features.
Unlike [SHOW MODELS](/sql-reference/sql/show-models), which lists all model objects
(including user-created models), this command is scoped to Cortex Base Models and
returns additional columns that describe each model’s lifecycle stage and
availability. Use this command to determine which models are currently available to
your current role.

See also:
:   [SHOW MODELS](/sql-reference/sql/show-models)

## Syntax

Copy code

```
SHOW CORTEX BASE MODELS
  [ LIKE '<pattern>' ]
  [ IN [ SCHEMA ] SNOWFLAKE.MODELS ]
  [ STARTS WITH '<name_string>' ]
  [ LIMIT <rows> ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN [ SCHEMA ] SNOWFLAKE.MODELS`
:   Scopes the command to the `SNOWFLAKE.MODELS` schema, where all Cortex Base Model
    objects are stored. Snowflake recommends specifying this clause.

    If you omit this clause, the command follows standard SHOW scoping:

    - If the session has a current database, the command is scoped to that database
      (and to the current schema, if one is set). Cortex Base Models exist only in
      `SNOWFLAKE.MODELS`, so an unqualified command returns no rows when another
      database is current, even if the current role has the required model privileges.
    - If the session has no current database, the command uses account scope and can
      return Cortex Base Models.

    To list Cortex Base Models regardless of the session’s current database, specify
    `IN SCHEMA SNOWFLAKE.MODELS`.

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

## Output

The command output provides the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the model object was created. |
| `name` | Name of the Cortex Base Model. |
| `model_type` | Type of the model object. For Cortex Base Models, this is `CORTEX_BASE`. |
| `database_name` | Database in which the model is stored. |
| `schema_name` | Schema in which the model is stored. |
| `owner` | Role that owns the model object. |
| `lifecycle_status` | Current lifecycle stage of the model, or `NULL` for models that have not yet been assigned a lifecycle stage. Possible values:   - `GA`: Generally available. The model is fully supported and recommended for production use. - `PUPR`: Public preview. The model is available to all accounts but may have limitations.   See [Snowflake Preview Features](/release-notes/preview-features) for details. - `PRPR`: Private preview. The model is available to accounts that have been specifically enabled. - `LEGACY`: The model has entered its legacy period. Accounts that used the   model before the legacy date can continue to use it until end-of-life.   Accounts that had not used the model can’t start using it. Using this   model is not recommended. Migrate to a supported model before its   end-of-life. For details, see   [Model lifecycle: legacy and end-of-life](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-model-lifecycle). - `EOL`: End of life. The model is no longer available to any account.   Queries and API calls that name the model fail. |
| `in_region_availability` | Array of Snowflake regions where the model is deployed and served directly in that region (without cross-region inference), for example `["AWS_US_EAST_1", "AZURE_EASTUS2"]`. For a complete list of region identifiers, see [Models and regional availability for Cortex AI Functions](/user-guide/snowflake-cortex/aisql-regional-availability).  This column is `NULL` for models that Snowflake doesn’t host directly in any region. Those models are available only through [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference); see the `cross_region_availability` column. Models with no active in-region deployment, such as models with `EOL` status, have an empty array. |
| `legacy_date` | The date the model entered or will enter its legacy period, as a free-form string. `NULL` if the model has not been marked as legacy. |
| `eol_date` | The end-of-life indicator for the model, as a free-form string. This is typically a date (for example, `2026-04-28`), but it can also be descriptive text (for example, `No sooner than 2027/01/01`). `NULL` if no end-of-life has been set. |
| `cross_region_availability` | Array of the [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) settings from which the model can be reached, for example `["ANY_REGION", "AWS_US", "AWS_EU", "AWS_APJ"]`. These correspond to the values you can set for the [CORTEX\_ENABLED\_CROSS\_REGION](/sql-reference/parameters#label-cortex-enable-cross-region) parameter. When the list isn’t empty, it always includes `ANY_REGION`. `NULL` if the model has no cross-region availability. |

Expand

Show lessSee more

## Access control requirements

The output is filtered based on the user’s model RBAC grants. Only models for
which the current role has been granted access appear in the results. If the
command is scoped to a database other than `SNOWFLAKE`, the result can be empty
even when those grants exist. For information about granting access to Cortex
Base Models, see
[Model access and privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access).

Note

The `SNOWFLAKE.MODELS` schema is automatically populated with Cortex Base Model objects and is refreshed daily by the
Snowflake-managed task `SNOWFLAKE.MODELS.CORTEX_BASE_MODELS_REFRESH_TASK`. Intermittent `FAILED` runs of that task in
[TASK\_HISTORY](/sql-reference/functions/task_history) don’t require action; the next daily run typically succeeds.
If you want to see newly available models immediately without waiting for the next daily refresh, an `ACCOUNTADMIN` can
run the refresh stored procedure on demand:

Copy code

```
CALL SNOWFLAKE.MODELS.CORTEX_BASE_MODELS_REFRESH();
```

For details, see [Refresh model objects and application roles](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-base-models-refresh-task).

## Usage notes

- Cortex Base Models exist only in `SNOWFLAKE.MODELS`. Use
  `SHOW CORTEX BASE MODELS IN SCHEMA SNOWFLAKE.MODELS` so the command isn’t
  scoped to the session’s current database. Omitting `IN SCHEMA SNOWFLAKE.MODELS`
  can return zero rows even when the current role has the correct
  `CORTEX-MODEL-ROLE-*` grants.
- This command returns only Cortex Base Models. To list all model objects in
  your account, including Cortex Base Models and user models, use
  [SHOW MODELS](/sql-reference/sql/show-models).
- A model that appears in the results with a region in `in_region_availability`
  may still be unavailable to invoke if your account is in a different region and
  cross-region inference is not enabled. Use the `cross_region_availability`
  column to see which cross-region settings can reach the model. See
  [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference).

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

List all Cortex Base Models accessible to the current role. Specify
`IN SCHEMA SNOWFLAKE.MODELS` so the listing isn’t limited to the session’s
current database:

Copy code

```
SHOW CORTEX BASE MODELS IN SCHEMA SNOWFLAKE.MODELS;
```

List Cortex Base Models whose names contain `claude`:

Copy code

```
SHOW CORTEX BASE MODELS LIKE '%claude%' IN SCHEMA SNOWFLAKE.MODELS;
```
