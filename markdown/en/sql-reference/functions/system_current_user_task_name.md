Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$CURRENT\_USER\_TASK\_NAME

Returns the name of the task currently executing when invoked from the statement or stored procedure defined by the task.

## Syntax

Copy code

```
SYSTEM$CURRENT_USER_TASK_NAME()
```

## Arguments

None.

## Examples

Insert the name of the current task into a table along with the current time:

> Copy code
>
> ```
> CREATE TASK mytask
>   WAREHOUSE = mywh,
>   SCHEDULE = '5 MINUTE'
> AS
>   INSERT INTO mytable(ts, task) VALUES(CURRENT_TIMESTAMP, SYSTEM$CURRENT_USER_TASK_NAME());
>
> SELECT * FROM mytable;
>
> +-------------------------+------------------------------------+
> | TS                      | TASK                               |
> |-------------------------+------------------------------------|
> | 2018-11-15 07:41:33.463 | MYDB.PUBLIC.MYTASK                 |
> +-------------------------+------------------------------------+
> ```
