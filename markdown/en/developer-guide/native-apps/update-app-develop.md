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

- Use CREATE IF NOT EXISTS:

  You should always use CREATE OR REPLACE, CREATE IF NOT EXISTS or CREATE OR ALTER, whichever is applicable,
  when creating database objects such as tables, views, functions, or procedures. This prevents errors when
  trying to create objects that already exist during upgrade.

  Snowflake recommends using CREATE OR REPLACE only for stateless objects, such as functions or procedures,
  but not for stateful objects, such as tables.
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

  Setting this value to value that is too long may cause other part of the app to fail if they are expecting a service to be
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
The process of upgrading an app with containers has two main stages:

- Upgrade the services in the containers managed by the app.

  Like other Snowpark Container Services, container apps use the
  [ALTER SERVICE](/sql-reference/sql/alter-service) command to modify a service
  based on a service specification file for the new version. This command
  runs asynchronously.
- Upgrade other objects in the app.

  After the services are successfully upgraded, other object within the app are
  upgraded. This is similar to the normal Snowflake Native App upgrade process. See
  [About app upgrades](/developer-guide/native-apps/update-app-overview#label-native-apps-upgrades-about) for more information.

The Snowflake Native App Framework allows users to continue using an app even during major version upgrades, ensuring no downtime for
a normal app. However, for apps with containers, as both [CREATE SERVICE](/sql-reference/sql/create-service) and
[ALTER SERVICE](/sql-reference/sql/alter-service) are asynchronous. This means that even after the upgrade finishes,
the new version of the service may not be immediately available.

The potential issue when upgrading an app with containers is that the
[ALTER SERVICE](/sql-reference/sql/alter-service) command runs asynchronously. If this command adds
the [ALTER SERVICE](/sql-reference/sql/alter-service) directly to the setup script, the setup script continues to run while the
service upgrade is in progress.

Providers should write their setup script assuming that service upgrades may not yet be complete or
they should use [SYSTEM$WAIT\_FOR\_SERVICES](/sql-reference/functions/system_wait_for_services) and
[Use a version initializer to manage service upgrades](#label-native-apps-container-upgrade-version-init) to guarantee the correct version of the service is
ready for use.

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

This system function ensures the app installation or upgrade waits until the service is available or until
a failure occurs, ensuring that the service state is in sync with the version upgrade.

### Considerations when upgrading services

The Snowflake Native App Framework provides the version initializer callback function that allows providers to synchronize upgrading
services with the rest of the upgrade procedure.

During the upgrade of a basic app, the setup script upgrades to the new version
of the app by modifying objects within a versioned schema. If an error occurs during
upgrade, the objects within the versioned schema revert back to the previous version of the
app.

In the case of an app with containers, services that are created or modified by running the
[CREATE SERVICE](/sql-reference/sql/create-service) or [ALTER SERVICE](/sql-reference/sql/alter-service) commands in the setup
script use a service specification file for the new version.

Because services are not created within versioned schemas, a service is upgraded as soon as
the [CREATE SERVICE](/sql-reference/sql/create-service) or [ALTER SERVICE](/sql-reference/sql/alter-service) command run successfully.
If there is a failure later in the setup script, for example, the objects in versioned schemas are reverted back to the
previous version, but the modified services are the services of the new version.

### Use a version initializer to manage service upgrades

The Snowflake Native App Framework provides a version initializer that is used to start or upgrade services or other
related processes, for example tasks. The version initializer is a callback stored procedure
that is specified in the manifest file.

The version initializer is invoked in the following contexts:

- During installation, the version initializer is called as soon as the setup script of
  the app finishes without errors.
- During upgrade, there are two possible scenarios where the version initializer is called:
  - If the setup script of the new version succeeds, then the
    version initializer of the new version of the app is called.
  - If the setup script or the version initializer of the new version fails, then
    the version initializer of the previous version of the app is called. This allows the version
    initializer of the previous version to use the [ALTER SERVICE](/sql-reference/sql/alter-service)
    to revert the services to the previous version.

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
