# ANOMALY\_INSIGHTS!ADHOC\_CALCULATE\_ANOMALIES\_FROM\_CONFIG

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Runs cost anomaly detection against a configuration without creating an [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors). Use this
method to test a combination of tags and service types before you save the combination as a monitor.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!ADHOC_CALCULATE_ANOMALIES_FROM_CONFIG(
  <config>,
  '<start_date>',
  '<end_date>' )
```

## Arguments

`config`
:   Configuration that defines the scope to test. It uses the same keys as the configuration of a saved monitor, but it names each tag directly
    with the `tagDatabase`, `tagSchema`, `tagName`, and `tagValues` keys instead of taking a tag reference. For more information, see
    [Monitor configuration](/user-guide/cost-anomalies-class#label-cost-anomaly-monitor-config).

    Data type: VARIANT

`'start_date'`
:   Specifies the beginning of the time period for which consumption data is returned.

    Data type: DATE

`'end_date'`
:   Specifies the end of the time period for which consumption data is returned.

    Data type: DATE

## Output

Returns a table with one row per day in the time period, with the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| USAGE\_DATE | DATE | Day in UTC when the consumption occurred. |
| CONSUMPTION | NUMBER | Amount of consumption attributed to the monitor on this day. |
| FORECASTED\_CONSUMPTION | NUMBER | Predicted consumption based on the anomaly-detecting algorithm. |
| CURRENCY\_TYPE | VARCHAR | Unit of measure for the consumption, which corresponds to the monitor’s credit family. |
| LOWER\_BOUND | NUMBER | Predicted lowest level of consumption based on the anomaly-detecting algorithm. Consumption levels below this value are considered anomalies. |
| UPPER\_BOUND | NUMBER | Predicted highest level of consumption based on the anomaly-detecting algorithm. Consumption levels above this value are considered anomalies. |
| IS\_ANOMALY | BOOLEAN | If `TRUE`, consumption fell outside the range defined by the lower and upper bounds, so Snowflake identified it as a cost anomaly. |
| ANOMALY\_ID | VARCHAR | System-generated identifier for the anomaly. Empty when `IS_ANOMALY` is `FALSE`. |
| LAST\_REFRESHED\_AT | TIMESTAMP | Time when Snowflake last finished computing results for the monitor. This value is the same for every row. |

Expand

Show lessSee more

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role
- SNOWFLAKE.APP\_USAGE\_VIEWER application role

Unlike [ANOMALY\_INSIGHTS!CREATE\_MONITOR](/sql-reference/classes/anomaly-insights/methods/create_monitor), this method doesn’t require the `APPLYBUDGET` privilege on the
tags in the configuration.

## Usage notes

- This method names each tag directly rather than taking a tag reference, so you don’t call
  [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) to build the configuration. Nothing is saved and the configuration runs only
  one time, so no reference needs to be resolved.
- The tag-name shape is the same one Snowflake returns when you read a configuration back, so you can pass a saved monitor’s configuration
  straight to this method.
- The configuration must include at least one tag in `resource_tags.tags` or at least one entry in `service_types`. The method fails if it
  contains neither.
- The results aren’t saved. To save a configuration as a monitor, use
  [ANOMALY\_INSIGHTS!CREATE\_MONITOR](/sql-reference/classes/anomaly-insights/methods/create_monitor), which takes tag references instead of tag names.
- The method regenerates the full consumption time series and calculates any anomalies, so it takes longer to return than
  [ANOMALY\_INSIGHTS!GET\_MONITOR\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/get_monitor_anomalies).

## Example

Test a configuration that tracks credits consumed by resources tagged with the department `finance`, along with all serverless task
consumption in the account, for consumption between January 1, 2026, and March 31, 2026:

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
