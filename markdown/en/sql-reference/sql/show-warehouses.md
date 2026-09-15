# SHOW WAREHOUSES

Lists all the [virtual warehouses](/user-guide/warehouses-overview) in your account for which you have access privileges.

See also:
:   [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) , [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse) , [DESCRIBE WAREHOUSE](/sql-reference/sql/desc-warehouse) , [DROP WAREHOUSE](/sql-reference/sql/drop-warehouse)

## Syntax

Copy code

```
SHOW WAREHOUSES
  [ LIKE '<pattern>' ]
  [ WITH PRIVILEGES <objectPrivilege> [ , <objectPrivilege> [ , ... ] ] ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`WITH PRIVILEGES object_privilege [ , object_privilege [ , ... ] ]`
:   Optionally limits rows to objects for which the [active role](/user-guide/security-access-control-overview#label-access-control-overview-active-roles) for the current
    user has been granted all of the specified privileges in the list on the object.

    If a CREATE <object> privilege is included in the privileges list, the command excludes objects for which secondary roles have
    been granted privileges. This is because only the primary role has the authorization to create objects. For more information, see
    [Authorization through primary role and secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement).

## Output

The columns in the output provide the following information. For accounts that have the [query acceleration service](/user-guide/query-acceleration-service) feature enabled, the output provides additional information.

> | Column | Description |
> | --- | --- |
> | `name` | Name of the warehouse. |
> | `state` | Whether the warehouse is:  active/running (`STARTED`), inactive (`SUSPENDED`), or resizing (`RESIZING`). |
> | `type` | Warehouse type. STANDARD and SNOWPARK-OPTIMIZED are the only currently supported types. |
> | `size` | Size of the warehouse (X-Small, Small, Medium, Large, X-Large, etc.) |
> | `min_cluster_count` | Minimum number of clusters for the (multi-cluster) warehouse (always 1 for single-cluster warehouses). |
> | `max_cluster_count` | Maximum number of clusters for the (multi-cluster) warehouse (always 1 for single-cluster warehouses). |
> | `started_clusters` | Number of clusters currently started. |
> | `running` | Number of SQL statements that are being executed by the warehouse. |
> | `queued` | Number of SQL statements that are queued for the warehouse. |
> | `is_default` | Whether the warehouse is the default for the current user. |
> | `is_current` | Whether the warehouse is in use for the session.  Only one warehouse can be in use at a time for a session. To specify or change the warehouse for a session, use the [USE WAREHOUSE](/sql-reference/sql/use-warehouse) command. |
> | `is_interactive` | Whether the warehouse is an [interactive warehouse](/user-guide/interactive) (`Y`) or not (`N`). Currently, the interactive warehouse feature is only available on Amazon Web Services (AWS). |
> | `auto_suspend` | Period of inactivity, in seconds, after which a running warehouse will automatically suspend and stop using credits.  A value of `null` indicates the warehouse never automatically suspends. |
> | `auto_resume` | Whether the warehouse, if suspended, automatically resumes when a query is submitted to the warehouse. |
> | `available` | Percentage of the warehouse compute resources that are provisioned and available. |
> | `provisioning` | Percentage of the warehouse compute resources that are in the process of provisioning. |
> | `quiescing` | Percentage of the warehouse compute resources that are executing SQL statements, but will be shut down once the queries complete. |
> | `other` | Percentage of the warehouse compute resources that are in a state other than `available`, `provisioning`, or `quiescing`. |
> | `created_on` | Date and time when the warehouse was created. |
> | `resumed_on` | Date and time when the warehouse was last started or restarted. |
> | `updated_on` | Date and time when the warehouse was last updated, which includes changing any of the properties of the warehouse or changing the state (`STARTED`, `SUSPENDED`, `RESIZING`) of the warehouse. |
> | `owner` | Role that owns the warehouse. |
> | `comment` | Comment for the warehouse. |
> | `enable_query_acceleration` | Whether the [query acceleration service](/user-guide/query-acceleration-service) is enabled for the warehouse. |
> | `query_acceleration_max_scale_factor` | [Maximum scale factor](/sql-reference/sql/create-warehouse#label-query-acceleration-max-scale-factor) for the query acceleration service. |
> | `resource_monitor` | ID of [resource monitor](/user-guide/resource-monitors) explicitly assigned to the warehouse; controls the monthly credit usage for the warehouse. |
> | `actives` , `pendings` , `failed` , `suspended` , `uuid` | These five columns are for internal use and will be removed in a future release. |
> | `scaling_policy` | Policy that determines when additional clusters (in a multi-cluster warehouse) are automatically started and shut down. |
> | `owner_role_type` | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
> | `resource_constraint` | If type is `SNOWPARK-OPTIMIZED`, one of:   - `MEMORY_1X`, `MEMORY_1X_x86`, `MEMORY_16X`, `MEMORY_16X_x86`, `MEMORY_64X`, `MEMORY_64X_x86`.   Otherwise `NULL`. |
> | `generation` | The [generation](/user-guide/warehouses-gen2) type of the warehouse. |
>
> Expand
>
> Show lessSee more

For more information about the properties that can be specified for a warehouse, see [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse).

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

Show warehouses with names that start with `test` that you have privileges to view:

Copy code

```
SHOW WAREHOUSES LIKE 'test%';
```

```
+---------------+-----------+--------------------+---------+-------------------+-------------------+------------------+---------+--------+------------+------------+--------------+-------------+-----------+--------------+-----------+-------+-------------------------------+-------------------------------+-------------------------------+--------------+---------+---------------------------+-------------------------------------+------------------+---------+----------+--------+-----------+----------+----------------+------------------+--------------------+
| name          | state     | type               | size    | min_cluster_count | max_cluster_count | started_clusters | running | queued | is_default | is_current | auto_suspend | auto_resume | available | provisioning | quiescing | other | created_on                    | resumed_on                    | updated_on                    | owner        | comment | enable_query_acceleration | query_acceleration_max_scale_factor | resource_monitor | actives | pendings | failed | suspended | uuid     | scaling_policy | owner_role_type | resource_constraint | generation |
|---------------+-----------+--------------------+---------+-------------------+-------------------+------------------+---------+--------+------------+------------+--------------+-------------+-----------+--------------+-----------+-------+-------------------------------+-------------------------------+-------------------------------+--------------+---------+---------------------------+-------------------------------------+------------------+---------+----------+--------+-----------+----------+----------------------------------|---------------------+
| TEST1         | SUSPENDED | STANDARD           | Medium  |                 1 |                 1 |                0 |       0 |      0 | N          | N          |          600 | true        |           |              |           |       | 2023-01-27 14:57:07.768 -0800 | 2023-05-10 16:17:49.258 -0700 | 2023-05-10 16:17:49.258 -0700 | MY_ROLE      |         | true                      |                                   8 | null             |       0 |        0 |      0 |         4 | 76064    | STANDARD       | ROLE            | NULL  | 1                 +
| TEST2         | SUSPENDED | STANDARD           | X-Small |                 1 |                 1 |                0 |       0 |      0 | N          | N          |          600 | true        |           |              |           |       | 2023-01-27 14:57:07.953 -0800 | 1969-12-31 16:00:00.000 -0800 | 2023-01-27 14:57:08.356 -0800 | MY_ROLE      |         | true                      |                                  16 | MYTEST_RM        |       0 |        0 |      0 |         1 | 76116    | STANDARD       |  ROLE           | NULL  | 2                 +
| TEST3         | SUSPENDED | STANDARD           | Small   |                 1 |                 1 |                0 |       0 |      0 | N          | N          |          600 | true        |           |              |           |       | 2023-08-08 10:26:45.534 -0700 | 2023-08-08 10:26:45.681 -0700 | 2023-08-08 10:26:45.681 -0700 | MY_ROLE      |         | false                     |                                   8 | null             |       0 |        0 |      0 |         2 | 19464517 | STANDARD       | ROLE            | NULL   | NULL             +
| TEST4         | RESUMING  | SNOWPARK-OPTIMIZED | Large   |                 1 |                 1 |                0 |       0 |      0 | N          | Y          |          600 | true        |           |              |           |       | 2023-09-21 17:29:58.165 -0700 | 2023-09-21 17:29:58.165 -0700 | 2023-09-21 17:29:58.207 -0700 | MY_ROLE      |         | false                     |                                   8 | null             |       0 |        0 |      0 |         0 | 19464585 | STANDARD       | ROLE            | MEMORY_16X_X86 | NULL             +
+---------------+-----------+--------------------+---------+-------------------+-------------------+------------------+---------+--------+------------+------------+--------------+-------------+-----------+--------------+-----------+-------+-------------------------------+-------------------------------+-------------------------------+--------------+---------+---------------------------+-------------------------------------+------------------+---------+----------+--------+-----------+----------+----------------+-----------------+---------------------+
```

Show warehouses that you have been granted the MODIFY and OPERATE privileges on:

Copy code

```
SHOW WAREHOUSES WITH PRIVILEGES MODIFY, OPERATE;
```

```
+------------------------------+-----------+----------+---------+-------------------+-------------------+------------------+---------+--------+------------+------------+--------------+-------------+-----------+--------------+-----------+-------+-------------------------------+-------------------------------+-------------------------------+--------------+-------------------------------------------------+---------------------------+-------------------------------------+------------------+---------+----------+--------+-----------+----------+----------------+-----------------+---------------------+
| name                         | state     | type     | size    | min_cluster_count | max_cluster_count | started_clusters | running | queued | is_default | is_current | auto_suspend | auto_resume | available | provisioning | quiescing | other | created_on                    | resumed_on                    | updated_on                    | owner        | comment                                         | enable_query_acceleration | query_acceleration_max_scale_factor | resource_monitor | actives | pendings | failed | suspended | uuid     | scaling_policy | owner_role_type |
|------------------------------+-----------+----------+---------+-------------------+-------------------+------------------+---------+--------+------------+------------+--------------+-------------+-----------+--------------+-----------+-------+-------------------------------+-------------------------------+-------------------------------+--------------+-------------------------------------------------+---------------------------+-------------------------------------+------------------+---------+----------+--------+-----------+----------+----------------+-----------------+---------------------+
| TEST_WH                      | SUSPENDED | STANDARD | X-Small |                 1 |                 1 |                0 |       0 |      0 | Y          | Y          |          600 | true        |           |              |           |       | 2023-01-27 14:57:07.768 -0800 | 2024-07-30 13:39:24.118 -0700 | 2024-07-30 13:39:24.118 -0700 | TEST_ROLE    |                                                 | true                      |                                  32 | TEST_RM          |       0 |        0 |      0 |         1 | 76056    | STANDARD       | ROLE            | NULL                +
| SNOWPARK_DEMO                | SUSPENDED | STANDARD | X-Large |                 1 |                 1 |                0 |       0 |      0 | N          | N          |          600 | true        |           |              |           |       | 2023-01-27 14:57:07.903 -0800 | 2023-04-10 11:47:03.146 -0700 | 2023-04-10 11:47:03.146 -0700 | ACCOUNTADMIN | Created by straut for Snowpark quickstart       | false                     |                                   8 | null             |       0 |        0 |      0 |        16 | 76104    | STANDARD       | ROLE            | NULL                +
| TASTY_DEV_WH                 | SUSPENDED | STANDARD | X-Small |                 1 |                 1 |                0 |       0 |      0 | N          | N          |           60 | true        |           |              |           |       | 2023-10-25 16:25:43.681 -0700 | 2023-10-25 16:25:43.681 -0700 | 2023-10-25 16:25:43.711 -0700 | SYSADMIN     | developer warehouse for tasty bytes             | false                     |                                   8 | null             |       0 |        0 |      0 |         1 | 19464633 | STANDARD       | ROLE            | NULL                +
| TB_DOCS_WH                   | SUSPENDED | STANDARD | X-Small |                 1 |                 1 |                0 |       0 |      0 | N          | N          |           60 | true        |           |              |           |       | 2024-07-24 15:02:32.172 -0700 | 2024-07-24 15:33:30.502 -0700 | 2024-07-24 15:33:30.502 -0700 | SYSADMIN     | developer warehouse for tasty bytes             | false                     |                                   8 | null             |       0 |        0 |      0 |         1 | 19465097 | STANDARD       | ROLE            | NULL                +
+------------------------------+-----------+----------+---------+-------------------+-------------------+------------------+---------+--------+------------+------------+--------------+-------------+-----------+--------------+-----------+-------+-------------------------------+-------------------------------+-------------------------------+--------------+-------------------------------------------------+---------------------------+-------------------------------------+------------------+---------+----------+--------+-----------+----------+----------------+-----------------+---------------------+
```

Show certain details about warehouses by filtering and reordering data from the full SHOW WAREHOUSES output.
This stored procedure runs a SHOW WAREHOUSES command, then calls the [RESULT\_SCAN](/sql-reference/functions/result_scan) function to filter and transform
the result set from the most recent SQL command. You can use this technique to generate different types of reports
if you don’t need the entire output of a SHOW command.

Copy code

```
CREATE OR REPLACE PROCEDURE started_and_suspended_warehouses()
  RETURNS TABLE(name VARCHAR, status VARCHAR, type VARCHAR, size VARCHAR)
  LANGUAGE SQL
  AS
  $$
    DECLARE
      res RESULTSET;
    BEGIN
      SHOW WAREHOUSES;
      res := (SELECT "name" name, "state" state, "type" type, "size" size
        FROM TABLE(RESULT_SCAN(LAST_QUERY_ID(-1)))
        WHERE "state" IN ('STARTED','SUSPENDED')
        ORDER BY "state", "name");
      RETURN TABLE(res);
    END;
  $$
  ;

CALL started_and_suspended_warehouses();
```

```
+------------------------------+-----------+--------------------+---------+
| NAME                         | STATUS    | TYPE               | SIZE    |
|------------------------------+-----------+--------------------+---------|
| COMPUTE_WH                   | STARTED   | STANDARD           | X-Small |
| DEFAULT_SIZE                 | SUSPENDED | STANDARD           | Small   |
| DEFAULT_SIZE_2               | SUSPENDED | STANDARD           | X-Small |
| MEDIUM                       | SUSPENDED | SNOWPARK-OPTIMIZED | Medium  |
| PRIV_WH                      | SUSPENDED | STANDARD           | X-Small |
| SYSTEM$STREAMLIT_NOTEBOOK_WH | SUSPENDED | STANDARD           | X-Small |
| XSMALL                       | SUSPENDED | STANDARD           | Medium  |
+------------------------------+-----------+--------------------+---------+
```
