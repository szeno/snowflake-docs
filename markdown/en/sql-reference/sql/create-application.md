# CREATE APPLICATION

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Creates a Snowflake Native App based on an application package or listing. Providers use this
command to install an app in their development account.

When this command runs, it runs the
[setup script](/developer-guide/native-apps/creating-setup-script) to create the app.

See also:
:   [ALTER APPLICATION](/sql-reference/sql/alter-application), [DESCRIBE APPLICATION](/sql-reference/sql/desc-application), [DROP APPLICATION](/sql-reference/sql/drop-application), [SHOW APPLICATIONS](/sql-reference/sql/show-applications)

## Syntax

Copy code

```
CREATE APPLICATION <name> FROM APPLICATION PACKAGE <package_name>
   [ USING RELEASE CHANNEL { QA | ALPHA | DEFAULT } ]
   [ COMMENT = '<string_literal>' ]
   [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
   [ AUTHORIZE_TELEMETRY_EVENT_SHARING = { TRUE | FALSE } ]
   [ AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = { '<timestamp>' | 'INDEFINITE' | 'NEVER' } ]
   [ WITH FEATURE POLICY = <policy_name> ]

CREATE APPLICATION <name> FROM APPLICATION PACKAGE <package_name>
  USING <path_to_version_directory>
  [ DEBUG_MODE = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [, ...] ) ]
  [ AUTHORIZE_TELEMETRY_EVENT_SHARING = { TRUE | FALSE } ]
  [ AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = { '<timestamp>' | 'INDEFINITE' | 'NEVER' } ]
  [ WITH FEATURE POLICY = <policy_name> ]

CREATE APPLICATION <name> FROM APPLICATION PACKAGE <package_name>
  USING VERSION  <version_identifier> [ PATCH <patch_num> ]
  [ DEBUG_MODE = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ AUTHORIZE_TELEMETRY_EVENT_SHARING = { TRUE | FALSE } ]
  [ AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = { '<timestamp>' | 'INDEFINITE' | 'NEVER' } ]
  [ WITH FEATURE POLICY = <policy_name> ]

CREATE APPLICATION <name> FROM LISTING <listing_global_name>
   [ USING RELEASE CHANNEL { QA | ALPHA | DEFAULT } ]
   [ COMMENT = '<string_literal>' ]
   [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
   [ BACKGROUND_INSTALL = { TRUE | FALSE } ]
   [ AUTHORIZE_TELEMETRY_EVENT_SHARING = { TRUE | FALSE } ]
   [ AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = { '<timestamp>' | 'INDEFINITE' | 'NEVER' } ]
   [ WITH FEATURE POLICY = <policy_name> ]
```

## Required parameters

`name`
:   Specifies the identifier for the app. Must be unique for your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces
    or special characters unless the entire identifier string is enclosed in double quotes
    (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, refer to [Identifier requirements](/sql-reference/identifiers-syntax).

`FROM APPLICATION PACKAGE package_name`
:   Specifies the name of the application package used to create the app. To use this
    clause to create an app from an application package without specifying a stage or a
    version/patch, the application package must have a default release directive defined.

    This clause can only be used to create an app in the same account as the application
    package. This clause cannot be used to create an app in development mode.

`FROM LISTING listing_global_name`
:   Specifies the global name of the listing that contains the application package used to create the app. Use the listing global name (for example, `GZSNP47HXH1`) rather than the display name.

`USING RELEASE CHANNEL { QA | ALPHA | DEFAULT }`
:   Specifies the release channel defined in the application package or listing used to create
    the app. If you do not specify this clause, the default release channel is used.

    - `QA` specifies the quality assurance release channel.
    - `ALPHA` specifies the alpha release channel.
    - `DEFAULT` specifies the default release channel.

    This clause can be used only when creating an app from an application package that has a
    release directive defined or when creating an app from a listing.

`USING path_to_version_directory`
:   Specifies the path to the stage that contains the files required by the app.

`USING version [ PATCH patch_num ]`
:   Specifies the version, and optionally the patch, defined in the application package
    used to create the app.

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the app.

    Default: No value

`DEBUG_MODE = { TRUE | FALSE }`
:   Enables or disables [debug mode](/developer-guide/native-apps/installing-testing-application#label-native-apps-testing-debug-mode) for the app
    being created. Debug mode allows a provider to see the contents of the app.

    - `TRUE` enables debug mode for the installed app.
    - `FALSE` disables debug mode for the installed app.

    Note

    You can only enable debug mode under the following conditions:

    - The app is in the same account as the application package.
    - The app is being created based on a specific version or from files on a named stage.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`BACKGROUND_INSTALL = { TRUE | FALSE }`
:   Creates the app from a listing in the background. If you specify this clause, the
    command returns you to the prompt immediately, and the installation process continues in the
    background. To monitor that status of the installation, use the
    [DESCRIBE APPLICATION](/sql-reference/sql/desc-application) command.

    Note

    When this clause is used, the app is created even if the command fails. In this
    situation, use the [DROP APPLICATION](/sql-reference/sql/drop-application) command to delete the object before
    running the [CREATE APPLICATION](/sql-reference/sql/create-application) command again.

    This clause is primarily used by Snowsight to install a Snowflake Native App in the background. Background
    installation allows the consumer to navigate away from the listing in Snowsight during
    installation. A provider might use this clause when testing the installation of a Snowflake Native App
    from a listing before publishing the listing.

`AUTHORIZE_TELEMETRY_EVENT_SHARING = { TRUE | FALSE }`
:   Enables [logging and event sharing](/developer-guide/native-apps/event-about) in the app.

`AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = { '<timestamp>' | 'INDEFINITE' | 'NEVER' }`
:   Specifies whether the provider can perform [restricted remote app operations](/developer-guide/native-apps/ui-consumer-remote-app-operation) on the app, such as the `run_sql` operation.

    - `'<timestamp>'`: Authorizes the provider to perform restricted remote app operations until the specified timestamp.
    - `'INDEFINITE'`: Authorizes the provider to perform restricted remote app operations indefinitely.
    - `'NEVER'`: Revokes authorization for restricted remote app operations.

    Default: `'NEVER'`

`WITH FEATURE POLICY = policy_name`
:   Create the app with the specified feature policy. If the app attempts to create an object that the feature policy prohibits (such as a database), the command fails.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE APPLICATION | Account |  |
| DEVELOP | Application package |  |
| INSTALL | Application package |  |
| IMPORT SHARE  CREATE APPLICATION | Account | These privileges are required to create an app in an account different than the account that contains the application package. |
| CREATE PREVIEW APPLICATION | Account | Required to create an app from a non-default release channel (QA or ALPHA). Not required when using `USING RELEASE CHANNEL DEFAULT` or when the `USING RELEASE CHANNEL` clause is omitted. |
| APPLY FEATURE POLICY  APPLY or OWNERSHIP | Account  Feature policy | These privileges are required to apply a feature policy when creating the app using the WITH FEATURE POLICY clause. |

Expand

Show lessSee more

## Usage notes

- To create an app directly from an application package, you must specify a default release directive in the application package.
- The app differs from a database in the following ways:

  - An app may not be transient.
  - The role with the OWNERSHIP privilege on the app has the following abilities and limitations:
    - Can drop the database or modify the COMMENT property and any properties that are specific to the app.
    - Cannot see or modify the contents of the app except via the privileges granted the application roles.
    - Cannot create a database-level object, such as a schema or a database role.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Copy code

```
CREATE APPLICATION hello_snowflake_app
  FROM APPLICATION PACKAGE hello_snowflake_package
  USING VERSION v1;
```

```
+---------------------------------------------------------+
| status                                                  |
|---------------------------------------------------------|
| Application 'hello_snowflake_app' created successfully. |
+---------------------------------------------------------+
```

Copy code

```
CREATE APPLICATION hello_snowflake_app
  FROM APPLICATION PACKAGE hello_snowflake_package
  USING '@hello_snowflake_code.core.hello_snowflake_stage';
```

```
+---------------------------------------------------------+
| status                                                  |
|---------------------------------------------------------|
| Application 'hello_snowflake_app' created successfully. |
+---------------------------------------------------------+
```
