# Cortex Agents Run API

Note

By default, requests to the Cortex Agent REST API time out after 15 minutes. To run longer requests, set the `background` field to `true` in the request body. Background runs time out after 6 hours, and you can reconnect to them with the [Stream Agent Run](#stream-agent-run) endpoint. Background runs are generally available on AWS and Azure, and they’re only available when you use threads to manage conversation history.

There are two methods to interact with an Agent:

- Build an agent object and reference this agent object in a request to the `agent:run` API.
- Call `agent:run` directly without an agent object. You provide the configuration in the request body of `agent:run`.

`agent:run` supports **streaming responses by default**. To disable streaming and receive a single JSON response, set `stream` to `false`.

Tip

You can also run agents using SQL with the [DATA\_AGENT\_RUN](/sql-reference/functions/data_agent_run-snowflake-cortex) function.
The SQL function returns a non-streaming JSON response and doesn’t require a REST client. For most use cases, Snowflake recommends the REST API.

## Agent run request with agent object

`POST /api/v2/databases/{database}/schemas/{schema}/agents/{name}:run`

Sends a user query to the agent object and returns its response.

By default, the API streams responses as server-sent events (SSE). To receive a single JSON response, set `stream` to `false` in the request body.

Note

You can’t set, update, or overwrite the `models`, `instructions`, and `orchestration` fields using this request. To update these fields, you must use [Update Cortex Agent](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agents-rest-api-update).

### Path parameters

| Parameter | Description |
| --- | --- |
| `database` | (Required) The database containing the agent. You can use the */api/v2/databases* GET request to get a list of available databases. |
| `schema` | (Required) The schema containing the agent. You can use the */api/v2/databases/{database}/schemas* GET request to get a list of available schemas for the specified database. |
| `name` | (Required) The name of the agent. |

Expand

Show lessSee more

### Request headers

| Header | Description |
| --- | --- |
| `Authorization` | (Required) Authorization token. See [Authentication](/user-guide/snowflake-cortex/cortex-agents-setup#label-chat-api-authenticate-example). |
| `Content-Type` | (Required) application/json |
| `Accept` | (Optional) Response content type. Use `text/event-stream` for streaming responses or `application/json` for a single non-streaming response. |

Expand

Show lessSee more

### Request body

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

The `orchestration` configuration, including `tool_not_accessible`, comes from the agent object’s specification. You can’t set `tool_not_accessible` in this run request. To change it, set it on the top-level `orchestration` object of the agent specification, not on `models.orchestration` or `instructions.orchestration`:

Copy code

```
{
  "orchestration": {
    "tool_not_accessible": "accept"
  }
}
```

For the update endpoint and full agent specification, see [Update Cortex Agent](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agents-rest-api-update).

The request body supports an optional `stream` boolean field:

- If `stream` is omitted, it defaults to `true` and the response is streamed as SSE events.
- If `stream` is `false`, the API returns a single JSON object (see [Non-streaming response (stream: false)](#label-snowflake-agents-run-non-streaming-response)).

## Agent run without an agent object

`POST /api/v2/cortex/agent:run`

Sends a user query to the Cortex Agents service provided in the request body and returns its response.
Interacts with the agent without creating an agent object.

Note

Before September 1st, 2025, the request and response schemas for the `agent:run` API were different from the schema listed in this document. Previously, the orchestration was static and the same sequence of tools was used to generate an answer. `agent:run` now has an updated schema for both the request and response. In addition, the API now dynamically orchestrates and iterates to arrive at the final response. We recommend using the schema described in this document for an improved end-user experience.

To use the legacy schema and behavior, use the following schema:

Copy code

```
{
  "model": "claude-sonnet-4-6",
  "messages": [
     {"role":"user", "content": [] }
  ]
}
```

### Request headers

| Header | Description |
| --- | --- |
| `Authorization` | (Required) Authorization token. See [Authentication](/user-guide/snowflake-cortex/cortex-agents-setup#label-chat-api-authenticate-example). |
| `Content-Type` | (Required) application/json |
| `Accept` | (Optional) Response content type. Use `text/event-stream` for streaming responses or `application/json` for a single non-streaming response. |

Expand

Show lessSee more

### Request body

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

For a run without an agent object, set `tool_not_accessible` in the top-level `orchestration` object of the request body. This request body has three different keys named `orchestration`: the top-level `orchestration` object holds run controls such as `tool_not_accessible` and `budget`, `models.orchestration` names the orchestration model, and `instructions.orchestration` holds natural-language instructions. Only the top-level object accepts `tool_not_accessible`:

Copy code

```
{
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
    "orchestration": "claude-4-sonnet"
  },
  "instructions": {
    "orchestration": "Use the search tool for all refund questions."
  },
  "orchestration": {
    "tool_not_accessible": "accept",
    "budget": {
      "seconds": 30,
      "tokens": 16000
    }
  },
  "tools": [],
  "tool_resources": {}
}
```

If you omit `tool_not_accessible`, the default is `accept`. For all values and their behavior, see [Where to set the field](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling#label-cortex-agents-inaccessible-tool-where-to-set).

The request body supports an optional `stream` boolean field:

- If `stream` is omitted, it defaults to `true` and the response is streamed as SSE events.
- If `stream` is `false`, the API returns a single JSON object (see [Non-streaming response (stream: false)](#label-snowflake-agents-run-non-streaming-response)).

## Streaming responses

The `agent:run` API provides streaming responses. The server streams back events. This allows you to display responses in your application, token-by-token, as they are generated by the Agent.
Each event streamed in the API response has a strictly typed schema. You can find a list of all of the events in the following section and select to which ones you’d like to subscribe.

The last event sent by the API is a `response` event. This event contains the entire agent output. You can use this as
the agent’s final response. For any non-streaming clients, you can subscribe to this event because it is the logical aggregation of all prior events. If you don’t want to use streaming responses, wait for the `response` event and ignore all prior events.

The majority of the other events streamed can be split into two categories: *Delta* and *Content Items*.

*Delta* events represent a single token generated by the Agent. By listening to these events, you can create
a typewriter effect. The main delta events are *response.thinking.delta*, which
represents a reasoning token, and *response.text.delta*, which represent an answer token.

*Content Item* events represent elements from the *content* array in the final agent response.

Note

Make sure your application can handle unknown event types.

When a named tool isn’t accessible and `tool_not_accessible` is `accept`, the stream includes a `response.warning` event before the first model call. The warning is also included in the top-level `warnings` array of the final `response` event. Applications should handle the SSE event or inspect the final array so users know the answer might not use every configured tool. For the warning format and the other access modes, see .

**Example Response**

Copy code

```
event: response.status
data: {"message":"Planning the next steps","status":"planning"}

event: response.thinking.delta
data: {"content_index":0,"text":"\nThe user is asking for a"}

event: response.thinking.delta
data: {"content_index":0,"text":" chart showing the"}

...
...
...

event: response.status
data: {"message":"Reviewing the results","status":"reasoning_agent_stop"}

event: response.status
data: {"message":"Forming the answer","status":"proceeding_to_answer"}
```

# `response`

Event streamed when the final response is available. This is the last event emitted, it represents the aggregation of all other events previously streamed.

| Field | Type | Description |
| --- | --- | --- |
| `role` | string | The role for the message. Always `assistant` in the API response. |
| `content` | array of [MessageContentItem](#label-snowflake-agent-run-messagecontentitem) | The content generated by the agent. |
| `warnings` | array of [Warning](#label-snowflake-agent-run-warning) | Non-fatal warnings that occurred during processing. Present for non-streaming clients or as a summary. |
| `metadata` | [ResponseMetadata](#label-snowflake-agent-run-responsemetadata) |  |
| `status` | string | The completion status of the agent run. Set to “cancelled” when the run was terminated via CancelAgentRun, or “timed\_out” when the run exceeded its max run length. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "role": "assistant",
  "content": [
    {
      "type": "actual_user_message"
    }
  ],
  "warnings": [
    {
      "message": "Unable to fetch tools from MCP server 'foo'. Response quality may be degraded.",
      "code": "003001"
    }
  ],
  "metadata": {
    "usage": {
      "tokens_consumed": [
        {
          "model_name": "llama3.1-70b",
          "input_tokens": {
            "total": 175,
            "cache_read": 50,
            "cache_write": 25,
            "uncached": 100
          },
          "output_tokens": {
            "total": 75
          },
          "context_window": 128000
        }
      ]
    },
    "run_id": "4264-83472",
    "thread_id": 4264,
    "user_message_id": 83472,
    "assistant_message_id": 83473
  },
  "status": "completed"
}
```

## `response.text`

An event streamed when a text content block is done streaming, including all the aggregated deltas for a particular content index.

| Field | Type | Description |
| --- | --- | --- |
| `content_index` | integer | The index in the response content array this event represents |
| `text` | string | A text result from the agent |
| `annotations` | array of [Annotation](#label-snowflake-agent-run-annotation) | Any annotations attached to the text result (e.g. citations) |
| `is_elicitation` | boolean | Whether this text content is the agent asking for more information from the end user. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "content_index": 0,
  "text": "Lorem ipsum dolor...",
  "annotations": [
    {
      "type": "cortex_search_citation",
      "index": 0,
      "search_result_id": "cs_61987ff6-6d56-4695-83c0-1e7cfed818c7",
      "doc_id": "4ac085cb-82d0-4eb4-94f3-2672aa0599a2",
      "doc_title": "Earnings Report",
      "text": "The revenue for 2025 was..."
    }
  ],
  "is_elicitation": false
}
```

## `response.text.delta`

Event streamed when a new output text delta is generated.

| Field | Type | Description |
| --- | --- | --- |
| `content_index` | integer | The index in the response content array this event represents |
| `text` | string | The text delta |
| `is_elicitation` | boolean | Whether this text content is the agent asking for more information from the end user. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "content_index": 0,
  "text": "Hello",
  "is_elicitation": false
}
```

## `response.text.annotation`

Event streamed when an annotation is added to a text content.

| Field | Type | Description |
| --- | --- | --- |
| `content_index` | integer | The index in the response content array this event represents |
| `annotation_index` | integer | The index in the annotation array this `annotation` belongs to. |
| `annotation` | [Annotation](#label-snowflake-agent-run-annotation) | The annotation object being added. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "content_index": 0,
  "annotation_index": 0,
  "annotation": {
    "type": "cortex_search_citation",
    "index": 0,
    "search_result_id": "cs_61987ff6-6d56-4695-83c0-1e7cfed818c7",
    "doc_id": "4ac085cb-82d0-4eb4-94f3-2672aa0599a2",
    "doc_title": "Earnings Report",
    "text": "The revenue for 2025 was..."
  }
}
```

## `response.thinking`

An event streamed when a thinking content block is done streaming, including all the aggregated deltas for a particular content index.

| Field | Type | Description |
| --- | --- | --- |
| `content_index` | integer | The index in the response content array this event represents |
| `text` | string | Thinking tokens from the agent |
| `signature` | string | The signature of the thinking token |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "content_index": 0,
  "text": "To answer your question I must...",
  "signature": "lorem ipsum"
}
```

## `response.thinking.delta`

Event streamed when a thinking delta is generated.

| Field | Type | Description |
| --- | --- | --- |
| `content_index` | integer | The index in the response content array this event represents |
| `text` | string | The thinking token |
| `signature` | string | The signature of the thinking token |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "content_index": 0,
  "text": "lorem ipsum",
  "signature": "lorem ipsum"
}
```

## `response.tool_use`

An event streamed when the agent requests a tool use.

| Field | Type | Description |
| --- | --- | --- |
| `content_index` | integer | The index in the response content array this event represents |
| `tool_use_id` | string | Unique identifier for this tool use. Can be used to associated tool results. |
| `type` | string | The type of the tool (e.g. cortex\_search, cortex\_analyst\_text\_to\_sql) |
| `name` | string | The unique identifier for this tool instance |
| `input` | object | The structured input for this tool. The schema of this object should will vary depending on the tool spec. |
| `client_side_execute` | boolean | Whether the tool use is executed on the client side. |
| `permission` | [ToolUsePermission](#label-snowflake-agent-run-toolusepermission) |  |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "content_index": 0,
  "tool_use_id": "toolu_123",
  "type": "cortex_analyst_text_to_sql",
  "name": "my_cortex_analyst_semantic_view",
  "input": {
    "location": "San Francisco, CA"
  },
  "client_side_execute": "true",
  "permission": {
    "options": [
      "Allow Once",
      "Deny"
    ]
  }
}
```

## `response.tool_result`

Event streamed when a tool finishes executing, including the tool result.

| Field | Type | Description |
| --- | --- | --- |
| `content_index` | integer | The index in the response content array this event represents |
| `tool_use_id` | string | Unique identifier for this tool use. Can be used to associated tool results. |
| `type` | string | The type of the tool (e.g. cortex\_search, cortex\_analyst\_text\_to\_sql) |
| `name` | string | The unique identifier for this tool instance |
| `content` | array of [ToolResultContent](#label-snowflake-agent-run-toolresultcontent) | The content on the tool result |
| `status` | string | The status of tool execution |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "content_index": 0,
  "tool_use_id": "toolu_123",
  "type": "cortex_analyst_text_to_sql",
  "name": "my_cortex_analyst_semantic_view",
  "content": [
    {
      "type": "json",
      "json": {
        "answer": 42
      }
    }
  ],
  "status": "success"
}
```

## `response.tool_result.status`

Status update for a specific tool use.

| Field | Type | Description |
| --- | --- | --- |
| `tool_use_id` | string | Unique identifier for this tool use. |
| `tool_type` | string | The type of the tool (e.g. cortex\_search, cortex\_analyst\_text\_to\_sql) |
| `status` | string | Enum for the current state. |
| `message` | string | A more descriptive message expanding on the current status. |
| `details` | object | Tool-specific status details. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "tool_use_id": "toolu_123",
  "tool_type": "cortex_analyst_text_to_sql",
  "status": "Executing SQL",
  "message": "Executing query 'SELECT * FROM my_table'",
  "details": {}
}
```

## `response.tool_result.analyst.delta`

An delta event streamed for the Cortex Analyst tool execution

| Field | Type | Description |
| --- | --- | --- |
| `content_index` | integer | The index in the response content array this event represents |
| `tool_use_id` | string | Unique identifier for this tool use. Can be used to associated tool results. |
| `tool_type` | string | The type of the tool (always cortex\_analyst\_text\_to\_sql for this event) |
| `tool_name` | string | The unique identifier for this tool instance |
| `delta` | [CortexAnalystToolResultDelta](#label-snowflake-agent-run-cortexanalysttoolresultdelta) | The content delta |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "content_index": 0,
  "tool_use_id": "toolu_123",
  "tool_type": "cortex_analyst_text_to_sql",
  "tool_name": "my_cortex_analyst_semantic_view",
  "delta": {
    "text": "The...",
    "think": "Thinking...",
    "sql": "SELECT...",
    "sql_explanation": "This...",
    "query_id": "707787a0-a684-4ead-adb0-3c3b62b043d9",
    "verified_query_used": false,
    "result_set": {
      "statementHandle": "707787a0-a684-4ead-adb0-3c3b62b043d9",
      "resultSetMetaData": {
        "partition": 0,
        "numRows": 0,
        "format": "jsonv2",
        "rowType": [
          {
            "name": "my_column",
            "type": "VARCHAR",
            "length": 0,
            "precision": 0,
            "scale": 0,
            "nullable": false
          }
        ]
      },
      "data": [
        [
          "row1 col1",
          "row1 col2"
        ],
        [
          "row2 col1",
          "row2 col2"
        ]
      ]
    },
    "suggestions": {
      "index": 0,
      "delta": "What..."
    }
  }
}
```

## `response.table`

An event streamed when a table content block is added.

| Field | Type | Description |
| --- | --- | --- |
| `content_index` | integer | The index in the response content array this event represents |
| `tool_use_id` | string | The ID of the tool use that generated this table |
| `query_id` | string | The query id of the sql query that generated this data |
| `result_set` | [ResultSet](#label-snowflake-agent-run-resultset) | The SQL results to render a table. Matches the schema from Snowflake’s SQL API ResultSet (<https://docs.snowflake.com/en/developer-guide/sql-api/reference#resultset>) |
| `title` | string | The title for this table |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "content_index": 0,
  "tool_use_id": "toolu_123",
  "query_id": "6ac75378-6337-48a6-80ab-6de48dd680eb",
  "result_set": {
    "statementHandle": "707787a0-a684-4ead-adb0-3c3b62b043d9",
    "resultSetMetaData": {
      "partition": 0,
      "numRows": 0,
      "format": "jsonv2",
      "rowType": [
        {
          "name": "my_column",
          "type": "VARCHAR",
          "length": 0,
          "precision": 0,
          "scale": 0,
          "nullable": false
        }
      ]
    },
    "data": [
      [
        "row1 col1",
        "row1 col2"
      ],
      [
        "row2 col1",
        "row2 col2"
      ]
    ]
  },
  "title": "Revenue by Month"
}
```

## `response.chart`

An event streamed when a chart content block is added.

| Field | Type | Description |
| --- | --- | --- |
| `content_index` | integer | The index in the response content array this event represents |
| `tool_use_id` | string | The ID of the tool use that generated this chart |
| `chart_spec` | string | The vega-lite chart specification serialized as a string |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "content_index": 0,
  "tool_use_id": "toolu_123",
  "chart_spec": "{\"$schema\":\"https://vega.github.io/schema/vega-lite/v5.json\",\"data\":{...},\"mark\":\"bar\"}"
}
```

## `response.status`

Status update for the agent execution.

| Field | Type | Description |
| --- | --- | --- |
| `status` | string | Enum for the current state. |
| `message` | string | A more descriptive message expanding on the current status. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "status": "executing_tool",
  "message": "Executing tool `my_analyst_tool`"
}
```

## `response.warning`

Sent when a non-fatal warning occurs. The stream continues after this event.

| Field | Type | Description |
| --- | --- | --- |
| `message` | string | The warning message to display to the user. |
| `code` | string | Optional structured warning code for clients to parse and handle. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "message": "Unable to fetch tools from MCP server 'foo'. Response quality may be degraded.",
  "code": "003001"
}
```

## `error`

Sent when a fatal error is encountered.

| Field | Type | Description |
| --- | --- | --- |
| `code` | string | The Snowflake error code |
| `error_code` | string | Error code, same as `code` above. This property has been deprecated and will be removed in a future release, but is temporarily supported for short-term backward compatibility. |
| `message` | string | The error message |
| `request_id` | string | The unique identifier for this request |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "code": "399504",
  "error_code": "lorem ipsum",
  "message": "Error during execution",
  "request_id": "61987ff6-6d56-4695-83c0-1e7cfed818c7"
}
```

## `metadata`

Metadata about the request. This event is sent when a message is added to the thread. It is useful for getting the `parent_message_id` to use in following requests to the Agents API.

| Field | Type | Description |
| --- | --- | --- |
| `metadata` | [Metadata](#label-snowflake-agent-run-metadata) |  |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "metadata": {
    "role": "user",
    "message_id": 83472,
    "run_id": "4264-83472"
  }
}
```

## Stream Agent Run

`GET /api/v2/cortex/agent/runs/{run_id}`

Connect to an Agent Run and stream its output. The Server-Sent Events returned match exactly
the events returned by the streaming `agent:run` API.

If the `starting_after` query parameter is not provided, all events are returned. If provided,
only events with a greater sequence number are returned (non-inclusive).

The events of an Agent Run are accessible via this endpoint while the run is active and for up
to 5 minutes after it completes. After that, connecting to a previously completed run returns a
409 Conflict, in which case the full agent response can be retrieved from a thread.

### Path parameters

| Parameter | Description |
| --- | --- |
| `run_id` | (Required) The Agent Run ID. Used to identify async runs. In the format {thread\_id}-{user\_message\_id}. |

Expand

Show lessSee more

### Query parameters

| Parameter | Description |
| --- | --- |
| `starting_after` | (Optional) The sequence number offset to start streaming from (non-inclusive). If not provided the entire output will be streamed. |

Expand

Show lessSee more

### Response

A stream of Server-Sent Events (`text/event-stream`). The events are identical to those
returned by the streaming `agent:run` API.

## Cancel Agent Run

`POST /api/v2/cortex/agent/runs/{run_id}/cancel`

Cancel an actively running Agent Run. Any partial output from the run will be saved
to the thread and billed accordingly.

Returns a `CancelAgentRunResponse` object. If partial output was saved to the thread,
`metadata.assistant_message_id` will be present and can be used as the `parent_message_id`
for follow-up requests to continue the conversation.

If the run has already completed or been canceled, returns 409 Conflict.

### Path parameters

| Parameter | Description |
| --- | --- |
| `run_id` | (Required) The Agent Run ID. Used to identify async runs. In the format {thread\_id}-{user\_message\_id}. |

Expand

Show lessSee more

### Response

Run successfully canceled. Returns metadata about the canceled run.

| Field | Type | Description |
| --- | --- | --- |
| `metadata` | [ResponseMetadata](#label-snowflake-agent-run-responsemetadata) | Metadata about the canceled run, including usage and message IDs. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "metadata": {
    "usage": {
      "tokens_consumed": [
        {
          "model_name": "llama3.1-70b",
          "input_tokens": {
            "total": 175,
            "cache_read": 50,
            "cache_write": 25,
            "uncached": 100
          },
          "output_tokens": {
            "total": 75
          },
          "context_window": 128000
        }
      ]
    },
    "run_id": "4264-83472",
    "thread_id": 4264,
    "user_message_id": 83472,
    "assistant_message_id": 83473
  }
}
```

## Schemas

# `AgentInstructions`

| Field | Type | Description |
| --- | --- | --- |
| `response` | string | Instructions for response generation. |
| `orchestration` | string | These custom instructions are used when the agent is planning which tools to use. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "response": "You will respond in a friendly but concise manner",
  "orchestration": "For any query related to revenue we should use Analyst; For all policy questions we should use Search"
}
```

## `Annotation`

> cortex\_search\_citation
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `type` | string | The citation type (always `cortex_search_citation`) |
> | `index` | integer | The index of the citation in the search results. |
> | `search_result_id` | string | The unique identifier for the search result. |
> | `doc_id` | string | The unique identifier for the document. |
> | `doc_title` | string | The title of the document. |
> | `text` | string | The text excerpt from the document used as the citation. |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "type": "cortex_search_citation",
>   "index": 0,
>   "search_result_id": "cs_61987ff6-6d56-4695-83c0-1e7cfed818c7",
>   "doc_id": "4ac085cb-82d0-4eb4-94f3-2672aa0599a2",
>   "doc_title": "Earnings Report",
>   "text": "The revenue for 2025 was..."
> }
> ```

## `BudgetConfig`

| Field | Type | Description |
| --- | --- | --- |
| `seconds` | integer | Time budget in seconds. |
| `tokens` | integer | Token budget. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "seconds": 30,
  "tokens": 16000
}
```

## `ChartContent`

| Field | Type | Description |
| --- | --- | --- |
| `tool_use_id` | string | The ID of the tool use that generated this chart |
| `chart_spec` | string | The vega-lite chart specification serialized as a string |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "tool_use_id": "toolu_123",
  "chart_spec": "{\"$schema\":\"https://vega.github.io/schema/vega-lite/v5.json\",\"data\":{...},\"mark\":\"bar\"}"
}
```

## `CortexAnalystSuggestionDelta`

| Field | Type | Description |
| --- | --- | --- |
| `index` | integer | The index of the suggestion array this delta represents |
| `delta` | string | The text delta for the suggestion in this index |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "index": 0,
  "delta": "What..."
}
```

## `CortexAnalystToolResultDelta`

| Field | Type | Description |
| --- | --- | --- |
| `text` | string | A text delta from Cortex Analyst’s final response. |
| `think` | string | A text delta from Cortex Analyst’s reasoning steps. |
| `sql` | string | A delta from Cortex Analyst’s SQL output. Currently, the entire SQL query comes in a single event but we may stream the SQL token-by-token in the future. |
| `sql_explanation` | string | A delta from Cortex Analyst’s explanation of what the SQL query does |
| `query_id` | string | The query id once SQL execution begins |
| `verified_query_used` | boolean | Whether a verified query was used to generate this response |
| `result_set` | [ResultSet](#label-snowflake-agent-run-resultset) | The results from SQL execution. Matches the schema from Snowflake’s SQL API ResultSet (<https://docs.snowflake.com/en/developer-guide/sql-api/reference#resultset>) |
| `suggestions` | [CortexAnalystSuggestionDelta](#label-snowflake-agent-run-cortexanalystsuggestiondelta) | A delta from Cortex Analyst’s suggested questions. This is sent when Analyst cannot answer the question due to missing information or other failures. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "text": "The...",
  "think": "Thinking...",
  "sql": "SELECT...",
  "sql_explanation": "This...",
  "query_id": "707787a0-a684-4ead-adb0-3c3b62b043d9",
  "verified_query_used": false,
  "result_set": {
    "statementHandle": "707787a0-a684-4ead-adb0-3c3b62b043d9",
    "resultSetMetaData": {
      "partition": 0,
      "numRows": 0,
      "format": "jsonv2",
      "rowType": [
        {
          "name": "my_column",
          "type": "VARCHAR",
          "length": 0,
          "precision": 0,
          "scale": 0,
          "nullable": false
        }
      ]
    },
    "data": [
      [
        "row1 col1",
        "row1 col2"
      ],
      [
        "row2 col1",
        "row2 col2"
      ]
    ]
  },
  "suggestions": {
    "index": 0,
    "delta": "What..."
  }
}
```

## `ExecutionEnvironment`

Configuration for server-executed tools.

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | The type of execution environment, currently only `warehouse` is supported. |
| `warehouse` | string | The name of the warehouse. Case-sensitive; if it is an unquoted identifier, provide the name in all-caps. If not specified, the user’s default warehouse is used. |
| `query_timeout` | integer | The query timeout in seconds |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "type": "warehouse",
  "warehouse": "MY_WAREHOUSE",
  "query_timeout": 60
}
```

## `InputTokens`

Input token breakdown by cache usage.

| Field | Type | Description |
| --- | --- | --- |
| `total` | integer | Total input tokens processed (including cached tokens). |
| `cache_read` | integer | Input tokens read from cache. |
| `cache_write` | integer | Input tokens written to cache. |
| `uncached` | integer | Input tokens that were not cached. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "total": 175,
  "cache_read": 50,
  "cache_write": 25,
  "uncached": 100
}
```

## `Message`

Represents a single message in the conversation. Can be from the user, assistant, or a control message.

| Field | Type | Description |
| --- | --- | --- |
| `role` | string | Identifies the message role. |
| `content` | array of [MessageContentItem](#label-snowflake-agent-run-messagecontentitem) | Array of content elements making up the message. Can include text, tool results, or custom content types. |
| `status` | string | The completion status of the message set by the server when saving to a thread. Set to “error” when the agent run terminated with an error; in that case the `error` field contains the error details. |
| `error` | [MessageError](#label-snowflake-agent-run-messageerror) | Details about the error that terminated the agent run. Only set when `status` is “error”. |

Expand

Show lessSee more

**Example**

Copy code

```
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
```

## `MessageContentItem`

> chartpermission\_decisiontabletextthinkingtool\_resulttool\_use
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `type` | string | The content type (always `chart`). |
> | `chart` | [ChartContent](#label-snowflake-agent-run-chartcontent) | The chart. |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "type": "chart",
>   "chart": {
>     "tool_use_id": "toolu_123",
>     "chart_spec": "{\"$schema\":\"https://vega.github.io/schema/vega-lite/v5.json\",\"data\":{...},\"mark\":\"bar\"}"
>   }
> }
> ```
>
> A user’s decision to grant or deny permission for a tool execution that had permission options. Sent by the client in the next request after receiving a tool\_use event with non-empty permission options.
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `type` | string | Content type identifier. |
> | `permission_decision` | [PermissionDecision](#label-snowflake-agent-run-permissiondecision) |  |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "type": "permission_decision",
>   "permission_decision": {
>     "tool_use_id": "toolu_abc123",
>     "decision": "Allow Once",
>     "reason": "I don't want to modify production config files"
>   }
> }
> ```
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `type` | string | The content type (always `table`). |
> | `table` | [TableContent](#label-snowflake-agent-run-tablecontent) | The table. |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "type": "table",
>   "table": {
>     "tool_use_id": "toolu_123",
>     "query_id": "6ac75378-6337-48a6-80ab-6de48dd680eb",
>     "result_set": {
>       "statementHandle": "707787a0-a684-4ead-adb0-3c3b62b043d9",
>       "resultSetMetaData": {
>         "partition": 0,
>         "numRows": 0,
>         "format": "jsonv2",
>         "rowType": [
>           {
>             "name": "my_column",
>             "type": "VARCHAR",
>             "length": 0,
>             "precision": 0,
>             "scale": 0,
>             "nullable": false
>           }
>         ]
>       },
>       "data": [
>         [
>           "row1 col1",
>           "row1 col2"
>         ],
>         [
>           "row2 col1",
>           "row2 col2"
>         ]
>       ]
>     },
>     "title": "Revenue by Month"
>   }
> }
> ```
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `text` | string | A text result from the agent |
> | `annotations` | array of [Annotation](#label-snowflake-agent-run-annotation) | Any annotations attached to the text result (e.g. citations) |
> | `is_elicitation` | boolean | Whether this text content is the agent asking for more information from the end user. |
> | `type` | string | The content type (always `text`). |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "text": "Lorem ipsum dolor...",
>   "annotations": [
>     {
>       "type": "cortex_search_citation",
>       "index": 0,
>       "search_result_id": "cs_61987ff6-6d56-4695-83c0-1e7cfed818c7",
>       "doc_id": "4ac085cb-82d0-4eb4-94f3-2672aa0599a2",
>       "doc_title": "Earnings Report",
>       "text": "The revenue for 2025 was..."
>     }
>   ],
>   "is_elicitation": false,
>   "type": "text"
> }
> ```
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `type` | string | The content type (always `thinking`). |
> | `thinking` | [ThinkingContent](#label-snowflake-agent-run-thinkingcontent) | The thinking content. |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "type": "thinking",
>   "thinking": {
>     "text": "To answer your question I must...",
>     "signature": "lorem ipsum"
>   }
> }
> ```
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `type` | string | The content type (always `tool_result`). |
> | `tool_result` | [ToolResult](#label-snowflake-agent-run-toolresult) | The tool result. |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "type": "tool_result",
>   "tool_result": {
>     "tool_use_id": "toolu_123",
>     "type": "cortex_analyst_text_to_sql",
>     "name": "my_cortex_analyst_semantic_view",
>     "content": [
>       {
>         "type": "json",
>         "json": {
>           "answer": 42
>         }
>       }
>     ],
>     "status": "success"
>   }
> }
> ```
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `type` | string | The content type (always `tool_use`). |
> | `tool_use` | [ToolUse](#label-snowflake-agent-run-tooluse) | The tool use. |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "type": "tool_use",
>   "tool_use": {
>     "tool_use_id": "toolu_123",
>     "type": "cortex_analyst_text_to_sql",
>     "name": "my_cortex_analyst_semantic_view",
>     "input": {
>       "location": "San Francisco, CA"
>     },
>     "client_side_execute": "true",
>     "permission": {
>       "options": [
>         "Allow Once",
>         "Deny"
>       ]
>     }
>   }
> }
> ```

## `MessageError`

Error details associated with a message that terminated with an error.

| Field | Type | Description |
| --- | --- | --- |
| `code` | string | The Snowflake error code. |
| `message` | string | The error message. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "code": "399504",
  "message": "Error during execution"
}
```

## `Metadata`

| Field | Type | Description |
| --- | --- | --- |
| `role` | string | Identifies the message role. |
| `message_id` | integer | The thread message id. Use this ID (when role is `assistant`) to ask a followup question on the thread. |
| `run_id` | string | The unique identifier for this Agent Run. Can be used to reconnect to the output stream. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "role": "user",
  "message_id": 83472,
  "run_id": "4264-83472"
}
```

## `ModelConfig`

| Field | Type | Description |
| --- | --- | --- |
| `orchestration` | string | Model to use for orchestration. If not provided, a model is automatically selected. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "orchestration": "claude-4-sonnet"
}
```

## `OrchestrationConfig`

| Field | Type | Description |
| --- | --- | --- |
| `budget` | [BudgetConfig](#label-snowflake-agent-run-budgetconfig) | Budget constraints for the agent. If more than one constraint is specified, whichever is first hit will end the request. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "budget": {
    "seconds": 30,
    "tokens": 16000
  }
}
```

## `OutputTokens`

Output token details.

| Field | Type | Description |
| --- | --- | --- |
| `total` | integer | Total output tokens generated. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "total": 75
}
```

## `PermissionDecision`

Contains the user’s decision on whether to allow a specific tool execution. The decision field must match one of the options from the tool\_use event’s permission.options list (e.g. “Allow Once” to approve, “Deny” to deny). If denied, an optional reason can be provided which will be shown to the LLM.

| Field | Type | Description |
| --- | --- | --- |
| `tool_use_id` | string | The ID of the tool\_use this decision applies to. |
| `decision` | string | Must match one of the options from the tool\_use permission.options list. |
| `reason` | string | Optional reason for denying permission. Only meaningful when decision is “Deny”. This reason will be shown to the LLM as an error message so it can respond appropriately. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "tool_use_id": "toolu_abc123",
  "decision": "Allow Once",
  "reason": "I don't want to modify production config files"
}
```

## `ResponseMetadata`

Metadata about the response, including usage information.

| Field | Type | Description |
| --- | --- | --- |
| `usage` | [UsageMetadata](#label-snowflake-agent-run-usagemetadata) |  |
| `run_id` | string | The unique identifier for this Agent Run. Can be used to reconnect to the output stream. |
| `thread_id` | integer | The Thead ID, if using a thread. |
| `user_message_id` | integer | If using a Thread, this is the message ID of the user question sent in this request. The `assistant_message_id` is a child of this message. |
| `assistant_message_id` | integer | If using a Thread, this is the message ID of this assistant response. Use this value as the `parent_message_id` in followup requests. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "usage": {
    "tokens_consumed": [
      {
        "model_name": "llama3.1-70b",
        "input_tokens": {
          "total": 175,
          "cache_read": 50,
          "cache_write": 25,
          "uncached": 100
        },
        "output_tokens": {
          "total": 75
        },
        "context_window": 128000
      }
    ]
  },
  "run_id": "4264-83472",
  "thread_id": 4264,
  "user_message_id": 83472,
  "assistant_message_id": 83473
}
```

## `ResultSet`

| Field | Type | Description |
| --- | --- | --- |
| `statementHandle` | string | The query id. |
| `resultSetMetaData` | [ResultSetMetaData](#label-snowflake-agent-run-resultsetmetadata) | Metadata on the result set. |
| `data` | array of array | 2D array representing the data |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "statementHandle": "707787a0-a684-4ead-adb0-3c3b62b043d9",
  "resultSetMetaData": {
    "partition": 0,
    "numRows": 0,
    "format": "jsonv2",
    "rowType": [
      {
        "name": "my_column",
        "type": "VARCHAR",
        "length": 0,
        "precision": 0,
        "scale": 0,
        "nullable": false
      }
    ]
  },
  "data": [
    [
      "row1 col1",
      "row1 col2"
    ],
    [
      "row2 col1",
      "row2 col2"
    ]
  ]
}
```

## `ResultSetMetaData`

| Field | Type | Description |
| --- | --- | --- |
| `partition` | integer | The index number of the partition. |
| `numRows` | integer | The total number of rows of results. |
| `format` | string | Format of the data in the result set. |
| `rowType` | array of [RowType](#label-snowflake-agent-run-rowtype) | Description of the columns in the result. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "partition": 0,
  "numRows": 0,
  "format": "jsonv2",
  "rowType": [
    {
      "name": "my_column",
      "type": "VARCHAR",
      "length": 0,
      "precision": 0,
      "scale": 0,
      "nullable": false
    }
  ]
}
```

## `RowType`

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Name of the column. |
| `type` | string | Snowflake data type of the column. (<https://docs.snowflake.com/en/sql-reference/intro-summary-data-types>) |
| `length` | integer | Length of the column. |
| `precision` | integer | Precision of the column. |
| `scale` | integer | Scale of the column. |
| `nullable` | boolean | Specifies whether or not the column is nullable. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "name": "my_column",
  "type": "VARCHAR",
  "length": 0,
  "precision": 0,
  "scale": 0,
  "nullable": false
}
```

## `TableContent`

| Field | Type | Description |
| --- | --- | --- |
| `tool_use_id` | string | The ID of the tool use that generated this table |
| `query_id` | string | The query id of the sql query that generated this data |
| `result_set` | [ResultSet](#label-snowflake-agent-run-resultset) | The SQL results to render a table. Matches the schema from Snowflake’s SQL API ResultSet (<https://docs.snowflake.com/en/developer-guide/sql-api/reference#resultset>) |
| `title` | string | The title for this table |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "tool_use_id": "toolu_123",
  "query_id": "6ac75378-6337-48a6-80ab-6de48dd680eb",
  "result_set": {
    "statementHandle": "707787a0-a684-4ead-adb0-3c3b62b043d9",
    "resultSetMetaData": {
      "partition": 0,
      "numRows": 0,
      "format": "jsonv2",
      "rowType": [
        {
          "name": "my_column",
          "type": "VARCHAR",
          "length": 0,
          "precision": 0,
          "scale": 0,
          "nullable": false
        }
      ]
    },
    "data": [
      [
        "row1 col1",
        "row1 col2"
      ],
      [
        "row2 col1",
        "row2 col2"
      ]
    ]
  },
  "title": "Revenue by Month"
}
```

## `ThinkingContent`

| Field | Type | Description |
| --- | --- | --- |
| `text` | string | Thinking tokens from the agent |
| `signature` | string | The signature of the thinking token |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "text": "To answer your question I must...",
  "signature": "lorem ipsum"
}
```

## `TokensConsumed`

Token consumption for a specific model.

| Field | Type | Description |
| --- | --- | --- |
| `model_name` | string | Name of the model used. |
| `input_tokens` | [InputTokens](#label-snowflake-agent-run-inputtokens) |  |
| `output_tokens` | [OutputTokens](#label-snowflake-agent-run-outputtokens) |  |
| `context_window` | integer | The model’s context window size (in tokens). |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "model_name": "llama3.1-70b",
  "input_tokens": {
    "total": 175,
    "cache_read": 50,
    "cache_write": 25,
    "uncached": 100
  },
  "output_tokens": {
    "total": 75
  },
  "context_window": 128000
}
```

## `Tool`

Defines a tool that can be used by the agent. Tools provide specific capabilities like data analysis, search, or generic functions.

| Field | Type | Description |
| --- | --- | --- |
| `tool_spec` | [ToolSpec](#label-snowflake-agent-run-toolspec) | Specification of the tool’s type, configuration, and input requirements. |

Expand

Show lessSee more

**Example**

Copy code

```
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
```

## `ToolChoice`

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | Determines how tools are selected: - auto - Automatic tool selection (default) - required - Must use at least one tool - tool - Use specific named tools |
| `name` | array of string | List of specific tool names to use when type is ‘tool’. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "type": "auto",
  "name": [
    "analyst_tool",
    "search_tool"
  ]
}
```

## `ToolInputSchema`

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | The type of the input schema object. |
| `description` | string | A description of what the input is. |
| `properties` | map of [ToolInputSchema](#label-snowflake-agent-run-toolinputschema) | If type is `object`, definitions of each input parameter. |
| `items` | [ToolInputSchema](#label-snowflake-agent-run-toolinputschema) | If type is `array`, the schema for the elements of the array. |
| `required` | array of string | If type is `object`, list of required input parameter names. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "type": "object",
  "description": "Input for my custom tool",
  "properties": {
    "location": {
      "type": "string",
      "description": "The city and state, e.g. San Francisco, CA"
    }
  },
  "items": {},
  "required": [
    "location"
  ]
}
```

## `ToolResource`

> cortex\_analyst\_text\_to\_sqlcortex\_searchgenericweb\_search
>
> Configuration for text-to-SQL analysis tool. Provides parameters for SQL query generation and execution. Exactly one of semantic\_model\_file or semantic\_view must be provided.
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `semantic_model_file` | string | The path to a file stored in a Snowflake Stage holding the semantic model yaml. |
> | `semantic_view` | string | The name of the Snowflake native semantic model object. |
> | `execution_environment` | [ExecutionEnvironment](#label-snowflake-agent-run-executionenvironment) | Configuration for how to execute the generated SQL query. |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "semantic_model_file": "@db.schema.stage/semantic_model.yaml",
>   "semantic_view": "db.schema.semantic_view",
>   "execution_environment": {
>     "type": "warehouse",
>     "warehouse": "MY_WAREHOUSE",
>     "query_timeout": 60
>   }
> }
> ```
>
> Configuration for search functionality. Defines how document search and retrieval should be performed.
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `search_service` | string | The fully qualified name of the search service. |
> | `title_column` | string | The title column of the document. |
> | `id_column` | string | The ID column of the document. |
> | `filter` | object | Filter query for search results. |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "search_service": "database.schema.service_name",
>   "title_column": "account_name",
>   "id_column": "account_id",
>   "filter": {
>     "@eq": {
>       "<column>": "<value>"
>     }
>   }
> }
> ```
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `type` | string | If the tool is server-side executed, whether it is a Stored Procedure or a UDF. |
> | `execution_environment` | [ExecutionEnvironment](#label-snowflake-agent-run-executionenvironment) |  |
> | `identifier` | string | Fully qualified name of the Stored Procedure or UDF. |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "type": "function",
>   "execution_environment": {
>     "type": "warehouse",
>     "warehouse": "MY_WAREHOUSE",
>     "query_timeout": 60
>   },
>   "identifier": "MY_DB.MY_SCHEMA.MY_UDF"
> }
> ```
>
> Configuration for web search functionality.
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `max_results` | integer | Max web search results returned. |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "max_results": 20
> }
> ```

## `ToolResult`

| Field | Type | Description |
| --- | --- | --- |
| `tool_use_id` | string | Unique identifier for this tool use. Can be used to associated tool results. |
| `type` | string | The type of the tool (e.g. cortex\_search, cortex\_analyst\_text\_to\_sql) |
| `name` | string | The unique identifier for this tool instance |
| `content` | array of [ToolResultContent](#label-snowflake-agent-run-toolresultcontent) | The content on the tool result |
| `status` | string | The status of tool execution |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "tool_use_id": "toolu_123",
  "type": "cortex_analyst_text_to_sql",
  "name": "my_cortex_analyst_semantic_view",
  "content": [
    {
      "type": "json",
      "json": {
        "answer": 42
      }
    }
  ],
  "status": "success"
}
```

## `ToolResultContent`

> jsontext
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `type` | string | The type of result (always `json`) |
> | `json` | object | Structured output from a tool. The schema varies depending on the tool type. |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "type": "json",
>   "json": {
>     "answer": 42
>   }
> }
> ```
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `type` | string | The type of result (always `text`) |
> | `text` | string | The result text |
>
> Expand
>
> Show lessSee more
>
> **Example**
>
> Copy code
>
> ```
> {
>   "type": "text",
>   "text": "The answer is 42"
> }
> ```

## `ToolSpec`

Specification of the tool’s type, configuration, and input requirements.

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | The type of tool capability. Can be specialized types like ‘cortex\_analyst\_text\_to\_sql’ or ‘generic’ for general-purpose tools. |
| `name` | string | Unique identifier for referencing this tool instance. Used to match with configuration in tool\_resources. |
| `description` | string | Description of the tool to be considered for tool use. |
| `input_schema` | [ToolInputSchema](#label-snowflake-agent-run-toolinputschema) | JSON Schema definition of the expected input parameters for this tool. This will be fed to the agent so it knows the structure it should follow for when generating the input for ToolUses. Required for generic tools to specify their input parameters. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "type": "generic",
  "name": "get_weather",
  "description": "lorem ipsum",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      }
    },
    "required": [
      "location"
    ]
  }
}
```

## `ToolUse`

| Field | Type | Description |
| --- | --- | --- |
| `tool_use_id` | string | Unique identifier for this tool use. Can be used to associated tool results. |
| `type` | string | The type of the tool (e.g. cortex\_search, cortex\_analyst\_text\_to\_sql) |
| `name` | string | The unique identifier for this tool instance |
| `input` | object | The structured input for this tool. The schema of this object should will vary depending on the tool spec. |
| `client_side_execute` | boolean | Whether the tool use is executed on the client side. |
| `permission` | [ToolUsePermission](#label-snowflake-agent-run-toolusepermission) |  |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "tool_use_id": "toolu_123",
  "type": "cortex_analyst_text_to_sql",
  "name": "my_cortex_analyst_semantic_view",
  "input": {
    "location": "San Francisco, CA"
  },
  "client_side_execute": "true",
  "permission": {
    "options": [
      "Allow Once",
      "Deny"
    ]
  }
}
```

## `ToolUsePermission`

Permission metadata for a tool use. A non-empty options list means the client must prompt the user for approval before the tool is executed.

| Field | Type | Description |
| --- | --- | --- |
| `options` | array of string | The complete set of valid options the user may choose from, including “Deny” to deny permission. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "options": [
    "Allow Once",
    "Deny"
  ]
}
```

## `UsageMetadata`

Usage information for this request.

| Field | Type | Description |
| --- | --- | --- |
| `tokens_consumed` | array of [TokensConsumed](#label-snowflake-agent-run-tokensconsumed) | Token consumption details per model used in this request. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "tokens_consumed": [
    {
      "model_name": "llama3.1-70b",
      "input_tokens": {
        "total": 175,
        "cache_read": 50,
        "cache_write": 25,
        "uncached": 100
      },
      "output_tokens": {
        "total": 75
      },
      "context_window": 128000
    }
  ]
}
```

## `Warning`

| Field | Type | Description |
| --- | --- | --- |
| `message` | string | The warning message to display to the user. |
| `code` | string | Optional structured warning code for clients to parse and handle. |

Expand

Show lessSee more

**Example**

Copy code

```
{
  "message": "Unable to fetch tools from MCP server 'foo'. Response quality may be degraded.",
  "code": "003001"
}
```

## Non-streaming response (stream: false)

To receive a **single non-streaming JSON response**, set `stream` to `false` in the request body and set the request `Accept` header to `application/json`.

The response body is the same object as the `response` event payload in streaming mode (that is, it corresponds to the JSON returned in the SSE `response` event’s `data` field).

If non-fatal warnings occur during the run, the response includes a top-level `warnings` array. For example, warning code `399569` indicates that the caller’s role couldn’t access a named tool and the agent produced an answer with its remaining tools.

**Example response**

Copy code

```
{
  "role": "assistant",
  "content": [
    {
      "thinking": {
        "text": "\nThe user is asking about types of products...\n"
      },
      "type": "thinking"
    },
    {
      "tool_use": {
        "client_side_execute": false,
        "input": {
          "sql": "WITH __table_a AS (...) SELECT ...",
          "execution_environment": {
            "type": "warehouse",
            "warehouse": "my_warehouse"
          }
        },
        "name": "system_execute_sql",
        "tool_use_id": "<tool_use_id>",
        "type": "system_execute_sql"
      },
      "type": "tool_use"
    },
    {
      "tool_result": {
        "content": [
          {
            "json": {
              "query_id": "<query_id>",
              "result_set": {
                "data": [
                  ["Electronics", "3", "3"],
                  ["Furniture", "2", "2"]
                ],
                "resultSetMetaData": {
                  "format": "jsonv2",
                  "numRows": 2,
                  "partition": 0
                },
                "statementHandle": "<statement_handle>"
              },
              "sql": "WITH __table_a AS (...) SELECT ..."
            },
            "type": "json"
          }
        ],
        "name": "system_execute_sql",
        "status": "success",
        "tool_use_id": "<tool_use_id>",
        "type": "system_execute_sql"
      },
      "type": "tool_result"
    },
    {
      "text": "Based on the data available, there are 2 main types of products...",
      "type": "text"
    }
  ],
  "warnings": [
    {
      "code": "399569",
      "message": "TOOL_NOT_ACCESSIBLE: Search1 (cortex_search) - The Cortex Search Service does not exist or access is not authorized for the current role: db.schema.css1"
    }
  ]
}
```
