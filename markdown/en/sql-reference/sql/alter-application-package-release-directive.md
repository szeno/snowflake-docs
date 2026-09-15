# ALTER APPLICATION PACKAGE … RELEASE DIRECTIVE (Legacy)

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Modifies the properties of an existing application package. Use this command to modify a release directive to a new version or patch.

Note

Most of the syntax described in this topic applies to application packages that do not use release channels. To add or remove accounts from a release directive in a specific release channel, include the optional MODIFY RELEASE CHANNEL clause. If omitted, the command applies only to release directives on the default release channel. To modify the release directive of an application package that uses release channels, see [ALTER APPLICATION PACKAGE … MODIFY RELEASE CHANNEL](/sql-reference/sql/alter-application-package-release-channel).

See also:
:   [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) , [ALTER APPLICATION PACKAGE … VERSION](/sql-reference/sql/alter-application-package-version)

## Syntax

Copy code

```
ALTER APPLICATION PACKAGE <name>
  MODIFY RELEASE DIRECTIVE <release_directive>
  VERSION = <version_identifier>
  PATCH = <patch_num>
  [ UPGRADE_AFTER = '<timestamp>' ]
  [ UPGRADE_IN_MAINTENANCE_WINDOW = { TRUE | FALSE } ]
  [ UPGRADE_DEADLINE = '<timestamp>' ]

ALTER APPLICATION PACKAGE <name>
  [ MODIFY RELEASE CHANNEL <release_channel_name> ]
  MODIFY RELEASE DIRECTIVE <release_directive>
  ADD ACCOUNTS = ( <organization_name>.<account_name> [ , <organization_name>.<account_name> , ... ] )
  [ VERSION = <version_identifier> PATCH = <patch_num> ]
  [ FORCE ]

ALTER APPLICATION PACKAGE <name>
  [ MODIFY RELEASE CHANNEL <release_channel_name> ]
  MODIFY RELEASE DIRECTIVE <release_directive>
  REMOVE ACCOUNTS = ( <organization_name>.<account_name> [ , <organization_name>.<account_name> , ... ] )
  [ VERSION = <version_identifier> PATCH = <patch_num> ]

ALTER APPLICATION PACKAGE <name>
  SET DEFAULT RELEASE DIRECTIVE
  VERSION = <version_identifier>
  PATCH = <patch_num>
  [ UPGRADE_AFTER = '<timestamp>' ]
  [ UPGRADE_IN_MAINTENANCE_WINDOW = { TRUE | FALSE } ]
  [ UPGRADE_DEADLINE = '<timestamp>' ]

ALTER APPLICATION PACKAGE <name>
  SET RELEASE DIRECTIVE <release_directive>
  ACCOUNTS = ( <organization_name>.<account_name> [ , <organization_name>.<account_name> , ... ] )
  VERSION = <version_identifier>
  PATCH = <patch_num>
  [ UPGRADE_AFTER = '<timestamp>' ]
  [ UPGRADE_IN_MAINTENANCE_WINDOW = { TRUE | FALSE } ]
  [ UPGRADE_DEADLINE = '<timestamp>' ]
  [ FORCE ]

ALTER APPLICATION PACKAGE <name> UNSET RELEASE DIRECTIVE <release_directive>
```

## Parameters

`name`
:   Specifies the identifier for the application package. If the identifier contains spaces, special characters, or mixed-case characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`MODIFY RELEASE DIRECTIVE release_directive` `VERSION = version_identifier` `PATCH = patch_num`
:   Modifies the version and patch level of the specified custom release directive.

`[ MODIFY RELEASE CHANNEL release_channel_name ]` `MODIFY RELEASE DIRECTIVE release_directive` `ADD ACCOUNTS = ( organization_name.account_name [ , organization_name.account_name , ... ] )` `[ VERSION = version_identifier PATCH = patch_num ]` `[ FORCE ]`
:   Adds accounts to the specified custom release directive.

    Specify `MODIFY RELEASE CHANNEL` to add accounts to a release directive in a specific release channel.

    If you specify `VERSION` and `PATCH`, the version and patch are updated for all accounts in the release directive, including accounts that were already in it. You must specify both or neither.

    Use `FORCE` to atomically move accounts that are already assigned to a different release directive. Without `FORCE`, the command fails if any of the specified accounts are already in another release directive.

`[ MODIFY RELEASE CHANNEL release_channel_name ]` `MODIFY RELEASE DIRECTIVE release_directive` `REMOVE ACCOUNTS = ( organization_name.account_name [ , organization_name.account_name , ... ] )` `[ VERSION = version_identifier PATCH = patch_num ]`
:   Removes accounts from the specified custom release directive.

    Specify `MODIFY RELEASE CHANNEL` to remove accounts from a release directive in a specific release channel.

    If you specify `VERSION` and `PATCH`, the version and patch are updated for all accounts remaining in the release directive after the removal. You must specify both or neither.

`SET`
:   Specifies one (or more) properties to set for the application package (separated by blank spaces, commas, or new lines). For more details
    about the properties you can set, see [CREATE APPLICATION](/sql-reference/sql/create-application).

    `DEFAULT RELEASE DIRECTIVE VERSION = version_identifier PATCH = patch_num`
    :   Sets the version and patch level of the application package that should be installed for consumers by default.

    `RELEASE DIRECTIVE release_directive` `ACCOUNTS = ( organization_name.account_name [ , organization_name.account_name , ... ] )` `VERSION = version_identifier` `PATCH = patch_num` `[ FORCE ]`
    :   Creates a custom release directive for the specified accounts.

        Use the ACCOUNTS clause to specify the list of accounts to which this release directive applies.

        Use the VERSION and PATCH clauses to specify the version identifier and patch number to be installed for these accounts.

        Use `FORCE` to atomically move accounts that are already assigned to a different release directive. Without `FORCE`, the command fails if any of the specified accounts are already in another release directive.

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
:   Specifies one (or more) properties and/or session parameters to unset for the application package, which resets them to the defaults.

    `UNSET RELEASE DIRECTIVE release_directive`
    :   Removes the specified custom release directive from the application package.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Application package | Required to modify a release directive. |
| MANAGE VERSIONS | Account | Global privilege that allows modifying release directives on any application package. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Modifying the release directive requires the OWNERSHIP privilege on the application or the global MANAGE VERSIONS privilege.
- If you do not specify the values for the optional properties, the command uses the values specified in the application manifest file.

  If you specify values for the properties in the command and in the application manifest file, the values specified in the command take
  precedence.

## Examples

The following example adds an account to the custom release directive `my_directive`:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package
  MODIFY RELEASE DIRECTIVE my_directive
  ADD ACCOUNTS = (myorg.myaccount)
  VERSION = V1
  PATCH = 0;
```

The following example removes an account from the custom release directive `my_directive`:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package
  MODIFY RELEASE DIRECTIVE my_directive
  REMOVE ACCOUNTS = (myorg.myaccount)
  VERSION = V1
  PATCH = 0;
```

The following example adds an account to the custom release directive `my_directive` in the release channel `my_channel`, and moves the account from any other release directive it belongs to:

Copy code

```
ALTER APPLICATION PACKAGE my_app_package
  MODIFY RELEASE CHANNEL my_channel
  MODIFY RELEASE DIRECTIVE my_directive
  ADD ACCOUNTS = (myorg.myaccount)
  VERSION = V1
  PATCH = 0
  FORCE;
```
