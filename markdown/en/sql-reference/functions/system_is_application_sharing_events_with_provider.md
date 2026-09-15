Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$IS\_APPLICATION\_SHARING\_EVENTS\_WITH\_PROVIDER

Shows if event sharing is enabled.

See also:
:   [SYSTEM$IS\_APPLICATION\_INSTALLED\_FROM\_SAME\_ACCOUNT](/sql-reference/functions/system_is_application_installed_from_same_account)

For more information about event sharing, see [Use logging and event tracing for an app](/developer-guide/native-apps/event-about).

## Syntax

Copy code

```
SYSTEM$IS_APPLICATION_SHARING_EVENTS_WITH_PROVIDER()
```

## Arguments

None.

## Returns

This function returns the following status messages:

| Status Message | Description |
| --- | --- |
| TRUE | Indicates that event sharing is enabled on the app and the app has an active event table. |
| FALSE | Indicates that event sharing is not enabled on the app. |

Expand

Show lessSee more

## Access control requirements

- These system functions can only be called from within an app.

## Examples

Copy code

```
SELECT SYSTEM$IS_APPLICATION_SHARING_EVENTS_WITH_PROVIDER();
```
