# CREATE RESOURCE MONITOR

Creates a new [resource monitor](/user-guide/resource-monitors). This command can only be executed by account administrators.

See also:
:   [ALTER RESOURCE MONITOR](/sql-reference/sql/alter-resource-monitor) , [DROP RESOURCE MONITOR](/sql-reference/sql/drop-resource-monitor) , [SHOW RESOURCE MONITORS](/sql-reference/sql/show-resource-monitors) , [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) , [ALTER ACCOUNT](/sql-reference/sql/alter-account)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] RESOURCE MONITOR [ IF NOT EXISTS ] <name> WITH
                      [ CREDIT_QUOTA = <number> ]
                      [ FREQUENCY = { MONTHLY | DAILY | WEEKLY | YEARLY | NEVER } ]
                      [ START_TIMESTAMP = { <timestamp> | IMMEDIATELY } ]
                      [ END_TIMESTAMP = <timestamp> ]
                      [ NOTIFY_USERS = ( <user_name> [ , <user_name> , ... ] ) ]
                      [ TRIGGERS triggerDefinition [ triggerDefinition ... ] ]
```

Where:

> Copy code
>
> ```
> triggerDefinition ::=
>     ON <threshold> PERCENT DO { SUSPEND | SUSPEND_IMMEDIATE | NOTIFY }
> ```

## Required parameters

`name`
:   Identifier for the resource monitor; must be unique for your account.

    The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier string
    is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`CREDIT_QUOTA = num`
:   The number of credits allocated to the resource monitor per frequency interval. When total usage for all warehouses assigned to the
    monitor reaches this number for the current frequency interval, the resource monitor is considered to be at 100% of quota.

    If a value is not specified for a resource monitor, the monitor has no quota and will never reach 100% usage within the specified interval.

    Default: No value (i.e. no credit quota)

`FREQUENCY = MONTHLY | DAILY | WEEKLY | YEARLY | NEVER`
:   The frequency interval at which the credit usage resets to `0`.

    If you set a frequency for a resource monitor, you must also set `START_TIMESTAMP`.

    If you specify `NEVER` for the frequency, the credit usage for the warehouse does not reset.

    Default: No value (i.e. legacy behavior, whereby the credit quota resets at the beginning of each calendar month)

`START_TIMESTAMP = timestamp | IMMEDIATELY`
:   The date and time when the resource monitor starts monitoring credit usage for the assigned warehouses.

    If you set a timestamp for a resource monitor, you must also set `FREQUENCY`.

    If you specify `IMMEDIATELY` for the start timestamp, the current timestamp is used.

    If you specify a date without a time, the current time is used.

    If you set a time without specifying a time zone, UTC is used as the default time zone.

    Default: No value (i.e. legacy behavior, whereby the resource monitor starts monitoring warehouses immediately)

`END_TIMESTAMP = timestamp`
:   The date and time when the resource monitor suspends the assigned warehouses.

    Default: No value (i.e. no warehouse suspension date)

`NOTIFY_USERS = ( user_name [ , user_name , ... ] )`
:   Specifies the list of users to receive email notifications on resource monitors. If a user identifier includes spaces or special
    characters or is case-sensitive, then the identifier must be enclosed in double quotes (e.g. “Mary Smith”). See
    [Identifier requirements](/sql-reference/identifiers-syntax) for details.

    The user identifier, `user_name`, is the value of the `name` column from the output of
    [SHOW USERS](/sql-reference/sql/show-users).

    Each user listed must have a verified email address. For instructions on verifying email addresses in the web interface, see [Verify your email address](/user-guide/ui-support#label-snowsight-verifying-email-address).

    Email notifications for non-administrator users do not supersede email notifications for administrators. Any account administrators that
    have [enabled email notifications](/user-guide/resource-monitors#label-enabling-notifications) will continue to receive email notifications.

    Note

    - The following limitations apply for non-administrator users:
      - Non-administrator users can only receive [notifications](/user-guide/resource-monitors#label-resource-monitor-notifications)
        for [warehouse monitors](/user-guide/resource-monitors#label-resource-monitors-type).
      - Non-administrator users are notified by email but can’t see notifications in Snowsight.
      - Non-administrator users can’t create resource monitors.
      - Non-administrator users can’t assign other users to be notified.

`TRIGGERS ...` (aka *actions*)
:   Specifies one or more triggers for the resource monitor. Each trigger definition consists of the following:

    > `ON threshold PERCENT`
    > :   A numeric value specified as a percentage of the credit quota for the resource monitor; values larger than `100` are supported.
    >     Once usage reaches this threshold for the current frequency interval, the trigger fires.
    >
    > `DO SUSPEND | SUSPEND_IMMEDIATE | NOTIFY`
    > :   Specifies the action performed by the trigger when the threshold is reached:
    >
    >     - `SUSPEND`: Suspend all assigned warehouses while allowing currently running queries to complete. No new queries can be executed
    >       by the warehouses until the credit quota for the resource monitor is increased. In addition, this action sends a notification to all
    >       users who have enabled notifications for themselves.
    >     - `SUSPEND_IMMEDIATE`: Suspend all assigned warehouses immediately and cancel any currently running queries or statements using
    >       the warehouses. In addition, this action sends a notification to all users who have enabled notifications for themselves.
    >     - `NOTIFY`: Send a notification (to all account administrators with notifications enabled), but do not take any other action.

    Default: No value (i.e. resource monitor performs no actions)

## Usage notes

- Triggers are optional; however, at least one trigger must be added to a resource monitor before it can perform any actions.
- Each resource monitor supports up to a maximum of 5 `NOTIFY` action triggers.
- After a resource monitor is created, it must be assigned to a warehouse or account before it can perform any monitoring actions:

  - To assign a warehouse to a resource monitor, use [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) (or [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse) if you are creating the warehouse).
  - To assign a resource monitor at the account level, use [ALTER ACCOUNT](/sql-reference/sql/alter-account). The NOTIFY\_USERS parameter must be null.
- To view all resource monitors created in your account and their assignment, use the [SHOW RESOURCE MONITORS](/sql-reference/sql/show-resource-monitors) command. The command
  output displays `NULL` in the `level` column for resource monitors that are not assigned to the account or any warehouses
  and, therefore, are not monitoring any credit usage.
- If `frequency` and `start_timestamp` parameters are set on a resource monitor, the day for the credit usage reset is
  calculated based on those parameters. The time the credit usage resets to `0` is 12:00 AM UTC regardless of the time specified in
  `start_timestamp`.
- If you specify an `end_timestamp`, monitoring ends at that specified date and time and all assigned warehouses are suspended
  at that date and time even if the credit quota has not been reached.

  When this occurs, a notification is sent that states the resource monitor has reached a percentage of its quota and has triggered a
  suspend immediate action. The percentage of the quota reflects the number of credits used in the current interval up to the end date
  and might not be a threshold you specified.
- If there are non-administrator users in the notification list, the following notes apply:

  - If any user in the notification list does not have a [verified email](/user-guide/notifications/email-notifications#label-email-notification-verify-address),
    the SQL statement fails.
  - If any user in the notification list changes their email address and does not verify the new email address, the
    notification silently fails.
  - The notification list is limited to a maximum number of 5 non-administrator users.
  - Account administrators can view the notification list of non-administrator users in the output of
    [SHOW RESOURCE MONITORS](/sql-reference/sql/show-resource-monitors) in the `notify_user` column.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

Important

To receive notifications generated by resource monitors, account administrators and non-administrator users in the notification
list must explicitly enable notifications in their preferences. In addition, to receive email notifications, users must have a
verified email in their preferences. Preferences can only
be set in the Snowflake web interface. For more information, see [Enabling receipt of notifications](/user-guide/resource-monitors#label-enabling-notifications).

## Examples

Create a resource monitor named `limiter` with 3 triggers:

> Copy code
>
> ```
> CREATE OR REPLACE RESOURCE MONITOR limiter
>   WITH CREDIT_QUOTA = 5000
>   TRIGGERS ON 75 PERCENT DO NOTIFY
>            ON 100 PERCENT DO SUSPEND
>            ON 110 PERCENT DO SUSPEND_IMMEDIATE;
> ```

Create a resource monitor to send notifications to three users when 75% of the credit quota is reached. In this example, the
`user_name` for two of the users includes a space and must be enclosed in double quotes:

> Copy code
>
> ```
> CREATE OR REPLACE RESOURCE MONITOR limiter
>   WITH CREDIT_QUOTA = 5000
>        NOTIFY_USERS = (JDOE, "Jane Smith", "John Doe")
>   TRIGGERS ON 75 PERCENT DO NOTIFY
>            ON 100 PERCENT DO SUSPEND
>            ON 110 PERCENT DO SUSPEND_IMMEDIATE;
> ```
