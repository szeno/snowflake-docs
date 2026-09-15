# SYSTEM$GET\_APPLICATION\_SERVICE\_LOGS

Returns the container logs for a running
[Application Service](/sql-reference/sql/create-application-service).
Use this function to troubleshoot a deployed application.

## Syntax

Copy code

```
SYSTEM$GET_APPLICATION_SERVICE_LOGS( '<service_identifier>' [ , <tail_lines> [ , <instance_id> ] ] )
```

## Arguments

`service_identifier`
:   Fully qualified or unqualified identifier of the Application Service.

`tail_lines`
:   Optional number of log lines to return, starting from the end. The default
    is `500`.

`instance_id`
:   Optional instance number to get logs from. Instances are numbered from `0`.
    The default is `0`. If that instance isn’t running, Snowflake returns an
    error that lists the valid IDs, for example:
    `Invalid instance id 3. Valid instance ids: 0, 1`.

## Returns

A string that contains the concatenated log output from the service containers.

## Access control requirements

The role must have the MONITOR privilege on the Application Service.

## Usage notes

- The service identifier must be enclosed in single quotes.
- The service must be in a running state to return container logs. For a
  suspended service, the function returns an empty result.
- If the service has more than one instance, pass `instance_id` to choose
  which one. You must also pass `tail_lines`.
- For structured logs routed through an active event table, query the event
  table directly. For more information, see
  [Logging, tracing, and metrics](/developer-guide/logging-tracing/logging-tracing-overview).

## Examples

Copy code

```
SELECT SYSTEM$GET_APPLICATION_SERVICE_LOGS('my_db.my_schema.my_app');

-- Return the last 200 lines
SELECT SYSTEM$GET_APPLICATION_SERVICE_LOGS('my_db.my_schema.my_app', 200);

-- Return logs from instance 1
SELECT SYSTEM$GET_APPLICATION_SERVICE_LOGS('my_db.my_schema.my_app', 500, 1);
```
