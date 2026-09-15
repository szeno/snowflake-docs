# ALTER APPLICATION

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Modifies the properties of an installed Snowflake Native App. Use ALTER APPLICATION to upgrade an app to a
specific version or patch. This command is also used to set other properties for an app.

See also:
:   [CREATE APPLICATION](/sql-reference/sql/create-application), [DESCRIBE APPLICATION](/sql-reference/sql/desc-application), [DROP APPLICATION](/sql-reference/sql/drop-application), [SHOW APPLICATIONS](/sql-reference/sql/show-applications)

## Syntax

Copy code

```
ALTER APPLICATION [ IF EXISTS ] <name> SET
  [ COMMENT = '<string-literal>' ]
  [ SHARE_EVENTS_WITH_PROVIDER = { TRUE | FALSE } ]
  [ DEBUG_MODE = { TRUE | FALSE } ]
  [ AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = { '<timestamp>' | 'INDEFINITE' | 'NEVER' } ]

ALTER APPLICATION [ IF EXISTS ] <name> UNSET
  [ COMMENT ]
  [ SHARE_EVENTS_WITH_PROVIDER ]
  [ DEBUG_MODE ]
  [ AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL ]

ALTER APPLICATION [ IF EXISTS ] <name> RENAME TO <new_app_name>

ALTER APPLICATION <name> SET FEATURE POLICY <policy_name> [ FORCE ]

ALTER APPLICATION <name> UNSET FEATURE POLICY;

ALTER APPLICATION <name> SET MAINTENANCE POLICY <policy_name> [ FORCE ]

ALTER APPLICATION <name> UNSET MAINTENANCE POLICY

ALTER APPLICATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER APPLICATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER APPLICATION <name> SET SHARED TELEMETRY EVENTS ('<event_definition' [ , <event_definition>, ...])

ALTER APPLICATION <name> SET AUTHORIZE_TELEMETRY_EVENT_SHARING = { TRUE | FALSE }

ALTER APPLICATION <name> UNSET REFERENCES [ ( '<reference_name>' [ , '<reference_alias>' ] ) ]

ALTER APPLICATION <name> UPGRADE

ALTER APPLICATION <name> UPGRADE USING VERSION <version_name> [ PATCH <patch_num> ]

ALTER APPLICATION <name> UPGRADE USING <path_to_stage>
```

## Parameters

`name`
:   Specifies the identifier for the app being altered. If the identifier contains
    spaces, special characters, or mixed-case characters, the entire string must be enclosed
    in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`SET`
:   Specifies one (or more) properties to set for the app (separated by blank spaces, commas, or new lines). For more details
    about the properties you can set, see [CREATE APPLICATION](/sql-reference/sql/create-application).

    `COMMENT = '{string}'`
    :   Adds a comment or overwrites an existing comment for the app.

    `DEBUG_MODE = { TRUE | FALSE }`
    :   Enables or disables debug mode for the installed app.

        - `TRUE` enables debug mode for the installed app.
        - `FALSE` disables debug mode for the installed app.

        You can only set `DEBUG_MODE` on the app if the following conditions are met:

        > - The installed app is in the same account as the application package.
        > - The installed app must have been created in development mode.
        >
        >   Development mode is installed with an explicit stage, version, or patch.
        > - You have OWNERSHIP privileges on the installed app and your role has been granted
        >   the DEVELOP privilege on the application package used to create the installed app.

    `SHARE_EVENTS_WITH_PROVIDER = { TRUE | FALSE }`
    :   Specifies whether to share logs and event data with the provider.

    `AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = { '<timestamp>' | 'INDEFINITE' | 'NEVER' }`
    :   Specifies whether the provider can perform [restricted remote app operations](/developer-guide/native-apps/ui-consumer-remote-app-operation) on the app, such as the `run_sql` operation.

        - `'<timestamp>'`: Authorizes the provider to perform restricted remote app operations until the specified timestamp.
        - `'INDEFINITE'`: Authorizes the provider to perform restricted remote app operations indefinitely.
        - `'NEVER'`: Revokes authorization for restricted remote app operations.

        Default: `'NEVER'`

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET`
:   Specifies one (or more) properties and/or session parameters to unset for the app, which resets them to the defaults.

    You can reset multiple properties/parameters with a single ALTER statement; however, each property/parameter must be
    separated by a comma. When resetting a property/parameter, specify only the name; specifying a value for the
    property/parameter will return an error.

    - `COMMENT`
    - `DEBUG_MODE`
      Disables debug mode for the installed app. This clause is semantically the same as setting `DEBUG_MODE = FALSE`.
    - `SHARE_EVENTS_WITH_PROVIDER`
    - `AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL`
      Revokes authorization for restricted provider remote app operations. This is semantically the same as setting `AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = 'NEVER'`.
    - `TAG tag_name [ , tag_name ... ]`
    - `REFERENCES[ ( 'reference_name' [, 'reference_alias' ] ) ]`

      [Unsets a persistent reference](/sql-reference/references#label-unset-persistent-reference) for an app. If no arguments are passed,
      unsets all persistent references set for the app.

`RENAME TO new_app_name`
:   Specifies a new identifier for the app. This identifier must be unique for
    your account.

`SET FEATURE POLICY policy_name [ FORCE ]`
:   Specifies the feature policy to apply to the app. If a feature policy is already set on
    the app, you can use FORCE to set the feature policy without having to unset the
    feature policy first.

`UNSET FEATURE POLICY`
:   Removes the feature policy from the app. When a feature policy is removed from an app
    the account-level feature policy, if it exists, is applied.

`SET MAINTENANCE POLICY policy_name [ FORCE ]`
:   Specifies the [maintenance policy](/developer-guide/native-apps/consumer-maintenance-policies) to apply to the app. If a maintenance policy is already set on
    the app, you can use FORCE to set the maintenance policy without having to unset the
    maintenance policy first.

`UNSET MAINTENANCE POLICY`
:   Removes the maintenance policy from the app. When a maintenance policy is removed from an app,
    the account-level maintenance policy, if it exists, is applied.

`SET SHARED TELEMETRY EVENTS ( 'event_definition' [ , event_definition, ... ] )`
:   Specifies the optional event definition to enable for an app.

`SET AUTHORIZE_TELEMETRY_EVENT_SHARING = { TRUE | FALSE }`
:   When set to TRUE, enables all required event definitions for an app. However, optional event definitions
    remain disabled. Use the SET SHARED TELEMETRY EVENTS clause to set optional event definitions for an app.

    Caution

    After setting this value to TRUE, you cannot reset the value back to FALSE if there are required event
    definitions in the app.

`UNSET REFERENCES[ ( 'reference_name' [ , 'reference_alias' ] ) ]`
:   Removes the specified references from the app.

`UPGRADE`
:   Upgrades the app if the provider has published a new version or patch for the app.

    An app is automatically upgraded when the provider sets the release directive of the app. However, this command may be used to
    begin the upgrade immediately without waiting for automatic upgrade to take place. This command may only be used on apps
    that were not created in development mode. Apps in development mode are installed from a listing or without specifying a stage
    or version, and are primarily intended to test the upgrade process.

`UPGRADE USING VERSION version_name [ PATCH patch_num ]`
:   Upgrades the app to the specified version. If `patch_num` is not specified,
    the latest patch is used. This command is only valid for apps that were installed by
    specifying a version and patch.

`UPGRADE USING path_to_stage`
:   Upgrades the app using files on a named stage at the path specified by `path_to_stage`.

    This clause applies only if you installed the app from a named stage.

## Usage notes

- If you do not specify values for optional parameters, values for these parameters are taken from the `manifest.yml` file. If you
  specify values in both the manifest and when running the command, values specified in the command take precedence.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
