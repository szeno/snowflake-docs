# Migrate from grant-based sharing to the manifest in a Snowflake Native App

[Preview Feature — Private](/release-notes/preview-features)

Declarative sharing in the Snowflake Native App Framework (Declarative Native Apps) is in Private Preview. Support isn’t in
production and is available only to selected accounts. To request access, contact your Snowflake
representative.

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to migrate a Snowflake Native App from grant-based sharing, which uses proxy views,
to declaring shared content in the manifest file.

## Before you begin

Each patch uses exactly one authorization model. A patch that declares a `shared_content` section
uses declarative sharing for all of its shared content. A patch with no `shared_content` section
uses the grant-based path. Plan your migration one patch at a time.

Note

It’s highly recommended to release the update to manifest sharing with no other changes. If a
problem occurs, the application package can downgrade to the prior version while you address it.

## Migration steps

1. Identify shared objects with `SHOW GRANTS TO SHARE IN APPLICATION PACKAGE`. All returned objects
   are tables or views in the application package.
2. Update the manifest to declare those objects in the `shared_content` section. For a simple view
   that references a single table or view in another database, you can either keep the view or refer
   directly to the target schema and table, provided the schema name in the target database matches
   the schema name in the application package.
3. (Optional) Native apps didn’t allow granting shared content directly to consumers. To do so now,
   add role declarations in the manifest for the newly shared content without breaking existing
   applications.
4. Review the declared shared content to confirm it aligns with the previously shared content.
5. Create an application instance using loose-file installation from a stage and test the app’s
   behavior.
6. When you’re confident it works, create the actual version and test again locally.
7. Deploy.

## Reference usage and grant cleanup

For databases outside the package that are used in the `shared_content` section, continue to grant
`REFERENCE_USAGE ... TO SHARE IN APPLICATION PACKAGE`. Adding a version or patch fails if this grant
is missing when shared objects depend on those databases.

Don’t revoke sharing grants or `REFERENCE_USAGE` grants until all release directives and all
consumers have migrated to the manifest path for every shared entity. Once no active version in any
account uses grant-based sharing, you can safely drop the existing `REFERENCE_USAGE` grants and the
grants to the share in the application package.

## Schema name overlap

Schemas used for manifest-declared shared content are versioned schemas. Don’t reuse a shared schema
name for objects created or managed by the setup script. If the setup script creates a schema with
the same name as a shared schema, the shared content declared in the manifest stays hidden and
inaccessible. For the specific behavior of each `CREATE SCHEMA` variant, see
[Create the setup script](/developer-guide/native-apps/creating-setup-script).
