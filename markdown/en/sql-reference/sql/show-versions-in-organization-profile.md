# SHOW VERSIONS IN ORGANIZATION PROFILE

Lists the organization profile versions for which you have access privileges.

See also:
:   [ALTER ORGANIZATION PROFILE](/sql-reference/sql/alter-organization-profile), [CREATE ORGANIZATION PROFILE](/sql-reference/sql/create-organization-profile), [DESCRIBE AVAILABLE ORGANIZATION PROFILE](/sql-reference/sql/desc-available-organization-profile), [DESCRIBE ORGANIZATION PROFILE](/sql-reference/sql/desc-organization-profile), [DROP ORGANIZATION PROFILE](/sql-reference/sql/drop-organization-profile), [SHOW AVAILABLE ORGANIZATION PROFILES](/sql-reference/sql/show-available-organization-profiles)

## Syntax

Copy code

```
SHOW VERSIONS IN ORGANIZATION PROFILE <name>
```

## Parameters

`name`
:   Specifies the identifier for the organization profile on which you want to list organization profile versions. Must contain only uppercase characters or numbers.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case sensitive. See [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `created_on` | The date and time when the organization profile was created. |
| `name` | The organization profile name. |
| `alias` | The user-defined alias for the organization profile version. |
| `location_uri` | The URI for the organization profile version. |
| `is_live` | The organization profile version is live. One of `TRUE` or `FALSE`. |
| `is_default` | The organization profile version is the default. One of `TRUE` or `FALSE`. Must be `FALSE` when `is_live` is `TRUE`. |
| `is_first` | The organization profile is the first version. One of `TRUE` or `FALSE`. |
| `is_last` | The organization profile is the last version. One of `TRUE` or `FALSE`. |
| `comment` | Comments added by users. |
| `source_location_uri` | The source location URI for the organization profile version. |
| `git_commit_hash` | The git commit hash for the organization profile version when it’s created from a git source. `NONE` when a git commit hash is unavailable. |

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

The following example lists the organization profile versions in the organization profile `MYORGANIZATIONPROFILE` that you have the privileges to access:

Copy code

```
SHOW VERSIONS IN ORGANIZATION PROFILE myorganizationprofile;
```

```
+------------------------+---------------------+---------------------+-----------------------------------------------+---------------------+---------------------+-------------+-----------------+---------------------+---------------------+----------------+
|created_on              |name                 |alias                |location_uri                                   |is_live              |is_default           |is_first     |is_last          |comment              |source_location_uri  |git_commit_hash |
+------------------------+---------------------+---------------------+-----------------------------------------------+---------------------+---------------------+-------------+-----------------+---------------------+---------------------+----------------+
|2025-01-01 01:01:01.000 |VERSION$1            |V1                   |snow://notebook/mynotebook/versions/version$1  |TRUE                 |FALSE                |TRUE         |FALSE            |                     |@TESTDB.PUBLIC.STAGE |NONE            |
+------------------------+---------------------+---------------------+-----------------------------------------------+---------------------+---------------------+-------------+-----------------+---------------------+---------------------+----------------+
```
