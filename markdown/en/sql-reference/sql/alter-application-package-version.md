# ALTER APPLICATION PACKAGE … VERSION

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Modifies the versioning of an existing application package in the Snowflake Native App Framework.

See also:
:   [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) , [ALTER APPLICATION PACKAGE … RELEASE DIRECTIVE (Legacy)](/sql-reference/sql/alter-application-package-release-directive)

## Syntax

Copy code

```
ALTER APPLICATION PACKAGE <name> ADD VERSION [ <version_identifier> ]
  USING <path_to_version_directory> [ LABEL = '<display_label>' ]

ALTER APPLICATION PACKAGE <name> DROP VERSION <version_identifier>

ALTER APPLICATION PACKAGE <name> ADD PATCH [<patch_number>] FOR VERSION [<version_identifier>]
  USING <path_to_version_directory> [ LABEL = '<display_label>' ]
```

## Parameters

`name`
:   Specifies the identifier for the application package to alter. If the identifier contains
    spaces, special characters, or mixed-case characters, the entire string must be enclosed
    in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`ADD VERSION [ version_identifier ] USING path_to_version_directory`
:   Adds a version or patch using the application files located in the path to a stage location specified by
    `path_to_version_directory`.

    You can specify an identifier for this version using `version_identifier`. If you do
    not specify a `version_identifier` in the manifest file, you must specify a
    `version_identifier` as part of this command. If you specify `version_identifier`
    as part of this command, it takes precedence over `version_identifier` specified
    in the manifest file.

`[ LABEL = 'display_label' ]`
:   You can use the LABEL clause to specify a label for this new version. This label is displayed
    to the consumer. If you omit the LABEL clause, the label specified in the `manifest.yml`
    file is used.

`DROP VERSION version_identifier`
:   Drops a version with the specified version identifier. A version may only be dropped when there are no release directives referring to it and no application is using that version.

    An application is considered to be using a version if it is the application’s current version, or if it was the application’s previous version and the upgrade has not yet finalized (jobs are still running on the previous version). Disabled applications do not block a version drop.

    Use the [APPLICATION\_STATE view](/sql-reference/data-sharing-usage/application-state-view) view to monitor
    the state of the application instances. Use the [SHOW VERSIONS IN APPLICATION PACKAGE](/sql-reference/sql/show-versions) command to monitor the
    status of the dropped version.

`ADD PATCH patch_number` `FOR VERSION version_identifier` `USING path_to_version_directory [ LABEL = 'display_label' ]`
:   Adds a patch for the specified version (`version_identifier`) using the application files located in the specified path to a
    stage location (`path_to_version_directory`).

    You can use the LABEL clause to specify a label for this new patch. This label is displayed to the consumer. If you omit the LABEL
    clause, the label specified in the `manifest.yml` file is used.

## Usage notes

- Version identifiers have a maximum limit of 30 characters.
- A single version can have up to 130 patches.
- Modifying the version requires a role with the OWNERSHIP privilege on the application or the global MANAGE VERSIONS privilege.
- If you do not specify the values for the optional properties, the command uses the values specified in the
  application manifest file.

  If you specify values for the properties in the command and in the application manifest file, the values
  specified in the command take precedence.
- If two versions are active, for example, if the current version has not finished rolling out, adding
  a new version results in an error.

## Examples

Copy code

```
ALTER APPLICATION PACKAGE hello_snowflake_package
  ADD VERSION v1_1
  USING '@hello_snowflake_code.core.hello_snowflake_stage';
```

```
+---------------------------------------------------------------------------------------+---------+-------+
| status                                                                                | version | patch |
|---------------------------------------------------------------------------------------+---------+-------|
| Version 'v1_1' of application package 'hello_snowflake_package' created successfully. | v1_1    |     0 |
+---------------------------------------------------------------------------------------+---------+-------+
```
