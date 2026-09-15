# SHOW DEPLOYMENTS IN DCM PROJECT

Shows all deployments for the specified [DCM project](/user-guide/dcm-projects/dcm-projects-overview).

The command returns deployment metadata and properties, ordered by creation date.

See also:
:   [CREATE DCM PROJECT](/sql-reference/sql/create-dcm-project) , [ALTER DCM PROJECT](/sql-reference/sql/alter-dcm-project), [DESCRIBE DCM PROJECT](/sql-reference/sql/desc-dcm-project) , [DROP DCM PROJECT](/sql-reference/sql/drop-dcm-project), [EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project), [SHOW DCM PROJECTS](/sql-reference/sql/show-dcm-projects)

## Syntax

Copy code

```
SHOW DEPLOYMENTS IN DCM PROJECT <name> [ LIMIT <rows> ]
```

## Required parameters

`IN DCM PROJECT name`
:   Specifies the identifier of the DCM project that contains the deployments to list.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

## Output

The command output provides deployment properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the deployment was created. |
| `name` | Name of the deployment. |
| `alias` | User-specified deployment alias. |
| `deployment_file_path` | Full location URL for the deployment. Example: `snow://project/MY_DB.PUBLIC.P/deployment/deployment$2/` |
| `source_file_path` | Source location where this deployment is created from. This is the value provided with FROM `<source_location>`. |
| `git_commit_hash` | The Git commit hash that indicates the deployment of files in the Git repository from which the DCM project originates. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| MONITOR | DCM project |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Show all deployments of the DCM project named `my_project`:

Copy code

```
SHOW DEPLOYMENTS IN DCM PROJECT my_project;
```
