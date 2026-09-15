# ALTER APPLICATION PACKAGE … MODIFY RELEASE CHANNEL

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Modifies the release channels defined for an existing application package. Use this command
to modify a release channel, change the version or patch assigned to a release channel, or
set the release directive for a release channel.

Note

The syntax in this topic only applies to application packages that use release channels. For more information, see
[Publish an app using release channels](/developer-guide/native-apps/release-channels). To set the release directive
for an application package that does not use release channels, see
[ALTER APPLICATION PACKAGE … RELEASE DIRECTIVE (Legacy)](/sql-reference/sql/alter-application-package-release-directive).

See also:
:   [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package), [ALTER APPLICATION PACKAGE … VERSION](/sql-reference/sql/alter-application-package-version),
    [ALTER APPLICATION PACKAGE … RELEASE DIRECTIVE (Legacy)](/sql-reference/sql/alter-application-package-release-directive),
    [SHOW RELEASE DIRECTIVES](/sql-reference/sql/show-release-directives)

## Syntax

Copy code

```
ALTER APPLICATION PACKAGE <name>
  REGISTER VERSION [ <version_identifier> ]
  USING <path_to_version_directory>
  [ LABEL = '<display_label>' ]

ALTER APPLICATION PACKAGE <name>
  DEREGISTER VERSION <version_identifier>

ALTER APPLICATION PACKAGE <name>
  MODIFY RELEASE CHANNEL <release_channel>
  ADD VERSION <version_identifier>

ALTER APPLICATION PACKAGE <name>
  MODIFY RELEASE CHANNEL <release_channel>
  DROP VERSION <version_identifier>

ALTER APPLICATION PACKAGE <name>
  MODIFY RELEASE CHANNEL <release_channel>
  ADD ACCOUNTS = ( <organization_name>.<account_name> [ , <organization_name>.<account_name> , ... ] )

ALTER APPLICATION PACKAGE <name>
  MODIFY RELEASE CHANNEL <release_channel>
  REMOVE ACCOUNTS = ( <organization_name>.<account_name> [ , <organization_name>.<account_name> , ... ] )

ALTER APPLICATION PACKAGE <name>
  MODIFY RELEASE CHANNEL <release_channel>
  SET ACCOUNTS = ( <organization_name>.<account_name> [ , <organization_name>.<account_name> , ... ] )

ALTER APPLICATION PACKAGE <name>
  MODIFY RELEASE CHANNEL <release_channel>
  SET DEFAULT RELEASE DIRECTIVE
  VERSION = <version_identifier>
  PATCH = <patch_num>
  [ UPGRADE_AFTER = '<timestamp>' ]
  [ UPGRADE_IN_MAINTENANCE_WINDOW = { TRUE | FALSE } ]
  [ UPGRADE_DEADLINE = '<timestamp>' ]

ALTER APPLICATION PACKAGE <name>
  MODIFY RELEASE CHANNEL <release_channel>
  SET RELEASE DIRECTIVE <release_directive>
  ACCOUNTS = ( <organization_name>.<account_name> [ , <organization_name>.<account_name> , ... ] )
  VERSION = <version_identifier>
  PATCH = <patch_num>
  [ UPGRADE_AFTER = '<timestamp>' ]
  [ UPGRADE_IN_MAINTENANCE_WINDOW = { TRUE | FALSE } ]
  [ UPGRADE_DEADLINE = '<timestamp>' ]

ALTER APPLICATION PACKAGE <name>
  MODIFY RELEASE CHANNEL <release_channel>
  MODIFY RELEASE DIRECTIVE <release_directive>
  VERSION = <version_identifier>
  PATCH = <patch_num>
  [ UPGRADE_AFTER = '<timestamp>' ]
  [ UPGRADE_IN_MAINTENANCE_WINDOW = { TRUE | FALSE } ]
  [ UPGRADE_DEADLINE = '<timestamp>' ]

ALTER APPLICATION PACKAGE <name>
  MODIFY RELEASE CHANNEL <release_channel>
  UNSET RELEASE DIRECTIVE <release_directive>
```

## Parameters

`name`
:   Specifies the identifier for the application package. If the identifier contains spaces, special characters, or mixed-case characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`REGISTER VERSION [ version_identifier ] USING path_to_version_directory [ LABEL = 'display_label' ]`
:   Registers a new version in the application package using the files in the stage path specified by `path_to_version_directory`. The registered version is not assigned to any release channel until you use `ADD VERSION` to assign it.

    Use `version_identifier` to specify a name for the version. If you do not specify a `version_identifier` in the `manifest.yml` file, you must specify one in this command. If you define a version identifier in the `manifest.yml` file and also specify one in this command, the command value takes precedence. If neither the command nor the `manifest.yml` file specifies a version identifier, the command fails with an error.

    Use the optional `LABEL` clause to specify a display label for the version. This label is shown to consumers. If omitted, the label from the `manifest.yml` file is used.

    Note

    `REGISTER VERSION` applies only to application packages that have release channels enabled. For application packages without release channels, use [ALTER APPLICATION PACKAGE … VERSION](/sql-reference/sql/alter-application-package-version) instead.

`DEREGISTER VERSION version_identifier`
:   Removes the specified version and its associated patches from the application package. An application package can have at most two registered versions at a time. Use this command to free up a version slot before registering a new version when the application package already has two versions.

    A version can only be deregistered when it is not assigned to any release channel and no installed application instances are running on it.

`MODIFY RELEASE CHANNEL release_channel`
:   Specifies the release channel to modify. The supported values are:

    - `ALPHA`
    - `QA`
    - `DEFAULT`

    For more information about release channels, see [Publish an app using release channels](/developer-guide/native-apps/release-channels).

`MODIFY RELEASE CHANNEL release_channel ADD VERSION version_identifier`
:   Adds a previously registered version to the specified release channel, making it available for release directives in that channel. A release channel can contain at most two versions at a time.

    Adding a version to the QA release channel does not trigger the automated security scan. To trigger the scan, add the version to the ALPHA or DEFAULT release channel.

`MODIFY RELEASE CHANNEL release_channel DROP VERSION version_identifier`
:   Removes the specified version from the release channel. This operation is asynchronous: the version is fully removed only after all consumer installations on that version have been upgraded to another version.

`MODIFY RELEASE CHANNEL release_channel ADD ACCOUNTS = ( organization_name.account_name [ , ... ] )`
:   Adds the specified consumer accounts to the release channel, allowing them to access versions and patches assigned to it.

`MODIFY RELEASE CHANNEL release_channel REMOVE ACCOUNTS = ( organization_name.account_name [ , ... ] )`
:   Removes the specified consumer accounts from the release channel.

`MODIFY RELEASE CHANNEL release_channel SET ACCOUNTS = ( organization_name.account_name [ , ... ] )`
:   Replaces the entire list of consumer accounts for the release channel with the specified accounts. All accounts previously in the channel that are not in the new list are removed.

`VERSION = version_identifier` `PATCH = patch_num`
:   Modifies the version and patch level of the specified custom release directive.

`SET`
:   Specifies one or more properties to set for the application package, separated by blank spaces, commas, or new lines. For more details
    about the properties you can set, see [CREATE APPLICATION](/sql-reference/sql/create-application).

    `DEFAULT RELEASE DIRECTIVE VERSION = version_identifier PATCH = patch_num`
    :   Sets the version and patch level of the application package that should be installed for consumers by default.

    `RELEASE DIRECTIVE release_directive` `ACCOUNTS = ( organization_name.account_name [ , organization_name.account_name , ... ] )` `VERSION = version_identifier` `PATCH = patch_num`
    :   Creates a custom release directive for the specified accounts.

        Use the ACCOUNTS clause to specify the list of accounts that this release directive applies to.

        Use the VERSION and PATCH clauses to specify the version identifier and patch number to be installed for these accounts.

`UPGRADE_AFTER = 'timestamp'`
:   Specifies the date and time when the automated upgrade process begins. Consumers can manually
    upgrade an app to a new version or patch before this date.

    This value can be any valid date and time format.

`UPGRADE_IN_MAINTENANCE_WINDOW = { TRUE | FALSE }`
:   When set to TRUE, upgrades respect consumer maintenance policies. Instead of upgrading immediately,
    the upgrade is delayed until the consumer’s next maintenance window or until the upgrade deadline
    is reached, whichever comes first.

    When this parameter is set to TRUE, the UPGRADE\_DEADLINE parameter is required.

    You can’t set the UPGRADE\_AFTER and UPGRADE\_IN\_MAINTENANCE\_WINDOW parameters at the same time.
    If you try to set both, the command fails with an error.

    For more information, see [Consumer-controlled maintenance policies: Provider guide](/developer-guide/native-apps/consumer-maintenance-policies-provider).

`UPGRADE_DEADLINE = 'timestamp'`
:   Required when UPGRADE\_IN\_MAINTENANCE\_WINDOW is set to TRUE. Specifies the deadline by which the
    upgrade must be completed. After this time, the system automatically upgrades the application
    regardless of the consumer’s maintenance policy.

    Set the deadline to a date and time that allows sufficient time for consumers to complete the
    upgrade within their maintenance windows.

`UNSET`
:   Specifies one or more properties or session parameters to unset for the application package, which resets them to the defaults.

    `UNSET RELEASE DIRECTIVE release_directive`
    :   Removes the specified custom release directive from the application package.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Application package | Required to modify release channels or register versions for the application package. |
| MANAGE VERSIONS | Account | Global privilege that allows modifying release channels and release directives on any application package. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Modifying the release directive requires the OWNERSHIP privilege on the application or the global MANAGE VERSIONS privilege.
- If you do not specify the values for the optional properties, the command uses the values specified in the application
  manifest file.
- If you specify values for the properties in the command and in the application manifest file, the values specified in
  the command take precedence.

## Examples

The following example adds version `V1` to the default release channel:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package
  MODIFY RELEASE CHANNEL DEFAULT
  ADD VERSION V1;
```

```
+---------------------------------------------------------------------------------------------------------+
| status                                                                                                  |
|---------------------------------------------------------------------------------------------------------|
| Version V1 added to release channel DEFAULT in application package my_app_package                       |
+---------------------------------------------------------------------------------------------------------+
```

The following example modifies the default release directive of the default release channel to set the version to
`V1` and the patch to `0`:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package
  MODIFY RELEASE CHANNEL DEFAULT
  SET DEFAULT RELEASE DIRECTIVE
  VERSION = V1
  PATCH = 0;
```

```
+---------------------------------------------------------------------------------------------------------+
| status                                                                                                  |
|---------------------------------------------------------------------------------------------------------|
| Version V1 added to release channel DEFAULT in application package my_app_package                       |
+---------------------------------------------------------------------------------------------------------+
```

The following example registers version `V2` in the application package:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package
  REGISTER VERSION V2
  USING '@my_app_package.core.app_stage/v2';
```

```
+---------------------------------------------------------------------------------------------------------+
| status                                                                                                  |
|---------------------------------------------------------------------------------------------------------|
| Version V2 registered in application package my_app_package                                             |
+---------------------------------------------------------------------------------------------------------+
```

The following example adds the `ORG1.ACCOUNT1` account to the ALPHA release channel:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package
  MODIFY RELEASE CHANNEL ALPHA
  ADD ACCOUNTS = (ORG1.ACCOUNT1);
```

```
+---------------------------------------------------------------------------------------------------------+
| status                                                                                                  |
|---------------------------------------------------------------------------------------------------------|
| Statement executed successfully.                                                                        |
+---------------------------------------------------------------------------------------------------------+
```
