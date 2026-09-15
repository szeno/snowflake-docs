# Share content privately in a Snowflake Native App

[Preview Feature — Private](/release-notes/preview-features)

Declarative sharing in the Snowflake Native App Framework (Declarative Native Apps) is in Private Preview. Support isn’t in
production and is available only to selected accounts. To request access, contact your Snowflake
representative.

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to share content privately in a Snowflake Native App by marking objects as private
in the manifest file.

## Mark shared content as private

Set `private: true` on a database, schema, or object in the `shared_content` section to hide it from
direct use by consumers:

Copy code

```
shared_content:
  databases:
    - <db_name>:
        schemas:
          - <schema_name>:
              tables:
                - <table_name>:
                    private: true
```

A private object is hidden from direct consumer use, but other objects within the app can still use
it. This lets you share building-block objects without exposing them as part of the consumer-facing
interface.

## Control access with application roles

To make a shared object available to consumers, add it to the `roles` list for that object. This
works the same way as application roles in declarative sharing: the framework creates an application
role to share the object. For more information, see
[Declarative roles for shared content](/developer-guide/native-apps/sharing-manifest-roles).

For the full syntax, see the [Manifest file reference](/developer-guide/native-apps/manifest-reference).
