# ALTER TASK

Modifies the properties for an existing task.

For information about tasks, see [Introduction to tasks](/user-guide/tasks-intro).

See also:
:   [CREATE TASK](/sql-reference/sql/create-task), [DROP TASK](/sql-reference/sql/drop-task), [SHOW TASKS](/sql-reference/sql/show-tasks), [DESCRIBE TASK](/sql-reference/sql/desc-task)

## Syntax

Copy code

```
ALTER TASK [ IF EXISTS ] <name> RESUME | SUSPEND

ALTER TASK [ IF EXISTS ] <name> REMOVE AFTER <string> [ , <string> , ... ]
  | ADD AFTER <string> [ , <string> , ... ]

ALTER TASK [ IF EXISTS ] <name> SET
  [ { WAREHOUSE = <string> }
    | { USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = <string> } ]
  [ SCHEDULE = { '<num> { HOURS | MINUTES | SECONDS }'
               | 'USING CRON <expr> <time_zone>' } ]
  [ CONFIG = <configuration_string> ]
  [ OVERLAP_POLICY = { NO_OVERLAP | ALLOW_CHILD_OVERLAP | ALLOW_ALL_OVERLAP } ]
  [ USER_TASK_TIMEOUT_MS = <num> ]
  [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
  [ ERROR_INTEGRATION = <integration_name> ]
  [ SUCCESS_INTEGRATION = <integration_name> ]
  [ LOG_LEVEL = '<log_level>' ]
  [ COMMENT = <string> ]
  [ <session_parameter> = <value>
    [ , <session_parameter> = <value> ... ] ]
  [ TASK_AUTO_RETRY_ATTEMPTS = <num> ]
  [ USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS = <num> ]
  [ TARGET_COMPLETION_INTERVAL = '<num> { HOURS | MINUTES | SECONDS }' ]
  [ SERVERLESS_TASK_MIN_STATEMENT_SIZE= 'XSMALL | SMALL
    | MEDIUM | LARGE | XLARGE | XXLARGE' ]
  [ SERVERLESS_TASK_MAX_STATEMENT_SIZE= 'XSMALL | SMALL
    | MEDIUM | LARGE | XLARGE | XXLARGE' ]
  [ CONTACT <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ]
  [ EXECUTE AS USER <user_name> ]

ALTER TASK [ IF EXISTS ] <name> UNSET
  [ WAREHOUSE ]
  [ SCHEDULE ]
  [ CONFIG ]
  [ OVERLAP_POLICY ]
  [ USER_TASK_TIMEOUT_MS ]
  [ SUSPEND_TASK_AFTER_NUM_FAILURES ]
  [ LOG_LEVEL ]
  [ COMMENT ]
  [ <session_parameter> [ , <session_parameter> ... ] ]
  [ TARGET_COMPLETION_INTERVAL ]
  [ SERVERLESS_TASK_MIN_STATEMENT_SIZE ]
  [ SERVERLESS_TASK_MAX_STATEMENT_SIZE ]
  [ CONTACT <purpose> [ , ... ]]
  [ EXECUTE AS USER ]
  [ DCM PROJECT ]

ALTER TASK [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>'
  [ , <tag_name> = '<tag_value>' ... ]

ALTER TASK [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER TASK [ IF EXISTS ] <name> SET FINALIZE = <string>

ALTER TASK [ IF EXISTS ] <name> UNSET FINALIZE

ALTER TASK [ IF EXISTS ] <name> MODIFY AS <sql>

ALTER TASK [ IF EXISTS ] <name> MODIFY WHEN <boolean_expr>

ALTER TASK [ IF EXISTS ] <name> REMOVE WHEN
```

## Parameters

`name`
:   Identifier for the task to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in double
    quotes. Identifiers enclosed in double quotes are also case-sensitive.

`RESUME | SUSPEND`
:   Specifies the action to perform on the task:

    - `RESUME` brings a suspended task to the ‘Started’ state. Note that accounts are currently limited to a maximum of 30000 started
      tasks.

      Before resuming the root task of your Task Graph, resume all child tasks. To recursively resume the root task’s child
      tasks, use [SYSTEM$TASK\_DEPENDENTS\_ENABLE](/sql-reference/functions/system_task_dependents_enable).
    - `SUSPEND` puts the task into a ‘Suspended’ state.

    If the task schedule is set to an interval of (`number { HOURS | MINUTES | SECONDS }`), the *base interval time* for the schedule is reset to the current time the task is resumed.

    The base interval time starts the interval counter from the current clock time. For example, if an INTERVAL value of `10 MINUTES` is set and
    the task is resumed at 9:03 AM, then the task runs at 9:13 AM, 9:23 AM, and so on. Note that we only guarantee that tasks don’t execute
    *before* their set interval occurs. In the current example, the task could first run at 9:14 AM, but won’t run at 9:12 AM.

`REMOVE AFTER string [ , string , ... ]`
:   Specifies the names of one or more current predecessor tasks for this child task in a [task graph](/user-guide/tasks-graphs#label-task-dag).

    When all predecessors for a child task are removed, then the former child task becomes either a standalone task or a root task, depending on
    whether other tasks identify this former child task as their predecessor. If the former child task becomes a root task, this task is suspended
    by default and must be resumed manually.

`ADD AFTER string [ , string , ... ]`
:   Specifies the names of one or more existing tasks to add as predecessors for this child task in a [task graph](/user-guide/tasks-graphs#label-task-dag).
    Each child task in a task graph runs when all predecessor tasks finish their runs successfully. For more information, see the description
    of the `AFTER` parameter in [CREATE TASK](/sql-reference/sql/create-task).

    Each child task is limited to 100 predecessor tasks.

`SET ...`
:   Specifies either or both of the following:

    - One or more properties to set for the task, which are separated by blank spaces, commas, or new lines. For more details about the properties you
      can set, see [CREATE TASK](/sql-reference/sql/create-task).

      When you set the configuration on a task, you specify the default configuration string for the task. You can override the default configuration
      for a single execution by using the [EXECUTE TASK](/sql-reference/sql/execute-task) command.
    - A comma-separated list of session parameters to set for the session when the task runs. A task supports all session parameters. For the
      complete list, see [Parameters](/sql-reference/parameters).
    - `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
      :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

          The tag value is always a string, and the maximum number of characters for the tag value is 256.

          For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).
    - `CONTACT purpose = contact [ , purpose = contact ... ]`
      :   Associate the existing object with one or more [contacts](/user-guide/contacts-using). For a list of valid purposes, see [Associate a contact with an object](/user-guide/contacts-using#label-contacts-associate).

          You cannot set the CONTACT property with other properties in the same statement.

`UNSET ...`
:   Specifies one (or more) properties and/or session parameters to unset for the task, which resets them to the defaults.

    You can reset multiple properties/parameters with a single ALTER statement; however, each property/parameter must be separated by a
    comma. When resetting a property/parameter, specify only the name; specifying a value for the property/parameter will return an error.

    To detach a contact from the task, specify `UNSET CONTACT purpose`. You cannot unset the CONTACT property with other properties in
    the same statement.

`UNSET DCM PROJECT`

> Detaches the task from the [DCM project](/user-guide/dcm-projects/dcm-projects-overview) that currently manages it.
> The command removes the association between the task and the DCM project without dropping the task. See [Detach objects from a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-detach-object) for more information.

`sql`
:   Specifies the SQL code to execute when the task runs:

    - Single SQL statement
    - Call to a stored procedure
    - Procedural logic using [Snowflake Scripting](/developer-guide/snowflake-scripting/index)

      Note that currently, Snowsight does not support creating or modifying tasks to use Snowflake Scripting.
      Instead, use SnowSQL or another command-line client.

    Note

    Verify that the SQL code you reference in a task executes as expected before you create the task. Tasks are intended to
    automate SQL code that has already been tested thoroughly.

`WHEN boolean_expr`
:   Specifies a Boolean SQL expression. When a task is triggered, it validates the conditions of the expression to determine whether to
    execute. If the conditions of the expression are not met, then the task skips the current run. Any tasks that identify this task
    as a predecessor also do not run.

    Validating the conditions of the WHEN expression does not require a virtual warehouse. The validation is instead processed in the cloud
    services layer. A nominal charge accrues each time a task evaluates its WHEN condition and does not run. The charges accumulate each time
    the task is triggered until it runs. At that time, the charge is converted to Snowflake credits and added to the compute resource usage
    for the task run.

    Generally the compute time to validate the condition is insignificant compared to task execution time. As a best practice, align
    scheduled and actual task runs as closely as possible. Avoid task schedules that are wildly out of sync with actual task runs. For
    example, if data is inserted into a table with a stream roughly every 24 hours, don’t schedule a task that checks for stream data every
    minute. The charge to validate the WHEN expression with each run is generally insignificant, but the charges are cumulative.

    Note that daily consumption of cloud services that falls below the
    [10% quota of the daily usage of the compute resources](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage) accumulates no cloud services charges.

    Currently, the following functions are supported for evaluation in the SQL expression:

    [SYSTEM$STREAM\_HAS\_DATA](/sql-reference/functions/system_stream_has_data)
    :   Indicates whether a specified stream contains change tracking data. Used to run a triggered task if no schedule is defined for the
        task. You can also use this to skip the current task run if the stream contains no change data.

        If the result is `FALSE`, then the task does not run.

    [SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](/sql-reference/functions/system_get_predecessor_return_value)
    :   Retrieves the return value for the predecessor task in a task graph.
        Used to decide whether the task should run based on the returned result.

`REMOVE WHEN`
:   Remove the `WHEN` condition that you have specified.

`EXECUTE AS USER user_name`
:   Runs the task on behalf of a specified user account. The user who runs the command must have permissions granted by using the [GRANT IMPERSONATE ON USER TO ROLE](/sql-reference/sql/grant-privilege-user) command.

    For more information, see [Run tasks with user privileges](/user-guide/tasks-intro#label-user-based-security-for-tasks).

## Rename a task

Renaming a task isn’t supported. Instead, you can clone the task, and then drop the old task; for example:

1. Suspend the task (`ALTER TASK task_old_name SUSPEND`).
2. Clone the task, giving it a new name ([CREATE TASK new\_task\_name CLONE old\_task\_name](/sql-reference/sql/create-task#label-create-task-clone-syntax)).
3. For task graphs, find dependent tasks that refer to the old task name, and update them to use the new name:

> 1. Find immediately dependent tasks (that is, child tasks and finalizer tasks, but not children-of-children tasks) using the [TASK\_DEPENDENTS … RECURSIVE](/sql-reference/functions/task_dependents) function; for example:
>
>    Copy code
>
>    ```
>    SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_DEPENDENTS('old_task_name', RECURSIVE => false));
>    ```
> 2. Update each dependent task to use the new task name (`ALTER TASK child_task_1 ADD AFTER new_task_name`).

1. Drop the old version of the task ([DROP TASK old\_task\_name](/sql-reference/sql/drop-task)).
2. Resume the new version of the task (`ALTER TASK new_task_name RESUME`).

## Usage notes

- Resuming or suspending a task (using ALTER TASK … RESUME or ALTER TASK … SUSPEND, respectively) requires either the OWNERSHIP or
  OPERATE privilege on the task.

  When a task is resumed, Snowflake verifies that the role with the OWNERSHIP privilege on the task also has the USAGE privilege on the
  warehouse assigned to the task, as well as the global EXECUTE TASK privilege; if not, an error is produced.

  Only account administrators (users with the ACCOUNTADMIN role) can grant the EXECUTE TASK privilege to a role. For ease of use, we recommend
  creating a custom role (e.g. TASKADMIN) and assigning the EXECUTE TASK privilege to this role. Any role that can grant privileges
  (e.g. SECURITYADMIN or any role with the MANAGE GRANTS privilege) can then grant this custom role to any task owner role to allow altering
  their own tasks. For instructions for creating custom roles and role hierarchies, see [Configuring access control](/user-guide/security-access-control-configure).
- Only the task owner — that is, the role with the OWNERSHIP privilege on the task — can set or unset properties on a task.
- To alter the default CONFIG, you must supply the entire replacement JSON string. You can’t update individual key-value pairs.
  To override the default configuration for a single execution, use the [EXECUTE TASK](/sql-reference/sql/execute-task).
- A standalone task must be suspended before it can be modified.
- The root task in a [task graph](/user-guide/tasks-graphs#label-task-dag) must be suspended before any
  task in the task graph is modified, a child task is suspended or resumed, or a child task is added (using ALTER TASK … AFTER).
- A task graph is limited to a maximum of 1000 tasks total (including the root task) in either a resumed or suspended state.
- To recursively resume all dependent tasks tied to a root task in a task graph, query the [SYSTEM$TASK\_DEPENDENTS\_ENABLE](/sql-reference/functions/system_task_dependents_enable)
  function rather than enabling each task individually (using ALTER TASK … RESUME).
- By default, a DML statement executed without explicitly starting a transaction is automatically committed on success or rolled back on failure
  at the end of the statement. This behavior is called *autocommit* and is controlled with the [AUTOCOMMIT](/sql-reference/parameters#label-autocommit) parameter. This parameter
  must be set to TRUE. If the AUTOCOMMIT parameter is set to FALSE at the account level, then set the parameter to TRUE for the
  individual task (using ALTER TASK … SET AUTOCOMMIT = TRUE).
- When a task is suspended, any current run of the task (i.e. a run with an EXECUTING state in the [TASK\_HISTORY](/sql-reference/functions/task_history)
  output) is completed. To abort the run of the specified task, execute the [SYSTEM$USER\_TASK\_CANCEL\_ONGOING\_EXECUTIONS](/sql-reference/functions/system_user_task_cancel_ongoing_executions)
  function.
- The compute resources for individual runs of a task are either managed by Snowflake (i.e. the serverless compute model) or a
  user-specified virtual warehouse. To convert a task that relies on a warehouse to the serverless compute model, unset the
  `WAREHOUSE`.
- If a task fails with an unexpected error, you can receive a notification about the error.
  For more information about configuring task error notifications, see [Set up error notifications for tasks](/user-guide/tasks-errors).
- The `OVERLAP_POLICY` parameter replaces the deprecated `ALLOW_OVERLAPPING_EXECUTION` parameter. For backward compatibility,
  `ALLOW_OVERLAPPING_EXECUTION = TRUE` maps to `OVERLAP_POLICY = ALLOW_CHILD_OVERLAP`, and
  `ALLOW_OVERLAPPING_EXECUTION = FALSE` maps to `OVERLAP_POLICY = NO_OVERLAP`.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- Regarding the finalizer task:

  - When you `SET FINALIZE = <root task name>`, this function configures a normal task to be a finalizer task associated with the
    given root task.
  - When you `UNSET FINALIZE`, a finalizer task changes to a normal standalone task with no schedule or predecessor.
  - `SET FINALIZE` conflicts with `SET SCHEDULE` and `ADD AFTER`. A task with an existing schedule or predecessor will
    also fail the `SET FINALIZE` query.
  - To alter the root task’s defined finalizer task, first use `UNSET FINALIZE` to unset the finalizer task and then use
    `SET FINALIZE = <root task name>` to update the root task’s finalizer task.
  - The root task must be suspended before the finalizer task is modified, set, or unset.

  For more information, see [Finalizer task](/user-guide/tasks-graphs#label-finalizer-task).

## Examples

The following example initiates operation of a task:

Copy code

```
ALTER TASK mytask RESUME;
```

The following example converts a task to the serverless compute model and sets `xsmall` as the amount of compute resources to provision
for the first serverless runs of the task:

Copy code

```
ALTER TASK mytask UNSET WAREHOUSE;

ALTER TASK mytask SET USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL';
```

The following example sets the TIMEZONE and CLIENT\_TIMESTAMP\_TYPE\_MAPPING session parameters for the session in which the task runs:

Copy code

```
ALTER TASK mytask SET TIMEZONE = 'America/Los_Angeles', CLIENT_TIMESTAMP_TYPE_MAPPING = TIMESTAMP_LTZ;
```

The following example sets a different schedule for a task:

Copy code

```
ALTER TASK mytask SET SCHEDULE = 'USING CRON */3 * * * * UTC';
```

The following example removes the current predecessor tasks for the `mytask` child task (`pred_task1`, `pred_task2`) and replaces them
with a different predecessor task (`pred_task3`):

Copy code

```
ALTER TASK mytask REMOVE AFTER pred_task1, pred_task2;

ALTER TASK mytask ADD AFTER pred_task3;
```

The following example changes the SQL statement associated with a task. The task now queries the CURRENT\_VERSION function when it runs:

Copy code

```
ALTER TASK mytask MODIFY AS SELECT CURRENT_VERSION();
```

The following example modifies the WHEN condition associated with a task. When triggered (on a schedule or after the predecessor task runs
successfully), the task now runs only when the `mystream` stream contains data:

Copy code

```
ALTER TASK mytask MODIFY WHEN SYSTEM$STREAM_HAS_DATA('MYSTREAM');
```

Update an existing task with new or replacement default configuration:

Copy code

```
ALTER TASK task_with_config SET
      CONFIG=$${"output_directory": "/temp/prod_directory/", "environment": "prod"}$$;
```

Remove the default configuration from an existing task:

Copy code

```
ALTER TASK task_with_config UNSET CONFIG;
```
