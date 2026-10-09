# Install and test an app locally

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how providers can create and test a Snowflake Native App locally.

## About creating and testing apps

With the Snowflake Native App Framework, you can create an app in the same account as its application package and test it
before you publish it to consumers.

[Cortex Code](/user-guide/cortex-code/cortex-code-cli) (CoCo) includes the
[`native-app-provider`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-native-app-provider)
skill, which can run the steps in this topic. Some sections include an example CoCo prompt.

## Privileges required to create and test an app

To create an app locally from an application package, you must have the following privileges
granted to your role:

- The CREATE APPLICATION account-level privilege granted to your role.
- The INSTALL object-level privilege granted on the application package.

The following examples show how to use the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command
to grant these privileges to a role:

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

To let other roles create and test apps from an application package, grant them the DEVELOP
object-level privilege on the application package.

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

To test an app, follow these steps:

1. [Create the app from files on a stage](#label-native-apps-application-creating-stage). The app is in
   [development mode](#label-native-apps-dev-mode-about), so you see only what a consumer would see.
2. If an object is missing or a statement fails, turn on [debug mode](#label-native-apps-testing-debug-mode)
   to see every object in the app, or [session debug mode](#label-native-apps-session-debug-mode) to run
   statements as the app.
3. Fix the files on the stage and [upgrade the app](#label-native-apps-application-upgrade-stage).
4. Register a version and [create an app from that version](#label-native-apps-application-creating-version).
5. Set a release directive and [create an app from it](#label-native-apps-application-creating-directive).
   This app isn’t in development mode, so it behaves like a consumer install.
6. Add the application package to a listing and
   [install the app from the listing](/developer-guide/native-apps/ui-provider-publishing-app-package)
   in a test consumer account.

CoCo prompt: “Create an app named hello\_snowflake\_app from application package hello\_snowflake\_package using
the files on @hello\_snowflake\_code.core.hello\_snowflake\_stage, then list the objects in the app that my role
can see.”

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

To create an app from a specific version, use the [CREATE APPLICATION](/sql-reference/sql/create-application)
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

After you set a release directive for an application package, you can create an app from it. Omit the
`USING` clause:

Copy code

```
CREATE APPLICATION hello_snowflake_app FROM APPLICATION PACKAGE hello_snowflake_package;
```

The app uses the version and patch that the release directive specifies. If the application package uses
release channels, set the release directive on a channel. See
[Set the release directive using a release channel](/developer-guide/native-apps/release-channels#label-native-apps-relchan-release-directive).

An app created from a release directive isn’t in development mode, so you can’t use debug mode, session
debug mode, or `DISABLE_APPLICATION_REDACTION` with it.

### Upgrade an app using a stage

To upgrade an app from files on a named stage, use the [ALTER APPLICATION](/sql-reference/sql/alter-application)
command:

Copy code

```
ALTER APPLICATION hello_snowflake_app
  UPGRADE USING '@hello_snowflake_code.core.hello_snowflake_stage';
```

### Upgrade an app from a version or patch

To upgrade an app created from a version to another version, use the
[ALTER APPLICATION](/sql-reference/sql/alter-application) command:

Copy code

```
ALTER APPLICATION hello_snowflake_app
  UPGRADE USING VERSION v1_1;
```

## Set an app as the active context

To set an app as the active context for a session, run the USE APPLICATION command, as shown in the following example:

Copy code

```
USE APPLICATION hello_snowflake_app;
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

The following table compares the three modes:

| Mode | How to turn it on | Applies to | What you can see | Objects you create are owned by | How to check |
| --- | --- | --- | --- | --- | --- |
| [Development mode](#label-native-apps-dev-mode-about) | Create the app from files on a stage or from a version. | The app | Objects granted to an application role, as a consumer sees them. | Not applicable | `IS_DEV_MODE` from app code; see [Check the mode of an app](#label-native-apps-dev-mode-check) |
| [Debug mode](#label-native-apps-testing-debug-mode) | `ALTER APPLICATION ... SET DEBUG_MODE = TRUE` | The app, in every session, until you turn it off | Every object in the app. | Your current role | The `debug_mode` row of `DESC APPLICATION` |
| [Session debug mode](#label-native-apps-session-debug-mode) | `SELECT SYSTEM$BEGIN_DEBUG_APPLICATION(...)` | The current session only | Every object that the app owns. | The app | `SELECT SYSTEM$GET_DEBUG_STATUS()` |

Expand

Show lessSee more

### About development mode

An app is in development mode when you create it in the same account as its application package from
[files on a named stage](#label-native-apps-application-creating-stage) or from a
[version](#label-native-apps-application-creating-version). Use development mode to test the app as a
consumer sees it: SHOW and DESC commands and queries reach only objects granted to an application role.

You can use development mode without enabling debug mode or session debug mode. You can enable either mode
only for an app in development mode. Disabling [redaction](#label-native-apps-disable-application-redaction)
also requires development mode.

### Check the mode of an app

To check the mode from code inside the app, read the `IS_DEV_MODE` property of
[SYS\_CONTEXT (SNOWFLAKE$APPLICATION namespace)](/sql-reference/functions/sys_context_snowflake_application).
For example, the setup script can define the following procedure:

Copy code

```
CREATE OR REPLACE PROCEDURE core.check_mode()
  RETURNS VARCHAR
  LANGUAGE SQL
  AS 'BEGIN RETURN SYS_CONTEXT(''SNOWFLAKE$APPLICATION'', ''IS_DEV_MODE''); END';
```

`CALL hello_snowflake_app.core.check_mode();` returns `TRUE` for an app created from files on a stage or
from a version, and `FALSE` for an app created from a release directive, which includes every app that a
consumer installs from a listing.

`IS_DEV_MODE` reports how the app was created. It doesn’t change when you turn debug mode or session debug
mode on or off. Called from your own session, it returns `NULL` unless session debug mode is on, because
session debug mode runs your statements as the app.

To check the debug state from your own session:

- Debug mode: run `DESC APPLICATION hello_snowflake_app;` and read the `debug_mode` row.
- Session debug mode: run `SELECT SYSTEM$GET_DEBUG_STATUS();`. See
  [View the session debug status for an app in the current session](#label-native-apps-session-debug-mode-status).

### About debug mode

In debug mode, you can view and modify every object in the app, including objects that the setup script
doesn’t grant to an application role. Debug mode is a property of the app, so it stays on in every session
until you turn it off.

Objects that you create in debug mode are owned by your current role, not by the app. To create objects
owned by the app, use [session debug mode](#label-native-apps-session-debug-mode).

To turn debug mode on or off, you need the OWNERSHIP privilege on the app and the DEVELOP privilege on the
application package. Use the
[ALTER APPLICATION](/sql-reference/sql/alter-application) command:

Copy code

```
ALTER APPLICATION hello_snowflake_app SET DEBUG_MODE = TRUE;
```

Copy code

```
ALTER APPLICATION hello_snowflake_app SET DEBUG_MODE = FALSE;
```

For an app that isn’t in development mode, the command fails with the following error:

```
093039 (0A000): DEBUG_MODE can only be set/unset if the application is created directly from a particular version or stage in the same account as the application package.
```

CoCo prompt: “Turn on debug mode for hello\_snowflake\_app, list the objects that are visible only in debug
mode, then turn debug mode off.”

#### Find objects that aren’t granted to an application role

If an object is visible in debug mode but not when debug mode is off, the setup script doesn’t grant
privileges on it to an application role. Consumers can’t see or use the object.

For example, the following setup script creates the `core.config` table but grants nothing on it:

Copy code

```
CREATE APPLICATION ROLE IF NOT EXISTS app_public;
CREATE OR ALTER VERSIONED SCHEMA core;
GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_public;

CREATE TABLE IF NOT EXISTS core.config (k VARCHAR, v VARCHAR);
```

With debug mode off, `SHOW TABLES IN APPLICATION hello_snowflake_app;` returns no rows, and querying the
table fails:

Copy code

```
SELECT * FROM hello_snowflake_app.core.config;
```

```
002003 (42S02): SQL compilation error: Object 'HELLO_SNOWFLAKE_APP.CORE.CONFIG' does not exist or not authorized.
```

After you run `ALTER APPLICATION hello_snowflake_app SET DEBUG_MODE = TRUE;`, the same `SHOW TABLES`
command lists `CONFIG` and the query succeeds.

To fix the app, add the grant to the setup script and upgrade the app from the updated files:

Copy code

```
GRANT SELECT ON TABLE core.config TO APPLICATION ROLE app_public;
```

Copy code

```
ALTER APPLICATION hello_snowflake_app
  UPGRADE USING '@hello_snowflake_code.core.hello_snowflake_stage';
```

After the upgrade, roles granted `app_public` can see and query the table.

## Session debug mode

Session debug mode runs your statements as the app, in the current session only. Use it to see every
object that the app owns and to test what the app can do with its own privileges. Objects that you create in
this mode are owned by the app. While session debug mode is on, `CURRENT_ROLE()` returns the name of the app.

When you [turn on session debug mode](#label-native-apps-session-debug-mode-enable), choose whose
privileges your statements use:

- `AS_APPLICATION` (default): the privileges that the app has in a consumer account.
- `AS_SETUP_SCRIPT`: the privileges that the setup script has when it runs during install or upgrade.

Session debug mode applies to one app at a time. End it before you start it for a different app.

### Privileges required to use session debug mode

Using session debug mode to view objects in an app has the following requirements:

- The app must be created in [development mode](#label-native-apps-dev-mode), which requires the
  app to be created based on a specific version or based on files located on a stage.
- The app must be in the same account as the application package on which the app is based.
- You must have the OWNERSHIP privilege on the app.
- You must have the DEVELOP privilege on the application package.

### Enable session debug mode for an app

To turn on session debug mode in the current session, call the
[SYSTEM$BEGIN\_DEBUG\_APPLICATION](/sql-reference/functions/system_begin_debug_application) system function. The default execution mode is
`AS_APPLICATION`:

Copy code

```
SELECT SYSTEM$BEGIN_DEBUG_APPLICATION('hello_snowflake_app');
```

To use the privileges of the setup script, pass the execution mode as the second argument:

Copy code

```
SELECT SYSTEM$BEGIN_DEBUG_APPLICATION('hello_snowflake_app', 'AS_SETUP_SCRIPT');
```

CoCo prompt: “Start session debug mode for hello\_snowflake\_app as the setup script, show which objects the app
owns, then end session debug mode.”

### View the session debug status for an app in the current session

To check session debug mode in the current session, call the
[SYSTEM$GET\_DEBUG\_STATUS](/sql-reference/functions/system_get_debug_status) system function:

Copy code

```
SELECT SYSTEM$GET_DEBUG_STATUS();
```

When session debug mode is on, the function returns the app and the execution mode:

Copy code

```
{"instance_name":"HELLO_SNOWFLAKE_APP","domain":"APPLICATION_INSTANCE","execution_mode":"AS_SETUP_SCRIPT"}
```

When session debug mode is off, the function returns `{}`.

### Disable session debug mode for an app

To turn off session debug mode in the current session, call the
[SYSTEM$END\_DEBUG\_APPLICATION](/sql-reference/functions/system_end_debug_application) system function:

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

When session debug mode is used, objects and data that the app owns are visible to the provider, even if the
information is redacted for the consumer. For example, information returned by the [SHOW APPLICATIONS](/sql-reference/sql/show-applications) and
[DESCRIBE APPLICATION](/sql-reference/sql/desc-application) commands is not redacted when session debug mode is used.

### Requirements to disable redaction of provider data

Disabling redaction of provider data for an app has the following requirements:

- The app must be created in development mode, meaning it must be based on a specific version or files on a stage.
- The app must be created within the same account containing the application package.
- You must have the OWNERSHIP privilege on the app.
- You must have the DEVELOP privilege on the application package.

### Disable information redaction of provider data

To disable information redaction for an app, use the [ALTER APPLICATION](/sql-reference/sql/alter-application) command as shown in the following example:

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

This override also leaves Cortex Agent observability records unredacted in the development
account, so you can inspect app-initiated runs while you test. For more information about
redaction in production consumer accounts, see
[Intellectual property protection during event logging](/developer-guide/native-apps/agents-mcp-servers#label-native-apps-agent-ip-protection).

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
