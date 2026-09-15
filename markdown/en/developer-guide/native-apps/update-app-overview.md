# Overview of app versions and upgrades (Legacy)

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic provides information about how versions, patches and upgrades work in the
Snowflake Native App Framework.

## About app versions and patches

The Snowflake Native App Framework allows providers to create versions and patches of an app. Versions and patches allow providers to
release new functionality and updates to consumers.

Version
:   Generally contains major updates to a Snowflake Native App. Versions generally introduce new features and changed
    functionality for an app.

Patch
:   Generally contains smaller updates to a Snowflake Native App. Unlike versions, patches should only contain small
    updates such as security fixes.

The versions and patches of an app are specified in the application package.

Caution

An app can only have two active versions at one time. Each version of an app can have up to 130 patches.

To add a new version to an application package that currently has two versions defined, providers must remove one of
the existing versions. To remove a version, a provider must:

1. Ensure that all consumers have upgraded off the version to be removed.
2. Remove the version from the application package.
3. Create a new version.
4. Upgrade the app.

Caution

Although an app might be upgraded in the consumer account, the previous version of the app might still have code that is
running. Providers cannot remove the previous of the app from the application package until all running code from the
previous version has completed. This applies to all installed versions of the app across all consumer accounts. If a single
upgrade fails, providers must fix the reason for the upgrade failure before they can remove the version.

Although an application package can only contain two active versions at one time, a single version can have multiple patches.
The Snowflake Native App Framework does not support dropping patches. When a provider adds a new version to an application package, the new version is
automatically assigned patch 0 by default. This cannot be changed.

When a provider adds a new patch to a version, they can manually specify the identifier for the patch. If no patch number is
provided, Snowflake automatically increments the patch version by 1.

Note

Each version and patch must have its own setup script and application files versions.

### Upgrading versions and patches

When a provider publishes a new version of an app, the Snowflake Native App Framework ensures that only the previous version of the
app is active. For example, if a provider has published versions v1 and v2 of an app, the Snowflake Native App Framework ensures that only v2 is
currently installed in a consumer account before upgrading to v3. This requires that all installed apps using version
v1 are migrated to version v2.

This ensures that the setup script of the app only has to account for differences between v2 and v3. The setup script is
only backwards compatible with the most recent version of the app. If a provider makes a state change to the app, for example
creating a new table or adding columns to a table, providers only have to ensure that there are no compatibility issues between
two versions.

In contrast, when a provider creates a new patch for a version of an app, the Snowflake Native App Framework does not enforce any
restrictions on the number of active patches running. Providers must avoid making changes to the state of
an app in a patch to avoid incompatibility across multiple patches.

## Stateful and stateless objects

For information on stateful and stateless objects in a Snowflake Native App, see
[Use versioned schema to manage app objects across versions](/developer-guide/native-apps/versioned-schema).

## About versioned schemas

For information on using versioned schema in a Snowflake Native App, see
[Use versioned schema to manage app objects across versions](/developer-guide/native-apps/versioned-schema).

## About app upgrades

The Snowflake Native App Framework allows providers to upgrade an app to a new version or patch. To see how
upgrades fit in the overall workflow for developing a new version or patch of an app, see
[Workflow for updating an app](/developer-guide/native-apps/update-app#label-update-workflow-legacy).

Providers can initiate an upgrade of an app to a new version or patch by setting a release directive
on the application package. When the release directive is modified, Snowflake automatically upgrades
all installed instances of the current version of the app to the version specified by the release directive.

When the provider initiates an upgrade, Snowflake adds each app to be upgraded to a queue. Each
app is upgraded as resources are available. The upgrade process can take a while to complete across all
installed versions of the app. To expedite the upgrade process, consumers can also manually initiate an upgrade
of an app when a new version or patch is available.

Note

After the upgrade process begins for their app, consumers can no longer manually upgrade the app.

For more information, see [Upgrade an app (Legacy)](/developer-guide/native-apps/update-app-upgrade).

### Upgrades across regions

See  for information on upgrading an app installed
across regions using Cross-Cloud Auto-Fulfillment.

## Lifecycle of app version and patches

To understand how app versions and patches work together, consider a scenario where a provider
has published an initial version, v1, of an app and consumer A and consumer B have installed that
version of the app in their accounts.

This scenario is shown in the following sections.

### Version v1.0 is installed in the consumer account

Figure 1 shows version `v1.0` of an app that a provider published and two consumers have
installed the app in their accounts:

![](/static/images/native-apps/na-app-lifecycle-1.png)

Figure 1 - version `v1.0`

This figure shows the following:

- The application files for `v1.0` are stored in a stage.
- The release directive of the application package is set to `v1.0`.
- Consumers have installed `v1.0` in their account.
- The provider has begun development of version v2.0 in their account.

### Add version v2.0 to the application package

Figure 2 shows that the provider has uploaded version `v2.0` and created a new
version in the application package:

![](/static/images/native-apps/na-app-lifecycle-2.png)

Figure 2 - upload files to the stage

This figures shows the following:

- After testing version `v2.0` of the app locally, the provider uploads the `v2.0` file to the stage
- The provider creates a new version for the app in the application package.
- The release directive continues to point to version `v1.0` of the app.
- Consumers continue to have version `v1.0` installed in their account.

### Upgrade the app from version v1.0 to version v2.0

To perform an upgrade from version `v1.0` to version `v2.0` of the app, the provider sets the
[release directive](/sql-reference/sql/alter-application-package-release-directive) of the application
package to version `v2.0`. This starts the process of upgrading the app in the consumer
accounts.

After the upgrade completes, both consumers A and B have version v2.0 installed in their accounts as shown in the
Figure 3 diagram.

![](/static/images/native-apps/na-app-lifecycle-3.png)

Figure 3 - upgrade from version `v1.0` to `v2.0`

Also, in this scenario the provider has begun developing and testing version v3.0 in their local development environment.

### Drop version v1.0 to be able to create v3.0

When testing is complete, the provider uploads version `v3.0` to the stage. When the provider wants to begin the upgrade to
version `v3.0`, they must first ensure that all consumers have migrated off of version `v1.0`.

In the scenario shown in the previous section, all consumers are currently on `v2.0`.

The provider must drop version `v1.0` from the application package as shown in Figure 4:

![](/static/images/native-apps/na-app-lifecycle-4.png)

Figure 4 - drop version `v1.0` from the application package

### Add version `v3.0` to the application package

After dropping version `v1.0`, the provider can then add version `v3.0` to the application package. In this context, the
release directive is still pointing to `v2.0` and consumers have `v2.0` installed in their account.

![](/static/images/native-apps/na-app-lifecycle-5.png)

Figure 5 - add version `v3.0` to the application package

### Upgrade to version `v3.0`

To upgrade to `v3.0`, the provider updates the release directive to point to `v3.0`. This begins the upgrade. When the upgrade
is complete, consumers are upgraded to version `v3.0` as shown in the following figure:

![](/static/images/native-apps/na-app-lifecycle-6.png)

Figure 5 - upgrade to version `v3.0`
