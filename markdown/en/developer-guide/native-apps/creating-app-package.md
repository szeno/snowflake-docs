# Create and manage an application package

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how providers can create an application package to develop a Snowflake Native App.

## About the application package

An application package is a container that encapsulates the data content and application logic used by a Snowflake Native App. An application package also contains
information about versions and patches defined for an app.

Each version of an app requires its own version of the manifest and setup script:

manifest file:
:   The manifest file contains information that the application package
    requires to create and manage a Snowflake Native App. This includes the location
    of the setup script, version definitions, and configuration information
    for the app.

    For more information, see [Create the manifest file for an app](/developer-guide/native-apps/manifest-overview).

setup script:
:   The setup script contains SQL statements that are run when the app is
    installed, either in the consumer account or locally during development and
    testing.

    For more information, see [Create the setup script](/developer-guide/native-apps/creating-setup-script).

Note

You can create an application package without creating the manifest file or
setup script. However, to develop or test an app, you must upload these
files to a stage so they are accessible to the application package.

## About release channels

Release channels manage the release lifecycle of Snowflake Native Apps. They allow providers to create
and manage versions of an app and to publish the app at different stages of development to all consumers or specific groups of consumers.

Caution

When you create an application package, release channels are enabled by default.
After release channels have been enabled for an application package, they can’t
be disabled.

For more information on using release channels to manage the release lifecycle
of an app, see [Publish an app using release channels](/developer-guide/native-apps/release-channels).

To use the previous process for managing versions and patches you must explicitly disable release
channels when creating the application package. However, for new app development Snowflake recommends
using release channels to manage the release lifecycle of your apps.

For information on using the older features for managing versions and patches, see
[Develop a new version of an app](/developer-guide/native-apps/update-app-develop).

## Privileges required to create an application package

To create an application package you must have the global CREATE APPLICATION PACKAGE privilege granted to your role.

## Create an application package

You can create an application package using one of the following methods:

- Snowsight
- The [CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package) command.
- The [Snowflake CLI](/developer-guide/snowflake-cli/index)

### Create an application package using Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **App packages**.
3. Select **Create** and then click **App Package** in the right pane.
4. Enter a name for your application package.
5. Select the intended consumer for the application package:

   - Select **Distribute to accounts outside of your organization** to make
     the application package available outside your organization. Selecting this
     option initiates an [automated security scan](/developer-guide/native-apps/security-overview) for each version and patch defined in your application package.
   - Select **Distribute to accounts in your organization** to make the
     application package available within your organization. The automated
     security scan is not initiated.
6. (Optional) Enter comments for the application package. These comments are not visible to the consumer.
7. Select **Add**.

### Create an application package using SQL commands

To create an application package using SQL, use the
[CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package)
command as shown in the following example:

Copy code

```
CREATE APPLICATION PACKAGE my_application_package;
```

This command creates an application package named `my_application_package` in your Snowflake account.
By default, [release channels](/developer-guide/native-apps/release-channels) are enabled for the application package.

After creating an application package, use the
[SHOW APPLICATION PACKAGES](/sql-reference/sql/show-application-packages) command to view the list
of available application packages.

### Create an application package using the Snowflake CLI

If you are using the Snowflake CLI to develop an app, the application package is
created when you run the
[snow app run](/developer-guide/snowflake-cli/command-reference/native-apps-commands/run-app)
command. This command creates an application package in your Snowflake account, uploads code
files to a stage, then creates or upgrades an app from the application package.

## Grant the required privileges on an application package

Some tasks related to creating or using an application package require specific privileges on the application package. The following table describes the privileges required to perform these tasks:

| Privilege | Task |
| --- | --- |
| ATTACH LISTING | Add an application package to a listing. |
| DEVELOP | Create an APPLICATION object in development mode from the application package. |
| INSTALL | Create an APPLICATION object based on the application package. |
| MANAGE RELEASES | Specify a release directive, view the version and patch level. |
| MANAGE VERSIONS | Add a version and patch level to an application package. |
| OWNERSHIP | Perform all of the tasks above. |

Expand

Show lessSee more

### Grant privileges on an application package using Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **App packages**.
3. Select the application package, then select the **Settings** tab.
4. In the **Privileges** section, select the edit icon next to the privilege you want to
   grant.
5. Select **Add Role**, then select the role to which you want to grant the privilege.
6. Select **Save**.

The role appears next to the privilege.

### Grant privileges on an application package using SQL commands

To grant a privilege on the application package to a role using SQL, use the
[GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command as shown in the following example:

Copy code

```
GRANT MANAGE RELEASES ON APPLICATION PACKAGE hello_snowflake_package TO ROLE app_release_mgr;
```

This command grants the MANAGE RELEASES privilege to the `app_release_mgr` role. You can
use the same command to grant the other privileges available on an application package.

## Set the default release directive for an application package

A release directive determines the version and patch of an app that is available
to a consumer when they install the app or when an installed app is automatically
upgraded. For information on setting the release directive, see
[Set the release directive for an app (Legacy)](/developer-guide/native-apps/update-app-release-directive)

## Allow consumers to install multiple instances of an app

Providers can configure an application package to allow consumers to install
multiple instances of an app.

To enable multiple instances of an app, use the `MULTIPLE_INSTANCES = TRUE` clause of the
[CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package) or
[ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) commands.

If multiple instances are allowed for an app, consumers can install a maximum of 30 instances of the app in their account.

You cannot set this property for an application package that is included in a trial listing. An app installed from a paid listing
can’t have multiple instances using the DEFAULT release channel.

Caution

After setting the `MULTIPLE_INSTANCES` property to `TRUE`, it cannot be unset or set to `FALSE`.

## Transfer ownership of an application package

After creating an application package, you can transfer ownership of the application package to
another account-level role.

### Transfer ownership using Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **App packages**.
3. Select **…** next to the application package you want to transfer ownership, then select
   **Transfer Ownership**.
4. Under **Transfer to**, select the new account-level role.
5. Select **Transfer**.

### Transfer ownership using SQL Commands

To transfer ownership of an application package to a different account-level role using SQL, use the
[GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command as shown in the following example:

Copy code

```
GRANT OWNERSHIP ON APPLICATION PACKAGE hello_snowflake_package TO ROLE native_app_dev;
```

## Delete an application package

Providers with the OWNERSHIP privilege on an application package can remove it
from an account. However, providers cannot remove an application package that is
currently associated with a listing.

After removing an application package, it is no longer available in the provider account.

Caution

After removing a listing and the attached application package, the consumer
can view but not access the Snowflake Native App created from the application package.
If a consumer tries to access the Snowflake Native App, they receive an error
indicating the application package has been removed.

### Delete an application package using Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **App packages**.
3. Select **…** next to the application package you want to remove, then select **Drop**.

### Delete an application package using SQL commands

To remove an application package using SQL, run the [DROP APPLICATION PACKAGE](/sql-reference/sql/drop-application-package) command
as shown in the following example:

Copy code

```
DROP APPLICATION PACKAGE hello_snowflake_package;
```
