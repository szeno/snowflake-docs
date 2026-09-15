Categories:
:   [Context functions](/sql-reference/functions-context) (Alerts)

# GET\_CONDITION\_QUERY\_UUID

Returns the query ID for the SQL statement executed for the condition of an [alert](/user-guide/alerts). In the action for
an alert, you can call this function to
[check the results of the statement for the condition](/user-guide/alerts#label-alerts-check-condition).

## Syntax

Copy code

```
SNOWFLAKE.ALERT.GET_CONDITION_QUERY_UUID()
```

## Arguments

None.

## Returns

The query ID for the SQL statement for the condition of the alert.

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

Refer to [Checking the results of the SQL statement for the condition in the alert action](/user-guide/alerts#label-alerts-check-condition).
