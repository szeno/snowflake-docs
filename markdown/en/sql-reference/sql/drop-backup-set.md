# DROP BACKUP SET

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deletes a [backup](/user-guide/backups) set.

See also:
:   [CREATE BACKUP SET](/sql-reference/sql/create-backup-set),
    [ALTER BACKUP SET](/sql-reference/sql/alter-backup-set),
    [SHOW BACKUP SETS](/sql-reference/sql/show-backup-sets)

## Syntax

Copy code

```
DROP BACKUP SET <name>
```

## Parameters

`name`
:   Specifies the identifier for the backup set.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Backup set | The role used to modify the backup policy for a backup set must have the OWNERSHIP privilege on the set. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Important

If the backup policy has a retention lock applied to it, and there are any
unexpired backups in the backup set, then you can’t delete the backup set.
In that case, you must wait for all the backups in the set to expire.
This restriction applies even to privileged roles such as ACCOUNTADMIN, and to Snowflake support.
For that reason, be careful when specifying retention lock and a long expiration
period in a backup policy.

You also can’t drop a backup set if any of the backups it contains have a legal hold applied.

## Examples

Delete the backup set `t1_backups`:

Copy code

```
DROP BACKUP SET t1_backups;
```
