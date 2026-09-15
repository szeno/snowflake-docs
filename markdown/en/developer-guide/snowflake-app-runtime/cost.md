# Cost and credit usage for Snowflake App Runtime

This topic describes how Snowflake bills compute used by
[Snowflake App Runtime](/developer-guide/snowflake-app-runtime/about-snowflake-app-runtime)
and where to track that usage.

## How App Runtime compute is billed

Snowflake App Runtime uses a dedicated service type:

| Service type | Description |
| --- | --- |
| `SNOWFLAKE_APP_RUNTIME` | Compute used to build and host Snowflake App Runtime services. |

Expand

Show lessSee more

All apps in an account share a single Snowflake-managed compute pool. Credit
usage is billed at the account level under the `SNOWFLAKE_APP_RUNTIME` service
type, separate from your warehouses and other compute. Per-app cost
attribution isn’t available.

### Credit rate

App Runtime credits are charged per compute-hour at the rate listed in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
under “Serverless Feature Credit Table” for the `SNOWFLAKE_APP_RUNTIME` service
type. The managed compute pool uses `CPU_X64_S` nodes (3 vCPU, 13 GiB RAM).
This rate reflects a discount relative to the equivalent self-managed SPCS
compute pool node rate.

You aren’t billed per request or per concurrent user. Cost depends on how
long the underlying compute nodes run, regardless of whether your app is
handling traffic.

You pay for nodes, not instances. App Runtime packs multiple instances onto
a node when resource requests allow it, so a new node is added only when
existing ones are full.

### Billing lifecycle

App Runtime billing follows the same lifecycle as SPCS compute pools. For
details on how costs accrue in each state (ACTIVE, IDLE, SUSPENDED), see
[Compute pool cost](/developer-guide/snowpark-container-services/accounts-orgs-usage-views#label-compute-pool-cost).

Apps left running while idle still accrue credits. To stop an app you don’t
need, see [Scale and suspend Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/scale-and-suspend).

## Find App Runtime usage in metering views

App Runtime credits appear in the same metering views that report other
Snowflake compute usage:

- [METERING\_HISTORY](/sql-reference/account-usage/metering_history): hourly
  credit usage for the last 365 days.
- [METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history):
  daily credit usage rolled up by service type.

For cross-account roll-ups, use organization-level metering views such as
[USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily).

The following query returns hourly App Runtime credit usage for the last 30 days:

Copy code

```
SELECT
    start_time,
    end_time,
    credits_used_compute
FROM snowflake.account_usage.metering_history
WHERE service_type = 'SNOWFLAKE_APP_RUNTIME'
  AND start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

## Inspect App Runtime credit usage

For a focused view of App Runtime credit usage, query
[SNOWFLAKE\_APP\_RUNTIME\_COMPUTE\_HISTORY](/sql-reference/account-usage/snowflake_app_runtime_compute_history).
The view returns hourly account-level credit usage for App Runtime over the
last 365 days.

Copy code

```
SELECT
    start_time,
    end_time,
    credits_used
FROM snowflake.account_usage.snowflake_app_runtime_compute_history
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

## Reduce App Runtime cost

App Runtime apps run continuously once created. An app that is deployed but
not actively used still consumes compute until it is suspended or dropped. To
control cost:

- **Suspend idle apps.** Suspending releases compute for apps not in active
  use. Lowering instance counts doesn’t: a running service keeps at least one
  instance. See [Scale and suspend Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/scale-and-suspend).
- **Drop unused apps.** Use
  [`DROP APPLICATION SERVICE`](/sql-reference/sql/drop-application-service)
  to permanently remove apps you no longer need.
- **Monitor app state.** Use
  [Observability for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/observability)
  to find apps stuck in unexpected states that may still be consuming compute.

## See also

- [Observability for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/observability): service state and
  logs.
- [Scale and suspend Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/scale-and-suspend): instance counts
  and suspend.
- [SNOWFLAKE\_APP\_RUNTIME\_COMPUTE\_HISTORY view](/sql-reference/account-usage/snowflake_app_runtime_compute_history):
  hourly App Runtime credit usage view.
- [Understanding compute cost](/user-guide/cost-understanding-compute): general cost concepts for
  Snowflake compute.
