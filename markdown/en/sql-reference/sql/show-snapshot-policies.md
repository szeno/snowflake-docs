# SHOW SNAPSHOT POLICIES — *Deprecated*

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The SHOW SNAPSHOT POLICIES command is deprecated. See [SHOW BACKUP POLICIES](/sql-reference/sql/show-backup-policies).

Lists all the [snapshot](/user-guide/backups) policies in your account for which you have access privileges.

See also:
:   [CREATE SNAPSHOT POLICY — Deprecated](/sql-reference/sql/create-snapshot-policy),
    [ALTER SNAPSHOT POLICY — Deprecated](/sql-reference/sql/alter-snapshot-policy),
    [DROP SNAPSHOT POLICY — Deprecated](/sql-reference/sql/drop-snapshot-policy)

## Syntax

Copy code

```
SHOW SNAPSHOT POLICIES
   [ LIKE '<pattern>' ]
   [ IN { ACCOUNT | DATABASE | DATABASE <db_name> | SCHEMA | SCHEMA <schema_name> }
     [ STARTS WITH '<name_string>' ]
     [ LIMIT <rows> [ FROM '<name_string>' ]
   ]
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

    If you specify the keyword `ACCOUNT`, then the command retrieves records for all schemas in all databases
    of the current account.

    If you specify the keyword `DATABASE`, then:

    - If you specify a `db_name`, then the command retrieves records for all schemas of the specified database.
    - If you don’t specify a `db_name`, then:
      - If there is a current database, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and schemas in the account.

    If you specify the keyword `SCHEMA`, then:

    - If you specify a qualified schema name (for example, `my_database.my_schema`), then the command
      retrieves records for the specified database and schema.
    - If you specify an unqualified `schema_name`, then:

      - If there is a current database, then the command retrieves records for the specified schema in the current database.
      - If there is no current database, then the command displays the error
        `SQL compilation error: Object does not exist, or operation cannot be performed`.
    - If you don’t specify a `schema_name`, then:

      - If there is a current database, then:

        - If there is a current schema, then the command retrieves records for the current schema in the current database.
        - If there is no current schema, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and all schemas in the account.

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

## Usage notes

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

To determine whether a snapshot policy is associated with any snapshot sets, use the SHOW SNAPSHOT SETS command.

Note

The snapshot policy is an object that’s inside a specific schema and database. Therefore, the policy
gets replicated, dropped or undropped, and so on, when those operations are performed on the schema and database
that contain it. If you can’t drop the snapshot policy because it’s associated with any snapshot sets,
then you also can’t drop the schema or database containing the policy.

## Output

| Column | Description |
| --- | --- |
| `created_on` | Timestamp snapshot policy was created. |
| `name` | Name of snapshot policy. |
| `database_name` | Name of database that contains the snapshot policy. |
| `schema_name` | Name of schema that contains the snapshot policy. |
| `owner` | Name of the role with the OWNERSHIP privilege on the snapshot policy. |
| `comment` | Comment for snapshot policy. |
| `schedule` | Schedule for snapshot creation. |
| `expire_after_days` | Number of days after snapshot creation when snapshot expires. |
| `has_retention_lock` | Indicates whether the policy includes a retention lock.  `Y` if policy has retention lock; `N` otherwise.  For more information, see [Retention lock](/user-guide/backups#label-snapshots-concept-retention-lock). |
| `owner` | Name of the role with the OWNERSHIP privilege on the snapshot set. |
| `owner_role_type` | Type of role with the OWNERSHIP privilege on the snapshot policy. |

Expand

Show lessSee more

## Examples

List all snapshot policies you have privileges for in the current account:

Copy code

```
SHOW SNAPSHOT POLICIES IN ACCOUNT;
```
