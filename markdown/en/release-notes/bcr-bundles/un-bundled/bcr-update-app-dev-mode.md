# Snowflake Native App Framework: Need to recreate or update some APPLICATION objects

As part of the rollout of the
[Support for reference and privilege validation in the manifest file](/release-notes/2023/7_42#label-nativeapps-refs-dev-mode)
feature, an APPLICATION object created in development mode that was based on staged files will no longer
function correctly if the APPLICATION object contains a versioned schema.

To resolve this issue, Snowflake recommends doing one of the following:

- If you do not need to preserve the existing APPLICATION object, you can delete the app and recreate it
  using the [CREATE APPLICATION](/sql-reference/sql/create-application) command.

  Following this process recreates the app and enables the new functionality added in the
  [Support for reference and privilege validation in the manifest file](/release-notes/2023/7_42#label-nativeapps-refs-dev-mode)
  feature.
- If you need to preserve an existing APPLICATION object, use the [ALTER APPLICATION](/sql-reference/sql/alter-application)
  command and specify the staged files using UPGRADE USING <path\_to\_stage>.

  Following this process will return the app to a functioning state, but it will not include the new
  functionality added in the
  [Support for reference and privilege validation in the manifest file](/release-notes/2023/7_42#label-nativeapps-refs-dev-mode)
  feature.
