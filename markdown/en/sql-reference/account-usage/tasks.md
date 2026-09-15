Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# TASKS view

This Account Usage view displays a row for each [task](/user-guide/tasks-intro) defined in your account.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| CREATED | TIMESTAMP\_LTZ | Date and time when the task was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the task was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the task was dropped. NULL if the task hasn’t been dropped. |
| ID | VARCHAR | Unique identifier for each task. Note that recreating a task (using CREATE OR REPLACE TASK) essentially creates a new task with a new ID. |
| TASK\_NAME | VARCHAR | Name of the task. |
| TASK\_DATABASE\_ID | NUMBER | Internal identifier for the database in which the task is stored. |
| TASK\_DATABASE | VARCHAR | Database in which the task is stored. |
| TASK\_SCHEMA\_ID | NUMBER | Internal identifier for the schema in which the task is stored. |
| TASK\_SCHEMA | VARCHAR | Schema in which the task is stored. |
| TASK\_OWNER | VARCHAR | Role that owns the task; that is, has the OWNERSHIP privilege on the task. |
| COMMENT | VARCHAR | Comment for the task. |
| WAREHOUSE | VARCHAR | Warehouse that provides the required resources to run the task. |
| SCHEDULE | VARCHAR | Schedule for running the task. Displays NULL if no schedule is specified or the task is a triggered task. |
| PREDECESSORS | ARRAY | JSON array of any tasks identified in the AFTER parameter for the task (that is, predecessor tasks). When run successfully to completion, these tasks trigger the current task. Individual task names in the array are fully qualified (that is, they include the container database and schema names).     Displays an empty array if the task has no predecessor. |
| STATE | VARCHAR | Current state of the task: `started` or `suspended`. |
| DEFINITION | VARCHAR | SQL statements executed when the task runs. |
| CONDITION | VARCHAR | Condition specified in the WHEN clause for the task. |
| ALLOW\_OVERLAPPING\_EXECUTION | BOOLEAN | For root tasks in a task graph, displays TRUE if overlapping execution of the task graph is explicitly allowed. For child tasks in a task graph, displays NULL. |
| ERROR\_INTEGRATION | VARCHAR | Name of the notification integration used to access Amazon Simple Notification Service (SNS), Google Pub/Sub, or Microsoft Azure Event Grid to relay error notifications for the task. |
| LAST\_COMMITTED | TIMESTAMP\_LTZ | Timestamp when a version of the task was last set. If no version was set—that is, if the task wasn’t resumed or manually run after it was created—the value is NULL. |
| LAST\_SUSPENDED | TIMESTAMP\_LTZ | Timestamp when the task was last suspended. Displays the timestamps for both the root tasks and the child tasks. NULL if the task hasn’t been suspended yet. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object. Common values include ROLE, DATABASE\_ROLE, APPLICATION, APPLICATION PACKAGE SHARE, USER, SHARE, and others. |
| INSTANCE\_ID | NUMBER | Internal/system-generated identifier for the instance which the object belongs to. |
| CONFIG | VARCHAR | For the root task in a task graph, displays the default configuration set in the task definition with CREATE TASK or ALTER TASK. For child tasks in a task graph, displays NULL. Returns an empty string for tasks in shared databases or application instances where the consumer account differs from the provider account. |
| TASK\_RELATIONS | OBJECT | JSON object describing the task relationships. Can contain: Predecessors (array of fully qualified predecessor task names), FinalizerTask (fully qualified name of the finalizer task, for root tasks that have a finalizer task), and FinalizedRootTask (fully qualified name of the root task being finalized, for finalizer tasks only). |
| TASK\_RELATIONS\_IDS | OBJECT | Same as TASK\_RELATIONS, but displays the identifier of each related task instead of its fully qualified name. |
| LAST\_SUSPENDED\_REASON | VARCHAR | Reason the task was suspended. Possible values: USER\_SUSPENDED, SCHEMA\_OR\_DATABASE\_DELETED, GRANT\_OWNERSHIP, SUSPENDED\_DUE\_TO\_ERRORS, CHILD\_BECAME\_ROOT, FINALIZER\_BECAME\_ROOT, APPLICATION\_IS\_DISABLED, SUSPENDED\_DUE\_TO\_OVERRUNS, REPLICATED\_WITHOUT\_GRANT. NULL if the task has never been suspended. |
| SUCCESS\_INTEGRATION | VARCHAR | Name of the notification integration used to access Amazon Simple Notification Service (SNS), Google Pub/Sub, or Microsoft Azure Event Grid to relay success notifications for the task. |
| SCHEDULING\_MODE | VARCHAR | Displays whether a serverless task is FIXED or FLEXIBLE. NULL for warehouse tasks. Note: Support for FLEXIBLE mode will end in a future release. |
| TARGET\_COMPLETION\_INTERVAL | VARCHAR | Target completion interval for a serverless task. Used to determine compute resource size for execution. |
| EXECUTE\_AS\_USER\_ID | NUMBER | Internal identifier for the task’s execute-as user. NULL if the task is configured to execute as the system user (default). Can be joined with ACCOUNT\_USAGE.USERS on the USER\_ID column. |
| OVERLAP\_POLICY | VARCHAR | Overlap policy for the task. Possible values: NO\_OVERLAP (task graph runs can’t execute concurrently), ALLOW\_CHILD\_OVERLAP (runs may execute concurrently but only one root task run at a time), ALLOW\_ALL\_OVERLAP (runs may execute fully concurrently; root tasks only). NULL for child tasks and finalizer tasks. |
| CREATED\_BY\_USER\_ID | NUMBER | The identifier of the user to whom the system attributes creating the task. |

Expand

Show lessSee more

## Usage notes

- Dropped tasks have NULL values in columns that reference the task’s predecessors, finalizer, and finalized root task (PREDECESSORS, TASK\_RELATIONS, and TASK\_RELATIONS\_IDS). To get information about the relations of a dropped task, query the [TASK\_VERSIONS view](/sql-reference/account-usage/task_versions) view.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:
  - DDL operations.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve all active tasks with names matching a specific pattern:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.TASKS
WHERE TASK_NAME ILIKE 'ABC%'
  AND DELETED IS NULL;
```

Retrieve task relations for dropped non-root tasks by joining with the TASK\_VERSIONS view:

Copy code

```
SELECT
    TASKS.ID,
    TASKS.TASK_NAME,
    TASK_VERSIONS.TASK_RELATIONS,
    TASK_VERSIONS.GRAPH_VERSION
FROM SNOWFLAKE.ACCOUNT_USAGE.TASKS
INNER JOIN SNOWFLAKE.ACCOUNT_USAGE.TASK_VERSIONS
    ON TASK_VERSIONS.ID = TASKS.ID
WHERE TASKS.DELETED IS NOT NULL
  AND TASK_VERSIONS.ROOT_TASK_ID != TASK_VERSIONS.ID;
```
