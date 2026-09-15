# CREATE EXPERIMENT

Creates a new [experiment](/developer-guide/snowflake-ml/experiments) or replaces an existing experiment.

See also:
:   [ALTER EXPERIMENT](/sql-reference/sql/alter-experiment) , [SHOW EXPERIMENTS](/sql-reference/sql/show-experiments) , [DROP EXPERIMENT](/sql-reference/sql/drop-experiment) , [SHOW RUNS IN EXPERIMENT](/sql-reference/sql/show-runs-in-experiment) , [SHOW RUN … IN EXPERIMENT](/sql-reference/sql/show-run-in-experiment)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] EXPERIMENT [ IF NOT EXISTS ] <name>
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the experiment; must be unique for the schema in which the experiment is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE EXPERIMENT | Schema |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.
