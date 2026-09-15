# DROP AGENT

Removes the specified [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents) with the specified name from the current or specified database and schema.

See also:
:   [ALTER AGENT](/sql-reference/sql/alter-agent), [CREATE AGENT](/sql-reference/sql/create-agent), [DESCRIBE AGENT](/sql-reference/sql/desc-agent), [SHOW AGENTS](/sql-reference/sql/show-agents), [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex)

## Syntax

Copy code

```
DROP AGENT [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the Cortex Agent to be dropped.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any one of these privileges: OWNERSHIP or MODIFY | Agent |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

The following example drops the agent named `my_agent` in the current schema:

Copy code

```
DROP AGENT my_agent;
```

The following example drops the agent named `my_agent` in the `mydb` database and `myschema` schema. This command fails if the agent does not exist:

Copy code

```
DROP AGENT mydb.myschema.my_agent;
```

The following example drops the agent named `my_agent` in the `mydb` database and `myschema` schema only if it exists:

Copy code

```
DROP AGENT IF EXISTS mydb.myschema.my_agent;
```
