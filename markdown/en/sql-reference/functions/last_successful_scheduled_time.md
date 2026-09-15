Categories:
:   [Date & time functions](/sql-reference/functions-date-time) (Alerts)

# LAST\_SUCCESSFUL\_SCHEDULED\_TIME

Returns the timestamp representing the scheduled time for the most recent successful evaluation of the alert condition, where no
errors occurred when executing the action. (In the [alert history](/user-guide/alerts#label-alerts-history), these are the alerts with the
STATE CONDITION\_FALSE or TRIGGERED.) Refer to [Specifying timestamps based on alert schedules](/user-guide/alerts#label-alerts-specify-timestamps).

## Syntax

Copy code

```
SNOWFLAKE.ALERT.LAST_SUCCESSFUL_SCHEDULED_TIME()
```

## Arguments

None.

## Returns

TIMESTAMP\_LTZ value that represents when the most recent successful evaluation of the alert condition was scheduled, or NULL
if there are no recent successful evaluations of the alert condition.

## Usage notes

- This function is defined in the ALERT schema of the SNOWFLAKE database.

  To call this function, you must use a role that is granted the
  [SNOWFLAKE database role](/sql-reference/snowflake-db-roles) ALERT\_VIEWER. For example, to call the function as a user
  with the role alert\_role, execute:

  Copy code

  ```
  GRANT DATABASE ROLE snowflake.alert_viewer TO ROLE alert_role;
  ```
- This function can only be called from within an [alert](/user-guide/alerts).

## Examples

Refer to [Specifying timestamps based on alert schedules](/user-guide/alerts#label-alerts-specify-timestamps).
