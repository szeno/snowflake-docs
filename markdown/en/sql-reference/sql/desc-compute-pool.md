# DESCRIBE COMPUTE POOL

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Describes the properties of a [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) , [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool), [DROP COMPUTE POOL](/sql-reference/sql/drop-compute-pool) , [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools)

## Syntax

Copy code

```
DESC[RIBE] COMPUTE POOL <name>
```

## Parameters

`name`
:   Specifies the identifier for the compute pool to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The command output provides compute pool properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Compute pool name. |
| `state` | Current state of the compute pool. |
| `min_nodes` | Minimum number of nodes in the compute pool. |
| `max_nodes` | Maximum number of nodes in the compute pool. |
| `instance_family` | Specifies the machine type of nodes in the compute pool. |
| `num_services` | The number of services and jobs running on the compute pool. |
| `num_jobs` | Number of jobs running on the compute pool. |
| `auto_suspend_secs` | Specifies the number of seconds of inactivity after which the compute pool is automatically suspended. |
| `auto_resume` | Specifies whether to automatically resume a compute pool when Snowflake attempts to start a service or job. |
| `active_nodes` | Number of nodes in the compute pool that are active (one or more services or jobs are running). |
| `idle_nodes` | Number of nodes in the compute pool that are idle (no service or job is running). |
| `target_nodes` | Indicates the number of nodes that Snowflake is targeting for your compute pool. If `active_nodes` isn’t equal to the `target_nodes`, Snowflake autoscales the cluster to add or remove the nodes. For more information, see [About the target\_nodes compute pool property](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-about-target-nodes). |
| `placement_group` | Specifies the fault domain into which the compute pool nodes are placed. A fault domain is similar to the cloud provider’s availability zone. For more information, see [Compute pool placement](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-placement-group). |
| `created_on` | Date and time when the compute pool was created. |
| `resumed_on` | Date and time when the suspended compute pool was resumed. |
| `updated_on` | Date and time when the compute pool was updated using ALTER COMPUTE POOL. |
| `owner` | Role that owns the compute pool. |
| `comment` | Specifies a comment for the compute pool. |
| `is_exclusive` | `true` if the compute pool is created exclusively for a Snowflake Native App; `false` otherwise. |
| `application` | Name of the Snowflake Native App if the compute pool is created exclusively for the app. Otherwise, NULL. |
| `budget` | The name of the [budget](/user-guide/budgets) monitoring the credit usage of the compute pool. |
| `error_code` | Error code, if any, relevant to the STATUS\_MESSAGE. Otherwise, this field is empty. For example, when you resize a compute pool:   - If Snowflake encounters a capacity error (new nodes can’t be provisioned), Snowflake returns the error code 392507.   Note that the capacity error indicates the instance type you requested for your compute pool node is currently not available with the cloud provider. You can either wait for the capacity to become available or create a new compute pool with a different instance family.   - If you have pending services (including job services) and Snowflake can’t scale up your compute pool, Snowflake returns the error code 392508. |
| `status_message` | Optional message about the status of the compute pool. For example:   - After creating a compute pool, if you run the DESC COMPUTE POOL command, the output might include the status message: “Compute pool is starting for last 1 minute”. - If Snowflake encounters a capacity error when provisioning a node, the output might include the status message: “Compute pool is   starting for the last 3 minutes. We have observed CAPACITY\_ERROR.” - If you have pending services (including job services) and Snowflake can’t scale up your compute pool, the output might include   the status message: “Compute pool has reached the maximum node limit. Consider increasing max\_nodes using the ALTER COMPUTE POOL command.” |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MONITOR | Compute pool |  |

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

## Examples

The following example describes the compute pool named `tutorial_compute_pool`:

Copy code

```
DESCRIBE COMPUTE POOL tutorial_compute_pool;
```

Sample output:

```
+-----------------------+--------+-----------+-----------+-----------------+--------------+----------+-------------------+-------------+--------------+------------+--------------+-------------------------------+-------------------------------+-------------------------------+-----------+---------+--------------+-------------+--------+------------+----------------+-----------------+
| name                  | state  | min_nodes | max_nodes | instance_family | num_services | num_jobs | auto_suspend_secs | auto_resume | active_nodes | idle_nodes | target_nodes | created_on                    | resumed_on                    | updated_on                    | owner     | comment | is_exclusive | application | budget | error_code | status_message | placement_group |
|-----------------------+--------+-----------+-----------+-----------------+--------------+----------+-------------------+-------------+--------------+------------+--------------+-------------------------------+-------------------------------+-------------------------------+-----------+---------+--------------+-------------+--------+------------+----------------+-----------------|
| TUTORIAL_COMPUTE_POOL | ACTIVE |         1 |         1 | CPU_X64_XS      |            3 |        0 |              3600 | true        |            1 |          0 |            1 | 2024-02-24 20:41:31.978 -0800 | 2024-08-08 11:27:01.775 -0700 | 2024-08-18 13:29:08.124 -0700 | TEST_ROLE | NULL    | false        | NULL        | NULL   |            |                |      A          |
+-----------------------+--------+-----------+-----------+-----------------+--------------+----------+-------------------+-------------+--------------+------------+--------------+-------------------------------+-------------------------------+-------------------------------+-----------+---------+--------------+-------------+--------+------------+----------------+-----------------+
```
