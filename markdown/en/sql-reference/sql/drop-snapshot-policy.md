# DROP SNAPSHOT POLICY — *Deprecated*

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The DROP SNAPSHOT POLICY command is deprecated. See [DROP BACKUP POLICY](/sql-reference/sql/drop-backup-policy).

Deletes a [snapshot](/user-guide/backups) policy.

See also:
:   [CREATE SNAPSHOT POLICY — Deprecated](/sql-reference/sql/create-snapshot-policy),
    [ALTER SNAPSHOT POLICY — Deprecated](/sql-reference/sql/alter-snapshot-policy),
    [SHOW SNAPSHOT POLICIES — Deprecated](/sql-reference/sql/show-snapshot-policies)

## Syntax

Copy code

```
DROP SNAPSHOT POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the snapshot policy.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Snapshot policy | The role used to delete a snapshot policy must have the OWNERSHIP privilege on the policy. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

A snapshot policy can’t be deleted if it is attached to any snapshot set.

## Examples

Delete the snapshot policy `hourly_snapshot_policy`:

Copy code

```
DROP SNAPSHOT POLICY hourly_snapshot_policy;
```
