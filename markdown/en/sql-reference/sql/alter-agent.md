# ALTER AGENT

Modifies the properties or specification for an existing [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents).

See also:
:   [CREATE AGENT](/sql-reference/sql/create-agent), [DESCRIBE AGENT](/sql-reference/sql/desc-agent), [DROP AGENT](/sql-reference/sql/drop-agent), [SHOW AGENTS](/sql-reference/sql/show-agents)

## Syntax

Copy code

```
ALTER AGENT <name> SET
  [ COMMENT = '<string>' ]
  [ PROFILE = '<string>' ]

ALTER AGENT <name> MODIFY LIVE VERSION SET SPECIFICATION = <specification>

ALTER AGENT <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER AGENT <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the agent to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`SET ...`
:   Sets one or more specified properties or parameters for the agent:

    `COMMENT = comment`
    :   Specifies the description of the agent.

    `PROFILE = string`
    :   Specifies the agent profile information, such as display name, avatar, and color. Format the string as follows:

        Copy code

        ```
        '{"display_name": "<display_name>", "avatar": "<avatar>", "color": "<color>"}'
        ```

        The following table describes the key-value pairs in the string:

        | Key | Type | Description |
        | --- | --- | --- |
        | `display_name` | String | Display name for the agent. |
        | `avatar` | String | Avatar image file name or identifier. |
        | `color` | String | Color theme for the agent (such as “blue”, “green”, “red”) |

        Expand

        Show lessSee more

`MODIFY LIVE VERSION SET SPECIFICATION specification`
:   Specifies the VARCHAR value containing the replacement settings for an agent as either a YAML or JSON object:

    - [Dollar-quoted literal](/sql-reference/data-types-text#label-dollar-quoted-string-constants): $$ … $$
    - [Single-quoted string](/sql-reference/data-types-text#label-single-quoted-string-constants): ‘…’

    The maximum length of the specification object is 100,000 bytes.

    Important

    The new specification completely replaces the existing one. Fields that are not included in the new specification are removed.

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

    The JSON object should have the following structure:

    Copy code

    ```
    {
      "models": {
        "orchestration": "<model_name>"
      },
      "orchestration": {
        "capabilities": {
          "analytical_search": true
        },
        "tool_not_accessible": "<accept | reject | legacy>",
        "budget": {
          "seconds": <number_of_seconds>,
          "tokens": <number_of_tokens>
        }
      },
      "instructions": {
        "response": "<response_instructions>",
        "orchestration": "<orchestration_instructions>",
        "sample_questions": [
          {
            "question": "<sample_question>"
          }
        ]
      },
      "tools": [
        {
          "tool_spec": {
            "type": "<tool_type>",
            "name": "<tool_name>",
            "description": "<tool_description>",
            "input_schema": {
              "type": "object",
              "properties": {
                "<property_name>": {
                  "type": "<property_type>",
                  "description": "<property_description>"
                }
              },
              "required": ["<required_property_names>"]
            }
          }
        }
      ],
      "tool_resources": {
        "<tool_name>": {
          "<resource_key>": "<resource_value>"
        }
      }
    }
    ```

    The following table describes the key-value pairs in this object:

    | Key | Type | Description |
    | --- | --- | --- |
    | `models` | [ModelConfig](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agent-object-modelconfig) | An optional model configuration for the agent. Includes the orchestration model (e.g., claude-4-sonnet). If not provided, a model is automatically selected. Currently only available for the *orchestration* step. |
    | `orchestration` | [OrchestrationConfig](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agent-object-orchestrationconfig) | An optional orchestration configuration, including budget constraints (seconds, tokens), capabilities such as `analytical_search`, and `tool_not_accessible` (`accept`, `reject`, or `legacy`). If `tool_not_accessible` is omitted, the default is `accept`. For details, see [Inaccessible tool handling](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling). |
    | `instructions` | [AgentInstructions](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agent-object-agentinstructions) | Optional instructions for the agent’s behavior, including response, orchestration, and sample questions. |
    | `tools` | array of [Tool](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agent-object-tool) | An optional list of tools available for the agent to use. Each tool includes a `tool_spec` with type, name, description, and input schema. Tools may have a corresponding configuration in `tool_resources`. |
    | `tool_resources` | map of [ToolResource](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agent-object-toolresource) | An optional configuration for each tool referenced in the tools array. Keys must match the name of the respective tool. |

    Expand

    Show lessSee more

`SET TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' ... ]`
:   `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET TAG tag_name [ , tag_name ... ]`
:   Specifies one or more tags to unset on the agent:

    - `tag_name [ , tag_name ... ]`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or MODIFY | Agent | Required to modify the agent properties or specification.  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When modifying a live version’s specification, the new specification completely replaces the existing one.
  Fields that are not included in the new specification are removed.
- Both YAML and JSON formats are supported for specifications.
- Invalid specification fields result in an error.
- To control whether a missing privilege on a configured tool aborts the run, set `tool_not_accessible` on the specification’s top-level `orchestration` key, not on `models.orchestration` or `instructions.orchestration`. For details, see [Where to set the field](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling#label-cortex-agents-inaccessible-tool-where-to-set).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Update the comment for an agent:

Copy code

```
ALTER AGENT my_support_agent SET COMMENT = 'Customer support agent for product inquiries';
```

Update the profile for an agent:

Copy code

```
ALTER AGENT my_support_agent SET PROFILE = '{"display_name": "Support Bot", "avatar": "bot-icon.png"}';
```

Update both the comment and profile together:

Copy code

```
ALTER AGENT my_support_agent
  SET COMMENT = 'Production support agent',
      PROFILE = '{"display_name": "Customer Assistant", "avatar": "assistant.png"}';
```

Update the live version specification using YAML format:

Copy code

```
ALTER AGENT my_support_agent
  MODIFY LIVE VERSION SET SPECIFICATION =
  $$
  models:
    orchestration: claude-sonnet-4-6

  orchestration:
    tool_not_accessible: accept
    budget:
      seconds: 30
      tokens: 50000

  instructions:
    response: "Always be concise and accurate."
    orchestration: "Use available tools to look up order details before answering."
    sample_questions:
      - question: "What is the status of my order?"
  $$;
```

Update the live version specification using JSON format:

Copy code

```
ALTER AGENT my_support_agent
  MODIFY LIVE VERSION SET SPECIFICATION = '{"models":{"orchestration":"claude-sonnet-4-6"},"orchestration":{"tool_not_accessible":"accept","budget":{"seconds":45,"tokens":80000}}}';
```

Set a tag on an agent:

Copy code

```
ALTER AGENT my_support_agent SET TAG cost_center = 'engineering';
```

Unset a tag on an agent:

Copy code

```
ALTER AGENT my_support_agent UNSET TAG cost_center;
```
