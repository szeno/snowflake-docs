# SHOW ENTITIES IN DCM PROJECT

Shows all Snowflake objects that are currently managed by a specified [DCM project](/user-guide/dcm-projects/dcm-projects-overview).

It provides a mixed list of fully qualified names for all objects. To see any results, users need both READ privilege on the DCM project
and READ privilege on the managed object itself.

Note

The result does not necessarily match the entities of the most recent deployment. Objects that were manually dropped or detached from the
project, will not be listed here.

The command returns object metadata and properties, ordered by creation date.

See also:
:   [CREATE DCM PROJECT](/sql-reference/sql/create-dcm-project) , [ALTER DCM PROJECT](/sql-reference/sql/alter-dcm-project), [DESCRIBE DCM PROJECT](/sql-reference/sql/desc-dcm-project) , [DROP DCM PROJECT](/sql-reference/sql/drop-dcm-project), [EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project), [SHOW DCM PROJECTS](/sql-reference/sql/show-dcm-projects)

## Syntax

Copy code

```
SHOW ENTITIES IN DCM PROJECT <name> [ LIMIT <rows> ]

SHOW ENTITIES LIKE <pattern> IN DCM PROJECT <name>;

SHOW ENTITIES IN DCM PROJECT <name> STARTS WITH <prefix>;

SHOW ENTITIES IN DCM PROJECT <name> LIMIT <n> FROM <cursor>;
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

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows [ FROM 'name_string' ]`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
    specified number of rows following the first row whose object name matches the specified string:

    - The string must be enclosed in single quotes and is case sensitive.
    - The string does not have to include the full object name; partial names are supported.

    Default: No value (no limit is applied to the output)

    Note

    For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
    both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
    returned.

    In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
    lexicographic value than the rows returned by `STARTS WITH 'name_string'`.

    For example:

    - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
    - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
    - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Output

| Column | Description |
| --- | --- |
| `CREATED_ON` | creation timestamp (LTZ) |
| `NAME` | fully-qualified name of the object (FQN), suitable for DESC |
| `OBJECT_TYPE` | object type |
| `OWNER` | owning role, per-domain conventions |
| `COMMENT` | user-specified comment |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| READ | - DCM project - Managed object |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Show all entities in the `my_project` DCM project:

Copy code

```
SHOW ENTITIES IN DCM PROJECT my_project;
```

Show all entities in the `my_project` DCM project that start with `my_`:

Copy code

```
SHOW ENTITIES LIKE 'my_%' IN DCM PROJECT my_project;
```

Show all dynamic tables in the `my_project` DCM project:

Copy code

```
SHOW ENTITIES IN DCM PROJECT my_project
  ->> SELECT * FROM $1 WHERE "object_type" = 'DYNAMIC_TABLE';
```
