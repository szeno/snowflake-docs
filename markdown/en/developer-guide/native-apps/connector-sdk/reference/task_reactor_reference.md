# Task reactor SQL reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following database objects are created through the file `task_reactor.sql`.

### TASK\_REACTOR SCHEMA

Versioned schema containing some database object of task reactor in the connector.

### TASK\_REACTOR\_INSTANCES SCHEMA

Non-Versioned schema containing some instance database object of task reactor in the connector.

### TASK\_REACTOR\_INSTANCES.INSTANCE\_REGISTRY

This table is created to store the data about Task Reactor instances in order to give the ability to track and manage
existing instances during the application runtime. The table is created in the `TASK_REACTOR_INSTANCES` schema.

- `instance_name` `VARCHAR`
- `is_initialized` `BOOLEAN`
- `is_active` `BOOLEAN`

### TASK\_REACTOR.DISPATCHER(INSTANCE\_SCHEMA\_NAME VARCHAR)

This procedure invokes the Java `DispatcherHandler.dispatchWorkItems` and dispatches work items.

### TASK\_REACTOR.SET\_WORKERS\_NUMBER (WORKERS\_NUMBER NUMBER, INSTANCE\_SCHEMA\_NAME VARCHAR)

This procedure invokes the Java `SetWorkersNumberHandler.setWorkersNumber` and sets the number of workers.

### TASK\_REACTOR.CREATE\_INSTANCE\_OBJECTS

Input parameters:

- `INSTANCE_SCHEMA_NAME` `VARCHAR`
- `WORKER_PROCEDURE_NAME` `VARCHAR`
- `WORK_SELECTOR_TYPE` `VARCHAR`
- `WORK_SELECTOR_NAME` `VARCHAR`
- `EXPIRED_WORK_SELECTOR_NAME` `VARCHAR`

Procedure creates all of instance objects required for accurate `Task reactor` flow and validates the ones who should
not be already initialized. At the end of process it insert new instance registry record to the table.

Possible errors include:

- `INSTANCE_NOT_FOUND` - Instance with this name does not exists.
- `INSTANCE_ALREADY_INITIALIZED` - Instance with this name is already initialized.
- `DEFAULT_PROCEDURE_VALIDATION_EXCEPTION` - Procedure not found.
- `SCHEMA_WITH_THE_SAME_NAME_ALREADY_EXISTS` - Schema with the same name already exists.
- `CREATING_TR_INSTANCE_EXCEPTION` - Something unexpected went wrong while creating a new instance of task reactor. No instance has been created.

### TASK\_REACTOR.INITIALIZE\_INSTANCE

Input parameters:

- `INSTANCE_SCHEMA_NAME` `VARCHAR`
- `WAREHOUSE_NAME` `VARCHAR`
- `DT_SHOULD_BE_STARTED` `BOOLEAN`
- `DT_TASK_SCHEDULE` `VARCHAR`
- `DT_ALLOW_OVERLAPPING_EXECUTION` `BOOLEAN`
- `DT_USER_TASK_TIMEOUT_MS` `VARCHAR`

Procedure starts all non initialized instances within the same database instance. It consist of checking instance exists,
or whether it is not already initialized and then creates dispatcher tasks and starts this task if was required.

Procedure ends successfully with:

Copy code

```
{
    "response_code": "OK",
    "message": "Instance has been initialized successfully."
}
```

Possible errors include:

- `INSTANCE_NOT_FOUND` - Instance does not exist.
- `INSTANCE_ALREADY_INITIALIZED` - Instance with this name is already initialized.

### TASK\_REACTOR.PAUSE\_INSTANCE

Input parameters:

- `INSTANCE_SCHEMA` `VARCHAR`

Procedure starts the process of pausing a given instance of Task Reactor and returns OK response.
It starts a job which asynchronously stops all worker tasks and the dispatcher task.
In case when a worker task was already performing an ingestion, the task is not being stopped right away, but the task will be stopped after the ingestion is finished.

Note

The logic of this procedure is already used in [Pause Connector](/developer-guide/native-apps/connector-sdk/reference/pause_connector_reference), so it’s not needed to use this procedure as a part of stopping the whole connector.

Procedure ends successfully with:

Copy code

```
{
    "response_code": "OK"
}
```

### TASK\_REACTOR.RESUME\_INSTANCE()

Input parameters:

- `INSTANCE_SCHEMA` `VARCHAR`

Procedure starts the process of resuming a given instance of Task Reactor and returns OK response.
It resumes the dispatcher task and starts a job which asynchronously resumes all worker tasks that have already assigned work.

Note

The logic of this procedure is already used in [Resume Connector](/developer-guide/native-apps/connector-sdk/reference/resume_connector_reference), so it’s not needed to use this procedure as a part of resuming the whole connector.

Procedure ends successfully with:

Copy code

```
{
    "response_code": "OK"
}
```

### TASK\_REACTOR.REMOVE\_INSTANCE()

Input parameters:

- `INSTANCE_SCHEMA` `VARCHAR`

Removes a given instance of Task Reactor from the instance registry and returns OK response.
If no instances exist with the provided name - no action is performed.

Procedure ends successfully with:

Copy code

```
{
    "response_code": "OK"
}
```

### TASK\_REACTOR.UPDATE\_WAREHOUSE\_INSTANCE

Input parameters:

- `WAREHOUSE_NAME` `VARCHAR`
- `INSTANCE_SCHEMA` `VARCHAR`

Procedure starts the process of changing the warehouse for a given instance of Task Reactor.
It changes the warehouse of the dispatcher task and then starts a job which asynchronously changes the warehouse of all worker tasks.

Note

The logic of this procedure is already used in [Update Warehouse](/developer-guide/native-apps/connector-sdk/reference/update_warehouse_reference), so it’s not needed to use this procedure as a part of updating the warehouse for the whole connector.

Procedure ends successfully with:

Copy code

```
{
    "response_code": "OK"
}
```

Possible errors include:

- `INSTANCE_NOT_FOUND` - Given instance does not exist.
- `TASK_REACTOR_INSTANCE_IS_ACTIVE` - Given Task Reactor instance has not been paused before using this procedure.

### Internal procedures

All of below procedures are used only for internal use in `task_reactor` setup script and should not be used externally.

#### TASK\_REACTOR.CREATE\_INSTANCE\_SCHEMA (INSTANCE\_SCHEMA\_NAME VARCHAR)

This procedure creates new schema with identifier named `instance_schema_name`, and then throws
a new exception if the schema could not be created.

Possible errors include:

- `SCHEMA_WITH_THE_SAME_NAME_ALREADY_EXISTS` - Schema with the same name already exists.

#### TASK\_REACTOR.VALIDATE\_PROCEDURE\_EXISTENCE

Input parameters:

- `PROCEDURE_NAME` `VARCHAR`
- `PROCEDURE_TYPE` `VARCHAR`

This procedure validates whether defined procedures does not exists and then throws new exception.

Possible errors include:

- `WORKER_PROCEDURE_NOT_FOUND_EXCEPTION` - Worker procedure not found.
- `WORK_SELECTOR_PROCEDURE_NOT_FOUND_EXCEPTION` - Work selector procedure not found.
- `DEFAULT_PROCEDURE_VALIDATION_EXCEPTION` - Procedure not found.

#### TASK\_REACTOR.CREATE\_QUEUE

Input parameters:

- `INSTANCE_SCHEMA_NAME` `VARCHAR`
- `TABLE_NAME` `VARCHAR`
- `STREAM_NAME` `VARCHAR`

The helper method for `Task Reactor`, it offers creating queue table with the name `instance_schema_name.table_name`
and the following columns:

- `ID` `STRING`
- `RESOURCE_ID` `STRING`
- `DISPATCHER_OPTIONS` `VARIANT`
- `WORKER_PAYLOAD` `VARIANT`
- `TIMESTAMP` `DATETIME`

Then it creates stream with name `instance_schema_name.stream_name` if it does not exist yet.

#### TASK\_REACTOR.CREATE\_WORKER\_REGISTRY\_SEQUENCE

Input parameters:

- `INSTANCE_SCHEMA_NAME` `VARCHAR`
- `SEQUENCE_NAME` `VARCHAR`

The helper method for `Task Reactor`, which offers creating sequence for worker registry with the
`instance_schema_name.sequence_name` sequence name.

#### TASK\_REACTOR.CREATE\_WORKER\_REGISTRY

Input parameters:

- `INSTANCE_SCHEMA_NAME` `VARCHAR`
- `TABLE_NAME` `VARCHAR`
- `SEQUENCE_NAME` `VARCHAR`

The helper method for `Task Reactor`, which offers creating worker registries consists of a table with the name
`instance_schema_name.table_name` and columns:

- `WORKER_ID NUMBER` with default `instance_schema_name.sequence_name` sequence
- `CREATED_AT` `DATETIME`
- `UPDATED_AT` `DATETIME`
- `STATUS` `STRING`

#### TASK\_REACTOR.CREATE\_WORKER\_STATUS\_TABLE

Input parameters:

- `INSTANCE_SCHEMA_NAME` `VARCHAR`
- `TABLE_NAME` `VARCHAR`

A helper method for `Task Reactor`, which offers creating a status table for a worker with the name `instance_schema_name.table_name` and columns:

- `WORKER_ID` `NUMBER`
- `TIMESTAMP` `DATETIME`
- `STATUS` `STRING`

#### TASK\_REACTOR.CREATE\_CONFIG\_TABLE

Input parameters:

- `INSTANCE_SCHEMA_NAME` `VARCHAR`
- `TABLE_NAME` `VARCHAR`
- `WORKER_PROCEDURE_NAME` `VARCHAR`
- `WORK_SELECTOR_TYPE` `VARCHAR`
- `WORK_SELECTOR_NAME` `VARCHAR`
- `EXPIRED_WORK_SELECTOR_NAME` `VARCHAR`
- `IS_INSTANCE_REGISTERED` `BOOLEAN`

The helper method for `Task Reactor`, offers to create a configuration table named `instance_schema_name.table_name`
with key and value columns. It then inserts the configuration data into the table if it is not already registered with the following values:

- `WORKER_PROCEDURE`
- `WORK_SELECTOR_TYPE`
- `WORK_SELECTOR`
- `SCHEMA`

### Related features

Other related features:

- `Scheduler`
- `Ingestion`

### Related Java objects

Java implementations and related classes:

- `Dispatcher`
- `SetWorkersNumber`
- `Worker`
