Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_SERVICE\_STATUS — *Deprecated*

Deprecated Feature

This function has been deprecated. Use the [SHOW SERVICE CONTAINERS IN SERVICE](/sql-reference/sql/show-service-containers-in-service) command instead.

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Retrieves the status of a
[Snowpark Container Services service](/developer-guide/snowpark-container-services/working-with-services).

## Syntax

Copy code

```
SYSTEM$GET_SERVICE_STATUS( [ <db_name>.<schema_name>. ]<service_name> [ , <timeout_secs> ]  )
```

## Arguments

**Required:**

`service_name`
:   Service name. If you omit the `db_name` and `schema_name`, the function uses the current database and schema.

**Optional:**

`timeout_secs`
:   Number of seconds to wait for the service to reach a steady state (for example, READY) before returning the status. If the
    service does not reach a steady state within the specified time, Snowflake returns the current state.

    If not specified, Snowflake returns the current state immediately.

    Default: 0 seconds

## Returns

Returns status information in a JSON array with one JSON object for each container in each service instance. The JSON fields are:

- `status`. Service container status. Currently supported status values include: PENDING, READY, FAILED and UNKNOWN.
- `message`. Provides details about the specific status. For example, when the status is PENDING, this field describes why.
- `containerName`. Container name.
- `instanceId`. Service instance ID.
- `serviceName`. Service name.
- `image`. URL of the image that is running.
- `restartCount`. Number of times Snowflake restarted the container. A higher restart count can indicate an unhealthy
  service. For example, if your service code crashes, the container can exit. Snowflake then tries to restart the container.
  In this case, to investigate, you can access the container log using these options:

  - Use the [SYSTEM$GET\_SERVICE\_LOGS](/sql-reference/functions/system_get_service_logs) function for live logs (the container is running).
  - Use Event tables for persistent logs (useful when the container is no longer running).
- `startTime`. Time when the container started.

## Usage notes

- The current role must have the MONITOR privilege on the service to get the status information.

## Examples

The following function retrieves status information for the “echo\_service” service. The function specifies a 5-second timeout:

Copy code

```
SELECT SYSTEM$GET_SERVICE_STATUS('echo_service', 5);
```

Example outputs:

- **Running one service instance that has one container.** The function returns the container information as shown:

  Copy code

  ```
  [
   {
   "status":"READY",
   "message":"Running",
   "containerName":"echo",
   "instanceId":"0",
   "serviceName":"ECHO_SERVICE",
   "image":"<account>.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_echo_service_image:tutorial",
   "restartCount":0,
   "startTime":"2023-01-01T00:00:00Z"
   }
  ]
  ```

  `instanceId` is the service instance ID. If you have two instances of this service running, the array includes two
  objects in the output, providing container status for two separate service instances (the `instanceId` will be 0 and 1).
- **Running one service instance that has three containers (as defined in the service specification).** The function returns an
  array with three objects (one for each container):

  Copy code

  ```
  [
    {
    "status":"READY",
    "message":"Running",
    "containerName":"echo-1",
    "instanceId":"0",
    "serviceName":"ECHO_SERVICE",
    "image":"<account>.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_echo_service_image_x:tutorial",
    "restartCount":0,
    "startTime":"2023-01-01T00:00:00Z"
    },
    {
    "status":"READY",
    "message":"Running",
    "containerName":"echo-2",
    "instanceId":"0",
    "serviceName":"ECHO_SERVICE",
    "image":"<account>.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_echo_service_image_y:tutorial",
    "restartCount":0,
    "startTime":"2023-01-01T00:00:00Z"
    },
    {
    "status":"READY",
    "message":"Running",
    "containerName":"echo-3",
    "instanceId":"0",
    "serviceName":"ECHO_SERVICE",
    "image":"<account>.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_echo_service_image_z:tutorial",
    "restartCount":0,
    "startTime":"2023-01-01T00:00:00Z"
    }
  ]
  ```

Because all these containers belong to the same service instance, the `instanceId` will be 0 for all containers.
