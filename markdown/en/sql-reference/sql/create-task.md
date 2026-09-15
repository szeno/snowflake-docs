# CREATE TASK

Creates a new [task](/user-guide/tasks-intro) in the current/specified schema or replaces an existing task.

This command supports the following variants:

- [CREATE OR ALTER TASK](#label-create-or-alter-task-syntax): Creates a task if it doesn’t exist or alters an existing task.
- [CREATE TASK … CLONE](#label-create-task-clone-syntax): Creates a clone of an existing task.

See also:
:   [ALTER TASK](/sql-reference/sql/alter-task), [DROP TASK](/sql-reference/sql/drop-task), [SHOW TASKS](/sql-reference/sql/show-tasks), [DESCRIBE TASK](/sql-reference/sql/desc-task)

Important

Newly created or cloned tasks are created suspended. For information about running suspended tasks, see [ALTER TASK … RESUME](/sql-reference/sql/alter-task) or [EXECUTE TASK](/sql-reference/sql/execute-task).

## Syntax

Copy code

```
CREATE [ OR REPLACE ] TASK [ IF NOT EXISTS ] <name>
    [ WITH TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
    [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
    [ { WAREHOUSE = <string> }
      | { USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = <string> } ]
    [ SCHEDULE = { '<num> { HOURS | MINUTES | SECONDS }'
      | 'USING CRON <expr> <time_zone>' } ]
    [ CONFIG = <configuration_string> ]
    [ OVERLAP_POLICY = { NO_OVERLAP | ALLOW_CHILD_OVERLAP | ALLOW_ALL_OVERLAP } ]
    [ <session_parameter> = <value>
      [ , <session_parameter> = <value> ... ] ]
    [ USER_TASK_TIMEOUT_MS = <num> ]
    [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
    [ ERROR_INTEGRATION = <integration_name> ]
    [ SUCCESS_INTEGRATION = <integration_name> ]
    [ LOG_LEVEL = '<log_level>' ]
    [ COMMENT = '<string_literal>' ]
    [ FINALIZE = <string> ]
    [ TASK_AUTO_RETRY_ATTEMPTS = <num> ]
    [ USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS = <num> ]
    [ TARGET_COMPLETION_INTERVAL = '<num> { HOURS | MINUTES | SECONDS }' ]
    [ SERVERLESS_TASK_MIN_STATEMENT_SIZE = '{ XSMALL | SMALL
      | MEDIUM | LARGE | XLARGE | XXLARGE }' ]
    [ SERVERLESS_TASK_MAX_STATEMENT_SIZE = '{ XSMALL | SMALL
      | MEDIUM | LARGE | XLARGE | XXLARGE }' ]
  [ AFTER <string> [ , <string> , ... ] ]
  [ EXECUTE AS USER <user_name> ]
  [ WHEN <boolean_expr> ]
  AS
    <sql>
```

## Variant syntax

### CREATE OR ALTER TASK

Creates a new task if it doesn’t already exist, or transforms an existing task into the task defined in the statement.
A CREATE OR ALTER TASK statement follows the syntax rules of a CREATE TASK statement and has the same limitations as an
[ALTER TASK](/sql-reference/sql/alter-task) statement.

Supported task alterations include:

- Change task properties and parameters. For example, SCHEDULE, USER\_TASK\_TIMEOUT\_MS, or COMMENT.
- Set, unset, or change task predecessors.
- Set, unset, or change task condition (WHEN clause).
- Change the task definition (AS clause).

For more information, see [CREATE OR ALTER TASK usage notes](#label-create-or-alter-task-usage-notes) and [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE OR ALTER TASK <name>
    [ { WAREHOUSE = <string> }
      | { USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = <string> } ]
    [ SCHEDULE = { '<num> { HOURS | MINUTES | SECONDS }'
      | 'USING CRON <expr> <time_zone>' } ]
    [ CONFIG = <configuration_string> ]
    [ OVERLAP_POLICY = { NO_OVERLAP | ALLOW_CHILD_OVERLAP | ALLOW_ALL_OVERLAP } ]
    [ USER_TASK_TIMEOUT_MS = <num> ]
    [ <session_parameter> = <value>
      [ , <session_parameter> = <value> ... ] ]
    [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
    [ ERROR_INTEGRATION = <integration_name> ]
    [ SUCCESS_INTEGRATION = <integration_name> ]
    [ COMMENT = '<string_literal>' ]
    [ FINALIZE = <string> ]
    [ TASK_AUTO_RETRY_ATTEMPTS = <num> ]
  [ AFTER <string> [ , <string> , ... ] ]
  [ EXECUTE AS USER <user_name> ]
  [ WHEN <boolean_expr> ]
  AS
    <sql>
```

### CREATE TASK … CLONE

Creates a new task with the same parameter values:

> Copy code
>
> ```
> CREATE [ OR REPLACE ] TASK <name> CLONE <source_task>
>   [ ... ]
> ```

For more details, see [CREATE <object> … CLONE](/sql-reference/sql/create-clone).

Note

Cloning tasks using CREATE TASK <name> CLONE, or cloning a schema containing tasks,
copies all underlying task properties unless explicitly overridden.

## Required parameters

`name`
:   String that specifies the identifier for the task; must be unique for the schema in which the task is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes, such as `"My object"`. Identifiers enclosed in double quotes are also
    case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`sql`
:   Any one of the following:

    - Single SQL statement
    - Call to a stored procedure
    - Procedural logic using [Snowflake Scripting](/developer-guide/snowflake-scripting/index)

    The SQL code is executed when the task runs. Verify that the `sql` executes as expected before using it in a task.

### Clone tasks in a task graph

> For task graphs, you might also need to make clones of each dependent task (that is, each child task or finalizer task); for example:
>
> 1. Clone the task (for example, `CREATE TASK new_task_name CLONE old_task_name`).
> 2. Find dependent tasks by using the [TASK\_DEPENDENTS](/sql-reference/functions/task_dependents) function; for example:
>
>    Copy code
>
>    ```
>    SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_DEPENDENTS('old_task_name'));
>    ```
> 3. Clone the dependent tasks (for example, `CREATE TASK new_child_task CLONE old_child_task`).
> 4. Update the new dependent tasks to use the new cloned task name (`ALTER TASK new_child_task ADD AFTER new_task_name`).

## Optional parameters

`CREATE OR REPLACE TASK` or   
 `CREATE TASK IF NOT EXISTS`

> - `..OR REPLACE`
>   Replaces an existing task with the same name. If the task doesn’t exist, this clause is ignored.
>
>   Consider the following behaviors when you replace a task:
>
>   - The recreated task is suspended by default.
>   - If a standalone or root task is recreated, the next scheduled run of the task is cancelled.
>   - CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.
>   - Tasks with large definitions can cause errors. If you experience an error due to task size, try using a stored procedure or making your task definition less complex.
>
>   When you replace a task, any ongoing task run is completed.
>
>   - To stop an ongoing task run before replacing it with CREATE OR REPLACE TASK, use the [SYSTEM$USER\_TASK\_CANCEL\_ONGOING\_EXECUTIONS](/sql-reference/functions/system_user_task_cancel_ongoing_executions) function.
>   - To stop an ongoing task run after you replace it with CREATE OR REPLACE TASK:
>
>     1. Find the query ID of the ongoing run; for example:
>
>        Copy code
>
>        ```
>        select name, query_id, state, scheduled_time, error_message
>        from table(information_schema.task_history(task_name => 'my_task'));
>        ```
>     2. Cancel the query using the [SYSTEM$CANCEL\_QUERY](/sql-reference/functions/system_cancel_query) function with the query ID, for example:
>
>        Copy code
>
>        ```
>        select system$cancel_query('query_id');
>        ```
>     3. Monitor the task run for a few seconds until the cancel completes, for example:
>
>        Copy code
>
>        ```
>        select name, query_id, state, scheduled_time, error_message
>        from table(information_schema.task_history(task_name => 'my_task'));
>        ```
> - `...IF NOT EXISTS`
>   Creates a new task only if a task with the same name doesn’t already exist. If the task already exists, this clause is ignored.
>
> Note
>
> - The `CREATE OR REPLACE` and `CREATE IF NOT EXISTS` clauses are mutually exclusive. They can’t both be used in the same statement.

`WAREHOUSE = string`
or
  
`USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = string`
> `WAREHOUSE = string`
> :   Specifies the virtual warehouse that provides compute resources for task runs.
>
>     Omit this parameter to use serverless compute resources for runs of this task. Snowflake automatically resizes and scales serverless
>     compute resources as required for each workload. When a schedule is specified for a task, Snowflake adjusts the resource size to
>     complete future runs of the task within the specified time frame. To specify the initial warehouse size for the task, set the
>     `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = string` parameter.
>
> `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = string`
> :   Applied only to serverless tasks.
>
>     Specifies the size of the compute resources to provision for the first run of the task, before a task history is available for
>     Snowflake to determine an ideal size. Once a task has successfully completed a few runs, Snowflake ignores this parameter setting.
>
>     Note that if the task history is unavailable for a given task, the compute resources revert to this initial size.
>
>     Note
>
>     If a `WAREHOUSE = string` parameter value is specified, then setting this parameter produces a user error.
>
>     The size is equivalent to the compute resources available when creating a warehouse (using
>     [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse)), such as `SMALL`, `MEDIUM`, or `LARGE`. The largest size supported by the parameter
>     is `XXLARGE`. If the parameter is omitted, the first runs of the task are executed using a medium-sized (`MEDIUM`) warehouse.
>
>     You can change the initial size (using [ALTER TASK](/sql-reference/sql/alter-task)) after the task is created but
>     before it has run successfully once. Changing the parameter after the first run of this task starts has no effect on the
>     compute resources for current or future task runs.
>
>     Note that suspending and resuming a task doesn’t remove the task history used to size the compute resources. The task history is
>     only removed if the task is recreated (using the CREATE OR REPLACE TASK syntax).
>
>     For more information about this parameter, see [USER\_TASK\_MANAGED\_INITIAL\_WAREHOUSE\_SIZE](/sql-reference/parameters#label-user-task-managed-initial-warehouse-size).

`SCHEDULE = ...`
:   Specifies the schedule for periodically running the task:

    Note

    - For [Triggered tasks](/user-guide/tasks-triggered), a schedule is not required. For other tasks, a schedule must be defined for a standalone task or the root task in a [task graph](/user-guide/tasks-graphs#label-task-dag);
      otherwise, the task only runs if manually executed using [EXECUTE TASK](/sql-reference/sql/execute-task).
    - A schedule cannot be specified for child tasks in a task graph.

    - `'USING CRON expr time_zone'`
      :   Specifies a cron expression and time zone for periodically running the task. Supports a subset of standard cron utility syntax.

      - `'expr'`: The cron expression consists of the following fields:

        Copy code

        ```
        # __________ minute (0-59)
        # | ________ hour (0-23)
        # | | ______ day of month (1-31, or L)
        # | | | ____ month (1-12, JAN-DEC)
        # | | | | __ day of week (0-6, SUN-SAT, or L)
        # | | | | |
        # | | | | |
          * * * * *
        ```

`OVERLAP_POLICY = { NO_OVERLAP | ALLOW_CHILD_OVERLAP | ALLOW_ALL_OVERLAP }`
:   Specifies the overlap policy for task graph runs, controlling whether multiple instances of the task graph can run concurrently and the level of parallelism allowed.

    Note

    - You can only set this parameter on a root task. The setting applies to all tasks in the task graph.

    - `NO_OVERLAP`: Executes tasks serially with no parallelism. Snowflake schedules the next run of a root task only after all
      child tasks in the task graph finish running. If the cumulative time to run all tasks in the task graph exceeds the scheduled
      interval defined for the root task, Snowflake skips at least one task graph run.
    - `ALLOW_CHILD_OVERLAP`: Allows child task parallelism. When the next scheduled run time for the root task occurs while any
      child task is still running, Snowflake starts a new instance of the task graph. If the root task itself is still running when
      the next scheduled run time occurs, Snowflake skips that scheduled run.
    - `ALLOW_ALL_OVERLAP`: Allows unlimited true parallelism. Multiple instances of the entire task graph, including the root
      task, can run concurrently. When the next scheduled run time occurs, Snowflake starts a new instance of the task graph
      immediately, regardless of whether any task (including the root task) is still running.

    Default: `NO_OVERLAP`

`session_parameter = value [ , session_parameter = value ... ]`
:   Specifies a comma-separated list of session parameters to set for the session when the task runs. A task supports all session
    parameters. For the complete list, see [Session parameters](/sql-reference/parameters#label-session-parameters).

    Note

    The following session parameter configurations aren’t supported for tasks:

    - [SEARCH\_PATH](/sql-reference/parameters#label-search-path) set to any value.
    - [AUTOCOMMIT = FALSE](/sql-reference/parameters#label-autocommit).

`USER_TASK_TIMEOUT_MS = num`
:   Specifies the time limit on a single run of the task before it times out (in milliseconds).

    Note

    - Before you increase the time limit on a task significantly, consider whether the SQL statement initiated by the task could be
      optimized (either by rewriting the statement or using a stored procedure) or the warehouse size should be increased.
    - When both [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds) and USER\_TASK\_TIMEOUT\_MS are set, the timeout is the lowest non-zero value of the two parameters.
    - When both [STATEMENT\_QUEUED\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-queued-timeout-in-seconds) and USER\_TASK\_TIMEOUT\_MS are set, the value of USER\_TASK\_TIMEOUT\_MS takes precedence.

    For more information about this parameter, see [USER\_TASK\_TIMEOUT\_MS](/sql-reference/parameters#label-user-task-timeout-ms).

    Values: `0` - `604800000` (7 days). A value of `0` specifies that the maximum timeout value is enforced.

    Default: `3600000` (1 hour)

`SUSPEND_TASK_AFTER_NUM_FAILURES = num`
:   Specifies the number of consecutive failed task runs after which the current task is suspended automatically. Failed task runs
    include runs in which the SQL code in the task body either produces a user error or times out. Task runs that are skipped,
    canceled, or that fail due to a system error are considered indeterminate and aren’t included in the count of failed task runs.

    Set the parameter on a standalone task or the root task in a task graph. When the parameter is set to a value greater than `0`, the
    following behavior applies to runs of the standalone task or task graph:

    - Standalone tasks are automatically suspended after the specified number of consecutive task runs either fail or time out.
    - The root task is automatically suspended after the run of any single task in a task graph fails or times out the specified
      number of times in consecutive runs.

    When the parameter is set to `0`, failed tasks aren’t automatically suspended.

    The setting applies to tasks that rely on either serverless compute resources or virtual warehouse compute resources.

    For more information about this parameter, see [SUSPEND\_TASK\_AFTER\_NUM\_FAILURES](/sql-reference/parameters#label-suspend-task-after-num-failures).

    Values: `0` - No upper limit.

    Default: `10`

`ERROR_INTEGRATION = 'integration_name'`
:   Required only when configuring a task to send error notifications using Amazon Simple Notification Service (SNS), Microsoft Azure Event Grid, or Google Pub/Sub.

    Specifies the name of the notification integration used to communicate with Amazon SNS, MS Azure Event Grid, or Google Pub/Sub. For more information, see
    [Set up error notifications for tasks](/user-guide/tasks-errors).

`SUCCESS_INTEGRATION = 'integration_name'`
:   Required only when configuring a task to send success notifications using Amazon Simple Notification Service (SNS), Microsoft Azure Event Grid, or Google Pub/Sub.

    Specifies the name of the notification integration used to communicate with Amazon SNS, MS Azure Event Grid, or Google Pub/Sub. For more information, see
    [Set up error notifications for tasks](/user-guide/tasks-errors).

`LOG_LEVEL = 'log_level'`
:   Specifies the severity level of [events for this task](/user-guide/tasks-events) that are ingested and made available in
    the active event table. Events at the specified level (and at more severe levels) are ingested.

    For more information about levels, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). For information about setting the log level, see
    [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

`COMMENT = 'string_literal'`
:   Specifies a comment for the task.

    Default: No value

`AFTER string [ , string , ... ]`
:   Specifies one or more predecessor tasks for the current task. Use this option to create a [task graph](/user-guide/tasks-graphs#label-task-dag) or
    add this task to an existing task graph. A task graph is a series of tasks that starts with a scheduled root task and is linked together
    by dependencies.

    Note that the structure of a task graph can be defined after all of its component tasks are created. Execute
    [ALTER TASK](/sql-reference/sql/alter-task) … ADD AFTER statements to specify the predecessors for each task in the planned task graph.

    A task runs after all of its predecessor tasks have finished their own runs successfully (after a brief lag).

    Note

    - The root task should have a defined schedule. Each child task must have one or more defined predecessor tasks, specified
      using the `AFTER` parameter, to link the tasks together.
    - A single task is limited to 100 predecessor tasks and 100 child tasks. In addition, a task graph is limited to a maximum of 1000 tasks
      total (including the root task) in either a resumed or suspended state.
    - Accounts are currently limited to a maximum of 30000 resumed tasks.
    - All tasks in a task graph must have the same task owner. A single role must have the OWNERSHIP privilege on all of the tasks in
      the task graph.
    - All tasks in a task graph must exist in the same schema.
    - The root task must be suspended before any task is recreated (using the CREATE OR REPLACE TASK syntax) or a child task
      is added (using CREATE TASK … AFTER or ALTER TASK … ADD AFTER) or removed (using ALTER TASK … REMOVE AFTER).
    - If any task in a task graph is cloned, the role that clones the task becomes the owner of the clone by default.

      - If the owner of the original task creates the clone, then the task clone retains the link between the task and the predecessor
        task. This means the same predecessor task triggers both the original task and the task clone.
      - If another role creates the clone, then the task clone can have a schedule but not a predecessor.
    - Current limitations:

      - Snowflake guarantees that at most one instance of a task with a defined schedule is running at a given time; however, we cannot
        provide the same guarantee for tasks with a defined predecessor task.

`WHEN boolean_expr`
:   Specifies a Boolean SQL expression; multiple conditions joined with AND/OR are supported. When a task is triggered (based on its
    `SCHEDULE` or `AFTER` setting), it validates the conditions of the expression to determine whether to execute. If the
    conditions of the expression are not met, then the task skips the current run. Any tasks that identify this task as a
    predecessor also don’t run.

    The following are supported in a task WHEN clause:

    - [SYSTEM$STREAM\_HAS\_DATA](/sql-reference/functions/system_stream_has_data) is supported for evaluation in the SQL expression.

      This function indicates whether a specified stream contains change tracking data. You can use this function to evaluate whether the specified stream contains
      change data before starting the current run. If the result is FALSE, then the task doesn’t run.

      Note

      [SYSTEM$STREAM\_HAS\_DATA](/sql-reference/functions/system_stream_has_data) is designed to avoid returning a FALSE value even when the stream contains
      change data. However, this function isn’t guaranteed to avoid returning a TRUE value when the stream contains no change data.
    - [SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](/sql-reference/functions/system_get_predecessor_return_value) is supported for evaluation in the SQL expression.

      This function retrieves the return value for the predecessor task in a task graph. The return value can be used as part of
      a boolean expression. When using SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE, you can cast the returned value to
      the appropriate numeric, string, or boolean type if required.

      Simple examples include:

      Copy code

      ```
      WHEN NOT SYSTEM$GET_PREDECESSOR_RETURN_VALUE('task_name')::BOOLEAN
      ```

      Copy code

      ```
      WHEN SYSTEM$GET_PREDECESSOR_RETURN_VALUE('task_name') != 'VALIDATION'
      ```

      Copy code

      ```
      WHEN SYSTEM$GET_PREDECESSOR_RETURN_VALUE('task_name')::FLOAT < 0.2
      ```

      Note

      Use of [PARSE\_JSON](/sql-reference/functions/parse_json) in TASK … WHEN expressions isn’t supported as it requires warehouse based compute resources.
    - [Boolean operators](/sql-reference/operators-logical) such as AND, OR, NOT, and others.

      Simple example that runs whenever data changes in either of two streams:

      Copy code

      ```
      CREATE TASK my_task
       WAREHOUSE = my_warehouse
       WHEN SYSTEM$STREAM_HAS_DATA('my_customer_stream')
       OR   SYSTEM$STREAM_HAS_DATA('my_order_stream')
       AS
         SELECT CURRENT_TIMESTAMP;
      ```
    - Casts between numeric, string, and boolean types.
    - [Comparison operators](/sql-reference/operators-comparison) such as equal, not equal, greater than, less than, and others.

    Validating the conditions of the WHEN expression does not require compute resources. The validation is instead processed in the cloud
    services layer. A nominal charge accrues each time a task evaluates its WHEN condition and doesn’t run. The charges accumulate each time
    the task is triggered until it runs. At that time, the charge is converted to Snowflake credits and added to the compute resource usage
    for the task run.

    Generally the compute time to validate the condition is insignificant compared to task execution time. As a best practice, align
    scheduled and actual task runs as closely as possible. Avoid task schedules that don’t align with task runs. For
    example, if data is inserted into a table with a stream roughly every 24 hours, don’t schedule a task that checks for stream data
    every minute. The charge to validate the WHEN expression with each run is generally insignificant, but the charges are cumulative.

    Note that daily consumption of cloud services that falls below the
    [10% quota of the daily usage of the compute resources](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage) accumulates no cloud services charges.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`WITH CONTACT ( purpose = contact [ , purpose = contact ...] )`
:   Associate the new object with one or more [contacts](/user-guide/contacts-using).

`FINALIZE = string`
:   Specifies the name of a root task that the finalizer task is associated with. Finalizer tasks run after all other tasks in the task graph run to completion. You can define the SQL of a finalizer task to handle notifications and the release and cleanup of resources that a task graph uses. For more information, see [Finalizer task](/user-guide/tasks-graphs#label-finalizer-task).

    - A root task can only have one finalizer task. If you create multiple finalizer tasks for a root task, the task creation will fail.
    - A finalizer task cannot have any child tasks. Any command attempting to make the finalizer task a predecessor will fail.
    - A finalizer task cannot have a schedule. Creating a finalizer task with a schedule will fail.

    Default: No value

`TASK_AUTO_RETRY_ATTEMPTS = num`
:   Specifies the number of automatic task graph retry attempts. If any task graphs complete in a FAILED state, Snowflake can automatically
    retry the task graphs from the last task in the graph that failed.

    The automatic task graph retry is disabled by default. To enable this feature, set TASK\_AUTO\_RETRY\_ATTEMPTS to a value greater than `0`
    on the root task of a task graph.

    Note that this parameter must be set to the root task of a task graph. If it’s set to a child task, an error will be returned.

    Values: `0` - `30`.

    Default: `0`

`USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS = num`
:   Defines how frequently a task can execute in seconds. If data changes occur more often than the specified minimum, changes will be
    grouped and processed together.

    The task will run every 12 hours even if this value is set to more than 12 hours.

    Values: Minimum `10`, maximum `604800`.

    Default: `30`

`TARGET_COMPLETION_INTERVAL = 'num { HOURS | MINUTES | SECONDS }'`
:   Specifies the desired task completion time. This parameter only applies to serverless tasks. This property is only set on a task.

    This parameter is required when you create serverless [Triggered tasks](/user-guide/tasks-triggered).

    Values: `\{ 10 - 86400 \} SECONDS`, `\{ 1 - 1440 \} MINUTES`, or `\{ 1-24 \} HOURS` (That is, from 10 seconds to the equivalent of 1 day). Accepts positive integers only.

    Also supports the notations: HOUR, MINUTE, SECOND, and H, M, S.

    Default: Snowflake resizes serverless compute resources to complete before the next scheduled execution time.

`SERVERLESS_TASK_MIN_STATEMENT_SIZE = string`
:   Specifies the minimum allowed warehouse size for the serverless task. This parameter only applies to serverless tasks. This parameter can be specified on the task, schema, database, or account. Precedence follows the standard parameter hierarchy.

    Values: Minimum `XSMALL`, Maximum `XXLARGE`. Values are consistent with [WAREHOUSE\_SIZE values](/sql-reference/sql/create-warehouse).

    Also supports the notation: X2LARGE.

    Default: `XSMALL`

    Note that if both SERVERLESS\_TASK\_MIN\_STATEMENT\_SIZE and USER\_TASK\_MANAGED\_INITIAL\_WAREHOUSE\_SIZE are specified, SERVERLESS\_TASK\_MIN\_STATEMENT\_SIZE must be equal to or smaller than USER\_TASK\_MANAGED\_INITIAL\_WAREHOUSE\_SIZE.

`SERVERLESS_TASK_MAX_STATEMENT_SIZE = string`
:   Specifies the maximum allowed warehouse size for the serverless task. This parameter only applies to serverless tasks. This parameter can be specified on the task, schema, database, or account. Precedence follows the standard parameter hierarchy.

    Values: Minimum `XSMALL`, Maximum `XXLARGE`.

    Also supports the notation: X2LARGE.

    Default: `XXLARGE`

    If both SERVERLESS\_TASK\_MIN\_STATEMENT\_SIZE and SERVERLESS\_TASK\_MAX\_STATEMENT\_SIZE are specified, SERVERLESS\_TASK\_MIN\_STATEMENT\_SIZE must be less than or equal to SERVERLESS\_TASK\_MAX\_STATEMENT\_SIZE. SERVERLESS\_TASK\_MAX\_STATEMENT\_SIZE must be equal to or greater than USER\_TASK\_MANAGED\_INITIAL\_WAREHOUSE\_SIZE.

`EXECUTE AS USER user_name`
:   Runs the task on behalf of a specified user account. The user who runs the command must have permissions granted by using the [GRANT IMPERSONATE ON USER TO ROLE](/sql-reference/sql/grant-privilege-user) command.

    For more information, see [Run tasks with user privileges](/user-guide/tasks-intro#label-user-based-security-for-tasks).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| EXECUTE TASK | Account | Required to run any tasks the role owns. Revoking the EXECUTE TASK privilege on a role prevents all subsequent task runs from starting under that role. |
| EXECUTE MANAGED TASK | Account | Required only for tasks that rely on serverless compute resources for runs. |
| CREATE TASK | Schema |  |
| USAGE | Warehouse | Required only for tasks that rely on user-managed warehouses for runs. |
| OWNERSHIP | Task | Required only when executing a [CREATE OR ALTER TASK](#label-create-or-alter-task-syntax) statement for an *existing* task.  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Tasks run using the task owner’s privileges. For the list of minimum required privileges to run tasks, see
  [Task security](/user-guide/tasks-intro#label-task-security-reqs).

  Run the SQL statement or call the stored procedure, as the task owner role, before you include it in a task definition to ensure
  the role has the required privileges on objects referenced by the SQL or stored procedure.
- For serverless tasks:

  - Serverless compute resources for a task can range from the equivalent of `XSMALL` to `XXLARGE` in warehouse sizes. To request a
    size increase, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
  - Individual tasks in a task graph can use serverless or user-managed compute resources. Using the serverless compute for
    all tasks in the task graph isn’t required.
- If a task fails with an unexpected error, you can receive a notification about the error.
  For more information on configuring task error notifications, see [Set up error notifications for tasks](/user-guide/tasks-errors).
- By default, a DML statement executed without explicitly starting a transaction is automatically committed on success or rolled back on
  failure at the end of the statement. This behavior is called *autocommit* and is controlled with the [AUTOCOMMIT](/sql-reference/parameters#label-autocommit) parameter.
  This parameter must be set to TRUE. If the AUTOCOMMIT parameter is set to FALSE at the account level, then set the parameter to
  TRUE for the individual task (using ALTER TASK … SET AUTOCOMMIT = TRUE); otherwise, any DML statement executed by the task fails.
- Only one task should consume data from a stream. Create multiple streams for the same table to be consumed by more than one task. When a
  task consumes the data in a stream using a DML statement, the stream advances the offset and change data is no longer available for the
  next task to consume.
- The `OVERLAP_POLICY` parameter replaces the deprecated `ALLOW_OVERLAPPING_EXECUTION` parameter. For backward compatibility,
  `ALLOW_OVERLAPPING_EXECUTION = TRUE` maps to `OVERLAP_POLICY = ALLOW_CHILD_OVERLAP`, and
  `ALLOW_OVERLAPPING_EXECUTION = FALSE` maps to `OVERLAP_POLICY = NO_OVERLAP`.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## CREATE OR ALTER TASK usage notes

- All limitations of the [ALTER TASK](/sql-reference/sql/alter-task) command apply.
- A task cannot be resumed or suspended using the CREATE OR ALTER TASK command. To resume or suspend a task, use the ALTER TASK command.
- Setting or unsetting a tag is not supported; however, existing tags are *not* altered by a CREATE OR ALTER statement and remain unchanged.

## Examples

### Single SQL statement

Create a serverless task that queries the current timestamp every hour starting at 9:18 a.m. and ending at 5:18 p.m. on Sundays
(America/Los\_Angeles time zone).

The initial warehouse size is XSMALL:

Copy code

```
CREATE TASK t1
  SCHEDULE = 'USING CRON 18 9-17 * * SUN America/Los_Angeles'  -- Use a random minute such as 18
  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
  AS
    SELECT CURRENT_TIMESTAMP;
```

Same as the previous example, but the task relies on a user-managed warehouse to provide the compute resources for runs:

Copy code

```
CREATE TASK mytask_hour
  WAREHOUSE = mywh
  SCHEDULE = 'USING CRON 34 9-17 * * SUN America/Los_Angeles'  -- Use a random minute such as 34
  AS
    SELECT CURRENT_TIMESTAMP;
```

Create a serverless task that inserts the current timestamp into a table every hour. The task sets the [TIMESTAMP\_INPUT\_FORMAT](/sql-reference/parameters#label-timestamp-input-format)
parameter for the session in which the task runs. This session parameter specifies the format of the inserted timestamp:

Copy code

```
CREATE TASK t1
  SCHEDULE = '60 MINUTES'
  TIMESTAMP_INPUT_FORMAT = 'YYYY-MM-DD HH24'
  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
  AS
    INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
```

Create a task that inserts the current timestamp into a table every 5 minutes:

Copy code

```
CREATE TASK mytask_minute
  WAREHOUSE = mywh
  SCHEDULE = '5 MINUTES'
  AS
    INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
```

Create a task that inserts change tracking data for INSERT operations from a stream into a table every 5 minutes. The task polls the
stream using the SYSTEM$STREAM\_HAS\_DATA function to determine whether change data exists and, if the result is `FALSE`, skips the
current run:

Copy code

```
CREATE TASK mytask1
  WAREHOUSE = mywh
  SCHEDULE = '5 MINUTES'
  WHEN
    SYSTEM$STREAM_HAS_DATA('MYSTREAM')
  AS
    INSERT INTO mytable1(id,name) SELECT id, name FROM mystream WHERE METADATA$ACTION = 'INSERT';
```

Create a serverless child task in a task graph and add multiple predecessor tasks. The child task runs only after all specified predecessor
tasks have successfully completed their own runs.

Suppose that the root task for a task graph is `task1` and that `task2`, `task3`, and `task4`
are child tasks of `task1`. This example adds child task `task5` to the task graph and specifies
`task2`, `task3`, and `task4` as predecessor tasks:

Copy code

```
-- Create task5 and specify task2, task3, task4 as predecessors tasks.
-- The new task is a serverless task that inserts the current timestamp into a table column.
CREATE TASK task5
  AFTER task2, task3, task4
AS
  INSERT INTO t1(ts) VALUES(CURRENT_TIMESTAMP);
```

### Stored procedure

Create a task named `my_copy_task` that calls a stored procedure to unload data from the `mytable` table to the named `mystage`
stage (using [COPY INTO <location>](/sql-reference/sql/copy-into-location)) every hour:

Copy code

```
-- Create a stored procedure that unloads data from a table
-- The COPY statement in the stored procedure unloads data to files in a path identified by epoch time (using the Date.now() method)
CREATE OR REPLACE PROCEDURE my_unload_sp()
  returns string not null
  language javascript
  AS
    $$
      var my_sql_command = ""
      var my_sql_command = my_sql_command.concat("copy into @mystage","/",Date.now(),"/"," from mytable overwrite=true;");
      var statement1 = snowflake.createStatement( {sqlText: my_sql_command} );
      var result_set1 = statement1.execute();
    return my_sql_command; // Statement returned for info/debug purposes
    $$;

-- Create a task that calls the stored procedure every hour
CREATE TASK my_copy_task
  WAREHOUSE = mywh
  SCHEDULE = '60 MINUTES'
  AS
    CALL my_unload_sp();
```

### Multiple SQL statements

Create a task that executes multiple SQL statements. In this example, the task modifies the TIMESTAMP\_OUTPUT\_FORMAT for the session and
then queries the CURRENT\_TIMESTAMP function.

Copy code

```
CREATE OR REPLACE TASK test_logging
  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
  SCHEDULE = 'USING CRON 37 * * * * America/Los_Angeles'  -- Use a random minute such as 37
  AS
    BEGIN
      ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF';
      SELECT CURRENT_TIMESTAMP;
    END;
```

### Procedural logic using Snowflake Scripting

Create a task that declares a variable, uses the variable, and returns the value of the variable every 15 seconds:

Copy code

```
CREATE TASK t1
  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
  SCHEDULE = '15 SECONDS'
  AS
    DECLARE
      radius_of_circle float;
      area_of_circle float;
    BEGIN
      radius_of_circle := 3;
      area_of_circle := pi() * radius_of_circle * radius_of_circle;
      return area_of_circle;
    END;
```

### Root task with configuration

Create a task that specifies configuration, and then reads that configuration.

Copy code

```
CREATE OR REPLACE TASK root_task_with_config
  WAREHOUSE=mywarehouse
  SCHEDULE='10 m'
  CONFIG=$${"output_dir": "/temp/test_directory/", "learning_rate": 0.1}$$
  AS
    BEGIN
      LET OUTPUT_DIR STRING := SYSTEM$GET_TASK_GRAPH_CONFIG('output_dir')::string;
      LET LEARNING_RATE DECIMAL := SYSTEM$GET_TASK_GRAPH_CONFIG('learning_rate')::DECIMAL;
    ...
    END;
```

### Finalizer task

Create a finalizer task, associated with the root task of a task graph, that sends an email alert after task completion. For more
information about finalizer tasks, see [Finalizer task](/user-guide/tasks-graphs#label-finalizer-task).

Copy code

```
CREATE TASK finalize_task
  WAREHOUSE = my_warehouse
  FINALIZE = my_root_task
  AS
    CALL SYSTEM$SEND_EMAIL(
      'my_email_int',
      'first.last@example.com, first2.last2@example.com',
      'Email Alert: Task A has finished.',
      'Task A has successfully finished.\nStart Time: 10:10:32\nEnd Time: 12:15:45\nTotal Records Processed: 115678'
    );
```

### Triggered task

Create a triggered task, associated with a stream, that inserts data from the specified stream into the table every time there is new data in the stream. For more information, see [Triggered tasks](/user-guide/tasks-triggered).

Copy code

```
CREATE TASK triggeredTask
  WAREHOUSE = my_warehouse
  WHEN system$stream_has_data('my_stream')
  AS
    INSERT INTO my_downstream_table
    SELECT * FROM my_stream;

ALTER TASK triggeredTask RESUME;
```

### Create and alter a simple task using the CREATE OR ALTER TASK command

Create a task `my_task` to execute every hour in warehouse `my_warehouse`:

Copy code

```
CREATE OR ALTER TASK my_task
  WAREHOUSE = my_warehouse
  SCHEDULE = '60 MINUTES'
  AS
    SELECT PI();
```

Alter task `my_task` to execute after task `my_other_task` and update the task definition:

Copy code

```
CREATE OR ALTER TASK my_task
  WAREHOUSE = regress
  AFTER my_other_task
  AS
    SELECT 2 * PI();
```
