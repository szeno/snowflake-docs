# Create a sequence of tasks with a task graph

In Snowflake, you can manage multiple tasks with a *task graph*, also known as a directed acyclic graph (DAG). A task graph is composed of a root task and dependent child tasks. The dependencies must run in a start-to-finish direction, with no loops. An optional final task, called a *finalizer*, can perform cleanup operations after all other tasks are complete.

Build task graphs that have dynamic behavior by specifying logic-based operations in the task body using runtime values, graph level configuration, and return values of parent tasks.

You can create tasks and task graphs using [supported languages and tools](/developer-guide/stored-procedure/stored-procedures-overview#label-stored-procedures-handler-languages) like SQL, JavaScript, Python,
Java, Scala, or Snowflake Scripting. This topic provides SQL examples. For Python examples, see [Managing Snowflake tasks and task graphs with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-tasks).

You can also use Snowsight to manage and view your task graphs. For more information, see [View tasks and task graphs in Snowsight](/user-guide/ui-snowsight-tasks).

## Create a task graph

Create a root task using [CREATE TASK](/sql-reference/sql/create-task), then create child tasks using CREATE TASK .. AFTER to select the parent tasks.

The root task defines [when the task graph runs](#label-run-task-graph). Child tasks are executed in the order defined by the task graph.

When multiple child tasks have the same parent, the child tasks run
in parallel.

When a task has multiple parents, the task waits for all
preceding tasks to successfully complete before starting.
(The task may also run when some parent tasks are skipped. For
more information, see [Skip or suspend a child task](#label-child-task-suspended)).

The following example creates a serverless task graph that starts
with a root task that is scheduled to run every minute. The root
task has two child tasks that run in parallel. (The diagram
shows an example where one of these tasks runs longer than the other.)
After both of those tasks complete, a third child task runs. The
finalizer task runs after all other tasks complete or fail to complete:

![A diagram of a sequence of tasks.](/static/images/task-graph.svg)

Copy code

```
CREATE TASK task_root
  SCHEDULE = '1 MINUTE'
  AS SELECT 1;

CREATE TASK task_a
  AFTER task_root
  AS SELECT 1;

CREATE TASK task_b
  AFTER task_root
  AS SELECT 1;

CREATE TASK task_c
  AFTER task_a, task_b
  AS SELECT 1;
```

Considerations:

- A task graph is limited to a maximum of 1000 tasks.
- A single task can have a maximum of 100 parent tasks and 100 child tasks.
- When tasks run in parallel on the same user-managed warehouse, the [compute resources](/user-guide/tasks-intro#label-tasks-compute-resources) must be sized to handle the concurrent task runs.

### Finalizer task

You can add an optional finalizer task to run after all other tasks in
the task graph complete (or fail to complete). Use this to do the following:

- Perform cleanup operations, for example, cleaning up intermediate data that is no longer needed.
- Send notifications about task success or failure.

![A task sequence shows a root task pointing to two child tasks, which in turn point to another task. A finalizer task is shown at the bottom, running after all other tasks complete or fail to complete.](/static/images/task-graph-fail.svg)

To create a finalizer task, use [CREATE TASK … FINALIZE …](/sql-reference/sql/create-task) on the root task. Example:

Copy code

```
CREATE TASK task_finalizer
  FINALIZE = task_root
  AS SELECT 1;
```

Considerations:

- A finalizer task is always associated with a root task. Each root task can have only one finalizer task, and a finalizer task can be
  associated with only one root task.
- When the root task of a task graph is skipped (for example, because of [overlap task graph runs](#label-task-graph-overlapping-runs)), the finalizer task won’t be started.
- A finalizer task cannot have any child tasks.
- A finalizer task is scheduled only when no other tasks are running or queued in the current task graph run.

For more examples, see [Finalizer task example: Send email notification](#label-finalizer-task-example-email) and [Finalizer task example: Correct for errors](#label-finalizer-task-example-correct-for-errors).

## Manage task graph ownership

All tasks in a task graph must have the same task owner and be stored in the same database and schema.

You can transfer ownership of all tasks in a task graph using one of the following actions:

- Drop the owner of all tasks in the task graph using [DROP ROLE](/sql-reference/sql/drop-role). Snowflake transfers ownership to the
  role that runs the DROP ROLE command.
- Transfer ownership of all tasks in the task graph using [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) on all tasks in a schema.

When you transfer ownership of the tasks in a task graph using these methods, the tasks in the task graph retain their relationships to
each other.

Transferring ownership of a single task removes the dependency between the task and any parent and child tasks. For more information, see
[Unlink parent and child tasks](#label-tasks-graphs-link-sever) (in this topic).

Note

Database replication does not work for task graphs if the graph is owned by a different role than the role that performs replication.

## Run or schedule tasks in a task graph

### Run a task graph manually

You can run a single instance of a task graph. This is useful for testing new or modified task graphs before enabling the task graph in production, or for one-time runs as needed.

Before starting the task graph, use [ALTER TASK … RESUME](/sql-reference/sql/alter-task) on each child task (including the optional finalizer task) that you want to include in the run.

To run a single instance of a task graph, use [EXECUTE TASK](/sql-reference/sql/execute-task) on the root task. When you run the root task, all resumed child tasks in the task graph are executed in the order defined by the task graph.

### Run a task on a schedule or as a triggered task

In the root task, define when the task graph runs. Task graphs can run on a recurring schedule, or they can be triggered by an event. For more information, see the following topics:

- [Scheduled tasks](/user-guide/tasks-intro#label-tasks-scheduling)
- [Triggered tasks](/user-guide/tasks-triggered)

To start the task graph, you can do either of the following:

- Resume each individual child task (including the finalizer) that you want to include in the run, and then resume the root task, using [ALTER TASK … RESUME](/sql-reference/sql/alter-task).
- Resume all of the tasks in a task graph at once using [SYSTEM$TASK\_DEPENDENTS\_ENABLE](/sql-reference/functions/system_task_dependents_enable) ( <root\_task\_name> ) on the root task.

## View dependent tasks in a task graph

To view the child tasks for a root task, call the [TASK\_DEPENDENTS](/sql-reference/functions/task_dependents) table function. To retrieve all tasks in a task graph, input the root task when calling the function.

You can also use Snowsight to manage and view your task graphs. For more information, see [View tasks and task graphs in Snowsight](/user-guide/ui-snowsight-tasks).

## Modify, suspend, or retry tasks

### Modify a task in a task graph

To modify a task in a scheduled task graph, suspend the root task using [ALTER TASK … SUSPEND](/sql-reference/sql/alter-task). If a run of the task graph is in process, it completes the current run. All future scheduled runs of the root task are canceled.

When the root task is suspended, child tasks including the finalizer task retain their state (suspended, running, or completed). The child tasks don’t need to be individually suspended.

After you suspend the root task, you can modify any task in the task graph.

To resume the task graph, you can do either of the following:

- Resume the root task using [ALTER TASK … RESUME](/sql-reference/sql/alter-task). Individual child tasks that were running before do not need to be resumed.
- Resume all of the tasks in a task graph at once by calling [SYSTEM$TASK\_DEPENDENTS\_ENABLE](/sql-reference/functions/system_task_dependents_enable) and passing in the name of the root task.

### Skip or suspend a child task

To skip a child task in a task graph, suspend the child task
using [ALTER TASK … SUSPEND](/sql-reference/sql/alter-task).

When you suspend a child task, the task graph continues to run as though
the child task had succeeded. A child task with multiple predecessors
runs as long as at least one of the predecessors is in a
resumed state, and all resumed predecessors run successfully to completion.

![A diagram shows a task graph that includes a suspended child task. The suspended child task is skipped, and the task graph completes.](/static/images/task-graph-child-tasks-skipped.svg)

### Retry a failed task

To retry the latest graph run, use [EXECUTE TASK … RETRY LAST](/sql-reference/sql/execute-task) to attempt to run the task graph from the last failed task. If the task succeeds, all child tasks will continue to run as their preceding tasks complete.

To retry an older graph run rather than the most recent one, use
[EXECUTE TASK … RETRY GRAPH RUN GROUP](/sql-reference/sql/execute-task) and pass the
GRAPH\_RUN\_GROUP\_ID of the graph run group you want to retry.

### Automatic retries

By default, if a child task fails, the entire task graph is considered to have failed.

Rather than waiting until the next scheduled task graph run, you can instruct the task graph to retry immediately by setting the `TASK_AUTO_RETRY_ATTEMPTS` parameter on the root task. When a child task fails, the entire task graph is immediately retried, up to the number of times specified. If the task graph still doesn’t complete, the task graph is considered to have failed.

### Suspend task graphs after failed task graph runs

By default, a task graph is suspended after 10 consecutive failures. You can change this value by setting `SUSPEND_TASK_AFTER_NUM_FAILURES` on the root task.

In the following example, whenever a child task fails, the task graph immediately retries twice before the entire task graph is considered failed. If the task graph fails three times in a row, the task graph is then suspended.

Copy code

```
CREATE OR REPLACE TASK task_root
  SCHEDULE = '1 MINUTE'
  TASK_AUTO_RETRY_ATTEMPTS = 2   --  Failed task graph retries up to 2 times
  SUSPEND_TASK_AFTER_NUM_FAILURES = 3   --  Task graph suspends after 3 consecutive failures
  AS SELECT 1;
```

## Unlink parent and child tasks

Dependencies between tasks in a task graph can be severed as a result of the following actions:

- ALTER TASK … REMOVE AFTER and ALTER TASK … UNSET FINALIZE remove the link between the target task and the specified
  parent tasks or finalized root task.
- DROP TASK and GRANT OWNERSHIP sever all the target task’s links. For example, root task A has child task B, and task B has child task C. If you drop task B, the link between task A and B is severed and so is the link between task B and C.

If any combination of the above actions severs the relationship between the child task and all parent tasks, the
child task becomes either a standalone task or a root task.

Note

If you grant the ownership of a task to its current owner, dependency links might not be severed.

## Overlap task graph runs

By default, Snowflake ensures that only one instance of a particular task graph is allowed to run at a time. The next run of a root task
is scheduled only after all tasks in the task graph have finished running. This means that if the cumulative time required to run all tasks
in the task graph exceeds the explicit scheduled time set in the definition of the root task, at least one run of the task graph is
skipped.

To control task graph parallelism, use [CREATE TASK](/sql-reference/sql/create-task) or [ALTER TASK](/sql-reference/sql/alter-task)
on the root task to set the OVERLAP\_POLICY parameter:

- `OVERLAP_POLICY = NO_OVERLAP` (default): Executes tasks serially with no parallelism.
  Snowflake schedules the next run of a root task only after all child tasks finish running.
- `OVERLAP_POLICY = ALLOW_CHILD_OVERLAP`: Allows child task parallelism.
  When the next scheduled run time for the root task occurs while any child task is still running,
  Snowflake starts a new instance of the task graph. Root tasks never overlap with this policy.
- `OVERLAP_POLICY = ALLOW_ALL_OVERLAP`: Allows unlimited true parallelism.
  Snowflake can run multiple instances of the entire task graph, including the root task, concurrently.

![Overlapping task graph runs](/static/images/tasks-tree-overlap.svg)

Overlapping runs may be tolerated (or even desirable) when read/write SQL operations executed by overlapping runs of a task graph do not
produce incorrect or duplicate data. However, for other task graphs, task owners (the role with the OWNERSHIP privilege on all tasks in the
task graph) should set an appropriate schedule on the root task and choose an appropriate warehouse size (or use serverless compute
resources) to ensure an instance of the task graph finishes to completion before the root task is next scheduled to run.

To better align a task graph with the schedule defined in the root task:

1. If feasible, increase the scheduling time between runs of the root task.
2. Consider modifying compute-heavy tasks to use serverless compute resources. If the task relies on user-managed compute resources, increase the size of the warehouse that runs large or complex SQL statements or stored procedures in the task graph.
3. Analyze the SQL statements or stored procedure executed by each task. Determine if code can be rewritten to leverage parallel processing.

If none of the above solutions help, consider whether it is necessary to allow concurrent runs of the task graph by setting
OVERLAP\_POLICY = ALLOW\_CHILD\_OVERLAP or OVERLAP\_POLICY = ALLOW\_ALL\_OVERLAP on the root task.
You can set this parameter when you create a task (using CREATE TASK) or later
(using ALTER TASK or in Snowsight).

### Versioning

When the root task in a task graph is resumed or manually executed, Snowflake sets a version of the entire task graph, including all properties for all tasks in the task graph. After a task is suspended and modified, Snowflake sets a new version when the root task is resumed or manually executed.

To modify or recreate any task in a task graph, the root task must first be suspended. When the root task is suspended, all future
scheduled runs of the root task are canceled; however, if any tasks are currently running, these tasks and any descendant tasks continue
to run using the current version.

Note

If the definition of a stored procedure called by a task changes while the task graph is executing, the new programming could be
executed when the stored procedure is called by the task in the current run.

For example, suppose the root task in a task graph is suspended, but a scheduled run of this task has already started. The owner of all
tasks in the task graph modifies the SQL code called by a child task while the root task is still running. The child task runs and executes
the SQL code in its definition using the version of the task graph that was current when the root task started its run. When the root task
is resumed or is manually executed, a new version of the task graph is set. This new version includes the modifications to the child task.

To retrieve the history of task versions, query [TASK\_VERSIONS](/sql-reference/account-usage/task_versions) [Account Usage view](/sql-reference/account-usage) (in the SNOWFLAKE shared database).

## Task graph duration

Task graph duration includes the time from when the root task is scheduled to start to when the last child task completes. To calculate the duration of a task graph, query [COMPLETE\_TASK\_GRAPHS view](/sql-reference/account-usage/complete_task_graphs), and compare SCHEDULED\_TIME with COMPLETED\_TIME.

For example, the following diagram shows a task graph that is scheduled to run every minute. The root task and its two child tasks each queue for 5 seconds and run for 10 seconds, requiring a total of 45 seconds to complete.

![A diagram of a task graph, including three tasks with dependencies. Each task queues for 5 seconds and runs for 10 seconds, for a total of a 45 second total run.](/static/images/task-graph-duration.svg)

### Task graph timeouts

When [USER\_TASK\_TIMEOUT\_MS](/sql-reference/parameters#label-user-task-timeout-ms) is set in the root task, the timeout applies to the entire task graph.

When [USER\_TASK\_TIMEOUT\_MS](/sql-reference/parameters#label-user-task-timeout-ms) is set in a child task or finalizer task, the timeout applies to only that task.

When [USER\_TASK\_TIMEOUT\_MS](/sql-reference/parameters#label-user-task-timeout-ms) is set in both the root task and a child task, the child task timeout overrides the root task timeout for that child task.

### Considerations

- For serverless tasks, Snowflake automatically scales resources to make sure tasks complete within a target completion interval, including queueing time.
- For user-managed tasks, longer queueing periods are common when tasks are scheduled to run on a shared or busy warehouse.
- For task graphs, the total time might include additional queueing time for child tasks waiting for their predecessors to complete.

## Create a task graph with logic (runtime info, configuration, and return values)

Tasks in a task graph can use return values from parent tasks to perform logic-based operations in their function body.

Considerations:

- Some logic-based commands, like [SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](/sql-reference/functions/system_get_predecessor_return_value), are case sensitive. However, tasks created using CREATE TASK without quotes are [stored and resolved in uppercase](/sql-reference/identifiers-syntax). To manage this, you can do any of the following:
  - Create task names using only uppercase letters.
  - Use quotes when naming and calling tasks.
  - For task names defined with lowercase characters, call the task using uppercase characters. For example: a task defined by “CREATE TASK task\_c…” can be called as SELECT SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE(‘TASK\_C’).

### Pass configuration information to the task graph

You can pass configuration information by using a JSON object that can be read by other tasks in a task graph.
Use the syntax [CREATE TASK](/sql-reference/sql/create-task) or [ALTER TASK](/sql-reference/sql/alter-task) with
the CONFIG parameter to set, unset, or modify the configuration information in the root task.
Use the function [SYSTEM$GET\_TASK\_GRAPH\_CONFIG](/sql-reference/functions/system_get_task_graph_config) to retrieve the configuration information.

Example:

Copy code

```
CREATE OR REPLACE TASK task_root
  SCHEDULE = '1 MINUTE'
  USER_TASK_TIMEOUT_MS = 60000
  CONFIG='{"environment": "production", "path": "/prod_directory/"}'
  AS SELECT 1;

CREATE OR REPLACE TASK task_a
  USER_TASK_TIMEOUT_MS = 600000
  AFTER task_root
  AS
    BEGIN
      LET VALUE := (SELECT SYSTEM$GET_TASK_GRAPH_CONFIG('path'));
      CREATE TABLE IF NOT EXISTS demo_table(NAME VARCHAR, VALUE VARCHAR);
      INSERT INTO demo_table VALUES('task c path',:value);
    END;
```

Note

You can dynamically override the configuration for a single task execution with the
[EXECUTE TASK … USING CONFIG](/sql-reference/sql/execute-task) command.
With this command, you can test different configurations or run ad-hoc executions with modified settings without changing the task definition.

### Pass return values between tasks

You can pass return values between tasks in a task graph.
Use the function [SYSTEM$SET\_RETURN\_VALUE](/sql-reference/functions/system_set_return_value)
to add a return value from a task, and use the function
[SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](/sql-reference/functions/system_get_predecessor_return_value) to retrieve it.

When a task has multiple predecessors, you must specify which task has the return value that you want.
In the following example, we create a root task in a task graph that adds configuration information.

Copy code

```
CREATE OR REPLACE TASK task_c
  SCHEDULE = '1 MINUTE'
  USER_TASK_TIMEOUT_MS = 60000
  AS
    BEGIN
      CALL SYSTEM$SET_RETURN_VALUE('task_c successful');
    END;

CREATE OR REPLACE TASK task_d
  USER_TASK_TIMEOUT_MS = 60000
  AFTER task_c
  AS
    BEGIN
      LET VALUE := (SELECT SYSTEM$GET_PREDECESSOR_RETURN_VALUE('task_c'));
      CREATE TABLE IF NOT EXISTS demo_table(NAME VARCHAR, VALUE VARCHAR);
      INSERT INTO demo_table VALUES('Value from predecessor task_c', :value);
    END;
```

### Get and use runtime information

Use the function [SYSTEM$TASK\_RUNTIME\_INFO](/sql-reference/functions/system_task_runtime_info) to report information about the current task run. This function has several options specific to task graphs. For example, use CURRENT\_ROOT\_TASK\_NAME to get the name of the root task in the current task graph.
The following example shows how to add a date stamp to a table based on when the root task of the task graph started.

Copy code

```
-- Updates the date/time table after the root task completes.
CREATE OR REPLACE TASK task_date_time_table
  USER_TASK_TIMEOUT_MS = 60000
  AFTER task_root
  AS
    BEGIN
      LET VALUE := (SELECT SYSTEM$TASK_RUNTIME_INFO('CURRENT_TASK_GRAPH_ORIGINAL_SCHEDULED_TIMESTAMP'));
      INSERT INTO date_time_table VALUES('order_date',:value);
    END;
```

## Examples

### Example: Start multiple tasks and report status

In the following example, the root task starts tasks to update three different tables. After those three tables are updated, a task combines the information from the other three tables into an aggregate sales table.

![Flowchart shows a root task that starts three child tasks, each of which updates a table. Those three tasks all precede another child task, which combines the previous changes into another table.](/static/images/task-graph-example-aggregate.svg)

Copy code

```
-- Create a notebook in the public schema
-- USE DATABASE <database name>;
-- USE SCHEMA <schema name>;

-- task_a: Root task. Starts the task graph and sets basic configurations.
CREATE OR REPLACE TASK task_a
  SCHEDULE = '1 MINUTE'
  TASK_AUTO_RETRY_ATTEMPTS = 2
  SUSPEND_TASK_AFTER_NUM_FAILURES = 3
  USER_TASK_TIMEOUT_MS = 60000
  CONFIG='{"environment": "production", "path": "/prod_directory/"}'
  AS
    BEGIN
      CALL SYSTEM$SET_RETURN_VALUE('task_a successful');
    END;
;

-- task_customer_table: Updates the customer table.
--   Runs after the root task completes.
CREATE OR REPLACE TASK task_customer_table
  USER_TASK_TIMEOUT_MS = 60000
  AFTER task_a
  AS
    BEGIN
      LET VALUE := (SELECT customer_id FROM ref_cust_table
        WHERE cust_name = "Jane Doe";);
      INSERT INTO customer_table VALUES('customer_id',:value);
    END;
;

-- task_product_table: Updates the product table.
--   Runs after the root task completes.
CREATE OR REPLACE TASK task_product_table
  USER_TASK_TIMEOUT_MS = 60000
  AFTER task_a
  AS
    BEGIN
      LET VALUE := (SELECT product_id FROM ref_item_table
        WHERE PRODUCT_NAME = "widget";);
      INSERT INTO product_table VALUES('product_id',:value);
    END;
;

-- task_date_time_table: Updates the date/time table.
--   Runs after the root task completes.
CREATE OR REPLACE TASK task_date_time_table
  USER_TASK_TIMEOUT_MS = 60000
  AFTER task_a
  AS
    BEGIN
      LET VALUE := (SELECT SYSTEM$TASK_RUNTIME_INFO('CURRENT_TASK_GRAPH_ORIGINAL_SCHEDULED_TIMESTAMP'));
      INSERT INTO "date_time_table" VALUES('order_date',:value);
    END;
;

-- task_sales_table: Aggregates changes from other tables.
--   Runs only after updates are complete to all three other tables.
CREATE OR REPLACE TASK task_sales_table
  USER_TASK_TIMEOUT_MS = 60000
  AFTER task_customer_table, task_product_table, task_date_time_table
  AS
    BEGIN
      LET VALUE := (SELECT sales_order_id FROM ORDERS);
      JOIN CUSTOMER_TABLE ON orders.customer_id=customer_table.customer_id;
      INSERT INTO sales_table VALUES('sales_order_id',:value);
    END;
;
```

### Finalizer task example: Send email notification

This example demonstrates how to use a finalizer task to send an email summary of a task graph run.
The finalizer task calls two external functions: one aggregates the completion status of each task,
and the other formats the information into an email for a remote messaging service.

This example uses an example root task named `task_root` and an example finalizer task named `notify_finalizer`.

![Diagram that shows a finalizer task that runs after all other tasks complete or fail.](/static/images/task-graph-finalizer-email.svg)

Copy code

```
CREATE OR REPLACE TASK notify_finalizer
  USER_TASK_TIMEOUT_MS = 60000
  FINALIZE = task_root
AS
  DECLARE
    my_root_task_id STRING;
    my_start_time TIMESTAMP_LTZ;
    summary_json STRING;
    summary_html STRING;
  BEGIN
    --- Get root task ID
    my_root_task_id := (SELECT SYSTEM$TASK_RUNTIME_INFO('CURRENT_ROOT_TASK_UUID'));
    --- Get root task scheduled time
    my_start_time := (SELECT SYSTEM$TASK_RUNTIME_INFO('CURRENT_TASK_GRAPH_ORIGINAL_SCHEDULED_TIMESTAMP')::timestamp_ltz);
    --- Combine all task run info into one JSON string
    summary_json := (SELECT get_task_graph_run_summary(:my_root_task_id, :my_start_time));
    --- Convert JSON into HTML table
    summary_html := (SELECT HTML_FROM_JSON_TASK_RUNS(:summary_json));

    --- Send HTML to email
    CALL SYSTEM$SEND_EMAIL(
        'email_notification',
        'admin@snowflake.com',
        'notification task run summary',
        :summary_html,
        'text/html');
    --- Set return value for finalizer
    CALL SYSTEM$SET_RETURN_VALUE('✅ Graph run summary sent.');
  END

CREATE OR REPLACE FUNCTION get_task_graph_run_summary(my_root_task_id STRING, my_start_time TIMESTAMP_LTZ)
  RETURNS STRING
AS
$$
  (SELECT
    ARRAY_AGG(OBJECT_CONSTRUCT(
      'task_name', name,
      'run_status', state,
      'return_value', return_value,
      'started', query_start_time,
      'duration', duration,
      'error_message', error_message
      )
    ) AS GRAPH_RUN_SUMMARY
  FROM
    (SELECT
      NAME,
      CASE
        WHEN STATE = 'SUCCEED' then '🟢 Succeeded'
        WHEN STATE = 'FAILED' then '🔴 Failed'
        WHEN STATE = 'SKIPPED' then '🔵 Skipped'
        WHEN STATE = 'CANCELLED' then '🔘 Cancelled'
      END AS STATE,
      RETURN_VALUE,
      TO_VARCHAR(QUERY_START_TIME, 'YYYY-MM-DD HH24:MI:SS') AS QUERY_START_TIME,
      CONCAT(TIMESTAMPDIFF('seconds', query_start_time, completed_time),
        ' s') AS DURATION,
      ERROR_MESSAGE
    FROM
      TABLE(my-database.information_schema.task_history(
        ROOT_TASK_ID => my_root_task_id ::STRING,
        SCHEDULED_TIME_RANGE_START => my_start_time,
        SCHEDULED_TIME_RANGE_END => current_timestamp()
      ))
    ORDER BY
      SCHEDULED_TIME)
  )::STRING
$$
;

CREATE OR REPLACE FUNCTION HTML_FROM_JSON_TASK_RUNS(JSON_DATA STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.9'
  HANDLER = 'GENERATE_HTML_TABLE'
AS
$$
import json

def GENERATE_HTML_TABLE(JSON_DATA):
    column_widths = ["320px", "120px", "400px", "160px", "80px", "480px"]

    DATA = json.loads(JSON_DATA)
    HTML = f"""
    <img src="https://docs.snowflake.com/images/logo-sample.png"
      alt="Sample organization logo" height="72">
    <p><strong>Task Graph Run Summary</strong>
      <br />Sign in to Snowsight to see more details.</p>
    <table border="1" style="border-color:#DEE3EA"
      cellpadding="5" cellspacing="0">
      <thead>
        <tr>
    """
    headers = ["Task name", "Run status", "Return value", "Started", "Duration", "Error message"]
    for i, header in enumerate(headers):
        HTML += f'<th scope="col" style="text-align:left; width: {column_widths[i]}">{header.capitalize()}</th>'

    HTML += """
        </tr>
      </thead>
      <tbody>
    """
    for ROW_DATA in DATA:
        HTML += "<tr>"
        for header in headers:
            key = header.replace(" ", "_").upper()
            CELL_DATA = ROW_DATA.get(key, "")
            HTML += f'<td style="text-align:left; width: {column_widths[headers.index(header)]}">{CELL_DATA}</td>'
        HTML += "</tr>"
    HTML += """
      </tbody>
    </table>
    """
    return HTML
$$
;
```

### Finalizer task example: Correct for errors

This example demonstrates how a finalizer task can correct for errors.

For demonstration purposes, the tasks are designed to fail during their first run. The finalizer tasks corrects the issue and restarts the tasks, which succeed on following runs:

![Diagram showing a task series. Task A is shown on the upper left. An arrow points right from Task A to Task B, which points to Task C, which points to Task D. Below Task A, an arrow points to the finalizer task, Task F.](/static/images/data-pipeline-tasks-dag-retry.svg)

Copy code

```
-- Configuration
-- By default, the notebook creates the objects in the public schema.
-- USE DATABASE <database name>;
-- USE SCHEMA <schema name>;

-- 1. Set the default configurations.
--    Creates a root task ("task_a"), and sets the default configurations
--    used throughout the task graph.
--    Configurations include:
--    * Each task runs after one minute, with a 60-second timeout.
--    * If a task fails, retry it twice. if it fails twice,
--      the entire task graph is considered as failed.
--    * If the task graph fails consecutively three times, suspend the task.
--    * Other environment values are set.

CREATE OR REPLACE TASK task_a
  SCHEDULE = '1 MINUTE'
  USER_TASK_TIMEOUT_MS = 60000
  TASK_AUTO_RETRY_ATTEMPTS = 2
  SUSPEND_TASK_AFTER_NUM_FAILURES = 3
  AS
    BEGIN
      CALL SYSTEM$SET_RETURN_VALUE('task a successful');
    END;
;

-- 2. Use a runtime reflection variable.
--    Creates a child task ("task_b").
--    By design, this example fails the first time it runs, because
--    it writes to a table ("demo_table") that doesn’t exist.
CREATE OR REPLACE TASK task_b
  USER_TASK_TIMEOUT_MS = 60000
  AFTER task_a
  AS
    BEGIN
      LET VALUE := (SELECT SYSTEM$TASK_RUNTIME_INFO('current_task_name'));
      INSERT INTO demo_table VALUES('task b name',:VALUE);
    END;
;

-- 3. Get a task graph configuration value.
--    Creates the child task ("task_c").
--    By design, this example fails the first time it runs, because
--    the predecessor task ("task_b") fails.
CREATE OR REPLACE TASK task_c
  USER_TASK_TIMEOUT_MS = 60000
  AFTER task_b
  AS
    BEGIN
      CALL SYSTEM$GET_TASK_GRAPH_CONFIG('path');
      LET VALUE := (SELECT SYSTEM$GET_TASK_GRAPH_CONFIG('path'));
      INSERT INTO demo_table VALUES('task c path',:value);
    END;
;

-- 4. Get a value from a predecessor.
--    Creates the child task ("task_d").
--    By design, this example fails the first time it runs, because
--    the predecessor task ("task_c") fails.
CREATE OR REPLACE TASK task_d
  USER_TASK_TIMEOUT_MS = 60000
  AFTER task_c
  AS
    BEGIN
      LET VALUE := (SELECT SYSTEM$GET_PREDECESSOR_RETURN_VALUE('TASK_A'));
      INSERT INTO demo_table VALUES('task d: predecessor return value', :value);
    END;
;

-- 5. Create the finalizer task ("task_f"), which creates the missing demo table.
--    After the finalizer completes, the task should automatically retry
--    (see task_a: task_auto_retry_attempts).
--    On retry, task_b, task_c, and task_d should complete successfully.
CREATE OR REPLACE TASK task_f
  USER_TASK_TIMEOUT_MS = 60000
  FINALIZE = task_a
  AS
    BEGIN
      CREATE TABLE IF NOT EXISTS demo_table(NAME VARCHAR, VALUE VARCHAR);
    END;
;

-- 6. Resume the finalizer. Upon creation, tasks start in a suspended state.
--    Use this command to resume the finalizer.
ALTER TASK task_f RESUME;
SELECT SYSTEM$TASK_DEPENDENTS_ENABLE('task_a');

-- 7. Query the task history
SELECT
    name, state, attempt_number, scheduled_from
  FROM
    TABLE(information_schema.task_history(task_name=> 'task_b'))
  LIMIT 5;
;

-- 8. Suspend the task graph to stop incurring costs
--    Note: To stop the task graph, you only need to suspend the root task
--    (task_a). Child tasks don’t run unless the root task is run.
--    If any child tasks are running, they have a limited duration
--    and will end soon.
ALTER TASK task_a SUSPEND;
DROP TABLE demo_table;

-- 9. Check tasks during execution (optional)
--    Run this command to query the demo table during execution
--    to check which tasks have run.
SELECT * FROM demo_table;

-- 10. Demo reset (optional)
--     Run this command to remove the demo table.
--     This causes task_b to fail during its first run.
--     After the task graph retries, task_b will succeed.
DROP TABLE demo_table;
```
