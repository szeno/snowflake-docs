# CREATE BACKUP POLICY

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a [backup](/user-guide/backups) policy.
You associate the policy with one or more backup sets.
The settings in the policy define the schedule and expiration periods for each backup sets
that uses the policy.

The schedule determines how often Snowflake automatically makes a backup and adds the resulting backup
to the backup set that’s governed by the policy.
The expiration period determines how long each backup is retained before Snowflake automatically deletes it from the
associated backup set.

This command supports the following variants:

- [CREATE OR ALTER BACKUP POLICY](#label-create-or-alter-backup-policy-syntax): Creates a backup policy if it doesn’t exist or alters an existing backup policy.

Tip

The backup policy is optional for a backup set. If you don’t need scheduled backups, a retention lock,
or an expiration period, you can create a backup set without a backup policy. You can also use
ALTER BACKUP SET to apply a backup policy later to an existing backup set, or to suspend and resume
the scheduled backups specified in the backup policy.

See also:
:   [ALTER BACKUP POLICY](/sql-reference/sql/alter-backup-policy),
    [DROP BACKUP POLICY](/sql-reference/sql/drop-backup-policy),
    [SHOW BACKUP POLICIES](/sql-reference/sql/show-backup-policies),
    [CREATE BACKUP SET](/sql-reference/sql/create-backup-set),
    [ALTER BACKUP SET](/sql-reference/sql/alter-backup-set),
    [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] BACKUP POLICY [ IF NOT EXISTS ] <name>
   [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
   [ WITH RETENTION LOCK ]
   [ SCHEDULE = '{ <num> MINUTE | <num> HOUR | USING CRON <expr> <time_zone> }' ]
   [ EXPIRE_AFTER_DAYS = <days_integer> ]
   [ COMMENT = <string> ]
```

## Variant syntax

### CREATE OR ALTER BACKUP POLICY

Creates a new backup policy if it doesn’t already exist, or transforms an existing backup policy into the backup policy defined in the
statement. A CREATE OR ALTER BACKUP POLICY statement follows the syntax rules of a CREATE BACKUP POLICY statement and has the same
limitations as an [ALTER BACKUP POLICY](/sql-reference/sql/alter-backup-policy) statement.

The following modifications are supported when altering a backup policy:

- Updating `SCHEDULE` or `EXPIRE_AFTER_DAYS`.
- Adding, updating, or removing a `COMMENT`.

Copy code

```
CREATE OR ALTER BACKUP POLICY <name>
   [ WITH RETENTION LOCK ]
   [ SCHEDULE = '{ <num> MINUTE | <num> HOUR | USING CRON <expr> <time_zone> }' ]
   [ EXPIRE_AFTER_DAYS = <days_integer> ]
   [ COMMENT = <string> ]
```

## Required parameters

`name`
:   Identifier for the backup policy; must be unique for your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`OR REPLACE`
:   If a backup policy with this name already exists, delete it and create a new one.
    This clause is mutually exclusive with `IF NOT EXISTS`.

`IF NOT EXISTS`
:   Creates the backup policy only if there isn’t a backup policy with the same name.
    If a backup policy already exists, the command returns a success message even though it has no effect.
    This clause is mutually exclusive with `OR REPLACE`.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`WITH RETENTION LOCK`
:   Specifies the mandatory retention period for backups. Backups with retention locks
    can’t be deleted, even by a privileged user.
    For more information, see the [restrictions for a backup with a retention lock](/user-guide/backups#label-backups-concept-retention-lock).

    Note

    Only a user with the APPLY BACKUP RETENTION LOCK privilege can create a backup policy with retention lock.

    Important

    Applying a backup policy with a retention lock to a backup set is *irreversible*.
    Due to the strong guarantees that are needed for regulatory compliance, after you put a retention lock on a backup set,
    you can’t revoke the lock. Snowflake support also can’t revoke such a retention lock. Plan carefully before
    you set a retention lock on a backup set with a long expiration period, to avoid unexpected storage charges
    for undeletable backup sets, and the schemas and databases that contain them.

    If a Snowflake organization is deleted, the organization is no longer a Snowflake customer. In this case,
    Snowflake deletes all backups, including those with retention locks. Deleting a Snowflake organization
    requires the involvement of Snowflake support. It isn’t something that an administrator can do by accident.

`SCHEDULE = '{ num MINUTE | num HOUR | USING CRON expr time_zone }'`
:   Specifies the schedule for creating backups of an object.

    Note

    The minimum schedule for backups must be 60 minutes or 1 hour.

    Each backup policy must have one or both of the schedule and expiration period properties.
    For more information, see [Backup policy](/user-guide/backups#label-backups-concept-backup-policy).

    - **`USING CRON expr time_zone`**

      Specifies a cron expression and time zone for the point in time a backup of an object is created. Supports a subset of
      standard cron utility syntax.

      For a list of time zones, see the [list of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
      (in Wikipedia).

      The cron expression consists of the following fields:

      ```
      # __________ minute (0-59)
      # | ________ hour (0-23)
      # | | ______ day of month (1-31, or L)
      # | | | ____ month (1-12, JAN-DEC)
      # | | | | __ day of week (0-6, SUN-SAT, or L)
      # | | | | |
      # | | | | |
        * * * * *
      ```

      The following special characters are supported:

      **`*`**

      Wildcard. Specifies any occurrence of the field.

      **`L`**

      Stands for “last”. When used in the day-of-week field, it lets you specify constructs such as “the last Friday” (“5L”) of a
      given month. In the day-of-month field, it specifies the last day of the month.

      **`/n`**

      Indicates the *nth* instance of a given unit of time. Each quanta of time is computed independently. For example, if `4/3` is
      specified in the month field, then the backup is scheduled for April, July and October (that is, every 3 months, starting with the 4th
      month of the year). The same schedule is maintained in subsequent years. That is, the backup is not scheduled to run in
      January (3 months after the October run).

      Note

      - The cron expression currently evaluates against the specified time zone only. Altering the [TIMEZONE](/sql-reference/parameters#label-timezone) parameter value
        for the account (or setting the value at the user or session level) does not change the time zone for the backup.
      - The cron expression defines all valid run times for the backup. Snowflake attempts to create a backup based on
        this schedule; however, any valid run time is skipped if a previous run has not completed before the next valid run time starts.
      - When both a specific day of month and day of week are included in the cron expression, then the backup is scheduled on days
        satisfying either the day of the month or the day of the week. For example, `SCHEDULE = 'USING CRON 0 0 10-20 * TUE,THU UTC'`
        schedules a backup at 0AM (midnight) on any 10th to 20th day of the month and also on any Tuesday or Thursday outside of those dates.
    - `num MINUTE` or `num MINUTES`
      :   Specifies an interval (in minutes) of wait time between backups. Accepts positive integers only.

          Also supports `num M` syntax.
    - `num HOUR` or `num HOURS`
      :   Specifies an interval (in hours) of wait time between backups. Accepts positive integers only.

          Also supports `num H` syntax.

    To avoid ambiguity, a *base interval time* is set in the following circumstances:

    - When the object is created (using CREATE BACKUP SET … WITH BACKUP POLICY).
    - When a different interval is set (using ALTER BACKUP SET … APPLY BACKUP POLICY or
      ALTER BACKUP POLICY … SET SCHEDULE).

    The base interval time starts the interval counter from the current clock time. For example, if an
    INTERVAL value of `10 MINUTES` is set and the scheduled backup is enabled at 9:03 AM, then the next backup
    is created at 9:13 AM, 9:23 AM, and so on. Note that we make a best effort to ensure absolute
    precision, but only guarantee that a backup does not execute before the set interval occurs
    (that is, in the current example, the backup could first run at 9:14 AM, but will definitely not run
    at 9:12 AM).

`EXPIRE_AFTER_DAYS = days_integer`
:   Specifies the number of days until the backup expires. Snowflake automatically deletes expired backups.
    If this parameter is not specified, backups remain in the backup set until they are manually deleted from the set.

    - Minimum value: `1`.
    - Maximum value: `3653` (roughly 10 years) if you don’t specify the `SCHEDULE` clause.

    Note

    Each backup policy must have one or both of the schedule and expiration period properties.
    For more information, see [Backup policy](/user-guide/backups#label-backups-concept-backup-policy).

`COMMENT = 'string_literal'`
:   Specifies a comment for the backup policy.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Notes |
| --- | --- |
| CREATE BACKUP POLICY | The role used to create a backup policy must have this privilege on the schema in which the policy is created. |
| APPLY BACKUP RETENTION LOCK | Only a user with this privilege on the account can create a backup policy with retention lock. |
| OWNERSHIP | Required to execute a [CREATE OR ALTER BACKUP POLICY](#label-create-or-alter-backup-policy-syntax) statement for an *existing* backup policy. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- [Time Travel and Failsafe](/user-guide/data-time-travel) retention do not apply to backups. A backup can’t be
  recovered after it expires.
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

### CREATE OR ALTER BACKUP POLICY

- All limitations of the [ALTER BACKUP POLICY](/sql-reference/sql/alter-backup-policy) command apply.
- Setting or unsetting a tag is not supported.
- The `WITH RETENTION LOCK` clause can’t be changed for an existing backup policy.

## Examples

Create a backup policy that creates a backup every hour and expires after 90 days:

Copy code

```
CREATE BACKUP POLICY hourly_backup_policy
  SCHEDULE = '60 MINUTE'
  EXPIRE_AFTER_DAYS = 90
  COMMENT = 'Hourly backups that expire after 90 days';
```

Create a backup policy with a retention lock that creates a backup every 24 hours and expires after 90 days. The backups
created using this backup policy can’t be modified or deleted before the expiration period ends:

Copy code

```
CREATE BACKUP POLICY daily_backup_policy_with_lock
  WITH RETENTION LOCK
  SCHEDULE = '1440 MINUTE'
  EXPIRE_AFTER_DAYS = 90
  COMMENT = 'regulatory backups expire after 90 days with retention lock';
```

Create a backup policy using a cron expression for the schedule. The following statement creates a policy that creates backups
every Tuesday and Friday of the week at 11PM:

Copy code

```
CREATE BACKUP POLICY twice_weekly_backup_policy
  SCHEDULE = 'USING CRON 0 23 * * 2,5 UTC'
  EXPIRE_AFTER_DAYS = 7
  COMMENT = 'Twice-weekly backups that expire after 7 days';
```

### CREATE OR ALTER BACKUP POLICY

Create a new backup policy, or update the schedule and expiration period of an existing one:

Copy code

```
CREATE OR ALTER BACKUP POLICY hourly_backup_policy
  SCHEDULE = '60 MINUTE'
  EXPIRE_AFTER_DAYS = 90
  COMMENT = 'Hourly backups that expire after 90 days';
```
