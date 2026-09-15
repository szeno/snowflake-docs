# ALTER RESOURCE MONITOR

Modifies the properties and triggers for an existing [resource monitor](/user-guide/resource-monitors). Use this command to
increase or decrease the credit quota, change the
scheduling information, or change/replace the triggers for a resource monitor.

See also:
:   [CREATE RESOURCE MONITOR](/sql-reference/sql/create-resource-monitor) , [DROP RESOURCE MONITOR](/sql-reference/sql/drop-resource-monitor) , [SHOW RESOURCE MONITORS](/sql-reference/sql/show-resource-monitors) , [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) , [ALTER ACCOUNT](/sql-reference/sql/alter-account)

## Syntax

Copy code

```
ALTER RESOURCE MONITOR [ IF EXISTS ] <name> [ SET { [ CREDIT_QUOTA = <num> ]
                                                    [ FREQUENCY = { MONTHLY | DAILY | WEEKLY | YEARLY | NEVER } ]
                                                    [ START_TIMESTAMP = { <timestamp> | IMMEDIATELY } ]
                                                    [ END_TIMESTAMP = <timestamp> ]
                                                    [ NOTIFY_USERS = ( <user_name> [ , <user_name> , ... ] ) ] } ]
                                            [ TRIGGERS triggerDefinition [ triggerDefinition ... ] ]
```

Where:

> Copy code
>
> ```
> triggerDefinition ::=
>    ON <threshold> PERCENT DO { SUSPEND | SUSPEND_IMMEDIATE | NOTIFY }
> ```

## Parameters

`name`
:   Specifies the identifier for the resource monitor to alter. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`SET ...`
:   `CREDIT_QUOTA = num`
    :   Specifies the number of credits allocated to the resource monitor per frequency interval. When total usage for all warehouses assigned to
        the monitor reaches this number for the current frequency interval, the resource monitor is considered to be at 100% of quota.

        If a value is not specified for a resource monitor, the monitor has no quota and will never reach 100% usage within the specified interval.

    `FREQUENCY = MONTHLY | DAILY | WEEKLY | YEARLY | NEVER`
    :   The frequency interval at which the credit usage resets to `0`.

        If you specify `NEVER` for the frequency, the credit usage for the warehouse does not reset.

    `START_TIMESTAMP = timestamp | IMMEDIATELY`
    :   The date and time when the resource monitor starts monitoring credit usage for the assigned warehouses.

        If you specify `IMMEDIATELY` for the start timestamp, the current timestamp is used.

        If you specify a date without a time, the current time is used.

        If you set a time without specifying a time zone, UTC is used as the default time zone.

    `END_TIMESTAMP = timestamp`
    :   The date and time when the resource monitor suspends the assigned warehouses.

    `NOTIFY_USERS = ( user_name [ , user_name , ... ] )`
    :   Specifies the list of users to receive email notifications on resource monitors. If a user identifier includes spaces or special
        characters or is case-sensitive, then the identifier must be enclosed in double quotes (e.g. “Mary Smith”). See
        [Identifier requirements](/sql-reference/identifiers-syntax) for details.

        The user identifier, `user_name`, is the value of the `name` column from the output of
        [SHOW USERS](/sql-reference/sql/show-users).

        Each user listed must have a verified email address. For instructions on verifying email addresses in the web interface, see: [Verify your email address](/user-guide/ui-support#label-snowsight-verifying-email-address).

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
:   Specifies one or more triggers for the resource monitor. Each trigger definition consists of:

    - `ON threshold PERCENT` (usage percentage; values larger than `100` are supported)
    - `DO SUSPEND | SUSPEND_IMMEDIATE | NOTIFY` (action to perform when the threshold is reached).

    For more details, see [CREATE RESOURCE MONITOR](/sql-reference/sql/create-resource-monitor).

## Usage notes

- If a `SUSPEND` or `SUSPEND_IMMEDIATE` trigger is active for a resource monitor and the trigger threshold has been reached for
  the specified frequency interval, thereby preventing all assigned warehouses from being started/resumed, you can use this command to
  either increase the credit quota above the trigger threshold or replace the trigger with a new trigger with a higher threshold.

  Once the credit quota or trigger threshold for the resource monitor has been increased, assigned warehouses can be started or resumed.
- The `TRIGGERS` parameter is not additive; it removes all existing triggers for the resource monitor and replaces them
  with the specified triggers.

  As a result, to make additions to the existing triggers, you must specify the new triggers and replicate the existing triggers.

  Replicating an existing trigger re-evaluates whether consumption has reached the trigger percentage and sends another notification if it
  has. For example, suppose a notification was sent at 70%, and consumption is currently at 90%. If you run an ALTER command to specify a
  70% trigger, a new notification is sent immediately.
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

## Examples

Specify a new credit quota for the resource monitor `limiter` and replace the existing triggers for the monitor with a new set
of triggers:

> Copy code
>
> ```
> ALTER RESOURCE MONITOR limiter
>   SET CREDIT_QUOTA=2000
>   TRIGGERS ON 80 PERCENT DO NOTIFY
>            ON 100 PERCENT DO SUSPEND_IMMEDIATE;
> ```

Alter a resource monitor to send notifications to three users when 80% of the credit quota is reached. In this example, the
`user_name` for two of the users includes a space and is therefore enclosed in double quotes:

> Copy code
>
> ```
> ALTER RESOURCE MONITOR limiter
>   SET CREDIT_QUOTA = 2000
>       NOTIFY_USERS = (JDOE, "Jane Smith", "John Doe")
>   TRIGGERS ON 80 PERCENT DO NOTIFY
>            ON 100 PERCENT DO SUSPEND_IMMEDIATE
> ```
