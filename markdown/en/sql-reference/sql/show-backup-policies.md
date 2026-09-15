# SHOW BACKUP POLICIES

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Lists all the [backup](/user-guide/backups) policies in your account for which you have access privileges.

See also:
:   [CREATE BACKUP POLICY](/sql-reference/sql/create-backup-policy),
    [ALTER BACKUP POLICY](/sql-reference/sql/alter-backup-policy),
    [DROP BACKUP POLICY](/sql-reference/sql/drop-backup-policy)

## Syntax

Copy code

```
SHOW BACKUP POLICIES
   [ LIKE '<pattern>' ]
   [ IN { ACCOUNT | DATABASE | DATABASE <db_name> | SCHEMA | SCHEMA <schema_name> }
     [ STARTS WITH '<name_string>' ]
     [ LIMIT <rows> ]
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

`LIMIT rows`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output)

## Usage notes

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

To determine whether a backup policy is associated with any backup sets, use the SHOW BACKUP SETS command.

Note

The backup policy is an object that’s inside a specific schema and database. Therefore, the policy
gets replicated, dropped or undropped, and so on, when those operations are performed on the schema and database
that contain it. If you can’t drop the backup policy because it’s associated with any backup sets,
then you also can’t drop the schema or database containing the policy.

## Output

| Column | Description |
| --- | --- |
| `created_on` | Timestamp backup policy was created. |
| `name` | Name of backup policy. |
| `database_name` | Name of database that contains the backup policy. |
| `schema_name` | Name of schema that contains the backup policy. |
| `owner` | Name of the role with the OWNERSHIP privilege on the backup policy. |
| `comment` | Comment for backup policy. |
| `schedule` | Schedule for backup creation. |
| `expire_after_days` | Number of days after backup creation when backup expires. |
| `has_retention_lock` | Indicates whether the policy includes a retention lock.  `Y` if policy has retention lock; `N` otherwise.  For more information, see [Retention lock](/user-guide/backups#label-backups-concept-retention-lock). |
| `owner` | Name of the role with the OWNERSHIP privilege on the backup set. |
| `owner_role_type` | Type of role with the OWNERSHIP privilege on the backup policy. |

Expand

Show lessSee more

## Examples

List all backup policies you have privileges for in the current account:

Copy code

```
SHOW BACKUP POLICIES IN ACCOUNT;
```
