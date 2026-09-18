# SHOW NODES IN COMPUTE POOL

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Lists the nodes currently provisioned in a specified [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool), including the instance family backing each node. Use this command to see which primary or backup instance families are actually in use when [backup instance types](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-backup-instance-types) are configured for a pool.

See also:
:   [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) , [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool), [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools) , [SHOW COMPUTE POOL INSTANCE FAMILIES](/sql-reference/sql/show-compute-pool-instance-families)

## Syntax

Copy code

```
SHOW NODES IN COMPUTE POOL <name>
             [ LIKE '<pattern>' ]
             [ LIMIT <rows> ]
```

## Parameters

`name`
:   Name of the compute pool whose nodes you want to list. The name must identify an existing compute pool in the current account.

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Compute pool | None |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

The command returns one row for each node currently provisioned in the compute pool. The output includes the following columns:

| Column | Description |
| --- | --- |
| `node_id` | Unique identifier for the node in the compute pool. |
| `instance_family` | The actual instance family allocated for the node (for example, `GEN_X64_G2_4`, `GEN_X64_G2_8`). When backup instance types are configured and a fallback is active, this value may differ from the pool’s primary `INSTANCE_FAMILY`. |
| `created_on` | Date and time when the node was provisioned. |
| `placement_group` | The availability zone in which the node is provisioned. |
| `vcpu` | Number of vCPUs available to services on this node. |
| `memory_gib` | Memory in GiB available to services on this node. |
| `storage_gib` | Storage in GiB available to services on this node. |
| `gpu` | Name of the GPU on this node, if applicable. Otherwise, an empty string. |
| `gpu_count` | Number of GPUs on this node, if applicable. Otherwise, 0. |
| `gpu_memory_gib` | Total GPU memory available per instance in GiB, if applicable. Otherwise, 0. |

Expand

Show lessSee more

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

- If the compute pool is suspended, the command returns 0 rows.
- The output is a real-time snapshot of currently provisioned nodes. It does not include historical node data.

## Examples

The following command lists all nodes in a compute pool:

Copy code

```
SHOW NODES IN COMPUTE POOL my_compute_pool;
```

The following command lists up to 10 nodes:

Copy code

```
SHOW NODES IN COMPUTE POOL my_compute_pool LIMIT 10;
```

Sample output for a compute pool whose primary instance family is `GEN_X64_G2_4` and that has `GEN_X64_G2_8` configured as a backup. The third node (`node-11-07-198-03`) is running on the backup family because `GEN_X64_G2_4` was capacity-constrained when that node was provisioned:

```
+--------------------+-----------------+-------------------------------+-----------------+------+------------+-------------+-----+-----------+----------------+
| node_id            | instance_family | created_on                    | placement_group | vcpu | memory_gib | storage_gib | gpu | gpu_count | gpu_memory_gib |
|--------------------+-----------------+-------------------------------+-----------------+------+------------+-------------+-----+-----------+----------------|
| node-11-07-198-01  | GEN_X64_G2_4    | 2026-06-16 09:12:04.000 -0700 | us-west-2a      |    3 |         13 |       93.13 |     |         0 |              0 |
| node-11-07-198-02  | GEN_X64_G2_4    | 2026-06-16 09:12:04.000 -0700 | us-west-2a      |    3 |         13 |       93.13 |     |         0 |              0 |
| node-11-07-198-03  | GEN_X64_G2_8    | 2026-06-16 10:48:31.000 -0700 | us-west-2b      |    6 |         28 |      186.26 |     |         0 |              0 |
+--------------------+-----------------+-------------------------------+-----------------+------+------------+-------------+-----+-----------+----------------+
```
