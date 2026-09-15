# SHOW TASKS

Lists the tasks for which you have access privileges. The command can be used to list tasks for the current/specified database or schema,
or across your entire account.

The output returns task metadata and properties, ordered lexicographically by database, schema, and task name (see [Output](#output) in this topic
for descriptions of the output columns). This is important to note if you wish to filter the results using the provided filters.

See also:
:   [CREATE TASK](/sql-reference/sql/create-task) , [ALTER TASK](/sql-reference/sql/alter-task) , [DROP TASK](/sql-reference/sql/drop-task) , [DESCRIBE TASK](/sql-reference/sql/desc-task)

## Syntax

Copy code

```
SHOW [ TERSE ] TASKS [ LIKE '<pattern>' ]
                     [ IN { ACCOUNT | DATABASE [ <db_name> ] | [ SCHEMA ] [ <schema_name> ] | APPLICATION <application_name> | APPLICATION PACKAGE <application_package_name> } ]
                     [ STARTS WITH '<name_string>' ]
                     [ ROOT ONLY ]
                     [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`TERSE`
:   Returns only a subset of the output columns:

    - created\_on
    - name
    - kind (shows NULL for all task records)
    - database\_name
    - schema\_name
    - schedule

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN ACCOUNT | DATABASE [ db_name ] | SCHEMA [ schema_name ] | APPLICATION application_name | APPLICATION PACKAGE application_package_name`
:   Optionally specifies the scope of the command, which determines whether the command lists records only for the current/specified database or schema, or across your entire account.

    The `APPLICATION` and `APPLICATION PACKAGE` keywords are not required, but they specify the scope for the named Snowflake Native App.

    If you specify the keyword `ACCOUNT`, then the command retrieves records for all schemas in all databases
    of the current account.

    If you specify the keyword `DATABASE`, then:

    - If you specify a `db_name`, then the command retrieves records for all schemas of the specified database.
    - If you don’t specify a `db_name`, then:
      - If there is a current database, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and schemas in the account.

    If you specify the keyword `SCHEMA`, then:

    - If you specify a qualified schema name (for example, `my_database.my_schema`), then the command
      retrieves records for the specified database and schema.
    - If you specify an unqualified `schema_name`, then:

      - If there is a current database, then the command retrieves records for the specified schema in the current database.
      - If there is no current database, then the command displays the error
        `SQL compilation error: Object does not exist, or operation cannot be performed`.
    - If you don’t specify a `schema_name`, then:

      - If there is a current database, then:

        - If there is a current schema, then the command retrieves records for the current schema in the current database.
        - If there is no current schema, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and all schemas in the account.

    Default: Depends on whether the session currently has a database in use:

    - Database: `DATABASE` is the default; that is, the command returns the objects that you have privileges to view in the database.
    - No database: `ACCOUNT` is the default; that is, the command returns the objects that you have privileges to view in your account.

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`ROOT ONLY`
:   Filters the command output to return only root tasks (tasks with no predecessors).

`LIMIT rows [ FROM 'name_string' ]`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
    specified number of rows following the first row whose object name matches the specified string:

    - The string must be enclosed in single quotes and is case sensitive.
    - The string does not have to include the full object name; partial names are supported.

    Default: No value (no limit is applied to the output)

    Note

    For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
    both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
    returned.

    In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
    lexicographic value than the rows returned by `STARTS WITH 'name_string'`.

    For example:

    - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
    - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
    - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Output

The command output provides task properties and metadata in the following columns:

| Column Name | Description |
| --- | --- |
| created\_on | Date and time when the task was created. |
| name | Name of the task. |
| id | Unique identifier for each task. Note that recreating a task (using CREATE OR REPLACE TASK) essentially creates a new task, which has a new ID. |
| database\_name | Database in which the task is stored. |
| schema\_name | Schema in which the task is stored. |
| owner | Role that owns the task; that is, has the OWNERSHIP privilege on the task |
| comment | Comment for the task. |
| warehouse | Warehouse that provides the required resources to run the task. |
| schedule | Schedule for running the task. Displays NULL if no schedule is specified or the task is a triggered task. |
| scheduling\_mode | Displays whether a serverless task is FIXED or FLEXIBLE.   - For FIXED, the task execution is based on the user-specified schedule for the task. - For FLEXIBLE, the task execution is based on the user-specified schedule and target completion interval for the task. |
| target\_completion\_interval | Target completion interval for a serverless task. Used to determine compute resource size for execution. |
| predecessors | JSON array of any tasks that are identified in the AFTER parameter for the task; that is, predecessor tasks. When they are run successfully to completion, these tasks trigger the current task. Individual task names in the array are fully qualified; that is, they include the container database and schema names.     Displays an empty array if the task has no predecessor. |
| state | ‘started’ or ‘suspended’ based on the current state of the task. |
| definition | SQL statements executed when the task runs. |
| condition | Condition specified in the WHEN clause for the task. |
| allow\_overlapping\_execution | For root tasks in a [task graph](/user-guide/tasks-graphs#label-task-dag), displays TRUE if overlapping execution of the task graph is explicitly allowed. For child tasks in a task graph, displays NULL. |
| error\_integration | Name of the notification integration used to access Amazon Simple Notification Service (SNS), Google Pub/Sub, or Microsoft Azure Event Grid to relay error notifications for the task. |
| success\_integration | Name of the notification integration that is used to access Amazon Simple Notification Service (SNS), Google Pub/Sub, or Microsoft Azure Event Grid to relay success notifications for the task. |
| last\_committed\_on | Timestamp when a [version](/user-guide/tasks-intro#label-versioning-of-task-runs) of the task was last set. If no version was set—that is, if the task wasn’t resumed or manually run after it was created—the value is NULL. |
| last\_suspended\_on | Timestamp when the task was last suspended. Displays the timestamps for both the root tasks and the child tasks. If the task hasn’t been suspended yet, the value is NULL. |
| owner\_role\_type | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| config | For the root task in a task graph, displays the default configuration set in the task definition with [CREATE TASK](/sql-reference/sql/create-task) or [ALTER TASK](/sql-reference/sql/alter-task). For child tasks in a task graph, displays NULL. |
| last\_suspended\_reason | Displays the reason why the task was suspended. The possible reasons include the following:  - USER\_SUSPENDED: The user suspended the task by running the `alter task <name> suspend` command. - SCHEMA\_OR\_DATABASE\_DELETED: The schema or database of the task was dropped. - GRANT\_OWNERSHIP: The user transferred the ownership of the task to another role by running the `grant ownership` command. - SUSPENDED\_DUE\_TO\_ERRORS: The task failed a certain number of consecutive times and was suspended. You can set the [SUSPEND\_TASK\_AFTER\_NUM\_FAILURES](/sql-reference/parameters#label-suspend-task-after-num-failures) parameter for the number of failures required to suspend this task. - CHILD\_BECAME\_ROOT: The task was previously a child task in a task graph, but all predecessors of the child task were removed and the child task became a root task. - FINALIZER\_BECAME\_ROOT: The task was previously a finalizer task in a task graph, but the finalization was removed and the task became a root task. - MATCHING\_OWNER\_NOT\_FOUND: During [task replication](/user-guide/account-replication-considerations#label-replication-and-tasks), the role that owns the task was not found on the secondary database.  Displays NULL if the task has never been suspended, or if the task was last suspended before the column was introduced with [2023\_08 Bundle (Generally Enabled)](/release-notes/bcr-bundles/2023_08_bundle). |
| task\_relations | JSON object that describes the task relationships, including predecessor tasks and finalizer tasks. The object can contain the following fields:   - `Predecessors`: Array of fully qualified names of tasks identified in the AFTER parameter for the task. When all predecessor tasks run successfully to   completion, they trigger the current task.   If the task has no predecessors, this is an empty array. - `FinalizerTask`: Fully qualified name of the finalizer task associated with this root task.   Displayed only for root tasks that have a finalizer task. - `FinalizedRootTask`: Fully qualified name of the root task that this task finalizes. Displayed only for finalizer tasks.   Examples:   - Root task with a finalizer task: `{"Predecessors":[],"FinalizerTask":"MY_DB.MY_SCHEMA.FINALIZE_LONG_RUNNING_TASK"}` - Finalizer task: `{"FinalizedRootTask":"MY_DB.MY_SCHEMA.LONG_RUNNING_TASK","Predecessors":[]}` - Task with predecessors: `{"Predecessors":["MY_DB.MY_SCHEMA.DEFTASK"]}` |
| execute\_as\_user | Shows as NULL if executed as the system user (default). Shows the user name of a user running a task using impersonated privileges (EXECUTE AS USER). To learn more, see [Run tasks with user privileges](/user-guide/tasks-intro#label-user-based-security-for-tasks). |

Expand

Show lessSee more

For more information about the properties that can be specified for a task, see [CREATE TASK](/sql-reference/sql/create-task).

## Usage notes

- Only returns rows for a task owner—that is, the role with the OWNERSHIP privilege on a task—or a role with either the MONITOR
  or OPERATE privilege on a task.

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

Show all the tasks whose name starts with `line` that you have privileges to view in the `tpch.public` schema:

> Copy code
>
> ```
> SHOW TASKS LIKE 'line%' IN tpch.public;
> ```

Show all the tasks that you have privileges to view in the `tpch.public` schema:

> Copy code
>
> ```
> SHOW TASKS IN tpch.public;
> ```
