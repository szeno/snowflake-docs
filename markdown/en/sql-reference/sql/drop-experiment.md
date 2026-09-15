# DROP EXPERIMENT

Removes the specified [experiment](/developer-guide/snowflake-ml/experiments) from the current/specified schema.

See also:
:   [CREATE EXPERIMENT](/sql-reference/sql/create-experiment) , [ALTER EXPERIMENT](/sql-reference/sql/alter-experiment) , [SHOW EXPERIMENTS](/sql-reference/sql/show-experiments) , [SHOW RUNS IN EXPERIMENT](/sql-reference/sql/show-runs-in-experiment) , [SHOW RUN … IN EXPERIMENT](/sql-reference/sql/show-run-in-experiment)

## Syntax

Copy code

```
DROP EXPERIMENT <name>;
```

## Parameters

`name`
:   Specifies the identifier for the experiment to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Experiment |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).
