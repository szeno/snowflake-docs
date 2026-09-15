# DESCRIBE EXTERNAL AGENT

Describes the properties of an external agent. External agents represent generative AI applications
in Snowflake for use with [AI Observability](/user-guide/snowflake-cortex/ai-observability).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE EXTERNAL AGENT](/sql-reference/sql/create-external-agent), [ALTER EXTERNAL AGENT](/sql-reference/sql/alter-external-agent), [DROP EXTERNAL AGENT](/sql-reference/sql/drop-external-agent), [SHOW EXTERNAL AGENTS](/sql-reference/sql/show-external-agents)

## Syntax

Copy code

```
{ DESC | DESCRIBE } EXTERNAL AGENT <name>
```

## Parameters

`name`
:   Specifies the identifier for the external agent to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

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

Describe an external agent:

Copy code

```
DESCRIBE EXTERNAL AGENT my_rag_app;
```

Describe an external agent in a specific database and schema:

Copy code

```
DESCRIBE EXTERNAL AGENT mydb.myschema.my_rag_app;
```
