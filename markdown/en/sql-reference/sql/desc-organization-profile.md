# DESCRIBE ORGANIZATION PROFILE

Describes the properties of an organization profile.

DESCRIBE can be abbreviated to DESC.

See also:
:   [ALTER ORGANIZATION PROFILE](/sql-reference/sql/alter-organization-profile), [CREATE ORGANIZATION PROFILE](/sql-reference/sql/create-organization-profile), [DESCRIBE AVAILABLE ORGANIZATION PROFILE](/sql-reference/sql/desc-available-organization-profile), [DROP ORGANIZATION PROFILE](/sql-reference/sql/drop-organization-profile), [SHOW AVAILABLE ORGANIZATION PROFILES](/sql-reference/sql/show-available-organization-profiles), [SHOW ORGANIZATION PROFILES](/sql-reference/sql/show-organization-profiles), [SHOW VERSIONS IN ORGANIZATION PROFILE](/sql-reference/sql/show-versions-in-organization-profile)

## Syntax

Copy code

```
{ DESC | DESCRIBE } ORGANIZATION PROFILE <name>
```

## Parameters

`name`
:   Specifies the identifier for the organization profile to describe. Must contain only uppercase characters or numbers.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case sensitive. See [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `created_on` | The date and time when the organization profile was created. |
| `name` | The organization profile name. |
| `title` | The title of the organization profile. |
| `system_generated` | Indicates the organization profile is system generated and can’t be dropped. One of `TRUE` or `FALSE`. |
| `state` | The organization profile state. One of ACTIVE or DRAFT. |
| `description` | The description of the organization profile. |
| `owner_contact` | The contact email of the owner of the organization profile. |
| `approver_contact` | The contact email of the access approver of the organization profile. |
| `logo` | The organization profile logo URL. |
| `allowed_publishers` | The accounts that are allowed to publish the organizational listing. |
| `manifest_yaml` | The contents of the default organization profile manifest. |
| `live_version_uri` | The URI for the live organization profile version. `NONE` when the URI is unavailable. |
| `published_version_uri` | The URI for the published organization profile version. `NONE` when the URI is unavailable. |
| `published_version_name` | The name of the published organization profile version. |
| `published_version_alias` | The alias for the published organization profile version. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY | Organization profile |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

The following example describes the organization profile named `MYORGANIZATIONPROFILE`:

Copy code

```
DESCRIBE ORGANIZATION PROFILE myorganizationprofile;
```

```
+-------------------------+-------------+--------------------------+---------------------+---------------------+----------------------------------+---------------------+---------------------+----------------+--------------------------------+----------------------------------------------------------------------------------------+----------------------------------------------------------+----------------------------------------------------------+-------------------------+-------------------------+
|created_on               |name         |title                     |system_generated     |state                |description                       |owner_contact        |approver_contact     |logo            |allowed_publishers              |manifest_yaml                                                                           |live_version_uri                                          |published_version_uri                                     |published_version_name   |published_version_alias  |
+-------------------------+-------------+--------------------------+---------------------+---------------------+----------------------------------+---------------------+---------------------+----------------+--------------------------------+----------------------------------------------------------------------------------------+----------------------------------------------------------+----------------------------------------------------------+-------------------------+-------------------------+
|2025-01-01 01:01:01.000  |ORGPROFILE   |My Organization Profile   |FALSE                |ACTIVE               |Organization profile description  |test@test.com        |test@test.com        |urn:icon:shield |{“all_internal_accounts”: true} | title: "My Organization Profile" description: "Organization profile description". . .  |snow://organization_profile/ORGPROFILE/versions/version$1 |snow://organization_profile/ORGPROFILE/versions/version$1 |VERSION$1                |V1                       |
+-------------------------+-------------+--------------------------+---------------------+---------------------+----------------------------------+---------------------+---------------------+----------------+--------------------------------+----------------------------------------------------------------------------------------+----------------------------------------------------------+----------------------------------------------------------+-------------------------+-------------------------+
```
