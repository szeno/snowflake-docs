# SHOW SERVICE CONTAINERS IN SERVICE

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Lists the containers in all instances of a [service](/developer-guide/snowpark-container-services/working-with-services).

If Snowflake encounters issues executing one or more of your service containers, this command provides visibility into the status of individual containers. Similarly, during a rolling upgrade, it shows the version of your service code running in each container.

See also:
:   [Snowpark Container Services overview](/developer-guide/snowpark-container-services/overview), [CREATE SERVICE](/sql-reference/sql/create-service), [SHOW SERVICES](/sql-reference/sql/show-services), [SHOW SERVICE INSTANCES IN SERVICE](/sql-reference/sql/show-service-instances-in-service)

## Syntax

Copy code

```
SHOW SERVICE CONTAINERS IN SERVICE <name>
```

## Parameters

`name`
:   Specifies the identifier for the service whose containers to list.

    Quoted names for special characters or case-sensitive names are not supported.

## Output

The command output provides properties and metadata of the service containers in the following columns:

| Column | Description |
| --- | --- |
| `database_name` | Database in which the service is created. |
| `schema_name` | Schema in which the service is created. |
| `service_name` | Name of the service. |
| `service_status` | One of the following values, which indicates the current status of the service:   - `PENDING` - `RUNNING` - `FAILED` - `DONE` - `SUSPENDING` - `SUSPENDED` - `DELETING` - `DELETED` - `INTERNAL_ERROR`   The value in this column is the same as the `status` column in the output of the [DESCRIBE SERVICE](/sql-reference/sql/desc-service). |
| `instance_id` | ID of the service instance (this is the index of the service instance starting from 0). When there are no service instances running (that is, service is either SUSPENDED or PENDING), instance\_id and instance\_status are returned as NULL. Also, container related fields in the output are also returned as NULL. |
| `instance_status` | One of the following values, which indicates the current status of the service instance:   - `PENDING`: The service instance is currently being deployed and is not yet ready to serve requests. - `READY`: All containers in the service instance are ready; the service instance is ready to serve requests. - `FAILED`: At least one container in the service instance has exited with a failure. - `TERMINATING`: The service instance is in the process of termination and will be removed after the process is complete. - `SUCCEEDED`: The service is a job service and all containers in the service instance have terminated successfully.   Note that for a given service instance, as identified by the `instance_id` column, the value in the `instance_status` column matches the value in the `status` column in the output of the SHOW SERVICE INSTANCES IN SERVICE command. |
| `container_name` | Name of the container. If no containers are running (that is, the service is in a SUSPENDED or PENDING state), the container name is returned as NULL, and all container-specific field values are also NULL. |
| `status` | Service container status. Currently supported status values include the following:   - `PENDING`: The container is currently being deployed. - `READY`: The container started and the readiness probe returned HTTP 200 OK status. - `DONE`: The container exited with a 0 exit code. - `FAILED`: The container exited with a non-zero exit code (exit code 0 indicates success). - `TERMINATING`: The container is shutting down due to an error, restart, completion, or deletion. - `UNKNOWN`: Snowflake could not retrieve the container status. Contact support. |
| `message` | Additional clarification about status. For example, when status is FAILED, Snowflake might provide additional information. |
| `image_name` | Image name used to create the service. |
| `image_digest` | The unique and immutable identifier representing the image content. |
| `restart_count` | Number of times Snowflake restarted the service. |
| `start_time` | Date and time when the container started. |
| `last_exit_code` | Indicates the exit code when the container last exited. For service containers, Snowflake restarts the container if it exits prematurely. The exit code is represented as an integer value:   - *NULL*: The container is currently running and has never exited. - 0: The container’s last exit was successful. - Non-zero value: The container encountered a failure. |
| `last_restart_time` | Provides the timestamp of the most recent restart of the container by Snowflake. A NULL value indicates the container never restarted. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any one of these privileges: OWNERSHIP or MONITOR | Service |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

The following example lists containers of the `echo_service` service in the current database and schema for the session:

Copy code

```
SHOW SERVICE CONTAINERS IN SERVICE echo_service;
```

Sample output:

```
+---------------+-------------+--------------+----------------+-------------+-----------------+----------------+--------+---------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+---------------+----------------------+----------------+-------------------+
| database_name | schema_name | service_name | service_status | instance_id | instance_status | container_name | status | message | image_name                                                                                                                                         | image_digest                                                            | restart_count | start_time           | last_exit_code | last_restart_time |
|---------------+-------------+--------------+----------------+-------------+-----------------+----------------+--------+---------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+---------------+----------------------+----------------+-------------------|
| TUTORIAL_DB   | DATA_SCHEMA | ECHO_SERVICE | RUNNING        | 0           | READY           | echo           | READY  | Running | orgname.acctname.registry-dev.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest                      | sha256:d04a2d7b7d9bd607df994926e3cc672edcb541474e4888a01703e8bb0dd3f173 |             0 | 2025-04-25T06:01:38Z |           NULL | NULL              |
+---------------+-------------+--------------+----------------+-------------+-----------------+----------------+--------+---------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+---------------+----------------------+----------------+-------------------+
```
