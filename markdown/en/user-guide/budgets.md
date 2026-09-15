# Monitor credit usage with budgets

A budget defines a monthly spending limit on the [compute costs](/user-guide/cost-understanding-compute) for
a Snowflake account or a custom group of Snowflake objects. When the spending limit is projected to be exceeded, a notification is
sent. You can configure the budget to send this notification to a list of email addresses, a queue provided by a cloud service
(Amazon SNS, Azure Event Grid, or Google Cloud PubSub), or a webhook for a third-party system (for example, Slack, Microsoft
Teams, or PagerDuty).

## Account budget and custom budgets

The *account budget* monitors spending for all credit usage in the account.

You can also create a *custom budget* to monitor the spending limits for a specific group of
[supported objects](/user-guide/budgets/custom-budget#label-budgets-supported-objects).

You can also use [per-user quotas](/user-guide/budgets/per-user-quotas) to enforce monthly and
daily credit limits for individual users in your account.

For both types of budgets, you must set up the spending limit and specify how you want to receive notifications.

To start using budgets in Snowflake, [activate the account budget](/user-guide/budgets/account-budget#label-activate-account-budget).

## Spending limit and time interval

The spending limit is expressed in Snowflake credits and is used for alerting and notification purposes only. The spending limit
is set for the time interval of one calendar month.

The time interval starts at 12:00 AM UTC on the first day of the month and ends at 11:59 PM UTC on the last day of the month. If a budget
is created after the first day of the month, the first monitoring interval is the period until the last day of the current month, then
is reset on the first of the following month.

If you activate your *account budget* after the first day of the month, data starting from the beginning of the month is backfilled
and used to determine if you are going to exceed your spending limit for the month.

If you create a *custom budget* after the first day of the month, historical data for the month is only backfilled for resources that were
added to the budget using a tag. Data from resources added individually is not backfilled.

Note

If you create a custom budget and individually add resources to the budget instead of using a tag, consider the following:

- Forecasting for future spend by those resources is based on the credit usage only for the days after the budget is enabled.
- You might exceed your budget for the first month. Because the data for the resources is not backfilled, the forecasting might be
  incorrect. Subsequent months will correctly forecast credit usage based on spending history.

## Creating user-defined actions

You can configure a budget to automatically call user-defined stored procedures at key points during a budget cycle. For example, you
can trigger a stored procedure when spending reaches a certain threshold, or when the budget cycle restarts at the
beginning of its monthly period. Each stored procedure you define can perform actions such as suspending warehouses,
sending notifications, or logging events to a table.

- To trigger actions when a spending threshold is met, see [Custom actions for budgets](/user-guide/budgets/custom-actions).
- To trigger actions when the budget cycle restarts, see [Cycle-start actions for budgets](/user-guide/budgets/cycle-start-actions).

## Adjusting the budget refresh interval

A budget cannot calculate whether consumption has reached a spending limit until the budget is refreshed with the most current consumption
data. The time period between consumption and the budget’s receipt of information about that consumption is called the
budget refresh interval.

By default, the budget refresh interval is up to 6.5 hours. You can reduce the budget refresh interval to one hour, which can be helpful
when you need to watch spending more carefully. A budget with a one-hour refresh interval is known as a *low latency budget*. You can
temporarily reduce the budget refresh interval to closely monitor consumption, and then set it back to the default to save on costs.

Setting the refresh interval to one hour increases the compute cost of the budget by a factor of 12. For example, if a budget consumes one
credit per month when the refresh interval is 6.5 hours, then the budget consumes 12 credits per month when the refresh period is one hour.
To determine the current compute cost of your budgets, see [Exploring compute costs](/user-guide/budgets/cost#label-budgets-cost-compute).

- To adjust the budget refresh interval, call the [SET\_REFRESH\_TIER](/sql-reference/classes/budget/methods/set_refresh_tier) method.
  You can also use Snowsight to adjust the interval for a custom budget by selecting or deselecting the
  **Enable low latency budget** field.
- To retrieve the current refresh interval, call the [GET\_REFRESH\_TIER](/sql-reference/classes/budget/methods/get_refresh_tier)
  method.

## Supported services

Budgets monitor credit usage for the following services. Use the table to determine whether custom budgets support the service and which
object is associated with the service.

Note

Account budget support for serverless features depends on the availability of
service types in the Account Usage [METERING\_HISTORY view](/sql-reference/account-usage/metering_history).

| Service | Account budget | Custom budget | Object |
| --- | --- | --- | --- |
| AI\_SERVICES | ✔ | ✔ | Snowflake CoWork, Cortex Agent |
| AUTO\_CLUSTERING | ✔ | ✔ | Table |
| COPY\_FILES | ✔ | ✔ | Database |
| DATA\_QUALITY\_MONITORING | ✔ | ✔ | Table |
| MATERIALIZED\_VIEW | ✔ | ✔ | Materialized view |
| PIPE | ✔ | ✔ | Pipe |
| QUERY\_ACCELERATION | ✔ | ✔ | Warehouse |
| REPLICATION | ✔ | ✔ | Database, Replication group |
| SEARCH\_OPTIMIZATION | ✔ | ✔ | Table |
| SERVERLESS\_ALERTS | ✔ | ✔ | Alert |
| SERVERLESS\_TASK | ✔ | ✔ | Task |
| SNOWPARK\_CONTAINER\_SERVICES | ✔ | ✔ | Compute pool |
| SNOWPIPE\_STREAMING | ✔ | ✔ | Table |
| WAREHOUSE\_METERING | ✔ | ✔ | Warehouse |

Expand

Show lessSee more

## Budgets notifications

A budget sends a daily alert notification when current spending is on track to exceed the spending limit based on time-series
forecasting.

To receive automatic alert notifications, you must do the following as part of activating the account budget or creating a custom budget:

- Set a spending limit for the budget.
- Specify how you want to receive notifications about the budget.

For more information, see [Notifications for budgets](/user-guide/budgets/notifications).

## Budgets roles and privileges

To enable a custom role in your account to work with budgets, you can grant the following roles and privileges.

Note

Snowflake provides application roles and database roles that control access to all cost-related features, including budgets. For
information about granting these roles to a custom role rather than working with budget-specific roles and privileges, see
[Access control for cost management](/user-guide/cost-access-control).

### Application roles to manage the account budget

You can grant the following application roles to a custom role in your account to monitor or manage the account budget:

| Application Role | Description |
| --- | --- |
| BUDGET\_VIEWER | Enables a role to view budget usage data and list the resources in the budget. |
| BUDGET\_ADMIN | Enables a role to activate or deactivate the account budget and modify the properties of a budget including spending limit, the notification integrations to use, the list of email addresses to receive notifications, and the mute notifications setting. |

Expand

Show lessSee more

In addition to the application role, there are other required privileges that must be granted to enable a custom role to monitor or manage
the account budget. For more information, see [Required roles and privileges](#label-budgets-required-roles-privileges).

### Instance roles to manage custom budgets

Each custom budget has instance roles that you can grant to other roles to view or modify the budget:

| Instance Role | Description |
| --- | --- |
| VIEWER | Enables a role to view budget usage data. |
| ADMIN | Enables a role to modify the properties of a budget including spending limit, the notification integrations to use, the list of email addresses to receive notifications, the mute notifications setting, and the objects in the group. |

Expand

Show lessSee more

In addition to the instance role, there are other required privileges that must be granted to enable a custom role to create, monitor, or
modify a custom budget. For more information, see [Required roles and privileges](#label-budgets-required-roles-privileges).

### Required roles and privileges

In addition to the application or instance roles, the following privileges must be granted to a custom role to monitor or manage budgets:

| Privilege or role | Budget type | Create | Manage | Monitor | Notes |
| --- | --- | --- | --- | --- | --- |
| USAGE\_VIEWER | Both | ✔ | ✔ | ✔ | Grant the [Snowflake database role](/sql-reference/snowflake-db-roles) USAGE\_VIEWER to the custom role. |
| USAGE | Custom | ✔ | ✔ | ✔ | Grant the USAGE privilege on the database or schema that contains the custom budget. |
| SNOWFLAKE.BUDGET\_CREATOR | Custom | ✔ |  |  | Grant this database role to the custom role to enable it to create custom budgets. |
| CREATE SNOWFLAKE.CORE.BUDGET | Custom | ✔ |  |  | Grant this privilege on the schema that will contain the custom budget. |
| APPLYBUDGET | Custom |  | ✔ |  | Must be granted on each object to be added or removed from a custom budget. |
| USAGE | Custom |  | ✔ |  | To add or remove schema objects from a custom budget, this privilege must be granted on the database and schema that contains the object. |

Expand

Show lessSee more

For more information and examples, see the following sections:

- [Create a custom role to manage the account budget](/user-guide/budgets/account-budget#label-account-budget-admin-role)
- [Create a custom role to monitor the account budget](/user-guide/budgets/monitor#label-account-budget-monitor-role)
- [Create a custom role to monitor a custom budget](/user-guide/budgets/monitor#label-custom-budgets-monitor-role)
- [Create a custom role to manage a custom budget](/user-guide/budgets/custom-budget#label-custom-budgets-admin-role)
- [Create a custom role to create budgets](/user-guide/budgets/custom-budget#label-custom-budgets-owner-role)

## Limitations

The following are limitations for Budgets:

- Instances of the BUDGET class can’t be [replicated](/user-guide/account-replication-intro) to target accounts.
- An account can contain a maximum of 100 custom budgets.
- Currently, Budgets does not support monitoring costs for [Hybrid tables](/user-guide/tables-hybrid).
- The following account-level parameters must be unset or set to the default value:

  - [AUTOCOMMIT](/sql-reference/parameters#label-autocommit) must be unset or set to TRUE.

    If this parameter is set to FALSE, activating a budget might fail, or usage might not be tracked correctly.
  - [TIMESTAMP\_INPUT\_FORMAT](/sql-reference/parameters#label-timestamp-input-format) and [DATE\_INPUT\_FORMAT](/sql-reference/parameters#label-date-input-format) must be unset or set to AUTO.

    If these parameters aren’t set to AUTO, usage might not be tracked correctly.

  Before you activate budgets, [check the values of these parameters](/sql-reference/parameters#label-parameters-list-by-name) by executing the
  [SHOW PARAMETERS](/sql-reference/sql/show-parameters) command:

  Copy code

  ```
  SHOW PARAMETERS LIKE 'AUTOCOMMIT' IN ACCOUNT;
  ```

  Copy code

  ```
  SHOW PARAMETERS LIKE 'TIMESTAMP_INPUT_FORMAT' IN ACCOUNT;
  ```

  Copy code

  ```
  SHOW PARAMETERS LIKE 'DATE_INPUT_FORMAT' IN ACCOUNT;
  ```

  Note

  You must set these parameters at the account level. Setting the parameters at a lower level (for example, at the session
  level) doesn’t have an effect on activating budgets or tracking usage.
