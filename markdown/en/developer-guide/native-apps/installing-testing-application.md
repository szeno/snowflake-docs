# Install and test an app locally

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how providers can create and test a Snowflake Native App locally.

## About creating and testing apps

With the Snowflake Native App Framework, providers can create an app within the same account as the
application package, so they can test the app before publishing it to consumers.

Providers can also test the app in a single account without having to
alternate between provider and consumer accounts.

## Privileges required to create and test an app

To create an app locally from an application package, you must have the following privileges
granted to your role:

- The CREATE APPLICATION account-level privilege granted to your role.
- The INSTALL object-level privilege granted on the application package.

The following examples show how to use the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command
to grant these privileges to an account:

Copy code

```
GRANT CREATE APPLICATION ON ACCOUNT TO ROLE provider_role;
GRANT INSTALL ON APPLICATION PACKAGE hello_snowflake_package
  TO ROLE provider_role;
```

### Use the DEVELOP privilege

By default, the role used to create an application package has permissions to use the
[CREATE APPLICATION](/sql-reference/sql/create-application) command to create an app based on the
application package.

However, in some development environments you may need to allow users with other roles to
create and test an application package. To do this, grant the DEVELOP object-level privilege
on the application package to a role.

The DEVELOP privilege grants the privileges required to create and test an
app based on an application package. This privilege allows a user to perform
the following tasks using the application package on which they have been granted access:

- Create an app based on a version or patch specified in the application package.
- Upgrade to a different version of an app using the [ALTER APPLICATION](/sql-reference/sql/alter-application) command.
- Create or upgrade an app using files on a named stage.
- Enable debug mode on an app created in [development mode](#label-native-apps-dev-mode).

To grant the DEVELOP privilege to a role, use the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command as
shown in the following example:

Copy code

```
GRANT DEVELOP ON APPLICATION PACKAGE hello_snowflake_package TO ROLE other_dev_role;
```

Note

The DEVELOP object-level privilege is specific to a single application package. You must run
[GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) for each application package you want
to assign the DEVELOP privilege for.

## Workflow for creating and testing an app

The Snowflake Native App Framework provides different ways of creating an app from an application
package. This allows you to test a Snowflake Native App before publishing it to consumers. The method you
use depends on what parts of the app you want to test.

The following steps outline a typical workflow for testing an app:

1. Create the app.

   You can create an app locally based on the following:

   - Files on a stage

     This allows you to quickly test a new version of a setup script or application code files.
     See [Create an app using staged files](#label-native-apps-application-creating-stage) for more information.
   - A version or patch defined in the application package

     After defining a version or patch for an application package, you can test this version by
     creating an app based on it. For
     more information, see [Create an app from a version or patch](#label-native-apps-application-creating-version).
2. Upgrade an app.

   After verifying that an app is working correctly, you can upgrade it to a new version in one of two ways:

   - From a file on a stage
   - From a version or patch defined in the application package
3. Create an app based on a release directive.

   After testing an app using specific files or a version or patch, you can create an app
   based on the release directive defined for the application package. Using the release directive,
   you do not need to specify a stage or version of the app.

   For more information, see [Create an app using staged files](#label-native-apps-application-creating-stage).
4. Install an app from a listing.

   After testing that the application package and app are working correctly in your local account, you
   can add the application package to a listing and test the installation using Snowsight.

   For more information, see [Create an app using staged files](#label-native-apps-application-creating-stage).

## Create an app

You can install an app directly in your account to test its functionality and privileges before
sharing it with customers. The [CREATE APPLICATION](/sql-reference/sql/create-application) command supports different
syntaxes for creating an app.

Note

The following sections assume that you have created an application package,
the required manifest file, and a setup script.

### Create an app using staged files

You can create an app using a manifest file and setup script uploaded to a named
stage. This allows you to test changes to these files without having to
add a new version to an application package.

Use the [CREATE APPLICATION](/sql-reference/sql/create-application) command to create an app
using staged files as shown in the following example:

Copy code

```
CREATE APPLICATION hello_snowflake_app FROM APPLICATION PACKAGE hello_snowflake_package
  USING '@hello_snowflake_code.core.hello_snowflake_stage';
```

### Create an app from a version or patch

After defining a version or patch in an application package, you can create an app
based on that version or patch.

To create a an app from a specific version, use the [CREATE APPLICATION](/sql-reference/sql/create-application)
command as shown in the following example:

Copy code

```
CREATE APPLICATION hello_snowflake_app
  FROM APPLICATION PACKAGE hello_snowflake_package
  USING VERSION v1_0;
```

To create an app from a specific patch, use the
[CREATE APPLICATION](/sql-reference/sql/create-application) command as shown in the following example:

Copy code

```
CREATE APPLICATION hello_snowflake_app
  FROM APPLICATION PACKAGE hello_snowflake_package
  USING VERSION v1_0 PATCH 2;
```

### Create an app based on a release directive

After specifying a release directive — either custom or default — in an application package, you can create an app based on that release directive.

To create an app based on a release directive, use the
[CREATE APPLICATION](/sql-reference/sql/create-application) command as shown in the following example:

Copy code

```
CREATE APPLICATION hello_snowflake_app FROM APPLICATION PACKAGE hello_snowflake_package;
```

### Upgrade an app using a stage

To upgrade an app using files on a named stage, use the [ALTER APPLICATION](/sql-reference/sql/alter-application)
command, as shown in the following example:

Copy code

```
ALTER APPLICATION HelloSnowflake
  UPGRADE USING @CODEDATABASE.CODESCHEMA.AppCodeStage;
```

### Upgrade an app from a version or patch

To upgrade an app that was created using a specific a version or patch, use the
[ALTER APPLICATION](/sql-reference/sql/alter-application) command as shown in the following example:

Copy code

```
ALTER APPLICATION HelloSnowflake
 UPGRADE USING VERSION "v1_1";
```

## Set an app as the active context

To set an app as the active context for a session, run the USE APPLICATION command, as shown in the following example:

Copy code

```
USE APPlICATION hello_snowflake_app;
```

Note

To run this command, you must have the USAGE privilege granted on the app to your role.

## View the app in your account

To see a list of apps available to your account, use the [SHOW APPLICATIONS](/sql-reference/sql/show-applications) command, as shown in
the following example:

Copy code

```
SHOW APPLICATIONS;
```

## View information about an app

To view details of an app, run the [DESCRIBE APPLICATION](/sql-reference/sql/desc-application) command, as shown in
the following example:

Copy code

```
DESC APPLICATION hello_snowflake_app;
```

In [development mode](#label-native-apps-dev-mode), this command displays the schemas allowed
by the consumer’s application roles.

In [debug mode](#label-native-apps-testing-debug-mode), this command displays all schemas in
the app.

## Use development, debug, and session debug modes to test an app

With the Snowflake Native App Framework, providers can use the following modes to create an app and test its functionality:

[Development mode](#label-native-apps-dev-mode-about)
:   An app installed in the same account as its application package from a specific version or from files on a named stage is in development mode.
    The provider can test and troubleshoot the app in a single account, but can only access objects
    granted to application roles, similar to the consumer perspective.

[Debug mode](#label-native-apps-testing-debug-mode)
:   The provider can view and modify all objects within the app, including objects not granted to
    an application role. Because the session’s primary role is used, objects created in debug mode
    are not owned by the app.

[Session debug mode](#label-native-apps-session-debug-mode)
:   The provider can view and modify all objects within the app using the same privileges as the
    app or the setup script. Objects created in this mode are owned by the app.

### About development mode

When you create an app locally from an application package by
[specifying a version](#label-native-apps-application-creating-version) or
[application files on a named stage](#label-native-apps-application-creating-stage),
the app is considered to be in development mode.

Use development mode to test and troubleshoot an app within a single account.
In development mode you can create and test an app based on a specific version of an
application package. You can also create and test an app using application files on a stage.
This enables you to quickly test changes to the setup script or application logic.

Development mode provides an additional [debug mode](#label-native-apps-testing-debug-mode) that
you can use to view and test all of the objects within an app that a consumer would not be able to view.

In development mode, for example, running the SHOW or DESC commands on objects within the app will only
display those objects that the consumer has been granted permissions to view. However, in debug mode, you
can see all objects within the app.

### About debug mode

In debug mode, you can view and modify all of the objects within an app. Objects that are not visible to a
consumer, for example, objects not granted to an application role or shared content objects, are visible while in
this mode.

Note

When you create objects, such as a table, in debug mode, the object will not have the same ownership
as the app. If you need to create new objects while testing an app, use
[session debug mode](#label-native-apps-session-debug-mode).

Testing an app in debug mode requires the following:

- The app must be created in development mode, meaning it must be based on a specific version or
  files on a stage.
- You must explicitly enable debug mode on the app.

Note

Debug mode can only be toggled on and off for an app created in development mode within
the same account containing the application package.

To enable debug mode on an app, use the [ALTER APPLICATION](/sql-reference/sql/alter-application)
command as shown in the following example:

Copy code

```
ALTER APPLICATION hello_snowflake_app SET DEBUG_MODE = TRUE;
```

This command turns on debug mode for an app named `hello_snowflake_app`.
Similarly, to turn off debug mode, use the same command, as shown in the following example:

Copy code

```
ALTER APPLICATION hello_snowflake_app SET DEBUG_MODE = FALSE;
```

This command turns off debug mode for the app named `hello_snowflake_app`.

Note

To run this command, you must have the OWNERSHIP privilege on the app.
You must also have the DEVELOP privilege on the application package.

Additionally, the app must be created in development mode and in the same account
as the application package.

## Session debug mode

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Session debug mode allows providers to view and modify all of the objects within the app and
execute statements using the same privileges that the app has when installed in the consumer account.
Objects that are not visible to a consumer, for example, objects that are not granted to an application
role, are also visible in session debug mode.

Unlike debug mode, session debug mode only applies to the current session to reduce security risks. You
must [enable session debug mode](#label-native-apps-session-debug-mode-enable) for an app each time you
start a new session. Session debug mode also differs from debug mode in that it allows you to test an app
using the same privileges as the app or the setup script. To use these privileges, you can specify one of the
following when enabling session debug mode. For more information, see [Enable session debug mode for an app](#label-native-apps-session-debug-mode-enable).

- `AS_APPLICATION`: all statements are executed using the same privileges as the app has when it is created
  in the consumer account.
- `AS_SETUP_SCRIPT`: all statements are executed using the same privileges as the setup script has when it is
  run in the consumer account when an app is created or upgraded.

When a provider creates objects, such as a table, using session debug mode, the object is created with
the same privileges as the app.

### Privileges required to use session debug mode

Using session debug mode to view objects in an app has the following requirements:

- The app must be created in [development mode](#label-native-apps-dev-mode), which requires the
  app to be created based on a specific version or based on files located on a stage.
- The app must be in the same account as the application package on which the app is based.
- You must have the OWNERSHIP privilege on the app.
- You must have the DEVELOP privilege on the application package.

Note

Enabling session debug mode applies only to the current session. For example, if you enable session
debug mode in one worksheet tab, it is not active in another worksheet tab.

### Enable session debug mode for an app

To enable session debug mode on an app in the current session, use the
[SYSTEM$BEGIN\_DEBUG\_APPLICATION](/sql-reference/functions/system_begin_debug_application)
system function as shown in the following example:

Copy code

```
SELECT SYSTEM$BEGIN_DEBUG_APPLICATION('hello_snowflake_app');
```

This function enables session debug mode for the app named `hello_snowflake_app`.

You can also enable session debugging by specifying the execution mode for the app
as shown in the following example:

Copy code

```
SYSTEM$BEGIN_DEBUG_APPLICATION( 'hello_snowflake_app', execution_mode ='AS_APPLICATION')
```

This function sets the execution mode of the `hello_snowflake_app` app to `AS_APPLICATION`.
This mode executes all statements using the same privileges as the app has when created in the
consumer account.

### View the session debug status for an app in the current session

To view the session debug status in the current session, use the
[SYSTEM$GET\_DEBUG\_STATUS](/sql-reference/functions/system_get_debug_status) system function, as
shown in the following example:

Copy code

```
SELECT SYSTEM$GET_DEBUG_STATUS();
```

### Disable session debug mode for an app

To disable session debug mode for an app in the current session, use the
[SYSTEM$END\_DEBUG\_APPLICATION](/sql-reference/functions/system_end_debug_application) system
function, as shown in the following example:

Copy code

```
SELECT SYSTEM$END_DEBUG_APPLICATION();
```

## Disable redaction of provider data when testing an app

Within an app, information is redacted from the query profile and query history to hide implementation details
about the app from the consumer. See [Protect provider intellectual property](/developer-guide/native-apps/redacted-content).

When testing an app locally, you can disable redaction of provider data from the query
profile and query history.

Note

When session debug mode is used, all objects and data within an app are visible to the provider, even if the information is
redacted for the consumer. For example, information returned by the [SHOW APPLICATIONS](/sql-reference/sql/show-applications) and
[DESCRIBE APPLICATION](/sql-reference/sql/desc-application) commands is not redacted when session debug mode is used.

### Privileges required to disable redaction of provider data when testing an app

Disabling redaction of provider data for an app requires the following privileges:

- The app must be created in development mode, meaning it must be based on a specific version or files on a stage.
- The app must be created within the same account containing the application package.
- You must have the OWNERSHIP privilege on the app.
- You must have the DEVELOP privilege on the application package.

### Disable information redaction of provider data

To disable information for an app, use the [ALTER APPLICATION](/sql-reference/sql/alter-application) command as shown in the following example:

Copy code

```
ALTER APPLICATION hello_snowflake_app SET DISABLE_APPLICATION_REDACTION = TRUE;
```

This command disables redaction of provider data for an app named `hello_snowflake_app`.

To enable redaction of provider data, use the same command as shown in the following example:

Copy code

```
ALTER APPLICATION hello_snowflake_app SET DISABLE_APPLICATION_REDACTION = FALSE;
```

## Test event sharing in development mode

Providers use development mode to install and test an app that uses
[logging and event tracing](/developer-guide/native-apps/event-about).
Providers can set up an event table locally in their development account,
install the app in development mode, and view the events and logs that the app emits and those
that are shared back with the provider.

Note

To test event sharing in development mode, the app must
[define event definitions](/developer-guide/native-apps/event-definition) in
the manifest file.

### Differences in development mode

In development mode, apps are created based on one of the following:

- Files uploaded to a stage.
- Versions or patches defined in the application package.

When testing event sharing locally in development mode, there are differences in
behavior from apps created from a listing.

- The MANAGE EVENT SHARING global privilege is not required to enable event sharing.
- Shared events are collected in local event tables. In the local event table, providers can
  see two entries for one event:
  - The event that the app emits on the consumer side when the app is installed.
  - The event that is shared with the provider.

### Test event sharing in development mode

1. Configure the app to [use logging and event tracing](/developer-guide/native-apps/event-about).
2. [Set up an event table](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging#label-nativeapps-consumer-logging-setting-up)
   in the local development account.
3. Create the app locally by running one of the following commands:

   Copy code

   ```
   CREATE APPLICATION hello_snowflake_app
     FROM APPLICATION PACKAGE hello_snowflake_package
     USING @path_to_staged_files
     AUTHORIZE_TELEMETRY_EVENT_SHARING = TRUE;

   CREATE APPLICATION hello_snowflake_app
     FROM APPLICATION PACKAGE hello_snowflake_package
     USING VERSION v1_0
     PATCH 0
     AUTHORIZE_TELEMETRY_EVENT_SHARING = TRUE;
   ```
4. [View the log messages and trace events in the event table](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging#view-the-log-messages-and-trace-events-in-the-event-table).
