Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ENABLE\_BEHAVIOR\_CHANGE\_BUNDLE

Enables behavior changes included in the specified [behavior change release bundle](/release-notes/behavior-change-policy#label-behavior-change-bundles) for the
current account.

By default, behavior change bundles are not enabled during the pre-announcement period. Use this function to test behavior changes before they are enabled for your account.

See also:
:   [SYSTEM$DISABLE\_BEHAVIOR\_CHANGE\_BUNDLE](/sql-reference/functions/system_disable_behavior_change_bundle),
    [SYSTEM$BEHAVIOR\_CHANGE\_BUNDLE\_STATUS](/sql-reference/functions/system_behavior_change_bundle_status)
    [SYSTEM$SHOW\_ACTIVE\_BEHAVIOR\_CHANGE\_BUNDLES](/sql-reference/functions/system_show_active_behavior_change_bundles)

## Syntax

Copy code

```
SYSTEM$ENABLE_BEHAVIOR_CHANGE_BUNDLE( '<bundle_name>' )
```

## Arguments

`bundle_name`
:   Name of the behavior change bundle, specified as a string. To obtain the name for a bundle, see
    [Behavior change announcements](/release-notes/behavior-changes).

## Returns

Returns the VARCHAR value `ENABLED` if the function successfully enables the behavior changes.

## Usage notes

- You cannot call this function from within a stored procedure or user-defined function (UDF).

## Examples

The following example enables the `2020_08` behavior change bundle for the current account.

Copy code

```
SELECT SYSTEM$ENABLE_BEHAVIOR_CHANGE_BUNDLE('2020_08');
```

```
+-------------------------------------------------+
| SYSTEM$ENABLE_BEHAVIOR_CHANGE_BUNDLE('2020_08') |
|-------------------------------------------------|
| ENABLED                                         |
+-------------------------------------------------+
```
