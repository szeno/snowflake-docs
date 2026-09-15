# SHOW SERVICE INSTANCES IN SERVICE

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Lists instances of a [service](/developer-guide/snowpark-container-services/working-with-services).

The command output offers visibility into auto-scaling and rolling upgrades by displaying the status of each individual service instance.

See also:
:   [Snowpark Container Services overview](/developer-guide/snowpark-container-services/overview), [CREATE SERVICE](/sql-reference/sql/create-service), [SHOW SERVICES](/sql-reference/sql/show-services), [SHOW SERVICE CONTAINERS IN SERVICE](/sql-reference/sql/show-service-containers-in-service)

## Syntax

Copy code

```
SHOW SERVICE INSTANCES IN SERVICE <name>
```

## Parameters

`name`
:   Specifies the identifier for the service whose instances to list.

    Quoted names for special characters or case-sensitive names are not supported.

## Output

The command output provides properties and metadata of the service instances in the following columns:

| Column | Description |
| --- | --- |
| `database_name` | Database in which the service is created. |
| `schema_name` | Schema in which the service is created. |
| `service_name` | Name of the service. |
| `service_status` | One of the following values, which indicates the current status of the service:   - `PENDING` - `RUNNING` - `FAILED` - `DONE` - `SUSPENDING` - `SUSPENDED` - `DELETING` - `DELETED` - `INTERNAL_ERROR`   Note that the value in this column is the same as the `status` column in the output of the [DESCRIBE SERVICE](/sql-reference/sql/desc-service). |
| `instance_id` | ID of the service instance (this is the index of the service instance starting from 0). |
| `status` | One of the following values, which indicates the current status of the service instance:   - `PENDING`: The service instance is currently being deployed and is not yet ready to serve requests. - `READY`: All containers in the service instance are ready; the service instance is ready to serve requests. - `FAILED`: At least one container in the service instance has exited with a failure. - `TERMINATING`: The service instance is in the process of termination and will be removed after the process is complete. - `SUCCEEDED`: The service is a job service and all containers in the service instance have terminated successfully. |
| `spec_digest` | The unique and immutable identifier that represents the service specification content. |
| `creation_time` | The time when Snowflake started creating the service instance. |
| `start_time` | The time when Snowflake acknowledged the service instance is running on a node. |
| `ip_address` | IP address of the service instance. Other instances of the same service (or other services) can use this IP address to connect to a specific service instance.  When you’re running multiple service instances, you can implement leader election among the instances of a service by electing the instance with `instance_id` 0 as the leader. |

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

The following example lists instances of the `echo_service` service in the current database and schema for the session:

Copy code

```
SHOW SERVICE INSTANCES IN SERVICE echo_service;
```

Sample output:

```
+---------------+-------------+--------------+----------------+-------------+--------+------------------------------------------------------------------+----------------------+----------------------+------------+
| database_name | schema_name | service_name | service_status | instance_id | status | spec_digest                                                      | creation_time        | start_time           | ip_address |
|---------------+-------------+--------------+----------------+-------------+--------+------------------------------------------------------------------+----------------------+----------------------+------------|
| TUTORIAL_DB   | DATA_SCHEMA | ECHO_SERVICE | RUNNING        | 0           | READY  | 2831c241b8d64104fbc562d60764d7abd28602c70b6a8357341e8c8210b79da4 | 2025-04-25T06:01:32Z | 2025-04-25T06:01:32Z | 10.244.0.9 |
+---------------+-------------+--------------+----------------+-------------+--------+------------------------------------------------------------------+----------------------+----------------------+------------+
```
