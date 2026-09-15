# ANOMALY\_INSIGHTS!GET\_MONITOR\_CONFIG

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns the configuration for a single [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors) in the current account.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_MONITOR_CONFIG(
  '<alias>' )
```

## Arguments

`'alias'`
:   Name of the monitor. The name isn’t case-sensitive.

    Data type: VARCHAR

## Output

Returns a VARIANT that contains the monitor’s persisted configuration. The `resource_tags` and `service_types` keys are always present,
even when empty. Tags are returned in the resolved form, which names each tag instead of using a reference string. For an example,
see [Monitor configuration](/user-guide/cost-anomalies-class#label-cost-anomaly-monitor-config).

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role
- SNOWFLAKE.APP\_USAGE\_VIEWER application role

## Usage notes

- The method fails if no monitor with the specified name exists in the account.
- To return the configuration for every monitor in one call, use
  [ANOMALY\_INSIGHTS!LIST\_MONITORS](/sql-reference/classes/anomaly-insights/methods/list_monitors).

## Example

Return the configuration for the monitor named `Eng-Platform`:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_MONITOR_CONFIG('Eng-Platform');
```
