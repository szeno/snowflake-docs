# CREATE SNAPSHOT SET — *Deprecated*

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The CREATE SNAPSHOT SET command is deprecated. See [CREATE BACKUP SET](/sql-reference/sql/create-backup-set).

Creates a [snapshot](/user-guide/backups) set for a table, a schema, or a database. Once the snapshot set exists, you can
add a new backup (snapshot) to the snapshot set at any time by running an ALTER SNAPSHOT SET command. Snowflake also adds snapshots
to the snapshot set automatically, if you defined a schedule in a [snapshot policy](/user-guide/backups#label-snapshots-concept-snapshot-policy)
and associated that snapshot policy with the snapshot set.

Each snapshot set represents a set of backups for a specific table, or the objects in a
specific schema, or the objects in a specific database. That way, you can make your backups
very granular or very comprehensive. And the backups for each table, schema, or database can
have their own independent schedules.

For the kinds of objects that are included in schema snapshots and database snapshots, see
[Backup objects](/user-guide/backups#label-backup-objects).

CREATE OR ALTER SNAPSHOT SET is also supported as an alias of [CREATE OR ALTER BACKUP SET](/sql-reference/sql/create-backup-set#label-create-or-alter-backup-set-syntax);
see that topic for the variant syntax, usage notes, and examples.

See also:
:   [ALTER SNAPSHOT SET — Deprecated](/sql-reference/sql/alter-snapshot-set),
    [DROP SNAPSHOT SET — Deprecated](/sql-reference/sql/drop-snapshot-set),
    [SHOW SNAPSHOT SETS — Deprecated](/sql-reference/sql/show-snapshot-sets),
    [CREATE SNAPSHOT POLICY — Deprecated](/sql-reference/sql/create-snapshot-policy)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] SNAPSHOT SET [ IF NOT EXISTS ] <name>
   FOR [ DYNAMIC ] TABLE <table_name>
   [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
   [ WITH SNAPSHOT POLICY <policy_name> ]
   [ COMMENT = <string> ]
```

Copy code

```
CREATE [ OR REPLACE ] SNAPSHOT SET [ IF NOT EXISTS ] <name>
  FOR SCHEMA <schema_name>
   [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
   [ WITH SNAPSHOT POLICY <policy_name> ]
   [ COMMENT = <string> ]
```

Copy code

```
CREATE [ OR REPLACE ] SNAPSHOT SET [ IF NOT EXISTS ] <name>
  FOR DATABASE <database_name>
   [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
   [ WITH SNAPSHOT POLICY <policy_name> ]
   [ COMMENT = <string> ]
```

## Required parameters

`name`
:   Identifier for the snapshot set; must be unique for your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`FOR [ DYNAMIC ] TABLE table_name`
:   Specifies the name of the table or dynamic table. In that case, the snapshot set represents backups
    of a single table.

`FOR SCHEMA schema_name`
:   Specifies the name of the schema. In that case, the snapshot set represents backups
    of all the tables and other objects in a specific schema.

`FOR DATABASE database_name`
:   Specifies the name of the database. In that case, the snapshot set represents backups
    of all the tables, schemas, and other objects in a specific database.

## Optional parameters

`OR REPLACE`
:   If a snapshot set with this name already exists, delete it and create a new one.
    If the snapshot set can’t be deleted because of snapshot policy rules for retention locks,
    legal holds, and expiry times, the command fails.
    This clause is mutually exclusive with `IF NOT EXISTS`.

`IF NOT EXISTS`
:   Creates the snapshot set only if there isn’t a snapshot set with the same name.
    If a snapshot set already exists, the command returns a success message even though it has no effect.
    This clause is mutually exclusive with `OR REPLACE`.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`WITH SNAPSHOT POLICY policy_name`
:   Specifies the name of the snapshot policy for the set.
    The snapshot policy defines properties of the snapshot set such as the schedule for backups,
    the retention period for each snapshot, and whether to prevent snapshots from being
    removed before the end of the retention period.

    If you omit this parameter from the CREATE SNAPSHOT SET command, you can apply a
    policy later with the ALTER SNAPSHOT SET command.

    Important

    Applying a snapshot policy with a retention lock to a snapshot set is *irreversible*.
    Due to the strong guarantees that are needed for regulatory compliance, after you put a retention lock on a snapshot set,
    you can’t revoke the lock. Snowflake support also can’t revoke such a retention lock. Plan carefully before
    you set a retention lock on a snapshot set with a long expiration period, to avoid unexpected storage charges
    for undeletable snapshot sets, and the schemas and databases that contain them.

    If a Snowflake organization is deleted, the organization is no longer a Snowflake customer. In this case,
    Snowflake deletes all snapshots, including those with retention locks. Deleting a Snowflake organization
    requires the involvement of Snowflake support. It isn’t something that an administrator can do by accident.

`COMMENT = 'string_literal'`
:   Specifies a comment for the snapshot set.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Notes |
| --- | --- |
| CREATE SNAPSHOT SET | The role used to create a snapshot set must have this privilege granted on the schema in which the snapshot set is created. To actually create the snapshot set also requires the appropriate privilege on the object that’s the subject of the snapshot set: SELECT for a table snapshot, or USAGE for a schema snapshot or database snapshot. |
| SELECT | The role used to create a snapshot set for a table must have the SELECT privilege on that table. |
| USAGE | The role used to create a snapshot set for a schema or database must have the USAGE privilege on that schema or database. |
| APPLY | The role used to apply a snapshot policy on a snapshot set must have this privilege on the snapshot policy. |
| APPLY SNAPSHOT RETENTION LOCK | The role used to apply a snapshot policy with retention lock on a snapshot set must have this privilege on the account. |

Expand

Show lessSee more

These privileges are required on the currently active primary role, not a secondary role.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Regarding metadata:

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

Create a snapshot set named `t1_snapshots` for table `t1`:

Copy code

```
CREATE SNAPSHOT SET t1_snapshots
  FOR TABLE t1;
```

Create a snapshot set `t1_snapshots` for table `t1` with a snapshot policy:

Copy code

```
CREATE SNAPSHOT SET t1_snapshots
  FOR TABLE t1
  WITH SNAPSHOT POLICY hourly_snapshot_policy;
```

Create a snapshot set `s1_snapshots` for schema `s1` with a snapshot policy:

Copy code

```
CREATE SNAPSHOT SET s1_snapshots
  FOR SCHEMA s1
  WITH SNAPSHOT POLICY hourly_snapshot_policy;
```

Create a snapshot set `d1_snapshots` for database `d1` with a snapshot policy:

Copy code

```
CREATE SNAPSHOT SET d1_snapshots
  FOR DATABASE d1
  WITH SNAPSHOT POLICY hourly_snapshot_policy;
```
