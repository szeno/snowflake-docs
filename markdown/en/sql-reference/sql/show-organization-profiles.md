# SHOW ORGANIZATION PROFILES

Lists the organization profiles for which you have access privileges.

See also:
:   [ALTER ORGANIZATION PROFILE](/sql-reference/sql/alter-organization-profile), [CREATE ORGANIZATION PROFILE](/sql-reference/sql/create-organization-profile), [DESCRIBE AVAILABLE ORGANIZATION PROFILE](/sql-reference/sql/desc-available-organization-profile), [DESCRIBE ORGANIZATION PROFILE](/sql-reference/sql/desc-organization-profile), [DROP ORGANIZATION PROFILE](/sql-reference/sql/drop-organization-profile), [SHOW AVAILABLE ORGANIZATION PROFILES](/sql-reference/sql/show-available-organization-profiles), [SHOW VERSIONS IN ORGANIZATION PROFILE](/sql-reference/sql/show-versions-in-organization-profile)

## Syntax

Copy code

```
SHOW ORGANIZATION PROFILES
```

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `created_on` | The date and time when the organization profile was created. |
| `name` | The organization profile name. |
| `system_generated` | Indicates the organization profile is system generated and can’t be dropped. One of `TRUE` or `FALSE`. |
| `state` | The organization profile state. One of ACTIVE or DRAFT. |
| `organization_name` | The name of the organization associated with the organization profile. |
| `title` | The title of the organization profile. |
| `description` | The description of the organization profile. |
| `owner_contact` | The contact email of the owner of the organization profile. |
| `approver_contact` | The contact email of the access approver of the organization profile. |
| `owner` | The owner role of the organization profile. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or MODIFY or a privileged role, such as ACCOUNTADMIN or SECURITYADMIN | Organization profile |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

The following example lists the organization profiles that you have privileges to access:

Copy code

```
SHOW ORGANIZATION PROFILES;
```

```
+-------------------------+-----------------+---------------------+---------------------+---------------------+---------------------------+----------------------------------+---------------------+---------------------+---------------------+
|created_on               |name             |system_generated     |state                |organization_name    |title                      |description                       |owner_contact        |approver_contact     |owner                |
+-------------------------+-----------------+---------------------+---------------------+---------------------+---------------------------+----------------------------------+---------------------+---------------------+---------------------+
| 2025-01-01 01:01:01.000 |ORGPROFILE       |FALSE                |ACTIVE               |TESTORG              |My Organization Profile    |Organization profile description  |test@test.com        |test@test.com        |ACCOUNTADMIN         |
+-------------------------+-----------------+---------------------+---------------------+---------------------+---------------------------+----------------------------------+---------------------+---------------------+---------------------+
```
