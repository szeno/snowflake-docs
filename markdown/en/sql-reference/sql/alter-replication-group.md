# ALTER REPLICATION GROUP

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Modifies the properties for an existing [replication group](/user-guide/account-replication-intro#label-replication-and-failover-groups).

From the source account, you can perform the following actions:

- Rename the replication group.
- Reset the list of specified object types enabled for replication.
- Set or update the replication schedule for automatic refresh of secondary replication groups.
- Add or remove account objects of the following types to or from a replication group:

  - Databases
  - External volumes
  - Shares
  - Security integrations
  - API integrations
  - Storage integrations
  - External access integrations
  - Certain types of notification integrations (see [Integration replication](/user-guide/account-replication-intro#label-account-replication-integrations))
- Add or remove target accounts enabled for replication.
- Move databases or shares from one replication group to another replication group.

From the target account, you can perform the following actions:

- Refresh objects in the target account from the source account.
- Suspend scheduled replication.
- Resume scheduled replication.

See also:
:   [CREATE REPLICATION GROUP](/sql-reference/sql/create-replication-group) , [DROP REPLICATION GROUP](/sql-reference/sql/drop-replication-group) , [SHOW REPLICATION GROUPS](/sql-reference/sql/show-replication-groups),
    [SYSTEM$SCHEDULE\_ASYNC\_REPLICATION\_GROUP\_REFRESH](/sql-reference/functions/system_schedule_async_replication_group_refresh)

## Syntax

**Source Account**

Copy code

```
ALTER REPLICATION GROUP [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER REPLICATION GROUP [ IF EXISTS ] <name> SET
  [ OBJECT_TYPES = <object_type> [ , <object_type> , ... ] ]
  [ ALLOWED_DATABASES = <db_name> [ , <db_name> , ... ] ]
  [ ALLOWED_EXTERNAL_VOLUMES = <external_volume_name> [ , <external_volume_name> , ... ] ]
  [ ALLOWED_SHARES = <share_name> [ , <share_name> , ... ] ]

ALTER REPLICATION GROUP [ IF EXISTS ] <name> SET
  OBJECT_TYPES = INTEGRATIONS [ , <object_type> , ... ]
  ALLOWED_INTEGRATION_TYPES = <integration_type_name> [ , <integration_type_name> ... ]

ALTER REPLICATION GROUP [ IF EXISTS ] <name> SET
  COMMENT = '<string_literal>'

ALTER REPLICATION GROUP [ IF EXISTS ] <name> SET
  REPLICATION_SCHEDULE = '{ <num> MINUTE | USING CRON <expr> <time_zone> }'

ALTER REPLICATION GROUP [ IF EXISTS ] <name> SET
  ERROR_INTEGRATION = <integration_name>

ALTER REPLICATION GROUP [ IF EXISTS ] <name> SET
  TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER REPLICATION GROUP [ IF EXISTS ] <name> UNSET
  { COMMENT | REPLICATION_SCHEDULE | ERROR_INTEGRATION } [ , ... ]

ALTER REPLICATION GROUP [ IF EXISTS ] <name> UNSET
  TAG <tag_name> [ , <tag_name> ... ]

ALTER REPLICATION GROUP [ IF EXISTS ] <name>
  ADD <db_name> [ , <db_name> ,  ... ] TO ALLOWED_DATABASES

ALTER REPLICATION GROUP [ IF EXISTS ] <name>
  MOVE DATABASES <db_name> [ , <db_name> ,  ... ] TO REPLICATION GROUP <move_to_rg_name>

ALTER REPLICATION GROUP [ IF EXISTS ] <name>
  REMOVE <db_name> [ , <db_name> ,  ... ] FROM ALLOWED_DATABASES

ALTER REPLICATION GROUP [ IF EXISTS ] <name>
  ADD <external_volume_name> [ , <external_volume_name> ,  ... ] TO ALLOWED_EXTERNAL_VOLUMES

ALTER REPLICATION GROUP [ IF EXISTS ] <name>
  MOVE EXTERNAL VOLUMES <external_volume_name> [ , <external_volume_name> ,  ... ] TO REPLICATION GROUP <move_to_rg_name>

ALTER REPLICATION GROUP [ IF EXISTS ] <name>
  REMOVE <external_volume_name> [ , <external_volume_name> ,  ... ] FROM ALLOWED_EXTERNAL_VOLUMES

ALTER REPLICATION GROUP [ IF EXISTS ] <name>
  ADD <share_name> [ , <share_name> ,  ... ] TO ALLOWED_SHARES

ALTER REPLICATION GROUP [ IF EXISTS ] <name>
  MOVE SHARES <share_name> [ , <share_name> ,  ... ] TO REPLICATION GROUP <move_to_rg_name>

ALTER REPLICATION GROUP [ IF EXISTS ] <name>
  REMOVE <share_name> [ , <share_name> ,  ... ] FROM ALLOWED_SHARES

ALTER REPLICATION GROUP [ IF EXISTS ] <name>
  ADD <org_name>.<target_account_name> [ , <org_name>.<target_account_name> ,  ... ] TO ALLOWED_ACCOUNTS
  [ IGNORE EDITION CHECK ]

ALTER REPLICATION GROUP [ IF EXISTS ] <name>
  REMOVE <org_name>.<target_account_name> [ , <org_name>.<target_account_name> ,  ... ] FROM ALLOWED_ACCOUNTS
```

**Target Account**

Copy code

```
ALTER REPLICATION GROUP [ IF EXISTS ] <name> REFRESH

ALTER REPLICATION GROUP [ IF EXISTS ] <name> SUSPEND [ IMMEDIATE ]

ALTER REPLICATION GROUP [ IF EXISTS ] <name> RESUME
```

## Parameters

**Source Account**

`name`
:   Specifies the identifier for the replication group.

`RENAME TO new_name`
:   `new_name`
    :   Specifies the new identifier for the replication group. The new identifier cannot be used if the identifier is already in place for a
        different replication or failover group.

        For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Specifies properties to set for the replication group (separated by blank spaces, commas, or new lines).

    `OBJECT_TYPES = object_type [ , object_type , ... ]`
    :   Reset the list of object types to replicate from the source account to target account(s).

        Note

        For database, external volume, and share objects:

        - If DATABASES, EXTERNAL VOLUMES, or SHARES are included in the OBJECT\_TYPES list, and remain in the OBJECT\_TYPES list after
          the list is reset, the respective allowed objects list (ALLOWED\_DATABASES, ALLOWED\_EXTERNAL\_VOLUMES, or ALLOWED\_SHARES) remains
          unchanged.
        - If the OBJECT\_TYPES list is reset to add or remove DATABASES, the ALLOWED\_DATABASES list is set to NULL.
        - If the OBJECT\_TYPES list is reset to add or remove EXTERNAL VOLUMES, the ALLOWED\_EXTERNAL\_VOLUMES list is set to NULL.
        - If the OBJECT\_TYPES list is reset to add or remove SHARES, the ALLOWED\_SHARES list is set to NULL.
        - Use the ADD, MOVE, and REMOVE clauses to modify the list of allowed database, external volume, or share objects.

        The following object types are supported:

        > ACCOUNT PARAMETERS:
        > :   *Requires Business Critical Edition (or higher).*
        >
        >     All account-level parameters. This includes [account parameters](/sql-reference/parameters#label-account-parameters) and parameters that can be
        >     [set for your account](/user-guide/admin-account-management).
        >
        > DATABASES:
        > :   Add database objects to the list of object types. If database objects were already included in the list of specified object
        >     types, the `ALLOWED_DATABASES` list remains unchanged. To modify the list of databases, use the
        >     ADD, MOVE, or REMOVE clauses.
        >
        > EXTERNAL VOLUMES:
        > :   Add external volume objects to the list of object types. If external volume objects are included in the list of specified object types,
        >     the `ALLOWED_EXTERNAL_VOLUMES` parameter must be set. To modify the list of external volumes, use the ADD, MOVE, or REMOVE clauses.
        >
        > INTEGRATIONS:
        > :   *Requires Business Critical Edition (or higher).*
        >
        >     Currently, only security, API, storage, external access, and certain types of notification integrations are supported.
        >     For details, see [Integration replication](/user-guide/account-replication-intro#label-account-replication-integrations).
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
        > :   Add share objects to the list of object types. If share objects were already included in the list of specified object types, the
        >     `ALLOWED_SHARES` list remains unchanged. To modify the list of shares, use the ADD, MOVE, or REMOVE clauses.
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

    `ALLOWED_DATABASES = db_name [ , db_name , ... ]`
    :   Specifies the database or list of databases for which you are enabling replication from the source account to the target
        account. In order for you to set this parameter, the `OBJECT_TYPES` list must include `DATABASES`.

        `db_name`
        :   Specifies the identifier for the database.

    `ALLOWED_EXTERNAL_VOLUMES = external_volume_name [ , external_volume_name , ... ]`
    :   [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

        Available to all accounts.

        Specifies the external volume or list of external volumes for which you are enabling replication from the source account to the target
        account. For you to set this parameter, the `OBJECT_TYPES` list must include `EXTERNAL VOLUMES`.

        `external_volume_name`
        :   Specifies the identifier for the external volume.

    `ALLOWED_SHARES = share_name [ , share_name , ... ]`
    :   Specifies the share or list of shares for which you are enabling replication from the source account to the target account.
        For you to set this parameter, the `OBJECT_TYPES` list must include `SHARES`.

        `share_name`
        :   Specifies the identifier for the share.

    Note

    If the ALLOWED\_DATABASES, ALLOWED\_EXTERNAL\_VOLUMES, or ALLOWED\_SHARES lists are modified, any objects that were previously in the list and removed
    will be dropped in any target account with a linked secondary replication group when the next refresh operation occurs.

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

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the replication group.

        Default:
        :   `NULL`

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

        Default:
        :   `NULL`

    `ERROR_INTEGRATION = integration_name`
    :   Specifies the name of the notification integration to use to email/push notifications when refresh errors occur for the replication
        group. For more details, see [Error notifications for replication and failover groups](/user-guide/account-replication-error-notifications).

        Default:
        :   `NULL`

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`ADD db_name [ , db_name , ... ] TO ALLOWED_DATABASES`
:   Specifies a comma-separated list of databases to add to the list of databases enabled for replication. To add a database, DATABASES must
    be included in the list of specified object types. If the list of object types does not already include DATABASES, you must add it.

    > `db_name`
    > :   Specifies the identifier for the database.

`MOVE DATABASES db_name [ , db_name , ... ] TO REPLICATION GROUP move_to_rg_name`
:   Specifies a comma-separated list of databases to move from one replication group to another replication group. The replication group the
    databases are being moved to must include DATABASES in the list of specified object types.

    > `db_name`
    > :   Specifies the identifier for the database.
    >
    > `move_to_rg_name`
    > :   Specifies the identifier for the replication group the databases are being moved to.

`REMOVE db_name [ , db_name , ... ] FROM ALLOWED_DATABASES`
:   Specifies a comma-separated list of database to remove from the list of databases enabled for replication.

    Note

    When you remove a database from a primary replication group, the database is dropped in any target account with a linked secondary
    replication group when the next refresh operation occurs.

    To avoid dropping databases in the target account, you can drop the secondary replication group *before* the next time the modified
    primary replication group is replicated to the target account. When you drop the secondary replication group, read-only secondary
    databases that were included in the group become standalone read-write databases in the target account.

`ADD external_volume_name [ , external_volume_name , ... ] TO ALLOWED_EXTERNAL_VOLUMES`
:   Specifies a comma-separated list of external volumes to add to the list of external volumes enabled for replication. To add an external volume,
    EXTERNAL VOLUMES must be included in the list of specified object types. If the list of object types does not already include EXTERNAL VOLUMES,
    you must add it.

    > `external_volume_name`
    > :   Specifies the identifier for the external volume.

`MOVE EXTERNAL VOLUMES external_volume_name [ , external_volume_name , ... ] TO REPLICATION GROUP move_to_rg_name`
:   Specifies a comma-separated list of external volumes to move from one replication group to another replication group. The replication group the
    external volumes are being moved to must include EXTERNAL VOLUMES in the list of specified object types.

    > `db_name`
    > :   Specifies the identifier for the external volume.
    >
    > `move_to_rg_name`
    > :   Specifies the identifier for the replication group the external volumes are being moved to.

`REMOVE external_volume_name [ , external_volume_name , ... ] FROM ALLOWED_EXTERNAL_VOLUMES`
:   Specifies a comma-separated list of external volumes to remove from the list of external volumes enabled for replication.

    Note

    When you remove an external volume from a primary replication group, the external volume is dropped in any target account with a
    linked secondary replication group when the next refresh operation occurs.

    To avoid dropping external volumes in the target account, you can drop the secondary replication group before the next time the
    modified primary replication group is replicated to the target account. When you drop the secondary replication group, read-only
    secondary external volumes that were included in the group become standalone read-write external volumes in the target account.

`ADD share_name [ , share_name , ... ] TO ALLOWED_SHARES`
:   Specifies a comma-separated list of shares to the list of shares for replication. To add a share, SHARES must be included in the list of
    specified object types. If the list of object types doesn’t already include SHARES, you must add it.

    > `share_name`
    > :   Specifies the identifier for the share.

`MOVE SHARES share_name [ , share_name , ... ] TO REPLICATION GROUP move_to_rg_name`
:   Specifies a comma-separated list of shares to move from one replication group to another replication group. The replication group the
    shares are being moved to must include SHARES in the list of specified object types.

    > `share_name`
    > :   Specifies the identifier for the share.
    >
    > `move_to_rg_name`
    > :   Specifies the identifier for the replication group the shares are being moved to.

`REMOVE share_name [ , share_name , ... ] FROM ALLOWED_SHARES`
:   Specifies a comma-separated list of shares to remove from the list of shares enabled for replication.

    Note

    When you remove a share from a primary replication group, the share is dropped in any target account with a linked secondary
    replication group when the next refresh operation occurs.

`ADD org_name.target_account_name [ , org_name.target_account_name , ... ] TO ALLOWED_ACCOUNTS`
:   Specifies a comma-separated list of target accounts to add to the primary replication group to enable replication of specified objects in
    the source account to the target account.

    > `org_name`
    > :   Name of your Snowflake organization.
    >
    > `target_account_name`
    > :   Target account to which you are enabling replication of the specified objects.

`REMOVE org_name.target_account_name [ , org_name.target_account_name , ... ] FROM ALLOWED_ACCOUNTS`
:   Specifies a comma-separated list of target accounts to remove from the primary replication group to disable replication of specified
    objects in the source account to the target account.

    > `org_name`
    > :   Name of your Snowflake organization.
    >
    > `target_account_name`
    > :   Target account to which you are disabling replication of the specified objects.

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

**Target Account**

`name`
:   Specifies the identifier for the replication group.

`REFRESH`
:   Refreshes the objects in the target (current) account from the source account.

`SUSPEND [ IMMEDIATE ]`
:   Suspends the scheduled refresh of the secondary replication group (if the primary replication group has automatically scheduled refresh set
    using the `REPLICATION_SCHEDULE` property).

    The optional `IMMEDIATE` clause cancels a scheduled refresh operation that is currently in progress for the secondary replication group
    (if there is one). Note that there might be a slight delay between the time that the statement returns and the time that the cancellation
    of the refresh operation is finished.

`RESUME`
:   Resume scheduled refresh of the secondary replication group (if the primary replication group has automatically scheduled refresh set
    using the `REPLICATION_SCHEDULE` property).

`UNSET ...`
:   Specifies one (or more) properties to unset for the replication group, which resets them to the defaults:

    - `COMMENT`
    - `REPLICATION_SCHEDULE`
    - `ERROR_INTEGRATION`
    - `TAG tag_name [ , tag_name ... ]`

    You can reset multiple properties with a single ALTER statement; however, each property must be separated by
    a comma. Also, when resetting a property, you only specify the name; no value is required.

## Usage notes

- The following minimal privileges are required:

  - To refresh a secondary replication group using ALTER REPLICATION GROUP … REFRESH, the active, primary role must have either the
    OWNERSHIP or REPLICATE privilege on the replication group.
  - To make any other changes to the replication group, only a user with a role with the OWNERSHIP privilege on the group can execute
    this SQL command.
  - To add a database to a replication group, the active role must have the MONITOR privilege on the database.
  - To add an external volume to a replication group, the active role must have the USAGE privilege on the external volume.
  - To add a share to a replication group, the active role must have the OWNERSHIP privilege on the share.
- Identifiers for failover groups and replication groups in an account must be unique.
- Objects other than databases, external volumes, and shares must be in the same replication group.
- A database can only be added to one replication or failover group.
- An external volume can only be added to one replication or failover group.
- To move databases, external volumes, or shares from one replication group (the move-from group) to another replication group (the move-to group):

  - Both groups must be of the same type: REPLICATION GROUP.
  - If the last database in the move-from group is moved to another group, the `allowed_databases` property for the move-from group
    is set to NULL. The same behavior applies to shares and external volumes.
  - If the move-to group doesn’t have the object type that is being moved (`databases`, `external volumes`, or `shares`) in the `object_types`
    list, it must be explicitly added to the move-to group before you move the objects.
- If database, external volume, or share objects are removed from a primary replication group (by using the REMOVE parameter or SET parameter to
  modify the ALLOWED\_DATABASES, ALLOWED\_EXTERNAL\_VOLUMES, or ALLOWED\_SHARES lists), those objects are dropped in any target account with a
  linked secondary replication group when the next refresh operation occurs.

  To avoid dropping these objects in the target account, you can drop the secondary replication group *before* the next time the modified
  primary replication group is replicated to the target account.
- [Inbound shares](/user-guide/data-share-consumers) (shares from providers) *cannot* be added to a replication or failover group.
- To retrieve the list of accounts in your organization that are enabled for replication, use the
  [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts) command.
- To retrieve the list of replication groups in your organization, use the [SHOW REPLICATION GROUPS](/sql-reference/sql/show-replication-groups#label-show-replication-groups) command. The
  `allowed_accounts` column lists all target accounts enabled for replication from a source account.
- Automatically [scheduled refresh operations](/user-guide/account-replication-intro#label-replication-schedule) are executed using the role with the OWNERSHIP
  privilege on the group. If a scheduled refresh operation fails due to insufficient privileges, grant the required privileges
  to the role with the OWNERSHIP privilege on the group.
- The ALTER REPLICATION GROUP … SUSPEND IMMEDIATE command doesn’t cancel an in-progress refresh operation if it was manually triggered.
  For more information, see [Cancel an in-progress refresh operation that wasn’t automatically scheduled](/user-guide/account-replication-failover-failback#label-cancel-manually-triggered-refresh-operation).
- Canceling an in-progress refresh operation that is in the SECONDARY\_DOWNLOADING\_METADATA or SECONDARY\_DOWNLOADING\_DATA phase might
  result in an inconsistent state on the target account. For more information see [View the current phase of an in-progress refresh operation](/user-guide/account-replication-failover-failback#label-view-current-phase-of-refresh-operation).

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

### Executed from the source account

Add `myorg.myaccount3` to the list of target accounts to which replication of specified objects from the source account is enabled:

Copy code

```
ALTER REPLICATION GROUP myrg ADD myorg.myaccount3 TO ALLOWED_ACCOUNTS;
```

Reset the object types list for replication in the source account:

Copy code

```
ALTER REPLICATION GROUP myrg SET
  OBJECT_TYPES = DATABASES, SHARES;
```

Add database `db1` to the list of databases enabled for replication:

Copy code

```
ALTER REPLICATION GROUP myrg
  ADD db1 to ALLOWED_DATABASES;
```

Add share `s2` to the list of shares enabled for replication:

Copy code

```
ALTER REPLICATION GROUP myrg
  ADD s2 TO ALLOWED_SHARES;
```

Move database `db1` to another replication group, `myrg2`:

Copy code

```
ALTER REPLICATION GROUP myrg
  MOVE DATABASES db1 TO REPLICATION GROUP myrg2;
```

Set the scheduled refresh interval time to 15 minutes:

Copy code

```
ALTER REPLICATION GROUP myrg SET
  REPLICATION_SCHEDULE = '15 MINUTE';
```

### Executed from the target account

Refresh objects in the replication group `myrg` in the target account:

Copy code

```
ALTER REPLICATION GROUP myrg REFRESH;
```

Suspend automatic refreshes:

Copy code

```
ALTER REPLICATION GROUP myrg SUSPEND;
```
