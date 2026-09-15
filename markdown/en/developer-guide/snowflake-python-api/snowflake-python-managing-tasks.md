# Managing Snowflake tasks and task graphs with Python

You can use Python to manage Snowflake tasks, with which you can execute SQL statements, procedure calls, and logic in
[Snowflake Scripting](/developer-guide/snowflake-scripting/index). For an overview of tasks, see [Introduction to tasks](/user-guide/tasks-intro).

The Snowflake Python APIs represents tasks with two separate types:

- `Task`: Exposes a task’s properties such as its schedule, parameters, and predecessors.
- `TaskResource`: Exposes methods you can use to fetch a corresponding `Task` object, execute the task, and alter the task.

## Prerequisites

The examples in this topic assume that you’ve added code to connect with Snowflake and to create a `Root` object from which to use the
Snowflake Python APIs.

For example, the following code uses connection parameters defined in a configuration file to create a connection to Snowflake:

Copy code

```
from snowflake.core import Root
from snowflake.snowpark import Session

session = Session.builder.config("connection_name", "myconnection").create()
root = Root(session)
```

Using the resulting `Session` object, the code creates a `Root` object to use the API’s types and methods. For more information,
see [Connect to Snowflake with the Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake).

## Creating a task

To create a task, first create a `Task` object. Then, specifying the database and schema in which to create the task,
create a `TaskCollection` object. Using `TaskCollection.create`, add the new task to Snowflake.

Code in the following example creates a `Task` object representing a task named `my_task` that runs a SQL query specified in
the `definition` parameter:

Copy code

```
from datetime import timedelta
from snowflake.core.task import Task

my_task = Task(name="my_task", definition="<sql query>", schedule=timedelta(hours=1))
tasks = root.databases['my_db'].schemas['my_schema'].tasks
tasks.create(my_task)
```

This code creates a `TaskCollection` variable `tasks` from the `my_db` database and the
`my_schema` schema. Using `TaskCollection.create`, it creates a new task in Snowflake.

This code example also specifies a `timedelta` value of one hour for the task’s schedule. You can define the schedule of a task using
either a `timedelta` value or a `Cron` expression.

You can also create a task that runs a Python function or a stored procedure. Code in the following example creates a task named
`my_task2` that runs a function represented by a `StoredProcedureCall` object:

Copy code

```
from snowflake.core.task import StoredProcedureCall, Task

my_task2 = Task(
  "my_task2",
  StoredProcedureCall(
      dosomething, stage_location="@mystage"
  ),
  warehouse="test_warehouse"
)
tasks = root.databases['my_db'].schemas['my_schema'].tasks
tasks.create(my_task2)
```

This object specifies a function named
`dosomething` located in the `@mystage` stage location. You must also specify a `warehouse` when creating a task with a `StoredProcedureCall` object.

## Creating or altering a task

You can set properties of a `Task` object and pass it to the `TaskResource.create_or_alter` method to create a task if it
doesn’t exist, or alter it according to the task definition if it does exist. The behavior of `create_or_alter` is intended to be
idempotent, which means that the resulting task object will be the same regardless of whether the task exists before you call the method.

Note

The `create_or_alter` method uses default values for any [Task](https://docs.snowflake.com/en/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.task.Task)
properties that you don’t explicitly define. For example, if you don’t set `schedule`, its value defaults to `None` even if the
task previously existed with a different value.

Code in the following example updates the definition and schedule of the `my_task` task, and then alters the task on Snowflake:

Copy code

```
from datetime import timedelta
from snowflake.core.task import Task

my_task = root.databases['my_db'].schemas['my_schema'].tasks['my_task'].fetch()
my_task.definition = "<sql query 2>"
my_task.schedule = timedelta(hours=2)

my_task_res = root.databases['my_db'].schemas['my_schema'].tasks['my_task']
my_task_res.create_or_alter(my_task)
```

## Listing tasks

You can list tasks using the `TaskCollection.iter` method. The method returns a `PagedIter` iterator of `Task` objects.

Code in the following example lists tasks whose name begins with *my*:

Copy code

```
from snowflake.core.task import TaskCollection

tasks: TaskCollection = root.databases['my_db'].schemas['my_schema'].tasks
task_iter = tasks.iter(like="my%")  # returns a PagedIter[Task]
for task_obj in task_iter:
  print(task_obj.name)
```

## Performing task operations

You can perform common task operations (such as executing, suspending, and resuming tasks) with a `TaskResource` object.

Code in the following example executes, suspends, resumes, and drops the `my_task` task:

Copy code

```
tasks = root.databases['my_db'].schemas['my_schema'].tasks
task_res = tasks['my_task']

task_res.execute()
task_res.suspend()
task_res.resume()
task_res.drop()
```

## Managing tasks in a task graph

You can manage tasks collected in a task graph. A task graph is a series of tasks with a single root task and additional tasks
organized by their dependencies.

For more about tasks in a task graph, see [Create a sequence of tasks with a task graph](/user-guide/tasks-graphs#label-task-dag).

### Creating a task graph

To create a task graph, first create a `DAG` object that specifies its name and other optional properties, such as its schedule.
You can define the schedule of a task graph using either a `timedelta` value or a `Cron` expression.

Code in the following example defines a Python function `dosomething`, then specifies the function as a `DAGTask` object named
`dag_task2` in the task graph:

Copy code

```
from datetime import timedelta
from snowflake.core.task import StoredProcedureCall
from snowflake.core.task.dagv1 import DAG, DAGTask, DAGOperation
from snowflake.snowpark import Session
from snowflake.snowpark.functions import sum as sum_

def dosomething(session: Session) -> None:
  df = session.table("target")
  df.group_by("a").agg(sum_("b")).save_as_table("agg_table")

with DAG("my_dag", schedule=timedelta(days=1)) as dag:
  # Create a task that runs some SQL.
  dag_task1 = DAGTask(
    "dagtask1",
    "MERGE INTO target USING source_stream WHEN MATCHED THEN UPDATE SET target.v = source_stream.v"
  )
  # Create a task that runs a Python function.
  dag_task2 = DAGTask(
    StoredProcedureCall(
      dosomething, stage_location="@mystage",
      packages=["snowflake-snowpark-python"]
    ),
    warehouse="test_warehouse"
  )
# Shift right and left operators can specify task relationships.
dag_task1 >> dag_task2  # dag_task1 is a predecessor of dag_task2
schema = root.databases["my_db"].schemas["my_schema"]
dag_op = DAGOperation(schema)
dag_op.deploy(dag)
```

This code also defines a SQL statement as another `DAGTask` object named `dag_task1`, and then specifies
`dag_task1` as a predecessor of `dag_task2`. Finally, it deploys the task graph to Snowflake in the `my_db` database and the
`my_schema` schema.

### Creating a task graph with a cron schedule, task branches, and function return values

You can also create a task graph with a specified cron schedule, task branches, and function return values that are used as task return
values.

Code in the following example creates a `DAG` object with a `Cron` object specifying its schedule. It defines a
`DAGTaskBranch` object named `task1_branch` along with other `DAGTask` objects, and specifies their dependencies to one
another:

Copy code

```
from snowflake.core._common import CreateMode
from snowflake.core.task import Cron
from snowflake.core.task.dagv1 import DAG, DAGTask, DAGOperation, DAGTaskBranch
from snowflake.snowpark import Session

def task_handler(session: Session) -> None:
  pass  # do something

def task_branch_handler(session: Session) -> str:
  # do something
  return "task3"

with DAG(
  "my_dag",
  schedule=Cron("10 * * * *", "America/Los_Angeles"),
  stage_location="@mystage",
  packages=["snowflake-snowpark-python"],
  use_func_return_value=True,
) as dag:
  task1 = DAGTask(
    "task1",
    task_handler,
    warehouse="test_warehouse",
  )
  task1_branch = DAGTaskBranch("task1_branch", task_branch_handler, warehouse="test_warehouse")
  task2 = DAGTask("task2", task_handler, warehouse="test_warehouse")
  task3 = DAGTask("task3", task_handler, warehouse="test_warehouse", condition="1=1")
  task1 >> task1_branch
  task1_branch >> [task2, task3]
schema = root.databases["my_db"].schemas["my_schema"]
op = DAGOperation(schema)
op.deploy(dag, mode=CreateMode.or_replace)
```

This code example also defines task handler functions and creates each `DAGTask` and `DAGTaskBranch` object with a specified
task handler assigned to the task. The code sets the DAG’s `use_func_return_value` parameter to `True`, which specifies to use the
Python function’s return value as the corresponding task’s return value. Otherwise the default value of `use_func_return_value` is
`False`.

### Setting and getting the return value of a task in a task graph

When a task’s definition is a `StoredProcedureCall` object, the handler of the stored procedure (or function) can explicitly set the
return value of the task by using a `TaskContext` object. To use a `TaskContext` object, you need to add `snowflake.core`
to the list of imported packages by using the `packages` argument of `StoredProcedureCall`, `DAG`, or `DAGTask` object.

For more information, see [SYSTEM$SET\_RETURN\_VALUE](/sql-reference/functions/system_set_return_value).

Code in the following example defines a task handler function that creates a `TaskContext` object named `context` from the
current session. Then it uses the `TaskContext.set_return_value` method to explicitly set the return value to a specified string:

Copy code

```
from snowflake.core.task.context import TaskContext
from snowflake.snowpark import Session

def task_handler(session: Session) -> None:
  context = TaskContext(session)
  # this return value can be retrieved by successor Tasks.
  context.set_return_value("predecessor_return_value")
```

In a task graph, an immediate successor task that identifies the previous task as its predecessor can then retrieve the return value
explicitly set by the predecessor task.

For more information, see [SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](/sql-reference/functions/system_get_predecessor_return_value).

Code in the following example defines a task handler function that uses the `TaskContext.get_predecessor_return_value` method to get
the return value of the predecessor task named `pred_task_name`:

Copy code

```
from snowflake.core.task.context import TaskContext
from snowflake.snowpark import Session

def task_handler(session: Session) -> None:
  context = TaskContext(session)
  pred_return_value = context.get_predecessor_return_value("pred_task_name")
```
