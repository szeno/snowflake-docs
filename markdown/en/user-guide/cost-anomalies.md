# Introduction to cost anomalies

A cost anomaly occurs when daily consumption is above or below the expected range of consumption for the day. Snowflake uses an algorithm to
automatically detect these cost anomalies based on prior levels of consumption, which simplifies the process of identifying spikes or dips
in costs so you can find ways to optimize your spend. Snowflake also provides tools to investigate these cost anomalies to identify root
causes.

Note

The algorithm that detects cost anomalies requires at least 30 days of consumption before it can identify anomalies. If your consumption
in the last seven days was less than 10 credits, Snowflake does not identify changes as an anomaly.

## Cost anomaly monitoring scope

Snowflake detects cost anomalies at three scopes. Account-level and organization-level detection is always on and requires no
configuration. Anomaly monitors let you define your own narrower scope.

Account-level cost anomalies
:   An account-level cost anomaly occurs when the consumption in a single account falls outside the expected range of consumption for that
    account.

Organization-level cost anomalies
:   An organization-level cost anomaly occurs when the consumption in the entire organization falls outside the expected range of consumption
    for the organization. An organization-level anomaly is based on the aggregate consumption of all accounts in the organization. For example, a
    spike in one account and
    a dip in another can offset each other, so no organization-level anomaly is flagged.

    To identify and investigate organization-level cost anomalies, you need to be signed in to the
    [organization account](/user-guide/organization-accounts) or an [ORGADMIN-enabled account](/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account).

Anomaly monitors
:   An anomaly monitor is a named, custom scope that you define yourself. Instead of watching a whole account, a monitor watches only the
    consumption that matches the [object tags](/user-guide/object-tagging/introduction) and
    [service types](/sql-reference/service-types) you choose. Snowflake attributes consumption to each monitor daily, runs the same
    detection algorithm against it, and can email a notification list that is specific to that monitor.

    Use monitors when account-level detection is too coarse. For example, you can create a monitor for each business unit, cost center, team,
    or project so a spike inside one team’s warehouses is flagged even when total account consumption looks normal.

    Anomaly monitors are a preview feature. For more information, see [Anomaly monitors](#label-cost-anomaly-monitors).

## Anomaly monitors

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

An anomaly monitor is scoped by a configuration that contains the following:

Object tags
:   Tag and value pairs. Consumption from any resource that carries a matching tag is attributed to the monitor, as long as that consumption
    belongs to the monitor’s [credit family](#label-cost-anomaly-monitor-credit-family).

    Only resource-level [object tags](/user-guide/object-tagging/introduction) are supported, which means tags applied directly to a resource
    such as a warehouse, database, or table. Monitors don’t support the following:

    - **User tags.** You can’t scope a monitor by tagging users. A monitor evaluates tags on resources only.
    - **Shared resource attribution.** When a resource is used by more than one team, a monitor attributes all of that resource’s consumption
      to the monitor. A monitor can’t attribute only the share consumed by specific users.

    [Budgets](/user-guide/budgets) support both of these. If you need to attribute the consumption of a shared resource by user, use a budget
    instead. For more information, see [Using budgets for AI features (shared resources)](/user-guide/budgets/budget-shared-resources).

    To include a tag in a monitor’s scope, you need the `APPLYBUDGET` privilege on that tag. For more information, see
    [Access control for cost anomalies](/user-guide/cost-anomalies-access-control).

Service types
:   Account-level [service types](/sql-reference/service-types). Consumption for a service type you include is attributed to
    the monitor in full, for the whole account, regardless of the tags in the monitor’s scope. Include service types when you want a monitor
    to cover consumption that isn’t attributable to a tagged resource.

Credit family
:   Either `CREDITS` or `AI-CREDITS`. See [Credit families](#label-cost-anomaly-monitor-credit-family).

A monitor’s scope must include at least one object tag or at least one service type. You can use tags on their own, service types on their
own, or a combination of both, but a monitor can’t have an empty scope. A monitor can include up to 20 tag and value pairs and up to 20
service types.

A monitor’s scope is the union of everything in it. Consumption is attributed to the monitor if it matches any tag in the scope or belongs to
any service type in the scope. Tags aren’t combined, so a resource doesn’t need to carry every tag to be included. When a resource matches
more than one part of the scope, the monitor counts its consumption once, so nothing is double counted.

Monitors are scoped to a single account, so you can’t create a monitor that spans all accounts in an organization. Each account can have
up to 20 monitors.

### Credit families

Credits and AI credits are different units of measure and can’t be added together. Because of this, each monitor tracks exactly one
credit family, which you choose when you create the monitor:

| Credit family | Description |
| --- | --- |
| `CREDITS` | Traditional consumption, such as virtual warehouse compute, serverless tasks, and Snowpipe. |
| `AI-CREDITS` | Consumption for AI-related services, such as Cortex Search, Cortex Agents, and AI functions. |

Expand

Show lessSee more

The credit family you choose determines which service types you can add to the monitor. You can only add service types that are billed
in that credit family. To find the credit family for a service type, see the `Unit` column in [Service types](/sql-reference/service-types). A unit of
`Credits` corresponds to the `CREDITS` credit family, and `AI Credits` corresponds to `AI-CREDITS`.

The credit family also filters the consumption that a monitor’s tags attribute. A tagged resource can consume both credits and AI credits,
but a monitor counts only the consumption that belongs to its own credit family. Consumption in the other credit family is excluded, even
though the tag matches.

To track both traditional consumption and AI consumption for the same set of tags, create two monitors, one for each credit family.

### Keep a monitor up to date

Snowflake recomputes each monitor’s consumption daily, so a change to a tag’s definition is reflected within 24 hours. Retagging resources
is different: Snowflake can’t detect that a resource gained or lost a tag, so if you retag resources and want the monitor’s history
refreshed immediately, you can force a recalculation. For more information, see
[Use Snowsight to work with cost anomalies](/user-guide/cost-anomalies-ui) or [Programmatically work with cost anomalies](/user-guide/cost-anomalies-class).

Before you save a monitor, you can also test a combination of tags and service types and see the anomalies it would produce. Test
configurations aren’t saved and are lost when your session ends. To save one, select **Create new monitor from config**.

## Get started

To identify and investigate cost anomalies using a user interface:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the [required privileges](/user-guide/cost-anomalies-access-control).
2. In the navigation menu, select **Admin** » **Cost management**, and then select **Anomalies**.

## Unit of measure for cost data

Cost data can be shown with credits as the unit of measure or with a currency as the unit of measure. The unit of measure is a currency in
the following situations:

- If you use the ACCOUNTADMIN or GLOBALORGADMIN system role to work with cost anomalies, cost data displays in a currency if you
  are signed in to the [organization account](/user-guide/organization-accounts) or one that has the
  [ORGADMIN role enabled](/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account).
- If you are not a system administrator, cost data displays in a currency if you are granted the ORGANIZATION\_BILLING\_VIEWER
  application role or APP\_ORGANIZATION\_BILLING\_VIEWER application role. For more information about these application roles, see
  [Access control for cost anomalies](/user-guide/cost-anomalies-access-control).

Note

Anomaly monitors always report consumption in credits or AI credits. Monitors don’t support a currency as the unit of measure.

## Run queries against cost anomaly views

You can run queries against views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas to return historical data about account-level cost
anomalies. Each row in the view includes the consumption on a specific day, and whether that consumption was a cost anomaly.

Cost anomalies for current account
:   Execute queries against the [ANOMALIES\_DAILY view](/sql-reference/account-usage/anomalies_daily) in the
    [ACCOUNT\_USAGE schema](/sql-reference/account-usage) to gain insights into whether cost anomalies occurred in the current account.

    This view uses credits as the unit of measure for consumption.

Cost anomalies for all accounts in an organization
:   Execute queries against the [ANOMALIES\_IN\_CURRENCY\_DAILY view](/sql-reference/organization-usage/anomalies_in_currency_daily) in the
    [ORGANIZATION\_USAGE schema](/sql-reference/organization-usage) to gain insights into whether cost anomalies occurred in accounts in
    the organization. Note that not all accounts have access to the ORGANIZATION\_USAGE schema.

    Use this view to see currency as the unit of measure rather than credits.

Anomaly monitor results aren’t available in these views. To retrieve results for a monitor, use
[ANOMALY\_INSIGHTS!GET\_MONITOR\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/get_monitor_anomalies).

## Notifications

Snowflake can notify you when a cost anomaly occurs so you can respond quickly. Notifications are sent once daily when a cost
anomaly is detected. The daily anomaly notification process sends both types of notification for account-level and
organization-level cost anomalies:

- **Email**: Send notifications to specific email addresses. Configure recipients in Snowsight (see
  [Use Snowsight to work with cost anomalies](/user-guide/cost-anomalies-ui)) or with the [ANOMALY\_INSIGHTS](/sql-reference/classes/anomaly_insights) class methods.
- **Notification integrations**: Send notifications to Slack, SMS (text message), or webhook destinations by registering a
  [notification integration](/sql-reference/sql/create-notification-integration). Use
  [ANOMALY\_INSIGHTS!ADD\_NOTIFICATION\_INTEGRATION](/sql-reference/classes/anomaly-insights/methods/add_notification_integration) to register an integration,
  [ANOMALY\_INSIGHTS!GET\_NOTIFICATION\_INTEGRATIONS](/sql-reference/classes/anomaly-insights/methods/get_notification_integrations) to list registered integrations, and
  [ANOMALY\_INSIGHTS!REMOVE\_NOTIFICATION\_INTEGRATION](/sql-reference/classes/anomaly-insights/methods/remove_notification_integration) to remove one.

Each anomaly monitor has its own email notification list, separate from the account-level and organization-level lists. Monitors
support email notifications only, not notification integrations. To set the list, use
[Configure notifications with Snowsight](/user-guide/cost-anomalies-ui#label-cost-anomaly-notifications) in Snowsight or
[ANOMALY\_INSIGHTS!SET\_MONITOR\_NOTIFICATION\_EMAILS](/sql-reference/classes/anomaly-insights/methods/set_monitor_notification_emails).

## Learn more

For information about how to work with cost anomalies, see the following:

- [Use Snowsight to work with cost anomalies](/user-guide/cost-anomalies-ui)
- [Programmatically work with cost anomalies](/user-guide/cost-anomalies-class)
- [Access control for cost anomalies](/user-guide/cost-anomalies-access-control)
