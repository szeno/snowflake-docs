# CREATE POSTGRES INSTANCE

Creates a new [Snowflake Postgres instance](/user-guide/snowflake-postgres/about) or creates a
fork of an existing instance.

Forking creates a **full, independent copy** of an instance at a specific point in time using
[point-in-time recovery (PITR)](/user-guide/snowflake-postgres/postgres-point-in-time-recovery).
This is useful for recovery, testing, or creating development environments from production data.

See also:
:   [ALTER POSTGRES INSTANCE](/sql-reference/sql/alter-postgres-instance), [DESCRIBE POSTGRES INSTANCE](/sql-reference/sql/desc-postgres-instance), [DROP POSTGRES INSTANCE](/sql-reference/sql/drop-postgres-instance), [SHOW POSTGRES INSTANCES](/sql-reference/sql/show-postgres-instances)

## Syntax

Copy code

```
CREATE POSTGRES INSTANCE <name>
  COMPUTE_FAMILY = '<compute_family>'
  STORAGE_SIZE_GB = <storage_gb>
  AUTHENTICATION_AUTHORITY = { POSTGRES | POSTGRES_OR_SNOWFLAKE }
  [ POSTGRES_VERSION = { 16 | 17 | 18 } ]
  [ NETWORK_POLICY = '<network_policy>' ]
  [ HIGH_AVAILABILITY = { TRUE | FALSE } ]
  [ STORAGE_INTEGRATION = '<storage_integration_name>' ]
  [ POSTGRES_SETTINGS = '<json_string>' ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
```

The following syntax creates a fork of an existing instance at a point in time. The FORK clause uses
[point-in-time recovery](/user-guide/snowflake-postgres/postgres-point-in-time-recovery)
with the same AT | BEFORE syntax as [Time Travel](/user-guide/data-time-travel), but creates a
full physical copy of the Postgres instance:

Copy code

```
CREATE POSTGRES INSTANCE <name>
  FORK <source_instance>
  [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> } ) ]
  [ COMPUTE_FAMILY = '<compute_family>' ]
  [ STORAGE_SIZE_GB = <storage_gb> ]
  [ HIGH_AVAILABILITY = { TRUE | FALSE } ]
  [ POSTGRES_SETTINGS = '<json_string>' ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
```

## Required parameters

`name`
:   Specifies the identifier (name) for the Postgres instance; must be unique for the account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`COMPUTE_FAMILY = 'compute_family'`
:   Specifies the [instance size](/user-guide/snowflake-postgres/postgres-instance-sizes) for the Postgres instance.

    Snowflake Postgres offers three tiers:

    - **Burstable** (BURST\_S, BURST\_M): Cost-effective for development and intermittent workloads. Limited to
      100GB storage and does not support high availability.
    - **Standard** (STANDARD\_M through STANDARD\_24XL): Balanced CPU and memory for general-purpose workloads. Supports
      all features including high availability.
    - **Memory-optimized** (HIGHMEM\_L through HIGHMEM\_48XL): Higher memory-to-CPU ratio for memory-intensive queries
      and large indexes. Supports all features including high availability.

    Note

    Some features require specific compute families. For example, high availability (`HIGH_AVAILABILITY = TRUE`)
    is only available on STANDARD and HIGHMEM instances, not on BURST instances.

`STORAGE_SIZE_GB = storage_gb`
:   Specifies the storage size in GB. Must be between 10 and 65,535.

    Storage is billed separately from compute based on the allocated amount. You can increase or decrease storage size later
    using ALTER POSTGRES INSTANCE. For more information about costs, see [Snowflake Postgres Cost Evaluation](/user-guide/snowflake-postgres/postgres-cost).

    Note

    When you decrease the storage size, you can’t set it too close to current disk usage. The new size must be
    at least 1.4x the disk space currently in use. That way, there’s still room to add more data without
    triggering an automatic storage increase.

`AUTHENTICATION_AUTHORITY = { POSTGRES | POSTGRES_OR_SNOWFLAKE }`
:   Specifies the authentication method for the instance. POSTGRES indicates that only Postgres user passwords can be used.
    POSTGRES\_OR\_SNOWFLAKE also allows the use of short-lived access token passwords. See
    [Snowflake Token Authentication for Snowflake Postgres](/user-guide/snowflake-postgres/postgres-token-auth) for more details.

## Optional parameters

`POSTGRES_VERSION = { 16 | 17 | 18 }`
:   Specifies the major version of Postgres to use.

    While the latest version includes new features and improvements, you might choose an earlier version for application
    compatibility or to match existing instances. You can upgrade to a newer version later using ALTER POSTGRES INSTANCE.

    Default: The latest Postgres version.

`NETWORK_POLICY = 'network_policy'`
:   Specifies the [network policy](/user-guide/snowflake-postgres/postgres-network) to use for the instance.
    To specify this parameter, you must have been granted the USAGE privilege on the network policy object.

    Default: No network policy is applied.

    Important

    Without a network policy, the instance can’t accept incoming connections. You can still view the instance
    using SHOW and DESCRIBE commands, but can’t connect to the Postgres database until you attach a network
    policy using ALTER POSTGRES INSTANCE.

`STORAGE_INTEGRATION = 'storage_integration_name'`
:   Attaches a storage integration of type `POSTGRES_EXTERNAL_STORAGE` to the Postgres instance,
    enabling the pg\_lake extension to access data in external object storage. For the complete setup
    procedure, see [pg\_lake](/user-guide/snowflake-postgres/postgres-pg_lake).

    You can also attach or remove a storage integration later using [ALTER POSTGRES INSTANCE](/sql-reference/sql/alter-postgres-instance).

    [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

    Default: No storage integration is attached.

`HIGH_AVAILABILITY = { TRUE | FALSE }`
:   Specifies whether to enable [high availability](/user-guide/snowflake-postgres/high-availability) for the instance.

    High availability provisions a standby instance in a separate availability zone for automatic failover. This minimizes
    downtime if the primary becomes unavailable. Without HA, recovery requires restoring from backup, which can take hours
    for large or active instances. Note that enabling or disabling HA later using ALTER POSTGRES INSTANCE requires a
    [maintenance operation](/user-guide/snowflake-postgres/managing-instances).

    Important

    Burstable instance sizes (BURST\_S, BURST\_M) do not support high availability.

    Default: `FALSE`

`POSTGRES_SETTINGS = 'json_string'`
:   Specifies custom [Postgres server settings](/user-guide/snowflake-postgres/postgres-server-settings) for the instance
    in JSON format:

    Copy code

    ```
    '{"component:name" = "value", ...}'
    ```

    The format uses `component:name` where `component` is either `postgres` (for PostgreSQL server settings) or
    `pgbouncer` (for connection pooler settings). For example:

    Copy code

    ```
    '{"postgres:work_mem" = "128MB", "pgbouncer:default_pool_size" = "200"}'
    ```

    See [Snowflake Postgres Server Settings](/user-guide/snowflake-postgres/postgres-server-settings) for available settings.

    Default: No custom Postgres configuration parameters are set.

`COMMENT = 'string_literal'`
:   Specifies a comment for the Postgres instance.

    Comments are useful for documenting the purpose or ownership of an instance, such as “Production instance for billing
    service” or “QA environment for team X”. Unlike tags, comments are free-form text and not used for organization or
    cost tracking.

    Default: No value.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

## Fork parameters

Forking a Snowflake Postgres instance creates an identical copy with all the same
schema objects and table data. You can also specify a point in time so that the forked
instance reflects a previous state of the instance. That way, you can recover from data
integrity issues such as accidentally dropping objects. You can also explore scenarios
in a development and test environment, such as trying different instance configurations
with identical data. For more information, see
[Snowflake Postgres point-in-time recovery](/user-guide/snowflake-postgres/postgres-point-in-time-recovery).

`FORK source_instance`
:   Creates a new instance as a fork (copy) of the specified source instance. To create a fork of a given source instance, you mush be granted
    the OWNERSHIP privilege on it.

`{ AT | BEFORE } ( { TIMESTAMP => timestamp | OFFSET => time_difference } )`
:   Specifies the point in time to fork from. You can’t fork from a point in time more than 10 days
    in the past. The timestamp or offset must fall within the 10-day Postgres data retention period.

    The [AT | BEFORE](/sql-reference/constructs/at-before) clause accepts one of the following parameters:

    `TIMESTAMP => timestamp`
    :   Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a
        TIMESTAMP, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, or TIMESTAMP\_TZ data type.

    `OFFSET => time_difference`
    :   Specifies the difference in seconds from the current time, in the form `-N` where `N`
        can be an integer or arithmetic expression (for example, `-120` is 120 seconds, `-30*60` is 30 minutes).

    Default: Uses the current time.

When creating a fork, the following parameters are optional and default to the values from the source instance:

- `COMPUTE_FAMILY`
- `STORAGE_SIZE_GB`
- `HIGH_AVAILABILITY`
- `POSTGRES_SETTINGS`

## Output

When you create a new instance, the command returns one row with the following columns:

| Column | Description |
| --- | --- |
| `status` | Status of the create operation. |
| `host` | Hostname for connecting to the instance. |
| `access_roles` | User names and passwords for the `snowflake_admin` and `application` roles. |
| `default_database` | Default database for the instance. |

Expand

Show lessSee more

Important

The `access_roles` column contains credentials that you can’t retrieve later. Save these details in a secure location.

When you create a fork, the command returns one row with only `status` and `host` columns. The fork uses
the same credentials that the source instance had, at the point in time that the fork corresponds to.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE POSTGRES INSTANCE | Account | By default, only the ACCOUNTADMIN role has this privilege. |
| OWNERSHIP | Postgres instances | Required on existing instance to create a fork of it. |
| USAGE | Network policy | Required only if specifying a NETWORK\_POLICY. |
| USAGE | Storage integration | Required only if specifying a STORAGE\_INTEGRATION. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Creating a new instance takes some time to complete. The instance displays its current
  [state](#instance-states) while it’s being built. You can use the DESC POSTGRES INSTANCE
  command to track the status during the instance setup.
- When you create a fork, you don’t specify or see the credentials. That’s because the fork uses
  the same credentials that the source instance had, at the point in time that the fork corresponds
  to. You can regenerate credentials for the forked instance later, if you need to provide access to
  a different set of users than on the original instance.
- The time needed to create a fork depends on the amount of data in the source instance. Larger databases with more
  data take longer to fork. The compute family (instance size) of the source doesn’t significantly affect fork duration.
- Forking performs a complete data copy using backup and write-ahead log (WAL) replay, which means
  that the forked instance is entirely separate: dropping the source instance does not affect any
  forks that you created from it.

  Note

  Postgres forking isn’t part of the Snowflake [Time Travel](/user-guide/data-time-travel) feature, which uses
  zero-copy technology for tables. However, forking uses the same AT | BEFORE syntax to specify a point in time.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Create a basic Postgres instance:

Copy code

```
CREATE POSTGRES INSTANCE my_postgres
  COMPUTE_FAMILY = 'STANDARD_S'
  STORAGE_SIZE_GB = 50
  AUTHENTICATION_AUTHORITY = POSTGRES;
```

Create a Postgres instance with high availability and a network policy:

Copy code

```
CREATE POSTGRES INSTANCE prod_postgres
  COMPUTE_FAMILY = 'STANDARD_M'
  STORAGE_SIZE_GB = 500
  AUTHENTICATION_AUTHORITY = POSTGRES
  POSTGRES_VERSION = 17
  HIGH_AVAILABILITY = TRUE
  NETWORK_POLICY = 'my_network_policy'
  COMMENT = 'Production Postgres instance';
```

Create an instance and configure a network policy later:

Copy code

```
-- Step 1: Create instance without network policy
CREATE POSTGRES INSTANCE my_postgres
  COMPUTE_FAMILY = 'STANDARD_S'
  STORAGE_SIZE_GB = 50
  AUTHENTICATION_AUTHORITY = POSTGRES;

-- Step 2: Monitor instance creation
DESCRIBE POSTGRES INSTANCE my_postgres
  ->> SELECT "property", "value"
      FROM $1
      WHERE "property" IN ('name', 'state', 'host');

-- Step 3: Once READY, attach network policy to enable connections
ALTER POSTGRES INSTANCE my_postgres
  SET NETWORK_POLICY = 'my_network_policy';

-- Step 4: Now you can connect to the Postgres database using the host and credentials
-- from the CREATE output
```

Create a fork of an existing instance:

Copy code

```
CREATE POSTGRES INSTANCE my_fork
  FORK my_source_instance;
```

Create a fork at a specific point in time:

Copy code

```
CREATE POSTGRES INSTANCE my_fork
  FORK my_source_instance
  AT (TIMESTAMP => '2025-01-15 12:00:00'::TIMESTAMP_NTZ);
```

Create a fork from 2 hours ago with a different instance size:

Copy code

```
CREATE POSTGRES INSTANCE my_fork
  FORK my_source_instance
  AT (OFFSET => -7200)
  COMPUTE_FAMILY = 'STANDARD_L';
```

Create a fork for reporting with a larger instance size and different storage:

Copy code

```
-- Fork production instance for reporting workload
CREATE POSTGRES INSTANCE reporting_instance
  FORK prod_instance
  COMPUTE_FAMILY = 'HIGHMEM_XL'
  STORAGE_SIZE_GB = 500
  COMMENT = 'Dedicated reporting instance to offload analytics queries';
```

Create a fork at midnight UTC for daily testing:

Copy code

```
-- Fork at start of day (midnight UTC)
CREATE POSTGRES INSTANCE daily_test_instance
  FORK prod_instance
  AT (TIMESTAMP => '2026-02-05 00:00:00'::TIMESTAMP_NTZ);
```

Create a development fork with HA disabled to reduce costs:

Copy code

```
CREATE POSTGRES INSTANCE dev_instance
  FORK prod_instance
  COMPUTE_FAMILY = 'STANDARD_S'
  STORAGE_SIZE_GB = 100
  HIGH_AVAILABILITY = FALSE
  COMMENT = 'Development environment from prod data';
```

Recover from accidental data deletion using a fork from before the incident:

Copy code

```
-- Recover by forking from 30 minutes ago
CREATE POSTGRES INSTANCE recovered_instance
  FORK damaged_instance
  AT (OFFSET => -1800)
  COMMENT = 'Recovery fork from before data deletion';
```
