# CREATE REPLICATION GROUP

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new [replication group](/user-guide/account-replication-intro#label-replication-and-failover-groups) of specified objects in the system.

For more information about using replication groups, see [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).

This command can be used to:

- Create a replication group in the source account to enable replication of specified objects to a target account in the same
  organization.
- Create a secondary replication group in a target account as a replica of the primary replication group in the source account in the
  same organization.

See also:
:   [ALTER REPLICATION GROUP](/sql-reference/sql/alter-replication-group) , [DROP REPLICATION GROUP](/sql-reference/sql/drop-replication-group) , [SHOW REPLICATION GROUPS](/sql-reference/sql/show-replication-groups)

## Syntax

Copy code

```
CREATE REPLICATION GROUP [ IF NOT EXISTS ] <name>
    OBJECT_TYPES = <object_type> [ , <object_type> , ... ]
    [ ALLOWED_DATABASES = <db_name> [ , <db_name> , ... ] ]
    [ ALLOWED_EXTERNAL_VOLUMES = <external_volume_name> [ , <external_volume_name> , ... ] ]
    [ ALLOWED_SHARES = <share_name> [ , <share_name> , ... ] ]
    [ ALLOWED_INTEGRATION_TYPES = <integration_type_name> [ , <integration_type_name> , ... ] ]
    ALLOWED_ACCOUNTS = <org_name>.<target_account_name> [ , <org_name>.<target_account_name> , ... ]
    [ IGNORE EDITION CHECK ]
    [ REPLICATION_SCHEDULE = '{ <num> MINUTE | USING CRON <expr> <time_zone> }' ]
    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
    [ ERROR_INTEGRATION = <integration_name> ]
```

**Secondary Replication Group**

Copy code

```
CREATE REPLICATION GROUP [ IF NOT EXISTS ] <secondary_name>
    AS REPLICA OF <org_name>.<source_account_name>.<name>
```

## Parameters

`name`
:   Specifies the identifier for the replication group. The identifier must start with an alphabetic character and cannot contain spaces or
    special characters unless the identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double
    quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`OBJECT_TYPES = object_type [ , object_type , ... ]`
:   Type(s) of objects for which you are enabling replication from the source account to the target account.

    The following object types are supported:

    > ACCOUNT PARAMETERS:
    > :   *Requires Business Critical Edition (or higher).*
    >
    >     All account-level parameters. This includes [account parameters](/sql-reference/parameters#label-account-parameters) and parameters that can be
    >     [set for your account](/user-guide/admin-account-management).
    >
    > DATABASES:
    > :   Add database objects to the list of object types. If database objects are included in the list of specified object types, the
    >     `ALLOWED_DATABASES` parameter must be set.
    >
    > EXTERNAL VOLUMES:
    > :   Add external volume objects to the list of object types. If external volume objects are included in the list of specified object types,
    >     the `ALLOWED_EXTERNAL_VOLUMES` parameter must be set.
    >
    > INTEGRATIONS:
    > :   *Requires Business Critical Edition (or higher).*
    >
    >     Currently, only security, API, storage, external access, and certain types of notification integrations are supported.
    >     For details, see
    >     [Integration replication](/user-guide/account-replication-intro#label-account-replication-integrations).
    >
    >     If integration objects are included in the list of specified object types, the
    >     `ALLOWED_INTEGRATION_TYPES` parameter must be set.
    >
    > NETWORK POLICIES:
    > :   *Requires Business Critical Edition (or higher).*
    >
    >     All network policies in the source account.
    >
    > RESOURCE MONITORS:
    > :   *Requires Business Critical Edition (or higher).*
    >
    >     All resource monitors in the source account.
    >
    > ROLES:
    > :   *Requires Business Critical Edition (or higher).*
    >
    >     All roles in the source account. Replicating roles implicitly includes all grants for object types included in the replication group.
    >     For example, if `ROLES` is the only object type that is replicated, then only hierarchies of roles (that is, roles granted to
    >     other roles) are replicated to target accounts. If the `USERS` object type is also included, then role grants to users are
    >     also replicated.
    >
    > SHARES:
    > :   Add share objects to the list of object types. If share objects are included in the list of specified object types, the
    >     `ALLOWED_SHARES` parameter must be set.
    >
    > USERS:
    > :   *Requires Business Critical Edition (or higher).*
    >
    >     All users in the source account.
    >
    > WAREHOUSES:
    > :   *Requires Business Critical Edition (or higher).*
    >
    >     All warehouses in the source account.

    Note

    If you replicate users and roles, programmatic access tokens for users are replicated automatically.

    To modify the list of replicated object types to a specified target account, use [ALTER REPLICATION GROUP](/sql-reference/sql/alter-replication-group)
    to reset the list of object types.

`ALLOWED_DATABASES = db_name [ , db_name , ... ]`
:   Specifies the database or list of databases for which you are enabling replication from the source account to the target account.
    For you to set this parameter, the `OBJECT_TYPES` list must include `DATABASES`.

`ALLOWED_EXTERNAL_VOLUMES = external_volume_name [ , external_volume_name , ... ]`
:   [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

    Specifies the external volume or list of external volumes for which you are enabling replication from the source account to the target
    account. For you to set this parameter, the `OBJECT_TYPES` list must include `EXTERNAL VOLUMES`.

`ALLOWED_SHARES = share_name [ , share_name , ... ]`
:   Specifies the share or list of shares for which you are enabling replication from the source account to the target account.
    For you to set this parameter, the `OBJECT_TYPES` list must include `SHARES`.

`ALLOWED_INTEGRATION_TYPES = integration_type_name [ , integration_type_name , ... ]`
:   *Requires Business Critical Edition (or higher).*

    Type(s) of integrations for which you are enabling replication from the source account to the target account.

    > This property requires that the `OBJECT_TYPES` list include `INTEGRATIONS` to set this parameter.
    >
    > The following integration types are supported:
    >
    > > SECURITY INTEGRATIONS:
    > > :   Specifies security integrations.
    > >
    > >     This property requires that the `OBJECT_TYPES` list include `ROLES`.
    > >
    > > API INTEGRATIONS:
    > > :   Specifies API integrations.
    > >
    > >     API integration replication requires additional set up after the API integration is replicated to the target account.
    > >     For more information, see [Updating the remote service for API integrations](/user-guide/account-replication-config#label-update-remote-service-for-api-integrations).
    > >
    > > STORAGE INTEGRATIONS:
    > > :   Specifies storage integrations.
    > >
    > > EXTERNAL ACCESS INTEGRATIONS:
    > > :   Specifies [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access).
    > >
    > >     For more information, see [Replication of stored procedures and user-defined functions (UDFs)](/user-guide/account-replication-considerations#label-replication-stored-procedures-udfs).
    > >
    > > NOTIFICATION INTEGRATIONS:
    > > :   Specifies notification integrations.
    > >
    > >     Only some types of notification integrations are replicated. For details, see
    > >     [Integration replication](/user-guide/account-replication-intro#label-account-replication-integrations).

`ALLOWED_ACCOUNTS = org_name.target_account_name1 [ , org_name.target_account_name2 , ... ]`
:   Specifies the target account or list of target accounts to which replication of specified objects from the source account is
    enabled.

    `org_name`
    :   Name of your Snowflake organization.

    `target_account_name`
    :   Target account to which you are enabling replication of the specified objects.

`IGNORE EDITION CHECK`

> Allows replicating objects to accounts on lower editions in either of the following scenarios:
>
> - A primary replication group with only database and/or share objects is in a Business Critical (or higher) account but
>   one or more accounts approved for replication are on lower editions. Business Critical Edition is intended for Snowflake accounts
>   with extremely sensitive data.
> - A primary replication group with any [object type](/sql-reference/sql/create-replication-group#label-create-replication-group-object-types) is in a Business
>   Critical (or higher) account and a signed business associate agreement is in place to store PHI data in the account per HIPAA and
>   [HITRUST](/user-guide/intro-cloud-platforms#label-hitrust-csf-cert) regulations. However, no such agreement is in place for one or more of the accounts approved
>   for replication, regardless if they are Business Critical (or higher) accounts.
>
> Both scenarios are prohibited by default in an effort to help prevent account administrators for Business Critical (or higher) accounts
> from inadvertently replicating sensitive data to accounts on lower editions.

`REPLICATION_SCHEDULE ...`
:   Specifies the schedule for refreshing secondary replication groups.

    - **`USING CRON expr time_zone`**

      Specifies a cron expression and time zone for the secondary group refresh. Supports a subset of standard cron utility syntax.

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

      Stands for “last”. When used in the day-of-week field, it allows you to specify constructs such as “the last Friday” (“5L”) of a
      given month. In the day-of-month field, it specifies the last day of the month.

      **`/n`**

      Indicates the *nth* instance of a given unit of time. Each quanta of time is computed independently. For example, if `4/3` is
      specified in the month field, then the refresh is scheduled for April, July and October (i.e. every 3 months, starting with the 4th
      month of the year). The same schedule is maintained in subsequent years. That is, the refresh is not scheduled to run in
      January (3 months after the October run).

      Note

      - The cron expression currently evaluates against the specified time zone only. Altering the [TIMEZONE](/sql-reference/parameters#label-timezone) parameter value
        for the account (or setting the value at the user or session level) does not change the time zone for the refresh.
      - The cron expression defines all valid run times for the refresh. Snowflake attempts to refresh secondary groups based on
        this schedule; however, any valid run time is skipped if a previous run has not completed before the next valid run time starts.
      - When both a specific day of month and day of week are included in the cron expression, then the refresh is scheduled on days
        satisfying either the day of month or day of week. For example, `SCHEDULE = 'USING CRON 0 0 10-20 * TUE,THU UTC'`
        schedules a refresh at 0AM on any 10th to 20th day of the month and also on any Tuesday or Thursday outside of those dates.
    - **`num MINUTE`**

      Specifies an interval (in minutes) of wait time between refreshes. Accepts positive integers only.

      Also supports `num M` syntax.

      To avoid ambiguity, a *base interval time* is set:

      - When the object is created (using CREATE <object>) or
      - When a different interval is set (using ALTER <object> … SET REPLICATION\_SCHEDULE)

      The base interval time starts the interval counter from the current clock time. For example, if an INTERVAL value of `10` is set and
      the scheduled refresh is enabled at 9:03 AM, then the refresh runs at 9:13 AM, 9:23 AM, and so on. Note that we make a best effort to
      ensure absolute precision, but only guarantee that refreshes do not execute before their set interval occurs (e.g. in the
      current example, the refresh could first run at 9:14 AM, but will definitely not run at 9:12 AM).

      Note

      The maximum supported value is `11520` (8 days). If the replication schedule has a greater `num MINUTE` value, the
      refresh operation never runs.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`ERROR_INTEGRATION = integration_name`
:   Specifies the name of the notification integration to use to email/push notifications when refresh errors occur for the replication
    group. For more details, see [Error notifications for replication and failover groups](/user-guide/account-replication-error-notifications).

**Secondary Replication Group Parameters**

`secondary_name`
:   Specifies the identifier for the secondary replication group. The identifier must start with an alphabetic character and cannot contain
    spaces or special characters unless the identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in
    double quotes are also case-sensitive. For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    The identifiers for the secondary replication group (`secondary_name`) and primary replication group (`name`) can be, but
    are not required to be, identical.

`AS REPLICA OF org_name.source_account_name.name`
:   Specifies the identifier of the primary replication group from which to create a secondary replication group.

    `org_name`
    :   Name of your Snowflake organization.

    `source_account_name`
    :   Source account from which you are enabling replication of the specified objects.

    `name`
    :   Identifier for the primary replication group in the source account.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE REPLICATION GROUP | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
| MONITOR | Database | To add a database to a replication group, the active role must have the MONITOR privilege on the database. |
| USAGE | External volume | To add an external volume to a replication group, the active role must have the USAGE privilege on the external volume. |
| OWNERSHIP | Share | To add a share to a replication group, the active role must have the OWNERSHIP privilege on the share. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Identifiers for failover groups and replication groups in an account must be unique.
- A database can only be added to one replication or failover group.
- An external volume can only be added to one replication or failover group.
- [Inbound shares](/user-guide/data-share-consumers) (shares from providers) *cannot* be added to a replication or failover group.
- To retrieve the set of accounts in your organization that are enabled for replication, use
  [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts).
- To retrieve the list of replication and failover groups in your organization, use [SHOW REPLICATION GROUPS](/sql-reference/sql/show-replication-groups).
  The `allowed_accounts` column lists all target accounts enabled for object replication from a source account.
- If there are account objects (for example, users or roles) in a target account that you do not want to drop during replication,
  use the [SYSTEM$LINK\_ACCOUNT\_OBJECTS\_BY\_NAME](/sql-reference/functions/system_link_account_objects_by_name) system function to apply a global identifier to objects
  created by means other than replication. For more information, see
  [Apply Global IDs to Objects Created by Scripts in Target Accounts](/user-guide/account-replication-config#label-apply-global-ids-to-objects) before
  you create a replication group.
- Automatically [scheduled refresh operations](/user-guide/account-replication-intro#label-replication-schedule) are executed using the role with the OWNERSHIP
  privilege on the group. If a scheduled refresh operation fails due to insufficient privileges, grant the required privileges
  to the role with the OWNERSHIP privilege on the group.

- If you create a replication or failover group with a tag or modify a replication or failover group by setting a tag on it,
  [tag inheritance](/user-guide/object-tagging/inheritance#label-object-tagging-lineage) does not apply to any objects that you specify in the replication or failover group.

  Tag inheritance is only applicable to objects with a [parent-child relationship](/user-guide/security-access-control-overview#label-access-control-securable-objects), such
  database, schema, and table. There are no child objects of replication or failover groups.
- You cannot set a tag or modify a tag on a secondary replication or failover group because these objects are read
  only.
- When you refresh a secondary replication or failover group, any tags that are set on the primary group are then set on
  the secondary group.

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

### Replicate a single database

**Executed on the source account**

Create a replication group named `myrg` in the source account to enable replication of database `db1` from the source
account to the `myaccount2` account. Set the replication schedule to refresh the database every 10 minutes:

Copy code

```
CREATE REPLICATION GROUP myrg
    OBJECT_TYPES = DATABASES
    ALLOWED_DATABASES = db1
    ALLOWED_ACCOUNTS = myorg.myaccount2
    REPLICATION_SCHEDULE = '10 MINUTE';
```

**Executed on target account**

Create a replication group in the target account as a replica of the replication group `myrg` in the source account:

Copy code

```
CREATE REPLICATION GROUP myrg
    AS REPLICA OF myorg.myaccount1.myrg;
```

### Replicate a database and share objects

**Executed on source account**

Create a replication group named `myrg` in the source account to enable replication of database `db1`, and share `s1` from the source
account to the `myaccount2` account. Set the replication schedule to refresh automatically every 10 minutes:

Copy code

```
CREATE REPLICATION GROUP myrg
    OBJECT_TYPES = DATABASES, SHARES
    ALLOWED_DATABASES = db1
    ALLOWED_SHARES = s1
    ALLOWED_ACCOUNTS = myorg.myaccount2
    REPLICATION_SCHEDULE = '10 MINUTE';
```

**Executed on target account**

Create a replication group in the target account as a replica of the replication group `myrg` in the source account:

Copy code

```
CREATE REPLICATION GROUP myrg
    AS REPLICA OF myorg.myaccount1.myrg;
```

### Replicate account objects

For examples of multiple database and account object replication, see the
[examples for CREATE FAILOVER GROUP](/sql-reference/sql/create-failover-group#label-create-failover-group-examples).
