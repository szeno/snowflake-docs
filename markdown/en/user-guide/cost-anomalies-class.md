# Programmatically work with cost anomalies

You can use the ANOMALY\_INSIGHTS [class](/sql-reference/snowflake-db-classes) to programmatically identify and investigate cost
anomalies. The fully qualified instance that you use to work with anomalies is SNOWFLAKE.LOCAL.ANOMALY\_INSIGHTS.

You must have the [required privileges](/user-guide/cost-anomalies-access-control) to run the
[class methods](/sql-reference/classes/anomaly_insights#label-anomaly-insights-methods).

For an overview of cost anomalies, see [Introduction to cost anomalies](/user-guide/cost-anomalies).

## Identify cost anomalies with ANOMALY\_INSIGHTS

Snowflake creates an instance of the ANOMALY\_INSIGHTS class that you can use to programmatically identify cost anomalies. The
[ANOMALY\_INSIGHTS!GET\_DAILY\_CONSUMPTION\_ANOMALY\_DATA](/sql-reference/classes/anomaly-insights/methods/get_daily_consumption_anomaly_data) method returns consumption data for an account or
organization along with a boolean value that indicates whether that consumption is a cost anomaly.

### Identify organization-level cost anomalies

Users call the GET\_DAILY\_CONSUMPTION\_ANOMALY\_DATA method from the organization account or an ORGADMIN-enabled account to identify
[organization-level cost anomalies](/user-guide/cost-anomalies#label-cost-anomaly-level). To focus on organization-level cost anomalies, the user passes NULL as
an argument instead of the name of an account.

Example: Organization-level cost anomaly
:   To identify organization-level cost anomalies between January 1, 2024, and March 31, 2024, do the following:

    1. Sign in to the [organization account](/user-guide/organization-accounts) or an
       [ORGADMIN-enabled account](/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account).
    2. Call the method:

       Copy code

       ```
       CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_DAILY_CONSUMPTION_ANOMALY_DATA(
         '2024-01-01', '2024-03-31', NULL);
       ```
    3. In the output, find days where the value of the `is_anomaly` column is `TRUE`.

### Identify account-level cost anomalies

You can use the GET\_DAILY\_CONSUMPTION\_ANOMALY\_DATA method to identify account-level cost anomalies for the current account or, if you are
signed in to the organization account or an ORGADMIN-enabled account, any account in the organization.

Example: Cost anomalies in the current account
:   To identify cost anomalies in the current account between January 1, 2024, and March 31, 2024, call the following method when signed in
    to the account.

    Copy code

    ```
    CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_DAILY_CONSUMPTION_ANOMALY_DATA(
      '2024-01-01', '2024-03-31', CURRENT_ACCOUNT_NAME() );
    ```

    To use the output to identify the cost anomalies, look for the days where the value of the `is_anomaly` column is `TRUE`.

Example: Cost anomalies in a different account
:   If you are signed in to the organization account or an ORGADMIN-enabled account, and want to identify cost anomalies in a different
    account, specify the name of the account when you call the GET\_DAILY\_CONSUMPTION\_ANOMALY\_DATA method.

    For example, suppose you are signed in to the organization account `my_orgacct`. You can identify cost anomalies in the account
    `prod_acct` between November 1, 2024, and December 31, 2024 by executing the following command:

    Copy code

    ```
    CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_DAILY_CONSUMPTION_ANOMALY_DATA(
      '2024-11-01', '2024-12-31', 'prod_acct');
    ```

    To use the output to identify the cost anomalies, look for the days where the value of the `is_anomaly` column is `TRUE`.

## Investigate cost anomalies with ANOMALY\_INSIGHTS

The ANOMALY\_INSIGHTS class provides methods that you can use to investigate why a cost anomaly occurred. These methods allow you to drill
down into the following:

- [Account-level consumption](#label-cost-anomaly-investigate-account-class)
- [Warehouse-level consumption](#label-cost-anomaly-investigate-warehouse-class)
- [Query-level consumption](#label-cost-anomaly-investigate-query-class)
- [Hourly consumption by service type](#label-cost-anomaly-investigate-hourly-service-type-class)

### Account-level consumption

Call the [ANOMALY\_INSIGHTS!GET\_TOP\_ACCOUNTS\_BY\_CONSUMPTION](/sql-reference/classes/anomaly-insights/methods/get_top_accounts_by_consumption) method to retrieve a list of accounts with
the highest change in consumption on a given day. Change in consumption is determined by comparing the consumption on a specified day with
consumption on the previous day. This is useful to investigate organization-level cost anomalies.

For example, if you are an administrator who wants to know the top five accounts in terms of change in consumption when comparing
December 14, 2024, and December 15, 2024, execute the following from the organization account or an ORGADMIN-enabled account:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_TOP_ACCOUNTS_BY_CONSUMPTION('2024-12-15', 5);
```

### Warehouse-level consumption

Call the [ANOMALY\_INSIGHTS!GET\_TOP\_WAREHOUSES\_ON\_DATE](/sql-reference/classes/anomaly-insights/methods/get_top_warehouses_on_date) method to retrieve a list of warehouses with the
highest change in consumption on a given day. Change in consumption is determined by comparing the consumption of a warehouse on a specified
day with consumption on the previous day. You can focus on the top warehouses within a specific account or identify top warehouses across
the organization.

Example: Identify top warehouses in the organization
:   To find the top six warehouses in the organization in terms of change in consumption when comparing August 9, 2024, and August 10, 2024,
    sign in to the organization account or an ORGADMIN-enabled account and execute the following:

    Copy code

    ```
    CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_TOP_WAREHOUSES_ON_DATE(
      '2024-08-10', 6, NULL);
    ```

Example: Identify top warehouses in current account
:   To find the top five warehouses in the current account in terms of change in consumption when comparing December 8, 2024, and December 9,
    2024, execute the following:

    Copy code

    ```
    CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_TOP_WAREHOUSES_ON_DATE(
      '2024-12-09', 5, CURRENT_ACCOUNT_NAME());
    ```

Example: Identify top warehouses in a different account
:   To find the top three warehouses in the account `my_acct` in terms of change in consumption when comparing November 8, 2024, and November 9,
    2024, sign in to the organization account or an ORGADMIN-enabled account and execute the following:

    Copy code

    ```
    CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_TOP_WAREHOUSES_ON_DATE(
      '2024-11-09', 5, 'my_acct');
    ```

### Query-level consumption

Call the [ANOMALY\_INSIGHTS!GET\_TOP\_QUERIES\_FROM\_WAREHOUSE](/sql-reference/classes/anomaly-insights/methods/get_top_queries_from_warehouse) method to retrieve a list of queries that ran
on a specific warehouse so you can identify which queries resulted in high consumption. The returned queries are listed in the order of
consumption, from highest to lowest.

You use a Warehouse ID to specify which warehouse you are investigating. You can find the Warehouse ID by calling the
[ANOMALY\_INSIGHTS!GET\_TOP\_WAREHOUSES\_ON\_DATE](/sql-reference/classes/anomaly-insights/methods/get_top_warehouses_on_date) method or querying the
[WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history).

For example, to investigate consumption of a warehouse whose Warehouse ID is `838`, execute the following to list the top six queries that
consumed the most credits on December 1, 2024:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_TOP_QUERIES_FROM_WAREHOUSE(838, '2024-12-01', 6);
```

### Hourly consumption by service type

Call the [ANOMALY\_INSIGHTS!GET\_HOURLY\_CONSUMPTION\_BY\_SERVICE\_TYPE](/sql-reference/classes/anomaly-insights/methods/get_hourly_consumption_by_service_type) method to retrieve the hourly
consumption for a given day, broken down by service type. This allows you to see which service types (for example, `AI_SERVICES`)
are contributing to your consumption during each hour of the day. You can only retrieve data for the account that you are currently
signed in to.

You can specify the number of top service types to return. If you specify `NULL` instead of a number, the method returns all service types
that had non-zero consumption on the specified day.

Example: Top 5 service types
:   To return the hourly consumption on January 15, 2026, broken down by the five services that had the most consumption, run the following:

    Copy code

    ```
    CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_HOURLY_CONSUMPTION_BY_SERVICE_TYPE(
      '2026-01-15',
      5);
    ```

Example: All service types
:   To return the hourly consumption on January 15, 2026, for all service types, run the following:

    Copy code

    ```
    CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_HOURLY_CONSUMPTION_BY_SERVICE_TYPE(
      '2026-01-15',
      NULL);
    ```

## Work with anomaly monitors

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

An [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors) watches a scope that you define with object tags and service types, rather than a whole
account. The ANOMALY\_INSIGHTS class provides methods to create monitors, read their results, and manage their notification lists.

A monitor is identified by its name. Names must be unique within an account and aren’t case-sensitive.

### Monitor configuration

Methods that create, update, or test a monitor accept a configuration as a VARIANT with the following keys:

| Key | Description |
| --- | --- |
| `resource_tags` | An object that describes the tag scope. It contains an `operator` key, which must be `UNION`, and a `tags` key, which is an array of tags. The way you identify a tag depends on the method. Only consumption that belongs to the configuration’s `credit_family` is attributed. |
| `service_types` | An array of account-level [service type](/sql-reference/service-types) names, such as `AUTO_CLUSTERING`. Consumption for an included service type is attributed to the monitor in full, for the whole account. |
| `credit_family` | Either `CREDITS` or `AI-CREDITS`. This determines which service types you can include, and it limits the consumption attributed by the monitor’s tags to that credit family. For more information, see [Credit families](/user-guide/cost-anomalies#label-cost-anomaly-monitor-credit-family). |

Expand

Show lessSee more

A configuration must include at least one tag in `resource_tags.tags` or at least one entry in `service_types`. You can supply either on
its own, or both, but a configuration with neither is invalid.

How you identify a tag depends on the method:

Tag references, for methods that save a monitor
:   [ANOMALY\_INSIGHTS!CREATE\_MONITOR](/sql-reference/classes/anomaly-insights/methods/create_monitor) and
    [ANOMALY\_INSIGHTS!UPDATE\_MONITOR\_CONFIG](/sql-reference/classes/anomaly-insights/methods/update_monitor_config) take each tag as a `[tag_reference, tag_value]` pair, where
    `tag_reference` is the output of [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) called with the `TAG` domain and the
    `APPLYBUDGET` privilege. This is the same pattern that [budgets](/user-guide/budgets) use. You need the `APPLYBUDGET` privilege on a tag to
    create a reference to that tag. Without the privilege, `SYSTEM$REFERENCE` fails before the method runs.

    The following example shows this input shape:

    Copy code

    ```
    OBJECT_CONSTRUCT(
      'resource_tags', OBJECT_CONSTRUCT(
        'operator', 'UNION',
        'tags', ARRAY_CONSTRUCT(
          ARRAY_CONSTRUCT(
            (SELECT SYSTEM$REFERENCE('TAG', 'it.warehouse_management.cost_center', 'SESSION', 'APPLYBUDGET')),
            'engineering'
          )
        )
      ),
      'service_types', ARRAY_CONSTRUCT('AUTO_CLUSTERING'),
      'credit_family', 'CREDITS'
    )
    ```

Tag names, for the ad hoc test method
:   [ANOMALY\_INSIGHTS!ADHOC\_CALCULATE\_ANOMALIES\_FROM\_CONFIG](/sql-reference/classes/anomaly-insights/methods/adhoc_calculate_anomalies_from_config) names each tag directly, using the
    `tagDatabase`, `tagSchema`, `tagName`, and `tagValues` keys. It doesn’t use `SYSTEM$REFERENCE`, and it doesn’t require the `APPLYBUDGET`
    privilege, because nothing is saved and the configuration runs only one time.

    This is the same shape that Snowflake returns when you read a configuration back, so you can copy a saved monitor’s configuration and pass
    it straight to the ad hoc method. For an example, see [Test a configuration before saving](#label-cost-anomaly-monitor-test).

When you read a configuration back, Snowflake returns the tag-name form, grouping values that share a tag:

Copy code

```
{
  "resource_tags": {
    "operator": "UNION",
    "tags": [
      {
        "tagDatabase": "IT",
        "tagSchema": "WAREHOUSE_MANAGEMENT",
        "tagName": "COST_CENTER",
        "tagValues": ["engineering", "platform"]
      }
    ]
  },
  "service_types": ["AUTO_CLUSTERING"],
  "credit_family": "CREDITS"
}
```

Because the resolved form reflects the current state of the catalog, a monitor keeps tracking a tag that you rename. You don’t need to
update the monitor’s configuration.

### Create a monitor

Call [ANOMALY\_INSIGHTS!CREATE\_MONITOR](/sql-reference/classes/anomaly-insights/methods/create_monitor) with a name and a configuration. The call fails if the name is
already in use or if the account already has 20 monitors.

For example, to create a monitor named `Eng-Platform` that tracks credits consumed by resources tagged with the cost center
`engineering`, along with all automatic clustering consumption in the account:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!CREATE_MONITOR(
  'Eng-Platform',
  OBJECT_CONSTRUCT(
    'resource_tags', OBJECT_CONSTRUCT(
      'operator', 'UNION',
      'tags', ARRAY_CONSTRUCT(
        ARRAY_CONSTRUCT(
          (SELECT SYSTEM$REFERENCE('TAG', 'it.warehouse_management.cost_center', 'SESSION', 'APPLYBUDGET')),
          'engineering'
        )
      )
    ),
    'service_types', ARRAY_CONSTRUCT('AUTO_CLUSTERING'),
    'credit_family', 'CREDITS'
  )
);
```

### List and inspect monitors

Call [ANOMALY\_INSIGHTS!LIST\_MONITORS](/sql-reference/classes/anomaly-insights/methods/list_monitors) to return every monitor in the account with its configuration:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!LIST_MONITORS();
```

To return the configuration for a single monitor, call
[ANOMALY\_INSIGHTS!GET\_MONITOR\_CONFIG](/sql-reference/classes/anomaly-insights/methods/get_monitor_config):

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_MONITOR_CONFIG('Eng-Platform');
```

### Update a monitor’s scope

Call [ANOMALY\_INSIGHTS!UPDATE\_MONITOR\_CONFIG](/sql-reference/classes/anomaly-insights/methods/update_monitor_config) to change the tags or service types of an existing monitor.
The monitor keeps its alias, anomaly history, and notification list.

The method interprets each top-level key you pass:

- If you omit a key, its current value is preserved.
- If you pass a key with a non-empty array, the new array replaces the current value.
- If you pass a key with an empty array, the current value is cleared.

Because a monitor’s scope can’t be empty, the method fails if clearing a key would leave the monitor with no tags and no service types.

For example, to remove all service types from a monitor while leaving its tags unchanged:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!UPDATE_MONITOR_CONFIG(
  'Eng-Platform',
  OBJECT_CONSTRUCT('service_types', ARRAY_CONSTRUCT())
);
```

Updating a monitor doesn’t recompute its history immediately. The next daily run picks up the new configuration. To refresh right away,
see [Recalculate a monitor](#label-cost-anomaly-monitor-recalculate).

### Rename or drop a monitor

Call [ANOMALY\_INSIGHTS!RENAME\_MONITOR](/sql-reference/classes/anomaly-insights/methods/rename_monitor) to change a monitor’s name. Everything else about the monitor is
preserved, and no recalculation is triggered.

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!RENAME_MONITOR('Eng-Platform', 'Eng-Foundations');
```

Call [ANOMALY\_INSIGHTS!DROP\_MONITOR](/sql-reference/classes/anomaly-insights/methods/drop_monitor) to delete a monitor. This permanently removes the monitor’s
configuration, anomaly history, and notification list. You can’t recover a dropped monitor.

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!DROP_MONITOR('Eng-Foundations');
```

### Retrieve anomalies for a monitor

Call [ANOMALY\_INSIGHTS!GET\_MONITOR\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/get_monitor_anomalies) to return a monitor’s saved results for a date range. The
output includes one row per day with the consumption attributed to the monitor, the expected range, and whether the day was an anomaly.

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_MONITOR_ANOMALIES(
  'Eng-Platform', '2026-01-01', '2026-03-31');
```

To identify the cost anomalies in the output, look for the days where the value of the `IS_ANOMALY` column is `TRUE`.

### Recalculate a monitor

Snowflake recomputes each monitor daily from the current state of your tags, but it can’t detect changes to which resources carry a tag.
After you tag or untag resources, call [ANOMALY\_INSIGHTS!RECALCULATE\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/recalculate_anomalies) to refresh the monitor’s
full history immediately:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!RECALCULATE_ANOMALIES('Eng-Platform');
```

The method regenerates the full consumption time series and calculates any anomalies, so it takes longer to return than
[ANOMALY\_INSIGHTS!GET\_MONITOR\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/get_monitor_anomalies). The refreshed results are saved. Recalculating doesn’t send
notifications.

### Test a configuration before saving

To see the anomalies a configuration would produce without saving a monitor, call
[ANOMALY\_INSIGHTS!ADHOC\_CALCULATE\_ANOMALIES\_FROM\_CONFIG](/sql-reference/classes/anomaly-insights/methods/adhoc_calculate_anomalies_from_config). The results aren’t saved, and no monitor name
is required.

This method names each tag directly instead of taking a tag reference, so you don’t call
[SYSTEM$REFERENCE](/sql-reference/functions/system_reference) and you don’t need the `APPLYBUDGET` privilege on the tag:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!ADHOC_CALCULATE_ANOMALIES_FROM_CONFIG(
  PARSE_JSON('{
    "credit_family": "CREDITS",
    "resource_tags": {
      "operator": "UNION",
      "tags": [
        {
          "tagDatabase": "IT",
          "tagSchema": "WAREHOUSE_MANAGEMENT",
          "tagName": "DEPT",
          "tagValues": ["finance"]
        }
      ]
    },
    "service_types": ["SERVERLESS_TASK"]
  }'),
  '2026-01-01',
  '2026-03-31'
);
```

### Configure notifications for a monitor

Each monitor has its own email notification list, separate from the account-level and organization-level lists. Set the list with
[ANOMALY\_INSIGHTS!SET\_MONITOR\_NOTIFICATION\_EMAILS](/sql-reference/classes/anomaly-insights/methods/set_monitor_notification_emails), which replaces the existing list rather than adding
to it:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!SET_MONITOR_NOTIFICATION_EMAILS(
  'Eng-Platform', 'user1@example.com,user2@example.com');
```

Each email address must be [verified by the user](/user-guide/ui-snowsight-profile#label-snowsight-verify-email-address). Addresses that aren’t verified aren’t saved,
but the verified addresses in the same call are.

To review the current list, call
[ANOMALY\_INSIGHTS!GET\_MONITOR\_NOTIFICATION\_EMAILS](/sql-reference/classes/anomaly-insights/methods/get_monitor_notification_emails). To review the notifications that were sent for a
monitor, call [ANOMALY\_INSIGHTS!GET\_MONITOR\_NOTIFICATION\_LOG](/sql-reference/classes/anomaly-insights/methods/get_monitor_notification_log). Notification records are retained for
180 days.

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_MONITOR_NOTIFICATION_LOG(
  'Eng-Platform', '2026-01-01', '2026-03-31');
```
