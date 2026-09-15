Categories:
:   [Date & time functions](/sql-reference/functions-date-time) (Alerts)

# SCHEDULED\_TIME

Returns the timestamp representing the scheduled time of the current alert. Refer to [Specifying timestamps based on alert schedules](/user-guide/alerts#label-alerts-specify-timestamps).

## Syntax

Copy code

```
SNOWFLAKE.ALERT.SCHEDULED_TIME()
```

## Arguments

None.

## Returns

TIMESTAMP\_LTZ value that represents the scheduled time of the current alert.

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
