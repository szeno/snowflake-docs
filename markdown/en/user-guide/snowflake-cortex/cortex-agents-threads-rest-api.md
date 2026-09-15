# Threads API

Use this API to create threads that are used to interact with Cortex Agents.

## Create thread

`POST /api/v2/cortex/threads`

Creates a new thread and returns a thread metadata object.

### Request

#### Request headers

| Header | Description |
| --- | --- |
| `Authorization` | (Required) Authorization token. For more information, see [Authentication](/user-guide/snowflake-cortex/cortex-agents-setup#label-chat-api-authenticate-example). |
| `Content-Type` | (Required) application/json |

Expand

Show lessSee more

#### Request body

The request body can include the following field:

| Field | Type | Description |
| --- | --- | --- |
| `origin_application` | string | (Optional) Name of the application that created the thread. Allows grouping threads by application. Limited to 16 bytes. |

Expand

Show lessSee more

Example:

Copy code

```
{
  "origin_application": "my_app"
}
```

### Response

Returns a thread metadata object.

| Field | Type | Description |
| --- | --- | --- |
| `thread_id` | integer | UUID for the thread. |
| `thread_name` | string | Name of the thread. |
| `origin_application` | string | The name of the application that created the thread. |
| `created_on` | integer | Time when the thread was created (milliseconds since UNIX epoch). |
| `updated_on` | integer | Time when the thread was last updated (milliseconds since UNIX epoch). |

Expand

Show lessSee more

Example:

Copy code

```
{
  "thread_id": 1234567890,
  "thread_name": "",
  "origin_application": "my_app",
  "created_on": 1717000000000,
  "updated_on": 1717000000000
}
```

## Describe thread

`GET /api/v2/cortex/threads/{id}`

Describes a thread and returns a batch of messages in that thread, based on the page\_size and the last\_message\_id, in descending order of creation. This request is only successful if the thread ID belongs to the user. To return only messages of a particular type, use the `message_type` query parameter.

### Request

#### Path parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | integer | (Required) UUID for the thread. |

Expand

Show lessSee more

#### Query parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `page_size` | integer | (Optional) Number of messages to return (default: 20, max: 100). |
| `last_message_id` | integer | (Optional) The ID of the last message received. Used to set the offset for next batch. Can be empty for the first batch of messages. |
| `message_type` | string | (Optional) When set, only messages of the specified type are returned. Valid values are `conversation` (messages exchanged between the user and the agent) and `compaction` (summary messages generated when a thread is compacted). When omitted, messages of all types are returned. |

Expand

Show lessSee more

#### Request headers

| Header | Description |
| --- | --- |
| `Authorization` | (Required) Authorization token. |
| `Content-Type` | (Required) application/json |

Expand

Show lessSee more

### Response

Returns a thread metadata object and an array of messages.

| Field | Type | Description |
| --- | --- | --- |
| [metadata](#label-snowflake-threads-rest-api) | object | Metadata for the thread, including the name, application that created the thread, and the time that it was created. |
| `messages` | array | Array of message objects. |

Expand

Show lessSee more

#### metadata

| Field | Type | Description |
| --- | --- | --- |
| `thread_id` | integer | UUID for the thread. |
| `thread_name` | string | Name of the thread. |
| `origin_application` | string | The name of the application that created the thread. |
| `created_on` | integer | Time when the thread was created (milliseconds since UNIX epoch). |
| `updated_on` | integer | Time when the thread was last updated (milliseconds since UNIX epoch). An update includes adding any new messages to the thread. |

Expand

Show lessSee more

#### Messages

| Field | Type | Description |
| --- | --- | --- |
| `message_id` | integer | UUID for the message. |
| `parent_id` | integer | UUID for the parent message. |
| `created_on` | integer | Time when the message was created (milliseconds since UNIX epoch). |
| `role` | string | The role that generated this message. |
| `message_payload` | string | Message payload. |
| `request_id` | string | Request ID for the original message. |
| `message_type` | string | The type of the message. Either `conversation` (a message exchanged between the user and the agent) or `compaction` (a summary message generated when a thread is compacted). |

Expand

Show lessSee more

Example:

Copy code

```
{
  "metadata": {
    "thread_id": 1234567890,
    "thread_name": "Support Chat",
    "origin_application": "my_app",
    "created_on": 1717000000000,
    "updated_on": 1717000100000
  },
  "messages": [
    {
      "message_id": 1,
      "parent_id": null,
      "created_on": 1717000000000,
      "role": "user",
      "message_payload": "Hello, I need help.",
      "request_id": "req_001",
      "message_type": "conversation"
    },
    {
      "message_id": 2,
      "parent_id": 1,
      "created_on": 1717000001000,
      "role": "assistant",
      "message_payload": "How can I assist you?",
      "request_id": "req_002",
      "message_type": "conversation"
    }
  ]
}
```

## Update thread

`POST /api/v2/cortex/threads/{id}`

Updates a thread.

### Request

#### Path parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | integer | (Required) UUID for the thread. |

Expand

Show lessSee more

#### Request headers

| Header | Description |
| --- | --- |
| `Authorization` | (Required) Authorization token. |
| `Content-Type` | (Required) application/json |

Expand

Show lessSee more

#### Request body

| Field | Type | Description |
| --- | --- | --- |
| `thread_name` | string | (Optional) Name of the thread. |

Expand

Show lessSee more

Example:

Copy code

```
{
  "thread_name": "New Thread Name"
}
```

### Response

Returns the status of the thread update.

Copy code

```
{"status": "Thread xxxx successfully updated."}
```

## List threads

`GET /api/v2/cortex/threads`

Lists all threads belonging to the user.

### Request

#### Query parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `origin_application` | string | (Optional) Filter the list of threads by this origin application. Without specifying this field, all threads are returned. |

Expand

Show lessSee more

#### Request headers

| Header | Description |
| --- | --- |
| `Authorization` | (Required) Authorization token. |
| `Content-Type` | (Required) application/json |

Expand

Show lessSee more

### Response

Returns an array of thread metadata objects.

#### Thread metadata

| Field | Type | Description |
| --- | --- | --- |
| `thread_id` | integer | UUID for the thread. |
| `thread_name` | string | Name of the thread. |
| `origin_application` | string | The name of the application that created the thread. |
| `created_on` | integer | Time when the thread was created (milliseconds since UNIX epoch). |
| `updated_on` | integer | Time when the thread was last updated (milliseconds since UNIX epoch). An update includes adding any new messages to the thread. |

Expand

Show lessSee more

Example:

Copy code

```
[
  {
    "thread_id": 1234567890,
    "thread_name": "Support Chat",
    "origin_application": "my_app",
    "created_on": 1717000000000,
    "updated_on": 1717000100000
  }
]
```

## Delete thread

`DELETE /api/v2/cortex/threads/{id}`

Deletes a thread and all the messages in that thread.

### Request

#### Path parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | integer | (Required) UUID for the thread. |

Expand

Show lessSee more

#### Request headers

| Header | Description |
| --- | --- |
| `Authorization` | (Required) Authorization token. |
| `Content-Type` | (Required) application/json |

Expand

Show lessSee more

### Response

Returns a success response if the thread is deleted.

Copy code

```
{
  "success": true
}
```
