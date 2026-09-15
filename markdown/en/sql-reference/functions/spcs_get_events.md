Categories:
:   [Table functions](/sql-reference/functions-table) (Snowpark Container Services)

# <service\_name>!SPCS\_GET\_EVENTS

Returns the events that Snowflake collected for the specified service.
For more information,
see [Accessing platform events](/developer-guide/snowpark-container-services/monitoring-services#label-spcs-monitoring-services-access-platform-events).

See also:
:   [Monitoring Services](/developer-guide/snowpark-container-services/monitoring-services)

## Syntax

Copy code

```
<service_name>!SPCS_GET_EVENTS(
  [ START_TIME => <constant_expr> ],
  [ END_TIME => <constant_expr> ] )
```

## Arguments

`START_TIME => constant_expr`
:   Start time (in TIMESTAMP\_LTZ format) for the time range from which to
    retrieve events. For available functions to construct date, time, and timestamp data, see [Date & time functions](/sql-reference/functions-date-time).

    If the `START_TIME` is not specified, it defaults to one day ago.

`END_TIME => constant_expr`
:   End time (in TIMESTAMP\_LTZ format) for the time range from which to retrieve events.

    If END\_TIME is not specified, it defaults to the current timestamp.

## Output

| Column | Type | Description |
| --- | --- | --- |
| TIMESTAMP | TIMESTAMP\_NTZ | Coordinated Universal Time (UTC) timestamp when Snowflake collected the event. This value maps to the TIMESTAMP column in the event table. |
| SEVERITY | VARCHAR | Severity of the event. This value maps to the `severity_text` field in the RECORD column in the event table. |
| EVENT\_NAME | VARCHAR | Name of the event. This value maps to the `name` field in the RECORD column in the event table. |
| EVENT\_DETAILS | OBJECT | Details about the event. This value maps to the VALUE column in the event table. |
| INSTANCE\_ID | NUMBER | Identifier of the service instance if the event is related to a service instance. This value maps to the `snow.service.instance` field in the RESOURCE\_ATTRIBUTES column in the event table. |
| CONTAINER\_NAME | VARCHAR | Name of the container if the event is related to a container. This value maps to the `snow.service.container.name` field in the RESOURCE\_ATTRIBUTES column in the event table. |
| RECORD | OBJECT | Event information in JSON format. This value maps to the RECORD column in the event table. |
| RECORD\_ATTRIBUTES | OBJECT | Additional information about the event. This value maps to the RECORD\_ATTRIBUTES column in the event table. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MONITOR | Service | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- It can take a few minutes before events show in the output.

## Examples

Retrieve the events that Snowflake recorded for the `my_test_job`
job over the past day.

Copy code

```
SELECT * FROM TABLE(mydb.myschema.my_test_job!SPCS_GET_EVENTS());
```

Example output:

```
+-------------------------+----------+--------------------------------+--------------------------------------------+-------------+----------------+---------------------------------------------+-------------------+
| TIMESTAMP               | SEVERITY | EVENT_NAME                     | EVENT_DETAILS                              | INSTANCE_ID | CONTAINER_NAME | RECORD                                      | RECORD_ATTRIBUTES |
|-------------------------+----------+--------------------------------+--------------------------------------------+-------------+----------------+---------------------------------------------+-------------------|
| 2026-07-07 22:46:14.861 | INFO     | SERVICE_INSTANCE.STATUS_CHANGE | {                                          |        0    |                | {                                           | NULL              |
|                         |          |                                |   "message": "Job instance has completed", |             |                |   "name": "SERVICE_INSTANCE.STATUS_CHANGE", |                   |
|                         |          |                                |   "status": "SUCCEEDED"                    |             |                |   "severity_text": "INFO"                   |                   |
|                         |          |                                | }                                          |             |                | }                                           |                   |
| 2026-07-07 22:46:14.366 | INFO     | SERVICE.STATUS_CHANGE          | {                                          |             |                | {                                           | NULL              |
|                         |          |                                |   "message": "Job is completed",           |             |                |   "name": "SERVICE.STATUS_CHANGE",          |                   |
|                         |          |                                |   "status": "DONE"                         |             |                |   "severity_text": "INFO"                   |                   |
|                         |          |                                | }                                          |             |                | }                                           |                   |
| 2026-07-07 22:46:10.658 | INFO     | CONTAINER.STATUS_CHANGE        | {                                          |        0    | main           | {                                           | NULL              |
|                         |          |                                |   "message": "Completed successfully",     |             |                |   "name": "CONTAINER.STATUS_CHANGE",        |                   |
|                         |          |                                |   "status": "DONE"                         |             |                |   "severity_text": "INFO"                   |                   |
|                         |          |                                | }                                          |             |                | }                                           |                   |
| 2026-07-07 22:46:07.276 | INFO     | SERVICE_INSTANCE.STATUS_CHANGE | {                                          |        0    |                | {                                           | NULL              |
|                         |          |                                |   "message": "Job instance is running",    |             |                |   "name": "SERVICE_INSTANCE.STATUS_CHANGE", |                   |
|                         |          |                                |   "status": "READY"                        |             |                |   "severity_text": "INFO"                   |                   |
|                         |          |                                | }                                          |             |                | }                                           |                   |
| 2026-07-07 22:46:07.050 | INFO     | SERVICE.STATUS_CHANGE          | {                                          |             |                | {                                           | NULL              |
|                         |          |                                |   "message": "Job is running",             |             |                |   "name": "SERVICE.STATUS_CHANGE",          |                   |
|                         |          |                                |   "status": "RUNNING"                      |             |                |   "severity_text": "INFO"                   |                   |
|                         |          |                                | }                                          |             |                | }                                           |                   |
| 2026-07-07 22:46:04.650 | INFO     | CONTAINER.STATUS_CHANGE        | {                                          |        0    | main           | {                                           | NULL              |
|                         |          |                                |   "message": "Running",                    |             |                |   "name": "CONTAINER.STATUS_CHANGE",        |                   |
|                         |          |                                |   "status": "READY"                        |             |                |   "severity_text": "INFO"                   |                   |
|                         |          |                                | }                                          |             |                | }                                           |                   |
| 2026-07-07 22:46:01.456 | INFO     | SERVICE_INSTANCE.STATUS_CHANGE | {                                          |        0    |                | {                                           | NULL              |
|                         |          |                                |   "message": "Job instance is pending",    |             |                |   "name": "SERVICE_INSTANCE.STATUS_CHANGE", |                   |
|                         |          |                                |   "status": "PENDING"                      |             |                |   "severity_text": "INFO"                   |                   |
|                         |          |                                | }                                          |             |                | }                                           |                   |
| 2026-07-07 22:46:01.384 | INFO     | SERVICE.STATUS_CHANGE          | {                                          |             |                | {                                           | NULL              |
|                         |          |                                |   "message": "Job is pending",             |             |                |   "name": "SERVICE.STATUS_CHANGE",          |                   |
|                         |          |                                |   "status": "PENDING"                      |             |                |   "severity_text": "INFO"                   |                   |
|                         |          |                                | }                                          |             |                | }                                           |                   |
| 2026-07-07 22:46:00.238 | INFO     | CONTAINER.STATUS_CHANGE        | {                                          |        0    | main           | {                                           | NULL              |
|                         |          |                                |   "message": "Waiting to start",           |             |                |   "name": "CONTAINER.STATUS_CHANGE",        |                   |
|                         |          |                                |   "status": "PENDING"                      |             |                |   "severity_text": "INFO"                   |                   |
|                         |          |                                | }                                          |             |                | }                                           |                   |
+-------------------------+----------+--------------------------------+--------------------------------------------+-------------+----------------+---------------------------------------------+-------------------+
```

Retrieve the events that Snowflake recorded for the `my_test_job` job over the past three days.

Copy code

```
SELECT * FROM TABLE(mydb.myschema.my_test_job!SPCS_GET_EVENTS(START_TIME => DATEADD('day', -3, CURRENT_TIMESTAMP())));
```
