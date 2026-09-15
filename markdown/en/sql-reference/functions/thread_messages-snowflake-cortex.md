Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# THREAD\_MESSAGES (SNOWFLAKE.CORTEX)

Returns the messages in a [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents) thread as JSON.

You can use this function to retrieve all messages in a thread after an agent run completes. This is
particularly useful for polling the results of an asynchronous (background) agent run started with
`background: true`.

Note

`SNOWFLAKE.CORTEX.THREAD_MESSAGES` is a utility wrapper around the
[Cortex Agents Threads REST API](/user-guide/snowflake-cortex/cortex-agents-threads-rest-api).

See also:
:   [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex), [AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/agent_run-snowflake-cortex)

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.THREAD_MESSAGES( <thread_id> [, <page_size>, <last_message_id> ] )
```

## Arguments

`thread_id`
:   The ID of the thread to retrieve messages from.

`page_size` (optional)
:   The maximum number of messages to return per page. Use this with `last_message_id` for pagination.

`last_message_id` (optional)
:   The ID of the last message from the previous page. Messages returned will be those after this message ID.
    Use this with `page_size` for pagination.

## Returns

Returns a JSON string containing an array of messages in the thread. Each message includes the role,
content, and message metadata.

## Access control requirements

To retrieve thread messages, you must use a role that can access Cortex Agents.
For details, see [API access roles](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-access-control).

## Usage notes

- The function returns a JSON string. Pass this string to [TRY\_PARSE\_JSON](/sql-reference/functions/try_parse_json) to convert the response to a VARIANT value.
- This function is commonly used to poll the results of an asynchronous agent run initiated with `background: true` in the request body. After kicking off a background run, call `THREAD_MESSAGES` with the thread ID to check whether the assistant response has been written.
- When paginating, provide both `page_size` and `last_message_id`. If you omit both optional arguments, all messages in the thread are returned.

## Examples

Retrieve all messages in a thread:

Copy code

```
SELECT
  TRY_PARSE_JSON(
    SNOWFLAKE.CORTEX.THREAD_MESSAGES(12345)
  ) AS messages;
```

Retrieve messages with pagination:

Copy code

```
SELECT
  TRY_PARSE_JSON(
    SNOWFLAKE.CORTEX.THREAD_MESSAGES(12345, 50, 67890)
  ) AS messages;
```

Use with an asynchronous agent run:

Copy code

```
-- 1) Start an async agent run
SELECT
  TRY_PARSE_JSON(
    SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
      'MY_DB.MY_SCHEMA.MY_AGENT',
      $${
        "messages": [
          {
            "role": "user",
            "content": [
              { "type": "text", "text": "What were the top-selling products last month?" }
            ]
          }
        ],
        "thread_id": 12345,
        "background": true
      }$$
    )
  ) AS resp;

-- 2) Poll thread messages for the assistant response
SELECT
  TRY_PARSE_JSON(
    SNOWFLAKE.CORTEX.THREAD_MESSAGES(12345)
  ) AS messages;
```
