# Set the release directive for an app (Legacy)

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to set the release directive for an application package.

## About release directives

Release directives determine the version of the app that is available to a consumer when they
install or upgrade an app. Release directives are defined in the application package using the
[ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command.

There are two types of release directives:

Custom release directive
:   Allows a provider to specify the version and patch of an application that specific
    Snowflake accounts can install. See
    [add a custom release directive](#label-native-apps-release-dir-custom-add-legacy) for more information.

Default release directive
:   Specifies the version and patch that is applicable to all consumers when
    installing a Snowflake Native App. If a provider creates versions V1 and V2 of an application, setting the
    default release directive to V2 ensures that when a consumer installs the Snowflake Native App, they install.

    See [set a default release directive](#label-native-apps-release-dir-default-legacy) for
    more information.

If a provider creates version V2 and V3 of an application, they can assign V2 to be the default release and
create a custom release directive to share V3 only with specific accounts. A provider may also
share version V3 of the application with a test account before publishing that version.

Note

If you specify both a default and custom release directive, the custom release directive always
takes precedence. In the example above, consumer accounts specified in the custom release directive
would only be able to install V3 of the application.

You must define a default release directive in an application package before you can publish a listing with the application package as the data content.

## Privileges required to set the release directive

To set a release directive, a provider must have the MANAGE RELEASES privilege or ownership of the application
package.

Copy code

```
GRANT MANAGE RELEASES ON APPLICATION PACKAGE hello_snowflake_package
  TO ROLE release_mgr;
```

## Set the default release directive

Use the [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command with SET DEFAULT RELEASE
DIRECTIVE to set the default release directive as shown in the following
example:

Copy code

```
ALTER APPLICATION PACKAGE hello_snowflake_package
  SET DEFAULT RELEASE DIRECTIVE
  VERSION = v1_0
  PATCH = 2;
```

To update the default release directive for an application package, run the
[ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command with SET DEFAULT RELEASE DIRECTIVE again, specifying
new values for VERSION or PATCH, as appropriate.

## Set and update a custom release directive

### Set a custom release directive

To add a custom release directive, use the [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command with
SET RELEASE DIRECTIVE. Use the ACCOUNTS clause to specify the accounts to which this
release directive applies. For example:

Copy code

```
ALTER APPLICATION PACKAGE hello_snowflake_package
  SET RELEASE DIRECTIVE hello_snowflake_package_custom
  ACCOUNTS = (CONSUMER_ORG.CONSUMER_ACCOUNT)
  VERSION = v1_0
  PATCH = 0;
```

### Update a custom release directive

To update the version or patch for a custom release directive, use the
[ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command with MODIFY RELEASE DIRECTIVE as shown
in the following example:

Copy code

```
ALTER APPLICATION PACKAGE hello_snowflake_package
  MODIFY RELEASE DIRECTIVE hello_snowflake_package_custom
  VERSION = v1_0
  PATCH = 0;
```

However, you cannot modify the accounts associated with the release directive. To change the
organization and account associated with a release directive do the following:

1. Remove the release directive from the application package by running the
   [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command with UNSET RELEASE DIRECTIVE.
2. Add the release directive back to the application package by running the
   [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command with SET RELEASE DIRECTIVE and
   using the ACCOUNTS clause to specify the list of accounts.

Note

When you change the organization and account associated with the release directive, add
the new release directive immediately after you remove the old one. If you don’t, the installed
apps for the accounts assigned to the custom release directive revert to default release directive.

### Remove a custom release directive

To remove a custom release directive from an application package, use the
[ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command with UNSET RELEASE DIRECTIVE as shown in the following
example:

Copy code

```
ALTER APPLICATION PACKAGE hello_snowflake_package
  UNSET RELEASE DIRECTIVE hello_snowflake_package_custom;
```

## Test an app based on a release directive

When installing an app from an application package in development mode, the version and
patch are explicitly specified. However, when the application is installed using the following
command:

Copy code

```
CREATE APPLICATION hello_snowflake
  FROM APPLICATION PACKAGE hello_snowflake_package
```

The release directive determines the version that is installed when running this command.

## View the release directives for an application package

To view the release directives by using SQL, run the
[SHOW RELEASE DIRECTIVES](/sql-reference/sql/show-release-directives) command as shown in the following example:

Copy code

```
SHOW RELEASE DIRECTIVES IN APPLICATION PACKAGE hello_snowflake_package;
```
