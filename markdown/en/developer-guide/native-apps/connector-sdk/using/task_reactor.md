# Task reactor

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Library which provides common elements and features that are used in all Snowflake connectors.

## Requirements

The task reactor requires at least the following sql files to be executed during Native App installation:

- `task_reactor.sql` (See: [Task reactor SQL reference](/developer-guide/native-apps/connector-sdk/reference/task_reactor_reference))

## Overview

Task reactor is a separate module that provides an orchestration mechanism for work chunks stored inside a queue with a limited set of tasks.
Task reactors’ queue and dispatcher is based on
[Snowflake Streams](/user-guide/streams-intro) with [Snowflake Tasks](/user-guide/tasks-intro) and will be triggered
every one minute due to the
refresh time limitation. The task reactor will be active only when there is data in the input queue, to allow the warehouse to save some credits.

The task Reactor consists of three main components - queue, dispatcher and workers:

1. Your connector application adds QueueItems to the queue.
2. Every minute the dispatcher (a Snowflake task) fetches awaiting QueueItems from the queue and passes them to the workers.
3. Every minute the workers (Snowflake tasks) work in parallel on the assigned QueueItems.

Once the connector configuration is finalized, the task reactor configuration is limited to 3 steps:

1. Creating All Components of Task Reactor
2. Initializing Instance
3. (optional) Changing workers number

### Creating all Components of task reactor

To create an instance object, the user first has to create `worker`, `selector` and optionally `expired selector` implementations and then integrate them using
the [TASK\_REACTOR.CREATE\_INSTANCE\_OBJECTS](/developer-guide/native-apps/connector-sdk/reference/task_reactor_reference#label-connectors-native-sdk-task-reactor-create-instance-objects) procedure.

#### Worker Implementation

The worker is responsible for performing a task assigned by the dispatcher, such as pulling and ingesting certain data.
The only mandatory part is to have a specific worker method that initiates the job. This method must be callable from the
Snowpark procedure, return a String and contain the following parameters:

- `session` - Snowpark session object
- `worker_id` - number, unique worker id
- `task_reactor_schema` - Schema name where task reactor objects are created. It can be used as a name of Task Reactor instance.

The worker is responsible for executing the task assigned by the dispatcher, e.g. pulling and
ingesting specific data. We recommend using the (`com.snowflake.connectors.sdk.taskreactor.worker.IngestionWorker`
and `com.snowflake.connectors.sdk.taskreactor.ingestion.Ingestion`) Java classes or for simpler tasks
(`com.snowflake.connectors.sdk.taskreactor.worker.SimpleTaskWorker` and `com.snowflake.connectors.sdk.taskreactor.ingestion.SimpleTask`),
however your worker can be created in any programming language supported for writing stored procedures handlers.

Example of Java worker method:

Copy code

```
public static String executeWork(Session session, int workerId, String taskReactorSchema) {
  FakeIngestion fakeIngestion = new FakeIngestion(session, workerId);
  WorkerId workerIdentifier = new WorkerId(workerId);
  Identifier schemaIdentifier = Identifier.fromWithAutoQuoting(taskReactorSchema);
  try {
    IngestionWorker.from(session, fakeIngestion, workerIdentifier, schemaIdentifier).run();
  } catch (WorkerException e) {
    // handle the exception...
    throw new RuntimeException(e);
  }
  return "Worker procedure executed.";
}
```

With an already created worker method, the user has to integrate it into `CONNECTOR.WORKER_PROCEDURE`. The procedure should call its
own worker method. It must be created in your application schema, return a STRING and contain the following parameters:

- `worker_id` - number
- `task_reactor_schema` - string

An example procedure, calling the Java implementation of the worker:

Copy code

```
CREATE OR REPLACE PROCEDURE CONNECTOR.WORKER_PROCEDURE(worker_id number, task_reactor_schema string)
  RETURNS STRING
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0', 'com.snowflake:telemetry:0.0.1')
  IMPORTS = ('@jars/myconnector-1.0.0.jar')
  HANDLER = 'com.snowflake.myconnector.WorkerImpl.executeWork';
```

The telemetry library is required to collect metrics which are logged to Event Table.

#### Selector Implementation

The selector’s job is to decide which queued tasks should be handled by the task reactor. Similar to the worker implementation -
it can be created in any language supported by Snowpark. The task selector can be implemented as a database procedure or a database view.
The selector (procedure or view) must be passed as an argument in the `TASK_REACTOR.CREATE_NEW_INSTANCE` procedure.

The procedure must be callable from a Snowpark procedure, return a string and contain the following parameters:

- `session` - Snowpark Session
- `queueItems` - String[] (an array of individual JSON Strings, each describing a single QueueItem)

Example of Java selector method:

Copy code

```
public static String selectWork(Session session, String[] queueItems) {
  Variant[] sorted =
    Arrays.stream(queueItems)
      .map(Variant::new)
      .filter(
        queueItem ->
          !queueItem.asMap().get("resourceId").asString().equals("filter-out-resource"))
      .sorted(comparing(queueItem -> queueItem.asMap().get("resourceId").asString()))
      .toArray(Variant[]::new);
  return new Variant(sorted).asJsonString();
}
```

Instead of the selector method, it is still possible to create a view that will filter and sort tasks from the existing queue.
The dispatcher can retrieve new tasks from the newly created view using an example query:

Copy code

```
CREATE VIEW CONNECTOR_SCHEMA.WORK_SELECTOR_VIEW AS SELECT * FROM TASK_REACTOR.QUEUE ORDER BY RESOURCE_ID;
```

With already created selector method, user has to integrate it into `CONNECTOR.WORK_SELECTOR`. The procedure should call
your obligatory work selector method. It must be created in your application schema, return an ARRAY, and contain the following parameter:

- `work_items - array`

An example procedure, calling the Java implementation of the work selector:

Copy code

```
CREATE OR REPLACE PROCEDURE CONNECTOR.WORK_SELECTOR(work_items array)
  RETURNS ARRAY
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('@jars/myconnector-1.0.0.jar')
  HANDLER = 'com.snowflake.myconnector.WorkSelector.selectWork';
```

#### Expired Selector Implementation

The expired selector’s job is to decide which queued items should be removed from the task reactor’s queue.
Items can be needed to be removed because the selector can never reach some items and these items would stay in the queue for ever.
Besides, some items that are waiting in the queue can be created long time before and it makes no sense to process them any more.
The expired selector can be implemented as a database view.
The selector view must be passed as an argument in the `TASK_REACTOR.CREATE_NEW_INSTANCE` procedure.
If there is no need to remove items from the queue, the default implementation can be used `TASK_REACTOR.EMPTY_EXPIRED_WORK_SELECTOR`.

Using the following query it is possible to create an expired selector view which selects the items that were created more than 3 days ago:

Copy code

```
CREATE VIEW CONNECTOR_SCHEMA.EXPIRED_WORK_SELECTOR_VIEW
  AS SELECT * FROM TASK_REACTOR.QUEUE q
  WHERE DATEDIFF(day, q.timestamp, sysdate()) > 3;
```

#### Integrate instance objects

The [TASK\_REACTOR.CREATE\_INSTANCE\_OBJECTS](/developer-guide/native-apps/connector-sdk/reference/task_reactor_reference#label-connectors-native-sdk-task-reactor-create-instance-objects) lets user configure all instances together before initializing created instances.
The procedure can be executed only once per schema, so any future calls will not effect any changes. We recommend to put
initialization call to the `setup.sql` file, to prevent the procedure from being executed multiple times or not being called at all.

Required parameters:

- `instance_schema_name VARCHAR` - One per instance unique schema which stores database objects that the instance works on.
- `worker_procedure_name VARCHAR` - Name of the worker procedure described in the `Worker Implementation` part.
- `work_selector_type VARCHAR` - Values specifying whether new tasks should use view or procedure. Possible values: VIEW, PROCEDURE.
- `work_selector_name VARCHAR` - Name of the selector procedure/view described in the `Selector Implementation` part.

Optional parameters:

- `expired_work_selector_name VARCHAR` - Name of the expired selector view described in `Expired Selector Implementation` part. If the value is not provided, `TASK_REACTOR.EMPTY_EXPIRED_WORK_SELECTOR` is used as a default implementation which returns nothing.

### Initializing Instance

To initialize and run all configurations in task reactor user has to call `INITIALIZE_INSTANCE`.
The procedure takes the following parameters as input:

- `instance_schema_name` - (required) Name of schema which stores database objects that the instance works on.
- `warehouse_name` (required) Name of warehouse on which the instance will run.
- `dt_should_be_started` (optional) - default: `TRUE`. Dispatcher task should start when creating a new instance or not.
- `dt_task_schedule` (optional) - default: `1 MINUTE`. Frequency of running the dispatcher task.
- `dt_allow_overlapping_execution` (optional) - default: `FALSE`. Allows the DAG to run concurrently.
- `dt_user_task_timeout_ms` (optional) - the time limit on a single run of the task before it times out (in milliseconds).

Note

If the worker procedure takes longer than the timeout set on the workers task
([USER\_TASK\_TIMEOUT\_MS](/sql-reference/parameters#label-user-task-timeout-ms)), the procedure
will abort with a timeout error. It is important to schedule tasks to not exceed the timeout of the
Snowflake task.

After providing the minimum number of required parameters, the `Task Reactor` is initialized with the provided configuration
and dispatches workers using the `TASK_REACTOR.DISPATCHER` procedure.

### Setting Number of Workers

Number of workers can be changed manually by calling [TASK\_REACTOR.SET\_WORKERS\_NUMBER](/developer-guide/native-apps/connector-sdk/reference/task_reactor_reference#label-connectors-native-sdk-task-reactor-set-workers-number) procedure with following parameters:

- `WORKERS_NUMBER` - new number of workers.
- `TR_INSTANCE_SCHEMA_NAME` - name of instance schema

### Metrics

Task Reactor contains a metrics mechanism. It is based on
[Snowflake Trace Events](/developer-guide/logging-tracing/tracing).
The metrics are logged into the Event Table, so the Event Table has to be enabled in order to make metrics work.

Currently, the following metrics are introduced:

- `worker working time` (`TASK_REACTOR_WORKER_WORKING_TIME`) - It shows the time when a worker was actually processing resources. The timer starts when a worker task begins and ends when the worker task finishes.
- `worker idle time` (`TASK_REACTOR_WORKER_IDLE_TIME`) - It is the opposite to the `worker working time`. It shows the time when a worker was asleep: either waiting for a new work or waiting for the next schedule of its task. The timer begins when a worker finishes its task and ends when the worker task starts again.
- `worker item waiting time` (`TASK_REACTOR_WORK_ITEM_WAITING_IN_QUEUE_TIME`) - It shows the time of work item waiting in the dispatcher queue. The timer starts when a work item is inserted to the dispatcher queue and ends when the work item is removed from the dispatcher queue and is inserted to a worker queue.
- `worker item number in queue` (`TASK_REACTOR_WORK_ITEMS_NUMBER_IN_QUEUE`) - It shows the number of work items present in the dispatcher queue.
- `worker statuses` (`TASK_REACTOR_WORKER_STATUS`) - It shows the number of workers in each worker status and the total number of workers.

In order to see all logged metrics events, the following query can be used:

Copy code

```
SET EVENT_TABLE = 'TOOLS.PUBLIC.EVENTS';
SET APP_NAME = 'YOUR_APP_NAME';

SELECT
    event.record:name::string AS EVENT_NAME,
    span.record_attributes:task_reactor_instance::string AS INSTANCE_NAME,
    span.record_attributes:worker_id AS WORKER_ID,
    event.record_attributes AS PAYLOAD
  FROM IDENTIFIER($EVENT_TABLE) event
  JOIN IDENTIFIER($EVENT_TABLE) span ON event.trace:span_id = span.trace:span_id AND event.record_type = 'SPAN_EVENT' AND span.record_type = 'SPAN'
  WHERE
    event.resource_attributes:"snow.database.name" = $APP_NAME
  ORDER BY event.timestamp DESC;
```

In order to select only one type of metrics, add `event.record:name = <metric name>` to the `where` clause of the query.
The following queries can be used to load individual metrics:

Worker working time (`TASK_REACTOR_WORKER_WORKING_TIME`)

Copy code

```
SELECT
  event.record:name::string AS EVENT_NAME,
    span.record_attributes:task_reactor_instance::string AS INSTANCE_NAME,
    span.record_attributes:worker_id AS WORKER_ID,
    event.record_attributes:value AS DURATION
  FROM IDENTIFIER($EVENT_TABLE) event
  JOIN IDENTIFIER($EVENT_TABLE) span ON event.trace:span_id = span.trace:span_id AND event.record_type = 'SPAN_EVENT' AND span.record_type = 'SPAN'
  WHERE
    event.resource_attributes:"snow.database.name" = $APP_NAME
      AND event.record:name = 'TASK_REACTOR_WORKER_WORKING_TIME'
  ORDER BY event.timestamp DESC;
```

Worker idle time (`TASK_REACTOR_WORKER_IDLE_TIME`)

Copy code

```
SELECT
    event.record:name::string AS EVENT_NAME,
    span.record_attributes:task_reactor_instance::string AS INSTANCE_NAME,
    span.record_attributes:worker_id AS WORKER_ID,
    event.record_attributes:value AS DURATION
  FROM IDENTIFIER($EVENT_TABLE) event
  JOIN IDENTIFIER($EVENT_TABLE) span ON event.trace:span_id = span.trace:span_id AND event.record_type = 'SPAN_EVENT' AND span.record_type = 'SPAN'
  WHERE
    event.resource_attributes:"snow.database.name" = $APP_NAME
        AND event.record:name = 'TASK_REACTOR_WORKER_IDLE_TIME'
  ORDER BY event.timestamp DESC;
```

Worker item waiting time (`TASK_REACTOR_WORK_ITEM_WAITING_IN_QUEUE_TIME`)

Copy code

```
SELECT
    event.record:name::string AS EVENT_NAME,
    span.record_attributes:task_reactor_instance::string AS INSTANCE_NAME,
    event.record_attributes:value AS DURATION,
    event.timestamp
  FROM IDENTIFIER($EVENT_TABLE) event
  JOIN IDENTIFIER($EVENT_TABLE) span ON event.trace:span_id = span.trace:span_id AND event.record_type = 'SPAN_EVENT' AND span.record_type = 'SPAN'
  WHERE
    event.resource_attributes:"snow.database.name" = $APP_NAME
      AND event.record:name = 'TASK_REACTOR_WORK_ITEM_WAITING_IN_QUEUE_TIME'
  ORDER BY event.timestamp DESC;
```

Worker item number in queue (`TASK_REACTOR_WORK_ITEMS_NUMBER_IN_QUEUE`)

Copy code

```
SELECT
    event.record:name::string AS EVENT_NAME,
    event.record_attributes:task_reactor_instance::string AS INSTANCE_NAME,
    event.record_attributes:value AS WORK_ITEMS_NUMBER,
    event.timestamp
  FROM IDENTIFIER($EVENT_TABLE) event
  WHERE
    event.resource_attributes:"snow.database.name" = $APP_NAME
      AND event.record:name = 'TASK_REACTOR_WORK_ITEMS_NUMBER_IN_QUEUE'
  ORDER BY event.timestamp DESC;
```

Worker statuses (`TASK_REACTOR_WORKER_STATUS`)

Copy code

```
SELECT
    event.record:name::string AS EVENT_NAME,
    span.record_attributes:task_reactor_instance::string AS INSTANCE_NAME,
    event.record_attributes:TOTAL AS WORKERS_TOTAL,
    IFNULL(event.record_attributes:AVAILABLE, 0) AS WORKERS_AVAILABLE,
    IFNULL(event.record_attributes:WORK_ASSIGNED, 0) AS WORKERS_WORK_ASSIGNED,
    IFNULL(event.record_attributes:IN_PROGRESS, 0) AS WORKERS_IN_PROGRESS,
    IFNULL(event.record_attributes:SCHEDULED_FOR_CANCELLATION, 0) AS WORKERS_SCHEDULED_FOR_CANCELLATION,
    event.timestamp
  FROM IDENTIFIER($EVENT_TABLE) event
  JOIN IDENTIFIER($EVENT_TABLE) span ON event.trace:span_id = span.trace:span_id AND event.record_type = 'SPAN_EVENT' AND span.record_type = 'SPAN'
  WHERE
    event.resource_attributes:"snow.database.name" = $APP_NAME
      AND event.record:name = 'TASK_REACTOR_WORKER_STATUS'
  ORDER BY event.timestamp DESC;
```
