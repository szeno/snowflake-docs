# ANOMALY\_INSIGHTS!UPDATE\_MONITOR\_CONFIG

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Changes the scope of an existing [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors). The monitor keeps its name, anomaly history,
and notification list.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!UPDATE_MONITOR_CONFIG(
  '<alias>',
  <config> )
```

## Arguments

`'alias'`
:   Name of the monitor to update. The name isn’t case-sensitive.

    Data type: VARCHAR

`config`
:   Configuration that defines the monitor’s scope. For the keys this object accepts and how to build a tag reference, see
    [Monitor configuration](/user-guide/cost-anomalies-class#label-cost-anomaly-monitor-config).

    Data type: VARIANT

## Output

Returns a VARIANT that contains the monitor’s persisted configuration. The `resource_tags` and `service_types` keys are always present,
even when empty. Tags are returned in the resolved form, which names each tag instead of using a reference string. For an example,
see [Monitor configuration](/user-guide/cost-anomalies-class#label-cost-anomaly-monitor-config).

The return value always contains the monitor’s full configuration, regardless of which keys you passed.

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role

To include a tag in the monitor’s configuration, you also need the `APPLYBUDGET` privilege on that tag. For more information, see
[Access control for cost anomalies](/user-guide/cost-anomalies-access-control).

## Usage notes

- The method fails if no monitor with the specified name exists in the account. To create a monitor, use
  [ANOMALY\_INSIGHTS!CREATE\_MONITOR](/sql-reference/classes/anomaly-insights/methods/create_monitor).
- Each top-level key in `config` is interpreted independently:

  - If you omit a key, its current value is preserved.
  - If you pass a key with a non-empty array, the new array replaces the current value.
  - If you pass a key with an empty array, the current value is cleared.
- A monitor’s scope can’t be empty. The method fails if the resulting configuration would have no tags in `resource_tags.tags` and no
  entries in `service_types`.
- The method doesn’t recompute the monitor’s history. The next daily run picks up the new configuration. To refresh immediately, use
  [ANOMALY\_INSIGHTS!RECALCULATE\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/recalculate_anomalies).
- The method is atomic. If validation fails, the monitor isn’t changed.

## Examples

Replace the tags in a monitor’s scope, leaving its service types unchanged:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!UPDATE_MONITOR_CONFIG(
  'Eng-Platform',
  OBJECT_CONSTRUCT(
    'resource_tags', OBJECT_CONSTRUCT(
      'operator', 'UNION',
      'tags', ARRAY_CONSTRUCT(
        ARRAY_CONSTRUCT(
          (SELECT SYSTEM$REFERENCE('TAG', 'it.warehouse_management.cost_center', 'SESSION', 'APPLYBUDGET')),
          'platform'
        )
      )
    )
  )
);
```

Remove all service types from a monitor, leaving its tags unchanged:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!UPDATE_MONITOR_CONFIG(
  'Eng-Platform',
  OBJECT_CONSTRUCT('service_types', ARRAY_CONSTRUCT())
);
```
