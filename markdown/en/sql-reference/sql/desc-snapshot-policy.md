# DESCRIBE SNAPSHOT POLICY

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Describes a specific [snapshot policy](/user-guide/backups).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE SNAPSHOT POLICY — Deprecated](/sql-reference/sql/create-snapshot-policy),
    [ALTER SNAPSHOT POLICY — Deprecated](/sql-reference/sql/alter-snapshot-policy),
    [DROP SNAPSHOT POLICY — Deprecated](/sql-reference/sql/drop-snapshot-policy),
    [SHOW SNAPSHOT POLICIES — Deprecated](/sql-reference/sql/show-snapshot-policies)

## Syntax

Copy code

```
DESC[RIBE] SNAPSHOT POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the snapshot policy to describe. If the identifier contains spaces or special characters, the entire
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

The snapshot policy is an object that’s inside a specific schema and database. Therefore, the policy
gets replicated, dropped or undropped, and so on, when those operations are performed on the schema and database
that contain it. If you can’t drop the snapshot policy because it’s associated with any snapshot sets,
then you also can’t drop the schema or database containing the policy.

To determine whether a snapshot policy is associated with any snapshot sets, use the SHOW SNAPSHOT SETS command.

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

Describe a snapshot policy:

Copy code

```
DESC SNAPSHOT POLICY my_snapshot_policy;
```
