Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AGENT\_RUN (SNOWFLAKE.CORTEX)

Runs a [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents) without an agent object and returns the response as JSON.

You can use this function to interact with Cortex Agents directly without first creating an agent object. You provide the configuration, including the orchestration model and tools, in the request body.

Note

`SNOWFLAKE.CORTEX.AGENT_RUN` is a utility wrapper around the [Cortex Agents Run REST API](/user-guide/snowflake-cortex/cortex-agents-run).
For most application integrations, Snowflake recommends calling the **streaming REST API** directly.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.AGENT_RUN( <request_body> [, <create_thread_if_not_present> ] )
```

## Arguments

`request_body`
:   JSON request body to send to the agent. This value must be a string (for example, a `$$...$$` literal).

    The following fields are supported in the request body:

    | Field | Type | Description |
    | --- | --- | --- |
    | `thread_id` | integer | The thread ID for the conversation. If thread\_id is used, then parent\_message\_id must be passed as well. |
    | `parent_message_id` | integer | The ID of the parent message in the thread. If this is the first message, parent\_message\_id should be 0. |
    | `messages` | array of [Message](#label-snowflake-agent-run-message) | If thread\_id and parent\_message\_id are passed in the request, messages includes the current user message in the conversation. Else, messages includes the conversation history and the current message. Messages contains both user queries and assistant responses in chronological order. |
    | `background` | boolean | Whether to run the agent asynchronously. If `true`, the agent runs asynchronously in the background with a 6 hour timeout, even if the client disconnects. For a background run with `stream` set to `false`, the API returns immediately with `status: in_progress` and a `run_id`; retrieve the response after the run completes by streaming from the Stream Agent Run endpoint with the `run_id` (REST API) or by polling the THREAD\_MESSAGES SQL function with the thread ID. If `stream` is `true`, the response is streamed as Server-Sent Events. If `background` is `false`, the agent runs synchronously with a 15 minute timeout. Only available when using threads to manage conversation history. |
    | `stream` | boolean | Whether to return a streaming response (`text/event-stream`) or a non-streaming JSON response (`application/json`). If true, the response will be streamed as Server-Sent Events. If false, the response will be returned as JSON. |
    | `tool_choice` | [ToolChoice](#label-snowflake-agent-run-toolchoice) | Configures how the agent should select and use tools during the interaction. Controls whether tool use is automatic, required, or whether specific tools should be used. |
    | `models` | [ModelConfig](#label-snowflake-agent-run-modelconfig) | Model configuration for the agent. Includes the orchestration model (e.g., claude-4-sonnet). If not provided, a model is automatically selected. Currently only available for the `orchestration` step. |
    | `instructions` | [AgentInstructions](#label-snowflake-agent-run-agentinstructions) | Instructions for the agent’s behavior, including response, orchestration, and sample questions. |
    | `orchestration` | [OrchestrationConfig](#label-snowflake-agent-run-orchestrationconfig) | Orchestration configuration, including budget constraints (e.g., seconds, tokens). |
    | `tools` | array of [Tool](#label-snowflake-agent-run-tool) | List of tools available for the agent to use. Each tool includes a tool\_spec with type, name, description, and input schema. Tools may have a corresponding configuration in tool\_resources. |
    | `tool_resources` | map of [ToolResource](#label-snowflake-agent-run-toolresource) | Configuration for each tool referenced in the tools array. Keys must match the name of the respective tool. |

    Expand

    Show lessSee more

    **Example**

    Copy code

    ```
    {
      "thread_id": 0,
      "parent_message_id": 0,
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "What is the total revenue for 2023?"
            }
          ],
          "status": "completed",
          "error": {
            "code": "399504",
            "message": "Error during execution"
          }
        }
      ],
      "background": false,
      "stream": false,
      "tool_choice": {
        "type": "auto",
        "name": [
          "analyst_tool",
          "search_tool"
        ]
      },
      "models": {
        "orchestration": "claude-4-sonnet"
      },
      "instructions": {
        "response": "You will respond in a friendly but concise manner",
        "orchestration": "For any query related to revenue we should use Analyst; For all policy questions we should use Search"
      },
      "orchestration": {
        "budget": {
          "seconds": 30,
          "tokens": 16000
        }
      },
      "tools": [
        {
          "tool_spec": {
            "type": "generic",
            "name": "get_revenue",
            "description": "Fetch the delivery revenue for a location.",
            "input_schema": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "The city and state, e.g. San Francisco, CA"
                }
              }
            },
            "required": [
              "location"
            ]
          }
        }
      ],
      "tool_resources": {
        "get_revenue": {
          "type": "function",
          "execution_environment": {
            "type": "warehouse",
            "warehouse": "MY_WH"
          },
          "identifier": "DB.SCHEMA.UDF"
        }
      }
    }
    ```

`create_thread_if_not_present`
:   A BOOLEAN value that specifies whether to automatically create a new thread when the request body does not include a `thread_id`. Default: `FALSE`.

Important

Setting `stream` to `true` in the request body is not supported. If you include `"stream": true`, the function returns an error.
A non-streaming response is always returned.

Asynchronous (background) runs

You can run the agent asynchronously by setting `"background": true` in the request body. Background runs are generally available on AWS and Azure. When you do:

- A `thread_id` is required in the request body.
- The function returns immediately with a response containing `"status": "in_progress"` and a `run_id`.
- Poll [THREAD\_MESSAGES (SNOWFLAKE.CORTEX)](/sql-reference/functions/thread_messages-snowflake-cortex) with the thread ID to retrieve the assistant response after the run completes.

## Returns

Returns a JSON string containing the agent’s response.

## Access control requirements

To run an agent, you must use a role that can access Cortex Agents.
For details, see [API access roles](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-access-control).

## Usage notes

- The function returns a JSON string. Pass this string to [TRY\_PARSE\_JSON](/sql-reference/functions/try_parse_json) to convert the response to a VARIANT value.
- Unlike [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex), this function does not require you to create an agent object first. Instead, you provide the configuration directly in the request body.
- When `create_thread_if_not_present` is set to `TRUE`, a new thread is automatically created if the request body does not contain a `thread_id`. The response includes the `thread_id` of the newly created thread, which you can use in subsequent requests to continue the conversation.
- To run the agent asynchronously, set `"background": true` in the request body and include a `thread_id`. The function returns immediately with an in-progress status and a `run_id`. Use [THREAD\_MESSAGES (SNOWFLAKE.CORTEX)](/sql-reference/functions/thread_messages-snowflake-cortex) to poll for the completed response.

## Examples

Run an agent and parse the response JSON:

Copy code

```
SELECT
  TRY_PARSE_JSON(
    SNOWFLAKE.CORTEX.AGENT_RUN(
      $${
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": "What is the total revenue for 2025?"
              }
            ]
          }
        ],
        "models": {
          "orchestration": "claude-sonnet-4-6"
        }
      }$$
    )
  ) AS resp;
```

Sample return value:

Copy code

```
{
  "content": [
    {
      "text": "The total revenue for 2025 was $100,000.",
      "type": "text"
    }
  ],
  "metadata": {
    "usage": {
      "tokens_consumed": [
        {
          "context_window": 200000,
          "input_tokens": {
            "cache_read": 0,
            "cache_write": 0,
            "total": 67,
            "uncached": 67
          },
          "model_name": "claude-sonnet-4-6",
          "output_tokens": {
            "total": 38
          }
        }
      ]
    }
  },
  "role": "assistant"
}
```

Run an agent with automatic thread creation:

Copy code

```
SELECT
  TRY_PARSE_JSON(
    SNOWFLAKE.CORTEX.AGENT_RUN(
      $${
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": "What is the total revenue for 2025?"
              }
            ]
          }
        ],
        "models": {
          "orchestration": "claude-sonnet-4-6"
        }
      }$$,
      TRUE
    )
  ) AS resp;
```
