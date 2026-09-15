# Publish an app using release channels

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to use release channels to manage and publish multiple versions of a Snowflake Native App.

## Privileges required to use release channels

To use release channels, you must use a role that has been granted the MANAGE RELEASES privilege. This privilege allows you to:

- Enable release channels on the application package.
- Enable the QA and ALPHA release channels.
- Register and deregister versions and patches.
- Add versions and patches.
- Set the release directive.

## Enable release channels for an application package

If you disabled release channels when you created an application package, you can enable them using
the ENABLE\_RELEASE\_CHANNELS clause of the application package as shown in the following commands:

Copy code

```
CREATE APPLICATION PACKAGE my_app_package ENABLE_RELEASE_CHANNELS=TRUE;
ALTER APPLICATION PACKAGE my_app_package SET ENABLE_RELEASE_CHANNELS=TRUE;
```

Warning

After release channels are enabled for an application package, they cannot be disabled.

## Enable the ALPHA and QA release channels

By default, only the DEFAULT release channel is available to all consumers and enables them to install
an app from a listing to which they have access.

To use the QA and ALPHA release channels providers must explicitly enable them on the application package for
specific accounts. For these channels, the application package maintains a list of accounts that have been
added to each channel.

Providers can add an account to a release channel using the MODIFY RELEASE CHANNEL clause of the
[ALTER APPLICATION PACKAGE … MODIFY RELEASE CHANNEL](/sql-reference/sql/alter-application-package-release-channel) command.

To add the ORG1.ACCOUNT1 account to the ALPHA release channel:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package MODIFY RELEASE CHANNEL ALPHA ADD ACCOUNTS=(ORG1.ACCOUNT1);
```

To remove the ORG1.ACCOUNT1 account from the ALPHA release channel:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package MODIFY RELEASE CHANNEL ALPHA REMOVE ACCOUNTS=(ORG1.ACCOUNT1);
```

To overwrite the current list of accounts added to a release channel, a provider can use the SET clause of the
[ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command as shown in the following example:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package MODIFY RELEASE CHANNEL ALPHA SET ACCOUNTS=(ORG1.ACCOUNT2);
```

This command removes all current accounts from the ALPHA release channel and adds the ORG1.ACCOUNT2 account.

Note

Apps installed from the QA or ALPHA release channels are meant for testing. Only apps installed from the DEFAULT release channel are meant for production. For limited trial and paid (with trial) listings, the following limitations apply:

- **For an app installed from a listing using the QA or ALPHA release channels**: These apps are free, and will be disabled after the trial period ends. If these apps are installed from a paid listing, they will still be available to the consumer after the trial period ends. If the provider would like to revoke access to these apps after the trial period ends, they can do so by removing the consumer from the active targets of the release channel.
- **For an app installed from a listing using the DEFAULT release channel**: These apps are disabled after the trial period ends. If the consumer wants to continue using the app, they must accept an offer, and select the app from the default release channel.

## Monitoring release channels

### View the release channels defined in an application package or listing

To view the release channels defined in the application package, use the SHOW RELEASE CHANNELS command as shown
in the following example:

Copy code

```
SHOW RELEASE CHANNELS IN APPLICATION PACKAGE my_app_package;
```

To view the release channels defined for a listing, use the SHOW RELEASE CHANNELS command as shown in the
following example:

Copy code

```
SHOW RELEASE CHANNELS IN LISTING <listing_id>;
```

### View the release channel of an installed app

To view the release channels for all installed instances of an app, view the `current_release_channel_name` column of
the SNOWFLAKE.DATA\_SHARING\_USAGE.APPLICATION\_STATE view.

## Manage versions and patches using release channels

Providers must add a version or patch to a specific release channel before they can be used by release directives
inside a release channel. After a version has been added to a release channel, subsequent patches for that version are also
bound to that release channel to be used.

Note

The `ADD VERSION USING ‘@stage/path’` clause of the [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command is not supported for application packages that have release
channels enabled. Providers must register and deregister a version in the application package.

### Register a version

Before adding a new version of an app to an application package with release channels, providers must
register the version in the release channel by using the REGISTER clause of the [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package)
command:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package REGISTER VERSION V1 USING '@stage/path';
```

This command creates version V1 of the app and also creates patch 0. This version is not assigned to any release channel. There
is a maximum of two unassigned versions (not added to any release channels) allowed in the application package.

### Deregister a version

To create a new version in an application package that already has two versions, providers must deregister an old version.

To deregister a version and its associated patches, use the DEREGISTER clause of the
[ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package). The following command shows how to deregister version `v1` from
the application package:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package DEREGISTER VERSION v1;
```

Note

When using release channels, you do not have to drop the existing version from the application package.

### Add a version to a release channel

After registering a new version of an app in the application package, you must explicitly add the version to a release channel
to set the release directive for the app.

To add a version to a release channel, use the ADD VERSION clause of the [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package)
command:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package MODIFY RELEASE CHANNEL QA ADD VERSION V1;
```

Note

A release channel can only contain two simultaneous versions.

Note

Adding a version to the QA release channel does not initiate the automated security scan. To trigger
the security scan, add the version to the ALPHA or DEFAULT release channel. For more information,
see [Run the automated security scan](/developer-guide/native-apps/security-run-scan).

### Remove a version from a release channel

To remove a version from a release channel, use the DROP clause of the [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package):

Copy code

```
ALTER APPLICATION PACKAGE my_app_package MODIFY RELEASE CHANNEL QA DROP VERSION V1;
```

Dropping a version from a release channel is asynchronous and will only be truly dropped once all
consumers have been upgraded off that version.

## Set the release directive using a release channel

When release channels are enabled for an application package, each channel has its own release directive.

To set the default release directive for a release channel:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package
  MODIFY RELEASE CHANNEL ALPHA
  SET DEFAULT RELEASE DIRECTIVE VERSION=v1 PATCH=10;
```

To set a custom release directive for a release channel:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package
  MODIFY RELEASE CHANNEL ALPHA
  SET RELEASE DIRECTIVE my_custom_release_directive
  VERSION=V1 PATCH=11 ACCOUNTS=(ORG1.ACCOUNT1);
```

## Enable multiple instances using release channels

You can allow consumers to create multiple instances of an app in their account. Providers can
also create multiple instances of an app in their test account.

To enable multiple instances use the MULTIPLE\_INSTANCES property of the application package as shown in the
following commands:

Copy code

```
CREATE APPLICATION PACKAGE <name> MULTIPLE_INSTANCES=TRUE;
ALTER APPLICATION PACKAGE <name> SET MULTIPLE_INSTANCES=TRUE;
```

Note

Enabling multiple instances for the application package applies to all release channels within the application
package.

Note

A consumer can have multiple instances of an app using the QA or ALPHA release channels. If your app package is deployed to a paid listing, a consumer can only have one instance of an app using the DEFAULT release channel. Consumers can still install multiple app instances using the DEFAULT release channel from app packages in a free listing.

## Monetization and release channels

All app instances installed using the DEFAULT release channel use the pricing plan configured for the listing.

App instances installed from ALPHA and QA release channels are free and do not use the pricing plan configured for
the listing.

## Install an app using release channels

Providers can use [CREATE APPLICATION](/sql-reference/sql/create-application) to create an app from a release channel in their
test environment.

Note

To install an app from the QA or ALPHA release channels, you must use a role that has been granted the
CREATE PREVIEW APPLICATION privilege.

To install an app from an application package in the same account, run the following command:

Copy code

```
CREATE APPLICATION my_app
  FROM APPLICATION PACKAGE my_app_package
  USING RELEASE CHANNEL QA;
```

If you do not explicitly use the `USING RELEASE CHANNEL` clause, the DEFAULT release channel is used.

- To install an app in another account from a listing, run the following command:

Copy code

```
CREATE APPLICATION my_app
  FROM LISTING
  USING RELEASE CHANNEL QA;
```

If you do not explicitly use the `USING RELEASE CHANNEL` clause, the DEFAULT release channel is used.
