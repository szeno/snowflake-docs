# DESCRIBE DCM PROJECT

Describes the properties of a [DCM project](/user-guide/dcm-projects/dcm-projects-overview).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE DCM PROJECT](/sql-reference/sql/create-dcm-project) , [ALTER DCM PROJECT](/sql-reference/sql/alter-dcm-project) , [DROP DCM PROJECT](/sql-reference/sql/drop-dcm-project) , [EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project), [SHOW DCM PROJECTS](/sql-reference/sql/show-dcm-projects), [SHOW DEPLOYMENTS IN DCM PROJECT](/sql-reference/sql/show-deployments-in-dcm-project)

## Syntax

Copy code

```
{ DESCRIBE | DESC } DCM PROJECT <name>
```

## Parameters

`name`
:   Specifies the identifier for the DCM project to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

**DCM project properties**

| Column | Description |
| --- | --- |
| `name` | Name of the DCM project.  Example: `my_project` |
| `created_on` | Timestamp when the DCM project was created.  Example: `2022-01-01 00:00:00` |
| `owner` | User who owns the DCM project. |
| `comment` | User-defined comment associated with the DCM project. |
| `last_executed_version_name` | Name of the last executed DCM project version.  Example: `VERSION$2` |
| `last_executed_version_alias` | Version alias of the last executed DCM project version. |
| `last_executed_version_path` | URI of the last executed version.  Example: `snow://project/MY_DB.PUBLIC.P/versions/version$2/` |
| `last_executed_source_path` | Path to the last executed version sources.  Example: `@project_stg/v1/` |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| READ | DCM project |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

Describe the DCM project named `my_project`:

Copy code

```
DESCRIBE DCM PROJECT my_project;
```
