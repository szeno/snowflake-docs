# SHOW AVAILABLE ORGANIZATION PROFILES

Lists the organization profiles available in the user’s organization.

See also:
:   [ALTER ORGANIZATION PROFILE](/sql-reference/sql/alter-organization-profile), [CREATE ORGANIZATION PROFILE](/sql-reference/sql/create-organization-profile), [DESCRIBE AVAILABLE ORGANIZATION PROFILE](/sql-reference/sql/desc-available-organization-profile), [DESCRIBE ORGANIZATION PROFILE](/sql-reference/sql/desc-organization-profile), [DROP ORGANIZATION PROFILE](/sql-reference/sql/drop-organization-profile), [SHOW ORGANIZATION PROFILES](/sql-reference/sql/show-organization-profiles), [SHOW VERSIONS IN ORGANIZATION PROFILE](/sql-reference/sql/show-versions-in-organization-profile)

## Syntax

Copy code

```
SHOW AVAILABLE ORGANIZATION PROFILES
```

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `created_on` | The date and time when the organization profile was created. |
| `name` | The name of the organization profile. |
| `system_generated` | Indicates the organization profile is system generated. |
| `state` | The organization profile state. One of ACTIVE or DRAFT. |
| `organization_name` | The name of the organization associated with the organization profile. |
| `title` | The title of the organization profile. |
| `description` | The description of the organization profile. |
| `owner_contact` | The contact email of the owner of the organization profile. |
| `approver_contact` | The contact email of the access approver of the organization profile. |
| `can_publish_listings_with_profile` | Whether the current user can publish organizational listings using this organization profile. One of `TRUE` or `FALSE`. |

Expand

Show lessSee more

## Examples

The following example lists the organization profiles that you have the privileges to access:

Copy code

```
SHOW AVAILABLE ORGANIZATION PROFILES;
```

```
+-------------------------+-------------+---------------------+---------------------+---------------------+------------------------+---------------------------------+---------------------+---------------------+-----------------------------------+
|created_on               |name         |system_generated     |state                |organization_name    |title                   |description                      |owner_contact        |approver_contact     |can_publish_listings_with_profile  |
+-------------------------+-------------+---------------------+---------------------+---------------------+------------------------+---------------------------------+---------------------+---------------------+-----------------------------------+
|2025-01-01 01:01:01.000  |ORGPROFILE   |FALSE                |ACTIVE               |TESTORG              |My Organization Profile |Organization profile description |test@test.com        |test@test.com        |TRUE                               |
+-------------------------+-------------+---------------------+---------------------+---------------------+------------------------+---------------------------------+---------------------+---------------------+-----------------------------------+
```
