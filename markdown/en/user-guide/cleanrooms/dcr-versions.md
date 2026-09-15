# Clean room versioning

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

Note

This topic is for clean room creators. Clean room consumers don’t need to think about clean room versioning.

## Clean room version numbering

Snowflake clean rooms are versioned. The initial version of a clean room without any Python code is V1.0.0.

Snowflake automatically creates a new version of a clean room after certain **provider** events, such as uploading Python code or enabling
external or Apache Iceberg™ tables. Snowflake creates a new version only if the security scan triggered by this action passes. Relatively few
provider actions can generate a new clean room version, and procedures that create a new version mention the new version in the procedure
response.

Actions that fail the security scan don’t generate a new version.

Only provider actions can result in a new clean room version; consumer actions cannot.

Snowflake increments only the patch number (the last digit) with each new version. So version numbers for three successive versions would be V1.0.0, V1.0.1, and V1.0.2.

Clean rooms are versioned because they are implemented as [native application packages](/developer-guide/native-apps/native-apps-about#label-components-of-the-naf). In
Snowflake’s native application framework, the convention is that for version V1.0.2, “V1.0” (a string) is the version number and 2 (an
integer) is the patch number. Clean room documentation typically uses the term “version” to indicate the entire number (V1.0.1) rather
than simply the “V1.0” prefix (as sometimes used in the native app framework).

You can see the version history and review status for a given clean room by calling
`SHOW VERSIONS IN APPLICATION PACKAGE samooha_cleanroom_CLEANROOM_ID;` with the ID of the clean room.

## Default release directive

Each clean room is assigned a *default release directive* by the clean room provider. The default release directive specifies which version
of the clean room should be installed or loaded in the user’s account. Consumers cannot specify which version of a clean room to install.
Updates are handled automatically by Snowflake [as available resources dictate](/developer-guide/native-apps/update-app-overview#label-native-apps-upgrades-about), and there can be
a delay before the new version is installed on the user’s account.

A clean room provider must specify the default release directive of a clean room before the clean room can be shared initially (either
internally or externally) or whenever the provider uploads code and the security scan passes. If a new version of the clean room is
generated but the default release directive is not updated, consumers will continue to be served the last default version.

You must always set the default release directive before publishing a clean room. If you haven’t added Python code, it should be
V1.0.0, as shown here:

Copy code

```
CALL samooha_by_snowflake_local_db.provider.set_default_release_directive(
  $cleanroom_name, 'V1_0', '0');
```

A clean room provider can roll the default release directive back to an earlier release if desired.

Specify the default release directive for a clean room by calling `provider.set_default_release_directive`.

A provider must set the default release directive only when creating or modifying a clean room in code. Versioning is handled
automatically when using the clean rooms UI.

Snowflake generates a new version only if the security scan triggered by a provider action passes. Therefore you should check the security
scan status for a clean room by calling `provider.view_cleanrooom_scan_status` before updating the default release directive. Not
updating the default release directive will not cause an error, but the newer version with your changes will not be published to users if you
don’t update the default release directive.

### Clean rooms with errors

If you publish a clean room with an error, which happens when the security scan fails or you upload Python code with a syntax error, a
patch is generated, but you cannot use that version as a default release directive. Until you publish a fixed version, any additional
patches incorporate the error from the previous failed patch and also result in a failed clean room patch.

## Versioning cheat sheet

List all clean room packages (clean rooms) created in this Snowflake account:

Copy code

```
SHOW APPLICATION PACKAGES STARTS WITH 'SAMOOHA_CLEANROOM_';
```

List all versions of the clean room MY\_FIRST\_CLEANROOM:

Copy code

```
SHOW VERSIONS IN APPLICATION PACKAGE SAMOOHA_CLEANROOM_MY_FIRST_CLEANROOM;
```

See your current default release directive:

Copy code

```
SHOW RELEASE DIRECTIVES IN APPLICATION PACKAGE SAMOOHA_CLEANROOM_<your_clean_room_name>;
```

Check the scan review status before setting the version if this is a clean room that you just made external, or if this is already external
and the version changed:

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_cleanroom_scan_status('MY_FIRST_CLEANROOM');

-- When REVIEW_STATUS = APPROVED, you can update the default version to the
-- latest version, if you haven't done so already.
SHOW VERSIONS IN APPLICATION PACKAGE SAMOOHA_CLEANROOM_MY_FIRST_CLEANROOM;
CALL samooha_by_snowflake_local_db.provider.set_default_release_directive(
  $cleanroom_name, 'V1_0', '<<LATEST_PATCH_NUMBER>>');
```
