# ALTER ORGANIZATION PROFILE

Modifies the properties of an [organization profile](/user-guide/collaboration/organization-profiles/org-profiles-create-manage)
using an inline YAML manifest, or using a YAML manifest file located in a stage location.

See also:
:   [CREATE ORGANIZATION PROFILE](/sql-reference/sql/create-organization-profile), [DESCRIBE AVAILABLE ORGANIZATION PROFILE](/sql-reference/sql/desc-available-organization-profile), [DESCRIBE ORGANIZATION PROFILE](/sql-reference/sql/desc-organization-profile), [DROP ORGANIZATION PROFILE](/sql-reference/sql/drop-organization-profile), [SHOW AVAILABLE ORGANIZATION PROFILES](/sql-reference/sql/show-available-organization-profiles), [SHOW ORGANIZATION PROFILES](/sql-reference/sql/show-organization-profiles), [SHOW VERSIONS IN ORGANIZATION PROFILE](/sql-reference/sql/show-versions-in-organization-profile)

## Syntax

Copy code

```
ALTER ORGANIZATION PROFILE [ IF EXISTS ] <name> AS '<yaml_manifest_string>'

ALTER ORGANIZATION PROFILE [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER ORGANIZATION PROFILE [ IF EXISTS ] <name> PUBLISH

ALTER ORGANIZATION PROFILE <name> ADD VERSION [ [ IF NOT EXISTS ] <version_alias_name> ]
  FROM @<yaml_manifest_stage_location>

ALTER ORGANIZATION PROFILE <name> ADD LIVE VERSION [ [ IF NOT EXISTS ] <version_alias_name> ]
  FROM LAST

ALTER ORGANIZATION PROFILE <name> COMMIT

ALTER ORGANIZATION PROFILE <name> ABORT
```

## Parameters

`name`
:   Specifies the identifier (name) for the organization profile being altered. Organization profile names can only contain uppercase characters or numbers, and they must start with an uppercase character.

`RENAME TO new_name`
:   Changes the name of the organization profile to `new_name`. The new identifier must be unique within the current organization. The identifier must conform to Snowflake identifier requirements. See [Identifier requirements](/sql-reference/identifiers-syntax). Additionally, organization profile names can only contain uppercase characters or numbers, and they must start with an uppercase character.

    Note

    An organization profile with the same name cannot already exist in the organization;
    otherwise, the statement returns an error.

`PUBLISH`
:   Makes a previously undiscoverable organization profile discoverable.

`ADD VERSION [ [ IF NOT EXISTS ] version_alias_name ]`
:   Specifies the unique version identifier for the version being added. If `version_alias_name` isn’t specified, an alias isn’t created. If the identifier contains spaces, special characters, or mixed-case characters, the entire identifier must be enclosed in double quotes. Identifiers enclosed in double quotes are also case sensitive. The FIRST, LAST, DEFAULT, and LIVE keywords are reserved as version shortcuts and can’t be used. The unique version identifier can’t start with “version$” and can’t contain slashes ( / ). For information about identifier syntax, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ADD LIVE VERSION [ [ IF NOT EXISTS ] version_alias_name ]`
:   > Adds a new live editable version with the specified name from the last committed version. `version_alias_name` is optional and if it isn’t specified, an alias isn’t created. If the identifier contains spaces, special characters, or mixed-case characters, the entire identifier must be enclosed in double quotes. Identifiers enclosed in double quotes are also case sensitive. The FIRST, LAST, DEFAULT, and LIVE keywords are reserved as version shortcuts and can’t be used. The unique version identifier can’t start with “version$” and can’t contain slashes ( / ). For information about identifier syntax, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Changes made to the files in a live version are not applied to the organization profile until the live version is committed. The properties of an organization profile remain unchanged until the live version is committed.

`AS yaml_manifest_string`
:   The YAML manifest for the organization profile. For organizational listing profile manifest fields,
    see [Organization profile manifest reference](/user-guide/collaboration/organization-profiles/org-profile-manifest-reference).

    Inline manifests are normally provided as dollar-quoted strings.
    For more information, see [Dollar-quoted string constants](/sql-reference/data-types-text#label-dollar-quoted-string-constants).

`FROM 'yaml_manifest_stage_location'`
:   Specifies the external stage, internal stage, or Snowflake [Git repository clone](/developer-guide/git/git-overview) YAML format manifest stage location.

`COMMIT`
:   Commits the changes in the organization profile. The live version being committed must contain a valid organization profile manifest file.

`ABORT`
:   Discards the changes in the organization profile.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or MODIFY | Organization profile |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Organization profiles can be renamed only when they are in draft state.
- When setting the live version of the YAML format manifest for an organization profile, you must use COMMIT to apply the changes, or ABORT to discard the changes. An organization profile can only have one live version at a time.

## Examples

Alter the organization profile MYORGPROFILE to use an updated manifest file:

Copy code

```
ALTER ORGANIZATION PROFILE MYORGPROFILE ADD VERSION V2 FROM @STAGE_PATH_WITH_UPDATED_MANIFEST;
```

Publish the organization profile MYORGPROFILE:

Copy code

```
ALTER ORGANIZATION PROFILE MYORGPROFILE PUBLISH;
```
