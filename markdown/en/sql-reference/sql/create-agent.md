# CREATE AGENT

Creates a new [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents) object with the specified attributes and specification.

See also:
:   [ALTER AGENT](/sql-reference/sql/alter-agent), [DESCRIBE AGENT](/sql-reference/sql/desc-agent), [DROP AGENT](/sql-reference/sql/drop-agent), [SHOW AGENTS](/sql-reference/sql/show-agents), [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] AGENT [ IF NOT EXISTS ] <name>
  [ COPY GRANTS ]
  [ SECURE = { TRUE | FALSE } ]
  [ COMMENT = '<comment>' ]
  [ PROFILE = '<profile_object>' ]
  FROM SPECIFICATION
  $$
    <specification_object>
  $$;
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the agent; must be unique for the schema in which the agent is created.

    You can create an agent in the `PUBLIC` schema of your [Personal Database](/user-guide/personal-databases) by using a fully qualified name in the form `"USER$<username>".PUBLIC.<agent_name>`.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`{ TEMP | TEMPORARY }`
:   Specifies that the agent persists only for the duration of the [session](/user-guide/session-policies) in which you created it. A temporary agent is bound to the creating user, role, and session. It is dropped automatically when the session ends and is not recoverable.

    `TEMP` is an accepted abbreviation for `TEMPORARY`.

    Creating a temporary agent does not require the CREATE AGENT privilege on the schema. Temporary agents cannot be converted to permanent agents, and they do not support versioning operations such as `COMMIT` or aliases.

    For more information, see [Working with temporary agents](/user-guide/snowflake-cortex/cortex-agents-temporary).

    Default: No value (agent is permanent)

`SECURE` or `SECURE = { TRUE | FALSE }`
:   Specifies whether the agent is secure. Use the `SECURE` keyword before `AGENT`, or set the `SECURE` property to `TRUE`, to create a secure agent. Setting the property to `FALSE` creates a non-secure agent.

    For a secure agent, the complete specification is visible only when the owner role is activated in the session. Roles with only USAGE or MODIFY cannot read the specification through DESCRIBE, GET\_DDL, SHOW VERSIONS, or stage paths. For more information, see [Secure agents](/user-guide/snowflake-cortex/cortex-agents-secure).

    Default: No value (agent is not secure)

`COPY GRANTS`
:   Retains the access privileges from the original agent when you replace it using `CREATE OR REPLACE AGENT`.

    When `COPY GRANTS` is specified, Snowflake copies all privileges granted on the existing agent to the replacement agent, except OWNERSHIP. The replacement agent does not inherit any future grants defined for the agent type in the schema. The role that executes the `CREATE OR REPLACE AGENT` statement owns the new agent.

    When `COPY GRANTS` is not specified, the replacement agent loses all explicit access privileges that were granted on the original agent. It inherits only future grants defined for the agent type in the schema.

    `COPY GRANTS` is meaningful only when used with `OR REPLACE`. If the agent does not already exist, there are no existing grants to copy and the clause has no effect.

    `COPY GRANTS` and `IF NOT EXISTS` are mutually exclusive. You cannot use both in the same statement.

    Default: No value (grants are not copied)

`COMMENT = 'comment'`
:   Description of the agent.

`PROFILE = profile_object`
:   Specifies the [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value containing agent profile information, such as display name, avatar, and color. Serialize the `profile_object` into a string as follows:

    Copy code

    ```
    '{"display_name": "<display_name>", "avatar": "<avatar>", "color": "<color>"}'
    ```

    The following table describes the key-value pairs in this object:

    | Key | Type | Description |
    | --- | --- | --- |
    | `display_name` | String | Display name for the agent. |
    | `avatar` | String | Avatar image file name or identifier. |
    | `color` | String | Color theme for the agent (such as “blue”, “green”, “red”) |

    Expand

    Show lessSee more

`FROM SPECIFICATION $$ specification_object $$`
:   Specifies the VARCHAR value containing the settings for an agent as a YAML object. The maximum length of the specification object is 100,000 bytes.

    Successful creation doesn’t guarantee valid tool specifications; test the agent before deploying it.

    The YAML object should have the following structure:

    Copy code

    ```
    models:
      orchestration: <model_name>

    orchestration:
      capabilities:
        analytical_search: true
      tool_not_accessible: <accept | reject | legacy>
      budget:
          seconds: <number_of_seconds>
          tokens: <number_of_tokens>

    instructions:
      response: '<response_instructions>'
      orchestration: '<orchestration_instructions>'
      sample_questions:
          - question: '<sample_question>'
          ...

    tools:
      - tool_spec:
          type: '<tool_type>'
          name: '<tool_name>'
          description: '<tool_description>'
          input_schema:
              type: 'object'
              properties:
                <property_name>:
                  type: '<property_type>'
                  description: '<property_description>'
              required: <required_property_names>
      ...

    tool_resources:
      <tool_name>:
        <resource_key>: '<resource_value>'
        ...
      ...
    ```

    The following table describes the key-value pairs in this object:

    | Key | Type | Description |
    | --- | --- | --- |
    | `models` | [ModelConfig](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agent-object-modelconfig) | An optional model configuration for the agent. Includes the orchestration model, for example `auto`, which lets Snowflake select the model. If not provided, a model is automatically selected. Currently only available for the *orchestration* step. |
    | `orchestration` | [OrchestrationConfig](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agent-object-orchestrationconfig) | An optional orchestration configuration, including budget constraints (seconds, tokens), capabilities such as `analytical_search`, and `tool_not_accessible` (`accept`, `reject`, or `legacy`). If `tool_not_accessible` is omitted, the default is `accept`. For details, see [Inaccessible tool handling](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling). |
    | `instructions` | [AgentInstructions](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agent-object-agentinstructions) | Optional instructions for the agent’s behavior, including response, orchestration, and sample questions. |
    | `tools` | array of [Tool](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agent-object-tool) | An optional list of tools available for the agent to use. Each tool includes a `tool_spec` with type, name, description, and input schema. Tools may have a corresponding configuration in `tool_resources`. |
    | `tool_resources` | map of [ToolResource](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agent-object-toolresource) | An optional configuration for each tool referenced in the tools array. Keys must match the name of the respective tool. |

    Expand

    Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE AGENT | Schema | Required to create a permanent Cortex Agent. Not required for temporary agents. |
| OWNERSHIP | Agent | Required to replace an existing agent with `CREATE OR REPLACE`. |
| USAGE | Cortex Search service | Required to run the Cortex Search services in the Cortex Agents request. |
| USAGE | Database, schema, table | Required to access the objects referenced in the Cortex Agents semantic model. |

Expand

Show lessSee more

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- Using `COPY GRANTS`:

  - When you run `CREATE OR REPLACE AGENT ... COPY GRANTS`, Snowflake drops the existing agent, creates the replacement, copies privileges (except OWNERSHIP), and assigns OWNERSHIP to the role that executed the statement, all within a single transaction.
  - Because the operation is atomic, any queries or runs in progress against the agent use either the old version or the new version, not a partial state.
  - `COPY GRANTS` does not copy future grants defined for the agent type in the schema. Only explicit grants on the original agent object are copied.
  - If the agent is shared with another account or exposed through a native app, the replacement agent remains shared when you use `COPY GRANTS`.
  - After replacing an agent with `COPY GRANTS`, run `SHOW GRANTS ON AGENT <name>` to verify that the expected privileges were copied.
  - Dropping explicit grants when replacing an agent without `COPY GRANTS` can break integrations and application flows that depend on those grants. Snowflake recommends using `COPY GRANTS` whenever you replace an agent that has been granted to other roles or shared with consumers.
- Temporary agents are session-scoped. If a temporary agent and a permanent agent share the same name in a schema, the temporary agent takes precedence for the duration of the session. For more information, see [Working with temporary agents](/user-guide/snowflake-cortex/cortex-agents-temporary).
- To control whether a missing privilege on a configured tool aborts the run, set `tool_not_accessible` on the specification’s top-level `orchestration` key, not on `models.orchestration` or `instructions.orchestration`. For details, see [Where to set the field](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling#label-cortex-agents-inaccessible-tool-where-to-set).

## Examples

Copy code

```
CREATE OR REPLACE AGENT my_agent1
  COMMENT = 'agent level comment'
  PROFILE = '{"display_name": "My Business Assistant", "avatar":  "business-icon.png", "color": "blue"}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto

  orchestration:
    capabilities:
      analytical_search: true
    tool_not_accessible: accept
    budget:
      seconds: 30
      tokens: 16000

  instructions:
    response: "You will respond in a friendly but concise manner"
    orchestration: "For any revenue question use Analyst; for policy use Search"
    sample_questions:
      - question: "What was our revenue last quarter?"

  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "Analyst1"
        description: "Converts natural language to SQL queries for financial analysis"
    - tool_spec:
        type: "cortex_search"
        name: "Search1"
        description: "Searches company policy and documentation"

  tool_resources:
    Analyst1:
      semantic_view: "db.schema.semantic_view"
    Search1:
      search_service: "db.schema.service_name"
      max_results: "5"
      filter:
        "@eq":
          region: "North America"
      title_column: "<title_name>"
      id_column: "<column_name>"
      stage_path: "@<db>.<schema>.<stage_name>"
      relative_path_column: "<relative_path_column_name>"
  $$;
```

### Create a temporary agent

Copy code

```
CREATE TEMPORARY AGENT my_temp_agent
  FROM SPECIFICATION
  $$
  models:
    orchestration: claude-sonnet-4-6
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "Analyst1"
  tool_resources:
    Analyst1:
      semantic_view: "my_db.my_schema.my_model"
  $$;
```

### Create an agent in a Personal Database

Create an agent in the `PUBLIC` schema of the Personal Database for the user `JSMITH`:

Copy code

```
CREATE OR REPLACE AGENT "USER$JSMITH".PUBLIC.MY_AGENT
  COMMENT = 'Personal Database agent'
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto

  instructions:
    response: "You are a helpful assistant."
  $$;
```

For an example that runs this agent, see [Run an agent in a [Personal Database](/user-guide/personal-databases) and…](/sql-reference/functions/data_agent_run-snowflake-cortex#label-data-agent-run-personal-database).

### Create a secure agent

Copy code

```
CREATE OR REPLACE SECURE AGENT my_sales_agent
  COMMENT = 'Production sales analyst.'
  FROM SPECIFICATION
  $$
  models:
    orchestration: claude-sonnet-4-6
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "RevenueAnalyst"
  tool_resources:
    RevenueAnalyst:
      semantic_view: "sales_db.public.revenue_model"
  $$;
```

### Replace an agent and preserve grants

Copy code

```
-- Create the original agent
CREATE OR REPLACE AGENT my_analytics_agent
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto
  $$;

-- Grant USAGE on the original agent
GRANT USAGE ON AGENT my_analytics_agent TO ROLE analyst_role;

-- Check existing grants before replacing
SHOW GRANTS ON AGENT my_analytics_agent;

-- Replace the agent and copy all existing grants to the replacement
CREATE OR REPLACE AGENT my_analytics_agent COPY GRANTS
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto
  $$;

-- Confirm grants were copied
SHOW GRANTS ON AGENT my_analytics_agent;
```

### Compare replace with and without COPY GRANTS

Copy code

```
-- Create the original agent
CREATE OR REPLACE AGENT my_agent
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto
  $$;

-- Grant USAGE on the original agent to an analyst role
GRANT USAGE ON AGENT my_agent TO ROLE analyst_role;

-- Replace WITHOUT COPY GRANTS: analyst_role loses USAGE
CREATE OR REPLACE AGENT my_agent
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto
  $$;
-- analyst_role can no longer invoke the agent

-- Restore the grant so the next replace has a privilege to copy
GRANT USAGE ON AGENT my_agent TO ROLE analyst_role;

-- Replace WITH COPY GRANTS: analyst_role retains USAGE
CREATE OR REPLACE AGENT my_agent COPY GRANTS
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto
  $$;
-- analyst_role can still invoke the agent
```
