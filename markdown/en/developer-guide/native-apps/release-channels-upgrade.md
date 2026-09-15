# Upgrade an app using release channels

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic provides information on how to upgrade a Snowflake Native App using release channels.

## About app upgrades

The Snowflake Native App Framework allows providers to upgrade an app to a new version or patch.

Providers can initiate an upgrade of an app to a new version or patch by setting the release directive
on a release channel. When the release directive is modified, Snowflake automatically upgrades all
installed instances of the current version of the app to the version specified by the release directive.

When the provider initiates an upgrade, Snowflake adds each app to be upgraded to a queue. Each app is
upgraded as resources are available. The upgrade process can take a while to complete across all installed
versions of the app. To expedite the upgrade process, consumers can also manually initiate an upgrade of
an app when a new version or patch is available.

Note

After the upgrade process begins on an app, consumers can no longer manually upgrade the app.

### Considerations when upgrading an app with multiple versions

When a provider publishes a new version of an app, Snowflake ensures that only the previous version of
the app is active. For example, if a provider has published versions v1 and v2 of an app, Snowflake ensures
that only v2 is currently installed in a consumer account before upgrading to v3. This requires that all
installed apps using version v1 are migrated to version v2.

This ensures that the setup script of the app only has to account for differences between v2 and v3. The
setup script is only backwards compatible with the most recent version of the app. If a provider makes a
state change to the app, for example creating a new table or adding columns to a table, providers only have
to ensure that there are no compatibility issues between two versions.

In contrast, when a provider creates a new patch for a version of an app, the Snowflake Native App Framework does not enforce any
restrictions on the number of active patches running. Providers must avoid making changes to the state of
an app in a patch to avoid incompatibility across multiple patches.

### Considerations when removing a version of an app after an upgrade

Although an app might be upgraded in the consumer account, the previous version of the app might still have code that is running. Providers cannot remove the previous version of the app from the release channel until all running code from the previous version has completed. This applies to all installed versions of the app across all consumer accounts. If a single upgrade fails, providers must fix the reason for the upgrade failure before they can remove the version.

### Upgrades across regions

For information on upgrading an app across multiple regions, see .

## Workflow for upgrading an app

A provider upgrades an app by using the following workflow:

1. Update the app to include any new features.
2. If you are creating a new version of the app and there are two versions currently defined for the app:

> 1. Ensure that no consumers are currently running the version.
> 2. Drop the version of the app you are replacing.

1. Create a new version or patch for the changes in the release channel.

   If the DISTRIBUTION property of the application package is set to EXTERNAL, the automated security scan is initiated. The security scan must pass before the upgrade can occur.
2. Test the new version by installing the app in your test account.
3. Update the release directive for the version or patch.

   This initiates an automated upgrade that will update all installed instances of the previous version. A provider can notify the consumer that an upgrade is available and ask them to manually upgrade the app.

## Set a start date and time for an upgrade

Providers can set a date and time that specifies when an automatic upgrade should begin.
This date and time is set in the release directive (default or custom) using the
`UPGRADE_AFTER` clause of the [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command.
Both default and custom release directives are supported.

The upgrade date and time can be any valid [date and time type](/sql-reference/data-types-datetime).
If the timestamp has already passed the upgrade is immediately scheduled. This is the same behavior as not setting the
`UPGRADE_AFTER` clause.

You can only use the `UPGRADE_AFTER` clause if you are setting the version and patch. This clause can’t be used
to modify only the upgrade time and date.

### Set the upgrade date and time for the default release directive

1. To set the upgrade date and time for the default release directive:

   Copy code

   ```
   ALTER APPLICATION PACKAGE hello_snowflake_package
     MODIFY RELEASE CHANNEL DEFAULT
     SET DEFAULT RELEASE DIRECTIVE
     VERSION = 'v1_0'
     PATCH = '2'
     UPGRADE_AFTER = '2025-04-06T11:00:00Z'
   ```

This command sets the upgrade date and time for patch `2` or version `v1_0` of the DEFAULT
release channel to April 6, 2025 at 11:00 am.

Note

This is the earliest date and time when the upgrade can begin. The actual upgrade might occur later
depending on the number of apps being upgraded, the number of consumer accounts, etc.

### Set the upgrade date and time for a custom release directive

1. To set the upgrade date and time for a default release directive:

   Copy code

   ```
   ALTER APPLICATION PACKAGE hello_snowflake_package
     MODIFY RELEASE CHANNEL DEFAULT
     SET DEFAULT RELEASE DIRECTIVE
     VERSION = 'v1_0'
     PATCH = '2'
     UPGRADE_AFTER = '2025-04-06T11:00:00Z'
   ```

This command sets the upgrade date and time for patch `2` or version `v1_0` of the DEFAULT
release channel to April 6, 2025 at 11:00 am.

Note

This is the earliest date and time when the upgrade can begin. The actual upgrade might occur later
depending on the number of apps being upgraded, the number of consumer accounts, etc.

### Change the upgrade date and time for a custom release directive

1. To change the upgrade date and time for a default release directive:

   Copy code

   ```
   ALTER APPLICATION PACKAGE hello_snowflake_package
     MODIFY RELEASE CHANNEL DEFAULT
     SET DEFAULT RELEASE DIRECTIVE
     ACCOUNTS = ( USER_ACCOUNT.snowflakecomputing.com )
     VERSION = 'v1_0'
     PATCH = '2'
     UPGRADE_AFTER = '2025-04-06T11:00:00Z'
   ```

This command changes the upgrade date and time for patch `2` or version `v1_0` of the DEFAULT
release channel to April 6, 2025 at 11:00 am.

Note

This is the earliest date and time when the upgrade can begin. The actual upgrade might occur later
depending on the number of apps being upgraded, the number of consumer accounts, etc.

## Start an upgrade

The upgrade process starts automatically when a provider updates the release directive (default or custom) of the release channel to point to a new version or patch. Use the
[ALTER APPLICATION PACKAGE … RELEASE DIRECTIVE (Legacy)](/sql-reference/sql/alter-application-package-release-directive) command to set the release directive
as shown in the following examples:

Copy code

```
ALTER APPLICATION PACKAGE my_application_package
  MODIFY RELEASE CHANNEL DEFAULT
  SET DEFAULT RELEASE DIRECTIVE
  VERSION = v2
  PATCH = 0;
```

This command sets the default release directive to version `v2` and patch `0` for the default
release channel.

Copy code

```
ALTER APPLICATION PACKAGE my_application_package
  MODIFY RELEASE CHANNEL DEFAULT
  SET RELEASE DIRECTIVE my_custom_release_directive
  ACCOUNTS = ( USER_ACCOUNT.snowflakecomputing.com )
  VERSION = v2
  PATCH = 0;
```

This command sets the custom release directive named `my_custom_release_directive` to version `v2`
and patch `0` for the account USER\_ACCOUNT.snowflakecomputing.com.

See [Set the release directive for an app (Legacy)](/developer-guide/native-apps/update-app-release-directive) for more information.

## Manually upgrade an app

Manual upgrades allow a consumer to upgrade their installed app faster than automated upgrades.
When a new version or patch is available, a provider can ask the consumer to perform
a manual upgrade.

The consumer performs a manual upgrade by running the [ALTER APPLICATION](/sql-reference/sql/alter-application).
This command initiate the upgrade of an installed version or patch of an app using the release directive
specified in the release channel.

To upgrade an installed Snowflake Native App to the latest available version, a consumer can use the UPGRADE clause of
the [ALTER APPLICATION](/sql-reference/sql/alter-application) command to modify the app:

Copy code

```
ALTER APPLICATION <name> UPGRADE
```

## Upgrade an app across regions

After upgrading an app, changes to the installed Snowflake Native App in the consumer account
might not be visible until the refresh to remote regions is performed.

You can use the [APPLICATION\_STATE view](/sql-reference/data-sharing-usage/application-state-view) in the
[Data Sharing Usage](/sql-reference/data-sharing-usage) schema to monitor the state. If the upgrade is not
complete more than one day after the first refresh following the upgrade, there might be an issue
with the refresh process. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

If a provider publishes a Snowflake Native App using
[Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment),
automated upgrades may take a while to upgrade depending on multiple factors, including:

- The value of the refresh schedule.
- The number of installed instances of the app.
- The number of regions where the app is deployed.

If the upgrade contains an urgent fix that needs to be upgraded in a remote region, the provider can reduce the refresh
frequency of the listing to a smaller value. See
[Managing and monitoring auto-fulfillment settings](/collaboration/provider-listings-auto-fulfillment-monitor)
for information on setting the account-level refresh frequency.

> Caution
>
> Reducing the refresh frequency can increase the costs associated with replication.

## Upgrade states

During the upgrade process, the app passes through different states. The following diagram shows the possible
states when upgrading from the previous version, v1, to a new version, v2.

Note

Although this diagram shows an upgrade for a version, it also applies to patch upgrades.

![](/static/images/native-apps/na-upgrade-statuses.png)

The following table shows each stage of the upgrade process for an app within the same region that the application
package is located:

|  | Stage | Description |
| --- | --- | --- |
| 1 | App is disabled? | If the app is disabled, no upgrade is possible. |
| 2 | Set release directive to v2.0 | The provider sets the release directive to v2.0. |
| 3 | Eligible to upgrade | Snowflake performs checks to verify that the app is eligible to upgrade. These checks include verifying that the app is not disabled, that application package is available, that the version and patch is valid for upgrade, the consumer account is valid, etc. |
| 4 | Obtain upgrade slot? | Depending on the number of apps being upgraded, the number of consumer accounts, etc. they may have to wait to begin the upgrade process. |
| 5 | Setup script run successfully? | When the upgrade begins, Snowflake runs setup script. If any uncaught errors occur, the setup script execution stops. Snowflake queues the app for upgrade again based on the number of retries configured. |
| 6 | Is version updated? | Snowflake checks to see if the upgrade is for a version or patch. If the upgrade is for a version, Snowflake performs additional checks and waits until all jobs from the older version of the app have completed. |

Expand

Show lessSee more

The following table shows the upgrade process for apps that are deployed to remote regions:

|  | Stage | Description |
| --- | --- | --- |
| 7 | Release directive v2.0 replicated in remote region | When a provider sets the release directive for an app that is deployed to a remote region, the release directive is propagated to the application package deployed in the remote region. |
| 8 | Active region for v2.0? | When most of the apps in the primary region have been upgraded, Snowflake sends messages to the remote region to begin the app upgrade. |
| 9 | Begin upgrade process | Begin upgrade process for the app as described in the previous table. |

Expand

Show lessSee more

The following table describes each of the possible states of the upgrade process:

| State | Description |
| --- | --- |
| DISABLED | The app is disabled and not eligible for upgrade. |
| QUEUED | The app is in the queue to be upgraded based on the number of apps and consumer accounts. |
| UPGRADING | The app is in the process of being upgraded. |
| COMPLETED | The app has upgraded successfully. |
| QUEUED\_RETRY | The setup script or other check failed and the app is returned to the upgrade queue. |
| FAILED | The app upgrade failed. Upgrades can fail on the provider side, for example due to an error in the setup script. Upgrades can also fail on the consumer side if the app is disabled, the consumer account is inactive, etc. |

Expand

Show lessSee more

## Monitor the state of an upgrade

To view the upgrade state of an app, use the [APPLICATION\_STATE view](/sql-reference/data-sharing-usage/application-state-view).

For example, in a situation where you updated the default release directive and want to see if all apps have
reached the target version. To find application instances that have not yet finished the upgrade, use the query in
the following example:

Copy code

```
SELECT * FROM snowflake.data_sharing_usage.APPLICATION_STATE
```

This view includes columns that are specific to upgrades, including the upgrade state and the region where
the app is deployed. For information on upgrade states see [Upgrade states](#label-native-apps-upgrade-process).

## Troubleshoot upgrade problems

The Snowflake Native App Framework provides several ways to troubleshoot the upgrade as described in the following sections:

### Identify upgrade errors

Consumers can use the [DESCRIBE APPLICATION](/sql-reference/sql/desc-application) command to view error messages related to
failed upgrades. This command provides insight into the errors that occurred during the upgrade process.

Providers can use the [APPLICATION\_STATE view](/sql-reference/data-sharing-usage/application-state-view) to view error messages for failed upgrades.
Using this view, providers can diagnose issues with specific applications. See [Monitor the state of an upgrade](#label-native-apps-upgrade-status)
for more information.

### Use logging and event tracing

If [logging and event tracing](/developer-guide/native-apps/event-about) is configured for the
app, providers can query the event table to diagnose problems with the app upgrade.

See [View the logs and events in the event table](/developer-guide/native-apps/event-manage-provider#label-nativeapps-provider-logging-view-logs-and-events) for more information.

### Monitor the state of an app’s services

To view information about the status of a compute pool or service within an app,
consumers can use the following system functions:

- [DESCRIBE COMPUTE POOL](/sql-reference/sql/desc-compute-pool)
- [SYSTEM$GET\_SERVICE\_LOGS](/sql-reference/functions/system_get_service_logs)

Consumers can share this information back to providers. Providers can also configure event sharing
to return this information.

## Disabled apps

When an app installed in the consumer account is disabled, it is no longer usable.
An app installed in a consumer account can become disabled for multiple reasons, including:

- Problems with the application package
- Problems with the installed application
- Problems with the consumer account

Both providers and consumers should avoid situations where an app remains disabled for an extended
period of time. Disabled apps can become unusable and must be reinstalled

### Upgrade a disabled app

Disabled apps are not part of the normal upgrade process and cannot be upgraded. If a disabled app becomes
reenabled, it is automatically upgraded to the version and patch of the release directive. However, if the
version or patch is no longer available, the app cannot be upgraded and must be reinstalled.

For example, if a disabled app is on version `v1`, but the current and previous versions in the release channel are `v2` and `v3`, the app cannot be upgraded and is unusable.

### Reasons an app can become disabled

You can view the DISABLEMENT\_REASONS column of the
[APPLICATION\_STATE view](/sql-reference/data-sharing-usage/application-state-view) to see the reasons an app is disabled. The
following table lists the possible values for the DISABLEMENT\_REASONS column:

| Value | Status description | Is recoverable? |
| --- | --- | --- |
| MANUALLY\_DISABLED | The app is disabled by Snowflake | Yes. To re-enable the app, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support). |
| ACCOUNT\_INACTIVE | The account becomes inactive by being locked or suspended causing the app to be unavailable. In this state a consumer cannot execute any SQL queries in their account and the app cannot be upgraded. | Yes. The app is automatically re-enabled if the account lock or suspension is removed |
| PACKAGE\_VERSION\_IS\_MISSING | The application package version for the app was dropped by the provider. | Possibly. This can be caused by a temporary platform outage, in which case the app may recover automatically. Otherwise, the provider can work with Snowflake Support to attempt version recovery. Contact the application provider for more details. |
| CMK\_ACCESS\_DENIED | The consumer manages the encryption key themselves (ENCRYPT\_USE\_CMK\_KMS is enabled) and Snowflake doesn’t have access to this key. | Yes. To re-enable the app, ensure that the cloud provider configuration to retrieve the CMK is correct and that Snowflake has access to the key. |
| LISTING\_ACCESS\_REVOKED | The listing used to create the app is no longer available. Possible reasons for this status include:   - The provider deleted the listing - The provider manually removed access to the private listing from the consumer account | Possibly. Recoverability depends on the reason why access was revoked.  For example, if the listing was deleted it is not recoverable. If a consumer account was manually removed from the private listing, access to the listing and app can be restored. |
| LISTING\_TRIAL\_USAGE\_EXCEEDED | The application has exceeded the usage limit for a usage-based trial listing. | No |
| LISTING\_PAYMENT\_REQUIRED | The listing used to install the app is a paid listing and requires payment for further usage. | Yes. The consumer must correctly set up payment for the app. |
| LISTING\_TRIAL\_TIME\_EXCEEDED | The application exceeded the trial duration. | No |
| APPLICATION\_PACKAGE\_NOT\_AVAILABLE | The application package used to create the app no longer exists. The provider may have dropped the corresponding application package. | No |
| APPLICATION\_PACKAGE\_DISABLED | The application package used to create the app is disabled by the Snowflake. | Yes. The app is re-enabled, if Snowflake re-enables the application package. |
| APPLICATION\_SUSPENDED | The app resources for example, tasks, services, and compute pools, are suspended due to the app being disabled.  The suspended objects remain suspended until the app is re-enabled and there are no other reasons the app was disabled. | Yes |
| APPLICATION\_SUSPEND\_RESUME\_IN\_PROGRESS | The app resources, for example tasks, services, and compute pools, are currently resuming. | Yes |

Expand

Show lessSee more
