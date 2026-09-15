# Cortex model deprecations for August 2026

The following models enter the **legacy** state on August 12, 2026. Legacy is not the same as
end-of-life. After the legacy date, Snowflake limits which accounts can call the model:

- If your **account** used the model anywhere before August 12, 2026, the account can continue to
  use it in every supported application (including AI\_COMPLETE, CORTEX.COMPLETE, the Agents API,
  Cortex Inference, and Snowflake CoWork) until that model’s end-of-life (EOL) date.
- If your account had not used the model anywhere before August 12, 2026, the account can’t start
  using it. Queries and API calls that name the model fail.

Any usage of the model in the account before the legacy date means that the account can continue
to use it until EOL.

Transition to a replacement model before the EOL date to avoid disruption. For the full
definitions of legacy and end-of-life, see
[Model lifecycle: legacy and end-of-life](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-model-lifecycle).

Note

[Managed functions](/user-guide/snowflake-cortex/aisql#cortex-ai-functions) are not impacted by these model deprecations. Snowflake manages and optimizes inference of the underlying models used by functions such as AI\_CLASSIFY, AI\_FILTER, and AI\_AGG.

| Model | Legacy date | End-of-life date |
| --- | --- | --- |
| claude-4-sonnet | August 12, 2026 | October 14, 2026 |
| openai-gpt-4.1 | August 12, 2026 | October 14, 2026 |
| llama3-70b | August 12, 2026 | No sooner than October 14, 2026 |
| llama3-70b (fine-tuned) | August 12, 2026 | No sooner than October 14, 2026 |
| llama3-8b | August 12, 2026 | No sooner than October 14, 2026 |
| llama3-8b (fine-tuned) | August 12, 2026 | No sooner than October 14, 2026 |
| llama3.1-70b | August 12, 2026 | No sooner than October 14, 2026 |
| llama3.1-70b (fine-tuned) | August 12, 2026 | No sooner than October 14, 2026 |
| llama3.1-8b (fine-tuned) | August 12, 2026 | No sooner than October 14, 2026 |
| llama4-maverick | August 12, 2026 | No sooner than October 14, 2026 |
| mistral-7b | August 12, 2026 | No sooner than October 14, 2026 |
| mistral-7b (fine-tuned) | August 12, 2026 | No sooner than October 14, 2026 |
| mistral-large2 | August 12, 2026 | No sooner than October 14, 2026 |
| mixtral-8x7b | August 12, 2026 | No sooner than October 14, 2026 |
| mixtral-8x7b (fine-tuned) | August 12, 2026 | No sooner than October 14, 2026 |
| pixtral-large | August 12, 2026 | No sooner than October 14, 2026 |

Expand

Show lessSee more

If the named model parameter is not updated, queries or API calls that reference the model fail
after its end-of-life date for every account, including accounts that were allowed to use the
model during the legacy period.

Ref: 2388
