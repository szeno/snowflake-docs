# DROP EXTERNAL AGENT

Removes the specified external agent from the current or specified schema.

Note

Dropping an external agent removes the application and evaluation metadata associated with the external agent.
The traces and evaluation results that were stored in the event table are not deleted and remain stored.
For more information, see [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

See also:
:   [CREATE EXTERNAL AGENT](/sql-reference/sql/create-external-agent), [ALTER EXTERNAL AGENT](/sql-reference/sql/alter-external-agent), [SHOW EXTERNAL AGENTS](/sql-reference/sql/show-external-agents), [DESCRIBE EXTERNAL AGENT](/sql-reference/sql/desc-external-agent)

## Syntax

Copy code

```
DROP EXTERNAL AGENT [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the external agent to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

    If the external agent identifier is not fully-qualified (in the form of `db_name.schema_name.external_agent_name` or
    `schema_name.external_agent_name`), the command looks for the external agent in the current schema for the session.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | External Agent | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the GRANT OWNERSHIP command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

- All versions associated with the external agent are dropped along with the external agent.
- Dropping an external agent removes the metadata (such as the application name, version name, and run name) associated with the
  external agent. The traces and evaluation records generated as part of the runs are not deleted and remain stored in the
  SNOWFLAKE.LOCAL.AI\_OBSERVABILITY\_EVENTS event table.
- External agent objects share a namespace with [model](/sql-reference/sql/create-model) objects. Make sure you are dropping
  the correct object.

## Examples

Drop an external agent in the current schema:

Copy code

```
DROP EXTERNAL AGENT my_rag_app;
```

Drop an external agent in a specific database and schema:

Copy code

```
DROP EXTERNAL AGENT mydb.myschema.my_rag_app;
```

Drop an external agent only if it exists:

Copy code

```
DROP EXTERNAL AGENT IF EXISTS my_rag_app;
```
