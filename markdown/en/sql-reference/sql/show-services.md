# SHOW SERVICES

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Lists the [Snowpark Container Services services](/developer-guide/snowpark-container-services/working-with-services) (including job services) for
which you have access privileges.

- The SHOW SERVICES output also includes services running as jobs (see [EXECUTE JOB SERVICE](/sql-reference/sql/execute-job-service)).
- SHOW JOB SERVICES provides only the list of services running as jobs.
- SHOW SERVICES EXCLUDE JOBS output does not include services running as jobs.

See also:
:   [CREATE SERVICE](/sql-reference/sql/create-service) , [ALTER SERVICE](/sql-reference/sql/alter-service), [DROP SERVICE](/sql-reference/sql/drop-service) , [DESCRIBE SERVICE](/sql-reference/sql/desc-service), [SHOW SERVICE INSTANCES IN SERVICE](/sql-reference/sql/show-service-instances-in-service), [SHOW SERVICE CONTAINERS IN SERVICE](/sql-reference/sql/show-service-containers-in-service)

## Syntax

Copy code

```
SHOW [ JOB ] SERVICES [ EXCLUDE JOBS ] [ LIKE '<pattern>' ]
           [ IN
                {
                  ACCOUNT                  |

                  DATABASE                 |
                  DATABASE <database_name> |

                  SCHEMA                   |
                  SCHEMA <schema_name>     |
                  <schema_name>            |

                  COMPUTE POOL <compute_pool_name>
                }
           ]
           [ STARTS WITH '<name_string>' ]
           [ LIMIT <rows> [ FROM '<name_string>' ] ]
           [ OF TYPE <workload_type> [ , ... ] ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns records for the entire account.

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or for a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

        Note

        Using SHOW commands without an `IN` clause in a database context can result in fewer than expected results.

        Objects with the same name are only displayed once if no `IN` clause is used. For example, if you have table `t1` in
        `schema1` and table `t1` in `schema2`, and they are both in scope of the database context you’ve specified (that is, the database
        you’ve selected is the parent of `schema1` and `schema2`), then SHOW TABLES only displays one of the `t1` tables.

    `SCHEMA`, `SCHEMA schema_name`
    :   Returns records for the current schema in use or a specified schema (`schema_name`).

        `SCHEMA` is optional if a database is in use or if you specify the fully qualified `schema_name` (for example, `db.schema`).

        If no database is in use, specifying `SCHEMA` has no effect on the output.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

`OF TYPE workload_type [ , ... ]`
:   Optionally filters the command output by the workload types. For a list of available workload types, see [ALLOWED\_SPCS\_WORKLOAD\_TYPES](/sql-reference/parameters#label-allowed-spcs-workload-types). The filter is case-insensitive.

    Default: ALL

## Output

The command output provides service properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Snowpark Container Services service name. |
| `status` | One of the following values, which indicates the current status of the service:   - `PENDING` - `RUNNING` - `FAILED` - `DONE` - `CANCELLING` (job services only) - `CANCELLED` (job services only) - `SUSPENDING` - `SUSPENDED` - `DELETING` - `DELETED` - `INTERNAL_ERROR` |
| `database_name` | Database in which the service is created. |
| `schema_name` | Schema in which the service is created. |
| `owner` | Role that owns the service. |
| `compute_pool` | Compute pool name where Snowflake runs the service. |
| `dns_name` | Snowflake-assigned DNS name of the service in this format: `service-name.unique-id.svc.spcs.internal`.  The `unique-id` is a 4-8 character long alphanumeric identifier that is unique to a particular instance of a database schema. To find the unique ID for a schema, call the SYSTEM$GET\_SERVICE\_DNS\_DOMAIN function. For example:  Copy code  ``` SELECT SYSTEM$GET_SERVICE_DNS_DOMAIN('mydb.myschema'); ```  Note the following:   - If you rename a schema, the identifier remains unchanged. - If you drop and recreate a schema with the same name, the identifier will change.   The DNS name enables service-to-service communications (see [Tutorial 4](/developer-guide/snowpark-container-services/tutorials/advanced/tutorial-4)). |
| `current_instances` | The current number of instances for the service. |
| `target_instances` | The target number of service instances that should be running as determined by Snowflake.  When the `current_instances` value is not equal to the `target_instances` value, Snowflake is either in the process of shutting down or launching service instances.  For example, consider the following:   - Suppose you create a service with MIN\_INSTANCES = 1 and MAX\_INSTANCES = 3. While the service is running, Snowflake might   determine that one instance is not enough. In this case, the value of `target_instances` will increase, indicating Snowflake is in the process of launching additional instances.   It’s also possible that the `target_instances` value is less than the `current_instances` value, which indicates that Snowflake is in the process of reducing the number of running instances.   - If you create services but the compute pool does’t have capacity for the minimum number of instances that you requested, the   value of `target_instances` will be equal to the value of `min_instances`. The value of `current_instances` will be less than the value of `target_instances`. |
| `min_ready_instances` | Indicates the minimum service instances that must be ready for Snowflake to consider the service is ready to process requests. |
| `min_instances` | Minimum number of service instances Snowflake should run. |
| `max_instances` | Maximum number of service instances that Snowflake can scale when needed. |
| `auto_resume` | If `true`, Snowflake auto-resumes the service, if suspended, when service function is called or when an incoming request (ingres) is received (see [Using a service](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating)). |
| `external_access_integrations` | List of external access integrations associated with the service. For more information, see [Configure service egress](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress). |
| `created_on` | Date and time when the service was created. |
| `updated_on` | Date and time when service is last updated. |
| `resumed_on` | Timestamp when the service was last resumed. |
| `suspended_on` | Timestamp when the service was last suspended. `suspended_on` is set when Snowflake suspends a service and remains unchanged even after the service is resumed. If `suspended_on` is NULL, the service was never suspended. |
| `auto_suspend_secs` | Number of seconds of inactivity after which Snowflake automatically suspends the service. If `auto_suspend_secs` is set to 0 or never set, Snowflake does not automatically suspend the service. |
| `comment` | Service related comment. |
| `owner_role_type` | The type of role that owns the object, either ROLE or DATABASE\_ROLE. |
| `query_warehouse` | When a service container connects to Snowflake to execute a query and does not explicitly specify a warehouse to use, Snowflake uses this warehouse as default. |
| `is_job` | `true` if the service is a job service; `false` otherwise. SHOW JOB SERVICES and SHOW SERVICES EXCLUDE JOBS do not include this column in the output. |
| `is_async_job` | If TRUE, the job service is running asynchronously. By default, Snowflake executes the job services synchronously. This column is included in the output of the SHOW SERVICES, and SHOW JOB SERVICES commands but not in the output of the SHOW SERVICES EXCLUDING JOBS command. |
| `spec_digest` | The unique and immutable identifier representing the service spec content.  To observe the changes to the value of the `spec_digest` column over time, a service user might execute the SHOW SERVICES command periodically. If the service user notices a change in value, they can infer that the service was upgraded. |
| `is_upgrading` | TRUE, if Snowflake is in the process of upgrading the service. |
| `managing_object_domain` | The domain of the managing object (for example, the domain of the notebook that manages the service). NULL if the service is not managed by a Snowflake entity. |
| `managing_object_name` | The name of the managing object (for example, the name of the notebook that manages the service). NULL if the service is not managed by a Snowflake entity. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any one of these privileges: OWNERSHIP, USAGE, MONITOR or OPERATE | Service |  |

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

The following example lists services in the current database and schema for the session:

Copy code

```
SHOW SERVICES;
```

Sample output:

```
+--------------+---------+---------------+-------------+-----------+-----------------------+-------------------------------------+-------------------+------------------+---------------------+---------------+---------------+-------------+------------------------------+-------------------------------+-------------------------------+------------+--------------+-------------------+---------+-----------------+-----------------+--------+--------------+------------------------------------------------------------------+--------------+------------------------+----------------------+
| name         | status  | database_name | schema_name | owner     | compute_pool          | dns_name                            | current_instances | target_instances | min_ready_instances | min_instances | max_instances | auto_resume | external_access_integrations | created_on                    | updated_on                    | resumed_on | suspended_on | auto_suspend_secs | comment | owner_role_type | query_warehouse | is_job | is_async_job | spec_digest                                                      | is_upgrading | managing_object_domain | managing_object_name |
|--------------+---------+---------------+-------------+-----------+-----------------------+-------------------------------------+-------------------+------------------+---------------------+---------------+---------------+-------------+------------------------------+-------------------------------+-------------------------------+------------+--------------+-------------------+---------+-----------------+-----------------+--------+--------------+------------------------------------------------------------------+--------------+------------------------+----------------------|
| ECHO_SERVICE | RUNNING | TUTORIAL_DB   | DATA_SCHEMA | TEST_ROLE | TUTORIAL_COMPUTE_POOL | echo-service.k3m6.svc.spcs.internal |                 1 |                1 |                   1 |             1 |             1 | true        | NULL                         | 2024-11-29 12:12:47.310 -0800 | 2024-11-29 12:12:48.843 -0800 | NULL       | NULL         |                 0 | NULL    | ROLE            | NULL            | false  | false        | edaf548eb0c2744a87426529b53aac75756d0ea1c0ba5edb3cbb4295a381f2b4 | false        | NULL                   | NULL                 |
+--------------+---------+---------------+-------------+-----------+-----------------------+-------------------------------------+-------------------+------------------+---------------------+---------------+---------------+-------------+------------------------------+-------------------------------+-------------------------------+------------+--------------+-------------------+---------+-----------------+-----------------+--------+--------------+------------------------------------------------------------------+--------------+------------------------+----------------------+
```

The following example lists one service:

Copy code

```
SHOW SERVICES LIMIT 1;
```

The following example lists services with names containing “echo”:

Copy code

```
SHOW SERVICES LIKE '%echo%';
```

The following example lists one service with a name containing “echo”:

Copy code

```
SHOW SERVICES LIKE '%echo%' LIMIT 1;
```

The following example lists only services running as a job:

Copy code

```
SHOW JOB SERVICES;
```
