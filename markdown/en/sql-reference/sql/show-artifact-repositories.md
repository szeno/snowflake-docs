# SHOW ARTIFACT REPOSITORIES

Lists the
[artifact repositories](/sql-reference/sql/create-artifact-repository)
for which you have access privileges.

See also:
:   [CREATE ARTIFACT REPOSITORY](/sql-reference/sql/create-artifact-repository) ,
    [ALTER ARTIFACT REPOSITORY](/sql-reference/sql/alter-artifact-repository) ,
    [DESCRIBE ARTIFACT REPOSITORY](/sql-reference/sql/desc-artifact-repository) ,
    [DROP ARTIFACT REPOSITORY](/sql-reference/sql/drop-artifact-repository)

## Syntax

Copy code

```
SHOW ARTIFACT REPOSITORIES
  [ LIKE '<pattern>' ]
  [ IN { ACCOUNT | DATABASE [ <database_name> ] | SCHEMA [ <schema_name> ] } ]
  [ LIMIT <rows> ]
```

## Parameters

`LIKE 'pattern'`
:   Filters the output by name. The match uses SQL `LIKE` pattern matching
    (case-insensitive).

`IN { ACCOUNT | DATABASE [ database_name ] | SCHEMA [ schema_name ] }`
:   Scopes the listing to an account, database, or schema. When `DATABASE` or
    `SCHEMA` is used without a name, the command uses the current database or
    schema.

`LIMIT rows`
:   Limits the maximum number of rows returned.

## Access control requirements

You can see a repository in the output if you have at least one privilege on
it, or ownership of it.

## Output

The command returns one row per repository with the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time the repository was created. |
| `name` | Name of the repository. |
| `database_name` | Database that contains the repository. |
| `schema_name` | Schema that contains the repository. |
| `type` | Repository type: `APPLICATION` or `PYPI`. |
| `api_integration` | API integration used by `PYPI` repositories. Empty for `APPLICATION`. |
| `owner` | Role that owns the repository. |
| `owner_role_type` | Type of role that owns the repository. |
| `comment` | Repository comment, if any. |

Expand

Show lessSee more

## Examples

List all artifact repositories in the current schema:

Copy code

```
SHOW ARTIFACT REPOSITORIES;
```

List all repositories whose name starts with `app_` in a specific database:

Copy code

```
SHOW ARTIFACT REPOSITORIES LIKE 'app_%' IN DATABASE my_db;
```
