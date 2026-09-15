# CREATE BACKUP SET

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a [backup](/user-guide/backups) set for a table, a schema, or a database. Once the backup set exists, you can
add a new backup (backup) to the backup set at any time by running an ALTER BACKUP SET command. Snowflake also adds backups
to the backup set automatically, if you defined a schedule in a [backup policy](/user-guide/backups#label-snapshots-concept-snapshot-policy)
and associated that backup policy with the backup set.

Each backup set represents a set of backups for a specific table, or the objects in a
specific schema, or the objects in a specific database. That way, you can make your backups
very granular or very comprehensive. And the backups for each table, schema, or database can
have their own independent schedules.

For the kinds of objects that are included in schema backups and database backups, see
[Backup objects](/user-guide/backups#label-backup-objects).

This command supports the following variants:

- [CREATE OR ALTER BACKUP SET](#label-create-or-alter-backup-set-syntax): Creates a backup set if it doesn’t exist or alters an existing backup set.

See also:
:   [ALTER BACKUP SET](/sql-reference/sql/alter-backup-set),
    [DROP BACKUP SET](/sql-reference/sql/drop-backup-set),
    [SHOW BACKUP SETS](/sql-reference/sql/show-backup-sets),
    [CREATE BACKUP POLICY](/sql-reference/sql/create-backup-policy),
    [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] BACKUP SET [ IF NOT EXISTS ] <name>
   FOR [ DYNAMIC ] TABLE <table_name>
   [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
   [ WITH BACKUP POLICY <policy_name> ]
   [ COMMENT = <string> ]
```

Copy code

```
CREATE [ OR REPLACE ] BACKUP SET [ IF NOT EXISTS ] <name>
  FOR SCHEMA <schema_name>
   [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
   [ WITH BACKUP POLICY <policy_name> ]
   [ COMMENT = <string> ]
```

Copy code

```
CREATE [ OR REPLACE ] BACKUP SET [ IF NOT EXISTS ] <name>
  FOR DATABASE <database_name>
   [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
   [ WITH BACKUP POLICY <policy_name> ]
   [ COMMENT = <string> ]
```

## Variant syntax

### CREATE OR ALTER BACKUP SET

Creates a new backup set if it doesn’t already exist, or updates an existing one.
A CREATE OR ALTER BACKUP SET statement follows the syntax rules of a CREATE BACKUP SET statement and has the same limitations as an
[ALTER BACKUP SET](/sql-reference/sql/alter-backup-set) statement.

For an existing backup set, you can update the `COMMENT` and attach a `WITH BACKUP POLICY` if one isn’t already set. The `FOR` target
can’t be changed, and an attached backup policy can’t be replaced or removed.

Copy code

```
CREATE OR ALTER BACKUP SET <name>
   FOR [ DYNAMIC ] TABLE <table_name>
   [ WITH BACKUP POLICY <policy_name> ]
   [ COMMENT = <string> ]
```

Copy code

```
CREATE OR ALTER BACKUP SET <name>
  FOR SCHEMA <schema_name>
   [ WITH BACKUP POLICY <policy_name> ]
   [ COMMENT = <string> ]
```

Copy code

```
CREATE OR ALTER BACKUP SET <name>
  FOR DATABASE <database_name>
   [ WITH BACKUP POLICY <policy_name> ]
   [ COMMENT = <string> ]
```

## Required parameters

`name`
:   Identifier for the backup set; must be unique for your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`FOR [ DYNAMIC ] TABLE table_name`
:   Specifies the name of the table or dynamic table. In that case, the backup set represents backups
    of a single table.

`FOR SCHEMA schema_name`
:   Specifies the name of the schema. In that case, the backup set represents backups
    of all the tables and other objects in a specific schema.

`FOR DATABASE database_name`
:   Specifies the name of the database. In that case, the backup set represents backups
    of all the tables, schemas, and other objects in a specific database.

## Optional parameters

`OR REPLACE`
:   If a backup set with this name already exists, delete it and create a new one.
    If the backup set can’t be deleted because of backup policy rules for retention locks,
    legal holds, and expiry times, the command fails.
    This clause is mutually exclusive with `IF NOT EXISTS`.

`IF NOT EXISTS`
:   Creates the backup set only if there isn’t a backup set with the same name.
    If a backup set already exists, the command returns a success message even though it has no effect.
    This clause is mutually exclusive with `OR REPLACE`.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`WITH BACKUP POLICY policy_name`
:   Specifies the name of the backup policy for the set.
    The backup policy defines properties of the backup set such as the schedule for backups,
    the retention period for each backup, and whether to prevent backups from being
    removed before the end of the retention period.

    If you omit this parameter from the CREATE BACKUP SET command, you can apply a
    policy later with the ALTER BACKUP SET command.

    Important

    Applying a backup policy with a retention lock to a backup set is *irreversible*.
    Due to the strong guarantees that are needed for regulatory compliance, after you put a retention lock on a backup set,
    you can’t revoke the lock. Snowflake support also can’t revoke such a retention lock. Plan carefully before
    you set a retention lock on a backup set with a long expiration period, to avoid unexpected storage charges
    for undeletable backup sets, and the schemas and databases that contain them.

    If a Snowflake organization is deleted, the organization is no longer a Snowflake customer. In this case,
    Snowflake deletes all backups, including those with retention locks. Deleting a Snowflake organization
    requires the involvement of Snowflake support. It isn’t something that an administrator can do by accident.

`COMMENT = 'string_literal'`
:   Specifies a comment for the backup set.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Notes |
| --- | --- |
| CREATE BACKUP SET | The role used to create a backup set must have this privilege granted on the schema in which the backup set is created. To actually create the backup set also requires the appropriate privilege on the object that’s the subject of the backup set: SELECT for a table backup, or USAGE for a schema backup or database backup. |
| SELECT | The role used to create a backup set for a table must have the SELECT privilege on that table. |
| USAGE | The role used to create a backup set for a schema or database must have the USAGE privilege on that schema or database. |
| APPLY | The role used to apply a backup policy on a backup set must have this privilege on the backup policy. |
| APPLY BACKUP RETENTION LOCK | The role used to apply a backup policy with retention lock on a backup set must have this privilege on the account. |
| OWNERSHIP | Required to execute a [CREATE OR ALTER BACKUP SET](#label-create-or-alter-backup-set-syntax) statement for an *existing* backup set. |

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

If the backup policy has a retention lock applied to it, and there are any
unexpired backups in the backup set, then you can’t delete the backup set.
In that case, you must wait for all the backups in the set to expire.
This restriction applies even to privileged roles such as ACCOUNTADMIN, and to Snowflake support.
For that reason, be careful when specifying retention lock and a long expiration
period in a backup policy.

### CREATE OR ALTER BACKUP SET

- All limitations of the [ALTER BACKUP SET](/sql-reference/sql/alter-backup-set) command apply.
- The `FOR` target can’t be changed.
- A backup policy can be attached if the backup set doesn’t already have one, but an existing backup policy can’t be replaced or
  removed.
- Tags aren’t supported.

## Examples

Create a backup set named `t1_backups` for table `t1`:

Copy code

```
CREATE BACKUP SET t1_backups
  FOR TABLE t1;
```

Create a backup set `t1_backups` for table `t1` with a backup policy:

Copy code

```
CREATE BACKUP SET t1_backups
  FOR TABLE t1
  WITH BACKUP POLICY hourly_backup_policy;
```

Create a backup set `s1_backups` for schema `s1` with a backup policy:

Copy code

```
CREATE BACKUP SET s1_backups
  FOR SCHEMA s1
  WITH BACKUP POLICY hourly_backup_policy;
```

Create a backup set `d1_backups` for database `d1` with a backup policy:

Copy code

```
CREATE BACKUP SET d1_backups
  FOR DATABASE d1
  WITH BACKUP POLICY hourly_backup_policy;
```

### CREATE OR ALTER BACKUP SET

Create a backup set for table `t1`, or update its comment and attach a backup policy if it already exists without one:

Copy code

```
CREATE OR ALTER BACKUP SET t1_backups
  FOR TABLE t1
  WITH BACKUP POLICY hourly_backup_policy
  COMMENT = 'Backups for t1';
```
