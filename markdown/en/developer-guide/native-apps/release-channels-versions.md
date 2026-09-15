# About release channels, versions, and patches

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic provides a general overview of release channels and how they are used to manage
updates to an app, including versions and patches.

## About release channels

Release channels allow providers to publish apps at different stages of the app development lifecycle. For
example, a provider can use release channels to perform the following tasks:

- Test an app locally in the provider account.
- Publish an app to consumers as a preview or for user acceptance testing (UAT).
- Publish the app to a production environment.

Release channels also allow providers to manage versions and patches of an app. By using release channels,
providers can create and publish multiple versions and patches of an app at the same time.

Using release channels, a provider can create more than two simultaneous versions of an app.

Note

The two-version limit applies to each release channel instead of per application package.

Providers enable release channels on the application package. By default, when you create an application package, release channels are enabled. However, if you create an application package with release channels
enabled, you cannot disable them later.

## Supported release channels

Release channels allow providers to publish an app at different stages of the development
life cycle. The specific release channel a provider uses depends on whether the app is
in development or ready for production. The Snowflake Native App Framework supports the following release channels:

QA:
:   Versions and patches of an app assigned to this release channel are only available to consumers within
    the provider’s organization. Apps published using this release channel must be targeted to one or more specific
    accounts within that organization; they are not available to all accounts in the organization by default.

    Providers can use this release channel for testing. Apps published using the QA release channel are not
    required to run the [automated security scan](/developer-guide/native-apps/security-run-scan). Adding
    a version only to the QA release channel does not initiate the security scan. To trigger the security
    scan, a version must be added to the ALPHA or DEFAULT release channel.

ALPHA:
:   Versions and patches of an app assigned to this release channel can be published to consumers
    outside the provider’s organization. When an app is assigned to this release channel, the automated
    security scan is performed.

    While the security scan is in progress, the provider can set the release directive for this version, and
    consumers can install it in their accounts. However, if a version assigned to this release channel fails
    the security scan, it can no longer be used.

    Providers can use this channel to collaborate with consumers during the development of an app.

DEFAULT:
:   Versions and patches of an app assigned to this release channel are available to all consumers
    who have access to the app version or patch. Apps assigned to this release channel must pass the automated
    security scan.

    This release channel is the production release channel. All apps assigned to this release channel must
    conform to the security requirements and guidelines for publishing an app. For more information, see
    [Security requirements and guidelines for a Snowflake Native App](/developer-guide/native-apps/security-overview).

## About versions and patches of an app

Snowflake Native Apps allow providers to create versions and patches of an app. Versions and patches allow providers
to release new functionality and updates to consumers.

Versions
:   Generally contain major updates to a Snowflake Native App. Versions generally introduce new features and changed
    functionality for an app.

Patches
:   Generally contain smaller updates to a Snowflake Native App. Unlike versions, patches should only contain small
    updates such as security fixes.

Note

Each version and patch must have its own manifest file and setup script.

### Number of available versions per release channel

Versions and patches are defined in the release channel. Providers can create multiple versions and patches of an app. However, each release channel only allows two versions of an app at a time. To add a new
version to a release channel that currently has two versions defined, providers must remove one of the versions that are currently in the release channel.

To remove a version, a provider must perform the following steps:

1. Ensure that all consumers have upgraded off the version to be removed.
2. Remove the version from the release channel.
3. Create a new version.
4. Upgrade the app.

For information about upgrading an app, see [Upgrade an app using release channels](/developer-guide/native-apps/release-channels-upgrade).

### Number of available patches per version

Although a release channel can only contain two versions at one time, a single version can have multiple patches. Patches cannot be dropped. When a provider adds a new version to a release channel, the new version is automatically assigned patch 0 by default. When a provider adds a new patch to a version, they can manually specify the identifier for the patch. If no patch number is provided, Snowflake automatically increments the patch version by 1.
