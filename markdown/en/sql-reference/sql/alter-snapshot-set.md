# ALTER SNAPSHOT SET — *Deprecated*

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The ALTER SNAPSHOT SET command is deprecated. See [ALTER BACKUP SET](/sql-reference/sql/alter-backup-set).

Modifies the properties for a [snapshot](/user-guide/backups) set.
This operation can be one of the following:

- Taking a new backup that becomes part of the snapshot set.
- Removing an old backup from the snapshot set.
- Suspending or resuming the scheduled backups and scheduled snapshot deletion
  that are specified by the snapshot policy.
- Applying a snapshot policy to a snapshot set that doesn’t already have a policy.
- Adding or removing a legal hold for a specific snapshot within the snapshot set.
- Specifying or removing a comment for a specific snapshot within the snapshot set.
- Specifying or removing a comment for the snapshot set.

See also:
:   [CREATE SNAPSHOT SET — Deprecated](/sql-reference/sql/create-snapshot-set),
    [DROP SNAPSHOT SET — Deprecated](/sql-reference/sql/drop-snapshot-set),
    [SHOW SNAPSHOT SETS — Deprecated](/sql-reference/sql/show-snapshot-sets)

## Syntax

Copy code

```
ALTER SNAPSHOT SET <name> ADD SNAPSHOT

ALTER SNAPSHOT SET <name> APPLY SNAPSHOT POLICY <policy_name> [ FORCE ]

ALTER SNAPSHOT SET <name> SUSPEND SNAPSHOT [ { CREATION | EXPIRATION } ] POLICY

ALTER SNAPSHOT SET <name> RESUME SNAPSHOT [ { CREATION | EXPIRATION } ] POLICY

ALTER SNAPSHOT SET <name> DELETE SNAPSHOT IDENTIFIER '<snapshot_id>'

ALTER SNAPSHOT SET <name> MODIFY SNAPSHOT IDENTIFIER '<snapshot_id>' { ADD | REMOVE } LEGAL HOLD

ALTER SNAPSHOT SET <name> MODIFY SNAPSHOT IDENTIFIER '<snapshot_id>' SET COMMENT = '<string_literal>'

ALTER SNAPSHOT SET <name> MODIFY SNAPSHOT IDENTIFIER '<snapshot_id>' UNSET COMMENT

ALTER SNAPSHOT SET <name> SET COMMENT = '<string_literal>'

ALTER SNAPSHOT SET <name> UNSET COMMENT

ALTER SNAPSHOT SET <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER SNAPSHOT SET <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Specifies the identifier for the snapshot set.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ADD SNAPSHOT`
:   Manually create a snapshot in the set. If the snapshot policy doesn’t include a schedule for
    taking new backups, this is how you make a new backup of the table, schema, or database that’s
    included in the snapshot set. You can also make new backups in the snapshot set at any time even
    when backups happen on a regular schedule.

`APPLY SNAPSHOT POLICY policy_name [ FORCE ]`
:   Specifies the snapshot policy to attach to the snapshot set.

    The FORCE option overwrites an existing policy on a snapshot set. You can only use this option if the old
    policy doesn’t have a retention lock.

    Important

    Applying a snapshot policy with a retention lock to a snapshot set is *irreversible*.
    Due to the strong guarantees that are needed for regulatory compliance, after you put a retention lock on a snapshot set,
    you can’t revoke the lock. Snowflake support also can’t revoke such a retention lock. Plan carefully before
    you set a retention lock on a snapshot set with a long expiration period, to avoid unexpected storage charges
    for undeletable snapshot sets, and the schemas and databases that contain them.

    If a Snowflake organization is deleted, the organization is no longer a Snowflake customer. In this case,
    Snowflake deletes all snapshots, including those with retention locks. Deleting a Snowflake organization
    requires the involvement of Snowflake support. It isn’t something that an administrator can do by accident.

`SUSPEND SNAPSHOT [ { CREATION | EXPIRATION } ] POLICY`
:   Suspend a snapshot policy in the snapshot set.
    You can suspend the entire snapshot policy, or only creation or expiration operations.
    When you specify SUSPEND SNAPSHOT POLICY without the CREATION or EXPIRATION keywords, Snowflake
    suspends both the creation and expiration aspects of the policy.
    For more information, see [Suspend a backup policy on a backup set](/user-guide/backups#label-suspending-a-snapshot-policy-on-a-snapshot).

`RESUME SNAPSHOT [ { CREATION | EXPIRATION } ] POLICY`
:   Resume a suspended snapshot policy in the set.
    You can resume the entire snapshot policy, or only creation or expiration operations.
    When you specify RESUME SNAPSHOT POLICY without the CREATION or EXPIRATION keywords, Snowflake
    resumes both the creation and expiration aspects of the policy.
    For more information, see [Resume a backup policy on a backup set](/user-guide/backups#label-resuming-a-snapshot-policy-on-a-snapshot).

`DELETE SNAPSHOT IDENTIFIER 'snapshot_id'`
:   Delete a snapshot in the snapshot set by ID.
    The snapshot ID is a UUID value, in the format returned by
    the [UUID\_STRING](/sql-reference/functions/uuid_string) function.
    Snowflake only allows deleting the oldest snapshot from the snapshot set.
    For more information, see [Delete a backup from a backup set](/user-guide/backups#label-deleting-a-snapshot).

`MODIFY SNAPSHOT IDENTIFIER 'snapshot_id' { ADD | REMOVE } LEGAL HOLD`
:   Adds or removes a legal hold from a specified snapshot within the snapshot set.
    For more information about legal holds for WORM snapshots, see [Legal hold](/user-guide/backups#label-snapshots-concept-legal-hold).
    For examples of using this clause, see [Add and remove legal holds](/user-guide/backups#label-adding-removing-snapshot-legal-hold).

`MODIFY SNAPSHOT IDENTIFIER 'snapshot_id' SET COMMENT = 'string_literal'`
:   Associates a comment with a specific snapshot within the snapshot set.

`MODIFY SNAPSHOT IDENTIFIER 'snapshot_id' UNSET COMMENT`
:   Removes the comment from a specific snapshot within the snapshot set.

`SET COMMENT = 'string_literal'`
:   Associate a comment with the snapshot set.

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies one (or more) properties and/or parameters to unset for the snapshot set, which resets them to the defaults:

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
| OWNERSHIP | The role used to modify a snapshot set must have the OWNERSHIP privilege on the snapshot set. |
| APPLY SNAPSHOT RETENTION LOCK | If the snapshot policy applied to a snapshot set includes a retention lock, the role used to apply the policy must have this privilege on the account. |
| APPLY LEGAL HOLD | This account privilege grants the ability to add or remove a legal hold from a snapshot. This privilege is only needed for the ADD LEGAL HOLD and REMOVE LEGAL HOLD clauses. By default, the ACCOUNTADMIN role has this privilege. |
| APPLY | Only a user with this privilege on the snapshot policy can use the ALTER SNAPSHOT SET command with the APPLY SNAPSHOT POLICY clause to add the snapshot policy to a snapshot set that already exists. |

Expand

Show lessSee more

These privileges are required on the currently active primary role, not a secondary role.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

Important

If the snapshot policy has a retention lock applied to it, and there are any
unexpired snapshots in the snapshot set, then you can’t delete the snapshot set.
In that case, you must wait for all the snapshots in the set to expire.
This restriction applies even to privileged roles such as ACCOUNTADMIN, and to Snowflake support.
For that reason, be careful when specifying retention lock and a long expiration
period in a snapshot policy.

## Examples

Manually add a snapshot to snapshot set `t1_snapshots`:

Copy code

```
ALTER SNAPSHOT SET t1_snapshots
  ADD SNAPSHOT;
```

Update the snapshot policy for snapshot set `t1_snapshots`:

Copy code

```
ALTER SNAPSHOT SET t1_snapshots
  APPLY SNAPSHOT POLICY daily_snapshot_policy;
```

Suspend a snapshot policy on the snapshot set `t1_snapshot`:

Copy code

```
ALTER SNAPSHOT SET t1_snapshots
  SUSPEND SNAPSHOT POLICY;
```

Resume a snapshot policy on the snapshot set `t1_snapshots`:

Copy code

```
ALTER SNAPSHOT SET t1_snapshots
  RESUME SNAPSHOT POLICY;
```

To find the snapshot identifier to use with the ADD LEGAL HOLD
and REMOVE LEGAL HOLD clauses, you typically use the SHOW SNAPSHOTS
command to list the eligible snapshots and their creation times.
The following example shows how you might list the appropriate
snapshots, add a legal hold to one specific snapshot, and later
remove that legal hold. Substitute your own role name, snapshot set name,
and snapshot identifier.

Copy code

```
USE ROLE my_legal_hold_role; -- use a role that has the APPLY LEGAL HOLD privilege
SHOW SNAPSHOTS IN SNAPSHOT SET my_db_snapshot_set
  ->> SELECT "created_on", "snapshot_id" FROM $1 WHERE "is_under_legal_hold" = 'N';
ALTER SNAPSHOT SET my_db_snapshot_set
  MODIFY SNAPSHOT IDENTIFIER '790d1ee4-88b2-451f-9ccc-eacd1e93a134'
  ADD LEGAL HOLD;

USE ROLE my_legal_hold_role; -- use a role that has the APPLY LEGAL HOLD privilege
SHOW SNAPSHOTS IN SNAPSHOT SET my_db_snapshot_set
  ->> SELECT "created_on", "snapshot_id" FROM $1 WHERE "is_under_legal_hold" = 'Y';
ALTER SNAPSHOT SET my_db_snapshot_set
  MODIFY SNAPSHOT IDENTIFIER '790d1ee4-88b2-451f-9ccc-eacd1e93a134'
  REMOVE LEGAL HOLD;
```

To add or remove a comment for a specific snapshot, use the snapshot identifier.
The following example finds a snapshot identifier, adds a comment, and then removes
the comment from the same snapshot:

Copy code

```
SHOW SNAPSHOTS IN SNAPSHOT SET my_db_snapshot_set
  ->> SELECT "created_on", "snapshot_id" FROM $1
        ORDER BY "created_on" DESC LIMIT 1;

ALTER SNAPSHOT SET my_db_snapshot_set
  MODIFY SNAPSHOT IDENTIFIER '790d1ee4-88b2-451f-9ccc-eacd1e93a134'
  SET COMMENT = 'Database state after CI/CD deployment at git commit 8f201bf.';

ALTER SNAPSHOT SET my_db_snapshot_set
  MODIFY SNAPSHOT IDENTIFIER '790d1ee4-88b2-451f-9ccc-eacd1e93a134'
  UNSET COMMENT;
```
