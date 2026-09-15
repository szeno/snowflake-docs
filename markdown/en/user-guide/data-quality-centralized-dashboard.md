# Using the data quality monitoring dashboard

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The data quality monitoring dashboard in Snowsight provides an account-wide view of data
quality health across all schemas and tables in your Snowflake account. Instead of reviewing results
one object at a time, you can use the dashboard to assess overall health, triage open incidents, and
understand which schemas are under active monitoring — all from a single page.

Use this dashboard when you need a broad view of data quality across your account — for example, during
a morning triage or when identifying which schemas have the most open issues. For investigating data
quality results on a specific table or view, see
[Monitoring data quality checks in Snowsight](/user-guide/data-quality-ui-monitor).

## Prerequisites

### Access control requirements

To view data quality results in the dashboard, your active role must have one of the following
[application roles](/user-guide/data-quality-access-control) granted on the `SNOWFLAKE` database:

- `SNOWFLAKE.DATA_QUALITY_MONITORING_VIEWER`
- `SNOWFLAKE.DATA_QUALITY_MONITORING_ADMIN`

## Navigate to the dashboard

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Governance & security** » **Data quality**.

## Dashboard overview

The dashboard displays an account-wide summary of data quality health. It includes the following sections.

### Summary cards

Two cards at the top of the page provide at-a-glance metrics:

Healthy tables
:   The percentage of monitored tables that currently have no open incidents. The bar shows the count
    of healthy versus unhealthy tables.

Monitoring coverage
:   The percentage of tables in the account that have at least one active data metric function (DMF)
    association. For example, if your account has 1,000 tables and 100 have at least one DMF associated,
    monitoring coverage is 10%. The bar shows the count of monitored versus unmonitored tables.

### Data quality incidents

This section shows a summary count of open incidents grouped by type, followed by a preview of the
most recent incidents. Incidents are grouped into three types:

Volume anomaly
:   Tables where the row count has deviated significantly from historical baselines, as detected by the
    automatic monitoring engine. For more information, see
    [AUTOMATIC\_DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/automatic_data_quality_monitoring_results).

Freshness anomaly
:   Tables that have not been updated within the expected window, as detected by the automatic
    monitoring engine. For more information, see
    [AUTOMATIC\_DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/automatic_data_quality_monitoring_results).

Failed expectations
:   DMF associations where the returned value violated a defined
    [expectation](/user-guide/data-quality-expectations).

Select **Investigate** on a specific incident row to open Cortex Code with that incident’s context
pre-loaded for root-cause analysis. Select **View all**, or select any row in the table, to open the
full [Data quality incidents](#label-dq-dashboard-incidents-page) page.

### Monitored schemas

This section lists all schemas in the account that contain at least one table with an active DMF
association, along with a health summary for each schema. Select **View all** to see the full
[Monitored schemas](#label-dq-dashboard-monitored-schemas) list, or select a row for schema-level
details.

## Filtering by time range

Use the **Time range** filter in the top-right corner to scope incident counts and summary
metrics to a specific time window. The default is the last 7 days.

The active compute warehouse is displayed alongside the time range filter. Snowflake uses this
warehouse to run the queries that power the dashboard. You can change the warehouse by selecting the
warehouse name.

## Data quality incidents page

The **Data quality incidents** page provides a complete, filterable list of all open incidents in
your account. Navigate to it by selecting **View all** from the incidents section on the dashboard,
or by selecting any incident row. Selecting **Investigate** on a row from the dashboard opens Cortex
Code directly for that incident — it does not navigate to this page.

### Incident table

Each row in the incidents table shows the following:

- **Metric name** — The name of the data metric function that generated the incident.
- **Database** — The database containing the affected object.
- **Schema** — The schema containing the affected object.
- **Object** — The table or view with the quality issue.
- **Column** — The column argument passed to the DMF, if applicable. Shown as `—` for table-level metrics.

Use the row checkboxes to select multiple incidents for bulk investigation. See
[Investigate multiple incidents with Cortex Code](#label-dq-dashboard-cortex) for details.

### Investigate multiple incidents with Cortex Code

To investigate several related incidents at once, select two or more rows using the row checkboxes
and then select **Investigate**. Cortex Code opens a single thread with context from all selected
incidents, enabling correlated root-cause analysis across multiple objects or schemas.

You can also select **Investigate** on any single row to open Cortex Code with that incident’s
context pre-loaded.

## Monitored schemas

The **Monitored schemas** section lists every schema in your account that contains at least one
table with an active DMF association. Each row shows the following columns:

- **Database** — The database containing the schema.
- **Schema** — The schema name.
- **Volume anomaly** — The number of open volume anomaly incidents in the schema.
- **Freshness anomaly** — The number of open freshness anomaly incidents in the schema.
- **Failing expectations** — The number of open DMF expectation violations in the schema.
- **Monitoring coverage** — A bar showing the percentage of tables in the schema that have at least
  one DMF association.
- **% unhealthy tables** — A bar showing the percentage of monitored tables in the schema that have
  at least one open incident.

Note

The monitored schemas list reflects schemas where DMF associations exist at either the table level
or the schema level. For information about schema-level associations, see
[Monitor the data quality of a schema](/user-guide/data-quality-schema-level).

## Manage your monitoring scope

Select **Manage Monitors** to view and edit which schemas are included in automatic monitoring.
The dialog shows schemas that contain high-popularity tables — Snowflake identifies these tables
based on activity signals such as query frequency and data update patterns. Snowflake runs its own
row count and freshness anomaly detection on these popular tables daily. This is a separate engine
from the [user-configured DMF anomaly detection](/user-guide/data-quality-anomaly) you set up on
your own tables. The underlying results are available in the
[AUTOMATIC\_DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/automatic_data_quality_monitoring_results)
view.

Note

During this preview, automatic monitoring is computed by Snowflake and does not incur compute
charges to your account. Billing applies only when a DMF you configure explicitly runs on a
scheduled object. For more information, see
[Cost considerations](/user-guide/data-quality-intro#label-data-quality-cost).

Because Snowflake determines which tables to monitor based on popularity, the set of monitored
tables can change over time. Automatic monitoring is a discovery tool — it helps you find where
quality issues exist across your data estate. It does not apply to views, materialized views, or
external tables. To ensure continuous, reliable monitoring of the specific objects that matter to
you, set up [data quality checks](/user-guide/data-quality-ui-setup) or
[schema-level DMF associations](/user-guide/data-quality-schema-level) with
[anomaly detection](/user-guide/data-quality-anomaly) on those objects.

### Edit monitored schemas

In the **Manage Monitors** dialog you can:

- **Uncheck a schema row** to remove it from monitoring entirely, dropping both Freshness and Volume
  anomaly detection for that schema.
- **Toggle Freshness or Volume** on a schema row to enable or disable that specific check while keeping
  the other active.
- Select **+ Add another schema** to add a new schema to your monitoring scope.

After making changes, select **Preview changes** to review your edits before saving.

### Extend monitoring with recommendations

When Snowflake finds schemas that contain popular tables but do not yet have automatic monitoring
enabled, a notification banner appears at the top of the dashboard:

> **New schemas recommended for monitoring** — We found *N* new schemas with popular tables that
> are not tracked yet. Review and add them to your monitoring scope.

Select **Review** to open the **Extend monitoring** dialog. The dialog lists schemas that Snowflake
recommends adding to your monitoring scope, with suggested checks (Freshness and/or Volume).
Schemas are recommended based on the popularity of their tables; a recommendation does not require
that an anomaly has already been detected. Each schema shows one of the following statuses:

- **Recommended** — The schema can be added to your monitoring scope with your current role.
- **No access** — The schema is owned by another role that your current role can’t modify.

Select the schemas you want to add and then select **Enable monitoring**. Changes take effect immediately.

The recommendations are based on popularity signals that Snowflake tracks in the
[AUTOMATIC\_DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/automatic_data_quality_monitoring_results)
view.

## Limitations and considerations

- The dashboard reflects results within a single account. Cross-account or cross-organization views
  are not supported.
- KPI cards and incident counts reflect results stored in the data quality event table. Newly created
  tables and schemas may take a short time to appear.
- Automatic monitoring (freshness and volume anomaly detection) runs daily. The dashboard reflects
  the most recent run for each monitored schema.
- Schemas owned by `SNOWFLAKE` can’t be added to your monitoring scope.
