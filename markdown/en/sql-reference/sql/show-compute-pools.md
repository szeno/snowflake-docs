# SHOW COMPUTE POOLS

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Lists the [compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool) in your account for which you have access privileges.

See also:
:   [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) , [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool), [DESCRIBE COMPUTE POOL](/sql-reference/sql/desc-compute-pool) , [DROP COMPUTE POOL](/sql-reference/sql/drop-compute-pool) , [SHOW NODES IN COMPUTE POOL](/sql-reference/sql/show-nodes-compute-pool)

## Syntax

Copy code

```
SHOW COMPUTE POOLS [ LIKE '<pattern>' ]
                   [ STARTS WITH '<name_string>' ]
                   [ LIMIT <ROWS> [ FROM '<name-string>' ] ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows [ FROM 'name_string' ]`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
    specified number of rows following the first row whose object name matches the specified string:

    - The string must be enclosed in single quotes and is case sensitive.
    - The string does not have to include the full object name; partial names are supported.

    Default: No value (no limit is applied to the output)

    Note

    For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
    both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
    returned.

    In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
    lexicographic value than the rows returned by `STARTS WITH 'name_string'`.

    For example:

    - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
    - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
    - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any one of these privileges: OWNERSHIP, USAGE, MONITOR, or OPERATE | Compute pool |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

The command output provides compute pool properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Compute pool name. |
| `state` | State of the compute pool. For more information, see [Compute pool lifecycle](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-lifecycle). |
| `min_nodes` | Minimum number of nodes in the compute pool. |
| `max_nodes` | Maximum number of nodes in the compute pool. |
| `instance_family` | Machine type of nodes in the compute pool. |
| `num_services` | Number of services running on the compute pool. |
| `num_jobs` | Number of jobs running on the compute pool. |
| `auto_suspend_secs` | Number of seconds of inactivity after which Snowflake automatically suspends the compute pool. |
| `auto_resume` | Whether to automatically resume a compute pool when Snowflake starts a service or job. |
| `active_nodes` | Number of nodes in the compute pool that are active (one or more services or jobs are running). |
| `idle_nodes` | Number of nodes in the compute pool that are idle (no service or job is running). |
| `target_nodes` | Indicates the number of nodes that Snowflake is targeting for your compute pool. If `active_nodes` isn’t equal to the `target_nodes`, Snowflake autoscales the cluster to add or remove the nodes. For more information, see [About the target\_nodes compute pool property](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-about-target-nodes). |
| `created_on` | Date and time when the compute pool was created. |
| `resumed_on` | Date and time when the suspended compute pool was resumed. |
| `updated_on` | Date and time when the compute pool was updated using ALTER COMPUTE POOL. |
| `owner` | Role that owns the compute pool. |
| `comment` | Specifies a comment for the compute pool. |
| `is_exclusive` | `true` if the compute pool is created exclusively for a Snowflake Native App; `false` otherwise. |
| `application` | Name of the Snowflake Native App if the compute pool is created exclusively for the app. Otherwise, NULL. |
| `placement_group` | Specifies the fault domain into which the compute pool nodes are placed. A fault domain is similar to the cloud provider’s availability zone. For more information, see [Compute pool placement](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-placement-group). |
| `backup_instance_families` | This column is in [public preview](/release-notes/preview-features). Ordered list of backup instance families configured for the compute pool; the order determines fallback priority. NULL if no backup families are configured. For more information, see [backup instance types](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-backup-instance-types). |

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

## Examples

The following command lists the compute pools for which you have access privileges in the current account:

Copy code

```
SHOW COMPUTE POOLS;
```

The following command lists one compute pool:

Copy code

```
SHOW COMPUTE POOLS LIMIT 1;
```

The following command lists compute pools with names containing “tu”:

Copy code

```
SHOW COMPUTE POOLS LIKE '%tu%';
```

The following command lists two compute pools with names containing “my\_pool”:

Copy code

```
SHOW COMPUTE POOLS LIKE '%my_pool%' LIMIT 2;
```

Sample output:

```
+-------------------------+-----------+-----------+-----------+-----------------+--------------+----------+-------------------+-------------+--------------+------------+--------------+-------------------------------+-------------------------------+-------------------------------+--------------+---------+--------------+-------------+-----------------+--------------------------+
| name                    | state     | min_nodes | max_nodes | instance_family | num_services | num_jobs | auto_suspend_secs | auto_resume | active_nodes | idle_nodes | target_nodes | created_on                    | resumed_on                    | updated_on                    | owner        | comment | is_exclusive | application | placement_group | backup_instance_families |
|-------------------------+-----------+-----------+-----------+-----------------+--------------+----------+-------------------+-------------+--------------+------------+--------------+-------------------------------+-------------------------------+-------------------------------+--------------+---------+--------------+-------------+-----------------+--------------------------+
| TUTORIAL_COMPUTE_POOL   | ACTIVE    |         1 |         1 | CPU_X64_XS      |            3 |        0 |              3600 | true        |            1 |          0 |            1 | 2024-02-24 20:41:31.978 -0800 | 2024-08-08 11:27:01.775 -0700 | 2024-08-18 13:47:08.150 -0700 | TEST_ROLE    | NULL    | false        | NULL        | A               | NULL                     |
| TUTORIAL_COMPUTE_POOL_2 | SUSPENDED |         1 |         1 | CPU_X64_XS      |            0 |        0 |              3600 | true        |            0 |          0 |            0 | 2024-01-15 21:23:09.744 -0800 | 2024-04-06 15:24:50.541 -0700 | 2024-08-18 13:46:08.110 -0700 | ACCOUNTADMIN | NULL    | false        | NULL        | NULL            | NULL                     |
+-------------------------+-----------+-----------+-----------+-----------------+--------------+----------+-------------------+-------------+--------------+------------+--------------+-------------------------------+-------------------------------+-------------------------------+--------------+---------+--------------+-------------+-----------------+--------------------------+
```
