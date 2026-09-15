# SHOW GRANTS IN DCM PROJECT

`SHOW GRANTS IN DCM PROJECT` lists all grants deployed and managed by the specified [DCM project](/user-guide/dcm-projects/dcm-projects-overview).

`SHOW FUTURE GRANTS IN DCM PROJECT` lists all grants that will be deployed and managed by the specified [DCM project](/user-guide/dcm-projects/dcm-projects-overview) when the next deployment is executed.

The command returns grant metadata and properties, ordered by creation date.

See also:
:   [CREATE DCM PROJECT](/sql-reference/sql/create-dcm-project) , [ALTER DCM PROJECT](/sql-reference/sql/alter-dcm-project), [DESCRIBE DCM PROJECT](/sql-reference/sql/desc-dcm-project) , [DROP DCM PROJECT](/sql-reference/sql/drop-dcm-project), [EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project), [SHOW DCM PROJECTS](/sql-reference/sql/show-dcm-projects)

## Syntax

Copy code

```
SHOW GRANTS IN DCM PROJECT <name> [ LIMIT <rows> ]

SHOW FUTURE GRANTS IN DCM PROJECT <name> [ LIMIT <rows> ]
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

SHOW GRANTS IN DCM PROJECT returns the following output, including one row per grant:

- `CREATED_ON`
- `PRIVILEGE`
- `GRANTED_ON` - object type, such as DATABASE, TABLE, ROLE
- `NAME` - object name
- `GRANTED_TO` - such as ROLE, DATABASE ROLE, SHARE
- `GRANTEE_NAME`
- `GRANT_OPTION`
- `GRANTED_BY`
- `GRANTED_BY_ROLE_TYPE`
