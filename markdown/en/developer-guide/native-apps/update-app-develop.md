# Develop a new version of an app

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic provides information and best practices when updating an app to a new version or patch.

## Best practices when developing a new version or patch

Providers should consider the following best practices when developing a new version or patch for an app.

### Fully test an app before initiating the automated security scan

The following actions can initiate the automated security scan:

- **Without release channels**:

  - Setting the DISTRIBUTION property of the application package to EXTERNAL if a version of
    the app exists
  - Adding a new version or patch to an application package that has the DISTRIBUTION property
    set to EXTERNAL
- **With release channels enabled**:

  - Adding a version to the ALPHA or DEFAULT release channel
  - Adding a patch to a version that is already added to the ALPHA or DEFAULT release channel

  Adding a version only to the QA release channel, or adding patches to a version that has not
  been added to the ALPHA or DEFAULT release channel, does not initiate the scan.

Snowflake recommends that you fully test a new version or patch of your app locally before
initiating the security scan to avoid delays and multiple iterations of the scan in case of failure.

### Ensure compatibility between versions

Providers must ensure that a new version is compatible with the previous version of an app. For example,
if an app has versions v1 and v2, v2 must be compatible with v1. When version v3 is added, it must be compatible with
version v2. However, because only two versions of an app can exist at one time, version v3 does not have to be
compatible with version v1.

Code running in the previous version must handle state changes introduced in the new version. To handle
stateless objects, providers should use versioned schemas to ensure that upgrades are handled correctly. See
[Use versioned schema to manage app objects across versions](/developer-guide/native-apps/versioned-schema) for more information.

### Minimize state changes in patches

Providers must ensure that new patches do not introduce state changes that are different from previous
patches of the same version. Providers must minimize state changes such as adding or altering tables or
columns when developing a patch. Tables and columns must remain compatible across all versions and patches.
Patches should focus on bug fixes or minor feature additions without involving state modifications.

State changes should only be made when updating the version of an app.

### Use safe practices when creating objects from the setup script

When creating objects from the setup script, consider the following best practices:

- Use the command that matches how the object retains state:

  - For stateless objects, use `CREATE OR REPLACE`. Each app version has its own copy of these objects in a
    versioned schema.
  - For stateful objects that don’t support `CREATE OR ALTER`, use `CREATE IF NOT EXISTS` followed by idempotent
    `ALTER` statements. This approach preserves the object’s existing state during an upgrade.
  - For stateful objects that support `CREATE OR ALTER`, you can use that command to describe the complete target
    state. Review the command’s object-specific behavior before using it. Omitted properties can be reset, and
    omitted table columns and their data can be dropped. For more information, see
    [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).
- Ensure that the setup script of each app is self-contained

  Each version of the app must be complete and independent. For example, if a table was created in version v2.0
  using the CREATE TABLE IF NOT EXISTS a(int c) and version v3.0 includes ALTER TABLE A(…), ensure both the
  CREATE TABLE and ALTER TABLE statements are present in version v3.0. This ensures users installing the app from a
  later version have all necessary schema and objects.
- Use only idempotent changes in the setup script
  Structure CREATE and ALTER statements to be idempotent, so that they can run multiple times without errors or
  unintended side effects. If the setup script fails during installation, Snowflake reruns the setup script from
  the beginning. If a versioned schema has already been created for this version it is not recreated or deleted.
  For this reason, providers should use the CREATE IF NOT EXISTS version of the CREATE commands.

  For example:

  - Use ALTER TABLE ADD COLUMN IF NOT EXISTS to ensure columns are added only if they do not already exist.
  - When inserting rows, implement safeguards to prevent duplicate rows if unintended, as upgrades may be retried
    multiple times.

### Use caution when creating or dropping application roles

Use caution when creating or dropping application roles in a version or patch. Application roles are not versioned.
Dropping an application role or revoking a grant on an object from one version to another can cause the app to stop working
or prevent consumers from accessing the app.

Avoid using CREATE OR REPLACE APPLICATION ROLE. Instead, use CREATE APPLICATION ROLE IF NOT EXISTS. The OR REPLACE clause will
drop and recreate roles, causing permission issues as account-level roles granted to the application role in previous versions
would need to be re-granted.

## Best practices when developing a new patch or version of an app with containers

Providers should consider the following best practices when developing a new version or patch for an app with containers:

- Use caution when setting the timeout value for the [SYSTEM$WAIT\_FOR\_SERVICES](/sql-reference/functions/system_wait_for_services) system function.

  Setting this value to a value that is too long may cause other parts of the app to fail if they are expecting a service to be
  available. See [Pause setup script execution](#label-native-apps-container-upgrade-pause) for more information.
- Snowflake recommends creating the version initializer stored procedure within a versioned schema. If the version initializer
  is not created within a versioned schema, the version initializer may not exist from one version to the next.
- If an app specifies a version initializer, Snowflake recommends that the app attempts to start or upgrade services within
  the version initializer instead of the setup script. This ensures that the correct version of the service is running if an
  upgrade attempt fails.
- The version initializer does not need to be granted to an application role.

See [Update an app with containers](#label-native-apps-container-upgrade-about) for additional information on updating an app with containers.

## Update an app with containers

Updating an app with containers to a new version adds additional considerations during upgrade.
An upgrade of an app with containers can involve the following operations:

- Create or modify other app objects by running the setup script.
- Start or upgrade services by running [CREATE SERVICE](/sql-reference/sql/create-service) or
  [ALTER SERVICE](/sql-reference/sql/alter-service). These commands run asynchronously.

These operations don’t have a fixed order. A service begins upgrading at the point where the provider runs the service
command. The provider can run the command from the setup script or from the version initializer, which Snowflake calls
after the setup script finishes.

Services aren’t supported in versioned schemas because they have their own version management. A service can be
stateful or stateless. The [CREATE SERVICE](/sql-reference/sql/create-service) and [ALTER SERVICE](/sql-reference/sql/alter-service) commands
run asynchronously, so the script that runs either command continues while the service upgrade is in progress.

For an app without containers, the Snowflake Native App Framework lets users continue using the current app version during a major version
upgrade without downtime. For an app with containers, the asynchronous service upgrade might still be in progress
when the app upgrade finishes, so the target version of the service might not be immediately available.

Providers must account for this asynchronous behavior before other parts of the upgrade depend on the new service.
They can use [SYSTEM$WAIT\_FOR\_SERVICES](/sql-reference/functions/system_wait_for_services) to wait for services from a setup script, or use
[Use a version initializer to manage service upgrades](#label-native-apps-container-upgrade-version-init) to coordinate service upgrades with the app version.

To handle service upgrades correctly, the Snowflake Native App Framework provides features that allow the app to:

- Pause the execution of the setup script until the services upgrade successfully or
  fail. Providers should ensure that the setup script can handle possible situations. See
  [Pause setup script execution](#label-native-apps-container-upgrade-pause) for more information.
- Use the version initializer function to rollback service upgrades to the previous
  version if the upgrade fails. See [Considerations when upgrading services](#label-native-apps-container-upgrade-callback)
  for more information.

### Pause setup script execution

To minimize downtime and ensure services are ready, use the [SYSTEM$WAIT\_FOR\_SERVICES](/sql-reference/functions/system_wait_for_services)
system function in the setup script after creating or altering a service:

Copy code

```
SELECT SYSTEM$WAIT_FOR_SERVICES(600, 'services.web_ui', 'services.worker', 'services.aggregation');
```

This command causes the setup script to pause until one of the following occurs:

- All named services passed to the system function have READY status.
- Any of the named services has the FAILED status.
- 600 seconds has passed.

Because the setup script pauses while this function runs, Snowflake doesn’t complete the app installation or upgrade
before the services become ready, a service fails, or the timeout expires.

### Considerations when upgrading services

The Snowflake Native App Framework provides the version initializer callback function that allows providers to synchronize upgrading
services with the rest of the upgrade procedure.

During an upgrade, the setup script creates or modifies the objects for the target app version. If the setup script
or target version initializer fails, Snowflake doesn’t make the target version’s objects in versioned schemas active.
The previous version remains active.

In the case of an app with containers, services that are created or modified by running the
[CREATE SERVICE](/sql-reference/sql/create-service) or [ALTER SERVICE](/sql-reference/sql/alter-service) commands in the setup
script use a service specification file for the new version.

Because services aren’t created within versioned schemas, a service begins upgrading after the
[CREATE SERVICE](/sql-reference/sql/create-service) or [ALTER SERVICE](/sql-reference/sql/alter-service) command is accepted. The asynchronous
service upgrade might finish before or after the script that issued the command. If a later part of the app upgrade
fails, the service might already use the specification for the target app version while the previous app version
remains active.

### Use a version initializer to manage service upgrades

The Snowflake Native App Framework provides a version initializer that is used to start or upgrade services or other
related processes, for example tasks. The version initializer is a callback stored procedure
that is specified in the manifest file.

The version initializer is invoked in the following contexts:

- During installation, the version initializer is called as soon as the setup script of
  the app finishes without errors.
- During upgrade, there are two possible scenarios where the version initializer is called:
  - If the setup script of the target version succeeds, Snowflake calls the target version’s initializer.
  - If the setup script or target version’s initializer fails, Snowflake calls the previous version’s initializer
    before reporting the upgrade failure. The previous initializer can use [ALTER SERVICE](/sql-reference/sql/alter-service) to
    restore the service specification for the previous version.

### Add the version initializer to an app

To specify the stored procedure used as the version initializer, add the following to
the manifest file:

Copy code

```
lifecycle_callbacks:
  version_initializer: callback.version_init
```

In this example, the `version_initializer` property is set to a stored procedure named
`version_init` within a schema named `callback`.

Within the setup script, a provider can define this procedure within a versioned schema
as shown in the following example:

Copy code

```
CREATE OR ALTER VERSIONED SCHEMA callback;

CREATE OR REPLACE PROCEDURE callback.version_init()
  ...
  -- body of the version_init() procedure
  ...
```
