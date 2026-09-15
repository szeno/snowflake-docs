# Share content using the manifest in a Snowflake Native App

[Preview Feature — Private](/release-notes/preview-features)

Declarative sharing in the Snowflake Native App Framework (Declarative Native Apps) is in Private Preview. Support isn’t in
production and is available only to selected accounts. To request access, contact your Snowflake
representative.

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to share provider-side content with consumers by declaring it in the
manifest file of a Snowflake Native App. Declaring shared content in the manifest is the recommended way to
share content. Use a [setup script](/developer-guide/native-apps/creating-setup-script) only for
advanced scenarios that must run code in the consumer account.

## Recommended: declare shared content in the manifest

You share content by adding a `shared_content` section to the manifest file, using the same syntax
as [Snowflake Declarative Sharing](/developer-guide/declarative-sharing/about). The framework
handles privilege management, object resolution, and versioning, so you don’t need to write GRANT
statements or create proxy views.

When a version or patch declares a `shared_content` section, authorization for that patch runs
entirely through the declarative sharing engine. Grant-based authorization no longer applies to that
patch. Code from earlier versions that uses grant-based sharing continues to work and sees only the
content granted that way.

Note

This isn’t the same as a standalone declarative share. A Snowflake Native App is a `NATIVE` application
package that can still run code in the consumer’s account. The standalone
[Snowflake Declarative Sharing](/developer-guide/declarative-sharing/about) topic covers `DATA`
application packages, which are stateless and read-only. Both use the same declarative manifest
syntax to share content.

## How manifest sharing improves on proxy views

Grant-based sharing requires a local proxy view in the application package to expose shared content
to consumers. Declaring content in the manifest removes that requirement and offers the following
advantages:

- No proxy view is required to expose a shared object.
- You can share object types that the grant path can’t share through a proxy view, including
  semantic views and Cortex Search services.
- Content shared by reference stays on the provider side and is read at query time.

Proxy views in a versioned schema still have one advantage: the view locks the structure of the
shared content to the application version, which keeps the application interface stable across
versions. There’s no automatic migration path from proxy views to direct sharing. For more
information, see [Migrate from grant-based sharing to the manifest](/developer-guide/native-apps/sharing-manifest-migrate).

## Supported object types

You can declare the following object types in the `shared_content` section of the manifest:

- Regular tables
- Dynamic tables
- Secure views
- Semantic views
- Cortex Search services

For the full manifest syntax and field semantics, see the
[Manifest file reference](/developer-guide/native-apps/manifest-reference).

## Choose between the manifest and a setup script

Both the manifest and the [setup script](/developer-guide/native-apps/creating-setup-script) can add
content to an app. Choose based on what the object needs to do, not preference.

- **Declare it in the manifest** when the object operates on provider-side content that consumers
  read at query time, such as tables, views, secure views, semantic views, and Cortex Search
  services. This is the default and the common case.
- **Use a setup script** when the object has to be built inside the app environment in the
  consumer’s account, such as Snowpark Container Services, stored procedures that use external
  access integrations, or logic that needs consumer-side tooling.

The following table summarizes the choice:

| Requirement | Author in the manifest | Author in a setup script |
| --- | --- | --- |
| Share provider-side data, views, or search read at query time | Yes | No |
| Share semantic views or Cortex Search services | Yes | No |
| Version and audit shared objects and roles declaratively | Yes | No |
| Run code in the consumer’s account (SPCS, external access) | No | Yes |
| Create consumer-side objects or tooling at install time | No | Yes |

Expand

Show lessSee more

A single patch uses one authorization model. If a patch declares a `shared_content` section, all of
its shared content is authorized through the declarative engine. You can still include a setup
script in the same patch for the advanced cases above.

### Scenarios

- **Ship non-grantable content alongside an app.** A provider wants to share notebooks, workspace
  content, and compliance documents with their app. These object types can’t be shared through the
  grant path, so the provider declares them in the manifest instead of recreating them in a setup
  script.
- **Share a governed service by reference.** A provider shares a PII-protected Cortex Search service
  so consumers query it by reference while the data stays on the provider side. The provider declares
  the service in the manifest.
- **Read consumer data and write results back.** A provider’s functions read the consumer’s data,
  combine it with provider data, and persist results in the consumer’s account. Because this runs
  code in the consumer’s account, the provider builds that logic in a setup script and shares the
  provider-side reference data through the manifest.
- **Call an external API from shared logic.** A provider’s shared analytics logic fetches data from a
  third-party API. The provider builds that logic in a setup script with an external access
  integration and declares any provider-side reference content in the manifest.
