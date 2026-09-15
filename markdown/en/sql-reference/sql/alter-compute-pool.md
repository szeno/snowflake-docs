# ALTER COMPUTE POOL

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Modifies the properties of an existing
[compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool).

See also:
:   [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) , [DESCRIBE COMPUTE POOL](/sql-reference/sql/desc-compute-pool), [DROP COMPUTE POOL](/sql-reference/sql/drop-compute-pool) , [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools) , [SHOW NODES IN COMPUTE POOL](/sql-reference/sql/show-nodes-compute-pool)

## Syntax

Copy code

```
ALTER COMPUTE POOL [ IF EXISTS ] <name> { SUSPEND | RESUME }

ALTER COMPUTE POOL [ IF EXISTS ] <name> STOP ALL  [ OF TYPE <workload_type> [ , ... ] ]

ALTER COMPUTE POOL [ IF EXISTS ] <name> SET [ MIN_NODES = <num> ]
                                            [ MAX_NODES = <num> ]
                                            [ AUTO_RESUME = { TRUE | FALSE } ]
                                            [ AUTO_SUSPEND_SECS = <num> ]
                                            [ PLACEMENT_GROUP = '<placement_group_name>' ]
                                            [ INSTANCE_FAMILY = <instance_family_name> ]
                                            [ BACKUP_INSTANCE_FAMILIES = ( '<instance_family_name>' [ , ... ] ) ]
                                            [ TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ]
                                            [ COMMENT = '<string_literal>' ]

ALTER COMPUTE POOL [ IF EXISTS ] <name> UNSET { AUTO_SUSPEND_SECS         |
                                                AUTO_RESUME               |
                                                PLACEMENT_GROUP           |
                                                BACKUP_INSTANCE_FAMILIES  |
                                                COMMENT
                                              }
                                              [ , ... ]
```

## Parameters

`name`
:   Specifies the identifier for the compute pool to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`{ SUSPEND | RESUME }`
:   Suspends a compute pool or resumes a previously suspended compute pool. When you suspend a compute pool, Snowflake suspends all services in that compute pool,
    but the jobs continue to run until they reach a terminal state (DONE or FAILED), after which the compute pool nodes are released.

`STOP ALL OF TYPE workload_type [ , ... ]`
:   Drops all services and cancels jobs executing in the compute pool. Snowflake then removes all the containers from the compute pool. If the optional `OF TYPE` clause is specified, Snowflake only stops the services of the specified workload types. For a list of available workload types, see [ALLOWED\_SPCS\_WORKLOAD\_TYPES](/sql-reference/parameters#label-allowed-spcs-workload-types).

    The filter is case-insensitive.

`SET ...`
:   Sets one or more specified properties or parameters for the compute pool:

    `MIN_NODES = num`
    :   Specifies the minimum number of compute pool nodes.

    `MAX_NODES = num`
    :   Specifies the maximum number of compute pool nodes.

    `AUTO_RESUME = { TRUE | FALSE }`
    :   Specifies whether to automatically resume a compute pool when a service or job is submitted to it. If AUTO\_RESUME is FALSE,
        you need to explicitly resume the compute pool (using ALTER COMPUTE POOL <name> RESUME) before you can start a service or
        job on the compute pool.

    `AUTO_SUSPEND_SECS = num`
    :   Number of seconds of inactivity after which you want Snowflake to automatically suspend the compute pool. Inactivity means
        no services and no jobs running on any node in the compute pool.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `PLACEMENT_GROUP = placement_group_name`
    :   Identifies the [placement group of the compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-placement-group). Use the [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools)
        and [DESCRIBE COMPUTE POOL](/sql-reference/sql/desc-compute-pool)
        commands to review the assignment of the compute pool into placement groups.

        You can also set `placement_group` to `DISTRIBUTED`. In this case, Snowflake attempts to distribute compute pool nodes across all available placement groups to maintain an even distribution across multiple placement groups so that the groups are more fault tolerant. For more information, see [Compute pool placement](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-placement-group).

    `INSTANCE_FAMILY = instance_family_name`
    :   Identifies the type of machine you want to provision for the nodes in the compute pool. The machine type determines the amount of compute resources in the compute pool and, therefore, the number of credits consumed while
        the compute pool is running. For a list of available instance family names, see [instance families](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pools-instance-family-table).

        INSTANCE\_FAMILY can be altered only when a compute pool is fully suspended. Upon resuming, Snowflake uses the new instance type to provision the compute pool.

    [Preview Feature — Open](/release-notes/preview-features)

    Backup instance types for compute pools is a [preview feature](/release-notes/preview-features) available to all accounts.

    `BACKUP_INSTANCE_FAMILIES = ( 'instance_family_name' [ , ... ] )`
    :   Sets or replaces the ordered list of backup instance families for the compute pool. The change takes effect immediately without requiring pool suspension or service restart; the next scale-up event uses the updated list. The list must contain at least one entry, must not include the primary `INSTANCE_FAMILY` or duplicates, and must use valid instance family identifiers.

        Snowflake does not validate workload compatibility. For compatibility requirements and selection guidance, see [BACKUP\_INSTANCE\_FAMILIES in CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool#label-create-compute-pool-backup-instance-families).

        Existing nodes running on a backup instance type are not affected immediately; they are replaced with primary-family nodes during a maintenance window or routine node retirement.

        If `INSTANCE_FAMILY` is also changed in the same `ALTER` statement, Snowflake re-validates that the new primary family is not present in the backup list and that all entries remain valid.

        For more information, see [Backup instance types](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-backup-instance-types).

    `COMMENT = 'string_literal'`
    :   Specifies a comment for the compute pool.

`UNSET ...`
:   Specifies one or more properties and/or parameters to unset for the compute pool,
    which resets them to the defaults. For more information, see
    [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool):

    - `AUTO_SUSPEND_SECS`
    - `AUTO_RESUME`
    - `PLACEMENT_GROUP`: The placement group can only be unset when the compute pool is fully suspended.
    - `BACKUP_INSTANCE_FAMILIES`: Returns the pool to single-family behavior. Snowflake no longer tries alternate instance types when the primary `INSTANCE_FAMILY` is constrained. Nodes already running on backup instance types continue until they are replaced through routine node retirement or a maintenance window.
    - `COMMENT`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OPERATE | Compute pool | To suspend or resume a compute pool, the role requires these permissions. |
| MODIFY | Compute pool | To alter the compute pool and set properties, the role requires this permission. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example sets the MAX\_NODES and AUTO\_RESUME properties for a compute pool:

Copy code

```
ALTER COMPUTE POOL tutorial_compute_pool SET
  MAX_NODES = 5
  AUTO_RESUME = FALSE
```

The following example sets the “CPU\_X64\_S” as the INSTANCE\_FAMILY for a compute pool. Because the compute pool must be stopped to change the instance family, the compute pool is first suspended:

Copy code

```
ALTER COMPUTE POOL tutorial_compute_pool SUSPEND;
ALTER COMPUTE POOL tutorial_compute_pool SET
  INSTANCE_FAMILY = CPU_X64_S;
ALTER COMPUTE POOL tutorial_compute_pool RESUME;
```

The following example configures backup instance families on an existing compute pool:

Copy code

```
ALTER COMPUTE POOL my_compute_pool
  SET BACKUP_INSTANCE_FAMILIES = ('GEN_X64_G2_8');
```

The following example removes all backup families, returning the pool to single-family behavior:

Copy code

```
ALTER COMPUTE POOL my_compute_pool
  UNSET BACKUP_INSTANCE_FAMILIES;
```
