# SHOW AGENTS

Lists the [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents) for which you have access privileges.

See also:
:   [ALTER AGENT](/sql-reference/sql/alter-agent), [CREATE AGENT](/sql-reference/sql/create-agent), [DROP AGENT](/sql-reference/sql/drop-agent), [DESCRIBE AGENT](/sql-reference/sql/desc-agent), [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex)

## Syntax

Copy code

```
SHOW AGENTS
  [ LIKE '<pattern>' ]
  [ IN { ACCOUNT | DATABASE <db_name> | SCHEMA [<db_name>.]<schema_name> } ]
  [ STARTS WITH '<string>' ]
  [ LIMIT <rows> [ FROM '<string_from>' ] ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns records for the entire account.

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or for a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

        Note

        Using SHOW commands without an `IN` clause in a database context can result in fewer than expected results.

        Objects with the same name are only displayed once if no `IN` clause is used. For example, if you have table `t1` in
        `schema1` and table `t1` in `schema2`, and they are both in scope of the database context you’ve specified (that is, the database
        you’ve selected is the parent of `schema1` and `schema2`), then SHOW TABLES only displays one of the `t1` tables.

    `SCHEMA`, `SCHEMA schema_name`
    :   Returns records for the current schema in use or a specified schema (`schema_name`).

        `SCHEMA` is optional if a database is in use or if you specify the fully qualified `schema_name` (for example, `db.schema`).

        If no database is in use, specifying `SCHEMA` has no effect on the output.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

## Output

The command output provides Cortex Agent properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Timestamp when the agent was created. |
| `name` | Name of the agent. |
| `database_name` | Database containing the agent. |
| `schema_name` | Schema containing the agent. |
| `owner` | Owner role of the agent. |
| `comment` | Comment text for the agent. |
| `profile` | Agent profile JSON (display\_name, avatar, color). |
| `is_secure` | Whether the agent is secure (`true` or `false`). For more information, see [Secure agents](/user-guide/snowflake-cortex/cortex-agents-secure). |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any one of these privileges: OWNERSHIP, USAGE, MODIFY, or MONITOR | Agent |  |

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

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

- Temporary agents created in the current session appear in the SHOW AGENTS output for that session. They are not visible to other sessions or users. See [Working with temporary agents](/user-guide/snowflake-cortex/cortex-agents-temporary).

## Examples

List all agents in the current schema:

Copy code

```
SHOW AGENTS;
```

Sample output:

```
+-------------------------------+------------+---------------+-------------+-----------+---------+--------------------------+-----------+
| created_on                    | name       | database_name | schema_name | owner     | comment | profile                  | is_secure |
|-------------------------------+------------+---------------+-------------+-----------+---------+--------------------------+-----------|
| 2025-09-15 17:04:37.263 +0000 | TEST_AGENT | EXAMPLE_DB    | AGENTS      | TEST_ROLE | null    | {"display_name":"test"}  | false     |
+-------------------------------+------------+---------------+-------------+-----------+---------+--------------------------+-----------+
```

The following example lists agents in a specific schema:

Copy code

```
SHOW AGENTS IN SCHEMA mydb.myschema;
```

The following example lists agents in a specific database:

Copy code

```
SHOW AGENTS IN DATABASE mydb;
```

The following example lists all agents in the account:

Copy code

```
SHOW AGENTS IN ACCOUNT;
```

The following example lists agents with names that start with `my_agent`:

Copy code

```
SHOW AGENTS LIKE 'my_agent%';
```

The following example lists the first 10 agents. The second statement lists the first 10 agents, started from the agent named `AGENT_NAME`.

Copy code

```
SHOW AGENTS LIMIT 10;
SHOW AGENTS LIMIT 10 FROM 'AGENT_NAME';
```

The following example lists agents as resources in JSON format:

Copy code

```
SHOW AS RESOURCE AGENTS;
```
