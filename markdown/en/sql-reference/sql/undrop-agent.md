# UNDROP AGENT

Restores the most recent version of a dropped [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents).

See also:
:   [ALTER AGENT](/sql-reference/sql/alter-agent), [CREATE AGENT](/sql-reference/sql/create-agent), [DESCRIBE AGENT](/sql-reference/sql/desc-agent), [DROP AGENT](/sql-reference/sql/drop-agent), [SHOW AGENTS](/sql-reference/sql/show-agents)

## Syntax

Copy code

```
UNDROP AGENT <name>
```

## Parameters

`name`
:   Specifies the identifier for the Cortex Agent to restore.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or MODIFY | Agent that you restore | USAGE or MONITOR on the agent isn’t sufficient. |
| CREATE AGENT | Schema where you restore the agent | Required even if your role owns the agent. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can restore an agent only to the database and schema that contained it when it was dropped.
- If an agent with the same name already exists, `UNDROP AGENT` returns an error.
- If the agent was dropped more than once, `UNDROP AGENT` restores the most recently dropped version.
- You can’t restore a [temporary agent](/user-guide/snowflake-cortex/cortex-agents-temporary).
- The restored agent keeps its specification, comment, [versions](/user-guide/snowflake-cortex/cortex-agents-versioning),
  aliases, live version, `SECURE` setting, privilege grants, and tags.
- If the agent was added to the Snowflake CoWork object before it was dropped, `UNDROP AGENT` doesn’t add it back.
  To add the restored agent to the Snowflake CoWork object, run `ALTER SNOWFLAKE INTELLIGENCE ... ADD AGENT`.
  For more information, see [Snowflake CoWork object](/user-guide/snowflake-cortex/snowflake-cowork/deploy-agents#label-snowflake-intelligence-setup).

- UNDROP relies on the Snowflake [Time Travel](/user-guide/data-time-travel) feature. An object can be restored only if
  the object was deleted within the [Data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period). The default value is 24 hours.

## Examples

The following example restores the dropped agent named `my_agent` in the current schema:

Copy code

```
UNDROP AGENT my_agent;
```

The following example restores the dropped agent named `my_agent` in the `mydb` database and `myschema` schema:

Copy code

```
UNDROP AGENT mydb.myschema.my_agent;
```
