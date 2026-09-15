# Account Overview

## Overview

The **Account Overview** page in Snowsight is the starting point for understanding and
optimizing the cost of using Snowflake in an account. The page summarizes spend, surfaces unexpected
spikes, and recommends ways to save, all in one place, so you don’t have to
stitch together multiple dashboards.

Use this page to:

- Track this month’s spend against your budget at a glance.
- Spot cost trends, untagged warehouses, and your top-spending resources.
- Investigate anomalies and act on optimization recommendations.
- Ask follow-up questions about anything on the page using [Cortex Code](/user-guide/cortex-code/cortex-code).

## Open the Account Overview page

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with [access to Account Overview](#label-account-overview-access-control).
3. In the navigation menu, select **Admin** » **Cost management**.
4. Select the **Account Overview** tab.

A note at the top of the page reminds you that usage data is not real-time: “Information latency can
be up to 72 hours.”

### Filters

Two filters at the top of the page control what every tile on the page shows. Changing a filter
updates all tiles at once.

#### Date range

The **Date range** filter sets the time period used for every calculation, chart, and comparison on
the page. The default is **This month**.

Available options:

- **This month** (default)
- **Last month**
- **Last 3 months**
- **Last 6 months**
- **This year**

When a tile shows a percent change “versus the previous period,” the previous period is determined
by the date range you select. For example, with **This month** selected, the comparison is to the
same number of days last month.

#### Currency

The **Currency** filter sets the unit used to display costs. The default is credits.

To switch to a fiat currency such as USD, you need additional privileges and must be signed in to
the right type of account. See [Viewing costs in currency](#label-account-overview-currency-display) for details.

The currency filter affects the Total Cost, Cost Attribution, Anomalies, and Cost summary tiles.

## What’s on the Account Overview page

The page is organized into three areas:

- [Summary cards](#label-account-overview-summary-cards): A row of headline metrics at the top of the page.
- [Cost breakdown](#label-account-overview-cost-breakdown-section): Detailed cost trends and attribution.
- [Alerts and recommendations](#label-account-overview-alerts-section): Cost anomalies and savings opportunities.

## Summary cards

A row of four cards at the top of the page gives you a single-glance view of account-wide spend,
budget status, and outstanding alerts.

### Cost summary

|  |  |
| --- | --- |
| Goal | Show total spend for the selected time period and how it compares to the previous comparable period. |
| Shows | Total cost, percent change versus the previous period, and the month-to-date average daily spend. |
| Use it to | Quickly answer “How much have we spent this month, and is it trending up or down?” |

Expand

Show lessSee more

### Monthly budget utilization

|  |  |
| --- | --- |
| Goal | Show how much of your account’s monthly budget has been consumed. |
| Shows | Percentage of budget used, on-track status, and credits spent against budget. Select the tile to open [Monitor credit usage with budgets](/user-guide/budgets). |
| Use it to | Catch budget overruns before they happen and confirm spending is on track. |
| Prerequisites | A monthly budget must be configured for the account. If no budget is configured, the tile displays a prompt to set one up. See [Monitor credit usage with budgets](/user-guide/budgets). |

Expand

Show lessSee more

### Anomalies

|  |  |
| --- | --- |
| Goal | Surface unexpected spikes in cost without requiring you to investigate. |
| Shows | A count of anomalies detected in the selected time period, or “No anomalies detected.” |
| Use it to | Identify cost spikes that fall outside normal patterns so you can investigate the cause. |
| Key term | An **anomaly** is a day when consumption falls outside the range expected by Snowflake’s anomaly detection model. See [Introduction to cost anomalies](/user-guide/cost-anomalies). |

Expand

Show lessSee more

### Optimization insights

|  |  |
| --- | --- |
| Goal | Surface concrete ways to reduce credit consumption based on your usage patterns. |
| Shows | Estimated weekly savings in credits and the number of savings opportunities identified. |
| Use it to | Find low-effort wins, such as rarely used materialized views or oversized warehouses, that reduce spend. |
| Key term | An **optimization insight** is a specific, actionable recommendation generated weekly by Snowflake. See [Using Optimization insights to save](/user-guide/cost-insights). |

Expand

Show lessSee more

## Cost breakdown

The Cost breakdown section breaks down spend into trends, attribution, and top spenders.

### Total cost

|  |  |
| --- | --- |
| Goal | Show how spend changes over time so you can spot trends and outliers. |
| Shows | A line chart of spend across the selected time period, alongside the period total, percent change versus the prior period, and the month-to-date average daily spend. |
| Use it to | Identify days, weeks, or events that drove unusual spend. |

Expand

Show lessSee more

#### Group by options (Total cost)

Use the **Group by** menu in the upper-right corner of the tile to break the chart into series. The
option you choose changes which lines appear on the chart.

| Group by | What you see |
| --- | --- |
| **Services** | One line per Snowflake service that incurred cost, such as Warehouse, AI Services, Replication, Snowpipe Streaming, Serverless Task, Cortex Code CLI, Cortex Code Snowsight, Cortex Code Desktop, Snowflake Intelligence, Cortex Agents, and others. Use this view to see which service is growing the fastest. |
| **Usage type** | One line per high-level usage type: Compute, Storage, Data transfer, and AI inference. Use this view to compare compute against storage and data transfer at a glance. |

Expand

Show lessSee more

The Cortex Code starter question changes with the Group by selection. For example, with **Services**
selected, the starter is “Which service has grown the fastest over this month?”; with **Usage type**
selected, it becomes “How has my compute vs storage cost changed over this month?”.

### Warehouse cost attribution

|  |  |
| --- | --- |
| Goal | Show how warehouse spend is attributed using cost attribution tags. |
| Shows | The percent of warehouse spend covered by the selected tag, along with the change versus the prior period and a breakdown of the contributing values. |
| Use it to | Improve cost attribution by identifying untagged spend, and see how spend distributes across teams, cost centers, or any other tag dimension. |
| Key term | A **cost attribution tag** is any tag applied to a warehouse for the purpose of chargeback. See [Attributing cost](/user-guide/cost-attributing). |

Expand

Show lessSee more

#### Group by options (Warehouse cost attribution)

Use the **Group by** menu in the upper-right corner of the tile to choose how the attribution is
calculated. The view changes based on what you pick.

| Group by | What you see |
| --- | --- |
| Default (no tag selected) | The percentage of your total credit spend attributed to warehouses **with any tag** versus those **without any tag**. Use this view to track tagging coverage at a glance. |
| A specific tag name (for example, **COST\_CENTER**) | A breakdown of spend by **values** of the selected tag, such as `finance`, `engineering`, or `product`. A **Without selected tag** row captures warehouses that may have other tags but are missing the one you grouped by. Use this view to chargeback spend by team, cost center, or any other tag dimension. |

Expand

Show lessSee more

Select **View more** in the upper-right corner of the tile to open the full warehouse cost
attribution view.

### Top spend by category

|  |  |
| --- | --- |
| Goal | Identify the biggest cost drivers in your account. |
| Shows | A ranked list of your top consumers in one of four categories: warehouses, queries, databases, or tags. Switch categories with the sub-tabs. |
| Use it to | Focus optimization efforts on the resources that move the needle. |

Expand

Show lessSee more

## Alerts and recommendations

The Alerts and recommendations section surfaces issues and opportunities you might otherwise miss.

### Anomalies (detail)

|  |  |
| --- | --- |
| Goal | Show recent cost anomalies in detail so you can investigate them. |
| Shows | A count of anomalies in the selected time period, a freshness label such as “No new since last 24h”, and a table with one row per anomaly. |
| Use it to | Investigate individual anomalies and decide whether they are explained by known events. |
| See also | [Introduction to cost anomalies](/user-guide/cost-anomalies) for how anomaly detection works. |

Expand

Show lessSee more

Each row in the anomalies table shows:

| Column | Description |
| --- | --- |
| Date | The day on which the anomaly was detected. |
| Consumption | The actual consumption for that day. |
| Expected range | The lower and upper bound of consumption that Snowflake’s anomaly detection model predicted for that day. |
| Over/Under expected | The amount above the upper bound (positive) or below the lower bound (negative). Red text indicates a deviation worth investigating. |

Expand

Show lessSee more

Select the **+** button on any row to open Cortex Code with that anomaly’s context preloaded.

### Optimization insights (detail)

|  |  |
| --- | --- |
| Goal | List specific optimization opportunities along with their estimated savings. |
| Shows | Insights with estimated credit savings, such as “Rarely used tables with automatic clustering”, plus a checklist of insight categories that were evaluated. |
| Use it to | Take action on the opportunities with the highest estimated savings first. |
| See also | [Using Optimization insights to save](/user-guide/cost-insights) for the full list of insight types. |

Expand

Show lessSee more

## Ask follow-up questions with Cortex Code

Every tile on the Account Overview page includes a **+** button with a starter question, such as
“What’s behind the cost trend over this month?” or “Which warehouses are untagged?”. Selecting a
starter question opens [Cortex Code](/user-guide/cortex-code/cortex-code), which uses the context
of the current tile to answer.

You can also type your own question. Common follow-ups include:

- “Why did spend spike on a particular day?”
- “Which roles spent the most this month?”
- “Show me the largest untagged warehouses.”

For more about Cortex Code, see [Overview of Snowflake CoCo](/user-guide/cortex-code/cortex-code).

Note

Cortex Code must be enabled for your account, and your role must have the necessary privileges.
If you don’t see the **+** buttons, see [Overview of Snowflake CoCo](/user-guide/cortex-code/cortex-code).

## View the SQL query behind a tile

Every tile on the Account Overview page is populated by a SQL query against views in the
[ACCOUNT\_USAGE](/sql-reference/account-usage) or [ORGANIZATION\_USAGE](/sql-reference/organization-usage)
schemas. You can inspect the exact query a tile runs so you can reuse it in a worksheet, adapt
it for a custom report, or learn how the metric is calculated.

To view the SQL query for a tile, select the **View SQL query** icon ([![View query button.](/static/images/snowsight/icons/view-query-icon.png)](/static/images/snowsight/icons/view-query-icon.png)) in
the upper-right corner of the tile. The query opens in a worksheet, where you can run it, modify
it, or save it.

For example, the **Top spend by category** tile (with the **Warehouse** sub-tab) queries the
[WAREHOUSE\_METERING\_HISTORY](/sql-reference/account-usage/warehouse_metering_history) view in the
ACCOUNT\_USAGE schema of the shared SNOWFLAKE database.

Note

The role you use to run the query must have the same privileges that the tile requires. See
[Access control](#label-account-overview-access-control) for the privileges required by each tile.

## Access control

Each section of the Account Overview page has different privilege requirements. The page itself
requires a baseline set of roles, and individual tiles may require additional privileges.

For general information about cost management access control, see
[Access control for cost management](/user-guide/cost-access-control).

### Accessing the Account Overview page

To view the **Account Overview** page, you must use a role that has access to account usage data.
Without sufficient privileges, the page displays the message “No access to account overview.”

Use one of the following roles:

- The ACCOUNTADMIN system-defined role (for regular accounts and ORGADMIN-enabled accounts).
- The GLOBALORGADMIN system-defined role (for organization accounts).
- A role that has been granted the APP\_USAGE\_VIEWER application role and the USAGE\_VIEWER database
  role.
- A role that has been granted the APP\_USAGE\_ADMIN application role and the USAGE\_ADMIN database
  role.

For information about granting these roles, see
[Granting access to other users](/user-guide/cost-access-control#label-cost-access-control-other-users).

Note

If a role has IMPORTED PRIVILEGES on the SNOWFLAKE database or the USAGE\_VIEWER database role but
doesn’t have the APP\_USAGE\_VIEWER application role, the page displays but some tiles aren’t
available. Snowflake recommends granting both the application role and the database role together
for full access.

### Viewing costs in currency

By default, tiles that display costs show values in credits. To view costs in a currency, you need
additional privileges and must be signed in to the right type of account.

To view costs in currency:

- You must be signed in to the [organization account](/user-guide/organization-accounts) or an
  [ORGADMIN-enabled account](/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account).
- Your role must also be granted one of the following roles:
  - ORGANIZATION\_BILLING\_VIEWER, if you’re signed in to the organization account.
  - APP\_ORGANIZATION\_BILLING\_VIEWER, if you’re signed in to an ORGADMIN-enabled account.

Note

The ACCOUNTADMIN and GLOBALORGADMIN roles also have the privileges required to view costs in
currency.

Currency display affects the Total Cost, Cost Attribution, and Anomalies tiles.

For more information, see
[Viewing a currency as the unit of measure](/user-guide/cost-access-control#label-cost-access-control-currency).

### Tile-level privileges

#### Total Cost tile

The **Total Cost** tile displays spending trends over a selected time range. This tile requires
[page access privileges](#label-account-overview-page-access).

To view costs in a currency instead of credits, you also need
[currency display privileges](#label-account-overview-currency-display).

#### Cost Attribution tile

The **Cost Attribution** tile shows a breakdown of costs by attribution tags. This tile requires
[page access privileges](#label-account-overview-page-access).

#### Top Spend tile

The **Top Spend** tile identifies the highest-cost resources in your account. It has sub-tabs for
warehouses, queries, databases, and tags. This tile requires
[page access privileges](#label-account-overview-page-access).

#### Anomalies tile

For information about the privileges required for the **Anomalies** tile, see
[Access control for cost anomalies](/user-guide/cost-anomalies-access-control).

#### Optimization insights tile

The **Optimization insights** tile requires the same application roles as Account Overview itself:
`APP_USAGE_VIEWER` (to view insights) or `APP_USAGE_ADMIN` (to view insights and configure cost
anomalies and budgets). See [Accessing the Account Overview page](#label-account-overview-page-access) for the grant examples.

Note

Having only the `USAGE_VIEWER` database role (without the `APP_USAGE_VIEWER` application role)
isn’t sufficient for viewing Optimization insights. The `APP_USAGE_VIEWER` application role
includes the internal `COST_INSIGHTS_USER` role that Optimization insights require.

### Granting access to Account Overview

The following examples show how to grant different levels of access to the **Account Overview**
page.

#### Grant basic view access (without currency display)

To grant a user view access to the **Account Overview** page without currency display, grant the
APP\_USAGE\_VIEWER application role and the USAGE\_VIEWER database role. For example, to grant view
access to user `joe`:

Copy code

```
USE ROLE ACCOUNTADMIN; -- Or GLOBALORGADMIN for organization accounts

CREATE ROLE account_overview_viewer;
GRANT APPLICATION ROLE SNOWFLAKE.APP_USAGE_VIEWER TO ROLE account_overview_viewer;
GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER TO ROLE account_overview_viewer;
GRANT ROLE account_overview_viewer TO USER joe;
```

#### Grant view access with currency display

To allow a user to view costs in a currency, grant the ORGANIZATION\_BILLING\_VIEWER role in addition
to the viewer roles. The user must be signed in to the organization account. For example, to grant
view access with currency display to user `ralph`:

Copy code

```
USE ROLE ACCOUNTADMIN; -- Or GLOBALORGADMIN for organization accounts

CREATE ROLE account_overview_viewer;
GRANT APPLICATION ROLE SNOWFLAKE.APP_USAGE_VIEWER TO ROLE account_overview_viewer;
GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER TO ROLE account_overview_viewer;
GRANT APPLICATION ROLE SNOWFLAKE.ORGANIZATION_BILLING_VIEWER TO ROLE account_overview_viewer;
-- For ORGADMIN-enabled accounts, use APP_ORGANIZATION_BILLING_VIEWER instead:
-- GRANT APPLICATION ROLE SNOWFLAKE.APP_ORGANIZATION_BILLING_VIEWER TO ROLE account_overview_viewer;
GRANT ROLE account_overview_viewer TO USER ralph;
```

#### Grant administrator access

To grant a user administrator access, which includes the ability to configure cost anomalies and
budgets, grant the APP\_USAGE\_ADMIN application role and the USAGE\_ADMIN database role. For example,
to grant administrator access to user `judy`:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE account_overview_admin;
GRANT APPLICATION ROLE SNOWFLAKE.APP_USAGE_ADMIN TO ROLE account_overview_admin;
GRANT DATABASE ROLE SNOWFLAKE.USAGE_ADMIN TO ROLE account_overview_admin;
GRANT ROLE account_overview_admin TO USER judy;
```
