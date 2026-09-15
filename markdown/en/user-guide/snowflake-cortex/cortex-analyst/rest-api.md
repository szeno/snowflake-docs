# Cortex Analyst REST API

Transition to Cortex Agents

Snowflake recommends transitioning to [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents), which supports every Cortex Analyst capability with higher answer quality.

Use this API to answer questions about your data with natural language queries.

## Send message

`POST /api/v2/cortex/analyst/message`

Generates a SQL query for the given question using a semantic model or [semantic view](/user-guide/views-semantic/overview)
provided in the request. One or more models can be specified; when multiple models are specified, Cortex Analyst chooses the most appropriate one.
You can have multi-turn conversations where you can ask follow-up questions that build upon previous queries. For more information, see [Multi-turn conversation in Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst#label-analyst-multi-turn-conversation).

The request includes a user question; the response includes the user question and the analyst response. Each message in a response
can have multiple content blocks of different types. Three values that are currently supported for the `type` field of the content
object are: `text`, `suggestions`, and `sql`.

Responses can be sent all at once after processing is complete, or incrementally as they are generated.

### Request headers

| Header | Description |
| --- | --- |
| `Authorization` | (Required) Authorization token. For more information, see [Authenticating to the server](/developer-guide/sql-api/authenticating). |
| `Content-Type` | (Required) application/json |
| `X-Snowflake-Authorization-Token-Type` | (Optional) Authorization token type. Defaults to OAuth. For more information, see [Authenticating to the server](/developer-guide/sql-api/authenticating). |

Expand

Show lessSee more

### Request body

In the request body:

- Set the last `messages[].role` field to the role of the speaker, which must be `user`.
- Include the user’s question in the `content` object. In this object:

  - Set `type` to `text`.
  - Set `text` to the user’s question.
- Include one of the following:

  - The [YAML specification](/user-guide/views-semantic/semantic-view-yaml-spec) for a semantic view.
  - The path to the YAML file that contains the semantic view specification. This file must be on a stage.
  - The name of the semantic view.

The following table describes the fields that you can set in the body of the request:

| Field | Description |
| --- | --- |
| `messages[].role` | (Required) The role of the entity that is creating the message. Currently only supports `user`.  Type: string:enum  Example: `user` |
| `messages[].content[]` | (Required) The content object that is part of a message.  Type: object  Example:  Copy code  ``` {   "type": "text",   "text":  "Which company had the most revenue?" } ``` |
| `messages[].content[].type` | (Required) The content type. Currently only `text` is supported.  Type: string:enum  Example: `text` |
| `messages[].content[].text` | (Required) The user’s question.  Type: string  Example: `Which company had the most revenue?` |
| `semantic_model_file` | Path to the semantic model YAML file. Must be a fully qualified stage URL including the database and schema.  To specify multiple semantic models, use the `semantic_models` field.  If you want to provide the YAML specification directly in the request instead, set the `semantic_model` field to the YAML specification for the semantic model.  Type: string  Example: `@my_db.my_schema.my_stage/my_semantic_model.yaml` |
| `semantic_model` | A string containing the entire semantic model YAML.  To specify multiple semantic models, use the `semantic_models` field instead.  If you want to point to a YAML specification in a file instead, upload the file to a stage, and set the `semantic_model_file` field to the path to the file.  Type: string |
| `semantic_models` | An array containing JSON objects, each of which contains a `semantic_model_file` or `semantic_view` field.  These fields have the same semantics as the top-level `semantic_model_file` and `semantic_view` fields:   - `semantic_model_file` specifies a YAML file, stored in a stage, that contains a semantic model definition.   (You cannot specify the YAML for the semantic model directly in the request with this form.) - `semantic_view` specifies the fully qualified name of a [semantic view](/user-guide/views-semantic/overview).   For example:   Copy code  ``` {   /* ... */   "semantic_models": [     {"semantic_view": "my_db.my_sch.my_sem_view_1" },     {"semantic_view": "my_db.my_sch.my_sem_view_2" }   ]   /* ... */ } ```  For each query, Cortex Analyst chooses the most appropriate model or view from the list.  This capability simplifies user interactions with Cortex Analyst. You don’t need to choose a data source to query, and you don’t need to keep track of which semantic model or semantic view to use for each. Just specify all of your models or views with each query and let Cortex Analyst figure out which one to use.  Type: array  Tip  Cortex Analyst does not require that you specify more than one model or view. If you specify a single model or view, the request is functionally equivalent to one containing a top-level `semantic_model_file` or `semantic_view` field.  The advantage of using `semantic_models` for single-model requests is that you can use the same client code, regardless of the number of models or views. |
| `semantic_view` | Fully qualified name of the [semantic view](/user-guide/views-semantic/overview). For example:  Copy code  ``` {   /* ... */   "semantic_view": "MY_DB.MY_SCHEMA.SEMANTIC_VIEW"   /* ... */ } ```  If the name is case-sensitive or contains characters that are not allowed in an [unquoted identifier](/sql-reference/identifiers-syntax), you must enclose the name in backslash-escaped double quotes. For example, if the database name, schema name, and view name include hyphens (`my-database.my-schema.my-semantic-view`):  Copy code  ``` {   /* ... */   "semantic_view": "\"my-database\".\"my-schema\".\"\"my-semantic-view\"\""   /* ... */ } ```  To specify multiple semantic views, use the `semantic_models` field.  Type: string |
| `stream` | (Optional) If set to `true`, the response is streamed to the client using [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) as it is generated (see [Streaming response](#label-cortex-analyst-rest-api-streaming)). Otherwise the complete response is returned after Cortex Analyst has fully processed the user’s question.  Type: boolean |

Expand

Show lessSee more

Important

You must specify one of the following fields in the body of the request:

- `semantic_model_file`
- `semantic_model`
- `semantic_models`
- `semantic_view`

#### Example of specifying a semantic model in a file on a stage

Copy code

```
{
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "which company had the most revenue?"
                }
            ]
        }
    ],
    "semantic_model_file": "@my_db.my_schema.my_stage/my_semantic_model.yaml"
}
```

#### Example of specifying a semantic view

Copy code

```
{
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "which company had the most revenue?"
        }
      ]
    }
  ],
  "semantic_view": "MY_DB.MY_SCH.MY_SEMANTIC_VIEW"
}
```

### Non-streaming response

This operation can return the response codes listed below.
The response always has the following structure. Currently, three content types are supported for the
response, `text`, `suggestion`, and `sql`. The content types `suggestion` and `sql` are mutually exclusive so that if the
response contains a `sql` content type, it won’t contain a `suggestion` content type, and vice versa. The `suggestion` content type is only included
in a response if the user question was ambiguous and Cortex Analyst could not return a SQL statement for that query.

When the request contains a `semantic_models` field, the response includes a `semantic_model_selection` field that indicates
which semantic model was chosen for the request.

To ensure forward compatibility, make sure your implementation takes the content type into account and handles types.

| Code | Description |
| --- | --- |
| 200 | The statement was executed successfully.  The body of the response contains a message object that contains the following fields:   - `message`: Messages of the conversation between the user and analyst. - `message` (object): Represents a message within a chat. - `message.role` (string:enum): The entity that produced the message. One of `user` or `analyst`. - `message.content[]` (object): The content object that is part of a message. - `message.content[].type` (string:enum): The content type of the message. One of `text`, `suggestion`, or `sql`. - `message.content[].text` (string): The text of the content. Only returned for content type `text`. - `message.content[].statement` (string): A SQL statement. Only returned for content type `sql`. - `message.content[].confidence` (object): Contains confidence-related information. Only returned for the `sql` content type. - `message.content[].confidence.verified_query_used` (object): Represents the verified query from Verified Query Repository used in SQL response generation. If no verified query used, the field value is `null`. - `message.content[].confidence.verified_query_used.name` (string): The name of the verified query used, extracted from the Verified Query Repository. - `message.content[].confidence.verified_query_used.question` (string): The question that is answered by the verified query, extracted from the Verified Query Repository. - `message.content[].confidence.verified_query_used.sql` (string): The SQL statement of the verified query used, extracted from the Verified Query Repository. - `message.content[].confidence.verified_query_used.verified_at` (integer): The numeric representation of the timestamp when the query is verified, extracted from the Verified Query Repository. - `message.content[].confidence.verified_query_used.verified_by` (string): The person who verified the query, extracted from the Verified Query Repository. - `message.content[].suggestions` (string): If SQL cannot be generated, a list of questions the semantic model can   generate SQL for. Only returned for content type `suggestion`. - `warnings`: List of warnings from the analyst about the user’s request. - `warnings[].message` (string): Contains a detailed description of one individual warning. - `response_metadata` (object): Metadata containing response generation details. - `response_metadata.model_names`: List of models used to generate response. - `response_metadata.cortex_search_retrieval` (object): Entities resolved with cortex search. - `response_metadata.question_category` (string): How the question in the request is categorized. |

Expand

Show lessSee more

By default, the response is returned all at once after Cortex Analyst has fully processed the user’s question. See [Streaming response](#label-cortex-analyst-rest-api-streaming)
for the format of streaming mode responses.

> Copy code
>
> ```
> {
>     "request_id": "75d343ee-699c-483f-83a1-e314609fb563",
>     "message": {
>         "role": "analyst",
>         "content": [
>             {
>                 "type": "text",
>                 "text": "We interpreted your question as ..."
>             },
>             {
>                 "type": "sql",
>                 "statement": "SELECT * FROM table",
>                 "confidence": {
>                     "verified_query_used": {
>                         "name": "My verified query",
>                         "question": "What was the total revenue?",
>                         "sql": "SELECT * FROM table2",
>                         "verified_at": 1714497970,
>                         "verified_by": "Jane Doe"
>                     }
>                 }
>             }
>         ]
>     },
>     "warnings": [
>         {
>             "message": "Table table1 has (30) columns, which exceeds the recommended maximum of 10"
>         },
>         {
>             "message": "Table table2 has (40) columns, which exceeds the recommended maximum of 10"
>         }
>     ],
>     "response_metadata": {
>         "model_names": [
>             "claude-sonnet-4-5"
>         ],
>         "cortex_search_retrieval": [
>             {
>                 "service": "my_db.my_schema.my_search_service",
>                 "response_body": {
>                     "results": [
>                         {
>                             "CUST_NAME": "customer1"
>                         }
>                     ],
>                     "request_id": "request1"
>                 },
>                 "query": "'customer1'"
>             }
>         ],
>         "question_category": "CLEAR_SQL"
>     }
> }
> ```

### Streaming response

Streaming mode lets your client receive responses as they are generated by Cortex Analyst, rather than waiting for the entire response to be generated.
This improves the perceived responsiveness of your application, especially for long-running queries, because users begin seeing output much sooner.
Streaming responses also provide status information that can help you understand where Cortex Analyst is in the process of generating a response, and
warnings that can help you understand what went wrong when Cortex Analyst doesn’t work as you expected.

To receive a streaming response, set the `stream` field in the request body to `true`.
Streaming responses use [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events).

Cortex Analyst sends six distinct types of events in a streaming response:

- `status`: Conveys status updates about the SQL generation process.
- `message.content.delta`: Contains a piece of the response. This event is sent multiple times.
- `error`: Indicates that Cortex Analyst has encountered an error and cannot continue processing the request. No further `message.content.delta` events will be sent.
- `warnings`: Contains any warnings encountered during processing. Warnings do not stop processing.
- `response_metadata`: Sent at the end of a response to display data about request processing.
- `done`: Sent to indicate that processing is complete and no further `message.content.delta` events will be sent.

Of these, the `message.content.delta` events are the most crucial to understand, because they contain the actual
response content. Each `delta` contains tokens from some field in the complete response. It is possible for each
`delta` event to contain anywhere from a single character to the full response, and they may be of different lengths. You receive these tokens as they
are generated; it is up to you to assemble them into the final response.

Important

Events from different responses (even extremely similar ones) can vary. There is no guarantee that events will be sent in the same order or with the same content.

#### Simple example

The following is a sample non-streaming response for a simple query:

Copy code

```
{
    "message": {
        "role": "analyst",
        "content": [
            {
                "type": "text",
                "text": "This is how we interpreted your question and this is how the sql is generated"
            },
            {
                "type": "sql",
                "statement": "SELECT * FROM table"
            }
        ]
    }
}
```

And this is one possible series of streaming events for that response (a different series of events is also possible):

```
event: status
data: { status: "interpreting_question" }

event: message.content.delta
data: {
  index: 0,
  type: "text",
  text_delta: "This is how we interpreted your question"
}

event: status
data: { status: "generating_sql" }

event: status
data: { status: "validating_sql" }

event: message.content.delta
data: {
  index: 0,
  type: "text",
  text_delta: " and this is how the sql is generated"
}

event: message.content.delta
data: {
  index: 1,
  type: "sql",
  statement_delta: "SELECT * FROM table"
}

event: status
data: { status: "done" }
```

Use the `index` field in the `message.content.delta` responses to determine which field in the full response the event is part of.
For example, here the first two `delta` events use index 0, which means they are part of the first field (element 0) in the `content` array
of the non-streaming response. Similarly, the `delta` event that contains the SQL response uses index 1.

#### Example with suggestions

This example contains suggested questions for an ambiguous question. The following is the non-streaming response:

Copy code

```
{
    "message": {
        "role": "analyst",
        "content": [
            {
                "type": "text",
                "text": "Your question is ambiguous, here are some alternatives:"
            },
            {
                "type": "suggestions",
                "suggestions": [
                    "which company had the most revenue?",
                    "which company placed the most orders?"
                ]
            }
        ]
    }
}
```

And here is a possible series of streaming events that constitute that response:

```
event: status
data: { status: "interpreting_question" }

event: message.content.delta
data: {
  index: 0,
  type: "text",
  text_delta: "Your question is ambiguous,"
}

event: status
data: { status: "generating_suggestions" }

event: message.content.delta
data: {
  index: 0,
  type: "text",
  text_delta: " here are some alternatives:"
}

event: message.content.delta
data: {
  index: 1,
  type: "suggestions",
  suggestions_delta: {
    index: 0,
    suggestion_delta: "which company had",
  }
}

event: message.content.delta
data: {
  index: 1,
  type: "suggestions",
  suggestions_delta: {
    index: 0,
    suggestion_delta: " the most revenue?",
  }
}

event: message.content.delta
data: {
  index: 1,
  type: "suggestions",
  suggestions_delta: {
    index: 1,
    suggestion_delta: "which company placed",
  }
}

event: message.content.delta
data: {
  index: 1,
  type: "suggestions",
  suggestions_delta: {
    index: 1,
    suggestion_delta: " the most orders?",
  }
}

event: status
data: { status: "done" }
```

In this example, the `content` field of the non-streaming response is an array. One of the elements of `content` is the `suggestions` array.
So the meaning of `index` fields for `text` and `suggestions` delta events refer to the location of elements in these two different arrays.
You will need to keep track of these indexes separately when assembling the full response.

Note

Currently, the generated SQL statement is always sent in a single event. This may not be the case in the future. Your client must be prepared to
receive the SQL statement in multiple events.

#### Other examples

You can find a Streamlit streaming client for Cortex Analyst in the Cortex Analyst
[GitHub repo](https://github.com/Snowflake-Labs/sfguide-getting-started-with-cortex-analyst/blob/main/cortex_analyst_streaming_demo.py).
This demo must be run locally; SiS does not currently support streaming.

See the Cortex Analyst playground in the AI/ML Studio (in Snowsight) for an interactive demonstration of streaming response.

### Streaming event schemas

The following are the OpenAPI/Swagger schemas of the events sent by Cortex Analyst in a streaming response.

status

message.content.delta

error
:   Copy code

    ```
    StreamingError:
    type: object
    properties:
      message:
        type: string
        description: A description of the error
      code:
        type: string
        description: The Snowflake error code categorizing the error
      request_id:
        type: string
        description: Unique request ID
    ```

warnings
:   Copy code

    ```
    Warnings:
    type: object
    description: Warnings found while processing the request
    properties:
      warnings:
        type: array
        items:
          $ref: "#/components/schemas/Warning"
    Warning:
    type: object
    title: The warning object
    description: Represents a warning within a chat.
    properties:
      message:
        type: string
        description: A human-readable message describing the warning
    ```

response\_metadata
:   Copy code

    ```
    ResponseMetadata:
    type: object
    description: Details about request processing
    ```

## Send feedback

`POST /api/v2/cortex/analyst/feedback`

Provides qualitative end-user feedback. Within Snowsight, the feedback is shown in **Snowsight → AI & ML → Cortex Analyst → Select Semantic View → Monitoring tab**.

### Request headers

| Header | Description |
| --- | --- |
| `Authorization` | (Required) Authorization token. For more information, see [Authenticating to the server](/developer-guide/sql-api/authenticating). |
| `Content-Type` | (Required) application/json |

Expand

Show lessSee more

### Request body

| Field | Description |
| --- | --- |
| `request_id` | (Required) The id of the request that you’ve made to send a message. Returned in the `request_id` field of `/api/v2/cortex/analyst/message`. For more information, see [Non-streaming response](#label-cortex-analyst-rest-api-response).  Type: string  Example: `75d343ee-699c-483f-83a1-e314609fb563` |
| `positive` | (Required) Whether the feedback is positive or negative. `true` for positive or “thumbs up”, `false` for negative or “thumbs down”.  Type: boolean  Example:  `true` |
| `feedback_message` | (Optional) The feedback message from the user.  Example: `This is the best answer I've ever seen!` |

Expand

Show lessSee more

### Response

Empty response body with status code 200.

## Access control requirements

For information on the required privileges, see [Access control requirements](/user-guide/snowflake-cortex/cortex-analyst#label-analyst-access-control).

For details about authenticating to the API, see [Authenticating Snowflake REST APIs with Snowflake](/developer-guide/snowflake-rest-api/authentication).
