Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions), [Table functions](/sql-reference/functions-table)

# DCM\_DEPLOYMENT\_HISTORY

This table function returns the deployment history for DCM project objects. You can use it to
query successful and failed deployments, including timestamps, status, error details, and summary
statistics. The function provides role-based access and low-latency results.

## Syntax

Copy code

```
DCM_DEPLOYMENT_HISTORY(
      [ PROJECT_NAME => '<string>' ]
      [, START_TIME_RANGE_START => <constant_expr> ]
      [, START_TIME_RANGE_END => <constant_expr> ]
      [, RESULT_LIMIT => <integer> ] )
```

## Arguments

All arguments are optional.

`PROJECT_NAME => 'string'`
:   Fully qualified name of the DCM project. If not provided, the function returns history for all
    projects accessible by the current role.

`START_TIME_RANGE_START => constant_expr`
:   Timestamp (in TIMESTAMP\_LTZ format) marking the start of the time range for retrieving
    deployment events.

    Default: 7 days ago.

`START_TIME_RANGE_END => constant_expr`
:   Timestamp (in TIMESTAMP\_LTZ format) marking the end of the time range for retrieving
    deployment events.

    Default: current timestamp.

`RESULT_LIMIT => integer`
:   Maximum number of rows to return.

    Default: `10000`.

## Output

The function returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `QUERY_UUID` | VARCHAR | Unique identifier of the query that executed the deployment. |
| `PROJECT_NAME` | VARCHAR | Name of the DCM project that was deployed. |
| `START_TIMESTAMP` | TIMESTAMP\_LTZ | Timestamp of when the deployment execution started. |
| `END_TIMESTAMP` | TIMESTAMP\_LTZ | Timestamp of when the deployment execution completed or failed. |
| `DEPLOYMENT_NAME` | VARCHAR | Internal deployment identifier (for example, `DEPLOYMENT$1`, `DEPLOYMENT$2`). |
| `DEPLOYMENT_ALIAS` | VARCHAR | User-specified alias for the deployment. Empty if no alias was provided. |
| `STATUS` | VARCHAR | Status of the deployment. Possible values: `EXECUTING`, `SUCCESSFUL`, `FAILED`, `CANCELED`. `EXECUTING` indicates that the deployment is still in progress; the other values are terminal states. |
| `PHASE` | VARCHAR | The phase of the execution. Possible values: `PLAN`, `DEPLOY`, `INIT`. |
| `CONFIGURATION_PROFILE` | VARCHAR | Name of the configuration profile used for the deployment. Empty if no configuration was specified. |
| `ERROR_MESSAGE` | VARCHAR | Error message if the deployment failed. Empty for successful deployments. |
| `ERROR_CODE` | VARCHAR | Error code if the deployment failed. Empty for successful deployments. |
| `DATABASE_NAME` | VARCHAR | Database that contains the DCM project. |
| `SCHEMA_NAME` | VARCHAR | Schema that contains the DCM project. |
| `EXECUTOR_ROLE` | VARCHAR | Role that executed the deployment command. |
| `STATS` | VARIANT | JSON object containing summary statistics of the deployment, broken down by category. Each category contains counts of `created`, `altered`, and `dropped` items. Categories include `entities` (managed objects), `columns`, `grants`, and `dmfAttachments` (data metric function expectations). |

Expand

Show lessSee more

## Usage notes

- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA
  schema in use or the function name must be fully qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).
- This function returns deployments from the past 12 months only. There is no ACCOUNT\_USAGE view
  equivalent for DCM deployment history.
- For long-term retention and deletion behavior, see
  [Deployment artifacts](/user-guide/dcm-projects/dcm-projects-monitor#label-dcm-projects-deployment-artifacts).

## Examples

Retrieve deployment history for a specific project, limited to 3 results:

> Copy code
>
> ```
> SELECT
>   PROJECT_NAME,
>   START_TIMESTAMP,
>   DEPLOYMENT_NAME,
>   DEPLOYMENT_ALIAS,
>   STATUS,
>   CONFIGURATION_PROFILE,
>   EXECUTOR_ROLE
> FROM
>   TABLE (MY_DB.INFORMATION_SCHEMA.DCM_DEPLOYMENT_HISTORY(
>     project_name => 'MY_DB.PROJECTS.MY_PROJECT',
>     result_limit => 3
>   ));
> ```
>
> ```
> +----------------+-----------------------------+--------------+------------------+------------+-----------------------+------------------+
> | PROJECT_NAME   | START_TIMESTAMP             | DEPLOYMENT   | DEPLOYMENT       | STATUS     | CONFIGURATION_PROFILE | EXECUTOR_ROLE    |
> |                |                             | _NAME        | _ALIAS           |            |                       |                  |
> +----------------+-----------------------------+--------------+------------------+------------+-----------------------+------------------+
> | MY_PROJECT     | 2026-03-20 09:15:22.254     | DEPLOYMENT$3 | staging update   | SUCCESSFUL | STAGE                 | PROJECT_DEPLOYER |
> | MY_PROJECT     | 2026-03-19 14:30:10.927     | DEPLOYMENT$2 |                  | FAILED     | DEV                   | PROJECT_DEPLOYER |
> | MY_PROJECT     | 2026-03-18 11:00:05.339     | DEPLOYMENT$1 | initial deploy   | SUCCESSFUL | DEV                   | PROJECT_DEPLOYER |
> +----------------+-----------------------------+--------------+------------------+------------+-----------------------+------------------+
> ```

The `STATS` column contains a JSON object with the following structure:

> ```
> {
>   "columns": {
>     "altered": 0,
>     "created": 12,
>     "dropped": 0
>   },
>   "dmfAttachments": {
>     "altered": 0,
>     "created": 2,
>     "dropped": 0
>   },
>   "entities": {
>     "altered": 1,
>     "created": 5,
>     "dropped": 0
>   },
>   "grants": {
>     "altered": 0,
>     "created": 4,
>     "dropped": 0
>   }
> }
> ```

Retrieve all columns for all projects accessible by the current role within the last 24 hours:

> Copy code
>
> ```
> SELECT *
> FROM TABLE (INFORMATION_SCHEMA.DCM_DEPLOYMENT_HISTORY(
>   start_time_range_start => DATEADD(hours, -24, CURRENT_TIMESTAMP())
> ));
> ```
