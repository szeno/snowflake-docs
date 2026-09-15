Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$IS\_APPLICATION\_ALL\_MANDATORY\_TELEMETRY\_EVENT\_DEFINITIONS\_ENABLED

Indicates that the AUTHORIZE\_TELEMETRY\_EVENT\_SHARING property has been set on the app.

## Syntax

Copy code

```
SYSTEM$IS_APPLICATION_ALL_MANDATORY_TELEMETRY_EVENT_DEFINITIONS_ENABLED
```

## Returns

- Returns `TRUE` if the AUTHORIZE\_TELEMETRY\_EVENT\_SHARING property is set
  on the app. This indicates that event sharing is allowed in the consumer account.
  Otherwise, returns `FALSE`.

  For more information, see [Determine information about event sharing in the consumer account](/developer-guide/native-apps/event-develop).
