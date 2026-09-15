# Consumer-controlled maintenance policies: Provider guide

With consumer-controlled maintenance policies, consumers can define when Snowflake Native App upgrades happen in their
accounts. Instead of upgrades happening immediately when you release a new version, consumers can delay upgrades
to a maintenance window that works for their operations. For information about how consumers create and manage
maintenance policies, see [Consumer-controlled maintenance policies](/developer-guide/native-apps/consumer-maintenance-policies).

As a provider, you need to:

- Enable maintenance window upgrades on your release directives.
- Set an upgrade deadline so that consumers can’t postpone upgrades indefinitely.
- Optionally, align Snowpark Container Services compute pool node maintenance with the consumer’s maintenance window.
  Such an alignment is recommended because it minimizes disruptions for the consumers.

## Enabling maintenance window upgrades

When setting a release directive, you can specify that upgrades should respect consumer maintenance policies by
setting the UPGRADE\_IN\_MAINTENANCE\_WINDOW parameter to TRUE. You must also set the UPGRADE\_DEADLINE
parameter, which defines the latest date and time by which the upgrade must be completed. After this deadline,
the upgrade proceeds regardless of the consumer’s maintenance policy.

To enable maintenance window upgrades, use the [ALTER APPLICATION PACKAGE … MODIFY RELEASE CHANNEL](/sql-reference/sql/alter-application-package-release-channel) command
as shown in the following example:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package
  MODIFY RELEASE CHANNEL DEFAULT
  SET DEFAULT RELEASE DIRECTIVE
  VERSION = v1_0
  PATCH = 2
  UPGRADE_IN_MAINTENANCE_WINDOW = TRUE
  UPGRADE_DEADLINE = '2026-2-10T10:00:00Z';
```

This command configures the release directive so that consumers with a maintenance policy can delay the upgrade
until their next maintenance window, up to a maximum of February 10, 2026 at 10:00 AM.

Note

- The UPGRADE\_DEADLINE parameter is required when UPGRADE\_IN\_MAINTENANCE\_WINDOW is set to TRUE.
  Set the deadline to a date and time that allows sufficient time for consumers to complete the upgrade
  within their maintenance windows.
- You can’t set the UPGRADE\_AFTER and UPGRADE\_IN\_MAINTENANCE\_WINDOW parameters at the same time.
  If you try to set both, the command fails with an error.

## Enabling automatic compute pool maintenance

If your app uses Snowpark Container Services, you can align compute pool node software upgrades with the consumer’s maintenance
window. Without this setting, application upgrades and compute pool node maintenance are separate concerns
that can happen at different times. By enabling automatic application maintenance, both are coordinated into
the consumer’s chosen maintenance window.

To enable this, set the AUTOMATIC\_APPLICATION\_MAINTENANCE property on the application package:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package
  SET AUTOMATIC_APPLICATION_MAINTENANCE = TRUE;
```

With this enabled, Snowpark Container Services compute pool node software upgrades are scheduled to occur during the consumer’s
maintenance window. The application upgrades first, then any compute pool node maintenance follows.

## What happens when a consumer has a maintenance policy

When you release an update with UPGRADE\_IN\_MAINTENANCE\_WINDOW set to TRUE, the following occurs:

- If the consumer has set a maintenance policy, the upgrade is delayed until the next maintenance window
  defined by the consumer’s policy, or until the upgrade deadline is reached, whichever comes first.
- If the consumer has not set a maintenance policy, the upgrade happens during the default system maintenance
  window.
- If AUTOMATIC\_APPLICATION\_MAINTENANCE is enabled, the application code upgrades first, followed by
  any Snowpark Container Services compute pool node maintenance, all within the same maintenance window.
