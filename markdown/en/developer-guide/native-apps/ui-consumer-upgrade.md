# Upgrade an app as a consumer

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how a consumer can upgrade a Snowflake Native App that is installed in
their account.

## Overview of upgrades

In general, when a provider publishes an updated version or patch for an app, the
app is automatically upgraded in the consumer account. The automated upgrade occurs
for all instances of the app across all Snowflake accounts where the app is installed.

It may take some time for all app instances to be upgraded. However, consumers can
manually upgrade an app after a new version of patch has been published as long
as the upgrade of the instance installed in their account has not started. Also,
providers can specify a date and time when an automated upgrade occurs.

## Manually upgrade an app

Manual upgrades allow a consumer to upgrade an app when a provider publishes a new version
or patch.

To upgrade an installed Snowflake Native App to the latest available version, a consumer can use the UPGRADE clause of the
[ALTER APPLICATION](/sql-reference/sql/alter-application) command to modify the app:

Copy code

```
ALTER APPLICATION hello_snowflake_app UPGRADE;
```

This command initiates the upgrade of an installed version or patch of an app using the
release directive specified in the application package.

## Upgrade an app at a specific date and time

When publishing a new version of an app, providers can specify a date and time when the app
will be upgraded. This date and time specifies the earliest date when the app can be
upgraded.

Consumers can [create a task](/sql-reference/sql/create-task) to upgrade the app at a specific time.

Copy code

```
CREATE OR REPLACE TASK APP_UPGRADE_TASK
 SCHEDULE = 'USING CRON 0 9-17 * * SUN America/Los_Angeles'
 WAREHOUSE = 'WH'
 AS
   ALTER APPLICATION hello_snowflake_app UPGRADE;

ALTER TASK APP_UPGRADE_TASK RESUME;
```

This example attempts to upgrade the app every hour starting at 9:00 am and ending at
5:00 pm on Sundays (America/Los\_Angeles time zone).

## Monitor the status of an upgrade

Consumers can use the
[DESCRIBE APPLICATION](/sql-reference/sql/desc-application)
command to view the status of an upgrade. The following columns provide information specific
to upgrades:

> | Column | Description |
> | --- | --- |
> | `upgrade_after` | Indicates that the provider has scheduled an upgrade to begin at this time. However, the app may be upgraded before this date and time. For more information, see . |
> | `upgrade_state` | The current state of the background installation or upgrade of the application object. Valid values are:  - `INSTALLING`: The application object is in the process of being created. - `INSTALL_FAILED`: The creation of the application object failed. The application object   remains in the `INSTALL_FAILED` state until it is dropped. See the `UPGRADE_FAILURE_REASON`   column of the [DESCRIBE APPLICATION](/sql-reference/sql/desc-application) command for information about why the   installation or upgrade failed. - `COMPLETE`: The setup script successfully completed and the application object was created   or upgraded. - `QUEUED`: The application object is queued for upgrade. - `UPGRADING`: The application object is in the process of being upgraded. - `FAILED`: All upgrade attempts failed. The reason for the failure is listed in the   `UPGRADE_FAILURE_REASON` column, if present. The instance remains in the `FAILED` state until   a release directive is updated to point to a different version than the one that the upgrade was   targeting, as defined in the `TARGET_UPGRADE_VERSION` column. - `QUEUED_DELAYED`: The application object is queued for an upgrade that is scheduled for a future time. - `QUEUED_RETRY`: The instance failed one or more upgrade attempts. The reason for the failure   is indicated in `UPGRADE_FAILURE_REASON`: The instance is queued to perform another upgrade attempt. - `DISABLED`: The application object and its upgrades were disabled. In this state the instance will be   inaccessible for consumers, it will not be considered for upgrades and will not block application package   version drop. The reason for the failure is listed in the `UPGRADE_FAILURE_REASON` column, if present. |
> | `upgrade_target_version` | The version identifier of the version to which the app is being upgraded. |
> | `upgrade_target_patch` | The patch to which the application object is being upgraded. |
>
> Expand
>
> Show lessSee more
