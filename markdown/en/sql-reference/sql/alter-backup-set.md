# ALTER BACKUP SET

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Modifies the properties for a [backup](/user-guide/backups) set.
This operation can be one of the following:

- Taking a new backup that becomes part of the backup set.
- Removing an old backup from the backup set.
- Suspending or resuming the scheduled backups and scheduled backup deletion
  that are specified by the backup policy.
- Applying a backup policy to a backup set that doesn’t already have a policy.
- Adding or removing a legal hold for a specific backup within the backup set.
- Renaming the backup set.
- Specifying or removing a comment for a specific backup within the backup set.
- Specifying or removing a comment for the backup set.

See also:
:   [CREATE BACKUP SET](/sql-reference/sql/create-backup-set),
    [DROP BACKUP SET](/sql-reference/sql/drop-backup-set),
    [SHOW BACKUP SETS](/sql-reference/sql/show-backup-sets)

## Syntax

Copy code

```
ALTER BACKUP SET <name> ADD BACKUP

ALTER BACKUP SET <name> APPLY BACKUP POLICY <policy_name> [ FORCE ]

ALTER BACKUP SET <name> SUSPEND BACKUP [ { CREATION | EXPIRATION } ] POLICY

ALTER BACKUP SET <name> RESUME BACKUP [ { CREATION | EXPIRATION } ] POLICY

ALTER BACKUP SET <name> DELETE BACKUP IDENTIFIER '<backup_id>'

ALTER BACKUP SET <name> MODIFY BACKUP IDENTIFIER '<backup_id>' { ADD | REMOVE } LEGAL HOLD

ALTER BACKUP SET <name> MODIFY BACKUP IDENTIFIER '<backup_id>' SET COMMENT = '<string_literal>'

ALTER BACKUP SET <name> MODIFY BACKUP IDENTIFIER '<backup_id>' UNSET COMMENT

ALTER BACKUP SET <name> RENAME TO <new_name>

ALTER BACKUP SET <name> SET COMMENT = '<string_literal>'

ALTER BACKUP SET <name> UNSET COMMENT

ALTER BACKUP SET <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER BACKUP SET <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Specifies the identifier for the backup set.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ADD BACKUP`
:   Manually create a backup in the set. If the backup policy doesn’t include a schedule for
    taking new backups, this is how you make a new backup of the table, schema, or database that’s
    included in the backup set. You can also make new backups in the backup set at any time even
    when backups happen on a regular schedule.

`APPLY BACKUP POLICY policy_name [ FORCE ]`
:   Specifies the backup policy to attach to the backup set.

    The FORCE option overwrites an existing policy on a backup set. You can only use this option if the old
    policy doesn’t have a retention lock.

    Important

    Applying a backup policy with a retention lock to a backup set is *irreversible*.
    Due to the strong guarantees that are needed for regulatory compliance, after you put a retention lock on a backup set,
    you can’t revoke the lock. Snowflake support also can’t revoke such a retention lock. Plan carefully before
    you set a retention lock on a backup set with a long expiration period, to avoid unexpected storage charges
    for undeletable backup sets, and the schemas and databases that contain them.

    If a Snowflake organization is deleted, the organization is no longer a Snowflake customer. In this case,
    Snowflake deletes all backups, including those with retention locks. Deleting a Snowflake organization
    requires the involvement of Snowflake support. It isn’t something that an administrator can do by accident.

`SUSPEND BACKUP [ { CREATION | EXPIRATION } ] POLICY`
:   Suspend a backup policy in the backup set.
    You can suspend the entire backup policy, or only creation or expiration operations.
    When you specify SUSPEND BACKUP POLICY without the CREATION or EXPIRATION keywords, Snowflake
    suspends both the creation and expiration aspects of the policy.
    For more information, see [Suspend a backup policy on a backup set](/user-guide/backups#label-suspending-a-backup-policy-on-a-backup).

`RESUME BACKUP [ { CREATION | EXPIRATION } ] POLICY`
:   Resume a suspended backup policy in the set.
    You can resume the entire backup policy, or only creation or expiration operations.
    When you specify RESUME BACKUP POLICY without the CREATION or EXPIRATION keywords, Snowflake
    resumes both the creation and expiration aspects of the policy.
    For more information, see [Resume a backup policy on a backup set](/user-guide/backups#label-resuming-a-backup-policy-on-a-backup).

`DELETE BACKUP IDENTIFIER 'backup_id'`
:   Delete a backup in the backup set by ID.
    The backup ID is a UUID value, in the format returned by
    the [UUID\_STRING](/sql-reference/functions/uuid_string) function.
    Snowflake only allows deleting the oldest backup from the backup set.
    For more information, see [Delete a backup from a backup set](/user-guide/backups#label-deleting-a-backup).

`MODIFY BACKUP IDENTIFIER 'backup_id' { ADD | REMOVE } LEGAL HOLD`
:   Adds or removes a legal hold from a specified backup within the backup set.
    For more information about legal holds for WORM backups, see [Legal hold](/user-guide/backups#label-snapshots-concept-legal-hold).
    For examples of using this clause, see [Add and remove legal holds](/user-guide/backups#label-adding-removing-backup-legal-hold).

`MODIFY BACKUP IDENTIFIER 'backup_id' SET COMMENT = 'string_literal'`
:   Associates a comment with a specific backup within the backup set.

`MODIFY BACKUP IDENTIFIER 'backup_id' UNSET COMMENT`
:   Removes the comment from a specific backup within the backup set.

`RENAME TO new_name`
:   Specifies a new identifier for the backup set; must be unique for your account.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET COMMENT = 'string_literal'`
:   Associate a comment with the backup set.

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies one (or more) properties and/or parameters to unset for the backup set, which resets them to the defaults:

    - `property_name`
    - `param_name`
      - `COMMENT`
      - `TAG tag_name [ , tag_name ... ]`

    You can reset multiple properties/parameters with a single ALTER statement; however, each
    property/parameter must be separated by a comma. Also, when resetting a
    property/parameter, you only specify the name; no value is required.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Description |
| --- | --- |
| OWNERSHIP | The role used to modify a backup set must have the OWNERSHIP privilege on the backup set. |
| APPLY BACKUP RETENTION LOCK | If the backup policy includes a retention lock, the owner role of the backup set must have this privilege on the account. |
| APPLY LEGAL HOLD | This account privilege grants the ability to add or remove a legal hold from a backup. This privilege is only needed for the ADD LEGAL HOLD and REMOVE LEGAL HOLD clauses. By default, the ACCOUNTADMIN role has this privilege. |
| APPLY | The owner role of the backup set must have this privilege on the backup policy, either directly or through the role hierarchy. |

Expand

Show lessSee more

APPLY on the backup policy and APPLY BACKUP RETENTION LOCK on the account must
be granted to the owner role of the backup set (that is, the role that holds
OWNERSHIP of the backup set), either directly or indirectly through role
hierarchy inheritance. Background snapshot creation jobs run under the backup
set’s owner role, so that role must be able to use the policy after it is
applied.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

Important

If the backup policy has a retention lock applied to it, and there are any
unexpired backups in the backup set, then you can’t delete the backup set.
In that case, you must wait for all the backups in the set to expire.
This restriction applies even to privileged roles such as ACCOUNTADMIN, and to Snowflake support.
For that reason, be careful when specifying retention lock and a long expiration
period in a backup policy.

## Examples

Manually add a backup to backup set `t1_backups`:

Copy code

```
ALTER BACKUP SET t1_backups
  ADD BACKUP;
```

Update the backup policy for backup set `t1_backups`:

Copy code

```
ALTER BACKUP SET t1_backups
  APPLY BACKUP POLICY daily_backup_policy;
```

Suspend a backup policy on the backup set `t1_backup`:

Copy code

```
ALTER BACKUP SET t1_backups
  SUSPEND BACKUP POLICY;
```

Resume a backup policy on the backup set `t1_backups`:

Copy code

```
ALTER BACKUP SET t1_backups
  RESUME BACKUP POLICY;
```

Rename the backup set `t1_backups` to `table1_backups`:

Copy code

```
ALTER BACKUP SET t1_backups
  RENAME TO table1_backups;
```

To find the backup identifier to use with the ADD LEGAL HOLD
and REMOVE LEGAL HOLD clauses, you typically use the SHOW BACKUPS
command to list the eligible backups and their creation times.
The following example shows how you might list the appropriate
backups, add a legal hold to one specific backup, and later
remove that legal hold. Substitute your own role name, backup set name,
and backup identifier.

Copy code

```
USE ROLE my_legal_hold_role; -- use a role that has the APPLY LEGAL HOLD privilege
SHOW BACKUPS IN BACKUP SET my_db_backup_set
  ->> SELECT "created_on", "backup_id" FROM $1 WHERE "is_under_legal_hold" = 'N';
ALTER BACKUP SET my_db_backup_set
  MODIFY BACKUP IDENTIFIER '790d1ee4-88b2-451f-9ccc-eacd1e93a134'
  ADD LEGAL HOLD;

USE ROLE my_legal_hold_role; -- use a role that has the APPLY LEGAL HOLD privilege
SHOW BACKUPS IN BACKUP SET my_db_backup_set
  ->> SELECT "created_on", "backup_id" FROM $1 WHERE "is_under_legal_hold" = 'Y';
ALTER BACKUP SET my_db_backup_set
  MODIFY BACKUP IDENTIFIER '790d1ee4-88b2-451f-9ccc-eacd1e93a134'
  REMOVE LEGAL HOLD;
```

To add or remove a comment for a specific backup, use the backup identifier.
The following example finds a backup identifier, adds a comment, and then removes
the comment from the same backup:

Copy code

```
SHOW BACKUPS IN BACKUP SET my_db_backup_set
  ->> SELECT "created_on", "backup_id" FROM $1
        ORDER BY "created_on" DESC LIMIT 1;

ALTER BACKUP SET my_db_backup_set
  MODIFY BACKUP IDENTIFIER '790d1ee4-88b2-451f-9ccc-eacd1e93a134'
  SET COMMENT = 'Database state after CI/CD deployment at git commit 8f201bf.';

ALTER BACKUP SET my_db_backup_set
  MODIFY BACKUP IDENTIFIER '790d1ee4-88b2-451f-9ccc-eacd1e93a134'
  UNSET COMMENT;
```
