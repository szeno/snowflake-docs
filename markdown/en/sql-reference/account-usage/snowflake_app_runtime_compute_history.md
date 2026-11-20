Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SNOWFLAKE\_APP\_RUNTIME\_COMPUTE\_HISTORY view

The SNOWFLAKE\_APP\_RUNTIME\_COMPUTE\_HISTORY view in the ACCOUNT\_USAGE schema returns
the hourly compute credit usage for
[Snowflake App Runtime](/developer-guide/snowflake-app-runtime/about-snowflake-app-runtime)
in an account within the last 365 days (1 year).

Each row is one hour of usage for one compute type. Use `COMPUTE_TYPE` to tell the rows apart:

- `MANAGED COMPUTE POOL`: account-level usage on the shared Snowflake-managed compute pool.
  `COMPUTE_POOL_NAME` is `SNOWFLAKE_APP_RUNTIME_COMPUTE`. The application service and user
  columns are NULL. Per-app cost attribution isn’t available for these rows.
- `SERVERLESS`: usage attributed to one application service. `APPLICATION_SERVICE_ID` and
  `APPLICATION_SERVICE_NAME` identify the service. `COMPUTE_POOL_NAME` and `USER_ID` are NULL.
- `PREVIEW`: usage attributed to the user who ran a Snowflake App Runtime preview on Workspaces.
  `USER_ID` identifies that user. `COMPUTE_POOL_NAME` and the application service columns are NULL.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the usage took place. |
| COMPUTE\_POOL\_NAME | VARCHAR | Name of the Snowflake-managed compute pool. `SNOWFLAKE_APP_RUNTIME_COMPUTE` when `COMPUTE_TYPE` is `MANAGED COMPUTE POOL`; NULL for serverless and preview rows. |
| CREDITS\_USED | NUMBER | Number of credits used for this row in the hour. |
| APPLICATION\_SERVICE\_ID | NUMBER | Identifier of the application service. Populated when `COMPUTE_TYPE` is `SERVERLESS`; otherwise NULL. |
| APPLICATION\_SERVICE\_NAME | VARCHAR | Name of the application service. Populated when `COMPUTE_TYPE` is `SERVERLESS`; otherwise NULL. |
| USER\_ID | NUMBER | Identifier of the user associated with the usage. Populated when `COMPUTE_TYPE` is `PREVIEW`; otherwise NULL. |
| COMPUTE\_TYPE | VARCHAR | Kind of App Runtime compute for the row: `MANAGED COMPUTE POOL`, `SERVERLESS`, or `PREVIEW`. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- Managed compute pool rows are one row per account per hour. Serverless rows are one application
  service per hour. Preview rows are one user per hour.
- Credit usage reported here is also included in
  [METERING\_HISTORY](/sql-reference/account-usage/metering_history) and
  [METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history).
  `SERVICE_TYPE` in those views depends on `COMPUTE_TYPE`:
  - `MANAGED COMPUTE POOL` is reported as `SNOWFLAKE_APP_RUNTIME`.
  - `SERVERLESS` is reported as `SNOWFLAKE_APP_RUNTIME_SERVERLESS`.
  - `PREVIEW` is reported as `SNOWFLAKE_APP_RUNTIME_PREVIEW`.

## Examples

Return daily Snowflake App Runtime credit usage for the last 30 days:

Copy code

```
SELECT
    DATE(start_time) AS usage_date,
    SUM(credits_used) AS credits_used
FROM snowflake.account_usage.snowflake_app_runtime_compute_history
WHERE start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY usage_date
ORDER BY usage_date DESC;
```

Return daily credit usage by compute type and application service for the last 30 days:

Copy code

```
SELECT
    DATE(start_time) AS usage_date,
    compute_type,
    application_service_name,
    SUM(credits_used) AS credits_used
FROM snowflake.account_usage.snowflake_app_runtime_compute_history
WHERE start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY usage_date, compute_type, application_service_name
ORDER BY usage_date DESC;
```
