Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$BEHAVIOR\_CHANGE\_BUNDLE\_STATUS

Returns the status of the specified [behavior change release bundle](/release-notes/behavior-change-policy#label-behavior-change-bundles) for the current account.

See also:
:   [SYSTEM$ENABLE\_BEHAVIOR\_CHANGE\_BUNDLE](/sql-reference/functions/system_enable_behavior_change_bundle),
    [SYSTEM$DISABLE\_BEHAVIOR\_CHANGE\_BUNDLE](/sql-reference/functions/system_disable_behavior_change_bundle),
    [SYSTEM$SHOW\_ACTIVE\_BEHAVIOR\_CHANGE\_BUNDLES](/sql-reference/functions/system_show_active_behavior_change_bundles)

## Syntax

Copy code

```
SYSTEM$BEHAVIOR_CHANGE_BUNDLE_STATUS( '<bundle_name>' )
```

## Arguments

`bundle_name`
:   Name of the behavior change bundle, specified as a string. To obtain the name for a bundle, see
    [Behavior change announcements](/release-notes/behavior-changes).

## Returns

Returns one of the following VARCHAR values:

- `ENABLED` (if the specified bundle is enabled for the current account)
- `DISABLED` (if the specified bundle is disabled for the current account)
- `RELEASED` (if the specified bundle is
  [generally enabled](/release-notes/behavior-change-policy#label-behavior-change-bundles-generally-enabled) for the current account and thus permanently enabled)

## Examples

The following example returns the status of the `2020_08` behavior change bundle for the current account.

Copy code

```
SELECT SYSTEM$BEHAVIOR_CHANGE_BUNDLE_STATUS('2020_08');
```

```
+-------------------------------------------------+
| SYSTEM$BEHAVIOR_CHANGE_BUNDLE_STATUS('2020_08') |
|-------------------------------------------------|
| DISABLED                                        |
+-------------------------------------------------+
```
