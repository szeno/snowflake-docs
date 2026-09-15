# DESCRIBE BACKUP SET

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Describes a specific [backup set](/user-guide/backups).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE BACKUP SET](/sql-reference/sql/create-backup-set),
    [ALTER BACKUP SET](/sql-reference/sql/alter-backup-set),
    [DROP BACKUP SET](/sql-reference/sql/drop-backup-set),
    [SHOW BACKUP SETS](/sql-reference/sql/show-backup-sets)

## Syntax

Copy code

```
DESC[RIBE] BACKUP SET <name>
```

## Parameters

`name`
:   Specifies the identifier for the backup set to describe. If the identifier contains spaces or special characters, the entire
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

## Output

| Column | Description |
| --- | --- |
| `created_on` | Timestamp that the backup set was created. |
| `name` | Name of the backup set. |
| `database_name` | Name of the database that contains the backup set. |
| `schema_name` | Name of the schema that contains the backup set. |
| `object_kind` | Type of the object that the backup set is backing up. |
| `object_name` | Name of the object that the backup set is backing up. |
| `object_database_name` | Name of the database that contains the object being backed up by this backup set. |
| `object_schema_name` | Name of the schema that contains the object being backed up by this backup set. |
| `backup_policy_name` | Name of the backup policy attached to this backup set. |
| `backup_policy_database_name` | Name of the database that contains the backup policy. |
| `backup_policy_schema_name` | Name of the schema that contains the backup policy. |
| `backup_policy_state` | Current state of the backup policy. |
| `owner_role` | Name of the role with the OWNERSHIP privilege on the backup set. |
| `owner_role_type` | Type of role with the OWNERSHIP privilege on the backup set. |
| `comment` | Comment for backup set. |

Expand

Show lessSee more

## Examples

Describe a backup set:

Copy code

```
DESC BACKUP SET my_backup_set;
```
