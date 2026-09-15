# DROP ORGANIZATION PROFILE

Removes an organization profile.

See also:
:   [ALTER ORGANIZATION PROFILE](/sql-reference/sql/alter-organization-profile), [CREATE ORGANIZATION PROFILE](/sql-reference/sql/create-organization-profile), [DESCRIBE AVAILABLE ORGANIZATION PROFILE](/sql-reference/sql/desc-available-organization-profile), [DESCRIBE ORGANIZATION PROFILE](/sql-reference/sql/desc-organization-profile), [SHOW AVAILABLE ORGANIZATION PROFILES](/sql-reference/sql/show-available-organization-profiles), [SHOW ORGANIZATION PROFILES](/sql-reference/sql/show-organization-profiles), [SHOW VERSIONS IN ORGANIZATION PROFILE](/sql-reference/sql/show-versions-in-organization-profile)

## Syntax

Copy code

```
DROP ORGANIZATION PROFILE <name>
```

## Parameters

`name`
:   Specifies the identifier for the organization profile to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case sensitive. For information about identifier syntax, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Organization profile | Executing this command with any other role returns an error. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Dropped organization profiles cannot be recovered; they must be recreated. An organization profile cannot be dropped if it is associated with an organizational listing.

## Examples

The following example drops the organization profile named `MYORGANIZATIONPROFILE`:

Copy code

```
DROP ORGANIZATION PROFILE myorganizationprofile;
```

```
+---------------------------------------------+
| status                                      |
|---------------------------------------------|
| MYORGANIZATIONPROFILE successfully dropped. |
+---------------------------------------------+
```
