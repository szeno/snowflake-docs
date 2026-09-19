Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)

Runs a [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents) and returns the response as JSON.

You can use this function to run a Cortex Agent, which orchestrates across both structured and unstructured data sources to deliver insights. This includes planning tasks, using tools to execute these tasks, and generating responses.

Note

`SNOWFLAKE.CORTEX.DATA_AGENT_RUN` is a utility wrapper around the [Cortex Agents Run API](/user-guide/snowflake-cortex/cortex-agents-run).
For most application integrations, Snowflake recommends calling the **streaming REST API** directly.

See also:
:   [CREATE AGENT](/sql-reference/sql/create-agent), [SHOW AGENTS](/sql-reference/sql/show-agents), [DESCRIBE AGENT](/sql-reference/sql/desc-agent), [DROP AGENT](/sql-reference/sql/drop-agent)

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.DATA_AGENT_RUN( '<agent_name>[!<version>]', <request_body> [, <create_thread_if_not_present> ] )
```

## Arguments

`'agent_name[!version]'`
:   Fully qualified name of the agent to run, in the form `database.schema.agent_name`.

    You can optionally append `!<version>` to target a specific [agent version](/user-guide/snowflake-cortex/cortex-agents-versioning).
    If no version suffix is specified, the agent’s DEFAULT version is used (which falls back to the LIVE version if no
    default has been explicitly set).

    The following version values are supported:

    | Version suffix | Description |
    | --- | --- |
    | `!LIVE` | Runs the current LIVE (draft) version. |
    | `!DEFAULT` | Runs the DEFAULT version. |
    | `!VERSION$N` | Runs a specific committed version (for example, `!VERSION$2`). |
    | `!LAST` | Runs the most recently committed version. |
    | `!FIRST` | Runs the first committed version. |

    Expand

    Show lessSee more

    If the agent name contains a `!` character, enclose that part of the name in double quotes so it is not
    treated as a version separator. For example, `'db.schema."my!agent"!LIVE'` targets the LIVE version of
    an agent named `my!agent`.

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

The function returns the final aggregated response rather than the individual SSE events produced by the Cortex Agents Run API. If a non-fatal warning occurs, the response includes a top-level `warnings` array. For example, warning code `399569` means that the caller’s role couldn’t access a named tool and the agent continued with its remaining tools.

## Access control requirements

To run an agent, you must use a role that can access Cortex Agents and the agent object you’re calling.
For details, see [API access roles](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-access-control).

## Usage notes

- The function returns a JSON string. Pass this string to [TRY\_PARSE\_JSON](/sql-reference/functions/try_parse_json) to convert the response to a VARIANT value.
- Inspect the top-level `warnings` array in the parsed response and surface relevant warnings to users. For inaccessible-tool warning behavior, see .
- When `create_thread_if_not_present` is set to `TRUE`, a new thread is automatically created if the request body does not contain a `thread_id`. The response includes the `thread_id` of the newly created thread, which you can use in subsequent requests to continue the conversation.
- To run the agent asynchronously, set `"background": true` in the request body and include a `thread_id`. The function returns immediately with an in-progress status and a `run_id`. Use [THREAD\_MESSAGES (SNOWFLAKE.CORTEX)](/sql-reference/functions/thread_messages-snowflake-cortex) to poll for the completed response.

## Examples

Run an agent and parse the response JSON:

Copy code

```
SELECT
  TRY_PARSE_JSON(
    SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
      'MY_DB.MY_SCHEMA.MY_AGENT',
      $${
        "parent_message_id": 1234,
        "thread_id": 5678,
        "messages": [
          {
            "role": "user",
            "content": [
              { "type": "text", "text": "What are some types of products?" }
            ]
          }
        ]
      }$$
    )
  ) AS resp;
```

Sample return value:

Copy code

```
{
  "role": "assistant",
  "content": [
    {
      "thinking": {
        "text": "\n...\n"
      },
      "type": "thinking"
    },
    {
      "tool_use": {
        "input": {
          "...": "..."
        },
        "name": "<tool_name>",
        "tool_use_id": "<tool_use_id>",
        "type": "<tool_type>"
      },
      "type": "tool_use"
    },
    {
      "text": "Based on the data available, there are two main types of products...",
      "type": "text"
    }
  ],
  "warnings": [
    {
      "code": "399569",
      "message": "TOOL_NOT_ACCESSIBLE: Search1 (cortex_search) - The Cortex Search Service does not exist or access is not authorized for the current role: db.schema.css1"
    }
  ],
  "metadata": {
    "run_id": "<run_id>"
  }
}
```

To return only inaccessible-tool warnings from a synchronous run:

Copy code

```
WITH agent_response AS (
  SELECT TRY_PARSE_JSON(
    SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
      'MY_DB.MY_SCHEMA.MY_AGENT',
      $${
        "messages": [
          {
            "role": "user",
            "content": [
              { "type": "text", "text": "What are some types of products?" }
            ]
          }
        ]
      }$$
    )
  ) AS response
)
SELECT warning.value
  FROM agent_response,
    LATERAL FLATTEN(input => response:warnings) AS warning
  WHERE warning.value:code::STRING = '399569';
```

Run an agent with automatic thread creation:

Copy code

```
SELECT
  TRY_PARSE_JSON(
    SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
      'MY_DB.MY_SCHEMA.MY_AGENT',
      $${
        "messages": [
          {
            "role": "user",
            "content": [
              { "type": "text", "text": "What are some types of products?" }
            ]
          }
        ]
      }$$,
      TRUE
    )
  ) AS resp;
```

Run an agent in a [Personal Database](/user-guide/personal-databases) and create a thread automatically:

Copy code

```
SELECT TRY_PARSE_JSON(
  SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    '"USER$JSMITH".PUBLIC.MY_AGENT',
    $${
      "messages": [
        {
          "role": "user",
          "content": [
            { "type": "text", "text": "What are some types of products?" }
          ]
        }
      ]
    }$$,
    TRUE
  )
) AS resp;
```

Run a specific committed version of an agent:

Copy code

```
SELECT
  TRY_PARSE_JSON(
    SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
      'MY_DB.MY_SCHEMA.MY_AGENT!VERSION$2',
      $${
        "messages": [
          {
            "role": "user",
            "content": [
              { "type": "text", "text": "What are some types of products?" }
            ]
          }
        ]
      }$$
    )
  ) AS resp;
```

Run the LIVE (draft) version of an agent:

Copy code

```
SELECT
  TRY_PARSE_JSON(
    SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
      'MY_DB.MY_SCHEMA.MY_AGENT!LIVE',
      $${
        "messages": [
          {
            "role": "user",
            "content": [
              { "type": "text", "text": "What are some types of products?" }
            ]
          }
        ]
      }$$
    )
  ) AS resp;
```
