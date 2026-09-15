# DESCRIBE POSTGRES INSTANCE

Describes the properties of a [Snowflake Postgres instance](/user-guide/snowflake-postgres/about).

Use this command to:

- Monitor the [state](#instance-states) of an instance during asynchronous operations like ALTER, CREATE, or FORK.
- Retrieve connection details such as the hostname.
- Check configuration settings like high availability status, Postgres version, and custom server settings.
- View the `origin` field to identify forked instances and their source.

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE POSTGRES INSTANCE](/sql-reference/sql/create-postgres-instance), [ALTER POSTGRES INSTANCE](/sql-reference/sql/alter-postgres-instance), [DROP POSTGRES INSTANCE](/sql-reference/sql/drop-postgres-instance), [SHOW POSTGRES INSTANCES](/sql-reference/sql/show-postgres-instances)

## Syntax

Copy code

```
{ DESC | DESCRIBE } POSTGRES INSTANCE <name>
```

## Parameters

`name`
:   Specifies the identifier for the Postgres instance to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

The command returns results in a property/value format rather than columnar output. Each property appears as
a separate row with its corresponding value.

| Property | Description |
| --- | --- |
| `name` | Name of the Postgres instance. |
| `owner` | Role that owns the Postgres instance. |
| `owner_role_type` | Type of the owner role (for example, ROLE or DATABASE\_ROLE). |
| `created_on` | Date and time when the Postgres instance was created. |
| `updated_on` | Date and time when the Postgres instance was last updated. |
| `type` | Type of the Postgres instance (for example, PRIMARY). |
| `host` | Hostname used to connect to the Postgres instance. |
| `privatelink_service_identifier` | Identifier for the [Private Link service](/user-guide/admin-security-privatelink), if Private Link is configured for the instance. |
| `compute_family` | [Compute family](/user-guide/snowflake-postgres/postgres-instance-sizes) (instance size) of the Postgres instance. |
| `storage_size_gb` | Storage size allocated to the Postgres instance, in GB. |
| `postgres_version` | Major version of Postgres running on the instance. |
| `postgres_settings` | Custom [Postgres server settings](/user-guide/snowflake-postgres/postgres-server-settings) configured for the instance. |
| `high_availability` | Whether [high availability](/user-guide/snowflake-postgres/high-availability) is enabled for the instance (`true` or `false`). |
| `authentication_authority` | Authentication method used for the instance (currently `POSTGRES`). |
| `maintenance_window_start` | Hour of day (0-23, UTC) when a [maintenance window](/user-guide/snowflake-postgres/managing-instances) can start, or `None` if not set. |
| `state` | Current [state](#instance-states) of the instance. Possible values: `CREATING`, `RESTORING`, `STARTING`, `REPLAYING`, `FINALIZING`, `READY`, `RESTARTING`, `RESUMING`, `SUSPENDING`, `SUSPENDED`. |
| `comment` | Comment for the Postgres instance, or `None` if not set. |
| `origin` | Origin of the Postgres instance (for example, if forked from another instance), or `None` if not a fork. |
| `replicas` | List of [read replicas](/user-guide/snowflake-postgres/postgres-create-replica) associated with the instance. |
| `operations` | Pending or in-progress operations on the instance (for example, resize, upgrade, HA enablement). |
| `network_policy` | [Network policy](/user-guide/snowflake-postgres/postgres-network) attached to the instance, or `None` if not set. |
| `storage_integration` | Storage integration used by the instance, or `None` if not set. |
| `certificate` | [SSL certificate](/user-guide/snowflake-postgres/postgres-ssl-certs) for secure connections to the Postgres instance. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OPERATE or OWNERSHIP | Postgres instance |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

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

- Use this command to check the [state](#instance-states) of an instance during create, modify, or other
  asynchronous operations. The `operations` field is a JSON string that reflects whatever sequence of operations
  happens during a CREATE POSTGRES INSTANCE or ALTER POSTGRES INSTANCE operation. You can wait for the `operations`
  field to become empty, or for one of the tasks to have the value `ready`. The following shows an example of
  the `operations` field value near the end of an ALTER POSTGRES INSTANCE operation to change the
  COMPUTE\_FAMILY setting.

```
 {
   "upgrade" : {
     "state" : "UPGRADING",
     "start" : "2026-02-16 14:13:58.371 -0800",
     "duration" : "3m36s",
     "compute_family" : "BURST_M",
     "tasks" : [ {
       "flavor" : "resize",
       "state" : "creating"
     }, {
       "flavor" : "resize",
       "state" : "finalizing"
     }, {
       "flavor" : "resize",
       "state" : "ready"
     } ]
   }
}
```

## Examples

Describe a Postgres instance:

Copy code

```
DESCRIBE POSTGRES INSTANCE my_postgres;
```

The following shows typical output from that command:

```
+------------------------------------------------------------------------+
| property                       | value                                 |
|--------------------------------+---------------------------------------|
| name                           | MY_TEST_INSTANCE                      |
| owner                          | ACCOUNTADMIN                          |
| owner_role_type                | ROLE                                  |
| created_on                     | 2026-01-29 10:04:59.485 -0800         |
| updated_on                     | 2026-02-16 13:21:58.018 -0800         |
| type                           | PRIMARY                               |
| host                           | my-instance-hostname.us-west-2.aws    |
|                                | .postgres.snowflake.pp                |
| privatelink_service_identifier | None                                  |
| compute_family                 | BURST_S                               |
| storage_size_gb                | 10                                    |
| postgres_version               | 18                                    |
| postgres_settings              | {}                                    |
| high_availability              | false                                 |
| authentication_authority       | POSTGRES                              |
| maintenance_window_start       | None                                  |
| state                          | READY                                 |
| comment                        | None                                  |
| origin                         | None                                  |
| replicas                       |                                       |
| operations                     | { }                                   |
| network_policy                 | None                                  |
| storage_integration            | None                                  |
| certificate                    | -----BEGIN CERTIFICATE-----           |
|                                | ... several lines of certificate ...  |
|                                | -----END CERTIFICATE-----             |
|                                |                                       |
+------------------------------------------------------------------------+
```

Use SHOW with the [flow operator](/sql-reference/operators-flow) to find an instance, then describe it:

Copy code

```
-- Find instances in a specific state
SHOW POSTGRES INSTANCES
  ->> SELECT "name", "state", "postgres_version"
      FROM $1
      WHERE "state" = 'READY' AND "postgres_version" = '17';

-- Then describe a specific instance for full details
DESCRIBE POSTGRES INSTANCE my_postgres;
```

Use the flow operator to extract specific properties:

Copy code

```
DESCRIBE POSTGRES INSTANCE my_postgres
  ->> SELECT "property", "value"
      FROM $1
      WHERE "property" IN ('name', 'state', 'host',
        'postgres_version', 'high_availability');
```

Check the connection hostname for an instance:

Copy code

```
DESCRIBE POSTGRES INSTANCE my_postgres
  ->> SELECT "value" AS hostname
      FROM $1
      WHERE "property" = 'host';
```
