# CREATE FAILOVER GROUP

[Business Critical Feature](/user-guide/intro-editions)

Requires Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new [failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups) of specified objects in the system.

For more information about using failover groups, see [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).

This command can be used to:

- Create a failover group in the source account to enable replication and failover of specified objects to a target account in
  the same organization.
- Create a secondary failover group in a target account as a replica of the primary failover group in the source account in the same
  organization.

See also:
:   [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group) , [DROP FAILOVER GROUP](/sql-reference/sql/drop-failover-group) , [SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups)

## Syntax

Copy code

```
CREATE FAILOVER GROUP [ IF NOT EXISTS ] <name>
    OBJECT_TYPES = <object_type> [ , <object_type> , ... ]
    [ ALLOWED_DATABASES = <db_name> [ , <db_name> , ... ] ]
    [ ALLOWED_EXTERNAL_VOLUMES = <external_volume_name> [ , <external_volume_name> , ... ] ]
    [ ALLOWED_SHARES = <share_name> [ , <share_name> , ... ] ]
    [ ALLOWED_INTEGRATION_TYPES = <integration_type_name> [ , <integration_type_name> , ... ] ]
    ALLOWED_ACCOUNTS = <org_name>.<target_account_name> [ , <org_name>.<target_account_name> ,  ... ]
    [ IGNORE EDITION CHECK ]
    [ REPLICATION_SCHEDULE = '{ <num> MINUTE | USING CRON <expr> <time_zone> }' ]
    [ OPTIMIZED_REFRESH = { TRUE | FALSE } ]
    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
    [ ERROR_INTEGRATION = <integration_name> ]
```

**Secondary Failover Group**

Copy code

```
CREATE FAILOVER GROUP [ IF NOT EXISTS ] <secondary_name>
    AS REPLICA OF <org_name>.<source_account_name>.<name>
```

## Parameters

`name`
:   Specifies the identifier for the failover group. The identifier must start with an alphabetic character and cannot contain spaces or
    special characters unless the identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double
    quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`OBJECT_TYPES = object_type [ , object_type , ... ]`
:   Type(s) of objects for which you are enabling replication and failover from the source account to the target account.

    The following object types are supported:

    > ACCOUNT PARAMETERS:
    > :   All account-level parameters. This includes [account parameters](/sql-reference/parameters#label-account-parameters) and parameters that can be [set for your account](/user-guide/admin-account-management).
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
    > :   Currently, only security, API, storage, external access, and certain types of notification integrations are supported.
    >     For details, see [Integration replication](/user-guide/account-replication-intro#label-account-replication-integrations).
    >
    >     If integration objects are included in the list of specified object types, the
    >     `ALLOWED_INTEGRATION_TYPES` parameter must be set.
    >
    > LISTINGS:
    > :   Add listings to the list of object types. When adding listings to a failover group, adding shares is optional. Snowflake automatically
    >     selects all of the eligible listings and their shares for replication and failover. For more information, see [Listing support in Business Continuity and Disaster Recovery](/collaboration/listings-bcdr).
    >
    > NETWORK POLICIES:
    > :   All network policies in the source account.
    >
    > PROFILES:
    > :   All profiles in the source account. Review [profile replication constraints](/collaboration/listings-bcdr#label-listings-bcdr-profile-replication-constraints) for information about current constraints.
    >
    > RESOURCE MONITORS:
    > :   All resource monitors in the source account.
    >
    > ROLES:
    > :   All roles in the source account. Replicating roles implicitly includes all grants for object types included in the replication group.
    >     For example, if `ROLES` is the only object type that is replicated, then only hierarchies of roles (that is, roles granted to
    >     other roles) are replicated to target accounts. If the `USERS` object type is also included, then role grants to users are
    >     also replicated.
    >
    > SHARES:
    > :   Add share objects to the list of object types. If share objects are included in the list of specified object types, the
    >     `ALLOWED_SHARES` parameter must be set.
    >
    > USERS:
    > :   All users in the source account.
    >
    > WAREHOUSES:
    > :   All warehouses in the source account.

    Note

    If you replicate users and roles, programmatic access tokens for users are replicated automatically.

    To modify the list of replicated object types to a specified target account, use [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group#label-alter-failover-group) to reset the list of
    object types.

`ALLOWED_DATABASES = db_name [ , db_name , ... ]`
:   Specifies the database or list of databases for which you are enabling replication and failover from the source account to the target
    account. In order for you to set this parameter, the `OBJECT_TYPES` list must include `DATABASES`.

    `db_name`
    :   Specifies the identifier for the database.

`ALLOWED_EXTERNAL_VOLUMES = external_volume_name [ , external_volume_name , ... ]`
:   [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

    Specifies the external volume or list of external volumes for which you are enabling replication and failover from the source account to the target
    account. For you to set this parameter, the `OBJECT_TYPES` list must include `EXTERNAL VOLUMES`.

    `external_volume_name`
    :   Specifies the identifier for the external volume.

`ALLOWED_SHARES = share_name [ , share_name , ... ]`
:   Specifies the share or list of shares for which you are enabling replication and failover from the source account to the target account.
    For you to set this parameter, the `OBJECT_TYPES` list must include `SHARES`.

    `share_name`
    :   Specifies the identifier for the share.

`ALLOWED_INTEGRATION_TYPES = integration_type_name [ , integration_type_name , ... ]`
:   Type(s) of integrations for which you are enabling replication and failover from the source account to the target account.

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

`ALLOWED_ACCOUNTS = org_name.target_account_name [ , org_name.target_account_name , ... ]`
:   Specifies the target account or list of target accounts to which replication and failover of specified objects from the source account is
    enabled. Secondary failover groups in the target accounts in this list can be promoted to serve as the primary failover group in
    case of failover.

    `org_name`
    :   Name of your Snowflake organization.

    `target_account_name`
    :   Target account to which you are enabling replication of the specified objects.

`IGNORE EDITION CHECK`

> Allows replicating objects to accounts in the following scenario:
>
> > The primary failover group is in a Business Critical (or higher) account and a signed business associate agreement is in place to
> > store PHI data in the account per HIPAA and [HITRUST](/user-guide/intro-cloud-platforms#label-hitrust-csf-cert) regulations. However, no such agreement is in place
> > for one or more of the accounts approved for replication, regardless if they are Business Critical (or higher) accounts.
>
> This scenario is prohibited by default.

`REPLICATION_SCHEDULE ...`
:   Specifies the schedule for refreshing secondary failover groups.

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

`OPTIMIZED_REFRESH = { TRUE | FALSE }`
:   [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all Business Critical Edition (or higher) accounts.

    Specifies whether the failover group uses [optimized refresh](/user-guide/account-replication-config#label-optimized-refresh).
    Optimized refresh tracks metadata changes on the source account and applies only those changes to the target account on each refresh,
    so refresh duration scales with the rate of change rather than the total size of your environment.

    When set to `TRUE`:

    - A [REPLICATION\_SCHEDULE](#replication-schedule) is required, and the schedule interval must be no more than 6 hours.
    - The property can be set on the primary failover group only. The CREATE FAILOVER GROUP … AS REPLICA OF statement that creates a
      secondary failover group does not accept the property.
    - The first refresh after enabling is a one-time bootstrapping refresh that establishes the baseline. Subsequent refreshes are
      incremental. The bootstrapping refresh is billed under the optimized-refresh pricing model.
    - The optimized-refresh pricing model applies for all refreshes while this property is `TRUE`. For details, see
      [Pricing for optimized refresh](/user-guide/account-replication-cost#label-optimized-refresh-pricing).

    Default:
    :   `FALSE`

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`ERROR_INTEGRATION = integration_name`
:   Specifies the name of the notification integration to use to send notifications when refresh errors occur for the failover
    group. For more details, see [Error notifications for replication and failover groups](/user-guide/account-replication-error-notifications).

**Secondary Failover Group Parameters**

`secondary_name`
:   Specifies the identifier for the secondary failover group. The identifier must start with an alphabetic character and cannot contain
    spaces or special characters unless the identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in
    double quotes are also case-sensitive. For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    The identifiers for the secondary failover group (`secondary_name`) and primary failover group (`name`) can be, but
    are not required to be, identical.

`AS REPLICA OF org_name.source_account_name.name`
:   Specifies the identifier of the primary failover group from which to create a secondary failover group.

    `org_name`
    :   Name of your Snowflake organization.

    `source_account_name`
    :   Source account from which you are enabling replication and failover of the specified objects.

    `name`
    :   Identifier for the primary failover group in the source account.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE FAILOVER GROUP | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
| MONITOR | Database | To add a database to a failover group, the active role must have the MONITOR privilege on the database. |
| USAGE | External volume | To add an external volume to a failover group, the active role must have the USAGE privilege on the external volume. |
| OWNERSHIP | Share | To add a share to a failover group, the active role must have the OWNERSHIP privilege on the share. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Identifiers for failover groups and replication groups in an account must be unique.
- Objects other than databases, external volumes, and shares must be in the same failover group.
- A database can only be added to one failover group.
- An external volume can only be added to one replication or failover group.
- [Inbound shares](/user-guide/data-share-consumers) (shares from providers) *cannot* be added to a replication or failover group.
- To retrieve the set of accounts in your organization that are enabled for replication, use
  [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts).
- To retrieve the list of failover groups in your organization, use [SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups#label-show-failover-groups).
- If there are account objects (for example, users or roles) in a target account that you do not want to drop during replication,
  use the [SYSTEM$LINK\_ACCOUNT\_OBJECTS\_BY\_NAME](/sql-reference/functions/system_link_account_objects_by_name) system function to apply a global identifier to objects
  created by means other than replication. For more information, see
  [Apply Global IDs to Objects Created by Scripts in Target Accounts](/user-guide/account-replication-config#label-apply-global-ids-to-objects) before
  you create a failover group.
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
- For an account that is newly upgraded to Business Critical Edition (or higher), it might take up to 12 hours for failover capabilities to
  become available.
- When `OPTIMIZED_REFRESH = TRUE`, the failover group must have a REPLICATION\_SCHEDULE with an interval of 6 hours or less. The property
  can be set on the primary failover group only. For details, see [Optimized refresh for failover groups](/user-guide/account-replication-config#label-optimized-refresh).

## Examples

### Create a failover group to enable replication and failover for a database

**Executed on source account**

Create a failover group named `myfg` to enable replication and failover of database `db1` from the source account to the
target account `myaccount2`. Set the replication schedule for `myfg` to refresh the database every 10 minutes:

Copy code

```
CREATE FAILOVER GROUP myfg
    OBJECT_TYPES = DATABASES
    ALLOWED_DATABASES = db1
    ALLOWED_ACCOUNTS = myorg.myaccount2
    REPLICATION_SCHEDULE = '10 MINUTE';
```

**Executed on target account**

Create a failover group in the target account as a replica of the failover group `myfg` in the source account:

Copy code

```
CREATE FAILOVER GROUP myfg
    AS REPLICA OF myorg.myaccount1.myfg;
```

### Create a failover group to enable replication and failover for multiple databases

**Executed on source account**

Create a failover group named `myfg` in the source account to enable replication and failover of databases
`db1`, `db2`, `db3` from the source to the `myaccount2` account. Set the replication schedule for `myfg`
to refresh the databases every 10 minutes:

Copy code

```
CREATE FAILOVER GROUP myfg
    OBJECT_TYPES = DATABASES
    ALLOWED_DATABASES = db1, db2, db3
    ALLOWED_ACCOUNTS = myorg.myaccount2
    REPLICATION_SCHEDULE = '10 MINUTE';
```

**Executed on target account**

Create a failover group in the target account as a replica of the failover group `myfg` in the source account:

Copy code

```
CREATE FAILOVER GROUP myfg
    AS REPLICA OF myorg.myaccount1.myfg;
```

### Create a failover group to enable replication and failover for account objects

**Executed on source account**

Create a failover group named `myfg` in the source account to enable replication and failover of users, roles, warehouses, resource
monitors, storage integrations, and notification integrations from the source account to the `myaccount2` account:

Copy code

```
CREATE FAILOVER GROUP myfg
    OBJECT_TYPES = USERS, ROLES, WAREHOUSES, RESOURCE MONITORS, INTEGRATIONS
    ALLOWED_INTEGRATION_TYPES = STORAGE INTEGRATIONS, NOTIFICATION INTEGRATIONS
    ALLOWED_ACCOUNTS = myorg.myaccount2
    REPLICATION_SCHEDULE = '10 MINUTE';
```

**Executed on target account**

Create a failover group in the target account as a replica of the failover group `myfg` in the source account:

Copy code

```
CREATE FAILOVER GROUP myfg
    AS REPLICA OF myorg.myaccount1.myfg;
```

### Create a failover group to enable replication and failover for profiles

**Executed on source account**

Create a failover group named `myfg` in the source account to enable replication and failover of users, roles, and profiles from the source account to the `myaccount2` account:

Copy code

```
CREATE FAILOVER GROUP myfg
    OBJECT_TYPES = USERS, ROLES, PROFILES
    ALLOWED_ACCOUNTS = myorg.myaccount2;
```

**Executed on target account**

Create a failover group in the target account as a replica of the failover group `myfg` in the source account:

Copy code

```
CREATE FAILOVER GROUP myfg
    AS REPLICA OF myorg.myaccount1.myfg;
ALTER FAILOVER GROUP myfg REFRESH;
```

**Confirm replication of profiles**

To confirm that profiles are replicated on the target account, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) on the target account.
2. Navigate to **Marketplace** » **Provider Studio** » **Profiles** to view the profiles that were replicated from the source account.

### Create a failover group to enable replication and failover for security integrations and network policies

For more information and examples for replicating security integrations and network policies,
see [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations).

### Create a failover group that uses optimized refresh

**Executed on source account**

Create a failover group named `myfg` that uses [optimized refresh](/user-guide/account-replication-config#label-optimized-refresh) to
replicate database `db1` to the target account `myaccount2`. The replication schedule refreshes the failover group every 10 minutes:

Copy code

```
CREATE FAILOVER GROUP myfg
    OBJECT_TYPES = DATABASES
    ALLOWED_DATABASES = db1
    ALLOWED_ACCOUNTS = myorg.myaccount2
    REPLICATION_SCHEDULE = '10 MINUTE'
    OPTIMIZED_REFRESH = TRUE;
```

**Executed on target account**

Create the secondary failover group as usual. No additional property is required on the secondary:

Copy code

```
CREATE FAILOVER GROUP myfg
    AS REPLICA OF myorg.myaccount1.myfg;
```
