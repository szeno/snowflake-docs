# Create versions and patches for an app (Legacy)

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to add versions and patches to an application package.

For general information about versions and patches and how they are used to update and
upgrade an app, see [About app versions and patches](/developer-guide/native-apps/update-app-overview#label-native-apps-versioning-about).

## Add a version or patch to an application package

The version and patches of an app are defined in the application package.

After adding a version or patch to an application package, providers can test the changes locally
by creating an app based on the version or patch.

See [Create an app from a version or patch](/developer-guide/native-apps/installing-testing-application#label-native-apps-application-creating-version) for more information.

### Privileges required to add or remove versions and patches

To specify a version or patch for an application package, you must have one of the following privileges
granted on the application package to your role:

- OWNERSHIP
- MANAGE VERSIONS

For example, to grant the MANAGE VERSION privilege on the application package to the
`release_mgr` role, use the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command as shown in the following
example:

Copy code

```
GRANT MANAGE VERSIONS ON APPLICATION PACKAGE hello_snowflake_package
  TO ROLE release_mgr;
```

### Add a version to an application package

To add a version to the application package by using SQL, run the [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package)
command:

Copy code

```
ALTER APPLICATION PACKAGE MyAppPackage
  ADD VERSION v1
  USING '@dev_stage/v1'
  LABEL = 'MyApp Version 1.0';
```

In this example, `v1` is an identifier for the version. The consumer sees both the version name and patch name; the patch name is defined in the LABEL clause.

Caution

Only two versions of an application can exist at the same time. See [About app versions and patches](/developer-guide/native-apps/update-app-overview#label-native-apps-versioning-about)
for more information.

You can define the version name and label in the manifest file or specify them directly with the
[ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command. If you define them in the manifest
file as well as with the SQL command, the values specified in the SQL command take precedence over the
values specified in the manifest file.

### Add a patch to an application package

In addition to creating versions for an app you can also create patches for a specific version. Like
versions, app patches also have their own application files.

To create a new patch for an application package, use the ADD PATCH FOR VERSION clause of the
[ALTER APPLICATION PACKAGE … VERSION](/sql-reference/sql/alter-application-package-version) command, as shown in the following
example:

Copy code

```
ALTER APPLICATION PACKAGE MyAppPackage
 ADD PATCH FOR VERSION V1_0
 USING '@dev_stage/v1_0_p1';
```

In the example, no patch number is provided to the ADD PATCH FOR VERSION V1\_0 clause. In this case
Snowflake automatically increments the patch number by 1.

To create a new patch for an application with a custom patch number, provide a patch number to the
ADD PATCH FOR VERSION clause of the [ALTER APPLICATION PACKAGE … VERSION](/sql-reference/sql/alter-application-package-version)
command, as shown in the following example:

Copy code

```
ALTER APPLICATION PACKAGE MyAppPackage
 ADD PATCH 3
 FOR VERSION V1_0
 USING '@dev_stage/v1_p1';
```

### View the versions and patches in an application package

As a provider, you can view the versions and patches defined for an application by running the
[SHOW VERSIONS IN APPLICATION PACKAGE](/sql-reference/sql/show-versions) command on the application package.

The following command displays the versions and patches that have been defined for an application
package named `hello_snowflake_package`:

Copy code

```
SHOW VERSIONS IN APPLICATION PACKAGE hello_snowflake_package;
```

### Remove a version from an application package

To remove a version from an application package, you must verify that there are no
[release directives](/developer-guide/native-apps/update-app-release-directive) currently
pointing that the version you want to remove.

See [View the release directives for an application package](/developer-guide/native-apps/update-app-release-directive#label-native-apps-release-dir-view-legacy) for information on viewing the release directives.

To remove a version from an application package, use the DROP VERSION clause of the
[ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command as shown in the following example:

Copy code

```
ALTER APPLICATION PACKAGE hello_snowflake_package
  DROP VERSION v1_0;
```

After running this command, the version is not dropped until all installed instances of the app are dropped.
To verify the status of the drop command, use the [SHOW VERSIONS IN APPLICATION PACKAGE](/sql-reference/sql/show-versions) as shown in
the following example:

Copy code

```
SHOW VERSIONS IN APPLICATION PACKAGE hello_snowflake_package;
```

The `dropped_on` column lists the timestamp when the drop was initiated.

Note

The dropped version only appears in the output of this command while the state is `DROPPING`.
When all installed instances of the app are dropped, the dropped version no longer appears.

When a version is dropped, consumers can no longer install new instances of that version of the app.

Depending on how the application is published to consumers, it can take different amounts of time
for the version to be dropped:

- If the application package has not been published to consumers, the version is dropped immediately.
- If the application package has been published as a public or private listing within a single region,
  the version is dropped immediately.
- If the application package is published as the data product of a listing shared within the same
  region as the application package, the version is dropped within a few hours.
- If the application package is published as the data product of a listing using
  [Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment),
  it may take longer for the version to be dropped across all regions.
