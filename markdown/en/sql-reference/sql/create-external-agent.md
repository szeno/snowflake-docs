# CREATE EXTERNAL AGENT

Creates a new external agent object in the current or specified schema. External agents represent generative AI applications
in Snowflake for use with [AI Observability](/user-guide/snowflake-cortex/ai-observability). The external agent object stores
application and evaluation metadata (such as the application name, version name, or run name) and governs access to traces and
evaluation results.

Note

External agent objects are typically created automatically by the TruLens SDK when you register an application or run an
evaluation. You generally do not need to create them manually using SQL. For more information, see
[AI Observability with Snowflake Cortex](/user-guide/snowflake-cortex/ai-observability).

See also:
:   [ALTER EXTERNAL AGENT](/sql-reference/sql/alter-external-agent), [DROP EXTERNAL AGENT](/sql-reference/sql/drop-external-agent), [SHOW EXTERNAL AGENTS](/sql-reference/sql/show-external-agents), [DESCRIBE EXTERNAL AGENT](/sql-reference/sql/desc-external-agent)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] EXTERNAL AGENT [ IF NOT EXISTS ] <name>
  [ WITH VERSION <version_name> ]
  [ COMMENT = '<comment>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the external agent; must be unique for the schema in which the external agent is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`WITH VERSION version_name`
:   Specifies the name of the initial version to create for the external agent. Versions represent different implementations of the application,
    such as different retrievers, prompts, LLMs, or inference configurations.

`COMMENT = comment`
:   String that specifies a description for the external agent.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE EXTERNAL AGENT | Schema | Required to create the external agent in a schema. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- External agent objects share a namespace with [model](/sql-reference/sql/create-model) objects. You cannot create an external agent
  with the same name as an existing model in the same schema, and vice versa. If a name collision occurs, you must rename or drop
  the conflicting object.
- The TruLens SDK automatically creates external agent objects when you call `TruApp()` (or the framework-specific wrappers
  `TruChain`, `TruGraph`, `TruLlama`) to register an application for AI Observability. Running an evaluation can also create
  an external agent if one does not already exist for the specified application name.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Create an external agent:

Copy code

```
CREATE EXTERNAL AGENT my_rag_app;
```

Create an external agent with an initial version:

Copy code

```
CREATE EXTERNAL AGENT my_rag_app WITH VERSION "v1";
```

Create an external agent only if it does not already exist:

Copy code

```
CREATE EXTERNAL AGENT IF NOT EXISTS my_rag_app WITH VERSION "v1";
```

Replace an existing external agent:

Copy code

```
CREATE OR REPLACE EXTERNAL AGENT my_rag_app WITH VERSION "v2";
```
