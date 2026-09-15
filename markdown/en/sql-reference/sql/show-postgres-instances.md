# SHOW POSTGRES INSTANCES

Lists the [Snowflake Postgres instances](/user-guide/snowflake-postgres/about) for which you have access privileges.

See also:
:   [CREATE POSTGRES INSTANCE](/sql-reference/sql/create-postgres-instance), [ALTER POSTGRES INSTANCE](/sql-reference/sql/alter-postgres-instance), [DESCRIBE POSTGRES INSTANCE](/sql-reference/sql/desc-postgres-instance), [DROP POSTGRES INSTANCE](/sql-reference/sql/drop-postgres-instance)

## Syntax

Copy code

```
SHOW POSTGRES INSTANCES [ LIKE '<pattern>' ]
                        [ STARTS WITH '<name_string>' ]
                        [ LIMIT <rows> [ FROM '<name_string>' ] ]
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

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `name` | Name of the Postgres instance. |
| `owner` | Role that owns the Postgres instance. |
| `owner_role_type` | Type of the owner role (for example, ROLE or DATABASE\_ROLE). |
| `created_on` | Date and time when the Postgres instance was created. |
| `updated_on` | Date and time when the Postgres instance was last updated. |
| `type` | Type of the Postgres instance. |
| `origin` | Origin of the Postgres instance (for example, if forked from another instance). |
| `host` | Hostname used to connect to the Postgres instance. |
| `privatelink_service_identifier` | Identifier for the Private Link service, if Private Link is configured for the instance. |
| `compute_family` | [Compute family](/user-guide/snowflake-postgres/postgres-instance-sizes) (instance size) of the Postgres instance. |
| `authentication_authority` | Authentication method used for the instance (currently `POSTGRES`). |
| `storage_size` | Storage size allocated to the Postgres instance, in GB. |
| `postgres_version` | Major version of Postgres running on the instance. |
| `postgres_settings` | Custom [Postgres server settings](/user-guide/snowflake-postgres/postgres-server-settings) configured for the instance. |
| `is_ha` | Whether [high availability](/user-guide/snowflake-postgres/high-availability) is enabled for the instance. |
| `retention_time` | Data retention time for the instance. |
| `state` | Current [state](#instance-states) of the instance. Possible values: `CREATING`, `RESTORING`, `STARTING`, `REPLAYING`, `FINALIZING`, `READY`, `RESTARTING`, `RESUMING`, `SUSPENDING`, `SUSPENDED`. |
| `comment` | Comment for the Postgres instance. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OPERATE or OWNERSHIP | Postgres instance | Only instances for which you have one of these privileges appear in the output. |

Expand

Show lessSee more

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

- Use this command to monitor the state and configuration of your Postgres instances for capacity planning,
  troubleshooting, and auditing purposes.
- Common use cases include checking instance states during operations, identifying instances that need upgrades,
  and reviewing storage usage across your account.

## Examples

List all Postgres instances in the account:

Copy code

```
SHOW POSTGRES INSTANCES;
```

List Postgres instances with names starting with `prod`:

Copy code

```
SHOW POSTGRES INSTANCES STARTS WITH 'PROD';
```

List Postgres instances matching a pattern:

Copy code

```
SHOW POSTGRES INSTANCES LIKE 'DEV_%';
```

Use the [flow operator](/sql-reference/operators-flow) to filter and select specific columns:

Copy code

```
SHOW POSTGRES INSTANCES
  ->> SELECT "name", "state", "compute_family", "storage_size"
      FROM $1
      WHERE "state" = 'READY'
      ORDER BY "name";
```

Find all instances with high availability enabled:

Copy code

```
SHOW POSTGRES INSTANCES
  ->> SELECT "name", "compute_family", "is_ha", "postgres_version"
      FROM $1
      WHERE "is_ha" = 'true';
```

Get a summary of storage usage across all instances:

Copy code

```
SHOW POSTGRES INSTANCES
  ->> SELECT "name", "storage_size", "created_on"
      FROM $1
      WHERE "storage_size" > 100
      ORDER BY "storage_size" DESC;
```
