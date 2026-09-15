# Monitor task runs

## Monitor task errors

You can configure Snowflake to push notifications when errors occur in task runs. You can also query the event table to
determine if tasks failed to run. For more information, see the following sections:

- [Set up error notifications for tasks](/user-guide/tasks-errors)
- [Monitor events for task executions](/user-guide/tasks-events)

## See task owners

To see who ran a task that is currently being run, see [SHOW TASKS](/sql-reference/sql/show-tasks) or [DESCRIBE TASK](/sql-reference/sql/desc-task).

- Check the OWNER column to see the role of the task owner.
- To see if the task has been run on behalf of the task owner, check the EXECUTE\_AS\_USER column. By default, this shows as NULL, but when the task is run using impersonated privileges, the user name of the user who modified the task is displayed.

To see who ran a task, use the [QUERY\_HISTORY](/sql-reference/account-usage/query_history) view.

- If the task is not run as an actual user, the QUERY EXECUTED BY TASK column displays the user name as “SYSTEM”.
- If the task is running on behalf of another user, the QUERY EXECUTED BY TASK column displays the user name that the task is running on behalf of.
