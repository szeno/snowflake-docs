# Running a Snowpark Container Services job as a Snowflake task

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

You can run a Snowpark Container Services [job service](/developer-guide/snowpark-container-services/working-with-services) as a Snowflake task. When you run a job service as a Snowflake task, the integration enables scenarios that leverage the robust containerization and scalability of Snowpark Container Services. This process occurs directly within your scheduled or event-triggered data pipelines that are managed by Snowflake Tasks.

For example, the following [CREATE TASK](/sql-reference/sql/create-task) command creates a task to run a job service every hour. The command provides the job details by using the [EXECUTE JOB SERVICE](/sql-reference/sql/execute-job-service) SQL command:

Copy code

```
CREATE TASK job_task
SCHEDULE = '60 MINUTE'
AS
  EXECUTE JOB SERVICE
    IN COMPUTE POOL my_compute_pool
    FROM SPECIFICATION $$
    spec:
      containers:
      - name: main
        image: /my_db/my_schema/my_repository/my_job_image:latest
        args:
          - "--process_data"
    $$;
```

Note

- Snowflake job tasks supports the [Serverless model](/user-guide/tasks-intro#label-tasks-compute-resources-serverless), so you don’t specify a warehouse in the CREATE TASK statement.
- When you run a job service as a task, you should run the job service synchronously, otherwise the task will report completion before the job service is completed.

## Passing data into and out of jobs running as tasks

[Task graphs](/user-guide/tasks-graphs) enable you to create and manage complex, multi-step data pipelines that seamlessly integrate job services running as tasks. You can use the [supported system functions](/user-guide/tasks-graphs#label-task-graph-with-logic) in your job service code to access the task context and use it to fetch task graph configuration, and runtime information of the executing task.

When you run job services as tasks, you can use the following data-sharing options between tasks in a task graph:

- **Predecessor return value mechanism:** In a task graph, you can pass output of a task as input to a subsequent, dependent task. Snowflake recommends this option when you pass small metadata, such as a file path, status string, or some other ID value. For more information, see [Pass return values between tasks](/user-guide/tasks-graphs#label-task-graph-pass-return-values).

  Just as with a SQL task, a job running as a task can retrieve the return value of a preceding task. Similarly, a job can also provide a return value for a subsequent task.
- **Common persistent storage mechanism:** When you transfer large datasets, such as files, Snowflake recommends that you persist the data in persistent storage, such as a Snowflake stage or table, and ensure that the tasks in your task graph can access the storage.

Note

Sessions aren’t shared between job services. Therefore, you can’t use temporary tables or session variables as a way to share data because these are session-scoped objects.

## Example

For an example, see [Tutorial: Run a Snowflake Container Services job as a Snowflake task](/developer-guide/snowpark-container-services/tutorials/advanced/run-job-as-task).
