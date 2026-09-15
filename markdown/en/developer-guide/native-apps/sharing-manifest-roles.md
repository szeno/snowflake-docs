# Declarative roles for shared content in a Snowflake Native App

[Preview Feature — Private](/release-notes/preview-features)

Declarative sharing in the Snowflake Native App Framework (Declarative Native Apps) is in Private Preview. Support isn’t in
production and is available only to selected accounts. To request access, contact your Snowflake
representative.

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to define roles for shared content in the manifest file of a Snowflake Native App.
Declaring roles in the manifest keeps role configuration versioned and auditable alongside the rest
of the package, rather than defined in the setup script.

## Define roles in the manifest

Add a `roles` section to the manifest to declare application roles and their privileges:

Copy code

```
roles:
  - <role_name>:
      comment: <comment>
```

You can then reference a declared role on a shared object in the `shared_content` section to grant
access to that object.

## Behavior in a Snowflake Native App

Declarative roles in a `NATIVE` application package behave like declarative roles in a standalone
declarative share, with the following differences:

- Declared roles are created automatically if they don’t already exist, and they’re visible within
  the context of the setup script.
- The setup script can manipulate declaratively defined roles.
- Unlike a standalone declarative application, removing a declared role in a later version doesn’t
  remove the application role from installed instances, because these roles might still be in use by
  objects created in the setup script. The setup script must explicitly remove the role.

For the full syntax, see the [Manifest file reference](/developer-guide/native-apps/manifest-reference).
