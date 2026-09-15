# DESCRIBE BACKUP POLICY

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Describes a specific [backup policy](/user-guide/backups).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE BACKUP POLICY](/sql-reference/sql/create-backup-policy),
    [ALTER BACKUP POLICY](/sql-reference/sql/alter-backup-policy),
    [DROP BACKUP POLICY](/sql-reference/sql/drop-backup-policy),
    [SHOW BACKUP POLICIES](/sql-reference/sql/show-backup-policies)

## Syntax

Copy code

```
DESC[RIBE] BACKUP POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the backup policy to describe. If the identifier contains spaces or special characters, the entire
    string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

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

Note

The backup policy is an object that’s inside a specific schema and database. Therefore, the policy
gets replicated, dropped or undropped, and so on, when those operations are performed on the schema and database
that contain it. If you can’t drop the backup policy because it’s associated with any backup sets,
then you also can’t drop the schema or database containing the policy.

To determine whether a backup policy is associated with any backup sets, use the SHOW BACKUP SETS command.

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

Describe a backup policy:

Copy code

```
DESC BACKUP POLICY my_backup_policy;
```
