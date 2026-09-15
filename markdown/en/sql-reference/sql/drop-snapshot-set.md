# DROP SNAPSHOT SET — *Deprecated*

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The DROP SNAPSHOT SET command is deprecated. See [DROP BACKUP SET](/sql-reference/sql/drop-backup-set).

Deletes a [snapshot](/user-guide/backups) set.

See also:
:   [CREATE SNAPSHOT SET — Deprecated](/sql-reference/sql/create-snapshot-set),
    [ALTER SNAPSHOT SET — Deprecated](/sql-reference/sql/alter-snapshot-set),
    [SHOW SNAPSHOT SETS — Deprecated](/sql-reference/sql/show-snapshot-sets)

## Syntax

Copy code

```
DROP SNAPSHOT SET <name>
```

## Parameters

`name`
:   Specifies the identifier for the snapshot set.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Snapshot set | The role used to modify the snapshot policy for a snapshot set must have the OWNERSHIP privilege on the set. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Important

If the snapshot policy has a retention lock applied to it, and there are any
unexpired snapshots in the snapshot set, then you can’t delete the snapshot set.
In that case, you must wait for all the snapshots in the set to expire.
This restriction applies even to privileged roles such as ACCOUNTADMIN, and to Snowflake support.
For that reason, be careful when specifying retention lock and a long expiration
period in a snapshot policy.

You also can’t drop a snapshot set if any of the snapshots it contains have a legal hold applied.

## Examples

Delete the snapshot set `t1_snapshots`:

Copy code

```
DROP SNAPSHOT SET t1_snapshots;
```
