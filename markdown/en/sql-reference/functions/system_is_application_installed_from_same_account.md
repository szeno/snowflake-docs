Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$IS\_APPLICATION\_INSTALLED\_FROM\_SAME\_ACCOUNT

Shows if an app is installed on the same account as the application package it is based on.

See also:
:   [SYSTEM$IS\_APPLICATION\_SHARING\_EVENTS\_WITH\_PROVIDER](/sql-reference/functions/system_is_application_sharing_events_with_provider)

For more information about event sharing, see [Use logging and event tracing for an app](/developer-guide/native-apps/event-about).

## Syntax

Copy code

```
SYSTEM$IS_APPLICATION_INSTALLED_FROM_SAME_ACCOUNT()
```

## Arguments

None.

## Returns

This function returns the following status messages:

| Status Message | Description |
| --- | --- |
| TRUE | Indicates if an app is installed on the same account as the application package it is based on. |
| FALSE | Indicates if an app is not installed on the same account as the application package it is based on. |

Expand

Show lessSee more

## Access control requirements

- These system functions can only be called from within an app.

## Examples

Copy code

```
SELECT SYSTEM$IS_APPLICATION_INSTALLED_FROM_SAME_ACCOUNT();
```
