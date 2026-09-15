# ANOMALY\_INSIGHTS!CREATE\_MONITOR

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates an [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors), which detects cost anomalies for a custom scope that you define with
object tags and service types.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!CREATE_MONITOR(
  '<alias>',
  <config> )
```

## Arguments

`'alias'`
:   Name for the new monitor. The name must be unique within the account and isn’t case-sensitive.

    Data type: VARCHAR

`config`
:   Configuration that defines the monitor’s scope. For the keys this object accepts and how to build a tag reference, see
    [Monitor configuration](/user-guide/cost-anomalies-class#label-cost-anomaly-monitor-config).

    Data type: VARIANT

## Output

Returns a VARIANT that contains the monitor’s persisted configuration. The `resource_tags` and `service_types` keys are always present,
even when empty. Tags are returned in the resolved form, which names each tag instead of using a reference string. For an example,
see [Monitor configuration](/user-guide/cost-anomalies-class#label-cost-anomaly-monitor-config).

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role

To include a tag in the monitor’s configuration, you also need the `APPLYBUDGET` privilege on that tag. For more information, see
[Access control for cost anomalies](/user-guide/cost-anomalies-access-control).

## Usage notes

- The method fails if a monitor with the same name already exists in the account. To change an existing monitor, use
  [ANOMALY\_INSIGHTS!UPDATE\_MONITOR\_CONFIG](/sql-reference/classes/anomaly-insights/methods/update_monitor_config).
- The configuration must include at least one tag in `resource_tags.tags` or at least one entry in `service_types`. The method fails if it
  contains neither.
- The method fails if the account already contains 20 monitors.
- The method is atomic. If validation fails, no monitor is created.
- Creating a monitor doesn’t compute results immediately. The next daily run computes the monitor’s history. To compute results right away,
  use [ANOMALY\_INSIGHTS!RECALCULATE\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/recalculate_anomalies).

## Example

Create a monitor named `Eng-Platform` that tracks credits consumed by resources tagged with the cost center `engineering`, along with all
automatic clustering consumption in the account:

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
