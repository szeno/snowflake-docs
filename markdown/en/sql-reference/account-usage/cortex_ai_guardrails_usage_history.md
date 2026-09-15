Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CORTEX\_AI\_GUARDRAILS\_USAGE\_HISTORY view

The CORTEX\_AI\_GUARDRAILS\_USAGE\_HISTORY view can be used to query the usage history of
[Cortex AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails). The view provides
visibility into guardrail scan activity, credit consumption, and token usage for each request.
Each row in the view represents a single guardrail scan for one tool use within an agent request.
A request with multiple tool results produces multiple rows, one per tool use scanned.

Note

This view captures the signals raised by the prompt injection detection guardrails and sent to the LLM
for adjudication. The LLM uses those signals to determine whether a request may contain a genuine
prompt injection attempt.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| USER\_ID | NUMBER | The unique identifier of the user who made the request. |
| USER\_NAME | VARCHAR | The name of the user who made the request. |
| USER\_TAGS | ARRAY | Tags associated with the user. Each object in the array contains the following fields: `level` (the level at which the tag is applied, for example, `ACCOUNT` or `USER`), `tag_database`, `tag_schema`, `tag_name`, and `tag_value`. |
| REQUEST\_ID | VARCHAR | The unique identifier for the request. |
| PARENT\_REQUEST\_ID | VARCHAR | The identifier of the parent request, if applicable. |
| AGENTIC\_SOURCE | VARCHAR | The Cortex client in which guardrails were invoked. Possible values include `CORTEX_CODE_CLI`, `CORTEX_CODE_DESKTOP`, `CORTEX_CODE_SNOWSIGHT`, `CORTEX_AGENT`, and `SNOWFLAKE_INTELLIGENCE`. |
| USAGE\_TIME | TIMESTAMP\_TZ | The timestamp when the usage was recorded. |
| TOKEN\_CREDITS | NUMBER | The number of token credits consumed for the request. |
| TOKENS | NUMBER | The total number of tokens used for the request. |
| TOKENS\_GRANULAR | OBJECT | Granular breakdown of token usage for the request. Contains the following fields: `input`, `cache_read_input`, `cache_write_input`, and `output`. |
| CREDITS\_GRANULAR | OBJECT | Granular breakdown of credit usage for the request. Contains the following fields: `input`, `cache_read_input`, `cache_write_input`, and `output`. |
| GUARDRAIL\_RESULTS | ARRAY | Guardrail scan results. Each object in the array contains: `tool_use_id`, `tool_type` (for example, `web_search`, `server_mcp`, or `sql_execute`), optional token fields (`input_token`, `output_token`, `cache_read_input_token`, `cache_read_output_token`, `token_count`), and `indirect_prompt_injection` (whether the scan detected a possible prompt injection for this tool use). |
| GUARDRAILS\_SIGNAL | BOOLEAN | Indicates whether any guardrail scan in the request was flagged. |
| METADATA | OBJECT | Metadata associated with the request. Contains `role_id` (the identifier of the role) and `role_name` (the name of the role). |

Expand

Show lessSee more

## Examples

Retrieve the most recent 100 guardrail scan events in the last 72 hours:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_GUARDRAILS_USAGE_HISTORY
  WHERE USAGE_TIME >= DATEADD('hour', -72, CURRENT_TIMESTAMP())
  ORDER BY USAGE_TIME DESC
  LIMIT 100;
```

Retrieve the most recent 100 guardrail scan events where a possible prompt injection was detected:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_GUARDRAILS_USAGE_HISTORY
  WHERE GUARDRAILS_SIGNAL = TRUE
    AND USAGE_TIME >= DATEADD('hour', -72, CURRENT_TIMESTAMP())
  ORDER BY USAGE_TIME DESC
  LIMIT 100;
```

## Usage notes

- Credit usage is based on the number of tokens scanned, as outlined in the
  [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
- For information on configuring Cortex AI Guardrails and monitoring guardrail activity, see
  [Cortex AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails).
