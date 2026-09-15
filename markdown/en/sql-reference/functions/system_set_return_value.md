Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$SET\_RETURN\_VALUE

Explicitly sets the return value for a task.

In a [task graph](/user-guide/tasks-graphs#label-task-dag), a task can call this function to set a return value.
Another task that identifies this task as the predecessor task (using the `AFTER` keyword in the task definition)
can retrieve the return value set by the predecessor task using [SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](/sql-reference/functions/system_get_predecessor_return_value).

## Syntax

Copy code

```
SYSTEM$SET_RETURN_VALUE( '<string_expression>' )
```

The value for the `string_expression` argument can be a string literal or a variable; for example, `SYSTEM$SET_RETURN_VALUE(:VARIABLE)`.

## Arguments

`string_expression`
:   The string to set as the return value. The string size must be <= 10 kB (when encoded in UTF8).

## Examples

Create a task that sets a return value. Create a second, child task that runs after the predecessor task has completed.
The child task retrieves the return value set by the predecessor task (by calling [SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](/sql-reference/functions/system_get_predecessor_return_value)) and inserts it into a table row:

> Copy code
>
> ```
> -- Create a table to store the return values.
> CREATE OR REPLACE TABLE return_values_table (str VARCHAR);
>
> -- Create a task that sets the return value for the task.
> CREATE TASK set_return_value_task
>   WAREHOUSE = return_task_wh
>   SCHEDULE = '1 MINUTE'
>   AS
>     CALL SYSTEM$SET_RETURN_VALUE('The quick brown fox jumps over the lazy dog');
>
> -- Create a task that identifies the first task as the predecessor task and retrieves the return value set for that task.
> CREATE TASK get_return_value_task
>   WAREHOUSE = return_task_wh
>   AFTER set_return_value_task
>   AS
>     INSERT INTO return_values_table VALUES(SYSTEM$GET_PREDECESSOR_RETURN_VALUE());
>
>
> -- Note that if there are multiple predecessor tasks that are enabled, you must specify the name of the task to retrieve the return value for that task.
> CREATE TASK get_return_value_by_pred_task
>   WAREHOUSE = return_task_wh
>   AFTER set_return_value_task
>   AS
>     INSERT INTO return_values_table VALUES(SYSTEM$GET_PREDECESSOR_RETURN_VALUE('get_return_value_task'));
>
> -- Resume task (using ALTER TASK ... RESUME).
> -- Wait for task to run on schedule.
>
> SELECT DISTINCT(str) FROM return_values_table;
> +-----------------------------------------------+
> |                      STR                      |
> +-----------------------------------------------+
> |  The quick brown fox jumps over the lazy dog  |
> +-----------------------------------------------+
>
> SELECT DISTINCT(RETURN_VALUE)
>   FROM TABLE(information_schema.task_history())
>   WHERE RETURN_VALUE IS NOT NULL;
>
>
> +-----------------------------------------------+
> |                  RETURN_VALUE                 |
> +-----------------------------------------------+
> |  The quick brown fox jumps over the lazy dog  |
> +-----------------------------------------------+
> ```

### Example 2: Call by using a separate stored procedure

Similar to the first example, but set the return value for the task and retrieve it by calling separate stored procedures:

Copy code

```
-- Create a table to store the return values.
CREATE OR REPLACE TABLE return_values_sp (str VARCHAR);

-- Create a stored procedure that sets the return value for the task.
CREATE OR REPLACE PROCEDURE set_return_value_sp()
RETURNS STRING
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS $$
var stmt = snowflake.createStatement({sqlText:`CALL SYSTEM$SET_RETURN_VALUE('The quick brown fox jumps over the lazy dog');`});
  var res = stmt.execute();
$$;

-- Create a stored procedure that inserts the return value for the predecessor task into the 'return_values_sp' table.
CREATE OR REPLACE PROCEDURE get_return_value_sp()
RETURNS STRING
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS $$
var stmt = snowflake.createStatement({sqlText:`INSERT INTO return_values_sp VALUES(SYSTEM$GET_PREDECESSOR_RETURN_VALUE());`});
var res = stmt.execute();
$$;

-- Create a task that calls the set_return_value_sp stored procedure.
CREATE TASK set_return_value_t
WAREHOUSE=warehouse1
SCHEDULE='1 MINUTE'
AS
  CALL set_return_value_sp();

-- Create a task that calls the get_return_value stored procedure.
CREATE TASK get_return_value_t
WAREHOUSE=warehouse1
AFTER set_return_value_t
AS
  CALL get_return_value_sp();

-- Resume task.
-- Wait for task to run on schedule.

SELECT DISTINCT(str) FROM return_values_sp;
+-----------------------------------------------+
|                      STR                      |
+-----------------------------------------------+
|  The quick brown fox jumps over the lazy dog  |
+-----------------------------------------------+

SELECT DISTINCT(RETURN_VALUE)
  FROM TABLE(information_schema.task_history())
  WHERE RETURN_VALUE IS NOT NULL;

+-----------------------------------------------+
|                  RETURN_VALUE                 |
+-----------------------------------------------+
|  The quick brown fox jumps over the lazy dog  |
+-----------------------------------------------+
```

### Example 3: Use a variable to set the return value

The following example demonstrates how to dynamically generate a return value based on the task’s execution and set the return value by using a variable. In this example, the task loads data from a stream into a landing table and sets the return value to indicate the number of rows loaded:

Copy code

```
CREATE OR REPLACE TASK load_raw_data
WAREHOUSE = 'WH'
WHEN
    SYSTEM$STREAM_HAS_DATA('NEW_WEATHER_DATA')
AS
    DECLARE
        rows_loaded NUMBER;
        result_string VARCHAR;
    BEGIN
        INSERT INTO raw_weather_data ( -- our landing table
            row_id)
        SELECT
            row_id
        FROM
            new_weather_data  -- our source stream
        ;

        -- to see the number of rows loaded in the UI
        rows_loaded := (SELECT $1 FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())));
        result_string := :rows_loaded || ' rows loaded into RAW_WEATHER_DATA';
        -- show result string as task return value
        CALL SYSTEM$SET_RETURN_VALUE(:result_string);
    END;
```
