# ALTER EXTERNAL AGENT

Modifies the properties of an existing external agent. External agents represent generative AI applications
in Snowflake for use with [AI Observability](/user-guide/snowflake-cortex/ai-observability).

See also:
:   [CREATE EXTERNAL AGENT](/sql-reference/sql/create-external-agent), [DROP EXTERNAL AGENT](/sql-reference/sql/drop-external-agent), [SHOW EXTERNAL AGENTS](/sql-reference/sql/show-external-agents), [DESCRIBE EXTERNAL AGENT](/sql-reference/sql/desc-external-agent)

## Syntax

Copy code

```
ALTER EXTERNAL AGENT [ IF EXISTS ] <name> SET
  [ COMMENT = '<comment>' ]

ALTER EXTERNAL AGENT [ IF EXISTS ] <name> ADD VERSION <version_name>
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the external agent to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`SET ...`
:   Sets one or more specified properties for the external agent:

    `COMMENT = comment`
    :   Specifies a description of the external agent.

`ADD VERSION version_name`
:   Adds a new version to the external agent. Versions represent different implementations of the application,
    such as different retrievers, prompts, LLMs, or inference configurations.

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

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Set a comment on an external agent:

Copy code

```
ALTER EXTERNAL AGENT my_rag_app SET COMMENT = 'RAG application for customer support';
```

Add a version to an external agent:

Copy code

```
ALTER EXTERNAL AGENT my_rag_app ADD VERSION "v2";
```
