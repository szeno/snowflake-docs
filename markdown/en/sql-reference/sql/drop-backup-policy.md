# DROP BACKUP POLICY

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deletes a [backup](/user-guide/backups) policy.

See also:
:   [CREATE BACKUP POLICY](/sql-reference/sql/create-backup-policy),
    [ALTER BACKUP POLICY](/sql-reference/sql/alter-backup-policy),
    [SHOW BACKUP POLICIES](/sql-reference/sql/show-backup-policies)

## Syntax

Copy code

```
DROP BACKUP POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the backup policy.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Backup policy | The role used to delete a backup policy must have the OWNERSHIP privilege on the policy. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

A backup policy can’t be deleted if it is attached to any backup set.

## Examples

Delete the backup policy `hourly_backup_policy`:

Copy code

```
DROP BACKUP POLICY hourly_backup_policy;
```
