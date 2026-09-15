# DESCRIBE SNAPSHOT SET

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Describes a specific [snapshot set](/user-guide/backups).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE SNAPSHOT SET — Deprecated](/sql-reference/sql/create-snapshot-set),
    [ALTER SNAPSHOT SET — Deprecated](/sql-reference/sql/alter-snapshot-set),
    [DROP SNAPSHOT SET — Deprecated](/sql-reference/sql/drop-snapshot-set),
    [SHOW SNAPSHOT SETS — Deprecated](/sql-reference/sql/show-snapshot-sets)

## Syntax

Copy code

```
DESC[RIBE] SNAPSHOT SET <name>
```

## Parameters

`name`
:   Specifies the identifier for the snapshot set to describe. If the identifier contains spaces or special characters, the entire
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
| `created_on` | Timestamp that the snapshot set was created. |
| `name` | Name of the snapshot set. |
| `database_name` | Name of the database that contains the snapshot set. |
| `schema_name` | Name of the schema that contains the snapshot set. |
| `object_kind` | Type of the object that the snapshot set is snapshotting. |
| `object_name` | Name of the object that the snapshot set is snapshotting. |
| `object_database_name` | Name of the database that contains the object being snapshotted by this snapshot set. |
| `object_schema_name` | Name of the schema that contains the object being snapshotted by this snapshot set. |
| `snapshot_policy_name` | Name of the snapshot policy attached to this snapshot set. |
| `snapshot_policy_database_name` | Name of the database that contains the snapshot policy. |
| `snapshot_policy_schema_name` | Name of the schema that contains the snapshot policy. |
| `snapshot_policy_state` | Current state of the snapshot policy. |
| `owner_role` | Name of the role with the OWNERSHIP privilege on the snapshot set. |
| `owner_role_type` | Type of role with the OWNERSHIP privilege on the snapshot set. |
| `comment` | Comment for backup set. |

Expand

Show lessSee more

## Examples

Describe a snapshot set:

Copy code

```
DESC SNAPSHOT SET my_snapshot_set;
```
