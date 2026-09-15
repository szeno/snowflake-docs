# SHOW EXTERNAL AGENTS

Lists the external agents for which you have access privileges. External agents represent generative AI applications
in Snowflake for use with [AI Observability](/user-guide/snowflake-cortex/ai-observability).

The output returns object metadata and properties, ordered lexicographically by database, schema, and external agent name
(see [Output](#output) in this topic for descriptions of the output columns).

See also:
:   [CREATE EXTERNAL AGENT](/sql-reference/sql/create-external-agent), [ALTER EXTERNAL AGENT](/sql-reference/sql/alter-external-agent), [DROP EXTERNAL AGENT](/sql-reference/sql/drop-external-agent), [DESCRIBE EXTERNAL AGENT](/sql-reference/sql/desc-external-agent)

## Syntax

Copy code

```
SHOW EXTERNAL AGENTS [ LIKE '<pattern>' ]
                     [ IN { ACCOUNT | DATABASE [ <db_name> ] | SCHEMA [ <schema_name> ] } ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN ACCOUNT | DATABASE [ db_name ] | SCHEMA [ schema_name ]`
:   Optionally specifies the scope of the command, which determines whether the command lists external agents only in the
    current/specified database or schema.

    If you specify the keyword `ACCOUNT`, then the command retrieves records for all schemas in all databases
    of the current account.

    If you specify the keyword `DATABASE`, then:

    - If you specify a `db_name`, then the command retrieves records for all schemas of the specified database.
    - If you don’t specify a `db_name`, then:
      - If there is a current database, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and schemas in the account.

    If you specify the keyword `SCHEMA`, then:

    - If you specify a qualified schema name (for example, `my_database.my_schema`), then the command
      retrieves records for the specified database and schema.
    - If you specify an unqualified `schema_name`, then:

      - If there is a current database, then the command retrieves records for the specified schema in the current database.
      - If there is no current database, then the command displays the error
        `SQL compilation error: Object does not exist, or operation cannot be performed`.
    - If you don’t specify a `schema_name`, then:

      - If there is a current database, then:

        - If there is a current schema, then the command retrieves records for the current schema in the current database.
        - If there is no current schema, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and all schemas in the account.

    Default: Depends on whether the session currently has a database in use:

    - Database: `DATABASE` is the default (i.e. the command returns the external agents you have privileges to view in the
      current database).
    - No database: Account scope is the default (i.e. the command returns the external agents you have privileges to view in your
      account).

## Output

The command output provides external agent properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Timestamp when the external agent was created. |
| `name` | Name of the external agent. |
| `database_name` | Database containing the external agent. |
| `schema_name` | Schema containing the external agent. |
| `owner` | Role that owns the external agent. |
| `comment` | Comment for the external agent. |
| `versions` | JSON array listing versions of the external agent. |
| `default_version_name` | Default version of the external agent. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any one of these privileges: OWNERSHIP, USAGE | External Agent |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

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

List all external agents in the current schema:

Copy code

```
SHOW EXTERNAL AGENTS;
```

List external agents in a specific schema:

Copy code

```
SHOW EXTERNAL AGENTS IN SCHEMA mydb.myschema;
```

List external agents in a specific database:

Copy code

```
SHOW EXTERNAL AGENTS IN DATABASE mydb;
```

List all external agents in the account:

Copy code

```
SHOW EXTERNAL AGENTS IN ACCOUNT;
```

List external agents with names that match a pattern:

Copy code

```
SHOW EXTERNAL AGENTS LIKE 'my_rag%';
```
