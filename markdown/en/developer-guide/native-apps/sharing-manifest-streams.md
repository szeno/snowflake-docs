# Create streams on shared content in a Snowflake Native App

[Preview Feature — Private](/release-notes/preview-features)

Declarative sharing in the Snowflake Native App Framework (Declarative Native Apps) is in Private Preview. Support isn’t in
production and is available only to selected accounts. To request access, contact your Snowflake
representative.

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how streams work with content shared through the manifest file of a
Snowflake Native App.

## Streams on directly shared content

Declaring content in the manifest lets consumers create streams on shared tables when the shared
table has `CHANGE_TRACKING = TRUE`. This applies only to content shared directly through the
manifest, not to application views on shared content.

Consumers can’t create streams on proxy views in a versioned schema. A stream on such a view would
be locked to a single version and would break when that version no longer exists.

For the object types and syntax you can declare in the manifest, see
[Share content using the manifest](/developer-guide/native-apps/sharing-manifest-about) and the
[Manifest file reference](/developer-guide/native-apps/manifest-reference).
