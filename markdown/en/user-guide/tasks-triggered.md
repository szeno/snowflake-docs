# Triggered tasks

Use triggered tasks to run tasks whenever there’s a change in a [stream](/user-guide/streams-intro). This eliminates the need to poll a source frequently when the availability of new data is unpredictable. It also reduces latency because data is processed immediately.

Triggered tasks don’t use compute resources until the event is triggered.

## Considerations

Triggered tasks are supported with the following items:

- Tables
- Views
- Dynamic tables
- Apache Iceberg™ tables (managed and unmanaged)
- Data shares
- Directory tables. A directory table must be refreshed before a triggered task can detect the changes. To detect changes, you can perform either of the following tasks:
  - Set the [directory table to auto-refresh](/user-guide/data-load-dirtables-auto).
  - Refresh the directory table manually by using the [ALTER STAGE name REFRESH](/sql-reference/sql/alter-stage) command.

Triggered tasks aren’t supported with the following items:

- Hybrid tables
- Streams on external tables

For consumers to create streams on shared tables or secure views, the data provider must enable change tracking on the tables and views that are intended for sharing in their account; that is, `ALTER VIEW <view_name> SET CHANGE_TRACKING = TRUE;`. Without change tracking enabled, consumers can’t create streams on the shared data. For more information, see [Streams on shared objects](/user-guide/data-sharing-provider#label-data-sharing-streams).

## Create a triggered task

Use [CREATE TASK](/sql-reference/sql/create-task), and set the following parameters:

- Define the target stream using the `WHEN` clause. (Do not include the `SCHEDULE` parameter.)
- Additional requirements based on [compute resources](/user-guide/tasks-intro#label-tasks-compute-resources):
  - To create a task that runs on a user-managed warehouse, include the `WAREHOUSE` parameter and define the warehouse.
  - To create a serverless task, you must include the `TARGET_COMPLETION_INTERVAL` parameter. Do not include the `WAREHOUSE` parameter. Snowflake estimates the resources needed using the target completion interval, and adjusts to complete the task in this time.

The following example creates a serverless triggered task that runs whenever data changes in a stream.

> ![Diagram showing a serverless triggered task](/static/images/tasks-serverless-triggered.svg)

Copy code

```
CREATE TASK my_triggered_task
  TARGET_COMPLETION_INTERVAL='15 MINUTES'
  WHEN SYSTEM$STREAM_HAS_DATA('my_order_stream')
  AS
    INSERT INTO customer_activity
    SELECT customer_id, order_total, order_date, 'order'
    FROM my_order_stream;
```

### Migrate an existing task from a scheduled task to a triggered task

1. Suspend the task.
2. Use [ALTER TASK](/sql-reference/sql/alter-task) to update the task. Unset the `SCHEDULE` parameter, and then add the `WHEN` clause to define the target stream.
3. Resume the task.

Copy code

```
ALTER TASK task SUSPEND;
ALTER TASK task UNSET SCHEDULE;
ALTER TASK task MODIFY WHEN SYSTEM$STREAM_HAS_DATA('my_return_stream');
ALTER TASK task RESUME;
```

### Migrate an existing user-managed triggered task to a serverless triggered task

1. Suspend the task.
2. Use [ALTER TASK](/sql-reference/sql/alter-task) to update the task. Remove the `WAREHOUSE` parameter, and then set the `TARGET_COMPLETION_INTERVAL` parameter.
3. Resume the task.

Copy code

```
ALTER TASK task SUSPEND;
ALTER TASK task UNSET WAREHOUSE;
ALTER TASK task RESUME;
```

For more information, see [serverless tasks](/user-guide/tasks-intro#label-tasks-compute-resources-serverless).

## Allow a triggered task to run

When you create a triggered task, it starts in the suspended state.

To begin monitoring the stream:

- Resume the task using [ALTER TASK … RESUME](/sql-reference/sql/alter-task).

The task runs in the following conditions:

- When you first resume a triggered task, the task checks the stream for changes after the last task was run. If there is a change, the task runs; otherwise, it skips the task without using compute resources.
- If a task is running and the stream has new data, the task pauses until the current task is complete. Snowflake ensures only one instance of a task runs at a time.
- After a task is complete, Snowflake checks for changes in the stream again. If there are changes, the task runs again; if not, it skips the task.
- The task runs whenever new data is detected in the stream.
- If the stream data is hosted on a directory table, you detect changes by performing either of the following tasks:
- If a task hasn’t run for 12 hours, Snowflake schedules a health check to prevent streams from becoming stale.
  The timing of this health check isn’t guaranteed.
  If Snowflake detects no changes, the task is skipped without using compute resources.
  Task instructions must consume stream data before data retention expires; otherwise, the stream becomes stale.
  For more information, see [Avoiding stream staleness](/user-guide/streams-manage#label-streams-manage-avoiding-stream-staleness).
- Triggered tasks run at most every 30 seconds by default. If a task gets triggered again while running, the next run starts 30 seconds after the previous one was scheduled. You can lower this interval to 10 seconds by setting the [USER\_TASK\_MINIMUM\_TRIGGER\_INTERVAL\_IN\_SECONDS](/sql-reference/parameters#label-user-task-minimum-trigger-interval-in-seconds) parameter.
- When a task is triggered by [Streams on views](/user-guide/streams-intro#label-streams-views), then any changes to tables referenced by the Streams on Views query will also trigger the task, regardless of any joins, aggregations, or filters in the query.

![A diagram shows how triggered tasks manage new data as it comes in, and also check for changes every 12 hours.](/static/images/tasks-triggered.svg)

## Monitor triggered tasks

- In the `SHOW TASKS` and `DESC TASK` output, the `SCHEDULE` property displays `NULL` for triggered tasks.
- In the output of the task\_history view of the information\_schema and account\_usage schemas, the SCHEDULED\_FROM column displays TRIGGER.

## Examples

Example 1: Create a user-managed task that runs whenever data changes in either of two streams.

Copy code

```
CREATE TASK triggered_task_either_of_two_streams
  WAREHOUSE = my_warehouse
  WHEN SYSTEM$STREAM_HAS_DATA('my_return_stream')
    OR SYSTEM$STREAM_HAS_DATA('my_order_stream')
  AS
    INSERT INTO customer_activity
    SELECT customer_id, return_total, return_date, 'return'
    FROM my_return_stream
    UNION ALL
    SELECT customer_id, order_total, order_date, 'order'
    FROM my_order_stream;
```

Example 2: Create a user-managed task to run whenever data changes are detected in two different data streams. Because the task uses the AND conditional, the task is skipped if only one of the two streams has new data.

Copy code

```
CREATE TASK triggered_task_both_streams
  WAREHOUSE = my_warehouse
  WHEN SYSTEM$STREAM_HAS_DATA('orders_stream')
    AND SYSTEM$STREAM_HAS_DATA('my_order_stream')
  AS
    INSERT INTO completed_promotions
    SELECT order_id, order_total, order_time, promotion_id
    FROM orders_stream
    WHERE promotion_id IS NOT NULL;
```

Example 3: Create a user-managed task that runs whenever data changes in a directory table. In the example, a stream — my\_directory\_table\_stream — is hosted on a [directory table](/user-guide/data-load-dirtables-manage) on a stage called my\_test\_stage.

Copy code

```
CREATE TASK triggered_task_directory_table
  WAREHOUSE = my_warehouse
  WHEN SYSTEM$STREAM_HAS_DATA('my_directory_table_stream')
  AS
    INSERT INTO tasks_runs
    SELECT 'trigger_t_internal_stage', relative_path, size,
            last_modified, file_url, etag, metadata$action
    FROM my_directory_table_stream;
```

To validate the triggered task, data is added to the stage.

Copy code

```
COPY INTO @my_test_stage/my_test_file
  FROM (SELECT 100)
  OVERWRITE=TRUE
```

The directory table is then refreshed manually, which triggers the task.

Copy code

```
ALTER STAGE my_test_stage REFRESH
```
