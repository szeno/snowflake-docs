# ANOMALY\_INSIGHTS!LIST\_MONITORS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns every [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors) defined in the current account, along with each monitor’s
configuration.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!LIST_MONITORS()
```

## Arguments

None.

## Output

Returns a table with one row per monitor, with the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| ALIAS | VARCHAR | Name of the monitor. |
| CONFIG | VARIANT | The monitor’s persisted configuration. For the keys this object contains, see [Monitor configuration](/user-guide/cost-anomalies-class#label-cost-anomaly-monitor-config). |

Expand

Show lessSee more

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role
- SNOWFLAKE.APP\_USAGE\_VIEWER application role

## Usage notes

- Rows are sorted by name in ascending order, without regard to case.
- If the account has no monitors, the method returns an empty result, which isn’t an error.
- To return the configuration for a single monitor, use
  [ANOMALY\_INSIGHTS!GET\_MONITOR\_CONFIG](/sql-reference/classes/anomaly-insights/methods/get_monitor_config).

## Example

List all monitors in the current account:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!LIST_MONITORS();
```
