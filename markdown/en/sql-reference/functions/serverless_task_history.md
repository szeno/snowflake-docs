Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# SERVERLESS\_TASK\_HISTORY

This table function is used for querying the [serverless task](/user-guide/tasks-intro#label-tasks-compute-resources) usage history. The information returned
by the function includes the task name and credits consumed by runs of each task.

Note

This function is generally deprecated in favor of the
[ACCOUNT\_USAGE.SERVERLESS\_TASK\_HISTORY view](/sql-reference/account-usage/serverless_task_history),
which provides a more complete data set and supports longer date ranges.

## Syntax

Copy code

```
SERVERLESS_TASK_HISTORY(
      [ DATE_RANGE_START => <constant_expr> ]
      [ , DATE_RANGE_END => <constant_expr> ]
      [ , TASK_NAME => '<string>' ] )
```

## Arguments

All of the arguments are optional.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   Date/time range of the usage window:

    - If an end date is not specified, then [CURRENT\_DATE](/sql-reference/functions/current_date) is used as the end of the range.
    - If a start date is not specified, then the range starts 10 minutes prior to the start of `DATE_RANGE_END` (i.e. the default is to
      show the previous 10 minutes of the usage history). For example, if `DATE_RANGE_END` is [CURRENT\_DATE](/sql-reference/functions/current_date), then the default
      `DATE_RANGE_START` is 11:50 PM on the previous day.

`TASK_NAME => string`
:   The name of the task to retrieve usage history for. Only the usage data for the specified task is returned.

    Note that the task name must be enclosed in single quotes. Also, if the task name contains any spaces, mixed-case characters, or special
    characters, the name must be double-quoted within the single quotes (e.g. `'"My Task"'` vs `'mytask'`).

## Usage notes

- Returns results only for the ACCOUNTADMIN role or any role that has been explicitly granted the MONITOR USAGE global privilege.

  Note

  A role with the MONITOR USAGE privilege can view per-object credit usage, but not object names.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be
  fully-qualified. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).
- The history is displayed in increments of 1 hour.

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| TASK\_NAME | TEXT | Name of the task. |
| CREDITS\_USED | TEXT | Number of credits billed for serverless task usage during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Examples

Retrieve the usage history for a one-hour range for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.serverless_task_history(
>     date_range_start=>'2021-10-08 19:00:00.000',
>     date_range_end=>'2021-10-08 20:00:00.000'));
> ```
>
> Sample output:
>
> Copy code
>
> ```
> +-------------------------------+-------------------------------+-----------+--------------+
> | START_TIME                    | END_TIME                      | TASK_NAME | CREDITS_USED |
> |-------------------------------+-------------------------------+-----------+--------------|
> | 2021-10-08 04:16:22.000 -0700 | 2021-10-08 05:16:22.000 -0700 | T1        |  0.000286714 |
> | 2021-10-08 05:16:22.000 -0700 | 2021-10-08 06:16:22.000 -0700 | T1        |  0.007001568 |
> +-------------------------------+-------------------------------+-----------+--------------+
> ```

Retrieve the history for the last 12 hours for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.serverless_task_history(
>     date_range_start=>dateadd(H, -12, current_timestamp)));
> ```

Retrieve the history for the past week for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.serverless_task_history(
>     date_range_start=>dateadd(D, -7, current_date),
>     date_range_end=>current_date));
> ```

Retrieve the usage history for the past week for a specified task in your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.serverless_task_history(
>     date_range_start=>dateadd(D, -7, current_date),
>     date_range_end=>current_date,
>     task_name=>'mydb.myschema.mytask'));
> ```
