# Access control for cost anomalies

A cost anomaly occurs when daily consumption is above or below the expected range of consumption for the day. This topic describes the
access control requirements for viewing and configuring cost anomalies, including [anomaly monitors](/user-guide/cost-anomalies#label-cost-anomaly-monitors).

## How access to cost anomalies works

Access works the same way for account-level anomalies, organization-level anomalies, and anomaly monitors. Two application roles set the
baseline, and a third role controls access to consumption data in a currency.

Viewing anomalies and consumption
:   Either APP\_USAGE\_ADMIN or APP\_USAGE\_VIEWER lets a user view cost anomalies and investigate the consumption behind them, with credits as the
    unit of measure. Both roles grant the same viewing access.

Changing configuration
:   APP\_USAGE\_ADMIN adds the ability to change configuration in the account. That includes setting the account notification list, and creating,
    changing, and deleting anomaly monitors. A user with APP\_USAGE\_ADMIN doesn’t also need APP\_USAGE\_VIEWER.

Viewing consumption in a currency
:   Consumption data in a currency is more sensitive than credits, so it requires an additional role granted alongside APP\_USAGE\_ADMIN or
    APP\_USAGE\_VIEWER. The same role also controls the organization notification list, because those notifications can contain currency amounts.

    Anomaly monitors always report credits or AI credits, never a currency, so this role doesn’t affect them.

The role that grants currency access depends on the type of account the user signs in to:

- In the [organization account](/user-guide/organization-accounts), grant ORGANIZATION\_BILLING\_VIEWER.
- In an [ORGADMIN-enabled account](/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account), grant APP\_ORGANIZATION\_BILLING\_VIEWER.

Regular accounts have access to neither the ORGANIZATION\_USAGE schema nor a currency role, so users in a regular account always see
consumption in credits.

## Administrators with system roles

Administrators with the following system roles can perform all tasks related to identifying and investigating cost anomalies, both in
Snowsight and by using the ANOMALY\_INSIGHTS class. They don’t need any of the application roles described in this topic:

- ACCOUNTADMIN role in an ORGADMIN-enabled account or a regular account.
- GLOBALORGADMIN role in the organization account.

## Application roles

You can let other users work with cost anomalies by granting the following application roles, which are within the SNOWFLAKE application.

| Application role | Description |
| --- | --- |
| APP\_USAGE\_VIEWER | Lets a user view cost anomalies and the consumption behind them, in credits. This includes the results of [anomaly monitors](/user-guide/cost-anomalies#label-cost-anomaly-monitors), but not the ability to create or change one. |
| APP\_USAGE\_ADMIN | Lets a user do everything APP\_USAGE\_VIEWER does, and configure cost anomalies within the account. Configuring includes setting the email addresses where notifications are sent for [account-level cost anomalies](/user-guide/cost-anomalies#label-cost-anomaly-level), and creating, updating, renaming, and dropping [anomaly monitors](/user-guide/cost-anomalies#label-cost-anomaly-monitors) along with each monitor’s notification list. |
| ORGANIZATION\_BILLING\_VIEWER | When combined with APP\_USAGE\_ADMIN or APP\_USAGE\_VIEWER, lets a user in the organization account see consumption with a currency as the unit of measure. Without this role, users see consumption in credits, not a currency.  Also required to view and set the email addresses where notifications are sent for [organization-level cost anomalies](/user-guide/cost-anomalies#label-cost-anomaly-level). |
| APP\_ORGANIZATION\_BILLING\_VIEWER | Provides the same access as ORGANIZATION\_BILLING\_VIEWER but in an ORGADMIN-enabled account instead of the organization account. |

Expand

Show lessSee more

## Application roles for ANOMALY\_INSIGHTS methods

The following table shows which application role lets a user call each method of the
[ANOMALY\_INSIGHTS](/sql-reference/classes/anomaly_insights) class. A user needs only one of the roles marked ✔ for a given method. An
empty cell means the role can’t call the method. Methods marked (*preview*) belong to
[anomaly monitors](/user-guide/cost-anomalies#label-cost-anomaly-monitors).

In an ORGADMIN-enabled account, grant APP\_ORGANIZATION\_BILLING\_VIEWER wherever this table lists ORGANIZATION\_BILLING\_VIEWER.

| Method | APP\_USAGE\_VIEWER | APP\_USAGE\_ADMIN | ORGANIZATION\_BILLING\_VIEWER |
| --- | --- | --- | --- |
| ADD\_NOTIFICATION\_INTEGRATION |  | ✔ | ✔ |
| ADHOC\_CALCULATE\_ANOMALIES\_FROM\_CONFIG (*preview*) | ✔ | ✔ |  |
| CREATE\_MONITOR (*preview*) |  | ✔ |  |
| DROP\_MONITOR (*preview*) |  | ✔ |  |
| GET\_ACCOUNT\_ANOMALIES\_IN\_CREDITS | ✔ | ✔ |  |
| GET\_ACCOUNT\_NOTIFICATION\_EMAILS |  | ✔ |  |
| GET\_DAILY\_CONSUMPTION\_ANOMALY\_DATA |  |  | ✔ |
| GET\_HOURLY\_CONSUMPTION\_BY\_SERVICE\_TYPE | ✔ | ✔ |  |
| GET\_HOURLY\_SPEND\_FOR\_ANOMALY | ✔ | ✔ |  |
| GET\_MONITOR\_ANOMALIES (*preview*) | ✔ | ✔ |  |
| GET\_MONITOR\_CONFIG (*preview*) | ✔ | ✔ |  |
| GET\_MONITOR\_NOTIFICATION\_EMAILS (*preview*) |  | ✔ |  |
| GET\_MONITOR\_NOTIFICATION\_LOG (*preview*) |  | ✔ |  |
| GET\_NOTIFICATION\_INTEGRATIONS | ✔ | ✔ | ✔ |
| GET\_ORG\_NOTIFICATION\_EMAILS |  |  | ✔ |
| GET\_TOP\_ACCOUNTS\_BY\_CONSUMPTION | ✔ | ✔ |  |
| GET\_TOP\_QUERIES\_FROM\_WAREHOUSE | ✔ | ✔ |  |
| GET\_TOP\_WAREHOUSES\_ON\_DATE | ✔ | ✔ |  |
| LIST\_MONITORS (*preview*) | ✔ | ✔ |  |
| RECALCULATE\_ANOMALIES (*preview*) | ✔ | ✔ |  |
| REMOVE\_NOTIFICATION\_INTEGRATION |  | ✔ | ✔ |
| RENAME\_MONITOR (*preview*) |  | ✔ |  |
| SET\_ACCOUNT\_NOTIFICATION\_EMAILS |  | ✔ |  |
| SET\_MONITOR\_NOTIFICATION\_EMAILS (*preview*) |  | ✔ |  |
| SET\_ORG\_NOTIFICATION\_EMAILS |  |  | ✔ |
| UPDATE\_MONITOR\_CONFIG (*preview*) |  | ✔ |  |

Expand

Show lessSee more

Note the following about how these roles apply:

- ADD\_NOTIFICATION\_INTEGRATION and REMOVE\_NOTIFICATION\_INTEGRATION require APP\_USAGE\_ADMIN to manage an integration for account-level
  anomalies, and a currency role to manage one for organization-level anomalies. Both also require privileges on the notification
  integration itself. For more information, see the method reference pages.
- Every anomaly monitor in an account is visible to anyone with APP\_USAGE\_VIEWER or APP\_USAGE\_ADMIN in that account. Monitors aren’t
  filtered per user, because a monitor’s results are aggregate cost data that these roles can already see.

## Grant access to users

The following sections show how to combine these application roles for common cases.

### Grant the ability to view cost anomalies in a specific account

If you want users to be able to view account-level cost anomalies in a specific account, but not act as an administrator, grant them the
APP\_USAGE\_VIEWER application role.

For example, if you want user `joe` to be able to view cost anomalies for a specific account, sign in to the account, and then run the
following commands:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE anomaly_viewer_role;
GRANT APPLICATION ROLE SNOWFLAKE.APP_USAGE_VIEWER TO ROLE anomaly_viewer_role;
GRANT ROLE anomaly_viewer_role TO USER joe;
```

### Grant the ability to view cost anomalies for all accounts

To let a user view account-level cost anomalies for all accounts in the organization and to view organization-level anomalies, grant
the APP\_USAGE\_VIEWER role and one of the following roles:

- If the user signs in to the organization account to view cost anomalies, also grant the ORGANIZATION\_BILLING\_VIEWER application role.
- If the user signs in to an ORGADMIN-enabled account to view cost anomalies, also grant the APP\_ORGANIZATION\_BILLING\_VIEWER application
  role.

A user who is granted these roles can see consumption data with a currency as the unit of measure instead of credits.

For example, if the user `ralph` signs in to the organization account to view cost anomalies that are related to the entire organization,
run the following commands:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE anomaly_viewer_role;
GRANT APPLICATION ROLE SNOWFLAKE.APP_USAGE_VIEWER TO ROLE anomaly_viewer_role;
GRANT APPLICATION ROLE SNOWFLAKE.ORGANIZATION_BILLING_VIEWER TO ROLE anomaly_viewer_role;
GRANT ROLE anomaly_viewer_role TO USER ralph;
```

### Grant the ability to configure cost anomalies in a specific account

If you want users to be able to view *and* configure account-level cost anomalies within a specific account, grant them the APP\_USAGE\_ADMIN
application role. A user with this role doesn’t need the APP\_USAGE\_VIEWER role to view the cost anomalies. Configuring cost anomalies
includes adding the email addresses where notifications are sent when there is an anomaly in the account, and managing anomaly monitors.

For example, if you want user `judy` to be able to view and configure account-level cost anomalies for a specific account, sign in to the
account, and then run the following commands:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE anomaly_admin_role;
GRANT APPLICATION ROLE SNOWFLAKE.APP_USAGE_ADMIN TO ROLE anomaly_admin_role;
GRANT ROLE anomaly_admin_role TO USER judy;
```

### Grant the ability to configure organization-level cost anomalies

To let a user configure organization-level cost anomalies, grant the APP\_USAGE\_ADMIN role and one of the following roles:

- If the user signs in to the organization account to configure and view cost anomalies, also grant the ORGANIZATION\_BILLING\_VIEWER
  application role.
- If the user signs in to an ORGADMIN-enabled account to configure and view cost anomalies, also grant the APP\_ORGANIZATION\_BILLING\_VIEWER
  application role.

An administrator with one of these role combinations can perform the following tasks:

- Set and view the email addresses where notifications are sent for organization-level anomalies.
- View account-level cost anomalies in all accounts in the organization.
- View organization-level cost anomalies.
- View consumption data that uses a currency as the unit of measure.

For example, if the user `steven` signs in to the organization account to work with cost anomalies related to the entire organization,
run the following commands:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE anomaly_admin_role;
GRANT APPLICATION ROLE SNOWFLAKE.APP_USAGE_ADMIN TO ROLE anomaly_admin_role;
GRANT APPLICATION ROLE SNOWFLAKE.ORGANIZATION_BILLING_VIEWER TO ROLE anomaly_admin_role;
GRANT ROLE anomaly_admin_role TO USER steven;
```

### Grant the ability to scope an anomaly monitor with tags

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Defining an [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors) requires APP\_USAGE\_ADMIN, plus the `APPLYBUDGET` privilege on each tag used in
the monitor’s scope. `APPLYBUDGET` is the same privilege that [budgets](/user-guide/budgets) require, and Snowflake doesn’t define a
separate privilege for anomaly monitors.

For example, to let the role `anomaly_admin_role` use the `cost_center` tag when defining a monitor:

Copy code

```
USE ROLE ACCOUNTADMIN;

GRANT APPLYBUDGET ON TAG it.warehouse_management.cost_center TO ROLE anomaly_admin_role;
```

Note the following about how `APPLYBUDGET` interacts with the application roles:

- `APPLYBUDGET` only grants the authority to name a tag in a monitor’s scope. It doesn’t grant access to consumption data for the resources
  that carry the tag.
- Access to a monitor’s results is always evaluated against the application role of the user reading them, not the privileges of the user
  who created the monitor.
- The privilege is checked when you create the tag reference. If you don’t hold `APPLYBUDGET` on a tag,
  [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) fails before the monitor method runs.
- `APPLYBUDGET` applies only to saving a monitor.
  [ANOMALY\_INSIGHTS!ADHOC\_CALCULATE\_ANOMALIES\_FROM\_CONFIG](/sql-reference/classes/anomaly-insights/methods/adhoc_calculate_anomalies_from_config), which tests a configuration without saving it,
  names tags directly and doesn’t require the privilege.

## Access to cost anomaly views

The application roles in this topic control the ANOMALY\_INSIGHTS class methods and Snowsight. Querying the cost anomaly views
directly requires database roles instead:

- [ANOMALIES\_DAILY view](/sql-reference/account-usage/anomalies_daily) requires a database role with read access to the
  [ACCOUNT\_USAGE schema](/sql-reference/account-usage), such as USAGE\_VIEWER.
- [ANOMALIES\_IN\_CURRENCY\_DAILY view](/sql-reference/organization-usage/anomalies_in_currency_daily) contains currency data and requires ORGANIZATION\_BILLING\_VIEWER.

Anomaly monitor results aren’t available in either schema. To retrieve them, use
[ANOMALY\_INSIGHTS!GET\_MONITOR\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/get_monitor_anomalies).
