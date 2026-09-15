# ALTER BACKUP POLICY

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Modifies the properties of a [backup](/user-guide/backups) policy. The following changes are supported:

- Rename the policy.
- Add or update the comment for the policy.
- Change the schedule and expiration settings for the policy. The schedule determines how often Snowflake
  automatically makes a backup and adds the resulting backup to the backup set that’s governed by the policy.
  The expiration period determines how long each backup is retained before Snowflake automatically deletes it from the
  associated backup set.
- Unset properties of the policy, so that they revert back to their default values.

See also:
:   [CREATE BACKUP POLICY](/sql-reference/sql/create-backup-policy),
    [DROP BACKUP POLICY](/sql-reference/sql/drop-backup-policy),
    [SHOW BACKUP POLICIES](/sql-reference/sql/show-backup-policies)

## Syntax

Copy code

```
ALTER BACKUP POLICY <name> RENAME TO <new_name>

ALTER BACKUP POLICY <name> SET
  [ COMMENT = '<string_literal>' ]
  [ SCHEDULE = '{ <num> MINUTE | <num> HOUR | USING CRON <expr> <time_zone> }' ]
  [ EXPIRE_AFTER_DAYS = <days_integer> ]

ALTER BACKUP POLICY <name> UNSET { COMMENT | SCHEDULE | EXPIRE_AFTER_DAYS }

ALTER BACKUP POLICY <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER BACKUP POLICY <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Specifies the identifier for the backup policy.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Specifies a new identifier for the backup policy; must be unique for your account.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET...`
:   Specifies one or more properties to set for the backup policy (separated by blank spaces, commas, or new lines):

    `COMMENT = 'string_literal'`
    :   Specifies a comment for the backup policy.

    `SCHEDULE = '{ num MINUTE | num HOUR | USING CRON expr time_zone }'`
    :   Specifies the schedule for creating backups of an object.

        Note

        The minimum schedule for backups is 60 minutes or 1 hour.

        Every policy must include a SCHEDULE clause, an EXPIRE\_AFTER\_DAYS clause, or both.

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
    :   > Specifies the number of days until the backup expires. Snowflake automatically deletes expired backups.
        > If this parameter isn’t specified, backups remain in the backup set until they are manually deleted from the set.
        >
        > - Minimum value: `1`
        > - Maximum value: `3653` (roughly 10 years) if you don’t specify the `SCHEDULE` clause.
        >
        > Note
        >
        > If the policy has a retention lock, you can increase the EXPIRE\_AFTER\_DAYS value, but you can’t decrease that value.
        >
        > Every policy must include a SCHEDULE clause, an EXPIRE\_AFTER\_DAYS clause, or both.

        `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
        :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

            The tag value is always a string, and the maximum number of characters for the tag value is 256.

            For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET...`
:   Unset one of the following properties for the backup policy. The property reverts to its default value.

    - COMMENT
    - `TAG tag_name [ , tag_name ... ]`
    - SCHEDULE
    - EXPIRE\_AFTER\_DAYS

    Note

    You can unset the SCHEDULE property, or the EXPIRE\_AFTER\_DAYS property, but not both.
    For example, you might keep the EXPIRE\_AFTER\_DAYS property when you don’t intend to create new backups,
    but you want existing backups to expire after a certain time.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Notes |
| --- | --- |
| OWNERSHIP | The role used to modify a backup policy must have the OWNERSHIP privilege on the backup policy. |
| APPLY BACKUP RETENTION LOCK | The role used to modify a backup policy with a retention lock must have this privilege on the account. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Regarding metadata:

Attention

Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Rename the backup policy `hourly_backup_policy` to `daily_backup_policy`:

Copy code

```
ALTER BACKUP POLICY hourly_backup_policy
  RENAME TO daily_backup_policy;
```

Add a comment to backup policy `hourly_backup_policy`:

Copy code

```
ALTER BACKUP POLICY hourly_backup_policy
  SET COMMENT = 'hourly backup expires in 90 days';
```

Change schedule for backup policy `every_two_hours`:

Copy code

```
ALTER BACKUP POLICY every_two_hours SET SCHEDULE = '120 MINUTE';
```

Revert the EXPIRE\_AFTER\_DAYS property back to its default value:

Copy code

```
ALTER BACKUP POLICY sample_backup_policy UNSET EXPIRE_AFTER_DAYS;
```
