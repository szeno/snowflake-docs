# CREATE COMPUTE POOL

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Creates a new [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool) in the current account.

See also:
:   [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool) , [DESCRIBE COMPUTE POOL](/sql-reference/sql/desc-compute-pool), [DROP COMPUTE POOL](/sql-reference/sql/drop-compute-pool) , [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools) , [SHOW NODES IN COMPUTE POOL](/sql-reference/sql/show-nodes-compute-pool)

## Syntax

Copy code

```
CREATE COMPUTE POOL [ IF NOT EXISTS ] <name>
  [ FOR APPLICATION <app-name> ]
  MIN_NODES = <num>
  MAX_NODES = <num>
  INSTANCE_FAMILY = <instance_family_name>
  [ AUTO_RESUME = { TRUE | FALSE } ]
  [ INITIALLY_SUSPENDED = { TRUE | FALSE } ]
  [ AUTO_SUSPEND_SECS = <num>  ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ COMMENT = '<string_literal>' ]
  [ PLACEMENT_GROUP = '<placement_group_name>' ]
  [ BACKUP_INSTANCE_FAMILIES = ( '<instance_family_name>' [ , '<instance_family_name>' ... ] ) ]
```

## Required parameters

`name`
:   String that specifies the identifier (that is, the name) for the compute pool; it must be unique for your account. Quoted names for special characters or case-sensitive names are not supported.

`MIN_NODES = num`
:   Specifies the minimum number of nodes for the compute pool. This value must be greater than 0. For more information, see
    [Creating a compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-creating-compute-pool).

`MAX_NODES = num`
:   Specifies the maximum number of nodes for the compute pool.

`INSTANCE_FAMILY = instance_family_name`
:   Identifies the type of machine you want to provision for the nodes in the compute pool. The machine type determines the amount
    of compute resources in the compute pool and, therefore, the number of credits consumed while the compute pool is running.

    For a complete list of available instance families organized by cloud provider, see
    [Instance Families](/developer-guide/snowpark-container-services/instance-families).
    You can also use [SHOW COMPUTE POOL INSTANCE FAMILIES](/sql-reference/sql/show-compute-pool-instance-families)
    to retrieve current availability and specifications programmatically.

## Optional parameters

`FOR APPLICATION app_name`
:   Specifies the Snowflake Native App name. If specified, the compute pool can only be used by the native app. The [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools) command output includes the `is_exclusive` and `application` columns to indicate whether the compute pool is created exclusively for an app and provides the app name.

`AUTO_RESUME = { TRUE | FALSE }`
:   Specifies whether to automatically resume a compute pool when a service or job is submitted to it.

    - If AUTO\_RESUME is FALSE, you need to explicitly resume the compute pool (using ALTER COMPUTE POOL RESUME) before you can
      start a service or job on the compute pool.
    - If AUTO\_RESUME is TRUE, if you start a new service on a suspended compute pool, Snowflake starts the compute pool. Similarly,
      when you use a service either by invoking a service function or accessing ingress (see
      [Using a service](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating)), Snowflake starts the previously suspended compute pool and resumes
      the service.

    Default: TRUE

`INITIALLY_SUSPENDED = { TRUE | FALSE }`
:   Specifies whether the compute pool is created initially in the suspended state. If you create a compute pool with
    INITIALLY\_SUSPENDED set to TRUE, Snowflake will not provision any nodes requested for the compute pool at the compute pool
    creation time. You can start the suspended compute pool using [ALTER COMPUTE POOL … RESUME](/sql-reference/sql/alter-compute-pool).

    Default: FALSE

`AUTO_SUSPEND_SECS = num`
:   Number of seconds of inactivity after which you want Snowflake to automatically suspend the compute pool. An inactive compute
    pool is one in which no services or jobs are currently active on any node in the pool. If `auto_suspend_secs` is set to 0,
    Snowflake does not suspend the compute pool automatically.

    Default: 3600 seconds

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`COMMENT = 'string_literal'`
:   Specifies a comment for the compute pool.

    Default: No value

`PLACEMENT_GROUP = placement_group_name`
:   Identifies the placement group of the compute pool. Use the [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools)
    and [DESCRIBE COMPUTE POOL](/sql-reference/sql/desc-compute-pool)
    commands to review the assignment of the compute pool into placement groups.

    You can also set `placement_group` to `DISTRIBUTED`. In this case, Snowflake attempts to distribute compute pool nodes across all available placement groups to maintain an even distribution across multiple placement groups so that the groups are more fault tolerant. For more information, see [Compute pool placement](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-placement-group).

[Preview Feature — Open](/release-notes/preview-features)

Backup instance types for compute pools is a [preview feature](/release-notes/preview-features) available to all accounts.

`BACKUP_INSTANCE_FAMILIES = ( 'instance_family_name' [ , ... ] )`
:   An ordered list of instance families to use as fallbacks when the primary `INSTANCE_FAMILY` cannot be provisioned due to an insufficient capacity error (ICE). Snowflake always attempts the primary family first, then tries each backup family in the order you specify.

    The list must contain at least one entry, must not include the primary `INSTANCE_FAMILY` or duplicates, and must use valid instance family identifiers.

    Snowflake does not validate workload compatibility. Before specifying a backup family, verify:

    - **Resources**: equal or greater per-node vCPU, memory, and local NVMe storage than the primary.
    - **Accelerator class** (GPU pools only): same type as the primary. A CPU family cannot run GPU workloads; a GPU backup must have equal or better GPU memory and generation.
    - **Hardware features**: same network and placement capabilities your services require, such as EFA or placement groups.
    - **CPU architecture**: same instruction set as the primary. x86\_64 container images do not run on ARM nodes, and vice versa.
    - **Service density**: the backup family must support the `MAX_INSTANCES_PER_NODE` your services are configured to use.

    When choosing backup families, a reliable starting point is to use the next-larger size within the same family. For example, `GEN_X64_G2_8` is a sound backup for a `GEN_X64_G2_4` primary because it shares the same architecture, network capabilities, and local storage ratios while providing more vCPU and memory headroom.

    For more information, see [Backup instance types](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-backup-instance-types).

    Default: None

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE COMPUTE POOL | Account |  |

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

Create a 1-node compute pool. This example command specifies the minimum required parameters:

Copy code

```
CREATE COMPUTE POOL tutorial_compute_pool
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_XS;
```

The following command specifies the optional AUTO\_RESUME parameter:

Copy code

```
CREATE COMPUTE POOL tutorial_compute_pool
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_XS
  AUTO_RESUME = FALSE;
```

The following command creates a compute pool with backup instance families. If `GEN_X64_G2_4` is capacity-constrained, Snowflake automatically tries `GEN_X64_G2_8`, then `GEN_X64_G2_16`:

Copy code

```
CREATE COMPUTE POOL my_compute_pool
  MIN_NODES = 1
  MAX_NODES = 10
  INSTANCE_FAMILY = GEN_X64_G2_4
  BACKUP_INSTANCE_FAMILIES = ('GEN_X64_G2_8', 'GEN_X64_G2_16');
```
